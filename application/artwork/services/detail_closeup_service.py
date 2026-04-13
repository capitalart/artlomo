# CLINE_DIRECTIVE: Detail crops must generate a companion .json coordinate file (schema_coordinates.json) for the VideoService.

"""Detail Closeup Generator & Editor Service

Handles generation of proxy preview images and final crop rendering for detail closeup editing.

The Detail Closeup feature allows artists to:
1. Select a zoomed region of the master artwork
2. Edit scale/pan interactively in a 2000x2000 viewport
3. Save the final crop as a registered mockup derivative

Key Architecture:
- Uses master image (14400px) for final render (perfect quality)
- Uses proxy preview (long edge 7200px) for interactive editor (fast UI)
- Stores crops as "detail-<slug>" mockup entries with slot=0
- Non-destructive: original master and analysis remain unchanged
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)
VIDEO_WORKER_DIR = Path(__file__).resolve().parents[2] / "video_worker"

# Detail closeup configuration
DETAIL_CLOSEUP_OUTPUT_SIZE = (2048, 2048)  # Final output is always 2048x2048 (per .clinerules)
DETAIL_PROXY_LONG_EDGE = 7200  # Proxy image for editor (fast, sufficient detail)
DETAIL_CLOSEUP_QUALITY = 95  # JPEG quality for saved closeup
DETAIL_CLOSEUP_SLOT = 999  # Reserved slot for detail closeup mockup entry

# === Photoshop Calibration & Real-World Metrics ===
MASTER_WIDTH = 14400  # Master artwork dimensions (square)
MASTER_HEIGHT = 14400
VIEWPORT_SIZE = 500  # Frontend viewport dimensions (square)
CROP_OUTPUT_SIZE = 2048  # Final crop output dimensions (square)

# Scale factor: number of master pixels per viewport pixel at 100% (Photoshop standard)
# 14400 px master / 500 px viewport = 28.8 scale
SCALE_100_PERCENT = MASTER_WIDTH / VIEWPORT_SIZE  # 28.8

# Direct Cut: scale needed to view exactly 2048 pixels of master in viewport
# 14400 / 2048 = 7.03125 (this is the "ideal" zoom for 2048px crop)
SCALE_DIRECT_CUT = MASTER_WIDTH / CROP_OUTPUT_SIZE  # 7.03125

# Fit: scale to show entire master in viewport
SCALE_FIT = 1.0


class DetailCloseupService:
    """Service for detail closeup generation, preview, and crop rendering."""

    def __init__(self, processed_root: Path):
        """Initialize service.

        Args:
            processed_root: Path to processed artworks directory (lab/processed/)
        """
        self.processed_root = Path(processed_root)

    def _get_artwork_dir(self, slug: str) -> Path:
        """Get the processed artwork directory for a slug."""
        return self.processed_root / slug

    def _get_master_image_path(self, slug: str) -> Path:
        """Get path to master image (original uploaded file).

        Search order (uses assets.json as single source of truth):
        1. assets.json "master" entry
        2. [slug]-MASTER.jpg (fallback)
        3. seo_filename (from listing.json)
        4. [slug].jpg (legacy)
        """
        artwork_dir = self._get_artwork_dir(slug)

        # 0. Check assets.json first (source of truth)
        sku = slug
        meta_path = artwork_dir / f"{slug.lower()}-metadata.json"
        if not meta_path.exists():
            meta_path = artwork_dir / "metadata.json"
        if meta_path.exists():
            try:
                meta_doc = json.loads(meta_path.read_text(encoding="utf-8"))
                if isinstance(meta_doc, dict):
                    sku = str(meta_doc.get("sku") or meta_doc.get("artwork_id") or sku).strip() or sku
            except Exception:
                pass
        
        assets_path = artwork_dir / f"{sku.lower()}-assets.json"
        if not assets_path.exists():
            assets_path = artwork_dir / "assets.json"
        if assets_path.exists():
            try:
                assets_doc = json.loads(assets_path.read_text(encoding="utf-8"))
                files = assets_doc.get("files") or {}
                master_from_assets = files.get("master")
                if master_from_assets:
                    p0 = artwork_dir / master_from_assets
                    if p0.exists():
                        return p0
            except Exception:
                pass

        # 1. Check [slug]-MASTER.jpg
        p1 = artwork_dir / f"{slug}-MASTER.jpg"
        if p1.exists():
            return p1

        # 2. Check seo_filename from listing.json
        listing_path = artwork_dir / f"{sku.lower()}-listing.json"
        if not listing_path.exists():
            listing_path = artwork_dir / "listing.json"
        if listing_path.exists():
            try:
                doc = json.loads(listing_path.read_text(encoding="utf-8"))
                seo_name = doc.get("seo_filename")
                if seo_name:
                    p2 = artwork_dir / seo_name
                    if p2.exists():
                        return p2
            except Exception:
                pass

        # 3. Check [slug].jpg (legacy)
        p3 = artwork_dir / f"{slug}.jpg"
        if p3.exists():
            return p3

        # Fallback to [slug]-MASTER.jpg
        return p1

    def _get_proxy_image_path(self, slug: str) -> Path:
        """Get path to proxy preview image (used for editor UI)."""
        return self._get_artwork_dir(slug) / f"{slug}-CLOSEUP-PROXY.jpg"

    def _get_detail_closeup_path(self, slug: str) -> Path:
        """Get path to saved detail closeup image."""
        from application.mockups import config as mockups_config
        artwork_dir = self._get_artwork_dir(slug)
        mockup_name = f"{slug}-detail-closeup.jpg"
        return artwork_dir / mockups_config.MOCKUPS_SUBDIR / mockup_name

    def _get_detail_closeup_thumb_path(self, slug: str) -> Path:
        """Get path to detail closeup thumbnail."""
        from application.mockups import config as mockups_config
        artwork_dir = self._get_artwork_dir(slug)
        thumb_name = f"{slug}-detail-closeup.jpg"
        return artwork_dir / mockups_config.MOCKUPS_SUBDIR / "thumbs" / thumb_name

    def _get_coordinates_json_path(self, slug: str) -> Path:
        """Get path to coordinates.json metadata file."""
        artwork_dir = self._get_artwork_dir(slug)
        return artwork_dir / "coordinates.json"

    def _resolve_binary_path(self, name: str) -> Optional[str]:
        binary = str(name or "").strip()
        if not binary:
            return None

        resolved = shutil.which(binary)
        if resolved:
            return resolved

        for candidate in (
            f"/usr/bin/{binary}",
            f"/usr/local/bin/{binary}",
            str((Path(__file__).resolve().parents[3] / "node_modules" / ".bin" / binary)),
        ):
            path = Path(candidate)
            if path.exists() and path.is_file():
                return str(path)
        return None

    def _run_node_processor(self, payload: dict) -> Optional[dict]:
        node_bin = self._resolve_binary_path("node") or self._resolve_binary_path("nodejs")
        if not node_bin:
            logger.error("Node runtime not found for detail processing")
            return None

        worker_args = [
            node_bin,
            str(VIDEO_WORKER_DIR / "processor.js"),
            json.dumps(payload, ensure_ascii=True, separators=(",", ":")),
        ]
        xvfb_bin = self._resolve_binary_path("xvfb-run")
        cmd = [xvfb_bin, "-a", *worker_args] if xvfb_bin else worker_args

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=os.environ.copy())
            if result.returncode != 0:
                detail = (result.stderr or "").strip() or (result.stdout or "").strip() or "node worker failed"
                logger.error("Node detail processor failed: %s", detail[-1200:])
                return None

            raw = (result.stdout or "").strip()
            if not raw:
                logger.error("Node detail processor returned empty stdout")
                return None
            payload_out = json.loads(raw)
            return payload_out if isinstance(payload_out, dict) else None
        except Exception as exc:
            logger.exception("Node detail processor execution failed: %s", exc)
            return None

    def generate_proxy_preview(self, slug: str) -> bool:
        """Generate a proxy preview image for the detail closeup editor.

        The proxy image is a downsampled version of the master (long edge specified)
        that provides good detail while being fast to load and manipulate in the browser.

        Args:
            slug: Artwork slug

        Returns:
            True if successful, False if master not found or error occurred
        """
        master_path = self._get_master_image_path(slug)
        proxy_path = self._get_proxy_image_path(slug)

        if not master_path.exists():
            logger.warning(
                "Master image not found for detail closeup proxy: %s", master_path
            )
            return False

        # Ensure parent directory exists
        proxy_path.parent.mkdir(parents=True, exist_ok=True)
        if not os.access(str(proxy_path.parent), os.W_OK):
            logger.error("Proxy directory not writable: %s", proxy_path.parent)
            return False

        payload = {
            "action": "generate_proxy",
            "master_path": str(master_path),
            "output_path": str(proxy_path),
            "long_edge": int(DETAIL_PROXY_LONG_EDGE),
            "quality": 80,
        }
        result = self._run_node_processor(payload)
        if not result or result.get("ok") is not True:
            return False

        logger.info("Generated detail closeup proxy: %s", proxy_path)
        return True

    def has_closeup_proxy(self, slug: str) -> bool:
        path = self._get_proxy_image_path(slug)
        return path.exists()

    def ensure_proxy_available(self, slug: str) -> bool:
        path = self._get_proxy_image_path(slug)
        if path.exists():
            return True
        logger.warning("Closeup proxy missing for %s; generating on-demand", slug)
        return self.generate_proxy_preview(slug)

    def render_detail_crop(
        self,
        slug: str,
        norm_x: float,
        norm_y: float,
        scale: float,
    ) -> bool:
        """Render the final detail closeup crop from the master image using ABSOLUTE CENTER mapping.

        The final crop is computed by:
        1. Loading the full master image (e.g., 14400px)
        2. Mapping normalized center coordinates (0.0-1.0) directly to master pixels
        3. Building a 2048x2048 crop box centered on that point
        4. Clamping to image bounds
        5. Extracting the crop region
        6. Resizing to exactly 2048x2048px with LANCZOS resampling
        7. Saving as high-quality JPEG

        Coordinate System (Absolute Center):
        - norm_x, norm_y are image-space coordinates (0.0 = left/top, 1.0 = right/bottom)
        - These are INDEPENDENT of scale/pan (calculated from proxy center)
        - Maps directly to master image coordinates
        - No offset ambiguity

        Args:
            slug: Artwork slug
            norm_x: Normalized X center on proxy (0.0-1.0)
            norm_y: Normalized Y center on proxy (0.0-1.0)
            scale: Zoom scale (for logging only, not used in crop calculation)

        Returns:
            True if successful, False if master not found or error occurred

        Raises:
            ValueError: If normalized coordinates are invalid
        """
        master_path = self._get_master_image_path(slug)

        if not master_path.exists():
            logger.warning("Master image not found for detail crop render: %s", master_path)
            return False

        # Validate normalized coordinates
        if not (0.1 <= float(scale) <= 10.0):
            raise ValueError(f"Invalid scale {scale}: must be between 0.1 and 10.0")

        if not (0.0 <= norm_x <= 1.0 and 0.0 <= norm_y <= 1.0):
            raise ValueError(
                f"Invalid normalized coordinates ({norm_x}, {norm_y}): must be 0.0-1.0"
            )
        
        try:
            detail_path = self._get_detail_closeup_path(slug)
            detail_path.parent.mkdir(parents=True, exist_ok=True)

            payload = {
                "action": "render_detail",
                "master_path": str(master_path),
                "output_path": str(detail_path),
                "norm_x": float(norm_x),
                "norm_y": float(norm_y),
                "output_size": int(DETAIL_CLOSEUP_OUTPUT_SIZE[0]),
                "quality": int(DETAIL_CLOSEUP_QUALITY),
            }
            result = self._run_node_processor(payload)
            if not result or result.get("ok") is not True:
                return False

            master_width = int(result.get("master_width") or 0)
            master_height = int(result.get("master_height") or 0)
            center_px_x = float(result.get("center_px_x") or 0.0)
            center_px_y = float(result.get("center_px_y") or 0.0)
            master_crop_width = float(result.get("crop_width") or 0.0)
            master_crop_height = float(result.get("crop_height") or 0.0)
            if master_width <= 0 or master_height <= 0 or master_crop_width <= 0 or master_crop_height <= 0:
                raise ValueError("Node worker returned invalid detail metadata")

            # Generate thumbnail (500x500 center-crop/resize)
            try:
                from application.upload.services.thumb_service import create_detail_closeup_thumb

                thumb_path = self._get_detail_closeup_thumb_path(slug)
                create_detail_closeup_thumb(detail_path, thumb_path)
                logger.info("Generated detail closeup thumbnail: %s", thumb_path)
            except Exception as te:
                logger.warning("Failed to generate detail closeup thumbnail: %s", te)

            logger.info(
                "Rendered detail closeup for %s: norm=(%.4f,%.4f) scale=%.2f -> %s",
                slug,
                norm_x,
                norm_y,
                scale,
                detail_path,
            )

            self._generate_coordinates_json(
                slug,
                master_width,
                master_height,
                center_px_x,
                center_px_y,
                master_crop_width,
                master_crop_height,
            )
            return True

        except Exception as e:
            logger.exception(
                "Failed to render detail crop for %s (norm_x=%.4f, norm_y=%.4f, scale=%.2f): %s",
                slug,
                norm_x,
                norm_y,
                scale,
                e,
            )
            return False

    def _generate_coordinates_json(
        self,
        slug: str,
        master_width: int,
        master_height: int,
        center_x: float,
        center_y: float,
        crop_width: float,
        crop_height: float,
    ) -> None:
        """Generate coordinates.json metadata file for kinematic video generation.

        Follows schema defined in application/docs/schema_coordinates.json.
        All coordinates are normalized (0.0 to 1.0).

        Args:
            slug: Artwork slug
            master_width: Master image width in pixels
            master_height: Master image height in pixels
            center_x: Center X coordinate of crop in master space (pixels)
            center_y: Center Y coordinate of crop in master space (pixels)
            crop_width: Crop width in master space (pixels)
            crop_height: Crop height in master space (pixels)
        """
        try:
            # Normalize coordinates (0.0 to 1.0)
            norm_center_x = center_x / master_width
            norm_center_y = center_y / master_height
            norm_width_pct = crop_width / master_width
            norm_height_pct = crop_height / master_height

            # Clamp to valid range
            norm_center_x = max(0.0, min(1.0, norm_center_x))
            norm_center_y = max(0.0, min(1.0, norm_center_y))
            norm_width_pct = max(0.0, min(1.0, norm_width_pct))
            norm_height_pct = max(0.0, min(1.0, norm_height_pct))

            coordinates_data = {
                "slug": slug,
                "version": "2.0",
                "coordinates": {
                    "center_x": round(norm_center_x, 4),
                    "center_y": round(norm_center_y, 4),
                    "width_pct": round(norm_width_pct, 4),
                    "height_pct": round(norm_height_pct, 4),
                },
                "dimensions": {
                    "canvas_width_px": 2048,
                    "canvas_height_px": 2048,
                    "is_normalized": True,
                },
                "kinematic_hints": {
                    "panning_direction": "center-to-artwork",
                    "zoom_factor": 1.5,
                },
            }

            coords_path = self._get_coordinates_json_path(slug)
            coords_path.write_text(json.dumps(coordinates_data, indent=2), encoding="utf-8")

            logger.info(
                "Generated coordinates.json for %s: center=(%.4f,%.4f) size=(%.4f,%.4f)",
                slug,
                norm_center_x,
                norm_center_y,
                norm_width_pct,
                norm_height_pct,
            )

        except Exception as e:
            logger.exception("Failed to generate coordinates.json for %s: %s", slug, e)

    def get_detail_closeup_url(self, slug: str) -> Optional[str]:
        """Get the URL to a saved detail closeup, if it exists.

        Args:
            slug: Artwork slug

        Returns:
            URL string if detail closeup exists, None otherwise
        """
        detail_path = self._get_detail_closeup_path(slug)
        if detail_path.exists():
            # Use same URL pattern as mockup composite
            return f"/artwork/{slug}/detail-closeup"
        return None

    def has_detail_closeup(self, slug: str) -> bool:
        """Check if a detail closeup has been saved for this artwork.

        Args:
            slug: Artwork slug

        Returns:
            True if detail closeup file exists
        """
        return self._get_detail_closeup_path(slug).exists()
