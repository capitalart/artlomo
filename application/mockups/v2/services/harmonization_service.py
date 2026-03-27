"""Service E: HarmonizationService (The Polisher).

Optional lighting/shadow harmonization pass via Gemini image model.
"""

from __future__ import annotations

from pathlib import Path

from ..contracts import HarmonizationInput, HarmonizationResult
from ..exceptions import HarmonizationError
from .mockup_generation_service import GeminiImageClientProtocol, GoogleGenAIGeminiClient


class HarmonizationService:
    """Run optional Gemini-based harmonization for final composites."""

    def __init__(self, image_client: GeminiImageClientProtocol | None = None):
        self._image_client = image_client or GoogleGenAIGeminiClient()

    def harmonize(self, request: HarmonizationInput) -> HarmonizationResult:
        source = Path(request.composite_jpeg_path)
        target = Path(request.output_jpeg_path)

        if not source.exists():
            raise HarmonizationError(f"Composite input does not exist: {source}")

        if not request.enabled:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
            return HarmonizationResult(
                output_jpeg_path=target,
                model=None,
                applied=False,
            )

        # The v2 implementation performs a strict pass: no silent fallback.
        # Current adapter supports prompt-only generation path. For future
        # image-conditioned edit APIs, replace this with direct image-edit call.
        prompt = (request.prompt or "").strip()
        if not prompt:
            raise HarmonizationError("Harmonization prompt is required when enabled")

        try:
            output_bytes = self._image_client.generate_image_bytes(
                prompt=prompt,
                model=request.model,
            )
        except Exception as exc:
            raise HarmonizationError(f"Harmonization generation failed: {exc}") from exc

        if not output_bytes:
            raise HarmonizationError("Harmonization returned empty image bytes")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(output_bytes)

        return HarmonizationResult(
            output_jpeg_path=target,
            model=request.model,
            applied=True,
        )
