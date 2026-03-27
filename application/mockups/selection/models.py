from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..catalog.models import Template


@dataclass(frozen=True)
class MandatorySpec:
    templates: List[str]
    category: str | None = None  # If set, randomly select one template from this category


@dataclass(frozen=True)
class OptionalSpec:
    categories: List[str]
    max_per_category: int | None = None


@dataclass(frozen=True)
class SelectionPolicy:
    total_slots: int
    mandatory: MandatorySpec
    optional: OptionalSpec


SlotPlan = Dict[int, Template]
