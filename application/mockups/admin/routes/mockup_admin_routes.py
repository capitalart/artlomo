from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Set, cast
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
from db import EzyMockupJob, GeminiStudioJob, PrecisionMockupJob, SessionLocal
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
from ...services.gemini_service import GeminiImageService
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


def _enabled_filter(raw: str | None) -> bool | None:
    if raw is None:
        return True
    if raw in {"1", "true", "enabled"}:
        return True
    if raw in {"0", "false", "disabled"}:
        return False
    return None


def _preserve_filters() -> Dict[str, str]:
    filters: Dict[str, str] = {}
    for key in ("category", "aspect", "enabled", "mandatory"):
        val = request.form.get(key) or request.args.get(key)
        if val:
            filters[key] = val
    return filters


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


def _studio_root() -> Path:
    configured = current_app.config.get("STUDIO_OUTPUT_DIR")
    if configured:
        configured_path = Path(configured)
        return configured_path.parent if configured_path.suffix else configured_path
    return Path("/srv/artlomo/var/studio")


def _studio_upload_dir() -> Path:
    return _studio_root() / "uploads"


def _studio_output_dir() -> Path:
    configured = current_app.config.get("STUDIO_OUTPUT_DIR")
    if configured:
        configured_path = Path(configured)
        if configured_path.suffix:
            return configured_path.parent
        return configured_path
    return _studio_root() / "outputs"


def _ezy_root() -> Path:
    return _studio_root() / "ezy"


def _ezy_upload_dir() -> Path:
    return _ezy_root() / "uploads"


def _ezy_room_output_dir() -> Path:
    return _ezy_root() / "rooms"


def _ezy_mask_output_dir() -> Path:
    return _ezy_root() / "masks"


def _ezy_transparent_output_dir() -> Path:
    return _ezy_root() / "transparent"


def _precision_root() -> Path:
    return _studio_root() / "precision"


def _precision_upload_dir() -> Path:
    return _precision_root() / "uploads"


def _precision_room_output_dir() -> Path:
    return _precision_root() / "rooms"


def _precision_transparent_output_dir() -> Path:
    return _precision_root() / "transparent"


def _studio_worker_running() -> bool:
    try:
        import subprocess

        result = subprocess.run(
            ["pgrep", "-fa", "celery"],
            capture_output=True,
            text=True,
            timeout=1,
            check=False,
        )
        output = (result.stdout or "").strip().lower()
        return "celery" in output and "worker" in output
    except Exception:
        return False


def _studio_image_url(job: GeminiStudioJob) -> str:
    return url_for("mockups_admin.gemini_studio_output", filename=Path(str(job.output_image_path or "")).name)


def _serialize_studio_job(job: GeminiStudioJob) -> dict:
    db_id = cast(int | None, job.id)
    db_variation_index = cast(int | None, job.variation_index)
    created_at = cast(datetime | None, job.created_at)
    updated_at = cast(datetime | None, job.updated_at)
    return {
        "id": db_id if db_id is not None else 0,
        "job_id": str(job.job_id),
        "batch_id": str(job.batch_id),
        "status": str(job.status),
        "prompt_text": str(job.prompt_text or ""),
        "aspect_ratio": str(job.aspect_ratio or "1x1"),
        "category": str(job.category or "uncategorised"),
        "variation_index": db_variation_index if db_variation_index is not None else 1,
        "image_url": _studio_image_url(job) if str(job.output_image_path or "").strip() else "",
        "error_message": str(job.error_message or ""),
        "frame_coordinates_json": str(job.frame_coordinates_json or ""),
        "frame_coordinates_model": str(job.frame_coordinates_model or ""),
        "frame_coordinates_error": str(job.frame_coordinates_error or ""),
        "added_to_library": bool(job.added_to_library),
        "library_base_slug": str(job.library_base_slug or ""),
        "created_at": created_at.isoformat() if created_at is not None else "",
        "updated_at": updated_at.isoformat() if updated_at is not None else "",
    }


def _recent_studio_jobs(limit: int = 24) -> List[dict]:
    session = SessionLocal()
    try:
        rows = (
            session.query(GeminiStudioJob)
            .order_by(GeminiStudioJob.created_at.desc(), GeminiStudioJob.id.desc())
            .limit(limit)
            .all()
        )
        return [_serialize_studio_job(row) for row in rows]
    finally:
        session.close()


def _ezy_image_url(path_value: str | None) -> str:
    clean_name = Path(str(path_value or "")).name
    if not clean_name:
        return ""
    return url_for("mockups_admin.ezy_mockup_output", filename=clean_name)


def _precision_image_url(path_value: str | None) -> str:
    clean_name = Path(str(path_value or "")).name
    if not clean_name:
        return ""
    return url_for("mockups_admin.precision_mockup_output", filename=clean_name)


def _read_image_size(path_value: str | None) -> tuple[int, int]:
    clean_path = str(path_value or "").strip()
    if not clean_path:
        return (0, 0)
    try:
        with Image.open(clean_path) as image_obj:
            return image_obj.size
    except Exception:
        return (0, 0)


def _parse_frame_coordinates(raw_value: str | None) -> dict[str, list[int]]:
    payload = str(raw_value or "").strip()
    if not payload:
        return {}
    try:
        parsed = json.loads(payload)
    except Exception:
        return {}
    if not isinstance(parsed, dict):
        return {}
    result: dict[str, list[int]] = {}
    for key in ("tl", "tr", "br", "bl"):
        point = parsed.get(key)
        if (
            isinstance(point, list)
            and len(point) == 2
            and all(isinstance(value, (int, float)) for value in point)
        ):
            result[key] = [int(point[0]), int(point[1])]
    return result


def _serialize_ezy_job(job: EzyMockupJob) -> dict:
    db_id = cast(int | None, job.id)
    db_variation_index = cast(int | None, job.variation_index)
    created_at = cast(datetime | None, job.created_at)
    updated_at = cast(datetime | None, job.updated_at)
    started_at = cast(datetime | None, job.started_at)
    finished_at = cast(datetime | None, job.finished_at)
    pipeline_stage_raw = str(job.pipeline_stage_json or "").strip()
    try:
        pipeline_stage = json.loads(pipeline_stage_raw) if pipeline_stage_raw else {}
    except Exception:
        pipeline_stage = {}
    if not isinstance(pipeline_stage, dict):
        pipeline_stage = {}
    result_details = {
        "job_id": str(job.job_id),
        "status": str(job.status or ""),
        "pipeline_stage": pipeline_stage,
        "error_message": str(job.error_message or ""),
        "frame_coordinates_error": str(job.frame_coordinates_error or ""),
        "frame_coordinates_model": str(job.frame_coordinates_model or ""),
        "room_output_path": str(job.room_output_path or ""),
        "mask_output_path": str(job.mask_output_path or ""),
        "transparent_output_path": str(job.transparent_output_path or ""),
        "harmonized_output_path": str(job.harmonized_output_path or ""),
        "started_at": started_at.isoformat() if started_at is not None else "",
        "finished_at": finished_at.isoformat() if finished_at is not None else "",
    }
    return {
        "id": db_id if db_id is not None else 0,
        "job_id": str(job.job_id),
        "batch_id": str(job.batch_id),
        "status": str(job.status),
        "prompt_text": str(job.prompt_text or ""),
        "aspect_ratio": str(job.aspect_ratio or "1x1"),
        "category": str(job.category or "uncategorised"),
        "variation_index": db_variation_index if db_variation_index is not None else 1,
        "room_image_url": _ezy_image_url(str(job.room_output_path or "")),
        "mask_image_url": _ezy_image_url(str(job.mask_output_path or "")),
        "transparent_image_url": _ezy_image_url(str(job.transparent_output_path or "")),
        "harmonized_image_url": _ezy_image_url(str(job.harmonized_output_path or "")),
        "error_message": str(job.error_message or ""),
        "frame_coordinates_json": str(job.frame_coordinates_json or ""),
        "frame_coordinates_model": str(job.frame_coordinates_model or ""),
        "frame_coordinates_error": str(job.frame_coordinates_error or ""),
        "pipeline_stage": pipeline_stage,
        "result_details": result_details,
        "auto_generate_alpha": bool(job.auto_generate_alpha),
        "edge_smoothing": bool(job.edge_smoothing),
        "created_at": created_at.isoformat() if created_at is not None else "",
        "updated_at": updated_at.isoformat() if updated_at is not None else "",
    }


def _recent_ezy_jobs(limit: int = 24) -> List[dict]:
    session = SessionLocal()
    try:
        rows = (
            session.query(EzyMockupJob)
            .order_by(EzyMockupJob.created_at.desc(), EzyMockupJob.id.desc())
            .limit(limit)
            .all()
        )
        return [_serialize_ezy_job(row) for row in rows]
    finally:
        session.close()


def _serialize_precision_job(job: PrecisionMockupJob) -> dict:
    db_id = cast(int | None, job.id)
    created_at = cast(datetime | None, job.created_at)
    updated_at = cast(datetime | None, job.updated_at)
    started_at = cast(datetime | None, job.started_at)
    finished_at = cast(datetime | None, job.finished_at)
    frame_coordinates = _parse_frame_coordinates(str(job.frame_coordinates_json or ""))
    image_width, image_height = _read_image_size(str(job.room_output_path or ""))
    overlay_points = [
        frame_coordinates.get("tl", []),
        frame_coordinates.get("tr", []),
        frame_coordinates.get("br", []),
        frame_coordinates.get("bl", []),
    ] if frame_coordinates else []
    result_details = {
        "job_id": str(job.job_id or ""),
        "status": str(job.status or ""),
        "error_message": str(job.error_message or ""),
        "frame_coordinates": frame_coordinates,
        "frame_coordinates_model": str(job.frame_coordinates_model or ""),
        "frame_coordinates_error": str(job.frame_coordinates_error or ""),
        "room_output_path": str(job.room_output_path or ""),
        "transparent_output_path": str(job.transparent_output_path or ""),
        "image_width": image_width,
        "image_height": image_height,
        "started_at": started_at.isoformat() if started_at is not None else "",
        "finished_at": finished_at.isoformat() if finished_at is not None else "",
    }
    return {
        "id": db_id if db_id is not None else 0,
        "job_id": str(job.job_id or ""),
        "batch_id": str(job.batch_id or ""),
        "status": str(job.status or "Pending"),
        "prompt_text": str(job.prompt_text or ""),
        "aspect_ratio": str(job.aspect_ratio or "4x5"),
        "category": str(job.category or "uncategorised"),
        "room_image_url": _precision_image_url(str(job.room_output_path or "")),
        "transparent_image_url": _precision_image_url(str(job.transparent_output_path or "")),
        "error_message": str(job.error_message or ""),
        "frame_coordinates_json": str(job.frame_coordinates_json or ""),
        "frame_coordinates": frame_coordinates,
        "frame_coordinates_model": str(job.frame_coordinates_model or ""),
        "frame_coordinates_error": str(job.frame_coordinates_error or ""),
        "frame_overlay_points": overlay_points,
        "image_width": image_width,
        "image_height": image_height,
        "result_details": result_details,
        "created_at": created_at.isoformat() if created_at is not None else "",
        "updated_at": updated_at.isoformat() if updated_at is not None else "",
    }


def _recent_precision_jobs(limit: int = 24) -> List[dict]:
    session = SessionLocal()
    try:
        rows = (
            session.query(PrecisionMockupJob)
            .order_by(PrecisionMockupJob.created_at.desc(), PrecisionMockupJob.id.desc())
            .limit(limit)
            .all()
        )
        return [_serialize_precision_job(row) for row in rows]
    finally:
        session.close()


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

        if wants_json and len(base_files) > 1:
            return jsonify({"status": "error", "message": "Upload expects one base PNG per request."}), 400

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

        category_raw = (form_data["category"] or "").strip()
        aspect_raw = (form_data["aspect_ratio"] or "").strip()
        if not category_raw or not aspect_raw:
            category_value = DEFAULT_MOCKUP_CATEGORY
            aspect_value = DEFAULT_MOCKUP_ASPECT
        else:
            category_value = category_raw
            aspect_value = aspect_raw

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

# ---------------------------------------------------------------------------
# Gemini Mockup Studio
# ---------------------------------------------------------------------------

_STUDIO_ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def _resolve_studio_placeholder_for_aspect(
    aspect_ratio: str,
    preferred_placeholder_name: str | None = None,
) -> Path | None:
    """Resolve default cyan placeholder guide for Gemini Studio auto mode."""
    preferred_name = str(preferred_placeholder_name or "").strip()
    preferred_candidates: tuple[Path, ...] = ()
    if preferred_name:
        safe_name = Path(preferred_name).name
        preferred_candidates = (
            GeminiImageService.REFERENCE_GUIDE_STORAGE_DIR / safe_name,
            GeminiImageService.LEGACY_REFERENCE_GUIDE_STORAGE_DIR / safe_name,
            GeminiImageService.POSITIONAL_REFERENCE_GUIDE_STORAGE_DIR / safe_name,
        )

    candidates = (
        *preferred_candidates,
        GeminiImageService.REFERENCE_GUIDE_STORAGE_DIR / f"cyan_placeholder_{aspect_ratio}.jpg",
        GeminiImageService.REFERENCE_GUIDE_STORAGE_DIR / f"cyan_placeholder_{aspect_ratio}.png",
        GeminiImageService.REFERENCE_GUIDE_STORAGE_DIR / f"cyan_guide_{aspect_ratio}.png",
        GeminiImageService.LEGACY_REFERENCE_GUIDE_STORAGE_DIR / f"solid_{aspect_ratio}_00ffff.png",
        GeminiImageService.POSITIONAL_REFERENCE_GUIDE_STORAGE_DIR / f"cyan_placeholder_{aspect_ratio}.jpg",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _cleanup_studio_source_if_unused(source_path: str) -> None:
    candidate = Path(str(source_path or "")).resolve()
    if not candidate.exists():
        return
    session = SessionLocal()
    try:
        remaining = (
            session.query(GeminiStudioJob)
            .filter(GeminiStudioJob.source_image_path == str(candidate))
            .count()
        )
    finally:
        session.close()
    if remaining == 0:
        candidate.unlink(missing_ok=True)


# ============================================================================
# Basic Mockups - Simple category-specific generation
# ============================================================================

_BASIC_MOCKUP_PROMPTS = {
    "kitchen": "Generate a square, photorealistic kitchen interior featuring the attached artwork as a single framed wall piece, captured from an oblique off-center camera angle. The artwork should hang on a side wall seen at a slight angle to the camera, creating architectural depth and a premium mockup feel. The artwork must remain fully visible and retain its original aspect ratio. The frame may show natural perspective, but the artwork itself must remain proportionally correct, unobscured, and free from distortion, glare, or cropping. Stylish realistic kitchen, daylight, editorial interior photography.",
    "living-room": "Generate a square, photorealistic living room mockup with the attached artwork displayed as one framed piece on a side wall, captured from diagonally across the room rather than front-on. The composition should feel editorial and architectural, with visible depth and a realistic premium-home aesthetic. The artwork must remain fully unobscured and preserve its original aspect ratio. Natural frame perspective is allowed, but the artwork itself must remain undistorted, uncropped, and glare-free. Elegant but believable interior photography.",
    "bedroom": "Generate a square, photorealistic bedroom with the attached artwork displayed as a framed wall piece, positioned at an angle that creates dynamic composition. The artwork should appear as a key design element in a stylish, contemporary bedroom. The artwork must retain its original aspect ratio and remain fully visible, unobscured, and free from distortion or glare. Premium interior design aesthetic with natural lighting.",
    "office": "Generate a square, photorealistic office or study with the attached artwork displayed as a framed piece on the wall. The composition should convey professional sophistication with the artwork integrated as a key design element. The artwork must maintain its original aspect ratio and remain fully visible, unobscured, and glare-free. Realistic office lighting and materials.",
    "dining-room": "Generate a square, photorealistic dining room with the attached artwork displayed as a framed wall piece above or adjacent to the dining area. The artwork should be prominently featured as a design focal point. The artwork must retain its original aspect ratio and remain fully visible, unobscured, and free from distortion or glare. Warm, inviting lighting with premium interior design.",
    "gallery": "Generate a square, photorealistic gallery or studio space with the attached artwork displayed as the main focal point on a clean white or light-colored wall. The lighting should be gallery-standard with even illumination. The artwork must retain its original aspect ratio and remain fully visible, unobscured, uncropped, and completely free from any glare, shadows, or contamination. Professional art gallery presentation.",
}


@mockups_admin_bp.get("/basic-mockups")
def basic_mockups():
    """Display the basic mockups page with simple category-specific prompts."""
    try:
        svc = _catalog_service()
        aspects = _aspect_options(svc) or list(STANDARD_MOCKUP_ASPECT_RATIOS)
        categories = list(_BASIC_MOCKUP_PROMPTS.keys())
    except Exception:
        aspects = list(STANDARD_MOCKUP_ASPECT_RATIOS)
        categories = list(_BASIC_MOCKUP_PROMPTS.keys())
    
    return render_template(
        "mockups/basic_mockups.html",
        aspects=aspects,
        categories=categories,
        csrf_token=get_csrf_token(),
        recent_jobs=_recent_studio_jobs(),
        worker_running=_studio_worker_running(),
        page_title="Basic Mockups",
    )


@mockups_admin_bp.post("/basic-mockups/generate")
def basic_mockups_generate():
    """Generate basic mockups using minimal, category-specific prompts."""
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp
    
    category = (request.form.get("category") or "").strip().lower()
    if category not in _BASIC_MOCKUP_PROMPTS:
        return jsonify({"status": "error", "message": "Invalid category."}), 400
    
    aspect_raw = (request.form.get("aspect_ratio") or "4x5").strip()
    valid_aspects = set(MockupBaseGenerationCatalog.ASPECT_RATIOS)
    aspect_ratio = aspect_raw if aspect_raw in valid_aspects else "4x5"
    
    # Allow user-edited prompt, falling back to category default.
    prompt_override = (request.form.get("prompt") or "").strip()
    base_prompt = prompt_override if prompt_override else _BASIC_MOCKUP_PROMPTS[category]
    
    try:
        variations = int(request.form.get("variations") or 1)
    except (TypeError, ValueError):
        variations = 1
    variations = max(1, min(10, variations))
    
    image_file = request.files.get("image")
    batch_id = uuid.uuid4().hex
    source_filename = ""
    cleanup_uploaded_source = False
    
    if image_file and image_file.filename:
        img_suffix = Path(image_file.filename).suffix.lower()
        if img_suffix not in _STUDIO_ALLOWED_EXTENSIONS:
            return jsonify({"status": "error", "message": "Unsupported file type. Use PNG, JPG, or WebP."}), 400
        upload_dir = _studio_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        source_path = upload_dir / f"{batch_id}{img_suffix}"
        image_file.save(str(source_path))
        source_filename = str(image_file.filename or source_path.name)
        cleanup_uploaded_source = True
    else:
        # Auto-select artwork-only placeholder (no borders)
        placeholder_dir = Path("/srv/artlomo/application/mockups/catalog/assets/mockups/reference-guides/artwork-only")
        placeholder_file = placeholder_dir / f"{aspect_ratio}-artwork-placeholder.png"
        
        if not placeholder_file.exists():
            return jsonify(
                {
                    "status": "error",
                    "message": f"No placeholder found for aspect ratio {aspect_ratio}.",
                }
            ), 400
        source_path = placeholder_file.resolve()
        source_filename = source_path.name
    
    session = SessionLocal()
    queued_job_ids: List[int] = []
    try:
        for variation_index in range(1, variations + 1):
            job = GeminiStudioJob(
                job_id=f"basic-{batch_id[:10]}-{variation_index}",
                batch_id=batch_id,
                prompt_text=base_prompt,
                source_image_path=str(source_path),
                source_filename=source_filename,
                aspect_ratio=aspect_ratio,
                category=category,
                variation_index=variation_index,
                status="Pending",
            )
            session.add(job)
            session.flush()
            queued_id = cast(int | None, job.id)
            if queued_id is not None:
                queued_job_ids.append(queued_id)
        session.commit()
    except Exception:
        session.rollback()
        if cleanup_uploaded_source:
            source_path.unlink(missing_ok=True)
        raise
    finally:
        session.close()
    
    from application.mockups.tasks_mockup_generator import process_gemini_studio_job
    
    dispatch_errors: List[str] = []
    dispatched = 0
    failed_dispatch_job_ids: List[int] = []
    for queued_job_id in queued_job_ids:
        try:
            process_gemini_studio_job.delay(queued_job_id)
            dispatched += 1
        except Exception as exc:
            dispatch_errors.append(str(exc))
            failed_dispatch_job_ids.append(queued_job_id)
    
    if failed_dispatch_job_ids:
        session = SessionLocal()
        try:
            error_message = (
                "Failed to dispatch to Celery queue. "
                + (dispatch_errors[0] if dispatch_errors else "Unknown dispatch error")
            )
            for failed_id in failed_dispatch_job_ids:
                job = session.get(GeminiStudioJob, failed_id)
                if job is None:
                    continue
                job.status = "Failed"  # type: ignore[assignment]
                job.error_message = error_message  # type: ignore[assignment]
                job.finished_at = datetime.utcnow()  # type: ignore[assignment]
            session.commit()
        except Exception:
            session.rollback()
            logger.exception("Failed to mark undelivered basic mockup jobs as Failed")
        finally:
            session.close()
    
    message = f"Queued {len(queued_job_ids)} variation{'s' if len(queued_job_ids) != 1 else ''}."
    if dispatch_errors and dispatched == 0:
        message = "Jobs were created but could not be dispatched to Celery."
    
    return jsonify(
        {
            "status": "ok" if dispatched > 0 else "warning",
            "message": message,
            "queued": len(queued_job_ids),
            "dispatched": dispatched,
            "dispatch_errors": dispatch_errors[:5],
            "jobs": _recent_studio_jobs(),
            "worker_running": _studio_worker_running(),
        }
    ), (202 if dispatched > 0 else 503)


@mockups_admin_bp.get("/ezy-mockups")
def ezy_mockups():
    try:
        svc = _catalog_service()
        aspects = _aspect_options(svc) or list(STANDARD_MOCKUP_ASPECT_RATIOS)
    except Exception:
        aspects = list(STANDARD_MOCKUP_ASPECT_RATIOS)

    return render_template(
        "mockups/ezy_mockups.html",
        aspects=aspects,
        categories=list(_BASIC_MOCKUP_PROMPTS.keys()),
        csrf_token=get_csrf_token(),
        recent_jobs=_recent_ezy_jobs(),
        worker_running=_studio_worker_running(),
        page_title="Ezy Mockups",
    )


@mockups_admin_bp.get("/precision-mockups")
def precision_mockups():
    try:
        svc = _catalog_service()
        aspects = _aspect_options(svc) or list(STANDARD_MOCKUP_ASPECT_RATIOS)
        categories = _category_options(svc) or list(MockupBaseGenerationCatalog.CATEGORIES)
    except Exception:
        aspects = list(STANDARD_MOCKUP_ASPECT_RATIOS)
        categories = list(MockupBaseGenerationCatalog.CATEGORIES)
    return render_template(
        "mockups/precision_mockups.html",
        aspects=aspects,
        categories=categories,
        csrf_token=get_csrf_token(),
        recent_jobs=_recent_precision_jobs(),
        worker_running=_studio_worker_running(),
        page_title="Precision Mockups",
    )


@mockups_admin_bp.get("/precision-mockups/status")
def precision_mockups_status():
    return jsonify(
        {
            "status": "ok",
            "jobs": _recent_precision_jobs(),
            "worker_running": _studio_worker_running(),
        }
    )


@mockups_admin_bp.post("/precision-mockups/generate")
def precision_mockups_generate():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp

    prompt = (request.form.get("prompt") or "").strip()
    category = (request.form.get("category") or "living-room").strip().lower()
    valid_categories = set(MockupBaseGenerationCatalog.CATEGORIES)
    if category not in valid_categories:
        return jsonify({"status": "error", "message": "Invalid category."}), 400

    aspect_raw = (request.form.get("aspect_ratio") or "4x5").strip()
    valid_aspects = set(MockupBaseGenerationCatalog.ASPECT_RATIOS)
    aspect_ratio = aspect_raw if aspect_raw in valid_aspects else "4x5"

    image_file = request.files.get("image")
    batch_id = uuid.uuid4().hex
    cleanup_uploaded_source = False

    if image_file and image_file.filename:
        img_suffix = Path(image_file.filename).suffix.lower()
        if img_suffix not in _STUDIO_ALLOWED_EXTENSIONS:
            return jsonify({"status": "error", "message": "Unsupported file type. Use PNG, JPG, or WebP."}), 400
        upload_dir = _precision_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        source_path = upload_dir / f"{batch_id}{img_suffix}"
        image_file.save(str(source_path))
        source_filename = str(image_file.filename or source_path.name)
        cleanup_uploaded_source = True
    else:
        placeholder_dir = Path("/srv/artlomo/application/mockups/catalog/assets/mockups/reference-guides/artwork-only")
        placeholder_file = placeholder_dir / f"{aspect_ratio}-artwork-placeholder.png"
        if not placeholder_file.exists():
            return jsonify(
                {
                    "status": "error",
                    "message": f"No placeholder found for aspect ratio {aspect_ratio}.",
                }
            ), 400
        source_path = placeholder_file.resolve()
        source_filename = source_path.name

    session = SessionLocal()
    queued_job_id: int | None = None
    try:
        job = PrecisionMockupJob(
            job_id=f"precision-{batch_id[:10]}",
            batch_id=batch_id,
            prompt_text=prompt,
            source_image_path=str(source_path),
            source_filename=source_filename,
            aspect_ratio=aspect_ratio,
            category=category,
            status="Pending",
        )
        session.add(job)
        session.flush()
        queued_job_id = cast(int | None, job.id)
        session.commit()
    except Exception:
        session.rollback()
        if cleanup_uploaded_source:
            source_path.unlink(missing_ok=True)
        raise
    finally:
        session.close()

    if queued_job_id is None:
        return jsonify({"status": "error", "message": "Failed to queue Precision job."}), 500

    from application.mockups.tasks_precision_generator import process_precision_mockup_job

    try:
        process_precision_mockup_job.delay(queued_job_id)
    except Exception as exc:
        session = SessionLocal()
        try:
            job = session.get(PrecisionMockupJob, queued_job_id)
            if job is not None:
                job.status = "Failed"  # type: ignore[assignment]
                job.error_message = f"Failed to dispatch to Celery queue. {exc}"  # type: ignore[assignment]
                job.finished_at = datetime.utcnow()  # type: ignore[assignment]
                session.commit()
        except Exception:
            session.rollback()
            logger.exception("Failed to mark undelivered Precision Mockup job as Failed")
        finally:
            session.close()
        return jsonify(
            {
                "status": "warning",
                "message": "Job was created but could not be dispatched to Celery.",
                "jobs": _recent_precision_jobs(),
                "worker_running": _studio_worker_running(),
            }
        ), 503

    return jsonify(
        {
            "status": "ok",
            "message": "Queued 1 Precision Mockup.",
            "queued": 1,
            "dispatched": 1,
            "jobs": _recent_precision_jobs(),
            "worker_running": _studio_worker_running(),
        }
    ), 202


@mockups_admin_bp.post("/precision-mockups/jobs/<int:job_id>/delete")
def precision_mockup_delete(job_id: int):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp

    session = SessionLocal()
    try:
        job = session.get(PrecisionMockupJob, job_id)
        if job is None:
            return jsonify({"status": "error", "message": "Precision job not found."}), 404

        output_paths = [
            Path(str(job.room_output_path or "")).resolve() if str(job.room_output_path or "").strip() else None,
            Path(str(job.transparent_output_path or "")).resolve() if str(job.transparent_output_path or "").strip() else None,
        ]
        source_path = str(job.source_image_path or "")
        session.delete(job)
        session.commit()
    finally:
        session.close()

    for output_path in output_paths:
        if output_path is not None:
            output_path.unlink(missing_ok=True)

    _cleanup_studio_source_if_unused(source_path)
    return jsonify({"status": "ok", "jobs": _recent_precision_jobs()})


@mockups_admin_bp.get("/precision-mockups/output/<filename>")
def precision_mockup_output(filename: str):
    clean_name = Path(filename).name
    for directory in (_precision_room_output_dir(), _precision_transparent_output_dir()):
        candidate = directory / clean_name
        if candidate.exists():
            return send_from_directory(directory, clean_name)
    abort(404)


@mockups_admin_bp.get("/ezy-mockups/status")
def ezy_mockups_status():
    return jsonify(
        {
            "status": "ok",
            "jobs": _recent_ezy_jobs(),
            "worker_running": _studio_worker_running(),
        }
    )


@mockups_admin_bp.post("/ezy-mockups/generate")
def ezy_mockups_generate():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp

    prompt = (request.form.get("prompt") or "").strip()

    category = (request.form.get("category") or "kitchen").strip().lower()
    if category not in _BASIC_MOCKUP_PROMPTS:
        return jsonify({"status": "error", "message": "Invalid category."}), 400

    aspect_raw = (request.form.get("aspect_ratio") or "4x5").strip()
    valid_aspects = set(MockupBaseGenerationCatalog.ASPECT_RATIOS)
    aspect_ratio = aspect_raw if aspect_raw in valid_aspects else "4x5"

    auto_generate_alpha = str(request.form.get("auto_generate_alpha") or "1").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    edge_smoothing = str(request.form.get("edge_smoothing") or "0").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    try:
        variations = int(request.form.get("variations") or 1)
    except (TypeError, ValueError):
        variations = 1
    variations = max(1, min(10, variations))

    image_file = request.files.get("image")
    batch_id = uuid.uuid4().hex
    source_filename = ""
    cleanup_uploaded_source = False

    if image_file and image_file.filename:
        img_suffix = Path(image_file.filename).suffix.lower()
        if img_suffix not in _STUDIO_ALLOWED_EXTENSIONS:
            return jsonify({"status": "error", "message": "Unsupported file type. Use PNG, JPG, or WebP."}), 400
        upload_dir = _ezy_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        source_path = upload_dir / f"{batch_id}{img_suffix}"
        image_file.save(str(source_path))
        source_filename = str(image_file.filename or source_path.name)
        cleanup_uploaded_source = True
    else:
        placeholder_dir = Path("/srv/artlomo/application/mockups/catalog/assets/mockups/reference-guides/artwork-only")
        placeholder_file = placeholder_dir / f"{aspect_ratio}-artwork-placeholder.png"
        if not placeholder_file.exists():
            return jsonify(
                {
                    "status": "error",
                    "message": f"No placeholder found for aspect ratio {aspect_ratio}.",
                }
            ), 400
        source_path = placeholder_file.resolve()
        source_filename = source_path.name

    session = SessionLocal()
    queued_job_ids: List[int] = []
    try:
        for variation_index in range(1, variations + 1):
            job = EzyMockupJob(
                job_id=f"ezy-{batch_id[:10]}-{variation_index}",
                batch_id=batch_id,
                prompt_text=prompt,
                source_image_path=str(source_path),
                source_filename=source_filename,
                aspect_ratio=aspect_ratio,
                category=category,
                variation_index=variation_index,
                auto_generate_alpha=auto_generate_alpha,
                edge_smoothing=edge_smoothing,
                status="Pending",
            )
            session.add(job)
            session.flush()
            queued_id = cast(int | None, job.id)
            if queued_id is not None:
                queued_job_ids.append(queued_id)
        session.commit()
    except Exception:
        session.rollback()
        if cleanup_uploaded_source:
            source_path.unlink(missing_ok=True)
        raise
    finally:
        session.close()

    from application.mockups.tasks_mockup_generator import process_ezy_mockup_job

    dispatch_errors: List[str] = []
    dispatched = 0
    failed_dispatch_job_ids: List[int] = []
    for queued_job_id in queued_job_ids:
        try:
            process_ezy_mockup_job.delay(queued_job_id)
            dispatched += 1
        except Exception as exc:
            dispatch_errors.append(str(exc))
            failed_dispatch_job_ids.append(queued_job_id)

    if failed_dispatch_job_ids:
        session = SessionLocal()
        try:
            error_message = (
                "Failed to dispatch to Celery queue. "
                + (dispatch_errors[0] if dispatch_errors else "Unknown dispatch error")
            )
            for failed_id in failed_dispatch_job_ids:
                job = session.get(EzyMockupJob, failed_id)
                if job is None:
                    continue
                job.status = "Failed"  # type: ignore[assignment]
                job.error_message = error_message  # type: ignore[assignment]
                job.finished_at = datetime.utcnow()  # type: ignore[assignment]
            session.commit()
        except Exception:
            session.rollback()
            logger.exception("Failed to mark undelivered Ezy Mockup jobs as Failed")
        finally:
            session.close()

    message = f"Queued {len(queued_job_ids)} variation{'s' if len(queued_job_ids) != 1 else ''}."
    if dispatch_errors and dispatched == 0:
        message = "Jobs were created but could not be dispatched to Celery."

    return jsonify(
        {
            "status": "ok" if dispatched > 0 else "warning",
            "message": message,
            "queued": len(queued_job_ids),
            "dispatched": dispatched,
            "dispatch_errors": dispatch_errors[:5],
            "jobs": _recent_ezy_jobs(),
            "worker_running": _studio_worker_running(),
        }
    ), (202 if dispatched > 0 else 503)


@mockups_admin_bp.post("/ezy-mockups/jobs/<int:job_id>/delete")
def ezy_mockup_delete(job_id: int):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp

    session = SessionLocal()
    try:
        job = session.get(EzyMockupJob, job_id)
        if job is None:
            return jsonify({"status": "error", "message": "Ezy job not found."}), 404

        output_paths = [
            Path(str(job.room_output_path or "")).resolve() if str(job.room_output_path or "").strip() else None,
            Path(str(job.mask_output_path or "")).resolve() if str(job.mask_output_path or "").strip() else None,
            Path(str(job.transparent_output_path or "")).resolve() if str(job.transparent_output_path or "").strip() else None,
        ]
        source_path = str(job.source_image_path or "")
        session.delete(job)
        session.commit()
    finally:
        session.close()

    for output_path in output_paths:
        if output_path is not None:
            output_path.unlink(missing_ok=True)

    _cleanup_studio_source_if_unused(source_path)
    return jsonify({"status": "ok", "jobs": _recent_ezy_jobs()})


@mockups_admin_bp.get("/ezy-mockups/output/<filename>")
def ezy_mockup_output(filename: str):
    clean_name = Path(filename).name
    for directory in (_ezy_room_output_dir(), _ezy_mask_output_dir(), _ezy_transparent_output_dir()):
        candidate = directory / clean_name
        if candidate.exists():
            return send_from_directory(directory, clean_name)
    abort(404)


@mockups_admin_bp.get("/gemini-studio")
def gemini_studio():
    try:
        svc = _catalog_service()
        aspects = _aspect_options(svc) or list(STANDARD_MOCKUP_ASPECT_RATIOS)
        categories = _category_options(svc) or list(MockupBaseGenerationCatalog.CATEGORIES)
    except Exception:
        aspects = list(STANDARD_MOCKUP_ASPECT_RATIOS)
        categories = list(MockupBaseGenerationCatalog.CATEGORIES)
    if "uncategorised" not in categories:
        categories = ["uncategorised", *categories]
    return render_template(
        "mockups/gemini_studio.html",
        aspects=aspects,
        categories=categories,
        csrf_token=get_csrf_token(),
        recent_jobs=_recent_studio_jobs(),
        worker_running=_studio_worker_running(),
        page_title="Gemini Mockup Studio",
    )


@mockups_admin_bp.get("/gemini-studio/status")
def gemini_studio_status():
    return jsonify(
        {
            "status": "ok",
            "jobs": _recent_studio_jobs(),
            "worker_running": _studio_worker_running(),
        }
    )


@mockups_admin_bp.get("/gemini-studio/jobs/<int:job_id>/full-prompt")
def gemini_studio_full_prompt(job_id: int):
    """Return the complete compiled prompt text sent to Gemini for debugging.
    
    Includes system instruction, base template, user prompt, all context injections,
    and thought signature if available.
    """
    session = SessionLocal()
    try:
        job = session.get(GeminiStudioJob, job_id)
        if job is None:
            return jsonify({"status": "error", "message": "Job not found"}), 404
        
        from application.mockups.services.gemini_service import GeminiImageService
        from application.mockups.tasks_mockup_generator import (
            _build_studio_reference_guided_prompt,
            _build_studio_pure_generation_prompt,
            _get_thought_signature,
        )
        
        gemini_service = GeminiImageService()
        source_path = Path(str(job.source_image_path or ""))
        has_reference = source_path.exists() and gemini_service._supports_reference_guided_editing()
        
        # Query total variations in batch
        total_variations = int(
            session.query(GeminiStudioJob)
            .filter(GeminiStudioJob.batch_id == job.batch_id)
            .count()
            or 1
        )
        
        # Get reused thought signature if applicable
        thought_signature_key = f"studio:{job.batch_id}:{job.aspect_ratio}"
        reused_thought_signature = (
            _get_thought_signature(thought_signature_key) 
            if int(str(job.variation_index) or "1") > 1 
            else ""
        )
        
        # Build the effective prompt based on reference availability
        if has_reference:
            effective_prompt = _build_studio_reference_guided_prompt(
                str(job.prompt_text or ""),
                str(job.aspect_ratio or "1x1"),
                int(str(job.variation_index) or "1"),
                str(job.category or "uncategorised"),
                total_variations,
                reused_thought_signature,
            )
            delivery_mode = "REFERENCE-GUIDED EDITING"
        else:
            effective_prompt = _build_studio_pure_generation_prompt(
                str(job.prompt_text or ""),
                str(job.aspect_ratio or "1x1"),
                int(str(job.variation_index) or "1"),
                str(job.category or "uncategorised"),
                total_variations,
                reused_thought_signature,
            )
            delivery_mode = "PURE GENERATION"
        
        # Compile full prompt with all metadata
        full_prompt_compilation = (
            f"[GEMINI STUDIO JOB COMPILATION]\n"
            f"Job ID: {job.id}\n"
            f"Batch ID: {job.batch_id}\n"
            f"Delivery Mode: {delivery_mode}\n"
            f"Status: {job.status}\n"
            f"\n"
            f"════════════════════════════════════════════════════════════════\n"
            f"EXECUTION METADATA (Logged for Debug, Not in Prompt):\n"
            f"════════════════════════════════════════════════════════════════\n"
            f"Artwork Aspect Ratio: {job.aspect_ratio}\n"
            f"Target Category: {job.category}\n"
            f"Placeholder Type: {job.placeholder_type if hasattr(job, 'placeholder_type') else '(unknown)'}\n"
            f"Variation: {job.variation_index} / {total_variations}\n"
            f"\n"
            f"════════════════════════════════════════════════════════════════\n"
            f"CLEAN PROMPT SENT TO GEMINI:\n"
            f"════════════════════════════════════════════════════════════════\n"
            f"{effective_prompt}\n"
            f"\n"
            f"════════════════════════════════════════════════════════════════\n"
            f"API CONFIGURATION:\n"
            f"════════════════════════════════════════════════════════════════\n"
            f"Primary Model: {gemini_service.IMAGE_GENERATION_MODEL}\n"
            f"Fallback Models: {', '.join(gemini_service.DEFAULT_IMAGE_GENERATION_MODEL_FALLBACKS)}\n"
            f"Thinking Level: {gemini_service.THINKING_LEVEL}\n"
            f"Output Aspect Ratio: 1:1 (canvas)\n"
            f"Reference File: {source_path.name if source_path.exists() else '(auto-placeholder selected)'}\n"
            f"Thought Signature: {reused_thought_signature if reused_thought_signature else '(none - first variation)'}\n"
        )
        
        return jsonify({
            "status": "ok",
            "job_id": job_id,
            "batch_id": job.batch_id,
            "full_prompt_compilation": full_prompt_compilation,
            "delivery_mode": delivery_mode,
            "has_reference": has_reference,
        })
    except Exception as e:
        logger.exception("Error retrieving full prompt for job %d", job_id)
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        session.close()


@mockups_admin_bp.post("/gemini-studio/generate")
def gemini_studio_generate():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp

    prompt = (request.form.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"status": "error", "message": "Prompt is required."}), 400

    aspect_raw = (request.form.get("aspect_ratio") or "1x1").strip()
    valid_aspects = set(MockupBaseGenerationCatalog.ASPECT_RATIOS)
    aspect_ratio = aspect_raw if aspect_raw in valid_aspects else "1x1"

    placeholder_type = (request.form.get("placeholder_type") or "artwork-only").strip()
    if placeholder_type not in {"outlined", "artwork-only"}:
        placeholder_type = "artwork-only"

    category_raw = (request.form.get("category") or "uncategorised").strip()
    valid_categories = set(_category_options(_catalog_service()) or list(MockupBaseGenerationCatalog.CATEGORIES) + ["uncategorised"])
    category = category_raw if category_raw in valid_categories else "uncategorised"

    try:
        variations = int(request.form.get("variations") or 1)
    except (TypeError, ValueError):
        variations = 1
    variations = max(1, min(10, variations))
    source_placeholder_name = Path(request.form.get("source_placeholder") or "").name.strip()

    image_file = request.files.get("image")
    batch_id = uuid.uuid4().hex
    source_filename = ""
    cleanup_uploaded_source = False

    if image_file and image_file.filename:
        img_suffix = Path(image_file.filename).suffix.lower()
        if img_suffix not in _STUDIO_ALLOWED_EXTENSIONS:
            return jsonify({"status": "error", "message": "Unsupported file type. Use PNG, JPG, or WebP."}), 400
        upload_dir = _studio_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        source_path = upload_dir / f"{batch_id}{img_suffix}"
        image_file.save(str(source_path))
        source_filename = str(image_file.filename or source_path.name)
        cleanup_uploaded_source = True
    else:
        # Auto-select placeholder based on type (outlined vs artwork-only)
        placeholder_dir = Path("/srv/artlomo/application/mockups/catalog/assets/mockups/reference-guides")
        if placeholder_type == "artwork-only":
            placeholder_dir = placeholder_dir / "artwork-only"
            default_name = f"{aspect_ratio}-artwork-placeholder.png"
        else:
            placeholder_dir = placeholder_dir / "outlined-artworks"
            default_name = f"{aspect_ratio}-outlined-artwork.png"

        placeholder_file = placeholder_dir / (source_placeholder_name or default_name)
        if not placeholder_file.exists() and source_placeholder_name:
            placeholder_file = placeholder_dir / default_name
        
        if not placeholder_file.exists():
            return jsonify(
                {
                    "status": "error",
                    "message": (
                        f"No placeholder found for aspect ratio {aspect_ratio} "
                        f"(placeholder type: {placeholder_type})."
                    ),
                }
            ), 400
        source_path = placeholder_file.resolve()
        source_filename = source_path.name

    session = SessionLocal()
    queued_job_ids: List[int] = []
    try:
        for variation_index in range(1, variations + 1):
            job = GeminiStudioJob(
                job_id=f"studio-{batch_id[:10]}-{variation_index}",
                batch_id=batch_id,
                prompt_text=prompt,
                source_image_path=str(source_path),
                source_filename=source_filename,
                aspect_ratio=aspect_ratio,
                category=category,
                variation_index=variation_index,
                status="Pending",
            )
            session.add(job)
            session.flush()
            queued_id = cast(int | None, job.id)
            if queued_id is not None:
                queued_job_ids.append(queued_id)
        session.commit()
    except Exception:
        session.rollback()
        if cleanup_uploaded_source:
            source_path.unlink(missing_ok=True)
        raise
    finally:
        session.close()

    from application.mockups.tasks_mockup_generator import process_gemini_studio_job

    dispatch_errors: List[str] = []
    dispatched = 0
    failed_dispatch_job_ids: List[int] = []
    for queued_job_id in queued_job_ids:
        try:
            process_gemini_studio_job.delay(queued_job_id)
            dispatched += 1
        except Exception as exc:
            dispatch_errors.append(str(exc))
            failed_dispatch_job_ids.append(queued_job_id)

    if failed_dispatch_job_ids:
        session = SessionLocal()
        try:
            error_message = (
                "Failed to dispatch to Celery queue. "
                + (dispatch_errors[0] if dispatch_errors else "Unknown dispatch error")
            )
            for failed_id in failed_dispatch_job_ids:
                job = session.get(GeminiStudioJob, failed_id)
                if job is None:
                    continue
                job.status = "Failed"  # type: ignore[assignment]
                job.error_message = error_message  # type: ignore[assignment]
                job.finished_at = datetime.utcnow()  # type: ignore[assignment]
            session.commit()
        except Exception:
            session.rollback()
            logger.exception("Failed to mark undelivered Gemini Studio jobs as Failed")
        finally:
            session.close()

    message = f"Queued {len(queued_job_ids)} variation{'s' if len(queued_job_ids) != 1 else ''}."
    if dispatch_errors and dispatched == 0:
        message = "Jobs were created but could not be dispatched to Celery."

    return jsonify(
        {
            "status": "ok" if dispatched > 0 else "warning",
            "message": message,
            "queued": len(queued_job_ids),
            "dispatched": dispatched,
            "dispatch_errors": dispatch_errors[:5],
            "jobs": _recent_studio_jobs(),
            "worker_running": _studio_worker_running(),
        }
    ), (202 if dispatched > 0 else 503)


@mockups_admin_bp.post("/gemini-studio/jobs/<int:job_id>/delete")
def gemini_studio_delete(job_id: int):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp

    session = SessionLocal()
    try:
        job = session.get(GeminiStudioJob, job_id)
        if job is None:
            return jsonify({"status": "error", "message": "Studio job not found."}), 404
        output_path = Path(str(job.output_image_path or "")).resolve() if str(job.output_image_path or "").strip() else None
        source_path = str(job.source_image_path or "")
        session.delete(job)
        session.commit()
    finally:
        session.close()

    if output_path is not None:
        output_path.unlink(missing_ok=True)
    _cleanup_studio_source_if_unused(source_path)

    return jsonify({"status": "ok", "jobs": _recent_studio_jobs()})


@mockups_admin_bp.post("/gemini-studio/clear-all-pending")
def gemini_studio_clear_all_pending():
    """Permanently delete all pending Gemini Studio jobs (DB + files).
    
    This is a destructive operation that:
    1. Finds all jobs with status='Pending'
    2. Deletes their database records
    3. Deletes associated output files from disk
    4. Cleans up unused source images
    
    Returns a summary of deleted jobs.
    """
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp

    session = SessionLocal()
    deleted_count = 0
    deleted_jobs = []
    errors = []
    
    try:
        # Find all pending jobs
        pending_jobs = session.query(GeminiStudioJob).filter(
            GeminiStudioJob.status == "Pending"
        ).all()
        
        deleted_count = len(pending_jobs)
        
        for job in pending_jobs:
            try:
                # Capture info for response
                deleted_jobs.append({
                    "id": job.id,
                    "batch_id": job.batch_id,
                    "job_id": str(job.job_id or ""),
                    "category": str(job.category or ""),
                    "aspect_ratio": str(job.aspect_ratio or ""),
                })
                
                # Delete output file if exists
                output_path = Path(str(job.output_image_path or "")).resolve() if str(job.output_image_path or "").strip() else None
                if output_path is not None and output_path.exists():
                    try:
                        output_path.unlink(missing_ok=True)
                    except Exception as e:
                        logger.warning("Could not delete output file %s: %s", output_path, e)
                
                # Track source for cleanup
                source_path = str(job.source_image_path or "")
                
                # Delete job from DB
                session.delete(job)
                session.flush()
                
                # Clean up source if unused by other jobs
                _cleanup_studio_source_if_unused(source_path)
                
            except Exception as e:
                msg = f"Error deleting job {job.id}: {str(e)}"
                logger.error(msg, exc_info=True)
                errors.append(msg)
        
        session.commit()
        logger.info("Cleared %d pending Gemini Studio jobs", deleted_count)
        
    except Exception as e:
        session.rollback()
        logger.exception("Failed to clear pending Gemini Studio jobs")
        return jsonify(
            {
                "status": "error",
                "message": f"Failed to clear pending jobs: {str(e)}",
                "deleted_count": 0,
            }
        ), 500
    finally:
        session.close()
    
    return jsonify(
        {
            "status": "ok",
            "message": f"Permanently deleted {deleted_count} pending job(s).",
            "deleted_count": deleted_count,
            "deleted_jobs": deleted_jobs,
            "errors": errors,
            "jobs": _recent_studio_jobs(),
        }
    )


@mockups_admin_bp.post("/gemini-studio/jobs/<int:job_id>/add-to-library")
def gemini_studio_add_to_library(job_id: int):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        if resp is None:
            abort(400)
        return resp

    session = SessionLocal()
    try:
        job = session.get(GeminiStudioJob, job_id)
        if job is None:
            return jsonify({"status": "error", "message": "Studio job not found."}), 404
        if str(job.status) != "Completed":
            return jsonify({"status": "error", "message": "Only completed studio jobs can be added to the library."}), 400
        if bool(job.added_to_library):
            return jsonify({"status": "ok", "message": "Already added to library.", "base_slug": str(job.library_base_slug or "")})

        output_path = Path(str(job.output_image_path or "")).resolve()
        if not output_path.exists():
            return jsonify({"status": "error", "message": "Generated image is missing from disk."}), 404

        catalog_svc = _catalog_service()
        target_dir = catalog_svc.base_root / str(job.aspect_ratio or "1x1") / "uncategorised"
        target_dir.mkdir(parents=True, exist_ok=True)
        base_slug = slugify(f"{job.aspect_ratio}-uncategorised-studio-{uuid.uuid4().hex[:8]}")
        target_path = target_dir / f"{base_slug}.png"

        image_obj = Image.open(output_path)
        image_obj.load()
        if image_obj.mode not in {"RGB", "RGBA"}:
            image_obj = image_obj.convert("RGB")
        image_obj.save(target_path, format="PNG")

        catalog_svc.sync_orphan_bases_from_filesystem()
        catalog_svc.generate_missing_base_thumbs()

        setattr(job, "added_to_library", True)
        setattr(job, "library_base_slug", base_slug)
        session.commit()
    finally:
        session.close()

    return jsonify(
        {
            "status": "ok",
            "message": f"Added to mockup library as {base_slug}.",
            "base_slug": base_slug,
            "jobs": _recent_studio_jobs(),
        }
    )


@mockups_admin_bp.get("/gemini-studio/output/<filename>")
def gemini_studio_output(filename: str):
    clean_name = Path(filename).name
    if not clean_name or clean_name != filename:
        abort(400)
    studio_dir = _studio_output_dir()
    return send_from_directory(studio_dir, clean_name, mimetype="image/png")
