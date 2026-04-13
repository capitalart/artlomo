"""Video Service - Kinematic Preview Generation

Generates kinematic videos that showcase artwork with smooth panning,
zooming, and match-cut transitions from mockup to detail closeup.

Per ArtLomo Constitution (.clinerules):
- All videos must be 2048x2048px (matching ANALYSE_LONG_EDGE)
- Must use coordinates.json (schema_coordinates.json) for positioning
- Must use H.264 codec for web compatibility
- Must log all operations to configured LOGS_DIR
"""

from __future__ import annotations

import json
import logging
import os
import random
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
APPLICATION_ROOT = PROJECT_ROOT / "application"
NODE_BIN_DIR = PROJECT_ROOT / "node_modules" / ".bin"
VIDEO_WORKER_DIR = Path(__file__).resolve().parents[2] / "video_worker"

# Video configuration (per .clinerules)
VIDEO_OUTPUT_SIZE = (1024, 1024)
VIDEO_FRAMERATE = 24
VIDEO_SLIDE_SECONDS = 2.5
VIDEO_CROSSFADE_SECONDS = 0.5
MAX_MOCKUP_SLIDES = 5
VIDEO_FILL_SCALE_SIZE = 1100
VIDEO_CODEC = "libx264"  # H.264 for web compatibility
VIDEO_PRESET = "fast"  # Encoding speed/quality tradeoff
VIDEO_CRF = 20  # Constant Rate Factor (18-28, lower = better quality)
VIDEO_ZOOM_DEFAULT = 1.1
VIDEO_DURATION_DEFAULT = 15
VIDEO_PANNING_DEFAULT = True
ARTWORK_ZOOM_DURATION_DEFAULT = 3.0


class VideoService:
    """Service for generating kinematic preview videos."""

    def __init__(self, processed_root: Path, logs_dir: Path):
        """Initialize the video service.

        Args:
            processed_root: Path to processed artworks directory (lab/processed/)
            logs_dir: Path to logs directory (from app config)
        """
        self.processed_root = Path(processed_root)
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.last_error: str = ""

    def _get_artwork_dir(self, slug: str) -> Path:
        """Get the processed artwork directory for a slug."""
        return self.processed_root / slug

    def _compute_mockup_durations(
        self,
        ordered_mockup_ids: list[str],
        total_duration: int,
        main_artwork_seconds: float,
        locked_timings: dict[str, float],
        fps: int = 24,
    ) -> dict[str, float]:
        """Compute effective per-mockup durations with auto-math algorithm.
        
        Args:
            ordered_mockup_ids: List of mockup IDs in final order
            total_duration: Total video duration in seconds (10/15/20)
            main_artwork_seconds: Duration of main artwork segment (1.0-10.0)
            locked_timings: Dict of mockup_id -> locked duration (1.0-4.0)
            fps: Frames per second for rounding
            
        Returns:
            Dict mapping mockup_id -> effective_duration (in seconds)
        """
        if not ordered_mockup_ids:
            return {}
        
        total_duration = max(10, min(60, int(total_duration) or 15))
        main_artwork_seconds = max(1.0, min(10.0, float(main_artwork_seconds) or 4.0))
        fps = max(1, int(fps) or 24)
        
        locked_timings = locked_timings or {}
        
        # Account for crossfade time savings in final video
        # Video will have: 1 master + N mockups = (N+1) total slides
        # Crossfades between slides save time: (N+1-1) * crossfade_seconds = N * 0.5
        # So we can give mockups: available_for_mockups + (N * 0.5)
        num_mockups = len(ordered_mockup_ids)
        crossfade_savings = num_mockups * VIDEO_CROSSFADE_SECONDS
        available_for_mockups = max(0, total_duration - main_artwork_seconds + crossfade_savings)
        
        # Separate locked vs auto
        locked_sum = 0.0
        locked_ids = set()
        auto_ids = set()
        
        for mockup_id in ordered_mockup_ids:
            if mockup_id in locked_timings:
                locked_sum += locked_timings[mockup_id]
                locked_ids.add(mockup_id)
            else:
                auto_ids.add(mockup_id)
        
        auto_count = len(auto_ids)
        
        # Handle overflow: scale locked durations if needed
        scale = 1.0
        if locked_sum > available_for_mockups and locked_sum > 0:
            scale = available_for_mockups / locked_sum
        
        # Compute scaled locked durations
        locked_scaled = {}
        for mockup_id in locked_ids:
            scaled_val = locked_timings[mockup_id] * scale
            locked_scaled[mockup_id] = scaled_val
        
        # Compute remaining for auto
        locked_sum_scaled = sum(locked_scaled.values())
        remaining_for_auto = max(0, available_for_mockups - locked_sum_scaled)
        each_auto = remaining_for_auto / auto_count if auto_count > 0 else 0
        
        # Build result dict with frame-boundary rounding
        result = {}
        frame_duration = 1.0 / fps  # seconds per frame
        
        # Add locked (scaled) durations
        for mockup_id in locked_ids:
            scaled_val = locked_scaled[mockup_id]
            frames = max(1, round(scaled_val / frame_duration))
            result[mockup_id] = frames * frame_duration
        
        # Add auto durations
        for mockup_id in auto_ids:
            frames = max(1, round(each_auto / frame_duration))
            result[mockup_id] = frames * frame_duration
        
        # Drift correction: adjust last mockup to maintain exact total
        if result:
            last_id = ordered_mockup_ids[-1]
            actual_sum = sum(result.values())
            drift = available_for_mockups - actual_sum
            if abs(drift) > 1e-6:  # Significant drift
                current_last = result[last_id]
                result[last_id] = max(frame_duration, current_last + drift)
        
        return result

    def _run_node_processor(self, payload: dict) -> Optional[dict]:
        node_bin = self._resolve_binary_path("node") or self._resolve_binary_path("nodejs")
        if not node_bin:
            logger.error("Node runtime not found for video metadata processing")
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
        except Exception as exc:
            logger.exception("Node metadata processor execution failed: %s", exc)
            return None

        if result.returncode != 0:
            detail = (result.stderr or "").strip() or (result.stdout or "").strip() or "node metadata processor failed"
            logger.error("Node metadata processor failed: %s", detail[-1200:])
            return None

        raw = (result.stdout or "").strip()
        if not raw:
            return None
        try:
            parsed = json.loads(raw)
        except Exception:
            logger.error("Node metadata processor returned invalid JSON")
            return None
        return parsed if isinstance(parsed, dict) else None

    def _image_dimensions_via_node(self, image_path: Path) -> Optional[Tuple[int, int]]:
        result = self._run_node_processor({"action": "read_image_meta", "image_path": str(image_path)})
        if not result or result.get("ok") is not True:
            return None
        try:
            width = int(result.get("width") or 0)
            height = int(result.get("height") or 0)
        except Exception:
            return None
        if width <= 0 or height <= 0:
            return None
        return (width, height)

    def _get_mockup_image_paths(
        self,
        slug: str,
        max_count: int = MAX_MOCKUP_SLIDES,
        selected_filenames: Optional[list[str]] = None,
    ) -> list[Path]:
        """Select up to max_count mockups with category variety and coordinate pairing."""
        artwork_dir = self._get_artwork_dir(slug)
        from application.mockups import config as mockups_config

        mockups_dir = artwork_dir / mockups_config.MOCKUPS_SUBDIR
        if not mockups_dir.exists() or not mockups_dir.is_dir():
            return []

        if selected_filenames:
            ordered_selected: list[Path] = []
            for name in selected_filenames:
                clean_name = str(name or "").strip()
                if not clean_name:
                    continue
                candidate = mockups_dir / Path(clean_name).name
                if not candidate.exists() or not candidate.is_file():
                    logger.warning("Storyboard-selected mockup missing on disk for %s: %s", slug, clean_name)
                    continue
                ordered_selected.append(candidate)
            # Selected storyboard mockups remain renderable without coordinate JSON.
            # The worker will fall back to derived zone targets or safe center framing.
            return ordered_selected[: int(max_count)]

        candidates: list[Path] = []
        for slot in range(1, 26):
            path = mockups_dir / f"mu-{slug}-{slot:02d}.jpg"
            if path.exists() and path.is_file():
                candidates.append(path)

        if not candidates:
            discovered = sorted(mockups_dir.glob("*.jpg"))
            for path in discovered:
                stem_upper = path.stem.upper()
                if "THUMB" in stem_upper or "DETAIL" in stem_upper:
                    continue
                if path.is_file():
                    candidates.append(path)

        if not candidates:
            return []

        valid_candidates: list[tuple[Path, str]] = []
        for candidate in candidates:
            if not self._has_matching_coordinate_json(slug, candidate):
                logger.warning("Skipping mockup without matching coordinate JSON: %s", candidate.name)
                continue
            category = self._mockup_category(slug, candidate)
            valid_candidates.append((candidate, category))

        if not valid_candidates:
            logger.error("No mockups with matching coordinate JSON found for %s", slug)
            return []

        random.shuffle(valid_candidates)
        selected = [path for path, _category in valid_candidates[: int(max_count)]]
        return selected

    def _get_ordered_mockup_paths(self, slug: str, max_count: int = MAX_MOCKUP_SLIDES) -> list[Path]:
        """Deterministically select mockups with coordinate JSON, sorted by slot."""
        artwork_dir = self._get_artwork_dir(slug)
        from application.mockups import config as mockups_config

        mockups_dir = artwork_dir / mockups_config.MOCKUPS_SUBDIR
        if not mockups_dir.exists() or not mockups_dir.is_dir():
            return []

        candidates: list[Path] = []
        for slot in range(1, 26):
            path = mockups_dir / f"mu-{slug}-{slot:02d}.jpg"
            if path.exists() and path.is_file():
                candidates.append(path)

        if not candidates:
            discovered = sorted(mockups_dir.glob("*.jpg"))
            for path in discovered:
                stem_upper = path.stem.upper()
                if "THUMB" in stem_upper or "DETAIL" in stem_upper:
                    continue
                if path.is_file():
                    candidates.append(path)

        if not candidates:
            return []

        ordered: list[Path] = []
        for candidate in candidates:
            if not self._has_matching_coordinate_json(slug, candidate):
                continue
            ordered.append(candidate)

        return ordered[: int(max_count)]

    def _has_matching_coordinate_json(self, slug: str, mockup_path: Path) -> bool:
        """Require resolvable zone JSON for a mockup, preferring template_slug mapping."""
        template_slug = self._resolve_template_slug_for_mockup(slug, mockup_path)
        if template_slug:
            coord_file = self._resolve_zone_json_path(template_slug)
            if coord_file is not None:
                print(f"DEBUG: Found coordinate file {coord_file} for mockup {mockup_path}")
                return True
            return False

        # Legacy fallback when assets index/template slug is unavailable.
        file_name = f"{mockup_path.stem}.json"
        root = self._coordinates_root_path()
        if not root.exists() or not root.is_dir():
            return False
        try:
            coord_file = next(root.rglob(file_name))
            print(f"DEBUG: Found coordinate file {coord_file} for mockup {mockup_path}")
            return True
        except StopIteration:
            return False
        except Exception:
            return False

    def _category_from_template_slug(self, template_slug: str) -> Optional[str]:
        """Extract category from template slug format [aspect]-[category]-MU-[id]."""
        parts = [part for part in str(template_slug or "").strip().split("-") if part]
        if len(parts) < 4:
            return None
        upper_parts = [part.upper() for part in parts]
        try:
            mu_idx = upper_parts.index("MU")
        except ValueError:
            return None
        if mu_idx <= 1:
            return None
        return "-".join(parts[1:mu_idx]).lower()

    def _category_from_filename_stem(self, stem: str) -> Optional[str]:
        """Extract category from fallback mockup filenames like Category-Descriptor-Number."""
        parts = [part for part in str(stem or "").strip().split("-") if part]
        if not parts:
            return None
        if len(parts) >= 2 and parts[-1].isdigit():
            return "-".join(parts[:-1]).lower()
        return parts[0].lower()

    def _mockup_category(self, slug: str, mockup_path: Path) -> str:
        """Resolve mockup category from new naming convention, fallback to assets index/template."""
        stem = mockup_path.stem

        template_slug = self._resolve_template_slug_for_mockup(slug, mockup_path)
        if template_slug:
            template_category = self._category_from_template_slug(template_slug)
            if template_category:
                return template_category

        parts = [part for part in stem.split("-") if part]
        fallback_category = self._category_from_filename_stem(stem)
        if fallback_category:
            return fallback_category
        if parts:
            return parts[0].lower()
        return "uncategorised"

    def _get_detail_closeup_path(self, slug: str) -> Path:
        """Get path to detail closeup image (2048px)."""
        from application.mockups import config as mockups_config
        artwork_dir = self._get_artwork_dir(slug)
        return artwork_dir / mockups_config.MOCKUPS_SUBDIR / f"{slug}-detail-closeup.jpg"

    def _get_master_path(self, slug: str) -> Path:
        """Resolve preferred high-res source path for video opening slide."""
        artwork_dir = self._get_artwork_dir(slug)

        # Get SKU from metadata to construct filenames
        sku = str(artwork_dir.name).strip()
        meta_path = artwork_dir / f"{sku.lower()}-metadata.json"
        if not meta_path.exists():
            meta_path = artwork_dir / "metadata.json"
        if meta_path.exists():
            try:
                meta_doc = json.loads(meta_path.read_text(encoding="utf-8"))
                if isinstance(meta_doc, dict):
                    sku = str(meta_doc.get("sku") or meta_doc.get("artwork_id") or sku).strip() or sku
            except Exception:
                pass
        
        # Check assets.json as source of truth - prefer closeup_proxy (7200px) for highest quality
        assets_path = artwork_dir / f"{sku.lower()}-assets.json"
        if not assets_path.exists():
            assets_path = artwork_dir / "assets.json"
        if assets_path.exists():
            try:
                assets_doc = json.loads(assets_path.read_text(encoding="utf-8"))
                files = assets_doc.get("files") or {}
                
                # Priority 1: CLOSEUP-PROXY (7200px - highest quality)
                closeup_from_assets = files.get("closeup_proxy")
                if closeup_from_assets:
                    closeup_path = artwork_dir / closeup_from_assets
                    if closeup_path.exists() and closeup_path.is_file():
                        return closeup_path
                
                # Priority 2: MASTER as fallback
                master_from_assets = files.get("master")
                if master_from_assets:
                    master_path = artwork_dir / master_from_assets
                    if master_path.exists() and master_path.is_file():
                        return master_path
            except Exception:
                pass

        # Direct file checks with closeup_proxy first
        closeup_proxy = artwork_dir / f"{slug}-CLOSEUP-PROXY.jpg"
        if closeup_proxy.exists() and closeup_proxy.is_file():
            return closeup_proxy

        direct_master = artwork_dir / f"{slug}-MASTER.jpg"
        if direct_master.exists() and direct_master.is_file():
            return direct_master

        logger.error(
            "High-resolution sources missing for %s (expected %s or %s); falling back to standard processed image",
            slug,
            closeup_proxy.name,
            direct_master.name,
        )

        # Get ANALYSE filename from assets.json (source of truth)
        analyse_from_assets = None
        if assets_path.exists():
            try:
                assets_doc = json.loads(assets_path.read_text(encoding="utf-8"))
                files = assets_doc.get("files") or {}
                analyse_from_assets = files.get("analyse")
            except Exception:
                pass
        
        analyse_name = analyse_from_assets or f"{slug}-ANALYSE.jpg"
        analyse_path = artwork_dir / analyse_name
        if analyse_path.exists() and analyse_path.is_file():
            return analyse_path

        listing_path = artwork_dir / f"{sku.lower()}-listing.json"
        if not listing_path.exists():
            listing_path = artwork_dir / "listing.json"
        if listing_path.exists() and listing_path.is_file():
            try:
                listing = json.loads(listing_path.read_text(encoding="utf-8"))
                seo_name = str(listing.get("seo_filename") or "").strip()
                if seo_name:
                    seo_path = artwork_dir / seo_name
                    if seo_path.exists() and seo_path.is_file():
                        return seo_path
            except Exception:
                logger.exception("Failed to parse listing.json for master resolution slug=%s", slug)

        legacy_master = artwork_dir / f"{slug}.jpg"
        if legacy_master.exists() and legacy_master.is_file():
            return legacy_master
        return direct_master

    def _get_coordinates_json_path(self, slug: str) -> Path:
        """Get path to coordinates.json metadata file."""
        return self._get_artwork_dir(slug) / "coordinates.json"

    def _get_assets_index_path(self, slug: str) -> Path:
        """Get path to generated mockup assets index for this slug."""
        return self._get_artwork_dir(slug) / f"{slug}-assets.json"

    def _coordinates_root_path(self) -> Path:
        """Get canonical coordinates root for target zone metadata."""
        canonical = Path("/var/coordinates")
        if canonical.exists() and canonical.is_dir() and any(canonical.rglob("*.json")):
            return canonical
        app_var = APPLICATION_ROOT / "var" / "coordinates"
        if app_var.exists() and app_var.is_dir() and any(app_var.rglob("*.json")):
            return app_var
        return APPLICATION_ROOT / "mockups" / "catalog" / "assets" / "mockups" / "bases"

    def _get_video_output_path(self, slug: str) -> Path:
        """Get path for output video file."""
        artwork_dir = self._get_artwork_dir(slug)
        return artwork_dir / f"{slug}_NODE_V1.mp4"

    def _load_cinematic_settings(self, slug: str) -> dict:
        """Load per-artwork cinematic settings from artwork_data.json.
        
        Reads from artwork_data["video_suite"] per VIDEO_SUITE_SETTINGS_CONTRACT.
        Falls back to legacy root keys for backward compatibility.
        """
        artwork_dir = self._get_artwork_dir(slug)
        settings_path = artwork_dir / "artwork_data.json"

        full_data: dict = {}
        if settings_path.exists() and settings_path.is_file():
            try:
                parsed = json.loads(settings_path.read_text(encoding="utf-8"))
                if isinstance(parsed, dict):
                    full_data = parsed
            except Exception:
                logger.exception("Failed reading artwork_data.json for slug=%s", slug)

        # Try reading from video_suite first (new contract), fall back to root keys
        suite = dict(full_data.get("video_suite") or {})
        artwork_settings = dict(suite.get("artwork") or {})
        mockups_settings = dict(suite.get("mockups") or {})
        output_settings = dict(suite.get("output") or {})
        
        # Fallback for backward compat: if video_suite is missing/empty, read legacy root keys
        if not suite:
            logger.info("video_suite empty/missing for slug=%s, reading legacy keys", slug)
            suite = full_data
        
        # Extract duration
        duration_raw = suite.get("duration_seconds") or suite.get("video_duration", VIDEO_DURATION_DEFAULT)
        try:
            video_duration = int(float(duration_raw))
        except Exception:
            video_duration = VIDEO_DURATION_DEFAULT
        if video_duration not in (10, 15, 20):
            video_duration = VIDEO_DURATION_DEFAULT

        # Artwork settings (from nestedartu.artwork or legacy payload)
        artwork_zoom_intensity_raw = artwork_settings.get("zoom_intensity") or suite.get("artwork_zoom_intensity", VIDEO_ZOOM_DEFAULT)
        try:
            artwork_zoom_intensity = float(artwork_zoom_intensity_raw)
        except Exception:
            artwork_zoom_intensity = VIDEO_ZOOM_DEFAULT
        artwork_zoom_intensity = max(1.0, min(2.25, artwork_zoom_intensity))

        artwork_zoom_duration_raw = artwork_settings.get("zoom_duration") or suite.get("artwork_zoom_duration", ARTWORK_ZOOM_DURATION_DEFAULT)
        try:
            artwork_zoom_duration = float(artwork_zoom_duration_raw)
        except Exception:
            artwork_zoom_duration = ARTWORK_ZOOM_DURATION_DEFAULT
        artwork_zoom_duration = max(0.0, min(8.0, min(float(video_duration), artwork_zoom_duration)))

        artwork_pan_raw = artwork_settings.get("pan_enabled") if "pan_enabled" in artwork_settings else suite.get("artwork_pan_enabled", suite.get("video_panning_enabled", VIDEO_PANNING_DEFAULT))
        if isinstance(artwork_pan_raw, bool):
            artwork_pan_enabled = artwork_pan_raw
        elif isinstance(artwork_pan_raw, str):
            artwork_pan_enabled = artwork_pan_raw.strip().lower() in {"1", "true", "yes", "on"}
        else:
            artwork_pan_enabled = bool(artwork_pan_raw)

        artwork_pan_direction = str(artwork_settings.get("pan_direction") or suite.get("artwork_pan_direction", "up") or "up").strip().lower()
        if artwork_pan_direction not in {"center", "top-left", "top-right", "bottom-right", "bottom-left", "up", "down", "left", "right", "none"}:
            artwork_pan_direction = "up"

        # Mockup settings (from nested mockups or legacy payload)
        mockup_zoom_intensity_raw = mockups_settings.get("zoom_intensity") or suite.get("mockup_zoom_intensity", 1.1)
        try:
            mockup_zoom_intensity = float(mockup_zoom_intensity_raw)
        except Exception:
            mockup_zoom_intensity = 1.1
        mockup_zoom_intensity = max(1.0, min(1.2, mockup_zoom_intensity))

        mockup_zoom_duration_raw = mockups_settings.get("zoom_duration") or suite.get("mockup_zoom_duration", 2.0)
        try:
            mockup_zoom_duration = float(mockup_zoom_duration_raw)
        except Exception:
           mockup_zoom_duration = 2.0
        mockup_zoom_duration = max(0.0, min(8.0, min(float(video_duration), mockup_zoom_duration)))

        mockup_pan_raw = mockups_settings.get("pan_enabled") if "pan_enabled" in mockups_settings else suite.get("mockup_pan_enabled", False)
        if isinstance(mockup_pan_raw, bool):
            mockup_pan_enabled = mockup_pan_raw
        elif isinstance(mockup_pan_raw, str):
            mockup_pan_enabled = mockup_pan_raw.strip().lower() in {"1", "true", "yes", "on"}
        else:
            mockup_pan_enabled = bool(mockup_pan_raw)

        mockup_pan_direction = str(mockups_settings.get("pan_direction") or suite.get("mockup_pan_direction", "up") or "up").strip().lower()
        if mockup_pan_direction not in {"center", "top-left", "top-right", "bottom-right", "bottom-left", "up", "down", "left", "right", "none", "aim"}:
            mockup_pan_direction = "up"

        mockup_auto_alternate_raw = mockups_settings.get("auto_alternate_pan") if "auto_alternate_pan" in mockups_settings else suite.get("mockup_pan_auto_alternate", False)
        if isinstance(mockup_auto_alternate_raw, bool):
            mockup_auto_alternate = mockup_auto_alternate_raw
        elif isinstance(mockup_auto_alternate_raw, str):
            mockup_auto_alternate = mockup_auto_alternate_raw.strip().lower() in {"1", "true", "yes", "on"}
        else:
            mockup_auto_alternate = bool(mockup_auto_alternate_raw)

        # Selected mockups
        selected_raw = suite.get("selected_mockups")
        selected_mockups: list[str] = []
        if isinstance(selected_raw, list):
            for item in selected_raw:
                if not isinstance(item, str):
                    continue
                cleaned = item.strip()
                if not cleaned:
                    continue
                selected_mockups.append(Path(cleaned).name)
        selected_mockups = list(dict.fromkeys(selected_mockups))

        # Output settings (from nested output or legacy payload)
        video_fps = output_settings.get("fps") or suite.get("video_fps", VIDEO_FRAMERATE)
        try:
            video_fps = int(float(video_fps))
        except Exception:
            video_fps = VIDEO_FRAMERATE
        if video_fps not in {24, 30, 60}:
            video_fps = VIDEO_FRAMERATE

        video_output_size = output_settings.get("size") or suite.get("video_output_size", VIDEO_OUTPUT_SIZE[0])
        try:
            video_output_size = int(float(video_output_size))
        except Exception:
            video_output_size = VIDEO_OUTPUT_SIZE[0]
        if video_output_size not in {1024, 1536, 1920, 2560, 3840}:
            video_output_size = VIDEO_OUTPUT_SIZE[0]

        preset_raw = str(output_settings.get("encoder_preset") or suite.get("video_encoder_preset", VIDEO_PRESET) or VIDEO_PRESET).strip().lower()
        if preset_raw not in {"fast", "medium", "slow"}:
            preset_raw = VIDEO_PRESET

        source_raw = str(output_settings.get("artwork_source") or suite.get("video_artwork_source", "auto") or "auto").strip().lower()
        if source_raw not in {"auto", "closeup_proxy", "master"}:
            source_raw = "auto"

        order_raw = suite.get("video_mockup_order")
        video_mockup_order: list[str] = []
        if isinstance(order_raw, list):
            for item in order_raw:
                if not isinstance(item, str):
                    continue
                cleaned = item.strip()
                if not cleaned:
                    continue
                base_id = Path(cleaned).stem
                if base_id:
                    video_mockup_order.append(base_id)
        video_mockup_order = list(dict.fromkeys(video_mockup_order))[:50]

        # Main artwork timing (seconds)
        main_artwork_seconds_raw = suite.get("main_artwork_seconds", 4.0)
        try:
            main_artwork_seconds = float(main_artwork_seconds_raw)
        except Exception:
            main_artwork_seconds = 4.0
        main_artwork_seconds = max(1.0, min(10.0, main_artwork_seconds))

        # Load per-mockup shot settings
        video_mockup_shots_raw = suite.get("video_mockup_shots")
        video_mockup_shots: list[dict] = []
        if isinstance(video_mockup_shots_raw, list):
            for shot in video_mockup_shots_raw:
                if not isinstance(shot, dict):
                    continue
                if not shot.get("id"):
                    continue
                video_mockup_shots.append(shot)

        # Load per-mockup timing locks
        video_mockup_timings_raw = suite.get("video_mockup_timings")
        video_mockup_timings: dict[str, float] = {}
        if isinstance(video_mockup_timings_raw, dict):
            for mockup_id, timing in video_mockup_timings_raw.items():
                if not isinstance(mockup_id, str):
                    continue
                mockup_id_clean = mockup_id.strip()
                if not mockup_id_clean:
                    continue
                try:
                    timing_val = float(timing)
                except Exception:
                    continue
                video_mockup_timings[mockup_id_clean] = max(1.0, min(4.0, timing_val))

        return {
            "zoom_intensity": round(artwork_zoom_intensity, 2),
            "panning_enabled": bool(artwork_pan_enabled),
            "duration_seconds": int(video_duration),
            "main_artwork_seconds": float(main_artwork_seconds),
            "artwork_zoom_duration": float(artwork_zoom_duration),
            "selected_mockups": selected_mockups,
            "video_mockup_order": video_mockup_order,
            "video_mockup_shots": video_mockup_shots,
            "video_mockup_timings": video_mockup_timings,
            "video_fps": int(video_fps),
            "video_output_size": int(video_output_size),
            "video_encoder_preset": preset_raw,
            "video_artwork_source": source_raw,
            "artwork": {
                "zoom_intensity": round(artwork_zoom_intensity, 2),
                "zoom_duration": float(artwork_zoom_duration),
                "pan_enabled": bool(artwork_pan_enabled),
                "pan_direction": artwork_pan_direction,
            },
            "mockups": {
                "zoom_intensity": round(mockup_zoom_intensity, 2),
                "zoom_duration": float(mockup_zoom_duration),
                "pan_enabled": bool(mockup_pan_enabled),
                "pan_direction": mockup_pan_direction,
                "auto_alternate": bool(mockup_auto_alternate),
            },
            "output": {
                "fps": int(video_fps),
                "size": int(video_output_size),
                "encoder_preset": preset_raw,
                "artwork_source": source_raw,
            },
        }

    def _load_mockup_coordinates(self, slug: str, mockup_id: str) -> Optional[dict]:
        """Load per-mockup coordinates from .coords.json file.
        
        Mockup coordinates typically contain artwork_rect_norm with {x, y, w, h}
        identifying where the artwork is located within the mockup image.
        
        Args:
            slug: Artwork slug
            mockup_id: Mockup base ID (e.g., "mu-slug-01")
            
        Returns:
            Coordinates dict if found and valid, None otherwise
        """
        artwork_dir = self._get_artwork_dir(slug)
        coords_path = artwork_dir / "mockups" / f"{mockup_id}.coords.json"
        
        if not coords_path.exists():
            # Only use explicit per-mockup coords files. If absent, caller should
            # fall back to zone-target resolution from canonical template metadata.
            return None
        
        try:
            coords_data = json.loads(coords_path.read_text(encoding="utf-8"))
            if not isinstance(coords_data, dict):
                return None
            # Validate and clamp normalized coordinates
            artwork_rect = coords_data.get("artwork_rect_norm")
            if isinstance(artwork_rect, dict):
                return {
                    "artwork_rect_norm": {
                        "x": max(0.0, min(1.0, float(artwork_rect.get("x", 0.5)))),
                        "y": max(0.0, min(1.0, float(artwork_rect.get("y", 0.5)))),
                        "w": max(0.0, min(1.0, float(artwork_rect.get("w", 0.3)))),
                        "h": max(0.0, min(1.0, float(artwork_rect.get("h", 0.3)))),
                    }
                }
            return coords_data
        except Exception:
            logger.debug("No valid mockup coordinates for %s/%s", slug, mockup_id)
            return None

    def _generate_mockup_coordinates_from_template(self, slug: str, mockup_id: str) -> Optional[dict]:
        """Generate per-mockup coordinates from template zone data as fallback.
        
        If per-mockup .coords.json doesn't exist, use the template's zone target point
        to create a normalized coordinate box around it.
        
        Args:
            slug: Artwork slug
            mockup_id: Mockup ID (e.g., "mu-slug-01")
            
        Returns:
            Coordinates dict with artwork_rect_norm, or None if template not found
        """
        # Try to find the template slug for this mockup
        artwork_dir = self._get_artwork_dir(slug)
        assets_path = artwork_dir / f"{slug}-assets.json"
        if not assets_path.exists():
            return None
        
        try:
            assets_data = json.loads(assets_path.read_text(encoding="utf-8"))
            assets_map = assets_data.get("mockups", {}).get("assets", {})
            slot = self._extract_slot(slug, mockup_id)
            if not slot or slot not in assets_map:
                return None
            
            slot_meta = assets_map.get(slot, {})
            template_slug = slot_meta.get("template_slug", "").strip()
            if not template_slug:
                return None
            
            # Load zone data from template
            zone_path = self._find_zone_json_path(template_slug)
            if not zone_path or not zone_path.exists():
                return None
            
            zone_data = json.loads(zone_path.read_text(encoding="utf-8"))
            zones = zone_data.get("zones", [])
            if not zones:
                return None
            
            # Extract target from first zone (default artwork location)
            zone = zones[0]
            points = zone.get("points", [])
            if not points or len(points) < 4:
                return None
            
            # Calculate zone center from 4 points (TL, TR, BR, BL)
            # Points are in PIXEL coordinates for 2048x2048 image
            xs = [float(p.get("x", 1024)) for p in points]
            ys = [float(p.get("y", 1024)) for p in points]
            center_x_px = sum(xs) / len(xs)
            center_y_px = sum(ys) / len(ys)
            
            # Convert from pixel to normalized 0..1 coordinates (image is 2048x2048)
            image_size = 2048
            norm_x = max(0.0, min(1.0, center_x_px / image_size))
            norm_y = max(0.0, min(1.0, center_y_px / image_size))
            
            # Create a small box around the center (30% width/height)
            box_width = 0.3
            box_height = 0.3
            box_x = max(0.0, min(1.0, norm_x - box_width / 2))
            box_y = max(0.0, min(1.0, norm_y - box_height / 2))
            
            logger.info("[COORD-GEN] Generated coordinates for %s/%s from template %s: center=(%.3f, %.3f) px=(%d, %d)", 
                       slug, mockup_id, template_slug, norm_x, norm_y, int(center_x_px), int(center_y_px))
            
            return {
                "artwork_rect_norm": {
                    "x": box_x,
                    "y": box_y,
                    "w": box_width,
                    "h": box_height,
                }
            }
        except Exception as e:
            logger.debug("Failed to generate coordinates from template for %s/%s: %s", slug, mockup_id, e)
            return None

    def _extract_slot(self, slug: str, mockup_id: str) -> Optional[str]:
        """Extract mockup slot number from mockup ID."""
        prefix = f"mu-{slug}-"
        if mockup_id.startswith(prefix):
            slot_str = mockup_id[len(prefix):]
            return slot_str if slot_str.isdigit() else None
        return None

    def _find_zone_json_path(self, template_slug: str) -> Optional[Path]:
        """Find zone.json file for a template slug.
        
        Template slugs are like "3x4-MUSIC-ROOM-MU-153" but stored in:
        /bases/3x4/music-room/3x4-MUSIC-ROOM-MU-153.json
        
        Strategy: extract aspect from template_slug, then search recursively
        in that aspect directory for the zone file.
        """
        base_name = f"{template_slug}.json"
        coordinates_root = self._coordinates_root_path()
        
        # Try direct matches first
        if (coordinates_root / base_name).exists():
            return coordinates_root / base_name
        
        # Extract aspect from slug (e.g., "3x4" from "3x4-MUSIC-ROOM-MU-153")
        parts = template_slug.split("-")
        if len(parts) >= 2:
            aspect = parts[0].lower()
            aspect_dir =  coordinates_root / aspect
            
            # If aspect dir exists, search recursively for the zone file
            if aspect_dir.exists() and aspect_dir.is_dir():
                # Search all subdirectories in the aspect directory
                for zone_file in aspect_dir.rglob(base_name):
                    if zone_file.exists():
                        return zone_file
        
        return None

    def _load_coordinates(self, slug: str) -> Optional[dict]:
        """Load coordinates.json metadata.

        Returns:
            Coordinates dict if found and valid, None otherwise
        """
        coords_path = self._get_coordinates_json_path(slug)
        if not coords_path.exists():
            logger.warning("Coordinates file not found: %s", coords_path)
            return None

        try:
            coords_data = json.loads(coords_path.read_text(encoding="utf-8"))
            if coords_data.get("version") != "2.0":
                logger.warning("Invalid coordinates version for %s", slug)
                return None
            return coords_data
        except Exception as e:
            logger.exception("Failed to load coordinates for %s: %s", slug, e)
            return None

    def _resolve_template_slug_for_mockup(self, slug: str, mockup_path: Path) -> Optional[str]:
        """Resolve template slug used for a generated mockup slot via assets index."""
        name = mockup_path.stem
        prefix = f"mu-{slug}-"
        if not name.startswith(prefix):
            return None

        slot = name[len(prefix):]
        if not slot.isdigit():
            return None

        assets_path = self._get_assets_index_path(slug)
        if not assets_path.exists():
            return None

        try:
            payload = json.loads(assets_path.read_text(encoding="utf-8"))
            assets_map = payload.get("mockups", {}).get("assets", {})
            slot_entry = assets_map.get(f"{int(slot):02d}") if isinstance(assets_map, dict) else None
            if not isinstance(slot_entry, dict):
                return None
            template_slug = slot_entry.get("template_slug")
            if isinstance(template_slug, str) and template_slug.strip():
                return template_slug.strip()
        except Exception:
            logger.exception("Failed reading mockup assets index for slug=%s", slug)
        return None

    def _resolve_zone_json_path(self, template_slug: str) -> Optional[Path]:
        """Resolve zone JSON by template slug from canonical coordinates root."""
        parts = [part for part in str(template_slug or "").strip().split("-") if part]
        if not parts:
            return None

        aspect = parts[0].lower()
        upper_parts = [part.upper() for part in parts]
        try:
            mu_idx = upper_parts.index("MU")
        except ValueError:
            mu_idx = -1

        category = "-".join(parts[1:mu_idx]).lower() if mu_idx > 1 else ""

        file_name = f"{template_slug}.json"
        root = self._coordinates_root_path()
        if not root.exists() or not root.is_dir():
            return None

        direct_candidates = [root / file_name]
        if aspect:
            direct_candidates.append(root / aspect / file_name)
        if aspect and category:
            direct_candidates.append(root / aspect / category / file_name)

        for candidate in direct_candidates:
            if candidate.exists() and candidate.is_file():
                return candidate

        try:
            hit = next(root.rglob(file_name))
            if hit.exists() and hit.is_file():
                return hit
        except StopIteration:
            return None
        except Exception:
            return None
        return None

    def _resolve_base_dimensions_for_template(self, template_slug: str) -> Optional[Tuple[int, int]]:
        """Resolve base PNG dimensions for a template slug."""
        parts = [part for part in str(template_slug or "").strip().split("-") if part]
        if not parts:
            return None

        aspect = parts[0].lower()
        upper_parts = [part.upper() for part in parts]
        try:
            mu_idx = upper_parts.index("MU")
        except ValueError:
            mu_idx = -1
        category = "-".join(parts[1:mu_idx]).lower() if mu_idx > 1 else ""

        root = APPLICATION_ROOT / "mockups" / "catalog" / "assets" / "mockups" / "bases"
        if not root.exists() or not root.is_dir():
            return None

        png_name = f"{template_slug}.png"
        candidates = [root / png_name]
        if aspect:
            candidates.append(root / aspect / png_name)
        if aspect and category:
            candidates.append(root / aspect / category / png_name)

        path: Optional[Path] = None
        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                path = candidate
                break
        if path is None:
            try:
                path = next(root.rglob(png_name))
            except StopIteration:
                return None
            except Exception:
                return None

        try:
            from PIL import Image as _PilImage
            with _PilImage.open(str(path)) as _img:
                w, h = _img.size
                return (int(w), int(h)) if w > 0 and h > 0 else None
        except Exception:
            logger.debug("Failed reading PNG dimensions for template_slug=%s at %s", template_slug, path)
            return None

    def _load_mockup_zone_target(self, slug: str, mockup_path: Path) -> Optional[Tuple[float, float]]:
        """Load target center from perspective zone JSON for a generated mockup."""
        template_slug = self._resolve_template_slug_for_mockup(slug, mockup_path)
        if not template_slug:
            return None

        zone_path = self._resolve_zone_json_path(template_slug)
        if not zone_path:
            logger.info("No zone JSON found for template_slug=%s", template_slug)
            return None

        try:
            payload = json.loads(zone_path.read_text(encoding="utf-8"))
            zones = payload.get("zones")
            if not isinstance(zones, list) or not zones:
                return None
            first_zone = zones[0] if isinstance(zones[0], dict) else None
            points = first_zone.get("points") if isinstance(first_zone, dict) else None
            if not isinstance(points, list) or len(points) < 4:
                return None

            xs: list[float] = []
            ys: list[float] = []
            for point in points:
                if not isinstance(point, dict):
                    continue
                x_raw = point.get("x")
                y_raw = point.get("y")
                if not isinstance(x_raw, (int, float, str)) or not isinstance(y_raw, (int, float, str)):
                    continue
                try:
                    x_val = float(x_raw)
                    y_val = float(y_raw)
                except Exception:
                    continue
                xs.append(x_val)
                ys.append(y_val)

            if len(xs) < 2 or len(ys) < 2:
                return None

            target_x = (min(xs) + max(xs)) / 2.0
            target_y = (min(ys) + max(ys)) / 2.0

            source_dims = self._resolve_base_dimensions_for_template(template_slug)
            if source_dims is not None:
                source_w, source_h = source_dims
            else:
                source_w = max(xs)
                source_h = max(ys)

            if source_w <= 0 or source_h <= 0:
                return None

            return (max(0.0, min(1.0, target_x / float(source_w))), max(0.0, min(1.0, target_y / float(source_h))))
        except Exception:
            logger.exception("Failed parsing zone target for slug=%s template=%s", slug, template_slug)
            return None

    def _mockup_targets(self, slug: str, mockup_paths: list[Path]) -> list[tuple[Path, float, float]]:
        """Resolve per-mockup target centers from zone metadata with safe center fallback."""
        targets: list[tuple[Path, float, float]] = []
        for path in mockup_paths[:MAX_MOCKUP_SLIDES]:
            zone_target = self._load_mockup_zone_target(slug, path)
            if zone_target is None:
                targets.append((path, 0.5, 0.5))
            else:
                targets.append((path, zone_target[0], zone_target[1]))
        return targets

    def _master_orientation_mode(self, master_path: Path) -> str:
        """Classify master orientation for opening movement direction."""
        dims = self._image_dimensions_via_node(master_path)
        if not dims:
            width, height = (1, 1)
        else:
            width, height = dims

        if width > height:
            return "landscape"
        if height > width:
            return "portrait"
        return "square"

    def generate_kinematic_video(self, slug: str) -> bool:
        """Generate a kinematic preview video for an artwork.

        The video showcases the artwork with a cinematic pan-and-zoom effect:
        1. Start at mockup center (2048x2048 canvas)
        2. Pan smoothly toward artwork detail location (using coordinates.json)
        3. Zoom into the detail closeup with a match-cut effect
        4. Hold on detail closeup for final reveal

        Args:
            slug: Artwork slug

        Returns:
            True if video generation succeeded, False otherwise
        """
        self.last_error = ""
        cinematic_settings = self._load_cinematic_settings(slug)
        selected_mockups = list(cinematic_settings.get("selected_mockups") or [])
        video_mockup_order = list(cinematic_settings.get("video_mockup_order") or [])
        selected_ids = [Path(name).stem for name in selected_mockups if name]

        auto_paths: list[Path] = []
        auto_ids: list[str] = []
        if not selected_ids:
            auto_paths = self._get_ordered_mockup_paths(slug, max_count=MAX_MOCKUP_SLIDES)
            auto_ids = [path.stem for path in auto_paths]

        base_ids = selected_ids or auto_ids
        if video_mockup_order:
            ordered = [mockup_id for mockup_id in video_mockup_order if mockup_id in base_ids]
            remainder = [mockup_id for mockup_id in base_ids if mockup_id not in ordered]
            final_ids = ordered + remainder
        else:
            final_ids = base_ids

        if selected_ids:
            id_to_filename = {Path(name).stem: Path(name).name for name in selected_mockups}
            ordered_filenames = [id_to_filename[mockup_id] for mockup_id in final_ids if mockup_id in id_to_filename]
            mockup_paths = self._get_mockup_image_paths(slug, selected_filenames=ordered_filenames)
        else:
            id_to_path = {path.stem: path for path in auto_paths}
            mockup_paths = [id_to_path[mockup_id] for mockup_id in final_ids if mockup_id in id_to_path]

        if not mockup_paths:
            if selected_mockups:
                self.last_error = f"Selected storyboard mockups are unavailable or missing coordinates for {slug}"
            else:
                self.last_error = f"No mockup images with matching coordinate JSON found for {slug}"
            logger.error("%s", self.last_error)
            return False

        master_path = self._get_master_path(slug)
        if not master_path.exists() or not master_path.is_file():
            self.last_error = f"Master image not found for {slug}"
            logger.error("%s", self.last_error)
            return False
        master_mode = self._master_orientation_mode(master_path)

        output_path = self._get_video_output_path(slug)

        try:
            # Always include master artwork slide at the beginning
            include_master_slide = True
            success = self._generate_with_ffmpeg(
                slug=slug,
                master_path=master_path,
                master_mode=master_mode,
                mockup_paths=mockup_paths,
                output_path=output_path,
                cinematic_settings=cinematic_settings,
                include_master_slide=include_master_slide,
            )

            if success:
                duration_seconds = float(cinematic_settings.get("duration_seconds") or VIDEO_DURATION_DEFAULT)
                fps_used = int(cinematic_settings.get("video_fps") or VIDEO_FRAMERATE)
                self._log_generation(slug, output_path, duration_seconds, fps_used)
                logger.info("Generated kinematic video for %s: %s", slug, output_path)
                self.last_error = ""
                return True
            else:
                if not self.last_error:
                    self.last_error = f"Node video worker generation failed for {slug}"
                logger.error("%s", self.last_error)
                return False

        except Exception as e:
            self.last_error = f"Failed to generate kinematic video for {slug}: {e}"
            logger.exception("Failed to generate kinematic video for %s: %s", slug, e)
            return False

    def _generate_with_ffmpeg(
        self,
        slug: str,
        master_path: Path,
        master_mode: str,
        mockup_paths: list[Path],
        output_path: Path,
        cinematic_settings: dict,
        include_master_slide: bool,
    ) -> bool:
        """Bridge to Node render worker via xvfb-run for 60fps output."""
        if not mockup_paths:
            return False

        node_bin = self._resolve_binary_path("node") or self._resolve_binary_path("nodejs")
        if not node_bin:
            self.last_error = "Node runtime not found (tried node/nodejs and common system paths)"
            logger.error("%s", self.last_error)
            return False

        ffmpeg_bin = self._resolve_binary_path("ffmpeg")
        if not ffmpeg_bin:
            self.last_error = f"FFmpeg runtime not found (tried PATH, /usr/bin, /usr/local/bin, and {NODE_BIN_DIR})"
            logger.error("%s", self.last_error)
            return False

        output_size = int(cinematic_settings.get("video_output_size") or VIDEO_OUTPUT_SIZE[0])
        fps = int(cinematic_settings.get("video_fps") or VIDEO_FRAMERATE)
        requested_duration = int(cinematic_settings.get("duration_seconds") or VIDEO_DURATION_DEFAULT)
        encoder_preset = str(cinematic_settings.get("video_encoder_preset") or VIDEO_PRESET)
        artwork_source = str(cinematic_settings.get("video_artwork_source") or "auto")
        # Extract global mockup pan settings from cinematic settings
        mockup_pan_enabled = bool(cinematic_settings.get("mockup_pan_enabled") or False)
        mockup_pan_direction = str(cinematic_settings.get("mockup_pan_direction") or "up").strip().lower()
        if mockup_pan_direction not in {"center", "top-left", "top-right", "bottom-right", "bottom-left", "up", "down", "left", "right", "none", "aim"}:
            mockup_pan_direction = "up"

        # Build per-mockup shots, maintaining order of mockup_paths
        video_mockup_shots_raw = list(cinematic_settings.get("video_mockup_shots") or [])
        shot_by_id = {shot.get("id"): shot for shot in video_mockup_shots_raw if shot.get("id")}
        
        # Extract mockup IDs from mockup_paths (up to MAX_MOCKUP_SLIDES)
        ordered_mockup_paths = mockup_paths[:MAX_MOCKUP_SLIDES]
        final_ids = [path.stem for path in ordered_mockup_paths]
        mockup_path_by_id = {path.stem: path for path in ordered_mockup_paths}
        
        # Build mockup_shots array in same order as mockup_paths, with defaults for missing shots
        # Also load per-mockup coordinates for aim-toward-artwork panning
        mockup_shots = []
        for mockup_id in final_ids:
            shot = None
            if mockup_id in shot_by_id:
                shot = dict(shot_by_id[mockup_id])  # Copy to avoid mutation
            else:
                # Default shot: use global mockup pan settings
                shot = {
                    "id": mockup_id,
                    "pan_enabled": mockup_pan_enabled,
                    "pan_direction": mockup_pan_direction,
                }
            
            # Load mockup-specific coordinates if available
            coords = self._load_mockup_coordinates(slug, mockup_id)

            # If explicit per-mockup coords are missing, derive from template zone target.
            # This uses canonical template metadata and avoids hardcoded normalization.
            if not coords:
                mockup_path = mockup_path_by_id.get(mockup_id)
                if mockup_path is not None:
                    zone_target = self._load_mockup_zone_target(slug, mockup_path)
                    if zone_target is not None:
                        tx, ty = zone_target
                        box_width = 0.24
                        box_height = 0.24
                        coords = {
                            "artwork_rect_norm": {
                                "x": max(0.0, min(1.0, float(tx) - box_width / 2.0)),
                                "y": max(0.0, min(1.0, float(ty) - box_height / 2.0)),
                                "w": box_width,
                                "h": box_height,
                            }
                        }
                        logger.info("[COORD] Derived zone-target coordinates for %s/%s: center=(%.3f, %.3f)", slug, mockup_id, tx, ty)

            if coords:
                shot["coordinates"] = coords
                logger.info("[COORD] Loaded coordinates for %s/%s: %s", slug, mockup_id, coords)
            else:
                # If aim mode is set but no coordinates could be resolved (e.g., legacy
                # assets.json with empty assets dict), inject center fallback so render.js
                # gets hasTarget=true at (0.5, 0.5). This produces no visible pan drift but
                # prevents a misleading wrong-direction pan in the Node worker.
                if shot.get("pan_direction") == "aim" and shot.get("pan_enabled"):
                    coords = {
                        "artwork_rect_norm": {
                            "x": 0.38,
                            "y": 0.38,
                            "w": 0.24,
                            "h": 0.24,
                        }
                    }
                    shot["coordinates"] = coords
                    logger.info("[COORD] Aim center fallback injected for %s/%s (no zone target)", slug, mockup_id)
                else:
                    logger.debug("[COORD] No coordinates found for %s/%s", slug, mockup_id)
            
            mockup_shots.append(shot)

        # Load per-mockup timings from cinematic settings
        locked_mockup_timings = {}
        if isinstance(cinematic_settings.get("video_mockup_timings"), dict):
            locked_mockup_timings = cinematic_settings["video_mockup_timings"]
        
        # Compute effective mockup durations
        total_duration = int(cinematic_settings.get("duration_seconds") or VIDEO_DURATION_DEFAULT)
        main_artwork_seconds = float(cinematic_settings.get("main_artwork_seconds") or 4.0)
        computed_mockup_durations = self._compute_mockup_durations(
            final_ids,
            total_duration,
            main_artwork_seconds,
            locked_mockup_timings,
            fps,
        )
        
        # DEBUG: Log what we're sending to render worker
        logger.info("[VIDEO] Mockup shots being sent to render worker:")
        for shot in mockup_shots:
            has_coords = "coordinates" in shot
            zoom_intensity = shot.get("zoom_intensity", "N/A")
            logger.info("[VIDEO]   - %s: pan_direction=%s, zoom_intensity=%s, has_coordinates=%s", 
                       shot.get("id"), shot.get("pan_direction"), zoom_intensity, has_coords)
            if has_coords:
                rect = shot.get("coordinates", {}).get("artwork_rect_norm", {})
                logger.info("[VIDEO]     coordinates: x=%.3f, y=%.3f, w=%.3f, h=%.3f",
                           rect.get("x", 0), rect.get("y", 0), rect.get("w", 0), rect.get("h", 0))

        # Extract nested artwork/mockup/output settings
        artwork_settings = dict(cinematic_settings.get("artwork") or {})
        mockups_settings = dict(cinematic_settings.get("mockups") or {})
        output_settings = dict(cinematic_settings.get("output") or {})
        
        # DEBUG: Log what settings were extracted
        logger.info("[VIDEO] Cinematic settings structure:")
        logger.info("[VIDEO]   artwork: %s", artwork_settings)
        logger.info("[VIDEO]   mockups keys: %s", list(mockups_settings.keys()) if mockups_settings else "EMPTY")
        logger.info("[VIDEO]   Top-level: zoom_intensity=%s, panning_enabled=%s, artwork_zoom_duration=%s",
                   cinematic_settings.get("zoom_intensity"),
                   cinematic_settings.get("panning_enabled"),
                   cinematic_settings.get("artwork_zoom_duration"))
        
        # Extract animation settings from nested structure with explicit False handling.
        artwork_zoom_intensity = float(
            artwork_settings.get("zoom_intensity")
            or cinematic_settings.get("zoom_intensity")
            or cinematic_settings.get("artwork_zoom_intensity")
            or VIDEO_ZOOM_DEFAULT
        )
        if "pan_enabled" in artwork_settings:
            artwork_pan_enabled = bool(artwork_settings.get("pan_enabled"))
        elif "panning_enabled" in cinematic_settings:
            artwork_pan_enabled = bool(cinematic_settings.get("panning_enabled"))
        else:
            artwork_pan_enabled = bool(cinematic_settings.get("artwork_pan_enabled", False))
        artwork_zoom_duration_val = float(
            artwork_settings.get("zoom_duration")
            or cinematic_settings.get("artwork_zoom_duration")
            or ARTWORK_ZOOM_DURATION_DEFAULT
        )

        logger.info("[VIDEO] Extracted animation settings: zoom_intensity=%s, pan_enabled=%s, zoom_duration=%s",
                   artwork_zoom_intensity, artwork_pan_enabled, artwork_zoom_duration_val)
        logger.info("[VIDEO] Artwork dict being passed to worker: %s", artwork_settings)
        
        payload = {
            "slug": slug,
            "master_path": str(master_path),
            "master_mode": str(master_mode),
            "mockup_paths": [str(path) for path in mockup_paths[:MAX_MOCKUP_SLIDES]],
            "output_path": str(output_path),
            "processed_root": str(self.processed_root),
            "coordinates_root": str(self._coordinates_root_path()),
            "ffmpeg_bin": str(ffmpeg_bin),
            "render_status_path": str(self._get_artwork_dir(slug) / "video_render_status.json"),
            "video": {
                "width": int(output_size),
                "height": int(output_size),
                "fps": int(fps),
                "slide_seconds": float(VIDEO_SLIDE_SECONDS),
                "crossfade_seconds": float(VIDEO_CROSSFADE_SECONDS),
                "fill_scale_size": int(VIDEO_FILL_SCALE_SIZE),
                "codec": VIDEO_CODEC,
                "preset": encoder_preset,
                "crf": int(VIDEO_CRF),
                "zoom_intensity": artwork_zoom_intensity,
                "panning_enabled": artwork_pan_enabled,
                "duration_seconds": int(requested_duration),
                "main_artwork_seconds": float(main_artwork_seconds),
                "artwork_zoom_duration": artwork_zoom_duration_val,
                "include_master_slide": bool(include_master_slide),
                "output_size": int(output_size),
                "encoder_preset": encoder_preset,
                "artwork_source": artwork_source,
                "mockup_shots": mockup_shots,
                "mockup_timings": locked_mockup_timings,
                "computed_mockup_durations": computed_mockup_durations,
                "selected_mockups": final_ids,
                "artwork": artwork_settings,
                "mockups": mockups_settings,
                "output": output_settings,
            },
        }

        render_status_path = Path(payload["render_status_path"])
        render_status_path.parent.mkdir(parents=True, exist_ok=True)

        worker_args = [
            node_bin,
            str(VIDEO_WORKER_DIR / "render.js"),
            json.dumps(payload, ensure_ascii=True, separators=(",", ":")),
        ]
        xvfb_bin = self._resolve_binary_path("xvfb-run")
        if xvfb_bin:
            cmd = [xvfb_bin, "-a", *worker_args]
        else:
            logger.warning("xvfb-run not found; running video worker without xvfb")
            cmd = worker_args

        try:
            # Timeout scales with render complexity to reduce false negatives on heavier profiles.
            # Baseline (10s @ 1024px @ 24fps) remains near 180s, with extra headroom for larger settings.
            duration_factor = max(1.0, float(requested_duration) / 10.0)
            size_factor = max(1.0, float(output_size) / 1024.0)
            fps_factor = max(1.0, float(fps) / 24.0)
            timeout_seconds = int(max(180, min(900, round(180 * duration_factor * size_factor * fps_factor))))

            env = os.environ.copy()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=env,
            )

            if result.returncode != 0:
                stderr = (result.stderr or "").strip()
                stdout = (result.stdout or "").strip()
                detail = stderr or stdout or "Node worker exited with non-zero status"
                self.last_error = f"Node video worker error: {detail[-1000:]}"
                logger.error("%s", self.last_error)
                return False

            if not output_path.exists() or output_path.stat().st_size == 0:
                self.last_error = "Node video output file missing or empty"
                logger.error("%s", self.last_error)
                return False

            return True

        except subprocess.TimeoutExpired:
            self.last_error = f"Node video worker timeout after {timeout_seconds} seconds"
            logger.error("%s", self.last_error)
            return False
        except Exception as e:
            self.last_error = f"Node video worker execution failed: {e}"
            logger.exception("Node video worker execution failed: %s", e)
            return False

    def _resolve_binary_path(self, name: str) -> Optional[str]:
        """Resolve executable path in restricted service PATH environments."""
        binary = str(name or "").strip()
        if not binary:
            return None

        resolved = shutil.which(binary)
        if resolved:
            return resolved

        for candidate in (
            f"/usr/bin/{binary}",
            f"/usr/local/bin/{binary}",
            str(NODE_BIN_DIR / binary),
        ):
            path = Path(candidate)
            if path.exists() and path.is_file():
                return str(path)
        return None

    def _log_generation(self, slug: str, output_path: Path, duration_seconds: float, fps_used: int = 24) -> None:
        """Log video generation to filesystem (per Constitution).

        Args:
            slug: Artwork slug
            output_path: Path to generated video
            duration_seconds: Video duration in seconds
            fps_used: Actual FPS used for rendering (default: 24)
        """
        try:
            timestamp = datetime.now().strftime("%a-%d-%b-%Y-%I-%M-%p")
            log_path = self.logs_dir / "kinematic-video-logs.log"

            file_size_mb = output_path.stat().st_size / (1024 * 1024)

            log_entry = (
                f"[{timestamp}] Generated kinematic video for {slug}\n"
                f"  Output: {output_path}\n"
                f"  Size: {file_size_mb:.2f} MB\n"
                f"  Resolution: {VIDEO_OUTPUT_SIZE[0]}x{VIDEO_OUTPUT_SIZE[1]}\n"
                f"  Duration: {duration_seconds:.2f}s @ {fps_used}fps\n"
                f"  Encoder Preset: (detected from cinematic_settings)\n"
                "\n"
            )

            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_entry)

        except Exception as e:
            logger.exception("Failed to write log entry: %s", e)

    def has_kinematic_video(self, slug: str) -> bool:
        """Check if a kinematic video exists for this artwork.

        Args:
            slug: Artwork slug

        Returns:
            True if video file exists
        """
        return self._get_video_output_path(slug).exists()

    def get_video_url(self, slug: str) -> Optional[str]:
        """Get the URL to the kinematic video.

        Args:
            slug: Artwork slug

        Returns:
            URL string if video exists, None otherwise
        """
        video_path = self._get_video_output_path(slug)
        if video_path.exists() and video_path.is_file():
            try:
                version = int(video_path.stat().st_mtime_ns)
            except Exception:
                version = int(time.time() * 1_000_000_000)
            return f"/artwork/{slug}/video?v={version}"
        return None
