"""Index helpers for deterministic artwork lookup.

Artworks and assets indexes are the only supported source of truth for locating
processed artwork files. Downstream code must resolve SKU → paths through
`artworks.json` instead of inferring folder names or scanning the filesystem.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple

from ...common.utilities.files import ensure_dir, write_json_atomic
from ..errors import IndexUpdateError, IndexValidationError, RequiredAssetMissingError


ASSETS_VERSION = 1
ARTWORKS_VERSION = 2
DEFAULT_MOCKUPS_DIRNAME = "mockups"
VALID_STAGE_NAMES = {"unprocessed", "processed", "locked"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_assets_document(
    *,
    slug: str,
    sku: str,
    files: Dict[str, str],
    mockups_dirname: str = DEFAULT_MOCKUPS_DIRNAME,
) -> Dict:
    """Construct the per-artwork assets document with relative paths only.

    Paths are stored relative to `artwork_dir` to avoid any implicit path
    guessing. `files` must already be validated for existence.
    """

    return {
        "version": ASSETS_VERSION,
        "slug": slug,
        "sku": sku,
        "files": files,
        "mockups": {"dir": mockups_dirname, "assets": {}},
        "updated_at": _now_iso(),
    }


def validate_asset_paths(artwork_dir: Path, files: Dict[str, str]) -> None:
    missing = [name for name, rel in files.items() if not (artwork_dir / rel).exists()]
    if missing:
        raise RequiredAssetMissingError(f"Missing required assets: {', '.join(sorted(missing))}")


class ArtworksIndex:
    """Atomic loader/writer for the global artworks index.

    This index maps SKU → artwork directory + assets filename. Consumers must
    use it to resolve paths; inferring folder names or scanning directories is
    explicitly forbidden by policy.
    """

    def __init__(self, index_path: Path, processed_root: Path) -> None:
        self.index_path = index_path
        self.processed_root = processed_root

    def _lab_root(self) -> Path:
        return self.index_path.parent.parent

    @staticmethod
    def _normalize_stage(stage: str) -> str:
        stage_text = str(stage or "").strip().lower() or "processed"
        if stage_text not in VALID_STAGE_NAMES:
            raise IndexValidationError(f"Invalid artwork stage: {stage}")
        return stage_text

    def load(self) -> Dict:
        if not self.index_path.exists():
            ensure_dir(self.index_path.parent)
            base = {"version": ARTWORKS_VERSION, "items": {}, "updated_at": _now_iso()}
            write_json_atomic(self.index_path, base)
            return base
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise IndexValidationError("artworks.json is not valid JSON") from exc
        if not isinstance(data, dict) or "items" not in data or not isinstance(data["items"], dict):
            raise IndexValidationError("artworks.json must contain an 'items' mapping")
        return data

    def upsert(
        self,
        *,
        sku: str,
        slug: str,
        artwork_dirname: str,
        assets_file: str,
        stage: str = "processed",
    ) -> Dict:
        doc = self.load()
        items = doc.get("items", {})
        if not isinstance(items, dict):
            raise IndexValidationError("artworks.json 'items' must be a mapping")

        stage_name = self._normalize_stage(stage)
        artwork_path = f"{stage_name}/{artwork_dirname}"
        assets_path = f"{artwork_path}/{assets_file}"

        now = _now_iso()
        existing = items.get(sku) or {}
        created_at = existing.get("created_at", now)
        items[sku] = {
            "sku": sku,
            "slug": slug,
            "artwork_dirname": artwork_dirname,
            "assets_file": assets_file,
            "assets_path": assets_path,
            "artwork_path": artwork_path,
            "created_at": created_at,
            "updated_at": now,
            "version": ARTWORKS_VERSION,
        }
        doc["items"] = items
        doc["updated_at"] = now

        try:
            write_json_atomic(self.index_path, doc)
        except Exception as exc:  # pylint: disable=broad-except
            raise IndexUpdateError("Failed to write artworks index atomically") from exc
        return doc

    def resolve(self, sku: str) -> Tuple[Path, Path]:
        doc = self.load()
        items = doc.get("items") or {}
        if sku not in items:
            raise IndexValidationError(f"SKU {sku} missing from artworks index")
        entry = items[sku]
        artwork_dirname = entry.get("artwork_dirname")
        assets_file = entry.get("assets_file")
        if not artwork_dirname or not assets_file:
            raise IndexValidationError(f"artworks.json entry for {sku} is incomplete")

        artwork_path = entry.get("artwork_path")
        assets_rel = entry.get("assets_path")
        lab_root = self._lab_root()

        if isinstance(artwork_path, str) and artwork_path.strip():
            artwork_dir = lab_root / artwork_path
            if isinstance(assets_rel, str) and assets_rel.strip():
                assets_path = lab_root / assets_rel
            else:
                assets_path = artwork_dir / assets_file
        else:
            artwork_dir = self.processed_root / artwork_dirname
            assets_path = artwork_dir / assets_file
        return artwork_dir, assets_path

    def remove_by_sku(self, sku: str) -> Dict:
        doc = self.load()
        items = doc.get("items", {})
        if not isinstance(items, dict):
            raise IndexValidationError("artworks.json 'items' must be a mapping")
        if sku in items:
            items.pop(sku, None)
            doc["items"] = items
            doc["updated_at"] = _now_iso()
            try:
                write_json_atomic(self.index_path, doc)
            except Exception as exc:  # pylint: disable=broad-except
                raise IndexUpdateError("Failed to update artworks index") from exc
        return doc

    def remove_by_slug(self, slug: str) -> Dict:
        doc = self.load()
        items = doc.get("items", {})
        if not isinstance(items, dict):
            raise IndexValidationError("artworks.json 'items' must be a mapping")

        removed = False
        for sku, entry in list(items.items()):
            entry_slug = (entry or {}).get("slug") if isinstance(entry, dict) else None
            if str(entry_slug or "").strip() == str(slug or "").strip():
                items.pop(sku, None)
                removed = True

        if removed:
            doc["items"] = items
            doc["updated_at"] = _now_iso()
            try:
                write_json_atomic(self.index_path, doc)
            except Exception as exc:  # pylint: disable=broad-except
                raise IndexUpdateError("Failed to update artworks index") from exc
        return doc
