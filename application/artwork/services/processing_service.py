"""Promotion pipeline from unprocessed → processed with index enforcement."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from ...common.utilities.files import ensure_dir, write_json_atomic
from ...upload.services import storage_service
from ..errors import ArtworkProcessingError, IndexValidationError, RequiredAssetMissingError
from .index_service import (
    DEFAULT_MOCKUPS_DIRNAME,
    ArtworksIndex,
    build_assets_document,
    validate_asset_paths,
)
from datetime import datetime, timezone


class ProcessingService:
    """Move required assets into processed/ and write index files.

    This is the only supported way to create processed artwork folders. All
    downstream consumers must resolve SKU → paths via artworks.json and then the
    per-artwork assets document; no code should infer locations or scan for
    filenames. The move is atomic to ensure a slug exists in only one stage
    (unprocessed | processed | locked).
    """

    def __init__(
        self,
        *,
        unprocessed_root: Path,
        processed_root: Path,
        artworks_index_path: Path,
        mockups_dirname: str = DEFAULT_MOCKUPS_DIRNAME,
    ) -> None:
        self.unprocessed_root = unprocessed_root
        self.processed_root = processed_root
        self.mockups_dirname = mockups_dirname
        self.artworks_index = ArtworksIndex(artworks_index_path, processed_root)

    def process(self, slug: str) -> Path:
        source_dir = self.unprocessed_root / slug
        if not source_dir.exists():
            raise RequiredAssetMissingError(f"Unprocessed folder missing: {source_dir}")

        # Load metadata with fallback logic (try SKU-prefixed first, then legacy)
        meta = storage_service.load_metadata_with_fallback(source_dir)
        if not meta:
            raise RequiredAssetMissingError("Missing or invalid metadata file in unprocessed folder")
        
        sku = str(meta.get("sku") or meta.get("artwork_id") or "").strip()
        if not sku:
            raise IndexValidationError("metadata.json missing sku/artwork_id")

        # Ensure master is -MASTER.jpg (legacy support)
        # We now enforce -MASTER.jpg suffix, but older uploads might be [slug].jpg
        master_target = storage_service.master_name(slug)
        master_path = source_dir / master_target
        if not master_path.exists():
            legacy_path = source_dir / f"{slug}.jpg"
            if legacy_path.exists():
                try:
                    legacy_path.replace(master_path)
                except Exception as exc:
                    raise ArtworkProcessingError(f"Failed to rename legacy master {legacy_path} to {master_path}") from exc

        # Use SKU-prefixed filenames for metadata and QC
        # Check if we have closeup_proxy or analyse (or both)
        analyse_file = storage_service.analyse_name(slug)
        closeup_proxy_file = f"{slug}-CLOSEUP-PROXY.jpg"
        has_analyse = (source_dir / analyse_file).exists()
        has_closeup_proxy = (source_dir / closeup_proxy_file).exists()
        
        required = {
            "master": master_target,
            "thumb": storage_service.thumb_name(slug),
            "metadata": storage_service._meta_name(sku),
            "qc": storage_service._qc_name(sku),
        }
        
        # Include whichever artwork image files exist
        if has_analyse:
            required["analyse"] = analyse_file
        if has_closeup_proxy:
            required["closeup_proxy"] = closeup_proxy_file
        
        # Must have at least one artwork image source
        if not (has_analyse or has_closeup_proxy):
            raise RequiredAssetMissingError(
                f"Missing artwork image: need either {analyse_file} or {closeup_proxy_file}"
            )
        
        self._ensure_required(source_dir, required)

        dest_dir = self.processed_root / slug
        if dest_dir.exists():
            raise IndexValidationError(f"Processed folder already exists for slug {slug}")

        # Atomic move enforces single-source-of-truth placement.
        self._move_dir_atomic(source_dir, dest_dir)
        ensure_dir(dest_dir / self.mockups_dirname)

        validate_asset_paths(dest_dir, required)

        assets_payload = build_assets_document(
            slug=slug,
            sku=sku,
            files=required,
            mockups_dirname=self.mockups_dirname,
        )
        assets_path = dest_dir / f"{sku.lower()}-assets.json"
        write_json_atomic(assets_path, assets_payload)

        self.artworks_index.upsert(
            sku=sku,
            slug=slug,
            artwork_dirname=slug,
            assets_file=assets_path.name,
            stage="processed",
        )
        
        # Update database status to 'processed' after successful file move
        try:
            from application.utils.artwork_db import update_artwork_status
            update_artwork_status(sku, "processed")
        except Exception:
            import logging
            logging.getLogger(__name__).warning(
                f"Failed to update DB status for {sku} to 'processed'"
            )
        try:
            now = datetime.now(timezone.utc).isoformat()
            status = storage_service.read_processing_status(dest_dir) or {
                "slug": slug,
                "done": False,
                "error": None,
                "message": "",
                "percent": 0,
                "stage": "processing",
                "started_at": now,
                "updated_at": now,
            }
            status.update({"stage": "closeup_proxy", "message": "Generating Closeup Proxy", "percent": 95, "updated_at": now})
            storage_service.store_processing_status(dest_dir, status, sku=sku)
            from .detail_closeup_service import DetailCloseupService
            svc = DetailCloseupService(processed_root=self.processed_root)
            svc.generate_proxy_preview(slug)
            now2 = datetime.now(timezone.utc).isoformat()
            status.update({"stage": "complete", "message": "Ready", "done": True, "percent": 100, "updated_at": now2})
            storage_service.store_processing_status(dest_dir, status, sku=sku)
        except Exception:
            import logging
            logging.getLogger(__name__).warning(f"Failed closeup proxy stage for {slug}")
        return dest_dir

    @staticmethod
    def _load_json(path: Path) -> dict:
        if not path.exists():
            raise RequiredAssetMissingError(f"Missing required JSON: {path.name}")
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise IndexValidationError(f"Invalid JSON payload: {path.name}") from exc

    @staticmethod
    def _ensure_required(source_dir: Path, required: dict[str, str]) -> None:
        missing = [name for name, rel in required.items() if not (source_dir / rel).exists()]
        if missing:
            raise RequiredAssetMissingError(f"Missing required assets: {', '.join(sorted(missing))}")

    @staticmethod
    def _move_dir_atomic(src: Path, dest: Path) -> None:
        ensure_dir(dest.parent)
        try:
            src.replace(dest)
        except Exception as exc:  # pylint: disable=broad-except
            raise ArtworkProcessingError(f"Failed to move {src} to {dest}") from exc
