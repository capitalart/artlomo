from __future__ import annotations

import json
import math
import random
import shutil
import subprocess
from pathlib import Path
from typing import Any

from flask import Blueprint, abort, current_app, flash, redirect, request, send_file, session, url_for

from application.artwork.errors import ArtworkProcessingError, IndexValidationError, RequiredAssetMissingError
from application.artwork.services.processing_service import ProcessingService
from application.mockups.assets_index import AssetsIndex
from application.common.utilities import slug_sku
from application.utils.logger_utils import log_security_event


mockups_bp = Blueprint(
    "mockups",
    __name__,
)
VIDEO_WORKER_DIR = Path(__file__).resolve().parents[2] / "video_worker"


def _image_dimensions_via_node(path: Path) -> tuple[int, int] | None:
    if not path.exists():
        return None
    node_bin = shutil.which("node") or shutil.which("nodejs")
    if not node_bin:
        return None
    payload = {
        "action": "read_image_meta",
        "image_path": str(path),
    }
    cmd = [
        node_bin,
        str(VIDEO_WORKER_DIR / "processor.js"),
        json.dumps(payload, ensure_ascii=True, separators=(",", ":")),
    ]
    xvfb_bin = shutil.which("xvfb-run")
    if xvfb_bin:
        cmd = [xvfb_bin, "-a", *cmd]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)
        if proc.returncode != 0:
            return None
        parsed = json.loads((proc.stdout or "").strip() or "{}")
        width = int(parsed.get("width") or 0)
        height = int(parsed.get("height") or 0)
        if width <= 0 or height <= 0:
            return None
        return (width, height)
    except Exception:
        return None

def _processing_service() -> ProcessingService:
    cfg = current_app.config
    return ProcessingService(
        unprocessed_root=Path(cfg["LAB_UNPROCESSED_DIR"]),
        processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
        artworks_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
    )


def _promote_to_processed(slug: str) -> None:
    cfg = current_app.config
    locked_root = Path(cfg["LAB_LOCKED_DIR"])
    if (locked_root / slug).exists():
        raise ArtworkProcessingError("Artwork is locked and cannot be re-analysed.")
    processed_root = Path(cfg["LAB_PROCESSED_DIR"])
    if (processed_root / slug).exists():
        return
    svc = _processing_service()
    try:
        svc.process(slug)
    except IndexValidationError:
        return
    except RequiredAssetMissingError:
        raise
    except ArtworkProcessingError:
        raise


def _normalized_aspect_from_image(path: Path) -> str | None:
    dims = _image_dimensions_via_node(path)
    if not dims:
        return None
    width, height = dims
    if width <= 0 or height <= 0:
        return None
    snapped = _snap_ratio_label(width=int(width), height=int(height))
    if snapped:
        return _normalize_ratio_label(snapped)
    gcd_val = math.gcd(int(width), int(height)) or 1
    return f"{int(width) // gcd_val}x{int(height) // gcd_val}"


def _normalize_ratio_label(label: str | None) -> str | None:
    if not label:
        return None
    cleaned = str(label).strip()
    if not cleaned:
        return None
    return cleaned.replace(":", "x").replace("/", "x").lower()


def _read_json_silent(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        return doc if isinstance(doc, dict) else {}
    except Exception:
        return {}


def _snap_ratio_label(*, width: int, height: int) -> str | None:
    if width <= 0 or height <= 0:
        return None
    calc = float(width) / float(height)

    standards: list[tuple[int, int, str]] = [
        (1, 1, "1:1"),
        (4, 5, "4:5"),
        (3, 4, "3:4"),
        (2, 3, "2:3"),
        (5, 7, "5:7"),
    ]

    best_label: str | None = None
    best_rel_err: float | None = None
    for w_ratio, h_ratio, label in standards:
        standard = float(w_ratio) / float(h_ratio)
        rel_err = abs(calc - standard) / standard
        if best_rel_err is None or rel_err < best_rel_err:
            best_rel_err = rel_err
            best_label = label

    if best_rel_err is not None and best_rel_err <= 0.03:
        return best_label
    return None


def resolve_artwork_aspect_for_preflight(slug: str) -> dict[str, Any]:
    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug

    # Get SKU first to check for SKU-prefixed files
    sku = slug
    meta_path = processed_dir / f"{slug.lower()}-metadata.json"
    if not meta_path.exists():
        meta_path = processed_dir / "metadata.json"
    if meta_path.exists():
        try:
            meta_temp = json.loads(meta_path.read_text(encoding="utf-8"))
            if isinstance(meta_temp, dict):
                sku = str(meta_temp.get("sku") or meta_temp.get("artwork_id") or sku).strip() or sku
        except Exception:
            pass
    
    # Try SKU-prefixed QC first, then fallback to legacy qc.json
    qc_doc = _read_json_silent(processed_dir / f"{sku.lower()}-qc.json") or _read_json_silent(processed_dir / "qc.json")
    qc_aspect = qc_doc.get("aspect_ratio") if isinstance(qc_doc, dict) else None
    if isinstance(qc_aspect, dict) and qc_aspect.get("label"):
        label = str(qc_aspect.get("label"))
        return {
            "match_key": _normalize_ratio_label(label) or "UNSET",
            "detected": f"{label} Matched",
            "source": "qc.json",
        }

    # Try SKU-prefixed metadata first, then fallback to legacy metadata.json
    meta_doc = _read_json_silent(processed_dir / f"{sku.lower()}-metadata.json") or _read_json_silent(processed_dir / "metadata.json")
    meta_aspect = meta_doc.get("aspect_ratio") if isinstance(meta_doc, dict) else None
    if isinstance(meta_aspect, dict) and meta_aspect.get("label"):
        label = str(meta_aspect.get("label"))
        return {
            "match_key": _normalize_ratio_label(label) or "UNSET",
            "detected": f"{label} Matched",
            "source": "metadata.json",
        }

    dims = qc_doc.get("dimensions") if isinstance(qc_doc, dict) else None
    if isinstance(dims, dict) and isinstance(dims.get("width"), (int, float)) and isinstance(dims.get("height"), (int, float)):
        width_val = dims.get("width", 0)
        height_val = dims.get("height", 0)
        snapped = _snap_ratio_label(width=int(width_val) if width_val else 0, height=int(height_val) if height_val else 0)  # type: ignore[arg-type]
        if snapped:
            return {
                "match_key": _normalize_ratio_label(snapped) or "UNSET",
                "detected": f"{snapped} Matched",
                "source": "dimensions",
            }

    analyse_path = processed_dir / f"{slug}-ANALYSE.jpg"
    if analyse_path.exists():
        dims = _image_dimensions_via_node(analyse_path)
        if dims:
            w_px, h_px = dims
        else:
            w_px, h_px = 0, 0
        snapped = _snap_ratio_label(width=int(w_px), height=int(h_px))
        if snapped:
            return {
                "match_key": _normalize_ratio_label(snapped) or "UNSET",
                "detected": f"{snapped} Matched",
                "source": "pixels",
            }

    return {
        "match_key": _normalized_aspect_from_image(analyse_path) if analyse_path.exists() else "UNSET",
        "detected": "UNSET",
        "source": "none",
    }


def _eligible_template_count(*, aspect: str | None) -> int:
    if not aspect or aspect == "UNSET":
        return 0
    from application.mockups.catalog.loader import load_physical_bases

    return len(load_physical_bases(aspect=aspect))


def _clear_existing_mockups_for_slug(*, slug: str) -> int:
    cfg = current_app.config
    from application.mockups import config as mockups_config
    from application.mockups import storage

    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    mockups_dir = processed_dir / mockups_config.MOCKUPS_SUBDIR
    thumbs_dir = mockups_dir / mockups_config.THUMBS_SUBDIR
    storage.ensure_dirs(mockups_dir, thumbs_dir)
    removed = 0

    # Primary: remove files declared in assets index slot entries.
    loaded = _load_assets_index_for_slug(slug)
    if loaded:
        _, artwork_dir, _, assets_index, assets_doc = loaded
        assets_map = assets_index.assets_map(assets_doc)
        for slot_entry in assets_map.values():
            if not isinstance(slot_entry, dict):
                continue
            for key in ("composite", "thumb"):
                rel = slot_entry.get(key)
                if not isinstance(rel, str) or not rel:
                    continue
                target = artwork_dir / rel
                try:
                    if target.exists() and target.is_file():
                        target.unlink()
                        removed += 1
                except Exception:
                    continue

    # Important: preserve non-slot assets (e.g., detail closeup files) that also live
    # under mockups/. Regeneration should only clear generated mockup slots.
    prefixes = [slug]
    sku = _resolve_sku_for_slug(processed_dir)
    if sku and sku.lower() != slug.lower():
        prefixes.append(sku.lower())

    for prefix in prefixes:
        comp_pattern = f"mu-{prefix}-*.jpg"
        thumb_pattern = f"mu-{prefix}-*-THUMB.jpg"

        for root, pattern in ((mockups_dir, comp_pattern), (thumbs_dir, thumb_pattern)):
            if not root.exists() or not root.is_dir():
                continue
            for path in root.glob(pattern):
                if not path.is_file():
                    continue
                stem = path.stem
                # Only remove slot files that end in 2-digit slot suffix.
                # Composite: mu-<slug|sku>-01.jpg
                # Thumb:     mu-<slug|sku>-01-THUMB.jpg
                if path.parent == thumbs_dir:
                    if not stem.endswith("-THUMB"):
                        continue
                    slot_part = stem.rsplit("-", 2)[-2]
                else:
                    slot_part = stem.rsplit("-", 1)[-1]
                if not (slot_part.isdigit() and len(slot_part) == 2):
                    continue
                try:
                    path.unlink()
                    removed += 1
                except Exception:
                    continue

    return int(removed)


def build_mockup_preflight_for_slug(slug: str) -> dict:
    aspect_info = resolve_artwork_aspect_for_preflight(slug)
    match_key = aspect_info.get("match_key") or "UNSET"
    eligible = _eligible_template_count(aspect=match_key)
    return {
        "aspect": match_key,
        "eligible_templates": int(eligible),
        "detected": aspect_info.get("detected") or "UNSET",
        "source": aspect_info.get("source") or "none",
    }


def list_catalog_categories() -> list[str]:
    from application.mockups.selection.planner import load_catalog_for_selection

    catalog = load_catalog_for_selection()
    categories = sorted({tpl.category for tpl in catalog.values() if tpl.enabled and tpl.category})
    return [str(c) for c in categories]


def _resolve_sku_for_slug(processed_dir: Path) -> str | None:
    # Try SKU-prefixed metadata first (assume slug from dirname matches slug used initially)
    slug = processed_dir.name
    meta_path = processed_dir / f"{slug.lower()}-metadata.json"
    if not meta_path.exists():
        meta_path = processed_dir / "metadata.json"
    if not meta_path.exists():
        return None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    sku = str(meta.get("sku") or meta.get("artwork_id") or "").strip()
    return sku or None

def _resolve_artwork_dir_for_slug(slug: str) -> Path | None:
    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if processed_dir.exists() and processed_dir.is_dir():
        return processed_dir
    locked_dir = Path(cfg["LAB_LOCKED_DIR"]) / slug
    if locked_dir.exists() and locked_dir.is_dir():
        return locked_dir
    return None


def _resolve_assets_for_slug(slug: str):
    cfg = current_app.config
    artwork_dir = _resolve_artwork_dir_for_slug(slug)
    if not artwork_dir:
        return None
    sku = _resolve_sku_for_slug(artwork_dir)
    if not sku:
        return None
    from application.mockups.artwork_index import resolve_artwork
    from application.mockups.errors import IndexLookupError

    try:
        artwork_dir, assets_path, _ = resolve_artwork(
            sku,
            master_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
            processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
        )
    except IndexLookupError:
        return None
    return sku, artwork_dir, assets_path


def _load_assets_index_for_slug(slug: str) -> tuple[str | None, Path, Path, AssetsIndex, dict[str, Any]] | None:
    """Resolve and load assets index for slug, preferring SKU-index mapping."""
    resolved = _resolve_assets_for_slug(slug)
    if resolved:
        sku, artwork_dir, assets_path = resolved
    else:
        cfg = current_app.config
        from application.mockups import config as mockups_config

        artwork_dir = _resolve_artwork_dir_for_slug(slug)
        if not artwork_dir:
            return None
        sku = _resolve_sku_for_slug(artwork_dir)
        assets_path = artwork_dir / mockups_config.ASSETS_BASENAME_TEMPLATE.format(slug=slug)
        if not assets_path.exists() and sku:
            assets_path = artwork_dir / mockups_config.ASSETS_BASENAME_TEMPLATE.format(slug=sku.lower())
        if not assets_path.exists():
            return None

    try:
        assets_index = AssetsIndex(artwork_dir, assets_path)
        assets_doc = assets_index.load()
    except Exception:
        return None

    return sku, artwork_dir, assets_path, assets_index, assets_doc


def _init_fresh_assets_index_for_slug(slug: str) -> tuple[str | None, Path, Path, AssetsIndex, dict[str, Any]] | None:
    """Initialize a fresh assets index if one doesn't exist. Calls _load_assets_index_for_slug after init."""
    cfg = current_app.config
    from application.mockups import config as mockups_config
    from application.mockups import storage as mockups_storage

    # First try normal load path
    loaded = _load_assets_index_for_slug(slug)
    if loaded:
        return loaded

    # If not found, try to initialize fresh
    artwork_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if not artwork_dir.exists() or not artwork_dir.is_dir():
        return None

    sku = _resolve_sku_for_slug(artwork_dir)
    if not sku:
        return None

    # Determine asset path (prefer SKU-based name)
    assets_path = artwork_dir / mockups_config.ASSETS_BASENAME_TEMPLATE.format(slug=sku.lower())

    # Create minimal fresh index
    assets_doc = {
        "slug": slug,
        "sku": sku,
        "mockups": {
            "dir": mockups_config.MOCKUPS_SUBDIR,
            "assets": {}
        }
    }

    try:
        # Write fresh index atomically
        mockups_storage.atomic_write_json(assets_doc, assets_path)
        
        # Load it fresh to validate
        assets_index = AssetsIndex(artwork_dir, assets_path)
        assets_doc = assets_index.load()
        return sku, artwork_dir, assets_path, assets_index, assets_doc
    except Exception:
        return None


def list_mockup_entries_for_slug(slug: str) -> list[dict[str, Any]]:
    artwork_dir = _resolve_artwork_dir_for_slug(slug)
    if not artwork_dir:
        return []

    from application.mockups import config as mockups_config

    mockups_dir = artwork_dir / mockups_config.MOCKUPS_SUBDIR
    thumbs_dir = mockups_dir / mockups_config.THUMBS_SUBDIR
    if not mockups_dir.exists() or not mockups_dir.is_dir():
        return []

    # Primary source of truth: per-artwork assets index (physical folder contract).
    sku = None
    entries: list[dict[str, Any]] = []
    try:
        loaded = _load_assets_index_for_slug(slug)
        if not loaded:
            raise ValueError("assets index unavailable")
        _, _, _, assets_index, assets_doc = loaded
        sku = str(assets_doc.get("sku") or "").strip() or None
        assets_map = assets_index.assets_map(assets_doc)

        for slot_key, slot_entry in sorted(assets_map.items(), key=lambda kv: kv[0]):
            if not isinstance(slot_key, str) or not slot_key.isdigit():
                continue
            slot_num = int(slot_key)
            if slot_num <= 0:
                continue
            if not isinstance(slot_entry, dict):
                slot_entry = {}

            entries.append(
                {
                    "slot": slot_num,
                    "slot_key": f"{slot_num:02d}",
                    "template_slug": slot_entry.get("template_slug"),
                    "category": slot_entry.get("category"),
                    "aspect_ratio": slot_entry.get("aspect_ratio"),
                    "thumb_rel": slot_entry.get("thumb"),
                    "composite_rel": slot_entry.get("composite"),
                    "sku": sku,
                }
            )

        return sorted(entries, key=lambda e: int(e.get("slot") or 0))
    except Exception:
        # Fallback: list whatever exists on disk (categories unknown without the index).
        sku = _resolve_sku_for_slug(artwork_dir)
        prefixes = [f"mu-{slug}-"]
        if sku and sku.lower() != slug.lower():
            prefixes.append(f"mu-{sku.lower()}-")
        try:
            candidates = [p for p in mockups_dir.glob("*.jpg") if p.is_file()]
        except Exception:
            candidates = []

        for comp_path in sorted(candidates):
            name = comp_path.name
            if not any(name.startswith(prefix) for prefix in prefixes) or not name.lower().endswith(".jpg"):
                continue
            slot_part = name[:-4].rsplit("-", 1)[-1]
            if not (len(slot_part) == 2 and slot_part.isdigit()):
                continue
            slot_num = int(slot_part)
            thumb_name = mockups_config.THUMB_BASENAME.format(slug=slug, slot=slot_num)
            thumb_path = thumbs_dir / thumb_name

            entries.append(
                {
                    "slot": slot_num,
                    "slot_key": f"{slot_num:02d}",
                    "template_slug": None,
                    "category": None,
                    "aspect_ratio": None,
                    "thumb_rel": thumb_path.relative_to(artwork_dir).as_posix() if thumb_path.exists() else None,
                    "composite_rel": comp_path.relative_to(artwork_dir).as_posix(),
                    "sku": sku,
                }
            )

        return sorted(entries, key=lambda e: int(e.get("slot") or 0))


def mockups_dir_has_files_for_slug(slug: str) -> bool:
    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if not processed_dir.exists() or not processed_dir.is_dir():
        return False
    from application.mockups import config as mockups_config

    mockups_dir = processed_dir / mockups_config.MOCKUPS_SUBDIR
    if not mockups_dir.exists() or not mockups_dir.is_dir():
        return False
    try:
        return any(p.is_file() for p in mockups_dir.rglob("*"))
    except Exception:
        return False


def build_studio_items_for_slug(slug: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    analyse_url = url_for("upload.processed_analyse", slug=slug)
    thumb_url = url_for("upload.processed_thumb", slug=slug)
    items.append(
        {
            "kind": "original",
            "slot": 0,
            "title": "Original",
            "analyse_url": analyse_url,
            "fallback_url": thumb_url,
        }
    )

    for entry in list_mockup_entries_for_slug(slug):
        slot = int(entry.get("slot") or 0)
        items.append(
            {
                "kind": "mockup",
                "slot": slot,
                "title": f"Mockup {slot}",
                "analyse_url": url_for("mockups.mockup_composite", slug=slug, slot=slot),
                "fallback_url": url_for("mockups.mockup_thumb", slug=slug, slot=slot),
                "template_slug": entry.get("template_slug"),
                "category": entry.get("category"),
            }
        )
    return items


def _safe_send_from_artwork(artwork_dir: Path, rel: str):
    if not rel:
        abort(404)
    target = (artwork_dir / rel).resolve()
    root = artwork_dir.resolve()
    if not target.exists() or root not in target.parents:
        abort(404)
    return send_file(target, mimetype="image/jpeg")


@mockups_bp.get("/<slug>/mockups/thumb/<int:slot>")
def mockup_thumb(slug: str, slot: int):
    if not slug_sku.is_safe_slug(slug):
        abort(404)

    loaded = _load_assets_index_for_slug(slug)
    if loaded:
        _, artwork_dir, _, assets_index, assets_doc = loaded
        slot_entry = assets_index.current_slot_entry(assets_doc, f"{int(slot):02d}")
        if isinstance(slot_entry, dict):
            rel = slot_entry.get("thumb")
            if isinstance(rel, str) and rel:
                return _safe_send_from_artwork(artwork_dir, rel)

    artwork_dir = _resolve_artwork_dir_for_slug(slug)
    if not artwork_dir:
        abort(404)
    from application.mockups import config as mockups_config

    thumb_name = mockups_config.THUMB_BASENAME.format(slug=slug, slot=int(slot))
    rel = f"{mockups_config.MOCKUPS_SUBDIR}/{mockups_config.THUMBS_SUBDIR}/{thumb_name}"
    return _safe_send_from_artwork(artwork_dir, rel)


@mockups_bp.get("/<slug>/mockups/composite/<int:slot>")
def mockup_composite(slug: str, slot: int):
    if not slug_sku.is_safe_slug(slug):
        abort(404)

    loaded = _load_assets_index_for_slug(slug)
    if loaded:
        _, artwork_dir, _, assets_index, assets_doc = loaded
        slot_entry = assets_index.current_slot_entry(assets_doc, f"{int(slot):02d}")
        if isinstance(slot_entry, dict):
            rel = slot_entry.get("composite")
            if isinstance(rel, str) and rel:
                return _safe_send_from_artwork(artwork_dir, rel)

    artwork_dir = _resolve_artwork_dir_for_slug(slug)
    if not artwork_dir:
        abort(404)
    from application.mockups import config as mockups_config

    comp_name = mockups_config.COMPOSITE_BASENAME.format(slug=slug, slot=int(slot))
    rel = f"{mockups_config.MOCKUPS_SUBDIR}/{comp_name}"
    return _safe_send_from_artwork(artwork_dir, rel)


@mockups_bp.post("/<slug>/mockups/<int:slot>/swap")  # type: ignore[misc]
def swap_mockup(slug: str, slot: int):
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    if not slug_sku.is_safe_slug(slug):
        abort(404)

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if not processed_dir.exists() or not processed_dir.is_dir():
        abort(404)

    # Get SKU first to check for SKU-prefixed metadata
    sku = slug
    meta_path = processed_dir / f"{slug.lower()}-metadata.json"
    if not meta_path.exists():
        meta_path = processed_dir / "metadata.json"
    if meta_path.exists():
        try:
            meta_temp = json.loads(meta_path.read_text(encoding="utf-8"))
            if isinstance(meta_temp, dict):
                sku = str(meta_temp.get("sku") or meta_temp.get("artwork_id") or sku).strip() or sku
        except Exception:
            pass
    
    # Try SKU-prefixed metadata first, then fallback to legacy metadata.json
    metadata = _read_json_silent(processed_dir / f"{sku.lower()}-metadata.json") or _read_json_silent(processed_dir / "metadata.json")
    if metadata.get("manual_lock"):
        return {"status": "error", "message": "Artwork is locked"}, 403

    body = request.get_json(silent=True) or {}
    category = body.get("category") or None

    try:
        from application.mockups.catalog.loader import load_physical_bases
        from application.mockups.pipeline import generate_mockups_for_artwork

        aspect_info = resolve_artwork_aspect_for_preflight(slug)
        aspect = str(aspect_info.get("match_key") or "UNSET")
        if not aspect or aspect == "UNSET":
            return {"status": "error", "message": "Aspect ratio is UNSET"}, 400

        loaded = _load_assets_index_for_slug(slug)
        if not loaded:
            return {"status": "error", "message": "Assets index not found"}, 400
        sku_for_assets, _, _, assets_index, assets_doc = loaded
        if not sku_for_assets:
            return {"status": "error", "message": "SKU not found"}, 400
        if not assets_index.current_slot_entry(assets_doc, f"{int(slot):02d}"):
            return {"status": "error", "message": "Slot not found"}, 400

        bases = load_physical_bases(aspect=aspect, category=category)
        if not bases:
            if category:
                return {"status": "error", "message": f"0 mockups found in {category}"}, 400
            return {"status": "error", "message": "No eligible templates for swap"}, 400

        tpl = random.choice(bases)
        slot_entry = generate_mockups_for_artwork(
            sku=sku_for_assets,
            template_slug=tpl.slug,
            aspect_ratio=tpl.aspect_ratio,
            category=tpl.category,
            base_image_path=tpl.base_image,
            coords_path=tpl.coords,
            slot=int(slot),
            mode="swap",
            master_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
            processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
        )
        return {
            "status": "ok",
            "slot": slot,
            "template_slug": slot_entry.get("template_slug") if isinstance(slot_entry, dict) else None,
            "category": slot_entry.get("category") if isinstance(slot_entry, dict) else None,
            "thumb_url": url_for("mockups.mockup_thumb", slug=slug, slot=slot),
            "composite_url": url_for("mockups.mockup_composite", slug=slug, slot=slot),
        }
    except Exception as exc:  # pylint: disable=broad-except
        current_app.logger.exception("mockups.swap.failed")
        return {"status": "error", "message": str(exc)}, 400


@mockups_bp.post("/<slug>/mockups/<int:slot>/category")  # type: ignore[misc]
def update_mockup_category(slug: str, slot: int):
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    if not slug_sku.is_safe_slug(slug):
        abort(404)

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if not processed_dir.exists() or not processed_dir.is_dir():
        abort(404)

    body = request.get_json(silent=True) or {}
    category = (body.get("category") or "").strip() or None

    try:
        from application.mockups import storage as mockups_storage
        loaded = _load_assets_index_for_slug(slug)
        if not loaded:
            return {"status": "error", "message": "Assets index not found"}, 400
        _, _, assets_path, assets_index, assets_doc = loaded

        slot_key = f"{int(slot):02d}"
        mockups_doc = assets_doc.get("mockups")
        if not isinstance(mockups_doc, dict):
            mockups_doc = {}
        assets_map = mockups_doc.get("assets")
        if not isinstance(assets_map, dict):
            assets_map = {}
        slot_entry = assets_map.get(slot_key)
        if not isinstance(slot_entry, dict):
            return {"status": "error", "message": "Slot not found"}, 400

        slot_entry["category"] = category
        assets_map[slot_key] = slot_entry
        mockups_doc["assets"] = assets_map
        assets_doc["mockups"] = mockups_doc
        mockups_storage.atomic_write_json(assets_doc, assets_path)
        return {"status": "ok", "slot": int(slot), "category": category}
    except Exception as exc:  # pylint: disable=broad-except
        current_app.logger.exception("mockups.category.failed")
        return {"status": "error", "message": str(exc)}, 400


@mockups_bp.post("/<slug>/mockups/generate")  # type: ignore[misc]
def generate_mockups(slug: str):
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    if not slug_sku.is_safe_slug(slug):
        abort(404)

    try:
        _promote_to_processed(slug)
    except RequiredAssetMissingError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("upload.unprocessed"))
    except ArtworkProcessingError as exc:
        flash(str(exc), "danger")
        target = "upload.locked" if "locked" in str(exc).lower() else "upload.unprocessed"
        return redirect(url_for(target))

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug

    aspect_info = resolve_artwork_aspect_for_preflight(slug)
    match_key = aspect_info.get("match_key") or "UNSET"
    detected = aspect_info.get("detected") or (match_key if match_key != "UNSET" else "UNSET")
    eligible_templates = _eligible_template_count(aspect=match_key)
    if eligible_templates <= 0:
        msg = f"No mockup bases found for aspect ratio {detected}. Please upload bases or map coordinates first."
        wants_json = (request.headers.get("X-Requested-With") == "XMLHttpRequest") or (
            "application/json" in (request.headers.get("Accept") or "").lower()
        )
        if wants_json:
            return {"ok": False, "error": msg}, 400
        flash(msg, "warning")
        return redirect(request.referrer or url_for("artwork.openai_analysis", slug=slug))

    count_raw = request.form.get("mockup_count") or "10"
    try:
        requested = int(str(count_raw).strip())
    except Exception:
        requested = 10
    if requested not in {1, 2, 3, 4, 5, 10, 15, 20, 25}:
        requested = 10

    wants_json = (request.headers.get("X-Requested-With") == "XMLHttpRequest") or (
        "application/json" in (request.headers.get("Accept") or "").lower()
    )

    try:
        # Overwrite workflow: if mockups already exist, clear them before regenerating.
        _clear_existing_mockups_for_slug(slug=slug)
        from application.mockups.catalog.loader import load_physical_bases
        from application.mockups.pipeline import generate_mockups_for_artwork
        from application.mockups import config as mockups_config
        from application.mockups.errors import IndexLookupError
        from application.mockups import storage as mockups_storage

        category_filter = (request.form.get("mockup_category") or "").strip() or None
        bases = load_physical_bases(aspect=match_key, category=category_filter)
        if not bases:
            if category_filter:
                flash(f"0 mockups found in {category_filter}", "warning")
                return redirect(request.referrer or url_for("artwork.openai_analysis", slug=slug))
            raise ValueError("No templates match aspect")

        loaded = _init_fresh_assets_index_for_slug(slug)
        if not loaded:
            raise IndexLookupError("Assets index not found for artwork and cannot be initialized")
        sku_for_assets, _, assets_path, assets_index, assets_doc = loaded
        if not sku_for_assets:
            raise IndexLookupError("SKU not found for artwork")

        mockups_doc = assets_doc.get("mockups")
        if not isinstance(mockups_doc, dict):
            mockups_doc = {}
        mockups_doc["dir"] = mockups_config.MOCKUPS_SUBDIR
        mockups_doc["assets"] = {}
        assets_doc["mockups"] = mockups_doc
        mockups_storage.atomic_write_json(assets_doc, assets_path)
        assets_doc = assets_index.load()

        pool = list(bases)
        random.shuffle(pool)
        chosen = pool[: min(requested, len(pool))]
        for i, tpl in enumerate(chosen, start=1):
            slot_entry = generate_mockups_for_artwork(
                sku=sku_for_assets,
                template_slug=tpl.slug,
                aspect_ratio=tpl.aspect_ratio,
                category=tpl.category,
                base_image_path=tpl.base_image,
                coords_path=tpl.coords,
                slot=int(i),
                mode="generate",
                master_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
                processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
            )
            try:
                slot_key = f"{int(i):02d}"
                assets_index.guard_generate(assets_doc, slot_key)
                if isinstance(slot_entry, dict):
                    assets_index.write_slot(assets_doc, slot_key, slot_entry)
                    assets_doc = assets_index.load()
            except Exception:
                current_app.logger.exception("mockups.generate.assets_index_failed")
        if wants_json:
            return {"ok": True, "slug": slug, "generated": int(len(chosen))}
        flash(f"Mockups generated ({len(chosen)}).", "success")
    except Exception as exc:  # pylint: disable=broad-except
        current_app.logger.exception("mockups.generate.failed")
        if wants_json:
            return {"ok": False, "error": f"Mockup generation failed: {exc}"}, 400
        flash(f"Mockup generation failed: {exc}", "danger")

    return redirect(request.referrer or url_for("artwork.openai_analysis", slug=slug))


@mockups_bp.post("/<slug>/mockups/delete-all")  # type: ignore[misc]
def delete_all_mockups(slug: str):
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    if not slug_sku.is_safe_slug(slug):
        abort(404)

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if not processed_dir.exists() or not processed_dir.is_dir():
        abort(404)

    removed = _clear_existing_mockups_for_slug(slug=slug)

    # Keep assets index in sync: remove all slot mappings after deleting files.
    try:
        from application.mockups import storage as mockups_storage

        loaded = _load_assets_index_for_slug(slug)
        if loaded:
            _, _, assets_path, _, assets_doc = loaded
            mockups_doc = assets_doc.get("mockups")
            if not isinstance(mockups_doc, dict):
                mockups_doc = {}
            mockups_doc["assets"] = {}
            assets_doc["mockups"] = mockups_doc
            mockups_storage.atomic_write_json(assets_doc, assets_path)
    except Exception:
        current_app.logger.exception("mockups.delete_all.assets_index_failed")

    log_security_event(user_id=session.get("username"), action="delete_all_mockups", details=f"slug={slug} removed={int(removed)}")
    return {"status": "ok", "removed": int(removed), "slug": slug}


@mockups_bp.post("/<slug>/mockups/delete-selected")  # type: ignore[misc]
def delete_selected_mockups(slug: str):
    from application.utils.csrf import require_csrf_or_400

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    if not slug_sku.is_safe_slug(slug):
        abort(404)

    cfg = current_app.config
    processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
    if not processed_dir.exists() or not processed_dir.is_dir():
        abort(404)

    body = request.get_json(silent=True) or {}
    slots_raw = body.get("slots") or []
    if not isinstance(slots_raw, list):
        return {"status": "error", "message": "slots must be a list"}, 400

    removed = 0
    removed_slots: list[int] = []

    loaded = _load_assets_index_for_slug(slug)
    if loaded:
        _, artwork_dir, assets_path, assets_index, assets_doc = loaded
    else:
        artwork_dir = processed_dir
        assets_path = None
        assets_index = None
        assets_doc = {}

    for slot_val in slots_raw:
        try:
            slot = int(slot_val)
        except Exception:
            continue
        if slot <= 0:
            continue

        # Prefer assets-index declared paths for slot deletion.
        slot_key = f"{int(slot):02d}"
        slot_entry = assets_index.current_slot_entry(assets_doc, slot_key) if assets_index else None
        if isinstance(slot_entry, dict):
            for key in ("composite", "thumb"):
                rel = slot_entry.get(key)
                if not isinstance(rel, str) or not rel:
                    continue
                try:
                    target = artwork_dir / rel
                    if target.exists() and target.is_file():
                        target.unlink()
                        removed += 1
                except Exception:
                    continue
        else:
            # Legacy fallback for deterministic names when assets index is unavailable.
            from application.mockups import config as mockups_config

            prefixes = [slug]
            sku_guess = _resolve_sku_for_slug(processed_dir)
            if sku_guess and sku_guess.lower() != slug.lower():
                prefixes.append(sku_guess.lower())
            for prefix in prefixes:
                comp_path = processed_dir / mockups_config.MOCKUPS_SUBDIR / mockups_config.COMPOSITE_BASENAME.format(slug=prefix, slot=int(slot))
                thumb_path = (
                    processed_dir
                    / mockups_config.MOCKUPS_SUBDIR
                    / mockups_config.THUMBS_SUBDIR
                    / mockups_config.THUMB_BASENAME.format(slug=prefix, slot=int(slot))
                )
                for p in (comp_path, thumb_path):
                    try:
                        if p.exists() and p.is_file():
                            p.unlink()
                            removed += 1
                    except Exception:
                        continue

        removed_slots.append(int(slot))

    # Best-effort: also remove deleted slots from the per-artwork assets index.
    try:
        from application.mockups import storage as mockups_storage

        if not assets_index or not assets_path:
            raise ValueError("assets index unavailable")
        mockups_doc = assets_doc.get("mockups")
        if not isinstance(mockups_doc, dict):
            mockups_doc = {}
        assets_map = mockups_doc.get("assets")
        if not isinstance(assets_map, dict):
            assets_map = {}
        for slot in removed_slots:
            assets_map.pop(f"{int(slot):02d}", None)
        mockups_doc["assets"] = assets_map
        assets_doc["mockups"] = mockups_doc
        mockups_storage.atomic_write_json(assets_doc, assets_path)
    except Exception:
        pass

    if removed_slots:
        log_security_event(
            user_id=session.get("username"),
            action="delete_selected_mockups",
            details=f"slug={slug} slots={','.join([str(s) for s in removed_slots])} removed={int(removed)}",
        )

    return {"status": "ok", "removed": int(removed), "slug": slug, "slots": removed_slots}
