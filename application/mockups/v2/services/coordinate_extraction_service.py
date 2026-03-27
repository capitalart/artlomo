"""Service B: CoordinateExtractionService (The Surveyor).

Performs deterministic OpenCV extraction of cyan fiducial corners and writes:
- coordinate JSON
- transparent PNG with marker region punched out (alpha=0)
"""

from __future__ import annotations

import json
from pathlib import Path

import cv2  # type: ignore
import numpy as np

from ..contracts import CoordinateExtractionInput, CoordinateExtractionResult
from ..exceptions import FailedDetectionError


class CoordinateExtractionService:
    """Extract a strict 4-point quadrilateral from cyan marker."""

    # HSV window for cyan marker (#00FFCC) with practical tolerance.
    HSV_LOWER = np.array([75, 80, 80], dtype=np.uint8)
    HSV_UPPER = np.array([100, 255, 255], dtype=np.uint8)

    def extract(self, request: CoordinateExtractionInput) -> CoordinateExtractionResult:
        source_path = Path(request.source_image_path)
        if not source_path.exists():
            raise FailedDetectionError(f"Source image not found: {source_path}")

        bgr = cv2.imread(str(source_path), cv2.IMREAD_COLOR)
        if bgr is None:
            raise FailedDetectionError(f"OpenCV could not load image: {source_path}")

        height, width = bgr.shape[:2]
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.HSV_LOWER, self.HSV_UPPER)

        kernel = np.ones((5, 5), dtype=np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise FailedDetectionError("FailedDetection: no cyan contour found")

        best = max(contours, key=cv2.contourArea)
        perimeter = cv2.arcLength(best, True)
        polygon = cv2.approxPolyDP(best, 0.02 * perimeter, True)

        if len(polygon) != 4:
            raise FailedDetectionError(
                f"FailedDetection: expected 4 corners, found {len(polygon)}"
            )

        points = polygon.reshape(4, 2).astype(np.float32)
        ordered = self._order_points(points)
        points_px = [
            {"x": int(round(pt[0])), "y": int(round(pt[1]))}
            for pt in ordered
        ]

        rgba = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
        polygon_int = np.array([[p["x"], p["y"]] for p in points_px], dtype=np.int32)
        cv2.fillConvexPoly(rgba[:, :, 3], polygon_int, 0)

        png_path = Path(request.output_png_path)
        json_path = Path(request.output_json_path)
        png_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.parent.mkdir(parents=True, exist_ok=True)

        if not cv2.imwrite(str(png_path), rgba):
            raise FailedDetectionError(f"Failed to write transparent PNG: {png_path}")

        payload = {
            "width": width,
            "height": height,
            "points": points_px,
            "point_order": ["TL", "TR", "BR", "BL"],
            "normalized_points": [
                {
                    "x": round(p["x"] / max(width, 1), 6),
                    "y": round(p["y"] / max(height, 1), 6),
                }
                for p in points_px
            ],
        }
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        return CoordinateExtractionResult(
            png_path=png_path,
            json_path=json_path,
            points_px=points_px,
            width=width,
            height=height,
        )

    @staticmethod
    def _order_points(points: np.ndarray) -> np.ndarray:
        """Order points clockwise as TL, TR, BR, BL."""

        s = points.sum(axis=1)
        diff = np.diff(points, axis=1).reshape(-1)

        top_left = points[np.argmin(s)]
        bottom_right = points[np.argmax(s)]
        top_right = points[np.argmin(diff)]
        bottom_left = points[np.argmax(diff)]

        return np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.float32)
