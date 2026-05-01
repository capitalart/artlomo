"""Video Routes - API endpoints and Director's Suite workspace."""

from __future__ import annotations

import logging
import json
import re
from pathlib import Path

from flask import Blueprint, abort, current_app, jsonify, render_template, request, url_for

from application.config import AppConfig
from application import config as app_config
from application.routes.auth_routes import login_required
from application.common.utilities import slug_sku
from application.utils.csrf import require_csrf_or_400
from application.video.services.video_service import MAX_MOCKUP_SLIDES, VideoService
from application.artwork.routes.artwork_routes import _resolve_review_target

logger = logging.getLogger(__name__)

# Create blueprint
video_bp = Blueprint("video", __name__, url_prefix="/api/video")
video_workspace_bp = Blueprint("video_workspace", __name__)

VIDEO_ZOOM_DEFAULT = 1.1
VIDEO_PANNING_DEFAULT = True
VIDEO_DURATION_DEFAULT = 15
ARTWORK_ZOOM_DURATION_DEFAULT = 3.0
SLOT_RE = re.compile(r"^mu-(?P<slug>[a-z0-9-]+)-(?P<slot>\d{2})\.jpg$", re.IGNORECASE)


def _logs_dir(config_map) -> Path:
    configured = config_map.get("LOGS_DIR") if hasattr(config_map, "get") else None
    if configured:
        return Path(configured)
    return Path(app_config.LOGS_DIR)


def _read_json_silent(path: Path) -> dict:
    if not path.exists() or not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _normalize_mockup_shots(raw) -> list:
    """Normalize video_mockup_shots array.
    
    Each shot dict must have "id" and may have "pan_enabled", "pan_direction",
    "zoom_enabled", "pan_to_artwork_center", "auto_target".
    De-dupes by id, clamping length to 50.
    """
    shots: list = []
    seen_ids: set = set()
    
    if not isinstance(raw, list):
        return shots
    
    for item in raw:
        if not isinstance(item, dict):
            continue
        
        shot_id = str(item.get("id") or "").strip()
        if not shot_id or shot_id in seen_ids:
            continue
        
        # Pan enabled
        pan_enabled_raw = item.get("pan_enabled", True)
        if isinstance(pan_enabled_raw, bool):
            pan_enabled = pan_enabled_raw
        elif isinstance(pan_enabled_raw, str):
            pan_enabled = pan_enabled_raw.strip().lower() in {"1", "true", "yes", "on"}
        else:
            pan_enabled = bool(pan_enabled_raw)
        
        # Pan direction (default "up" to match JavaScript)
        # Now supports "aim" for auto-aim toward artwork center
        pan_direction_raw = str(item.get("pan_direction", "up") or "up").strip().lower()
        if pan_direction_raw not in {"none", "aim", "up", "down", "left", "right"}:
            pan_direction_raw = "up"
        
        # Rule: If direction is "none", force pan_enabled to False
        if pan_direction_raw == "none":
            pan_enabled = False
        
        # Zoom enabled
        zoom_enabled_raw = item.get("zoom_enabled", True)
        if isinstance(zoom_enabled_raw, bool):
            zoom_enabled = zoom_enabled_raw
        elif isinstance(zoom_enabled_raw, str):
            zoom_enabled = zoom_enabled_raw.strip().lower() in {"1", "true", "yes", "on"}
        else:
            zoom_enabled = bool(zoom_enabled_raw)

        # Per-mockup zoom intensity
        zoom_intensity_raw = item.get("zoom_intensity", None)
        zoom_intensity = None
        if zoom_intensity_raw is not None:
            try:
                zoom_intensity = float(zoom_intensity_raw)
                zoom_intensity = max(1.0, min(2.25, zoom_intensity))
            except Exception:
                zoom_intensity = None
        
        # Rule: If direction is "aim", derive auto_target from it
        pan_to_artwork_center = (pan_direction_raw == "aim")
        
        # Backward compatibility: also read legacy aim fields if direction not "aim"
        if pan_direction_raw != "aim":
            aim_raw = item.get("pan_to_artwork_center") or item.get("auto_target")
            if isinstance(aim_raw, bool):
                pan_to_artwork_center = aim_raw
            elif isinstance(aim_raw, str):
                pan_to_artwork_center = aim_raw.strip().lower() in {"1", "true", "yes", "on"}
            else:
                pan_to_artwork_center = bool(aim_raw) if aim_raw else False
        
        shot = {
            "id": shot_id,
            "pan_enabled": bool(pan_enabled),
            "pan_direction": pan_direction_raw,
            "zoom_enabled": bool(zoom_enabled),
            "pan_to_artwork_center": bool(pan_to_artwork_center),
            "auto_target": bool(pan_to_artwork_center),
        }
        if zoom_intensity is not None:
            shot["zoom_intensity"] = zoom_intensity
        shots.append(shot)
        seen_ids.add(shot_id)
        
        if len(shots) >= 50:
            break
    
    return shots


def _normalize_video_settings(raw: dict | None) -> dict:
    payload = raw if isinstance(raw, dict) else {}

    ffmpeg_profile_raw = str(payload.get("video_ffmpeg_profile", "default") or "default").strip().lower()
    if ffmpeg_profile_raw not in {"default", "ffmpeg5", "ffmpeg8"}:
        ffmpeg_profile_raw = "default"

    compositor_raw = str(payload.get("video_compositor", "auto") or "auto").strip().lower()
    if compositor_raw not in {"auto", "xfade", "fade_concat", "concat"}:
        compositor_raw = "auto"

    timing_mode_raw = str(payload.get("video_timing_mode", "frame_quantized") or "frame_quantized").strip().lower()
    if timing_mode_raw not in {"frame_quantized", "time_continuous"}:
        timing_mode_raw = "frame_quantized"

    motion_profile_raw = str(payload.get("video_motion_profile", "distance_normalized") or "distance_normalized").strip().lower()
    if motion_profile_raw not in {"legacy", "distance_normalized"}:
        motion_profile_raw = "distance_normalized"

    # Duration (only 10, 15, 20 allowed)
    duration_raw = payload.get("video_duration", VIDEO_DURATION_DEFAULT)
    try:
        duration = int(float(duration_raw))
    except Exception:
        duration = VIDEO_DURATION_DEFAULT
    if duration not in (10, 15, 20):
        duration = VIDEO_DURATION_DEFAULT

    # Legacy video_zoom_intensity (fallback for artwork_zoom_intensity)
    legacy_zoom = payload.get("video_zoom_intensity", VIDEO_ZOOM_DEFAULT)
    try:
        legacy_zoom = float(legacy_zoom)
    except Exception:
        legacy_zoom = VIDEO_ZOOM_DEFAULT
    legacy_zoom = max(1.0, min(1.3, legacy_zoom))

    # Artwork settings
    artwork_zoom_intensity_raw = payload.get("artwork_zoom_intensity", legacy_zoom)
    try:
        artwork_zoom_intensity = float(artwork_zoom_intensity_raw)
    except Exception:
        artwork_zoom_intensity = legacy_zoom
    artwork_zoom_intensity = max(1.0, min(2.25, artwork_zoom_intensity))

    artwork_zoom_duration_raw = payload.get("artwork_zoom_duration", ARTWORK_ZOOM_DURATION_DEFAULT)
    try:
        artwork_zoom_duration = float(artwork_zoom_duration_raw)
    except Exception:
        artwork_zoom_duration = ARTWORK_ZOOM_DURATION_DEFAULT
    artwork_zoom_duration = max(0.0, min(8.0, min(float(duration), artwork_zoom_duration)))

    artwork_pan_raw = payload.get("artwork_pan_enabled", payload.get("video_panning_enabled", VIDEO_PANNING_DEFAULT))
    if isinstance(artwork_pan_raw, bool):
        artwork_pan_enabled = artwork_pan_raw
    elif isinstance(artwork_pan_raw, str):
        artwork_pan_enabled = artwork_pan_raw.strip().lower() in {"1", "true", "yes", "on"}
    else:
        artwork_pan_enabled = bool(artwork_pan_raw)

    artwork_pan_direction = str(payload.get("artwork_pan_direction", "up") or "up").strip().lower()
    if artwork_pan_direction not in {"center", "top-left", "top-right", "bottom-right", "bottom-left", "up", "down", "left", "right"}:
        artwork_pan_direction = "up"

    # Mockup settings
    mockup_zoom_intensity_raw = payload.get("mockup_zoom_intensity", 1.1)
    try:
        mockup_zoom_intensity = float(mockup_zoom_intensity_raw)
    except Exception:
        mockup_zoom_intensity = 1.1
    mockup_zoom_intensity = max(1.0, min(1.2, mockup_zoom_intensity))

    mockup_zoom_duration_raw = payload.get("mockup_zoom_duration", 2.0)
    try:
        mockup_zoom_duration = float(mockup_zoom_duration_raw)
    except Exception:
        mockup_zoom_duration = 2.0
    mockup_zoom_duration = max(0.0, min(8.0, min(float(duration), mockup_zoom_duration)))

    mockup_pan_raw = payload.get("mockup_pan_enabled", False)
    if isinstance(mockup_pan_raw, bool):
        mockup_pan_enabled = mockup_pan_raw
    elif isinstance(mockup_pan_raw, str):
        mockup_pan_enabled = mockup_pan_raw.strip().lower() in {"1", "true", "yes", "on"}
    else:
        mockup_pan_enabled = bool(mockup_pan_raw)

    mockup_pan_direction = str(payload.get("mockup_pan_direction", "up") or "up").strip().lower()
    if mockup_pan_direction not in {"up", "down", "left", "right"}:
        mockup_pan_direction = "up"

    mockup_auto_alternate_raw = payload.get("mockup_pan_auto_alternate", False)
    if isinstance(mockup_auto_alternate_raw, bool):
        mockup_auto_alternate = mockup_auto_alternate_raw
    elif isinstance(mockup_auto_alternate_raw, str):
        mockup_auto_alternate = mockup_auto_alternate_raw.strip().lower() in {"1", "true", "yes", "on"}
    else:
        mockup_auto_alternate = bool(mockup_auto_alternate_raw)

    # Selected mockups
    selected_raw = payload.get("selected_mockups")
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

    order_raw = payload.get("video_mockup_order")
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

    fps_raw = payload.get("video_fps", 24)
    try:
        video_fps = int(float(fps_raw))
    except Exception:
        video_fps = 24
    if video_fps not in {24, 30, 60}:
        video_fps = 24

    output_raw = payload.get("video_output_size", 1024)
    try:
        video_output_size = int(float(output_raw))
    except Exception:
        video_output_size = 1024
    if video_output_size not in {1024, 1536, 1920, 2560, 3840}:
        video_output_size = 1024

    preset_raw = str(payload.get("video_encoder_preset", "fast") or "fast").strip().lower()
    if preset_raw not in {"fast", "medium", "slow"}:
        preset_raw = "fast"

    source_raw = str(payload.get("video_artwork_source", "auto") or "auto").strip().lower()
    if source_raw not in {"auto", "closeup_proxy", "master"}:
        source_raw = "auto"

    video_mockup_shots_raw = payload.get("video_mockup_shots")
    video_mockup_shots = _normalize_mockup_shots(video_mockup_shots_raw)

    # Main artwork timing (default 4.0 seconds)
    main_artwork_seconds_raw = payload.get("main_artwork_seconds", 4.0)
    try:
        main_artwork_seconds = float(main_artwork_seconds_raw)
    except Exception:
        main_artwork_seconds = 4.0
    main_artwork_seconds = max(1.0, min(10.0, main_artwork_seconds))

    # Mockup timings (per-mockup duration locks)
    video_mockup_timings_raw = payload.get("video_mockup_timings")
    video_mockup_timings: dict = {}
    if isinstance(video_mockup_timings_raw, dict):
        for mockup_id, timing in video_mockup_timings_raw.items():
            try:
                timing_val = float(timing)
                timing_val = max(1.0, min(4.0, timing_val))
                if isinstance(mockup_id, str) and mockup_id.strip():
                    video_mockup_timings[mockup_id.strip()] = timing_val
            except Exception:
                continue

    return {
        "video_duration": int(duration),
        "video_zoom_intensity": round(legacy_zoom, 2),
        "video_panning_enabled": bool(artwork_pan_enabled),
        "artwork_zoom_duration": float(artwork_zoom_duration),
        "selected_mockups": selected_mockups,
        "video_mockup_order": video_mockup_order,
        "video_fps": int(video_fps),
        "video_output_size": int(video_output_size),
        "video_encoder_preset": preset_raw,
        "video_artwork_source": source_raw,
        "video_ffmpeg_profile": ffmpeg_profile_raw,
        "video_compositor": compositor_raw,
        "video_timing_mode": timing_mode_raw,
        "video_motion_profile": motion_profile_raw,
        "artwork_zoom_intensity": round(artwork_zoom_intensity, 2),
        "artwork_pan_enabled": bool(artwork_pan_enabled),
        "artwork_pan_direction": artwork_pan_direction,
        "mockup_zoom_intensity": round(mockup_zoom_intensity, 2),
        "mockup_zoom_duration": float(mockup_zoom_duration),
        "mockup_pan_enabled": bool(mockup_pan_enabled),
        "mockup_pan_direction": mockup_pan_direction,
        "mockup_pan_auto_alternate": bool(mockup_auto_alternate),
        "video_mockup_shots": video_mockup_shots,
        "main_artwork_seconds": round(main_artwork_seconds, 2),
        "video_mockup_timings": video_mockup_timings,
    }


def _storyboard_category_options() -> list[str]:
    bases_root = app_config.BASE_DIR / "application" / "mockups" / "catalog" / "assets" / "mockups" / "bases"
    if not bases_root.exists() or not bases_root.is_dir():
        return []
    categories: set[str] = set()
    try:
        for aspect_dir in bases_root.iterdir():
            if not aspect_dir.is_dir():
                continue
            for category_dir in aspect_dir.iterdir():
                if category_dir.is_dir():
                    categories.add(category_dir.name)
    except Exception:
        return []
    return sorted(categories)


def _storyboard_entries(slug: str, processed_dir: Path, selected_mockups: list[str]) -> list[dict]:
    mockups_dir = processed_dir / "mockups"
    if not mockups_dir.exists() or not mockups_dir.is_dir():
        return []

    assets_path = processed_dir / f"{slug}-assets.json"
    assets_map: dict[str, dict] = {}
    if assets_path.exists() and assets_path.is_file():
        assets_doc = _read_json_silent(assets_path)
        mockups_doc = assets_doc.get("mockups") if isinstance(assets_doc, dict) else {}
        maybe_assets = mockups_doc.get("assets") if isinstance(mockups_doc, dict) else {}
        if isinstance(maybe_assets, dict):
            assets_map = {str(k): v for k, v in maybe_assets.items() if isinstance(v, dict)}

    selected_set = set(selected_mockups)
    entries: list[dict] = []
    for comp_path in sorted(mockups_dir.glob(f"mu-{slug}-*.jpg")):
        if not comp_path.is_file() or "-THUMB" in comp_path.name.upper():
            continue
        match = SLOT_RE.match(comp_path.name)
        if not match:
            continue
        slot = int(match.group("slot"))
        slot_key = f"{slot:02d}"
        slot_meta = assets_map.get(slot_key, {})

        entries.append(
            {
                "slot": slot,
                "slot_key": slot_key,
                "mockup_id": comp_path.stem,
                "filename": comp_path.name,
                "selected": comp_path.name in selected_set,
                "category": slot_meta.get("category"),
                "template_slug": slot_meta.get("template_slug"),
                "thumb_url": url_for("mockups.mockup_thumb", slug=slug, slot=slot),
                "composite_url": url_for("mockups.mockup_composite", slug=slug, slot=slot),
                "swap_url": url_for("mockups.swap_mockup", slug=slug, slot=slot),
                "category_url": url_for("mockups.update_mockup_category", slug=slug, slot=slot),
            }
        )

    return entries


def _flatten_nested_suite(suite: dict) -> dict:
    """Flatten nested video_suite structure for normalization.
    
    Converts from nested structure:
    {
      "artwork": {"zoom_intensity": ..., "pan_enabled": ...},
      "mockups": {"zoom_intensity": ..., "pan_enabled": ...},
      "output": {"fps": ..., "size": ...},
      ...
    }
    
    To flat structure expected by _normalize_video_settings:
    {
      "artwork_zoom_intensity": ...,
      "artwork_pan_enabled": ...,
      "mockup_zoom_intensity": ...,
      "mockup_pan_enabled": ...,
      "video_fps": ...,
      "video_output_size": ...,
      ...
    }
    """
    flat = {}
    
    # Copy top-level keys
    for key in [
        "duration_seconds",
        "video_duration",
        "main_artwork_seconds",
        "video_mockup_order",
        "video_mockup_shots",
        "video_mockup_timings",
        "selected_mockups",
        "video_ffmpeg_profile",
        "video_compositor",
        "video_timing_mode",
        "video_motion_profile",
    ]:
        if key in suite:
            if key == "duration_seconds":
                flat["video_duration"] = suite[key]
            else:
                flat[key] = suite[key]
    
    # Flatten artwork settings
    artwork = suite.get("artwork", {})
    if isinstance(artwork, dict):
        if "zoom_intensity" in artwork:
            flat["artwork_zoom_intensity"] = artwork["zoom_intensity"]
        if "zoom_duration" in artwork:
            flat["artwork_zoom_duration"] = artwork["zoom_duration"]
        if "pan_enabled" in artwork:
            flat["artwork_pan_enabled"] = artwork["pan_enabled"]
        if "pan_direction" in artwork:
            flat["artwork_pan_direction"] = artwork["pan_direction"]
    
    # Flatten mockups settings
    mockups = suite.get("mockups", {})
    if isinstance(mockups, dict):
        if "zoom_intensity" in mockups:
            flat["mockup_zoom_intensity"] = mockups["zoom_intensity"]
        if "zoom_duration" in mockups:
            flat["mockup_zoom_duration"] = mockups["zoom_duration"]
        if "pan_enabled" in mockups:
            flat["mockup_pan_enabled"] = mockups["pan_enabled"]
        if "pan_direction" in mockups:
            flat["mockup_pan_direction"] = mockups["pan_direction"]
        if "auto_alternate_pan" in mockups:
            flat["mockup_pan_auto_alternate"] = mockups["auto_alternate_pan"]
    
    # Flatten output settings
    output = suite.get("output", {})
    if isinstance(output, dict):
        if "fps" in output:
            flat["video_fps"] = output["fps"]
        if "size" in output:
            flat["video_output_size"] = output["size"]
        if "encoder_preset" in output:
            flat["video_encoder_preset"] = output["encoder_preset"]
        if "artwork_source" in output:
            flat["video_artwork_source"] = output["artwork_source"]
        if "ffmpeg_profile" in output:
            flat["video_ffmpeg_profile"] = output["ffmpeg_profile"]
        if "compositor" in output:
            flat["video_compositor"] = output["compositor"]
        if "timing_mode" in output:
            flat["video_timing_mode"] = output["timing_mode"]
        if "motion_profile" in output:
            flat["video_motion_profile"] = output["motion_profile"]

    render = suite.get("render", {})
    if isinstance(render, dict):
        if "compositor" in render:
            flat["video_compositor"] = render["compositor"]
        if "timing_mode" in render:
            flat["video_timing_mode"] = render["timing_mode"]
        if "motion_profile" in render:
            flat["video_motion_profile"] = render["motion_profile"]

    return flat


@video_workspace_bp.get("/artwork/<slug>/video-workspace")
@login_required
def video_workspace(slug: str):
    slug_clean = str(slug or "").strip()
    if not slug_clean or not slug_sku.is_safe_slug(slug_clean):
        abort(404)

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug_clean
    if not processed_dir.exists() or not processed_dir.is_dir():
        abort(404)

    # Get SKU from metadata to construct filenames
    sku = slug_clean
    meta_path = processed_dir / f"{slug_clean.lower()}-metadata.json"
    if not meta_path.exists():
        meta_path = processed_dir / "metadata.json"
    else:
        # Use the SKU-prefixed version
        metadata = _read_json_silent(meta_path)
        if isinstance(metadata, dict):
            sku = str(metadata.get("sku") or metadata.get("artwork_id") or sku).strip() or sku
    
    # Load metadata and artwork data with SKU-prefixed filenames
    metadata = _read_json_silent(processed_dir / f"{sku.lower()}-metadata.json") or _read_json_silent(processed_dir / "metadata.json")
    artwork_data = _read_json_silent(processed_dir / "artwork_data.json")
    
    # Prefer video_suite if it exists, else fall back to legacy top-level keys
    video_suite = artwork_data.get("video_suite", {})
    if isinstance(video_suite, dict) and video_suite:
        # Flatten nested structure for normalization
        flat_settings = _flatten_nested_suite(video_suite)
        video_settings = _normalize_video_settings(flat_settings)
    else:
        video_settings = _normalize_video_settings(artwork_data)
    
    storyboard_entries = _storyboard_entries(slug_clean, processed_dir, list(video_settings.get("selected_mockups") or []))
    storyboard_categories = _storyboard_category_options()

    svc = VideoService(processed_root=Path(cfg["LAB_PROCESSED_DIR"]), logs_dir=_logs_dir(cfg))
    video_path = svc._get_video_output_path(slug_clean)
    has_video = video_path.exists() and video_path.is_file() and video_path.stat().st_size > 0

    auto_mockup_ids: list[str] = []
    try:
        auto_paths = svc._get_ordered_mockup_paths(slug_clean, max_count=MAX_MOCKUP_SLIDES)
        auto_mockup_ids = [path.stem for path in auto_paths]
    except Exception:
        auto_mockup_ids = []

    mockup_01_path = processed_dir / "mockups" / f"mu-{slug_clean}-01.jpg"
    placeholder_url = url_for("mockups.mockup_composite", slug=slug_clean, slot=1) if mockup_01_path.exists() else None

    # Determine the correct review page based on analysis source
    review_target = _resolve_review_target(slug_clean)
    if review_target == "artwork.review_openai":
        review_url = url_for("artwork.review_openai", slug=slug_clean)
    elif review_target == "artwork.review_gemini":
        review_url = url_for("artwork.review_gemini", slug=slug_clean)
    else:
        review_url = url_for("artwork.review", slug=slug_clean)

    return render_template(
        "video_workspace.html",
        slug=slug_clean,
        sku=str(metadata.get("sku") or metadata.get("artwork_id") or slug_clean),
        video_settings=video_settings,
        has_video=has_video,
        video_url=url_for("artwork.video_view", slug=slug_clean) if has_video else None,
        placeholder_url=placeholder_url,
        status_url=url_for("artwork.video_status", slug=slug_clean),
        generate_url=url_for("artwork.video_generate", slug=slug_clean),
        delete_url=url_for("artwork.video_delete", slug=slug_clean),
        settings_url=url_for("artwork.video_settings_save", slug=slug_clean),
        review_url=review_url,
        storyboard_entries=storyboard_entries,
        storyboard_categories=storyboard_categories,
        auto_mockup_ids=auto_mockup_ids,
    )


@video_bp.route("/generate/<slug>", methods=["POST"])
@login_required
def generate_kinematic_video(slug: str):
    """Generate a kinematic preview video for an artwork.

    POST /api/video/generate/<slug>

    Returns:
        JSON response with success status and video URL
    """
    # Validate CSRF token
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    try:
        # Initialize video service
        config = AppConfig()
        video_service = VideoService(
            processed_root=config.LAB_PROCESSED_DIR,
            logs_dir=Path(app_config.LOGS_DIR),
        )

        # Generate video
        logger.info("Generating kinematic video for %s", slug)
        success = video_service.generate_kinematic_video(slug)

        if success:
            video_url = video_service.get_video_url(slug)
            return jsonify({
                "success": True,
                "message": f"Kinematic video generated for {slug}",
                "video_url": video_url,
            })
        else:
            return jsonify({
                "success": False,
                "error": "Video generation failed. Check logs for details.",
            }), 500

    except Exception as e:
        logger.exception("Error generating kinematic video for %s: %s", slug, e)
        return jsonify({
            "success": False,
            "error": f"Video generation error: {str(e)}",
        }), 500


@video_bp.route("/status/<slug>", methods=["GET"])
@login_required
def video_status(slug: str):
    """Check if a kinematic video exists for an artwork.

    GET /api/video/status/<slug>

    Returns:
        JSON response with video availability status
    """
    try:
        config = AppConfig()
        video_service = VideoService(
            processed_root=config.LAB_PROCESSED_DIR,
            logs_dir=Path(app_config.LOGS_DIR),
        )

        has_video = video_service.has_kinematic_video(slug)
        video_url = video_service.get_video_url(slug) if has_video else None

        return jsonify({
            "success": True,
            "has_video": has_video,
            "video_url": video_url,
        })

    except Exception as e:
        logger.exception("Error checking video status for %s: %s", slug, e)
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500
