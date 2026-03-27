"""Job status and queue monitoring API endpoints."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path
from flask import Blueprint, current_app, jsonify, request
from typing import Any
from sqlalchemy import or_

from db import AnalysisJob, SessionLocal
from application.analysis.services import cleanup_analysis_job_artifacts
from application.utils.csrf import require_csrf_or_400

logger = logging.getLogger(__name__)

job_api_bp = Blueprint("job_api", __name__)
IGNORED_HEADER_REASONS = {"ERR_STALE_TEST_JOB"}


def _to_recent_job_payload(job: AnalysisJob) -> dict[str, Any]:
    """Normalize ORM instance values for JSON payload typing."""
    job_id = getattr(job, "job_id", None)
    slug = getattr(job, "slug", None)
    sku = getattr(job, "sku", None)
    provider = getattr(job, "provider", None)
    status = getattr(job, "status", None)
    stage = getattr(job, "stage", None)
    progress = getattr(job, "progress", None)
    reason = getattr(job, "reason", None)
    error_message = getattr(job, "error_message", None)
    finished_at = getattr(job, "finished_at", None)

    message = error_message[:100] if isinstance(error_message, str) else None
    finished_at_iso = finished_at.isoformat() if isinstance(finished_at, datetime) else None

    slug_text = slug if isinstance(slug, str) else ""

    return {
        "job_id": job_id if isinstance(job_id, str) else "",
        "slug": slug_text,
        "sku": sku if isinstance(sku, str) and sku else slug_text,
        "provider": provider if isinstance(provider, str) else "",
        "status": status if isinstance(status, str) else "",
        "stage": stage if isinstance(stage, str) else "",
        "progress": progress if isinstance(progress, int) else 0,
        "reason": reason if isinstance(reason, str) else None,
        "message": message,
        "finished_at": finished_at_iso,
    }


def _to_admin_job_payload(job: AnalysisJob) -> dict[str, Any]:
    created_at = getattr(job, "created_at", None)
    updated_at = getattr(job, "updated_at", None)
    started_at = getattr(job, "started_at", None)
    finished_at = getattr(job, "finished_at", None)
    attempts = getattr(job, "attempts", None)

    payload = _to_recent_job_payload(job)
    payload["attempts"] = attempts if isinstance(attempts, int) else 0
    payload["created_at"] = created_at.isoformat() if isinstance(created_at, datetime) else None
    payload["updated_at"] = updated_at.isoformat() if isinstance(updated_at, datetime) else None
    payload["started_at"] = started_at.isoformat() if isinstance(started_at, datetime) else None
    payload["finished_at"] = finished_at.isoformat() if isinstance(finished_at, datetime) else None
    payload["error_message"] = getattr(job, "error_message", None)
    return payload


def _lab_roots() -> list[Path]:
    cfg = current_app.config
    roots = []
    for key in ("LAB_PROCESSED_DIR", "LAB_UNPROCESSED_DIR", "LAB_LOCKED_DIR"):
        value = cfg.get(key)
        if value:
            roots.append(Path(str(value)))
    return roots


@job_api_bp.get("/jobs/summary")
def job_summary():
    """Get job counts for header notification.
    
    Returns:
        {
            "queued": int,
            "running": int,
            "done_recent": int (last 5 minutes),
            "failed_recent": int (last 5 minutes)
        }
    """
    session = SessionLocal()
    try:
        # Count jobs by status
        queued = session.query(AnalysisJob).filter(AnalysisJob.status == "QUEUED").count()
        running = session.query(AnalysisJob).filter(AnalysisJob.status == "RUNNING").count()
        
        # Count recent completions (last 5 minutes)
        recent_cutoff = datetime.utcnow() - timedelta(minutes=5)
        
        done_recent = (
            session.query(AnalysisJob)
            .filter(
                AnalysisJob.status == "DONE",
                AnalysisJob.finished_at >= recent_cutoff,
                or_(AnalysisJob.reason.is_(None), ~AnalysisJob.reason.in_(IGNORED_HEADER_REASONS)),
            )
            .count()
        )
        
        failed_recent = (
            session.query(AnalysisJob)
            .filter(
                AnalysisJob.status == "FAILED",
                AnalysisJob.finished_at >= recent_cutoff,
                or_(AnalysisJob.reason.is_(None), ~AnalysisJob.reason.in_(IGNORED_HEADER_REASONS)),
            )
            .count()
        )
        
        return jsonify({
            "queued": queued,
            "running": running,
            "done_recent": done_recent,
            "failed_recent": failed_recent,
            "total_active": queued + running,
        })
    
    finally:
        session.close()


@job_api_bp.get("/jobs/recent")
def recent_jobs():
    """Get recent completed/failed jobs for header dropdown.
    
    Returns:
        {
            "jobs": [
                {
                    "job_id": str,
                    "slug": str,
                    "sku": str,
                    "provider": str,
                    "status": str,
                    "stage": str,
                    "progress": int,
                    "reason": str | null,
                    "message": str | null,
                    "finished_at": str (ISO),
                },
                ...
            ]
        }
    """
    session = SessionLocal()
    try:
        # Get recent DONE/FAILED jobs (last 30 minutes, max 20)
        recent_cutoff = datetime.utcnow() - timedelta(minutes=30)
        
        jobs = (
            session.query(AnalysisJob)
            .filter(
                AnalysisJob.status.in_(["DONE", "FAILED"]),
                AnalysisJob.finished_at >= recent_cutoff,
                or_(AnalysisJob.reason.is_(None), ~AnalysisJob.reason.in_(IGNORED_HEADER_REASONS)),
            )
            .order_by(AnalysisJob.finished_at.desc())
            .limit(20)
            .all()
        )
        
        return jsonify({
            "jobs": [_to_recent_job_payload(job) for job in jobs]
        })
    
    finally:
        session.close()


@job_api_bp.get("/jobs/<job_id>")
def job_detail(job_id: str):
    """Get detailed status of a specific job.
    
    Returns:
        {
            "job_id": str,
            "slug": str,
            "sku": str,
            "provider": str,
            "status": str,
            "stage": str,
            "progress": int,
            "attempts": int,
            "reason": str | null,
            "error_message": str | null,
            "created_at": str,
            "started_at": str | null,
            "finished_at": str | null,
        }
    """
    session = SessionLocal()
    try:
        job = session.query(AnalysisJob).filter(AnalysisJob.job_id == job_id).first()
        
        if not job:
            return jsonify({"error": "Job not found"}), 404
        
        job_id_value = getattr(job, "job_id", None)
        slug_value = getattr(job, "slug", None)
        sku_value = getattr(job, "sku", None)
        provider_value = getattr(job, "provider", None)
        status_value = getattr(job, "status", None)
        stage_value = getattr(job, "stage", None)
        progress_value = getattr(job, "progress", None)
        attempts_value = getattr(job, "attempts", None)
        reason_value = getattr(job, "reason", None)
        error_message_value = getattr(job, "error_message", None)
        created_at_value = getattr(job, "created_at", None)
        started_at_value = getattr(job, "started_at", None)
        finished_at_value = getattr(job, "finished_at", None)

        slug_text = slug_value if isinstance(slug_value, str) else ""

        return jsonify({
            "job_id": job_id_value if isinstance(job_id_value, str) else "",
            "slug": slug_text,
            "sku": sku_value if isinstance(sku_value, str) and sku_value else slug_text,
            "provider": provider_value if isinstance(provider_value, str) else "",
            "status": status_value if isinstance(status_value, str) else "",
            "stage": stage_value if isinstance(stage_value, str) else "",
            "progress": progress_value if isinstance(progress_value, int) else 0,
            "attempts": attempts_value if isinstance(attempts_value, int) else 0,
            "reason": reason_value if isinstance(reason_value, str) else None,
            "error_message": error_message_value if isinstance(error_message_value, str) else None,
            "created_at": created_at_value.isoformat() if isinstance(created_at_value, datetime) else None,
            "started_at": started_at_value.isoformat() if isinstance(started_at_value, datetime) else None,
            "finished_at": finished_at_value.isoformat() if isinstance(finished_at_value, datetime) else None,
        })
    
    finally:
        session.close()


@job_api_bp.get("/jobs/admin/list")
def admin_jobs_list():
    """List jobs for the admin jobs console."""
    raw_limit = str(request.args.get("limit") or "150").strip()
    try:
        limit = int(raw_limit)
    except Exception:
        limit = 150
    limit = max(1, min(limit, 500))

    status_filter = str(request.args.get("status") or "").strip().upper()

    session = SessionLocal()
    try:
        query = session.query(AnalysisJob)
        if status_filter:
            query = query.filter(AnalysisJob.status == status_filter)

        jobs = query.order_by(AnalysisJob.created_at.desc()).limit(limit).all()
        return jsonify({"jobs": [_to_admin_job_payload(job) for job in jobs], "count": len(jobs)})
    finally:
        session.close()


@job_api_bp.post("/jobs/<job_id>/cancel")
def cancel_job(job_id: str):
    """Cancel a job and clean up generated files/records."""
    ok, resp = require_csrf_or_400(request)
    if not ok and resp is not None:
        return resp
    if not ok:
        return jsonify({"ok": False, "error": "missing or invalid csrf token"}), 400

    body = request.get_json(silent=True) if request.is_json else None
    if not isinstance(body, dict):
        body = {}

    cleanup_enabled = bool(body.get("cleanup", True))
    remove_artwork_record = bool(body.get("remove_artwork_record", True))

    session = SessionLocal()
    try:
        job = session.query(AnalysisJob).filter(AnalysisJob.job_id == job_id).first()
        if not job:
            return jsonify({"ok": False, "error": "Job not found"}), 404

        slug = str(getattr(job, "slug", "") or "").strip()
        sku_raw = getattr(job, "sku", None)
        sku = str(sku_raw).strip() if isinstance(sku_raw, str) and str(sku_raw).strip() else None
        status = str(getattr(job, "status", "") or "").strip().upper()

        cleanup = {
            "slug": slug,
            "deleted_files": [],
            "touched_dirs": [],
            "manifest_updates": 0,
            "artwork_rows_deleted": 0,
        }
        if cleanup_enabled and slug:
            cleanup = cleanup_analysis_job_artifacts(
                slug=slug,
                sku=sku,
                lab_roots=_lab_roots(),
                remove_artwork_record=remove_artwork_record,
            )

        # Running jobs are switched to a cancellation marker so the worker can stop gracefully.
        if status == "RUNNING":
            job.status = "CANCEL_REQUESTED"  # type: ignore[misc]
            job.reason = "ERR_CANCELLED"  # type: ignore[misc]
            job.error_message = "Cancelled by admin"  # type: ignore[misc]
            job.updated_at = datetime.utcnow()  # type: ignore[misc]
            session.commit()
            return jsonify(
                {
                    "ok": True,
                    "pending": True,
                    "message": "Cancellation requested. Worker will stop this job shortly.",
                    "job_id": job_id,
                    "cleanup": cleanup,
                }
            )

        session.delete(job)
        session.commit()
        return jsonify(
            {
                "ok": True,
                "pending": False,
                "message": "Job cancelled and deleted.",
                "job_id": job_id,
                "cleanup": cleanup,
            }
        )

    except Exception:
        logger.exception("Failed cancelling job %s", job_id)
        session.rollback()
        return jsonify({"ok": False, "error": "Failed to cancel job"}), 500
    finally:
        session.close()
