"""Assets Index Sync - Keep assets.json synchronized with directory contents."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def sync_assets_index(artwork_dir: Path, sku: str | None = None) -> bool:
    """Synchronize assets.json with actual directory contents.
    
    Args:
        artwork_dir: Path to artwork directory
        sku: Optional SKU (will try to extract from metadata if not provided)
        
    Returns:
        True if sync successful, False otherwise
    """
    if not artwork_dir.exists():
        logger.warning("[sync] Artwork directory does not exist: %s", artwork_dir)
        return False
    
    try:
        # Determine SKU if not provided
        if not sku:
            sku = _extract_sku(artwork_dir)
        
        # Load or create assets index
        assets_data = _load_or_create_assets(artwork_dir, sku)
        
        # Scan and update files
        _update_image_files(artwork_dir, assets_data, sku)
        _update_metadata_files(artwork_dir, assets_data, sku)
        _update_directories(artwork_dir, assets_data)
        
        # Update timestamp and version
        assets_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        assets_data["version"] = 2
        
        # Write back atomically
        assets_path = artwork_dir / f"{sku.lower()}-assets.json"
        assets_path.write_text(json.dumps(assets_data, indent=2) + "\n")
        
        logger.info("[sync] Updated assets index for %s (%d files)", sku, len(assets_data.get("files", {})))
        return True
        
    except Exception as e:
        logger.exception("[sync] Failed to sync assets index for %s: %s", artwork_dir.name, e)
        return False


def _extract_sku(artwork_dir: Path) -> str:
    """Extract SKU from metadata or use slug as fallback."""
    slug = artwork_dir.name
    
    # Try to extract SKU from listing or metadata
    for candidate in [
        artwork_dir / f"{slug.lower()}-listing.json",
        artwork_dir / "listing.json",
        artwork_dir / f"{slug.lower()}-metadata.json",
        artwork_dir / "metadata.json"
    ]:
        if candidate.exists():
            try:
                doc = json.loads(candidate.read_text(encoding="utf-8"))
                if isinstance(doc, dict):
                    sku = str(doc.get("sku") or "").strip().lower()
                    if sku:
                        return sku
            except Exception:
                pass
    
    return slug.lower()


def _load_or_create_assets(artwork_dir: Path, sku: str) -> dict:
    """Load existing assets.json or create new one."""
    assets_path = artwork_dir / f"{sku}-assets.json"
    
    if assets_path.exists():
        try:
            return json.loads(assets_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    
    # Create new
    return {
        "sku": sku.upper(),
        "slug": artwork_dir.name,
        "version": 2,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "files": {},
        "directories": {},
        "mockups": {
            "dir": "mockups",
            "assets": {},
            "count": 0
        }
    }


def _update_image_files(artwork_dir: Path, assets_data: dict, sku: str) -> None:
    """Scan and update image file references."""
    files = assets_data.get("files") or {}
    
    # Define image file patterns to check (in priority order)
    image_patterns = {
        "master": [f"{sku}-MASTER.jpg", f"{artwork_dir.name}-MASTER.jpg", f"{artwork_dir.name}.jpg"],
        "analyse": [f"{sku}-ANALYSE.jpg", f"{artwork_dir.name}-ANALYSE.jpg"],
        "thumb": [f"{sku}-THUMB.jpg", f"{artwork_dir.name}-THUMB.jpg"],
        "closeup_proxy": [f"{artwork_dir.name}-CLOSEUP-PROXY.jpg"],
        "detail_closeup": [f"mockups/{artwork_dir.name}-detail-closeup.jpg"]
    }
    
    for key, patterns in image_patterns.items():
        found = None
        for pattern in patterns:
            candidate = artwork_dir / pattern
            if candidate.exists() and candidate.is_file():
                found = pattern
                break
        
        if found:
            files[key] = found
        elif key in files:
            # Remove if no longer exists
            del files[key]
    
    assets_data["files"] = files


def _update_metadata_files(artwork_dir: Path, assets_data: dict, sku: str) -> None:
    """Scan and update metadata file references."""
    files = assets_data.get("files") or {}
    
    # Define metadata patterns (SKU-prefixed first, then legacy)
    metadata_patterns = {
        "metadata": [f"{sku}-metadata.json", "metadata.json"],
        "listing": [f"{sku}-listing.json", "listing.json"],
        "qc": [f"{sku}-qc.json", "qc.json"],
        "status": [f"{sku}-status.json", "status.json"],
        "processing_status": [f"{sku}-processing_status.json", "processing_status.json"],
        "metadata_openai": [f"{sku}-metadata_openai.json", "metadata_openai.json"],
        "metadata_gemini": [f"{sku}-metadata_gemini.json", "metadata_gemini.json"],
        "seed_context": ["seed_context.json"]
    }
    
    for key, candidates in metadata_patterns.items():
        found = None
        for candidate_name in candidates:
            candidate = artwork_dir / candidate_name
            if candidate.exists() and candidate.is_file():
                found = candidate_name
                break
        
        if found:
            files[key] = found
        elif key in files:
            # Remove if no longer exists
            del files[key]
    
    assets_data["files"] = files


def _update_directories(artwork_dir: Path, assets_data: dict) -> None:
    """Scan and update directory references."""
    dirs = assets_data.get("directories") or {}
    mockups = assets_data.get("mockups") or {}
    
    # Check for mockups subdirectory
    mockups_dir = artwork_dir / "mockups"
    if mockups_dir.exists() and mockups_dir.is_dir():
        dirs["mockups"] = "mockups"
        
        # Count mockup files
        mockup_files = list(mockups_dir.glob("*.jpg")) + list(mockups_dir.glob("*.jpeg"))
        mockups["count"] = len(mockup_files)
    else:
        # Remove mockups reference if directory no longer exists
        if "mockups" in dirs:
            del dirs["mockups"]
        if "count" in mockups:
            mockups["count"] = 0
    
    assets_data["directories"] = dirs
    assets_data["mockups"] = mockups
