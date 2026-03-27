#!/usr/bin/env python3
"""
Auto-purge script for 14-day old trash items.
Permanently removes artwork files and database records for items deleted more than 14 days ago.

Usage:
    python -m application.tools.purge_trash
    
Or call purge_old_trash() from app startup.
"""
from __future__ import annotations

import logging
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from db import SessionLocal, Artwork

logger = logging.getLogger(__name__)


def purge_old_trash(days: int = 14, dry_run: bool = False) -> dict:
    """
    Permanently delete artworks that have been in trash for more than `days` days.
    
    Args:
        days: Number of days after which deleted items are purged (default 14)
        dry_run: If True, only report what would be deleted without actually deleting
        
    Returns:
        dict with purge statistics
    """
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    stats = {
        "checked_at": datetime.utcnow().isoformat(),
        "cutoff_date": cutoff.isoformat(),
        "days_threshold": days,
        "dry_run": dry_run,
        "purged": [],
        "errors": [],
        "total_purged": 0,
    }
    
    try:
        with SessionLocal() as session:
            old_deleted = session.query(Artwork).filter(
                Artwork.status == "deleted",
                Artwork.deleted_at < cutoff
            ).all()
            
            if not old_deleted:
                logger.info(f"No items to purge (cutoff: {cutoff})")
                return stats
            
            logger.info(f"Found {len(old_deleted)} items to purge (cutoff: {cutoff})")
            
            for artwork in old_deleted:
                sku = artwork.id
                slug = artwork.slug
                prev_status = artwork.previous_status
                deleted_at = artwork.deleted_at
                
                item_info = {
                    "sku": sku,
                    "slug": slug,
                    "previous_status": prev_status,
                    "deleted_at": deleted_at.isoformat() if deleted_at is not None else None,  # type: ignore[union-attr]
                }
                
                if dry_run:
                    logger.info(f"[DRY RUN] Would purge: {sku} ({slug})")
                    stats["purged"].append(item_info)
                    continue
                
                # Determine file location based on previous status
                try:
                    from flask import current_app
                    cfg = current_app.config
                    if prev_status == "processed":  # type: ignore[comparison-overlap]
                        slug_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
                    elif prev_status == "locked":  # type: ignore[comparison-overlap]
                        slug_dir = Path(cfg["LAB_LOCKED_DIR"]) / slug
                    else:
                        slug_dir = Path(cfg["LAB_UNPROCESSED_DIR"]) / slug
                    
                    # Delete files
                    if slug_dir.exists() and slug_dir.is_dir():
                        shutil.rmtree(str(slug_dir))  # type: ignore[arg-type]
                        logger.info(f"Deleted files: {slug_dir}")
                except Exception as e:
                    # If we can't get Flask config, try to find the directory
                    logger.warning(f"Could not delete files for {sku}: {e}")
                    stats["errors"].append({"sku": sku, "error": f"File deletion failed: {e}"})
                
                # Remove from database
                session.delete(artwork)
                logger.info(f"Purged from DB: {sku} ({slug})")
                stats["purged"].append(item_info)
            
            if not dry_run:
                session.commit()
            
            stats["total_purged"] = len(stats["purged"])
            
    except Exception as e:
        logger.error(f"Purge failed: {e}")
        stats["errors"].append({"error": str(e)})
    
    return stats


def run_purge_on_startup(app):
    """
    Run the purge task on application startup.
    Call this from your Flask app factory.
    """
    with app.app_context():
        logger.info("Running startup trash purge...")
        stats = purge_old_trash(days=14, dry_run=False)
        if stats["total_purged"] > 0:
            logger.info(f"Purged {stats['total_purged']} old trash items on startup")
        return stats


if __name__ == "__main__":
    import argparse
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    parser = argparse.ArgumentParser(description="Purge old trash items")
    parser.add_argument("--days", type=int, default=14, help="Days threshold (default: 14)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without deleting")
    args = parser.parse_args()
    
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Purging items deleted more than {args.days} days ago...")
    
    stats = purge_old_trash(days=args.days, dry_run=args.dry_run)
    
    print(f"\nPurge Results:")
    print(f"  Cutoff date: {stats['cutoff_date']}")
    print(f"  Items purged: {stats['total_purged']}")
    
    if stats["purged"]:
        print("\n  Purged items:")
        for item in stats["purged"]:
            print(f"    - {item['sku']} ({item['slug']}) - was {item['previous_status']}")
    
    if stats["errors"]:
        print("\n  Errors:")
        for err in stats["errors"]:
            print(f"    - {err}")
