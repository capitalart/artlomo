"""Custom exceptions for artwork processing and index enforcement."""

class ArtworkProcessingError(Exception):
    """Base error for processing failures."""


class RequiredAssetMissingError(ArtworkProcessingError):
    """Raised when expected assets are missing before processing."""


class IndexValidationError(ArtworkProcessingError):
    """Raised when an index is unreadable or violates invariants."""


class IndexUpdateError(ArtworkProcessingError):
    """Raised when an index cannot be written safely."""
