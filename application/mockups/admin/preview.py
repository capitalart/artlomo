from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Tuple
import logging
import re

from PIL import Image

from .. import compositor, loader, transforms, validation
from ..config import DEFAULT_MOCKUP_ASPECT, MOCKUP_TESTS_DIR
from ..errors import ValidationError
from ...common.utilities.files import ensure_dir
from .services import CatalogAdminService

logger = logging.getLogger(__name__)

ALLOWED_PREVIEW_EXTS = {".jpg"}
MAX_CACHE_ITEMS = 5


class PreviewService:
    def __init__(
        self,
        *,
        catalog_path: Path | None = None,
        preview_art_root: Path | None = None,
        cache_root: Path | None = None,
    ) -> None:
        self.catalog_path = catalog_path
        default_preview_root = MOCKUP_TESTS_DIR
        configured_root = preview_art_root or default_preview_root
        self.preview_art_root = configured_root if configured_root.exists() else default_preview_root
        self.cache_root = cache_root or Path(__file__).resolve().parents[1] / "tmp" / "previews"
        self.catalog = CatalogAdminService(catalog_path=catalog_path)

    # ------------------------------------------------------------------
    # Artwork selection
    # ------------------------------------------------------------------
    def _all_preview_art_files(self) -> List[Path]:
        root = self.preview_art_root
        if not root.exists() or not root.is_dir():
            return []
        return [p for p in sorted(root.iterdir()) if p.is_file() and p.suffix.lower() in ALLOWED_PREVIEW_EXTS]

    def _aspect_candidates(self, aspect: str) -> List[str]:
        # Prefer new naming, keep legacy support for backwards compatibility.
        return [f"coordinate-tester-{aspect}.jpg", f"{aspect}.jpg"]

    def _aspect_from_filename(self, filename: str) -> str:
        stem = Path(filename).stem
        match = re.match(r"^coordinate-tester-(.+)$", stem)
        if match:
            return match.group(1)
        return stem

    def _iter_preview_art_files(self, aspect_ratio: str | None) -> List[Path]:
        if aspect_ratio is None:
            aspect = None
        else:
            aspect = (aspect_ratio or DEFAULT_MOCKUP_ASPECT).strip() or DEFAULT_MOCKUP_ASPECT
        root = self.preview_art_root
        if not root.exists() or not root.is_dir():
            return []

        if aspect is None:
            return self._all_preview_art_files()

        # Try exact aspect match first (new + legacy naming)
        if aspect != DEFAULT_MOCKUP_ASPECT:
            for candidate in self._aspect_candidates(aspect):
                target = root / candidate
                if target.exists() and target.is_file():
                    return [target]

        # Fallback: if exact aspect match not found (or aspect is DEFAULT), use all available.
        # This ensures UNSET bases can still preview using any available test asset.
        return self._all_preview_art_files()

    def list_preview_artworks(self, aspect_ratio: str | None) -> List[Path]:
        return self._iter_preview_art_files(aspect_ratio)

    def list_preview_artwork_records(self, aspect_ratio: str | None) -> List[dict]:
        from flask import url_for

        records: List[dict] = []
        files = self._iter_preview_art_files(aspect_ratio)

        for path in files:
            try:
                url = url_for("mockups_admin.preview_artwork_asset", filename=path.name)
            except Exception:  # url_for may fail outside request context
                url = None
            records.append(
                {
                    "filename": path.name,
                    "aspect": self._aspect_from_filename(path.name),
                    "path": url,
                }
            )
        
        return records

    def default_preview_artwork(self, aspect_ratio: str | None) -> Path | None:
        files = self.list_preview_artworks(aspect_ratio)
        return files[0] if files else None

    # ------------------------------------------------------------------
    # Preview generation
    # ------------------------------------------------------------------
    def _load_base_by_id(self, mockup_id: str):
        bases = self.catalog.load_bases()
        for base in bases:
            if base.id == mockup_id:
                return base
        raise ValidationError("Mockup not found")

    def _resolve_artwork(self, aspect_ratio: str | None, key: str | None) -> Path:
        options = self._iter_preview_art_files(aspect_ratio)
        if not options:
            # Fallback: if no exact aspect ratio match, try all available artworks
            all_options = self._iter_preview_art_files(None)
            if not all_options:
                raise ValidationError("No preview artworks found for this aspect")
            logger.debug(f"preview.no_aspect_match: aspect={aspect_ratio}, falling back to all {len(all_options)} available artworks")
            options = all_options
        if key:
            for path in options:
                if path.name == key:
                    return path
            raise ValidationError("Preview artwork not found")
        # Default to first (deterministic due to sorted() in _iter_preview_art_files)
        selected = options[0]
        logger.debug(f"preview.artwork_selected: aspect={aspect_ratio}, key={key or 'default'}, selected={selected.name}")
        return selected

    def resolve_preview_artwork(self, filename: str) -> Path:
        filename_clean = (filename or "").strip()
        if not filename_clean:
            raise ValidationError("Filename is required")
        if Path(filename_clean).name != filename_clean:
            raise ValidationError("Invalid filename")
        candidates = self._iter_preview_art_files(None)
        for path in candidates:
            if path.name == filename_clean:
                return path
        raise ValidationError("Preview artwork not found")

    def _cache_dir(self, mockup_id: str) -> Path:
        return self.cache_root / mockup_id

    def _write_preview(self, image: Image.Image, cache_dir: Path) -> Path:
        ensure_dir(cache_dir)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        filename = f"preview-{ts}.jpg"
        out_path = cache_dir / filename
        image.save(out_path, format="JPEG", quality=95)
        self._trim_cache(cache_dir)
        return out_path

    def _trim_cache(self, cache_dir: Path) -> None:
        if not cache_dir.exists():
            return
        files = [p for p in cache_dir.iterdir() if p.is_file()]
        files.sort(key=lambda p: p.stat().st_mtime)
        while len(files) > MAX_CACHE_ITEMS:
            old = files.pop(0)
            try:
                old.unlink()
            except Exception:
                pass

    def _composite(self, base_img: Image.Image, art_img: Image.Image, placements: Iterable) -> Image.Image:
        warped = [transforms.warp_artwork_to_region(art_img, placement, base_img.size) for placement in placements]
        layered = compositor.composite_layers(base_img, warped)
        return compositor.flatten_to_rgb(layered)

    def generate_preview(self, mockup_id: str, *, artwork_key: str | None = None) -> Tuple[Path, str]:
        base = self._load_base_by_id(mockup_id)
        if base.status != "coordinates_ready" or base.coordinates is None:
            raise ValidationError("Coordinates are not ready for this mockup")

        base_img = loader.load_base_rgba(base.base_image)
        coords_payload = loader.load_coords(base.coordinates)
        coord_spec = validation.validate_coordinate_schema(coords_payload)
        validation.validate_corners_within_image(coord_spec, base_img.size)

        artwork_path = self._resolve_artwork(base.aspect_ratio, artwork_key)
        art_img = loader.load_artwork_rgba(artwork_path)

        composite = self._composite(base_img, art_img, coord_spec.regions)
        cache_dir = self._cache_dir(base.id)
        out_path = self._write_preview(composite, cache_dir)
        generated_at = datetime.now(timezone.utc).isoformat()
        return out_path, generated_at

    # ------------------------------------------------------------------
    # Serving helpers
    # ------------------------------------------------------------------
    def resolve_cached_file(self, mockup_id: str, filename: str) -> Path:
        cache_dir = self._cache_dir(mockup_id).resolve()
        target = (cache_dir / filename).resolve()
        if cache_dir not in target.parents and cache_dir != target.parent:
            raise ValidationError("Invalid preview path")
        if not target.exists() or not target.is_file():
            raise ValidationError("Preview not found")
        return target
