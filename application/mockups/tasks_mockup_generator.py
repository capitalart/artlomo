"""Celery orchestration tasks for mockup base generation pipeline.

Stage 4 coordinates the full asynchronous flow:
1. Queue missing mockup generation jobs idempotently.
2. Process individual jobs through prompt generation, Gemini image generation,
   and cyan coordinate extraction.

This module enforces strict SQLAlchemy transaction handling to reduce lock risk
in long-running batch operations.
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from contextlib import contextmanager
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Iterator

from celery import Celery
from celery.exceptions import MaxRetriesExceededError
from PIL import Image, ImageDraw, ImageFilter
from sqlalchemy.exc import SQLAlchemyError

from db import EzyMockupJob, GeminiStudioJob, MockupBaseGenerationJob, SessionLocal
from application.mockups.admin.services import CatalogAdminService
from application.mockups.config import MockupBaseGenerationCatalog
from application.common.utilities.slug_sku import slugify
from application.mockups.services.mockup_prompt_service import MockupPromptService
from application.mockups.services.gemini_service import (
    GeminiAuthenticationError,
    GeminiFileSaveError,
    GeminiGenerationError,
    GeminiImageService,
    GeminiRateLimitError,
)
from application.mockups.services.MockupCoordinateService import (
    CyanQuadNotFoundError,
    InvalidCyanShapeError,
    MockupCoordinateService,
)
from application.mockups.services.CompositeCoordinateService import (
    CompositeCoordinateService,
    CompositeCyanContourNotFoundError,
    CompositeInvalidQuadError,
)
from application.mockups.services.chromakey_bridge_service import (
    ChromakeyBridgeService,
    ChromakeyBridgeError,
    ChromakeyQuadError,
    ChromakeyRegionNotFoundError,
)


logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
APPLICATION_ROOT = PROJECT_ROOT / "application"
CONTROL_STATE_PATH = PROJECT_ROOT / "var" / "state" / "mockup_generator_control.json"
PROMPT_SETTINGS_PATH = PROJECT_ROOT / "var" / "state" / "mockup_generator_prompt_settings.json"
MAX_CYAN_REGEN_ATTEMPTS = 2
MOCKUP_CANVAS_ASPECT_RATIO = "1x1"
MOCKUP_GEMINI_TASK_RATE_LIMIT = os.getenv("MOCKUP_GEMINI_TASK_RATE_LIMIT", "8/m")
MOCKUP_GEMINI_RATE_LIMIT_RETRY_FALLBACK_SECONDS = int(
    os.getenv("MOCKUP_GEMINI_RATE_LIMIT_RETRY_FALLBACK_SECONDS", "30")
)
MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES = int(
    os.getenv("MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES", "6")
)
PROMPT_METADATA_PREFIX = "[[MOCKUP_GUIDE_METADATA]]"
GENERATION_MODE_STANDARD = "standard"
GENERATION_MODE_CHROMAKEY_AUTO = "chromakey_auto"
GENERATION_MODE_ARTWORK_TROJAN = "artwork_trojan"
GENERATION_MODE_ARTWORK_ONLY_COMPOSITE = "artwork_only_composite"
CHROMAKEY_TARGET_HEX = os.getenv("MOCKUP_CHROMAKEY_HEX", "#00FFCC").strip() or "#00FFCC"
STUDIO_CANVAS_ASPECT_RATIO = "1x1"
THOUGHT_SIGNATURE_STATE_PATH = PROJECT_ROOT / "var" / "state" / "mockup_generator_thought_signatures.json"

# Reference-guided editing prompt (used when a reference image is provided to edit_image)
MATTE_REFERENCE_GUIDED_PROMPT_TEMPLATE = (
    "[THINKING_LEVEL: HIGH]\n"
    "Place the provided artwork on a wall in a photorealistic {category_descriptor} interior. "
    "Preserve the artwork's {aspect_ratio_colon} aspect ratio exactly. Output at 1:1 canvas scale."
)

# Pure generation prompt (used when NO reference image is provided, or when edit fails and generates from scratch)
MATTE_PURE_GENERATION_PROMPT_TEMPLATE = (
    "[THINKING_LEVEL: HIGH]\n"
    "Generate a photorealistic {category_descriptor} interior with a wall-mounted artwork placeholder at {aspect_ratio_colon} aspect ratio. "
    "Output at 1:1 canvas scale. Preserve the placeholder's aspect ratio exactly."
)

MATTE_INSERTION_PROMPT_TEMPLATE = MATTE_PURE_GENERATION_PROMPT_TEMPLATE  # Fallback for compatibility
DEFAULT_STANDARD_PREFIX = (
    "You are generating a production mockup base image for ArtLomo.\n"
    "Prioritise photorealism, clean architectural composition, and export-safe image quality.\n"
    "Follow all placeholder and geometry instructions in the base prompt exactly."
)
DEFAULT_STANDARD_SUFFIX = (
    "Output one clean, photorealistic image with the placeholder visible on the wall."
)
DEFAULT_OUTLINED_PREFIX = (
    "You are generating a production mockup base using provided reference artwork.\n"
    "Build a premium interior scene around the artwork."
)
DEFAULT_OUTLINED_SUFFIX = (
    "Output one clean, photorealistic image with the artwork visible on the wall."
)
STYLE_OPTIONS = (
    "Contemporary",
    "Luxury",
    "Minimal",
    "Eccentric",
    "Classical",
    "Realistic lived in",
    "Industrial",
    "Scandinavian",
    "Bohemian",
    "Japandi",
    "Rustic",
    "Coastal",
)
TONE_OPTIONS = (
    "Warm",
    "Cool",
    "Cold",
    "Colourful",
    "Neutral",
    "Moody",
    "Earthy",
)
SEASON_OPTIONS = (
    "Summer",
    "Winter",
    "Autumn",
    "Spring",
    "Any",
)
TROJAN_ARTWORK_DIR = Path(
    APPLICATION_ROOT / "mockups" / "catalog" / "assets" / "mockups" / "reference-guides" / "outlined-artworks"
)
ARTWORK_ONLY_GUIDE_DIR = Path(
    APPLICATION_ROOT / "mockups" / "catalog" / "assets" / "mockups" / "reference-guides" / "artwork-only"
)
LEGACY_TROJAN_ARTWORK_DIR = Path(
    APPLICATION_ROOT / "mockups" / "catalog" / "assets" / "mockups" / "reference-guides" / "trojan-artworks"
)
GEMINI_STUDIO_ROOT = PROJECT_ROOT / "var" / "studio"
GEMINI_STUDIO_OUTPUT_DIR = GEMINI_STUDIO_ROOT / "outputs"
STUDIO_OUTPUT_TARGET_PX = int(os.getenv("MOCKUP_STUDIO_OUTPUT_TARGET_PX", "2048"))
EZY_MOCKUP_ROOT = GEMINI_STUDIO_ROOT / "ezy"
EZY_ROOM_OUTPUT_DIR = EZY_MOCKUP_ROOT / "rooms"
EZY_MASK_OUTPUT_DIR = EZY_MOCKUP_ROOT / "masks"
EZY_TRANSPARENT_OUTPUT_DIR = EZY_MOCKUP_ROOT / "transparent"
EZY_ARTIST_MODEL = os.getenv("EZY_ARTIST_MODEL", "gemini-2.0-ultra-001")
EZY_VERIFIER_MODEL = os.getenv("EZY_VERIFIER_MODEL", "gemini-2.5-pro")
EZY_ENABLE_HARMONIZE = os.getenv("EZY_ENABLE_HARMONIZE", "false").strip().lower() in {"1", "true", "yes", "on"}
EZY_MAX_SCENE_ATTEMPTS = int(os.getenv("EZY_MAX_SCENE_ATTEMPTS", "3"))
EZY_COMPOSITION_VARIANTS = (
    "Place the frame on the right third with furniture depth on the left.",
    "Place the frame on the left third with negative space and natural light from the opposite side.",
    "Use a three-quarter camera angle with the frame slightly above center and room depth visible.",
    "Use a staged corner vignette composition with the frame offset from center and strong environmental storytelling.",
)

DEFAULT_PROMPT_SETTINGS: dict[str, Any] = {
    "standard_prefix": DEFAULT_STANDARD_PREFIX,
    "standard_suffix": DEFAULT_STANDARD_SUFFIX,
    "outlined_prefix": DEFAULT_OUTLINED_PREFIX,
    "outlined_suffix": DEFAULT_OUTLINED_SUFFIX,
    "generation_canvas_aspect_ratio": MOCKUP_CANVAS_ASPECT_RATIO,
    "default_style": "Contemporary",
    "default_tone": "Warm",
    "default_season": "Any",
}


def _parse_aspect_ratio(aspect_ratio: str) -> tuple[float, float]:
    raw = str(aspect_ratio or "").strip().lower()
    if "x" not in raw:
        return (1.0, 1.0)
    left, right = raw.split("x", 1)
    try:
        w = float(left)
        h = float(right)
        if w <= 0 or h <= 0:
            return (1.0, 1.0)
        return (w, h)
    except Exception:
        return (1.0, 1.0)


def _load_thought_signature_state() -> dict[str, str]:
    if not THOUGHT_SIGNATURE_STATE_PATH.exists():
        return {}

    try:
        payload = json.loads(THOUGHT_SIGNATURE_STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}

    if not isinstance(payload, dict):
        return {}

    cleaned: dict[str, str] = {}
    for key, value in payload.items():
        if not isinstance(key, str):
            continue
        if isinstance(value, str) and value.strip():
            cleaned[key] = value.strip()
    return cleaned


def _save_thought_signature_state(state: dict[str, str]) -> None:
    THOUGHT_SIGNATURE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    THOUGHT_SIGNATURE_STATE_PATH.write_text(
        json.dumps(state, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _get_thought_signature(batch_key: str) -> str:
    state = _load_thought_signature_state()
    return str(state.get(batch_key) or "").strip()


def _set_thought_signature(batch_key: str, thought_signature: str) -> None:
    cleaned = str(thought_signature or "").strip()
    if not cleaned:
        return

    state = _load_thought_signature_state()
    if state.get(batch_key) == cleaned:
        return
    state[batch_key] = cleaned
    _save_thought_signature_state(state)


def _build_fallback_coordinates(image_path: str, aspect_ratio: str) -> list[dict[str, int]]:
    """Create a centered fallback quad when fiducial extraction is intentionally bypassed."""
    with Image.open(image_path) as image_obj:
        width, height = image_obj.size

    target_w, target_h = _parse_aspect_ratio(aspect_ratio)
    target_ratio = target_w / target_h if target_h > 0 else 1.0

    # Keep fallback frame comfortably inside scene boundaries.
    safe_w = float(width) * 0.62
    safe_h = float(height) * 0.58
    safe_ratio = safe_w / safe_h if safe_h > 0 else target_ratio

    if safe_ratio > target_ratio:
        frame_h = safe_h
        frame_w = frame_h * target_ratio
    else:
        frame_w = safe_w
        frame_h = frame_w / target_ratio

    cx = float(width) * 0.50
    cy = float(height) * 0.45
    half_w = frame_w * 0.5
    half_h = frame_h * 0.5

    left = max(0, int(round(cx - half_w)))
    right = min(width - 1, int(round(cx + half_w)))
    top = max(0, int(round(cy - half_h)))
    bottom = min(height - 1, int(round(cy + half_h)))

    if right <= left:
        right = min(width - 1, left + max(8, width // 10))
    if bottom <= top:
        bottom = min(height - 1, top + max(8, height // 10))

    return [
        {"x": left, "y": top},
        {"x": right, "y": top},
        {"x": right, "y": bottom},
        {"x": left, "y": bottom},
    ]


def _is_coordinate_fallback_enabled(control_state: dict[str, Any]) -> bool:
    raw = str(control_state.get("skip_coordinate_detection") or "").strip().lower()
    return raw in {"1", "true", "yes", "on"}


def _normalize_prompt_settings(payload: dict[str, Any] | None) -> dict[str, Any]:
    merged = dict(DEFAULT_PROMPT_SETTINGS)
    if isinstance(payload, dict):
        merged.update(payload)

    for key in ("standard_prefix", "standard_suffix", "outlined_prefix", "outlined_suffix"):
        value = str(merged.get(key) or "").strip()
        merged[key] = value if value else str(DEFAULT_PROMPT_SETTINGS[key])

    canvas_aspect = str(merged.get("generation_canvas_aspect_ratio") or MOCKUP_CANVAS_ASPECT_RATIO)
    if canvas_aspect not in MockupBaseGenerationCatalog.ASPECT_RATIOS:
        canvas_aspect = MOCKUP_CANVAS_ASPECT_RATIO
    merged["generation_canvas_aspect_ratio"] = canvas_aspect

    style = str(merged.get("default_style") or DEFAULT_PROMPT_SETTINGS["default_style"])
    tone = str(merged.get("default_tone") or DEFAULT_PROMPT_SETTINGS["default_tone"])
    season = str(merged.get("default_season") or DEFAULT_PROMPT_SETTINGS["default_season"])
    merged["default_style"] = style if style in STYLE_OPTIONS else str(DEFAULT_PROMPT_SETTINGS["default_style"])
    merged["default_tone"] = tone if tone in TONE_OPTIONS else str(DEFAULT_PROMPT_SETTINGS["default_tone"])
    merged["default_season"] = season if season in SEASON_OPTIONS else str(DEFAULT_PROMPT_SETTINGS["default_season"])
    return merged


def _apply_environment_modifiers(prompt_text: str, settings: dict[str, Any]) -> str:
    style = str(settings.get("default_style") or "Contemporary")
    tone = str(settings.get("default_tone") or "Warm")
    season = str(settings.get("default_season") or "Any")
    lines = [
        "STYLE AND MOOD DIRECTION:",
        f"- Visual style: {style}",
        f"- Tone: {tone}",
    ]
    if season != "Any":
        lines.append(f"- Season cue: {season}")
    lines.append("- Keep these directions secondary to all geometry/placeholder constraints.")
    return prompt_text + "\n\n" + "\n".join(lines)


def _serialize_prompt_with_metadata(
    prompt_text: str,
    *,
    placeholder_mode: str,
    guide_path: str,
) -> str:
    """Embed guide metadata into prompt_text without requiring a schema change."""
    payload = {
        "placeholder_mode": str(placeholder_mode or "cyan"),
        "guide_path": str(guide_path or ""),
    }
    return f"{PROMPT_METADATA_PREFIX}{json.dumps(payload, sort_keys=True)}\n{prompt_text}"


def _append_guide_context(message: str, *, placeholder_mode: str, guide_path: str) -> str:
    suffix = f" [placeholder_mode={placeholder_mode or 'cyan'} guide_path={guide_path or '<none>'}]"
    return f"{message}{suffix}"


def _build_cyan_retry_prompt(base_prompt: str, retry_attempt: int) -> str:
    """Retry prompt for placeholder generation."""
    return f"{base_prompt}\nRetry attempt #{retry_attempt}."


def _build_trojan_retry_prompt(base_prompt: str, retry_attempt: int) -> str:
    """Retry prompt for artwork editing."""
    return f"{base_prompt}\nRetry attempt #{retry_attempt}."


def _normalize_generation_mode(mode: str | None) -> str:
    """Normalize queue and job mode values to supported generation modes."""
    normalized = str(mode or GENERATION_MODE_STANDARD).strip().lower()
    if normalized == GENERATION_MODE_CHROMAKEY_AUTO:
        return GENERATION_MODE_CHROMAKEY_AUTO
    if normalized == GENERATION_MODE_ARTWORK_TROJAN:
        return GENERATION_MODE_ARTWORK_TROJAN
    if normalized == GENERATION_MODE_ARTWORK_ONLY_COMPOSITE:
        return GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
    return GENERATION_MODE_STANDARD


def _resolve_trojan_reference_artwork_path(aspect_ratio: str) -> Path:
    """Return the prepared outlined-artwork reference image for a requested aspect ratio."""
    candidate_paths = (
        TROJAN_ARTWORK_DIR / f"{aspect_ratio}-outlined-artwork.png",
        TROJAN_ARTWORK_DIR / f"{aspect_ratio}.png",
        TROJAN_ARTWORK_DIR / f"{aspect_ratio}.jpg",
        TROJAN_ARTWORK_DIR / f"{aspect_ratio}.jpeg",
        LEGACY_TROJAN_ARTWORK_DIR / f"{aspect_ratio}.jpg",
        LEGACY_TROJAN_ARTWORK_DIR / f"{aspect_ratio}.png",
        LEGACY_TROJAN_ARTWORK_DIR / f"{aspect_ratio}.jpeg",
    )
    for candidate_path in candidate_paths:
        if candidate_path.exists():
            return candidate_path

    raise FileNotFoundError(
        "Outlined reference artwork not found for "
        f"aspect_ratio={aspect_ratio} in {TROJAN_ARTWORK_DIR} "
        f"or legacy path {LEGACY_TROJAN_ARTWORK_DIR}"
    )


def _resolve_artwork_only_reference_path(aspect_ratio: str) -> Path:
    candidate_paths = (
        ARTWORK_ONLY_GUIDE_DIR / f"{aspect_ratio}-artwork-placeholder.png",
        ARTWORK_ONLY_GUIDE_DIR / f"{aspect_ratio}.png",
        ARTWORK_ONLY_GUIDE_DIR / f"{aspect_ratio}.jpg",
        ARTWORK_ONLY_GUIDE_DIR / f"{aspect_ratio}.jpeg",
    )
    for candidate_path in candidate_paths:
        if candidate_path.exists():
            return candidate_path

    raise FileNotFoundError(
        "Artwork-only reference guide not found for "
        f"aspect_ratio={aspect_ratio} in {ARTWORK_ONLY_GUIDE_DIR}"
    )


def _build_artwork_trojan_prompt(category: str, variation_index: int) -> str:
    """Build a prompt for Trojan Art mode using the provided bordered artwork as the anchor."""
    category_descriptor = MockupPromptService._get_category_descriptor(category)
    return (
        f"Create a photorealistic, professional interior design photograph of a {category_descriptor}.\n\n"
        "SCENE COMPOSITION:\n"
        "- Three-quarter perspective view of the room interior\n"
        "- Camera positioned to show depth and realistic architectural space\n"
        "- Professional commercial staging and magazine-quality composition\n\n"
        "ARTWORK PLACEMENT:\n"
        "- Use the provided bordered reference artwork exactly as the wall artwork subject\n"
        "- Preserve the full rectangular artwork geometry and perspective naturally on the wall\n"
        "- Keep the complete cyan-black fiducial border fully visible and unobstructed\n"
        "- Preserve fiducial stripe widths exactly: 30px outer cyan and 30px inner black\n"
        "- Do not blur, feather, recolor, or stylize the fiducial border edges\n"
        "- Do not crop, repaint, replace, stylize, or partially hide the bordered artwork\n"
        "- Do not add glare, reflections, shadows, texture overlays, furniture overlap, or sunlight patches across the bordered artwork\n\n"
        "ROOM DIRECTION:\n"
        "- The room should feel premium, realistic, and commercially staged for wall art presentation\n"
        "- Lighting should flatter the space while leaving the bordered artwork clean and fully legible\n"
        f"- Variation #{variation_index}: create a distinct but believable composition for this category\n\n"
        "OUTPUT:\n"
        "Generate a single high-quality photorealistic image with the bordered reference artwork mounted clearly on the wall."
    )


def _build_chromakey_prompt(
    *,
    category: str,
    variation_index: int,
    aspect_ratio: str,
    chromakey_hex: str,
) -> str:
    """Build prompt for chromakey automation mode (#00FFCC keyed cutout workflow)."""
    category_descriptor = MockupPromptService._get_category_descriptor(category)
    aspect_ratio_colon = str(aspect_ratio or "4x5").replace("x", ":")
    base_prompt = MATTE_INSERTION_PROMPT_TEMPLATE.format(aspect_ratio=aspect_ratio_colon)
    return (
        f"{base_prompt}\n\n"
        "SCENE DIRECTION:\n"
        f"- Style the room as a {category_descriptor}.\n"
        "- Keep realistic architecture, depth, and 24mm wide-angle camera perspective.\n"
        f"- Maintain exact chromakey value {chromakey_hex} in the cyan selection ring.\n"
        "- Preserve both black guard rails around cyan as crisp geometric borders; never blur or blend them.\n"
        f"- Variation #{variation_index}: provide a distinct composition while preserving the outlined target geometry."
    )


def _build_studio_matte_prompt(
    prompt_text: str,
    aspect_ratio: str,
    variation_index: int,
    category: str,
    total_variations: int,
    has_reference: bool = False,
) -> str:
    """Compose Gemini Studio prompt based on whether a reference image is available.
    
    Args:
        prompt_text: Custom user prompt text
        aspect_ratio: Target aspect ratio (e.g., "4x5")
        variation_index: Which variation in batch (1-indexed)
        category: Target interior category
        total_variations: Total variations in batch
        has_reference: True if a reference image was provided (for edit_image); False for pure generation
    
    Returns:
        Formatted prompt string appropriate for the generation mode
    """
    aspect_ratio_colon = str(aspect_ratio or "4x5").replace("x", ":")
    category_descriptor = MockupPromptService._get_category_descriptor(category) or category
    
    if has_reference:
        # Reference-guided editing: preserve the artwork exactly
        seed = MATTE_REFERENCE_GUIDED_PROMPT_TEMPLATE.format(
            aspect_ratio_colon=aspect_ratio_colon,
            category_descriptor=category_descriptor,
        )
    else:
        # Pure generation: create a placeholder from scratch
        seed = MATTE_PURE_GENERATION_PROMPT_TEMPLATE.format(
            aspect_ratio_colon=aspect_ratio_colon,
            category_descriptor=category_descriptor,
        )
    
    custom = str(prompt_text or "").strip()
    if custom:
        # Clean-pass mode: when the UI already provides a fully authored prompt,
        # pass it through directly without re-appending batch metadata or helper prose.
        return custom

    if has_reference:
        return (
            f"{seed}\n\n"
            "Use the provided reference artwork as the immutable centerpiece. "
            "Do not warp, crop, repaint, stylize, or obscure it."
        )

    return (
        f"{seed}\n\n"
        "Create a premium, photorealistic room scene suitable for a production mockup base."
    )


def _build_studio_reference_guided_prompt(
    prompt_text: str,
    aspect_ratio: str,
    variation_index: int,
    category: str,
    total_variations: int,
    thought_signature: str,
) -> str:
    """Build prompt for reference-guided editing (when artwork reference image is provided)."""
    base_prompt = _build_studio_matte_prompt(
        prompt_text,
        aspect_ratio,
        variation_index,
        category,
        total_variations,
        has_reference=True,
    )
    # Consistency guardrail removed to reduce prompt bloat; thought signature handled internally by Gemini API
    return base_prompt


def _build_studio_pure_generation_prompt(
    prompt_text: str,
    aspect_ratio: str,
    variation_index: int,
    category: str,
    total_variations: int,
    thought_signature: str,
) -> str:
    """Build prompt for pure generation (when NO artwork reference image is available)."""
    base_prompt = _build_studio_matte_prompt(
        prompt_text,
        aspect_ratio,
        variation_index,
        category,
        total_variations,
        has_reference=False,
    )
    # Consistency guardrail removed to reduce prompt bloat; thought signature handled internally by Gemini API
    return base_prompt


def _build_studio_matte_prompt_with_signature(
    prompt_text: str,
    aspect_ratio: str,
    variation_index: int,
    category: str,
    total_variations: int,
    thought_signature: str,
) -> str:
    """DEPRECATED: Use _build_studio_reference_guided_prompt or _build_studio_pure_generation_prompt instead."""
    base_prompt = _build_studio_matte_prompt(
        prompt_text,
        aspect_ratio,
        variation_index,
        category,
        total_variations,
        has_reference=False,
    )
    signature = str(thought_signature or "").strip()
    if not signature:
        return base_prompt
    return (
        f"{base_prompt}\n\n"
        "CONSISTENCY GUARDRAIL:\n"
        f"- Reuse thought signature: {signature}\n"
        "- Keep global lighting direction, white-balance mood, and tonal continuity aligned with this signature."
    )


def _build_artwork_only_composite_prompt(
    *,
    category: str,
    variation_index: int,
    aspect_ratio: str,
) -> str:
    """Build a minimal plain composite prompt with strict artwork placement rules."""
    category_descriptor = MockupPromptService._get_category_descriptor(category)
    return (
        f"Create a photorealistic interior mockup of a {category_descriptor}. "
        "Use the supplied artwork image as the only wall artwork. "
        f"The visible artwork area must remain exact aspect ratio {aspect_ratio} (width:height). "
        "Keep a direct frontal view of the artwork with minimal perspective distortion. "
        "Keep the artwork fully visible and unobstructed. "
        "Do not crop, warp, repaint, stylize, or replace the artwork. "
        "Do not add overlay marks, text, or watermarks. "
        f"Create a distinct but realistic composition for variation {variation_index}."
    )


def _resolve_generation_assets(
    *,
    generation_mode: str,
    aspect_ratio: str,
    category: str,
    variation_index: int,
    prompt_settings: dict[str, Any],
) -> tuple[str, Path | None, str]:
    normalized_mode = _normalize_generation_mode(generation_mode)
    if normalized_mode == GENERATION_MODE_ARTWORK_ONLY_COMPOSITE:
        prompt_text = _build_artwork_only_composite_prompt(
            category=category,
            variation_index=variation_index,
            aspect_ratio=aspect_ratio,
        )
        return (
            prompt_text,
            _resolve_artwork_only_reference_path(aspect_ratio),
            GENERATION_MODE_ARTWORK_ONLY_COMPOSITE,
        )

    if normalized_mode == GENERATION_MODE_CHROMAKEY_AUTO:
        prompt_text = _build_chromakey_prompt(
            category=category,
            variation_index=variation_index,
            aspect_ratio=aspect_ratio,
            chromakey_hex=CHROMAKEY_TARGET_HEX,
        )
        prompt_text = _apply_prompt_wrapper(
            str(prompt_settings.get("standard_prefix") or ""),
            prompt_text,
            str(prompt_settings.get("standard_suffix") or ""),
        )
        prompt_text = _apply_environment_modifiers(prompt_text, prompt_settings)
        return (
            prompt_text,
            _resolve_trojan_reference_artwork_path(aspect_ratio),
            "outlined",
        )

    prompt_text = _build_artwork_trojan_prompt(
        category=category,
        variation_index=variation_index,
    )
    prompt_text = _apply_prompt_wrapper(
        str(prompt_settings.get("outlined_prefix") or ""),
        prompt_text,
        str(prompt_settings.get("outlined_suffix") or ""),
    )
    prompt_text = _apply_environment_modifiers(prompt_text, prompt_settings)
    return (
        prompt_text,
        _resolve_trojan_reference_artwork_path(aspect_ratio),
        GENERATION_MODE_ARTWORK_TROJAN,
    )


def _load_prompt_settings() -> dict[str, Any]:
    if not PROMPT_SETTINGS_PATH.exists():
        return _normalize_prompt_settings(None)

    try:
        payload = json.loads(PROMPT_SETTINGS_PATH.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            return _normalize_prompt_settings(None)
    except Exception:
        return _normalize_prompt_settings(None)

    return _normalize_prompt_settings(payload)


def _apply_prompt_wrapper(prefix: str, body: str, suffix: str) -> str:
    pieces = [str(prefix or "").strip(), str(body or "").strip(), str(suffix or "").strip()]
    return "\n\n".join(piece for piece in pieces if piece)


def _resolve_celery_app() -> Celery:
    """Resolve the shared Celery app or create a fallback instance."""
    try:
        from application.app import celery as shared_celery  # type: ignore

        return shared_celery
    except (ImportError, AttributeError):
        broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
        result_backend = os.getenv("CELERY_RESULT_BACKEND", broker_url)
        fallback = Celery(
            "artlomo.mockup_generator",
            broker=broker_url,
            backend=result_backend,
        )
        fallback.conf.update(
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
            timezone="UTC",
            enable_utc=True,
        )
        return fallback


celery = _resolve_celery_app()


def _load_control_state() -> dict[str, str]:
    """Load persisted operator control state for the mockup generator."""
    if not CONTROL_STATE_PATH.exists():
        return {
            "state": "running",
            "updated_at": "",
            "message": "",
            "max_retries": str(MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES),
            "skip_coordinate_detection": "false",
            "custom_prompt_text": "",
            "raw_prompt_only_enabled": "false",
            "raw_prompt_text": "",
        }

    try:
        payload = json.loads(CONTROL_STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {
            "state": "running",
            "updated_at": "",
            "message": "",
            "max_retries": str(MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES),
            "skip_coordinate_detection": "false",
            "custom_prompt_text": "",
            "raw_prompt_only_enabled": "false",
            "raw_prompt_text": "",
        }

    if not isinstance(payload, dict):
        return {
            "state": "running",
            "updated_at": "",
            "message": "",
            "max_retries": str(MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES),
            "skip_coordinate_detection": "false",
            "custom_prompt_text": "",
            "raw_prompt_only_enabled": "false",
            "raw_prompt_text": "",
        }

    return {
        "state": str(payload.get("state") or "running"),
        "updated_at": str(payload.get("updated_at") or ""),
        "message": str(payload.get("message") or ""),
        "max_retries": str(payload.get("max_retries") or MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES),
        "skip_coordinate_detection": str(payload.get("skip_coordinate_detection") or "false"),
        "custom_prompt_text": str(payload.get("custom_prompt_text") or ""),
        "raw_prompt_only_enabled": str(payload.get("raw_prompt_only_enabled") or "false"),
        "raw_prompt_text": str(payload.get("raw_prompt_text") or ""),
    }


def _render_custom_prompt(
    template_text: str,
    *,
    aspect_ratio: str,
    category: str,
    variation_index: int,
) -> str:
    rendered = str(template_text or "")
    replacement_groups = {
        aspect_ratio: ("{{aspect_ratio}}", "{aspect_ratio}", "[[aspect_ratio]]"),
        category: ("{{category}}", "{category}", "[[category]]"),
        str(variation_index): ("{{variation_index}}", "{variation_index}", "[[variation_index]]"),
    }
    for value, tokens in replacement_groups.items():
        for token in tokens:
            rendered = rendered.replace(token, value)

    rendered = rendered.strip()
    if aspect_ratio not in rendered:
        rendered = (
            f"{rendered}\n\n"
            f"Technical constraint: preserve the supplied artwork at exact aspect ratio {aspect_ratio} (width:height)."
        ).strip()
    return rendered


@contextmanager
def _session_scope() -> Iterator[Any]:
    """Yield a SQLAlchemy session with safe rollback/close semantics."""
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _make_job_external_id(
    aspect_ratio: str,
    category: str,
    variation_index: int,
    generation_mode: str = GENERATION_MODE_STANDARD,
) -> str:
    """Create deterministic unique external job_id for idempotent queueing."""
    normalized_mode = _normalize_generation_mode(generation_mode)
    base_job_id = f"mbg_{aspect_ratio}_{category}_v{variation_index}".replace(" ", "-")
    if normalized_mode == GENERATION_MODE_STANDARD:
        return base_job_id
    return f"{base_job_id}__{normalized_mode}".replace(" ", "-")


def _coordinates_output_path(image_path: str) -> Path:
    """Build path for per-image schema coordinate output."""
    image_file = Path(image_path)
    return image_file.with_name(f"{image_file.stem}_schema_coordinates.json")


def _save_coordinates_schema(image_path: str, coordinates: list[dict[str, int]]) -> str:
    """Persist extracted coordinates next to generated image in JSON schema form."""
    output_path = _coordinates_output_path(image_path)
    payload = {
        "format_version": "1.0",
        "image_path": image_path,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "points": coordinates,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(output_path)


def _delete_file_if_exists(path_value: str | None) -> None:
    """Delete an output file if it exists, ignoring missing files."""
    if not path_value:
        return

    try:
        path = Path(path_value)
        if path.exists():
            path.unlink()
    except Exception:
        logger.warning("Failed to remove partial output file: %s", path_value, exc_info=True)


def _cleanup_partial_outputs(generated_image_path: str | None, coordinates_path: str | None) -> None:
    """Best-effort cleanup for partially generated job artifacts."""
    _delete_file_if_exists(coordinates_path)
    _delete_file_if_exists(generated_image_path)


def _register_generated_base(
    *,
    external_job_id: str,
    aspect_ratio: str,
    category: str,
    variation_index: int,
    generated_image_path: str,
    coordinates_path: str,
) -> str:
    """Promote a completed generated job into the mockup catalog staging queue."""
    service = CatalogAdminService()
    base = service.upsert_generated_base(
        job_id=external_job_id,
        aspect_ratio=aspect_ratio,
        category=category,
        variation_index=variation_index,
        generated_image_path=generated_image_path,
        source_coordinates_path=coordinates_path,
    )
    return str(base.id)


def _reset_job_to_pending(*, job_id: int, stage: str, message: str) -> None:
    """Return a job to Pending state after a safe stop boundary is reached."""
    with _session_scope() as session:
        job = session.get(MockupBaseGenerationJob, job_id)
        if job is None:
            logger.error("Unable to reset job %s to pending; record not found", job_id)
            return

        job.status = "Pending"
        job.stage = stage
        job.reason = "Stopped"
        job.error_message = message[:4000]
        job.generated_image_path = None
        job.coordinates_path = None
        job.finished_at = None
        session.commit()


def _set_job_failed(
    *,
    job_id: int,
    error_message: str,
    reason: str,
) -> None:
    """Persist failed status in an isolated transaction."""
    with _session_scope() as session:
        job = session.get(MockupBaseGenerationJob, job_id)
        if job is None:
            logger.error("Unable to mark job %s as failed; record not found", job_id)
            return

        job.status = "Failed"
        job.stage = "Failed"
        job.error_message = error_message[:4000]
        job.reason = reason[:128]
        job.generated_image_path = None
        job.coordinates_path = None
        job.finished_at = datetime.utcnow()
        session.commit()


def _reset_job_for_retry(
    *,
    job_id: int,
    stage: str,
    message: str,
    reason: str,
) -> None:
    """Return a job to Pending while preserving retry context on the dashboard."""
    with _session_scope() as session:
        job = session.get(MockupBaseGenerationJob, job_id)
        if job is None:
            logger.error("Unable to reset job %s for retry; record not found", job_id)
            return

        job.status = "Pending"
        job.stage = stage
        job.reason = reason[:128]
        job.error_message = message[:4000]
        job.generated_image_path = None
        job.coordinates_path = None
        job.finished_at = None
        session.commit()


def _compute_rate_limit_retry_delay(*, job_id: int, retry_after_seconds: int | None, retry_count: int) -> int:
    """Spread 429 retries so queued jobs do not stampede Gemini again."""
    base_delay = retry_after_seconds or MOCKUP_GEMINI_RATE_LIMIT_RETRY_FALLBACK_SECONDS
    stagger_seconds = (job_id % 5) * 4
    retry_penalty_seconds = retry_count * 10
    return max(1, base_delay + stagger_seconds + retry_penalty_seconds)


@celery.task(name="mockups.queue_mockup_jobs")
def queue_mockup_jobs(mode: str = GENERATION_MODE_STANDARD) -> dict[str, int]:
    """Create any missing jobs for every (aspect, category, variation) tuple.

    Returns:
        Summary dictionary with counts of expected, existing, and created jobs.
    """
    aspects = tuple(MockupBaseGenerationCatalog.ASPECT_RATIOS)
    categories = tuple(MockupBaseGenerationCatalog.CATEGORIES)
    variation_min = MockupBaseGenerationCatalog.VARIATION_MIN_INDEX
    variation_max = MockupBaseGenerationCatalog.VARIATION_MAX_INDEX
    generation_mode = _normalize_generation_mode(mode)

    expected_total = len(aspects) * len(categories) * (variation_max - variation_min + 1)

    with _session_scope() as session:
        existing_rows = session.query(
            MockupBaseGenerationJob.aspect_ratio,
            MockupBaseGenerationJob.category,
            MockupBaseGenerationJob.variation_index,
            MockupBaseGenerationJob.generation_mode,
        ).all()

        existing_keys = {
            (str(r[0]), str(r[1]), int(r[2]), _normalize_generation_mode(str(r[3] or GENERATION_MODE_STANDARD)))
            for r in existing_rows
        }
        existing_mode_keys = {k for k in existing_keys if k[3] == generation_mode}

        new_jobs: list[MockupBaseGenerationJob] = []
        for aspect_ratio in aspects:
            for category in categories:
                for variation_index in range(variation_min, variation_max + 1):
                    identity = (aspect_ratio, category, variation_index, generation_mode)
                    if identity in existing_keys:
                        continue

                    new_jobs.append(
                        MockupBaseGenerationJob(
                            job_id=_make_job_external_id(
                                aspect_ratio=aspect_ratio,
                                category=category,
                                variation_index=variation_index,
                                generation_mode=generation_mode,
                            ),
                            aspect_ratio=aspect_ratio,
                            category=category,
                            variation_index=variation_index,
                            generation_mode=generation_mode,
                            status="Pending",
                            attempts=0,
                            stage="Queued",
                        )
                    )

        if new_jobs:
            session.add_all(new_jobs)
            session.commit()

        result = {
            "expected_total": expected_total,
            "existing_before": len(existing_mode_keys),
            "created": len(new_jobs),
            "final_total": len(existing_mode_keys) + len(new_jobs),
        }

        logger.info(
            "Queued mockup jobs: mode=%s expected=%s existing_before=%s created=%s final_total=%s",
            generation_mode,
            result["expected_total"],
            result["existing_before"],
            result["created"],
            result["final_total"],
        )

        return result


@celery.task(name="mockups.build_chromakey_library")
def build_chromakey_library(limit: int = 0) -> dict[str, int]:
    """Queue and dispatch the full chromakey automation library build.

    This task is designed for unattended generation of the 22x13x20 matrix.

    Args:
        limit: Optional cap for canary runs. 0 dispatches all pending jobs.

    Returns:
        Summary counts for queued/dispatch state.
    """
    queue_summary = queue_mockup_jobs(mode=GENERATION_MODE_CHROMAKEY_AUTO)

    with _session_scope() as session:
        query = (
            session.query(MockupBaseGenerationJob.id)
            .filter(MockupBaseGenerationJob.status == "Pending")
            .filter(MockupBaseGenerationJob.generation_mode == GENERATION_MODE_CHROMAKEY_AUTO)
            .order_by(MockupBaseGenerationJob.aspect_ratio.asc(), MockupBaseGenerationJob.category.asc(), MockupBaseGenerationJob.variation_index.asc())
        )
        if int(limit or 0) > 0:
            query = query.limit(int(limit))

        pending_ids = [int(row[0]) for row in query.all()]

    dispatched = 0
    for db_job_id in pending_ids:
        process_mockup_job.delay(db_job_id)
        dispatched += 1

    summary = {
        "queued_expected_total": int(queue_summary.get("expected_total", 0)),
        "queued_created": int(queue_summary.get("created", 0)),
        "pending_selected": len(pending_ids),
        "dispatched": dispatched,
    }
    logger.info("Chromakey library build dispatch summary: %s", summary)
    return summary


@celery.task(
    bind=True,
    name="mockups.process_mockup_job",
    rate_limit=MOCKUP_GEMINI_TASK_RATE_LIMIT,
)
def process_mockup_job(self: Any, job_id: int) -> dict[str, Any]:
    """Process one mockup generation job end-to-end.

    Steps:
    1. Claim job if status is Pending/Failed.
    2. Build prompt via MockupPromptService.
    3. Generate image via GeminiImageService.
    4. Extract cyan coordinates via MockupCoordinateService.
    5. Persist output references and mark job Completed.

    Args:
        job_id: Primary key of MockupBaseGenerationJob.

    Returns:
        Structured status payload for monitoring/logging.
    """
    generated_image_path: str | None = None
    coordinates_path: str | None = None
    gemini_service: GeminiImageService | None = None
    effective_prompt = ""
    used_coordinate_fallback = False

    try:
        control_state = _load_control_state()
        control_state_value = str(control_state.get("state", "running"))
        coordinate_fallback_enabled = _is_coordinate_fallback_enabled(control_state)
        custom_prompt_template = str(control_state.get("custom_prompt_text") or "").strip()
        use_custom_prompt = bool(custom_prompt_template)
        raw_prompt_only_enabled = str(control_state.get("raw_prompt_only_enabled") or "false").strip().lower() in {"1", "true", "yes", "on"}
        raw_prompt_text = str(control_state.get("raw_prompt_text") or "")
        use_raw_prompt_only = raw_prompt_only_enabled and bool(raw_prompt_text)
        if control_state_value == "paused":
            return {
                "status": "paused",
                "job_id": job_id,
                "message": "Pipeline is paused; job was not started",
            }

        if control_state_value == "stopped":
            _reset_job_to_pending(
                job_id=job_id,
                stage="Stopped",
                message="Stop requested before job claim",
            )
            return {
                "status": "stopped",
                "job_id": job_id,
                "message": "Pipeline is stopped; job remains pending until re-queued",
            }

        with _session_scope() as session:
            job = session.get(MockupBaseGenerationJob, job_id)
            if job is None:
                return {
                    "status": "not_found",
                    "job_id": job_id,
                    "message": "Job record does not exist",
                }

            if job.status not in {"Pending", "Failed"}:
                return {
                    "status": "skipped",
                    "job_id": job_id,
                    "message": f"Job in status '{job.status}' cannot be processed",
                }

            job.status = "Generating"
            job.stage = "GeneratingImage"
            job.started_at = job.started_at or datetime.utcnow()
            job.finished_at = None
            job.error_message = None
            job.reason = None
            job.attempts = int(job.attempts or 0) + 1
            session.commit()

            aspect_ratio = str(job.aspect_ratio)
            category = str(job.category)
            variation_index = int(job.variation_index)
            external_job_id = str(job.job_id)
            generation_mode = _normalize_generation_mode(str(job.generation_mode or GENERATION_MODE_ARTWORK_TROJAN))

        thought_signature_key = f"mockup:{generation_mode}:{aspect_ratio}:{category}"
        reused_thought_signature = ""
        if variation_index > 1:
            reused_thought_signature = _get_thought_signature(thought_signature_key)

        prompt_settings = _load_prompt_settings()
        canvas_aspect_ratio = str(
            prompt_settings.get("generation_canvas_aspect_ratio")
            or MOCKUP_CANVAS_ASPECT_RATIO
        )
        if generation_mode == GENERATION_MODE_CHROMAKEY_AUTO:
            canvas_aspect_ratio = MOCKUP_CANVAS_ASPECT_RATIO

        if use_raw_prompt_only:
            generation_mode = GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
            prompt_text = raw_prompt_text
            reference_guide_path = _resolve_artwork_only_reference_path(aspect_ratio)
            placeholder_mode_override = GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
        else:
            prompt_text, reference_guide_path, placeholder_mode_override = _resolve_generation_assets(
                generation_mode=generation_mode,
                aspect_ratio=aspect_ratio,
                category=category,
                variation_index=variation_index,
                prompt_settings=prompt_settings,
            )

        if (not use_raw_prompt_only) and use_custom_prompt:
            prompt_text = _render_custom_prompt(
                custom_prompt_template,
                aspect_ratio=aspect_ratio,
                category=category,
                variation_index=variation_index,
            )
        effective_prompt = prompt_text

        gemini_service = GeminiImageService()
        coordinates: list[dict[str, int]] | None = None
        placeholder_mode = placeholder_mode_override
        guide_path = ""
        for attempt_index in range(1, MAX_CYAN_REGEN_ATTEMPTS + 1):
            generated_image_path = gemini_service.generate_image(
                prompt=effective_prompt,
                aspect_ratio=aspect_ratio,
                category=category,
                variation_index=variation_index,
                generation_aspect_ratio=canvas_aspect_ratio,
                reference_guide_override=reference_guide_path,
                placeholder_mode_override=placeholder_mode_override,
                thought_signature_override=reused_thought_signature or None,
            )

            captured_signature = str(getattr(gemini_service, "last_thought_signature", "") or "").strip()
            if variation_index == 1 and captured_signature:
                _set_thought_signature(thought_signature_key, captured_signature)
            elif variation_index > 1 and not reused_thought_signature and captured_signature:
                _set_thought_signature(thought_signature_key, captured_signature)
            placeholder_mode = str(
                getattr(gemini_service, "last_placeholder_mode", placeholder_mode_override)
                or placeholder_mode_override
            )
            guide_path = str(getattr(gemini_service, "last_reference_guide_path", "") or "")
            logger.info(
                "Mockup job guide context: job_id=%s generation_mode=%s placeholder_mode=%s guide_path=%s attempt=%s/%s",
                job_id,
                generation_mode,
                placeholder_mode,
                guide_path or "<none>",
                attempt_index,
                MAX_CYAN_REGEN_ATTEMPTS,
            )

            if _load_control_state().get("state", "running") == "stopped":
                _cleanup_partial_outputs(generated_image_path, None)
                _reset_job_to_pending(
                    job_id=job_id,
                    stage="StoppedAfterImageGeneration",
                    message="Stop requested after image generation; partial outputs cleaned",
                )
                return {
                    "status": "stopped",
                    "job_id": job_id,
                    "message": "Stop requested after image generation; outputs cleaned",
                }

            with _session_scope() as session:
                job = session.get(MockupBaseGenerationJob, job_id)
                if job is None:
                    raise RuntimeError(f"Job {job_id} disappeared before processing stage update")

                job.status = "Processing"
                job.stage = "ExtractingCoordinates"
                job.prompt_text = _serialize_prompt_with_metadata(
                    effective_prompt,
                    placeholder_mode=placeholder_mode,
                    guide_path=guide_path,
                )
                job.generated_image_path = generated_image_path
                session.commit()

            should_skip_coordinate_detection = (
                generation_mode == GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
                or coordinate_fallback_enabled
            )

            if should_skip_coordinate_detection:
                coordinates = _build_fallback_coordinates(
                    generated_image_path,
                    aspect_ratio=aspect_ratio,
                )
                used_coordinate_fallback = True
                logger.warning(
                    "Coordinate detection skipped for job %s (generation_mode=%s); using fallback coordinates.",
                    job_id,
                    generation_mode,
                )
                break

            try:
                if generation_mode == GENERATION_MODE_CHROMAKEY_AUTO:
                    coordinates = ChromakeyBridgeService.extract_coordinates_and_erase(
                        image_path=generated_image_path,
                        hex_color=CHROMAKEY_TARGET_HEX,
                    )
                else:
                    coordinates = CompositeCoordinateService.extract_coordinates_and_erase(generated_image_path)
                break
            except (
                CompositeCyanContourNotFoundError,
                CompositeInvalidQuadError,
                ChromakeyRegionNotFoundError,
                ChromakeyQuadError,
                ChromakeyBridgeError,
            ) as exc:
                if attempt_index >= MAX_CYAN_REGEN_ATTEMPTS:
                    if should_skip_coordinate_detection:
                        coordinates = _build_fallback_coordinates(
                            generated_image_path,
                            aspect_ratio=aspect_ratio,
                        )
                        used_coordinate_fallback = True
                        logger.warning(
                            "Using fallback coordinates for job %s after extraction failure (%s).",
                            job_id,
                            type(exc).__name__,
                        )
                        break
                    raise
                logger.warning(
                    "Trojan coordinate extraction failed for job %s on attempt %s/%s; regenerating image.",
                    job_id,
                    attempt_index,
                    MAX_CYAN_REGEN_ATTEMPTS,
                )
                _cleanup_partial_outputs(generated_image_path, None)
                generated_image_path = None
                if (not use_raw_prompt_only) and (not use_custom_prompt) and generation_mode == GENERATION_MODE_ARTWORK_TROJAN:
                    effective_prompt = _build_trojan_retry_prompt(prompt_text, attempt_index + 1)

        if coordinates is None or generated_image_path is None:
            raise RuntimeError(f"Job {job_id} did not produce coordinates after retry loop")

        coordinates_path = _save_coordinates_schema(
            image_path=generated_image_path,
            coordinates=coordinates,
        )

        registered_base_id = _register_generated_base(
            external_job_id=external_job_id,
            aspect_ratio=aspect_ratio,
            category=category,
            variation_index=variation_index,
            generated_image_path=generated_image_path,
            coordinates_path=coordinates_path,
        )

        if _load_control_state().get("state", "running") == "stopped":
            _cleanup_partial_outputs(generated_image_path, coordinates_path)
            _reset_job_to_pending(
                job_id=job_id,
                stage="StoppedAfterCoordinateExtraction",
                message="Stop requested after coordinate extraction; partial outputs cleaned",
            )
            return {
                "status": "stopped",
                "job_id": job_id,
                "message": "Stop requested after coordinate extraction; outputs cleaned",
            }

        with _session_scope() as session:
            job = session.get(MockupBaseGenerationJob, job_id)
            if job is None:
                raise RuntimeError(f"Job {job_id} disappeared before completion update")

            job.status = "Completed"
            job.stage = "Completed"
            if used_coordinate_fallback:
                job.reason = "FallbackCoordinates"
            job.coordinates_path = coordinates_path
            job.finished_at = datetime.utcnow()
            session.commit()

        logger.info(
            "Mockup job completed: job_id=%s generation_mode=%s category=%s aspect_ratio=%s variation=%s placeholder_mode=%s guide_path=%s",
            job_id,
            generation_mode,
            category,
            aspect_ratio,
            variation_index,
            placeholder_mode,
            guide_path or "<none>",
        )
        return {
            "status": "completed",
            "job_id": job_id,
            "generated_image_path": generated_image_path,
            "coordinates_path": coordinates_path,
            "base_id": registered_base_id,
            "coordinates": coordinates,
            "coordinates_source": "fallback" if used_coordinate_fallback else "extracted",
        }

    except GeminiRateLimitError as exc:
        placeholder_mode = str(
            getattr(gemini_service, "last_placeholder_mode", GENERATION_MODE_ARTWORK_TROJAN)
            or GENERATION_MODE_ARTWORK_TROJAN
        )
        guide_path = str(getattr(gemini_service, "last_reference_guide_path", "") or "")
        contextual_error = _append_guide_context(str(exc), placeholder_mode=placeholder_mode, guide_path=guide_path)
        logger.warning("Gemini rate limit hit for mockup job %s: %s", job_id, contextual_error)
        _cleanup_partial_outputs(generated_image_path, coordinates_path)

        retry_count = int(getattr(getattr(self, "request", None), "retries", 0) or 0)
        countdown = _compute_rate_limit_retry_delay(
            job_id=job_id,
            retry_after_seconds=exc.retry_after_seconds,
            retry_count=retry_count,
        )

        retry_message = f"{contextual_error} Scheduled retry in approximately {countdown}s."
        _reset_job_for_retry(
            job_id=job_id,
            stage="RetryQueued",
            message=retry_message,
            reason=type(exc).__name__,
        )

        # Read max_retries from persisted control state so the UI selector takes effect.
        task_max_retries = int(_load_control_state().get("max_retries") or MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES)
        try:
            raise self.retry(
                exc=exc,
                countdown=countdown,
                max_retries=task_max_retries,
            )
        except MaxRetriesExceededError:
            logger.error("Gemini rate limit retries exhausted for mockup job %s", job_id)
            _set_job_failed(job_id=job_id, error_message=contextual_error, reason=type(exc).__name__)
            return {
                "status": "failed",
                "job_id": job_id,
                "error_type": type(exc).__name__,
                "error": contextual_error,
            }

    except (
        CyanQuadNotFoundError,
        InvalidCyanShapeError,
        CompositeCyanContourNotFoundError,
        CompositeInvalidQuadError,
        ChromakeyRegionNotFoundError,
        ChromakeyQuadError,
        ChromakeyBridgeError,
        GeminiGenerationError,
        GeminiAuthenticationError,
        GeminiFileSaveError,
        ValueError,
        FileNotFoundError,
    ) as exc:
        placeholder_mode = str(
            getattr(gemini_service, "last_placeholder_mode", GENERATION_MODE_ARTWORK_TROJAN)
            or GENERATION_MODE_ARTWORK_TROJAN
        )
        guide_path = str(getattr(gemini_service, "last_reference_guide_path", "") or "")
        contextual_error = _append_guide_context(str(exc), placeholder_mode=placeholder_mode, guide_path=guide_path)
        logger.error(
            "Mockup job failed (%s): job_id=%s placeholder_mode=%s guide_path=%s",
            type(exc).__name__,
            job_id,
            placeholder_mode,
            guide_path or "<none>",
            exc_info=True,
        )
        _cleanup_partial_outputs(generated_image_path, coordinates_path)
        with _session_scope() as session:
            job = session.get(MockupBaseGenerationJob, job_id)
            if job is not None and not str(job.prompt_text or "").startswith(PROMPT_METADATA_PREFIX):
                job.prompt_text = _serialize_prompt_with_metadata(
                    prompt_text=effective_prompt,
                    placeholder_mode=placeholder_mode,
                    guide_path=guide_path,
                )
                session.commit()
        _set_job_failed(job_id=job_id, error_message=contextual_error, reason=type(exc).__name__)
        return {
            "status": "failed",
            "job_id": job_id,
            "error_type": type(exc).__name__,
            "error": contextual_error,
        }

    except SQLAlchemyError as exc:
        logger.error("Database error while processing mockup job %s", job_id, exc_info=True)
        _cleanup_partial_outputs(generated_image_path, coordinates_path)
        _set_job_failed(job_id=job_id, error_message=str(exc), reason="SQLAlchemyError")
        return {
            "status": "failed",
            "job_id": job_id,
            "error_type": "SQLAlchemyError",
            "error": str(exc),
        }

    except Exception as exc:
        logger.error("Unexpected error while processing mockup job %s", job_id, exc_info=True)
        _cleanup_partial_outputs(generated_image_path, coordinates_path)
        _set_job_failed(job_id=job_id, error_message=str(exc), reason="UnexpectedError")
        return {
            "status": "failed",
            "job_id": job_id,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }


def _studio_variation_prompt(prompt_text: str, variation_index: int) -> str:
    base = str(prompt_text or "").strip()
    if variation_index <= 1:
        return base
    return (
        base
        + "\n\n"
        + f"Produce a clearly distinct composition variation number {variation_index}. "
        + "Keep the same artwork and core room intent, but vary layout, furniture placement, framing context, styling, or camera composition."
    )


def _set_studio_job_failed(job_id: int, message: str) -> None:
    with _session_scope() as session:
        job = session.get(GeminiStudioJob, job_id)
        if job is None:
            return
        job.status = "Failed"
        job.error_message = str(message or "Generation failed")
        job.finished_at = datetime.utcnow()
        session.commit()


def _save_studio_output_png(job_external_id: str, image_bytes: bytes) -> str:
    GEMINI_STUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = GEMINI_STUDIO_OUTPUT_DIR / f"{job_external_id}.png"
    image_obj = Image.open(BytesIO(image_bytes))
    image_obj.load()
    if image_obj.mode not in {"RGB", "RGBA"}:
        image_obj = image_obj.convert("RGB")
    if image_obj.size != (STUDIO_OUTPUT_TARGET_PX, STUDIO_OUTPUT_TARGET_PX):
        logger.info(
            "Resizing studio output %s from %sx%s to %sx%s",
            job_external_id,
            image_obj.width,
            image_obj.height,
            STUDIO_OUTPUT_TARGET_PX,
            STUDIO_OUTPUT_TARGET_PX,
        )
        resampling = getattr(getattr(Image, "Resampling", None), "LANCZOS", 1)
        image_obj = image_obj.resize(
            (STUDIO_OUTPUT_TARGET_PX, STUDIO_OUTPUT_TARGET_PX),
            resample=resampling,
        )
    image_obj.save(output_path, format="PNG")
    return str(output_path)


def _save_ezy_room_output(job_external_id: str, image_bytes: bytes) -> str:
    EZY_ROOM_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = EZY_ROOM_OUTPUT_DIR / f"{job_external_id}-room.jpg"
    image_obj = Image.open(BytesIO(image_bytes))
    image_obj.load()
    if image_obj.mode not in {"RGB", "RGBA"}:
        image_obj = image_obj.convert("RGB")
    if image_obj.mode == "RGBA":
        image_obj = image_obj.convert("RGB")
    image_obj.save(output_path, format="JPEG", quality=95)
    return str(output_path)


def _save_ezy_mask_output(job_external_id: str, mask_image: Image.Image) -> str:
    EZY_MASK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = EZY_MASK_OUTPUT_DIR / f"{job_external_id}-mask.png"
    mask_image.save(output_path, format="PNG")
    return str(output_path)


def _save_ezy_transparent_output(job_external_id: str, room_image_path: str, mask_image: Image.Image) -> str:
    EZY_TRANSPARENT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = EZY_TRANSPARENT_OUTPUT_DIR / f"{job_external_id}-alpha.png"
    room_image = Image.open(room_image_path)
    room_image.load()
    room_rgba = room_image.convert("RGBA")
    alpha_mask = mask_image.convert("L")
    # Ezy template contract: keep room visible while cutting a transparent hole
    # where artwork is composited so downstream swaps align exactly.
    room_alpha = Image.new("L", room_rgba.size, 255)
    room_alpha.paste(0, mask=alpha_mask)
    room_rgba.putalpha(room_alpha)
    room_rgba.save(output_path, format="PNG")
    return str(output_path)


def _default_ezy_pipeline_stage() -> dict[str, str]:
    return {
        "gen": "Pending",
        "detect": "Pending",
        "comp": "Pending",
        "harmonize": "Pending",
    }


def _build_ezy_default_generation_prompt(*, category: str, aspect_ratio: str, variation_index: int) -> str:
    variant = EZY_COMPOSITION_VARIANTS[(max(1, int(variation_index)) - 1) % len(EZY_COMPOSITION_VARIANTS)]
    return (
        "[THINKING_LEVEL: HIGH]\n"
        f"Generate a premium photorealistic {category} interior mockup scene at 1:1 output. "
        f"Include a clearly visible wall frame area intended for an inserted artwork at exact {aspect_ratio.replace('x', ':')} ratio. "
        "Do not place the frame dead center unless physically unavoidable. "
        f"{variant} "
        "Use realistic architecture, believable furniture scale, and coherent lighting. "
        "Avoid abstract textures, horizontal line artifacts, repeated stripe patterns, or glitch-like banding. "
        "No text, no logos, no watermarks, no posterized graphics. "
        "Preserve clean frame edges and keep the entire frame fully visible for precise coordinate detection."
    )


def _set_pipeline_stage(stage_map: dict[str, str], stage_name: str, status: str) -> dict[str, str]:
    if stage_name in stage_map:
        stage_map[stage_name] = status
    return stage_map


def _persist_ezy_pipeline_stage(job_id: int, stage_map: dict[str, str]) -> None:
    with _session_scope() as session:
        job = session.get(EzyMockupJob, job_id)
        if job is None:
            return
        job.pipeline_stage_json = json.dumps(stage_map, separators=(",", ":"))
        session.commit()


def _save_ezy_harmonized_output(job_external_id: str, image_bytes: bytes) -> str:
    EZY_ROOM_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = EZY_ROOM_OUTPUT_DIR / f"{job_external_id}-harmonized.jpg"
    image_obj = Image.open(BytesIO(image_bytes))
    image_obj.load()
    if image_obj.mode not in {"RGB", "RGBA"}:
        image_obj = image_obj.convert("RGB")
    if image_obj.mode == "RGBA":
        image_obj = image_obj.convert("RGB")
    image_obj.save(output_path, format="JPEG", quality=95)
    return str(output_path)


def _build_ezy_quadrilateral_mask(
    room_image_path: str,
    frame_coords: dict[str, list[int]],
    edge_smoothing: bool = False,
) -> Image.Image:
    room_image = Image.open(room_image_path)
    room_image.load()
    width, height = room_image.size

    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    polygon = [
        tuple(frame_coords["tl"]),
        tuple(frame_coords["tr"]),
        tuple(frame_coords["br"]),
        tuple(frame_coords["bl"]),
    ]
    draw.polygon(polygon, fill=255)

    if edge_smoothing:
        mask = mask.filter(ImageFilter.GaussianBlur(radius=1.2))

    return mask


def _ezy_image_size(image_path: str) -> tuple[int, int]:
    room_image = Image.open(image_path)
    room_image.load()
    return room_image.size


def _validate_ezy_composition(
    *,
    frame_coords: dict[str, list[int]],
    image_width: int,
    image_height: int,
) -> tuple[bool, str]:
    tl = frame_coords.get("tl")
    tr = frame_coords.get("tr")
    br = frame_coords.get("br")
    bl = frame_coords.get("bl")
    if not all(isinstance(point, list) and len(point) == 2 for point in (tl, tr, br, bl)):
        return False, "Frame coordinates incomplete for composition validation"

    xs = [int(tl[0]), int(tr[0]), int(br[0]), int(bl[0])]  # type: ignore[index]
    ys = [int(tl[1]), int(tr[1]), int(br[1]), int(bl[1])]  # type: ignore[index]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    frame_w = max(1, max_x - min_x)
    frame_h = max(1, max_y - min_y)
    frame_area_ratio = (frame_w * frame_h) / float(max(1, image_width * image_height))

    frame_cx = (min_x + max_x) / 2.0
    frame_cy = (min_y + max_y) / 2.0
    img_cx = image_width / 2.0
    img_cy = image_height / 2.0

    dx = abs(frame_cx - img_cx) / float(max(1, image_width))
    dy = abs(frame_cy - img_cy) / float(max(1, image_height))
    centered_score = dx + dy

    if frame_area_ratio < 0.05:
        return False, f"Detected frame is too small ({frame_area_ratio:.3f} area ratio)"
    if frame_area_ratio > 0.62:
        return False, f"Detected frame is too dominant ({frame_area_ratio:.3f} area ratio)"
    if centered_score < 0.07:
        return False, "Detected frame is too centered; scene lacks situational composition"

    return True, "OK"


@celery.task(
    bind=True,
    name="mockups.process_gemini_studio_job",
    rate_limit=MOCKUP_GEMINI_TASK_RATE_LIMIT,
)
def process_gemini_studio_job(self: Any, job_id: int) -> dict[str, Any]:
    output_image_path: str | None = None
    gemini_service: GeminiImageService | None = None

    try:
        with _session_scope() as session:
            job = session.get(GeminiStudioJob, job_id)
            if job is None:
                return {"status": "not_found", "job_id": job_id}
            if job.status != "Pending":
                return {"status": "skipped", "job_id": job_id, "message": f"Job in status '{job.status}' cannot be processed"}

            job.status = "Generating"
            job.started_at = job.started_at or datetime.utcnow()
            job.finished_at = None
            job.error_message = None
            session.commit()

            external_job_id = str(job.job_id)
            prompt_text = str(job.prompt_text or "")
            source_image_path = str(job.source_image_path or "")
            aspect_ratio = str(job.aspect_ratio or "1x1")
            category = str(job.category or "uncategorised")
            variation_index = int(job.variation_index or 1)
            batch_id = str(job.batch_id or "")
            total_variations = int(
                session.query(GeminiStudioJob)
                .filter(GeminiStudioJob.batch_id == batch_id)
                .count()
                or 1
            )

        thought_signature_key = f"studio:{batch_id}:{aspect_ratio}"
        reused_thought_signature = _get_thought_signature(thought_signature_key) if variation_index > 1 else ""

        source_path = Path(source_image_path)
        gemini_service = GeminiImageService()
        
        # Determine if we have a valid reference image available
        has_valid_reference = source_path.exists() and gemini_service._supports_reference_guided_editing()

        # Build appropriate prompt based on whether reference is available
        if has_valid_reference:
            effective_prompt = _build_studio_reference_guided_prompt(
                prompt_text,
                aspect_ratio,
                variation_index,
                category,
                total_variations,
                reused_thought_signature,
            )
            logger.info(
                "Studio job %d: Using REFERENCE-GUIDED editing mode "
                "(source_path=%s, variation=%d/%d, category=%s)",
                job_id,
                source_path,
                variation_index,
                total_variations,
                category,
            )
        else:
            effective_prompt = _build_studio_pure_generation_prompt(
                prompt_text,
                aspect_ratio,
                variation_index,
                category,
                total_variations,
                reused_thought_signature,
            )
            if source_path.exists():
                logger.warning(
                    "Studio job %d: Source file exists (%s) but edit_image not supported. "
                    "Using PURE GENERATION mode instead.",
                    job_id,
                    source_path,
                )
            else:
                logger.info(
                    "Studio job %d: No reference source found. Using PURE GENERATION mode "
                    "(variation=%d/%d, category=%s)",
                    job_id,
                    variation_index,
                    total_variations,
                    category,
                )

        # Attempt image generation/editing
        if has_valid_reference:
            try:
                logger.debug("Studio job %d: Attempting reference-guided edit with source (%s)", job_id, source_path)
                image_bytes = gemini_service._call_gemini_edit_image(
                    prompt=effective_prompt,
                    reference_guide_path=source_path,
                )
                logger.info("Studio job %d: Reference-guided edit succeeded", job_id)
            except GeminiGenerationError as edit_exc:
                logger.warning(
                    "Studio job %d: Reference-guided edit failed (%s), falling back to pure generation. Error: %s",
                    job_id,
                    type(edit_exc).__name__,
                    str(edit_exc)[:200],
                )
                # Rebuild prompt for pure generation fallback
                effective_prompt = _build_studio_pure_generation_prompt(
                    prompt_text,
                    aspect_ratio,
                    variation_index,
                    category,
                    total_variations,
                    reused_thought_signature,
                )
                image_bytes = gemini_service._call_gemini_generate_images(
                    prompt=effective_prompt,
                    aspect_ratio=STUDIO_CANVAS_ASPECT_RATIO,
                    thought_signature=reused_thought_signature or None,
                )
                logger.info("Studio job %d: Pure generation fallback succeeded", job_id)
        else:
            logger.debug("Studio job %d: Performing pure generation (no reference available)", job_id)
            image_bytes = gemini_service._call_gemini_generate_images(
                prompt=effective_prompt,
                aspect_ratio=STUDIO_CANVAS_ASPECT_RATIO,
                thought_signature=reused_thought_signature or None,
            )
            logger.info("Studio job %d: Pure generation succeeded", job_id)

        captured_signature = str(getattr(gemini_service, "last_thought_signature", "") or "").strip()
        if variation_index == 1 and captured_signature:
            _set_thought_signature(thought_signature_key, captured_signature)
        elif variation_index > 1 and not reused_thought_signature and captured_signature:
            _set_thought_signature(thought_signature_key, captured_signature)

        output_image_path = _save_studio_output_png(external_job_id, image_bytes)

        verifier_coordinates: dict[str, list[int]] | None = None
        verifier_error = ""
        try:
            verifier_coordinates = gemini_service.extract_frame_coordinates(output_image_path)
            logger.info(
                "Studio job %d: Frame verifier succeeded using %s -> %s",
                job_id,
                getattr(gemini_service, "FRAME_COORDINATE_MODEL", "unknown-model"),
                json.dumps(verifier_coordinates, separators=(",", ":")),
            )
        except Exception as exc:
            verifier_error = str(exc)
            logger.warning(
                "Studio job %d: Frame verifier failed (%s): %s",
                job_id,
                type(exc).__name__,
                verifier_error,
            )

        with _session_scope() as session:
            job = session.get(GeminiStudioJob, job_id)
            if job is None:
                raise RuntimeError(f"Studio job {job_id} disappeared before completion update")
            job.status = "Completed"
            job.output_image_path = output_image_path
            job.frame_coordinates_json = (
                json.dumps(verifier_coordinates, separators=(",", ":")) if verifier_coordinates else None
            )
            job.frame_coordinates_model = str(getattr(gemini_service, "FRAME_COORDINATE_MODEL", "") or "") or None
            job.frame_coordinates_error = verifier_error or None
            job.finished_at = datetime.utcnow()
            session.commit()

        return {
            "status": "completed",
            "job_id": job_id,
            "output_image_path": output_image_path,
        }

    except GeminiRateLimitError as exc:
        retry_count = int(getattr(getattr(self, "request", None), "retries", 0) or 0)
        countdown = _compute_rate_limit_retry_delay(
            job_id=job_id,
            retry_after_seconds=exc.retry_after_seconds,
            retry_count=retry_count,
        )
        try:
            raise self.retry(
                exc=exc,
                countdown=countdown,
                max_retries=MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES,
            )
        except MaxRetriesExceededError:
            _set_studio_job_failed(job_id, str(exc))
            return {"status": "failed", "job_id": job_id, "error": str(exc)}

    except (GeminiGenerationError, GeminiAuthenticationError, GeminiFileSaveError, ValueError, FileNotFoundError) as exc:
        _set_studio_job_failed(job_id, str(exc))
        return {"status": "failed", "job_id": job_id, "error": str(exc)}

    except SQLAlchemyError as exc:
        logger.error("Database error while processing Gemini Studio job %s", job_id, exc_info=True)
        _set_studio_job_failed(job_id, str(exc))
        return {"status": "failed", "job_id": job_id, "error": str(exc)}

    except Exception as exc:
        logger.error("Unexpected error while processing Gemini Studio job %s", job_id, exc_info=True)
        _set_studio_job_failed(job_id, str(exc))
        return {"status": "failed", "job_id": job_id, "error": str(exc)}


def _set_ezy_job_failed(job_id: int, message: str) -> None:
    with _session_scope() as session:
        job = session.get(EzyMockupJob, job_id)
        if job is None:
            return
        pipeline_stage_raw = str(job.pipeline_stage_json or "").strip()
        try:
            stage_map = json.loads(pipeline_stage_raw) if pipeline_stage_raw else _default_ezy_pipeline_stage()
        except Exception:
            stage_map = _default_ezy_pipeline_stage()
        if isinstance(stage_map, dict):
            if stage_map.get("gen") == "Pending":
                stage_map["gen"] = "Failed"
            elif stage_map.get("detect") == "Pending":
                stage_map["detect"] = "Failed"
            elif stage_map.get("comp") == "Pending":
                stage_map["comp"] = "Failed"
            elif stage_map.get("harmonize") == "Pending":
                stage_map["harmonize"] = "Failed"
            job.pipeline_stage_json = json.dumps(stage_map, separators=(",", ":"))
        job.status = "Failed"
        job.error_message = str(message or "Generation failed")
        job.finished_at = datetime.utcnow()
        session.commit()


@celery.task(
    bind=True,
    name="mockups.process_ezy_mockup_job",
    rate_limit=MOCKUP_GEMINI_TASK_RATE_LIMIT,
)
def process_ezy_mockup_job(self: Any, job_id: int) -> dict[str, Any]:
    room_output_path: str | None = None
    mask_output_path: str | None = None
    transparent_output_path: str | None = None
    harmonized_output_path: str | None = None
    pipeline_stage = _default_ezy_pipeline_stage()

    try:
        with _session_scope() as session:
            job = session.get(EzyMockupJob, job_id)
            if job is None:
                return {"status": "not_found", "job_id": job_id}
            if job.status != "Pending":
                return {"status": "skipped", "job_id": job_id, "message": f"Job in status '{job.status}' cannot be processed"}

            job.status = "Generating"
            job.started_at = job.started_at or datetime.utcnow()
            job.finished_at = None
            job.error_message = None
            job.pipeline_stage_json = json.dumps(pipeline_stage, separators=(",", ":"))
            session.commit()

            external_job_id = str(job.job_id)
            prompt_text = str(job.prompt_text or "")
            source_image_path = str(job.source_image_path or "")
            aspect_ratio = str(job.aspect_ratio or "1x1")
            category = str(job.category or "uncategorised")
            variation_index = int(job.variation_index or 1)
            auto_generate_alpha = bool(job.auto_generate_alpha)
            edge_smoothing = bool(job.edge_smoothing)

        source_path = Path(source_image_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Ezy source image missing: {source_path}")

        gemini_service = GeminiImageService()
        gemini_service.IMAGE_GENERATION_MODEL = EZY_ARTIST_MODEL
        gemini_service.FRAME_COORDINATE_MODEL = EZY_VERIFIER_MODEL

        clean_prompt = (
            str(prompt_text).strip()
            or _build_ezy_default_generation_prompt(
                category=category,
                aspect_ratio=aspect_ratio,
                variation_index=variation_index,
            )
        )

        frame_coords: dict[str, list[int]] | None = None
        frame_error = ""
        scene_attempts = max(1, int(EZY_MAX_SCENE_ATTEMPTS))
        working_prompt = clean_prompt

        for scene_attempt in range(1, scene_attempts + 1):
            image_bytes = gemini_service._call_gemini_generate_images(
                prompt=working_prompt,
                aspect_ratio=STUDIO_CANVAS_ASPECT_RATIO,
                raw_prompt=True,
            )
            room_output_path = _save_ezy_room_output(external_job_id, image_bytes)
            _set_pipeline_stage(pipeline_stage, "gen", "OK")
            _persist_ezy_pipeline_stage(job_id, pipeline_stage)

            try:
                candidate_coords = gemini_service.extract_frame_coordinates(
                    room_output_path,
                    aspect_ratio=aspect_ratio,
                    coordinate_mode="absolute",
                )
            except Exception as exc:
                frame_error = str(exc)
                if scene_attempt >= scene_attempts:
                    _set_pipeline_stage(pipeline_stage, "detect", "Failed")
                    _set_pipeline_stage(pipeline_stage, "comp", "Skipped")
                    _set_pipeline_stage(pipeline_stage, "harmonize", "Skipped")
                    _persist_ezy_pipeline_stage(job_id, pipeline_stage)
                    raise
                working_prompt = (
                    f"{clean_prompt}\n\n"
                    "RETRY DIRECTION: Generate a clearly readable interior with a clean wall frame area, "
                    "no abstract stripe textures, and stronger scene realism."
                )
                continue

            width, height = _ezy_image_size(room_output_path)
            composition_ok, composition_reason = _validate_ezy_composition(
                frame_coords=candidate_coords,
                image_width=width,
                image_height=height,
            )
            if not composition_ok:
                frame_error = composition_reason
                if scene_attempt >= scene_attempts:
                    _set_pipeline_stage(pipeline_stage, "detect", "Failed")
                    _set_pipeline_stage(pipeline_stage, "comp", "Skipped")
                    _set_pipeline_stage(pipeline_stage, "harmonize", "Skipped")
                    _persist_ezy_pipeline_stage(job_id, pipeline_stage)
                    raise GeminiGenerationError(composition_reason)
                logger.warning(
                    "Ezy composition gate rejected scene for job %s on attempt %s/%s: %s",
                    job_id,
                    scene_attempt,
                    scene_attempts,
                    composition_reason,
                )
                working_prompt = (
                    f"{clean_prompt}\n\n"
                    "RETRY DIRECTION: Ensure clearly situational composition with the artwork frame offset from center, "
                    "visible room depth, and realistic furniture context."
                )
                continue

            frame_coords = candidate_coords
            _set_pipeline_stage(pipeline_stage, "detect", "OK")
            _persist_ezy_pipeline_stage(job_id, pipeline_stage)
            break

        if frame_coords is None:
            raise GeminiGenerationError("Frame coordinate extraction returned no coordinates")
        if room_output_path is None:
            raise GeminiGenerationError("Room generation did not produce an output path")

        composite_image, placement_mask = gemini_service.composite_artwork_locally(
            room_output_path,
            source_path,
            frame_coords,
        )

        if edge_smoothing:
            placement_mask = placement_mask.filter(ImageFilter.GaussianBlur(radius=1.2))

        composite_rgb = composite_image.convert("RGB")
        composite_rgb.save(room_output_path, format="JPEG", quality=95)

        if auto_generate_alpha:
            mask_output_path = _save_ezy_mask_output(external_job_id, placement_mask)
            transparent_output_path = _save_ezy_transparent_output(
                external_job_id,
                room_output_path,
                placement_mask,
            )
        _set_pipeline_stage(pipeline_stage, "comp", "OK")
        _persist_ezy_pipeline_stage(job_id, pipeline_stage)

        if EZY_ENABLE_HARMONIZE:
            try:
                harmonize_prompt = (
                    "Apply subtle realistic room harmonization only: gentle contact shadow and lighting coherence. "
                    "Do not change geometry, framing, or artwork content."
                )
                harmonize_bytes = gemini_service._call_gemini_generate_images(
                    prompt=harmonize_prompt,
                    aspect_ratio=STUDIO_CANVAS_ASPECT_RATIO,
                )
                harmonized_output_path = _save_ezy_harmonized_output(external_job_id, harmonize_bytes)
                _set_pipeline_stage(pipeline_stage, "harmonize", "OK")
            except Exception as harmonize_exc:
                frame_error = (frame_error + "\n" if frame_error else "") + f"Harmonize skipped: {harmonize_exc}"
                _set_pipeline_stage(pipeline_stage, "harmonize", "Failed")
        else:
            _set_pipeline_stage(pipeline_stage, "harmonize", "Skipped")
        _persist_ezy_pipeline_stage(job_id, pipeline_stage)

        with _session_scope() as session:
            job = session.get(EzyMockupJob, job_id)
            if job is None:
                raise RuntimeError(f"Ezy job {job_id} disappeared before completion update")
            job.status = "Completed"
            job.room_output_path = room_output_path
            job.mask_output_path = mask_output_path
            job.transparent_output_path = transparent_output_path
            job.harmonized_output_path = harmonized_output_path
            job.frame_coordinates_json = (
                json.dumps(frame_coords, separators=(",", ":")) if frame_coords else None
            )
            job.frame_coordinates_model = str(getattr(gemini_service, "FRAME_COORDINATE_MODEL", "") or "") or None
            job.frame_coordinates_error = frame_error or None
            job.pipeline_stage_json = json.dumps(pipeline_stage, separators=(",", ":"))
            job.finished_at = datetime.utcnow()
            session.commit()

        return {
            "status": "completed",
            "job_id": job_id,
            "room_output_path": room_output_path,
            "transparent_output_path": transparent_output_path,
            "pipeline_stage": pipeline_stage,
        }

    except GeminiRateLimitError as exc:
        retry_count = int(getattr(getattr(self, "request", None), "retries", 0) or 0)
        countdown = _compute_rate_limit_retry_delay(
            job_id=job_id,
            retry_after_seconds=exc.retry_after_seconds,
            retry_count=retry_count,
        )
        try:
            raise self.retry(
                exc=exc,
                countdown=countdown,
                max_retries=MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES,
            )
        except MaxRetriesExceededError:
            _set_ezy_job_failed(job_id, str(exc))
            return {"status": "failed", "job_id": job_id, "error": str(exc)}

    except (GeminiGenerationError, GeminiAuthenticationError, GeminiFileSaveError, ValueError, FileNotFoundError) as exc:
        _set_ezy_job_failed(job_id, str(exc))
        return {"status": "failed", "job_id": job_id, "error": str(exc)}

    except SQLAlchemyError as exc:
        logger.error("Database error while processing Ezy Mockup job %s", job_id, exc_info=True)
        _set_ezy_job_failed(job_id, str(exc))
        return {"status": "failed", "job_id": job_id, "error": str(exc)}

    except Exception as exc:
        logger.error("Unexpected error while processing Ezy Mockup job %s", job_id, exc_info=True)
        _set_ezy_job_failed(job_id, str(exc))
        return {"status": "failed", "job_id": job_id, "error": str(exc)}


import application.mockups.tasks_precision_generator  # noqa: F401


__all__ = [
    "celery",
    "queue_mockup_jobs",
    "process_mockup_job",
    "process_gemini_studio_job",
    "process_ezy_mockup_job",
]
