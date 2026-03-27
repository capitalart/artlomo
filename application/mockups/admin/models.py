from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from ..catalog.models import Template


@dataclass(frozen=True)
class TemplateRecord:
    slug: str
    aspect_ratio: str
    category: str
    base_image: Path
    coords: Path
    roles: List[str]
    enabled: bool
    region_count: int | None = None


@dataclass(frozen=True)
class CatalogView:
    templates: List[TemplateRecord]
    categories: List[str]


@dataclass(frozen=True)
class PolicyDocument:
    mandatory_templates: List[str]
    version: int = 1
    mandatory_category: str | None = None  # If set, will randomly select one template from this category


SlotMap = Dict[str, Dict]
