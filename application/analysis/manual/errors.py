"""Manual workflow error types."""

class ManualWorkflowError(Exception):
    """Raised when manual workflow operations cannot proceed."""


class ManualValidationError(ManualWorkflowError):
    """Raised when input data for manual workflow is invalid."""
