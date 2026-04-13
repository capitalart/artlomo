"""Manual workflow services (promotion, metadata, mockup enqueue).

Storage contract (enforced): a slug may live in only one lab tier at a time.
- lab/unprocessed/<slug>
- lab/processed/<slug>
- lab/locked/<slug>
Legacy processed/manual content is migrated forward and removed once verified.
"""

from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

from flask import current_app

import application.config as config
from application.common.utilities.files import ensure_dir, write_bytes_atomic, write_json_atomic
from application.common.utilities.slug_sku import is_safe_slug
from application.utils import categories, sku_assigner
from application.upload.services.storage_service import SEED_CONTEXT_NAME

from ..errors import ManualValidationError, ManualWorkflowError


# Filenames follow the upload workflow conventions to avoid cross-workflow imports.
META_NAME = "metadata.json"
QC_NAME = "qc.json"


def _meta_name(sku: str | None = None) -> str:
    """Return metadata filename with optional SKU prefix."""
    return f"{sku.lower()}-metadata.json" if sku else META_NAME


def _qc_name(sku: str | None = None) -> str:
    """Return QC filename with optional SKU prefix."""
    return f"{sku.lower()}-qc.json" if sku else QC_NAME


def _listing_name(sku: str | None = None) -> str:
    """Return listing filename with optional SKU prefix."""
    return f"{sku.lower()}-listing.json" if sku else "listing.json"


logger = logging.getLogger(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_slug(slug: str) -> str:
    trimmed = (slug or "").strip()
    if not trimmed:
        raise ManualWorkflowError("Slug is required for manual analysis.")
    if not is_safe_slug(trimmed):
        raise ManualWorkflowError("Invalid slug.")
    return trimmed


def _cfg() -> dict:
    return current_app.config


def _log(event: str, extra: dict[str, Any]) -> None:
    try:
        current_app.logger.info(event, extra=extra)
    except Exception:
        logger.info("%s %s", event, extra)


def _unprocessed_root() -> Path:
    root = _cfg().get("LAB_UNPROCESSED_DIR")
    if not root:
        raise ManualWorkflowError("Unprocessed directory is not configured.")
    return Path(root)


def _processed_root() -> Path:
    root = _cfg().get("LAB_PROCESSED_DIR")
    if not root:
        raise ManualWorkflowError("Processed directory is not configured.")
    ensure_dir(Path(root))
    return Path(root)


def _locked_root() -> Path:
    root = _cfg().get("LAB_LOCKED_DIR")
    if not root:
        raise ManualWorkflowError("Locked directory is not configured.")
    ensure_dir(Path(root))
    return Path(root)


def _legacy_manual_root() -> Path:
    return _processed_root() / "manual"


def _processed_dir(slug: str) -> Path:
    target = _processed_root() / _require_slug(slug)
    if target.exists():
        return target
    # Attempt to migrate legacy content on-demand for this slug.
    legacy_dir = _legacy_manual_root() / _require_slug(slug)
    if legacy_dir.exists():
        summary = migrate_legacy_manual_storage(slug_filter={_require_slug(slug)})
        if target.exists():
            _log("manual.storage.migrated_on_demand", {"slug": slug, "summary": summary})
            return target
    raise ManualWorkflowError(f"Manual workspace missing for slug '{slug}'.")


def get_manual_asset_dir(slug: str) -> Path:
    """Return the directory containing manual assets for a slug."""

    return _processed_dir(slug)


def resolve_manual_assets(slug: str) -> dict[str, Path]:
    """Resolve deterministic manual asset paths for UI serving (thumb/analyse).

    MASTER images are intentionally excluded. Mockups may be served via
    explicit filenames under the `mockups/` prefix; this resolver focuses on
    core assets used by the UI contract.
    
    Asset filenames are loaded from SKU-assets.json as the single source of truth.
    """

    manual_dir = _processed_dir(slug)
    
    # Load assets.json to get the authoritative filenames
    thumb_name = None
    analyse_name = None
    
    # Try to find and load assets manifest
    assets_files = list(manual_dir.glob("*-assets.json"))
    if assets_files:
        assets_path = assets_files[0]
        try:
            import json
            assets_doc = json.loads(assets_path.read_text(encoding="utf-8"))
            files = assets_doc.get("files") or {}
            thumb_name = files.get("thumb")
            analyse_name = files.get("analyse")
        except Exception:
            pass
    
    # Fallback to legacy hardcoded names if not found in assets
    if not thumb_name:
        thumb_name = f"{slug}-THUMB.jpg"
    if not analyse_name:
        analyse_name = f"{slug}-ANALYSE.jpg"
    
    thumb_path = manual_dir / thumb_name
    analyse_path = manual_dir / analyse_name

    missing: list[str] = []
    if not thumb_path.exists():
        missing.append(thumb_name)
    if not analyse_path.exists():
        missing.append(analyse_name)
    if missing:
        raise ManualWorkflowError(f"Missing manual assets: {', '.join(missing)}")

    return {"thumb": thumb_path, "analyse": analyse_path}


def get_manual_asset(slug: str, filename: str) -> Path:
    """Return a validated path for a manual asset.

    Allowed filenames:
    - <slug>-THUMB.jpg
    - <slug>-ANALYSE.jpg
    - paths under mockups/ (no traversal)
    """

    manual_dir = _processed_dir(slug)
    safe_name = filename.strip("/")
    thumb = f"{slug}-THUMB.jpg"
    analyse = f"{slug}-ANALYSE.jpg"

    allowed_roots: list[Path] = []
    if safe_name == thumb:
        allowed_roots.append(manual_dir / thumb)
    elif safe_name == analyse:
        allowed_roots.append(manual_dir / analyse)
    elif safe_name.startswith("mockups/"):
        allowed_roots.append(manual_dir / safe_name)
    else:
        raise ManualWorkflowError("Requested asset not permitted for manual workflow.")

    asset_path = allowed_roots[0]
    try:
        asset_path.resolve().relative_to(manual_dir.resolve())
    except Exception as exc:  # pragma: no cover - defensive
        raise ManualWorkflowError("Invalid asset path.") from exc

    if not asset_path.exists():
        raise ManualWorkflowError("Requested asset is missing.")
    return asset_path


def _ensure_unprocessed_artwork(slug: str) -> Path:
    slug_dir = _unprocessed_root() / slug
    if not slug_dir.exists():
        raise ManualWorkflowError(f"Artwork '{slug}' not found in unprocessed storage.")
    return slug_dir


def _assert_not_elsewhere(slug: str) -> None:
    processed_dir = _processed_root() / slug
    locked_dir = _locked_root() / slug
    if processed_dir.exists():
        raise ManualWorkflowError(f"Artwork '{slug}' already exists in processed storage.")
    if locked_dir.exists():
        raise ManualWorkflowError(f"Artwork '{slug}' is locked and cannot be promoted.")


def _load_json(path: Path, *, required: bool = True) -> dict:
    if not path.exists():
        if required:
            raise ManualWorkflowError(f"Missing required file: {path.name}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManualWorkflowError(f"Invalid JSON payload: {path.name}") from exc


def _copy_if_present(src: Path, dest: Path) -> None:
    try:
        data = src.read_bytes()
    except FileNotFoundError as exc:
        raise ManualWorkflowError(f"Required asset missing: {src.name}") from exc
    write_bytes_atomic(dest, data)


def _move_dir_atomic(src: Path, dest: Path) -> None:
    if dest.exists():
        raise ManualWorkflowError(f"Destination already exists: {dest}")
    ensure_dir(dest.parent)
    try:
        src.replace(dest)
    except Exception as exc:  # pragma: no cover - filesystem guard
        raise ManualWorkflowError(f"Failed to move {src} to {dest}") from exc


def _sku_from_meta(meta: dict) -> str:
    value = str(meta.get("sku") or meta.get("artwork_id") or "").strip()
    if value:
        return value
    tracker_path = Path(getattr(config, "SKU_TRACKER", Path("var") / "state" / "sku_tracker.json"))
    ensure_dir(tracker_path.parent)
    return sku_assigner.get_next_sku(tracker_path)


def _registry_path() -> Path:
    path = _cfg().get("ARTWORKS_INDEX_PATH")
    if path:
        return Path(path)
    base = Path(_cfg().get("LAB_INDEX_DIR", Path("lab") / "index"))
    return base / "artworks.json"


def _upsert_registry(*, sku: str, slug: str, listing_filename: str) -> None:
    index_path = _registry_path()
    ensure_dir(index_path.parent)
    if index_path.exists():
        try:
            doc = json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            doc = {}
    else:
        doc = {}

    now = _now_iso()
    if "items" not in doc or not isinstance(doc.get("items"), dict):
        doc = {"version": 1, "items": {}, "updated_at": now}

    items: Dict[str, Dict[str, Any]] = doc.get("items", {})
    existing = items.get(sku) or {}
    created_at = existing.get("created_at", now)
    items[sku] = {
        "sku": sku,
        "slug": slug,
        "artwork_dirname": slug,
        "assets_file": listing_filename,
        "created_at": created_at,
        "updated_at": now,
        "version": 1,
    }
    doc["items"] = items
    doc["updated_at"] = now
    write_json_atomic(index_path, doc)


def _seed_listing_payload(*, slug: str, sku: str, meta: dict, thumb_name: str, analyse_name: str, hero_name: str) -> dict:
    return {
        "slug": slug,
        "sku": sku,
        "title": meta.get("display_title", ""),
        "description": meta.get("description", ""),
        "tags": meta.get("tags") or [],
        "materials": meta.get("materials") or [],
        "price": meta.get("price") or "",
        "quantity": meta.get("quantity") or config.LISTING_DEFAULTS.get("QUANTITY", 0),
        "category": meta.get("category", ""),
        "seo_filename": meta.get("seo_filename", ""),
        "analysis_source": "manual",
        "images": {
            "hero": hero_name,
            "small": thumb_name,
            "analyse": analyse_name,
        },
        "artist": meta.get("artist", {}),
        "created_at": meta.get("created_at") or _now_iso(),
        "updated_at": _now_iso(),
    }


def _write_listing(dest_dir: Path, payload: dict, sku: str | None = None) -> Path:
    filename = _listing_name(sku)
    listing_path = dest_dir / filename
    write_json_atomic(listing_path, payload)
    return listing_path


def _split_csv(value: str | None) -> List[str]:
    if not value:
        return []
    return [part.strip() for part in str(value).split(",") if part.strip()]


def _coerce_float(value: str | None) -> float | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(str(value).replace(",", "").strip())
    except Exception:
        return None


def _coerce_int(value: str | None, default: int) -> int:
    try:
        if value is None or str(value).strip() == "":
            return default
        return int(float(str(value).replace(",", "").strip()))
    except Exception:
        return default


def promote_unanalysed_to_manual(slug: str) -> dict[str, Any]:
    """Promote an unanalysed artwork into the manual workspace.

    - Validates unprocessed slug exists
    - Ensures slug does not already exist in processed/locked
    - Moves unprocessed/<slug> → processed/<slug> atomically
    - Seeds listing.json with analysis_source=manual
    - Registers into the artworks registry
    - Updates database status from 'unprocessed' to 'processed'
    """

    validated = _require_slug(slug)
    source_dir = _ensure_unprocessed_artwork(validated)

    meta = _load_json(source_dir / META_NAME)
    qc = _load_json(source_dir / QC_NAME)

    sku = _sku_from_meta(meta)
    manual_slug = meta.get("slug") or validated

    _assert_not_elsewhere(manual_slug)
    dest_dir = _processed_root() / manual_slug

    # Move entire folder to enforce single-source-of-truth placement.
    _move_dir_atomic(source_dir, dest_dir)

    # Ensure mockups folder exists for downstream pipelines.
    ensure_dir(dest_dir / "mockups")

    master_name = meta.get("stored_filename") or f"{validated}.jpg"
    thumb_name = meta.get("thumb_filename") or f"{validated}-THUMB.jpg"
    analyse_name = meta.get("analyse_filename") or f"{validated}-ANALYSE.jpg"

    write_json_atomic(dest_dir / _meta_name(sku), meta)
    write_json_atomic(dest_dir / _qc_name(sku), qc)

    listing_payload = _seed_listing_payload(
        slug=manual_slug,
        sku=sku,
        meta=meta,
        thumb_name=thumb_name,
        analyse_name=analyse_name,
        hero_name=master_name,
    )
    listing_path = _write_listing(dest_dir, listing_payload, sku=sku)
    _upsert_registry(sku=sku, slug=manual_slug, listing_filename=listing_path.name)

    # Update database status to 'processed' after successful promotion
    try:
        from application.utils.artwork_db import update_artwork_status
        update_artwork_status(sku, "processed")
    except Exception as e:
        logger.error(f"Failed to update DB status for {sku} to 'processed': {e}")

    _log(
        "manual.promote_unanalysed_to_manual",
        {"slug": validated, "manual_slug": manual_slug, "sku": sku, "dest_dir": str(dest_dir)},
    )
    return {"manual_slug": manual_slug, "listing_path": str(listing_path)}


def _load_listing(manual_slug: str) -> tuple[Path, dict]:
    manual_dir = _processed_dir(manual_slug)
    listing_path = manual_dir / "listing.json"
    if not listing_path.exists():
        meta = _load_json(manual_dir / META_NAME, required=False)
        listing_payload = _seed_listing_payload(
            slug=manual_slug,
            sku=_sku_from_meta(meta),
            meta=meta,
            thumb_name=meta.get("thumb_filename", ""),
            analyse_name=meta.get("analyse_filename", ""),
            hero_name=meta.get("stored_filename", ""),
        )
        _write_listing(manual_dir, listing_payload)
        return manual_dir, listing_payload
    listing = _load_json(listing_path)
    if "analysis_source" not in listing:
        listing["analysis_source"] = "manual"
    return manual_dir, listing


def _mockup_previews(manual_dir: Path) -> List[str]:
    previews: List[str] = []
    thumbs_dir = manual_dir / "mockups" / "thumbs"
    if not thumbs_dir.exists() or not thumbs_dir.is_dir():
        return previews
    for path in sorted(thumbs_dir.glob("*.jpg")):
        previews.append(f"mockups/thumbs/{path.name}")
    return previews


def load_manual_listing(slug: str) -> dict[str, Any]:
    manual_slug = _require_slug(slug)
    manual_dir, listing = _load_listing(manual_slug)
    listing = {**listing}  # shallow copy for normalization
    listing["display_title"] = listing.get("title", "")
    listing["tags"] = ", ".join(listing.get("tags") or [])
    listing["materials"] = ", ".join(listing.get("materials") or [])
    listing["mockup_previews"] = _mockup_previews(manual_dir)
    return listing


def save_manual_metadata(slug: str, form_data: dict[str, Any]) -> dict[str, Any]:
    manual_slug = _require_slug(slug)
    manual_dir, listing = _load_listing(manual_slug)

    aspect = listing.get("aspect_ratio") or getattr(config, "DEFAULT_ASPECT", "3x4")
    valid_categories = {opt["value"] for opt in categories.list_category_options(aspect)}
    category_input = (form_data.get("category") or "").strip()
    if category_input and valid_categories and category_input not in valid_categories:
        raise ManualValidationError("Invalid category for selected aspect.")

    tags = _split_csv(form_data.get("tags"))
    materials = _split_csv(form_data.get("materials"))
    price = _coerce_float(form_data.get("price"))
    quantity_default = config.LISTING_DEFAULTS.get("QUANTITY", 0)
    quantity = _coerce_int(form_data.get("quantity"), quantity_default)
    sku_input = (form_data.get("sku") or "").strip()

    # Visual Analysis fields (atomic merge — only overwrite keys that are present)
    va_patch = {}
    for va_key, form_key in (("subject", "va_subject"), ("dot_rhythm", "va_dot_rhythm"), ("palette", "va_palette"), ("mood", "va_mood")):
        val = (form_data.get(form_key) or "").strip()
        if val:
            va_patch[va_key] = val

    existing_va = listing.get("visual_analysis") or {}
    if isinstance(existing_va, dict):
        merged_va = {**existing_va, **va_patch}
    else:
        merged_va = va_patch
    if merged_va:
        listing["visual_analysis"] = merged_va

    # Extract seed context fields if present in form_data
    seed_context_patch = {}
    for key in ("location", "sentiment", "original_prompt"):
        val = (form_data.get(key) or "").strip()
        if val:
            seed_context_patch[key] = val
    
    if seed_context_patch:
        seed_context_path = manual_dir / SEED_CONTEXT_NAME
        existing_seed = _load_json(seed_context_path, required=False)
        updated_seed = {**existing_seed, **seed_context_patch}
        updated_seed["updated_at"] = _now_iso()
        if "created_at" not in updated_seed:
            updated_seed["created_at"] = updated_seed["updated_at"]
        write_json_atomic(seed_context_path, updated_seed)

    listing.update(
        {
            "title": (form_data.get("title") or "").strip(),
            "description": (form_data.get("description") or "").strip(),
            "tags": tags,
            "materials": materials,
            "price": price,
            "quantity": quantity,
            "category": category_input,
            "seo_filename": (form_data.get("seo_filename") or "").strip(),
            "materials_used": (form_data.get("materials") or "").strip(),
            "location_inspiration": (form_data.get("location") or "").strip(),
            "sentiment": (form_data.get("sentiment") or "").strip(),
            "original_prompt": (form_data.get("original_prompt") or "").strip(),
            "updated_at": _now_iso(),
        }
    )

    if sku_input:
        listing["sku"] = sku_input

    listing_path = _write_listing(manual_dir, listing)
    snapshot_path = manual_dir / "metadata_manual.json"
    write_json_atomic(snapshot_path, listing)

    meta_path = manual_dir / META_NAME
    try:
        meta_doc = _load_json(meta_path, required=False)
    except ManualWorkflowError:
        meta_doc = None
    if meta_doc is not None:
        meta_doc["display_title"] = listing.get("title", "")
        meta_doc["title"] = listing.get("title", "")
        if sku_input:
            meta_doc["sku"] = sku_input
        meta_doc["updated_at"] = _now_iso()
        write_json_atomic(meta_path, meta_doc)

    sku = listing.get("sku") or _sku_from_meta(_load_json(manual_dir / META_NAME, required=False))
    _upsert_registry(sku=sku, slug=manual_slug, listing_filename=listing_path.name)

    current_app.logger.info(
        "manual.save_manual_metadata",
        extra={"slug": manual_slug, "fields": sorted(form_data.keys()), "snapshot": str(snapshot_path)},
    )
    return listing


def lock_manual_workspace(slug: str) -> dict[str, Any]:
    manual_slug = _require_slug(slug)
    manual_dir, listing = _load_listing(manual_slug)
    locked_dir = _locked_root() / manual_slug
    if locked_dir.exists():
        raise ManualWorkflowError("Artwork is already locked.")

    sku = listing.get("sku") or _sku_from_meta(_load_json(manual_dir / META_NAME, required=False))

    _move_dir_atomic(manual_dir, locked_dir)

    if sku:
        try:  # Best-effort index cleanup to avoid pointing at missing processed items
            from application.artwork.services.index_service import ArtworksIndex

            index_path = _cfg().get("ARTWORKS_INDEX_PATH")
            processed_dir = _cfg().get("LAB_PROCESSED_DIR")
            if index_path and processed_dir:
                ArtworksIndex(Path(index_path), Path(processed_dir)).remove_by_sku(sku)
        except Exception:  # pragma: no cover - non-blocking cleanup
            current_app.logger.warning("manual.lock_manual_workspace.index_cleanup_failed", extra={"slug": manual_slug, "sku": sku})

    _log("manual.lock_manual_workspace", {"slug": manual_slug, "locked_dir": str(locked_dir)})
    return {"slug": manual_slug, "locked_dir": str(locked_dir), "sku": sku}


def enqueue_mockups(slug: str) -> None:
    manual_slug = _require_slug(slug)
    try:
        # Attempt to call the mockups pipeline if available; best-effort only.
        from application.mockups import generate_mockups_for_artwork  # type: ignore

        _, listing = _load_listing(manual_slug)
        sku = listing.get("sku")
        if not sku:
            raise ManualWorkflowError("SKU missing; cannot enqueue mockups.")
        current_app.logger.info("manual.enqueue_mockups", extra={"slug": manual_slug, "sku": sku})
        # Without template context, defer to pipeline defaults; callers can extend later.
        generate_mockups_for_artwork(
            sku=sku,
            template_slug="auto",
            aspect_ratio=listing.get("aspect_ratio") or getattr(config, "DEFAULT_ASPECT", "3x4"),
            base_image_path=Path(config.MOCKUPS_INPUT_DIR) / "templates" / "auto.png",
            coords_path=Path(config.COORDS_DIR) / "auto.json",
            slot=1,
            mode="generate",
            master_index_path=_registry_path(),
            processed_root=Path(_cfg().get("LAB_PROCESSED_DIR", config.PROCESSED_ROOT)),
        )
    except Exception as exc:  # pragma: no cover - best-effort guard
        current_app.logger.warning("manual.enqueue_mockups.failed", extra={"slug": manual_slug, "error": str(exc)})


def _iter_files(base: Path) -> List[Path]:
    return [p for p in base.rglob("*") if p.is_file()]


def migrate_legacy_manual_storage(*, slug_filter: Set[str] | None = None) -> dict[str, Any]:
    """Merge legacy processed/manual content into processed root safely.

    - If only legacy folder exists, move it wholesale to processed/<slug>.
    - If both exist, copy only missing files into processed/<slug>.
    - Remove legacy folder only after verifying all files are present in
      processed/<slug>.
    """

    processed_root = _processed_root()
    legacy_root = _legacy_manual_root()
    summary: dict[str, Any] = {
        "legacy_present": legacy_root.exists(),
        "moved": [],
        "merged": [],
        "removed": [],
        "conflicts": [],
        "skipped": [],
    }

    if not legacy_root.exists() or not legacy_root.is_dir():
        return summary

    for legacy_dir in sorted(p for p in legacy_root.iterdir() if p.is_dir()):
        slug_name = legacy_dir.name
        if slug_filter and slug_name not in slug_filter:
            summary["skipped"].append(slug_name)
            continue

        canonical_dir = processed_root / slug_name
        files = _iter_files(legacy_dir)
        rel_files: List[Path] = [p.relative_to(legacy_dir) for p in files]

        if not canonical_dir.exists():
            _move_dir_atomic(legacy_dir, canonical_dir)
            summary["moved"].append(slug_name)
            _log("manual.storage.migrated.move", {"slug": slug_name, "dest": str(canonical_dir)})
            continue

        merged: List[str] = []
        for rel in rel_files:
            src = legacy_dir / rel
            dest = canonical_dir / rel
            if dest.exists():
                continue
            ensure_dir(dest.parent)
            _copy_if_present(src, dest)
            merged.append(str(rel))

        missing_after: List[str] = [str(rel) for rel in rel_files if not (canonical_dir / rel).exists()]
        if missing_after:
            summary["conflicts"].append({"slug": slug_name, "missing": missing_after})
            _log(
                "manual.storage.migrated.conflict",
                {"slug": slug_name, "missing": missing_after, "canonical": str(canonical_dir)},
            )
            continue

        try:
            shutil.rmtree(legacy_dir)
            summary["removed"].append(slug_name)
            summary["merged"].append({"slug": slug_name, "merged_files": merged})
            _log(
                "manual.storage.migrated.merge",
                {"slug": slug_name, "merged_files": merged, "canonical": str(canonical_dir)},
            )
        except Exception as exc:  # pragma: no cover - filesystem guard
            summary["conflicts"].append({"slug": slug_name, "error": str(exc)})
            _log("manual.storage.migrated.cleanup_failed", {"slug": slug_name, "error": str(exc)})

    # Remove the legacy root if empty and no conflicts remain.
    try:
        if not summary["conflicts"] and legacy_root.exists() and not any(legacy_root.iterdir()):
            shutil.rmtree(legacy_root)
            _log("manual.storage.migrated.root_removed", {"legacy_root": str(legacy_root)})
    except Exception as exc:  # pragma: no cover - defensive
        _log("manual.storage.migrated.root_cleanup_failed", {"legacy_root": str(legacy_root), "error": str(exc)})

    return summary


def ensure_manual_storage_migrated(slug: str | None = None) -> dict[str, Any]:
    summary = migrate_legacy_manual_storage(slug_filter={_require_slug(slug)} if slug else None)
    if summary.get("conflicts"):
        raise ManualWorkflowError(f"Manual storage migration incomplete: {summary['conflicts']}")
    return summary
