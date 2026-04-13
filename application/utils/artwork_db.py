"""
Artwork database operations for hybrid JSON + DB storage.
Provides double-write logic: every artwork change updates both JSON and DB.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from db import SessionLocal, Artwork

logger = logging.getLogger(__name__)


def sync_artwork_to_db(
    *,
    sku: str,
    slug: str,
    title: str | None = None,
    owner_id: str | None = None,
    status: str = "unprocessed",
    analysis_source: str | None = None,
    image_path: str | None = None,
    thumb_path: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> Artwork | None:
    """
    Create or update an artwork record in the database.
    This is the core double-write function.
    """
    try:
        with SessionLocal() as session:
            existing = session.query(Artwork).filter_by(id=sku).first()
            
            if existing:
                existing.slug = slug  # type: ignore[misc]
                if title is not None:
                    existing.title = title  # type: ignore[misc]
                if owner_id is not None:
                    existing.owner_id = owner_id  # type: ignore[misc]
                existing.status = status  # type: ignore[misc]
                if analysis_source is not None:
                    existing.analysis_source = analysis_source  # type: ignore[misc]
                if image_path is not None:
                    existing.image_path = image_path  # type: ignore[misc]
                if thumb_path is not None:
                    existing.thumb_path = thumb_path  # type: ignore[misc]
                if metadata is not None:
                    existing.metadata_json = json.dumps(metadata, ensure_ascii=False)  # type: ignore[misc]
                existing.updated_at = datetime.utcnow()  # type: ignore[misc]
                session.commit()
                logger.info(f"Updated artwork in DB: {sku} ({status})")
                return existing
            else:
                artwork = Artwork(
                    id=sku,
                    slug=slug,
                    title=title or sku,
                    owner_id=owner_id,
                    status=status,
                    analysis_source=analysis_source,
                    image_path=image_path,
                    thumb_path=thumb_path,
                    metadata_json=json.dumps(metadata, ensure_ascii=False) if metadata else None,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(artwork)
                session.commit()
                logger.info(f"Created artwork in DB: {sku} ({status})")
                return artwork
    except Exception as e:
        logger.error(f"Failed to sync artwork to DB: {sku} - {e}")
        return None


def update_artwork_status(sku: str, status: str) -> bool:
    """Update just the status of an artwork (e.g., processed -> locked)."""
    try:
        with SessionLocal() as session:
            artwork = session.query(Artwork).filter_by(id=sku).first()
            if artwork:
                artwork.status = status  # type: ignore[misc]
                artwork.updated_at = datetime.utcnow()  # type: ignore[misc]
                session.commit()
                logger.info(f"Updated artwork status: {sku} -> {status}")
                return True
            return False
    except Exception as e:
        logger.error(f"Failed to update artwork status: {sku} - {e}")
        return False


def delete_artwork_from_db(sku: str) -> bool:
    """Remove an artwork from the database."""
    try:
        with SessionLocal() as session:
            artwork = session.query(Artwork).filter_by(id=sku).first()
            if artwork:
                session.delete(artwork)
                session.commit()
                logger.info(f"Deleted artwork from DB: {sku}")
                return True
            return False
    except Exception as e:
        logger.error(f"Failed to delete artwork from DB: {sku} - {e}")
        return False


def get_artwork_by_sku(sku: str) -> dict[str, Any] | None:
    """Retrieve a single artwork by SKU."""
    try:
        with SessionLocal() as session:
            artwork = session.query(Artwork).filter_by(id=sku).first()
            if artwork:
                return _artwork_to_dict(artwork)
            return None
    except Exception as e:
        logger.error(f"Failed to get artwork: {sku} - {e}")
        return None


def get_artworks_by_owner(owner_id: str, status: str | None = None) -> list[dict[str, Any]]:
    """Get all artworks owned by a specific user."""
    try:
        with SessionLocal() as session:
            query = session.query(Artwork).filter_by(owner_id=owner_id)
            if status:
                query = query.filter_by(status=status)
            artworks = query.order_by(Artwork.updated_at.desc()).all()
            return [_artwork_to_dict(a) for a in artworks]
    except Exception as e:
        logger.error(f"Failed to get artworks for owner: {owner_id} - {e}")
        return []


def get_artworks_by_status(status: str, owner_id: str | None = None) -> list[dict[str, Any]]:
    """
    Get all artworks by status.
    If owner_id is provided, filter to that owner only (for artists).
    If owner_id is None, return all (for admins).
    """
    try:
        with SessionLocal() as session:
            query = session.query(Artwork).filter_by(status=status)
            if owner_id:
                query = query.filter_by(owner_id=owner_id)
            artworks = query.order_by(Artwork.updated_at.desc()).all()
            return [_artwork_to_dict(a) for a in artworks]
    except Exception as e:
        logger.error(f"Failed to get artworks by status: {status} - {e}")
        return []


def get_all_artworks(owner_id: str | None = None) -> list[dict[str, Any]]:
    """
    Get all artworks.
    If owner_id is provided, filter to that owner only.
    """
    try:
        with SessionLocal() as session:
            query = session.query(Artwork)
            if owner_id:
                query = query.filter_by(owner_id=owner_id)
            artworks = query.order_by(Artwork.updated_at.desc()).all()
            return [_artwork_to_dict(a) for a in artworks]
    except Exception as e:
        logger.error(f"Failed to get all artworks - {e}")
        return []


def soft_delete_artwork(sku: str) -> bool:
    """
    Move artwork to trash (soft delete).
    Sets status='deleted', stores previous_status, and sets deleted_at timestamp.
    """
    try:
        with SessionLocal() as session:
            artwork = session.query(Artwork).filter_by(id=sku).first()
            if artwork:
                artwork.previous_status = artwork.status  # type: ignore[misc]
                artwork.status = "deleted"  # type: ignore[misc]
                artwork.deleted_at = datetime.utcnow()  # type: ignore[misc]
                artwork.updated_at = datetime.utcnow()  # type: ignore[misc]
                session.commit()
                logger.info(f"Soft deleted artwork: {sku} (was {artwork.previous_status})")
                return True
            return False
    except Exception as e:
        logger.error(f"Failed to soft delete artwork: {sku} - {e}")
        return False


def soft_delete_artwork_by_slug(slug: str) -> bool:
    """
    Move artwork to trash by slug (soft delete).
    Used as fallback when SKU lookup fails. Deletes artwork identified by slug,
    setting status='deleted', stores previous_status, and sets deleted_at timestamp.
    """
    try:
        with SessionLocal() as session:
            artwork = session.query(Artwork).filter_by(slug=slug).first()
            if artwork:
                artwork.previous_status = artwork.status  # type: ignore[misc]
                artwork.status = "deleted"  # type: ignore[misc]
                artwork.deleted_at = datetime.utcnow()  # type: ignore[misc]
                artwork.updated_at = datetime.utcnow()  # type: ignore[misc]
                session.commit()
                logger.info(f"Soft deleted artwork by slug: {slug} (was {artwork.previous_status}, id={artwork.id})")
                return True
            return False
    except Exception as e:
        logger.error(f"Failed to soft delete artwork by slug: {slug} - {e}")
        return False


def restore_artwork(sku: str) -> bool:
    """
    Restore artwork from trash to its previous status.
    """
    try:
        with SessionLocal() as session:
            artwork = session.query(Artwork).filter_by(id=sku).first()
            if artwork and artwork.status == "deleted":  # type: ignore[comparison-overlap]
                restored_status = artwork.previous_status or "unprocessed"
                artwork.status = restored_status  # type: ignore[misc]
                artwork.previous_status = None  # type: ignore[misc]
                artwork.deleted_at = None  # type: ignore[misc]
                artwork.updated_at = datetime.utcnow()  # type: ignore[misc]
                session.commit()
                logger.info(f"Restored artwork: {sku} -> {restored_status}")
                return True
            return False
    except Exception as e:
        logger.error(f"Failed to restore artwork: {sku} - {e}")
        return False


def get_deleted_artworks(owner_id: str | None = None) -> list[dict[str, Any]]:
    """Get all artworks in trash (status='deleted')."""
    return get_artworks_by_status("deleted", owner_id=owner_id)


def purge_old_deleted_artworks(days: int = 14) -> list[str]:
    """
    Permanently delete artworks that have been in trash for more than `days` days.
    Returns list of purged SKUs.
    """
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)
    purged = []
    
    try:
        with SessionLocal() as session:
            old_deleted = session.query(Artwork).filter(
                Artwork.status == "deleted",
                Artwork.deleted_at < cutoff
            ).all()
            
            for artwork in old_deleted:
                purged.append(artwork.id)
                session.delete(artwork)
                logger.info(f"Purged old deleted artwork: {artwork.id} (deleted_at={artwork.deleted_at})")
            
            session.commit()
    except Exception as e:
        logger.error(f"Failed to purge old deleted artworks: {e}")
    
    return purged


def _artwork_to_dict(artwork: Artwork) -> dict[str, Any]:
    """Convert Artwork ORM object to dictionary."""
    metadata = {}
    if artwork.metadata_json:  # type: ignore[truthy-bool]
        try:
            metadata = json.loads(artwork.metadata_json)  # type: ignore[arg-type]
        except Exception:
            pass
    
    return {
        "id": artwork.id,
        "sku": artwork.id,
        "slug": artwork.slug,
        "title": artwork.title,
        "owner_id": artwork.owner_id,
        "status": artwork.status,
        "previous_status": getattr(artwork, 'previous_status', None),
        "analysis_source": artwork.analysis_source,
        "image_path": artwork.image_path,
        "thumb_path": artwork.thumb_path,
        "metadata": metadata,
        "created_at": artwork.created_at.isoformat() if artwork.created_at else None,  # type: ignore[union-attr]
        "updated_at": artwork.updated_at.isoformat() if artwork.updated_at else None,  # type: ignore[union-attr]
        "deleted_at": artwork.deleted_at.isoformat() if getattr(artwork, 'deleted_at', None) else None,
    }
