from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from application.mockups.services.precision_service import PrecisionGeometryService


def test_detect_frame_geometry_finds_black_frame(tmp_path: Path) -> None:
    image = np.full((1024, 1024, 3), 255, dtype=np.uint8)
    cv2.rectangle(image, (280, 180), (760, 780), (20, 20, 20), thickness=28)
    image_path = tmp_path / "precision-frame.png"
    cv2.imwrite(str(image_path), image)

    coords = PrecisionGeometryService.detect_frame_geometry(image_path)

    assert coords["tl"][0] < 340
    assert coords["tl"][1] < 240
    assert coords["tr"][0] > 700
    assert coords["br"][1] > 720


def test_detect_frame_geometry_falls_back_when_no_quad(tmp_path: Path) -> None:
    image = np.full((1000, 1000, 3), 245, dtype=np.uint8)
    image_path = tmp_path / "precision-blank.png"
    cv2.imwrite(str(image_path), image)

    result = PrecisionGeometryService.detect_frame_geometry_with_metadata(image_path)

    assert result.used_fallback is True
    assert set(result.coordinates.keys()) == {"tl", "tr", "br", "bl"}
    width = result.coordinates["tr"][0] - result.coordinates["tl"][0]
    height = result.coordinates["bl"][1] - result.coordinates["tl"][1]
    assert height > width