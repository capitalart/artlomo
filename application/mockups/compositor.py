"""Compositing helpers for mockup generation."""

from __future__ import annotations

from typing import Iterable

from PIL import Image

from .errors import TransformError


def composite_layers(base_rgba: Image.Image, warped_layers: Iterable[Image.Image]) -> Image.Image:
    # Compose onto a copy of the base so mapped artwork directly replaces the
    # placeholder region regardless of placeholder colour/shading drift.
    canvas = base_rgba.copy()
    for layer in warped_layers:
        if base_rgba.size != layer.size:
            raise TransformError("Base and warped artwork sizes must match for compositing")
        canvas.alpha_composite(layer)
    return canvas


def flatten_to_rgb(image_rgba: Image.Image) -> Image.Image:
    return image_rgba.convert("RGB")
