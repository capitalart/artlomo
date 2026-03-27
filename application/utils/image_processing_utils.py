from __future__ import annotations

from typing import Sequence

import cv2
import numpy as np
from PIL import Image


class PerspectiveTransformError(RuntimeError):
    pass


def _pil_to_bgra(image: Image.Image) -> np.ndarray:
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    arr = np.array(image)
    return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)


def _bgra_to_pil(arr: np.ndarray) -> Image.Image:
    rgba = cv2.cvtColor(arr, cv2.COLOR_BGRA2RGBA)
    return Image.fromarray(rgba, mode="RGBA")


def _order_points(pts: np.ndarray) -> np.ndarray:
    if pts.shape != (4, 2):
        raise PerspectiveTransformError("Perspective points must be 4x2")

    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1).reshape(4)

    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]

    return np.array([tl, tr, br, bl], dtype=np.float32)


def _try_axis_aligned_rect(ordered_tl_tr_br_bl: np.ndarray, *, eps: float = 0.5) -> tuple[int, int, int, int] | None:
    tl, tr, br, bl = ordered_tl_tr_br_bl
    if abs(float(tl[1]) - float(tr[1])) > eps:
        return None
    if abs(float(bl[1]) - float(br[1])) > eps:
        return None
    if abs(float(tl[0]) - float(bl[0])) > eps:
        return None
    if abs(float(tr[0]) - float(br[0])) > eps:
        return None

    x = int(round(float(tl[0])))
    y = int(round(float(tl[1])))
    w = int(round(float(tr[0]) - float(tl[0])))
    h = int(round(float(bl[1]) - float(tl[1])))
    if w <= 0 or h <= 0:
        return None
    return x, y, w, h


def warp_image_to_quad(
    image: Image.Image,
    dst_points: Sequence[Sequence[float]],
    output_size: tuple[int, int],
) -> Image.Image:
    try:
        width, height = int(output_size[0]), int(output_size[1])
        if width <= 0 or height <= 0:
            raise PerspectiveTransformError("Output size must be positive")

        pts = np.array(dst_points, dtype=np.float32)
        ordered = _order_points(pts)

        rect = _try_axis_aligned_rect(ordered)
        if rect is not None:
            x, y, w, h = rect
            safe_w = max(1, min(int(w), int(width)))
            safe_h = max(1, min(int(h), int(height)))
            x0 = max(0, min(int(x), int(width - 1)))
            y0 = max(0, min(int(y), int(height - 1)))

            if image.mode != "RGBA":
                image = image.convert("RGBA")
            resample = getattr(getattr(Image, "Resampling", None), "LANCZOS", Image.Resampling.LANCZOS)
            stretched = image.resize((safe_w, safe_h), resample=resample)

            layer = Image.new("RGBA", (int(width), int(height)), (0, 0, 0, 0))
            layer.paste(stretched, (x0, y0), mask=stretched.split()[3])
            return layer

        src_bgra = _pil_to_bgra(image)
        src_h, src_w = src_bgra.shape[:2]
        if src_w <= 0 or src_h <= 0:
            raise PerspectiveTransformError("Source image has invalid dimensions")

        src_rect = np.array(
            [
                [0.0, 0.0],
                [float(src_w - 1), 0.0],
                [float(src_w - 1), float(src_h - 1)],
                [0.0, float(src_h - 1)],
            ],
            dtype=np.float32,
        )

        matrix = cv2.getPerspectiveTransform(src_rect, ordered)
        warped = cv2.warpPerspective(
            src_bgra,
            matrix,
            (width, height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0, 0),
        )
        return _bgra_to_pil(warped)
    except PerspectiveTransformError:
        raise
    except Exception as exc:  # pylint: disable=broad-except
        raise PerspectiveTransformError("Failed to warp image") from exc
