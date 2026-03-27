from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class Template:
    slug: str
    aspect_ratio: str
    category: str
    base_image: Path
    coords: Path
    roles: List[str]
    enabled: bool = True


@dataclass(frozen=True)
class MockupBase:
    id: str
    slug: str
    original_filename: str
    base_image: Path
    coordinates: Optional[Path]
    category: str
    aspect_ratio: Optional[str]
    status: str
    region_count: Optional[int]
    created_at: str
    updated_at: str
    aspect_source: Optional[str] = None
    last_coordinated_at: Optional[str] = None
    coordinate_type: Optional[str] = None
