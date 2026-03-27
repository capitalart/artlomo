"""Service A: MockupGenerationService (The Painter).

Generates a room scene image with Gemini and hard-fails on any generation issue.
"""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

from ..contracts import MockupGenerationInput, MockupGenerationResult
from ..exceptions import GenerationFailedError


class GeminiImageClientProtocol:
    """Protocol-like adapter for Gemini image generation."""

    def generate_image_bytes(self, prompt: str, model: str) -> bytes:
        raise NotImplementedError


class GoogleGenAIGeminiClient(GeminiImageClientProtocol):
    """Gemini client wrapper using google-genai SDK.

    Uses generate_content with image modality and extracts first returned image part.
    """

    def __init__(self, api_key: str | None = None):
        api_key_value = (api_key or os.getenv("GEMINI_API_KEY") or "").strip()
        if not api_key_value:
            raise GenerationFailedError("Missing GEMINI_API_KEY for generation service")

        try:
            from google import genai
            from google.genai import types
        except Exception as exc:
            raise GenerationFailedError("google-genai SDK import failed") from exc

        self._genai = genai
        self._types = types
        self._client = genai.Client(api_key=api_key_value)

    def generate_image_bytes(self, prompt: str, model: str) -> bytes:
        try:
            response = self._client.models.generate_content(
                model=model,
                contents=prompt,
                config=self._types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                ),
            )
        except Exception as exc:
            raise GenerationFailedError(f"Gemini generation call failed: {exc}") from exc

        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None) or []
            for part in parts:
                inline_data = getattr(part, "inline_data", None)
                data = getattr(inline_data, "data", None) if inline_data else None
                if isinstance(data, (bytes, bytearray)) and data:
                    return bytes(data)

        raise GenerationFailedError("Gemini returned no image bytes")


class MockupGenerationService:
    """Generate mockup base scenes from prompts."""

    def __init__(self, image_client: GeminiImageClientProtocol | None = None):
        self._image_client = image_client or GoogleGenAIGeminiClient()

    def generate(self, request: MockupGenerationInput) -> MockupGenerationResult:
        prompt = (request.prompt or "").strip()
        if not prompt:
            raise GenerationFailedError("Prompt is required for generation")

        output_path = Path(request.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        image_bytes = self._image_client.generate_image_bytes(prompt=prompt, model=request.model)
        if not image_bytes:
            raise GenerationFailedError("Gemini returned empty image bytes")

        try:
            output_path.write_bytes(image_bytes)
            with Image.open(output_path) as img:
                width, height = img.size
                if width <= 0 or height <= 0:
                    raise GenerationFailedError("Generated image has invalid dimensions")
        except GenerationFailedError:
            raise
        except Exception as exc:
            raise GenerationFailedError(f"Failed to persist generated image: {exc}") from exc

        return MockupGenerationResult(
            image_path=output_path,
            width=width,
            height=height,
            model=request.model,
        )
