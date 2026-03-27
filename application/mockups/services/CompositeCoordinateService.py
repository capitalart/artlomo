"""Composite coordinate extraction and in-place erasure service.

This service powers the Trojan Art generation mode. It:
1) Detects the cyan fiducial stripe contour in a generated image.
2) Approximates and orders the contour corners (TL, TR, BR, BL).
3) Expands the quad outward to target the full black/cyan/black border envelope.
4) Erases the expanded polygon area by writing alpha=0 to produce a reusable
   transparent-window PNG base.

The existing MockupCoordinateService remains unchanged and continues to support
standard generation mode.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Final

import cv2
import numpy as np


class CompositeCoordinateServiceError(Exception):
    """Base exception for composite coordinate extraction failures."""


class CompositeCyanContourNotFoundError(CompositeCoordinateServiceError):
    """Raised when no cyan fiducial contour can be detected."""


class CompositeInvalidQuadError(CompositeCoordinateServiceError):
    """Raised when the cyan contour cannot be reduced to a valid quad."""


class CompositeCoordinateService:
    """Extracts cyan fiducial coordinates and erases the interior region to alpha."""

    # Strict + relaxed cyan windows to handle lighting drift.
    CYAN_HSV_RANGES: Final[tuple[tuple[np.ndarray, np.ndarray], ...]] = (
        (
            np.array([86, 160, 120], dtype=np.uint8),
            np.array([96, 255, 255], dtype=np.uint8),
        ),
        (
            np.array([78, 90, 60], dtype=np.uint8),
            np.array([104, 255, 255], dtype=np.uint8),
        ),
    )

    OPEN_KERNEL: Final[np.ndarray] = np.ones((3, 3), dtype=np.uint8)
    CLOSE_KERNEL: Final[np.ndarray] = np.ones((5, 5), dtype=np.uint8)

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

    BORDER_EXPANSION_PX: Final[float] = 20.0
    BLACK_MAX_VALUE: Final[int] = 135
    BLACK_MAX_SATURATION: Final[int] = 165
    BLACK_SAMPLE_OFFSET_MIN_PX: Final[float] = 1.0
    BLACK_SAMPLE_OFFSET_MAX_PX: Final[float] = 6.0
    EDGE_SAMPLE_COUNT: Final[int] = 20
    MIN_BLACK_EDGE_RATIO: Final[float] = 0.55
    MIN_CYAN_EDGE_RATIO: Final[float] = 0.76
    BLACK_SAMPLE_FACTORS: Final[tuple[float, ...]] = (0.14, 0.24, 0.36)

    @classmethod
    def extract_coordinates_and_erase(cls, image_path: str) -> list[dict[str, int]]:
        """Extract expanded quad coordinates and erase that region to transparency.

        The output image is always written as PNG. If the source extension is not
        .png, the original file is removed and replaced by a same-stem .png.

        Args:
            image_path: Path to generated image.

        Returns:
            Ordered corners for the expanded polygon as:
            [TL, TR, BR, BL] with integer coordinates.

        Raises:
            FileNotFoundError: If image path does not exist.
            ValueError: If the image cannot be decoded.
            CompositeCyanContourNotFoundError: If no cyan contour is found.
            CompositeInvalidQuadError: If contour cannot be reduced to a quad.
        """
        src_path = Path(image_path)
        if not src_path.exists():
            raise FileNotFoundError(f"Image not found: {src_path}")

        bgr = cv2.imread(str(src_path), cv2.IMREAD_COLOR)
        if bgr is None:
            raise ValueError(f"Unable to read image: {src_path}")

        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        outer_contour, inner_contour = cls._find_cyan_ring_contours(hsv)
        outer_quad = cls._approximate_quad_points(outer_contour)
        inner_quad = cls._approximate_quad_points(inner_contour)
        ordered = cls._order_points_tl_tr_br_bl(outer_quad)
        ordered_inner = cls._order_points_tl_tr_br_bl(inner_quad)
        cls._validate_black_cyan_black_structure(hsv, ordered_outer=ordered, ordered_inner=ordered_inner)
        rgba = cls._load_rgba(src_path)
        expanded = cls._expand_quad_outward(ordered, pixels=cls.BORDER_EXPANSION_PX)
        clamped = cls._clamp_polygon_to_image_bounds(expanded, width=rgba.shape[1], height=rgba.shape[0])

        erased = cls._erase_polygon_rgba(rgba, clamped)
        cls._write_png_overwrite(src_path, erased)

        return [
            {"x": int(round(x)), "y": int(round(y))}
            for x, y in clamped
        ]

    @classmethod
    def _find_cyan_ring_contours(cls, hsv: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        best_outer: np.ndarray | None = None
        best_inner: np.ndarray | None = None
        best_outer_area = 0.0

        for lower, upper in cls.CYAN_HSV_RANGES:
            mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cls.OPEN_KERNEL, iterations=1)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cls.CLOSE_KERNEL, iterations=2)

            contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            if not contours or hierarchy is None:
                continue

            h = hierarchy[0]
            for idx, contour in enumerate(contours):
                # We only care about top-level contours (possible cyan outer ring edges).
                if int(h[idx][3]) != -1:
                    continue
                outer_area = float(cv2.contourArea(contour))
                if outer_area <= 0:
                    continue

                # Find the largest direct child hole contour (inner cyan edge).
                child = int(h[idx][2])
                if child == -1:
                    continue

                inner_best_idx = -1
                inner_best_area = 0.0
                while child != -1:
                    child_area = float(cv2.contourArea(contours[child]))
                    if child_area > inner_best_area:
                        inner_best_area = child_area
                        inner_best_idx = child
                    child = int(h[child][0])

                if inner_best_idx == -1 or inner_best_area <= 0:
                    continue

                if outer_area > best_outer_area:
                    best_outer_area = outer_area
                    best_outer = contour
                    best_inner = contours[inner_best_idx]

            if best_outer is not None and best_inner is not None:
                break

        if best_outer is None or best_inner is None:
            raise CompositeCyanContourNotFoundError(
                "No cyan fiducial ring detected (expected black-cyan-black bordered artwork guide)."
            )

        return best_outer, best_inner

    @classmethod
    def _validate_black_cyan_black_structure(
        cls,
        hsv: np.ndarray,
        *,
        ordered_outer: list[tuple[float, float]],
        ordered_inner: list[tuple[float, float]],
    ) -> None:
        if len(ordered_outer) != 4 or len(ordered_inner) != 4:
            raise CompositeInvalidQuadError("Border validation requires 4 outer and 4 inner points.")

        # Validate color bands around each edge using adaptive offsets.
        # The generated scene can scale/perspective-warp the ring, so we do not
        # enforce an absolute pixel thickness in output space.
        centroid = (
            float(sum(p[0] for p in ordered_outer) / 4.0),
            float(sum(p[1] for p in ordered_outer) / 4.0),
        )
        for i in range(4):
            outer_a = ordered_outer[i]
            outer_b = ordered_outer[(i + 1) % 4]
            inner_a = ordered_inner[i]
            inner_b = ordered_inner[(i + 1) % 4]

            cyan_ok = 0
            black_inner_ok = 0

            for step in range(1, cls.EDGE_SAMPLE_COUNT + 1):
                t = step / float(cls.EDGE_SAMPLE_COUNT + 1)
                po = cls._lerp(outer_a, outer_b, t)
                pi = cls._lerp(inner_a, inner_b, t)
                local_thickness = math.hypot(po[0] - pi[0], po[1] - pi[1])
                if local_thickness < 1.0:
                    continue

                inward_vec = cls._unit_vector((centroid[0] - po[0], centroid[1] - po[1]))

                # Cyan sample (midpoint between outer and inner cyan boundaries).
                cyan_p = ((po[0] + pi[0]) * 0.5, (po[1] + pi[1]) * 0.5)
                if cls._is_cyan_hsv(cls._sample_hsv(hsv, cyan_p)):
                    cyan_ok += 1

                # Inner dark-band samples (inside cyan inner edge toward artwork content).
                # Generated scenes often soften or slightly tint the nominal black band,
                # so validate a short run of inward samples instead of one brittle point.
                inward_from_inner = cls._unit_vector((centroid[0] - pi[0], centroid[1] - pi[1]))
                if cls._edge_has_dark_inner_band(
                    hsv,
                    inner_point=pi,
                    inward_vector=inward_from_inner,
                    local_thickness=local_thickness,
                ):
                    black_inner_ok += 1

            required = int(math.ceil(cls.EDGE_SAMPLE_COUNT * cls.MIN_BLACK_EDGE_RATIO))
            required_cyan = int(math.ceil(cls.EDGE_SAMPLE_COUNT * cls.MIN_CYAN_EDGE_RATIO))
            if cyan_ok < required_cyan:
                raise CompositeInvalidQuadError(
                    "Outer 30px cyan border validation failed for fiducial guide."
                )
            if black_inner_ok < required:
                raise CompositeInvalidQuadError(
                    "Inner 30px black border validation failed for fiducial guide."
                )

    @staticmethod
    def _lerp(a: tuple[float, float], b: tuple[float, float], t: float) -> tuple[float, float]:
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    @staticmethod
    def _unit_vector(v: tuple[float, float]) -> tuple[float, float]:
        length = math.hypot(v[0], v[1])
        if length <= 1e-6:
            return (0.0, 0.0)
        return (v[0] / length, v[1] / length)

    @staticmethod
    def _sample_hsv(hsv: np.ndarray, p: tuple[float, float]) -> tuple[int, int, int]:
        h, w = hsv.shape[:2]
        x = int(round(p[0]))
        y = int(round(p[1]))
        x = min(max(x, 0), w - 1)
        y = min(max(y, 0), h - 1)
        px = hsv[y, x]
        return int(px[0]), int(px[1]), int(px[2])

    @classmethod
    def _edge_has_dark_inner_band(
        cls,
        hsv: np.ndarray,
        *,
        inner_point: tuple[float, float],
        inward_vector: tuple[float, float],
        local_thickness: float,
    ) -> bool:
        for factor in cls.BLACK_SAMPLE_FACTORS:
            sample_offset = max(
                cls.BLACK_SAMPLE_OFFSET_MIN_PX,
                min(cls.BLACK_SAMPLE_OFFSET_MAX_PX, local_thickness * factor),
            )
            sample_point = (
                inner_point[0] + inward_vector[0] * sample_offset,
                inner_point[1] + inward_vector[1] * sample_offset,
            )
            if cls._is_black_hsv(cls._sample_hsv(hsv, sample_point)):
                return True
        return False

    @classmethod
    def _is_black_hsv(cls, px: tuple[int, int, int]) -> bool:
        _h, s, v = px
        return v <= cls.BLACK_MAX_VALUE and s <= cls.BLACK_MAX_SATURATION

    @classmethod
    def _is_cyan_hsv(cls, px: tuple[int, int, int]) -> bool:
        h, s, v = px
        for lower, upper in cls.CYAN_HSV_RANGES:
            if int(lower[0]) <= h <= int(upper[0]) and int(lower[1]) <= s <= int(upper[1]) and int(lower[2]) <= v <= int(upper[2]):
                return True
        return False

    @classmethod
    def _approximate_quad_points(cls, contour: np.ndarray) -> np.ndarray:
        perimeter = cv2.arcLength(contour, True)
        if perimeter <= 0:
            raise CompositeInvalidQuadError("Contour perimeter is zero.")

        best_candidate: np.ndarray | None = None
        best_distance = math.inf

        for eps_factor in cls.APPROX_EPSILON_FACTORS:
            approx = cv2.approxPolyDP(contour, eps_factor * perimeter, True)
            point_count = len(approx)
            if point_count == 4:
                return approx.reshape(4, 2).astype(np.float32)

            distance = abs(point_count - 4)
            if distance < best_distance:
                best_distance = distance
                best_candidate = approx

        candidate_count = len(best_candidate) if best_candidate is not None else 0
        raise CompositeInvalidQuadError(
            "Could not approximate cyan contour to 4 points "
            f"(closest candidate had {candidate_count} points)."
        )

    @staticmethod
    def _order_points_tl_tr_br_bl(points: np.ndarray) -> list[tuple[float, float]]:
        if points.shape != (4, 2):
            raise CompositeInvalidQuadError("Point ordering requires shape (4, 2).")

        # Robust ordering for perspective quads that avoids sum/diff tie collisions.
        x_sorted = points[np.argsort(points[:, 0]), :]
        left_most = x_sorted[:2, :]
        right_most = x_sorted[2:, :]

        left_most = left_most[np.argsort(left_most[:, 1]), :]
        tl = left_most[0]
        bl = left_most[1]

        distances = np.linalg.norm(right_most - tl, axis=1)
        br = right_most[int(np.argmax(distances))]
        tr = right_most[int(np.argmin(distances))]

        ordered = [
            (float(tl[0]), float(tl[1])),
            (float(tr[0]), float(tr[1])),
            (float(br[0]), float(br[1])),
            (float(bl[0]), float(bl[1])),
        ]

        unique_points = {(round(x, 4), round(y, 4)) for x, y in ordered}
        if len(unique_points) != 4:
            raise CompositeInvalidQuadError("Failed to derive 4 unique ordered points.")

        return ordered

    @classmethod
    def _expand_quad_outward(
        cls,
        ordered_points: list[tuple[float, float]],
        *,
        pixels: float,
    ) -> list[tuple[float, float]]:
        """Expand quad corners radially from centroid by a fixed pixel distance."""
        pts = np.array(ordered_points, dtype=np.float32)
        cx = float(np.mean(pts[:, 0]))
        cy = float(np.mean(pts[:, 1]))

        expanded: list[tuple[float, float]] = []
        for x, y in ordered_points:
            dx = x - cx
            dy = y - cy
            norm = math.hypot(dx, dy)
            if norm < 1e-6:
                expanded.append((x, y))
                continue
            ux = dx / norm
            uy = dy / norm
            expanded.append((x + ux * pixels, y + uy * pixels))

        return expanded

    @staticmethod
    def _load_rgba(path: Path) -> np.ndarray:
        bgra = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if bgra is None:
            raise ValueError(f"Unable to read image for erasure: {path}")

        if bgra.ndim == 2:
            # grayscale -> BGRA
            bgra = cv2.cvtColor(bgra, cv2.COLOR_GRAY2BGRA)
        elif bgra.shape[2] == 3:
            bgra = cv2.cvtColor(bgra, cv2.COLOR_BGR2BGRA)
        elif bgra.shape[2] != 4:
            raise ValueError(f"Unsupported channel count for image: {path}")

        return bgra

    @staticmethod
    def _clamp_polygon_to_image_bounds(
        polygon: list[tuple[float, float]],
        *,
        width: int,
        height: int,
    ) -> list[tuple[float, float]]:
        """Clamp polygon coordinates so they are always within image bounds."""
        if width <= 0 or height <= 0:
            raise ValueError("Image dimensions must be positive for coordinate clamping.")

        max_x = float(width - 1)
        max_y = float(height - 1)
        return [
            (min(max(float(x), 0.0), max_x), min(max(float(y), 0.0), max_y))
            for x, y in polygon
        ]

    @staticmethod
    def _erase_polygon_rgba(bgra: np.ndarray, polygon: list[tuple[float, float]]) -> np.ndarray:
        out = bgra.copy()
        h, w = out.shape[:2]

        pts = np.array(
            [[int(round(x)), int(round(y))] for x, y in polygon],
            dtype=np.int32,
        )
        pts[:, 0] = np.clip(pts[:, 0], 0, w - 1)
        pts[:, 1] = np.clip(pts[:, 1], 0, h - 1)

        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillConvexPoly(mask, pts, 255)

        # Zero alpha (transparent) in the polygon area.
        out[mask == 255, 3] = 0
        return out

    @staticmethod
    def _write_png_overwrite(src_path: Path, bgra: np.ndarray) -> None:
        target = src_path.with_suffix(".png")
        ok = cv2.imwrite(str(target), bgra)
        if not ok:
            raise ValueError(f"Failed to write PNG output: {target}")

        if target != src_path and src_path.exists():
            src_path.unlink(missing_ok=True)
