"""Template catalog (read-only) for Phase 2 selection."""

from .loader import load_catalog
from .models import Template

__all__ = ["Template", "load_catalog"]
