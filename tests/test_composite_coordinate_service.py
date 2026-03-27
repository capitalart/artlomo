from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from application.mockups.services.CompositeCoordinateService import CompositeCoordinateService


def _write_image(path: Path, bgr_image: np.ndarray) -> None:
    ok = cv2.imwrite(str(path), bgr_image)
    assert ok, "Failed to write test image"


def test_extract_coordinates_accepts_softened_dark_tinted_inner_band(tmp_path):
    image_path = tmp_path / "soft-dark-band.png"

    canvas = np.full((1100, 800, 3), 180, dtype=np.uint8)
    x0, y0, x1, y1 = 140, 140, 660, 960

    cv2.rectangle(canvas, (x0, y0), (x1, y1), (255, 255, 0), thickness=30)
    cv2.rectangle(canvas, (x0 + 30, y0 + 30), (x1 - 30, y1 - 30), (50, 70, 110), thickness=30)
    cv2.rectangle(canvas, (x0 + 60, y0 + 60), (x1 - 60, y1 - 60), (140, 170, 180), thickness=-1)

    softened = cv2.GaussianBlur(canvas, (7, 7), 1.5)
    _write_image(image_path, softened)

    points = CompositeCoordinateService.extract_coordinates_and_erase(str(image_path))

    assert len(points) == 4
    xs = [point["x"] for point in points]
    ys = [point["y"] for point in points]
    assert min(xs) < 140
    assert max(xs) > 660
    assert min(ys) < 140
    assert max(ys) > 960