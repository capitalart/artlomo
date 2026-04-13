from __future__ import annotations

import json
import logging
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Set
from math import ceil

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for,
)

from application.common.utilities.slug_sku import slugify
from PIL import Image
from application.mockups.catalog.models import MockupBase
from ...config import (
    DEFAULT_MOCKUP_ASPECT,
    DEFAULT_MOCKUP_CATEGORY,
    STANDARD_MOCKUP_ASPECT_RATIOS,
    MockupBaseGenerationCatalog,
)
from ...artwork_index import resolve_artwork
from ...errors import IndexLookupError, IoError, ValidationError
from ..validators import validate_png_bytes
from ..readers import read_mockup_slots
from ..services import CatalogAdminService, ManualMockupService


logger = logging.getLogger(__name__)
from ..preview import PreviewService
from application.utils.csrf import get_csrf_token, require_csrf_or_400

mockups_admin_bp = Blueprint(
    "mockups_admin",
    __name__,
    template_folder="../ui/templates",
    static_folder="../ui/static",
)

MAX_UPLOAD_BATCH = 25
BASE_STATUS_LABELS = {
    "missing_coordinates": "Missing coordinates",
    "needs_regeneration": "Needs regeneration",
    "uploaded": "Missing coordinates",
    "coordinates_ready": "Live ready",
    "invalid": "Invalid",
    "disabled": "Staged (not live)",
    "in_use": "Live (in use)",
}

PER_PAGE_CHOICES = [25, 50, 75, 100, 150, 200, 250]


@mockups_admin_bp.route("/aspects", methods=["GET", "POST"])  # type: ignore[misc]
def aspect_manager():
    svc = _catalog_service()
    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            return resp
        action = (request.form.get("action") or "").strip()
        aspect_raw = (request.form.get("aspect") or "").strip()
        try:
            if action == "create":
                created = svc.create_aspect(aspect_raw)
                flash(f"Created aspect: {created}", "success")
            elif action == "ensure_standard":
                for aspect in STANDARD_MOCKUP_ASPECT_RATIOS:
                    svc.create_aspect(str(aspect))
                flash("Ensured standard aspects.", "success")
            elif action == "delete":
                deleted = svc.delete_aspect(aspect_raw)
                flash(f"Deleted aspect: {deleted}", "success")
            else:
                flash("Unknown action", "danger")
        except ValidationError as exc:
            flash(str(exc), "danger")
        return redirect(url_for("mockups_admin.aspect_manager"))

    aspects = svc.list_physical_aspects()
    categories = svc.list_physical_categories()
    return render_template(
        "mockups/aspect_manager.html",
        aspects=aspects,
        categories=categories,
        standard_aspects=list(STANDARD_MOCKUP_ASPECT_RATIOS),
        base_root=str(getattr(svc, "base_root", "")),
        csrf_token=get_csrf_token(),
    )


@mockups_admin_bp.route("/categories-manager", methods=["GET", "POST"])  # type: ignore[misc]
def category_manager():
    svc = _catalog_service()
    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            return resp
        action = (request.form.get("action") or "").strip()
        category_raw = (request.form.get("category") or "").strip()
        try:
            if action == "create":
                created = svc.create_category_across_aspects(category_raw)
                flash(f"Created category: {created}", "success")
            elif action == "delete":
                deleted = svc.delete_category_across_aspects(category_raw)
                flash(f"Deleted category: {deleted}", "success")
            else:
                flash("Unknown action", "danger")
        except ValidationError as exc:
            flash(str(exc), "danger")
        return redirect(url_for("mockups_admin.category_manager"))

    aspects = svc.list_physical_aspects()
    categories = svc.list_physical_categories()
    known_categories = svc.list_known_categories()
    return render_template(
        "mockups/category_manager.html",
        aspects=aspects,
        categories=categories,
        known_categories=known_categories,
        base_root=str(getattr(svc, "base_root", "")),
        csrf_token=get_csrf_token(),
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _path_from_config(key: str) -> Path | None:
    value = current_app.config.get(key)
    if value is None:
        return None
    return value if isinstance(value, Path) else Path(value)


def _catalog_service() -> CatalogAdminService:
    catalog_path = _path_from_config("MOCKUP_CATALOG_PATH")
    return CatalogAdminService(catalog_path=catalog_path)


def _manual_service() -> ManualMockupService:
    catalog_path = _path_from_config("MOCKUP_CATALOG_PATH")
    master_index_path = _master_index_path()
    processed_root = _processed_root()
    return ManualMockupService(
        catalog_path=catalog_path,
        master_index_path=master_index_path,
        processed_root=processed_root,
    )

def _preview_service() -> PreviewService:
    catalog_path = _path_from_config("MOCKUP_CATALOG_PATH")
    preview_art_root = _path_from_config("MOCKUP_PREVIEW_ART_ROOT")
    preview_cache_root = _path_from_config("MOCKUP_PREVIEW_CACHE_ROOT")
    return PreviewService(
        catalog_path=catalog_path,
        preview_art_root=preview_art_root,
        cache_root=preview_cache_root,
    )


def _master_index_path() -> Path | None:
    return _path_from_config("MOCKUP_MASTER_INDEX_PATH") or _path_from_config("ARTWORKS_INDEX_PATH")


def _processed_root() -> Path | None:
    return _path_from_config("MOCKUP_PROCESSED_ROOT") or _path_from_config("LAB_PROCESSED_DIR")


def _category_options(svc: CatalogAdminService) -> List[str]:
    return svc.list_known_categories()


def _aspect_options(svc: CatalogAdminService) -> List[str]:
    raw_values = [str(value or "").strip() for value in svc.list_known_aspects()]
    allowed = list(dict.fromkeys(list(MockupBaseGenerationCatalog.ASPECT_RATIOS) + list(STANDARD_MOCKUP_ASPECT_RATIOS)))
    allowed_set = set(allowed)
    cleaned = [value for value in raw_values if value in allowed_set]
    if not cleaned:
        return allowed
    ordered = [value for value in allowed if value in cleaned]
    extras = sorted(value for value in cleaned if value not in ordered)
    return ordered + extras




def _log_upload(event: str, **extra) -> None:
    try:
        enabled = current_app.debug or current_app.config.get("MOCKUP_UPLOAD_DEBUG")
    except Exception:  # pylint: disable=broad-except
        enabled = False
    if enabled:
        current_app.logger.info("[mockups-upload] %s | %s", event, extra)


def _dedupe_slug(base_slug: str, reserved: Set[str], planned: Set[str]) -> str:
    if base_slug not in reserved and base_slug not in planned:
        return base_slug
    suffix = 2
    while True:
        candidate = f"{base_slug}-{suffix}"
        if candidate not in reserved and candidate not in planned:
            return candidate
        suffix += 1


def _coerce_dam_points_to_zones(payload: dict) -> dict:
    """Normalize DAM point payloads to zones so CatalogAdminService can validate them."""
    points = payload.get("points")
    if not isinstance(points, list) or len(points) != 4:
        return payload

    normalized_points = []
    for point in points:
        if not isinstance(point, dict):
            return payload
        try:
            x_val = float(point.get("x"))
            y_val = float(point.get("y"))
        except (TypeError, ValueError):
            return payload
        normalized_points.append({"x": x_val, "y": y_val})

    normalized = dict(payload)
    normalized["zones"] = [{"points": normalized_points}]
    return normalized


def _extract_upload_coordinates_payload(coords_upload_bytes: bytes | None) -> tuple[dict | bytes | str | None, dict[str, str]]:
    """Extract coordinates payload from direct JSON or DAM export sidecar JSON."""
    if not coords_upload_bytes:
        return None, {}

    try:
        parsed = json.loads(coords_upload_bytes.decode("utf-8"))
    except Exception:
        return coords_upload_bytes, {}

    if not isinstance(parsed, dict):
        return parsed, {}

    sidecar_meta: dict[str, str] = {}

    if str(parsed.get("schema_version") or "").strip() == "2.0" and isinstance(parsed.get("coordinates"), dict):
        coords_node = parsed.get("coordinates") or {}
        coords_data = coords_node.get("data") if isinstance(coords_node, dict) else None
        if isinstance(coords_data, dict):
            payload = _coerce_dam_points_to_zones(coords_data)
            aspect_ratio = str(parsed.get("aspect_ratio") or "").strip()
            category = str(parsed.get("category") or "").strip()
            if aspect_ratio:
                sidecar_meta["aspect_ratio"] = aspect_ratio
            if category:
                sidecar_meta["category"] = category
            return payload, sidecar_meta

    return _coerce_dam_points_to_zones(parsed), sidecar_meta


def _base_status_options() -> List[tuple[str, str]]:
    return [
        ("live_catalog", "Live Catalog"),
        ("staging_queue", "Staging Queue"),
        ("missing_coordinates", "Missing coordinates"),
        ("needs_regeneration", "Needs regeneration"),
        ("coordinates_ready", "Live ready"),
        ("in_use", "Live (in use)"),
        ("disabled", "Staged (not live)"),
        ("invalid", "Invalid"),
        ("uploaded", "Uploaded (legacy)"),
        ("all", "All"),
    ]


def _build_page_links(current_page: int, total_pages: int) -> List[int | None]:
    if total_pages <= 7:
        return list(range(1, total_pages + 1))

    links: List[int | None] = [1]
    window_start = max(2, current_page - 1)
    window_end = min(total_pages - 1, current_page + 1)

    if window_start > 2:
        links.append(None)

    links.extend(range(window_start, window_end + 1))

    if window_end < total_pages - 1:
        links.append(None)

    links.append(total_pages)
    return links


def _fallback_load_bases_from_catalog(svc: CatalogAdminService) -> tuple[List[MockupBase], int]:
    doc = svc._load_catalog_json()
    raw_entries = doc.get("bases") if isinstance(doc, dict) else []
    if not isinstance(raw_entries, list):
        return [], 0

    deduped_by_slug: dict[str, dict] = {}
    duplicates_skipped = 0
    for raw in raw_entries:
        if not isinstance(raw, dict):
            continue
        slug = str(raw.get("slug") or "").strip()
        base_id = str(raw.get("id") or "").strip()
        if not slug or not base_id:
            continue
        existing = deduped_by_slug.get(slug)
        if existing is not None:
            duplicates_skipped += 1
            existing_updated = str(existing.get("updated_at") or "")
            current_updated = str(raw.get("updated_at") or "")
            if current_updated >= existing_updated:
                deduped_by_slug[slug] = raw
            continue
        deduped_by_slug[slug] = raw

    base_dir = svc.catalog_path.parent
    fallback_bases: List[MockupBase] = []
    for raw in deduped_by_slug.values():
        try:
            base_image_val = str(raw.get("base_image_path") or raw.get("base_image") or "").strip()
            if not base_image_val:
                continue
            base_image_path = Path(base_image_val)
            if not base_image_path.is_absolute():
                base_image_path = (base_dir / base_image_path).resolve()

            coords_val = str(raw.get("coordinates_path") or raw.get("coordinates") or "").strip()
            coords_path = None
            if coords_val:
                candidate = Path(coords_val)
                coords_path = candidate if candidate.is_absolute() else (base_dir / candidate).resolve()
                if not coords_path.exists():
                    coords_path = None

            status = str(raw.get("status") or "missing_coordinates").strip() or "missing_coordinates"
            if not base_image_path.exists():
                status = "missing_coordinates"
            elif coords_path is None and status in {"coordinates_ready", "in_use", "disabled"}:
                status = "needs_regeneration"

            fallback_bases.append(
                MockupBase(
                    id=str(raw.get("id") or "").strip(),
                    slug=str(raw.get("slug") or "").strip(),
                    original_filename=str(raw.get("original_filename") or Path(base_image_path).name).strip(),
                    base_image=base_image_path,
                    coordinates=coords_path,
                    category=str(raw.get("category") or "uncategorised").strip() or "uncategorised",
                    aspect_ratio=str(raw.get("aspect_ratio") or "").strip() or None,
                    status=status,
                    region_count=raw.get("region_count") if isinstance(raw.get("region_count"), int) else None,
                    created_at=str(raw.get("created_at") or "").strip(),
                    updated_at=str(raw.get("updated_at") or "").strip(),
                    aspect_source=str(raw.get("aspect_source") or "").strip() or None,
                    last_coordinated_at=str(raw.get("last_coordinated_at") or "").strip() or None,
                    coordinate_type=str(raw.get("coordinate_type") or "").strip() or None,
                )
            )
        except Exception:
            continue

    return fallback_bases, duplicates_skipped


def _load_bases_catalog_resilient(svc: CatalogAdminService) -> tuple[List[MockupBase], str | None]:
    try:
        return svc.load_bases(), None
    except ValidationError as exc:
        if "Duplicate base slug:" not in str(exc) and "Duplicate base id:" not in str(exc):
            raise
        fallback_bases, duplicates_skipped = _fallback_load_bases_from_catalog(svc)
        if not fallback_bases:
            raise
        warning = f"Recovered from catalog duplicates and skipped {duplicates_skipped} duplicate base entr{'y' if duplicates_skipped == 1 else 'ies'}."
        return fallback_bases, warning

def _is_size_chart(category: str | None) -> bool:
    return (category or "").strip().lower() == "size-chart"


def _coords_path_for_base(base) -> Path:
    if getattr(base, "coordinates", None):
        return base.coordinates
    return base.base_image.with_suffix(".json")


def _thumb_candidates_for_base(base) -> List[Path]:
    base_path = base.base_image
    aspect = getattr(base, "aspect_ratio", None) or DEFAULT_MOCKUP_ASPECT
    category_folder = base_path.parent.name

    id_num = None
    try:
        if "-MU-" in base.slug:
            _, suffix = base.slug.rsplit("-MU-", 1)
            id_num = int(suffix)
    except Exception:
        id_num = None

    candidates: List[Path] = []
    if id_num is not None:
        candidates.append(base_path.with_name(f"{aspect}-THUMB-{category_folder}-{id_num}.jpg"))

    candidates.append(base_path.with_name(f"{base.slug}-THUMB.jpg"))

    rest = base.slug
    prefix = f"{aspect}-"
    if rest.startswith(prefix):
        rest = rest[len(prefix):]
    candidates.append(base_path.with_name(f"{aspect}-THUMB-{rest}.jpg"))

    try:
        if "-MU-" in base.slug:
            pre, suf = base.slug.rsplit("-MU-", 1)
            candidates.append(base_path.with_name(f"{pre}-MU-THUMB-{suf}.jpg"))
    except Exception:
        pass

    return candidates


def _find_base_by_slug_resilient(slug: str) -> MockupBase:
    svc = _catalog_service()
    try:
        bases_catalog, _warning = _load_bases_catalog_resilient(svc)
    except ValidationError as exc:
        abort(404, description=str(exc))

    for base in bases_catalog:
        if base.slug == slug:
            return base
    abort(404)


def _dynamic_thumb_response(image_path: Path):
    image_obj = Image.open(image_path)
    image_obj.load()
    if image_obj.mode not in {"RGB", "L"}:
        image_obj = image_obj.convert("RGB")
    elif image_obj.mode == "L":
        image_obj = image_obj.convert("RGB")

    image_obj.thumbnail((512, 512))
    buffer = BytesIO()
    image_obj.save(buffer, format="JPEG", quality=88, optimize=True)
    buffer.seek(0)
    return send_file(buffer, mimetype="image/jpeg")


def _serialize_base_entry(base, *, preview_svc: PreviewService | None = None, preview_cache: Dict[str, List[dict]] | None = None) -> dict:
    cache = preview_cache if preview_cache is not None else {}
    aspect = base.aspect_ratio or DEFAULT_MOCKUP_ASPECT
    preview_records: List[dict] = []
    if preview_svc:
        if aspect not in cache:
            cache[aspect] = preview_svc.list_preview_artwork_records(aspect)
        preview_records = cache[aspect]

    raw_status = base.status
    status = "missing_coordinates" if raw_status == "uploaded" else raw_status
    aspect_source = getattr(base, "aspect_source", None) or ("region" if _is_size_chart(base.category) else "auto")
    size_chart = _is_size_chart(base.category)
    if aspect_source == "manual":
        aspect_source_label = "Manual override"
    elif aspect_source == "region":
        aspect_source_label = "Region 1 (size chart)" if size_chart else "Region 1"
    elif aspect_source == "upload":
        aspect_source_label = "Uploaded file"
    else:
        aspect_source_label = "Auto"

    coords_path = _coords_path_for_base(base)
    coords_ok = False
    try:
        coords_ok = coords_path.exists()
    except Exception:
        coords_ok = False

    thumb_ok = False
    try:
        thumb_ok = any(candidate.exists() for candidate in _thumb_candidates_for_base(base))
    except Exception:
        thumb_ok = False

    trio_complete = bool(coords_ok and thumb_ok)
    is_live = status in {"coordinates_ready", "in_use"}

    return {
        "id": base.id,
        "slug": base.slug,
        "category": base.category,
        "aspect_ratio": aspect,
        "aspect_source": aspect_source,
        "aspect_source_label": aspect_source_label,
        "status": status,
        "raw_status": raw_status,
        "original_filename": base.original_filename,
        "created_at": base.created_at,
        "updated_at": base.updated_at,
        "last_coordinated_at": getattr(base, "last_coordinated_at", None),
        "coordinate_type": getattr(base, "coordinate_type", None),
        "region_count": base.region_count,
        "coordinates_present": base.coordinates is not None,
        "coordinates_path": str(base.coordinates) if base.coordinates else None,
        "coords_exists": coords_ok,
        "thumb_exists": thumb_ok,
        "trio_complete": trio_complete,
        "is_incomplete": (not trio_complete),
        "is_live": is_live,
        "image_url": url_for("mockups_admin.base_image", slug=base.slug),
        "preview_artworks": [item.get("filename", "") for item in preview_records],
        "preview_artwork_options": preview_records,
        "is_size_chart": size_chart,
        "thumb_url": url_for("mockups_admin.base_thumb", slug=base.slug),
    }


# ---------------------------------------------------------------------------
# Mockup bases
@mockups_admin_bp.route("/bases", methods=["GET"])
def bases():
    svc = _catalog_service()
    preview_svc = _preview_service()

    try:
        svc.sync_orphan_bases_from_filesystem()
    except ValidationError:
        pass

    status_filter = request.args.get("status") or "live_catalog"
    category_filter = request.args.get("category") or ""
    aspect_filter = request.args.get("aspect") or ""
    sort_order = request.args.get("sort") or "newest"
    if sort_order not in ("newest", "oldest"):
        sort_order = "newest"
    page = request.args.get("page", type=int) or 1
    per_page = request.args.get("per_page", type=int) or 25
    if per_page not in PER_PAGE_CHOICES:
        per_page = PER_PAGE_CHOICES[0]
    if page < 1:
        page = 1

    try:
        bases_catalog, fallback_warning = _load_bases_catalog_resilient(svc)
        if fallback_warning:
            flash(fallback_warning, "warning")
    except ValidationError as exc:
        flash(str(exc), "danger")
        empty_filters = {
            "status": status_filter,
            "category": category_filter,
            "aspect": aspect_filter,
            "sort": sort_order,
            "per_page": per_page,
            "page": 1,
            "pages": 1,
            "page_links": [1],
            "total": 0,
            "per_page_choices": PER_PAGE_CHOICES,
            "search": "",
        }
        categories = _category_options(svc)
        category_counts = {cat: 0 for cat in categories}
        return render_template(
            "mockups/bases.html",
            bases=[],
            categories=categories,
            category_counts=category_counts,
            aspects=_aspect_options(svc),
            filters=empty_filters,
            status_options=_base_status_options(),
            status_labels=BASE_STATUS_LABELS,
            csrf_token=get_csrf_token(),
            total_live_count=0,
            total_staged_count=0,
        ), 400

    categories = _category_options(svc)
    category_counts = svc.physical_category_counts()
    aspects = _aspect_options(svc)

    preview_map: Dict[str, List[dict]] = {}
    entries = []
    total_live_count = 0
    total_staged_count = 0
    for base in bases_catalog:
        entry = _serialize_base_entry(base, preview_svc=preview_svc, preview_cache=preview_map)
        # Global counts are computed before any filter is applied.
        if entry["status"] in {"coordinates_ready", "in_use"}:
            total_live_count += 1
        elif entry["status"] == "disabled":
            total_staged_count += 1
        if category_filter and entry["category"] != category_filter:
            continue
        if aspect_filter and entry["aspect_ratio"] != aspect_filter:
            continue

        if status_filter != "all":
            if status_filter == "live_catalog":
                if entry["status"] not in {"coordinates_ready", "in_use"}:
                    continue
            elif status_filter == "staging_queue":
                if entry["status"] != "disabled":
                    continue
            elif status_filter == "missing_coordinates":
                if entry["status"] not in {"missing_coordinates", "needs_regeneration"}:
                    continue
            elif status_filter == "uploaded":
                if entry["raw_status"] != "uploaded":
                    continue
            elif entry["status"] != status_filter:
                continue

        entries.append(entry)

    entries.sort(key=lambda e: e.get("created_at") or "", reverse=(sort_order == "newest"))

    _log_upload(
        "bases_view",
        count=len(entries),
        status_filter=status_filter,
        category_filter=category_filter,
        aspect_filter=aspect_filter,
    )

    total = len(entries)
    pages = max(1, ceil(total / per_page)) if per_page else 1
    if page > pages:
        page = pages
    start = (page - 1) * per_page
    end = start + per_page
    entries = entries[start:end]

    filters = {
        "status": status_filter,
        "category": category_filter,
        "aspect": aspect_filter,
        "sort": sort_order,
        "per_page": per_page,
        "page": page,
        "pages": pages,
        "page_links": _build_page_links(page, pages),
        "total": total,
        "per_page_choices": PER_PAGE_CHOICES,
    }
    return render_template(
        "mockups/bases.html",
        bases=entries,
        categories=categories,
        category_counts=category_counts,
        aspects=aspects,
        filters=filters,
        status_options=_base_status_options(),
        status_labels=BASE_STATUS_LABELS,
        csrf_token=get_csrf_token(),
        total_live_count=total_live_count,
        total_staged_count=total_staged_count,
    )


# ---------------------------------------------------------------------------
# Base assets
# ---------------------------------------------------------------------------
@mockups_admin_bp.get("/bases/<slug>/image")
def base_image(slug: str):
    base = _find_base_by_slug_resilient(slug)

    image_path = base.base_image
    try:
        if not image_path.exists():
            abort(404)
    except Exception:
        abort(404)

    return send_file(image_path, mimetype="image/png")


@mockups_admin_bp.get("/bases/<slug>/thumb")
def base_thumb(slug: str):
    base = _find_base_by_slug_resilient(slug)

    base_path = base.base_image
    try:
        for candidate in _thumb_candidates_for_base(base):
            if candidate.exists():
                return send_file(candidate, mimetype="image/jpeg")
    except Exception:
        pass

    try:
        if base_path.exists():
            return _dynamic_thumb_response(base_path)
    except Exception:
        pass

    abort(404)


@mockups_admin_bp.post("/bases/sanitize-sync")  # type: ignore[misc]
def sanitize_sync_bases():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    try:
        status = svc.start_sanitize_sync_async()
        return {"status": "ok", "detail": status}, 202
    except ValidationError as exc:
        status_code = 409 if "already running" in str(exc).lower() else 400
        return {"status": "error", "message": str(exc)}, status_code


@mockups_admin_bp.get("/bases/sanitize-sync/status")  # type: ignore[misc]
def sanitize_sync_status():
    svc = _catalog_service()
    return {"status": "ok", "detail": svc.get_sanitize_sync_status()}


@mockups_admin_bp.post("/bases/generate-thumbs")  # type: ignore[misc]
def generate_base_thumbs():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    try:
        summary = svc.generate_missing_base_thumbs()
        return {"status": "ok", "summary": summary}
    except ValidationError as exc:
        return {"status": "error", "message": str(exc)}, 400


# ---------------------------------------------------------------------------
# Batch operations for mockup bases
# ---------------------------------------------------------------------------
@mockups_admin_bp.post("/batch/delete")  # type: ignore[misc]
def batch_delete():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    payload = request.get_json(silent=True) or {}
    ids = payload.get("mockup_ids") or []
    try:
        removed = svc.delete_bases(ids)
        return {"status": "ok", "removed": removed}
    except ValidationError as exc:
        return {"status": "error", "message": str(exc)}, 400


@mockups_admin_bp.post("/batch/move")  # type: ignore[misc]
def batch_move():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    payload = request.get_json(silent=True) or {}
    ids = payload.get("mockup_ids") or []
    new_category = payload.get("category") or ""
    try:
        updated = svc.move_bases_to_category(ids, new_category)
        return {"status": "ok", "updated": updated, "category": slugify(new_category)}
    except ValidationError as exc:
        return {"status": "error", "message": str(exc)}, 400


@mockups_admin_bp.post("/batch/change-aspect")  # type: ignore[misc]
def batch_change_aspect():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    payload = request.get_json(silent=True) or {}
    ids = payload.get("mockup_ids") or []
    new_aspect = payload.get("aspect_ratio") or ""
    try:
        updated = svc.change_bases_aspect(ids, new_aspect)
        return {"status": "ok", "updated": updated, "aspect_ratio": new_aspect}
    except ValidationError as exc:
        return {"status": "error", "message": str(exc)}, 400


@mockups_admin_bp.post("/batch/generate-coordinates")  # type: ignore[misc]
def batch_generate_coordinates():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    payload = request.get_json(silent=True) or {}
    ids = payload.get("mockup_ids") or []
    try:
        generated = svc.generate_coordinates_for_bases(ids, force=True)
        return {"status": "ok", "generated": generated, "count": len(generated)}
    except ValidationError as exc:
        return {"status": "error", "message": str(exc)}, 400


# ---------------------------------------------------------------------------
# Per-base operations and bulk updates
# ---------------------------------------------------------------------------
@mockups_admin_bp.post("/bases/<mockup_id>/delete")  # type: ignore[misc]
def delete_base(mockup_id: str):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    try:
        removed = svc.delete_base(mockup_id)
        if not removed:
            return {"status": "error", "message": "Base not found"}, 404
        return {"status": "ok", "removed": removed[0]}
    except ValidationError as exc:
        return {"status": "error", "message": str(exc)}, 400


@mockups_admin_bp.post("/bases/<mockup_id>/regenerate")  # type: ignore[misc]
def regenerate_base(mockup_id: str):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    preview_svc = _preview_service()
    try:
        base = svc.regenerate_base(mockup_id)
        entry = _serialize_base_entry(base, preview_svc=preview_svc)
        return {"status": "ok", "base": entry}
    except ValidationError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        return {"status": "error", "message": str(exc)}, status_code


@mockups_admin_bp.post("/generate-async")  # type: ignore[misc]
def generate_coordinates_async():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    payload = request.get_json(silent=True) or {}
    ids = payload.get("mockup_ids") or []
    force = bool(payload.get("force", True))
    svc = _manual_service()
    try:
        status = svc.start_bulk_generation_async(ids, force=force)
        return {"status": "ok", "message": "Task Started", "detail": status}, 202
    except ValidationError as exc:
        status_code = 409 if "already running" in str(exc).lower() else 400
        return {"status": "error", "message": str(exc)}, status_code


@mockups_admin_bp.get("/generation-progress")  # type: ignore[misc]
def generation_progress():
    svc = _manual_service()
    status = svc.get_bulk_generation_status()
    return {"status": "ok", "detail": status}


@mockups_admin_bp.get("/generation-status")  # type: ignore[misc]
def generation_status():
    svc = _manual_service()
    status = svc.get_bulk_generation_status()
    return {"status": "ok", "detail": status}


@mockups_admin_bp.get("/get_generation_progress")  # type: ignore[misc]
def get_generation_progress():
    svc = _manual_service()
    status = svc.get_bulk_generation_status()
    return {"status": "ok", "detail": status}


@mockups_admin_bp.post("/bases/<mockup_id>/category")  # type: ignore[misc]
def update_base_category(mockup_id: str):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    preview_svc = _preview_service()
    payload = request.get_json(silent=True) or {}
    new_category = (payload.get("category") or "").strip()
    try:
        base = svc.update_base_category(mockup_id, category=new_category)
        entry = _serialize_base_entry(base, preview_svc=preview_svc)
        return {"status": "ok", "base": entry}
    except ValidationError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        return {"status": "error", "message": str(exc)}, status_code


@mockups_admin_bp.post("/bases/<mockup_id>/aspect")  # type: ignore[misc]
def override_base_aspect(mockup_id: str):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    preview_svc = _preview_service()
    payload = request.get_json(silent=True) or {}
    aspect = (payload.get("aspect_ratio") or "").strip()
    try:
        base = svc.override_base_aspect(mockup_id, aspect_ratio=aspect)
        entry = _serialize_base_entry(base, preview_svc=preview_svc)
        return {"status": "ok", "base": entry}
    except ValidationError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        return {"status": "error", "message": str(exc)}, status_code


@mockups_admin_bp.post("/bases/<mockup_id>/publication")  # type: ignore[misc]
def update_base_publication(mockup_id: str):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    preview_svc = _preview_service()
    payload = request.get_json(silent=True) or {}
    live_raw = payload.get("live")
    if not isinstance(live_raw, bool):
        return {"status": "error", "message": "live must be a boolean"}, 400

    try:
        base = svc.set_base_live_state(mockup_id, live=live_raw)
        entry = _serialize_base_entry(base, preview_svc=preview_svc)
        return {"status": "ok", "base": entry}
    except ValidationError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        return {"status": "error", "message": str(exc)}, status_code


@mockups_admin_bp.post("/bases/bulk/update")  # type: ignore[misc]
def bulk_update_bases():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    svc = _catalog_service()
    preview_svc = _preview_service()
    payload = request.get_json(silent=True) or {}
    ids = payload.get("mockup_ids") or []
    action = (payload.get("action") or "").strip()

    try:
        updated_ids: List[str] = []
        if action == "delete":
            removed = svc.delete_bases(ids)
            return {"status": "ok", "removed": removed}
        if action == "regenerate":
            regenerated = svc.generate_coordinates_for_bases(ids, force=True)
            updated_ids = [pair[0] for pair in regenerated]
        elif action == "category":
            category = (payload.get("category") or "").strip()
            svc.move_bases_to_category(ids, category)
            updated_ids = ids
        elif action == "aspect":
            aspect = (payload.get("aspect_ratio") or "").strip()
            svc.change_bases_aspect(ids, aspect)
            updated_ids = ids
        else:
            raise ValidationError("Invalid action")

        if not updated_ids:
            return {"status": "ok", "updated": []}

        bases_by_id = {b.id: b for b in svc.load_bases() if b.id in set(updated_ids)}
        entries = [_serialize_base_entry(bases_by_id[bid], preview_svc=preview_svc) for bid in updated_ids if bid in bases_by_id]
        return {"status": "ok", "updated": updated_ids, "bases": entries}
    except ValidationError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        return {"status": "error", "message": str(exc)}, status_code


# ---------------------------------------------------------------------------
# Upload mockup bases
# ---------------------------------------------------------------------------
@mockups_admin_bp.route("/bases/upload", methods=["GET", "POST"])
def upload_bases():
    svc = _catalog_service()

    form_data = {
        "slug": request.form.get("slug", ""),
        "category": request.form.get("category", ""),
        "aspect_ratio": request.form.get("aspect_ratio", ""),
    }

    if request.method == "POST":
        wants_json = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.accept_mimetypes.best == "application/json"
        _log_upload(
            "upload_bases_post",
            path=request.path,
            endpoint=request.endpoint,
            file_keys=list(request.files.keys()),
            file_count=len(request.files),
        )

        base_files = [f for f in request.files.getlist("base_images") if f and f.filename]
        if not base_files:
            legacy_single = request.files.get("base_image")
            if legacy_single and legacy_single.filename:
                base_files = [legacy_single]
        coords_upload = request.files.get("coords_json")

        if wants_json and len(base_files) > 1:
            return jsonify({"status": "error", "message": "Upload expects one base PNG per request."}), 400

        if coords_upload and coords_upload.filename and len(base_files) != 1:
            message = "Coordinate JSON can only be uploaded when exactly one base PNG is provided."
            flash(message, "danger")
            if wants_json:
                return jsonify({"status": "error", "message": message}), 400
            return render_template(
                "mockups/upload_bases.html",
                categories=_category_options(svc),
                category_counts=svc.physical_category_counts(),
                aspects=_aspect_options(svc),
                form_data=form_data,
            ), 400

        if not base_files:
            flash("At least one base PNG is required.", "danger")
            if wants_json:
                return jsonify({"status": "error", "message": "At least one base PNG is required."}), 400
            return render_template(
                "mockups/upload_bases.html",
                categories=_category_options(svc),
                category_counts=svc.physical_category_counts(),
                aspects=_aspect_options(svc),
                form_data=form_data,
            ), 400

        if len(base_files) > MAX_UPLOAD_BATCH:
            flash(f"Too many files. Maximum {MAX_UPLOAD_BATCH} per batch.", "danger")
            if wants_json:
                return jsonify({"status": "error", "message": f"Too many files. Maximum {MAX_UPLOAD_BATCH} per batch."}), 400
            return render_template(
                "mockups/upload_bases.html",
                categories=_category_options(svc),
                category_counts=svc.physical_category_counts(),
                aspects=_aspect_options(svc),
                form_data=form_data,
            ), 400

        try:
            existing_slugs = {tpl.slug for tpl in svc.load_catalog()}
            existing_base_slugs = {b.slug for b in svc.load_bases()}
        except ValidationError as exc:
            flash(str(exc), "danger")
            if wants_json:
                return jsonify({"status": "error", "message": str(exc)}), 400
            return render_template(
                "mockups/upload_bases.html",
                categories=_category_options(svc),
                category_counts=svc.physical_category_counts(),
                aspects=_aspect_options(svc),
                form_data=form_data,
            ), 400

        reserved_slugs = set(existing_slugs) | set(existing_base_slugs)
        planned = []
        planned_slugs: Set[str] = set()
        errors: List[str] = []
        coords_upload_bytes = None
        coords_payload_value = None
        sidecar_meta: dict[str, str] = {}
        if coords_upload and coords_upload.filename:
            coords_upload_bytes = coords_upload.read()
            coords_payload_value, sidecar_meta = _extract_upload_coordinates_payload(coords_upload_bytes)

        category_raw = (form_data["category"] or "").strip()
        aspect_raw = (form_data["aspect_ratio"] or "").strip()
        category_value = category_raw or str(sidecar_meta.get("category") or "").strip() or DEFAULT_MOCKUP_CATEGORY
        aspect_value = aspect_raw or str(sidecar_meta.get("aspect_ratio") or "").strip() or DEFAULT_MOCKUP_ASPECT

        for upload in base_files:
            raw_bytes = upload.read()
            try:
                validate_png_bytes(raw_bytes)
            except ValidationError as exc:
                errors.append(f"{upload.filename or 'file'}: {exc}")
                continue

            slug_source = form_data["slug"] if (form_data["slug"] and len(base_files) == 1) else Path(upload.filename or "unknown").stem
            slug_candidate = slugify(slug_source)
            if not slug_candidate:
                errors.append(f"{upload.filename or 'file'}: Slug is required.")
                continue

            unique_slug = _dedupe_slug(slug_candidate, reserved_slugs, planned_slugs)
            planned_slugs.add(unique_slug)
            planned.append({
                "slug": unique_slug,
                "base_bytes": raw_bytes,
                "filename": upload.filename,
                "coords_payload": coords_payload_value if len(base_files) == 1 else None,
            })

        if errors:
            flash("Upload failed: " + "; ".join(errors), "danger")
            if wants_json:
                return jsonify({"status": "error", "message": "Upload failed: " + "; ".join(errors)}), 400
            return render_template(
                "mockups/upload_bases.html",
                categories=_category_options(svc),
                category_counts=svc.physical_category_counts(),
                aspects=_aspect_options(svc),
                form_data=form_data,
            ), 400

        if not planned:
            flash("No valid files to upload.", "danger")
            if wants_json:
                return jsonify({"status": "error", "message": "No valid files to upload."}), 400
            return render_template(
                "mockups/upload_bases.html",
                categories=_category_options(svc),
                category_counts=svc.physical_category_counts(),
                aspects=_aspect_options(svc),
                form_data=form_data,
            ), 400

        added_slugs: List[str] = []
        try:
            for item in planned:
                record = svc.add_base(
                    slug=item["slug"],
                    original_filename=item["filename"],
                    category=category_value,
                    aspect_ratio=aspect_value,
                    base_image_bytes=item["base_bytes"],
                    coords_payload=item.get("coords_payload"),
                )
                added_slugs.append(record.slug)
        except ValidationError as exc:
            flash(str(exc), "danger")
            if wants_json:
                return jsonify({"status": "error", "message": str(exc)}), 400
            return render_template(
                "mockups/upload_bases.html",
                categories=_category_options(svc),
                category_counts=svc.physical_category_counts(),
                aspects=_aspect_options(svc),
                form_data=form_data,
            ), 400

        _log_upload("upload_bases_success", added_slugs=added_slugs, count=len(added_slugs))
        flash(f"Uploaded {len(added_slugs)} mockup base(s).", "success")
        if wants_json:
            return jsonify({"status": "ok", "slugs": added_slugs, "count": len(added_slugs)})
        return redirect(url_for("mockups_admin.bases", status="staging_queue"))

    categories = _category_options(svc)
    aspects = _aspect_options(svc)
    return render_template(
        "mockups/upload_bases.html",
        categories=categories,
        category_counts=svc.physical_category_counts(),
        aspects=aspects,
        form_data=form_data,
    )


@mockups_admin_bp.route("/templates/upload", methods=["GET", "POST"])
def upload_template():
    if request.method == "GET":
        return redirect(url_for("mockups_admin.upload_bases"))
    return upload_bases()


# ---------------------------------------------------------------------------
# Artwork mockup viewer (read-only)
# ---------------------------------------------------------------------------
@mockups_admin_bp.route("/artworks/<sku>/mockups", methods=["GET"])
def artwork_mockups(sku: str):
    master_index_path = _master_index_path()
    processed_root = _processed_root()

    try:
        artwork_dir, assets_path, slug = resolve_artwork(
            sku,
            master_index_path=master_index_path,
            processed_root=processed_root,
        )
        slot_map = read_mockup_slots(
            sku,
            master_index_path=master_index_path,
            processed_root=processed_root,
        )
    except (ValidationError, IndexLookupError, IoError) as exc:
        flash(str(exc), "danger")
        return render_template("mockups/artwork_mockups.html", sku=sku, entries=[], assets_path=None, slug=None, error=str(exc)), 400

    catalog = {tpl.slug: tpl for tpl in _catalog_service().load_catalog()}
    entries = []
    for slot, entry in sorted(slot_map.items(), key=lambda kv: kv[0]):
        template_slug = entry.get("template_slug", "")
        tpl = catalog.get(template_slug) if template_slug else None
        entries.append(
            {
                "slot": slot,
                "template_slug": entry.get("template_slug"),
                "category": tpl.category if tpl else None,
                "aspect_ratio": entry.get("aspect_ratio"),
                "regions": entry.get("regions") or [],
                "thumb_url": url_for("mockups_admin.mockup_thumb", sku=sku, slot_key=slot),
                "updated_at": entry.get("updated_at"),
            }
        )

    return render_template(
        "mockups/artwork_mockups.html",
        sku=sku,
        slug=slug,
        entries=entries,
        assets_path=assets_path,
        error=None,
    )


@mockups_admin_bp.get("/artworks/<sku>/mockups/thumb/<slot_key>")
def mockup_thumb(sku: str, slot_key: str):
    master_index_path = _master_index_path()
    processed_root = _processed_root()

    try:
        artwork_dir, assets_path, _ = resolve_artwork(
            sku,
            master_index_path=master_index_path,
            processed_root=processed_root,
        )
        slots = read_mockup_slots(
            sku,
            master_index_path=master_index_path,
            processed_root=processed_root,
        )
    except (ValidationError, IndexLookupError, IoError):
        abort(404)

    entry = slots.get(slot_key)
    thumb_rel = entry.get("thumb") if isinstance(entry, dict) else None
    if not thumb_rel:
        abort(404)

    thumb_path = (artwork_dir / thumb_rel).resolve()
    try:
        artwork_root = artwork_dir.resolve()
        if not thumb_path.exists():
            abort(404)
        if artwork_root not in thumb_path.parents:
            abort(404)
    except Exception:
        abort(404)

    return send_file(thumb_path, mimetype="image/jpeg")


# ---------------------------------------------------------------------------
# Preview generation and assets
# ---------------------------------------------------------------------------
@mockups_admin_bp.post("/<mockup_id>/preview")  # type: ignore[misc]
def generate_preview(mockup_id: str):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    payload = request.get_json(silent=True) or {}
    artwork_key = (payload.get("preview_artwork") or "").strip() or None
    svc = _preview_service()
    try:
        out_path, generated_at = svc.generate_preview(mockup_id, artwork_key=artwork_key)
        url = url_for("mockups_admin.preview_cached", mockup_id=mockup_id, filename=out_path.name)
        return {"status": "ok", "preview_url": url, "generated_at": generated_at}
    except ValidationError as exc:
        return {"status": "error", "message": str(exc)}, 400


@mockups_admin_bp.get("/preview/<mockup_id>/<filename>")
def preview_cached(mockup_id: str, filename: str):
    svc = _preview_service()
    try:
        target = svc.resolve_cached_file(mockup_id, filename)
    except ValidationError:
        abort(404)
    return send_file(target, mimetype="image/jpeg")


@mockups_admin_bp.get("/preview-art/<filename>")
def preview_artwork_asset(filename: str):
    svc = _preview_service()
    try:
        path = svc.resolve_preview_artwork(filename)
    except ValidationError:
        abort(404)
    return send_file(path, mimetype="image/jpeg")

"""Legacy mockup trial routes were intentionally decommissioned.

Retired paths:
- /admin/mockups/gemini-studio
- /admin/mockups/basic-mockups
- /admin/mockups/ezy-mockups
- /admin/mockups/precision-mockups

Shared mockup management routes (bases, upload, aspect manager, category manager,
catalog preview, and template upload policy) remain active in this module.
"""
