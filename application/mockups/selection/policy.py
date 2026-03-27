from __future__ import annotations

from dataclasses import dataclass

from .models import MandatorySpec, OptionalSpec, SelectionPolicy


# Default policy placeholder for programmatic construction.
# Consumers should instantiate SelectionPolicy explicitly for clarity.
DEFAULT_POLICY = SelectionPolicy(
    total_slots=4,
    mandatory=MandatorySpec(templates=[]),
    optional=OptionalSpec(categories=[], max_per_category=None),
)

__all__ = ["SelectionPolicy", "MandatorySpec", "OptionalSpec", "DEFAULT_POLICY"]
