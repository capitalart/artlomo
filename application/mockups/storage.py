"""Deterministic filesystem helpers for mockup generation."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from hashlib import new as hashlib_new
from pathlib import Path
from typing import Dict, Tuple

from PIL import Image

import application.mockups.config as mockups_config
from .errors import AssetConflictError, IoError


def compute_hash(*payloads: bytes) -> str:
    hasher = hashlib_new(mockups_config.HASH_ALGO)
    for blob in payloads:
        hasher.update(blob)
    return hasher.hexdigest()


def ensure_dirs(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def resolve_output_paths(artwork_dir: Path, mockups_dirname: str, slug: str, slot: int) -> Dict[str, Path]:
    mockups_dir = artwork_dir / mockups_dirname
    thumbs_dir = mockups_dir / mockups_config.THUMBS_SUBDIR
    composite_name = mockups_config.COMPOSITE_BASENAME.format(slug=slug, slot=slot)
    thumb_name = mockups_config.THUMB_BASENAME.format(slug=slug, slot=slot)
    return {
        "mockups_dir": mockups_dir,
        "thumbs_dir": thumbs_dir,
        "composite_path": mockups_dir / composite_name,
        "thumb_path": thumbs_dir / thumb_name,
    }


def _atomic_write_bytes(data: bytes, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.NamedTemporaryFile(delete=False, dir=str(target.parent)) as tmp:
            tmp.write(data)
            tmp_path = Path(tmp.name)
        os.replace(tmp_path, target)
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError(f"Failed to write file atomically: {target}") from exc


def atomic_write_json(data: Dict, target: Path) -> None:
    try:
        payload = json.dumps(data, indent=2, sort_keys=True).encode("utf-8")
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError("Failed to serialize JSON") from exc
    _atomic_write_bytes(payload, target)


def atomic_write_jpeg(image: Image.Image, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.NamedTemporaryFile(delete=False, dir=str(target.parent), suffix=".jpg") as tmp:
            image.save(tmp, **mockups_config.JPEG_PARAMS)
            tmp_path = Path(tmp.name)
        os.replace(tmp_path, target)
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError(f"Failed to write JPEG: {target}") from exc


def delete_if_exists(path: Path) -> None:
    try:
        if path.exists():
            path.unlink()
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError(f"Failed to delete file: {path}") from exc



def copy_or_overwrite(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(src, dest)
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError(f"Failed to copy file to {dest}") from exc


def guard_slot_for_generate(assets: Dict, slot_key: str) -> None:
    # Overwrite is permitted for regeneration workflows.
    # Generation callers that require strict no-overwrite should enforce that at a higher level.
    return


def guard_slot_for_swap(assets: Dict, slot_key: str) -> Dict:
    if slot_key not in assets:
        raise AssetConflictError(f"Slot {slot_key} does not exist; swap requires an existing slot")
    return assets[slot_key]
