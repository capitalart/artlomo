"""Mockup Engine V2: strict 5-service pipeline implementation.

This package is intentionally isolated from legacy mockup logic.
"""

from .contracts import (
    CatalogState,
    CoordinateExtractionInput,
    CoordinateExtractionResult,
    HarmonizationInput,
    HarmonizationResult,
    MockupGenerationInput,
    MockupGenerationResult,
    PipelineGenerationInput,
    PipelineGenerationResult,
    RenderCompositeInput,
    RenderCompositeResult,
)

__all__ = [
    "CatalogState",
    "CoordinateExtractionInput",
    "CoordinateExtractionResult",
    "HarmonizationInput",
    "HarmonizationResult",
    "MockupGenerationInput",
    "MockupGenerationResult",
    "PipelineGenerationInput",
    "PipelineGenerationResult",
    "RenderCompositeInput",
    "RenderCompositeResult",
]
