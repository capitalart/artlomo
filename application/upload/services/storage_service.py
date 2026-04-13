from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
from ...common.utilities.files import ensure_dir, write_bytes_atomic, write_json_atomic
from ...common.utilities.slug_sku import slugify


QC_NAME = "qc.json"
META_NAME = "metadata.json"
LEGACY_META_NAME = "upload_meta.json"
PROCESSING_STATUS_NAME = "processing_status.json"
SEED_CONTEXT_NAME = "seed_context.json"


def _qc_name(sku: str | None = None) -> str:
    """Return QC filename with optional SKU prefix."""
    return f"{sku.lower()}-qc.json" if sku else QC_NAME


def _meta_name(sku: str | None = None) -> str:
    """Return metadata filename with optional SKU prefix."""
    return f"{sku.lower()}-metadata.json" if sku else META_NAME


def _processing_status_name(sku: str | None = None) -> str:
    """Return processing status filename with optional SKU prefix."""
    return f"{sku.lower()}-processing_status.json" if sku else PROCESSING_STATUS_NAME
PROCESSING_ALLOWED_STAGES = [
    "queued",
    "uploaded",
    "preparing",
    "uploading",
    "upload_complete",
    "processing",
    "closeup_proxy",
    "qc",
    "thumbnail",
    "derivatives",
    "metadata",
    "finalizing",
    "complete",
    "done",  # legacy alias
    "error",
]
ORIGINAL_SUFFIX = "-MASTER.jpg"
THUMB_SUFFIX = "-THUMB.jpg"
ANALYSE_SUFFIX = "-ANALYSE.jpg"


def target_dir(base_dir: Path, slug: str) -> Path:
    path = base_dir / slug
    ensure_dir(path)
    return path


def master_name(slug: str) -> str:
    return f"{slug}{ORIGINAL_SUFFIX}"


def thumb_name(slug: str) -> str:
    return f"{slug}{THUMB_SUFFIX}"


def analyse_name(slug: str) -> str:
    return f"{slug}{ANALYSE_SUFFIX}"


def store_original(slug_dir: Path, file_bytes: bytes, slug: str) -> Path:
    dest = slug_dir / master_name(slug)
    write_bytes_atomic(dest, file_bytes)
    return dest


def store_thumb(slug_dir: Path, thumb_bytes: bytes, slug: str) -> Path:
    dest = slug_dir / thumb_name(slug)
    write_bytes_atomic(dest, thumb_bytes)
    return dest


def store_analyse(slug_dir: Path, slug: str, image_bytes: bytes) -> Path:
    dest = slug_dir / analyse_name(slug)
    write_bytes_atomic(dest, image_bytes)
    return dest


def store_qc(slug_dir: Path, payload: dict[str, Any], sku: str | None = None) -> Path:
    filename = _qc_name(sku)
    dest = slug_dir / filename
    write_json_atomic(dest, payload)
    return dest


def store_meta(slug_dir: Path, payload: dict[str, Any], sku: str | None = None) -> Path:
    filename = _meta_name(sku)
    dest = slug_dir / filename
    write_json_atomic(dest, payload)
    return dest


def store_processing_status(slug_dir: Path, payload: dict[str, Any], sku: str | None = None) -> Path:
    filename = _processing_status_name(sku)
    dest = slug_dir / filename
    write_json_atomic(dest, payload)
    return dest


def base_meta(
    *,
    slug: str,
    artwork_id: str,
    display_title: str,
    artist_name: str,
    original_filename: str,
    prompt_text: str | None = None,
    owner_id: str | None = None,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "slug": slug,
        "artwork_id": artwork_id,
        "sku": artwork_id,
        "display_title": display_title or "",
        "artist": {"name": artist_name, "slug": slugify(artist_name) if artist_name else ""},
        "artist_name": artist_name,
        "original_filename": original_filename,
        "stored_filename": master_name(slug),
        "analyse_filename": analyse_name(slug),
        "thumb_filename": thumb_name(slug),
        "closeup_proxy_filename": f"{slug}-CLOSEUP-PROXY.jpg",
        "prompt": prompt_text,
        "owner_id": owner_id,
        "created_at": now,
        "updated_at": now,
    }


def list_artwork_dirs(root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if not root.exists():
        return items
    for slug_dir in sorted(root.iterdir()):
        if not slug_dir.is_dir():
            continue
        qc_payload = load_qc_with_fallback(slug_dir)
        meta_payload = load_metadata_with_fallback(slug_dir) or _read_json_or_none(slug_dir / LEGACY_META_NAME)

        thumb_candidates: list[str] = []
        if meta_payload and meta_payload.get("thumb_filename"):
            thumb_candidates.append(str(meta_payload["thumb_filename"]))

        thumb_candidates.append(thumb_name(slug_dir.name))

        legacy_id = None
        if meta_payload:
            legacy_id = meta_payload.get("artwork_id") or meta_payload.get("sku")
        if legacy_id:
            thumb_candidates.append(thumb_name(str(legacy_id)))

        thumb_path = None
        for candidate in thumb_candidates:
            candidate_path = slug_dir / candidate
            if candidate_path.exists():
                thumb_path = candidate_path
                break
        items.append(
            {
                "slug": slug_dir.name,
                "qc": qc_payload,
                "meta": meta_payload,
                "thumb_path": thumb_path if thumb_path and thumb_path.exists() else None,
            }
        )
    return items


def load_artwork(root: Path, slug: str) -> dict[str, Any] | None:
    slug_dir = root / slug
    if not slug_dir.exists() or not slug_dir.is_dir():
        return None
    qc_payload = load_qc_with_fallback(slug_dir)
    meta_payload = load_metadata_with_fallback(slug_dir) or _read_json_or_none(slug_dir / LEGACY_META_NAME)

    thumb_candidates: list[str] = []
    if meta_payload and meta_payload.get("thumb_filename"):
        thumb_candidates.append(str(meta_payload["thumb_filename"]))
    thumb_candidates.append(thumb_name(slug_dir.name))

    legacy_id = None
    if meta_payload:
        legacy_id = meta_payload.get("artwork_id") or meta_payload.get("sku")
    if legacy_id:
        thumb_candidates.append(thumb_name(str(legacy_id)))

    thumb_path = None
    for candidate in thumb_candidates:
        candidate_path = slug_dir / candidate
        if candidate_path.exists():
            thumb_path = candidate_path
            break

    return {
        "slug": slug_dir.name,
        "qc": qc_payload,
        "meta": meta_payload,
        "thumb_path": thumb_path if thumb_path and thumb_path.exists() else None,
    }


def read_processing_status(slug_dir: Path) -> dict[str, Any] | None:
    status_path = slug_dir / PROCESSING_STATUS_NAME
    if not status_path.exists():
        return None
    return _read_json_or_none(status_path)


def store_seed_context(slug_dir: Path, payload: dict[str, Any]) -> Path:
    """Store artist-provided seed context (location, notes, original prompt)."""
    now = datetime.now(timezone.utc).isoformat()
    payload["updated_at"] = now
    if "created_at" not in payload:
        payload["created_at"] = now
    dest = slug_dir / SEED_CONTEXT_NAME
    write_json_atomic(dest, payload)
    return dest


def load_seed_context(slug_dir: Path) -> dict[str, Any] | None:
    """Load artist-provided seed context if it exists."""
    context_path = slug_dir / SEED_CONTEXT_NAME
    return _read_json_or_none(context_path)


def load_assets_manifest(slug_dir: Path) -> dict[str, Any] | None:
    """Load assets manifest (source of truth for file references).
    
    Tries to find {sku}-assets.json or falls back to generic name.
    Returns the first found, or None if neither exists.
    """
    # Try to find SKU-prefixed assets file first
    for candidate in slug_dir.iterdir():
        if candidate.is_file() and candidate.name.endswith("-assets.json"):
            result = _read_json_or_none(candidate)
            if result is not None:
                return result
    
    # Fall back to generic assets.json
    assets_path = slug_dir / "assets.json"
    return _read_json_or_none(assets_path)


def load_qc_with_fallback(slug_dir: Path) -> dict[str, Any] | None:
    """Load QC with fallback logic for SKU-prefixed files.

    Tries in order:
    1. Any {prefix}-qc.json (SKU-prefixed version)
    2. qc.json (legacy version)

    Returns the first found, or None if neither exists.
    """
    for candidate in slug_dir.iterdir():
        if candidate.is_file() and candidate.name.endswith("-qc.json"):
            result = _read_json_or_none(candidate)
            if result is not None:
                return result

    qc_path = slug_dir / QC_NAME
    return _read_json_or_none(qc_path)


def load_metadata_with_fallback(slug_dir: Path) -> dict[str, Any] | None:
    """Load metadata with fallback logic for SKU-prefixed files.
    
    Tries in order:
    1. Any {prefix}-metadata.json (SKU-prefixed version)
    2. metadata.json (legacy version)
    
    Returns the first found, or None if neither exists.
    """
    # Try to find SKU-prefixed metadata file first
    for candidate in slug_dir.iterdir():
        if candidate.is_file() and candidate.name.endswith("-metadata.json"):
            result = _read_json_or_none(candidate)
            if result is not None:
                return result
    
    # Fall back to legacy metadata.json
    meta_path = slug_dir / META_NAME
    return _read_json_or_none(meta_path)


def list_unprocessed(unprocessed_root: Path) -> list[dict[str, Any]]:
    return list_artwork_dirs(unprocessed_root)


def list_processed(processed_root: Path) -> list[dict[str, Any]]:
    return list_artwork_dirs(processed_root)


def list_locked(locked_root: Path) -> list[dict[str, Any]]:
    return list_artwork_dirs(locked_root)


def _read_json_or_none(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
