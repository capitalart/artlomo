from __future__ import annotations

import json
import logging
import shutil
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Blueprint, Flask, current_app, jsonify, request

from application.artwork.errors import ArtworkProcessingError, IndexValidationError, RequiredAssetMissingError
from application.artwork.services.processing_service import ProcessingService
from application.artwork.services.index_service import ArtworksIndex
from application.common.utilities.files import write_json_atomic
from application.common.utilities.slug_sku import is_safe_slug
from application.upload.services import storage_service
from application.utils.csrf import require_csrf_or_400

from application.analysis.openai import OpenAIAnalysisError, run_openai_analysis_for_slug
from application.analysis.gemini import GeminiAnalysisError, run_gemini_analysis_for_slug
from application.analysis.services import AnalysisPresetService
from application.analysis.services.response_contract import validate_analysis_response
from application.common.utilities.files import ensure_dir
from application.utils.artwork_db import update_artwork_status

from application.logging_config import get_ai_logger

logger = logging.getLogger(__name__)


def _ai_logger() -> logging.Logger:
    return get_ai_logger()

analysis_api_bp = Blueprint("analysis_api", __name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _processed_root() -> Path:
    cfg = current_app.config
    return Path(cfg["LAB_PROCESSED_DIR"])


def _locked_root() -> Path:
    cfg = current_app.config
    return Path(cfg["LAB_LOCKED_DIR"])


def _unprocessed_root() -> Path:
    cfg = current_app.config
    return Path(cfg["LAB_UNPROCESSED_DIR"])


def _processing_service() -> ProcessingService:
    cfg = current_app.config
    return ProcessingService(
        unprocessed_root=Path(cfg["LAB_UNPROCESSED_DIR"]),
        processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
        artworks_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
    )


def _artworks_index() -> ArtworksIndex:
    cfg = current_app.config
    return ArtworksIndex(Path(cfg["ARTWORKS_INDEX_PATH"]), _processed_root())


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_manifest(artwork_dir: Path, slug: str) -> dict[str, Any]:
    candidates = sorted(artwork_dir.glob("*-assets.json"))
    if candidates:
        return _load_json(candidates[0])
    return _load_json(artwork_dir / f"{slug}-assets.json")


def _manifest_path(artwork_dir: Path, slug: str) -> Path:
    candidates = sorted(artwork_dir.glob("*-assets.json"))
    if candidates:
        return candidates[0]
    return artwork_dir / f"{slug}-assets.json"


def _set_manifest_analysis_queued(*, artwork_dir: Path, slug: str, provider: str, job_id: str) -> None:
    manifest = _load_manifest(artwork_dir, slug)
    manifest.setdefault("files", {})
    manifest.setdefault("analysis", {})
    now = _now_iso()
    manifest["analysis"].update(
        {
            "status": "queued",
            "stage": "stage1_image",
            "progress": 0,
            "provider": provider,
            "job_id": job_id,
            "queued_at": now,
            "updated_at": now,
        }
    )
    write_json_atomic(_manifest_path(artwork_dir, slug), manifest)


def _resolve_sku_for_slug(slug: str, artwork_dir: Path | None = None) -> str:
    base_dir = artwork_dir or (_processed_root() / slug)
    meta = storage_service.load_metadata_with_fallback(base_dir) or {}
    return str(meta.get("sku") or meta.get("artwork_id") or slug).strip() or slug


def _append_analysis_failure_log(
    *,
    slug: str,
    sku: str,
    source: str,
    stage_before: str,
    stage_after: str,
    reason: str,
    error_code: str,
) -> None:
    cfg = current_app.config
    logs_dir = Path(cfg.get("LOGS_DIR") or "/srv/artlomo/logs")
    ensure_dir(logs_dir)
    log_path = logs_dir / "artwork-analysis-errors.log"
    line = (
        f"{_now_iso()}"
        f"\tsku={sku}"
        f"\tslug={slug}"
        f"\tsource={source}"
        f"\tstage_before={stage_before}"
        f"\tstage_after={stage_after}"
        f"\terror_code={error_code}"
        f"\treason={reason}\n"
    )
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(line)


def _update_listing_status(
    *,
    slug: str,
    stage: str,
    message: str,
    done: bool,
    source: str,
    error: str | None = None,
    error_code: str | None = None,
    root_dir: Path | None = None,
) -> None:
    processed_dir = (root_dir or _processed_root()) / slug
    
    # Try to load existing listing, or create from metadata SKU
    listing: dict[str, Any] = {}
    meta = storage_service.load_metadata_with_fallback(processed_dir)
    if not meta:
        meta = {"sku": slug, "artwork_id": slug}
    sku = str(meta.get("sku") or meta.get("artwork_id") or slug).strip() or slug
    
    # Try SKU-prefixed listing first, then fallback to non-prefixed
    listing_path = processed_dir / f"{sku.lower()}-listing.json"
    if not listing_path.exists():
        listing_path = processed_dir / "listing.json"
    
    listing = _load_json(listing_path)
    if not listing:
        listing = {
            "slug": slug,
            "sku": sku,
            "analysis_source": source,
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
        }

    listing.setdefault("slug", slug)
    listing.setdefault("sku", sku)
    listing["analysis_source"] = source
    listing["analysis_status"] = {
        "stage": stage,
        "message": message,
        "done": bool(done),
        "error": error,
        "error_code": error_code,
        "source": source,
        "updated_at": _now_iso(),
    }
    listing["updated_at"] = _now_iso()
    
    # Write with SKU prefix
    sku_prefixed_listing_path = processed_dir / f"{sku.lower()}-listing.json"
    write_json_atomic(sku_prefixed_listing_path, listing)

    status_path = processed_dir / f"{sku.lower()}-status.json"
    status_payload = {
        "status": "error" if stage == "error" else "ok",
        "slug": slug,
        "sku": sku,
        "stage": stage,
        "message": message,
        "done": bool(done),
        "error": error,
        "error_code": error_code,
        "source": source,
        "updated_at": _now_iso(),
    }
    try:
        write_json_atomic(status_path, status_payload)
    except Exception:
        _ai_logger().exception("Failed to write status.json (slug=%s)", slug)


def _rollback_failed_analysis(*, slug: str, source: str, reason: str, error_code: str) -> None:
    processed_dir = _processed_root() / slug
    unprocessed_dir = _unprocessed_root() / slug

    stage_before = "processed" if processed_dir.exists() else "unknown"
    stage_after = "unprocessed"

    sku = _resolve_sku_for_slug(slug, processed_dir if processed_dir.exists() else None)

    if processed_dir.exists():
        if unprocessed_dir.exists():
            shutil.rmtree(unprocessed_dir, ignore_errors=True)
        processed_dir.replace(unprocessed_dir)

    sku = _resolve_sku_for_slug(slug, unprocessed_dir if unprocessed_dir.exists() else processed_dir)

    assets_name = f"{slug}-assets.json"
    if unprocessed_dir.exists():
        candidates = sorted(unprocessed_dir.glob("*-assets.json"))
        if candidates:
            assets_name = candidates[0].name

    try:
        _artworks_index().upsert(
            sku=sku,
            slug=slug,
            artwork_dirname=slug,
            assets_file=assets_name,
            stage="unprocessed",
        )
    except Exception:
        _ai_logger().exception("Failed to upsert artworks index for failed analysis rollback (slug=%s)", slug)

    try:
        update_artwork_status(sku, "unprocessed")
    except Exception:
        _ai_logger().warning("Failed to update DB status to unprocessed for failed analysis (slug=%s)", slug)

    try:
        _update_listing_status(
            slug=slug,
            stage="failed",
            message="FAILED ANALYSIS",
            done=True,
            source=source,
            error=reason,
            error_code=error_code,
            root_dir=_unprocessed_root(),
        )
    except Exception:
        _ai_logger().exception("Failed to persist failed analysis status (slug=%s)", slug)

    try:
        _append_analysis_failure_log(
            slug=slug,
            sku=sku,
            source=source,
            stage_before=stage_before,
            stage_after=stage_after,
            reason=reason,
            error_code=error_code,
        )
    except Exception:
        _ai_logger().exception("Failed to append analysis failure log (slug=%s)", slug)


def _promote_to_processed(slug: str) -> None:
    if (_locked_root() / slug).exists():
        raise ArtworkProcessingError("Artwork is locked and cannot be analysed.")

    processed_dir = _processed_root() / slug
    if processed_dir.exists():
        return

    svc = _processing_service()
    try:
        svc.process(slug)
    except IndexValidationError:
        # Already processed or invalid; let analysis continue without duplication
        return


def _openai_worker(app: Flask, slug: str) -> None:
    with app.app_context():
        _ai_logger()
        try:
            _promote_to_processed(slug)
            _update_listing_status(
                slug=slug,
                stage="processing",
                message="Running OpenAI analysis",
                done=False,
                source="openai",
            )
            result = run_openai_analysis_for_slug(slug=slug, processed_root=_processed_root())
            contract = validate_analysis_response(result)
            if not contract.ok:
                exc = OpenAIAnalysisError(contract.reason or "Analysis response failed contract validation")
                setattr(exc, "error_code", "ERR_CONTRACT")
                raise exc
            _update_listing_status(
                slug=slug,
                stage="complete",
                message="OpenAI analysis complete",
                done=True,
                source="openai",
            )
        except Exception as exc:  # pylint: disable=broad-except
            _ai_logger().exception("OpenAI analysis worker crashed (slug=%s)", slug)
            err_code = getattr(exc, "error_code", None) or "ERR_UNKNOWN"
            err_detail = str(exc)
            try:
                _rollback_failed_analysis(slug=slug, source="openai", reason=err_detail, error_code=err_code)
            except Exception:
                _ai_logger().exception("Failed to persist OpenAI error status (slug=%s)", slug)
                return


def _gemini_worker(app: Flask, slug: str) -> None:
    with app.app_context():
        _ai_logger()
        try:
            _promote_to_processed(slug)
            _update_listing_status(
                slug=slug,
                stage="processing",
                message="Running Gemini analysis",
                done=False,
                source="gemini",
            )
            result = run_gemini_analysis_for_slug(slug=slug, processed_root=_processed_root())
            contract = validate_analysis_response(result)
            if not contract.ok:
                raise GeminiAnalysisError(contract.reason or "Analysis response failed contract validation", error_code="ERR_CONTRACT")
            _update_listing_status(
                slug=slug,
                stage="complete",
                message="Gemini analysis complete",
                done=True,
                source="gemini",
            )
        except Exception as exc:  # pylint: disable=broad-except
            _ai_logger().exception("Gemini analysis worker crashed (slug=%s)", slug)
            err_code = getattr(exc, "error_code", None) or "ERR_UNKNOWN"
            err_detail = getattr(exc, "error_detail", None) or str(exc)
            
            # Build user-friendly error message
            error_messages = {
                "ERR_AUTH": "Invalid or missing Gemini API key",
                "ERR_RATE_LIMIT": "Rate limit exceeded - try again later",
                "ERR_BALANCE": "API quota exhausted - check billing",
                "ERR_TIMEOUT": "Request timed out - try again",
                "ERR_MODEL": "Model not available - check configuration",
                "ERR_PARSE": "Failed to parse Gemini response",
                "ERR_BAD_REQUEST": "Invalid request to Gemini API",
            }
            user_message = error_messages.get(err_code, f"Gemini analysis failed: {err_detail}")
            
            try:
                _rollback_failed_analysis(slug=slug, source="gemini", reason=user_message, error_code=err_code)
            except Exception:
                _ai_logger().exception("Failed to persist Gemini error status (slug=%s)", slug)
                return


@analysis_api_bp.get("/analysis/status/<slug>")
def status(slug: str):
    slug_clean = str(slug or "").strip()
    if not slug_clean:
        return jsonify({"stage": "invalid", "message": "Missing slug", "done": True, "error": "invalid slug"}), 400

    # Look up the artwork by slug directly
    artwork_dir = _processed_root() / slug_clean
    stage_hint = "processed"
    if not artwork_dir.exists():
        fallback_dir = _unprocessed_root() / slug_clean
        if fallback_dir.exists():
            artwork_dir = fallback_dir
            stage_hint = "unprocessed"
        else:
            return jsonify({"stage": "not_found", "message": "Listing not found", "done": False, "error": None}), 404

    # Load metadata to get SKU - try SKU-prefixed first, then fallback to non-prefixed
    meta_path_prefixed = artwork_dir / f"{slug_clean.lower()}-{storage_service.META_NAME}"
    meta_path = artwork_dir / storage_service.META_NAME
    meta = _load_json(meta_path_prefixed if meta_path_prefixed.exists() else meta_path)
    sku = str(meta.get("sku") or meta.get("artwork_id") or slug_clean).strip() or slug_clean

    # Prefer manifest.analysis (source of truth for queue/worker progress)
    manifest = _load_manifest(artwork_dir, slug_clean)
    manifest_analysis = manifest.get("analysis") if isinstance(manifest, dict) else None
    if isinstance(manifest_analysis, dict):
        analysis_status = str(manifest_analysis.get("status") or "").strip().lower()
        stage_value = manifest_analysis.get("stage") or "unknown"
        message_value = manifest_analysis.get("message")
        source_value = manifest_analysis.get("provider")
        updated_at_value = manifest_analysis.get("updated_at")
        reason_value = manifest_analysis.get("reason")
        done_value = analysis_status in {"success", "failed", "needs_review"}
        error_value = message_value if analysis_status == "failed" else None
        derived_status = "error" if analysis_status == "failed" else ("warning" if analysis_status == "needs_review" else "ok")

        return jsonify(
            {
                "status": derived_status,
                "sku": sku,
                "slug": slug_clean,
                "stage_root": stage_hint,
                "stage": stage_value,
                "message": message_value,
                "done": done_value,
                "error": error_value,
                "reason": reason_value,
                "source": source_value,
                "updated_at": updated_at_value,
            }
        )
    
    # Legacy fallback: listing analysis_status
    listing_path = artwork_dir / f"{sku.lower()}-listing.json"
    if not listing_path.exists():
        listing_path = artwork_dir / "listing.json"
    
    if not listing_path.exists():
        return jsonify({"stage": "not_found", "message": "Listing not found", "done": False, "error": None}), 404

    listing = _load_json(listing_path)
    status_payload = listing.get("analysis_status") if isinstance(listing, dict) else None
    if not isinstance(status_payload, dict):
        status_payload = {"stage": "unknown", "message": "No analysis status available", "done": False, "error": None}

    derived_status = "error" if (status_payload.get("stage") == "error" or status_payload.get("error")) else "ok"

    return jsonify(
        {
            "status": derived_status,
            "sku": listing.get("sku") if isinstance(listing, dict) else slug_clean,
            "slug": slug_clean,
            "stage_root": stage_hint,
            "stage": status_payload.get("stage"),
            "message": status_payload.get("message"),
            "done": bool(status_payload.get("done")),
            "error": status_payload.get("error"),
            "source": status_payload.get("source") or listing.get("analysis_source"),
            "updated_at": status_payload.get("updated_at") or listing.get("updated_at"),
        }
    )


@analysis_api_bp.post("/analysis/openai/<slug>")  # type: ignore[misc]
def trigger_openai(slug: str):
    """Enqueue OpenAI analysis job (no longer runs in-process thread)."""
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    slug_clean = str(slug or "").strip()
    if not slug_clean or not is_safe_slug(slug_clean):
        return jsonify({"status": "error", "message": "Invalid slug"}), 404

    try:
        _promote_to_processed(slug_clean)
    except (RequiredAssetMissingError, ArtworkProcessingError) as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400

    # Resolve SKU via metadata
    meta = storage_service.load_metadata_with_fallback((_processed_root() / slug_clean))
    sku = str((meta or {}).get("sku") or (meta or {}).get("artwork_id") or slug_clean).strip() or slug_clean

    # Create AnalysisJob record (enqueue)
    from db import AnalysisJob, SessionLocal
    import uuid
    
    job_id = str(uuid.uuid4())
    session = SessionLocal()
    try:
        job = AnalysisJob(
            job_id=job_id,
            slug=slug_clean,
            sku=sku,
            provider="openai",
            status="QUEUED",
            stage="stage1_image",
            progress=0,
            attempts=0,
        )
        session.add(job)
        session.commit()
        logger.info(f"Enqueued OpenAI analysis job {job_id} for slug={slug_clean}, sku={sku}")
    except Exception as exc:
        logger.exception(f"Failed to enqueue OpenAI job for {slug_clean}")
        session.rollback()
        return jsonify({"status": "error", "message": "Failed to enqueue job"}), 500
    finally:
        session.close()

    # Update listing status (legacy file-based tracking)
    try:
        _update_listing_status(
            slug=slug_clean,
            stage="queued",
            message="OpenAI analysis queued",
            done=False,
            source="openai",
        )
    except Exception as exc:
        logger.warning(f"Failed to update listing status for {slug_clean}: {exc}")

    # Update manifest queue status (canonical stage tracking)
    try:
        _set_manifest_analysis_queued(
            artwork_dir=_processed_root() / slug_clean,
            slug=slug_clean,
            provider="openai",
            job_id=job_id,
        )
    except Exception as exc:
        logger.warning(f"Failed to update manifest queued status for {slug_clean}: {exc}")

    return jsonify({"status": "ok", "slug": slug_clean, "sku": sku, "job_id": job_id})


@analysis_api_bp.post("/analysis/gemini/<slug>")  # type: ignore[misc]
def trigger_gemini(slug: str):
    """Enqueue Gemini analysis job (no longer runs in-process thread)."""
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    slug_clean = str(slug or "").strip()
    if not slug_clean or not is_safe_slug(slug_clean):
        return jsonify({"status": "error", "message": "Invalid slug"}), 404

    try:
        _promote_to_processed(slug_clean)
    except (RequiredAssetMissingError, ArtworkProcessingError) as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400

    # Resolve SKU via metadata
    meta = storage_service.load_metadata_with_fallback((_processed_root() / slug_clean))
    sku = str((meta or {}).get("sku") or (meta or {}).get("artwork_id") or slug_clean).strip() or slug_clean

    # Create AnalysisJob record (enqueue)
    from db import AnalysisJob, SessionLocal
    import uuid
    
    job_id = str(uuid.uuid4())
    session = SessionLocal()
    try:
        job = AnalysisJob(
            job_id=job_id,
            slug=slug_clean,
            sku=sku,
            provider="gemini",
            status="QUEUED",
            stage="stage1_image",
            progress=0,
            attempts=0,
        )
        session.add(job)
        session.commit()
        logger.info(f"Enqueued Gemini analysis job {job_id} for slug={slug_clean}, sku={sku}")
    except Exception as exc:
        logger.exception(f"Failed to enqueue Gemini job for {slug_clean}")
        session.rollback()
        return jsonify({"status": "error", "message": "Failed to enqueue job"}), 500
    finally:
        session.close()

    # Update listing status (legacy file-based tracking)
    try:
        _update_listing_status(
            slug=slug_clean,
            stage="queued",
            message="Gemini analysis queued",
            done=False,
            source="gemini",
        )
    except Exception as exc:
        logger.warning(f"Failed to update listing status for {slug_clean}: {exc}")

    # Update manifest queue status (canonical stage tracking)
    try:
        _set_manifest_analysis_queued(
            artwork_dir=_processed_root() / slug_clean,
            slug=slug_clean,
            provider="gemini",
            job_id=job_id,
        )
    except Exception as exc:
        logger.warning(f"Failed to update manifest queued status for {slug_clean}: {exc}")

    return jsonify({"status": "ok", "slug": slug_clean, "sku": sku, "job_id": job_id})
