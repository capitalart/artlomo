"""Domain exceptions for Mockup Engine V2."""

from __future__ import annotations


class MockupEngineError(Exception):
    """Base exception for v2 mockup engine errors."""


class GenerationFailedError(MockupEngineError):
    """Raised when image generation fails."""


class CoordinateExtractionError(MockupEngineError):
    """Raised when the fiducial marker cannot be extracted correctly."""


class FailedDetectionError(CoordinateExtractionError):
    """Raised when extraction does not find exactly one valid quadrilateral."""


class CatalogRegistrationError(MockupEngineError):
    """Raised when catalog registration preconditions fail."""


class CompositeRenderError(MockupEngineError):
    """Raised when perspective compositing fails."""


class HarmonizationError(MockupEngineError):
    """Raised when optional harmonization is requested and fails."""
