from __future__ import annotations

import hashlib
import random
from pathlib import Path
from typing import Dict, Iterable, Literal

import application.mockups.config as mockups_config
from ..catalog.models import Template
from ..catalog.loader import load_physical_catalog
from ..errors import ValidationError
from ..pipeline import generate_mockups_for_artwork
from .models import SelectionPolicy, SlotPlan
from .validation import ensure_templates_available, validate_policy, _filter_optional_pool


def _deterministic_key(seed: str, value: str) -> str:
    return hashlib.sha256(f"{seed}::{value}".encode("utf-8")).hexdigest()


def plan_slots(policy: SelectionPolicy, catalog: Dict[str, Template], *, sku: str) -> SlotPlan:
    validate_policy(policy)
    ensure_templates_available(policy, catalog)

    plan: SlotPlan = {}
    slot = 1

    # Mandatory templates from explicit list
    mandatory_slugs = list(policy.mandatory.templates)
    
    # If mandatory_category is specified, randomly select one template from that category
    if policy.mandatory.category:
        category_templates = [
            tpl for tpl in catalog.values()
            if tpl.category == policy.mandatory.category and tpl.enabled
        ]
        if not category_templates:
            raise ValidationError(f"No enabled templates found in mandatory category: {policy.mandatory.category}")
        # Use sku as seed for deterministic random selection
        random.seed(sku)
        selected_mandatory = random.choice(category_templates)
        mandatory_slugs.append(selected_mandatory.slug)
    
    # Add mandatory templates to plan
    for slug in mandatory_slugs:
        plan[slot] = catalog[slug]
        slot += 1

    # Optional pool filtered by categories and enabled templates
    optional_pool = _filter_optional_pool(policy.optional, catalog.values(), mandatory_slugs)

    # Deterministic ordering using seed = SKU
    optional_pool = sorted(optional_pool, key=lambda tpl: _deterministic_key(sku, tpl.slug))

    cat_counts: Dict[str, int] = {}
    remaining_slots = policy.total_slots - len(mandatory_slugs)
    for tpl in optional_pool:
        if remaining_slots <= 0:
            break
        max_per_cat = policy.optional.max_per_category
        if max_per_cat is not None:
            used = cat_counts.get(tpl.category, 0)
            if used >= max_per_cat:
                continue
        plan[slot] = tpl
        cat_counts[tpl.category] = cat_counts.get(tpl.category, 0) + 1
        slot += 1
        remaining_slots -= 1

    if len(plan) < policy.total_slots:
        raise ValidationError("Unable to fill all slots with available templates")

    return plan


def execute_plan(
    *,
    sku: str,
    plan: SlotPlan,
    mode: Literal["generate", "swap"] = "generate",
    processed_root: Path | None = None,
    master_index_path: Path | None = None,
):
    results = {}
    for slot, template in sorted(plan.items()):
        base_path = template.base_image if template.base_image.is_absolute() else mockups_config.BASE_DIR / template.base_image
        coords_path = template.coords if template.coords.is_absolute() else mockups_config.BASE_DIR / template.coords
        results[slot] = generate_mockups_for_artwork(
            sku=sku,
            template_slug=template.slug,
            aspect_ratio=template.aspect_ratio,
            category=template.category,
            base_image_path=base_path,
            coords_path=coords_path,
            slot=slot,
            mode=mode,
            master_index_path=master_index_path,
            processed_root=processed_root,
        )
    return results


def load_catalog_for_selection(path: Path | None = None) -> Dict[str, Template]:
    if path is None:
        catalog_dir = Path(__file__).resolve().parents[1] / "catalog"
    else:
        catalog_dir = path if path.is_dir() else path.parent

    templates = load_physical_catalog(catalog_dir=catalog_dir)
    return {tpl.slug: tpl for tpl in templates if isinstance(tpl, Template)}
