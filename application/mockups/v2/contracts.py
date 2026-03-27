"""Strict contracts for Mockup Engine V2 services."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class CatalogState(str, Enum):
    """Allowed lifecycle states for mockup base generation."""

    PENDING = "Pending"
    GENERATING = "Generating"
    EXTRACTING = "Extracting"
    REVIEW_REQUIRED = "Review_Required"
    CATALOG_READY = "Catalog_Ready"
    FAILED = "Failed"


@dataclass(frozen=True)
class MockupGenerationInput:
    prompt: str
    output_path: Path
    model: str = "gemini-2.5-flash-image"


@dataclass(frozen=True)
class MockupGenerationResult:
    image_path: Path
    width: int
    height: int
    model: str


@dataclass(frozen=True)
class CoordinateExtractionInput:
    source_image_path: Path
    output_png_path: Path
    output_json_path: Path


@dataclass(frozen=True)
class CoordinateExtractionResult:
    png_path: Path
    json_path: Path
    points_px: list[dict[str, int]]
    width: int
    height: int


@dataclass(frozen=True)
class RenderCompositeInput:
    artwork_path: Path
    base_png_path: Path
    coordinates_json_path: Path
    output_jpeg_path: Path
    jpeg_quality: int = 95


@dataclass(frozen=True)
class RenderCompositeResult:
    output_jpeg_path: Path
    width: int
    height: int


@dataclass(frozen=True)
class HarmonizationInput:
    composite_jpeg_path: Path
    output_jpeg_path: Path
    prompt: str
    enabled: bool = False
    model: str = "gemini-2.5-flash-image"


@dataclass(frozen=True)
class HarmonizationResult:
    output_jpeg_path: Path
    model: str | None
    applied: bool


@dataclass(frozen=True)
class PipelineGenerationInput:
    job_id: str
    prompt: str
    work_dir: Path
    thumbnail_path: Path
    generation_model: str = "gemini-2.5-flash-image"
    metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class PipelineGenerationResult:
    job_id: str
    state: CatalogState
    generated_image_path: Path
    transparent_base_png_path: Path
    coordinates_json_path: Path
    thumbnail_path: Path
