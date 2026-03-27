"""Mockup coordinate extraction service for cyan placeholder detection.

Stage 3 service that extracts the four ordered corner points of the cyan
placeholder quad from generated mockup images.

This module is logic-only and does not perform database updates.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Final

import cv2
import numpy as np


class MockupCoordinateServiceError(Exception):
    """Base exception for coordinate extraction failures."""


class CyanQuadNotFoundError(MockupCoordinateServiceError):
    """Raised when no cyan contour can be detected in the image."""


class InvalidCyanShapeError(MockupCoordinateServiceError):
    """Raised when the detected cyan contour cannot be resolved to a quad."""


class MockupCoordinateService:
    """Extract ordered quad coordinates from cyan placeholder regions."""

    # OpenCV HSV ranges for cyan-like placeholders.
    # Pass 1 is strict near #00FFFF. Pass 2 is relaxed to tolerate model drift.
    CYAN_HSV_RANGES: Final[tuple[tuple[np.ndarray, np.ndarray], ...]] = (
        (
            np.array([86, 180, 150], dtype=np.uint8),
            np.array([96, 255, 255], dtype=np.uint8),
        ),
        (
            np.array([78, 110, 80], dtype=np.uint8),
            np.array([104, 255, 255], dtype=np.uint8),
        ),
    )

    # Morphological kernels to reduce speckle and close tiny gaps.
    OPEN_KERNEL: Final[np.ndarray] = np.ones((3, 3), dtype=np.uint8)
    CLOSE_KERNEL: Final[np.ndarray] = np.ones((5, 5), dtype=np.uint8)

    # Epsilon schedule for iterative quad approximation.
    APPROX_EPSILON_FACTORS: Final[tuple[float, ...]] = (
        0.010,
        0.012,
        0.015,
        0.018,
        0.022,
        0.028,
        0.035,
        0.045,
        0.060,
    )

    @classmethod
    def extract_coordinates(cls, image_path: str) -> list[dict[str, int]]:
        """Extract artwork placeholder corners from an image.

        Supports two placeholder formats:
        1. **Cyan rectangle** (Gemini-generated): A solid #00FFFF region detected via
           HSV colour masking. Tried first with a strict pass then a relaxed pass.
        2. **Transparent cutout** (legacy uploaded bases): A fully- or partially-transparent
           region detected via the PNG alpha channel. Used as a fallback only when cyan
           detection finds nothing.

        Args:
            image_path: Absolute or relative path to the input image.

        Returns:
            Ordered list of four coordinates in strict order:
            Top-Left, Top-Right, Bottom-Right, Bottom-Left.

        Raises:
            FileNotFoundError: If the input image path does not exist.
            ValueError: If the image cannot be decoded.
            CyanQuadNotFoundError: If neither cyan nor transparent region is found.
            InvalidCyanShapeError: If the contour cannot be approximated to 4 points.
        """
        path_obj = Path(image_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Image not found: {path_obj}")

        image_bgr = cv2.imread(str(path_obj), cv2.IMREAD_COLOR)
        if image_bgr is None:
            raise ValueError(f"Unable to read image: {path_obj}")

        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        largest_contour: np.ndarray | None = None
        for lower_hsv, upper_hsv in cls.CYAN_HSV_RANGES:
            mask = cv2.inRange(image_hsv, lower_hsv, upper_hsv)

            # Reduce isolated cyan noise, then close small boundary holes.
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cls.OPEN_KERNEL, iterations=1)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cls.CLOSE_KERNEL, iterations=2)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                continue

            candidate = max(contours, key=cv2.contourArea)
            if cv2.contourArea(candidate) <= 0:
                continue

            largest_contour = candidate
            break

        if largest_contour is None:
            # Fallback: try alpha-channel transparent cutout (legacy uploaded bases).
            try:
                return cls._extract_alpha_coordinates(image_path)
            except MockupCoordinateServiceError:
                pass
            raise CyanQuadNotFoundError(
                "No cyan contour detected. Ensure the image contains a #00FFFF placeholder."
            )

        quad_points = cls._approximate_quad_points(largest_contour)
        ordered_points = cls._order_points_tl_tr_br_bl(quad_points)

        return [
            {"x": int(round(x)), "y": int(round(y))}
            for x, y in ordered_points
        ]

    @classmethod
    def _extract_alpha_coordinates(cls, image_path: str) -> list[dict[str, int]]:
        """Extract artwork area corners from a transparent (alpha-channel) PNG.

        Used as a fallback for legacy uploaded mockup bases where the artwork
        placement region is a fully or partially transparent cutout rather than
        a cyan-coloured rectangle.

        Args:
            image_path: Absolute or relative path to the input image.

        Returns:
            Ordered list of four coordinates: Top-Left, Top-Right, Bottom-Right,
            Bottom-Left.

        Raises:
            CyanQuadNotFoundError: If the image has no alpha channel or no
                transparent region is detected.
            InvalidCyanShapeError: If the transparent region cannot be
                approximated to 4 corner points.
        """
        image_bgra = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        if image_bgra is None or image_bgra.ndim < 3 or image_bgra.shape[2] < 4:
            raise CyanQuadNotFoundError(
                "Image has no alpha channel; cannot use transparent-cutout fallback."
            )

        alpha = image_bgra[:, :, 3]
        # Transparent pixels have alpha < 128.
        _, mask = cv2.threshold(alpha, 127, 255, cv2.THRESH_BINARY_INV)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cls.OPEN_KERNEL, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cls.CLOSE_KERNEL, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise CyanQuadNotFoundError(
                "No transparent region found in alpha channel."
            )

        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) <= 0:
            raise CyanQuadNotFoundError(
                "Transparent region detected but has zero area."
            )

        quad_points = cls._approximate_quad_points(largest)
        ordered_points = cls._order_points_tl_tr_br_bl(quad_points)
        return [{"x": int(round(x)), "y": int(round(y))} for x, y in ordered_points]

    @classmethod
    def _approximate_quad_points(
        cls,
        contour: np.ndarray,
    ) -> np.ndarray:
        """Approximate a contour to exactly four corner points."""
        perimeter = cv2.arcLength(contour, True)
        if perimeter <= 0:
            raise InvalidCyanShapeError("Contour perimeter is zero; cannot approximate shape.")

        best_candidate: np.ndarray | None = None
        best_distance = math.inf

        for epsilon_factor in cls.APPROX_EPSILON_FACTORS:
            epsilon = epsilon_factor * perimeter
            approximation = cv2.approxPolyDP(contour, epsilon, True)
            point_count = len(approximation)

            if point_count == 4:
                return approximation.reshape(4, 2).astype(np.float32)

            # Track closest candidate to aid diagnostics if no exact quad is found.
            distance_from_quad = abs(point_count - 4)
            if distance_from_quad < best_distance:
                best_distance = distance_from_quad
                best_candidate = approximation

        candidate_count = len(best_candidate) if best_candidate is not None else 0
        raise InvalidCyanShapeError(
            "Cyan contour could not be approximated to exactly 4 points "
            f"(closest candidate had {candidate_count} points)."
        )

    @staticmethod
    def _order_points_tl_tr_br_bl(points: np.ndarray) -> list[tuple[float, float]]:
        """Order 4 points as Top-Left, Top-Right, Bottom-Right, Bottom-Left.

        Uses sum/difference heuristics, which are robust for convex quads under
        perspective distortion in mockup scenes.
        """
        if points.shape != (4, 2):
            raise InvalidCyanShapeError(
                "Point ordering requires exactly 4 points shaped as (4, 2)."
            )

        sums = points.sum(axis=1)
        diffs = np.diff(points, axis=1).reshape(4)

        top_left = points[int(np.argmin(sums))]
        bottom_right = points[int(np.argmax(sums))]
        top_right = points[int(np.argmin(diffs))]
        bottom_left = points[int(np.argmax(diffs))]

        ordered = [
            (float(top_left[0]), float(top_left[1])),
            (float(top_right[0]), float(top_right[1])),
            (float(bottom_right[0]), float(bottom_right[1])),
            (float(bottom_left[0]), float(bottom_left[1])),
        ]

        # Guard against degenerate ordering where two points collapse together.
        unique_points = {(round(x, 4), round(y, 4)) for x, y in ordered}
        if len(unique_points) != 4:
            raise InvalidCyanShapeError(
                "Failed to derive 4 unique ordered corners from cyan contour."
            )

        return ordered
