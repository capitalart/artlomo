"""Admin Export Service for bundling analysis data"""

from __future__ import annotations

import json
import logging
import tarfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AdminExportError(Exception):
    """Raised when admin export fails"""
    pass


class AdminExportService:
    """Service to bundle analysis data, metadata, and images for iteration"""

    def __init__(self, *, processed_root: Path, artworks_index_path: Path):
        self.processed_root = processed_root
        self.artworks_index_path = artworks_index_path

    def read_json_silent(self, path: Path) -> dict[str, Any]:
        """Read JSON file, return empty dict if not found or invalid"""
        if not path.exists():
            return {}
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
            return doc if isinstance(doc, dict) else {}
        except Exception as e:
            logger.warning(f"Failed to read JSON from {path}: {e}")
            return {}

    def _add_file_to_tar(self, tar: tarfile.TarFile, slug: str, file_path: Path) -> bool:
        """Add a file to the tar archive if it exists. Returns True if added."""
        if not file_path.exists():
            return False
        try:
            tar.add(str(file_path), arcname=f"{slug}/{file_path.name}")
            return True
        except Exception as e:
            logger.warning(f"Failed to add {file_path} to archive: {e}")
            return False

    def _add_json_to_tar(self, tar: tarfile.TarFile, slug: str, filename: str, data: dict) -> None:
        """Add a JSON object to the tar archive."""
        json_str = json.dumps(data, indent=2)
        json_bytes = json_str.encode("utf-8")
        tar_info = tarfile.TarInfo(name=f"{slug}/{filename}")
        tar_info.size = len(json_bytes)
        tar.addfile(tar_info, BytesIO(json_bytes))

    def get_artwork_bundle(self, slug: str, provider: str = "openai") -> bytes:
        """
        Create a tar.gz bundle containing all analysis data and assets:
        - metadata_openai/gemini.json (AI analysis response)
        - seed_context.json (seed context for analysis)
        - status.json (analysis status)
        - {slug}-ANALYSE.jpg (ANALYSE version of image)
        - {slug}-assets.json (assets metadata)
        - qc.json (quality control data)
        - processing_status.json (processing status)
        - metadata.json (artwork metadata)
        - listing.json (listing information)
        - analysis_prompts.json (all prompts sent to AI)
        
        Returns the tar.gz as bytes
        """
        provider_lower = provider.lower()
        if provider_lower not in ["openai", "gemini"]:
            raise AdminExportError(f"Invalid provider: {provider}")

        artwork_dir = self.processed_root / slug
        if not artwork_dir.exists():
            raise AdminExportError(f"Artwork not found: {slug}")

        # Create tar.gz in memory
        tar_buffer = BytesIO()
        with tarfile.open(mode="w:gz", fileobj=tar_buffer) as tar:
            # 1. Add all specified JSON files
            # Extract SKU from metadata to construct proper filenames
            sku = slug
            meta_file = artwork_dir / f"{slug.lower()}-metadata.json"
            if not meta_file.exists():
                meta_file = artwork_dir / "metadata.json"
            if meta_file.exists():
                try:
                    meta_doc = self.read_json_silent(meta_file)
                    if isinstance(meta_doc, dict):
                        sku = str(meta_doc.get("sku") or meta_doc.get("artwork_id") or sku).strip() or sku
                except Exception:
                    pass
            
            files_to_add = [
                "seed_context.json",
                f"{sku.lower()}-status.json",
                f"{sku.lower()}-metadata_{provider_lower}.json",  # The analysis response
                f"{sku.lower()}-assets.json",
                f"{sku.lower()}-qc.json",
                f"{sku.lower()}-processing_status.json",
                f"{sku.lower()}-metadata.json",
                f"{sku.lower()}-listing.json",
            ]
            # Add fallback non-prefixed versions for backward compatibility
            fallback_files = [
                "status.json",
                f"metadata_{provider_lower}.json",
                f"{slug}-assets.json",
                "qc.json",
                "processing_status.json",
                "metadata.json",
                "listing.json",
            ]
            
            # Try SKU-prefixed first, then fall back to non-prefixed
            for filename in files_to_add:
                file_path = artwork_dir / filename
                if file_path.exists():
                    self._add_file_to_tar(tar, slug, file_path)
                else:
                    # Try fallback (non-prefixed) version
                    idx = files_to_add.index(filename)
                    if idx < len(fallback_files):
                        fallback_path = artwork_dir / fallback_files[idx]
                        if fallback_path.exists():
                            self._add_file_to_tar(tar, slug, fallback_path)
                        else:
                            logger.debug(f"File not found: {filename} or {fallback_files[idx]} in {slug}")

            # 2. Add ANALYSE image
            analyse_image = None
            for pattern in [f"{slug}-ANALYSE.jpg", f"{slug}-ANALYSE.jpeg", f"{slug}-ANALYSE.png"]:
                candidate = artwork_dir / pattern
                if candidate.exists():
                    analyse_image = candidate
                    break
            
            if analyse_image:
                self._add_file_to_tar(tar, slug, analyse_image)
            else:
                logger.warning(f"No ANALYSE image found for {slug}")

            # 3. Create analysis_prompts.json containing all prompts sent to AI
            # This includes system prompt, user prompts, and context
            prompts_data = self._collect_analysis_prompts(artwork_dir, provider_lower)
            if prompts_data:
                self._add_json_to_tar(tar, slug, "analysis_prompts.json", prompts_data)

            # 4. Add export metadata
            export_metadata = {
                "slug": slug,
                "provider": provider_lower,
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "bundle_contents": [
                    "metadata_{provider}.json - AI analysis response",
                    "seed_context.json - Context provided for analysis",
                    "status.json - Status information",
                    "{slug}-ANALYSE.jpg - ANALYSE version of artwork",
                    "{slug}-assets.json - Assets metadata",
                    "qc.json - Quality control data",
                    "processing_status.json - Processing status",
                    "metadata.json - Artwork metadata",
                    "listing.json - Listing information",
                    "analysis_prompts.json - All prompts sent to AI",
                ],
            }
            self._add_json_to_tar(tar, slug, "EXPORT_INFO.json", export_metadata)

        tar_buffer.seek(0)
        return tar_buffer.getvalue()

    def _collect_analysis_prompts(self, artwork_dir: Path, provider: str) -> dict[str, Any]:
        """Collect all prompts and context sent to AI for analysis"""
        prompts = {
            "provider": provider,
            "collected_at": datetime.now(timezone.utc).isoformat(),
        }
        
        # Try to extract prompts from metadata if available
        metadata_file = artwork_dir / f"metadata_{provider}.json"
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
                if isinstance(metadata, dict):
                    # Store the prompt_id if available
                    prompts["prompt_id"] = metadata.get("prompt_id", "")
                    prompts["model"] = metadata.get("model", "")
                    prompts["temperature"] = metadata.get("temperature", "")
                    prompts["source"] = metadata.get("source", "")
                    
                    # Store analysis input metadata
                    prompts["image_metadata"] = metadata.get("image", {})
                    
                    # Analysis analysis result
                    prompts["analysis_result"] = metadata.get("analysis", {})
            except Exception as e:
                logger.warning(f"Failed to extract prompts from metadata: {e}")
        
        # Try to get seed context
        seed_file = artwork_dir / "seed_context.json"
        if seed_file.exists():
            try:
                seed = json.loads(seed_file.read_text(encoding="utf-8"))
                prompts["seed_context"] = seed
            except Exception:
                pass
        
        # Try to get status/context
        status_file = artwork_dir / "status.json"
        if status_file.exists():
            try:
                status = json.loads(status_file.read_text(encoding="utf-8"))
                prompts["processing_context"] = status
            except Exception:
                pass
        
        return prompts if len(prompts) > 2 else {}

    def get_bundle_filename(self, slug: str, provider: str = "openai") -> str:
        """Generate a filename for the export bundle in format: Provider-Analysis-SLUG-DATE-TIME.tar.gz"""
        now = datetime.now(timezone.utc)
        
        # Format: "OpenAi-Analysis-RJC-0214-05-Jan-2026-10-03am.tar.gz"
        date_str = now.strftime("%d-%b-%Y").upper()  # "05-JAN-2026"
        time_str = now.strftime("%I-%M%p").lower()  # "10-03am"
        
        provider_display = provider.capitalize()  # "Openai" or "Gemini"
        
        return f"{provider_display}-Analysis-{slug.upper()}-{date_str}-{time_str}.tar.gz"
