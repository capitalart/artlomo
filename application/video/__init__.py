"""Video Generation Module - Kinematic Preview Generation

This module handles the generation of kinematic video previews
that showcase artwork mockups with smooth panning and zooming effects.
"""

from pathlib import Path

try:
    from application.tools.video.service import VideoService
    __all__ = ["VideoService"]
except ImportError:
    VideoService = None  # type: ignore[misc,assignment]
    __all__: list[str] = []  # type: ignore[no-redef]
