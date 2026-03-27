"""Validation helpers for the mockup backend."""

from __future__ import annotations

from typing import Iterable, List, Tuple

import application.mockups.config as mockups_config
from application.mockups.errors import CoordinateSchemaError, DimensionMismatchError, ValidationError
from application.mockups.models import CoordinateSpec, Point, RegionPlacement


def _parse_corners_list(corners: Iterable) -> Tuple[Point, Point, Point, Point]:
    def to_point(entry: dict, label: str) -> Point:
        if isinstance(entry, (list, tuple)) and len(entry) == 2:
            x_val, y_val = entry[0], entry[1]
        elif isinstance(entry, dict):
            if "x" not in entry or "y" not in entry:
                raise CoordinateSchemaError(f"Corner {label} must contain x and y")
            x_val = entry["x"]
            y_val = entry["y"]
        else:
            raise CoordinateSchemaError(f"Corner {label} must be an object with x/y or a [x,y] list")
        if not isinstance(x_val, (int, float)) or not isinstance(y_val, (int, float)):
            raise CoordinateSchemaError(f"Corner {label} x/y must be numbers")
        return Point(float(x_val), float(y_val))

    labels = ["top-left", "top-right", "bottom-left", "bottom-right"]
    try:
        corners_list = list(corners)  # Convert Iterable to list for indexing
        points = [to_point(corners_list[i], labels[i]) for i in range(4)]
    except Exception as exc:  # pylint: disable=broad-except
        # Re-raise as schema error for consistency
        if isinstance(exc, CoordinateSchemaError):
            raise
        raise CoordinateSchemaError(str(exc)) from exc
    return tuple(points)  # type: ignore[return-value]


def _parse_zone_entry(zone: dict, idx: int, *, format_version: str | None = None) -> RegionPlacement:
    if not isinstance(zone, dict):
        raise CoordinateSchemaError(f"Zone at index {idx} must be an object")

    corners = zone.get("corners")
    points = zone.get("points")
    is_v2 = str(format_version or "").strip().startswith("2")
    if isinstance(corners, list) and len(corners) == 4:
        # NOTE: v2 format already outputs correct corner order [TL, TR, BR, BL]
        # No reordering needed for v2 - processor.js generates the correct order
        points = _parse_corners_list(corners)
        return RegionPlacement(region_id=f"zone{idx + 1}", corners=points)

    if isinstance(points, list) and len(points) == 4:
        # NOTE: v2 format already outputs correct point order [TL, TR, BR, BL]
        # No reordering needed for v2 - processor.js generates the correct order
        parsed = _parse_corners_list(points)
        return RegionPlacement(region_id=f"zone{idx + 1}", corners=parsed)

    x_val = zone.get("x")
    y_val = zone.get("y")
    w_val = zone.get("w")
    h_val = zone.get("h")
    if all(isinstance(v, (int, float)) for v in (x_val, y_val, w_val, h_val)):
        x = float(x_val) if x_val is not None else 0.0  # type: ignore[arg-type]
        y = float(y_val) if y_val is not None else 0.0  # type: ignore[arg-type]
        w = float(w_val) if w_val is not None else 0.0  # type: ignore[arg-type]
        h = float(h_val) if h_val is not None else 0.0  # type: ignore[arg-type]
        corners_list = [
            {"x": x, "y": y},
            {"x": x + w, "y": y},
            {"x": x, "y": y + h},
            {"x": x + w, "y": y + h},
        ]
        points = _parse_corners_list(corners_list)
        return RegionPlacement(region_id=f"zone{idx + 1}", corners=points)

    raise CoordinateSchemaError("Zone must define corners (4 points) or x/y/w/h rectangle")


def validate_coordinate_schema(payload: dict) -> CoordinateSpec:
    if not isinstance(payload, dict):
        raise CoordinateSchemaError("Coordinate payload must be an object")

    template = payload.get("template")
    regions = payload.get("regions")
    zones = payload.get("zones")
    legacy_corners = payload.get("corners")
    format_version = payload.get("format_version")

    if not isinstance(template, str) or not template.strip():
        raise CoordinateSchemaError("Field 'template' must be a non-empty string")

    placements: List[RegionPlacement] = []
    if isinstance(zones, list) and zones:
        if len(zones) > mockups_config.MAX_REGIONS:
            raise CoordinateSchemaError(f"Coordinate payload supports up to {mockups_config.MAX_REGIONS} zones")
        placements = [_parse_zone_entry(zone, idx, format_version=str(format_version) if format_version is not None else None) for idx, zone in enumerate(zones)]
    elif isinstance(regions, list) and regions:
        if len(regions) > mockups_config.MAX_REGIONS:
            raise CoordinateSchemaError(f"Coordinate payload supports up to {mockups_config.MAX_REGIONS} regions")
        seen_ids = set()
        for idx, region in enumerate(regions):
            if not isinstance(region, dict):
                raise CoordinateSchemaError(f"Region at index {idx} must be an object")
            region_id = region.get("id")
            corners = region.get("corners")
            if not isinstance(region_id, str) or not region_id.strip():
                raise CoordinateSchemaError("Region id must be a non-empty string")
            if region_id in seen_ids:
                raise CoordinateSchemaError(f"Duplicate region id: {region_id}")
            seen_ids.add(region_id)
            if not isinstance(corners, list) or len(corners) != 4:
                raise CoordinateSchemaError(f"Region '{region_id}' must have exactly four corners")
            # NOTE: v2 format already outputs correct corner order [TL, TR, BR, BL]
            # No reordering needed for v2 - processor.js generates the correct order
            points = _parse_corners_list(corners)
            placements.append(RegionPlacement(region_id=region_id.strip(), corners=points))
    elif isinstance(legacy_corners, list) and len(legacy_corners) == 4:
        # Legacy schema: top-level corners list only
        points = _parse_corners_list(legacy_corners)
        placements.append(RegionPlacement(region_id="primary", corners=points))
    else:
        raise CoordinateSchemaError("Field 'zones' or 'regions' must be a non-empty list or legacy 'corners' must contain four points")

    return CoordinateSpec(template=template.strip(), regions=tuple(placements))


def validate_corners_within_image(spec: CoordinateSpec, base_size: Tuple[int, int]) -> None:
    width, height = base_size
    if width <= 0 or height <= 0:
        raise DimensionMismatchError("Base image dimensions must be positive")

    for placement in spec.regions:
        for pt in placement.corners:
            if not (0 <= pt.x < width) or not (0 <= pt.y < height):
                raise DimensionMismatchError(
                    "Coordinate point lies outside base image bounds: "
                    f"({pt.x}, {pt.y}) not within [0,{width})x[0,{height})"
                )


def validate_slots(slots: Iterable[int]) -> List[int]:
    if slots is None:
        raise ValidationError("Slots must be provided")
    cleaned: List[int] = []
    seen = set()
    for slot in slots:
        if not isinstance(slot, int):
            raise ValidationError("Slots must be integers")
        if slot <= 0:
            raise ValidationError("Slots must be positive integers")
        if slot in seen:
            raise ValidationError(f"Duplicate slot specified: {slot}")
        seen.add(slot)
        cleaned.append(slot)
    return cleaned
