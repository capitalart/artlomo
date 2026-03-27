"""Chromakey bridge service for Gemini-generated mockup bases.

This service detects a flat chromakey rectangle (default #00FFCC), extracts
ordered quad coordinates, removes the keyed region to transparency, and writes
an output PNG suitable for mockup compositing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final, cast

import cv2
import numpy as np


def process_and_map_cyan_mask(
    image_bytes: bytes,
    *,
    lower_hsv: tuple[int, int, int] = (85, 100, 100),
    upper_hsv: tuple[int, int, int] = (95, 255, 255),
    min_area_ratio: float = 0.0025,
    negative_inset_px: int = 2,
    black_guard_value_max: int = 70,
    black_guard_search_px: int = 36,
) -> tuple[bytes, list[dict[str, int]]]:
    """Detect triple-border target, erase external boundary, and return inner corners.

    This function is the byte-oriented bridge used by Gemini studio and batch
    generation flows.

    Args:
        image_bytes: Raw PNG/JPEG bytes.
        lower_hsv: Lower HSV threshold for cyan detection.
        upper_hsv: Upper HSV threshold for cyan detection.
        min_area_ratio: Minimum contour area ratio to accept as valid.

    Returns:
        Tuple of:
        - Transparent PNG bytes where keyed target pixels are alpha=0
        - Ordered 4-point corners in TL, TR, BR, BL order as {x, y}
    """
    if not image_bytes:
        raise ValueError("image_bytes must not be empty")

    encoded = np.frombuffer(image_bytes, dtype=np.uint8)
    bgr = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("Unable to decode image bytes")

    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    lower = np.array(lower_hsv, dtype=np.uint8)
    upper = np.array(upper_hsv, dtype=np.uint8)

    # Primary detection: locate the high-contrast cyan ring first.
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, ChromakeyBridgeService.OPEN_KERNEL, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, ChromakeyBridgeService.CLOSE_KERNEL, iterations=2)

    # Edge-snapping strategy: bilateral filter preserves hard boundaries while
    # reducing compression noise, then Canny edges constrain contour selection.
    filtered = cv2.bilateralFilter(bgr, d=9, sigmaColor=75, sigmaSpace=75)
    gray_filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_filtered, threshold1=60, threshold2=160)
    edges = cv2.dilate(edges, ChromakeyBridgeService.OPEN_KERNEL, iterations=1)

    snapped_mask = cv2.bitwise_and(mask, edges)
    if int(cv2.countNonZero(snapped_mask)) < 40:
        contour_input = mask
    else:
        contour_input = cv2.morphologyEx(
            snapped_mask,
            cv2.MORPH_CLOSE,
            ChromakeyBridgeService.CLOSE_KERNEL,
            iterations=1,
        )

    contours, _ = cv2.findContours(contour_input, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        relaxed_lower = np.array(
            [max(0, int(lower[0]) - 8), max(50, int(lower[1]) - 40), max(50, int(lower[2]) - 40)],
            dtype=np.uint8,
        )
        relaxed_upper = np.array(
            [min(179, int(upper[0]) + 8), min(255, int(upper[1]) + 20), min(255, int(upper[2]) + 20)],
            dtype=np.uint8,
        )
        relaxed_mask = cv2.inRange(hsv, relaxed_lower, relaxed_upper)
        relaxed_mask = cv2.morphologyEx(
            relaxed_mask,
            cv2.MORPH_CLOSE,
            ChromakeyBridgeService.CLOSE_KERNEL,
            iterations=1,
        )
        contours, _ = cv2.findContours(relaxed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ChromakeyRegionNotFoundError("No chromakey contour found for cyan HSV mask.")

    largest = max(contours, key=cv2.contourArea)
    contour_area = float(cv2.contourArea(largest))
    total_area = float(bgr.shape[0] * bgr.shape[1])
    if contour_area <= 0 or contour_area < (total_area * float(min_area_ratio)):
        raise ChromakeyRegionNotFoundError(
            "Chromakey contour found but below minimum usable area threshold."
        )

    cyan_boundary = ChromakeyBridgeService._order_points_tl_tr_br_bl(
        ChromakeyBridgeService._approximate_quad(largest)
    )

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    black_threshold = max(15, min(120, int(black_guard_value_max)))
    black_lower = np.array(0, dtype=np.uint8)
    black_upper = np.array(black_threshold, dtype=np.uint8)
    black_mask = cv2.inRange(gray, black_lower, black_upper)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, ChromakeyBridgeService.OPEN_KERNEL, iterations=1)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, ChromakeyBridgeService.CLOSE_KERNEL, iterations=1)

    cyan_polygon = np.array(cyan_boundary, dtype=np.float32)
    cyan_area = float(cv2.contourArea(cyan_polygon.reshape(-1, 1, 2)))
    cyan_center = tuple(np.mean(cyan_polygon, axis=0).tolist())
    contour_candidates, _ = cv2.findContours(black_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    outer_candidates: list[tuple[float, list[tuple[float, float]]]] = []
    inner_candidates: list[tuple[float, list[tuple[float, float]]]] = []

    for candidate in contour_candidates:
        area = float(cv2.contourArea(candidate))
        if area < 20.0:
            continue

        try:
            candidate_boundary = ChromakeyBridgeService._order_points_tl_tr_br_bl(
                ChromakeyBridgeService._approximate_quad(candidate)
            )
        except ChromakeyBridgeError:
            continue

        candidate_polygon = np.array(candidate_boundary, dtype=np.float32).reshape(-1, 1, 2)
        contains_center = float(cv2.pointPolygonTest(candidate_polygon, cyan_center, False)) >= 0.0
        contains_cyan = all(
            float(cv2.pointPolygonTest(candidate_polygon, (float(x), float(y)), False)) >= 0.0
            for x, y in cyan_boundary
        )
        inside_cyan = all(
            float(cv2.pointPolygonTest(largest, (float(x), float(y)), False)) >= 0.0
            for x, y in candidate_boundary
        )

        if contains_center and contains_cyan and area > cyan_area:
            outer_candidates.append((area, candidate_boundary))
        elif inside_cyan and area < cyan_area:
            inner_candidates.append((area, candidate_boundary))

    external_boundary = max(outer_candidates, key=lambda item: item[0])[1] if outer_candidates else cyan_boundary
    internal_boundary = max(inner_candidates, key=lambda item: item[0])[1] if inner_candidates else cyan_boundary

    inset_internal = ChromakeyBridgeService._apply_negative_inset(
        internal_boundary,
        inset_px=max(0, int(negative_inset_px)),
    )

    bgra = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
    alpha = np.full((bgr.shape[0], bgr.shape[1]), 255, dtype=np.uint8)
    cutout_polygon = np.array([[int(round(x)), int(round(y))] for x, y in external_boundary], dtype=np.int32)
    cv2.fillPoly(alpha, [cutout_polygon], 0)
    bgra[:, :, 3] = alpha

    ok, encoded_png = cv2.imencode(".png", bgra)
    if not ok:
        raise ChromakeyBridgeError("Failed to encode transparent PNG")

    corners = [{"x": int(round(x)), "y": int(round(y))} for x, y in inset_internal]
    return bytes(encoded_png.tobytes()), corners


def process_cyan_mask(
    image_bytes: bytes,
    *,
    lower_hsv: tuple[int, int, int] = (85, 100, 100),
    upper_hsv: tuple[int, int, int] = (95, 255, 255),
    min_area_ratio: float = 0.0025,
) -> tuple[bytes, list[tuple[int, int]]]:
    """Backward-compatible wrapper around process_and_map_cyan_mask()."""
    png_bytes, points = process_and_map_cyan_mask(
        image_bytes,
        lower_hsv=lower_hsv,
        upper_hsv=upper_hsv,
        min_area_ratio=min_area_ratio,
        negative_inset_px=0,
    )
    return png_bytes, [(int(p["x"]), int(p["y"])) for p in points]


class ChromakeyBridgeError(Exception):
    """Base exception for chromakey processing failures."""


class ChromakeyRegionNotFoundError(ChromakeyBridgeError):
    """Raised when no chromakey contour can be detected."""


class ChromakeyQuadError(ChromakeyBridgeError):
    """Raised when a valid 4-corner region cannot be derived."""


class ChromakeyBridgeService:
    """Detect, erase, and export chromakey region geometry for mockup bases."""

    APPROX_EPSILON_FACTORS: Final[tuple[float, ...]] = (
        0.010,
        0.012,
        0.015,
        0.020,
        0.028,
        0.038,
        0.050,
    )
    OPEN_KERNEL: Final[np.ndarray] = np.ones((3, 3), dtype=np.uint8)
    CLOSE_KERNEL: Final[np.ndarray] = np.ones((5, 5), dtype=np.uint8)

    @classmethod
    def extract_coordinates_and_erase(
        cls,
        *,
        image_path: str,
        hex_color: str = "#00FFCC",
        hue_tolerance: int = 12,
        min_area_ratio: float = 0.0025,
    ) -> list[dict[str, int]]:
        """Extract chromakey quad and convert keyed region to transparent alpha.

        Args:
            image_path: PNG/JPEG path produced by Gemini.
            hex_color: Target key color (default #00FFCC).
            hue_tolerance: Hue window tolerance around target HSV.
            min_area_ratio: Min contour area as ratio of image area.

        Returns:
            Ordered points in expected format: TL, TR, BR, BL.
            Example: [{"x":..,"y":..}, ...]
        """
        src_path = Path(image_path)
        if not src_path.exists():
            raise FileNotFoundError(f"Image not found: {src_path}")

        out_path = src_path.with_suffix(".png")
        image_bytes = src_path.read_bytes()
        lower, upper = cls._build_hsv_range(hex_color=hex_color, hue_tolerance=hue_tolerance)
        # March 2026 contract: edge-snapped + 2px negative inset for cyan cleanup.
        transparent_png_bytes, inset_corners = process_and_map_cyan_mask(
            image_bytes,
            lower_hsv=(int(lower[0]), int(lower[1]), int(lower[2])),
            upper_hsv=(int(upper[0]), int(upper[1]), int(upper[2])),
            min_area_ratio=min_area_ratio,
            negative_inset_px=2,
        )

        out_path.write_bytes(transparent_png_bytes)

        if out_path != src_path and src_path.exists():
            try:
                src_path.unlink()
            except Exception:
                pass

        return [{"x": int(point["x"]), "y": int(point["y"])} for point in inset_corners]

    @staticmethod
    def _build_hsv_range(*, hex_color: str, hue_tolerance: int) -> tuple[np.ndarray, np.ndarray]:
        raw = hex_color.strip().lstrip("#")
        if len(raw) != 6:
            raise ValueError(f"Invalid hex color: {hex_color}")

        r = int(raw[0:2], 16)
        g = int(raw[2:4], 16)
        b = int(raw[4:6], 16)

        bgr = np.array([[[b, g, r]]], dtype=np.uint8)
        hsv = cv2.cvtColor(cast(np.ndarray, bgr), cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = int(hsv[0]), int(hsv[1]), int(hsv[2])

        lower_h = max(0, h - int(hue_tolerance))
        upper_h = min(179, h + int(hue_tolerance))
        lower = np.array([lower_h, max(50, s - 120), max(50, v - 120)], dtype=np.uint8)
        upper = np.array([upper_h, 255, 255], dtype=np.uint8)
        return lower, upper

    @classmethod
    def _approximate_quad(cls, contour: np.ndarray) -> np.ndarray:
        perimeter = cv2.arcLength(contour, True)
        if perimeter <= 0:
            raise ChromakeyQuadError("Invalid contour perimeter.")

        for factor in cls.APPROX_EPSILON_FACTORS:
            epsilon = factor * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 4:
                return approx.reshape(4, 2).astype(np.float32)

        # Fallback to min area rectangle when contour is noisy but rectangular.
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        if box.shape == (4, 2):
            return box.astype(np.float32)

        raise ChromakeyQuadError("Could not resolve chromakey contour to 4 points.")

    @staticmethod
    def _order_points_tl_tr_br_bl(points: np.ndarray) -> list[tuple[float, float]]:
        if points.shape != (4, 2):
            raise ChromakeyQuadError("Point ordering requires shape (4, 2).")

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

        unique = {(round(x, 4), round(y, 4)) for x, y in ordered}
        if len(unique) != 4:
            raise ChromakeyQuadError("Derived corners are not unique.")

        return ordered

    @staticmethod
    def _apply_negative_inset(
        ordered_points: list[tuple[float, float]],
        *,
        inset_px: int,
    ) -> list[tuple[float, float]]:
        """Move each corner toward centroid by inset_px while preserving TL/TR/BR/BL order."""
        if inset_px <= 0:
            return ordered_points

        pts = np.array(ordered_points, dtype=np.float32)
        centroid = pts.mean(axis=0)
        inset_points: list[tuple[float, float]] = []

        for point in pts:
            direction = centroid - point
            distance = float(np.linalg.norm(direction))
            if distance <= 1e-6:
                inset_points.append((float(point[0]), float(point[1])))
                continue

            step = min(float(inset_px), max(0.0, distance - 1.0))
            moved = point + (direction / distance) * step
            inset_points.append((float(moved[0]), float(moved[1])))

        return inset_points
