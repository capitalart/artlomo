"""Mockup Base Generation - Solid Color Image Utility Service.

Generates high-resolution solid color images for given aspect ratios.
Used to create reference cyan placeholder images and colored testing assets.

Design Principles:
- Aspect ratios expected as "X:Y" format (e.g., "16:9", "3:4", "1:1")
- High-resolution output by multiplying dimensions by scale factor (default 1000)
- Memory-aware capping of longest edge (4000-5000px max) to prevent OOM
- Optional file persistence or BytesIO return for in-memory processing
- Pillow/PIL for image generation
"""

from __future__ import annotations

import logging
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

from PIL import Image


logger = logging.getLogger(__name__)


class SolidImageServiceException(Exception):
    """Base exception for SolidImageService errors."""

    pass


class SolidImageValidationError(SolidImageServiceException):
    """Raised when input parameters are invalid."""

    pass


class SolidImageGenerationError(SolidImageServiceException):
    """Raised when image generation fails."""

    pass


class SolidImageService:
    """Service for generating high-resolution solid color images."""

    # Scaling factor for dimension calculation (multiplies aspect ratio components)
    DEFAULT_SCALE_FACTOR = 1000

    # Maximum pixel dimension to prevent OOM for large ratios like 70:99
    MAX_PIXEL_DIMENSION = 5000

    # Default color (matte cyan, matching cyan placeholder specification)
    DEFAULT_COLOR = "#00FFFF"

    @classmethod
    def generate_solid_image(
        cls,
        aspect_ratio: str,
        color: str = DEFAULT_COLOR,
        scale_factor: Optional[int] = None,
        output_path: Optional[Path] = None,
    ) -> Union[str, BytesIO]:
        """Generate a solid color image for a given aspect ratio.

        Args:
            aspect_ratio: Aspect ratio in "X:Y" format (e.g., "16:9", "3:4", "1:1")
            color: Hex color code with or without '#' prefix (default: matte cyan #00FFFF)
            scale_factor: Multiplier for dimensions (default: 1000). Higher values
                         produce larger filesizes; dimension capping prevents OOM.
            output_path: Optional Path to save image to disk. If None, returns BytesIO.

        Returns:
            If output_path provided: str path to saved file
            If output_path is None: BytesIO object with PNG-encoded image

        Raises:
            SolidImageValidationError: If aspect_ratio or color format is invalid
            SolidImageGenerationError: If image generation or file writing fails
        """
        if scale_factor is None:
            scale_factor = cls.DEFAULT_SCALE_FACTOR

        # Validate and parse aspect ratio
        try:
            width_ratio, height_ratio = cls._parse_aspect_ratio(aspect_ratio)
        except ValueError as e:
            raise SolidImageValidationError(str(e)) from e

        # Validate and normalize color
        try:
            rgb_tuple = cls._parse_hex_color(color)
        except ValueError as e:
            raise SolidImageValidationError(str(e)) from e

        # Calculate dimensions with scaling
        width_px, height_px = cls._calculate_dimensions(
            width_ratio=width_ratio,
            height_ratio=height_ratio,
            scale_factor=scale_factor,
        )

        logger.info(
            f"Generating solid image: aspect_ratio={aspect_ratio}, "
            f"color={color}, dimensions={width_px}x{height_px}px"
        )

        # Generate image
        try:
            image = Image.new("RGB", (width_px, height_px), rgb_tuple)
            logger.debug(f"Image created: {width_px}x{height_px}px")
        except MemoryError as e:
            msg = (
                f"Out of memory generating {width_px}x{height_px}px image. "
                f"Try a smaller scale_factor."
            )
            logger.error(msg)
            raise SolidImageGenerationError(msg) from e
        except Exception as e:
            msg = f"Failed to create image: {str(e)}"
            logger.error(msg, exc_info=True)
            raise SolidImageGenerationError(msg) from e

        # Return as file or BytesIO
        if output_path:
            return cls._save_image_to_disk(image, output_path)
        else:
            return cls._image_to_bytesio(image)

    @classmethod
    def _parse_aspect_ratio(cls, aspect_ratio: str) -> tuple[int, int]:
        """Parse aspect ratio string to component integers.

        Args:
            aspect_ratio: String in format "X:Y" (e.g., "16:9")

        Returns:
            Tuple of (width_ratio, height_ratio) as integers

        Raises:
            ValueError: If format is invalid or components are non-positive
        """
        aspect_ratio = aspect_ratio.strip()

        if ":" not in aspect_ratio:
            raise ValueError(
                f"Aspect ratio must be in 'X:Y' format (e.g., '16:9'), "
                f"got: {aspect_ratio}"
            )

        parts = aspect_ratio.split(":")
        if len(parts) != 2:
            raise ValueError(
                f"Aspect ratio must have exactly one colon (e.g., '16:9'), "
                f"got: {aspect_ratio}"
            )

        try:
            width_ratio = int(parts[0].strip())
            height_ratio = int(parts[1].strip())
        except ValueError:
            raise ValueError(
                f"Aspect ratio components must be integers, "
                f"got: {parts[0]}, {parts[1]}"
            )

        if width_ratio <= 0 or height_ratio <= 0:
            raise ValueError(
                f"Aspect ratio components must be positive, "
                f"got: {width_ratio}:{height_ratio}"
            )

        return width_ratio, height_ratio

    @classmethod
    def _parse_hex_color(cls, color: str) -> tuple[int, int, int]:
        """Parse hex color string to RGB tuple.

        Args:
            color: Hex color in "#RRGGBB" or "RRGGBB" format (case-insensitive)

        Returns:
            Tuple of (R, G, B) integers 0-255

        Raises:
            ValueError: If format is invalid or out of range
        """
        color = color.strip().lstrip("#").upper()

        if len(color) != 6:
            raise ValueError(
                f"Hex color must be 6 digits (e.g., '#00FFFF' or '00FFFF'), "
                f"got: {color}"
            )

        try:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
        except ValueError:
            raise ValueError(
                f"Hex color contains invalid characters: {color}"
            )

        return r, g, b

    @classmethod
    def _calculate_dimensions(
        cls,
        width_ratio: int,
        height_ratio: int,
        scale_factor: int,
    ) -> tuple[int, int]:
        """Calculate pixel dimensions with scaling and OOM protection.

        Multiplies ratio components by scale_factor, then caps the longest
        edge at MAX_PIXEL_DIMENSION to prevent excessive memory usage.

        Args:
            width_ratio: Width component of aspect ratio
            height_ratio: Height component of aspect ratio
            scale_factor: Multiplier for dimensions

        Returns:
            Tuple of (width_px, height_px)
        """
        width_px = width_ratio * scale_factor
        height_px = height_ratio * scale_factor

        # Cap longest edge to prevent OOM
        max_dim = max(width_px, height_px)
        if max_dim > cls.MAX_PIXEL_DIMENSION:
            scale_used = cls.MAX_PIXEL_DIMENSION / max_dim
            width_px = int(width_px * scale_used)
            height_px = int(height_px * scale_used)
            logger.info(
                f"Capped dimensions to {width_px}x{height_px}px "
                f"(max edge {cls.MAX_PIXEL_DIMENSION}px)"
            )

        return width_px, height_px

    @classmethod
    def _save_image_to_disk(cls, image: Image.Image, output_path: Path) -> str:
        """Save image to disk and return file path.

        Args:
            image: PIL Image object
            output_path: Path where image should be saved

        Returns:
            Absolute file path as string

        Raises:
            SolidImageGenerationError: If file write fails
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Determine format from extension
            extension = output_path.suffix.lower()
            if extension == ".jpg" or extension == ".jpeg":
                image.save(output_path, format="JPEG", quality=95)
            elif extension == ".png":
                image.save(output_path, format="PNG")
            else:
                # Default to PNG if extension not recognized
                if not extension:
                    output_path = output_path.with_suffix(".png")
                image.save(output_path, format="PNG")

            file_size = output_path.stat().st_size
            logger.info(f"Image saved: {output_path} ({file_size} bytes)")
            return str(output_path)

        except IOError as e:
            msg = f"Failed to write image to {output_path}: {str(e)}"
            logger.error(msg, exc_info=True)
            raise SolidImageGenerationError(msg) from e
        except Exception as e:
            msg = f"Unexpected error saving image: {str(e)}"
            logger.error(msg, exc_info=True)
            raise SolidImageGenerationError(msg) from e

    @classmethod
    def _image_to_bytesio(cls, image: Image.Image) -> BytesIO:
        """Convert PIL Image to BytesIO for in-memory transmission.

        Args:
            image: PIL Image object

        Returns:
            BytesIO object containing PNG-encoded image data

        Raises:
            SolidImageGenerationError: If encoding fails
        """
        try:
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            logger.debug(f"Image converted to BytesIO ({buffer.getbuffer().nbytes} bytes)")
            return buffer
        except Exception as e:
            msg = f"Failed to encode image to BytesIO: {str(e)}"
            logger.error(msg, exc_info=True)
            raise SolidImageGenerationError(msg) from e
