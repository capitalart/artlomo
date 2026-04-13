"""Safe loaders for images and JSON used by the mockup backend."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

from PIL import Image

from .errors import IoError, MissingAssetError

logger = logging.getLogger(__name__)


def _check_exists(path: Path) -> None:
    if not path.exists():
        raise MissingAssetError(f"Missing required asset: {path}")
    if not path.is_file():
        raise IoError(f"Expected file, found directory or invalid path: {path}")


def load_base_rgba(path: Path) -> Image.Image:
    _check_exists(path)
    try:
        with Image.open(path) as img:
            rgba = img.convert("RGBA")
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError(f"Failed to load base image: {path}") from exc
    # Keep the generated base untouched. Artwork is composited by mapped regions
    # in the compositor, not by deleting cyan pixels from the base image.
    return rgba


def load_artwork_rgba(path: Path) -> Image.Image:
    _check_exists(path)
    try:
        with Image.open(path) as img:
            return img.convert("RGBA")
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError(f"Failed to load artwork image: {path}") from exc


def load_coords(path: Path) -> Dict[str, Any]:
    _check_exists(path)
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError(f"Failed to load coordinate JSON: {path}") from exc


def load_json(path: Path) -> Dict[str, Any]:
    _check_exists(path)
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError(f"Failed to load JSON: {path}") from exc
