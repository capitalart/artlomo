# === [ utils/categories.py | dynamic-mockup-categories ] ===
"""
Utilities for dynamically discovering mockup categories from the filesystem
and mapping canonical folder names (values) to friendly labels for display.

Contracts
- Source of truth: inputs/mockups/categorised/<aspect>/<CategoryFolder>/*
- Canonical value: folder name, e.g. "Living-Room", "Bedroom-Adults"
- Friendly label: hyphens -> spaces, Title Case, e.g. "Living Room"

Public API
- list_category_options(aspect: str) -> List[Dict[str, str]]
  Returns a list of {"value": folder_name, "label": friendly_label},
  sorted case-insensitively by folder name. Hidden/"dot" directories ignored.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Dict

import application.config as config

# Fallback root for categorised mockups if config is missing the constant
_DEFAULT_INPUTS_ROOT = Path("inputs") / "mockups" / "categorised"


def _inputs_root() -> Path:
    root = getattr(config, "MOCKUPS_CATEGORISED_INPUTS_DIR", None)
    try:
        if isinstance(root, (str, Path)):
            return Path(root)
    except Exception:
        pass
    return _DEFAULT_INPUTS_ROOT


def _folder_to_label(folder: str) -> str:
    # Replace hyphens/underscores with spaces and Title Case
    name = str(folder or "").strip().replace("_", " ").replace("-", " ")
    # Collapse multiple spaces
    name = " ".join(name.split())
    return name.title()


def list_category_options(aspect: str) -> List[Dict[str, str]]:
    """Return discovered category options for a given aspect.

    Each option is a dict: {"value": folder_name, "label": friendly_label}
    Only directories directly under the aspect folder are considered; dot-dirs ignored.
    Sorted case-insensitively by the canonical folder name.
    """
    aspect = (aspect or "").strip() or getattr(config, "DEFAULT_ASPECT", "3x4")
    root = _inputs_root() / aspect
    if not root.exists() or not root.is_dir():
        return []

    options: List[Dict[str, str]] = []
    for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        if child.name.startswith('.'):
            continue
        value = child.name
        label = _folder_to_label(value)
        options.append({"value": value, "label": label})
    return options


__all__ = ["list_category_options", "_folder_to_label"]
