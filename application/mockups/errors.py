"""Custom exception types for the mockup backend."""

class MockupError(Exception):
    """Base mockup exception."""


class ValidationError(MockupError):
    """Raised when input fails validation."""


class CoordinateSchemaError(ValidationError):
    """Coordinate JSON schema is invalid."""


class DimensionMismatchError(ValidationError):
    """Coordinate bounds do not fit the base image dimensions."""


class MissingAssetError(MockupError):
    """Required asset (artwork/base/coords) is missing."""


class TransformError(MockupError):
    """Perspective or warp computation failed."""


class AssetConflictError(MockupError):
    """Slot or path conflicts during generate/swap."""


class IoError(MockupError):
    """Filesystem I/O failure."""


class HashMismatchError(MockupError):
    """Content hash differs where immutability is expected."""


class SlotConflictError(MockupError):
    """Slot state does not permit the requested operation."""


class IndexLookupError(MockupError):
    """artworks.json or assets index could not be resolved or was invalid."""
