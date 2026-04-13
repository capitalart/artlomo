"""DB-backed analysis job queue worker.

This worker polls the AnalysisJob table for QUEUED jobs and processes them
sequentially. Stage 2 implements REAL AI execution for Stage 1 image analysis.

Run as: python -m application.analysis.worker.analysis_worker
"""

from __future__ import annotations

import json
import logging
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db import AnalysisJob, SessionLocal
from application.config import get_config
from application.artwork.services.index_service import ArtworksIndex
from application.common.utilities.files import write_json_atomic
from application.analysis.openai import OpenAIAnalysisError, run_openai_analysis_for_slug
from application.analysis.gemini import GeminiAnalysisError, run_gemini_analysis_for_slug
from application.analysis.services import cleanup_analysis_job_artifacts

logger = logging.getLogger(__name__)

_FAIL_MARKERS = ("STATUS: FAILED", "STATUS=FAILED", "ANALYSIS_FAILED")


class JobCancelledError(RuntimeError):
    """Raised when an admin requests cancellation for a running job."""


def _is_cancel_requested(job_id: str) -> bool:
    if not job_id:
        return False
    with SessionLocal() as probe_session:
        row = probe_session.query(AnalysisJob).filter(AnalysisJob.job_id == job_id).first()
        if row is None:
            return True
        status = str(getattr(row, "status", "") or "").strip().upper()
        return status in {"CANCEL_REQUESTED", "CANCELLED"}


def _abort_if_cancel_requested(job_id: str) -> None:
    if _is_cancel_requested(job_id):
        raise JobCancelledError("ERR_CANCELLED: Job cancelled by admin")


def _job_str(job: AnalysisJob, field: str, default: str = "") -> str:
    value = getattr(job, field, None)
    return value if isinstance(value, str) else default


def _job_int(job: AnalysisJob, field: str, default: int = 0) -> int:
    value = getattr(job, field, None)
    return value if isinstance(value, int) else default


def _cfg_bool(cfg: Any, name: str, default: bool) -> bool:
    raw = getattr(cfg, name, default)
    if isinstance(raw, bool):
        return raw
    txt = str(raw or "").strip().lower()
    if txt in {"1", "true", "yes", "on"}:
        return True
    if txt in {"0", "false", "no", "off", ""}:
        return False
    return bool(default)


def _now_iso() -> str:
    """ISO 8601 timestamp in UTC."""
    return datetime.now(timezone.utc).isoformat()


def _find_manifest_path(artwork_dir: Path, slug: str) -> Path:
    candidates = sorted(artwork_dir.glob("*-assets.json"))
    if candidates:
        return candidates[0]
    return artwork_dir / f"{slug}-assets.json"


def _load_manifest(artwork_dir: Path, slug: str) -> dict:
    """Load artwork assets manifest."""
    manifest_path = _find_manifest_path(artwork_dir, slug)
    
    if manifest_path.exists():
        import json
        try:
            return json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _update_manifest_analysis(
    artwork_dir: Path,
    slug: str,
    *,
    status: str,
    stage: str,
    progress: int,
    provider: str,
    job_id: str,
    attempts: int = 0,
    reason: str | None = None,
    message: str | None = None,
) -> None:
    """Update artwork manifest with analysis tracking block."""
    manifest = _load_manifest(artwork_dir, slug)
    
    now = _now_iso()
    manifest.setdefault("analysis", {})
    analysis = manifest["analysis"]
    
    analysis["status"] = status
    analysis["stage"] = stage
    analysis["progress"] = progress
    analysis["provider"] = provider
    analysis["job_id"] = job_id
    analysis["attempts"] = attempts
    analysis["updated_at"] = now
    
    if reason:
        analysis["reason"] = reason
    if message:
        analysis["message"] = message
    
    if status == "running" and "started_at" not in analysis:
        analysis["started_at"] = now
    elif status in ("success", "failed", "needs_review"):
        analysis["finished_at"] = now
    
    manifest_path = _find_manifest_path(artwork_dir, slug)
    write_json_atomic(manifest_path, manifest)


def _split_terms(value: Any) -> list[str]:
    if isinstance(value, list):
        out = [str(v).strip() for v in value if str(v).strip()]
        return out
    if not isinstance(value, str):
        return []
    cleaned = re.sub(r"[\n|;/]+", ",", value)
    return [chunk.strip() for chunk in cleaned.split(",") if chunk.strip()]


def _contains_failure_marker(value: Any) -> bool:
    text = str(value or "").strip().upper()
    if not text:
        return False
    return any(marker in text for marker in _FAIL_MARKERS)


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _ensure_printing_options_block(description: str) -> str:
    base = str(description or "").strip()
    marker = "🖨️ Professional Printing Options for My Artwork"
    if marker.lower() in base.lower():
        return base

    block = (
        "🖨️ Professional Printing Options for My Artwork\n\n"
        "Many collectors enjoy downloading my artwork and choosing where to print. "
        "Here are trusted print-on-demand services for high-quality wall art:\n\n"
        "🌍 Gelato\n"
        "Global network, fast international fulfilment, and reliable posters, framed prints, and canvas options.\n\n"
        "🖼️ Printful\n"
        "Consistent premium quality with museum-grade posters, plus framed, canvas, and metal print options.\n\n"
        "💰 Printify\n"
        "Strong value pricing, wide print partner choice, and a good quality-to-affordability balance.\n\n"
        "🎨 Prodigi\n"
        "Premium fine-art output with museum-grade paper and gallery-style framing choices.\n\n"
        "📦 Gooten\n"
        "Reliable global fulfilment with broad wall art product support."
    )

    if not base:
        return block

    separator = "\n\n---\n\n" if "---" in base else "\n\n"
    return f"{base}{separator}{block}".strip()


def _extract_stage1_payload(*, slug: str, result: dict[str, Any]) -> dict[str, Any]:
    listing = _as_dict(result.get("listing"))
    metadata = _as_dict(result.get("metadata"))
    analysis = _as_dict(metadata.get("analysis"))
    visual = _as_dict(analysis.get("visual_analysis"))
    if not visual:
        visual = _as_dict(listing.get("visual_analysis"))

    subject = str(visual.get("subject") or "").strip()
    style = str(visual.get("dot_rhythm") or "").strip()
    lighting = str(visual.get("mood") or "").strip()

    palette = _split_terms(visual.get("palette"))
    if not palette:
        palette = [
            val
            for val in [
                str(listing.get("primary_colour") or "").strip(),
                str(listing.get("secondary_colour") or "").strip(),
            ]
            if val
        ]

    tags = _as_list(listing.get("tags"))
    keywords = [str(tag).strip() for tag in tags if str(tag).strip()]

    location_guess = str(metadata.get("original_filename") or "").strip()
    if not location_guess:
        location_guess = slug.replace("-", " ").title()

    return {
        "subject": subject,
        "palette": palette,
        "lighting": lighting,
        "location_guess": location_guess,
        "style": style,
        "keywords": keywords,
    }


def _validate_stage1_payload(payload: Any) -> tuple[bool, str | None, str | None]:
    if not isinstance(payload, dict):
        return False, "ERR_STAGE1_PARSE", "Stage 1 output is not a JSON object"

    status = str(payload.get("STATUS") or "").strip().upper()
    if status == "FAILED":
        reason = str(payload.get("REASON") or "ERR_AI_FAILED").strip() or "ERR_AI_FAILED"
        message = str(payload.get("MESSAGE") or "AI reported structured stage1 failure").strip()
        return False, reason, message

    required_str = ("subject", "lighting", "location_guess", "style")
    for key in required_str:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            return False, "ERR_STAGE1_VALIDATE", f"Missing or empty required field: {key}"
        if _contains_failure_marker(value):
            return False, "ERR_STAGE1_VALIDATE", f"Failure marker detected in field: {key}"

    for key in ("palette", "keywords"):
        value = payload.get(key)
        if not isinstance(value, list):
            return False, "ERR_STAGE1_VALIDATE", f"Field must be a list: {key}"
        if key == "palette" and not (1 <= len(value) <= 16):
            return False, "ERR_STAGE1_VALIDATE", "Palette list length must be between 1 and 16"
        if key == "keywords" and not (1 <= len(value) <= 30):
            return False, "ERR_STAGE1_VALIDATE", "Keywords list length must be between 1 and 30"
        for idx, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                return False, "ERR_STAGE1_VALIDATE", f"Invalid {key}[{idx}] entry"
            if _contains_failure_marker(item):
                return False, "ERR_STAGE1_VALIDATE", f"Failure marker detected in {key}[{idx}]"

    return True, None, None


def _detect_structured_failure(payload: Any) -> tuple[str, str] | None:
    if not isinstance(payload, dict):
        return None
    status = str(payload.get("STATUS") or payload.get("status") or "").strip().upper()
    if status != "FAILED":
        return None
    reason = str(payload.get("REASON") or payload.get("reason") or "ERR_AI_FAILED").strip() or "ERR_AI_FAILED"
    message = str(payload.get("MESSAGE") or payload.get("message") or "AI reported stage1 failure").strip() or "AI reported stage1 failure"
    return reason[:128], message[:1024]


def _write_stage1_outputs(
    *,
    artwork_dir: Path,
    slug: str,
    provider: str,
    job_id: str,
    stage1_payload: dict[str, Any],
) -> tuple[Path, Path]:
    analysis_stage1_name = f"{slug}-analysis-stage1.json"
    ai_packet_name = f"{slug}-ai-packet.json"
    stage1_path = artwork_dir / analysis_stage1_name
    ai_packet_path = artwork_dir / ai_packet_name

    write_json_atomic(stage1_path, stage1_payload)

    now = _now_iso()
    ai_packet = {
        "slug": slug,
        "provider": provider,
        "job_id": job_id,
        "updated_at": now,
        "stages": {
            "stage1_image": {
                "status": "success",
                "output_file": analysis_stage1_name,
                "payload": stage1_payload,
                "updated_at": now,
            }
        },
    }
    write_json_atomic(ai_packet_path, ai_packet)

    manifest = _load_manifest(artwork_dir, slug)
    manifest.setdefault("files", {})
    manifest["files"]["analysis_stage1"] = analysis_stage1_name
    manifest["files"]["ai_packet"] = ai_packet_name
    write_json_atomic(_find_manifest_path(artwork_dir, slug), manifest)

    return stage1_path, ai_packet_path


def _load_stage1_payload(artwork_dir: Path, slug: str) -> dict[str, Any]:
    stage1_path = artwork_dir / f"{slug}-analysis-stage1.json"
    if not stage1_path.exists():
        raise RuntimeError("ERR_MISSING_STAGE1: Stage 1 output file missing")
    try:
        payload = json.loads(stage1_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError("ERR_STAGE1_INVALID: Stage 1 output is not valid JSON") from exc
    valid, reason, message = _validate_stage1_payload(payload)
    if not valid:
        raise RuntimeError(f"{reason or 'ERR_STAGE1_INVALID'}: {message or 'Invalid Stage 1 payload'}")
    return payload


def _extract_stage2_payload(*, stage1_payload: dict[str, Any], provider_result: dict[str, Any]) -> dict[str, Any]:
    listing = _as_dict(provider_result.get("listing"))
    metadata = _as_dict(provider_result.get("metadata"))

    title = str(listing.get("title") or listing.get("etsy_title") or "").strip()
    description = str(listing.get("description") or listing.get("etsy_description") or "").strip()
    description = _ensure_printing_options_block(description)

    tags = _as_list(listing.get("tags"))
    tags_clean = [str(t).strip() for t in tags if str(t).strip()]

    stage1_keywords = _as_list(stage1_payload.get("keywords"))
    seo_keywords = [str(k).strip() for k in stage1_keywords if str(k).strip()]
    for tag in tags_clean:
        if tag not in seo_keywords:
            seo_keywords.append(tag)

    if not seo_keywords:
        visual = _as_dict(metadata.get("analysis"))
        visual_analysis = _as_dict(visual.get("visual_analysis"))
        palette_terms = _split_terms(visual_analysis.get("palette"))
        seo_keywords = palette_terms[:10]

    sizes = [
        'Up to 48" on the long edge (14,400px)',
        'Up to 24" on the long edge (7,200px)',
        "300 DPI print-ready",
        "7200–14400px long edge master file",
    ]

    disclaimers = [
        "Digital download only — no physical item is shipped.",
        "Personal use only. Copyright remains with the artist.",
        "Due to the instant digital nature of this product, refunds are not offered.",
    ]

    return {
        "title": title,
        "description": description,
        "seo_keywords": seo_keywords,
        "tags": tags_clean,
        "sizes": sizes,
        "disclaimers": disclaimers,
    }


def _validate_stage2_payload(payload: Any) -> tuple[str, str | None, str | None]:
    if not isinstance(payload, dict):
        return "failed", "ERR_STAGE2_PARSE", "Stage 2 output is not a JSON object"

    status = str(payload.get("STATUS") or payload.get("status") or "").strip().upper()
    if status == "FAILED":
        reason = str(payload.get("REASON") or payload.get("reason") or "ERR_AI_FAILED").strip() or "ERR_AI_FAILED"
        message = str(payload.get("MESSAGE") or payload.get("message") or "AI reported structured stage2 failure").strip()
        return "failed", reason[:128], message[:1024]

    title = payload.get("title")
    description = payload.get("description")
    seo_keywords = payload.get("seo_keywords")
    disclaimers = payload.get("disclaimers")

    if not isinstance(title, str) or not title.strip():
        return "failed", "ERR_STAGE2_VALIDATE", "Missing or empty title"
    if not isinstance(description, str) or not description.strip():
        return "failed", "ERR_STAGE2_VALIDATE", "Missing or empty description"
    if not isinstance(seo_keywords, list) or not seo_keywords:
        return "failed", "ERR_STAGE2_VALIDATE", "Missing or empty seo_keywords"
    if not isinstance(disclaimers, list) or not disclaimers:
        return "failed", "ERR_STAGE2_VALIDATE", "Missing disclaimers"

    html_pattern = re.compile(r"<[^>]+>")
    if html_pattern.search(title) or html_pattern.search(description):
        return "failed", "ERR_STAGE2_HTML", "HTML tags are not allowed in Etsy output"

    joined_disclaimers = "\n".join(str(item) for item in disclaimers)
    all_text = f"{title}\n{description}\n{joined_disclaimers}".lower()

    review_issues: list[str] = []

    if "digital download" not in all_text and "digital file" not in all_text:
        review_issues.append("Missing digital-download clarity")

    if not ("14400" in all_text or "7200" in all_text or "48\"" in all_text or "48 inch" in all_text or "48”" in all_text or "24 inch" in all_text or "24\"" in all_text):
        review_issues.append("Missing print quality statement (7200–14400px / up to 24–48\")")

    if "personal use" not in all_text and "copyright" not in all_text:
        review_issues.append("Missing personal-use/copyright statement")

    lines = description.splitlines() or [description]
    if any(len(line.strip()) > 260 for line in lines if line.strip()):
        review_issues.append("Description contains very long unbroken lines")

    if review_issues:
        return "needs_review", "WARN_STAGE2_REVIEW", "; ".join(review_issues)[:1024]

    return "success", None, None


def _write_stage2_outputs(
    *,
    artwork_dir: Path,
    slug: str,
    stage2_payload: dict[str, Any],
    stage2_status: str,
) -> Path:
    copy_etsy_name = f"{slug}-copy-etsy.json"
    copy_etsy_path = artwork_dir / copy_etsy_name
    write_json_atomic(copy_etsy_path, stage2_payload)

    manifest = _load_manifest(artwork_dir, slug)
    manifest.setdefault("files", {})
    manifest["files"]["copy_etsy"] = copy_etsy_name
    write_json_atomic(_find_manifest_path(artwork_dir, slug), manifest)

    ai_packet_name = manifest["files"].get("ai_packet") or f"{slug}-ai-packet.json"
    ai_packet_path = artwork_dir / str(ai_packet_name)
    if ai_packet_path.exists():
        try:
            ai_packet = json.loads(ai_packet_path.read_text(encoding="utf-8"))
        except Exception:
            ai_packet = {}
    else:
        ai_packet = {
            "slug": slug,
            "updated_at": _now_iso(),
            "stages": {},
        }

    if not isinstance(ai_packet, dict):
        ai_packet = {"slug": slug, "updated_at": _now_iso(), "stages": {}}
    ai_packet.setdefault("stages", {})
    ai_packet["stages"]["stage2_etsy"] = {
        "status": stage2_status,
        "output_file": copy_etsy_name,
        "payload": stage2_payload,
        "updated_at": _now_iso(),
    }
    ai_packet["updated_at"] = _now_iso()
    write_json_atomic(ai_packet_path, ai_packet)

    return copy_etsy_path


def _classify_worker_error(exc: Exception) -> tuple[str, str]:
    reason = str(getattr(exc, "error_code", "") or "").strip() or "ERR_WORKER"
    message = str(getattr(exc, "error_detail", "") or str(exc) or "Worker error").strip()
    if ":" in message:
        prefix, detail = message.split(":", 1)
        if prefix.strip().startswith("ERR_"):
            reason = prefix.strip()
            message = detail.strip() or message
    return reason[:128], message[:1024]


def _claim_next_job(session) -> AnalysisJob | None:
    """Claim the next QUEUED job atomically."""
    try:
        # Find oldest QUEUED job
        job = (
            session.query(AnalysisJob)
            .filter(AnalysisJob.status == "QUEUED")
            .order_by(AnalysisJob.created_at.asc())
            .first()
        )
        
        if not job:
            return None
        
        # Claim it by setting RUNNING
        job.status = "RUNNING"  # type: ignore[misc]
        job.started_at = datetime.utcnow()  # type: ignore[assignment]
        job.updated_at = datetime.utcnow()  # type: ignore[assignment]
        job.attempts = (job.attempts or 0) + 1  # type: ignore[operator,assignment]
        
        session.commit()
        logger.info(f"Claimed job {job.job_id}: {job.provider} analysis for slug={job.slug}")
        return job
    
    except Exception as exc:
        logger.exception("Failed to claim job")
        session.rollback()
        return None


def _process_job_stage1a(job: AnalysisJob, session) -> None:
    """Process one queue job: Stage 1 image analysis, then Stage 2 Etsy listing generation."""
    cfg = get_config()
    processed_root = cfg.LAB_PROCESSED_DIR
    index_path = cfg.ARTWORKS_INDEX_PATH
    slug = _job_str(job, "slug")
    provider = _job_str(job, "provider")
    job_id = _job_str(job, "job_id")
    attempts = _job_int(job, "attempts", 0)
    stage = _job_str(job, "stage", "stage1_image")
    current_stage = "stage1_image"
    sku_value = getattr(job, "sku", None)
    sku = sku_value if isinstance(sku_value, str) and sku_value else None
    artwork_dir: Path = processed_root / slug

    try:
        index = ArtworksIndex(index_path, processed_root)

        if sku:
            try:
                resolved_dir, _ = index.resolve(sku)
                artwork_dir = Path(resolved_dir)
            except Exception:
                artwork_dir = processed_root / slug

        if not artwork_dir.exists():
            raise FileNotFoundError(f"Artwork directory not found: {artwork_dir}")

        _abort_if_cancel_requested(job_id)

        _update_manifest_analysis(
            artwork_dir,
            slug,
            status="running",
            stage="stage1_image",
            progress=5,
            provider=provider,
            job_id=job_id,
            attempts=attempts or 1,
            message="Running stage 1 image analysis",
        )

        logger.info("Job %s: Running provider=%s stage1_image for slug=%s", job_id, provider, slug)
        if provider == "openai":
            stage1_provider_result = run_openai_analysis_for_slug(slug=slug, processed_root=processed_root)
        elif provider == "gemini":
            stage1_provider_result = run_gemini_analysis_for_slug(slug=slug, processed_root=processed_root)
        else:
            raise RuntimeError(f"ERR_PROVIDER: Unsupported provider: {provider}")

        _abort_if_cancel_requested(job_id)

        if not isinstance(stage1_provider_result, dict):
            raise RuntimeError("ERR_STAGE1_PARSE: Stage 1 provider response is not JSON object")

        structured_failure = _detect_structured_failure(stage1_provider_result)
        if structured_failure:
            reason, message = structured_failure
            raise RuntimeError(f"{reason}: {message}")

        stage1_payload = _extract_stage1_payload(slug=slug, result=stage1_provider_result)
        is_valid, fail_reason, fail_message = _validate_stage1_payload(stage1_payload)
        if not is_valid:
            raise RuntimeError(f"{fail_reason or 'ERR_STAGE1_VALIDATE'}: {fail_message or 'Invalid stage1 payload'}")

        _update_manifest_analysis(
            artwork_dir,
            slug,
            status="running",
            stage="stage1_image",
            progress=24,
            provider=provider,
            job_id=job_id,
            attempts=attempts or 1,
            message="Writing stage 1 outputs",
        )

        _write_stage1_outputs(
            artwork_dir=artwork_dir,
            slug=slug,
            provider=provider,
            job_id=job_id,
            stage1_payload=stage1_payload,
        )

        _abort_if_cancel_requested(job_id)

        current_stage = "stage2_etsy"
        _update_manifest_analysis(
            artwork_dir,
            slug,
            status="running",
            stage="stage2_etsy",
            progress=40,
            provider=provider,
            job_id=job_id,
            attempts=attempts or 1,
            message="Running stage 2 Etsy listing generation",
        )

        stage1_file_payload = _load_stage1_payload(artwork_dir, slug)
        single_pass = _cfg_bool(cfg, "ANALYSIS_SINGLE_PASS", True)

        if single_pass:
            logger.info(
                "Job %s: Stage 2 using single-pass provider payload (no second AI call)",
                job_id,
            )
            stage2_provider_result = stage1_provider_result
        else:
            logger.info(
                "Job %s: Stage 2 legacy mode enabled (second AI call)",
                job_id,
            )
            if provider == "openai":
                stage2_provider_result = run_openai_analysis_for_slug(slug=slug, processed_root=processed_root)
            elif provider == "gemini":
                stage2_provider_result = run_gemini_analysis_for_slug(slug=slug, processed_root=processed_root)
            else:
                raise RuntimeError(f"ERR_PROVIDER: Unsupported provider: {provider}")

        _abort_if_cancel_requested(job_id)

        if not isinstance(stage2_provider_result, dict):
            raise RuntimeError("ERR_STAGE2_PARSE: Stage 2 provider response is not JSON object")

        structured_failure = _detect_structured_failure(stage2_provider_result)
        if structured_failure:
            reason, message = structured_failure
            raise RuntimeError(f"{reason}: {message}")

        stage2_payload = _extract_stage2_payload(
            stage1_payload=stage1_file_payload,
            provider_result=stage2_provider_result,
        )

        stage2_status, stage2_reason, stage2_message = _validate_stage2_payload(stage2_payload)
        if stage2_status == "failed":
            raise RuntimeError(f"{stage2_reason or 'ERR_STAGE2_VALIDATE'}: {stage2_message or 'Invalid stage2 payload'}")

        _update_manifest_analysis(
            artwork_dir,
            slug,
            status="running",
            stage="stage2_etsy",
            progress=58,
            provider=provider,
            job_id=job_id,
            attempts=attempts or 1,
            message="Writing stage 2 Etsy output",
        )

        _write_stage2_outputs(
            artwork_dir=artwork_dir,
            slug=slug,
            stage2_payload=stage2_payload,
            stage2_status=stage2_status,
        )

        _abort_if_cancel_requested(job_id)

        job.status = "DONE"  # type: ignore[misc]
        job.stage = "stage2_etsy"  # type: ignore[assignment]
        job.progress = 66  # type: ignore[assignment]
        job.reason = stage2_reason if stage2_status == "needs_review" else None  # type: ignore[assignment]
        job.error_message = stage2_message if stage2_status == "needs_review" else None  # type: ignore[assignment]
        job.finished_at = datetime.utcnow()  # type: ignore[assignment]
        job.updated_at = datetime.utcnow()  # type: ignore[assignment]
        session.commit()

        _update_manifest_analysis(
            artwork_dir,
            slug,
            status="needs_review" if stage2_status == "needs_review" else "success",
            stage="stage2_etsy",
            progress=66,
            provider=provider,
            job_id=job_id,
            attempts=attempts or 1,
            reason=stage2_reason if stage2_status == "needs_review" else None,
            message=(stage2_message or "Stage 2 Etsy listing generated") if stage2_status == "needs_review" else "Stage 2 Etsy listing generated",
        )

        logger.info("Job %s: Stage 2 complete with status=%s", job_id, stage2_status)

    except Exception as exc:
        logger.exception(f"Job {job_id}: Failed with error")
        reason, message = _classify_worker_error(exc)
        if isinstance(exc, JobCancelledError):
            reason = "ERR_CANCELLED"
            message = "Cancelled by admin"
        if isinstance(exc, (OpenAIAnalysisError, GeminiAnalysisError)):
            reason = str(getattr(exc, "error_code", reason) or reason)[:128]
            detail = str(getattr(exc, "error_detail", "") or "").strip()
            if detail:
                message = detail[:1024]

        job.status = "FAILED"  # type: ignore[misc]
        job.reason = reason  # type: ignore[assignment]
        job.error_message = message  # type: ignore[assignment]
        job.finished_at = datetime.utcnow()  # type: ignore[assignment]
        job.updated_at = datetime.utcnow()  # type: ignore[assignment]
        session.commit()

        if reason == "ERR_CANCELLED":
            try:
                cleanup_analysis_job_artifacts(
                    slug=slug,
                    sku=sku,
                    lab_roots=[cfg.LAB_PROCESSED_DIR, cfg.LAB_UNPROCESSED_DIR, cfg.LAB_LOCKED_DIR],
                    remove_artwork_record=True,
                )
            except Exception:
                logger.exception("Failed cleanup for cancelled job %s", job_id)

            try:
                session.delete(job)
                session.commit()
            except Exception:
                logger.exception("Failed deleting cancelled job row %s", job_id)
                session.rollback()
            return

        try:
            artwork_dir = processed_root / slug
            if artwork_dir.exists():
                _update_manifest_analysis(
                    artwork_dir,
                    slug,
                    status="failed",
                    stage=current_stage or stage,
                    progress=66 if current_stage == "stage2_etsy" else 33,
                    provider=provider,
                    job_id=job_id,
                    attempts=attempts or 1,
                    reason=reason,
                    message=message[:256],
                )
        except Exception:
            logger.exception(f"Failed to update manifest for failed job {job_id}")


def run_worker(poll_interval: float = 3.0, max_iterations: int | None = None) -> None:
    """Run the analysis job worker loop.
    
    Args:
        poll_interval: Seconds between polls (default: 3.0)
        max_iterations: Max loops before exit (None = infinite)
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    
    logger.info(f"Starting analysis worker (poll_interval={poll_interval}s)")
    
    iterations = 0
    while True:
        session = SessionLocal()
        try:
            job = _claim_next_job(session)
            
            if job:
                _process_job_stage1a(job, session)
            else:
                # No jobs available
                pass
        
        except KeyboardInterrupt:
            logger.info("Worker interrupted by user")
            break
        
        except Exception as exc:
            logger.exception("Worker loop error")
        
        finally:
            session.close()
        
        iterations += 1
        if max_iterations and iterations >= max_iterations:
            logger.info(f"Worker exiting after {iterations} iterations")
            break
        
        time.sleep(poll_interval)


if __name__ == "__main__":
    run_worker()
