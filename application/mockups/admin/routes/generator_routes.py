"""Mockup Base Generation - Flask Routes for Generator Control Center and Utilities.

Provides two main blueprints:
1. Mockup Generator Dashboard: Real-time view and control of the mockup generation pipeline
2. Solid Image Utility: Generate and download solid color placeholder images

Both routes interoperate with the Stage 1 database models (MockupBaseGenerationJob)
and Stage 2A services (MockupPromptService, GeminiImageService).
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast
from zoneinfo import ZoneInfo

from sqlalchemy import or_

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    send_file,
    flash,
    url_for,
    abort,
    redirect,
)

from db import SessionLocal, MockupBaseGenerationJob, GeminiStudioJob
from application.mockups.config import MockupBaseGenerationCatalog
from application.mockups.services.solid_image_service import (
    SolidImageService,
    SolidImageValidationError,
    SolidImageGenerationError,
)
from application.mockups.admin.services import CatalogAdminService, ValidationError
from application.utils.csrf import require_csrf_or_400, get_csrf_token


logger = logging.getLogger(__name__)

CONTROL_STATE_PATH = Path("/srv/artlomo/var/state/mockup_generator_control.json")
PROMPT_SETTINGS_PATH = Path("/srv/artlomo/var/state/mockup_generator_prompt_settings.json")
QUANTITY_OPTIONS = (1, 2, 3, 4, 5, 10, 15, 20, 25, 30)
RECENT_FAILURE_LIMIT = 12
RECENT_COMPLETED_LIMIT = 100
RECENT_ATTEMPT_LIMIT = 25
MOCKUP_CELERY_REDIS_URL = "redis://localhost:6379/0"
STUDIO_RUNTIME_ROOT = Path("/srv/artlomo/var/studio").resolve()

# Blueprint for mockup generator control center
mockup_generator_bp = Blueprint(
    "mockup_generator",
    __name__,
    template_folder="../ui/templates",
    static_folder="../ui/static",
)

# Blueprint for solid image utility
utility_bp = Blueprint(
    "utility",
    __name__,
    template_folder="../ui/templates",
    static_folder="../ui/static",
)


# ============================================================================
# Mockup Generator Dashboard Routes
# ============================================================================


DEFAULT_MAX_RETRIES = 3
DEFAULT_PLACEHOLDER_MODE = "artwork_trojan"
PROMPT_METADATA_PREFIX = "[[MOCKUP_GUIDE_METADATA]]"
GENERATION_MODE_STANDARD = "standard"
GENERATION_MODE_CHROMAKEY_AUTO = "chromakey_auto"
GENERATION_MODE_ARTWORK_TROJAN = "artwork_trojan"
GENERATION_MODE_ARTWORK_ONLY_COMPOSITE = "artwork_only_composite"

DEFAULT_STANDARD_PREFIX = (
    "You are generating a production mockup base image for ArtLomo.\n"
    "Prioritise photorealism, clean architectural composition, and export-safe image quality.\n"
    "Follow all placeholder and geometry instructions in the base prompt exactly."
)
DEFAULT_STANDARD_SUFFIX = (
    "Final quality constraints:\n"
    "- Output one image only.\n"
    "- Keep edges clean and realistic with no artifacts or added overlays.\n"
    "- Preserve true perspective with believable lens geometry.\n"
    "- Keep the wall placeholder fully visible and unobstructed."
)
DEFAULT_OUTLINED_PREFIX = (
    "You are generating a production mockup base using provided outlined reference artwork.\n"
    "Preserve artwork fidelity and frame geometry exactly while building a premium interior scene.\n"
    "Do not stylize, repaint, or alter the supplied artwork content."
)
DEFAULT_OUTLINED_SUFFIX = (
    "Final quality constraints:\n"
    "- Output one image only.\n"
    "- Keep the full bordered artwork visible, rectangular, and unobstructed.\n"
    "- No glare, clipping, distortion, or occlusion on artwork edges.\n"
    "- Maintain photorealistic room lighting without contaminating the artwork surface."
)
DEFAULT_CANVAS_ASPECT = "1x1"
STYLE_OPTIONS = (
    "Contemporary",
    "Luxury",
    "Minimal",
    "Eccentric",
    "Classical",
    "Realistic lived in",
    "Industrial",
    "Scandinavian",
    "Bohemian",
    "Japandi",
    "Rustic",
    "Coastal",
)
TONE_OPTIONS = (
    "Warm",
    "Cool",
    "Cold",
    "Colourful",
    "Neutral",
    "Moody",
    "Earthy",
)
SEASON_OPTIONS = (
    "Summer",
    "Winter",
    "Autumn",
    "Spring",
    "Any",
)

DEFAULT_PROMPT_SETTINGS: dict[str, object] = {
    "standard_prefix": DEFAULT_STANDARD_PREFIX,
    "standard_suffix": DEFAULT_STANDARD_SUFFIX,
    "outlined_prefix": DEFAULT_OUTLINED_PREFIX,
    "outlined_suffix": DEFAULT_OUTLINED_SUFFIX,
    "generation_canvas_aspect_ratio": DEFAULT_CANVAS_ASPECT,
    "default_style": "Contemporary",
    "default_tone": "Warm",
    "default_season": "Any",
}


def _normalize_prompt_settings(payload: dict[str, object] | None) -> dict[str, object]:
    merged = dict(DEFAULT_PROMPT_SETTINGS)
    if isinstance(payload, dict):
        merged.update(payload)

    for key in ("standard_prefix", "standard_suffix", "outlined_prefix", "outlined_suffix"):
        value = str(merged.get(key) or "").strip()
        merged[key] = value if value else str(DEFAULT_PROMPT_SETTINGS[key])

    raw_canvas_aspect = str(merged.get("generation_canvas_aspect_ratio") or DEFAULT_CANVAS_ASPECT)
    if raw_canvas_aspect not in MockupBaseGenerationCatalog.ASPECT_RATIOS:
        raw_canvas_aspect = DEFAULT_CANVAS_ASPECT
    merged["generation_canvas_aspect_ratio"] = raw_canvas_aspect

    style = str(merged.get("default_style") or DEFAULT_PROMPT_SETTINGS["default_style"])
    tone = str(merged.get("default_tone") or DEFAULT_PROMPT_SETTINGS["default_tone"])
    season = str(merged.get("default_season") or DEFAULT_PROMPT_SETTINGS["default_season"])
    merged["default_style"] = style if style in STYLE_OPTIONS else str(DEFAULT_PROMPT_SETTINGS["default_style"])
    merged["default_tone"] = tone if tone in TONE_OPTIONS else str(DEFAULT_PROMPT_SETTINGS["default_tone"])
    merged["default_season"] = season if season in SEASON_OPTIONS else str(DEFAULT_PROMPT_SETTINGS["default_season"])
    return merged


def _build_prompt_examples(settings: dict[str, object]) -> list[str]:
    style = str(settings.get("default_style") or "Contemporary")
    tone = str(settings.get("default_tone") or "Warm")
    season = str(settings.get("default_season") or "Any")
    season_suffix = "" if season == "Any" else f" during {season.lower()}"
    return [
        f"Please generate a square image of this 2x3 aspect ratio artwork as a mockup framed and on the wall in a {style.lower()} office.",
        f"Please generate a square image of this 3x4 aspect ratio artwork as a mockup framed and on the wall in a {style.lower()} living room.",
        f"Please generate a square image of this 4x5 aspect ratio artwork as a mockup framed and on the wall in a {tone.lower()}, realistic lived in music room{season_suffix}.",
        "Please generate a square image of this 70x99 aspect ratio artwork as a mockup framed and on the wall in a luxury apartment.",
    ]


def _celery_worker_running() -> bool:
    try:
        import subprocess

        result = subprocess.run(
            ["pgrep", "-fa", "celery"],
            capture_output=True,
            text=True,
            timeout=1,
            check=False,
        )
        output = (result.stdout or "").strip().lower()
        return "celery" in output and "worker" in output
    except Exception:
        return False


def _resolve_celery_redis_url() -> str:
    return str(os.getenv("CELERY_BROKER_URL") or MOCKUP_CELERY_REDIS_URL).strip()


def _get_redis_client():
    try:
        import redis  # type: ignore

        return redis.Redis.from_url(_resolve_celery_redis_url())
    except Exception:
        return None


def _redis_llen(redis_client: Any, queue_name: str) -> int:
    value = redis_client.llen(queue_name)
    return int(cast(int, value))


def _redis_lrange(redis_client: Any, queue_name: str, start: int, end: int) -> list[bytes]:
    values = redis_client.lrange(queue_name, start, end)
    return [v for v in cast(list[Any], values) if isinstance(v, (bytes, bytearray))]


def _redis_lpop(redis_client: Any, queue_name: str) -> bytes | None:
    value = redis_client.lpop(queue_name)
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    return None


def _redis_rpush_many(redis_client: Any, queue_name: str, items: list[bytes]) -> None:
    if not items:
        return
    redis_client.rpush(queue_name, *items)


def _decode_queue_payload(raw_message: bytes) -> dict[str, object]:
    try:
        return cast(dict[str, object], json.loads(raw_message))
    except Exception:
        return {}


def _queue_task_name(payload: dict[str, object]) -> str:
    headers = payload.get("headers")
    if isinstance(headers, dict):
        return str(headers.get("task") or "")
    return ""


def _queue_task_id(payload: dict[str, object]) -> str:
    headers = payload.get("headers")
    if isinstance(headers, dict):
        return str(headers.get("id") or "")
    return ""


def _queue_args_repr(payload: dict[str, object]) -> str:
    headers = payload.get("headers")
    if isinstance(headers, dict):
        return str(headers.get("argsrepr") or "")
    return ""


def _extract_job_id_from_argsrepr(argsrepr: str) -> int | None:
    value = str(argsrepr or "").strip()
    if value.startswith("(") and value.endswith(")"):
        value = value[1:-1]
    value = value.replace(",", "").strip()
    if value.isdigit():
        return int(value)
    return None


def _queue_snapshot(limit: int = 120) -> dict[str, object]:
    redis_client = _get_redis_client()
    if redis_client is None:
        return {"available": False, "error": "Redis client unavailable", "queue_length": 0, "items": []}

    queue_name = "celery"
    try:
        queue_length = _redis_llen(redis_client, queue_name)
        sample = _redis_lrange(redis_client, queue_name, 0, max(0, int(limit) - 1))
    except Exception as exc:
        return {
            "available": False,
            "error": str(exc),
            "queue_length": 0,
            "items": [],
        }

    items: list[dict[str, object]] = []
    by_task: dict[str, int] = {}
    for raw in sample:
        payload = _decode_queue_payload(raw)
        task_name = _queue_task_name(payload)
        task_id = _queue_task_id(payload)
        argsrepr = _queue_args_repr(payload)
        by_task[task_name or "<unknown>"] = by_task.get(task_name or "<unknown>", 0) + 1
        items.append(
            {
                "task_name": task_name,
                "task_id": task_id,
                "argsrepr": argsrepr,
                "job_id": _extract_job_id_from_argsrepr(argsrepr),
            }
        )

    return {
        "available": True,
        "error": "",
        "queue_length": queue_length,
        "items": items,
        "by_task": by_task,
    }


def _rewrite_celery_queue(should_remove) -> tuple[int, int]:
    redis_client = _get_redis_client()
    if redis_client is None:
        return (0, 0)

    queue_name = "celery"
    initial = _redis_llen(redis_client, queue_name)
    kept: list[bytes] = []
    removed = 0

    for _ in range(initial):
        raw = _redis_lpop(redis_client, queue_name)
        if raw is None:
            break
        payload = _decode_queue_payload(raw)
        if should_remove(payload):
            removed += 1
            continue
        kept.append(raw)

    _redis_rpush_many(redis_client, queue_name, kept)

    return removed, _redis_llen(redis_client, queue_name)


def _safe_unlink(path_value: str | None) -> bool:
    candidate = str(path_value or "").strip()
    if not candidate:
        return False
    path = Path(candidate)
    if not path.is_absolute():
        return False
    if not path.exists() or not path.is_file():
        return False
    try:
        path_resolved = path.resolve()
    except Exception:
        return False

    # Only allow cleanup under known runtime/output roots.
    allowed_roots = (
        Path("/srv/artlomo/application/mockups/catalog/assets/mockups/bases").resolve(),
        Path("/srv/artlomo/application/mockups/catalog/assets/mockups/coordinates").resolve(),
        STUDIO_RUNTIME_ROOT,
    )
    if not any(str(path_resolved).startswith(str(root)) for root in allowed_roots):
        return False

    try:
        path_resolved.unlink(missing_ok=True)
        return True
    except Exception:
        return False


def _clear_pending_db_and_files() -> dict[str, int]:
    session = SessionLocal()
    removed_mockup_rows = 0
    removed_gemini_rows = 0
    deleted_files = 0
    try:
        mockup_rows = (
            session.query(MockupBaseGenerationJob)
            .filter(MockupBaseGenerationJob.status.in_(["Pending", "Generating", "Processing", "Queued"]))
            .all()
        )
        for row in mockup_rows:
            if _safe_unlink(str(row.generated_image_path or "")):
                deleted_files += 1
            if _safe_unlink(str(row.coordinates_path or "")):
                deleted_files += 1
            session.delete(row)
            removed_mockup_rows += 1

        gemini_rows = (
            session.query(GeminiStudioJob)
            .filter(GeminiStudioJob.status.in_(["Pending", "Generating"]))
            .all()
        )
        for row in gemini_rows:
            if _safe_unlink(str(row.output_image_path or "")):
                deleted_files += 1
            source_path = str(row.source_image_path or "")
            if source_path and str(Path(source_path).resolve()).startswith(str(STUDIO_RUNTIME_ROOT)):
                if _safe_unlink(source_path):
                    deleted_files += 1
            session.delete(row)
            removed_gemini_rows += 1

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return {
        "removed_mockup_rows": removed_mockup_rows,
        "removed_gemini_rows": removed_gemini_rows,
        "deleted_files": deleted_files,
    }


def _remove_orphan_queue_items() -> tuple[int, int]:
    session = SessionLocal()
    try:
        mockup_ids = {row_id for (row_id,) in session.query(MockupBaseGenerationJob.id).all()}
        gemini_ids = {row_id for (row_id,) in session.query(GeminiStudioJob.id).all()}
    finally:
        session.close()

    def should_remove(payload: dict[str, object]) -> bool:
        task_name = _queue_task_name(payload)
        argsrepr = _queue_args_repr(payload)
        job_id = _extract_job_id_from_argsrepr(argsrepr)
        if job_id is None:
            return False
        if task_name == "mockups.process_mockup_job":
            return job_id not in mockup_ids
        if task_name == "mockups.process_gemini_studio_job":
            return job_id not in gemini_ids
        return False

    return _rewrite_celery_queue(should_remove)


def _sanitize_placeholder_mode(value: object) -> str:
    normalized = str(value or DEFAULT_PLACEHOLDER_MODE).strip().lower()
    if normalized == GENERATION_MODE_CHROMAKEY_AUTO:
        return GENERATION_MODE_CHROMAKEY_AUTO
    if normalized == GENERATION_MODE_ARTWORK_ONLY_COMPOSITE:
        return GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
    return GENERATION_MODE_ARTWORK_TROJAN


def _resolve_generation_mode_from_placeholder(placeholder_mode: str) -> str:
    """Map UI placeholder mode to generation mode."""
    normalized = _sanitize_placeholder_mode(placeholder_mode)
    if normalized == GENERATION_MODE_CHROMAKEY_AUTO:
        return GENERATION_MODE_CHROMAKEY_AUTO
    if normalized == GENERATION_MODE_ARTWORK_ONLY_COMPOSITE:
        return GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
    return GENERATION_MODE_ARTWORK_TROJAN


def _make_mode_job_external_id(
    *,
    aspect_ratio: str,
    category: str,
    variation_index: int,
    generation_mode: str,
) -> str:
    """Build deterministic mode-aware job IDs to keep standard/trojan queues parallel."""
    base_job_id = f"mbg_{aspect_ratio}_{category}_v{variation_index}".replace(" ", "-")
    if generation_mode == GENERATION_MODE_STANDARD:
        return base_job_id
    return f"{base_job_id}__{generation_mode}".replace(" ", "-")


def _extract_prompt_metadata(prompt_text: object) -> dict[str, str]:
    raw = str(prompt_text or "")
    if not raw.startswith(PROMPT_METADATA_PREFIX):
        return {"placeholder_mode": "", "guide_path": ""}

    metadata_line, _, _ = raw.partition("\n")
    payload = metadata_line[len(PROMPT_METADATA_PREFIX):]
    try:
        parsed = json.loads(payload)
    except Exception:
        return {"placeholder_mode": "", "guide_path": ""}

    if not isinstance(parsed, dict):
        return {"placeholder_mode": "", "guide_path": ""}

    return {
        "placeholder_mode": _sanitize_placeholder_mode(parsed.get("placeholder_mode")),
        "guide_path": str(parsed.get("guide_path") or ""),
    }


def _default_control_state() -> dict[str, str]:
    return {
        "state": "running",
        "updated_at": "",
        "message": "",
        "max_retries": str(DEFAULT_MAX_RETRIES),
        "placeholder_mode": DEFAULT_PLACEHOLDER_MODE,
        "skip_coordinate_detection": "false",
        "custom_prompt_text": "",
        "raw_prompt_only_enabled": "false",
        "raw_prompt_text": "",
    }


def _load_control_state() -> dict[str, str]:
    if not CONTROL_STATE_PATH.exists():
        return _default_control_state()
    try:
        parsed = json.loads(CONTROL_STATE_PATH.read_text(encoding="utf-8"))
        if not isinstance(parsed, dict):
            return _default_control_state()
        return {
            "state": str(parsed.get("state") or "running"),
            "updated_at": str(parsed.get("updated_at") or ""),
            "message": str(parsed.get("message") or ""),
            "max_retries": str(parsed.get("max_retries") or DEFAULT_MAX_RETRIES),
            "placeholder_mode": _sanitize_placeholder_mode(parsed.get("placeholder_mode")),
            "skip_coordinate_detection": str(parsed.get("skip_coordinate_detection") or "false"),
            "custom_prompt_text": str(parsed.get("custom_prompt_text") or ""),
            "raw_prompt_only_enabled": str(parsed.get("raw_prompt_only_enabled") or "false"),
            "raw_prompt_text": str(parsed.get("raw_prompt_text") or ""),
        }
    except Exception:
        return _default_control_state()


def _save_control_state(
    state: str,
    message: str,
    *,
    max_retries: int | None = None,
    placeholder_mode: str | None = None,
    skip_coordinate_detection: bool | None = None,
    custom_prompt_text: str | None = None,
    raw_prompt_only_enabled: bool | None = None,
    raw_prompt_text: str | None = None,
) -> dict[str, str]:
    # Preserve existing max_retries unless a new value is explicitly provided.
    existing = _load_control_state()
    resolved_max_retries = max_retries if max_retries is not None else int(existing.get("max_retries") or DEFAULT_MAX_RETRIES)
    resolved_placeholder_mode = (
        _sanitize_placeholder_mode(placeholder_mode)
        if placeholder_mode is not None
        else _sanitize_placeholder_mode(existing.get("placeholder_mode"))
    )
    resolved_skip_coordinate_detection = (
        bool(skip_coordinate_detection)
        if skip_coordinate_detection is not None
        else str(existing.get("skip_coordinate_detection") or "false").strip().lower() in {"1", "true", "yes", "on"}
    )
    resolved_custom_prompt_text = (
        str(custom_prompt_text or "").strip()
        if custom_prompt_text is not None
        else str(existing.get("custom_prompt_text") or "").strip()
    )
    resolved_raw_prompt_only_enabled = (
        bool(raw_prompt_only_enabled)
        if raw_prompt_only_enabled is not None
        else str(existing.get("raw_prompt_only_enabled") or "false").strip().lower() in {"1", "true", "yes", "on"}
    )
    resolved_raw_prompt_text = (
        str(raw_prompt_text or "")
        if raw_prompt_text is not None
        else str(existing.get("raw_prompt_text") or "")
    )
    payload = {
        "state": state,
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "message": message,
        "max_retries": resolved_max_retries,
        "placeholder_mode": resolved_placeholder_mode,
        "skip_coordinate_detection": resolved_skip_coordinate_detection,
        "custom_prompt_text": resolved_custom_prompt_text,
        "raw_prompt_only_enabled": resolved_raw_prompt_only_enabled,
        "raw_prompt_text": resolved_raw_prompt_text,
    }
    CONTROL_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTROL_STATE_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return {
        "state": state,
        "updated_at": str(payload["updated_at"]),
        "message": message,
        "max_retries": str(resolved_max_retries),
        "placeholder_mode": resolved_placeholder_mode,
        "skip_coordinate_detection": "true" if resolved_skip_coordinate_detection else "false",
        "custom_prompt_text": resolved_custom_prompt_text,
        "raw_prompt_only_enabled": "true" if resolved_raw_prompt_only_enabled else "false",
        "raw_prompt_text": resolved_raw_prompt_text,
    }


def _load_prompt_settings() -> dict[str, object]:
    if not PROMPT_SETTINGS_PATH.exists():
        return _normalize_prompt_settings(None)

    try:
        parsed = json.loads(PROMPT_SETTINGS_PATH.read_text(encoding="utf-8"))
        if not isinstance(parsed, dict):
            return _normalize_prompt_settings(None)
        return _normalize_prompt_settings(parsed)
    except Exception:
        return _normalize_prompt_settings(None)


def _save_prompt_settings(payload: dict[str, object]) -> dict[str, object]:
    merged = _normalize_prompt_settings(payload)

    PROMPT_SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROMPT_SETTINGS_PATH.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    return merged


def _serialize_generation_job(job: MockupBaseGenerationJob) -> dict[str, object]:
    prompt_metadata = _extract_prompt_metadata(job.prompt_text)
    prompt_raw = str(job.prompt_text or "")
    prompt_text_only = prompt_raw
    if prompt_raw.startswith(PROMPT_METADATA_PREFIX):
        _metadata_line, _sep, remainder = prompt_raw.partition("\n")
        prompt_text_only = remainder if _sep else ""
    preview_url = ""
    started_at = cast(datetime | None, job.started_at)
    finished_at = cast(datetime | None, job.finished_at)
    updated_at = cast(datetime | None, job.updated_at)
    if job.id is not None and str(job.status) == "Completed" and str(job.generated_image_path or "").strip():
        try:
            preview_url = url_for("mockup_generator.generated_job_image", job_id=cast(int, job.id))
        except Exception:
            preview_url = ""

    def _format_adelaide(value: datetime | None) -> str:
        if value is None:
            return ""
        normalized = value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
        return normalized.astimezone(ZoneInfo("Australia/Adelaide")).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "id": cast(int | None, job.id),
        "job_id": str(job.job_id),
        "aspect_ratio": str(job.aspect_ratio),
        "category": str(job.category),
        "variation_index": cast(int, job.variation_index),
        "status": str(job.status),
        "stage": str(job.stage or ""),
        "reason": str(job.reason or ""),
        "error_message": str(job.error_message or ""),
        "attempts": cast(int, job.attempts or 0),
        "generated_image_path": str(job.generated_image_path or ""),
        "image_preview_url": preview_url,
        "started_at": started_at.isoformat() if started_at else "",
        "started_at_adelaide": _format_adelaide(started_at),
        "finished_at": finished_at.isoformat() if finished_at else "",
        "updated_at": updated_at.isoformat() if updated_at else "",
        "finished_at_adelaide": _format_adelaide(finished_at),
        "updated_at_adelaide": _format_adelaide(updated_at),
        "placeholder_mode": prompt_metadata["placeholder_mode"],
        "guide_path": prompt_metadata["guide_path"],
        "submitted_prompt_text": prompt_text_only,
        "submitted_guide_image": prompt_metadata["guide_path"],
    }


def _collect_generator_snapshot(session) -> dict[str, object]:
    status_counts = {}
    for status in (
        "Pending",
        "Generating",
        "Processing",
        "ProcessingCoordinates",
        "Completed",
        "Failed",
    ):
        status_counts[status] = session.query(MockupBaseGenerationJob).filter_by(status=status).count()

    recent_failed_jobs = [
        _serialize_generation_job(row)
        for row in (
            session.query(MockupBaseGenerationJob)
            .filter_by(status="Failed")
            .order_by(MockupBaseGenerationJob.updated_at.desc(), MockupBaseGenerationJob.id.desc())
            .limit(RECENT_FAILURE_LIMIT)
            .all()
        )
    ]

    recent_completed_jobs = [
        _serialize_generation_job(row)
        for row in (
            session.query(MockupBaseGenerationJob)
            .filter_by(status="Completed")
            .order_by(MockupBaseGenerationJob.updated_at.desc(), MockupBaseGenerationJob.id.desc())
            .limit(RECENT_COMPLETED_LIMIT)
            .all()
        )
    ]

    recent_attempt_logs = [
        _serialize_generation_job(row)
        for row in (
            session.query(MockupBaseGenerationJob)
            .filter(MockupBaseGenerationJob.status.in_(["Completed", "Failed"]))
            .order_by(MockupBaseGenerationJob.updated_at.desc(), MockupBaseGenerationJob.id.desc())
            .limit(RECENT_ATTEMPT_LIMIT)
            .all()
        )
    ]

    total_jobs = sum(status_counts.values())
    completed_jobs = status_counts.get("Completed", 0)
    failed_jobs = status_counts.get("Failed", 0)
    active_jobs = (
        status_counts.get("Generating", 0)
        + status_counts.get("Processing", 0)
        + status_counts.get("ProcessingCoordinates", 0)
    )
    pending_jobs = status_counts.get("Pending", 0)
    completion_percentage = int((completed_jobs / total_jobs) * 100) if total_jobs > 0 else 0

    # Retry-queued sub-count: Pending jobs sitting in a rate-limit retry countdown.
    retry_queued_count = (
        session.query(MockupBaseGenerationJob)
        .filter_by(status="Pending", stage="RetryQueued")
        .count()
    )

    # Currently active job (the one the worker is actually processing right now).
    active_job_row = (
        session.query(MockupBaseGenerationJob)
        .filter(MockupBaseGenerationJob.status.in_(["Generating", "Processing", "ProcessingCoordinates"]))
        .order_by(MockupBaseGenerationJob.updated_at.desc())
        .first()
    )
    active_job: dict | None = None
    if active_job_row is not None:
        now_utc = datetime.utcnow()
        started = active_job_row.started_at or active_job_row.updated_at
        running_seconds = int((now_utc - started).total_seconds()) if started else 0
        active_job = _serialize_generation_job(active_job_row)
        active_job["running_seconds"] = running_seconds

    # Upcoming pending items — fetch a pool and split into normal vs retry-queued.
    upcoming_rows = (
        session.query(MockupBaseGenerationJob)
        .filter_by(status="Pending")
        .order_by(MockupBaseGenerationJob.id.asc())
        .limit(20)
        .all()
    )
    next_pending = [_serialize_generation_job(r) for r in upcoming_rows if str(r.stage or "") != "RetryQueued"][:10]
    retry_queued_jobs = [_serialize_generation_job(r) for r in upcoming_rows if str(r.stage or "") == "RetryQueued"][:5]

    return {
        "status_counts": status_counts,
        "recent_failed_jobs": recent_failed_jobs,
        "recent_completed_jobs": recent_completed_jobs,
        "recent_attempt_logs": recent_attempt_logs,
        "total_jobs": total_jobs,
        "completed_jobs": completed_jobs,
        "failed_jobs": failed_jobs,
        "active_jobs": active_jobs,
        "pending_jobs": pending_jobs,
        "completion_percentage": completion_percentage,
        "retry_queued_count": retry_queued_count,
        "active_job": active_job,
        "next_pending": next_pending,
        "retry_queued_jobs": retry_queued_jobs,
    }


def _resolve_scope_filters(data: dict[str, object]) -> tuple[list[str], list[str], str]:
    mode = str(data.get("mode") or "full_batch")
    selected_aspect = str(data.get("aspect_ratio") or "").strip()
    selected_category = str(data.get("category") or "").strip()

    if mode == "full_batch":
        return list(MockupBaseGenerationCatalog.ASPECT_RATIOS), list(MockupBaseGenerationCatalog.CATEGORIES), mode

    if mode == "aspect_only":
        if selected_aspect not in MockupBaseGenerationCatalog.ASPECT_RATIOS:
            raise ValueError("Select a valid aspect ratio for aspect-only generation")
        return [selected_aspect], list(MockupBaseGenerationCatalog.CATEGORIES), mode

    if mode == "category_only":
        if selected_category not in MockupBaseGenerationCatalog.CATEGORIES:
            raise ValueError("Select a valid category for category-only generation")
        return list(MockupBaseGenerationCatalog.ASPECT_RATIOS), [selected_category], mode

    if mode == "aspect_and_category":
        if selected_aspect not in MockupBaseGenerationCatalog.ASPECT_RATIOS:
            raise ValueError("Select a valid aspect ratio")
        if selected_category not in MockupBaseGenerationCatalog.CATEGORIES:
            raise ValueError("Select a valid category")
        return [selected_aspect], [selected_category], mode

    raise ValueError(f"Invalid mode '{mode}'")


def _resolve_quantity(data: dict[str, object]) -> int:
    raw_quantity = data.get("quantity", MockupBaseGenerationCatalog.VARIATION_MAX_INDEX)
    try:
        if isinstance(raw_quantity, bool):
            raise ValueError("Quantity must be an integer")
        if isinstance(raw_quantity, int):
            quantity = raw_quantity
        elif isinstance(raw_quantity, str):
            quantity = int(raw_quantity)
        else:
            raise ValueError("Quantity must be an integer")
    except (TypeError, ValueError) as exc:
        raise ValueError("Quantity must be an integer") from exc

    if quantity not in QUANTITY_OPTIONS:
        raise ValueError(
            f"Quantity must be one of: {', '.join(str(option) for option in QUANTITY_OPTIONS)}"
        )

    if quantity > MockupBaseGenerationCatalog.VARIATION_MAX_INDEX:
        raise ValueError(
            "Current pipeline supports up to 20 variations. Raise the Stage 1 contract before using 25 or 30."
        )

    return quantity


@mockup_generator_bp.route("/mockup-generator", methods=["GET"])
def mockup_generator_dashboard():
    """Display the mockup generator control center dashboard.

    Queries the database to fetch current generation status:
    - Total count by status: Pending, Generating, ProcessingCoordinates, Completed, Failed
    - Displays real-time pipeline metrics
    - Provides button to trigger batch generation (Stage 4 - Celery job submission)
    """
    try:
        session = SessionLocal()
        try:
            snapshot = _collect_generator_snapshot(session)

            logger.info(
                f"Dashboard loaded: {snapshot['total_jobs']} total, "
                f"{snapshot['active_jobs']} active, {snapshot['pending_jobs']} pending"
            )

            control_state = _load_control_state()

            return render_template(
                "mockups/mockup_generator_dashboard.html",
                status_counts=snapshot["status_counts"],
                total_jobs=snapshot["total_jobs"],
                active_jobs=snapshot["active_jobs"],
                pending_jobs=snapshot["pending_jobs"],
                completed_jobs=snapshot["completed_jobs"],
                failed_jobs=snapshot["failed_jobs"],
                completion_percentage=snapshot["completion_percentage"],
                retry_queued_count=snapshot["retry_queued_count"],
                active_job=snapshot["active_job"],
                next_pending=snapshot["next_pending"],
                retry_queued_jobs=snapshot["retry_queued_jobs"],
                recent_failed_jobs=snapshot["recent_failed_jobs"],
                recent_completed_jobs=snapshot["recent_completed_jobs"],
                recent_attempt_logs=snapshot["recent_attempt_logs"],
                max_variations=MockupBaseGenerationCatalog.VARIATION_MAX_INDEX,
                expected_total=(
                    len(MockupBaseGenerationCatalog.ASPECT_RATIOS)
                    * len(MockupBaseGenerationCatalog.CATEGORIES)
                    * MockupBaseGenerationCatalog.VARIATION_MAX_INDEX
                ),
                num_aspects=len(MockupBaseGenerationCatalog.ASPECT_RATIOS),
                num_categories=len(MockupBaseGenerationCatalog.CATEGORIES),
                aspect_ratios=list(MockupBaseGenerationCatalog.ASPECT_RATIOS),
                categories=list(MockupBaseGenerationCatalog.CATEGORIES),
                quantity_options=list(QUANTITY_OPTIONS),
                control_state=control_state,
                saved_max_retries=int(control_state.get("max_retries") or DEFAULT_MAX_RETRIES),
                saved_placeholder_mode=_sanitize_placeholder_mode(control_state.get("placeholder_mode")),
                worker_running=_celery_worker_running(),
            )
        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error loading mockup generator dashboard: {str(e)}", exc_info=True)
        flash("Error loading dashboard. Check server logs.", "error")
        control_state = _load_control_state()
        return render_template(
            "mockups/mockup_generator_dashboard.html",
            error=str(e),
            status_counts={
                "Pending": 0,
                "Generating": 0,
                "ProcessingCoordinates": 0,
                "Processing": 0,
                "Completed": 0,
                "Failed": 0,
            },
            total_jobs=0,
            active_jobs=0,
            pending_jobs=0,
            completed_jobs=0,
            failed_jobs=0,
            completion_percentage=0,
            recent_failed_jobs=[],
            recent_completed_jobs=[],
            recent_attempt_logs=[],
            max_variations=MockupBaseGenerationCatalog.VARIATION_MAX_INDEX,
            expected_total=(
                len(MockupBaseGenerationCatalog.ASPECT_RATIOS)
                * len(MockupBaseGenerationCatalog.CATEGORIES)
                * MockupBaseGenerationCatalog.VARIATION_MAX_INDEX
            ),
            num_aspects=len(MockupBaseGenerationCatalog.ASPECT_RATIOS),
            num_categories=len(MockupBaseGenerationCatalog.CATEGORIES),
            aspect_ratios=list(MockupBaseGenerationCatalog.ASPECT_RATIOS),
            categories=list(MockupBaseGenerationCatalog.CATEGORIES),
            quantity_options=list(QUANTITY_OPTIONS),
            control_state=control_state,
            saved_max_retries=int(control_state.get("max_retries") or DEFAULT_MAX_RETRIES),
            saved_placeholder_mode=_sanitize_placeholder_mode(control_state.get("placeholder_mode")),
            worker_running=_celery_worker_running(),
            prompt_settings=_load_prompt_settings(),
        )


@mockup_generator_bp.route("/mockup-generator/prompt-settings", methods=["GET", "POST"])
def mockup_generator_prompt_settings():
    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            if resp is None:
                abort(400)
            return resp

        payload: dict[str, object] = {
            "standard_prefix": request.form.get("standard_prefix", ""),
            "standard_suffix": request.form.get("standard_suffix", ""),
            "outlined_prefix": request.form.get("outlined_prefix", ""),
            "outlined_suffix": request.form.get("outlined_suffix", ""),
            "generation_canvas_aspect_ratio": request.form.get("generation_canvas_aspect_ratio", "1x1"),
            "default_style": request.form.get("default_style", "Contemporary"),
            "default_tone": request.form.get("default_tone", "Warm"),
            "default_season": request.form.get("default_season", "Any"),
        }
        saved = _save_prompt_settings(payload)
        flash("Mockup generator prompt settings saved.", "success")
        return render_template(
            "mockups/mockup_generator_prompt_settings.html",
            settings=saved,
            aspect_ratios=list(MockupBaseGenerationCatalog.ASPECT_RATIOS),
            categories=list(MockupBaseGenerationCatalog.CATEGORIES),
            style_options=list(STYLE_OPTIONS),
            tone_options=list(TONE_OPTIONS),
            season_options=list(SEASON_OPTIONS),
            prompt_examples=_build_prompt_examples(saved),
            csrf_token=get_csrf_token(),
        )

    settings = _load_prompt_settings()
    return render_template(
        "mockups/mockup_generator_prompt_settings.html",
        settings=settings,
        aspect_ratios=list(MockupBaseGenerationCatalog.ASPECT_RATIOS),
        categories=list(MockupBaseGenerationCatalog.CATEGORIES),
        style_options=list(STYLE_OPTIONS),
        tone_options=list(TONE_OPTIONS),
        season_options=list(SEASON_OPTIONS),
        prompt_examples=_build_prompt_examples(settings),
        csrf_token=get_csrf_token(),
    )


@mockup_generator_bp.route("/mockup-generator/prompt-preview", methods=["POST"])
def mockup_generator_prompt_preview():
    """Return the full compiled prompt text that would be sent to Gemini, for live preview."""
    try:
        data = request.get_json() or {}
        custom_prompt_text = str(data.get("custom_prompt_text") or "").strip()
        preview_variation_index = 1
        try:
            preview_variation_index = max(1, int(data.get("variation_index") or 1))
        except (TypeError, ValueError):
            preview_variation_index = 1

        requested_mode = data.get("placeholder_mode") or data.get("generation_mode")
        generation_mode = _resolve_generation_mode_from_placeholder(_sanitize_placeholder_mode(requested_mode))

        settings = _normalize_prompt_settings({
            "standard_prefix": data.get("standard_prefix", ""),
            "standard_suffix": data.get("standard_suffix", ""),
            "outlined_prefix": data.get("outlined_prefix", ""),
            "outlined_suffix": data.get("outlined_suffix", ""),
            "generation_canvas_aspect_ratio": data.get("generation_canvas_aspect_ratio", DEFAULT_CANVAS_ASPECT),
            "default_style": data.get("default_style", "Contemporary"),
            "default_tone": data.get("default_tone", "Warm"),
            "default_season": data.get("default_season", "Any"),
        })

        category = str(data.get("category") or MockupBaseGenerationCatalog.CATEGORIES[0])
        if category not in MockupBaseGenerationCatalog.CATEGORIES:
            category = MockupBaseGenerationCatalog.CATEGORIES[0]

        aspect_ratio = str(data.get("aspect_ratio") or MockupBaseGenerationCatalog.ASPECT_RATIOS[0])
        if aspect_ratio not in MockupBaseGenerationCatalog.ASPECT_RATIOS:
            aspect_ratio = str(MockupBaseGenerationCatalog.ASPECT_RATIOS[0])

        from application.mockups.tasks_mockup_generator import (
            _build_artwork_trojan_prompt,
            _build_artwork_only_composite_prompt,
            _build_chromakey_prompt,
            _render_custom_prompt,
            _apply_prompt_wrapper,
            _apply_environment_modifiers,
            TROJAN_ARTWORK_DIR,
            ARTWORK_ONLY_GUIDE_DIR,
        )

        if generation_mode == GENERATION_MODE_ARTWORK_ONLY_COMPOSITE:
            body = _build_artwork_only_composite_prompt(
                category=category,
                variation_index=preview_variation_index,
                aspect_ratio=aspect_ratio,
            )
            prompt_text = body
            guide_path = ARTWORK_ONLY_GUIDE_DIR / f"{aspect_ratio}-artwork-placeholder.png"
        elif generation_mode == GENERATION_MODE_CHROMAKEY_AUTO:
            body = _build_chromakey_prompt(
                category=category,
                variation_index=preview_variation_index,
                aspect_ratio=aspect_ratio,
                chromakey_hex="#00FFCC",
            )
            prompt_text = _apply_prompt_wrapper(
                str(settings.get("standard_prefix") or ""),
                body,
                str(settings.get("standard_suffix") or ""),
            )
            prompt_text = _apply_environment_modifiers(prompt_text, settings)
            guide_path = None
        else:
            body = _build_artwork_trojan_prompt(category=category, variation_index=preview_variation_index)
            prompt_text = _apply_prompt_wrapper(
                str(settings.get("outlined_prefix") or ""),
                body,
                str(settings.get("outlined_suffix") or ""),
            )
            prompt_text = _apply_environment_modifiers(prompt_text, settings)
            guide_path = TROJAN_ARTWORK_DIR / f"{aspect_ratio}-outlined-artwork.png"

        if custom_prompt_text:
            prompt_text = _render_custom_prompt(
                custom_prompt_text,
                aspect_ratio=aspect_ratio,
                category=category,
                variation_index=preview_variation_index,
            )

        if guide_path is None:
            guide_note = "No reference image sent; chromakey region is specified in prompt instructions."
        else:
            exists_flag = " [FILE NOT FOUND]" if not guide_path.exists() else ""
            guide_note = f"Reference image sent alongside prompt: {guide_path}{exists_flag}"

        return jsonify({
            "prompt_text": prompt_text,
            "guide_note": guide_note,
            "generation_mode": generation_mode,
            "category": category,
            "aspect_ratio": aspect_ratio,
        }), 200

    except Exception as e:
        logger.error("Error building prompt preview: %s", str(e), exc_info=True)
        return jsonify({"error": str(e)}), 500


@mockup_generator_bp.route("/mockup-generator/start-pipeline", methods=["POST"])
def start_generation_pipeline():
    """Trigger batch generation pipeline (Stage 4 - Celery job).

    This endpoint is a placeholder for Stage 4 implementation.
    Currently validates request and logs intent.

    Returns:
        JSON response with job ID or error message
    """
    try:
        data = request.get_json() or {}
        run_inline_single = bool(data.get("run_inline_single") is True)

        control_state = _load_control_state().get("state", "running")
        if control_state == "stopped":
            return jsonify({"error": "Pipeline is stopped. Resume before queueing new jobs."}), 409

        # Persist control selections from the UI selector immediately.
        raw_mr = data.get("max_retries")
        raw_placeholder_mode = data.get("placeholder_mode")
        raw_custom_prompt_text = str(data.get("custom_prompt_text") or "").strip()
        raw_prompt_only_enabled = bool(data.get("raw_prompt_only_enabled") is True)
        raw_prompt_text = str(data.get("raw_prompt_text") or "")
        new_max_retries: int | None = None
        if raw_mr is not None:
            try:
                new_max_retries = max(1, min(20, int(raw_mr)))
            except (TypeError, ValueError):
                new_max_retries = None
        new_placeholder_mode = _sanitize_placeholder_mode(raw_placeholder_mode)
        if raw_prompt_only_enabled:
            # Raw prompt-only mode targets plain composite guide flow.
            new_placeholder_mode = GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
        generation_mode = _resolve_generation_mode_from_placeholder(new_placeholder_mode)
        _save_control_state(
            control_state,
            "control settings updated",
            max_retries=new_max_retries,
            placeholder_mode=new_placeholder_mode,
            custom_prompt_text=raw_custom_prompt_text,
            raw_prompt_only_enabled=raw_prompt_only_enabled,
            raw_prompt_text=raw_prompt_text,
        )

        retry_failed = bool(data.get("retry_failed") is True)
        aspect_ratios, categories, mode = _resolve_scope_filters(data)
        quantity = _resolve_quantity(data)

        session = SessionLocal()
        try:
            if generation_mode == GENERATION_MODE_STANDARD:
                mode_filter = or_(
                    MockupBaseGenerationJob.generation_mode == GENERATION_MODE_STANDARD,
                    MockupBaseGenerationJob.generation_mode.is_(None),
                )
            else:
                mode_filter = MockupBaseGenerationJob.generation_mode == generation_mode

            existing_rows = (
                session.query(MockupBaseGenerationJob)
                .filter(MockupBaseGenerationJob.aspect_ratio.in_(aspect_ratios))
                .filter(MockupBaseGenerationJob.category.in_(categories))
                .filter(mode_filter)
                .all()
            )

            existing_map: dict[tuple[str, str, int], MockupBaseGenerationJob] = {
                (
                    str(row.aspect_ratio),
                    str(row.category),
                    cast(int, row.variation_index),
                ): row
                for row in existing_rows
            }

            created = 0
            retried = 0
            for aspect_ratio in aspect_ratios:
                for category in categories:
                    for variation_index in range(
                        MockupBaseGenerationCatalog.VARIATION_MIN_INDEX,
                        quantity + 1,
                    ):
                        key = (aspect_ratio, category, variation_index)
                        existing = existing_map.get(key)
                        if existing is None:
                            row = MockupBaseGenerationJob(
                                job_id=_make_mode_job_external_id(
                                    aspect_ratio=aspect_ratio,
                                    category=category,
                                    variation_index=variation_index,
                                    generation_mode=generation_mode,
                                ),
                                aspect_ratio=aspect_ratio,
                                category=category,
                                variation_index=variation_index,
                                generation_mode=generation_mode,
                                status="Pending",
                                stage="Queued",
                                attempts=0,
                            )
                            session.add(row)
                            created += 1
                            continue

                        if generation_mode == GENERATION_MODE_STANDARD and not str(existing.generation_mode or "").strip():
                            existing.generation_mode = GENERATION_MODE_STANDARD  # type: ignore[assignment]

                        if retry_failed and str(existing.status) == "Failed":
                            existing.status = "Pending"  # type: ignore[assignment]
                            existing.stage = "Queued"  # type: ignore[assignment]
                            existing.error_message = None  # type: ignore[assignment]
                            existing.reason = None  # type: ignore[assignment]
                            existing.finished_at = None  # type: ignore[assignment]
                            retried += 1

            session.commit()
        finally:
            session.close()

        dispatch_job_ids: list[int] = []
        session = SessionLocal()
        try:
            if generation_mode == GENERATION_MODE_STANDARD:
                dispatch_mode_filter = or_(
                    MockupBaseGenerationJob.generation_mode == GENERATION_MODE_STANDARD,
                    MockupBaseGenerationJob.generation_mode.is_(None),
                )
            else:
                dispatch_mode_filter = MockupBaseGenerationJob.generation_mode == generation_mode

            pending_rows = (
                session.query(MockupBaseGenerationJob)
                .filter(MockupBaseGenerationJob.aspect_ratio.in_(aspect_ratios))
                .filter(MockupBaseGenerationJob.category.in_(categories))
                .filter(
                    MockupBaseGenerationJob.variation_index >= MockupBaseGenerationCatalog.VARIATION_MIN_INDEX
                )
                .filter(MockupBaseGenerationJob.variation_index <= quantity)
                .filter(dispatch_mode_filter)
                .filter_by(status="Pending")
                .all()
            )
            dispatch_job_ids = [cast(int, row.id) for row in pending_rows if row.id is not None]
        finally:
            session.close()

        dispatched = 0
        dispatch_errors: list[str] = []
        inline_result: dict[str, object] | None = None
        if dispatch_job_ids:
            from application.mockups.tasks_mockup_generator import process_mockup_job
            if run_inline_single and len(dispatch_job_ids) == 1:
                target_job_id = dispatch_job_ids[0]
                try:
                    # Single-test fallback: execute one queued job in-process.
                    exec_result = process_mockup_job.apply(args=(target_job_id,))
                    payload = exec_result.get() if hasattr(exec_result, "get") else None
                    inline_result = payload if isinstance(payload, dict) else {"status": "completed"}
                    dispatched = 1
                except Exception as exc:
                    dispatch_errors.append(f"job {target_job_id}: {exc}")
            else:
                for target_job_id in dispatch_job_ids:
                    try:
                        process_mockup_job.delay(target_job_id)
                        dispatched += 1
                    except Exception as exc:
                        dispatch_errors.append(f"job {target_job_id}: {exc}")

        if dispatch_errors and dispatched == 0:
            logger.error(
                "Generation dispatch failed for all queued jobs: %s",
                "; ".join(dispatch_errors),
            )
            return jsonify(
                {
                    "error": "Queue rows were created, but no background tasks could be dispatched.",
                    "dispatch_errors": dispatch_errors[:10],
                    "created": created,
                    "retried": retried,
                    "pending_jobs": len(dispatch_job_ids),
                }
            ), 503

        scope_total = (
            len(aspect_ratios)
            * len(categories)
            * quantity
        )

        logger.info(
            "Generation queue prepared: mode=%s generation_mode=%s placeholder_mode=%s scope_total=%s created=%s retried=%s retry_failed=%s",
            mode,
            generation_mode,
            new_placeholder_mode,
            scope_total,
            created,
            retried,
            retry_failed,
        )

        return jsonify(
            {
                "status": "pending",
                "message": "Queue prepared successfully",
                "mode": mode,
                "generation_mode": generation_mode,
                "placeholder_mode": new_placeholder_mode,
                "custom_prompt_enabled": bool(raw_custom_prompt_text),
                "raw_prompt_only_enabled": raw_prompt_only_enabled,
                "scope_total": scope_total,
                "quantity": quantity,
                "created": created,
                "retried": retried,
                "dispatched": dispatched,
                "pending_jobs": len(dispatch_job_ids),
                "retry_failed": retry_failed,
                "run_inline_single": run_inline_single,
                "inline_result": inline_result,
                "worker_running": _celery_worker_running(),
                "dispatch_errors": dispatch_errors[:10],
            }
        ), 202

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"Error starting generation pipeline: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@mockup_generator_bp.route("/mockup-generator/control", methods=["POST"])
def control_generation_pipeline():
    """Pause, resume, or stop the pipeline via persisted control state."""
    try:
        payload = request.get_json() or {}
        action = str(payload.get("action") or "").strip().lower()
        if action not in {"pause", "resume", "stop", "set_skip_coordinate_detection"}:
            return jsonify({"error": f"Invalid action '{action}'"}), 400

        if action == "pause":
            state = _save_control_state("paused", "Pause requested by operator")
        elif action == "resume":
            state = _save_control_state("running", "Resume requested by operator")
        elif action == "set_skip_coordinate_detection":
            enabled = bool(payload.get("skip_coordinate_detection") is True)
            current_state = _load_control_state().get("state", "running")
            msg = "Coordinate detection disabled (fallback coordinates enabled)." if enabled else "Coordinate detection enabled."
            state = _save_control_state(
                current_state,
                msg,
                skip_coordinate_detection=enabled,
            )
        else:
            state = _save_control_state("stopped", "Stop requested by operator")

        return jsonify({"status": "ok", "control_state": state}), 200
    except Exception as e:
        logger.error(f"Error controlling pipeline: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@mockup_generator_bp.route("/mockup-generator/clear-pending", methods=["POST"])
def clear_pending_generation_jobs():
    """Delete pending jobs and reset any stale Generating/Processing jobs back to Pending."""
    try:
        session = SessionLocal()
        try:
            cleared = (
                session.query(MockupBaseGenerationJob)
                .filter_by(status="Pending")
                .delete(synchronize_session=False)
            )
            # Reset orphaned active jobs (worker was killed while processing them).
            stale = (
                session.query(MockupBaseGenerationJob)
                .filter(MockupBaseGenerationJob.status.in_(["Generating", "Processing", "ProcessingCoordinates"]))
                .all()
            )
            reset_count = 0
            for job in stale:
                job.status = "Pending"  # type: ignore[assignment]
                job.stage = "Queued"  # type: ignore[assignment]
                job.error_message = "Reset from stale active state by operator"  # type: ignore[assignment]
                job.generated_image_path = None  # type: ignore[assignment]
                job.coordinates_path = None  # type: ignore[assignment]
                reset_count += 1
            session.commit()
            snapshot = _collect_generator_snapshot(session)
        finally:
            session.close()

        logger.info("Cleared %s pending + reset %s stale mockup generation jobs", cleared, reset_count)
        return jsonify(
            {
                "status": "ok",
                "cleared": int(cleared or 0),
                "stale_reset": reset_count,
                "status_counts": snapshot["status_counts"],
                "recent_failed_jobs": snapshot["recent_failed_jobs"],
                "recent_completed_jobs": snapshot["recent_completed_jobs"],
                "total_jobs": snapshot["total_jobs"],
                "control_state": _load_control_state(),
            }
        ), 200
    except Exception as e:
        logger.error("Error clearing pending generation jobs: %s", str(e), exc_info=True)
        return jsonify({"error": str(e)}), 500


@mockup_generator_bp.route("/mockup-generator/clear-failed", methods=["POST"])
def clear_failed_generation_jobs():
    """Delete failed jobs and return refreshed dashboard status."""
    try:
        session = SessionLocal()
        try:
            cleared = (
                session.query(MockupBaseGenerationJob)
                .filter_by(status="Failed")
                .delete(synchronize_session=False)
            )
            session.commit()
            snapshot = _collect_generator_snapshot(session)
        finally:
            session.close()

        logger.info("Cleared %s failed mockup generation jobs", cleared)
        return jsonify(
            {
                "status": "ok",
                "cleared": int(cleared or 0),
                "status_counts": snapshot["status_counts"],
                "recent_failed_jobs": snapshot["recent_failed_jobs"],
                "recent_completed_jobs": snapshot["recent_completed_jobs"],
                "total_jobs": snapshot["total_jobs"],
                "control_state": _load_control_state(),
            }
        ), 200
    except Exception as e:
        logger.error("Error clearing failed generation jobs: %s", str(e), exc_info=True)
        return jsonify({"error": str(e)}), 500


@mockup_generator_bp.route("/mockup-generator/delete-completed", methods=["POST"])
def delete_completed_generation_jobs():
    """Delete selected completed jobs and remove their generated output files where possible."""
    try:
        payload = request.get_json(silent=True) or {}
        raw_job_ids = payload.get("job_ids") if isinstance(payload, dict) else []
        if not isinstance(raw_job_ids, list):
            return jsonify({"error": "job_ids must be a list of integer IDs"}), 400

        requested_ids = [int(v) for v in raw_job_ids if str(v).isdigit() and int(v) > 0]
        if not requested_ids:
            return jsonify({"error": "No valid completed job IDs were provided"}), 400

        requested_ids = list(dict.fromkeys(requested_ids))[:200]

        allowed_roots = (
            Path("/srv/artlomo/application/mockups/catalog/assets/mockups/bases").resolve(),
            Path("/srv/artlomo/var/coordinates").resolve(),
        )

        def _safe_delete(path_text: str) -> bool:
            raw = str(path_text or "").strip()
            if not raw:
                return False
            try:
                target = Path(raw).resolve()
            except Exception:
                return False
            if not any(str(target).startswith(str(root)) for root in allowed_roots):
                return False
            if not target.exists() or not target.is_file():
                return False
            try:
                target.unlink(missing_ok=True)
                return True
            except Exception:
                return False

        session = SessionLocal()
        try:
            rows = (
                session.query(MockupBaseGenerationJob)
                .filter(MockupBaseGenerationJob.id.in_(requested_ids))
                .filter_by(status="Completed")
                .all()
            )

            file_delete_count = 0
            for row in rows:
                if _safe_delete(str(row.generated_image_path or "")):
                    file_delete_count += 1
                if _safe_delete(str(row.coordinates_path or "")):
                    file_delete_count += 1

            deleted_job_count = len(rows)
            if rows:
                row_ids = [cast(int, row.id) for row in rows if row.id is not None]
                session.query(MockupBaseGenerationJob).filter(MockupBaseGenerationJob.id.in_(row_ids)).delete(synchronize_session=False)

            session.commit()
            snapshot = _collect_generator_snapshot(session)
        finally:
            session.close()

        logger.info(
            "Deleted completed jobs: requested=%s deleted=%s deleted_files=%s",
            len(requested_ids),
            deleted_job_count,
            file_delete_count,
        )
        return jsonify(
            {
                "status": "ok",
                "requested": len(requested_ids),
                "cleared": deleted_job_count,
                "deleted_files": file_delete_count,
                "status_counts": snapshot["status_counts"],
                "recent_failed_jobs": snapshot["recent_failed_jobs"],
                "recent_completed_jobs": snapshot["recent_completed_jobs"],
                "total_jobs": snapshot["total_jobs"],
                "control_state": _load_control_state(),
            }
        ), 200
    except Exception as e:
        logger.error("Error deleting completed generation jobs: %s", str(e), exc_info=True)
        return jsonify({"error": str(e)}), 500


@mockup_generator_bp.route("/mockup-generator/approve-completed", methods=["POST"])
def approve_completed_generation_jobs():
    """Publish selected completed jobs to live catalog and remove them from preview queue."""
    try:
        payload = request.get_json(silent=True) or {}
        raw_job_ids = payload.get("job_ids") if isinstance(payload, dict) else []
        if not isinstance(raw_job_ids, list):
            return jsonify({"error": "job_ids must be a list of integer IDs"}), 400

        requested_ids = [int(v) for v in raw_job_ids if str(v).isdigit() and int(v) > 0]
        if not requested_ids:
            return jsonify({"error": "No valid completed job IDs were provided"}), 400
        requested_ids = list(dict.fromkeys(requested_ids))[:200]

        catalog = CatalogAdminService()

        session = SessionLocal()
        try:
            rows = (
                session.query(MockupBaseGenerationJob)
                .filter(MockupBaseGenerationJob.id.in_(requested_ids))
                .filter_by(status="Completed")
                .all()
            )

            approved = 0
            skipped = 0
            failures: list[str] = []
            deletable_row_ids: list[int] = []

            for row in rows:
                row_id = cast(int | None, row.id)
                if row_id is None:
                    skipped += 1
                    continue

                source_job_id = str(row.job_id or "").strip()
                if not source_job_id:
                    skipped += 1
                    continue

                try:
                    base_entry = next(
                        (
                            b
                            for b in catalog.load_bases()
                            if str(getattr(b, "source_job_id", "") or "").strip() == source_job_id
                        ),
                        None,
                    )
                    if base_entry is None:
                        skipped += 1
                        failures.append(f"job {row_id}: base not found for source_job_id={source_job_id}")
                        continue

                    catalog.set_base_live_state(str(base_entry.id), live=True)
                    approved += 1
                    deletable_row_ids.append(row_id)
                except ValidationError as exc:
                    skipped += 1
                    failures.append(f"job {row_id}: {exc}")
                except Exception as exc:
                    skipped += 1
                    failures.append(f"job {row_id}: {exc}")

            if deletable_row_ids:
                session.query(MockupBaseGenerationJob).filter(
                    MockupBaseGenerationJob.id.in_(deletable_row_ids)
                ).delete(synchronize_session=False)

            session.commit()
            snapshot = _collect_generator_snapshot(session)
        finally:
            session.close()

        logger.info(
            "Approved completed jobs to live: requested=%s approved=%s skipped=%s",
            len(requested_ids),
            approved,
            skipped,
        )
        return jsonify(
            {
                "status": "ok",
                "requested": len(requested_ids),
                "approved": approved,
                "skipped": skipped,
                "failures": failures[:20],
                "status_counts": snapshot["status_counts"],
                "recent_failed_jobs": snapshot["recent_failed_jobs"],
                "recent_completed_jobs": snapshot["recent_completed_jobs"],
                "total_jobs": snapshot["total_jobs"],
                "control_state": _load_control_state(),
            }
        ), 200
    except Exception as e:
        logger.error("Error approving completed generation jobs: %s", str(e), exc_info=True)
        return jsonify({"error": str(e)}), 500


@mockup_generator_bp.route("/mockup-generator/jobs/<int:job_id>/force-retry", methods=["POST"])
def force_retry_job(job_id: int):
    """Immediately re-queue a single Retry Queued job, bypassing its countdown.

    Resets stage to 'Queued' in the DB and re-dispatches the Celery task with no
    countdown delay.  The original countdown task in Celery will also fire
    eventually, but process_mockup_job claims the row atomically so the duplicate
    will simply find the job already in-progress and exit cleanly.
    """
    try:
        session = SessionLocal()
        try:
            job = session.get(MockupBaseGenerationJob, job_id)
            if job is None:
                return jsonify({"error": f"Job {job_id} not found"}), 404
            if str(job.status) != "Pending" or str(job.stage or "") != "RetryQueued":
                return jsonify({"error": f"Job {job_id} is not in RetryQueued state (status={job.status} stage={job.stage})"}), 409
            job.stage = "Queued"  # type: ignore[assignment]
            job.reason = None  # type: ignore[assignment]
            session.commit()
            db_job_id = cast(int, job.id)
        finally:
            session.close()

        from application.mockups.tasks_mockup_generator import process_mockup_job
        process_mockup_job.delay(db_job_id)

        logger.info("Force-retried job %s (DB id %s)", job_id, db_job_id)
        return jsonify({"status": "ok", "job_id": job_id}), 200

    except Exception as e:
        logger.error("Error force-retrying job %s: %s", job_id, str(e), exc_info=True)
        return jsonify({"error": str(e)}), 500


@mockup_generator_bp.route("/mockup-generator/status", methods=["GET"])
def get_generator_status():
    """Fetch current generator status as JSON (for AJAX updates).

    Returns:
        JSON object with status counts and completion metrics
    """
    try:
        session = SessionLocal()
        try:
            snapshot = _collect_generator_snapshot(session)

            return jsonify(
                {
                    "status_counts": snapshot["status_counts"],
                    "recent_failed_jobs": snapshot["recent_failed_jobs"],
                    "recent_completed_jobs": snapshot["recent_completed_jobs"],
                    "recent_attempt_logs": snapshot["recent_attempt_logs"],
                    "total_jobs": snapshot["total_jobs"],
                    "retry_queued_count": snapshot["retry_queued_count"],
                    "active_job": snapshot["active_job"],
                    "next_pending": snapshot["next_pending"],
                    "retry_queued_jobs": snapshot["retry_queued_jobs"],
                    "control_state": _load_control_state(),
                    "server_time": datetime.utcnow().isoformat() + "Z",
                }
            )
        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error fetching generator status: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@mockup_generator_bp.route("/mockup-generator/jobs/<int:job_id>/image", methods=["GET"])
def generated_job_image(job_id: int):
    """Serve the generated image file for a completed mockup generation job."""
    try:
        session = SessionLocal()
        try:
            job = session.get(MockupBaseGenerationJob, job_id)
            if job is None:
                abort(404)

            generated_image_path = Path(str(job.generated_image_path or "")).resolve()
            base_dir = Path("/srv/artlomo/application/mockups/catalog/assets/mockups/bases").resolve()

            if not str(generated_image_path).startswith(str(base_dir)):
                abort(404)

            if not generated_image_path.exists():
                abort(404)

            return send_file(generated_image_path, mimetype="image/png")
        finally:
            session.close()
    except Exception:
        abort(404)


@mockup_generator_bp.route("/mockup-generator/queue-admin", methods=["GET"])
def mockup_generator_queue_admin_page():
    queue_data = _queue_snapshot(limit=150)

    session = SessionLocal()
    try:
        pending_mockup = int(
            session.query(MockupBaseGenerationJob)
            .filter(MockupBaseGenerationJob.status.in_(["Pending", "Queued", "Generating", "Processing"]))
            .count()
        )
        pending_gemini = int(
            session.query(GeminiStudioJob)
            .filter(GeminiStudioJob.status.in_(["Pending", "Generating"]))
            .count()
        )
    finally:
        session.close()

    return render_template(
        "mockups/mockup_generator_queue_admin.html",
        queue_data=queue_data,
        pending_mockup=pending_mockup,
        pending_gemini=pending_gemini,
        control_state=_load_control_state(),
        worker_running=_celery_worker_running(),
        csrf_token=get_csrf_token(),
    )


@mockup_generator_bp.route("/mockup-generator/queue-admin/action", methods=["POST"])
def mockup_generator_queue_admin_action():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp

    action = str(request.form.get("action") or "").strip().lower()
    task_id = str(request.form.get("task_id") or "").strip()
    task_name = str(request.form.get("task_name") or "").strip()

    try:
        if action == "pause_pipeline":
            _save_control_state("paused", "Paused from Celery Queue Admin")
            flash("Pipeline paused.", "success")
        elif action == "resume_pipeline":
            _save_control_state("running", "Resumed from Celery Queue Admin")
            flash("Pipeline resumed.", "success")
        elif action == "stop_pipeline":
            _save_control_state("stopped", "Stopped from Celery Queue Admin")
            flash("Pipeline stopped.", "warning")
        elif action == "purge_mockups_queue":
            removed, remaining = _rewrite_celery_queue(
                lambda payload: _queue_task_name(payload).startswith("mockups.")
            )
            flash(f"Removed {removed} mockups queue item(s). Remaining queue length: {remaining}.", "success")
        elif action == "purge_task_type":
            if not task_name:
                flash("Task type is required.", "danger")
            else:
                removed, remaining = _rewrite_celery_queue(
                    lambda payload: _queue_task_name(payload) == task_name
                )
                flash(f"Removed {removed} item(s) for task '{task_name}'. Remaining: {remaining}.", "success")
        elif action == "purge_task_id":
            if not task_id:
                flash("Task id is required.", "danger")
            else:
                removed, remaining = _rewrite_celery_queue(
                    lambda payload: _queue_task_id(payload) == task_id
                )
                flash(f"Removed {removed} item(s) for task id '{task_id}'. Remaining: {remaining}.", "success")
        elif action == "purge_orphan_queue":
            removed, remaining = _remove_orphan_queue_items()
            flash(
                f"Removed {removed} orphan queue item(s) with missing DB rows. Remaining queue length: {remaining}.",
                "success",
            )
        elif action == "clear_pending_db_and_files":
            summary = _clear_pending_db_and_files()
            flash(
                "Deleted pending rows and files: "
                f"mockup_rows={summary['removed_mockup_rows']}, "
                f"gemini_rows={summary['removed_gemini_rows']}, "
                f"files={summary['deleted_files']}.",
                "warning",
            )
        else:
            flash(f"Unknown action: {action}", "danger")
    except Exception as exc:
        logger.error("Queue admin action failed: %s", str(exc), exc_info=True)
        flash(f"Queue admin action failed: {str(exc)}", "danger")

    return redirect(url_for("mockup_generator.mockup_generator_queue_admin_page"))


# ============================================================================
# Solid Image Utility Routes
# ============================================================================


@utility_bp.route("/solid-image-generator", methods=["GET"])
def solid_image_generator_form():
    """Display the solid image generator form.

    Provides:
    - Dropdown for 13 aspect ratios
    - HTML5 color picker (default #00FFFF)
    - Form submission to download generated image
    """
    try:
        return render_template(
            "mockups/solid_image_generator.html",
            aspect_ratios=MockupBaseGenerationCatalog.ASPECT_RATIOS,
            default_color="00FFFF",
        )
    except Exception as e:
        logger.error(f"Error rendering solid image form: {str(e)}", exc_info=True)
        flash("Error rendering form. Check server logs.", "error")
        abort(500)


@utility_bp.route("/solid-image-generator", methods=["POST"])
def solid_image_generator_download():
    """Process form submission and return solid image for download.

    Expected POST data:
    - aspect_ratio: One of the 13 standard aspect ratios (e.g., "16:9")
    - color: Hex color code (e.g., "00FFFF" or "#00FFFF")

    Returns:
        PNG image file for download
    """
    try:
        # Get form parameters
        aspect_ratio_key = request.form.get("aspect_ratio", "")
        color_input = request.form.get("color", SolidImageService.DEFAULT_COLOR)

        # Normalize color to remove # if present 
        if color_input.startswith("#"):
            color_input = color_input[1:]

        # Validate aspect ratio
        if aspect_ratio_key not in MockupBaseGenerationCatalog.ASPECT_RATIOS:
            flash(f"Invalid aspect ratio: {aspect_ratio_key}", "error")
            return render_template(
                "mockups/solid_image_generator.html",
                aspect_ratios=MockupBaseGenerationCatalog.ASPECT_RATIOS,
                default_color=color_input,
            ), 400

        # Convert aspect ratio from "XxY" format to "X:Y" format for service
        aspect_ratio_colon = aspect_ratio_key.replace("x", ":")

        logger.info(
            f"Generating solid image: aspect_ratio={aspect_ratio_colon}, "
            f"color={color_input}"
        )

        try:
            # Generate image to BytesIO (in-memory)
            image_buffer = SolidImageService.generate_solid_image(
                aspect_ratio=aspect_ratio_colon,
                color=f"#{color_input}",
                output_path=None,  # Return as BytesIO, not saved to disk
            )

            # Send to client as download
            filename = f"solid_{aspect_ratio_key}_{color_input}.png"
            return send_file(
                image_buffer,
                mimetype="image/png",
                as_attachment=True,
                download_name=filename,
            )

        except (SolidImageValidationError, SolidImageGenerationError) as e:
            logger.error(f"Image generation error: {str(e)}")
            flash(f"Image generation error: {str(e)}", "error")
            return render_template(
                "mockups/solid_image_generator.html",
                aspect_ratios=MockupBaseGenerationCatalog.ASPECT_RATIOS,
                default_color=color_input,
            ), 400

    except Exception as e:
        logger.error(f"Error processing solid image request: {str(e)}", exc_info=True)
        flash("Error processing request. Check server logs.", "error")
        abort(500)
