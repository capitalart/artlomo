from __future__ import annotations

import json
import uuid
import random
import logging
import shutil
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path
import math
import os
from typing import Callable, Dict, Iterable, List, Tuple

import numpy as np

from application.mockups.catalog.loader import load_physical_bases, load_physical_catalog
from application.mockups.catalog.validation import load_and_validate_bases, load_and_validate_catalog
from application.mockups.errors import ValidationError
from application.mockups.catalog.models import MockupBase, Template
from application.mockups.config import (
    BASE_DIR,
    DEFAULT_MOCKUP_ASPECT,
    DEFAULT_MOCKUP_CATEGORY,
    MASTER_INDEX_PATH,
    MAX_REGIONS,
    PROCESSED_DIR,
    STANDARD_MOCKUP_ASPECT_RATIOS,
    STANDARD_MOCKUP_BASE_CATEGORIES,
    TARGET_IMAGE_NAME_SUFFIX,
)
from application.mockups.artwork_index import resolve_artwork
from application.mockups.assets_index import AssetsIndex
from application.mockups.pipeline import generate_mockups_for_artwork
from application.common.utilities.files import ensure_dir, write_json_atomic
from application.common.utilities.slug_sku import slugify
from application.mockups.admin.models import CatalogView, PolicyDocument, TemplateRecord
from application.mockups.admin.validators import (
    validate_coords_payload,
    validate_json_payload,
    validate_png_bytes,
    validate_roles,
    validate_slug_unique,
)

import re

CATALOG_FILENAME = "catalog.json"
POLICY_FILENAME = "policy.json"
DEFAULT_BASE_STATUS = "missing_coordinates"
MAX_COORD_GEN_BATCH = 250
COORDINATE_FORMAT_VERSION = "2.0"
COORDINATE_TYPE_PERSPECTIVE = "Perspective"
COORDINATE_TYPE_LEGACY = "Legacy"
COORDINATE_BLEED_PX = 4
ASPECT_SOURCE_AUTO = "auto"
ASPECT_SOURCE_MANUAL = "manual"
ASPECT_SOURCE_REGION = "region"
ASPECT_SOURCE_UPLOAD = "upload"

_BULK_GEN_STATUS_PATH = Path(__file__).resolve().parent / "ui" / "static" / "temp" / "bulk_status.json"
_BULK_GEN_MUTEX = threading.Lock()
_BULK_GEN_THREAD: threading.Thread | None = None

logger = logging.getLogger(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_bulk_status(payload: dict) -> None:
    ensure_dir(_BULK_GEN_STATUS_PATH.parent)
    write_json_atomic(_BULK_GEN_STATUS_PATH, payload)


def _status_payload(*, status: str, current: int, total: int, message: str, run_id: str | None = None, force: bool | None = None) -> dict:
    pct = int(round((float(current) / float(max(1, total))) * 100.0)) if total > 0 else 0
    payload = {
        "status": str(status).strip().lower(),
        "message": message,
        "current": int(current),
        "total": int(total),
        "percent": max(0, min(100, int(pct))),
        "updated_at": _now_iso(),
    }
    if run_id:
        payload["run_id"] = run_id
    if force is not None:
        payload["force"] = bool(force)
    return payload


def _read_bulk_status() -> dict:
    if not _BULK_GEN_STATUS_PATH.exists():
        return _status_payload(status="idle", current=0, total=0, message="No background generation running.")
    try:
        raw = json.loads(_BULK_GEN_STATUS_PATH.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            return _status_payload(status="idle", current=0, total=0, message="No background generation running.")
        current = int(raw.get("current", raw.get("completed", 0)) or 0)
        total = int(raw.get("total", 0) or 0)
        normalized = dict(raw)
        normalized["status"] = str(raw.get("status", "idle")).strip().lower()
        normalized["current"] = current
        normalized["completed"] = current
        normalized["total"] = total
        normalized["percent"] = int(raw.get("percent", _status_payload(status="processing", current=current, total=total, message="").get("percent", 0)) or 0)
        normalized["updated_at"] = raw.get("updated_at") or _now_iso()
        return normalized
    except Exception:
        return _status_payload(status="failed", current=0, total=0, message="Unable to read bulk generation status.")


def _catalog_path(catalog_path: Path | None) -> Path:
    if catalog_path:
        return catalog_path
    return Path(__file__).resolve().parents[1] / "catalog" / CATALOG_FILENAME


def _policy_path(policy_path: Path | None) -> Path:
    if policy_path:
        return policy_path
    return Path(__file__).resolve().parents[1] / "catalog" / POLICY_FILENAME


def _relative_to(base: Path, target: Path) -> Path:
    try:
        return target.relative_to(base)
    except ValueError:
        return target


def _extract_numeric_id(value: str) -> int | None:
    raw = (value or "").strip()
    if not raw:
        return None
    m = re.search(r"-MU-(\d+)$", raw)
    if not m:
        m = re.search(r"(\d+)$", raw)
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def _thumb_name(*, aspect: str, category: str, id_num: int) -> str:
    return f"{aspect}-THUMB-{category}-{id_num}.jpg"


def _render_thumb_500_jpg(*, base_png: Path, thumb_out: Path) -> None:
    ensure_dir(thumb_out.parent)
    result = _run_node_processor(
        {
            "action": "render_thumb_500",
            "base_path": str(base_png),
            "output_path": str(thumb_out),
            "output_size": 500,
            "quality": 92,
        }
    )
    if not result or result.get("ok") is not True:
        raise ValidationError(f"Unable to generate thumbnail for {base_png.name}")


def _normalize_category(category: str | None) -> str:
    return slugify(category or DEFAULT_MOCKUP_CATEGORY)


def _normalize_aspect(aspect_ratio: str | None) -> str:
    aspect = (aspect_ratio or DEFAULT_MOCKUP_ASPECT).strip() or DEFAULT_MOCKUP_ASPECT
    return aspect


def _sort_corners(pts: List[Dict[str, int]]) -> List[Dict[str, int]]:
    pts.sort(key=lambda p: (p["y"], p["x"]))
    top = sorted(pts[:2], key=lambda p: p["x"])
    bottom = sorted(pts[2:], key=lambda p: p["x"])
    return [*top, *bottom]


def _order_points_tl_tr_br_bl(points: List[Dict[str, float]]) -> List[Dict[str, int]]:
    pts = np.array([[float(p.get("x", 0)), float(p.get("y", 0))] for p in points], dtype=np.float32)
    if pts.shape != (4, 2):
        raise ValidationError("Expected exactly four points")

    xs = pts[:, 0]
    ys = pts[:, 1]
    s = xs + ys
    d = xs - ys

    tl = pts[int(np.argmin(s))]
    br = pts[int(np.argmax(s))]
    tr = pts[int(np.argmax(d))]
    bl = pts[int(np.argmin(d))]

    ordered = [tl, tr, br, bl]
    return [{"x": int(round(float(x))), "y": int(round(float(y)))} for (x, y) in ordered]


def _rect_zone_to_points(zone: Dict[str, int | float]) -> List[Dict[str, int]]:
    x = float(zone.get("x", 0))
    y = float(zone.get("y", 0))
    w = float(zone.get("w", 0))
    h = float(zone.get("h", 0))
    return _order_points_tl_tr_br_bl(
        [
            {"x": x, "y": y},
            {"x": x + w, "y": y},
            {"x": x + w, "y": y + h},
            {"x": x, "y": y + h},
        ]
    )


def _apply_bleed_to_points(points_tl_tr_br_bl: List[Dict[str, int]], *, bleed_px: int = COORDINATE_BLEED_PX) -> List[Dict[str, int]]:
    if len(points_tl_tr_br_bl) != 4:
        return points_tl_tr_br_bl
    tl, tr, br, bl = points_tl_tr_br_bl
    return [
        {"x": int(tl.get("x", 0)) - bleed_px, "y": int(tl.get("y", 0)) - bleed_px},
        {"x": int(tr.get("x", 0)) + bleed_px, "y": int(tr.get("y", 0)) - bleed_px},
        {"x": int(br.get("x", 0)) + bleed_px, "y": int(br.get("y", 0)) + bleed_px},
        {"x": int(bl.get("x", 0)) - bleed_px, "y": int(bl.get("y", 0)) + bleed_px},
    ]


def _legacy_corners_to_points(corners: List[Dict[str, int | float]]) -> List[Dict[str, int]]:
    if len(corners) != 4:
        raise ValidationError("Expected exactly four corners")
    tl, tr, bl, br = corners
    return _order_points_tl_tr_br_bl(
        [
            {"x": float(tl.get("x", 0)), "y": float(tl.get("y", 0))},
            {"x": float(tr.get("x", 0)), "y": float(tr.get("y", 0))},
            {"x": float(br.get("x", 0)), "y": float(br.get("y", 0))},
            {"x": float(bl.get("x", 0)), "y": float(bl.get("y", 0))},
        ]
    )


def _normalize_coords_payload_v2(coords_payload: dict, *, template: str) -> tuple[dict, str]:
    if not isinstance(coords_payload, dict):
        raise ValidationError("Coordinates payload must be an object")

    coord_type = COORDINATE_TYPE_PERSPECTIVE
    zones_out: List[dict] = []

    zones = coords_payload.get("zones")
    if isinstance(zones, list) and zones:
        for zone in zones:
            if not isinstance(zone, dict):
                continue
            pts = zone.get("points")
            if isinstance(pts, list) and len(pts) == 4:
                pts_list = [{"x": float(p.get("x", 0)), "y": float(p.get("y", 0))} for p in pts if isinstance(p, dict)]
                if len(pts_list) == 4:
                    ordered = _order_points_tl_tr_br_bl(pts_list)
                    zones_out.append({"points": _apply_bleed_to_points(ordered)})
                    continue
            corners = zone.get("corners")
            if isinstance(corners, list) and len(corners) == 4:
                pts_list = [{"x": float(p.get("x", 0)), "y": float(p.get("y", 0))} for p in corners if isinstance(p, dict)]
                if len(pts_list) == 4:
                    ordered = _order_points_tl_tr_br_bl(pts_list)
                    zones_out.append({"points": _apply_bleed_to_points(ordered)})
                    continue
            if all(isinstance(zone.get(k), (int, float)) for k in ("x", "y", "w", "h")):
                coord_type = COORDINATE_TYPE_LEGACY
                zones_out.append({"points": _apply_bleed_to_points(_rect_zone_to_points(zone))})
        if zones_out:
            return {"template": template, "format_version": COORDINATE_FORMAT_VERSION, "zones": zones_out}, coord_type

    corners = coords_payload.get("corners")
    if isinstance(corners, list) and len(corners) == 4:
        return {
            "template": template,
            "format_version": COORDINATE_FORMAT_VERSION,
            "zones": [{"points": _apply_bleed_to_points(_legacy_corners_to_points(corners))}],
        }, COORDINATE_TYPE_PERSPECTIVE

    regions = coords_payload.get("regions")
    if isinstance(regions, list) and regions:
        for region in regions:
            if not isinstance(region, dict):
                continue
            rc = region.get("corners")
            if not isinstance(rc, list) or len(rc) != 4:
                continue
            pts_list = [{"x": float(p.get("x", 0)), "y": float(p.get("y", 0))} for p in rc if isinstance(p, dict)]
            if len(pts_list) == 4:
                ordered = _order_points_tl_tr_br_bl(pts_list)
                zones_out.append({"points": _apply_bleed_to_points(ordered)})
        if zones_out:
            return {"template": template, "format_version": COORDINATE_FORMAT_VERSION, "zones": zones_out}, COORDINATE_TYPE_PERSPECTIVE

    raise ValidationError("Unable to normalize coordinates payload")


def _resolve_binary_path(name: str) -> str | None:
    binary = str(name or "").strip()
    if not binary:
        return None
    resolved = shutil.which(binary)
    if resolved:
        return resolved
    for candidate in (f"/usr/bin/{binary}", f"/usr/local/bin/{binary}", f"/srv/artlomo/node_modules/.bin/{binary}"):
        path = Path(candidate)
        if path.exists() and path.is_file():
            return str(path)
    return None


def _run_node_processor(payload: dict) -> dict | None:
    node_bin = _resolve_binary_path("node") or _resolve_binary_path("nodejs")
    if not node_bin:
        logger.error("Node runtime not found for mockup coordinate scanning")
        return None

    worker_args = [
        node_bin,
        "/srv/artlomo/video_worker/processor.js",
        json.dumps(payload, ensure_ascii=True, separators=(",", ":")),
    ]
    xvfb_bin = _resolve_binary_path("xvfb-run")
    cmd = [xvfb_bin, "-a", *worker_args] if xvfb_bin else worker_args

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=os.environ.copy())
    except Exception as exc:
        logger.exception("Node scanner execution failed: %s", exc)
        return None

    if result.returncode != 0:
        detail = (result.stderr or "").strip() or (result.stdout or "").strip() or "node scanner failed"
        logger.error("Node scanner failed: %s", detail[-1200:])
        return None

    raw = (result.stdout or "").strip()
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except Exception:
        logger.error("Node scanner returned invalid JSON")
        return None
    return parsed if isinstance(parsed, dict) else None


def _scan_transparent_zones_normalized(image_path: Path) -> List[Dict[str, object]] | None:
    payload = {
        "action": "scan_transparent_zones",
        "image_path": str(image_path),
        "alpha_threshold": 5,
        "min_area": 10,
        "max_regions": int(MAX_REGIONS),
    }
    result = _run_node_processor(payload)
    if not result or result.get("ok") is not True:
        return None
    zones = result.get("zones")
    if not isinstance(zones, list) or not zones:
        return None
    cleaned: List[Dict[str, object]] = []
    for zone in zones:
        if not isinstance(zone, dict):
            continue
        points = zone.get("points")
        if not isinstance(points, list) or len(points) != 4:
            continue
        cleaned_points: List[Dict[str, float]] = []
        for pt in points:
            if not isinstance(pt, dict):
                continue
            try:
                x = float(pt.get("x", 0.0))
                y = float(pt.get("y", 0.0))
            except Exception:
                continue
            cleaned_points.append({"x": max(0.0, min(1.0, x)), "y": max(0.0, min(1.0, y))})
        if len(cleaned_points) == 4:
            cleaned.append({"points": cleaned_points})
    return cleaned or None


def _normalized_zones_to_pixel_zones(zones: List[Dict[str, object]], *, size: tuple[int, int]) -> List[Dict[str, object]]:
    width, height = size
    out: List[Dict[str, object]] = []
    for zone in zones:
        if not isinstance(zone, dict):
            continue
        points = zone.get("points")
        if not isinstance(points, list) or len(points) != 4:
            continue
        px_points: List[Dict[str, float]] = []
        for pt in points:
            if not isinstance(pt, dict):
                continue
            try:
                nx = float(pt.get("x", 0.0))
                ny = float(pt.get("y", 0.0))
            except Exception:
                continue
            px_points.append({"x": nx * float(width), "y": ny * float(height)})
        if len(px_points) == 4:
            out.append({"points": _order_points_tl_tr_br_bl(px_points)})
    return out


def _detect_corners_from_alpha(image_path: Path, *, size: tuple[int, int]) -> List[Dict[str, int]] | None:
    zones = _scan_transparent_zones_normalized(image_path)
    if not zones:
        return None
    first = _normalized_zones_to_pixel_zones([zones[0]], size=size)
    if not first:
        return None
    points = first[0].get("points")
    if not isinstance(points, list) or len(points) != 4:
        return None
    return [{"x": int(p.get("x", 0)), "y": int(p.get("y", 0))} for p in points if isinstance(p, dict)]


def _image_dimensions_via_node(image_path: Path) -> tuple[int, int] | None:
    result = _run_node_processor({"action": "read_image_meta", "image_path": str(image_path)})
    if not result or result.get("ok") is not True:
        return None
    try:
        width = int(result.get("width") or 0)
        height = int(result.get("height") or 0)
    except Exception:
        return None
    if width <= 0 or height <= 0:
        return None
    return width, height


def _legacy_coords_lookup(slug: str, aspect: str) -> dict | None:
    """Return legacy coord payload if present under var/coordinates.<aspect>."""
    legacy_root = BASE_DIR / "var" / "coordinates" / aspect
    os.makedirs(legacy_root, exist_ok=True)
    target = slug.lower()
    for path in legacy_root.rglob("*.json"):
        if path.stem.lower() != target:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            corners = data.get("corners")
            if isinstance(corners, list) and len(corners) == 4:
                if not isinstance(data.get("template"), str) or not data.get("template"):
                    data["template"] = f"{slug}.png"
                return data
        except Exception:
            continue
    return None


def _is_size_chart_category(category: str | None) -> bool:
    return (category or "").strip().lower() == "size-chart"


def _aspect_from_region(region) -> str | None:
    try:
        xs = [p.x for p in region.corners]
        ys = [p.y for p in region.corners]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        if width <= 0 or height <= 0:
            return None
        gcd_val = math.gcd(int(width), int(height)) or 1
        return f"{int(width) // gcd_val}x{int(height) // gcd_val}"
    except Exception:
        return None


def _clamp_coord_value(val: float, max_exclusive: float) -> float:
    try:
        v = float(val)
    except Exception:
        return val
    if max_exclusive <= 0:
        return v
    if v < 0:
        return 0.0
    if v >= max_exclusive:
        return float(max_exclusive) - 0.1
    return v


def _clamp_coords_payload(payload: dict, *, size: tuple[int, int]) -> dict:
    width, height = size
    if not isinstance(payload, dict):
        return payload
    zones = payload.get("zones")
    if isinstance(zones, list):
        for zone in zones:
            if not isinstance(zone, dict):
                continue
            points = zone.get("points")
            if isinstance(points, list):
                for pt in points:
                    if not isinstance(pt, dict):
                        continue
                    if isinstance(pt.get("x"), (int, float)):
                        pt["x"] = _clamp_coord_value(pt["x"], float(width))
                    if isinstance(pt.get("y"), (int, float)):
                        pt["y"] = _clamp_coord_value(pt["y"], float(height))
            if isinstance(zone.get("x"), (int, float)):
                zone["x"] = _clamp_coord_value(zone["x"], float(width))
            if isinstance(zone.get("y"), (int, float)):
                zone["y"] = _clamp_coord_value(zone["y"], float(height))
            if all(isinstance(zone.get(k), (int, float)) for k in ("x", "w")):
                zone["w"] = _clamp_coord_value(float(zone["w"]), float(width) - float(zone["x"]))
            if all(isinstance(zone.get(k), (int, float)) for k in ("y", "h")):
                zone["h"] = _clamp_coord_value(float(zone["h"]), float(height) - float(zone["y"]))

    corners = payload.get("corners")
    if isinstance(corners, list):
        for pt in corners:
            if not isinstance(pt, dict):
                continue
            if isinstance(pt.get("x"), (int, float)):
                pt["x"] = _clamp_coord_value(pt["x"], float(width))
            if isinstance(pt.get("y"), (int, float)):
                pt["y"] = _clamp_coord_value(pt["y"], float(height))

    regions = payload.get("regions")
    if isinstance(regions, list):
        for region in regions:
            if not isinstance(region, dict):
                continue
            rc = region.get("corners")
            if not isinstance(rc, list):
                continue
            for pt in rc:
                if not isinstance(pt, dict):
                    continue
                if isinstance(pt.get("x"), (int, float)):
                    pt["x"] = _clamp_coord_value(pt["x"], float(width))
                if isinstance(pt.get("y"), (int, float)):
                    pt["y"] = _clamp_coord_value(pt["y"], float(height))

    return payload


class CatalogAdminService:
    def __init__(self, *, catalog_path: Path | None = None) -> None:
        self.catalog_path = _catalog_path(catalog_path)
        self.catalog_dir = self.catalog_path.parent
        self.base_root = self.catalog_dir / "assets" / "mockups" / "bases"

    def create_aspect(self, aspect_ratio: str) -> str:
        aspect = _normalize_aspect(aspect_ratio)
        if not aspect:
            raise ValidationError("Aspect ratio is required")
        ensure_dir(self.base_root)
        aspect_dir = self.base_root / aspect
        ensure_dir(aspect_dir)
        categories = self.list_physical_categories()
        for cat in categories:
            ensure_dir(aspect_dir / cat)
        return aspect

    def delete_aspect(self, aspect_ratio: str) -> str:
        aspect = _normalize_aspect(aspect_ratio)
        if not aspect:
            raise ValidationError("Aspect ratio is required")
        aspect_dir = self.base_root / aspect
        if not aspect_dir.exists() or not aspect_dir.is_dir():
            raise ValidationError("Aspect folder does not exist")
        has_files = any(p.is_file() for p in aspect_dir.rglob("*"))
        if has_files:
            raise ValidationError("Refusing to delete non-empty aspect folder")
        dirs = sorted([p for p in aspect_dir.rglob("*") if p.is_dir()], key=lambda p: len(p.parts), reverse=True)
        for d in dirs:
            try:
                d.rmdir()
            except Exception:
                pass
        aspect_dir.rmdir()
        return aspect

    def create_category_across_aspects(self, category: str) -> str:
        cat = _normalize_category(category)
        if not cat:
            raise ValidationError("Category is required")
        ensure_dir(self.base_root)
        aspects = self.list_physical_aspects()
        if not aspects:
            aspects = [DEFAULT_MOCKUP_ASPECT]
            ensure_dir(self.base_root / DEFAULT_MOCKUP_ASPECT)
        for aspect in aspects:
            ensure_dir(self.base_root / aspect / cat)
        return cat

    def delete_category_across_aspects(self, category: str) -> str:
        cat = _normalize_category(category)
        if not cat:
            raise ValidationError("Category is required")
        if not self.base_root.exists() or not self.base_root.is_dir():
            raise ValidationError("Base folder root does not exist")
        blocked: List[str] = []
        targets: List[Path] = []
        for aspect in self.list_physical_aspects():
            folder = self.base_root / aspect / cat
            if not folder.exists() or not folder.is_dir():
                continue
            has_files = any(p.is_file() for p in folder.rglob("*"))
            if has_files:
                blocked.append(aspect)
                continue
            targets.append(folder)
        if blocked:
            raise ValidationError("Refusing to delete category that contains files in: " + ", ".join(sorted(blocked)))
        for folder in targets:
            dirs = sorted([p for p in folder.rglob("*") if p.is_dir()], key=lambda p: len(p.parts), reverse=True)
            for d in dirs:
                try:
                    d.rmdir()
                except Exception:
                    pass
            folder.rmdir()
        return cat

    def list_physical_aspects(self) -> List[str]:
        if not self.base_root.exists() or not self.base_root.is_dir():
            return []
        return sorted([p.name for p in self.base_root.iterdir() if p.is_dir()])

    def list_physical_categories(self) -> List[str]:
        if not self.base_root.exists() or not self.base_root.is_dir():
            return []
        cats = set()
        for aspect_dir in [p for p in self.base_root.iterdir() if p.is_dir()]:
            for cat_dir in [p for p in aspect_dir.iterdir() if p.is_dir()]:
                cats.add(cat_dir.name)
        return sorted(cats)

    def list_known_categories(self) -> List[str]:
        bases = []
        try:
            bases = self.load_bases()
        except ValidationError:
            bases = []

        cats = {b.category for b in bases if getattr(b, "category", None)}
        physical = set(self.list_physical_categories())
        standard = set(STANDARD_MOCKUP_BASE_CATEGORIES)
        return sorted({DEFAULT_MOCKUP_CATEGORY} | standard | physical | set(cats))

    def physical_category_counts(self) -> Dict[str, int]:
        physical_counts = load_physical_catalog(catalog_dir=self.catalog_dir, return_counts=True)
        if not isinstance(physical_counts, dict):
            physical_counts = {}
        known = self.list_known_categories()
        return {cat: int(physical_counts.get(cat, 0) or 0) for cat in known}

    def list_known_aspects(self) -> List[str]:
        bases = []
        try:
            bases = self.load_bases()
        except ValidationError:
            bases = []

        aspects = {b.aspect_ratio for b in bases if getattr(b, "aspect_ratio", None)}
        aspects = {a for a in aspects if a}
        if any(not getattr(b, "aspect_ratio", None) for b in bases):
            aspects.add(DEFAULT_MOCKUP_ASPECT)

        physical = set(self.list_physical_aspects())
        standard = set(STANDARD_MOCKUP_ASPECT_RATIOS)
        return sorted({DEFAULT_MOCKUP_ASPECT} | standard | physical | set(aspects))

    def load_catalog(self) -> List[Template]:
        return load_and_validate_catalog(self.catalog_path)

    def load_bases(self) -> List[MockupBase]:
        return load_and_validate_bases(self.catalog_path)

    def sanitize_and_sync_bases(self) -> Dict[str, int]:
        doc = self._load_catalog_json()
        bases = doc.get("bases", [])
        if not isinstance(bases, list):
            raise ValidationError("Catalog document must contain bases list")

        used_ids: Dict[tuple[str, str], set[int]] = {}

        def _next_id(key: tuple[str, str]) -> int:
            bucket = used_ids.setdefault(key, set())
            candidate = 1
            while candidate in bucket:
                candidate += 1
            bucket.add(candidate)
            return candidate

        def _seed_used_ids_from_disk() -> None:
            if not self.base_root.exists():
                return
            for aspect_dir in [p for p in self.base_root.iterdir() if p.is_dir()]:
                aspect = aspect_dir.name
                for category_dir in [p for p in aspect_dir.iterdir() if p.is_dir()]:
                    category_folder = category_dir.name
                    key = (aspect, category_folder)
                    for png in category_dir.glob("*.png"):
                        base_id = _extract_numeric_id(png.stem)
                        if base_id is None:
                            continue
                        used_ids.setdefault(key, set()).add(base_id)

        def _thumb_path_for(*, folder: Path, aspect: str, category_folder: str, id_num: int) -> Path:
            return folder / _thumb_name(aspect=aspect, category=category_folder, id_num=id_num)

        def _remove_old_thumb_variants(*, folder: Path, base_slug: str, aspect: str, category_folder: str, id_num: int, keep: Path) -> None:
            candidates = [
                folder / f"{base_slug}-THUMB.jpg",
            ]
            try:
                rest = base_slug
                prefix = f"{aspect}-"
                if rest.startswith(prefix):
                    rest = rest[len(prefix):]
                candidates.append(folder / f"{aspect}-THUMB-{rest}.jpg")
            except Exception:
                pass
            try:
                if "-MU-" in base_slug:
                    pre, suf = base_slug.rsplit("-MU-", 1)
                    candidates.append(folder / f"{pre}-MU-THUMB-{suf}.jpg")
            except Exception:
                pass
            candidates.append(folder / _thumb_name(aspect=aspect, category=category_folder, id_num=id_num))
            for candidate in candidates:
                try:
                    if candidate.resolve() == keep.resolve():
                        continue
                except Exception:
                    pass
                try:
                    if candidate.exists():
                        candidate.unlink()
                except Exception:
                    pass

        renamed = 0
        thumbs = 0
        coords_updated = 0
        removed_empty_dirs = 0

        _seed_used_ids_from_disk()

        now = _now_iso()
        for entry in bases:
            if not isinstance(entry, dict):
                continue

            aspect = _normalize_aspect(entry.get("aspect_ratio"))
            category_folder = _normalize_category(entry.get("category"))
            category_code = category_folder.upper()
            folder = self.base_root / aspect / category_folder
            ensure_dir(folder)

            current_base = self._resolve_base_image_path(entry)
            current_coords = self._resolve_coords_path(entry)

            base_id = _extract_numeric_id(str(entry.get("slug") or ""))
            key = (aspect, category_folder)
            if base_id is None:
                base_id = _next_id(key)
            else:
                used_ids.setdefault(key, set()).add(base_id)

            # Collision-safe: never overwrite an existing MU base/coords/thumb.
            while True:
                new_slug = f"{aspect}-{category_code}-MU-{base_id}"
                new_base = folder / f"{new_slug}.png"
                new_coords = folder / f"{new_slug}.json"
                new_thumb = _thumb_path_for(folder=folder, aspect=aspect, category_folder=category_folder, id_num=base_id)
                if (not new_base.exists()) and (not new_coords.exists()) and (not new_thumb.exists()):
                    break
                # If this entry already targets the existing slug path, allow it.
                existing_slug = str(entry.get("slug") or "")
                if existing_slug == new_slug:
                    break
                base_id = _next_id(key)

            if current_base.exists() and current_base.resolve() != new_base.resolve():
                ensure_dir(new_base.parent)
                if new_base.exists():
                    raise ValidationError(f"Refusing to overwrite existing base: {new_base.name}")
                new_base.write_bytes(current_base.read_bytes())
                try:
                    current_base.unlink()
                except Exception:
                    pass
                renamed += 1
            current_base = new_base

            if current_coords.exists():
                try:
                    payload = json.loads(current_coords.read_text(encoding="utf-8"))
                except Exception:
                    payload = {}
                if isinstance(payload, dict):
                    payload["template"] = f"{new_slug}.png"
                    try:
                        payload, _coordinate_type = _normalize_coords_payload_v2(payload, template=f"{new_slug}.png")
                        payload = _clamp_coords_payload(payload, size=validate_png_bytes(current_base.read_bytes()).size)
                    except Exception:
                        pass
                ensure_dir(new_coords.parent)
                if new_coords.exists() and current_coords.resolve() != new_coords.resolve():
                    raise ValidationError(f"Refusing to overwrite existing coords: {new_coords.name}")
                write_json_atomic(new_coords, payload)
                if current_coords.resolve() != new_coords.resolve():
                    try:
                        current_coords.unlink()
                    except Exception:
                        pass
                    renamed += 1
                coords_updated += 1
            else:
                if not new_coords.exists():
                    write_json_atomic(new_coords, {"template": f"{new_slug}.png", "format_version": COORDINATE_FORMAT_VERSION, "zones": []})

            try:
                _render_thumb_500_jpg(base_png=current_base, thumb_out=new_thumb)
                _remove_old_thumb_variants(
                    folder=folder,
                    base_slug=new_slug,
                    aspect=aspect,
                    category_folder=category_folder,
                    id_num=base_id,
                    keep=new_thumb,
                )
                thumbs += 1
            except Exception as exc:
                raise ValidationError(str(exc)) from exc

            entry["slug"] = new_slug
            entry["base_image"] = _relative_to(self.catalog_dir, current_base).as_posix()
            entry["coordinates_path"] = _relative_to(self.catalog_dir, new_coords).as_posix()
            entry["updated_at"] = now

        # Cleanup: remove empty UNSET folders after normalization
        try:
            unset_dir = self.base_root / "UNSET"
            if unset_dir.exists() and unset_dir.is_dir():
                for child in [p for p in unset_dir.iterdir() if p.is_dir()]:
                    try:
                        if not any(child.iterdir()):
                            child.rmdir()
                            removed_empty_dirs += 1
                    except Exception:
                        pass
                try:
                    if not any(unset_dir.iterdir()):
                        unset_dir.rmdir()
                        removed_empty_dirs += 1
                except Exception:
                    pass
        except Exception:
            pass

        self._write_catalog_json(doc)
        return {
            "renamed": int(renamed),
            "thumbs": int(thumbs),
            "coords_updated": int(coords_updated),
            "removed_empty_dirs": int(removed_empty_dirs),
        }

    def normalize_base_storage(self) -> None:
        doc = self._load_catalog_json()
        changed = False
        now = _now_iso()
        for entry in doc.get("bases", []):
            before_base = entry.get("base_image")
            before_coords = entry.get("coordinates_path")
            self._ensure_base_files(entry)
            if entry.get("base_image") != before_base or entry.get("coordinates_path") != before_coords:
                entry["updated_at"] = now
                changed = True
        if changed:
            self._write_catalog_json(doc)

    def list_templates(self, *, category: str | None = None, aspect_ratio: str | None = None, enabled: bool | None = None) -> CatalogView:
        templates = self.load_catalog()
        filtered: List[Template] = []
        for tpl in templates:
            if category and tpl.category != category:
                continue
            if aspect_ratio and tpl.aspect_ratio != aspect_ratio:
                continue
            if enabled is not None and tpl.enabled != enabled:
                continue
            filtered.append(tpl)
        records = [self._to_record(tpl) for tpl in filtered]
        scope_for_categories = filtered if aspect_ratio or category or enabled is not None else templates
        categories = sorted({tpl.category for tpl in scope_for_categories})
        return CatalogView(templates=records, categories=categories)

    def set_enabled(self, slug: str, enabled: bool, *, policy_path: Path | None = None) -> TemplateRecord:
        doc = self._load_catalog_json()
        found = False
        for entry in doc["templates"]:
            if entry.get("slug") == slug:
                found = True
                entry["enabled"] = bool(enabled)
                break
        if not found:
            raise ValidationError(f"Template not found: {slug}")

        policy = PolicyAdminService(policy_path=policy_path).load_policy()
        if slug in policy.mandatory_templates and not enabled:
            raise ValidationError("Cannot disable a mandatory template")

        self._write_catalog_json(doc)
        # reload to include validation/paths
        updated = [tpl for tpl in self.load_catalog() if tpl.slug == slug][0]
        return self._to_record(updated)

    def rename_category(self, old: str, new: str, *, aspect_ratio: str) -> None:
        new_slug = slugify(new)
        doc = self._load_catalog_json()
        changed = False
        for entry in doc["templates"]:
            if entry.get("category") == old and entry.get("aspect_ratio") == aspect_ratio:
                entry["category"] = new_slug
                changed = True
        if not changed:
            raise ValidationError(f"Category not found for aspect {aspect_ratio}: {old}")
        self._write_catalog_json(doc)

    def assign_category(self, slug: str, category: str) -> TemplateRecord:
        doc = self._load_catalog_json()
        new_cat = slugify(category)
        found = False
        for entry in doc["templates"]:
            if entry.get("slug") == slug:
                entry["category"] = new_cat
                found = True
                break
        if not found:
            raise ValidationError(f"Template not found: {slug}")
        self._write_catalog_json(doc)
        updated = [tpl for tpl in self.load_catalog() if tpl.slug == slug][0]
        return self._to_record(updated)

    def _desired_base_paths(self, *, slug: str, aspect: str, category: str) -> tuple[Path, Path]:
        base_dir = self.base_root / aspect / category
        base_png = base_dir / f"{slug}.png"
        coords_json = base_dir / f"{slug}.json"
        return base_png, coords_json

    def _ensure_base_files(self, entry: Dict) -> tuple[Path, Path]:
        slug_val = entry.get("slug") or ""
        if not slug_val:
            raise ValidationError("Base entry missing slug")
        aspect = _normalize_aspect(entry.get("aspect_ratio"))
        category = _normalize_category(entry.get("category"))
        desired_base, desired_coords = self._desired_base_paths(slug=slug_val, aspect=aspect, category=category)

        current_base = self._resolve_base_image_path(entry)
        current_coords = self._resolve_coords_path(entry)

        # Move base image if path differs
        if current_base.resolve() != desired_base.resolve():
            ensure_dir(desired_base.parent)
            if current_base.exists():
                desired_base.write_bytes(current_base.read_bytes())
                try:
                    current_base.unlink()
                except Exception:
                    pass
            current_base = desired_base

        entry["base_image"] = _relative_to(self.catalog_dir, desired_base).as_posix()

        # Move coords if present and different
        if current_coords and current_coords.exists() and current_coords.resolve() != desired_coords.resolve():
            ensure_dir(desired_coords.parent)
            desired_coords.write_bytes(current_coords.read_bytes())
            try:
                current_coords.unlink()
            except Exception:
                pass
            current_coords = desired_coords

        entry["coordinates_path"] = _relative_to(self.catalog_dir, desired_coords).as_posix()
        return current_base, desired_coords

    def add_base(
        self,
        *,
        slug: str,
        original_filename: str,
        category: str | None,
        aspect_ratio: str | None,
        base_image_bytes: bytes,
    ) -> MockupBase:
        slug_clean = slugify(slug)
        if not slug_clean:
            raise ValidationError("Slug is required for base upload")
        category_slug = _normalize_category(category)
        aspect_clean = _normalize_aspect(aspect_ratio)

        # Validate image and ensure alpha
        base_img = validate_png_bytes(base_image_bytes)

        doc = self._load_catalog_json()
        existing_slugs = {entry.get("slug") for entry in doc["bases"]}
        template_slugs = {entry.get("slug") for entry in doc["templates"]}
        if slug_clean in existing_slugs or slug_clean in template_slugs:
            raise ValidationError(f"Mockup slug already exists: {slug_clean}.")

        base_abs, coords_abs = self._desired_base_paths(slug=slug_clean, aspect=aspect_clean, category=category_slug)
        ensure_dir(base_abs.parent)
        base_img.save(base_abs, format="PNG")

        id_num = _extract_numeric_id(slug_clean)
        if id_num is None:
            rest = slug_clean
            prefix = f"{aspect_clean}-"
            if rest.startswith(prefix):
                rest = rest[len(prefix):]
            thumb_abs = base_abs.with_name(f"{aspect_clean}-THUMB-{rest}.jpg")
        else:
            thumb_abs = base_abs.with_name(_thumb_name(aspect=aspect_clean, category=category_slug, id_num=id_num))
        if thumb_abs.exists():
            raise ValidationError(f"Thumb already exists: {thumb_abs.name}")
        _render_thumb_500_jpg(base_png=base_abs, thumb_out=thumb_abs)

        if id_num is not None:
            try:
                alt1 = base_abs.with_name(f"{slug_clean}-THUMB.jpg")
                alt2 = base_abs.with_name(f"{aspect_clean}-THUMB-{slug_clean}.jpg")
                for candidate in (alt1, alt2):
                    if candidate.exists() and candidate.resolve() != thumb_abs.resolve():
                        candidate.unlink()
            except Exception:
                pass

        coords_payload = None
        zones_normalized = _scan_transparent_zones_normalized(base_abs)
        zones = _normalized_zones_to_pixel_zones(zones_normalized or [], size=base_img.size)
        if zones:
            coords_payload = {
                "template": f"{slug_clean}.png",
                "zones": zones,
            }
        else:
            corners = _detect_corners_from_alpha(base_abs, size=base_img.size)
            if not corners:
                w, h = base_img.size
                corners = [
                    {"x": 0, "y": 0},
                    {"x": int(w), "y": 0},
                    {"x": 0, "y": int(h)},
                    {"x": int(w), "y": int(h)},
                ]
            coords_payload = {
                "template": f"{slug_clean}.png",
                "corners": corners,
            }

        coords_payload = _clamp_coords_payload(coords_payload, size=base_img.size)
        coords_payload, coordinate_type = _normalize_coords_payload_v2(coords_payload, template=f"{slug_clean}.png")
        coords_payload = _clamp_coords_payload(coords_payload, size=base_img.size)
        placements = validate_coords_payload(coords_payload, base_img.size)
        ensure_dir(coords_abs.parent)
        write_json_atomic(coords_abs, coords_payload)

        now = _now_iso()
        base_entry = {
            "id": uuid.uuid4().hex,
            "slug": slug_clean,
            "original_filename": original_filename,
            "base_image": _relative_to(self.catalog_dir, base_abs).as_posix(),
            "category": category_slug,
            "aspect_ratio": aspect_clean,
            "aspect_source": ASPECT_SOURCE_UPLOAD,
            "status": "coordinates_ready",
            "coordinates_path": _relative_to(self.catalog_dir, coords_abs).as_posix(),
            "region_count": len(placements),
            "last_coordinated_at": now,
            "coordinate_type": coordinate_type,
            "created_at": now,
            "updated_at": now,
        }

        doc["bases"].append(base_entry)
        self._write_catalog_json(doc)

        added = [b for b in self.load_bases() if b.slug == slug_clean][0]
        return added

    def generate_missing_base_thumbs(self) -> Dict[str, int]:
        generated = 0
        renamed_legacy = 0
        skipped = 0
        failed = 0
        scanned = 0
        if not self.base_root.exists():
            return {"generated": 0, "renamed_legacy": 0, "skipped": 0, "failed": 0, "scanned": 0}

        for aspect_dir in [p for p in self.base_root.iterdir() if p.is_dir()]:
            aspect = aspect_dir.name
            for category_dir in [p for p in aspect_dir.iterdir() if p.is_dir()]:
                category_folder = category_dir.name
                for base_png in category_dir.glob("*.png"):
                    scanned += 1
                    base_slug = base_png.stem
                    id_num = _extract_numeric_id(base_slug)
                    if id_num is None:
                        skipped += 1
                        continue

                    desired_thumb = category_dir / _thumb_name(
                        aspect=aspect,
                        category=category_folder,
                        id_num=id_num,
                    )
                    if desired_thumb.exists():
                        skipped += 1
                        continue

                    legacy_candidates = [
                        category_dir / f"{base_slug}-THUMB.jpg",
                        category_dir / f"{aspect}-THUMB-{base_slug}.jpg",
                    ]
                    try:
                        if "-MU-" in base_slug:
                            pre, suf = base_slug.rsplit("-MU-", 1)
                            legacy_candidates.append(category_dir / f"{pre}-MU-THUMB-{suf}.jpg")
                    except Exception:
                        pass

                    legacy_existing = next((p for p in legacy_candidates if p.exists()), None)
                    if legacy_existing is not None:
                        try:
                            ensure_dir(desired_thumb.parent)
                            legacy_existing.replace(desired_thumb)
                            renamed_legacy += 1
                        except Exception:
                            failed += 1
                        continue

                    try:
                        _render_thumb_500_jpg(base_png=base_png, thumb_out=desired_thumb)
                        generated += 1
                    except Exception:
                        failed += 1

        return {
            "generated": int(generated),
            "renamed_legacy": int(renamed_legacy),
            "skipped": int(skipped),
            "failed": int(failed),
            "scanned": int(scanned),
        }

    def add_template(
        self,
        *,
        slug: str,
        aspect_ratio: str,
        category: str,
        roles: Iterable[str],
        base_image_bytes: bytes,
        coords_payload: dict | bytes | str,
        enabled: bool = False,
    ) -> TemplateRecord:
        slug = slugify(slug)
        category_slug = slugify(category)
        roles_clean = validate_roles(roles)

        existing = self.load_catalog()
        validate_slug_unique(slug, [tpl.slug for tpl in existing])

        base_img = validate_png_bytes(base_image_bytes)
        coords_dict = coords_payload if isinstance(coords_payload, dict) else validate_json_payload(coords_payload)
        coords_dict = _clamp_coords_payload(coords_dict, size=base_img.size)
        coords_dict, _coordinate_type = _normalize_coords_payload_v2(coords_dict, template=f"{slug}.png")
        coords_dict = _clamp_coords_payload(coords_dict, size=base_img.size)
        regions = validate_coords_payload(coords_dict, base_img.size)

        base_rel = Path("assets") / "mockups" / aspect_ratio / category_slug / f"{slug}.png"
        coords_rel = Path("assets") / "mockups" / aspect_ratio / category_slug / f"{slug}.json"
        base_abs = self.catalog_dir / base_rel
        coords_abs = self.catalog_dir / coords_rel

        if base_abs.exists() or coords_abs.exists():
            raise ValidationError("Template assets already exist on disk")

        ensure_dir(base_abs.parent)
        ensure_dir(coords_abs.parent)
        base_img.save(base_abs, format="PNG")
        coords_dict["template"] = f"{slug}.png"
        write_json_atomic(coords_abs, coords_dict)

        doc = self._load_catalog_json()
        doc["templates"].append(
            {
                "slug": slug,
                "aspect_ratio": aspect_ratio,
                "category": category_slug,
                "base_image": _relative_to(self.catalog_dir, base_abs).as_posix(),
                "coords": _relative_to(self.catalog_dir, coords_abs).as_posix(),
                "roles": roles_clean,
                "enabled": bool(enabled),
            }
        )
        self._write_catalog_json(doc)
        added = [tpl for tpl in self.load_catalog() if tpl.slug == slug][0]
        return self._to_record(added, region_count=len(regions))

    def _load_catalog_json(self) -> Dict[str, List[Dict]]:
        if not self.catalog_path.exists():
            return {"templates": [], "bases": []}
        try:
            raw = json.loads(self.catalog_path.read_text(encoding="utf-8"))
        except Exception as exc:  # pylint: disable=broad-except
            raise ValidationError("Catalog file is invalid JSON") from exc
        if isinstance(raw, list):
            return {"templates": raw, "bases": []}
        if isinstance(raw, dict):
            templates = raw.get("templates", [])
            bases = raw.get("bases", [])
            if not isinstance(templates, list) or not isinstance(bases, list):
                raise ValidationError("Catalog document must contain list sections for templates and bases")
            return {"templates": templates, "bases": bases}
        raise ValidationError("Catalog file is invalid JSON structure")

    def _write_catalog_json(self, payload: Dict[str, List[Dict]]) -> None:
        payload = {
            "templates": payload.get("templates", []),
            "bases": payload.get("bases", []),
        }
        write_json_atomic(self.catalog_path, payload)

    def _resolve_base_image_path(self, entry: Dict) -> Path:
        base_val = entry.get("base_image_path") or entry.get("base_image")
        if not isinstance(base_val, str) or not base_val.strip():
            raise ValidationError("Base entry is missing base_image path")
        base_path = Path(base_val.strip())
        return base_path if base_path.is_absolute() else self.catalog_dir / base_path

    def _resolve_coords_path(self, entry: Dict) -> Path:
        coords_val = entry.get("coordinates_path") or entry.get("coordinates")
        if isinstance(coords_val, str) and coords_val.strip():
            coords_path = Path(coords_val.strip())
            return coords_path if coords_path.is_absolute() else self.catalog_dir / coords_path
        base_path = self._resolve_base_image_path(entry)
        return base_path.with_suffix(".json")

    def _to_record(self, tpl: Template, region_count: int | None = None) -> TemplateRecord:
        if region_count is None:
            try:
                coords_data = json.loads(tpl.coords.read_text(encoding="utf-8"))
                regions = coords_data.get("regions", [])
                if isinstance(regions, list) and regions:
                    region_count = len(regions)
                elif isinstance(coords_data.get("corners"), list) and len(coords_data.get("corners")) == 4:
                    region_count = 1
                else:
                    region_count = None
            except Exception:
                region_count = None
        return TemplateRecord(
            slug=tpl.slug,
            aspect_ratio=tpl.aspect_ratio,
            category=tpl.category,
            base_image=tpl.base_image,
            coords=tpl.coords,
            roles=tpl.roles,
            enabled=tpl.enabled,
            region_count=region_count,
        )

    def _derive_aspect_ratio(self, size: tuple[int, int], existing: str | None) -> str:
        width, height = size
        if existing and existing not in {"", DEFAULT_MOCKUP_ASPECT, None}:  # type: ignore[arg-type]
            return existing
        if width == 0 or height == 0:
            return DEFAULT_MOCKUP_ASPECT
        if width == height:
            return "1x1"
        gcd_val = math.gcd(int(width), int(height)) or 1
        return f"{width // gcd_val}x{height // gcd_val}"

    def delete_bases(self, base_ids: Iterable[str]) -> List[str]:
        ids = [bid.strip() for bid in base_ids if isinstance(bid, str) and bid.strip()]
        if not ids:
            raise ValidationError("No base ids provided")

        doc = self._load_catalog_json()
        by_id = {entry.get("id"): entry for entry in doc["bases"]}
        missing = [bid for bid in ids if bid not in by_id]
        if missing:
            raise ValidationError(f"Base id not found: {', '.join(missing)}")

        blocked = [bid for bid in ids if by_id[bid].get("status") == "in_use"]
        if blocked:
            raise ValidationError(f"Cannot delete bases in use: {', '.join(blocked)}")

        removed_slugs: List[str] = []
        for bid in ids:
            entry = by_id[bid]
            base_path = self._resolve_base_image_path(entry)
            coords_path = None
            coords_val = entry.get("coordinates_path") or entry.get("coordinates")
            if isinstance(coords_val, str) and coords_val.strip():
                coords_path = Path(coords_val.strip())
                coords_path = coords_path if coords_path.is_absolute() else self.catalog_dir / coords_path

            try:
                if base_path.exists():
                    base_path.unlink()
            except Exception:
                pass
            if coords_path:
                try:
                    if coords_path.exists():
                        coords_path.unlink()
                except Exception:
                    pass

            doc["bases"].remove(entry)
            removed_slugs.append(entry.get("slug", ""))

        self._write_catalog_json(doc)
        return removed_slugs

    def move_bases_to_category(self, base_ids: Iterable[str], category: str) -> List[str]:
        ids = [bid.strip() for bid in base_ids if isinstance(bid, str) and bid.strip()]
        if not ids:
            raise ValidationError("No base ids provided")
        new_cat = _normalize_category(category)
        if not new_cat:
            raise ValidationError("Category is required")

        doc = self._load_catalog_json()
        by_id = {entry.get("id"): entry for entry in doc["bases"]}
        missing = [bid for bid in ids if bid not in by_id]
        if missing:
            raise ValidationError(f"Base id not found: {', '.join(missing)}")

        now = _now_iso()
        updated: List[str] = []
        for bid in ids:
            entry = by_id[bid]
            entry["category"] = new_cat
            self._ensure_base_files(entry)
            entry["updated_at"] = now
            updated.append(entry.get("slug", ""))

        self._write_catalog_json(doc)
        return updated

    def change_bases_aspect(self, base_ids: Iterable[str], aspect_ratio: str) -> List[str]:
        ids = [bid.strip() for bid in base_ids if isinstance(bid, str) and bid.strip()]
        if not ids:
            raise ValidationError("No base ids provided")
        aspect_clean = _normalize_aspect(aspect_ratio)
        if not aspect_clean:
            raise ValidationError("Aspect ratio is required")

        doc = self._load_catalog_json()
        by_id = {entry.get("id"): entry for entry in doc["bases"]}
        missing = [bid for bid in ids if bid not in by_id]
        if missing:
            raise ValidationError(f"Base id not found: {', '.join(missing)}")

        now = _now_iso()
        updated: List[str] = []
        for bid in ids:
            entry = by_id[bid]
            entry["aspect_ratio"] = aspect_clean
            entry["aspect_source"] = ASPECT_SOURCE_MANUAL
            entry["updated_at"] = now
            self._ensure_base_files(entry)
            updated.append(entry.get("slug", ""))

        self._write_catalog_json(doc)
        return updated

    def generate_coordinates_for_bases(
        self,
        base_ids: Iterable[str],
        *,
        force: bool = False,
        progress_hook: Callable[[int, int, str, str], None] | None = None,
    ) -> List[Tuple[str, str]]:
        ids = [bid.strip() for bid in base_ids if isinstance(bid, str) and bid.strip()]
        if not ids:
            raise ValidationError("No base ids provided")
        if len(ids) > MAX_COORD_GEN_BATCH:
            raise ValidationError(f"Too many bases for one batch; max {MAX_COORD_GEN_BATCH}")

        doc = self._load_catalog_json()
        by_id = {entry.get("id"): entry for entry in doc["bases"]}
        missing = [bid for bid in ids if bid not in by_id]
        if missing:
            raise ValidationError(f"Base id not found: {', '.join(missing)}")

        prepared = []
        for bid in ids:
            entry = by_id[bid]
            base_path, coords_target = self._ensure_base_files(entry)
            if not base_path.exists():
                raise ValidationError(f"Base image missing for id {bid}: {base_path}")

            if force and coords_target.exists() and coords_target.is_file():
                try:
                    coords_target.unlink()
                except Exception as exc:
                    logger.warning(
                        "Unable to delete existing coordinates for %s; will overwrite on write: %s",
                        entry.get("slug"),
                        exc,
                    )

            # Load and validate image while deriving coordinates
            img = validate_png_bytes(base_path.read_bytes())
            aspect_clean = _normalize_aspect(entry.get("aspect_ratio"))
            # Legacy fallback is allowed only when a coords JSON already exists and we are
            # not forcing regeneration. A missing coords JSON must trigger high-fidelity
            # alpha detection (clean-slate migration behavior).
            legacy = None if (force or not coords_target.exists()) else _legacy_coords_lookup(entry.get("slug", ""), aspect_clean)

            coords_payload = None
            generated_from_detection = False

            # Cache hit: if coords JSON already exists, reuse it (unless forced).
            if not force and coords_target.exists():
                try:
                    coords_payload = json.loads(coords_target.read_text(encoding="utf-8"))
                except Exception:
                    coords_payload = None

            if coords_payload is None:
                if legacy:
                    coords_payload = legacy
                    coords_payload["template"] = coords_payload.get("template") or f"{entry.get('slug')}.png"
                else:
                    zones_normalized = _scan_transparent_zones_normalized(base_path)
                    zones = _normalized_zones_to_pixel_zones(zones_normalized or [], size=img.size)
                    if zones:
                        coords_payload = {
                            "template": f"{entry.get('slug')}.png",
                            "zones": zones,
                        }
                        generated_from_detection = True
                    else:
                        detected = _detect_corners_from_alpha(base_path, size=img.size)
                        if not detected:
                            raise ValidationError(f"Unable to detect artwork zone for {entry.get('slug')}")
                        coords_payload = {
                            "template": f"{entry.get('slug')}.png",
                            "corners": detected,
                        }
                        generated_from_detection = True

            coords_payload = _clamp_coords_payload(coords_payload, size=img.size)
            coords_payload, coordinate_type = _normalize_coords_payload_v2(
                coords_payload,
                template=f"{entry.get('slug')}.png",
            )
            coords_payload = _clamp_coords_payload(coords_payload, size=img.size)
            placements = validate_coords_payload(coords_payload, img.size)
            coords_path = coords_target
            prepared.append(
                {
                    "entry": entry,
                    "coords_payload": coords_payload,
                    "placements": placements,
                    "coordinate_type": coordinate_type,
                    "generated_from_detection": generated_from_detection,
                    "coords_path": coords_path,
                    "size": img.size,
                }
            )

        now = _now_iso()
        results: List[Tuple[str, str]] = []
        total_items = len(prepared)
        for idx, item in enumerate(prepared, start=1):
            coords_path: Path = item["coords_path"]
            ensure_dir(coords_path.parent)
            coords_payload = item["coords_payload"]
            write_json_atomic(coords_path, coords_payload)

            entry = item["entry"]
            entry["coordinates_path"] = _relative_to(self.catalog_dir, coords_path).as_posix()
            entry["status"] = "coordinates_ready"
            entry["region_count"] = len(item["placements"])
            entry["last_coordinated_at"] = now
            if item.get("generated_from_detection"):
                entry["coordinate_type"] = COORDINATE_TYPE_PERSPECTIVE
            else:
                entry["coordinate_type"] = item.get("coordinate_type") or COORDINATE_TYPE_PERSPECTIVE
            entry["updated_at"] = now
            if entry.get("aspect_source") == ASPECT_SOURCE_MANUAL:
                aspect_val = entry.get("aspect_ratio")
                aspect_source = ASPECT_SOURCE_MANUAL
            elif _is_size_chart_category(entry.get("category")) and item["placements"]:
                aspect_val = _aspect_from_region(item["placements"][0]) or self._derive_aspect_ratio(item["size"], entry.get("aspect_ratio"))
                aspect_source = ASPECT_SOURCE_REGION
            else:
                aspect_val = self._derive_aspect_ratio(item["size"], entry.get("aspect_ratio"))
                aspect_source = ASPECT_SOURCE_AUTO

            entry["aspect_ratio"] = aspect_val
            entry["aspect_source"] = aspect_source
            results.append((entry.get("id"), entry.get("slug")))
            if progress_hook:
                progress_hook(idx, total_items, str(entry.get("id") or ""), str(entry.get("slug") or ""))
            if idx % 20 == 0:
                self._write_catalog_json(doc)

        self._write_catalog_json(doc)
        return results

    def _base_by_id(self, base_id: str) -> MockupBase:
        base_id = base_id.strip()
        if not base_id:
            raise ValidationError("Base id is required")
        bases = {b.id: b for b in self.load_bases()}
        if base_id not in bases:
            raise ValidationError(f"Base id not found: {base_id}")
        return bases[base_id]

    def regenerate_base(self, base_id: str) -> MockupBase:
        self.generate_coordinates_for_bases([base_id], force=True)
        return self._base_by_id(base_id)

    def delete_base(self, base_id: str) -> List[str]:
        return self.delete_bases([base_id])

    def update_base_category(self, base_id: str, category: str) -> MockupBase:
        self.move_bases_to_category([base_id], category)
        return self._base_by_id(base_id)

    def override_base_aspect(self, base_id: str, aspect_ratio: str) -> MockupBase:
        self.change_bases_aspect([base_id], aspect_ratio)
        return self._base_by_id(base_id)


class PolicyAdminService:
    def __init__(self, *, policy_path: Path | None = None, catalog_path: Path | None = None) -> None:
        self.policy_path = _policy_path(policy_path)
        self.catalog_path = _catalog_path(catalog_path)

    def load_policy(self) -> PolicyDocument:
        if not self.policy_path.exists():
            return self._write_policy(PolicyDocument(mandatory_templates=[]))
        try:
            data = json.loads(self.policy_path.read_text(encoding="utf-8"))
        except Exception as exc:  # pylint: disable=broad-except
            raise ValidationError("Policy file is invalid JSON") from exc
        mandatory = data.get("mandatory_templates") or []
        if not isinstance(mandatory, list):
            raise ValidationError("mandatory_templates must be a list")
        mandatory_clean = []
        for slug in mandatory:
            if not isinstance(slug, str) or not slug.strip():
                raise ValidationError("mandatory_templates entries must be non-empty strings")
            mandatory_clean.append(slug.strip())
        
        mandatory_category = data.get("mandatory_category")
        if mandatory_category is not None and (not isinstance(mandatory_category, str) or not mandatory_category.strip()):
            raise ValidationError("mandatory_category must be a non-empty string when set")
        
        return PolicyDocument(
            mandatory_templates=mandatory_clean,
            version=int(data.get("version", 1)),
            mandatory_category=mandatory_category.strip() if mandatory_category else None
        )

    def set_mandatory_templates(self, slugs: Iterable[str]) -> PolicyDocument:
        slugs_clean = [s.strip() for s in slugs if isinstance(s, str) and s.strip()]
        catalog = CatalogAdminService(catalog_path=self.catalog_path).load_catalog()
        catalog_slugs = {tpl.slug for tpl in catalog}
        for slug in slugs_clean:
            if slug not in catalog_slugs:
                raise ValidationError(f"Mandatory template not in catalog: {slug}")
        doc = PolicyDocument(mandatory_templates=slugs_clean)
        return self._write_policy(doc)

    def ensure_not_mandatory(self, slug: str) -> None:
        policy = self.load_policy()
        if slug in policy.mandatory_templates:
            raise ValidationError("Cannot modify template flagged as mandatory")

    def _write_policy(self, policy: PolicyDocument) -> PolicyDocument:
        ensure_dir(self.policy_path.parent)
        payload = {
            "version": policy.version,
            "mandatory_templates": policy.mandatory_templates,
            "mandatory_category": policy.mandatory_category,
            "updated_at": _now_iso(),
        }
        write_json_atomic(self.policy_path, payload)
        return policy


class ManualMockupService:
    """Manual artwork helper for admin workflows (generation + swap + metadata hints)."""

    def __init__(
        self,
        *,
        catalog_path: Path | None = None,
        master_index_path: Path | None = None,
        processed_root: Path | None = None,
    ) -> None:
        self.catalog_path = _catalog_path(catalog_path)
        self.master_index_path = master_index_path or MASTER_INDEX_PATH
        self.processed_root = processed_root or PROCESSED_DIR

    def _catalog_map(self) -> Dict[str, Template]:
        templates = load_physical_catalog(catalog_dir=self.catalog_path.parent)
        return {tpl.slug: tpl for tpl in templates if isinstance(tpl, Template) and tpl.enabled}

    def _physical_candidates(self, *, aspect: str | None, category: str | None) -> List[Template]:
        aspect_norm = aspect if (aspect and aspect != DEFAULT_MOCKUP_ASPECT) else None
        cat_norm = _normalize_category(category) if category else None
        templates = load_physical_bases(
            catalog_dir=self.catalog_path.parent,
            aspect=aspect_norm,
            category=cat_norm,
        )
        results: List[Template] = []
        for tpl in templates:
            if not tpl.enabled:
                continue
            base_path, coords_path = self._resolve_paths(tpl)
            if not base_path.exists() or not coords_path.exists():
                continue
            results.append(tpl)
        return results

    def _resolve_artwork(self, sku: str) -> tuple[Path, AssetsIndex, Dict, str]:
        artwork_dir, assets_path, slug = resolve_artwork(
            sku,
            master_index_path=self.master_index_path,
            processed_root=self.processed_root,
        )
        assets_index = AssetsIndex(artwork_dir, assets_path)
        assets_doc = assets_index.load()
        return artwork_dir, assets_index, assets_doc, slug

    def _artwork_aspect(self, analyse_path: Path) -> str | None:
        if not analyse_path.exists():
            return None
        dims = _image_dimensions_via_node(analyse_path)
        if not dims:
            return None
        width, height = dims
        if width <= 0 or height <= 0:
            return None
        gcd_val = math.gcd(int(width), int(height)) or 1
        return f"{int(width) // gcd_val}x{int(height) // gcd_val}"

    def _resolve_paths(self, tpl: Template) -> tuple[Path, Path]:
        base_path = tpl.base_image if tpl.base_image.is_absolute() else BASE_DIR / tpl.base_image
        coords_path = tpl.coords if tpl.coords.is_absolute() else BASE_DIR / tpl.coords
        return base_path, coords_path

    def _eligible_templates(self, *, aspect: str | None, category: str | None) -> List[Template]:
        return self._physical_candidates(aspect=aspect, category=category)

    def _next_slots(self, assets_map: Dict, count: int) -> List[int]:
        slots: List[int] = []
        existing = {int(k) for k in assets_map.keys() if str(k).isdigit()}
        candidate = 1
        while len(slots) < count:
            if candidate not in existing:
                slots.append(candidate)
            candidate += 1
        return slots

    def get_bulk_generation_status(self) -> dict:
        return _read_bulk_status()

    def start_bulk_generation_async(self, base_ids: Iterable[str], *, force: bool = True) -> dict:
        ids = [bid.strip() for bid in base_ids if isinstance(bid, str) and bid.strip()]
        if not ids:
            raise ValidationError("No base ids provided")
        if len(ids) > MAX_COORD_GEN_BATCH:
            raise ValidationError(f"Too many bases for one batch; max {MAX_COORD_GEN_BATCH}")

        global _BULK_GEN_THREAD
        with _BULK_GEN_MUTEX:
            current = _read_bulk_status()
            running = str(current.get("status", "")).lower() in {"queued", "running", "processing"}
            if _BULK_GEN_THREAD and _BULK_GEN_THREAD.is_alive():
                running = True
            if running:
                raise ValidationError("A coordinate generation job is already running")

            run_id = str(uuid.uuid4())
            _write_bulk_status(
                _status_payload(
                    run_id=run_id,
                    status="queued",
                    message=f"Task Started: queued {len(ids)} base(s).",
                    current=0,
                    total=len(ids),
                    force=bool(force),
                )
            )

            thread = threading.Thread(
                target=self._run_bulk_generation_async,
                args=(ids, bool(force), run_id),
                daemon=True,
                name=f"mockup-bulk-gen-{run_id[:8]}",
            )
            _BULK_GEN_THREAD = thread
            thread.start()

        return _read_bulk_status()

    def _run_bulk_generation_async(self, ids: List[str], force: bool, run_id: str) -> None:
        global _BULK_GEN_THREAD
        total = len(ids)
        _write_bulk_status(
            _status_payload(
                run_id=run_id,
                status="processing",
                message=f"Step 0 of {total}",
                current=0,
                total=total,
                force=bool(force),
            )
        )

        def _progress(step: int, count: int, _base_id: str, _slug: str) -> None:
            _write_bulk_status(
                _status_payload(
                    run_id=run_id,
                    status="processing",
                    message=f"Step {step} of {count}",
                    current=int(step),
                    total=int(count),
                    force=bool(force),
                )
            )

        try:
            catalog_svc = CatalogAdminService(catalog_path=self.catalog_path)
            generated = catalog_svc.generate_coordinates_for_bases(ids, force=force, progress_hook=_progress)
            _write_bulk_status(
                _status_payload(
                    run_id=run_id,
                    status="completed",
                    message=f"Completed {len(generated)} of {total} base(s).",
                    current=len(generated),
                    total=total,
                    force=bool(force),
                )
            )
        except Exception as exc:
            _write_bulk_status(
                _status_payload(
                    run_id=run_id,
                    status="failed",
                    message=str(exc),
                    current=0,
                    total=total,
                    force=bool(force),
                )
            )
        finally:
            with _BULK_GEN_MUTEX:
                _BULK_GEN_THREAD = None

    def generate_mockups_for_artwork(
        self,
        *,
        sku: str,
        count: int,
        category: str | None = None,
    ) -> Dict[int, dict]:
        if count <= 0:
            raise ValidationError("Count must be positive")

        artwork_dir, assets_index, assets_doc, _ = self._resolve_artwork(sku)
        # Try closeup_proxy first (higher res), fallback to analyse
        files_dict = assets_doc.get("files") or {}
        image_rel = files_dict.get("closeup_proxy") or files_dict.get("analyse")
        analyse_path = artwork_dir / image_rel if image_rel else (artwork_dir / f"{sku.lower()}{TARGET_IMAGE_NAME_SUFFIX}")
        if not analyse_path.exists():
            analyse_path = artwork_dir / f"{assets_doc.get('slug')}{TARGET_IMAGE_NAME_SUFFIX}" if assets_doc.get("slug") else analyse_path
        aspect = self._artwork_aspect(analyse_path) if analyse_path and analyse_path.exists() else None

        candidates = self._eligible_templates(aspect=aspect, category=category)
        if not candidates:
            if category:
                raise ValidationError(f"0 mockups found in {_normalize_category(category)}")
            raise ValidationError("No eligible templates for this artwork")

        selection = candidates if count >= len(candidates) else random.sample(candidates, count)
        slots = self._next_slots(assets_index.assets_map(assets_doc), len(selection))

        results: Dict[int, dict] = {}
        for slot_num, tpl in zip(slots, selection, strict=False):
            base_path, coords_path = self._resolve_paths(tpl)
            results[slot_num] = generate_mockups_for_artwork(
                sku=sku,
                template_slug=tpl.slug,
                aspect_ratio=tpl.aspect_ratio,
                category=tpl.category,
                base_image_path=base_path,
                coords_path=coords_path,
                slot=slot_num,
                mode="generate",
                master_index_path=self.master_index_path,
                processed_root=self.processed_root,
            )
        return results

    def regenerate_single_mockup(
        self,
        *,
        sku: str,
        slot: int,
        new_category: str | None = None,
    ) -> dict:
        artwork_dir, assets_index, assets_doc, _ = self._resolve_artwork(sku)
        assets_map = assets_index.assets_map(assets_doc)
        slot_key = f"{slot:02d}"
        existing = assets_map.get(slot_key)
        if not existing:
            raise ValidationError("Slot not found")

        aspect = existing.get("aspect_ratio")
        current_slug = existing.get("template_slug")
        catalog = self._catalog_map()
        current_tpl = catalog.get(current_slug)
        if not aspect and current_tpl:
            aspect = current_tpl.aspect_ratio

        desired_category = new_category or (current_tpl.category if current_tpl else None)
        candidates = self._eligible_templates(aspect=aspect, category=desired_category)
        if not candidates:
            if desired_category:
                raise ValidationError(f"0 mockups found in {_normalize_category(desired_category)}")
            raise ValidationError("No eligible templates for swap")

        pool = [tpl for tpl in candidates if tpl.slug != current_slug] or candidates
        tpl = random.choice(pool)
        base_path, coords_path = self._resolve_paths(tpl)

        return generate_mockups_for_artwork(
            sku=sku,
            template_slug=tpl.slug,
            aspect_ratio=tpl.aspect_ratio,
            category=tpl.category,
            base_image_path=base_path,
            coords_path=coords_path,
            slot=slot,
            mode="swap",
            master_index_path=self.master_index_path,
            processed_root=self.processed_root,
        )
