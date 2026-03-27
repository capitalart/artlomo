from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any

from celery.exceptions import MaxRetriesExceededError
from PIL import Image, ImageDraw
from sqlalchemy.exc import SQLAlchemyError

from db import PrecisionMockupJob
from application.mockups.services.gemini_service import (
    GeminiAuthenticationError,
    GeminiFileSaveError,
    GeminiGenerationError,
    GeminiImageService,
    GeminiRateLimitError,
)
from application.mockups.services.precision_service import PrecisionGeometryService
from application.mockups.tasks_mockup_generator import (
    MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES,
    MOCKUP_GEMINI_TASK_RATE_LIMIT,
    STUDIO_CANVAS_ASPECT_RATIO,
    _compute_rate_limit_retry_delay,
    _session_scope,
    celery,
)


logger = logging.getLogger(__name__)

PRECISION_MOCKUP_ROOT = Path("/srv/artlomo/var/studio/precision")
PRECISION_ROOM_OUTPUT_DIR = PRECISION_MOCKUP_ROOT / "rooms"
PRECISION_TRANSPARENT_OUTPUT_DIR = PRECISION_MOCKUP_ROOT / "transparent"
PRECISION_ARTIST_MODEL = os.getenv("PRECISION_ARTIST_MODEL", "gemini-2.0-ultra-001")
PRECISION_FRAME_FORCE = "Place the asset inside a thick, high-contrast matte black wooden frame."
PRECISION_DETECTION_MODEL = "local-opencv-precision-v1"


def _save_precision_room_output(job_external_id: str, image_bytes: bytes) -> str:
    PRECISION_ROOM_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PRECISION_ROOM_OUTPUT_DIR / f"{job_external_id}-room.jpg"
    image_obj = Image.open(BytesIO(image_bytes))
    image_obj.load()
    if image_obj.mode not in {"RGB", "RGBA"}:
        image_obj = image_obj.convert("RGB")
    if image_obj.mode == "RGBA":
        image_obj = image_obj.convert("RGB")
    image_obj.save(output_path, format="JPEG", quality=95)
    return str(output_path)


def _save_precision_transparent_output(
    job_external_id: str,
    room_image_path: str,
    frame_coords: dict[str, list[int]],
) -> str:
    PRECISION_TRANSPARENT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PRECISION_TRANSPARENT_OUTPUT_DIR / f"{job_external_id}-transparent.png"

    room_image = Image.open(room_image_path).convert("RGBA")
    alpha = Image.new("L", room_image.size, 255)
    draw = ImageDraw.Draw(alpha)
    draw.polygon(
        [
            tuple(frame_coords["tl"]),
            tuple(frame_coords["tr"]),
            tuple(frame_coords["br"]),
            tuple(frame_coords["bl"]),
        ],
        fill=0,
    )
    room_image.putalpha(alpha)
    room_image.save(output_path, format="PNG")
    return str(output_path)


def _build_precision_prompt(*, raw_prompt: str, aspect_ratio: str, category: str) -> str:
    cleaned_prompt = str(raw_prompt or "").strip()
    category_label = category.replace("-", " ")
    return (
        "[THINKING_LEVEL: HIGH]\n"
        f"Generate a photorealistic {category_label} interior mockup scene at 1:1 output. "
        f"The inserted artwork area must read as {aspect_ratio.replace('x', ':')} ratio. "
        f"{PRECISION_FRAME_FORCE} "
        "Keep the entire frame visible, geometrically clean, and easy to detect from the room image. "
        "Use realistic room depth, natural lighting, and clean wall separation. "
        "No abstract textures, no warped frames, no text, no watermarks."
        + (f"\n\nRAW PROMPT:\n{cleaned_prompt}" if cleaned_prompt else "")
    )


def _set_precision_job_failed(job_id: int, message: str) -> None:
    with _session_scope() as session:
        job = session.get(PrecisionMockupJob, job_id)
        if job is None:
            return
        job.status = "Failed"
        job.error_message = str(message or "Precision generation failed")
        job.finished_at = datetime.utcnow()
        session.commit()


@celery.task(
    bind=True,
    name="mockups.process_precision_mockup_job",
    rate_limit=MOCKUP_GEMINI_TASK_RATE_LIMIT,
)
def process_precision_mockup_job(self: Any, job_id: int) -> dict[str, Any]:
    room_output_path: str | None = None
    transparent_output_path: str | None = None

    try:
        with _session_scope() as session:
            job = session.get(PrecisionMockupJob, job_id)
            if job is None:
                return {"status": "not_found", "job_id": job_id}
            if job.status != "Pending":
                return {"status": "skipped", "job_id": job_id, "message": f"Job in status '{job.status}' cannot be processed"}

            job.status = "Generating"
            job.started_at = job.started_at or datetime.utcnow()
            job.finished_at = None
            job.error_message = None
            session.commit()

            external_job_id = str(job.job_id)
            prompt_text = str(job.prompt_text or "")
            source_image_path = str(job.source_image_path or "")
            aspect_ratio = str(job.aspect_ratio or "4x5")
            category = str(job.category or "uncategorised")

        source_path = Path(source_image_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Precision source image missing: {source_path}")

        gemini_service = GeminiImageService()
        gemini_service.IMAGE_GENERATION_MODEL = PRECISION_ARTIST_MODEL

        image_bytes = gemini_service._call_gemini_generate_images(
            prompt=_build_precision_prompt(raw_prompt=prompt_text, aspect_ratio=aspect_ratio, category=category),
            aspect_ratio=STUDIO_CANVAS_ASPECT_RATIO,
            raw_prompt=True,
        )
        room_output_path = _save_precision_room_output(external_job_id, image_bytes)

        geometry_result = PrecisionGeometryService.detect_frame_geometry_with_metadata(room_output_path)
        frame_coords = geometry_result.coordinates
        transparent_output_path = _save_precision_transparent_output(
            external_job_id,
            room_output_path,
            frame_coords,
        )

        composite_image, _ = gemini_service.composite_artwork_locally(
            room_output_path,
            source_path,
            frame_coords,
        )
        composite_image.convert("RGB").save(room_output_path, format="JPEG", quality=95)

        detection_note = geometry_result.reason if geometry_result.used_fallback else ""
        with _session_scope() as session:
            job = session.get(PrecisionMockupJob, job_id)
            if job is None:
                raise RuntimeError(f"Precision job {job_id} disappeared before completion update")
            job.status = "Completed"
            job.room_output_path = room_output_path
            job.transparent_output_path = transparent_output_path
            job.frame_coordinates_json = json.dumps(frame_coords, separators=(",", ":"))
            job.frame_coordinates_model = PRECISION_DETECTION_MODEL
            job.frame_coordinates_error = detection_note or None
            job.finished_at = datetime.utcnow()
            session.commit()

        return {
            "status": "completed",
            "job_id": job_id,
            "room_output_path": room_output_path,
            "transparent_output_path": transparent_output_path,
        }

    except GeminiRateLimitError as exc:
        retry_count = int(getattr(getattr(self, "request", None), "retries", 0) or 0)
        countdown = _compute_rate_limit_retry_delay(
            job_id=job_id,
            retry_after_seconds=exc.retry_after_seconds,
            retry_count=retry_count,
        )
        try:
            raise self.retry(
                exc=exc,
                countdown=countdown,
                max_retries=MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES,
            )
        except MaxRetriesExceededError:
            _set_precision_job_failed(job_id, str(exc))
            return {"status": "failed", "job_id": job_id, "error": str(exc)}

    except (GeminiGenerationError, GeminiAuthenticationError, GeminiFileSaveError, ValueError, FileNotFoundError) as exc:
        _set_precision_job_failed(job_id, str(exc))
        return {"status": "failed", "job_id": job_id, "error": str(exc)}

    except SQLAlchemyError as exc:
        logger.error("Database error while processing Precision Mockup job %s", job_id, exc_info=True)
        _set_precision_job_failed(job_id, str(exc))
        return {"status": "failed", "job_id": job_id, "error": str(exc)}

    except Exception as exc:
        logger.error("Unexpected error while processing Precision Mockup job %s", job_id, exc_info=True)
        _set_precision_job_failed(job_id, str(exc))
        return {"status": "failed", "job_id": job_id, "error": str(exc)}


__all__ = ["process_precision_mockup_job"]