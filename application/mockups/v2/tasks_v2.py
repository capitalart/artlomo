"""Celery tasks for Mockup Engine V2 pipeline."""

from __future__ import annotations

import os
from pathlib import Path

from celery import Celery

from .contracts import PipelineGenerationInput, RenderCompositeInput
from .pipeline_orchestrator import MockupPipelineOrchestrator
from .services.composite_render_service import CompositeRenderService

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", BROKER_URL)

celery_app = Celery("mockup_engine_v2", broker=BROKER_URL, backend=RESULT_BACKEND)


@celery_app.task(name="mockup_v2.generate_base_and_coordinates", bind=True, max_retries=2)
def generate_base_and_coordinates_task(
    self,
    *,
    job_id: str,
    prompt: str,
    work_dir: str,
    thumbnail_path: str,
    generation_model: str = "gemini-2.5-flash-image",
    metadata: dict | None = None,
):
    orchestrator = MockupPipelineOrchestrator()
    result = orchestrator.run_generation(
        PipelineGenerationInput(
            job_id=job_id,
            prompt=prompt,
            work_dir=Path(work_dir),
            thumbnail_path=Path(thumbnail_path),
            generation_model=generation_model,
            metadata=metadata,
        )
    )
    return {
        "job_id": result.job_id,
        "state": result.state.value,
        "generated_image_path": str(result.generated_image_path),
        "transparent_base_png_path": str(result.transparent_base_png_path),
        "coordinates_json_path": str(result.coordinates_json_path),
        "thumbnail_path": str(result.thumbnail_path),
    }


@celery_app.task(name="mockup_v2.render_composite", bind=True, max_retries=2)
def render_composite_task(
    self,
    *,
    artwork_path: str,
    base_png_path: str,
    coordinates_json_path: str,
    output_jpeg_path: str,
    jpeg_quality: int = 95,
):
    service = CompositeRenderService()
    result = service.render(
        RenderCompositeInput(
            artwork_path=Path(artwork_path),
            base_png_path=Path(base_png_path),
            coordinates_json_path=Path(coordinates_json_path),
            output_jpeg_path=Path(output_jpeg_path),
            jpeg_quality=jpeg_quality,
        )
    )
    return {
        "output_jpeg_path": str(result.output_jpeg_path),
        "width": result.width,
        "height": result.height,
    }
