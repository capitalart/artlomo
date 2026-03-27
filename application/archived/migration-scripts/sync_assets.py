#!/usr/bin/env python3
"""
One-time sync script: Migrate artwork JSON files to database.
Scans lab/unprocessed, lab/processed, lab/locked and creates/updates Artwork rows.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import SessionLocal, Artwork


def parse_datetime(val: str | None) -> datetime | None:
    """Parse ISO datetime string."""
    if not val:
        return None
    try:
        # Handle various ISO formats
        val = val.replace("Z", "+00:00")
        if "+" in val:
            val = val.split("+")[0]
        return datetime.fromisoformat(val)
    except Exception:
        return None


def find_thumbnail(slug_dir: Path, slug: str, meta: dict) -> str | None:
    """Find the actual thumbnail file in a slug directory."""
    # Possible thumbnail filenames
    candidates = [
        meta.get("thumb_filename"),
        f"{slug}-THUMB.jpg",
        f"{slug.upper()}-THUMB.jpg",
        f"{slug.lower()}-THUMB.jpg",
    ]
    # Also check for SKU-based names
    sku = meta.get("sku") or meta.get("artwork_id")
    if sku:
        candidates.extend([
            f"{sku}-THUMB.jpg",
            f"{sku.upper()}-THUMB.jpg",
            f"{sku.lower()}-THUMB.jpg",
        ])
    
    for candidate in candidates:
        if candidate and (slug_dir / candidate).exists():
            return candidate
    
    # Check for any *THUMB* file
    for f in slug_dir.iterdir():
        if f.is_file() and "THUMB" in f.name.upper() and f.suffix.lower() in (".jpg", ".jpeg", ".png"):
            return f.name
    
    return None


def sync_artwork_folder(folder: Path, status: str, session) -> int:
    """Sync all artworks in a folder to the database."""
    synced = 0
    
    if not folder.exists():
        print(f"  Folder does not exist: {folder}")
        return 0
    
    for slug_dir in folder.iterdir():
        if not slug_dir.is_dir():
            continue
        if slug_dir.name.startswith("."):
            continue
            
        metadata_path = slug_dir / "metadata.json"
        listing_path = slug_dir / "listing.json"
        
        # Try metadata.json first, then listing.json
        meta = {}
        if metadata_path.exists():
            try:
                meta = json.loads(metadata_path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  Error reading {metadata_path}: {e}")
                continue
        elif listing_path.exists():
            try:
                meta = json.loads(listing_path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  Error reading {listing_path}: {e}")
                continue
        else:
            print(f"  No metadata found for {slug_dir.name}, skipping")
            continue
        
        # Extract fields
        sku = meta.get("sku") or meta.get("artwork_id") or slug_dir.name.upper()
        slug = meta.get("slug") or slug_dir.name
        title = meta.get("display_title") or meta.get("etsy_title") or meta.get("title") or sku
        owner_id = meta.get("owner_id") or meta.get("artist", {}).get("slug") or None
        analysis_source = meta.get("analysis_source")
        image_path = meta.get("stored_filename")
        
        # Find actual thumbnail file
        thumb_path = find_thumbnail(slug_dir, slug, meta)
        if thumb_path:
            print(f"    Found thumbnail: {thumb_path}")
        else:
            print(f"    No thumbnail found for {slug}, will use fallback")
        
        created_at = parse_datetime(meta.get("created_at"))
        updated_at = parse_datetime(meta.get("updated_at"))
        
        # Check if artwork exists
        existing = session.query(Artwork).filter_by(id=sku).first()
        
        if existing:
            # Update existing
            existing.slug = slug
            existing.title = title
            existing.owner_id = owner_id
            existing.status = status
            existing.analysis_source = analysis_source
            existing.image_path = image_path
            existing.thumb_path = thumb_path
            existing.metadata_json = json.dumps(meta, ensure_ascii=False)
            if updated_at:
                existing.updated_at = updated_at
            print(f"  Updated: {sku} ({status})")
        else:
            # Create new
            artwork = Artwork(
                id=sku,
                slug=slug,
                title=title,
                owner_id=owner_id,
                status=status,
                analysis_source=analysis_source,
                image_path=image_path,
                thumb_path=thumb_path,
                metadata_json=json.dumps(meta, ensure_ascii=False),
                created_at=created_at or datetime.utcnow(),
                updated_at=updated_at or datetime.utcnow(),
            )
            session.add(artwork)
            print(f"  Created: {sku} ({status})")
        
        synced += 1
    
    return synced


def find_artwork_in_lab(slug: str, lab_root: Path) -> tuple[Path | None, str | None]:
    """Search all lab folders for an artwork by slug. Returns (path, status) or (None, None)."""
    for status in ["unprocessed", "processed", "locked"]:
        folder = lab_root / status / slug
        if folder.exists() and folder.is_dir():
            return folder, status
    return None, None


def prune_ghost_entries(session, lab_root: Path) -> int:
    """Remove DB entries that don't have corresponding physical folders."""
    pruned = 0
    all_artworks = session.query(Artwork).all()
    
    for art in all_artworks:
        slug = art.slug
        db_status = art.status
        
        # Skip deleted items (they're in trash)
        if db_status == "deleted":
            continue
        
        # Check if artwork exists in its expected location
        expected_folder = lab_root / db_status / slug
        
        if expected_folder.exists():
            continue  # All good
        
        # Not in expected location - search other folders
        found_folder, actual_status = find_artwork_in_lab(slug, lab_root)
        
        if found_folder and actual_status:
            # Found in different location - update status
            print(f"  FIX: {art.id} was '{db_status}' but found in '{actual_status}' - updating")
            art.status = actual_status
        else:
            # Not found anywhere - delete ghost entry
            print(f"  PRUNE: {art.id} ({slug}) not found on disk - removing from DB")
            session.delete(art)
            pruned += 1
    
    return pruned


def verify_and_fix_status(session, lab_root: Path) -> int:
    """Verify DB status matches filesystem location and fix mismatches."""
    fixed = 0
    all_artworks = session.query(Artwork).filter(Artwork.status != "deleted").all()
    
    for art in all_artworks:
        slug = art.slug
        db_status = art.status
        
        # Find where artwork actually lives
        found_folder, actual_status = find_artwork_in_lab(slug, lab_root)
        
        if not found_folder:
            continue  # Will be handled by prune
        
        if db_status != actual_status:
            print(f"  STATUS FIX: {art.id} DB='{db_status}' -> actual='{actual_status}'")
            art.status = actual_status
            fixed += 1
    
    return fixed


def main():
    print("=" * 60)
    print("ARTWORK SYNC: JSON -> Database (Aggressive Mode)")
    print("=" * 60)
    
    lab_root = Path(__file__).resolve().parent / "application" / "lab"
    
    folders = [
        (lab_root / "unprocessed", "unprocessed"),
        (lab_root / "processed", "processed"),
        (lab_root / "locked", "locked"),
    ]
    
    total = 0
    
    with SessionLocal() as session:
        # Phase 1: Sync from filesystem to DB
        print("\n--- PHASE 1: Sync filesystem to database ---")
        for folder, status in folders:
            print(f"\nScanning {status}: {folder}")
            count = sync_artwork_folder(folder, status, session)
            total += count
            print(f"  Synced {count} artworks")
        
        # Phase 2: Verify and fix status mismatches
        print("\n--- PHASE 2: Verify and fix status mismatches ---")
        fixed = verify_and_fix_status(session, lab_root)
        print(f"  Fixed {fixed} status mismatches")
        
        # Phase 3: Prune ghost entries
        print("\n--- PHASE 3: Prune ghost entries ---")
        pruned = prune_ghost_entries(session, lab_root)
        print(f"  Pruned {pruned} ghost entries")
        
        session.commit()
    
    print("\n" + "=" * 60)
    print(f"SYNC COMPLETE: {total} synced, {fixed} fixed, {pruned} pruned")
    print("=" * 60)


if __name__ == "__main__":
    main()
