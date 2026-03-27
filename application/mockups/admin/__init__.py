"""Mockup admin / management (Phase 3A).

Admin manages catalog, categories, and mandatory template policy. It does not
invoke generation or mutate per-artwork assets.
"""

from .services import CatalogAdminService
from .readers import read_mockup_slots
from .routes import mockups_admin_bp

__all__ = [
    "CatalogAdminService",
    "read_mockup_slots",
    "mockups_admin_bp",
]
