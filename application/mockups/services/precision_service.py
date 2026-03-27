from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class PrecisionGeometryResult:
    coordinates: dict[str, list[int]]
    used_fallback: bool
    reason: str


class PrecisionGeometryService:
    """Local OpenCV-only frame detection for Precision Mockups."""

    CANNY_LOW = 50
    CANNY_HIGH = 150
    BLUR_KERNEL = (5, 5)
    MORPH_KERNEL = np.ones((3, 3), dtype=np.uint8)
    APPROX_EPSILON_FACTORS = (0.010, 0.014, 0.018, 0.022, 0.028, 0.036, 0.048)

    @classmethod
    def detect_frame_geometry(cls, image_path: str | Path) -> dict[str, list[int]]:
        return cls.detect_frame_geometry_with_metadata(image_path).coordinates

    @classmethod
    def detect_frame_geometry_with_metadata(cls, image_path: str | Path) -> PrecisionGeometryResult:
        path_obj = Path(image_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Image not found: {path_obj}")

        image_bgr = cv2.imread(str(path_obj), cv2.IMREAD_COLOR)
        if image_bgr is None:
            raise ValueError(f"Unable to read image: {path_obj}")

        image_height, image_width = image_bgr.shape[:2]
        try:
            quad = cls._detect_quad(image_bgr)
            ordered = cls._order_points_tl_tr_br_bl(quad)
            return PrecisionGeometryResult(
                coordinates=cls._to_coordinate_dict(ordered),
                used_fallback=False,
                reason="detected_quadrilateral",
            )
        except Exception as exc:
            return PrecisionGeometryResult(
                coordinates=cls._fallback_center_wall_4x5(image_width, image_height),
                used_fallback=True,
                reason=str(exc) or "fallback_center_wall_4x5",
            )

    @classmethod
    def _detect_quad(cls, image_bgr: np.ndarray) -> np.ndarray:
        image_height, image_width = image_bgr.shape[:2]
        grayscale = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayscale, cls.BLUR_KERNEL, 0)
        edges = cv2.Canny(blurred, cls.CANNY_LOW, cls.CANNY_HIGH)
        edges = cv2.dilate(edges, cls.MORPH_KERNEL, iterations=1)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, cls.MORPH_KERNEL, iterations=2)

        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise ValueError("No contours found after Canny edge detection")

        image_area = float(image_width * image_height)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for contour in sorted_contours:
            area = float(cv2.contourArea(contour))
            if area <= 0:
                continue
            if image_area > 0 and area >= image_area * 0.97:
                continue

            perimeter = cv2.arcLength(contour, True)
            if perimeter <= 0:
                continue

            for epsilon_factor in cls.APPROX_EPSILON_FACTORS:
                approx = cv2.approxPolyDP(contour, epsilon_factor * perimeter, True)
                if len(approx) != 4:
                    continue
                points = approx.reshape(4, 2).astype(np.float32)
                if not cls._is_reasonable_quad(points, image_width, image_height):
                    continue
                return points

        raise ValueError("No 4-point frame contour detected")

    @staticmethod
    def _is_reasonable_quad(points: np.ndarray, image_width: int, image_height: int) -> bool:
        contour = points.reshape((-1, 1, 2)).astype(np.float32)
        area = abs(float(cv2.contourArea(contour)))
        image_area = float(max(1, image_width * image_height))
        if area < image_area * 0.03:
            return False
        if area > image_area * 0.90:
            return False
        xs = points[:, 0]
        ys = points[:, 1]
        if xs.max() - xs.min() < image_width * 0.10:
            return False
        if ys.max() - ys.min() < image_height * 0.10:
            return False
        return True

    @staticmethod
    def _order_points_tl_tr_br_bl(points: np.ndarray) -> np.ndarray:
        ordered = np.zeros((4, 2), dtype=np.float32)
        point_sums = points.sum(axis=1)
        point_diffs = np.diff(points, axis=1).reshape(-1)

        ordered[0] = points[np.argmin(point_sums)]
        ordered[2] = points[np.argmax(point_sums)]
        ordered[1] = points[np.argmin(point_diffs)]
        ordered[3] = points[np.argmax(point_diffs)]
        return ordered

    @staticmethod
    def _to_coordinate_dict(points: np.ndarray) -> dict[str, list[int]]:
        labels = ("tl", "tr", "br", "bl")
        return {
            label: [int(round(point[0])), int(round(point[1]))]
            for label, point in zip(labels, points)
        }

    @staticmethod
    def _fallback_center_wall_4x5(image_width: int, image_height: int) -> dict[str, list[int]]:
        max_width = image_width * 0.54
        max_height = image_height * 0.68

        width = min(max_width, max_height * (4.0 / 5.0))
        height = width * (5.0 / 4.0)

        center_x = image_width / 2.0
        center_y = image_height / 2.0

        left = int(round(center_x - (width / 2.0)))
        right = int(round(center_x + (width / 2.0)))
        top = int(round(center_y - (height / 2.0)))
        bottom = int(round(center_y + (height / 2.0)))

        return {
            "tl": [left, top],
            "tr": [right, top],
            "br": [right, bottom],
            "bl": [left, bottom],
        }