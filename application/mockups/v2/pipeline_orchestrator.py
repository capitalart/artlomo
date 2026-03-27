"""Orchestration layer for v2 5-service pipeline."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from .contracts import (
    CatalogState,
    CoordinateExtractionInput,
    MockupGenerationInput,
    PipelineGenerationInput,
    PipelineGenerationResult,
)
from .exceptions import CatalogRegistrationError, FailedDetectionError, MockupEngineError
from .services import (
    BaseCatalogService,
    CoordinateExtractionService,
    MockupGenerationService,
)


class MockupPipelineOrchestrator:
    """Strict orchestrator for generation and coordinate extraction pipeline."""

    def __init__(
        self,
        generation_service: MockupGenerationService | None = None,
        extraction_service: CoordinateExtractionService | None = None,
        catalog_service: BaseCatalogService | None = None,
    ):
        self._generation = generation_service or MockupGenerationService()
        self._extraction = extraction_service or CoordinateExtractionService()
        self._catalog = catalog_service or BaseCatalogService()

    def run_generation(self, request: PipelineGenerationInput) -> PipelineGenerationResult:
        work_dir = Path(request.work_dir)
        work_dir.mkdir(parents=True, exist_ok=True)

        generated_jpg_path = work_dir / "generated_scene.jpg"
        transparent_png_path = work_dir / "base_transparent.png"
        coordinates_json_path = work_dir / "coordinates.json"

        try:
            self._catalog.set_state(request.job_id, CatalogState.GENERATING)
            self._generation.generate(
                MockupGenerationInput(
                    prompt=request.prompt,
                    output_path=generated_jpg_path,
                    model=request.generation_model,
                )
            )

            self._catalog.set_state(request.job_id, CatalogState.EXTRACTING)
            self._extraction.extract(
                CoordinateExtractionInput(
                    source_image_path=generated_jpg_path,
                    output_png_path=transparent_png_path,
                    output_json_path=coordinates_json_path,
                )
            )

            self._create_thumbnail(transparent_png_path, request.thumbnail_path)
            self._catalog.register_if_complete(
                job_id=request.job_id,
                base_png_path=transparent_png_path,
                coordinates_json_path=coordinates_json_path,
                thumbnail_path=request.thumbnail_path,
                metadata=request.metadata,
            )
            self._catalog.set_state(request.job_id, CatalogState.CATALOG_READY)
        except FailedDetectionError as exc:
            self._catalog.set_state(
                request.job_id,
                CatalogState.REVIEW_REQUIRED,
                reason="FAILED_DETECTION",
                error_message=str(exc),
            )
            raise
        except (CatalogRegistrationError, MockupEngineError) as exc:
            self._catalog.set_state(
                request.job_id,
                CatalogState.FAILED,
                reason="PIPELINE_ERROR",
                error_message=str(exc),
            )
            raise
        except Exception as exc:  # noqa: BLE001
            self._catalog.set_state(
                request.job_id,
                CatalogState.FAILED,
                reason="UNHANDLED_PIPELINE_ERROR",
                error_message=str(exc),
            )
            raise

        return PipelineGenerationResult(
            job_id=request.job_id,
            state=CatalogState.CATALOG_READY,
            generated_image_path=generated_jpg_path,
            transparent_base_png_path=transparent_png_path,
            coordinates_json_path=coordinates_json_path,
            thumbnail_path=request.thumbnail_path,
        )

    @staticmethod
    def _create_thumbnail(source_png_path: Path, thumbnail_path: Path) -> None:
        thumbnail_path.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source_png_path) as img:
            thumb = img.convert("RGBA")
            thumb.thumbnail((512, 512))
            thumb.save(thumbnail_path, format="PNG")
