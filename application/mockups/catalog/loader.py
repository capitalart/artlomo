from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from .models import Template
from .validation import load_and_validate_catalog
from ..config import MOCKUP_BASES_DIR


def load_catalog(path: Path) -> List[Template]:
    """Load and validate the template catalog (read-only)."""

    return [tpl for tpl in load_and_validate_catalog(path) if tpl.enabled]


def load_physical_bases(
    *,
    catalog_dir: Path | None = None,
    aspect: str | None = None,
    category: str | None = None,
) -> List[Template]:
    root = (catalog_dir / "assets" / "mockups" / "bases") if catalog_dir else MOCKUP_BASES_DIR
    if not root.exists() or not root.is_dir():
        return []

    aspect_dirs: List[Path]
    if aspect:
        target_aspect = root / aspect
        aspect_dirs = [target_aspect] if target_aspect.exists() and target_aspect.is_dir() else []
    else:
        aspect_dirs = [p for p in root.iterdir() if p.is_dir()]

    templates: List[Template] = []
    seen = set()
    for aspect_dir in sorted(aspect_dirs):
        aspect_name = aspect_dir.name
        category_dirs: List[Path]
        if category:
            target_cat = aspect_dir / category
            category_dirs = [target_cat] if target_cat.exists() and target_cat.is_dir() else []
        else:
            category_dirs = [p for p in aspect_dir.iterdir() if p.is_dir()]
        for category_dir in sorted(category_dirs):
            category_name = category_dir.name
            for base_png in sorted(category_dir.glob("*.png")):
                coords = base_png.with_suffix(".json")
                if not coords.exists():
                    continue
                slug = base_png.stem
                if slug in seen:
                    continue
                seen.add(slug)
                templates.append(
                    Template(
                        slug=slug,
                        aspect_ratio=aspect_name,
                        category=category_name,
                        base_image=base_png,
                        coords=coords,
                        roles=["studio"],
                        enabled=True,
                    )
                )
    return templates


def load_physical_catalog(*, catalog_dir: Path | None = None, return_counts: bool = False) -> List[Template] | Dict[str, int]:
    root = (catalog_dir / "assets" / "mockups" / "bases") if catalog_dir else MOCKUP_BASES_DIR
    if not root.exists() or not root.is_dir():
        return {} if return_counts else []

    templates: List[Template] = []
    counts: Dict[str, int] = {}
    seen = set()
    for aspect_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
        aspect = aspect_dir.name
        for category_dir in sorted([p for p in aspect_dir.iterdir() if p.is_dir()]):
            category = category_dir.name
            for base_png in sorted(category_dir.glob("*.png")):
                counts[category] = counts.get(category, 0) + 1
                coords = base_png.with_suffix(".json")
                if not coords.exists():
                    continue
                slug = base_png.stem
                if slug in seen:
                    continue
                seen.add(slug)
                templates.append(
                    Template(
                        slug=slug,
                        aspect_ratio=aspect,
                        category=category,
                        base_image=base_png,
                        coords=coords,
                        roles=["studio"],
                        enabled=True,
                    )
                )

    return counts if return_counts else templates
