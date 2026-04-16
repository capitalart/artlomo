import io
import json
import shutil
import threading
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Blueprint, abort, current_app, flash, jsonify, redirect, render_template, request, send_file, session, url_for
from PIL import Image

from application.artwork.errors import ArtworkProcessingError, IndexValidationError, RequiredAssetMissingError
from application.artwork.services.processing_service import ProcessingService
from application.artwork.services.admin_export_service import AdminExportService, AdminExportError
from application import config as app_config
from application.utils.artwork_db import sync_artwork_to_db, update_artwork_status, delete_artwork_from_db
from application.utils.logger_utils import log_security_event
from application.common.utilities import slug_sku


artwork_bp = Blueprint(
    "artwork",
    __name__,
    template_folder="../ui/templates",
)

ARTWORK_DATA_NAME = "artwork_data.json"
VIDEO_ZOOM_DEFAULT = 1.1
VIDEO_PANNING_DEFAULT = True
VIDEO_DURATION_DEFAULT = 15
ARTWORK_ZOOM_DURATION_DEFAULT = 3.0


def _logs_dir() -> Path:
    configured = current_app.config.get("LOGS_DIR")
    if configured:
        return Path(configured)
    return Path(app_config.LOGS_DIR)


def _processing_service() -> ProcessingService:
    cfg = current_app.config
    return ProcessingService(
        unprocessed_root=Path(cfg["LAB_UNPROCESSED_DIR"]),
        processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
        artworks_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
    )


def _read_json_silent(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        return doc if isinstance(doc, dict) else {}
    except Exception:
        return {}


def _read_assets_index(slug: str, processed_dir: Path) -> dict:
    """Read assets.json as source of truth for file references."""
    # Try SKU-prefixed assets first by scanning directory
    sku = slug
    meta_path = processed_dir / f"{slug.lower()}-metadata.json"
    if not meta_path.exists():
        meta_path = processed_dir / "metadata.json"
    if meta_path.exists():
        try:
            meta_doc = json.loads(meta_path.read_text(encoding="utf-8"))
            sku = str(meta_doc.get("sku") or slug).strip().lower()
        except Exception:
            pass
    
    # Try SKU-prefixed assets.json first
    assets_path = processed_dir / f"{sku}-assets.json"
    if not assets_path.exists():
        assets_path = processed_dir / "assets.json"
    
    return _read_json_silent(assets_path)


def _resolve_sku_from_artwork_dir(artwork_dir: Path, slug_hint: str | None = None) -> str:
    """Resolve SKU from metadata/assets with SKU-prefixed fallback support."""
    slug_text = str(slug_hint or artwork_dir.name or "").strip()

    # 1) Prefer metadata documents
    metadata_candidates = sorted(artwork_dir.glob("*-metadata.json"))
    metadata_candidates.append(artwork_dir / "metadata.json")
    for path in metadata_candidates:
        doc = _read_json_silent(path)
        sku = str(doc.get("sku") or doc.get("artwork_id") or "").strip()
        if sku:
            return sku

    # 2) Fall back to assets manifest
    assets_candidates = sorted(artwork_dir.glob("*-assets.json"))
    assets_candidates.append(artwork_dir / "assets.json")
    for path in assets_candidates:
        doc = _read_json_silent(path)
        sku = str(doc.get("sku") or "").strip()
        if sku:
            return sku

    # 3) Best-effort fallback from slug
    return slug_text.upper() if slug_text else ""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_artwork_dir(slug: str) -> Path | None:
    """Resolve artwork directory, checking processed then locked folders."""
    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if processed_dir.exists() and processed_dir.is_dir():
        return processed_dir
    locked_dir = Path(cfg["LAB_LOCKED_DIR"]) / slug
    if locked_dir.exists() and locked_dir.is_dir():
        return locked_dir
    return None


def _normalize_video_settings(raw: dict[str, Any] | None) -> dict[str, Any]:
    payload = raw if isinstance(raw, dict) else {}

    zoom_raw = payload.get("video_zoom_intensity", VIDEO_ZOOM_DEFAULT)
    try:
        zoom = float(zoom_raw)
    except Exception:
        zoom = VIDEO_ZOOM_DEFAULT
    zoom = max(1.0, min(1.3, zoom))

    artwork_zoom_intensity_raw = payload.get("artwork_zoom_intensity", zoom)
    try:
        artwork_zoom_intensity = float(artwork_zoom_intensity_raw)
    except Exception:
        artwork_zoom_intensity = zoom
    artwork_zoom_intensity = max(1.0, min(2.25, artwork_zoom_intensity))

    duration_raw = payload.get("video_duration", VIDEO_DURATION_DEFAULT)
    try:
        duration = int(float(duration_raw))
    except Exception:
        duration = VIDEO_DURATION_DEFAULT
    if duration not in (10, 15, 20):
        duration = VIDEO_DURATION_DEFAULT

    artwork_zoom_raw = payload.get("artwork_zoom_duration", ARTWORK_ZOOM_DURATION_DEFAULT)
    try:
        artwork_zoom_duration = float(artwork_zoom_raw)
    except Exception:
        artwork_zoom_duration = ARTWORK_ZOOM_DURATION_DEFAULT
    artwork_zoom_duration = max(0.0, min(float(duration), float(artwork_zoom_duration)))

    panning_raw = payload.get("artwork_pan_enabled", payload.get("video_panning_enabled", VIDEO_PANNING_DEFAULT))
    if isinstance(panning_raw, bool):
        artwork_pan_enabled = panning_raw
    elif isinstance(panning_raw, str):
        artwork_pan_enabled = panning_raw.strip().lower() in {"1", "true", "yes", "on"}
    else:
        artwork_pan_enabled = bool(panning_raw)

    artwork_pan_direction = str(payload.get("artwork_pan_direction", "up") or "up").strip().lower()
    if artwork_pan_direction not in {"center", "top-left", "top-right", "bottom-right", "bottom-left", "up", "down", "left", "right"}:
        artwork_pan_direction = "up"

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
    mockup_zoom_duration = max(0.0, min(float(duration), float(mockup_zoom_duration)))

    mockup_pan_raw = payload.get("mockup_pan_enabled", False)
    if isinstance(mockup_pan_raw, bool):
        mockup_pan_enabled = mockup_pan_raw
    elif isinstance(mockup_pan_raw, str):
        mockup_pan_enabled = mockup_pan_raw.strip().lower() in {"1", "true", "yes", "on"}
    else:
        mockup_pan_enabled = bool(mockup_pan_raw)

    mockup_pan_direction = str(payload.get("mockup_pan_direction", "up") or "up").strip().lower()
    if mockup_pan_direction not in {"center", "top-left", "top-right", "bottom-right", "bottom-left", "up", "down", "left", "right"}:
        mockup_pan_direction = "up"

    mockup_auto_raw = payload.get("mockup_pan_auto_alternate", False)
    if isinstance(mockup_auto_raw, bool):
        mockup_pan_auto_alternate = mockup_auto_raw
    elif isinstance(mockup_auto_raw, str):
        mockup_pan_auto_alternate = mockup_auto_raw.strip().lower() in {"1", "true", "yes", "on"}
    else:
        mockup_pan_auto_alternate = bool(mockup_auto_raw)

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
    # Stable de-duplication while preserving incoming order.
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

    # Normalize per-mockup timings
    main_artwork_seconds_raw = payload.get("main_artwork_seconds", 4.0)
    try:
        main_artwork_seconds = float(main_artwork_seconds_raw)
    except Exception:
        main_artwork_seconds = 4.0
    main_artwork_seconds = max(1.0, min(10.0, main_artwork_seconds))
    # Round to 0.5 steps
    main_artwork_seconds = round(main_artwork_seconds * 2) / 2

    # Normalize per-mockup timings dict
    video_mockup_timings_raw = payload.get("video_mockup_timings")
    video_mockup_timings: dict[str, float] = {}
    if isinstance(video_mockup_timings_raw, dict):
        for mockup_id, duration in video_mockup_timings_raw.items():
            try:
                mockup_id_clean = str(mockup_id or "").strip()
                if not mockup_id_clean or len(mockup_id_clean) > 100:
                    continue
                duration_val = float(duration)
                # Clamp 1.0 to 4.0
                duration_val = max(1.0, min(4.0, duration_val))
                # Round to 0.5 steps
                duration_val = round(duration_val * 2) / 2
                video_mockup_timings[mockup_id_clean] = duration_val
            except Exception:
                continue
        # Limit to 100 entries
        if len(video_mockup_timings) > 100:
            video_mockup_timings = dict(list(video_mockup_timings.items())[:100])

    # Return nested structure per VIDEO_SUITE_SETTINGS_CONTRACT
    return {
        "duration_seconds": int(duration),
        "main_artwork_seconds": float(main_artwork_seconds),
        "artwork": {
            "zoom_intensity": round(artwork_zoom_intensity, 2),
            "zoom_duration": float(artwork_zoom_duration),
            "pan_enabled": bool(artwork_pan_enabled),
            "pan_direction": str(artwork_pan_direction),
        },
        "mockups": {
            "zoom_intensity": round(mockup_zoom_intensity, 2),
            "zoom_duration": float(mockup_zoom_duration),
            "pan_enabled": bool(mockup_pan_enabled),
            "pan_direction": str(mockup_pan_direction),
            "auto_alternate_pan": bool(mockup_pan_auto_alternate),
        },
        "output": {
            "fps": int(video_fps),
            "size": int(video_output_size),
            "encoder_preset": preset_raw,
            "artwork_source": source_raw,
        },
        "video_mockup_order": video_mockup_order,
        "video_mockup_shots": video_mockup_shots,
        "video_mockup_timings": video_mockup_timings,
        # Keep top-level for backward compatibility
        "selected_mockups": selected_mockups,
    }


def _normalize_mockup_shots(raw: Any) -> list[dict[str, Any]]:
    """Normalize video_mockup_shots array.
    
    Each shot dict must have "id" and may have "pan_enabled", "pan_direction",
    "zoom_enabled", "pan_to_artwork_center", "auto_target".
    De-dupes by id, clamping length to 50.
    
    Special rule: If direction is "none", force pan_enabled=False.
    Default: If zoom_enabled not provided, defaults to True.
    """
    shots: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    
    if not isinstance(raw, list):
        return shots
    
    for item in raw:
        if not isinstance(item, dict):
            continue
        
        shot_id = str(item.get("id") or "").strip()
        if not shot_id or shot_id in seen_ids:
            continue
        
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
        if pan_direction_raw not in {"none", "aim", "center", "top-left", "top-right", "bottom-right", "bottom-left", "up", "down", "left", "right"}:
            pan_direction_raw = "up"
        
        # Rule: If direction is "none", force pan_enabled to False
        if pan_direction_raw == "none":
            pan_enabled = False
        
        # Handle zoom_enabled (defaults to True if missing)
        zoom_enabled_raw = item.get("zoom_enabled", True)
        if isinstance(zoom_enabled_raw, bool):
            zoom_enabled = zoom_enabled_raw
        elif isinstance(zoom_enabled_raw, str):
            zoom_enabled = zoom_enabled_raw.strip().lower() in {"1", "true", "yes", "on"}
        else:
            zoom_enabled = bool(zoom_enabled_raw)
        
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
        
        # Handle zoom_intensity (per-mockup zoom level)
        zoom_intensity_raw = item.get("zoom_intensity", None)
        zoom_intensity = None
        if zoom_intensity_raw is not None:
            try:
                zoom_intensity = float(zoom_intensity_raw)
                # Clamp to valid range 1.0-2.25
                zoom_intensity = max(1.0, min(2.25, zoom_intensity))
            except (ValueError, TypeError):
                zoom_intensity = None
        
        shot = {
            "id": shot_id,
            "pan_enabled": bool(pan_enabled),
            "pan_direction": pan_direction_raw,
            "zoom_enabled": bool(zoom_enabled),
            "pan_to_artwork_center": bool(pan_to_artwork_center),
            "auto_target": bool(pan_to_artwork_center),
        }
        
        # Only include zoom_intensity if it was explicitly set
        if zoom_intensity is not None:
            shot["zoom_intensity"] = zoom_intensity
        
        shots.append(shot)
        seen_ids.add(shot_id)
        
        if len(shots) >= 50:
            break
    
    return shots


def _read_artwork_data(processed_dir: Path) -> dict[str, Any]:
    return _read_json_silent(processed_dir / ARTWORK_DATA_NAME)


def _write_artwork_data(processed_dir: Path, patch: dict[str, Any]) -> dict[str, Any]:
    from application.common.utilities.files import write_json_atomic

    current = _read_artwork_data(processed_dir)
    merged = dict(current) if isinstance(current, dict) else {}
    
    # If patch contains video_suite key, deep merge it; otherwise update top level
    if "video_suite" in patch and isinstance(patch["video_suite"], dict):
        video_suite_patch = patch["video_suite"]
        existing_suite = merged.get("video_suite", {})
        if not isinstance(existing_suite, dict):
            existing_suite = {}
        merged_suite = dict(existing_suite)
        merged_suite.update(video_suite_patch)
        merged["video_suite"] = merged_suite
        # Apply remaining patch keys (excluding video_suite)
        for k, v in patch.items():
            if k != "video_suite":
                merged[k] = v
    else:
        # No video_suite in patch, standard update
        merged.update(patch)
    
    merged["updated_at"] = _now_iso()
    if "created_at" not in merged:
        merged["created_at"] = merged["updated_at"]
    write_json_atomic(processed_dir / ARTWORK_DATA_NAME, merged)
    return merged


def _promote_to_processed(slug: str) -> None:
    cfg = current_app.config
    locked_root = Path(cfg["LAB_LOCKED_DIR"])
    if (locked_root / slug).exists():
        raise ArtworkProcessingError("Artwork is locked and cannot be re-analysed.")
    processed_root = Path(cfg["LAB_PROCESSED_DIR"])
    if (processed_root / slug).exists():
        return
    svc = _processing_service()
    try:
        svc.process(slug)
    except IndexValidationError:
        # Already processed or invalid; let reanalysis continue without duplication
        return
    except RequiredAssetMissingError as exc:
        raise
    except ArtworkProcessingError as exc:
        raise


def _render_analysis(slug: str, analysis_source: str, provider: str | None = None):
    from application.mockups.routes.mockup_routes import (
        build_mockup_preflight_for_slug,
        list_mockup_entries_for_slug,
    )
    from collections import Counter

    from application.mockups.catalog.loader import load_physical_bases

    cfg = current_app.config
    artwork_dir = _resolve_artwork_dir(slug)
    if not artwork_dir:
        flash("Artwork not found.", "warning")
        return redirect(url_for("upload.processed"))
    processed_dir = artwork_dir
    sku = slug
    # Try SKU-prefixed metadata first, then fall back
    meta_path = processed_dir / f"{slug.lower()}-metadata.json"
    if not meta_path.exists():
        meta_path = processed_dir / "metadata.json"
    if meta_path.exists():
        try:
            meta_doc = json.loads(meta_path.read_text(encoding="utf-8"))
            if isinstance(meta_doc, dict):
                sku = str(meta_doc.get("sku") or meta_doc.get("artwork_id") or sku).strip() or sku
        except Exception:
            sku = slug

    # Load all metadata files with SKU prefix fallback
    listing_doc = _read_json_silent(processed_dir / f"{sku.lower()}-listing.json") or _read_json_silent(processed_dir / "listing.json")
    qc_doc = _read_json_silent(processed_dir / f"{sku.lower()}-qc.json") or _read_json_silent(processed_dir / "qc.json")
    provider_key = str(provider or "").strip().lower()
    if provider_key not in {"openai", "gemini"}:
        provider_key = "openai" if str(analysis_source).strip().lower() == "openai" else "gemini"

    provider_doc = _read_json_silent(processed_dir / f"{sku.lower()}-metadata_{provider_key}.json") or _read_json_silent(
        processed_dir / f"metadata_{provider_key}.json"
    )
    if not provider_doc:
        # Backward-compatible fallback for mixed or migrated records.
        provider_doc = _read_json_silent(processed_dir / f"{sku.lower()}-metadata_openai.json") or _read_json_silent(
            processed_dir / "metadata_openai.json"
        ) or _read_json_silent(processed_dir / f"{sku.lower()}-metadata_gemini.json") or _read_json_silent(
            processed_dir / "metadata_gemini.json"
        )
    analysis_doc = provider_doc.get("analysis") if isinstance(provider_doc.get("analysis"), dict) else {}
    seed_context = _read_json_silent(processed_dir / "seed_context.json")
    artwork_data = _read_artwork_data(processed_dir)
    video_settings = _normalize_video_settings(artwork_data)

    # Read from assets.json as source of truth for file references
    assets_index = _read_assets_index(slug, processed_dir)
    files = assets_index.get("files") or {}

    copy_etsy_doc: dict[str, Any] = {}
    copy_etsy_name = files.get("copy_etsy")
    if isinstance(copy_etsy_name, str) and copy_etsy_name.strip():
        copy_etsy_doc = _read_json_silent(processed_dir / copy_etsy_name.strip())
    if not copy_etsy_doc:
        copy_etsy_doc = _read_json_silent(processed_dir / f"{slug}-copy-etsy.json")
    
    # Use assets.json filenames, fall back to defaults if not found
    analyse_name = files.get("analyse") or f"{slug}-ANALYSE.jpg"
    thumb_name = files.get("thumb") or f"{slug}-THUMB.jpg"
    analyse_path = processed_dir / analyse_name
    thumb_path = processed_dir / thumb_name
    analyse_url = url_for("artwork.asset", slug=slug, filename=analyse_name) if analyse_path.exists() else None
    thumb_url = url_for("artwork.asset", slug=slug, filename=thumb_name) if thumb_path.exists() else None

    # Normalize source label for the shared workspace template.
    source_label = str(analysis_source or "").strip().lower()
    if source_label == "openai":
        source_label = "OpenAI"
    elif source_label == "gemini":
        source_label = "Gemini"
    else:
        source_label = "Manual"

    try:
        preflight = build_mockup_preflight_for_slug(slug)
    except Exception:
        current_app.logger.exception("Mockup preflight failed for slug=%s", slug)
        preflight = {"aspect": "UNSET", "eligible_templates": 0, "detected": "UNSET", "source": "error"}

    try:
        mockup_entries = list_mockup_entries_for_slug(slug)
    except Exception:
        current_app.logger.exception("Mockup entries failed for slug=%s", slug)
        mockup_entries = []

    aspect = str(preflight.get("aspect") or "").strip() or None
    bases = load_physical_bases(aspect=aspect) if aspect else []
    counts = Counter([b.category for b in bases if getattr(b, "category", None)])
    categories = sorted(counts.keys())
    mockup_category_options = [
        {
            "value": str(cat),
            "label": f"{str(cat).replace('-', ' ').title()} ({int(counts.get(cat) or 0)})",
            "count": int(counts.get(cat) or 0),
        }
        for cat in categories
    ]

    # Detail Closeup integration
    from application.artwork.services.detail_closeup_service import DetailCloseupService
    detail_closeup_svc = DetailCloseupService(processed_root=Path(cfg["LAB_PROCESSED_DIR"]))
    has_detail_closeup = detail_closeup_svc.has_detail_closeup(slug)
    detail_closeup_url = url_for("artwork.detail_closeup_view", slug=slug) if has_detail_closeup else None
    detail_closeup_thumb_url = url_for("artwork.detail_closeup_thumb", slug=slug) if has_detail_closeup else None

    return render_template(
        "analysis_workspace.html",
        analysis_source=source_label,
        slug=slug,
        sku=sku,
        listing=listing_doc,
        qc=qc_doc,
        analysis=analysis_doc,
        copy_etsy=copy_etsy_doc,
        analyse_url=analyse_url,
        thumb_url=thumb_url,
        mockups_preflight=preflight,
        mockup_entries=mockup_entries,
        mockup_category_options=mockup_category_options,
        seed_context=seed_context,
        video_settings=video_settings,
        has_detail_closeup=has_detail_closeup,
        detail_closeup_url=detail_closeup_url,
        detail_closeup_thumb_url=detail_closeup_thumb_url,
    )


@artwork_bp.get("/<slug>/asset/<path:filename>", endpoint="asset")
def asset(slug: str, filename: str):
    artwork_dir = _resolve_artwork_dir(slug)
    if not artwork_dir:
        abort(404)

    safe_name = filename.strip("/")
    
    # Read from assets.json for allowed files (source of truth)
    assets_index = _read_assets_index(slug, artwork_dir)
    files = assets_index.get("files") or {}
    analyse_name = files.get("analyse") or f"{slug}-ANALYSE.jpg"
    thumb_name = files.get("thumb") or f"{slug}-THUMB.jpg"
    allowed = {thumb_name, analyse_name}
    
    if safe_name not in allowed:
        abort(404)

    asset_path = artwork_dir / safe_name
    if not asset_path.exists():
        abort(404)
    return send_file(asset_path, as_attachment=False)


@artwork_bp.route("/<slug>/analysis/openai")
def openai_analysis(slug: str):
    try:
        _promote_to_processed(slug)
    except RequiredAssetMissingError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("upload.unprocessed"))
    except ArtworkProcessingError as exc:
        flash(str(exc), "danger")
        target = "upload.locked" if "locked" in str(exc).lower() else "upload.unprocessed"
        return redirect(url_for(target))
    return _render_analysis(slug, "OpenAI", provider="openai")


@artwork_bp.route("/<slug>/analysis/gemini")
def gemini_analysis(slug: str):
    try:
        _promote_to_processed(slug)
    except RequiredAssetMissingError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("upload.unprocessed"))
    except ArtworkProcessingError as exc:
        flash(str(exc), "danger")
        target = "upload.locked" if "locked" in str(exc).lower() else "upload.unprocessed"
        return redirect(url_for(target))
    return _render_analysis(slug, "Gemini", provider="gemini")


@artwork_bp.route("/<slug>/analysis/manual")
def manual_analysis(slug: str):
    try:
        _promote_to_processed(slug)
    except RequiredAssetMissingError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("upload.unprocessed"))
    except ArtworkProcessingError as exc:
        flash(str(exc), "danger")
        target = "upload.locked" if "locked" in str(exc).lower() else "upload.unprocessed"
        return redirect(url_for(target))
    return _render_analysis(slug, "Manual", provider="openai")


def _resolve_review_target(slug: str) -> str | None:
    artwork_dir = _resolve_artwork_dir(slug)
    if not artwork_dir:
        return None
    processed_dir = artwork_dir

    def exists(name: str) -> bool:
        return (processed_dir / name).exists()

    # Get SKU from metadata first
    sku = slug
    meta_path = processed_dir / f"{slug.lower()}-metadata.json"
    if not meta_path.exists():
        meta_path = processed_dir / "metadata.json"
    if meta_path.exists():
        try:
            meta_doc = json.loads(meta_path.read_text(encoding="utf-8"))
            if isinstance(meta_doc, dict):
                sku = str(meta_doc.get("sku") or meta_doc.get("artwork_id") or sku).strip() or sku
        except Exception:
            pass

    listing_source = None
    listing_path = processed_dir / f"{sku.lower()}-listing.json"
    if not listing_path.exists():
        listing_path = processed_dir / "listing.json"
    if listing_path.exists():
        try:
            listing_doc = json.loads(listing_path.read_text(encoding="utf-8"))
            listing_source = str(listing_doc.get("analysis_source") or "").lower()
        except Exception:
            listing_source = None

    if listing_source == "manual" or exists("metadata_manual.json"):
        return "manual.workspace"
    if listing_source == "openai" and exists("metadata_openai.json"):
        return "artwork.review_openai"
    if listing_source == "gemini" and exists("metadata_gemini.json"):
        return "artwork.review_gemini"
    if exists("metadata_manual.json"):
        return "manual.workspace"
    if exists("metadata_openai.json"):
        return "artwork.review_openai"
    if exists("metadata_gemini.json"):
        return "artwork.review_gemini"
    if exists("metadata.json"):
        return "artwork.review_openai"
    return None


@artwork_bp.route("/<slug>/review")
def review(slug: str):
    target = _resolve_review_target(slug)
    if target:
        return redirect(url_for(target, slug=slug))
    flash("Processed artwork missing analysis metadata.", "warning")
    return redirect(url_for("upload.processed"))


@artwork_bp.route("/<slug>/review/openai")
def review_openai(slug: str):
    artwork_dir = _resolve_artwork_dir(slug)
    if not artwork_dir:
        flash("Artwork not found.", "warning")
        return redirect(url_for("upload.processed"))
    return _render_analysis(slug, "OpenAI", provider="openai")


@artwork_bp.route("/<slug>/review/gemini")
def review_gemini(slug: str):
    artwork_dir = _resolve_artwork_dir(slug)
    if not artwork_dir:
        flash("Artwork not found.", "warning")
        return redirect(url_for("upload.processed"))
    return _render_analysis(slug, "Gemini", provider="gemini")


@artwork_bp.route("/<slug>/assets", methods=["GET"])  # type: ignore[misc]
def get_asset_manifest(slug: str):
    """Serve the asset manifest (SKU-assets.json) for an artwork.
    
    This is the single source of truth for all asset paths and metadata.
    All file access should be routed through this manifest.
    
    Returns: JSON with complete asset manifest including:
      - Artwork metadata (sku, slug, version)
      - File paths for all image assets (master, thumb, analyse, etc.)
      - Metadata file paths (metadata.json, qc.json, etc.)
      - Mockup slot entries with paths and metadata
    """
    from application.common.utilities import slug_sku
    from application.mockups.artwork_index import resolve_artwork
    from application.mockups.assets_index import AssetsIndex
    
    if not slug_sku.is_safe_slug(slug):
        abort(404)
    
    try:
        cfg = current_app.config
        artwork_dir, assets_path, sku = resolve_artwork(
            _resolve_sku_for_slug(Path(cfg["LAB_PROCESSED_DIR"]) / slug),
            master_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
            processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
        )
        
        assets_index = AssetsIndex(artwork_dir, assets_path)
        assets_doc = assets_index.load()
        
        return jsonify(assets_doc)
    except Exception as exc:
        current_app.logger.exception("artwork.get_asset_manifest")
        return {"error": f"Failed to load asset manifest: {exc}"}, 500


def _resolve_sku_for_slug(artwork_dir: Path) -> str:
    """Resolve SKU from artwork directory metadata."""
    # Try metadata.json first
    metadata_file = artwork_dir / "metadata.json"
    if metadata_file.exists():
        try:
            data = json.loads(metadata_file.read_text(encoding="utf-8"))
            sku = data.get("sku")
            if isinstance(sku, str) and sku.strip():
                return sku.strip()
        except Exception:
            pass
    
    # Try status.json
    status_file = artwork_dir / "status.json"
    if status_file.exists():
        try:
            data = json.loads(status_file.read_text(encoding="utf-8"))
            sku = data.get("sku")
            if isinstance(sku, str) and sku.strip():
                return sku.strip()
        except Exception:
            pass
    
    # Fallback to directory name as SKU (uppercase slug)
    return artwork_dir.name.upper().replace("-", "_")


@artwork_bp.route("/<slug>/delete")
def delete(slug: str):
    return render_template("delete_confirm.html", slug=slug)


@artwork_bp.post("/<slug>/save")  # type: ignore[misc]
def save(slug: str):
    from application.common.utilities.slug_sku import is_safe_slug
    from application.common.utilities.files import write_json_atomic
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    slug_clean = str(slug or "").strip()
    if not slug_clean or not is_safe_slug(slug_clean):
        abort(404)

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug_clean
    if not processed_dir.exists() or not processed_dir.is_dir():
        return {"status": "error", "message": "Not found"}, 404

    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    description = (payload.get("description") or "").strip()
    tags_raw = (payload.get("tags") or "").strip()
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    materials_raw = (payload.get("materials") or "").strip()
    materials = [m.strip() for m in materials_raw.split(",") if m.strip()]
    colours_raw = (payload.get("colours") or "").strip()
    colours = [c.strip() for c in colours_raw.split(",") if c.strip()]
    primary_colour = colours[0] if colours else ""
    secondary_colour = colours[1] if len(colours) > 1 else ""
    quantity_raw = str(payload.get("quantity") or "").strip()
    price_raw = str(payload.get("price") or "").strip()

    quantity = None
    if quantity_raw:
        try:
            parsed_qty = int(float(quantity_raw))
            if parsed_qty > 0:
                quantity = parsed_qty
        except Exception:
            quantity = None

    price = None
    if price_raw:
        try:
            parsed_price = float(price_raw)
            if parsed_price >= 0:
                price = round(parsed_price, 2)
        except Exception:
            price = None

    incoming_video_settings = {
        "video_zoom_intensity": payload.get("video_zoom_intensity"),
        "video_panning_enabled": payload.get("video_panning_enabled"),
        "video_duration": payload.get("video_duration"),
        "selected_mockups": payload.get("selected_mockups"),
    }
    video_settings_present = any(value is not None for value in incoming_video_settings.values())

    # Extract seed context fields if present in payload
    from application.upload.services.storage_service import SEED_CONTEXT_NAME
    seed_context_patch = {}
    for key in ("location", "sentiment", "original_prompt"):
        val = (payload.get(key) or "").strip()
        if val:
            seed_context_patch[key] = val
    
    if seed_context_patch:
        seed_context_path = processed_dir / SEED_CONTEXT_NAME
        existing_seed = _read_json_silent(seed_context_path)
        updated_seed = {**existing_seed, **seed_context_patch}
        updated_seed["updated_at"] = _now_iso()
        if "created_at" not in updated_seed:
            updated_seed["created_at"] = updated_seed["updated_at"]
        from application.common.utilities.files import write_json_atomic
        write_json_atomic(seed_context_path, updated_seed)

    # Visual Analysis fields (atomic merge — only overwrite keys that are present)
    va_incoming = payload.get("visual_analysis")
    va_patch = {}
    if isinstance(va_incoming, dict):
        for key in ("subject", "dot_rhythm", "palette", "mood"):
            val = (va_incoming.get(key) or "").strip()
            if val:
                va_patch[key] = val

    # Get SKU first so we can use it for filenames
    meta = _read_json_silent(processed_dir / "metadata.json")
    sku = str(meta.get("sku") or meta.get("artwork_id") or slug_clean).strip() or slug_clean
    
    # Try SKU-prefixed listing first, then fallback
    listing_path = processed_dir / f"{sku.lower()}-listing.json"
    if not listing_path.exists():
        listing_path = processed_dir / "listing.json"
    
    listing = _read_json_silent(listing_path)
    if not isinstance(listing, dict):
        listing = {}

    # Merge visual_analysis atomically: preserve existing keys not in this save
    existing_va = listing.get("visual_analysis") or {}
    if isinstance(existing_va, dict):
        merged_va = {**existing_va, **va_patch}
    else:
        merged_va = va_patch
    if merged_va:
        listing["visual_analysis"] = merged_va

    listing.update(
        {
            "title": title,
            "description": description,
            "tags": tags,
            "materials": materials,
            "primary_colour": primary_colour,
            "secondary_colour": secondary_colour,
            "quantity": quantity,
            "price": price,
            "seo_filename": (payload.get("seo_filename") or payload.get("seo_filename_slug") or "").strip(),
            "updated_at": _now_iso(),
        }
    )
    # Write with SKU prefix
    sku_prefixed_listing_path = processed_dir / f"{sku.lower()}-listing.json"
    write_json_atomic(sku_prefixed_listing_path, listing)

    if video_settings_present:
        normalized = _normalize_video_settings(incoming_video_settings)
        _write_artwork_data(processed_dir, normalized)

    # Double-write: sync to database
    sync_artwork_to_db(
        sku=sku,
        slug=slug_clean,
        title=title or sku,
        owner_id=session.get("username"),
        status="processed",
        analysis_source=listing.get("analysis_source"),
        image_path=meta.get("stored_filename"),
        thumb_path=meta.get("thumb_filename"),
        metadata=listing,
    )

    return {
        "status": "ok",
        "slug": slug_clean,
        "listing": {
            "title": title,
            "description": description,
            "tags": tags,
            "materials": materials,
            "primary_colour": primary_colour,
            "secondary_colour": secondary_colour,
            "quantity": quantity,
            "price": price,
        },
    }


@artwork_bp.post("/<slug>/video/settings")  # type: ignore[misc]
def video_settings_save(slug: str):
    from application.common.utilities.slug_sku import is_safe_slug
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    slug_clean = str(slug or "").strip()
    if not slug_clean or not is_safe_slug(slug_clean):
        return {"status": "error", "message": "Invalid slug"}, 400

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug_clean
    if not processed_dir.exists() or not processed_dir.is_dir():
        return {"status": "error", "message": "Artwork not found"}, 404

    payload = request.get_json(silent=True) or {}
    normalized = _normalize_video_settings(payload)
    
    # Write under video_suite key
    _write_artwork_data(processed_dir, {"video_suite": normalized})
    
    # Read back to get persisted values
    artwork_data = _read_artwork_data(processed_dir)
    video_suite = artwork_data.get("video_suite", {})

    return {
        "status": "ok",
        "slug": slug_clean,
        "video_suite": video_suite,
    }


@artwork_bp.post("/<slug>/lock")  # type: ignore[misc]
def lock(slug: str):
    from application.common.utilities.slug_sku import is_safe_slug
    from application.artwork.services.index_service import ArtworksIndex
    from application.upload.services import storage_service
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    slug_clean = str(slug or "").strip()
    if not slug_clean or not is_safe_slug(slug_clean):
        abort(404)

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug_clean
    locked_dir = Path(cfg["LAB_LOCKED_DIR"]) / slug_clean
    if not processed_dir.exists() or not processed_dir.is_dir():
        return {"status": "error", "message": "Not found"}, 404
    if locked_dir.exists():
        return {"status": "error", "message": "Already locked"}, 400

    sku = _resolve_sku_from_artwork_dir(processed_dir, slug_clean) or None

    try:
        processed_dir.replace(locked_dir)
        
        # Rename master to SEO filename if available
        try:
            listing_path = locked_dir / "listing.json"
            if listing_path.exists():
                listing_doc = json.loads(listing_path.read_text(encoding="utf-8"))
                seo_filename = listing_doc.get("seo_filename")
                if seo_filename:
                    master_path = locked_dir / f"{slug_clean}-MASTER.jpg"
                    legacy_path = locked_dir / f"{slug_clean}.jpg"
                    target_path = locked_dir / seo_filename
                    
                    if master_path.exists():
                        master_path.rename(target_path)
                    elif legacy_path.exists():
                        legacy_path.rename(target_path)
        except Exception as e:
            current_app.logger.warning(f"Failed to rename master to SEO filename during lock: {e}")

    except Exception as exc:
        return {"status": "error", "message": str(exc)}, 500

    try:
        index = ArtworksIndex(Path(cfg["ARTWORKS_INDEX_PATH"]), Path(cfg["LAB_PROCESSED_DIR"]))
        sku_text = str(sku or "").strip()
        if sku_text:
            assets_name = f"{slug_clean}-assets.json"
            assets_candidate = locked_dir / assets_name
            if not assets_candidate.exists():
                candidates = sorted(locked_dir.glob("*-assets.json"))
                if candidates:
                    assets_name = candidates[0].name

            index.upsert(
                sku=sku_text,
                slug=slug_clean,
                artwork_dirname=slug_clean,
                assets_file=assets_name,
                stage="locked",
            )
        else:
            index.remove_by_slug(slug_clean)
    except Exception:
        current_app.logger.exception("Failed to sync artworks index after lock slug=%s sku=%s", slug_clean, sku)

    # Double-write: update status in database
    if sku:
        update_artwork_status(str(sku), "locked")

    log_security_event(user_id=session.get("username"), action="lock_processed", details=f"slug={slug_clean} sku={sku or ''}")
    return {"status": "ok", "slug": slug_clean, "sku": sku}


@artwork_bp.post("/<slug>/delete")  # type: ignore[misc]
def delete_post(slug: str):
    from application.common.utilities.slug_sku import is_safe_slug
    from application.artwork.services.index_service import ArtworksIndex
    from application.upload.services import storage_service
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    slug_clean = str(slug or "").strip()
    if not slug_clean or not is_safe_slug(slug_clean):
        abort(404)

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug_clean
    if not processed_dir.exists() or not processed_dir.is_dir():
        return {"status": "error", "message": "Not found"}, 404

    sku = _resolve_sku_from_artwork_dir(processed_dir, slug_clean) or None

    try:
        shutil.rmtree(processed_dir)
    except Exception as exc:
        return {"status": "error", "message": str(exc)}, 500

    try:
        index = ArtworksIndex(Path(cfg["ARTWORKS_INDEX_PATH"]), Path(cfg["LAB_PROCESSED_DIR"]))
        sku_text = str(sku or "").strip()
        if sku_text:
            index.remove_by_sku(sku_text)
        else:
            index.remove_by_slug(slug_clean)
    except Exception:
        current_app.logger.exception("Failed to sync artworks index after delete slug=%s sku=%s", slug_clean, sku)

    # Double-write: remove from database
    if sku:
        delete_artwork_from_db(str(sku))

    log_security_event(user_id=session.get("username"), action="delete_processed", details=f"slug={slug_clean} sku={sku or ''}")
    return {"status": "ok", "slug": slug_clean, "sku": sku}


@artwork_bp.post("/<slug>/regenerate-images")  # type: ignore[misc]
def regenerate_images_post(slug: str):
    from application.common.utilities.slug_sku import is_safe_slug
    from application.artwork.services.image_regeneration_service import ImageRegenerationService
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    slug_clean = str(slug or "").strip()
    if not slug_clean or not is_safe_slug(slug_clean):
        abort(404)

    cfg = current_app.config
    artwork_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug_clean
    if not artwork_dir.exists() or not artwork_dir.is_dir():
        return {"status": "error", "message": "Artwork not found"}, 404

    try:
        regen_svc = ImageRegenerationService(processed_root=Path(cfg["LAB_PROCESSED_DIR"]))
        results = regen_svc.regenerate_all(slug_clean)
        
        # Check if all regenerations succeeded
        all_success = all(r.get("success", False) for r in results.values())
        
        log_security_event(
            user_id=session.get("username"),
            action="regenerate_images",
            details=f"slug={slug_clean} success={all_success}"
        )
        
        return {
            "status": "ok" if all_success else "partial",
            "slug": slug_clean,
            "results": results
        }
    except Exception as exc:
        current_app.logger.exception("Image regeneration failed for slug=%s", slug_clean)
        return {
            "status": "error",
            "message": str(exc)
        }, 500


def _video_generate_worker(app_obj, slug: str) -> None:
    with app_obj.app_context():
        from application.video.services.video_service import VideoService

        cfg = current_app.config
        processed_root = Path(cfg["LAB_PROCESSED_DIR"])
        status_path = processed_root / slug / "video_status.json"

        def _write_video_status(*, status: str, percent: int, stage: str, message: str = "") -> None:
            status_path.write_text(
                json.dumps(
                    {
                        "status": status,
                        "percent": int(max(0, min(100, percent))),
                        "stage": stage,
                        "message": message,
                    },
                    ensure_ascii=True,
                    indent=2,
                ),
                encoding="utf-8",
            )

        try:
            _write_video_status(status="processing", percent=5, stage="initializing", message="Starting render")
            svc = VideoService(processed_root=processed_root, logs_dir=_logs_dir())
            ok = svc.generate_kinematic_video(slug)
            if ok:
                _write_video_status(status="success", percent=100, stage="complete", message="Video generation complete")
            else:
                detail = str(getattr(svc, "last_error", "") or "").strip()
                _write_video_status(
                    status="error",
                    percent=100,
                    stage="error",
                    message=detail or "Video generation failed",
                )
        except Exception as exc:  # pylint: disable=broad-except
            current_app.logger.exception("Video worker failed for slug=%s: %s", slug, exc)
            try:
                _write_video_status(status="error", percent=100, stage="error", message=str(exc))
            except Exception:
                current_app.logger.exception("Failed to persist video error status for slug=%s", slug)

@artwork_bp.post("/<slug>/video/generate")  # type: ignore[misc]
def video_generate(slug: str):
    """Generate 15-second vertical promo video for artwork.

    Saves to lab/processed/<slug>/promo_video.mp4 (Single-State Invariant).
    Returns JSON with status and video_url on success.
    """
    from application.common.utilities.slug_sku import is_safe_slug
    from application.utils.csrf import require_csrf_or_400
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    slug_clean = str(slug or "").strip()
    if not slug_clean or not is_safe_slug(slug_clean):
        return {"status": "error", "message": "Invalid slug"}, 400

    cfg = current_app.config
    processed_root = Path(cfg["LAB_PROCESSED_DIR"])
    artwork_dir = processed_root / slug_clean
    if not artwork_dir.exists() or not artwork_dir.is_dir():
        return {"status": "error", "message": "Artwork not found"}, 404

    payload = request.get_json(silent=True) or {}
    if isinstance(payload, dict) and "selected_mockups" in payload:
        normalized = _normalize_video_settings({"selected_mockups": payload.get("selected_mockups")})
        # Persist selection inside video_suite to match the canonical settings contract.
        _write_artwork_data(
            artwork_dir,
            {
                "video_suite": {
                    "selected_mockups": normalized.get("selected_mockups") or [],
                }
            },
        )

    status_path = artwork_dir / "video_status.json"
    try:
        status_path.write_text(
            json.dumps(
                {
                    "status": "processing",
                    "percent": 0,
                    "stage": "initializing",
                    "message": "Queued",
                },
                ensure_ascii=True,
                indent=2,
            ),
            encoding="utf-8",
        )
    except Exception:
        current_app.logger.exception("Failed to write initial video status for slug=%s", slug_clean)

    # Clear stale ffmpeg frame progress from previous runs before the new worker starts.
    render_status_path = artwork_dir / "video_render_status.json"
    try:
        if render_status_path.exists() and render_status_path.is_file():
            render_status_path.unlink()
    except Exception:
        current_app.logger.exception("Failed to clear stale render status for slug=%s", slug_clean)

    app_obj = current_app._get_current_object()  # type: ignore[attr-defined]
    thread = threading.Thread(target=_video_generate_worker, args=(app_obj, slug_clean), daemon=True)
    thread.start()

    return {
        "status": "ok",
        "message": "Video generation started",
        "video_url": url_for("artwork.video_view", slug=slug_clean),
        "status_url": url_for("artwork.video_status", slug=slug_clean),
    }


@artwork_bp.get("/<slug>/video")
def video_view(slug: str):
    """Serve the generated promo video."""
    from application.video.services.video_service import VideoService

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    video_path = VideoService(processed_root=Path(cfg["LAB_PROCESSED_DIR"]), logs_dir=_logs_dir())._get_video_output_path(slug)

    if not slug_sku.is_safe_slug(str(slug or "").strip()):
        abort(404)
    if not video_path.exists():
        abort(404)

    return send_file(
        video_path,
        mimetype="video/mp4",
        as_attachment=False,
        conditional=False,
        max_age=0,
    )


@artwork_bp.route("/<slug>/video", methods=["DELETE"])  # type: ignore[misc]
def video_delete(slug: str):
    """Delete generated promo video for artwork."""
    from application.common.utilities.slug_sku import is_safe_slug
    from application.utils.csrf import require_csrf_or_400
    from application.video.services.video_service import VideoService

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    slug_clean = str(slug or "").strip()
    if not slug_clean or not is_safe_slug(slug_clean):
        return {"status": "error", "message": "Invalid slug"}, 400

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug_clean
    if not processed_dir.exists() or not processed_dir.is_dir():
        return {"status": "error", "message": "Artwork not found"}, 404

    svc = VideoService(processed_root=Path(cfg["LAB_PROCESSED_DIR"]), logs_dir=_logs_dir())
    video_path = svc._get_video_output_path(slug_clean)
    if not video_path.exists() or not video_path.is_file():
        return {"status": "error", "message": "Video not found"}, 404

    try:
        video_path.unlink()
    except Exception as exc:
        current_app.logger.exception("Failed deleting video for slug=%s: %s", slug_clean, exc)
        return {"status": "error", "message": "Failed to delete video"}, 500

    log_security_event(user_id=session.get("username"), action="delete_video", details=f"slug={slug_clean} file={video_path.name}")
    return {"status": "ok", "slug": slug_clean, "deleted": True}


@artwork_bp.get("/<slug>/video-status")
def video_status(slug: str):
    """Return real-time promo video generation status for artwork."""
    from application.video.services.video_service import VideoService

    if not slug_sku.is_safe_slug(str(slug or "").strip()):
        return {"status": "error", "message": "Invalid slug"}, 404

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if not processed_dir.exists() or not processed_dir.is_dir():
        return {"status": "error", "message": "Artwork not found"}, 404

    status_path = processed_dir / "video_status.json"
    payload = {
        "status": "idle",
        "percent": 0,
        "stage": "idle",
        "message": "No active video job",
    }
    if status_path.exists():
        try:
            raw = json.loads(status_path.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                payload.update(raw)
        except Exception:
            payload = {
                "status": "error",
                "percent": 100,
                "stage": "error",
                "message": "Invalid status payload",
            }

    video_path = VideoService(processed_root=Path(cfg["LAB_PROCESSED_DIR"]), logs_dir=_logs_dir())._get_video_output_path(slug)
    payload["has_video"] = video_path.exists() and video_path.stat().st_size > 0 if video_path.exists() else False
    payload["video_url"] = url_for("artwork.video_view", slug=slug) if payload["has_video"] else None
    payload["slug"] = slug

    render_status_path = processed_dir / "video_render_status.json"
    if render_status_path.exists() and render_status_path.is_file():
        try:
            render_raw = json.loads(render_status_path.read_text(encoding="utf-8"))
            if isinstance(render_raw, dict) and render_raw.get("slug") == slug:
                payload["frames_completed"] = int(render_raw.get("frames_completed") or 0)
                payload["total_frames"] = int(render_raw.get("total_frames") or 0)
                payload["started_at"] = render_raw.get("started_at")
        except Exception:
            current_app.logger.exception("Failed reading render status for slug=%s", slug)
    return payload


@artwork_bp.get("/<slug>/admin-export/<provider>")
def admin_export(slug: str, provider: str):
    """Export analysis bundle for admin iteration"""
    from application.common.utilities.slug_sku import is_safe_slug
    from application.routes.auth_routes import login_required
    
    # Check authentication (user must be logged in as admin)
    if not session.get("is_admin"):
        flash("Admin access required", "danger")
        return redirect(url_for("auth.login", next=request.path))
    
    slug_clean = str(slug or "").strip()
    provider_clean = str(provider or "").strip().lower()
    
    if not slug_clean or not is_safe_slug(slug_clean):
        abort(404)
    
    if provider_clean not in ["openai", "gemini"]:
        abort(400)
    
    cfg = current_app.config
    
    try:
        svc = AdminExportService(
            processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
            artworks_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
        )
        
        bundle_bytes = svc.get_artwork_bundle(slug_clean, provider_clean)
        filename = svc.get_bundle_filename(slug_clean, provider_clean)
        
        # Log the export
        log_security_event(
            user_id=session.get("username"),
            action="admin_export",
            details=f"slug={slug_clean} provider={provider_clean}"
        )
        
        return send_file(
            __import__("io").BytesIO(bundle_bytes),
            mimetype="application/gzip",
            as_attachment=True,
            download_name=filename,
        )
    except AdminExportError as e:
        flash(f"Export failed: {str(e)}", "danger")
        return redirect(url_for("artwork.review", slug=slug_clean))
    except Exception as e:
        current_app.logger.exception(f"Admin export failed for slug={slug_clean} provider={provider_clean}")
        flash("Export failed. Please try again.", "danger")
        return redirect(url_for("artwork.review", slug=slug_clean))


# ============================================================================
# DETAIL CLOSEUP ROUTES
# ============================================================================

@artwork_bp.get("/<slug>/detail-closeup/proxy")
def detail_closeup_proxy(slug: str):
    """Serve proxy preview image for detail closeup editor.

    The proxy is a downsampled version (long edge 7200px) of the master used for fast
    interactive editing in the browser.
    """
    from application.artwork.services.detail_closeup_service import DetailCloseupService

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"])

    svc = DetailCloseupService(processed_root=processed_dir)

    # Generate proxy if it doesn't exist
    if not (processed_dir / slug / f"{slug}-CLOSEUP-PROXY.jpg").exists():
        svc.generate_proxy_preview(slug)

    # Serve the proxy
    proxy_path = processed_dir / slug / f"{slug}-CLOSEUP-PROXY.jpg"
    if not proxy_path.exists():
        abort(404)

    return send_file(proxy_path, mimetype="image/jpeg")


@artwork_bp.get("/<slug>/detail-closeup")
def detail_closeup_view(slug: str):
    """Serve the saved detail closeup image."""
    from application.mockups import config as mockups_config

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug

    detail_name = f"{slug}-detail-closeup.jpg"
    detail_path = (
        processed_dir
        / mockups_config.MOCKUPS_SUBDIR
        / detail_name
    )

    if not detail_path.exists():
        abort(404)

    return send_file(detail_path, mimetype="image/jpeg")


@artwork_bp.get("/<slug>/detail-closeup-thumb")
def detail_closeup_thumb(slug: str):
    """Serve the detail closeup thumbnail (500x500)."""
    from application.mockups import config as mockups_config

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug

    thumb_name = f"{slug}-detail-closeup.jpg"
    thumb_path = (
        processed_dir
        / mockups_config.MOCKUPS_SUBDIR
        / "thumbs"
        / thumb_name
    )

    if not thumb_path.exists():
        # Fallback to full-size if thumb doesn't exist
        detail_path = (
            processed_dir
            / mockups_config.MOCKUPS_SUBDIR
            / thumb_name
        )
        if detail_path.exists():
            return send_file(detail_path, mimetype="image/jpeg")
        abort(404)

    return send_file(thumb_path, mimetype="image/jpeg")


@artwork_bp.get("/<slug>/detail-closeup/editor")
def detail_closeup_editor(slug: str):
    """Render the detail closeup editor UI.

    This page provides an interactive editor with:
    - Proxy image viewport (2000x2000 square)
    - Zoom +/- buttons (10% increments)
    - Drag to pan
    - FREEZE button (preview the crop result)
    - SAVE button (render final crop and register as mockup)
    """
    from application.artwork.services.detail_closeup_service import DetailCloseupService

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"])
    slug_clean = str(slug).strip()
    
    # Get provider from query parameter (openai by default)
    provider = request.args.get("provider", "openai").strip().lower()
    if provider not in ["openai", "gemini"]:
        provider = "openai"

    if not slug_sku.is_safe_slug(slug_clean):
        abort(404)

    svc = DetailCloseupService(processed_root=processed_dir)

    # Ensure proxy exists
    if not (processed_dir / slug_clean / f"{slug_clean}-CLOSEUP-PROXY.jpg").exists():
        if not svc.generate_proxy_preview(slug_clean):
            abort(404)

    proxy_url = url_for("artwork.detail_closeup_proxy", slug=slug_clean)
    has_saved = svc.has_detail_closeup(slug_clean)
    saved_url = url_for("artwork.detail_closeup_view", slug=slug_clean) if has_saved else None

    return render_template(
        "detail_closeup_editor.html",
        slug=slug_clean,
        provider=provider,
        proxy_url=proxy_url,
        saved_url=saved_url,
        has_saved=has_saved,
    )


@artwork_bp.post("/<slug>/detail-closeup/save")  # type: ignore[misc]
def detail_closeup_save(slug: str):
    """Save a detail closeup crop using normalized coordinates."""
    try:
        data = request.get_json()
        
        # Parse normalized coordinates - default to center (0.5, 0.5)
        norm_x = float(data.get('norm_x', 0.5))
        norm_y = float(data.get('norm_y', 0.5))
        scale = float(data.get('scale', 1.0))
        
        current_app.logger.debug(f"DetailCloseup Save - Slug: {slug} | NormX: {norm_x} | NormY: {norm_y} | Scale: {scale}")

        # Initialize Service with config-safe access
        from application.artwork.services.detail_closeup_service import DetailCloseupService
        
        processed_root = current_app.config.get('LAB_PROCESSED_DIR') or current_app.config.get('PROCESSED_ROOT')
        if not processed_root:
            current_app.logger.error("DetailCloseup: Missing LAB_PROCESSED_DIR or PROCESSED_ROOT config")
            return jsonify({'error': 'Server configuration error'}), 500
            
        service = DetailCloseupService(processed_root)
        
        # Render the detail crop
        success = service.render_detail_crop(slug, norm_x, norm_y, scale)
        
        if success:
            # Return timestamp to force browser cache bust
            return jsonify({
                'status': 'success', 
                'url': f'/artwork/{slug}/detail-closeup?t={int(time.time())}'
            })
        
        current_app.logger.warning(f"DetailCloseup: Service returned False for {slug}")
        return jsonify({'error': 'Service returned False'}), 500

    except ValueError as e:
        current_app.logger.error(f"DetailCloseup: Invalid parameter - {str(e)}")
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        current_app.logger.error(f"DetailCloseup: Error saving {slug} - {str(e)}")
        return jsonify({'error': str(e)}), 500


@artwork_bp.post("/<slug>/detail-closeup/freeze")  # type: ignore[misc]
def detail_closeup_freeze(slug: str):
    """Preview what the crop will look like (non-destructive).

    Expected JSON body:
    {
        "scale": 1.5,
        "offset_x": 100,
        "offset_y": 50,
        "viewport_width": 500,     # Viewport width (optional, defaults to 500)
        "viewport_height": 500     # Viewport height (optional, defaults to 500)
    }

    Returns:
    {
        "status": "ok",
        "preview_data": "data:image/jpeg;base64,..."
    }
    """
    from application.artwork.services.detail_closeup_service import DETAIL_CLOSEUP_OUTPUT_SIZE
    from application.utils.csrf import require_csrf_or_400
    import base64
    from io import BytesIO

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"])
    slug_clean = str(slug).strip()

    if not slug_sku.is_safe_slug(slug_clean):
        return {"status": "error", "message": "Invalid slug"}, 400

    body = request.get_json(silent=True) or {}
    try:
        scale = float(body.get("scale", 1.0))
        offset_x = float(body.get("offset_x", 0))
        offset_y = float(body.get("offset_y", 0))
        viewport_width = int(body.get("viewport_width", 500))
        viewport_height = int(body.get("viewport_height", 500))
    except (ValueError, TypeError):
        return {"status": "error", "message": "Invalid parameters"}, 400

    master_path = processed_dir / slug_clean / f"{slug_clean}-MASTER.jpg"
    if not master_path.exists():
        return {"status": "error", "message": "Master image not found"}, 404

    # Get proxy dimensions for accurate scaling
    proxy_path = processed_dir / slug_clean / f"{slug_clean}-CLOSEUP-PROXY.jpg"
    if not proxy_path.exists():
        from application.artwork.services.detail_closeup_service import DetailCloseupService

        service = DetailCloseupService(processed_root=processed_dir)
        if not service.generate_proxy_preview(slug_clean):
            return {"status": "error", "message": "Proxy image not found"}, 404

    try:
        # Get actual proxy dimensions
        with Image.open(proxy_path) as proxy_img:
            proxy_width, proxy_height = proxy_img.size
        
        with Image.open(master_path) as img:
            img = img.convert("RGB")
            master_width, master_height = img.size

            # Use same coordinate mapping as the save function
            # Coordinate chain: Viewport (500px display) -> Proxy (7200px) -> Master (14400px)
            
            # Calculate viewport center accounting for pan offset
            viewport_center_x = (viewport_width / 2.0) - offset_x
            viewport_center_y = (viewport_height / 2.0) - offset_y
            
            # Convert from viewport display space to proxy image space
            viewport_to_proxy_ratio = proxy_width / float(viewport_width)
            
            proxy_center_x = (viewport_center_x / scale) * viewport_to_proxy_ratio
            proxy_center_y = (viewport_center_y / scale) * viewport_to_proxy_ratio
            
            # Convert from proxy space to master space
            proxy_to_master_ratio = master_width / float(proxy_width)
            
            master_center_x = proxy_center_x * proxy_to_master_ratio
            master_center_y = proxy_center_y * proxy_to_master_ratio
            
            # Calculate visible area in each coordinate space
            visible_width_in_viewport = viewport_width / scale
            visible_height_in_viewport = viewport_height / scale
            
            visible_width_in_proxy = visible_width_in_viewport * viewport_to_proxy_ratio
            visible_height_in_proxy = visible_height_in_viewport * viewport_to_proxy_ratio
            
            master_crop_width = visible_width_in_proxy * proxy_to_master_ratio
            master_crop_height = visible_height_in_proxy * proxy_to_master_ratio
            
            # Half sizes for center-based cropping
            half_width = master_crop_width / 2.0
            half_height = master_crop_height / 2.0
            
            # Crop box in master coordinates (centered on view)
            crop_x = int(master_center_x - half_width)
            crop_y = int(master_center_y - half_height)
            crop_x2 = int(master_center_x + half_width)
            crop_y2 = int(master_center_y + half_height)
            
            # Clamp to image bounds
            crop_x = max(0, crop_x)
            crop_y = max(0, crop_y)
            crop_x2 = min(master_width, crop_x2)
            crop_y2 = min(master_height, crop_y2)
            
            # Ensure valid crop region
            if crop_x2 <= crop_x or crop_y2 <= crop_y:
                raise ValueError("Crop region is invalid")

            # Extract and resize with high-quality LANCZOS resampling
            cropped = img.crop((crop_x, crop_y, crop_x2, crop_y2))
            cropped = cropped.resize(DETAIL_CLOSEUP_OUTPUT_SIZE, Image.Resampling.LANCZOS)

            # Convert to base64 for data URL
            img_bytes = BytesIO()
            cropped.save(img_bytes, "JPEG", quality=85)
            img_bytes.seek(0)
            b64_data = base64.b64encode(img_bytes.read()).decode("utf-8")

            return {
                "status": "ok",
                "preview_data": f"data:image/jpeg;base64,{b64_data}",
            }

    except Exception as e:
        current_app.logger.exception("Detail closeup freeze failed for %s: %s", slug_clean, e)
        return {"status": "error", "message": "Failed to generate preview"}, 500


@artwork_bp.post("/<slug>/export")  # type: ignore[misc]
def export_artwork(slug: str):
    """Export all generated artwork assets as ZIP file."""
    from application.utils.csrf import require_csrf_or_400
    from application.upload.services import storage_service
    
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    
    slug_clean = str(slug or "").strip()
    if not slug_clean or not slug_sku.is_safe_slug(slug_clean):
        abort(404)
    
    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug_clean
    if not processed_dir.exists() or not processed_dir.is_dir():
        return {"status": "error", "message": "Artwork not found"}, 404
    
    # Load assets.json to get correct filenames (source of truth)
    assets_manifest = storage_service.load_assets_manifest(processed_dir)
    
    # Build list of specific files to export
    specific_files = []
    
    # Add main artwork images from assets.json
    if assets_manifest and assets_manifest.get("files"):
        files = assets_manifest["files"]
        if files.get("master"):
            specific_files.append(("", files["master"]))
        if files.get("analyse"):
            specific_files.append(("", files["analyse"]))
        if files.get("thumb"):
            specific_files.append(("", files["thumb"]))
        if files.get("closeup_proxy"):
            specific_files.append(("", files["closeup_proxy"]))
    
    # Pattern-based files (mockups, metadata, video)
    pattern_files = [
        # All mockup composites
        ("mockups", "mu-*.jpg"),
        # Mockup thumbs
        ("mockups/thumbs", "*.jpg"),
        # Detail closeup from mockups folder
        ("mockups", "*-detail-closeup.jpg"),
        # Metadata files (try both SKU-prefixed and non-prefixed)
        ("", "artwork_data.json"),
        ("", "coordinates.json"),
        ("", "listing.json"),
        ("", f"{slug_clean}-listing.json"),
        ("", "metadata.json"),
        ("", f"{slug_clean}-metadata.json"),
        ("", "metadata_openai.json"),
        ("", f"{slug_clean}-metadata_openai.json"),
        ("", "processing_status.json"),
        ("", f"{slug_clean}-processing_status.json"),
        ("", "qc.json"),
        ("", f"{slug_clean}-qc.json"),
        # Video file
        ("", "*_NODE_V1.mp4"),
        # Status files
        ("", "status.json"),
        ("", f"{slug_clean}-status.json"),
        ("", "video_status.json"),
        # Assets manifest
        ("", "*-assets.json"),
    ]
    
    try:
        # Create in-memory ZIP
        zip_buffer = io.BytesIO()
        added_files = set()  # Track to avoid duplicates
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add specific files from assets.json
            for subdir, filename in specific_files:
                search_dir = processed_dir / subdir if subdir else processed_dir
                file_path = search_dir / filename
                if file_path.is_file():
                    arcname = f"{slug_clean}/{file_path.relative_to(processed_dir)}"
                    if arcname not in added_files:
                        zf.write(file_path, arcname=arcname)
                        added_files.add(arcname)
            
            # Add pattern-matched files
            for subdir, pattern in pattern_files:
                search_dir = processed_dir / subdir if subdir else processed_dir
                if not search_dir.exists():
                    continue
                
                for file_path in search_dir.glob(pattern):
                    if file_path.is_file():
                        arcname = f"{slug_clean}/{file_path.relative_to(processed_dir)}"
                        if arcname not in added_files:
                            zf.write(file_path, arcname=arcname)
                            added_files.add(arcname)
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"{slug_clean}-export.zip"
        )
    
    except Exception as e:
        current_app.logger.exception("Export failed for %s: %s", slug_clean, e)
        return {"status": "error", "message": "Export failed"}, 500
