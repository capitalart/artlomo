"""Mockup Base Generation - Gemini Image Generation Service.

Wrapper around the Google Generative AI (Gemini) SDK for generating photorealistic
mockup background images. Handles prompt passing, aspect ratio configuration,
image persistence, and robust error handling.

Critical Design Constraint:
- Aspect ratio is passed ONLY via the Gemini API config parameter
- Aspect ratio TEXT must NOT appear in the prompt itself
- This maintains prompt consistency and ensures correct API handling
"""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Optional, cast

from PIL import Image, ImageDraw, ImageFilter

from dotenv import load_dotenv

try:
    import cv2  # type: ignore
except Exception:
    cv2 = None  # type: ignore

try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore

try:
    import google.genai as genai
    from google import genai as genai_module
    try:
        from google.genai import types
    except (ImportError, AttributeError):
        types = None  # type: ignore
except ImportError:
    genai = None
    genai_module = None
    types = None

from application.mockups.config import MockupBaseGenerationCatalog


logger = logging.getLogger(__name__)
_ARTLOMO_BASE_DIR = Path(os.getenv("ARTLOMO_BASE_DIR") or Path(__file__).resolve().parents[3]).resolve()
_APPLICATION_ROOT = _ARTLOMO_BASE_DIR / "application"
CONTROL_STATE_PATH = _ARTLOMO_BASE_DIR / "var" / "state" / "mockup_generator_control.json"

# Ensure environment variables from the project .env are available in worker contexts
# (e.g., Celery service startup) before client initialization reads os.getenv().
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DOTENV_PATH = _PROJECT_ROOT / ".env"
if _DOTENV_PATH.exists():
    load_dotenv(dotenv_path=_DOTENV_PATH, override=False)
else:
    load_dotenv(override=False)


class GeminiImageServiceException(Exception):
    """Base exception for GeminiImageService errors."""

    pass


class GeminiAuthenticationError(GeminiImageServiceException):
    """Raised when Gemini API authentication fails."""

    pass


class GeminiGenerationError(GeminiImageServiceException):
    """Raised when image generation fails."""

    pass


class GeminiRateLimitError(GeminiGenerationError):
    """Raised when Gemini rejects a request due to rate limits or quota."""

    def __init__(self, message: str, retry_after_seconds: Optional[int] = None):
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


class GeminiFileSaveError(GeminiImageServiceException):
    """Raised when image file cannot be saved."""

    pass


class GeminiImageService:
    """Service for generating mockup background images via Google Gemini."""

    # Base directory for storing generated mockup images
    MOCKUP_BASE_STORAGE_DIR = _APPLICATION_ROOT / "mockups" / "catalog" / "assets" / "mockups" / "bases"

    # Canonical directory for per-aspect cyan placement guides used to steer
    # Gemini's artwork placement during mockup base generation.
    REFERENCE_GUIDE_STORAGE_DIR = Path(
        _APPLICATION_ROOT / "mockups" / "catalog" / "assets" / "mockups" / "reference-guides" / "cyan-placement"
    )

    # Operator-selectable positional placeholders for guide testing.
    POSITIONAL_REFERENCE_GUIDE_STORAGE_DIR = Path(
        _APPLICATION_ROOT / "mockups" / "catalog" / "assets" / "mockups" / "reference-guides" / "positional-placement"
    )

    # Raw uploaded tester directory retained as an additional fallback source.
    POSITIONAL_REFERENCE_GUIDE_SOURCE_DIR = Path(
        _APPLICATION_ROOT / "mockups" / "mockup-preview-tests"
    )

    # Legacy source directory retained as a fallback during migration.
    LEGACY_REFERENCE_GUIDE_STORAGE_DIR = Path(
        _APPLICATION_ROOT / "mockups" / "catalog" / "assets" / "mockups" / "cyan-art-bases"
    )

    # Gemini 3 image preview defaults for higher-fidelity mockup scene reasoning.
    IMAGE_GENERATION_MODEL = os.getenv("MOCKUP_IMAGE_GENERATION_MODEL", "gemini-3.1-flash-image-preview")

    # Ordered fallback candidates when the configured generation model is unavailable.
    # March 2026: Using current stable Gemini 3/3.1 series (2.0 series deprecated June 2025)
    DEFAULT_IMAGE_GENERATION_MODEL_FALLBACKS = (
        "gemini-3-pro-image-preview",
        "imagen-3.0-generate-002",
        "gemini-2.5-flash-image-preview",
    )

    # Higher-fidelity edit/inpainting model for guide-backed mockup composition.
    IMAGE_EDIT_MODEL = os.getenv("MOCKUP_IMAGE_EDIT_MODEL", "gemini-3-pro-image-preview")

    # Ordered fallback candidates when the configured edit model is unavailable.
    DEFAULT_IMAGE_EDIT_MODEL_FALLBACKS = (
        "gemini-3-pro-image-preview",
        "gemini-2.5-flash-image-preview",
    )

    # Vision verifier model used to read final generated mockups and extract frame coordinates.
    FRAME_COORDINATE_MODEL = os.getenv("MOCKUP_FRAME_COORDINATE_MODEL", "gemini-2.5-pro")

    # Ordered fallback candidates when the configured frame verifier model is unavailable.
    DEFAULT_FRAME_COORDINATE_MODEL_FALLBACKS = (
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-1.5-pro",
    )

    # Native output target for generated mockup bases (professional print labs expect 2K+).
    NATIVE_IMAGE_SIZE = os.getenv("MOCKUP_IMAGE_SIZE", "2K")

    # March 2026 chromakey automation contract: generation canvas is fixed to 1:1.
    FORCE_GENERATION_ASPECT_RATIO = os.getenv("MOCKUP_IMAGE_FORCE_ASPECT_RATIO", "1:1")

    # Gemini 3 reasoning control for image generation calls (HIGH for spatial/geometric reasoning).
    THINKING_LEVEL = os.getenv("MOCKUP_IMAGE_THINKING_LEVEL", "HIGH").strip().upper()

    # Hard-edge mask directive for chromakey generation stability.
    HARD_EDGE_PROMPT_PREFIX = (
        "[THINKING_LEVEL: HIGH] Generate a photorealistic 1:1 interior. "
        "Use the attached Outlined Artwork Placeholder as the central asset on the wall. "
        "CRITICAL TECHNICAL CONSTRAINT: Maintain the High-Contrast Border System (Black-Cyan-Black) exactly as shown in the reference. "
        "Do not allow these lines to blend; they must remain distinct, aliased, and geometric. "
        "The cyan must remain a flat, non-emissive technical marker with no cyan glow, no light-spill, and no reflected tint."
    )

    # Master system instruction: permanently treats artwork as immutable geometric asset.
    # This ensures the model spends reasoning cycles on room composition, not artwork distortion.
    SYSTEM_INSTRUCTION_FOR_MOCKUP_COMPOSITION = (
        "You are a professional interior photography AI specialized in product placement mockups. "
        "When the user provides an uploaded artwork asset (e.g., a 4:5 vertical portrait), you MUST treat "
        "its internal aspect ratio as immutable. Never stretch, warp, crop, or occlude the artwork subject. "
        "Your task is to generate a photorealistic room around this asset at the requested output aspect ratio. "
        "If the final output is 1:1 square, expand the field of view (room scene) horizontally to fill the "
        "left and right margins while keeping the artwork perfectly centered, undistorted, and fully visible. "
        "Use professional interior photography composition: wide-angle 24mm equivalent framing, three-quarter "
        "camera angle, realistic depth, soft natural lighting. The artwork must remain the hero; the room is the stage."
    )

    # System instructions disabled as of March 2026 for improved prompt flexibility

    # Timeout for API calls (seconds)
    API_TIMEOUT_SECONDS = 60

    # Supported aspect ratios for Imagen generate_images endpoint.
    GEMINI_SUPPORTED_ASPECT_RATIOS = ("1:1", "9:16", "16:9", "4:3", "3:4")

    RETRY_DELAY_PATTERNS = (
        re.compile(r"retryDelay['\"]?\s*[:=]\s*['\"]?(?P<seconds>\d+(?:\.\d+)?)s", re.IGNORECASE),
        re.compile(r"Please retry in\s+(?P<seconds>\d+(?:\.\d+)?)s", re.IGNORECASE),
    )

    def __init__(self, api_key: Optional[str] = None):
        """Initialize GeminiImageService with API credentials.

        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY environment variable.

        Raises:
            GeminiAuthenticationError: If API key is not provided and not in environment
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.use_vertexai = self._is_vertexai_enabled()
        self.require_reference_guide = self._is_reference_guide_required()
        self.strict_reference_guide = self._is_reference_guide_strict()
        self.last_placeholder_mode = "cyan"
        self.last_reference_guide_path = ""
        self.last_thought_signature = ""

        if not self.use_vertexai and not self.api_key:
            raise GeminiAuthenticationError(
                "Gemini credentials not configured. Set GEMINI_API_KEY or GOOGLE_API_KEY, "
                "or enable Vertex AI with GOOGLE_GENAI_USE_VERTEXAI plus project/location settings."
            )

        if genai is None:
            raise GeminiAuthenticationError(
                "google-genai library not installed. Install with: pip install google-generativeai"
            )

        try:
            self.client = self._build_client()
            logger.info(
                "Gemini client initialized successfully (vertexai=%s, generation_model=%s)",
                self.use_vertexai,
                self.IMAGE_GENERATION_MODEL,
            )
        except Exception as e:
            raise GeminiAuthenticationError(f"Failed to initialize Gemini client: {str(e)}") from e

    def generate_image(
        self,
        prompt: str,
        aspect_ratio: str,
        category: str,
        variation_index: int,
        generation_aspect_ratio: Optional[str] = None,
        reference_guide_override: Optional[Path | str] = None,
        placeholder_mode_override: Optional[str] = None,
        thought_signature_override: Optional[str] = None,
    ) -> str:
        """Generate a mockup background image using Gemini.

        This method:
        1. Validates the aspect ratio against known configurations
        2. Calls Gemini image generation API with prompt and aspect ratio config
        3. Saves the generated image to a category-specific directory
        4. Returns the file path to the saved image

        Critical: The aspect_ratio is passed ONLY via the Gemini API config parameter,
        NOT in the prompt text. This ensures prompt consistency.

        Args:
            prompt: Text prompt describing the desired image (e.g., from MockupPromptService)
            aspect_ratio: Aspect ratio string (e.g., '16x9', '1x1') - must be in ASPECT_RATIOS
            category: Category of the mockup (e.g., 'living-room', 'cafe')
            variation_index: Variation index (1-20) for tracking and organization

        Returns:
            Absolute file path to the saved image as a string

        Raises:
            ValueError: If aspect_ratio or category are invalid
            GeminiGenerationError: If image generation fails
            GeminiFileSaveError: If image cannot be saved to disk
        """
        # Validate inputs
        if aspect_ratio not in MockupBaseGenerationCatalog.ASPECT_RATIOS:
            raise ValueError(
                f"Invalid aspect_ratio '{aspect_ratio}'. Must be one of: "
                f"{', '.join(MockupBaseGenerationCatalog.ASPECT_RATIOS)}"
            )

        canvas_aspect_ratio = generation_aspect_ratio or aspect_ratio
        if canvas_aspect_ratio not in MockupBaseGenerationCatalog.ASPECT_RATIOS:
            raise ValueError(
                f"Invalid generation_aspect_ratio '{canvas_aspect_ratio}'. Must be one of: "
                f"{', '.join(MockupBaseGenerationCatalog.ASPECT_RATIOS)}"
            )

        if category not in MockupBaseGenerationCatalog.CATEGORIES:
            raise ValueError(
                f"Invalid category '{category}'. Must be one of: "
                f"{', '.join(MockupBaseGenerationCatalog.CATEGORIES)}"
            )

        if not (1 <= variation_index <= 20):
            raise ValueError(f"variation_index must be 1-20, got {variation_index}")

        logger.info(
            f"Starting image generation: category={category}, "
            f"placeholder_aspect={aspect_ratio}, canvas_aspect={canvas_aspect_ratio}, "
            f"variation={variation_index}"
        )

        try:
            placeholder_mode = str(placeholder_mode_override or self._load_placeholder_mode() or "cyan")
            reference_guide_path = (
                Path(reference_guide_override)
                if reference_guide_override is not None
                else self._resolve_reference_guide_path(aspect_ratio)
            )
            self.last_placeholder_mode = placeholder_mode
            self.last_reference_guide_path = str(reference_guide_path or "")

            if reference_guide_path is not None and not reference_guide_path.exists():
                raise FileNotFoundError(f"Reference guide not found: {reference_guide_path}")

            if reference_guide_path is None and self.require_reference_guide:
                raise GeminiGenerationError(
                    "No reference guide found for aspect_ratio="
                    f"{aspect_ratio} in placeholder_mode={placeholder_mode}. Expected a guide image in "
                    f"{self.POSITIONAL_REFERENCE_GUIDE_STORAGE_DIR} or {self.REFERENCE_GUIDE_STORAGE_DIR}."
                )

            if reference_guide_path is None:
                image_bytes = self._call_gemini_generate_images(
                    prompt=prompt,
                    aspect_ratio=canvas_aspect_ratio,
                    thought_signature=thought_signature_override,
                )
            elif not self._supports_reference_guided_editing():
                allow_text_fallback = (
                    placeholder_mode in {"outlined", "artwork_trojan", "artwork_only_composite"}
                    or not self.strict_reference_guide
                )
                if not allow_text_fallback:
                    raise GeminiGenerationError(
                        "Reference guide generation is required, but reference-guided edit_image "
                        f"is unavailable for placeholder_mode={placeholder_mode}. Enable a Gemini client "
                        "that supports edit_image, typically Vertex AI "
                        "(GOOGLE_GENAI_USE_VERTEXAI=true with project/location settings)."
                    )

                logger.warning(
                    "Reference-guided editing unavailable for placeholder_mode=%s; falling back to generate_images.",
                    placeholder_mode,
                )
                image_bytes = self._call_gemini_generate_images(
                    prompt=prompt,
                    aspect_ratio=canvas_aspect_ratio,
                    thought_signature=thought_signature_override,
                )
            else:
                logger.info(
                    "Using %s placement guide for aspect_ratio=%s: %s",
                    placeholder_mode,
                    aspect_ratio,
                    reference_guide_path,
                )
                try:
                    image_bytes = self._call_gemini_edit_image(
                        prompt=prompt,
                        reference_guide_path=reference_guide_path,
                    )
                except GeminiGenerationError as exc:
                    unavailable_edit_models = "No edit_image-compatible model is available" in str(exc)
                    if placeholder_mode in {"outlined", "artwork_trojan", "artwork_only_composite"}:
                        logger.warning(
                            "Reference-guided generation failed for placeholder_mode=%s; falling back to generate_images.",
                            placeholder_mode,
                        )
                        image_bytes = self._call_gemini_generate_images(
                            prompt=prompt,
                            aspect_ratio=canvas_aspect_ratio,
                            thought_signature=thought_signature_override,
                        )
                    elif unavailable_edit_models:
                        logger.warning(
                            "Reference-guided generation unavailable for placeholder_mode=%s because edit models are inaccessible; falling back to generate_images.",
                            placeholder_mode,
                        )
                        image_bytes = self._call_gemini_generate_images(
                            prompt=prompt,
                            aspect_ratio=canvas_aspect_ratio,
                            thought_signature=thought_signature_override,
                        )
                    else:
                        raise GeminiGenerationError(
                            "Reference-guided generation failed and text-only fallback is disabled. "
                            f"placeholder_mode={placeholder_mode} aspect_ratio={aspect_ratio}."
                        ) from exc

            logger.debug(f"Image generated successfully, size: {len(image_bytes)} bytes")

            # Save the image to disk
            file_path = self._save_image_to_disk(
                image_bytes=image_bytes,
                category=category,
                aspect_ratio=aspect_ratio,
                variation_index=variation_index,
            )
            logger.info(f"Image saved to: {file_path}")

            return str(file_path)

        except GeminiGenerationError:
            raise
        except GeminiFileSaveError:
            raise
        except Exception as e:
            msg = f"Unexpected error during image generation: {str(e)}"
            logger.error(msg, exc_info=True)
            raise GeminiGenerationError(msg) from e

    def _call_gemini_generate_images(
        self,
        prompt: str,
        aspect_ratio: str,
        thought_signature: Optional[str] = None,
        system_instruction: Optional[str] = None,
        raw_prompt: bool = False,
    ) -> bytes:
        """Call the Gemini image generation API with high-fidelity spatial reasoning.

        Args:
            prompt: Text prompt (does NOT include aspect ratio)
            aspect_ratio: Aspect ratio (e.g., '16x9') for API config
            thought_signature: Optional thought signature for consistency guardrails
            system_instruction: Optional system instruction for spatial reasoning guidance
                (defaults to SYSTEM_INSTRUCTION_FOR_CREATIVE_COMPOSITION when generating from reference)
            raw_prompt: When True, sends the prompt directly without prepending the reference-guide
                boilerplate (HARD_EDGE_PROMPT_PREFIX / SYSTEM_INSTRUCTION). Use for Ezy pipeline
                scene generation where there is no attached reference image.

        Returns:
            Image bytes from the API response

        Raises:
            GeminiGenerationError: If the API call fails
        """
        # Convert aspect_ratio string to a format recognized by Gemini API
        requested_aspect_ratio = aspect_ratio.replace("x", ":")
        forced_aspect_ratio = str(self.FORCE_GENERATION_ASPECT_RATIO or "").strip()
        if forced_aspect_ratio:
            requested_aspect_ratio = forced_aspect_ratio.replace("x", ":")
        gemini_aspect_ratio = self._resolve_supported_generation_aspect_ratio(requested_aspect_ratio)

        if gemini_aspect_ratio != requested_aspect_ratio:
            logger.warning(
                "Aspect ratio %s is not directly supported by Gemini generate_images; "
                "using nearest supported ratio %s",
                requested_aspect_ratio,
                gemini_aspect_ratio,
            )

        logger.debug(
            "Calling Gemini with aspect_ratio=%s and image_size=%s and thinking_level=%s",
            gemini_aspect_ratio,
            self.NATIVE_IMAGE_SIZE,
            self.THINKING_LEVEL,
        )

        effective_prompt = (
            str(prompt).strip()
            if raw_prompt
            else self._build_generation_prompt(prompt, gemini_aspect_ratio)
        )
        model_candidates = self._generation_model_candidates()
        last_exception: Exception | None = None

        for model_name in model_candidates:
            try:
                response = self._generate_images_with_model(
                    model_name=model_name,
                    effective_prompt=effective_prompt,
                    gemini_aspect_ratio=gemini_aspect_ratio,
                    thought_signature=thought_signature,
                    system_instruction=system_instruction,
                )
                self.last_thought_signature = self._extract_thought_signature(response)
                return self._extract_generated_image_bytes(response)
            except Exception as e:
                last_exception = e
                if self._is_unavailable_model_error(e) and model_name != model_candidates[-1]:
                    logger.warning(
                        "Model %s unavailable (404/access). Retrying with fallback model.",
                        model_name,
                    )
                    continue
                raise self._map_generation_exception(e)

        if last_exception is not None:
            raise self._map_generation_exception(last_exception)
        raise GeminiGenerationError("Gemini API call failed: no generation model candidates available")

    def _generation_model_candidates(self) -> list[str]:
        configured = str(self.IMAGE_GENERATION_MODEL or "").strip()
        env_fallbacks = str(os.getenv("MOCKUP_IMAGE_GENERATION_MODEL_FALLBACKS") or "").strip()
        parsed_env = [item.strip() for item in env_fallbacks.split(",") if item.strip()]
        defaults = list(self.DEFAULT_IMAGE_GENERATION_MODEL_FALLBACKS)

        ordered: list[str] = []
        for candidate in [configured, *parsed_env, *defaults]:
            if not candidate:
                continue
            if candidate not in ordered:
                ordered.append(candidate)
        return ordered

    def _edit_model_candidates(self) -> list[str]:
        configured = str(self.IMAGE_EDIT_MODEL or "").strip()
        env_fallbacks = str(os.getenv("MOCKUP_IMAGE_EDIT_MODEL_FALLBACKS") or "").strip()
        parsed_env = [item.strip() for item in env_fallbacks.split(",") if item.strip()]
        defaults = list(self.DEFAULT_IMAGE_EDIT_MODEL_FALLBACKS)

        ordered: list[str] = []
        for candidate in [configured, *parsed_env, *defaults]:
            if not candidate:
                continue
            if candidate not in ordered:
                ordered.append(candidate)
        return ordered

    def _frame_coordinate_model_candidates(self) -> list[str]:
        configured = str(self.FRAME_COORDINATE_MODEL or "").strip()
        env_fallbacks = str(os.getenv("MOCKUP_FRAME_COORDINATE_MODEL_FALLBACKS") or "").strip()
        parsed_env = [item.strip() for item in env_fallbacks.split(",") if item.strip()]
        defaults = list(self.DEFAULT_FRAME_COORDINATE_MODEL_FALLBACKS)

        ordered: list[str] = []
        for candidate in [configured, *parsed_env, *defaults]:
            if not candidate:
                continue
            if candidate not in ordered:
                ordered.append(candidate)
        return ordered

    def _generate_images_with_model(
        self,
        *,
        model_name: str,
        effective_prompt: str,
        gemini_aspect_ratio: str,
        thought_signature: Optional[str],
        system_instruction: Optional[str] = None,
    ) -> Any:
        base_config: dict[str, Any] = {
            "aspect_ratio": gemini_aspect_ratio,
            "image_size": self.NATIVE_IMAGE_SIZE,
            "number_of_images": 1,
        }
        if thought_signature:
            base_config["thought_signature"] = str(thought_signature).strip()

        thinking_config = self._build_thinking_config()
        if thinking_config is not None:
            base_config["thinking_config"] = thinking_config
        elif self.THINKING_LEVEL:
            base_config["thinking_level"] = str(self.THINKING_LEVEL).upper()

        try:
            return self._invoke_generate_images(
                model_name=model_name,
                effective_prompt=effective_prompt,
                config_kwargs=base_config,
                system_instruction=system_instruction,
            )
        except Exception as e:
            if "thinking" in str(e).lower() and self.THINKING_LEVEL:
                logger.warning(
                    "Endpoint rejected thinking_level=%s for model=%s; retrying without thinking_level",
                    self.THINKING_LEVEL,
                    model_name,
                )
                retry_config = {
                    "aspect_ratio": gemini_aspect_ratio,
                    "image_size": self.NATIVE_IMAGE_SIZE,
                    "number_of_images": 1,
                }
                if thought_signature:
                    retry_config["thought_signature"] = str(thought_signature).strip()
                try:
                    return self._invoke_generate_images(
                        model_name=model_name,
                        effective_prompt=effective_prompt,
                        config_kwargs=retry_config,
                        system_instruction=system_instruction,
                    )
                except Exception as retry_exc:
                    e = retry_exc

            if "thought_signature" in str(e).lower() and thought_signature:
                logger.warning(
                    "Endpoint rejected thought_signature; retrying without thought_signature for model=%s",
                    model_name,
                )
                retry_no_signature: dict[str, Any] = {
                    "aspect_ratio": gemini_aspect_ratio,
                    "image_size": self.NATIVE_IMAGE_SIZE,
                    "number_of_images": 1,
                }
                if thinking_config is not None:
                    retry_no_signature["thinking_config"] = thinking_config
                elif self.THINKING_LEVEL:
                    retry_no_signature["thinking_level"] = str(self.THINKING_LEVEL).upper()
                return self._invoke_generate_images(
                    model_name=model_name,
                    effective_prompt=effective_prompt,
                    config_kwargs=retry_no_signature,
                    system_instruction=system_instruction,
                )

            raise e

    def _invoke_generate_images(
        self,
        *,
        model_name: str,
        effective_prompt: str,
        config_kwargs: dict[str, Any],
        system_instruction: Optional[str] = None,
    ) -> Any:
        """Invoke the Gemini generate_images API with optional system instruction.
        
        Args:
            model_name: The model ID to use
            effective_prompt: The text prompt for image generation
            config_kwargs: Configuration parameters (aspect_ratio, image_size, etc.)
            system_instruction: Optional system instruction to anchor spatial reasoning
        
        Returns:
            API response object
        """
        api_kwargs: dict[str, Any] = {
            "model": model_name,
            "prompt": effective_prompt,
            "config": config_kwargs,
        }
        
        # Include system_instruction if provided (requires google.genai 0.5.0+)
        if system_instruction:
            api_kwargs["system_instruction"] = system_instruction
            logger.debug(
                "Using system_instruction for model=%s (length=%d chars)",
                model_name,
                len(system_instruction),
            )
        
        if types is not None:
            try:
                return self.client.models.generate_images(**api_kwargs)  # type: ignore[arg-type]
            except (AttributeError, TypeError) as e:
                # Fallback if GenerateImagesConfig doesn't support system_instruction
                if system_instruction and "system_instruction" in str(e):
                    logger.warning(
                        "Model %s does not support system_instruction parameter. Retrying without it.",
                        model_name,
                    )
                    api_kwargs.pop("system_instruction", None)
                    return self.client.models.generate_images(**api_kwargs)  # type: ignore[arg-type]
                raise

        return self.client.models.generate_images(**api_kwargs)  # type: ignore[arg-type]

    def _is_unavailable_model_error(self, exc: Exception) -> bool:
        text = str(exc)
        lowered = text.lower()
        return (
            "404" in lowered
            and (
                "not_found" in lowered
                or "was not found" in lowered
                or "does not have access" in lowered
                or "publisher model" in lowered
            )
        )

    def _map_generation_exception(self, e: Exception) -> GeminiImageServiceException:
        error_type = type(e).__name__
        if "UNAUTHENTICATED" in str(e) or "authentication" in str(e).lower():
            msg = f"Gemini API authentication failed: {str(e)}"
            logger.error(msg)
            return GeminiAuthenticationError(msg)
        if "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
            retry_after_seconds = self._extract_retry_after_seconds(str(e))
            retry_suffix = (
                f" Retry after approximately {retry_after_seconds}s."
                if retry_after_seconds is not None
                else ""
            )
            msg = f"Gemini API quota exceeded.{retry_suffix} {str(e)}".strip()
            logger.error(msg)
            return GeminiRateLimitError(msg, retry_after_seconds=retry_after_seconds)
        if "DEADLINE_EXCEEDED" in str(e) or "timeout" in str(e).lower():
            msg = f"Gemini API call timed out after {self.API_TIMEOUT_SECONDS}s: {str(e)}"
            logger.error(msg)
            return GeminiGenerationError(msg)
        msg = f"Gemini API call failed ({error_type}): {str(e)}"
        logger.error(msg, exc_info=True)
        return GeminiGenerationError(msg)

    def _resolve_supported_generation_aspect_ratio(self, requested_aspect_ratio: str) -> str:
        """Map requested aspect ratio to one supported by Gemini generate_images."""
        if requested_aspect_ratio in self.GEMINI_SUPPORTED_ASPECT_RATIOS:
            return requested_aspect_ratio

        try:
            requested_width, requested_height = requested_aspect_ratio.split(":", 1)
            requested_ratio_value = float(requested_width) / float(requested_height)
        except (ValueError, ZeroDivisionError):
            return "1:1"

        def _ratio_value(aspect: str) -> float:
            width, height = aspect.split(":", 1)
            return float(width) / float(height)

        return min(
            self.GEMINI_SUPPORTED_ASPECT_RATIOS,
            key=lambda aspect: abs(_ratio_value(aspect) - requested_ratio_value),
        )

    def _call_gemini_edit_image(
        self,
        prompt: str,
        reference_guide_path: Path,
        system_instruction: Optional[str] = None,
    ) -> bytes:
        """Call Gemini's reference-guided edit endpoint for professional inpainting.
        
        Uses cyan placement guides as spatial control references, ensuring artwork remains
        immutable while the surrounding scene is regenerated with professional composition.
        
        Args:
            prompt: Text prompt for inpainting
            reference_guide_path: Path to reference/guide image
            system_instruction: Optional system instruction for spatial reasoning
        
        Returns:
            Image bytes from the API response
        
        Raises:
            GeminiGenerationError: If the API call fails
        """
        if not self._supports_reference_guided_editing():
            raise GeminiGenerationError(
                "Reference-guided generation requires a Vertex AI Gemini client with edit_image support"
            )

        if types is None:
            raise GeminiGenerationError(
                "Reference-guided generation requires google.genai.types support"
            )

        try:
            guide_image = types.Image.from_file(location=str(reference_guide_path))
            control_reference = types.ControlReferenceImage(
                reference_id=1,
                reference_image=guide_image,
                config=types.ControlReferenceConfig(
                    control_type=types.ControlReferenceType.CONTROL_TYPE_SCRIBBLE,
                    enable_control_image_computation=True,
                ),
            )
            edit_config = types.EditImageConfig(
                edit_mode=types.EditMode.EDIT_MODE_CONTROLLED_EDITING,
                number_of_images=1,
                output_mime_type="image/png",
            )

            reference_images = cast(list[Any], [control_reference])
            # Build refined prompt for guide-backed inpainting with immutable asset rules
            effective_prompt = self._build_inpaint_prompt(prompt, reference_guide_path=reference_guide_path)
            
            model_candidates = self._edit_model_candidates()
            last_exception: Exception | None = None

            for model_name in model_candidates:
                api_kwargs: dict[str, Any] = {
                    "model": model_name,
                    "prompt": effective_prompt,
                    "reference_images": reference_images,
                    "config": edit_config,
                }

                # Include system_instruction if provided
                if system_instruction:
                    api_kwargs["system_instruction"] = system_instruction
                    logger.debug(
                        "Using system_instruction for edit_image model=%s (length=%d chars)",
                        model_name,
                        len(system_instruction),
                    )

                try:
                    response = self.client.models.edit_image(**api_kwargs)
                    return self._extract_generated_image_bytes(response)
                except Exception as e:
                    last_exception = e
                    if self._is_unavailable_model_error(e) and model_name != model_candidates[-1]:
                        logger.warning(
                            "Edit model %s unavailable (404/access). Retrying with fallback model.",
                            model_name,
                        )
                        continue
                    if self._is_unavailable_model_error(e):
                        raise GeminiGenerationError(
                            "No edit_image-compatible model is available for this Vertex project. "
                            "Configure MOCKUP_IMAGE_EDIT_MODEL / MOCKUP_IMAGE_EDIT_MODEL_FALLBACKS with "
                            "models your project can access."
                        ) from e
                    raise

            if last_exception is not None:
                raise last_exception
            raise GeminiGenerationError("Gemini edit_image call failed: no edit model candidates available")

        except GeminiGenerationError:
            raise
        except Exception as e:
            error_type = type(e).__name__
            details = str(e)
            if "RESOURCE_EXHAUSTED" in details or "quota" in details.lower():
                retry_after_seconds = self._extract_retry_after_seconds(details)
                retry_suffix = (
                    f" Retry after approximately {retry_after_seconds}s."
                    if retry_after_seconds is not None
                    else ""
                )
                msg = f"Gemini edit_image quota exceeded.{retry_suffix} {details}".strip()
                logger.error(msg)
                raise GeminiRateLimitError(msg, retry_after_seconds=retry_after_seconds) from e

            msg = f"Gemini edit_image call failed ({error_type}): {details}"
            logger.error(msg, exc_info=True)
            raise GeminiGenerationError(msg) from e

    def _extract_retry_after_seconds(self, error_text: str) -> Optional[int]:
        """Extract a suggested retry delay from Gemini error text when available."""
        for pattern in self.RETRY_DELAY_PATTERNS:
            match = pattern.search(error_text)
            if not match:
                continue

            try:
                seconds = float(match.group("seconds"))
            except (TypeError, ValueError):
                continue

            if seconds > 0:
                rounded = int(seconds)
                return rounded if float(rounded) == seconds else rounded + 1

        return None

    def _build_thinking_config(self) -> Any | None:
        """Build typed ThinkingConfig for Gemini 3.1 when supported by SDK."""
        if not self.THINKING_LEVEL or types is None:
            return None

        thinking_config_cls = getattr(types, "ThinkingConfig", None)
        if thinking_config_cls is None:
            return None

        level_value: Any = self.THINKING_LEVEL
        thinking_level_cls = getattr(types, "ThinkingLevel", None)
        if thinking_level_cls is not None:
            normalized = str(self.THINKING_LEVEL).strip().upper()
            level_value = (
                getattr(thinking_level_cls, normalized, None)
                or getattr(thinking_level_cls, f"THINKING_LEVEL_{normalized}", None)
                or normalized
            )

        try:
            return thinking_config_cls(thinking_level=level_value)
        except Exception:
            return None

    def _build_client(self):
        """Create the appropriate Gemini client for the configured backend."""
        if genai is None:
            raise GeminiAuthenticationError("google-genai library is not available")

        if self.use_vertexai:
            project = os.getenv("GOOGLE_CLOUD_PROJECT") or "ezy-empire"
            location = os.getenv("GOOGLE_CLOUD_LOCATION") or "us-central1"
            if not project:
                raise GeminiAuthenticationError(
                    "GOOGLE_CLOUD_PROJECT must be set when GOOGLE_GENAI_USE_VERTEXAI is enabled"
                )
            return genai.Client(
                vertexai=True,
                project=project,
                location=location,
            )

        return genai.Client(api_key=self.api_key)

    def _is_vertexai_enabled(self) -> bool:
        """Return True when the service should use Vertex AI instead of API-key mode."""
        raw_value = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "")
        return raw_value.strip().lower() in {"1", "true", "yes", "on"}

    def _build_generation_prompt(self, user_prompt: str, target_aspect_ratio: str) -> str:
        """Build a high-fidelity generation prompt with camera/perspective/preservation guidance.
        
        Architecture: System Instruction → Camera Framing → Perspective Geometry → User Prompt
        """
        cleaned_user = str(user_prompt or "").strip()
        if not cleaned_user:
            cleaned_user = "Interior room mockup with a framed artwork"
        
        # Inject camera/perspective guidance that works WITH the immutable artwork rule
        guidance = (
            "CAMERA: 24mm wide-angle equivalent lens, three-quarter view angle, realistic depth. "
            "PRESERVE: The uploaded artwork subject must NOT be distorted, stretched, or warped. "
            "COMPOSITION: Artwork is centered and fully visible; room expands to fill output aspect ratio. "
        )

        return (
            f"{self.HARD_EDGE_PROMPT_PREFIX}\n\n"
            f"{self.SYSTEM_INSTRUCTION_FOR_MOCKUP_COMPOSITION}\n\n"
            f"{guidance}\n\n"
            f"{cleaned_user}"
        )

    def _build_inpaint_prompt(self, user_prompt: str, reference_guide_path: Optional[Path] = None) -> str:
        """Build the inpaint prompt, using a clean pass for artwork-placeholder references."""
        cleaned_user = str(user_prompt or "").strip()
        if not cleaned_user:
            cleaned_user = "Generate interior room around the placed artwork"

        reference_name = str(reference_guide_path.name if reference_guide_path else "").lower()
        if "artwork-placeholder" in reference_name:
            return (
                f"{self.SYSTEM_INSTRUCTION_FOR_MOCKUP_COMPOSITION}\n\n"
                f"{cleaned_user}"
            )

        return (
            f"{self.HARD_EDGE_PROMPT_PREFIX}\n\n"
            f"{self.SYSTEM_INSTRUCTION_FOR_MOCKUP_COMPOSITION}\n\n"
            f"{cleaned_user}"
        )

    def extract_frame_coordinates(
        self,
        image_path: str | Path,
        *,
        aspect_ratio: Optional[str] = None,
        coordinate_mode: str = "absolute",
    ) -> dict[str, list[int]]:
        """Use a vision-capable Gemini model to extract inner frame corners from a mockup image."""
        if types is None:
            raise GeminiGenerationError("Gemini coordinate extraction requires google.genai.types support")

        target_path = Path(image_path)
        if not target_path.exists():
            raise FileNotFoundError(f"Generated mockup not found for coordinate extraction: {target_path}")

        image_obj = Image.open(target_path)
        image_obj.load()
        mime_type = "image/png"
        if image_obj.format and str(image_obj.format).upper() in {"JPEG", "JPG"}:
            mime_type = "image/jpeg"
        elif image_obj.format and str(image_obj.format).upper() == "WEBP":
            mime_type = "image/webp"

        with open(target_path, "rb") as handle:
            image_bytes = handle.read()

        mode = str(coordinate_mode or "absolute").strip().lower()
        if mode not in {"absolute", "normalized"}:
            mode = "absolute"

        if mode == "normalized":
            coordinate_instruction = (
                "Return normalized coordinates in the range 0..1000 where (0,0) is top-left and (1000,1000) is bottom-right."
            )
        else:
            coordinate_instruction = (
                "Return absolute pixel coordinates for this image in its native resolution. "
                "For a 2048 output, expected values are approximately in the range 0..2048."
            )

        aspect_hint = str(aspect_ratio or "").strip()
        aspect_line = (
            f"The target placeholder aspect ratio label is {aspect_hint.replace('x', ':')}. "
            if aspect_hint
            else ""
        )

        verifier_prompt = (
            "Analyze this generated mockup image. Locate the four INNER corners of the white placeholder/frame area. "
            f"{aspect_line}"
            f"{coordinate_instruction} "
            "Return ONLY valid JSON with this exact shape: "
            '{"tl": [x, y], "tr": [x, y], "br": [x, y], "bl": [x, y]}.'
        )

        contents = cast(list[Any], [
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            types.Part.from_text(text=verifier_prompt),
        ])

        request_config = types.GenerateContentConfig(
            response_mime_type="application/json",  # type: ignore[call-arg]
        )

        response: Any | None = None
        model_candidates = self._frame_coordinate_model_candidates()
        last_exception: Exception | None = None

        for model_name in model_candidates:
            try:
                response = self.client.models.generate_content(  # type: ignore[arg-type]
                    model=model_name,
                    contents=contents,
                    config=request_config,
                )
                # Keep diagnostics aligned with the model that actually worked.
                self.FRAME_COORDINATE_MODEL = model_name
                break
            except Exception as exc:
                last_exception = exc
                if self._is_unavailable_model_error(exc) and model_name != model_candidates[-1]:
                    logger.warning(
                        "Frame verifier model %s unavailable (404/access). Retrying with fallback model.",
                        model_name,
                    )
                    continue
                raise GeminiGenerationError(
                    f"Gemini frame coordinate extraction failed ({type(exc).__name__}): {str(exc)}"
                ) from exc

        if response is None:
            if last_exception is not None:
                raise GeminiGenerationError(
                    f"Gemini frame coordinate extraction failed ({type(last_exception).__name__}): {str(last_exception)}"
                ) from last_exception
            raise GeminiGenerationError("Gemini frame coordinate extraction failed: no verifier model candidates available")

        raw_text = str(getattr(response, "text", "") or "").strip()
        if not raw_text:
            raise GeminiGenerationError("Gemini frame coordinate extraction returned an empty response")

        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise GeminiGenerationError(
                f"Gemini frame coordinate extraction returned invalid JSON: {raw_text[:400]}"
            ) from exc

        normalized: dict[str, list[int]] = {}
        raw_points: dict[str, tuple[float, float]] = {}
        width, height = image_obj.size
        for key in ("tl", "tr", "br", "bl"):
            value = payload.get(key)
            if not isinstance(value, (list, tuple)) or len(value) != 2:
                raise GeminiGenerationError(
                    f"Gemini frame coordinate extraction returned invalid '{key}' point: {value!r}"
                )
            try:
                x_val = float(value[0])
                y_val = float(value[1])
            except (TypeError, ValueError) as exc:
                raise GeminiGenerationError(
                    f"Gemini frame coordinate extraction returned non-numeric '{key}' point: {value!r}"
                ) from exc

            raw_points[key] = (x_val, y_val)

            if mode == "normalized":
                x_val = (x_val / 1000.0) * width
                y_val = (y_val / 1000.0) * height

            normalized[key] = [int(round(x_val)), int(round(y_val))]

        normalized = self._repair_frame_points_if_needed(
            points=normalized,
            raw_points=raw_points,
            width=width,
            height=height,
            mode=mode,
        )

        for key, point in normalized.items():
            x_val, y_val = point
            if not (0 <= x_val <= width and 0 <= y_val <= height):
                raise GeminiGenerationError(
                    f"Gemini frame coordinate extraction returned out-of-bounds '{key}' point {point} for {width}x{height} image"
                )

        return normalized

    def _frame_points_in_bounds(self, points: dict[str, list[int]], width: int, height: int) -> bool:
        for key in ("tl", "tr", "br", "bl"):
            if key not in points:
                return False
            x_val, y_val = points[key]
            if not (0 <= int(x_val) <= int(width) and 0 <= int(y_val) <= int(height)):
                return False
        return True

    def _repair_frame_points_if_needed(
        self,
        *,
        points: dict[str, list[int]],
        raw_points: dict[str, tuple[float, float]],
        width: int,
        height: int,
        mode: str,
    ) -> dict[str, list[int]]:
        if self._frame_points_in_bounds(points, width, height):
            return points

        repaired: dict[str, list[int]] | None = None
        max_x = max((float(v[0]) for v in raw_points.values()), default=0.0)
        max_y = max((float(v[1]) for v in raw_points.values()), default=0.0)

        # Some verifier responses use 0..1000 normalized coordinates even when
        # absolute coordinates are requested.
        if mode == "absolute" and max_x <= 1100.0 and max_y <= 1100.0:
            candidate = {
                key: [
                    int(round((raw_points[key][0] / 1000.0) * width)),
                    int(round((raw_points[key][1] / 1000.0) * height)),
                ]
                for key in ("tl", "tr", "br", "bl")
            }
            if self._frame_points_in_bounds(candidate, width, height):
                repaired = candidate

        # Some responses are in a 2048 reference space even when output is 1024.
        if repaired is None and mode == "absolute" and max_x <= 2600.0 and max_y <= 2600.0:
            candidate = {
                key: [
                    int(round((raw_points[key][0] / 2048.0) * width)),
                    int(round((raw_points[key][1] / 2048.0) * height)),
                ]
                for key in ("tl", "tr", "br", "bl")
            }
            if self._frame_points_in_bounds(candidate, width, height):
                repaired = candidate

        # Last-resort clamp so pipeline can proceed; downstream composition
        # validation will still reject invalid/degenerate geometry.
        if repaired is None:
            repaired = {
                key: [
                    max(0, min(width, int(points[key][0]))),
                    max(0, min(height, int(points[key][1]))),
                ]
                for key in ("tl", "tr", "br", "bl")
            }

        logger.warning(
            "Repaired out-of-bounds frame coordinates for %sx%s image. mode=%s raw_max=(%.1f, %.1f)",
            width,
            height,
            mode,
            max_x,
            max_y,
        )
        return repaired

    def generate_alpha_mask(
        self,
        image_path: str | Path,
        edge_smoothing: bool = False,
    ) -> tuple[Image.Image, dict[str, list[int]]]:
        """Generate a binary/soft alpha mask from verifier frame coordinates."""
        target_path = Path(image_path)
        if not target_path.exists():
            raise FileNotFoundError(f"Image not found for alpha mask generation: {target_path}")

        image_obj = Image.open(target_path)
        image_obj.load()
        width, height = image_obj.size

        coords = self.extract_frame_coordinates(target_path)
        polygon = [
            tuple(coords["tl"]),
            tuple(coords["tr"]),
            tuple(coords["br"]),
            tuple(coords["bl"]),
        ]

        mask = Image.new("L", (width, height), 0)
        drawer = ImageDraw.Draw(mask)
        drawer.polygon(polygon, fill=255)

        if edge_smoothing:
            if cv2 is not None and np is not None:
                mask_np = np.array(mask)
                mask_np = cv2.GaussianBlur(mask_np, (5, 5), 0)
                mask = Image.fromarray(mask_np, mode="L")
            else:
                mask = mask.filter(ImageFilter.GaussianBlur(radius=1.2))

        return mask, coords

    def composite_artwork_locally(
        self,
        background_path: str | Path,
        artwork_path: str | Path,
        coordinates: dict[str, list[int]],
    ) -> tuple[Image.Image, Image.Image]:
        """Warp artwork into a detected quadrilateral and composite it locally.

        This is the deterministic assembly-line compositor step:
        - Perspective transform with OpenCV for exact fit
        - Alpha-aware blend onto generated room
        - Placement mask returned for downstream transparent template exports
        """
        if cv2 is None or np is None:
            raise GeminiGenerationError(
                "Local compositing requires opencv-python and numpy in the worker environment"
            )

        bg_path = Path(background_path)
        art_path = Path(artwork_path)
        if not bg_path.exists():
            raise FileNotFoundError(f"Background image not found: {bg_path}")
        if not art_path.exists():
            raise FileNotFoundError(f"Artwork image not found: {art_path}")

        background_pil = Image.open(bg_path).convert("RGBA")
        artwork_pil = Image.open(art_path).convert("RGBA")

        bg_np = np.array(background_pil)
        art_np = np.array(artwork_pil)

        bg_h, bg_w = bg_np.shape[:2]
        art_h, art_w = art_np.shape[:2]
        if art_w <= 1 or art_h <= 1:
            raise GeminiGenerationError("Artwork image dimensions are invalid for perspective transform")

        try:
            dst = np.array(
                [
                    coordinates["tl"],
                    coordinates["tr"],
                    coordinates["br"],
                    coordinates["bl"],
                ],
                dtype=np.float32,
            ).reshape((4, 2))
        except Exception as exc:
            raise GeminiGenerationError("Invalid coordinate payload for local compositing") from exc

        src = np.array(
            [
                [0, 0],
                [art_w - 1, 0],
                [art_w - 1, art_h - 1],
                [0, art_h - 1],
            ],
            dtype=np.float32,
        ).reshape((4, 2))

        matrix = cv2.getPerspectiveTransform(src, dst)  # type: ignore[arg-type]
        warped_rgba = cv2.warpPerspective(
            art_np,
            matrix,
            (bg_w, bg_h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_TRANSPARENT,
        )

        alpha = warped_rgba[:, :, 3].astype(np.float32) / 255.0
        alpha_3 = np.repeat(alpha[:, :, None], 3, axis=2)

        bg_rgb = bg_np[:, :, :3].astype(np.float32)
        warped_rgb = warped_rgba[:, :, :3].astype(np.float32)
        composite_rgb = warped_rgb * alpha_3 + bg_rgb * (1.0 - alpha_3)

        composite_rgba = np.zeros((bg_h, bg_w, 4), dtype=np.uint8)
        composite_rgba[:, :, :3] = np.clip(composite_rgb, 0, 255).astype(np.uint8)
        composite_rgba[:, :, 3] = 255

        mask_np = np.clip(alpha * 255.0, 0, 255).astype(np.uint8)
        if int(mask_np.max()) == 0:
            raise GeminiGenerationError("Local compositor produced an empty placement mask")

        composite_image = Image.fromarray(composite_rgba, mode="RGBA")
        mask_image = Image.fromarray(mask_np, mode="L")
        return composite_image, mask_image

    def _extract_thought_signature(self, response: Any) -> str:
        """Extract a thought signature from Gemini response payload when available."""
        candidate_fields = (
            "thought_signature",
            "thoughtSignature",
            "reasoning_signature",
            "reasoningSignature",
            "signature",
        )

        for field_name in candidate_fields:
            try:
                value = getattr(response, field_name, None)
            except Exception:
                value = None
            if isinstance(value, str) and value.strip():
                return value.strip()

        # Best-effort scan nested dict payloads in SDK objects.
        try:
            response_dict = getattr(response, "__dict__", None)
            if isinstance(response_dict, dict):
                for field_name in candidate_fields:
                    nested_value = response_dict.get(field_name)
                    if isinstance(nested_value, str) and nested_value.strip():
                        return nested_value.strip()
        except Exception:
            pass

        return ""

    def _is_reference_guide_required(self) -> bool:
        """Return True when generation must use per-aspect cyan guide images.

        Behavior:
        - If MOCKUP_REQUIRE_REFERENCE_GUIDE is explicitly set, honor it.
        - Otherwise default to requiring guide-backed generation for the mockup
          pipeline so aspect ratio control is not left to prompt-only behavior.
        """
        raw_value = os.getenv("MOCKUP_REQUIRE_REFERENCE_GUIDE")
        if raw_value is None:
            return True

        return raw_value.strip().lower() not in {"0", "false", "no", "off"}

    def _is_reference_guide_strict(self) -> bool:
        """Return True when missing/unavailable guide-editing should hard-fail generation."""
        raw_value = os.getenv("MOCKUP_REQUIRE_REFERENCE_GUIDE_STRICT", "true")
        return raw_value.strip().lower() in {"1", "true", "yes", "on"}

    def _supports_reference_guided_editing(self) -> bool:
        """Return True when the active client can call edit_image()."""
        return bool(
            types is not None
            and getattr(getattr(self.client, "models", None), "edit_image", None)
        )

    def _resolve_reference_guide_path(self, aspect_ratio: str) -> Optional[Path]:
        """Resolve the per-aspect placement guide path for the active guide mode."""
        placeholder_mode = self._load_placeholder_mode()
        candidate_paths: list[Path] = []

        if placeholder_mode == "positional":
            candidate_paths.extend(
                [
                    self.POSITIONAL_REFERENCE_GUIDE_STORAGE_DIR / f"coordinate-tester-{aspect_ratio}.jpg",
                    self.POSITIONAL_REFERENCE_GUIDE_STORAGE_DIR / f"coordinate-tester-{aspect_ratio}.png",
                    self.POSITIONAL_REFERENCE_GUIDE_SOURCE_DIR / f"coordinate-tester-{aspect_ratio}.jpg",
                    self.POSITIONAL_REFERENCE_GUIDE_SOURCE_DIR / f"coordinate-tester-{aspect_ratio}.png",
                ]
            )

        # Always include cyan guides as fallback so queue runs do not hard-fail
        # when positional test files are incomplete for some aspect ratios.
        candidate_paths.extend(
            [
                self.REFERENCE_GUIDE_STORAGE_DIR / f"cyan_guide_{aspect_ratio}.png",
                self.LEGACY_REFERENCE_GUIDE_STORAGE_DIR / f"solid_{aspect_ratio}_00ffff.png",
            ]
        )

        for candidate_path in candidate_paths:
            if candidate_path.exists():
                logger.info(
                    "Resolved guide image for aspect=%s mode=%s path=%s",
                    aspect_ratio,
                    placeholder_mode,
                    candidate_path,
                )
                return candidate_path

        return None

    def _load_placeholder_mode(self) -> str:
        """Read operator-selected placeholder guide mode from shared control state."""
        default_mode = "cyan"
        try:
            if not CONTROL_STATE_PATH.exists():
                return default_mode
            payload = json.loads(CONTROL_STATE_PATH.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                return default_mode
            mode = str(payload.get("placeholder_mode") or default_mode).strip().lower()
            return mode if mode in {"cyan", "positional"} else default_mode
        except Exception:
            return default_mode

    def _extract_generated_image_bytes(self, response: Any) -> bytes:
        """Extract raw image bytes from a Gemini image generation response."""
        if not getattr(response, "generated_images", None):
            raise GeminiGenerationError("Gemini API returned no images")

        image = response.generated_images[0]

        image_data = None
        if hasattr(image, "data") and isinstance(getattr(image, "data", None), bytes):
            image_data = getattr(image, "data")
        elif hasattr(image, "bytes") and isinstance(getattr(image, "bytes", None), bytes):
            image_data = getattr(image, "bytes")
        elif hasattr(image, "image"):
            nested_image = getattr(image, "image", None)
            if hasattr(nested_image, "image_bytes") and isinstance(
                getattr(nested_image, "image_bytes", None),
                bytes,
            ):
                image_data = getattr(nested_image, "image_bytes")
        elif isinstance(image, bytes):
            image_data = image
        else:
            try:
                image_data = (
                    getattr(image, "_raw_data", None)
                    or getattr(image, "raw_image", None)
                    or getattr(image, "content", None)
                )
            except (AttributeError, TypeError):
                image_data = None

        if not isinstance(image_data, bytes):
            raise GeminiGenerationError(
                "Gemini API image has no valid data payload "
                f"(got {type(image_data).__name__})"
            )

        return image_data

    def _save_image_to_disk(
        self,
        image_bytes: bytes,
        category: str,
        aspect_ratio: str,
        variation_index: int,
    ) -> Path:
        """Save image bytes to disk in a category-specific directory.

        Directory structure:
            <project>/application/mockups/catalog/assets/mockups/bases/{category}/
                {category}_{aspect_ratio}_{variation_index}_{timestamp}.png

        Args:
            image_bytes: Raw image bytes from Gemini
            category: Category name (used for directory)
            aspect_ratio: Aspect ratio string (used for filename)
            variation_index: Variation index (used for filename and tracking)

        Returns:
            Full Path object to the saved file

        Raises:
            GeminiFileSaveError: If directory creation or file write fails
        """
        try:
            # Create category-specific directory
            category_dir = self.MOCKUP_BASE_STORAGE_DIR / category
            category_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename with timestamp and metadata
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{category}_{aspect_ratio}_var{variation_index}_{timestamp}.png"
            file_path = category_dir / filename

            # Write image bytes to file
            with open(file_path, "wb") as f:
                f.write(image_bytes)

            # Verify the file was written
            if not file_path.exists() or file_path.stat().st_size == 0:
                raise GeminiFileSaveError(
                    f"Image file was not written correctly: {file_path}"
                )

            logger.info(
                f"Image saved successfully: {file_path} ({file_path.stat().st_size} bytes)"
            )
            return file_path

        except GeminiFileSaveError:
            raise
        except IOError as e:
            msg = f"Failed to write image to disk at {self.MOCKUP_BASE_STORAGE_DIR}: {str(e)}"
            logger.error(msg, exc_info=True)
            raise GeminiFileSaveError(msg) from e
        except Exception as e:
            msg = f"Unexpected error saving image to disk: {str(e)}"
            logger.error(msg, exc_info=True)
            raise GeminiFileSaveError(msg) from e

    def validate_api_connection(self) -> bool:
        """Test the Gemini API connection with a simple call.

        Returns:
            True if connection is valid and working
            False if connection fails

        This is useful for health checks before starting batch generation.
        """
        try:
            # Make a lightweight API call to validate auth
            response = self.client.models.list()
            logger.info("Gemini API connection validated successfully")
            return True
        except GeminiAuthenticationError:
            logger.error("Gemini API authentication validation failed")
            return False
        except Exception as e:
            logger.error(f"Gemini API connection validation failed: {str(e)}")
            return False
