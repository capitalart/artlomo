from __future__ import annotations

import json
from io import BytesIO
from typing import Iterable, List

from PIL import Image

from .. import validation as coord_validation
from ..config import MAX_REGIONS
from ..errors import ValidationError
from ..models import RegionPlacement


def validate_png_bytes(data: bytes) -> Image.Image:
    try:
        img = Image.open(BytesIO(data))
        img.load()
    except Exception as exc:  # pylint: disable=broad-except
        raise ValidationError("Base image must be a valid PNG") from exc
    if img.format != "PNG":
        raise ValidationError("Base image must be PNG")
    if "A" not in img.getbands():
        raise ValidationError("Base image must have transparency (alpha channel)")
    return img


def validate_coords_payload(payload: dict, base_size: tuple[int, int]) -> List[RegionPlacement]:
    spec = coord_validation.validate_coordinate_schema(payload)
    if len(spec.regions) < 1 or len(spec.regions) > MAX_REGIONS:
        raise ValidationError("Coordinates must define between 1 and 6 regions")
    coord_validation.validate_corners_within_image(spec, base_size)
    return list(spec.regions)


def validate_roles(roles: Iterable[str]) -> List[str]:
    if not isinstance(roles, Iterable):
        raise ValidationError("roles must be iterable")
    cleaned: List[str] = []
    for role in roles:
        if not isinstance(role, str) or not role.strip():
            raise ValidationError("roles must contain non-empty strings")
        cleaned.append(role.strip())
    if not cleaned:
        raise ValidationError("roles must not be empty")
    return cleaned


def validate_slug_unique(slug: str, existing_slugs: Iterable[str]) -> None:
    if slug in existing_slugs:
        raise ValidationError(f"Template slug already exists: {slug}")


def validate_json_payload(raw: bytes | str) -> dict:
    try:
        if isinstance(raw, bytes):
            return json.loads(raw.decode("utf-8"))
        return json.loads(raw)
    except Exception as exc:  # pylint: disable=broad-except
        raise ValidationError("Coordinate JSON is invalid") from exc
