"""Image regeneration service for reprocessing artwork derivatives.

Handles regenerating THUMB, ANALYSE, CLOSEUP-PROXY, and SEO-named copies
of artwork images after processing.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from application.common.utilities import images
from application.upload.services import storage_service, thumb_service, qc_service
from application.artwork.services.detail_closeup_service import DetailCloseupService

logger = logging.getLogger(__name__)


class ImageRegenerationService:
    """Regenerate artwork image derivatives (THUMB, ANALYSE, CLOSEUP-PROXY, SEO copy)."""

    def __init__(self, processed_root: Path):
        self.processed_root = Path(processed_root)

    def regenerate_all(self, slug: str) -> dict[str, Any]:
        """Regenerate all image derivatives for artwork and update assets.json.

        Returns dict with status of each regenerated file:
        {
            "thumb": {"success": bool, "path": str or None, "error": str or None},
            "analyse": {...},
            "analyse_qc": {...},
            "closeup_proxy": {...},
            "seo_copy": {...},
            "assets_updated": {...},
        }
        """
        artwork_dir = self.processed_root / slug
        if not artwork_dir.exists():
            raise ValueError(f"Artwork directory not found: {artwork_dir}")

        # Load MASTER image as source for all derivatives
        master_path = self._find_master_or_large_original(artwork_dir, slug)
        if not master_path or not master_path.exists():
            raise ValueError(f"MASTER image not found for {slug}")

        master_bytes = master_path.read_bytes()
        results = {}

        # Always use config constants for resolutions
        from flask import current_app
        cfg = current_app.config

        # 1. Regenerate THUMB (500px long edge)
        results["thumb"] = self._regenerate_thumb(artwork_dir, slug, master_bytes, cfg)

        # 2. Regenerate ANALYSE (2400px long edge)
        results["analyse"] = self._regenerate_analyse(artwork_dir, slug, master_bytes, cfg)

        # 3. Regenerate QC for ANALYSE image
        results["analyse_qc"] = self._regenerate_qc(artwork_dir, slug, master_bytes, cfg)

        # 4. Regenerate CLOSEUP-PROXY (7200px long edge)
        results["closeup_proxy"] = self._regenerate_closeup_proxy(artwork_dir, slug)

        # 5. Create SEO-named copy of MASTER (exact copy, no resize)
        results["seo_copy"] = self._create_seo_copy(artwork_dir, slug, master_path)

        # 6. Update assets.json with all new file references
        results["assets_updated"] = self._update_assets_json(artwork_dir, slug, results)

        # 7. Update related status/metadata files
        results["status_files_updated"] = self._update_status_files(artwork_dir, slug, results)

        return results

    def _find_master_or_large_original(self, artwork_dir: Path, slug: str) -> Path | None:
        """Find MASTER or largest image file."""
        # Try direct MASTER first
        master_direct = artwork_dir / f"{slug}-MASTER.jpg"
        if master_direct.exists():
            return master_direct

        # Try assets.json for master reference
        assets_path = artwork_dir / f"{slug.lower()}-assets.json"
        if not assets_path.exists():
            assets_path = artwork_dir / "assets.json"

        if assets_path.exists():
            try:
                assets_doc = json.loads(assets_path.read_text(encoding="utf-8"))
                files = assets_doc.get("files") or {}
                if files.get("master"):
                    master_ref = artwork_dir / files["master"]
                    if master_ref.exists():
                        return master_ref
            except Exception:
                pass

        # Fall back to finding largest JPG file
        largest = None
        max_size = 0
        for jpg_path in sorted(artwork_dir.glob("**/*.jpg")):
            if jpg_path.is_file() and jpg_path.stat().st_size > max_size:
                largest = jpg_path
                max_size = jpg_path.stat().st_size

        return largest

    def _regenerate_thumb(
        self, artwork_dir: Path, slug: str, master_bytes: bytes, cfg: Any
    ) -> dict[str, Any]:
        """Regenerate THUMB image (500px long edge)."""
        try:
            thumb_bytes = thumb_service.create_thumb(master_bytes, cfg["THUMB_SIZE"])
            thumb_path = storage_service.store_thumb(artwork_dir, thumb_bytes, slug=slug)
            return {"success": True, "path": str(thumb_path), "filename": thumb_path.name, "error": None}
        except Exception as exc:
            error_msg = f"THUMB regeneration failed: {str(exc)}"
            logger.error(error_msg)
            return {"success": False, "path": None, "error": error_msg}

    def _regenerate_analyse(
        self, artwork_dir: Path, slug: str, master_bytes: bytes, cfg: Any
    ) -> dict[str, Any]:
        """Regenerate ANALYSE image (2400px long edge)."""
        try:
            analyse_bytes = images.generate_analyse_image(
                master_bytes, target_long_edge=cfg["ANALYSE_LONG_EDGE"]
            )
            analyse_path = storage_service.store_analyse(artwork_dir, slug, analyse_bytes)
            return {"success": True, "path": str(analyse_path), "filename": analyse_path.name, "error": None}
        except Exception as exc:
            error_msg = f"ANALYSE regeneration failed: {str(exc)}"
            logger.error(error_msg)
            return {"success": False, "path": None, "error": error_msg}

    def _regenerate_closeup_proxy(self, artwork_dir: Path, slug: str) -> dict[str, Any]:
        """Regenerate CLOSEUP-PROXY image (7200px long edge)."""
        try:
            # DetailCloseupService expects processed_root, not individual artwork dir
            proxy_svc = DetailCloseupService(processed_root=artwork_dir.parent)
            success = proxy_svc.generate_proxy_preview(slug)
            if success:
                proxy_path = artwork_dir / f"{slug}-CLOSEUP-PROXY.jpg"
                return {"success": True, "path": str(proxy_path), "filename": proxy_path.name, "error": None}
            else:
                error_msg = "CLOSEUP-PROXY generation returned False"
                logger.warning(error_msg)
                return {"success": False, "path": None, "error": error_msg}
        except Exception as exc:
            error_msg = f"CLOSEUP-PROXY regeneration failed: {str(exc)}"
            logger.error(error_msg)
            return {"success": False, "path": None, "error": error_msg}

    def _regenerate_qc(self, artwork_dir: Path, slug: str, master_bytes: bytes, cfg: Any) -> dict[str, Any]:
        """Regenerate QC analysis for ANALYSE image and store in both metadata and qc.json."""
        try:
            # First regenerate ANALYSE to get fresh analyse_bytes
            analyse_bytes = images.generate_analyse_image(
                master_bytes, target_long_edge=cfg["ANALYSE_LONG_EDGE"]
            )
            analyse_qc = qc_service.QCService.analyse_qc(analyse_bytes)
            
            # Store updated QC in metadata
            sku = slug.upper()  # Try to get from metadata first
            metadata_path = artwork_dir / f"{slug.lower()}-metadata.json"
            if not metadata_path.exists():
                metadata_path = artwork_dir / "metadata.json"
            
            if metadata_path.exists():
                try:
                    meta_doc = json.loads(metadata_path.read_text(encoding="utf-8"))
                    sku = meta_doc.get("sku") or meta_doc.get("artwork_id") or sku
                    meta_doc["analyse_qc"] = analyse_qc
                    storage_service.store_meta(artwork_dir, meta_doc, sku=sku)
                except Exception as e:
                    logger.warning(f"Failed to update metadata with new QC: {e}")
            
            # Also store QC in standalone qc.json file
            try:
                qc_path = artwork_dir / f"{sku.lower()}-qc.json"
                if not qc_path.exists():
                    qc_path = artwork_dir / "qc.json"
                qc_path.write_text(json.dumps(analyse_qc, indent=2), encoding="utf-8")
            except Exception as e:
                logger.warning(f"Failed to write standalone qc.json: {e}")
            
            return {"success": True, "path": None, "error": None, "data": analyse_qc}
        except Exception as exc:
            error_msg = f"QC regeneration failed: {str(exc)}"
            logger.error(error_msg)
            return {"success": False, "path": None, "error": error_msg}

    def _create_seo_copy(self, artwork_dir: Path, slug: str, master_path: Path) -> dict[str, Any]:
        """Create SEO-named copy of MASTER image (exact copy)."""
        try:
            # Load metadata to get the SEO filename
            metadata_path = artwork_dir / f"{slug.lower()}-metadata.json"
            if not metadata_path.exists():
                metadata_path = artwork_dir / "metadata.json"

            seo_filename = None
            if metadata_path.exists():
                try:
                    meta_doc = json.loads(metadata_path.read_text(encoding="utf-8"))
                    seo_filename = meta_doc.get("seo_filename")
                except Exception:
                    pass

            # Fall back to listing.json
            if not seo_filename:
                listing_path = artwork_dir / f"{slug.lower()}-listing.json"
                if not listing_path.exists():
                    listing_path = artwork_dir / "listing.json"
                if listing_path.exists():
                    try:
                        listing_doc = json.loads(listing_path.read_text(encoding="utf-8"))
                        seo_filename = listing_doc.get("seo_filename")
                    except Exception:
                        pass

            if not seo_filename:
                return {"success": False, "path": None, "error": "SEO filename not found in metadata/listing"}

            # Create exact copy with SEO name
            seo_path = artwork_dir / seo_filename
            seo_path.write_bytes(master_path.read_bytes())

            return {"success": True, "path": str(seo_path), "filename": seo_filename, "error": None}
        except Exception as exc:
            error_msg = f"SEO copy creation failed: {str(exc)}"
            logger.error(error_msg)
            return {"success": False, "path": None, "error": error_msg}

    def _update_assets_json(self, artwork_dir: Path, slug: str, results: dict[str, Any]) -> dict[str, Any]:
        """Update assets.json with new file references, then write atomically."""
        try:
            # Find and load assets.json
            assets_path = artwork_dir / f"{slug.lower()}-assets.json"
            if not assets_path.exists():
                assets_path = artwork_dir / "assets.json"
            
            if not assets_path.exists():
                return {"success": False, "error": "assets.json not found"}
            
            assets_doc = json.loads(assets_path.read_text(encoding="utf-8"))
            files = assets_doc.get("files") or {}
            
            # Update file references with regenerated images
            if results.get("thumb", {}).get("success"):
                thumb_filename = f"{slug}-THUMB.jpg"
                files["thumb"] = thumb_filename
            
            if results.get("analyse", {}).get("success"):
                analyse_filename = f"{slug}-ANALYSE.jpg"
                files["analyse"] = analyse_filename
            
            if results.get("closeup_proxy", {}).get("success"):
                closeup_filename = f"{slug}-CLOSEUP-PROXY.jpg"
                files["closeup_proxy"] = closeup_filename
            
            # Add SEO-named copy if successful
            if results.get("seo_copy", {}).get("success"):
                seo_filename = results["seo_copy"].get("filename")
                if seo_filename:
                    files["seo_download"] = seo_filename
            
            # Ensure metadata and qc references are present
            sku = slug.upper()
            metadata_path = artwork_dir / f"{slug.lower()}-metadata.json"
            if not metadata_path.exists():
                metadata_path = artwork_dir / "metadata.json"
            if metadata_path.exists():
                try:
                    meta_doc = json.loads(metadata_path.read_text(encoding="utf-8"))
                    sku = meta_doc.get("sku") or sku
                except Exception:
                    pass
            
            files["metadata"] = f"{sku.lower()}-metadata.json"
            files["qc"] = f"{sku.lower()}-qc.json"
            
            # Update timestamp
            assets_doc["files"] = files
            assets_doc["updated_at"] = datetime.now(timezone.utc).isoformat()
            
            # Write atomically
            temp_path = assets_path.with_suffix(".tmp")
            temp_path.write_text(json.dumps(assets_doc, indent=2), encoding="utf-8")
            temp_path.replace(assets_path)
            
            return {"success": True, "path": str(assets_path), "error": None}
        except Exception as exc:
            error_msg = f"assets.json update failed: {str(exc)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def _update_status_files(self, artwork_dir: Path, slug: str, results: dict[str, Any]) -> dict[str, Any]:
        """Update status tracking files with regeneration timestamp."""
        now_iso = datetime.now(timezone.utc).isoformat()
        updates = {}
        
        # Update rjc-XXXX-listing.json
        listing_path = artwork_dir / f"{slug.lower()}-listing.json"
        if not listing_path.exists():
            listing_path = artwork_dir / "listing.json"
        if listing_path.exists():
            try:
                listing_doc = json.loads(listing_path.read_text(encoding="utf-8"))
                if "analysis_status" not in listing_doc:
                    listing_doc["analysis_status"] = {}
                listing_doc["analysis_status"]["images_regenerated_at"] = now_iso
                listing_path.write_text(json.dumps(listing_doc, indent=2), encoding="utf-8")
                updates["listing"] = {"success": True, "path": str(listing_path)}
            except Exception as e:
                logger.warning(f"Failed to update listing.json: {e}")
                updates["listing"] = {"success": False, "error": str(e)}
        else:
            updates["listing"] = {"success": False, "error": "File not found"}
        
        # Update rjc-XXXX-status.json
        status_path = artwork_dir / f"{slug.lower()}-status.json"
        if not status_path.exists():
            status_path = artwork_dir / "status.json"
        if status_path.exists():
            try:
                status_doc = json.loads(status_path.read_text(encoding="utf-8"))
                status_doc["images_regenerated_at"] = now_iso
                status_doc["updated_at"] = now_iso
                status_path.write_text(json.dumps(status_doc, indent=2), encoding="utf-8")
                updates["status"] = {"success": True, "path": str(status_path)}
            except Exception as e:
                logger.warning(f"Failed to update status.json: {e}")
                updates["status"] = {"success": False, "error": str(e)}
        else:
            updates["status"] = {"success": False, "error": "File not found"}
        
        return {"success": len([v for v in updates.values() if v.get("success")]) > 0, "updates": updates}
