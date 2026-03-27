import json
import os
from hashlib import sha256
from pathlib import Path
from typing import Any

from application.utils.json_util import safe_json_dump


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_bytes_atomic(path: Path, data: bytes) -> None:
    ensure_dir(path.parent)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "wb") as tmp:
        tmp.write(data)
    os.replace(tmp_path, path)


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    ensure_dir(path.parent)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as tmp:
        safe_json_dump(payload, tmp, indent=2, sort_keys=True)
    os.replace(tmp_path, path)


def file_hash(data: bytes) -> str:
    return sha256(data).hexdigest()


def sanitize_etsy_filename(seo_slug: str, sku: str | None = None, max_length: int = 66) -> str:
    """Sanitize and truncate filename for Etsy's 70-character limit.
    
    Args:
        seo_slug: The SEO-friendly filename slug (before .jpg extension)
        sku: Optional SKU to append (typically artwork ID)
        max_length: Maximum length before .jpg extension (default: 66 to allow for .jpg = 70 total)
    
    Returns:
        Clean filename string (without .jpg extension) that meets Etsy requirements.
        Format: [Short-Title]-[Location]-Digital-Art-Robin-Custance
        Truncates at nearest hyphen if exceeding max_length.
    
    Example:
        >>> sanitize_etsy_filename("bool-lagoon-wetlands-sunset-digital-art-robin-custance", "RJC-0270")
        'bool-lagoon-wetlands-sunset-digital-art-robin-custance-RJC-0270'
    """
    base = str(seo_slug or "").strip()
    if not base:
        return "artwork"
    
    # Remove .jpg extension if present
    if base.lower().endswith(".jpg"):
        base = base[:-4]
    
    # Append SKU if provided
    if sku:
        sku_clean = str(sku).strip()
        if sku_clean:
            base = f"{base}-{sku_clean}".strip("-")
    
    # If within limit, return as-is
    if len(base) <= max_length:
        return base
    
    # Truncate at nearest hyphen before max_length
    # Find the last hyphen before or at max_length
    truncated = base[:max_length]
    last_hyphen = truncated.rfind("-")
    
    if last_hyphen > 0:
        # Truncate at the last hyphen to keep it clean
        base = base[:last_hyphen]
    else:
        # No hyphen found, hard truncate at max_length
        base = base[:max_length]
    
    # Strip any trailing hyphens
    return base.rstrip("-")
