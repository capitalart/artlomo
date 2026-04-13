import gc
import json
import logging
import os
import psutil
import threading
import uuid
from datetime import datetime, timezone
import shutil
from pathlib import Path
from flask import Blueprint, abort, current_app, flash, jsonify, redirect, render_template, request, send_file, session, url_for
from ..services import qc_service, storage_service, thumb_service
from ..services.storage_service import _read_json_or_none
from ...common.utilities import slug_sku
from ...common.utilities import images
from ...artwork.services.index_service import ArtworksIndex, build_assets_document, validate_asset_paths
from ...artwork.services.processing_service import ProcessingService
from ...artwork.errors import ArtworkProcessingError, IndexValidationError, RequiredAssetMissingError
from application.utils.csrf import require_csrf_or_400
from application.utils.logger_utils import log_security_event
from application.utils.artwork_db import sync_artwork_to_db, delete_artwork_from_db, get_artworks_by_status, soft_delete_artwork, soft_delete_artwork_by_slug, restore_artwork, get_deleted_artworks, purge_old_deleted_artworks, update_artwork_status

upload_bp = Blueprint(
    "upload",
    __name__,
)

# ============================================================================
# Memory-Safe Upload Processing (Sequential to prevent OOM on 2-CPU VM)
# ============================================================================
# Lock ensures only one artwork is processed at a time, preventing memory
# contention from multiple concurrent image processing threads.
_upload_processing_lock = threading.Lock()
_logger = logging.getLogger(__name__)


def _require_safe_slug(slug: str) -> None:
    if not slug_sku.is_safe_slug(slug):
        abort(404)


def _cfg() -> dict:
    return current_app.config


def _sync_artworks_index_after_delete(cfg: dict, *, slug: str, sku: str | None) -> None:
    """Remove deleted artwork entry from artworks.json using SKU, then slug fallback."""
    index = ArtworksIndex(Path(cfg["ARTWORKS_INDEX_PATH"]), Path(cfg["LAB_PROCESSED_DIR"]))
    sku_text = str(sku or "").strip()
    if sku_text:
        index.remove_by_sku(sku_text)
        return
    index.remove_by_slug(slug)


@upload_bp.route("/", methods=["GET"])
def root():
    return redirect(url_for("upload.unprocessed"))


@upload_bp.route("/upload", methods=["GET"])
def upload_page():
    return render_template("artworks/upload.html", constraints=_constraints(), page_title="Upload")


@upload_bp.route("/upload", methods=["POST"])  # type: ignore[misc]
def handle_upload():
    cfg = _cfg()
    file = request.files.get("artwork")
    wants_json = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.accept_mimetypes.best == "application/json"

    ok, resp = require_csrf_or_400(request)
    if not ok:
        if wants_json:
            return jsonify({"status": "error", "message": "missing or invalid csrf token"}), 400
        return resp

    if not file or file.filename == "":
        message = "Please choose a JPG file to upload."
        if wants_json:
            return jsonify({"status": "error", "message": message}), 400
        flash(message, "danger")
        return render_template("artworks/upload.html", constraints=_constraints(), page_title="Upload"), 400

    file_bytes = file.read()
    filename = file.filename or "unknown"
    validator = qc_service.QCService(
        required_long_edge=cfg["REQUIRED_LONG_EDGE_PX"],
        required_dpi=cfg["REQUIRED_DPI"],
        allowed_extensions=cfg["ALLOWED_EXTENSIONS"],
    )
    qc_result = validator.validate_upload(file_bytes, filename)

    if not qc_result.passed or not qc_result.info:
        if wants_json:
            return jsonify({"status": "error", "message": "; ".join(qc_result.reasons) or "Upload failed validation"}), 400
        for reason in qc_result.reasons:
            flash(reason, "danger")
        return render_template("artworks/upload.html", constraints=_constraints(), page_title="Upload"), 400

    sku = slug_sku.next_sku(Path(cfg["SKU_SEQUENCE_PATH"]))
    slug = slug_sku.slugify(sku)
    slug_dir = storage_service.target_dir(Path(cfg["LAB_UNPROCESSED_DIR"]), slug)
    artwork_id = sku

    # ========================================================================
    # MEMORY-SAFE SEQUENTIAL PROCESSING
    # Acquire lock to ensure only one artwork processes at a time (prevents OOM).
    # This prevents multiple concurrent image processing operations on a 2-CPU VM.
    # ========================================================================
    _upload_processing_lock.acquire()
    try:
        _update_processing_status(slug_dir, slug, stage="queued", message="Queued", done=False, percent=0)
        _update_processing_status(slug_dir, slug, stage="upload_complete", message="Upload received", done=False, percent=10)

        storage_service.store_original(slug_dir, file_bytes, slug=slug)
        _update_processing_status(slug_dir, slug, stage="qc", message="Running quality checks", done=False, percent=30)

        thumb_bytes = thumb_service.create_thumb(file_bytes, cfg["THUMB_SIZE"])
        storage_service.store_thumb(slug_dir, thumb_bytes, slug=slug)
        _update_processing_status(slug_dir, slug, stage="thumbnail", message="Thumbnail generated", done=False, percent=45)

        analyse_bytes = images.generate_analyse_image(file_bytes, target_long_edge=cfg["ANALYSE_LONG_EDGE"])
        storage_service.store_analyse(slug_dir, slug, analyse_bytes)
        analyse_qc = qc_service.QCService.analyse_qc(analyse_bytes)
        
        # ====================================================================
        # STAGE 8: DERIVATIVES - Memory-critical stage
        # Log available RAM before high-memory image operations
        # ====================================================================
        available_mb = psutil.virtual_memory().available / (1024 * 1024)
        _logger.info(f"[MEMORY] Available RAM: {available_mb:.2f} MB | Stage: DERIVATIVES | Slug: {slug}")
        
        _update_processing_status(slug_dir, slug, stage="derivatives", message="Generating sizes", done=False, percent=65)
        
        # Generate 7200px Closeup Proxy for detail editing (Stage 8: DERIVATIVES)
        logger = logging.getLogger(__name__)
        try:
            from ...artwork.services.detail_closeup_service import DetailCloseupService
            proxy_svc = DetailCloseupService(processed_root=slug_dir.parent)
            if proxy_svc.generate_proxy_preview(slug):
                logger.info(f"[DERIVATIVES] Generated 7200px Closeup Proxy for {slug}")
            else:
                logger.warning(f"[DERIVATIVES] Closeup Proxy generation returned False for {slug}")
        except Exception as proxy_exc:
            logger.warning(
                f"[DERIVATIVES] Failed to generate Closeup Proxy for {slug}: {proxy_exc}"
            )

        # ====================================================================
        # POST-STAGE 8: Memory cleanup
        # Explicitly free large image buffers after derivatives complete.
        # Call gc.collect() to reclaim pixel buffers held by PIL/cv2/numpy.
        # ====================================================================
        del analyse_bytes
        del thumb_bytes
        images.cleanup_memory()
        
        qc_payload = qc_service.QCService.qc_payload(
            file_bytes=file_bytes,
            min_long_edge=cfg["REQUIRED_LONG_EDGE_PX"],
            min_dpi=cfg["REQUIRED_DPI"],
        )
        storage_service.store_qc(slug_dir, qc_payload, sku=sku)
        _update_processing_status(slug_dir, slug, stage="metadata", message="Writing metadata", done=False, percent=82)
        owner_id = session.get("username") if session.get("role") == "artist" else None
        original_filename = file.filename or "unknown"
        meta_payload = storage_service.base_meta(
            slug=slug,
            artwork_id=artwork_id,
            display_title=sku,
            artist_name="",
            original_filename=original_filename,
            prompt_text=None,
            owner_id=owner_id,
        )
        meta_payload["analyse_qc"] = analyse_qc
        storage_service.store_meta(slug_dir, meta_payload, sku=sku)
        
        # ====================================================================
        # Final cleanup before completion (now safe to delete all buffers)
        # ====================================================================
        del file_bytes
        del analyse_qc
        images.cleanup_memory()
        
        _update_processing_status(slug_dir, slug, stage="finalizing", message="Finalizing", done=False, percent=93)

        # Initialize unprocessed assets manifest + global artworks index entry.
        files_map = {
            "master": storage_service.master_name(slug),
            "thumb": storage_service.thumb_name(slug),
            "analyse": storage_service.analyse_name(slug),
            "metadata": storage_service._meta_name(sku),
            "qc": storage_service._qc_name(sku),
            "processing_status": storage_service.PROCESSING_STATUS_NAME,
        }
        closeup_proxy_name = f"{slug}-CLOSEUP-PROXY.jpg"
        if (slug_dir / closeup_proxy_name).exists():
            files_map["closeup_proxy"] = closeup_proxy_name

        validate_asset_paths(slug_dir, files_map)
        assets_payload = build_assets_document(slug=slug, sku=sku, files=files_map)
        assets_path = slug_dir / f"{sku.lower()}-assets.json"
        from ...common.utilities.files import write_json_atomic

        write_json_atomic(assets_path, assets_payload)
        ArtworksIndex(Path(cfg["ARTWORKS_INDEX_PATH"]), Path(cfg["LAB_PROCESSED_DIR"])).upsert(
            sku=sku,
            slug=slug,
            artwork_dirname=slug,
            assets_file=assets_path.name,
            stage="unprocessed",
        )

        _update_processing_status(slug_dir, slug, stage="complete", message="Ready", done=True, percent=100)

        # Double-write: sync to database
        sync_artwork_to_db(
            sku=sku,
            slug=slug,
            title=sku,
            owner_id=owner_id,
            status="unprocessed",
            image_path=f"{slug}.jpg",
            thumb_path=f"{slug}-THUMB.jpg",
            metadata=meta_payload,
        )
    except Exception as exc:  # pylint: disable=broad-except
        _logger.exception(f"[UPLOAD_ERROR] Upload processing failed for {slug}: {exc}")
        _update_processing_status(slug_dir, slug, stage="error", message=str(exc), done=True, percent=100, error=str(exc))
        if wants_json:
            return jsonify({"status": "error", "message": "Upload processing failed"}), 500
        flash("Upload processing failed", "danger")
        return render_template("artworks/upload.html", constraints=_constraints(), page_title="Upload"), 500
    finally:
        # Release the upload processing lock (critical for memory safety)
        _upload_processing_lock.release()

    if wants_json:
        return jsonify(
            {
                "status": "ok",
                "slug": slug,
                "thumb_url": url_for("upload.thumb", slug=slug),
                "unprocessed_url": url_for("upload.unprocessed"),
            }
        )

    flash("Upload passed QC and was stored in Unprocessed.", "success")
    return redirect(url_for("upload.unprocessed"))


def _get_profile_artist_name() -> str | None:
    """Load artist name from profile.json (prioritized over per-artwork metadata)."""
    try:
        profile_path = Path(current_app.root_path) / "var" / "profile.json"
        if profile_path.exists():
            data = json.loads(profile_path.read_text(encoding="utf-8"))
            return (data.get("artist_name") or "").strip() or None
    except Exception:
        pass
    return None


def _filter_by_owner(items: list[dict]) -> list[dict]:
    """Filter artworks by owner_id for artist role users. Admins see all."""
    role = session.get("role")
    if role == "admin" or session.get("is_admin"):
        return items
    
    if role != "artist":
        return items
    
    username = session.get("username")
    if not username:
        return []
    
    return [
        item for item in items
        if (item.get("meta") or {}).get("owner_id") == username
        or (item.get("meta") or {}).get("owner_id") is None
    ]


def _enrich_items(items: list[dict], root: Path | None = None) -> list[dict]:
    profile_name = _get_profile_artist_name()

    def _load_listing_status(slug: str) -> dict | None:
        if root is None:
            return None
        slug_dir = root / str(slug or "").strip()
        if not slug_dir.exists() or not slug_dir.is_dir():
            return None

        for candidate in sorted(slug_dir.glob("*-listing.json")):
            try:
                listing_doc = json.loads(candidate.read_text(encoding="utf-8"))
                if isinstance(listing_doc, dict):
                    return listing_doc
            except Exception:
                continue

        legacy = slug_dir / "listing.json"
        if legacy.exists():
            try:
                listing_doc = json.loads(legacy.read_text(encoding="utf-8"))
                if isinstance(listing_doc, dict):
                    return listing_doc
            except Exception:
                return None
        return None

    for item in items:
        qc = item.get("qc") or {}
        uploaded_at = qc.get("uploaded_at") if isinstance(qc, dict) else None
        item["upload_date_display"] = _format_uploaded_date(uploaded_at)
        meta = item.get("meta") or {}
        item["sku"] = meta.get("sku") or meta.get("artwork_id") or item.get("slug")
        artist_meta = meta.get("artist") if isinstance(meta, dict) else None
        fallback_name = (artist_meta or {}).get("name") or meta.get("artist_name") if isinstance(meta, dict) else None
        item["artist_display"] = profile_name or fallback_name
        print_sizes = qc_service.derive_max_print_sizes(qc) if qc else {}
        item["print_size_display"] = _format_print_sizes(print_sizes)

        listing_doc = _load_listing_status(item.get("slug") or "")
        status_doc = listing_doc.get("analysis_status") if isinstance(listing_doc, dict) else None
        stage = str((status_doc or {}).get("stage") or "").strip().lower() if isinstance(status_doc, dict) else ""
        message = str((status_doc or {}).get("message") or "").strip() if isinstance(status_doc, dict) else ""
        error = str((status_doc or {}).get("error") or "").strip() if isinstance(status_doc, dict) else ""
        source = str((listing_doc or {}).get("analysis_source") or "").strip().lower() if isinstance(listing_doc, dict) else ""

        item["analysis_source"] = item.get("analysis_source") or source or None
        item["analysis_status"] = status_doc if isinstance(status_doc, dict) else None
        item["analysis_failed"] = stage in {"failed", "error"}
        item["analysis_failure_reason"] = error or message
    return items


def _resolve_review_url(slug: str, processed_root: Path) -> str | None:
    slug_dir = processed_root / slug
    if not slug_dir.exists() or not slug_dir.is_dir():
        return None

    def exists(name: str) -> bool:
        return (slug_dir / name).exists()
    
    def exists_prefixed(sku: str, base_name: str) -> bool:
        """Check for both SKU-prefixed and legacy filenames."""
        # Try SKU-prefixed first (newer format)
        if (slug_dir / f"{sku.lower()}-{base_name}").exists():
            return True
        # Fall back to legacy format
        return (slug_dir / base_name).exists()

    listing_source = None
    
    # Try to find listing file (SKU-prefixed or legacy)
    listing_path = None
    # First, try to find any {sku}-listing.json file
    for candidate in slug_dir.iterdir():
        if candidate.is_file() and candidate.name.endswith("-listing.json"):
            listing_path = candidate
            break
    # Fall back to legacy listing.json
    if not listing_path:
        legacy_path = slug_dir / "listing.json"
        if legacy_path.exists():
            listing_path = legacy_path
    
    if listing_path and listing_path.exists():
        try:
            listing_doc = json.loads(listing_path.read_text(encoding="utf-8"))
            listing_source = str(listing_doc.get("analysis_source") or "").lower()
        except Exception:
            listing_source = None
    
    # Extract SKU from slug or listing
    sku = slug
    if listing_path:
        try:
            listing_doc = json.loads(listing_path.read_text(encoding="utf-8"))
            sku = str(listing_doc.get("sku") or slug).lower()
        except Exception:
            sku = slug

    if listing_source == "manual" or exists_prefixed(sku, "metadata_manual.json"):
        return url_for("manual.workspace", slug=slug)
    if listing_source == "openai" or exists_prefixed(sku, "metadata_openai.json"):
        return url_for("artwork.review_openai", slug=slug)
    if listing_source == "gemini" or exists_prefixed(sku, "metadata_gemini.json"):
        return url_for("artwork.review_gemini", slug=slug)
    if exists("metadata.json"):
        return url_for("artwork.review_openai", slug=slug)
    return url_for("artwork.review", slug=slug)


def _analysis_source_for_slug(slug: str, processed_root: Path) -> str | None:
    slug_dir = processed_root / slug
    if not slug_dir.exists() or not slug_dir.is_dir():
        return None

    listing_path = slug_dir / "listing.json"
    if listing_path.exists():
        try:
            listing_doc = json.loads(listing_path.read_text(encoding="utf-8"))
            value = str(listing_doc.get("analysis_source") or "").strip().lower()
            return value or None
        except Exception:
            return None

    if (slug_dir / "metadata_manual.json").exists():
        return "manual"
    if (slug_dir / "metadata_openai.json").exists():
        return "openai"
    if (slug_dir / "metadata_gemini.json").exists():
        return "gemini"

    meta_path = slug_dir / "metadata.json"
    if meta_path.exists():
        try:
            meta_doc = json.loads(meta_path.read_text(encoding="utf-8"))
            value = str(meta_doc.get("analysis_source") or "").strip().lower()
            return value or None
        except Exception:
            return None
    return None


def _format_analysed_date(iso_str: str | None) -> str | None:
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        local_dt = dt.astimezone()
        return local_dt.strftime("%d %b %Y")
    except Exception:
        return None


def _analysed_date_for_slug(slug: str, processed_root: Path) -> str | None:
    slug_dir = processed_root / str(slug or "").strip()
    if not slug_dir.exists() or not slug_dir.is_dir():
        return None
    listing_path = slug_dir / "listing.json"
    if not listing_path.exists():
        return None
    try:
        listing_doc = json.loads(listing_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(listing_doc, dict):
        return None
    status = listing_doc.get("analysis_status")
    updated_at = status.get("updated_at") if isinstance(status, dict) else None
    return _format_analysed_date(str(updated_at)) if updated_at else None


def _get_owner_filter() -> str | None:
    """Return owner_id for DB filtering. None means show all (admin)."""
    role = session.get("role")
    if role == "admin" or session.get("is_admin"):
        return None  # Admins see all
    if role == "artist":
        return session.get("username")
    return None


def _resolve_sku_from_slug_dir(slug_dir: Path, slug_hint: str | None = None) -> str:
    """Resolve SKU from filesystem docs with SKU-prefixed fallback support."""
    slug_text = str(slug_hint or slug_dir.name or "").strip()

    # 1) Metadata (preferred)
    try:
        meta = storage_service.load_metadata_with_fallback(slug_dir) or {}
        if isinstance(meta, dict):
            sku = str(meta.get("sku") or meta.get("artwork_id") or "").strip()
            if sku:
                return sku
    except Exception:
        pass

    # 2) Assets manifest
    try:
        assets = storage_service.load_assets_manifest(slug_dir) or {}
        if isinstance(assets, dict):
            sku = str(assets.get("sku") or "").strip()
            if sku:
                return sku
    except Exception:
        pass

    # 3) Best-effort fallback from slug
    return slug_text.upper() if slug_text else ""


def _load_qc_with_fallback(slug_dir: Path) -> dict:
    """Load QC JSON with support for SKU-prefixed filenames."""
    # Try SKU-prefixed QC first
    try:
        for candidate in slug_dir.iterdir():
            if candidate.is_file() and candidate.name.endswith("-qc.json"):
                return json.loads(candidate.read_text(encoding="utf-8"))
    except Exception:
        pass

    # Fall back to legacy qc.json
    qc_path = slug_dir / "qc.json"
    if qc_path.exists():
        try:
            return json.loads(qc_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    return {}


def _db_artworks_to_items(db_artworks: list[dict], root: Path) -> list[dict]:
    """Convert database artwork records to template-compatible items."""
    items = []
    for art in db_artworks:
        slug = art.get("slug")
        slug_dir = root / slug if slug else None
        
        # Load additional data from filesystem for enrichment
        meta = art.get("metadata") or {}
        qc = {}
        if slug_dir and slug_dir.exists():
            qc = _load_qc_with_fallback(slug_dir)
            if not isinstance(meta, dict) or not meta:
                try:
                    meta = storage_service.load_metadata_with_fallback(slug_dir) or {}
                except Exception:
                    meta = {}
        
        # Include thumb_path - templates need this to render thumbnail URLs
        thumb_path = art.get("thumb_path")
        if not thumb_path and slug_dir and slug_dir.exists():
            # Try to find thumbnail file if not in DB
            slug_upper = slug.upper() if slug else ""
            for candidate in [f"{slug}-THUMB.jpg", f"{slug_upper}-THUMB.jpg"]:
                if (slug_dir / candidate).exists():
                    thumb_path = candidate
                    break
        
        items.append({
            "slug": slug,
            "meta": meta,
            "qc": qc,
            "sku": art.get("sku") or art.get("id"),
            "title": art.get("title"),
            "owner_id": art.get("owner_id"),
            "analysis_source": art.get("analysis_source"),
            "thumb_path": thumb_path,
            "image_path": art.get("image_path"),
            "created_at": art.get("created_at"),
            "updated_at": art.get("updated_at"),
        })
    return items


@upload_bp.route("/unprocessed", methods=["GET"])
def unprocessed():
    cfg = _cfg()
    
    # Use database for owner-filtered queries
    owner_filter = _get_owner_filter()
    db_artworks = get_artworks_by_status("unprocessed", owner_id=owner_filter)
    
    if db_artworks:
        # DB has data - use it for filtering
        items = _enrich_items(_db_artworks_to_items(db_artworks, Path(cfg["LAB_UNPROCESSED_DIR"])), root=Path(cfg["LAB_UNPROCESSED_DIR"]))
    else:
        # Fallback to filesystem scan (backward compatibility)
        items = _filter_by_owner(_enrich_items(storage_service.list_unprocessed(Path(cfg["LAB_UNPROCESSED_DIR"])), root=Path(cfg["LAB_UNPROCESSED_DIR"])))
    
    username = (session.get("username") or "").strip()
    display_name = current_app.config.get("ADMIN_DISPLAY_NAME") or os.getenv("ADMIN_DISPLAY_NAME")
    if not display_name and username:
        display_name = username
    return render_template(
        "artworks/unprocessed.html",
        items=items,
        current_artist=(display_name or ""),
        page_title="Unprocessed",
    )


@upload_bp.route("/unprocessed/<slug>", methods=["GET"])
def unprocessed_item(slug: str):
    _require_safe_slug(slug)
    cfg = _cfg()
    item = storage_service.load_artwork(Path(cfg["LAB_UNPROCESSED_DIR"]), slug)
    if not item:
        flash("Artwork not found in Unprocessed.", "warning")
        return render_template("artworks/unprocessed.html", items=[], current_artist="", page_title="Unprocessed")
    items = _enrich_items([item], root=Path(cfg["LAB_UNPROCESSED_DIR"]))
    username = (session.get("username") or "").strip()
    display_name = current_app.config.get("ADMIN_DISPLAY_NAME") or os.getenv("ADMIN_DISPLAY_NAME")
    if not display_name and username:
        display_name = username
    return render_template(
        "artworks/unprocessed.html",
        items=items,
        current_artist=(display_name or ""),
        page_title="Unprocessed",
    )


@upload_bp.route("/unprocessed/<slug>/custom-input", methods=["GET"])
def custom_input(slug: str):
    """Display the custom input form for artist-provided seed context."""
    _require_safe_slug(slug)
    cfg = _cfg()
    slug_dir = Path(cfg["LAB_UNPROCESSED_DIR"]) / slug
    if not slug_dir.exists():
        flash("Artwork not found.", "warning")
        return redirect(url_for("upload.unprocessed"))
    
    item = storage_service.load_artwork(Path(cfg["LAB_UNPROCESSED_DIR"]), slug)
    seed_context = storage_service.load_seed_context(slug_dir) or {}
    
    display_title = ""
    sku = slug
    thumb_url = None
    original_filename = ""
    if item:
        meta = item.get("meta") or {}
        display_title = meta.get("display_title") or ""
        sku = meta.get("sku") or meta.get("artwork_id") or slug
        original_filename = meta.get("original_filename") or ""
        if item.get("thumb_path"):
            thumb_url = url_for("upload.thumb", slug=slug)
    
    return render_template(
        "artworks/custom_input.html",
        slug=slug,
        sku=sku,
        display_title=display_title,
        thumb_url=thumb_url,
        seed_context=seed_context,
        original_filename=original_filename,
        page_title="Custom Input",
    )


def _processing_service() -> ProcessingService:
    """Get the processing service for promoting artwork."""
    cfg = _cfg()
    return ProcessingService(
        unprocessed_root=Path(cfg["LAB_UNPROCESSED_DIR"]),
        processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
        artworks_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
    )


def _promote_to_processed_for_analysis(slug: str) -> None:
    """Promote artwork from unprocessed to processed for analysis."""
    cfg = _cfg()
    locked_root = Path(cfg["LAB_LOCKED_DIR"])
    if (locked_root / slug).exists():
        raise ArtworkProcessingError("Artwork is locked and cannot be analysed.")
    
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if processed_dir.exists():
        return  # Already processed
    
    svc = _processing_service()
    try:
        svc.process(slug)
    except IndexValidationError:
        # Already processed or invalid; let analysis continue
        return


def _start_analysis_thread(slug: str, provider: str) -> None:
    """Enqueue AI analysis job in DB-backed worker queue."""
    from application.common.utilities.files import write_json_atomic
    from db import AnalysisJob, SessionLocal
    
    cfg = _cfg()
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    listing_path = processed_dir / "listing.json"
    
    # Initialize listing status
    now_iso = datetime.now(timezone.utc).isoformat()
    meta_path = processed_dir / storage_service.META_NAME
    meta = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    sku = str(meta.get("sku") or meta.get("artwork_id") or slug).strip() or slug
    
    listing = {}
    if listing_path.exists():
        try:
            listing = json.loads(listing_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    
    listing.update({
        "slug": slug,
        "sku": sku,
        "analysis_source": provider,
        "analysis_status": {
            "stage": "queued",
            "message": f"{provider.title()} analysis queued",
            "done": False,
            "error": None,
            "source": provider,
            "updated_at": now_iso,
        },
        "updated_at": now_iso,
    })
    if "created_at" not in listing:
        listing["created_at"] = now_iso
    
    # Persist listing with SKU-prefixed naming to align with processing conventions.
    write_json_atomic(processed_dir / f"{sku.lower()}-listing.json", listing)

    # Queue the analysis job for the shared background worker.
    job_id = str(uuid.uuid4())
    session = SessionLocal()
    try:
        session.add(
            AnalysisJob(
                job_id=job_id,
                slug=slug,
                sku=sku,
                provider=provider,
                status="QUEUED",
                stage="stage1_image",
                progress=0,
                attempts=0,
            )
        )
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    # Keep manifest-level analysis status in sync with queue state.
    manifest_path = processed_dir / f"{slug}-assets.json"
    manifest_candidates = sorted(processed_dir.glob("*-assets.json"))
    if manifest_candidates:
        manifest_path = manifest_candidates[0]
    manifest = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}
    manifest.setdefault("files", {})
    manifest.setdefault("analysis", {})
    manifest["analysis"].update(
        {
            "status": "queued",
            "stage": "stage1_image",
            "progress": 0,
            "provider": provider,
            "job_id": job_id,
            "queued_at": now_iso,
            "updated_at": now_iso,
        }
    )
    write_json_atomic(manifest_path, manifest)


@upload_bp.route("/unprocessed/<slug>/seed-context", methods=["POST"])  # type: ignore[misc]
def save_seed_context(slug: str):
    """Save artist-provided seed context and optionally trigger analysis."""
    _require_safe_slug(slug)
    
    ok, resp = require_csrf_or_400(request)
    if not ok:
        assert resp is not None
        return resp
    
    cfg = _cfg()
    slug_dir = Path(cfg["LAB_UNPROCESSED_DIR"]) / slug
    if not slug_dir.exists():
        flash("Artwork not found.", "warning")
        return redirect(url_for("upload.unprocessed"))
    
    # Extract form data
    location = request.form.get("location", "").strip()
    # Support both 'sentiment' (new) and 'notes' (legacy) field names
    sentiment = request.form.get("sentiment", "").strip() or request.form.get("notes", "").strip()
    original_prompt = request.form.get("original_prompt", "").strip()
    action = request.form.get("action", "save_only")
    
    # Build seed context payload
    seed_payload = {
        "location": location,
        "sentiment": sentiment,
        "original_prompt": original_prompt,
    }
    
    # Save to seed_context.json
    storage_service.store_seed_context(slug_dir, seed_payload)
    flash("Seed context saved successfully.", "success")
    
    # Route to appropriate analysis based on action
    if action == "analyze_openai":
        try:
            _promote_to_processed_for_analysis(slug)
            _start_analysis_thread(slug, "openai")
            flash("OpenAI analysis started. Processing...", "info")
        except (RequiredAssetMissingError, ArtworkProcessingError) as exc:
            flash(str(exc), "danger")
            return redirect(url_for("upload.unprocessed"))
        return redirect(url_for("artwork.openai_analysis", slug=slug))
    
    elif action == "analyze_gemini":
        try:
            _promote_to_processed_for_analysis(slug)
            _start_analysis_thread(slug, "gemini")
            flash("Gemini analysis started. Processing...", "info")
        except (RequiredAssetMissingError, ArtworkProcessingError) as exc:
            flash(str(exc), "danger")
            return redirect(url_for("upload.unprocessed"))
        return redirect(url_for("artwork.gemini_analysis", slug=slug))
    
    # Otherwise, return to unprocessed list
    return redirect(url_for("upload.unprocessed"))


@upload_bp.route("/processed", methods=["GET"])
def processed():
    cfg = _cfg()
    processed_root = Path(cfg["LAB_PROCESSED_DIR"])
    
    # Use database for owner-filtered queries
    owner_filter = _get_owner_filter()
    db_artworks = get_artworks_by_status("processed", owner_id=owner_filter)
    
    if db_artworks:
        # DB has data - use it for filtering
        items = _enrich_items(_db_artworks_to_items(db_artworks, processed_root), root=processed_root)
    else:
        # Fallback to filesystem scan (backward compatibility)
        items = _filter_by_owner(_enrich_items(storage_service.list_processed(processed_root), root=processed_root))
    
    for item in items:
        item["review_url"] = _resolve_review_url(item.get("slug") or "", processed_root)
        item["analysis_source"] = item.get("analysis_source") or _analysis_source_for_slug(item.get("slug") or "", processed_root)
        item["analysed_date_display"] = _analysed_date_for_slug(item.get("slug") or "", processed_root)
    return render_template("artworks/processed.html", items=items, page_title="Processed")


@upload_bp.route("/locked", methods=["GET"])
def locked():
    cfg = _cfg()
    locked_root = Path(cfg["LAB_LOCKED_DIR"])
    
    # Use database for owner-filtered queries
    owner_filter = _get_owner_filter()
    db_artworks = get_artworks_by_status("locked", owner_id=owner_filter)
    
    if db_artworks:
        # DB has data - use it for filtering
        items = _enrich_items(_db_artworks_to_items(db_artworks, locked_root))
    else:
        # Fallback to filesystem scan (backward compatibility)
        items = _filter_by_owner(_enrich_items(storage_service.list_locked(locked_root)))

    for item in items:
        item["analysed_date_display"] = _analysed_date_for_slug(item.get("slug") or "", locked_root)
    
    return render_template("artworks/locked.html", items=items, page_title="Locked")


@upload_bp.route("/locked/<slug>/unlock", methods=["POST"])
def unlock_locked(slug: str):
    _require_safe_slug(slug)

    ok, resp = require_csrf_or_400(request)
    if not ok:
        assert resp is not None
        return resp

    cfg = _cfg()
    locked_dir = Path(cfg["LAB_LOCKED_DIR"]) / slug
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug

    wants_json = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.accept_mimetypes.best == "application/json"

    if not locked_dir.exists() or not locked_dir.is_dir():
        msg = "Locked artwork not found"
        if wants_json:
            return jsonify({"status": "error", "message": msg}), 404
        flash(msg, "warning")
        return redirect(url_for("upload.locked"))

    if processed_dir.exists():
        msg = "Processed artwork already exists for this slug"
        if wants_json:
            return jsonify({"status": "error", "message": msg}), 400
        flash(msg, "warning")
        return redirect(url_for("upload.locked"))

    sku = _resolve_sku_from_slug_dir(locked_dir, slug)

    try:
        shutil.move(str(locked_dir), str(processed_dir))
    except Exception as exc:
        if wants_json:
            return jsonify({"status": "error", "message": str(exc)}), 500
        flash(f"Unlock failed: {exc}", "danger")
        return redirect(url_for("upload.locked"))

    if sku:
        try:
            assets_name = f"{slug}-assets.json"
            assets_path = processed_dir / assets_name
            if not assets_path.exists():
                candidates = sorted(processed_dir.glob("*-assets.json"))
                if candidates:
                    assets_name = candidates[0].name

            ArtworksIndex(Path(cfg["ARTWORKS_INDEX_PATH"]), Path(cfg["LAB_PROCESSED_DIR"])).upsert(
                sku=sku,
                slug=slug,
                artwork_dirname=slug,
                assets_file=assets_name,
                stage="processed",
            )
        except Exception:
            current_app.logger.warning("Failed to upsert artworks index during unlock for slug=%s", slug)

        try:
            update_artwork_status(sku, "processed")
        except Exception:
            current_app.logger.warning("Failed to update DB status during unlock for slug=%s", slug)

    log_security_event(user_id=session.get("username"), action="unlock_locked", details=f"slug={slug} sku={sku}")

    if wants_json:
        return jsonify({"status": "ok", "slug": slug, "sku": sku, "redirect_url": url_for("upload.processed")})

    flash(f"{slug} moved back to Processed.", "success")
    return redirect(url_for("upload.processed"))


@upload_bp.route("/trash", methods=["GET"])
def trash():
    """Display artworks in trash (soft-deleted)."""
    from datetime import datetime, timedelta
    
    cfg = _cfg()
    
    # Use database for owner-filtered queries
    owner_filter = _get_owner_filter()
    db_artworks = get_deleted_artworks(owner_id=owner_filter)
    
    # Determine which root to use based on previous_status
    items = []
    now = datetime.utcnow()
    
    for art in db_artworks:
        prev_status = art.get("previous_status") or "unprocessed"
        if prev_status == "processed":
            root = Path(cfg["LAB_PROCESSED_DIR"])
        elif prev_status == "locked":
            root = Path(cfg["LAB_LOCKED_DIR"])
        else:
            root = Path(cfg["LAB_UNPROCESSED_DIR"])
        
        item_list = _db_artworks_to_items([art], root)
        if item_list:
            item_list[0]["previous_status"] = prev_status
            item_list[0]["deleted_at"] = art.get("deleted_at")
            
            # Calculate days left until permanent deletion (14 days from deleted_at)
            deleted_at = art.get("deleted_at")
            if deleted_at:
                if isinstance(deleted_at, str):
                    try:
                        deleted_at = datetime.fromisoformat(deleted_at.replace("Z", "+00:00").split("+")[0])
                    except Exception:
                        deleted_at = None
                if deleted_at:
                    expiry_date = deleted_at + timedelta(days=14)
                    days_left = (expiry_date - now).days
                    item_list[0]["days_left"] = max(0, days_left)
                else:
                    item_list[0]["days_left"] = 14
            else:
                item_list[0]["days_left"] = 14
            
            items.extend(item_list)
    
    items = _enrich_items(items)
    return render_template("artworks/trash.html", items=items, page_title="Trash")


@upload_bp.post("/trash/<slug>/restore")  # type: ignore[misc]
def restore_from_trash(slug: str):
    """Restore artwork from trash to its previous status."""
    _require_safe_slug(slug)
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    
    # Find the artwork by slug to get its SKU
    from application.utils.artwork_db import get_artwork_by_sku
    from db import SessionLocal, Artwork
    
    sku = None
    try:
        with SessionLocal() as db_session:
            artwork = db_session.query(Artwork).filter_by(slug=slug, status="deleted").first()
            if artwork:
                sku = str(artwork.id)
    except Exception:
        pass
    
    if not sku:
        return {"status": "error", "message": "Artwork not found in trash"}, 404
    
    if restore_artwork(sku):
        log_security_event(user_id=session.get("username"), action="restore_from_trash", details=f"slug={slug} sku={sku}")  # type: ignore[call-arg]
        return {"status": "ok", "slug": slug, "sku": sku, "action": "restored"}
    
    return {"status": "error", "message": "Failed to restore artwork"}, 500


@upload_bp.post("/trash/<slug>/permanent-delete")  # type: ignore[misc]
def permanent_delete(slug: str):
    """Permanently delete artwork from trash (removes files and DB record)."""
    _require_safe_slug(slug)
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    
    cfg = _cfg()
    
    # Find the artwork by slug
    from db import SessionLocal, Artwork
    
    sku = None
    prev_status = None
    try:
        with SessionLocal() as db_session:
            artwork = db_session.query(Artwork).filter_by(slug=slug, status="deleted").first()
            if artwork:
                sku = str(artwork.id)
                prev_status = str(artwork.previous_status) if (artwork.previous_status is not None) else None
    except Exception:
        pass
    
    if not sku:
        return {"status": "error", "message": "Artwork not found in trash"}, 404
    
    # Determine which directory to delete from
    if prev_status == "processed":
        slug_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    elif prev_status == "locked":
        slug_dir = Path(cfg["LAB_LOCKED_DIR"]) / slug
    else:
        slug_dir = Path(cfg["LAB_UNPROCESSED_DIR"]) / slug
    
    # Delete files
    try:
        if slug_dir.exists() and slug_dir.is_dir():
            shutil.rmtree(slug_dir)
    except Exception as exc:
        return {"status": "error", "message": f"Failed to delete files: {exc}"}, 500
    
    # Remove from database
    delete_artwork_from_db(sku)
    
    # Remove from index if it was processed
    if prev_status == "processed":
        try:
            _sync_artworks_index_after_delete(cfg, slug=slug, sku=sku)
        except Exception:
            _logger.exception("Failed to sync artworks index after permanent delete slug=%s sku=%s", slug, sku)
    
    log_security_event(user_id=session.get("username"), action="permanent_delete", details=f"slug={slug} sku={sku}")  # type: ignore[call-arg]
    
    return {"status": "ok", "slug": slug, "sku": sku, "action": "permanently_deleted"}


@upload_bp.post("/unprocessed/<slug>/delete")  # type: ignore[misc]
def delete_unprocessed(slug: str):
    import shutil
    _require_safe_slug(slug)
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    cfg = _cfg()
    slug_dir = Path(cfg["LAB_UNPROCESSED_DIR"]) / slug
    if not slug_dir.exists():
        return {"status": "error", "message": "Not found"}, 404
    if not slug_dir.is_dir():
        return {"status": "error", "message": "Invalid target"}, 400

    # Read metadata to get SKU
    meta_path = slug_dir / storage_service.META_NAME
    sku = None
    try:
        if meta_path.exists():
            meta_payload = json.loads(meta_path.read_text(encoding="utf-8"))
            sku = meta_payload.get("sku") or meta_payload.get("artwork_id")
    except Exception as exc:
        _logger.warning("Failed to read metadata for slug %s: %s", slug, exc)
        sku = None

    # Delete files physically
    try:
        shutil.rmtree(slug_dir)
    except Exception as exc:
        return {"status": "error", "message": f"Failed to delete files: {exc}"}, 500

    # Soft delete: move to trash in database (try SKU first, then fallback to slug)
    db_deleted = False
    if sku:
        db_deleted = soft_delete_artwork(str(sku))
        if not db_deleted:
            _logger.warning("Failed to soft-delete artwork by SKU (slug=%s sku=%s), trying slug fallback...", slug, sku)
            db_deleted = soft_delete_artwork_by_slug(slug)
    else:
        _logger.warning("No SKU found for slug %s - attempting delete by slug", slug)
        db_deleted = soft_delete_artwork_by_slug(slug)
    
    if not db_deleted:
        _logger.error("Failed to soft-delete artwork in database: slug=%s sku=%s (artwork not found in DB or error occurred)", slug, sku)

    try:
        _sync_artworks_index_after_delete(cfg, slug=slug, sku=str(sku) if sku else None)
    except Exception:
        _logger.exception("Failed to sync artworks index after unprocessed delete slug=%s sku=%s", slug, sku)

    log_security_event(user_id=session.get("username"), action="trash_unprocessed", details=f"slug={slug} sku={sku or ''} db_deleted={db_deleted}")

    return {"status": "ok", "slug": slug, "sku": sku, "action": "moved_to_trash", "db_deleted": db_deleted}


@upload_bp.post("/processed/<slug>/delete")  # type: ignore[misc]
def delete_processed(slug: str):
    import shutil
    _require_safe_slug(slug)
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    cfg = _cfg()
    slug_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if not slug_dir.exists():
        return {"status": "error", "message": "Not found"}, 404
    if not slug_dir.is_dir():
        return {"status": "error", "message": "Invalid target"}, 400

    meta_path = slug_dir / storage_service.META_NAME
    sku = None
    try:
        if meta_path.exists():
            meta_payload = json.loads(meta_path.read_text(encoding="utf-8"))
            sku = meta_payload.get("sku") or meta_payload.get("artwork_id")
    except Exception as exc:
        _logger.warning("Failed to read metadata for slug %s: %s", slug, exc)
        sku = None

    # Delete files physically
    try:
        shutil.rmtree(slug_dir)
    except Exception as exc:
        return {"status": "error", "message": f"Failed to delete files: {exc}"}, 500

    # Soft delete: move to trash in database (try SKU first, then fallback to slug)
    db_deleted = False
    if sku:
        db_deleted = soft_delete_artwork(str(sku))
        if not db_deleted:
            _logger.warning("Failed to soft-delete artwork by SKU (slug=%s sku=%s), trying slug fallback...", slug, sku)
            db_deleted = soft_delete_artwork_by_slug(slug)
    else:
        _logger.warning("No SKU found for slug %s - attempting delete by slug", slug)
        db_deleted = soft_delete_artwork_by_slug(slug)
    
    if not db_deleted:
        _logger.error("Failed to soft-delete artwork in database: slug=%s sku=%s (artwork not found in DB or error occurred)", slug, sku)

    try:
        _sync_artworks_index_after_delete(cfg, slug=slug, sku=str(sku) if sku else None)
    except Exception:
        _logger.exception("Failed to sync artworks index after processed delete slug=%s sku=%s", slug, sku)

    log_security_event(user_id=session.get("username"), action="trash_processed", details=f"slug={slug} sku={sku or ''} db_deleted={db_deleted}")

    return {"status": "ok", "slug": slug, "sku": sku, "action": "moved_to_trash", "db_deleted": db_deleted}


def _serve_thumb(slug: str, root: Path, redirect_endpoint: str):
    _require_safe_slug(slug)
    slug_dir = root / slug
    meta_path = slug_dir / storage_service.META_NAME
    legacy_meta = slug_dir / "upload_meta.json"
    thumb_filename = storage_service.thumb_name(slug)
    
    meta_payload: dict | None = None
    for candidate in (meta_path, legacy_meta):
        if candidate.exists():
            try:
                meta_payload = json.loads(candidate.read_text(encoding="utf-8"))
                break
            except Exception:
                meta_payload = None

    thumb_candidates = [thumb_filename]
    if meta_payload:
        if meta_payload.get("thumb_filename"):
            thumb_candidates.insert(0, meta_payload["thumb_filename"])
        legacy_id = meta_payload.get("artwork_id") or meta_payload.get("sku")
        if legacy_id:
            thumb_candidates.append(storage_service.thumb_name(str(legacy_id)))

    thumb_path = None
    for candidate in thumb_candidates:
        candidate_path = slug_dir / candidate
        if candidate_path.exists():
            thumb_path = candidate_path
            break

    if thumb_path is None or not thumb_path.exists():
        flash("Thumbnail not found.", "warning")
        return redirect(url_for(redirect_endpoint))
    
    return send_file(thumb_path)


@upload_bp.route("/unprocessed/<slug>/thumb")
def thumb(slug: str):
    _require_safe_slug(slug)
    cfg = _cfg()
    return _serve_thumb(slug, Path(cfg["LAB_UNPROCESSED_DIR"]), "upload.unprocessed")


@upload_bp.route("/processed/<slug>/thumb")
def processed_thumb(slug: str):
    _require_safe_slug(slug)
    cfg = _cfg()
    return _serve_thumb(slug, Path(cfg["LAB_PROCESSED_DIR"]), "upload.processed")


@upload_bp.route("/locked/<slug>/thumb")
def locked_thumb(slug: str):
    _require_safe_slug(slug)
    cfg = _cfg()
    return _serve_thumb(slug, Path(cfg["LAB_LOCKED_DIR"]), "upload.locked")


def _serve_analyse(slug: str, root: Path, redirect_endpoint: str):
    _require_safe_slug(slug)
    slug_dir = root / slug
    meta_path = slug_dir / storage_service.META_NAME
    legacy_meta = slug_dir / "upload_meta.json"
    analyse_filename = storage_service.analyse_name(slug)

    meta_payload: dict | None = None
    for candidate in (meta_path, legacy_meta):
        if candidate.exists():
            try:
                meta_payload = json.loads(candidate.read_text(encoding="utf-8"))
                break
            except Exception:
                meta_payload = None

    analyse_candidates = []
    
    # 1. Check assets.json first (source of truth)
    sku = slug
    if meta_payload:
        sku = str(meta_payload.get("sku") or meta_payload.get("artwork_id") or slug).strip().lower()
    assets_path = slug_dir / f"{sku}-assets.json"
    if not assets_path.exists():
        assets_path = slug_dir / "assets.json"
    if assets_path.exists():
        try:
            assets_doc = json.loads(assets_path.read_text(encoding="utf-8"))
            files = assets_doc.get("files") or {}
            analyse_from_assets = files.get("analyse")
            if analyse_from_assets:
                analyse_candidates.append(analyse_from_assets)
        except Exception:
            pass
    
    # 2. Check metadata analyse_filename
    if meta_payload and meta_payload.get("analyse_filename"):
        analyse_candidates.append(meta_payload["analyse_filename"])
    
    # 3. Default SKU-based filename
    analyse_candidates.append(analyse_filename)
    
    # 4. Legacy ID-based filename
    legacy_id = None
    if meta_payload:
        legacy_id = meta_payload.get("artwork_id") or meta_payload.get("sku")
    if legacy_id:
        analyse_candidates.append(storage_service.analyse_name(str(legacy_id)))

    selected = None
    for candidate in analyse_candidates:
        candidate_path = slug_dir / candidate
        if candidate_path.exists():
            selected = candidate
            break

    if not selected:
        master_candidates: list[str] = [storage_service.master_name(slug)]
        if meta_payload:
            master_from_meta = str(meta_payload.get("stored_filename") or "").strip()
            if master_from_meta:
                master_candidates.insert(0, master_from_meta)
            legacy_id = str(meta_payload.get("artwork_id") or meta_payload.get("sku") or "").strip()
            if legacy_id:
                master_candidates.append(storage_service.master_name(legacy_id))

        for master_name in master_candidates:
            master_path = slug_dir / master_name
            if not master_path.exists():
                continue
            try:
                master_bytes = master_path.read_bytes()
                analyse_bytes = images.generate_analyse_image(master_bytes, target_long_edge=_cfg()["ANALYSE_LONG_EDGE"])
                generated_path = storage_service.store_analyse(slug_dir, slug, analyse_bytes)
                selected = generated_path.name
                break
            except Exception:
                _logger.exception("Failed to regenerate analyse image for slug=%s", slug)

    if not selected:
        flash("Analyse preview not found.", "warning")
        return redirect(url_for(redirect_endpoint))

    return send_file(slug_dir / selected)


@upload_bp.route("/unprocessed/<slug>/analyse")
def analyse(slug: str):
    _require_safe_slug(slug)
    cfg = _cfg()
    return _serve_analyse(slug, Path(cfg["LAB_UNPROCESSED_DIR"]), "upload.unprocessed")


@upload_bp.route("/processed/<slug>/analyse")
def processed_analyse(slug: str):
    _require_safe_slug(slug)
    cfg = _cfg()
    return _serve_analyse(slug, Path(cfg["LAB_PROCESSED_DIR"]), "upload.processed")


@upload_bp.route("/locked/<slug>/analyse")
def locked_analyse(slug: str):
    _require_safe_slug(slug)
    cfg = _cfg()
    return _serve_analyse(slug, Path(cfg["LAB_LOCKED_DIR"]), "upload.locked")


@upload_bp.route("/<slug>/status", methods=["GET"])
def processing_status(slug: str):
    _require_safe_slug(slug)
    cfg = _cfg()
    slug_dir = Path(cfg["LAB_UNPROCESSED_DIR"]) / slug
    if not slug_dir.exists() or not slug_dir.is_dir():
        return jsonify({"id": slug, "stage": "preparing", "message": "Preparing", "done": False, "error": None})

    try:
        status_payload = storage_service.read_processing_status(slug_dir) or {}
    except FileNotFoundError:
        return jsonify({"id": slug, "stage": "preparing", "message": "Preparing", "done": False, "error": None})
    except Exception as exc:  # pragma: no cover - defensive guard
        return jsonify({"error": str(exc), "done": False, "stage": "queued"})

    if not status_payload:
        status_payload = {"slug": slug, "stage": "queued", "message": "Queued", "done": False, "error": None}

    stage = (status_payload.get("stage") or "queued").lower()
    if stage == "done":
        stage = "complete"
    done = bool(status_payload.get("done")) or stage == "complete"
    message = status_payload.get("message") or "Queued"
    error = status_payload.get("error")

    return jsonify({"id": slug, "stage": stage, "message": message, "done": done, "error": error})


def _constraints() -> dict[str, str]:
    cfg = _cfg()
    max_mb = int(cfg.get("MAX_CONTENT_LENGTH", 0) / (1024 * 1024)) if cfg.get("MAX_CONTENT_LENGTH") else None
    return {
        "long_edge": str(cfg["REQUIRED_LONG_EDGE_PX"]),
        "dpi": str(cfg["REQUIRED_DPI"]),
        "formats": ", ".join(sorted(cfg["ALLOWED_EXTENSIONS"])),
        "max_mb": str(max_mb) if max_mb else "unlimited",
    }


def _format_uploaded_date(iso_str: str | None) -> str | None:
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        local_dt = dt.astimezone()
        return f"{local_dt.day} {local_dt.strftime('%b %Y')}"
    except Exception:
        return None


def _format_print_sizes(print_info: dict | None) -> str | None:
    if not print_info:
        return None
    if isinstance(print_info, str):
        cleaned = print_info.strip()
        if cleaned.lower().startswith("max print size"):
            cleaned = cleaned.split(":", 1)[-1].strip()
        return cleaned or None
    inches = print_info.get("inches") or {}
    cm = print_info.get("cm") or {}
    parts: list[str] = []
    a_label = print_info.get("a_series")
    if a_label:
        parts.append(a_label.upper())
    if inches.get("width") and inches.get("height"):
        parts.append(f"{inches['width']}×{inches['height']} in")
    if cm.get("width") and cm.get("height"):
        parts.append(f"{cm['width']}×{cm['height']} cm")
    if not parts:
        return None
    return " · ".join(parts)


def _update_processing_status(slug_dir: Path, slug: str, *, stage: str, message: str, done: bool, percent: int | None = None, error: str | None = None) -> None:
    if stage not in storage_service.PROCESSING_ALLOWED_STAGES:
        raise ValueError(f"Invalid processing stage: {stage}")
    existing = storage_service.read_processing_status(slug_dir) or {}
    started_at = existing.get("started_at") or datetime.now(timezone.utc).isoformat()
    payload = {
        "slug": slug,
        "stage": stage,
        "message": message,
        "done": done,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "started_at": started_at,
        "error": error,
    }
    if percent is not None:
        payload["percent"] = percent
    
    # Get SKU from metadata if available to use for filename prefix
    sku = None
    meta_path = slug_dir / storage_service.META_NAME
    if meta_path.exists():
        meta_doc = _read_json_or_none(meta_path)
        if isinstance(meta_doc, dict):
            sku = str(meta_doc.get("sku") or meta_doc.get("artwork_id") or "").strip() or None
    
    storage_service.store_processing_status(slug_dir, payload, sku=sku)
