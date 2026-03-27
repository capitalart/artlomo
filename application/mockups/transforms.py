"""Perspective transforms for mockup compositing."""

from __future__ import annotations

from typing import Tuple

import cv2
import numpy as np
from PIL import Image

from .config import BORDER_MODE, PERSPECTIVE_INTERPOLATION
from .errors import TransformError
from .models import RegionPlacement

_INTERP_MAP = {
    "linear": cv2.INTER_LINEAR,
}

_BORDER_MAP = {
    "constant": cv2.BORDER_CONSTANT,
}


def _pil_to_bgra(image: Image.Image) -> np.ndarray:
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    arr = np.array(image)
    return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)


def _bgra_to_pil(arr: np.ndarray) -> Image.Image:
    rgba = cv2.cvtColor(arr, cv2.COLOR_BGRA2RGBA)
    return Image.fromarray(rgba, mode="RGBA")


def _try_axis_aligned_rect(placement: RegionPlacement) -> tuple[int, int, int, int] | None:
    corners = placement.corners
    if len(corners) != 4:
        return None

    tl, tr, bl, br = corners

    eps = 0.5
    if abs(tl.y - tr.y) > eps:
        return None
    if abs(bl.y - br.y) > eps:
        return None
    if abs(tl.x - bl.x) > eps:
        return None
    if abs(tr.x - br.x) > eps:
        return None

    x = int(round(tl.x))
    y = int(round(tl.y))
    w = int(round(tr.x - tl.x))
    h = int(round(bl.y - tl.y))
    if w <= 0 or h <= 0:
        return None
    return x, y, w, h


def build_perspective_matrix(src_rect: Tuple[Tuple[float, float], ...], dst_quad: Tuple[Tuple[float, float], ...]) -> np.ndarray:
    try:
        src = np.array(src_rect, dtype=np.float32)
        dst = np.array(dst_quad, dtype=np.float32)
        if src.shape != (4, 2) or dst.shape != (4, 2):
            raise ValueError("Perspective points must be 4x2")
        return cv2.getPerspectiveTransform(src, dst)
    except Exception as exc:  # pylint: disable=broad-except
        raise TransformError("Failed to compute perspective matrix") from exc


def _pillow_perspective_coeffs(
    *,
    src_quad: Tuple[Tuple[float, float], ...],
    dst_quad: Tuple[Tuple[float, float], ...],
) -> Tuple[float, ...]:
    try:
        if len(src_quad) != 4 or len(dst_quad) != 4:
            raise ValueError("Perspective points must contain 4 corners")

        matrix = []
        vector = []
        for (x, y), (u, v) in zip(dst_quad, src_quad):
            matrix.append([x, y, 1.0, 0.0, 0.0, 0.0, -u * x, -u * y])
            matrix.append([0.0, 0.0, 0.0, x, y, 1.0, -v * x, -v * y])
            vector.append(u)
            vector.append(v)

        a = np.array(matrix, dtype=np.float64)
        b = np.array(vector, dtype=np.float64)
        res = np.linalg.solve(a, b)
        return tuple(float(x) for x in res)
    except Exception as exc:  # pylint: disable=broad-except
        raise TransformError("Failed to compute Pillow perspective coefficients") from exc


def warp_artwork_to_region(artwork: Image.Image, placement: RegionPlacement, base_size: Tuple[int, int]) -> Image.Image:
    width, height = base_size
    try:
        rect = _try_axis_aligned_rect(placement)
        if rect is not None:
            x, y, w, h = rect
            safe_w = max(1, min(int(w), int(width)))
            safe_h = max(1, min(int(h), int(height)))
            x0 = max(0, min(int(x), int(width - 1)))
            y0 = max(0, min(int(y), int(height - 1)))

            if artwork.mode != "RGBA":
                artwork = artwork.convert("RGBA")
            resample = getattr(getattr(Image, "Resampling", None), "LANCZOS", Image.Resampling.LANCZOS)
            stretched = artwork.resize((safe_w, safe_h), resample=resample)

            layer = Image.new("RGBA", (int(width), int(height)), (0, 0, 0, 0))
            layer.paste(stretched, (x0, y0), mask=stretched.split()[3])
            return layer

        if artwork.mode != "RGBA":
            artwork = artwork.convert("RGBA")

        src_w, src_h = artwork.size
        src_quad = (
            (0.0, 0.0),
            (float(src_w - 1), 0.0),
            (float(src_w - 1), float(src_h - 1)),
            (0.0, float(src_h - 1)),
        )

        corners = placement.corners
        dst_quad = (
            (float(corners[0].x), float(corners[0].y)),
            (float(corners[1].x), float(corners[1].y)),
            (float(corners[2].x), float(corners[2].y)),
            (float(corners[3].x), float(corners[3].y)),
        )

        coeffs = _pillow_perspective_coeffs(src_quad=src_quad, dst_quad=dst_quad)
        resample = getattr(getattr(Image, "Resampling", None), "BICUBIC", Image.Resampling.BICUBIC)
        transformed = artwork.transform(
            (int(width), int(height)),
            Image.Transform.PERSPECTIVE,
            coeffs,
            resample=resample,
            fillcolor=(0, 0, 0, 0),
        )
        return transformed
    except TransformError:
        raise
    except Exception as exc:  # pylint: disable=broad-except
        raise TransformError("Failed to warp artwork to placement quad") from exc
