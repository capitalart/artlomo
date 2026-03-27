from __future__ import annotations
from pathlib import Path
from typing import List
import application.config as config


# -------- Slug helpers --------
def slug_dir_from_listing(listing: dict) -> str:
    """
    Returns the canonical slug directory name (stem only, no extension).
    Accepts slug from 'seo_filename' (e.g. '<slug>.jpg'), 'seo_slug', or 'slug'.
    """
    raw = listing.get("seo_filename") or listing.get("seo_slug") or listing.get("slug") or ""
    name = Path(str(raw)).name
    stem = Path(name).stem
    return stem


def slug_dir_from_any(value: str) -> str:
    name = Path(str(value)).name
    return Path(name).stem


# -------- URL builder (absolute) --------
def public_processed_url(rel_path: str) -> str:
    """
    Build absolute URL for a path relative to static/, ensuring one leading slash.
    Example input: 'art-processing/processed-artwork/<slug>/<file>.jpg'
    """
    base_raw = getattr(config, "BASE_URL", "https://artlomo.com")
    base = str(base_raw).replace("http://", "https://").rstrip("/")
    return f"{base}/static/{str(rel_path).lstrip('/')}"


def rel_paths_for_slug(slug_dir: str) -> dict:
    """
    Returns a dict of relative file paths inside 'art-processing/processed-artwork/<slug>/'.
    Does NOT add 'static/' or BASE_URL; these are rel to static/.
    """
    base = f"art-processing/processed-artwork/{slug_dir}"
    return {
        "hero": f"{base}/{slug_dir}.jpg",
        "large_thumb": f"{base}/{slug_dir}-LARGE-THUMB.jpg",
        "small_thumb": f"{base}/{slug_dir}-SMALL-THUMB.jpg",
        "mockups": [f"{base}/{slug_dir}-MU-{i:02d}.jpg" for i in range(1, 10)],
    }


def _fs_exists_under(root: Path, sub: Path) -> bool:
    try:
        return (root / sub).exists()
    except Exception:
        return False


def fs_exists(rel_path: str) -> bool:
    """Check existence in processed or vault stage.

    Map rel_path 'art-processing/processed-artwork/<slug>/<file>' to filesystem:
    - Primary check under PROCESSED_ROOT/<slug>/<file>
    - Also check vault: ARTWORK_VAULT_ROOT/(LOCKED-<slug>|<slug>)/<file>
    """
    p = Path(str(rel_path))
    try:
        idx = p.parts.index("processed-artwork")
    except ValueError:
        return False
    sub = Path(*p.parts[idx + 1:])  # <slug>/<file>
    # processed
    if _fs_exists_under(getattr(config, "PROCESSED_ROOT"), sub):
        return True
    # vault (LOCKED-<slug> first)
    slug = sub.parts[0] if len(sub.parts) else ""
    file_rest = Path(*sub.parts[1:]) if len(sub.parts) > 1 else Path("")
    vault_root = getattr(config, "ARTWORK_VAULT_ROOT")
    if _fs_exists_under(vault_root, Path(f"LOCKED-{slug}") / file_rest):
        return True
    if _fs_exists_under(vault_root, Path(slug) / file_rest):
        return True
    return False
