"""
utils/image_utils.py — Image utilities (Robbie Mode™)
=====================================================

Provides helpers for image resizing and thumbnail generation.

Sections
--------
- [img-utils-1] Imports & Constants
- [img-utils-2] Public API
    - generate_upload_thumb(src_path, dest_path, long_edge=600, target_kb=100)

Notes
-----
- The UPLOAD thumb is meant ONLY for the unanalysed upload stage to speed up
  gallery rendering. It should not propagate to processed or finalised stages.
"""

from __future__ import annotations

# === [img-utils-1] Imports & Constants ======================================
import json
import logging
import os
import shutil
import errno
import subprocess
import time
from pathlib import Path
from typing import Any, Optional

import application.config as config

from application.utils.image_processing_utils import PerspectiveTransformError, warp_image_to_quad


logger = logging.getLogger(__name__)
VIDEO_WORKER_DIR = Path(__file__).resolve().parents[1] / "video_worker"


def _resolve_binary_path(name: str) -> str | None:
    binary = str(name or "").strip()
    if not binary:
        return None
    resolved = shutil.which(binary)
    if resolved:
        return resolved
    node_bin = Path(getattr(config, "BASE_DIR", Path(__file__).resolve().parents[2])) / "node_modules" / ".bin" / binary
    for candidate in (f"/usr/bin/{binary}", f"/usr/local/bin/{binary}", str(node_bin)):
        path = Path(candidate)
        if path.exists() and path.is_file():
            return str(path)
    return None


def _run_node_processor(payload: dict) -> dict | None:
    node_bin = _resolve_binary_path("node") or _resolve_binary_path("nodejs")
    if not node_bin:
        logger.error("Node runtime not found for image utils processor bridge")
        return None

    worker_args = [
        node_bin,
        str(VIDEO_WORKER_DIR / "processor.js"),
        json.dumps(payload, ensure_ascii=True, separators=(",", ":")),
    ]
    xvfb_bin = _resolve_binary_path("xvfb-run")
    cmd = [xvfb_bin, "-a", *worker_args] if xvfb_bin else worker_args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180, env=os.environ.copy())
    except Exception:
        logger.exception("Node processor bridge execution failed")
        return None

    if result.returncode != 0:
        detail = (result.stderr or "").strip() or (result.stdout or "").strip() or "processor bridge failed"
        logger.error("Node processor bridge failed: %s", detail[-1200:])
        return None

    raw = (result.stdout or "").strip()
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except Exception:
        logger.error("Node processor bridge returned invalid JSON")
        return None
    return parsed if isinstance(parsed, dict) else None


# === [img-utils-2] Public API ===============================================
def generate_upload_thumb(src_path: Path, dest_path: Path, *, long_edge: int = 600, target_kb: int = 100) -> bool:
    """Generate a lightweight JPEG thumbnail for the upload stage.

    Contract
    - Resize to fit within `long_edge` on the longest side (preserve aspect).
    - Save as JPEG and iteratively reduce quality to remain below `target_kb`.
    - Convert to RGB if needed.
    - Return True on success, False if the source doesn't exist or save fails.

    Args:
        src_path: Path to the source image (any supported input format).
        dest_path: Output path for the thumbnail (should end with .jpg).
        long_edge: Max dimension for the long edge in pixels (default 600).
        target_kb: Target maximum file size in kilobytes (default 100).

    Why this exists
    - This UPLOAD thumb is for fast UI-only previews in the Unanalysed pane.
      It is safe to delete and must not be copied to processed/finalised.
    """
    try:
        if not src_path.exists():
            return False
        payload = {
            "action": "generate_upload_thumb",
            "src_path": str(src_path),
            "dest_path": str(dest_path),
            "long_edge": int(long_edge),
            "target_kb": int(target_kb),
        }
        result = _run_node_processor(payload)
        return bool(result and result.get("ok") is True)
    except Exception:
        return False


def image_long_edge(path: Path) -> int:
    result = _run_node_processor({"action": "read_image_meta", "image_path": str(path)})
    if not result or result.get("ok") is not True:
        return 0
    try:
        return int(max(int(result.get("width") or 0), int(result.get("height") or 0)))
    except Exception:
        return 0


def _same_filesystem(a: Path, b: Path) -> bool:
    try:
        return os.stat(a).st_dev == os.stat(b.parent).st_dev
    except Exception:
        return False


def save_original_as_seo(src_path: Path, dest_path: Path) -> bool:
    """Create the buyer hero file at dest_path following invariants.

    Rules
    - If src is JPEG: DO NOT re-encode. Prefer hard link when on same FS; else shutil.copy2.
    - If src is not JPEG: transcode to JPEG, preserving dimensions. If long edge != BUYER_LONG_EDGE,
      resample with LANCZOS to exactly BUYER_LONG_EDGE on the long side.
    - After write, verify max(width,height) == BUYER_LONG_EDGE. Raise RuntimeError on mismatch.
    - Never modify the source file.
    """
    if not src_path.exists():
        return False
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    buyer_edge = int(getattr(config, "BUYER_LONG_EDGE", 14400))
    payload = {
        "action": "save_original_as_seo",
        "src_path": str(src_path),
        "dest_path": str(dest_path),
        "buyer_long_edge": int(buyer_edge),
    }
    result = _run_node_processor(payload)
    if not result or result.get("ok") is not True:
        raise RuntimeError("Failed to generate SEO master via Sharp bridge")
    return True


def archive_original(src_any_path: Path, seo_folder: str, target_root: Path | None = None) -> Path:
    """Archive an original folder into a target root.

    Default target is the canonical ORIGINALS_DIR; callers may explicitly pass
    ARTWORK_VAULT_ROOT or another root if needed. Legacy callers that relied
    on ORIGINALS_STAGING_ROOT will now be routed via the higher-level helpers
    in utils.artwork_files when reading originals; staging remains a
    backwards-compatible fallback for reads and migration.
    """
    from application.utils.artwork_files import archive_original_folder, ORIGINALS_DIR  # type: ignore

    # If a target_root is provided, mirror the old behaviour of archiving under
    # that root; otherwise use the canonical originals directory.
    if target_root is not None and target_root != ORIGINALS_DIR:
        try:
            base_root = Path(target_root)
            src_dir = src_any_path if src_any_path.is_dir() else src_any_path.parent
            if not src_dir.exists():
                return base_root / seo_folder / "ORIGINALS"
            dst_base = base_root / seo_folder / "ORIGINALS"
            dst_base.mkdir(parents=True, exist_ok=True)
            dst = dst_base / src_dir.name
            if dst.exists():
                ts = str(int(time.time()))
                dst = dst_base / f"{src_dir.name}-{ts}"
            shutil.move(str(src_dir), str(dst))
            return dst
        except Exception:
            return base_root / seo_folder / "ORIGINALS"  # type: ignore[name-defined]

    # Canonical path: archive into ORIGINALS_DIR
    return archive_original_folder(src_any_path, seo_folder)


def warp_to_region_layer(image: Any, region: dict[str, Any], *, output_size: tuple[int, int]) -> Any:
    corners = region.get("corners")
    points = region.get("points")
    dst = corners if isinstance(corners, list) and len(corners) == 4 else points
    if isinstance(dst, list) and len(dst) == 4:
        return warp_image_to_quad(image, dst, output_size)

    x_val = region.get("x")
    y_val = region.get("y")
    w_val = region.get("w")
    h_val = region.get("h")
    if all(v is not None and isinstance(v, (int, float)) for v in (x_val, y_val, w_val, h_val)):
        # Type narrowing: all values are confirmed to be int or float, not None
        assert x_val is not None and y_val is not None and w_val is not None and h_val is not None
        x = float(x_val)
        y = float(y_val)
        w = float(w_val)
        h = float(h_val)
        dst_rect = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
        return warp_image_to_quad(image, dst_rect, output_size)

    raise PerspectiveTransformError("Region must provide 4-point corners/points or x/y/w/h")
