from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from ..artwork_index import resolve_artwork
from ..errors import ValidationError
from .models import SlotMap


def read_mockup_slots(sku: str, *, master_index_path: Path | None = None, processed_root: Path | None = None) -> SlotMap:
    """Read-only view of slot assignments for an artwork.

    Uses artworks.json to resolve the assets index; does not write or generate.
    """

    artwork_dir, assets_path, _ = resolve_artwork(sku, master_index_path=master_index_path, processed_root=processed_root)
    try:
        data = json.loads(assets_path.read_text(encoding="utf-8"))
    except Exception as exc:  # pylint: disable=broad-except
        raise ValidationError("Assets index is invalid JSON") from exc

    mockups = data.get("mockups") or {}
    assets = mockups.get("assets")
    if assets is None:
        return {}
    if not isinstance(assets, dict):
        raise ValidationError("mockups.assets must be a mapping")
    return assets
