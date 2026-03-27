from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from application.mockups.services.MockupCoordinateService import (
    CyanQuadNotFoundError,
    MockupCoordinateService,
)
from application.mockups.services.chromakey_bridge_service import process_and_map_cyan_mask


def _write_test_image(path: Path, bgr_image: np.ndarray) -> None:
    ok = cv2.imwrite(str(path), bgr_image)
    assert ok, "Failed to write test image"


def test_extract_coordinates_detects_relaxed_cyan_placeholder(tmp_path):
    image_path = tmp_path / "relaxed-cyan.png"

    canvas = np.zeros((512, 512, 3), dtype=np.uint8)
    # Slightly off #00FFFF to mimic model color drift while still cyan-like.
    off_cyan_bgr = np.array([200, 235, 12], dtype=np.uint8)
    cv2.rectangle(canvas, (90, 110), (420, 430), off_cyan_bgr.tolist(), thickness=-1)

    _write_test_image(image_path, canvas)

    points = MockupCoordinateService.extract_coordinates(str(image_path))

    assert len(points) == 4
    xs = [point["x"] for point in points]
    ys = [point["y"] for point in points]
    assert min(xs) <= 100
    assert max(xs) >= 410
    assert min(ys) <= 120
    assert max(ys) >= 420


def test_extract_coordinates_raises_when_no_cyan_present(tmp_path):
    image_path = tmp_path / "no-cyan.png"

    canvas = np.zeros((256, 256, 3), dtype=np.uint8)
    cv2.rectangle(canvas, (40, 40), (200, 200), (255, 0, 255), thickness=-1)
    _write_test_image(image_path, canvas)

    with pytest.raises(CyanQuadNotFoundError):
        MockupCoordinateService.extract_coordinates(str(image_path))


def test_extract_coordinates_detects_transparent_alpha_cutout(tmp_path):
    """Legacy uploaded bases use a transparent cutout; service must handle both formats."""
    image_path = tmp_path / "transparent-cutout.png"

    # 4-channel BGRA: opaque grey background with a rectangular transparent hole.
    canvas = np.full((512, 512, 4), (180, 180, 180, 255), dtype=np.uint8)
    canvas[110:430, 90:420, 3] = 0  # transparent artwork area

    ok = cv2.imwrite(str(image_path), canvas)
    assert ok, "Failed to write BGRA test image"

    points = MockupCoordinateService.extract_coordinates(str(image_path))

    assert len(points) == 4
    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    assert min(xs) <= 100
    assert max(xs) >= 410
    assert min(ys) <= 120
    assert max(ys) >= 420


def test_process_and_map_cyan_mask_returns_transparent_png_and_inset_points():
    canvas = np.full((512, 512, 3), (40, 40, 40), dtype=np.uint8)
    # #00FFCC in BGR
    chromakey_bgr = (204, 255, 0)
    cv2.rectangle(canvas, (110, 130), (410, 420), chromakey_bgr, thickness=-1)

    ok, encoded = cv2.imencode(".png", canvas)
    assert ok

    transparent_png_bytes, points = process_and_map_cyan_mask(
        bytes(encoded.tobytes()),
        negative_inset_px=2,
    )

    assert len(points) == 4

    decoded = cv2.imdecode(np.frombuffer(transparent_png_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    assert decoded is not None
    assert decoded.shape[2] == 4

    xs = [int(p["x"]) for p in points]
    ys = [int(p["y"]) for p in points]

    # Inset should keep coordinates inside the original mask bounds.
    assert min(xs) >= 110
    assert max(xs) <= 410
    assert min(ys) >= 130
    assert max(ys) <= 420

    # Center of masked area should be transparent.
    alpha_center = int(decoded[275, 260, 3])
    assert alpha_center == 0


def test_process_and_map_cyan_mask_uses_black_outer_cutout_and_inner_coordinates():
    canvas = np.full((512, 512, 3), (110, 110, 110), dtype=np.uint8)
    black = (0, 0, 0)
    cyan = (255, 255, 0)  # bright cyan in BGR, safely inside default HSV window

    # Triple-border target: black-cyan-black around inner artwork zone.
    cv2.rectangle(canvas, (100, 110), (420, 430), black, thickness=-1)   # outer black guard
    cv2.rectangle(canvas, (120, 130), (400, 410), cyan, thickness=-1)    # cyan ring
    cv2.rectangle(canvas, (150, 160), (370, 380), black, thickness=-1)   # inner black guard
    cv2.rectangle(canvas, (180, 190), (340, 350), (45, 90, 180), thickness=-1)  # artwork core

    ok, encoded = cv2.imencode(".png", canvas)
    assert ok

    transparent_png_bytes, points = process_and_map_cyan_mask(
        bytes(encoded.tobytes()),
        negative_inset_px=2,
    )

    assert len(points) == 4

    decoded = cv2.imdecode(np.frombuffer(transparent_png_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    assert decoded is not None
    assert decoded.shape[2] == 4

    xs = [int(p["x"]) for p in points]
    ys = [int(p["y"]) for p in points]

    # Coordinates should track inner black boundary (plus small negative inset).
    assert min(xs) >= 150
    assert max(xs) <= 370
    assert min(ys) >= 160
    assert max(ys) <= 380

    # Cutout should follow external boundary, clearing the cyan ring and inner area.
    assert int(decoded[120, 120, 3]) == 0
    assert int(decoded[250, 250, 3]) == 0
    assert int(decoded[80, 80, 3]) == 255
