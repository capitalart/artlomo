"""Dataclasses for deterministic mockup generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class RegionPlacement:
    region_id: str
    corners: Tuple[Point, Point, Point, Point]


@dataclass(frozen=True)
class CoordinateSpec:
    template: str
    regions: Tuple[RegionPlacement, ...]


@dataclass(frozen=True)
class MockupTemplate:
    slug: str
    aspect_ratio: str
    base_path: Path
    coords_path: Path
    slot: int


@dataclass(frozen=True)
class GeneratedMockup:
    sku: str
    slot: int
    aspect_ratio: str
    template_slug: str
    composite_path: Path
    thumb_path: Path
    assets_json_path: Path
    content_hash: str
