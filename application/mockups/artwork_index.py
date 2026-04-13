"""Read-only access to the master artworks index (artworks.json).

All path resolution for mockup generation must flow through this module. No
callers may guess folder names or scan directories.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

import application.mockups.config as mockups_config
from .errors import IndexLookupError, IoError


def _load_index(path: Path) -> dict:
    if not path.exists():
        raise IndexLookupError(f"artworks index missing: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise IndexLookupError("artworks.json is not valid JSON") from exc
    except Exception as exc:  # pylint: disable=broad-except
        raise IoError(f"Failed to read artworks index: {path}") from exc


def resolve_artwork(
    sku: str,
    *,
    master_index_path: Path | None = None,
    processed_root: Path | None = None,
) -> Tuple[Path, Path, str]:
    """Resolve SKU → (artwork_dir, assets_index_path, slug).

    Raises IndexLookupError if the SKU is missing or the index is invalid.
    """

    index_path = master_index_path or mockups_config.MASTER_INDEX_PATH
    processed_root = processed_root or mockups_config.PROCESSED_DIR

    doc = _load_index(index_path)
    items = doc.get("items") if isinstance(doc, dict) else None
    if not isinstance(items, dict):
        raise IndexLookupError("artworks.json must contain an 'items' mapping")
    if sku not in items:
        raise IndexLookupError(f"SKU {sku} not found in artworks.json")

    entry = items[sku]
    if not isinstance(entry, dict):
        raise IndexLookupError(f"artworks.json entry for {sku} must be an object")

    artwork_dirname = entry.get("artwork_dirname")
    assets_file = entry.get("assets_file")
    slug = entry.get("slug")

    if not all(isinstance(val, str) and val for val in (artwork_dirname, assets_file, slug)):
        raise IndexLookupError(f"artworks.json entry for {sku} is incomplete")
    
    # Type narrowing: at this point we know these are non-empty strings
    artwork_dirname_str: str = artwork_dirname  # type: ignore[assignment]
    assets_file_str: str = assets_file  # type: ignore[assignment]
    slug_str: str = slug  # type: ignore[assignment]
    
    if Path(artwork_dirname_str).is_absolute() or Path(assets_file_str).is_absolute():
        raise IndexLookupError("Index entries must be relative paths")

    artwork_dir = processed_root / artwork_dirname_str
    assets_path = artwork_dir / assets_file_str

    if not artwork_dir.exists():
        raise IndexLookupError(f"Artwork directory missing: {artwork_dir}")
    if not assets_path.exists():
        raise IndexLookupError(f"Assets index missing: {assets_path}")

    return artwork_dir, assets_path, slug_str
