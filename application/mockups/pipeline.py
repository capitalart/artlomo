"""Index-driven, deterministic mockup generation pipeline (Phase 1)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Literal

from PIL import Image

from . import compositor, config, loader, storage, transforms, validation
from .assets_index import AssetsIndex
from .artwork_index import resolve_artwork
from .errors import HashMismatchError, ValidationError


def _normalize_template_name(name: str) -> str:
    return name[:-4] if name.lower().endswith(".png") else name


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _compute_content_hash(art_path: Path, base_path: Path, coords_path: Path) -> str:
    art_bytes = art_path.read_bytes()
    base_bytes = base_path.read_bytes()
    coords_bytes = coords_path.read_bytes()
    digest = storage.compute_hash(art_bytes, base_bytes, coords_bytes)
    return f"{config.HASH_ALGO}:{digest}"


def _generate_thumb(image: Image.Image) -> Image.Image:
    thumb = image.copy()
    thumb.thumbnail((config.THUMB_MAX_DIM, config.THUMB_MAX_DIM), Image.Resampling.LANCZOS)
    return thumb


def _composite(base_img: Image.Image, art_img: Image.Image, placements: Iterable) -> Image.Image:
    warped_layers = [transforms.warp_artwork_to_region(art_img, placement, base_img.size) for placement in placements]
    layered = compositor.composite_layers(base_img, warped_layers)
    return compositor.flatten_to_rgb(layered)


def generate_mockups_for_artwork(
    *,
    sku: str,
    template_slug: str,
    aspect_ratio: str,
    category: str | None = None,
    base_image_path: Path,
    coords_path: Path,
    slot: int,
    mode: Literal["generate", "swap"] = "generate",
    expected_hash: str | None = None,
    master_index_path: Path | None = None,
    processed_root: Path | None = None,
):
    if mode not in {"generate", "swap"}:
        raise ValidationError("Mode must be 'generate' or 'swap'")
    slot_num = validation.validate_slots([slot])[0]
    slot_key = f"{slot_num:02d}"

    artwork_dir, assets_path, slug = resolve_artwork(
        sku,
        master_index_path=master_index_path,
        processed_root=processed_root,
    )

    assets_index = AssetsIndex(artwork_dir, assets_path)
    assets_doc = assets_index.load()

    # Try closeup_proxy first (higher res), fallback to analyse, then suffix
    files_dict = assets_doc.get("files") or {}
    image_rel = files_dict.get("closeup_proxy") or files_dict.get("analyse")
    analyse_path = artwork_dir / image_rel if image_rel else (artwork_dir / f"{slug}{config.TARGET_IMAGE_NAME_SUFFIX}")
    if not analyse_path.exists():
        raise ValidationError("Source artwork image is missing (need CLOSEUP-PROXY or ANALYSE)")

    base_path = Path(base_image_path)
    coords_path = Path(coords_path)
    if not base_path.exists():
        raise ValidationError(f"Base image missing: {base_path}")
    if not coords_path.exists():
        raise ValidationError(f"Coordinate JSON missing: {coords_path}")

    coords_payload = loader.load_coords(coords_path)
    coord_spec = validation.validate_coordinate_schema(coords_payload)
    if _normalize_template_name(coord_spec.template) != _normalize_template_name(template_slug):
        raise ValidationError("Template slug does not match coordinate template")

    base_img = loader.load_base_rgba(base_path)
    validation.validate_corners_within_image(coord_spec, base_img.size)

    # Hash for determinism over artwork + base + coords
    content_hash = _compute_content_hash(analyse_path, base_path, coords_path)
    if expected_hash and mode == "generate" and expected_hash != content_hash:
        raise HashMismatchError("Content hash mismatch for generate")

    if mode == "generate":
        assets_index.guard_generate(assets_doc, slot_key)
    else:
        existing_entry = assets_index.guard_swap(assets_doc, slot_key)

    mockups_dirname = assets_index.mockups_dirname(assets_doc)
    output = storage.resolve_output_paths(artwork_dir, mockups_dirname, slug, slot_num)

    if mode == "swap":
        old_composite = (existing_entry or {}).get("composite")
        old_thumb = (existing_entry or {}).get("thumb")
        if old_composite:
            storage.delete_if_exists(artwork_dir / old_composite)
        if old_thumb:
            storage.delete_if_exists(artwork_dir / old_thumb)

    art_img = loader.load_artwork_rgba(analyse_path)
    composite_rgb = _composite(base_img, art_img, coord_spec.regions)

    storage.atomic_write_jpeg(composite_rgb, output["composite_path"])
    thumb = _generate_thumb(composite_rgb)
    storage.atomic_write_jpeg(thumb, output["thumb_path"])

    slot_entry = {
        "template_slug": template_slug,
        "aspect_ratio": aspect_ratio,
        "category": category,
        "regions": [placement.region_id for placement in coord_spec.regions],
        "composite": output["composite_path"].relative_to(artwork_dir).as_posix(),
        "thumb": output["thumb_path"].relative_to(artwork_dir).as_posix(),
        "hash": content_hash,
        "updated_at": _now_iso(),
    }

    assets_index.write_slot(assets_doc, slot_key, slot_entry)

    return slot_entry


def generate_mockups_for_slug(
    *,
    artwork_dir: Path,
    slug: str,
    template_slug: str,
    aspect_ratio: str,
    category: str | None = None,
    base_image_path: Path,
    coords_path: Path,
    slot: int,
    mode: Literal["generate", "swap"] = "generate",
    expected_hash: str | None = None,
) -> dict:
    if mode not in {"generate", "swap"}:
        raise ValidationError("Mode must be 'generate' or 'swap'")

    slot_num = validation.validate_slots([slot])[0]
    analyse_path = artwork_dir / f"{slug}{config.TARGET_IMAGE_NAME_SUFFIX}"
    if not analyse_path.exists():
        raise ValidationError("Source artwork image is missing (need CLOSEUP-PROXY or ANALYSE)")

    base_path = Path(base_image_path)
    coords_path = Path(coords_path)
    if not base_path.exists():
        raise ValidationError(f"Base image missing: {base_path}")
    if not coords_path.exists():
        raise ValidationError(f"Coordinate JSON missing: {coords_path}")

    coords_payload = loader.load_coords(coords_path)
    coord_spec = validation.validate_coordinate_schema(coords_payload)
    if _normalize_template_name(coord_spec.template) != _normalize_template_name(template_slug):
        raise ValidationError("Template slug does not match coordinate template")

    base_img = loader.load_base_rgba(base_path)
    validation.validate_corners_within_image(coord_spec, base_img.size)

    content_hash = _compute_content_hash(analyse_path, base_path, coords_path)
    if expected_hash and expected_hash != content_hash:
        raise HashMismatchError("Content hash mismatch")

    output = storage.resolve_output_paths(artwork_dir, config.MOCKUPS_SUBDIR, slug, slot_num)

    if mode == "swap":
        storage.delete_if_exists(output["composite_path"])
        storage.delete_if_exists(output["thumb_path"])

    art_img = loader.load_artwork_rgba(analyse_path)
    composite_rgb = _composite(base_img, art_img, coord_spec.regions)

    storage.atomic_write_jpeg(composite_rgb, output["composite_path"])
    thumb = _generate_thumb(composite_rgb)
    storage.atomic_write_jpeg(thumb, output["thumb_path"])

    return {
        "template_slug": template_slug,
        "aspect_ratio": aspect_ratio,
        "category": category,
        "regions": [placement.region_id for placement in coord_spec.regions],
        "composite": output["composite_path"].relative_to(artwork_dir).as_posix(),
        "thumb": output["thumb_path"].relative_to(artwork_dir).as_posix(),
        "hash": content_hash,
        "updated_at": _now_iso(),
    }
