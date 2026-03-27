"""Per-artwork assets index management (authoritative, atomic).

Only this module may mutate `<slug>-assets.json`. All callers must treat it as
source of truth for both required artwork files and mockup slot state.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import application.mockups.config as mockups_config
from . import storage
from .errors import IndexLookupError, IoError, MissingAssetError, ValidationError

REQUIRED_FILE_KEYS = ("master", "thumb", "metadata", "qc")
# Either "analyse" or "closeup_proxy" must be present (checked separately)
ARTWORK_IMAGE_KEYS = ("analyse", "closeup_proxy")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class AssetsIndex:
    def __init__(self, artwork_dir: Path, assets_path: Path) -> None:
        self.artwork_dir = artwork_dir
        self.assets_path = assets_path

    def load(self) -> Dict:
        if not self.assets_path.exists():
            raise IndexLookupError(f"Assets index missing: {self.assets_path}")
        try:
            data = json.loads(self.assets_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise IndexLookupError("Assets index is not valid JSON") from exc
        except Exception as exc:  # pylint: disable=broad-except
            raise IoError(f"Failed to read assets index: {self.assets_path}") from exc

        self._validate_shape(data)
        self._validate_files_exist(data)
        self._ensure_mockups_dirs(data)
        return data

    def guard_generate(self, assets_doc: Dict, slot_key: str) -> None:
        storage.guard_slot_for_generate(assets_doc.get("mockups", {}).get("assets", {}), slot_key)

    def guard_swap(self, assets_doc: Dict, slot_key: str) -> Dict:
        return storage.guard_slot_for_swap(assets_doc.get("mockups", {}).get("assets", {}), slot_key)

    def write_slot(self, assets_doc: Dict, slot_key: str, slot_entry: Dict) -> None:
        mockups = assets_doc.get("mockups")
        if not isinstance(mockups, dict):
            mockups = {}
        assets_doc["mockups"] = mockups
        assets_map = mockups.get("assets")
        if not isinstance(assets_map, dict):
            assets_map = {}
        assets_map[slot_key] = slot_entry
        mockups["assets"] = assets_map
        assets_doc["mockups"] = mockups
        assets_doc["updated_at"] = _now_iso()
        storage.atomic_write_json(assets_doc, self.assets_path)

    def _validate_shape(self, data: Dict) -> None:
        if not isinstance(data, dict):
            raise ValidationError("Assets index must be a JSON object")
        slug = data.get("slug")
        sku = data.get("sku")
        if not all(isinstance(val, str) and val for val in (slug, sku)):
            raise ValidationError("Assets index must contain slug and sku")

        files = data.get("files")
        if files is not None:
            if not isinstance(files, dict):
                raise ValidationError("Assets index files must be a mapping when present")
            for key in REQUIRED_FILE_KEYS:
                if key not in files:
                    raise ValidationError(f"Assets index missing required file key: {key}")
                rel = files[key]
                if not isinstance(rel, str) or not rel:
                    raise ValidationError(f"Assets index file path for {key} must be a non-empty string")
                if Path(rel).is_absolute():
                    raise ValidationError("Asset file paths must be relative to the artwork directory")
            
            # Verify at least one artwork image source exists (for mockup generation)
            has_artwork_image = any(key in files for key in ARTWORK_IMAGE_KEYS)
            if not has_artwork_image:
                raise ValidationError(f"Assets index must contain at least one of: {', '.join(ARTWORK_IMAGE_KEYS)}")

        mockups = data.get("mockups")
        if mockups is None:
            mockups = {"dir": mockups_config.MOCKUPS_SUBDIR, "assets": {}}
            data["mockups"] = mockups
        if not isinstance(mockups, dict):
            raise ValidationError("Assets index mockups must be an object when present")
        mockups_dir = mockups.get("dir") or mockups_config.MOCKUPS_SUBDIR
        assets_map = mockups.get("assets")
        if not isinstance(mockups_dir, str) or not mockups_dir:
            raise ValidationError("mockups.dir must be a non-empty string")
        if Path(mockups_dir).is_absolute():
            raise ValidationError("mockups.dir must be relative")
        if assets_map is None:
            mockups["assets"] = {}
        elif not isinstance(assets_map, dict):
            raise ValidationError("mockups.assets must be a mapping")

    def _validate_files_exist(self, data: Dict) -> None:
        files = data.get("files", {})
        missing = [key for key, rel in files.items() if not (self.artwork_dir / rel).exists()]
        if missing:
            raise MissingAssetError(f"Missing required assets: {', '.join(sorted(missing))}")

    def _ensure_mockups_dirs(self, data: Dict) -> None:
        mockups = data.get("mockups")
        mockups_dirname = mockups.get("dir") if isinstance(mockups, dict) else None
        mockups_dirname = mockups_dirname or mockups_config.MOCKUPS_SUBDIR
        mockups_dir = self.artwork_dir / mockups_dirname
        thumbs_dir = mockups_dir / mockups_config.THUMBS_SUBDIR
        storage.ensure_dirs(mockups_dir, thumbs_dir)

    def mockups_dirname(self, assets_doc: Dict) -> str:
        mockups = assets_doc.get("mockups")
        dirname = mockups.get("dir") if isinstance(mockups, dict) else None
        dirname = dirname or mockups_config.MOCKUPS_SUBDIR
        return dirname

    def assets_map(self, assets_doc: Dict) -> Dict:
        mockups = assets_doc.get("mockups", {})
        assets = mockups.get("assets")
        return assets if isinstance(assets, dict) else {}

    def current_slot_entry(self, assets_doc: Dict, slot_key: str) -> Dict | None:
        return self.assets_map(assets_doc).get(slot_key)
