from __future__ import annotations

from typing import Dict, Iterable, List

from ..errors import ValidationError
from ..catalog.models import Template
from .models import MandatorySpec, OptionalSpec, SelectionPolicy


def validate_policy(policy: SelectionPolicy) -> None:
    if policy.total_slots <= 0:
        raise ValidationError("total_slots must be positive")
    if len(policy.mandatory.templates) > policy.total_slots:
        raise ValidationError("mandatory templates exceed total slots")
    if not isinstance(policy.optional.max_per_category, (int, type(None))):
        raise ValidationError("max_per_category must be int or None")
    if isinstance(policy.optional.max_per_category, int) and policy.optional.max_per_category <= 0:
        raise ValidationError("max_per_category must be positive when set")


def ensure_templates_available(policy: SelectionPolicy, catalog: Dict[str, Template]) -> None:
    for slug in policy.mandatory.templates:
        if slug not in catalog:
            raise ValidationError(f"Mandatory template missing or disabled: {slug}")
    
    # Check mandatory category if specified
    mandatory_count = len(policy.mandatory.templates)
    if policy.mandatory.category:
        category_templates = [tpl for tpl in catalog.values() if tpl.category == policy.mandatory.category and tpl.enabled]
        if not category_templates:
            raise ValidationError(f"No enabled templates found in mandatory category: {policy.mandatory.category}")
        mandatory_count += 1
    
    optional_pool = _filter_optional_pool(policy.optional, catalog.values(), policy.mandatory.templates)
    needed = policy.total_slots - mandatory_count
    if needed > len(optional_pool):
        raise ValidationError("Insufficient optional templates to satisfy policy")


def _filter_optional_pool(optional: OptionalSpec, templates: Iterable[Template], mandatory_slugs: Iterable[str]) -> List[Template]:
    mandatory_set = set(mandatory_slugs)
    category_allow = set(optional.categories)
    pool = [tpl for tpl in templates if tpl.category in category_allow and tpl.slug not in mandatory_set]
    return pool
