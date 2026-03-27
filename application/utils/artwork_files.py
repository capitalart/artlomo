"""artwork_files.py — Canonical originals & file helpers.

This module centralises path logic for original artwork files so that there is
exactly one canonical master location per artwork, with optional legacy
fallback into originals-staging.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import application.config as config

# Canonical roots (env-driven via config)
ART_PROCESSING_DIR: Path = Path(getattr(config, "ART_PROCESSING_DIR", config.BASE_DIR / "art-processing"))
ORIGINALS_DIR: Path = Path(getattr(config, "ORIGINALS_DIR", ART_PROCESSING_DIR / "originals"))
ORIGINALS_STAGING_ROOT: Path = Path(getattr(config, "ORIGINALS_STAGING_ROOT", ART_PROCESSING_DIR / "originals-staging"))
UNANALYSED_ROOT: Path = Path(getattr(config, "UNANALYSED_ROOT", ART_PROCESSING_DIR / "unanalysed-artwork"))
PROCESSED_ROOT: Path = Path(getattr(config, "PROCESSED_ROOT", ART_PROCESSING_DIR / "processed-artwork"))


def _candidate_original_dirs(slug: str) -> list[Path]:
    """Return candidate folders that may contain original files for slug.

    Order:
      1. Canonical ORIGINALS_DIR
      2. Legacy ORIGINALS_STAGING_ROOT
      3. UNANALYSED_ROOT/<slug>
      4. PROCESSED_ROOT/<slug>
    """
    paths: list[Path] = []
    paths.append(ORIGINALS_DIR / slug / "ORIGINALS" / slug)
    paths.append(ORIGINALS_STAGING_ROOT / slug / "ORIGINALS" / slug)
    paths.append(UNANALYSED_ROOT / slug)
    paths.append(PROCESSED_ROOT / slug)
    return paths


def get_original_path(slug: str) -> Optional[Path]:
    """Return the best candidate original image path for a slug.

    Prefers the canonical ORIGINALS_DIR; falls back to legacy staging and,
    finally, to unanalysed/processed folders.
    """
    exts = (".jpg", ".jpeg", ".png", ".webp")
    for root in _candidate_original_dirs(slug):
        if not root.exists() or not root.is_dir():
            continue
        # Prefer non-thumb, non-analyse hero-sized images first.
        candidates: list[Path] = []
        for p in sorted(root.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in exts:
                continue
            low = p.name.lower()
            penalty = 0
            if "thumb" in low or "-analyse" in low:
                penalty += 1
            size = 0
            try:
                size = p.stat().st_size
            except Exception:
                size = 0
            candidates.append((penalty, -int(size), p))  # type: ignore[arg-type]
        if not candidates:
            continue
        candidates.sort(key=lambda t: (t[0], t[1]))  # type: ignore[index,misc]
        return candidates[0][2]  # type: ignore[index]
    return None


def file_exists_in_originals(slug: str) -> bool:
    """Return True if a canonical original folder exists for slug."""
    return (ORIGINALS_DIR / slug / "ORIGINALS" / slug).exists()


def archive_original_folder(src_any_path: Path, seo_folder: str) -> Path:
    """Archive an original folder into the canonical ORIGINALS_DIR.

    This replaces the older behaviour that defaulted to ORIGINALS_STAGING_ROOT.
    The layout under ORIGINALS_DIR mirrors the previous staging convention:
      originals/<slug>/ORIGINALS/<original_folder_name>/...

    The source folder is moved; caller is responsible for ensuring that this is
    safe (e.g. after making sure UNANALYSED_ROOT no longer needs the folder).
    """
    from shutil import move
    import time

    # Resolve a directory to move
    src_dir = src_any_path if src_any_path.is_dir() else src_any_path.parent
    if not src_dir.exists():
        return ORIGINALS_DIR / seo_folder / "ORIGINALS"

    dst_base = ORIGINALS_DIR / seo_folder / "ORIGINALS"
    dst_base.mkdir(parents=True, exist_ok=True)
    dst = dst_base / src_dir.name
    if dst.exists():
        ts = str(int(time.time()))
        dst = dst_base / f"{src_dir.name}-{ts}"
    try:
        move(str(src_dir), str(dst))
        return dst
    except Exception:
        return dst


def move_upload_to_originals(upload_path: Path, slug: str) -> Path:
    """Ensure a canonical copy of an uploaded original exists in ORIGINALS_DIR.

    For now this copies a single uploaded file into the canonical originals
    tree without deleting the source; higher-level flows can later decide when
    it is safe to remove UNANALYSED_ROOT copies.
    """
    from shutil import copy2

    dst_dir = ORIGINALS_DIR / slug / "ORIGINALS" / slug
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / upload_path.name
    try:
        copy2(str(upload_path), str(dst))
    except Exception:
        # Best-effort; if copy fails, still return intended destination path.
        pass
    return dst
