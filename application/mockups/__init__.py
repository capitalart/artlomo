"""Mockup generation backend (Phase 1, clean-room, deterministic).

Public API:
    generate_mockups_for_artwork from pipeline.
"""

from .pipeline import generate_mockups_for_artwork

__all__ = ["generate_mockups_for_artwork"]
