"""Analysis Preset Service

Manages loading, saving, and assembling analysis presets.
Supports both database and JSON file storage with automatic fallback.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from sqlalchemy.orm import Session

from db import AnalysisPreset, SessionLocal
from application.utils.house_prompts import (
    SYSTEM,
    USER_FULL,
    USER_SECTION,
    LISTING_BOILERPLATE,
    ANALYSIS_PROMPT,
)

logger = logging.getLogger(__name__)


class AnalysisPresetService:
    """Service for managing analysis presets."""

    PRESETS_DIR = Path(__file__).parent.parent.parent / "var" / "analysis_presets"

    @classmethod
    def _ensure_presets_dir(cls) -> Path:
        """Ensure presets directory exists."""
        cls.PRESETS_DIR.mkdir(parents=True, exist_ok=True)
        return cls.PRESETS_DIR

    @classmethod
    def _get_db_session(cls) -> Session:
        """Get a database session."""
        return SessionLocal()

    @classmethod
    def initialize_defaults(cls, force: bool = False) -> None:
        """Initialize default presets in database if they don't exist.
        
        Args:
            force: If True, recreate defaults even if they exist
        """
        session = cls._get_db_session()
        try:
            # Check if defaults already exist
            existing = session.query(AnalysisPreset).filter(
                AnalysisPreset.is_default == True
            ).first()
            
            if existing and not force:
                logger.info("Default presets already exist in database")
                return
            
            # If force and exists, delete the old one
            if force and existing:
                session.delete(existing)
                session.commit()
            
            # Create default presets for OpenAI and Gemini
            for provider in ["openai", "gemini"]:
                preset = AnalysisPreset(
                    name=f"Default {provider.title()} Preset",
                    provider=provider,
                    is_default=True,
                    system_prompt=SYSTEM,
                    user_full_prompt=USER_FULL,
                    user_section_prompt=USER_SECTION,
                    listing_boilerplate=LISTING_BOILERPLATE,
                    analysis_prompt=ANALYSIS_PROMPT,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                session.add(preset)
            
            session.commit()
            logger.info("Initialized default presets in database")
        except Exception as e:
            logger.exception("Failed to initialize default presets: %s", e)
            session.rollback()
        finally:
            session.close()

    @classmethod
    def get_default_preset(cls, provider: str) -> Optional[AnalysisPreset]:
        """Get the default preset for a provider.
        
        Args:
            provider: 'openai' or 'gemini'
            
        Returns:
            AnalysisPreset or None
        """
        session = cls._get_db_session()
        try:
            preset = session.query(AnalysisPreset).filter(
                AnalysisPreset.provider == provider.lower(),
                AnalysisPreset.is_default == True,
            ).first()
            
            if not preset:
                logger.warning("No default preset found for provider: %s", provider)
                return None
            
            # Detach from session
            session.expunge(preset)
            return preset
        except Exception as e:
            logger.exception("Failed to get default preset for %s: %s", provider, e)
            return None
        finally:
            session.close()

    @classmethod
    def get_preset_by_name(cls, name: str, provider: str) -> Optional[AnalysisPreset]:
        """Get a preset by name for a specific provider.
        
        Args:
            name: Preset name
            provider: 'openai' or 'gemini'
            
        Returns:
            AnalysisPreset or None
        """
        session = cls._get_db_session()
        try:
            preset = session.query(AnalysisPreset).filter(
                AnalysisPreset.name == name,
                AnalysisPreset.provider == provider.lower(),
            ).first()
            
            if not preset:
                logger.warning("Preset not found: name=%s, provider=%s", name, provider)
                return None
            
            session.expunge(preset)
            return preset
        except Exception as e:
            logger.exception("Failed to get preset %s: %s", name, e)
            return None
        finally:
            session.close()

    @classmethod
    def list_presets(cls, provider: Optional[str] = None) -> list[AnalysisPreset]:
        """List all presets, optionally filtered by provider.
        
        Args:
            provider: Optional 'openai' or 'gemini' filter
            
        Returns:
            List of AnalysisPreset objects
        """
        session = cls._get_db_session()
        try:
            query = session.query(AnalysisPreset)
            
            if provider:
                query = query.filter(AnalysisPreset.provider == provider.lower())
            
            presets = query.order_by(
                AnalysisPreset.is_default.desc(),
                AnalysisPreset.name.asc()
            ).all()
            
            for preset in presets:
                session.expunge(preset)
            
            return presets
        except Exception as e:
            logger.exception("Failed to list presets: %s", e)
            return []
        finally:
            session.close()

    @classmethod
    def save_preset(
        cls,
        name: str,
        provider: str,
        system_prompt: str,
        user_full_prompt: str,
        user_section_prompt: str,
        listing_boilerplate: str,
        analysis_prompt: str,
        is_default: bool = False,
        preset_id: Optional[int] = None,
    ) -> Optional[AnalysisPreset]:
        """Save or update a preset.
        
        Args:
            name: Preset name
            provider: 'openai' or 'gemini'
            system_prompt: System prompt text
            user_full_prompt: Full user prompt text
            user_section_prompt: Section-by-section prompt text
            listing_boilerplate: Listing boilerplate text
            analysis_prompt: Analysis/metadata extraction prompt
            is_default: Whether this should be the default
            preset_id: If provided, update existing; else create new
            
        Returns:
            Saved AnalysisPreset or None on error
        """
        session = cls._get_db_session()
        try:
            if preset_id:
                # Update existing
                preset = session.query(AnalysisPreset).filter(
                    AnalysisPreset.id == preset_id
                ).first()
                
                if not preset:
                    logger.warning("Preset not found for update: id=%s", preset_id)
                    return None
                
                # If setting as default, unset others for this provider
                if is_default:
                    session.query(AnalysisPreset).filter(
                        AnalysisPreset.provider == provider.lower(),
                        AnalysisPreset.id != preset_id,
                    ).update({"is_default": False})
                
                preset.name = name  # type: ignore[misc]
                preset.provider = provider.lower()  # type: ignore[misc]
                preset.system_prompt = system_prompt  # type: ignore[misc]
                preset.user_full_prompt = user_full_prompt  # type: ignore[misc]
                preset.user_section_prompt = user_section_prompt  # type: ignore[misc]
                preset.listing_boilerplate = listing_boilerplate  # type: ignore[misc]
                preset.analysis_prompt = analysis_prompt  # type: ignore[misc]
                preset.is_default = is_default  # type: ignore[misc]
                preset.updated_at = datetime.now(timezone.utc)  # type: ignore[misc]
            else:
                # Create new
                # If setting as default, unset others for this provider
                if is_default:
                    session.query(AnalysisPreset).filter(
                        AnalysisPreset.provider == provider.lower()
                    ).update({"is_default": False})
                
                preset = AnalysisPreset(
                    name=name,
                    provider=provider.lower(),
                    system_prompt=system_prompt,
                    user_full_prompt=user_full_prompt,
                    user_section_prompt=user_section_prompt,
                    listing_boilerplate=listing_boilerplate,
                    analysis_prompt=analysis_prompt,
                    is_default=is_default,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                session.add(preset)
            
            session.commit()
            preset_id_result: int | None = int(preset.id)  # type: ignore[arg-type]
            session.expunge(preset)
            logger.info("Saved preset: name=%s, provider=%s, id=%s", name, provider, preset_id_result)
            return preset
        except Exception as e:
            logger.exception("Failed to save preset: %s", e)
            session.rollback()
            return None
        finally:
            session.close()

    @classmethod
    def delete_preset(cls, preset_id: int) -> bool:
        """Delete a preset by ID.
        
        Args:
            preset_id: ID of preset to delete
            
        Returns:
            True if deleted, False otherwise
        """
        session = cls._get_db_session()
        try:
            preset = session.query(AnalysisPreset).filter(
                AnalysisPreset.id == preset_id
            ).first()
            
            if not preset:
                logger.warning("Preset not found for deletion: id=%s", preset_id)
                return False
            
            if preset.is_default:  # type: ignore[truthy-bool]
                logger.warning("Cannot delete default preset: id=%s", preset_id)
                return False
            
            session.delete(preset)
            session.commit()
            logger.info("Deleted preset: id=%s, name=%s", preset_id, preset.name)
            return True
        except Exception as e:
            logger.exception("Failed to delete preset: %s", e)
            session.rollback()
            return False
        finally:
            session.close()

    @classmethod
    def assemble_full_prompt(cls, preset: AnalysisPreset) -> str:
        """Assemble a complete prompt from preset sections.
        
        Args:
            preset: AnalysisPreset object
            
        Returns:
            Complete assembled prompt string
        """
        return f"{preset.system_prompt}\n\n{preset.user_full_prompt}"

    @classmethod
    def assemble_section_prompt(cls, preset: AnalysisPreset) -> str:
        """Assemble the section editing prompt from preset.
        
        Args:
            preset: AnalysisPreset object
            
        Returns:
            Complete section prompt string
        """
        return f"{preset.system_prompt}\n\n{preset.user_section_prompt}"

    @classmethod
    def assemble_analysis_prompt(cls, preset: AnalysisPreset) -> str:
        """Assemble the metadata analysis prompt from preset.
        
        Args:
            preset: AnalysisPreset object
            
        Returns:
            Complete analysis prompt string
        """
        return str(preset.analysis_prompt)  # type: ignore[return-value]

    @classmethod
    def to_dict(cls, preset: AnalysisPreset) -> dict[str, Any]:
        """Convert preset to dictionary.
        
        Args:
            preset: AnalysisPreset object
            
        Returns:
            Dictionary representation
        """
        return {
            "id": preset.id,
            "name": preset.name,
            "provider": preset.provider,
            "is_default": preset.is_default,
            "system_prompt": preset.system_prompt,
            "user_full_prompt": preset.user_full_prompt,
            "user_section_prompt": preset.user_section_prompt,
            "listing_boilerplate": preset.listing_boilerplate,
            "analysis_prompt": preset.analysis_prompt,
            "created_at": preset.created_at.isoformat() if (preset.created_at is not None) else None,  # type: ignore[operator]
            "updated_at": preset.updated_at.isoformat() if (preset.updated_at is not None) else None,  # type: ignore[operator]
        }
