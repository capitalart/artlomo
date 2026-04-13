from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List, Tuple

from ..errors import ValidationError
from .models import MockupBase, Template

REQUIRED_FIELDS = {"slug", "aspect_ratio", "category", "base_image", "coords", "roles"}
BASE_REQUIRED_FIELDS = {
    "id",
    "slug",
    "original_filename",
    "base_image",
    "category",
    "status",
    "created_at",
    "updated_at",
}
BASE_STATUSES = {"uploaded", "missing_coordinates", "needs_regeneration", "coordinates_ready", "invalid", "disabled", "in_use"}

logger = logging.getLogger(__name__)


def _as_path(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / value)


def load_catalog_sections(path: Path) -> Tuple[List[dict], List[dict], Path]:
    if not path.exists():
        raise ValidationError(f"Catalog file missing: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError("Catalog file is not valid JSON") from exc

    base_dir = path.parent
    if isinstance(payload, list):
        return payload, [], base_dir
    if isinstance(payload, dict):
        templates = payload.get("templates") or []
        bases = payload.get("bases") or []
        if not isinstance(templates, list) or not isinstance(bases, list):
            raise ValidationError("Catalog document must contain list sections for templates and bases")
        return templates, bases, base_dir
    raise ValidationError("Catalog document must be an object or list")


def validate_catalog_payload(payload) -> List[dict]:
    if not isinstance(payload, list):
        raise ValidationError("Catalog payload must be a list of templates")
    return payload


def _validate_templates(entries: List[dict], base_dir: Path) -> List[Template]:
    templates: List[Template] = []
    seen_slugs = set()

    for raw in entries:
        if not isinstance(raw, dict):
            raise ValidationError("Each catalog entry must be an object")
        missing = REQUIRED_FIELDS - raw.keys()
        if missing:
            raise ValidationError(f"Catalog entry missing fields: {', '.join(sorted(missing))}")

        slug = str(raw.get("slug") or "").strip()
        aspect = str(raw.get("aspect_ratio") or "").strip()
        category = str(raw.get("category") or "").strip()
        base_image_val = raw.get("base_image")
        coords_val = raw.get("coords")
        roles_val = raw.get("roles")
        enabled_val = raw.get("enabled", True)

        if not slug:
            raise ValidationError("Template slug must be non-empty")
        if slug in seen_slugs:
            raise ValidationError(f"Duplicate template slug: {slug}")
        seen_slugs.add(slug)

        if not aspect:
            raise ValidationError("Template aspect_ratio must be non-empty")
        if not category:
            raise ValidationError("Template category must be non-empty")
        if not isinstance(base_image_val, str) or not base_image_val.strip():
            raise ValidationError("base_image must be a non-empty string")
        if not isinstance(coords_val, str) or not coords_val.strip():
            raise ValidationError("coords must be a non-empty string")
        if not isinstance(roles_val, list) or not roles_val:
            raise ValidationError("roles must be a non-empty list")
        if not all(isinstance(r, str) and r.strip() for r in roles_val):
            raise ValidationError("roles must contain non-empty strings")
        if not isinstance(enabled_val, bool):
            raise ValidationError("enabled must be a boolean")

        base_image_path = _as_path(base_dir, base_image_val.strip())
        coords_path = _as_path(base_dir, coords_val.strip())

        if not base_image_path.exists():
            raise ValidationError(f"Base image missing for template {slug}: {base_image_path}")
        if not coords_path.exists():
            raise ValidationError(f"Coords file missing for template {slug}: {coords_path}")

        templates.append(
            Template(
                slug=slug,
                aspect_ratio=aspect,
                category=category,
                base_image=base_image_path,
                coords=coords_path,
                roles=[r.strip() for r in roles_val],
                enabled=enabled_val,
            )
        )

    return templates


def _validate_bases(entries: List[dict], base_dir: Path) -> List[MockupBase]:
    bases: List[MockupBase] = []
    seen_ids = set()
    seen_slugs = set()

    for raw in entries:
        if not isinstance(raw, dict):
            raise ValidationError("Each base entry must be an object")
        missing = BASE_REQUIRED_FIELDS - raw.keys()
        if missing:
            raise ValidationError(f"Base entry missing fields: {', '.join(sorted(missing))}")

        base_id = str(raw.get("id") or "").strip()
        slug = str(raw.get("slug") or "").strip()
        original_filename = str(raw.get("original_filename") or "").strip()
        category = str(raw.get("category") or "").strip()
        status = str(raw.get("status") or "").strip()
        aspect = raw.get("aspect_ratio")
        coordinates_val = raw.get("coordinates_path") or raw.get("coordinates")
        region_count = raw.get("region_count")
        aspect_source = raw.get("aspect_source")
        last_coordinated_at = raw.get("last_coordinated_at")
        coordinate_type = raw.get("coordinate_type")
        created_at = str(raw.get("created_at") or "").strip()
        updated_at = str(raw.get("updated_at") or "").strip()

        if not base_id:
            raise ValidationError("Base id must be non-empty")
        if base_id in seen_ids:
            raise ValidationError(f"Duplicate base id: {base_id}")
        seen_ids.add(base_id)

        if not slug:
            raise ValidationError("Base slug must be non-empty")
        if slug in seen_slugs:
            raise ValidationError(f"Duplicate base slug: {slug}")
        seen_slugs.add(slug)

        if not original_filename:
            raise ValidationError("original_filename must be non-empty")
        if not category:
            raise ValidationError("category must be non-empty")
        if status not in BASE_STATUSES:
            raise ValidationError(f"Invalid base status: {status}")
        if created_at == "" or updated_at == "":
            raise ValidationError("created_at and updated_at must be non-empty")

        base_image_val = raw.get("base_image_path") or raw.get("base_image")
        if not isinstance(base_image_val, str) or not base_image_val.strip():
            raise ValidationError("base_image_path must be a non-empty string")
        base_image_path = _as_path(base_dir, base_image_val.strip())
        if not base_image_path.exists():
            logger.warning("Mockup base image missing; marking as missing_coordinates", extra={"slug": slug, "path": str(base_image_path)})
            status = "missing_coordinates"

        coords_path: Path | None = None
        if coordinates_val:
            if not isinstance(coordinates_val, str) or not coordinates_val.strip():
                raise ValidationError("coordinates_path must be a string when provided")
            coords_path = _as_path(base_dir, coordinates_val.strip())
            if not coords_path.exists():
                logger.warning("Mockup base coords missing; marking as needs_regeneration", extra={"slug": slug, "path": str(coords_path)})
                status = "needs_regeneration"
                coords_path = None

        if aspect is not None and aspect != "":
            if not isinstance(aspect, str):
                raise ValidationError("aspect_ratio must be a string when provided")
            if not aspect.strip():
                aspect = None
            else:
                aspect = aspect.strip()
        else:
            aspect = None

        if region_count is not None:
            if not isinstance(region_count, int) or region_count < 0:
                raise ValidationError("region_count must be a non-negative integer when provided")
            if region_count > 6:
                raise ValidationError("region_count must not exceed 6")

        if aspect_source is not None:
            if not isinstance(aspect_source, str) or not aspect_source.strip():
                raise ValidationError("aspect_source must be a non-empty string when provided")
            aspect_source = aspect_source.strip()
        else:
            aspect_source = None

        if last_coordinated_at is not None:
            if not isinstance(last_coordinated_at, str) or not last_coordinated_at.strip():
                raise ValidationError("last_coordinated_at must be a non-empty string when provided")
            last_coordinated_at = last_coordinated_at.strip()
        else:
            last_coordinated_at = None

        if coordinate_type is not None:
            if not isinstance(coordinate_type, str) or not coordinate_type.strip():
                raise ValidationError("coordinate_type must be a non-empty string when provided")
            coordinate_type = coordinate_type.strip()
        else:
            coordinate_type = None

        bases.append(
            MockupBase(
                id=base_id,
                slug=slug,
                original_filename=original_filename,
                base_image=base_image_path,
                coordinates=coords_path,
                category=category,
                aspect_ratio=aspect,
                status=status,
                region_count=region_count,
                created_at=created_at,
                updated_at=updated_at,
                aspect_source=aspect_source,
                last_coordinated_at=last_coordinated_at,
                coordinate_type=coordinate_type,
            )
        )

    return bases


def load_and_validate_catalog(path: Path) -> List[Template]:
    templates_payload, _, base_dir = load_catalog_sections(path)
    entries = validate_catalog_payload(templates_payload)
    return _validate_templates(entries, base_dir)


def load_and_validate_bases(path: Path) -> List[MockupBase]:
    _, bases_payload, base_dir = load_catalog_sections(path)
    return _validate_bases(bases_payload, base_dir)
