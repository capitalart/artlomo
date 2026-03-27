"""Service D: CompositeRenderService (The Builder)."""

from __future__ import annotations

import json
from pathlib import Path

import cv2  # type: ignore
import numpy as np

from ..contracts import RenderCompositeInput, RenderCompositeResult
from ..exceptions import CompositeRenderError


class CompositeRenderService:
    """Warp artwork by homography and composite into transparent base."""

    def render(self, request: RenderCompositeInput) -> RenderCompositeResult:
        artwork_path = Path(request.artwork_path)
        base_path = Path(request.base_png_path)
        coords_path = Path(request.coordinates_json_path)
        output_path = Path(request.output_jpeg_path)

        if not artwork_path.exists() or not base_path.exists() or not coords_path.exists():
            raise CompositeRenderError("Required input files are missing")

        artwork = cv2.imread(str(artwork_path), cv2.IMREAD_COLOR)
        base = cv2.imread(str(base_path), cv2.IMREAD_UNCHANGED)
        if artwork is None or base is None:
            raise CompositeRenderError("Failed to load artwork or base image")

        payload = json.loads(coords_path.read_text(encoding="utf-8"))
        points = payload.get("points")
        if not isinstance(points, list) or len(points) != 4:
            raise CompositeRenderError("Coordinate JSON must contain exactly 4 points")

        dst = np.array(
            [[float(p["x"]), float(p["y"])] for p in points],
            dtype=np.float32,
        )

        h_src, w_src = artwork.shape[:2]
        src = np.array(
            [
                [0.0, 0.0],
                [float(w_src - 1), 0.0],
                [float(w_src - 1), float(h_src - 1)],
                [0.0, float(h_src - 1)],
            ],
            dtype=np.float32,
        )

        transform = cv2.getPerspectiveTransform(src, dst)

        if base.ndim == 2:
            base_rgba = cv2.cvtColor(base, cv2.COLOR_GRAY2BGRA)
        elif base.shape[2] == 3:
            base_rgba = cv2.cvtColor(base, cv2.COLOR_BGR2BGRA)
        else:
            base_rgba = base.copy()

        h_base, w_base = base_rgba.shape[:2]
        warped = cv2.warpPerspective(
            artwork,
            transform,
            (w_base, h_base),
            flags=cv2.INTER_LANCZOS4,
            borderMode=cv2.BORDER_TRANSPARENT,
        )

        scene_rgba = np.zeros((h_base, w_base, 4), dtype=np.uint8)
        scene_rgba[:, :, :3] = warped
        scene_rgba[:, :, 3] = 255

        # Keep warped art below base details, leveraging base alpha hole.
        composed = self._alpha_composite(scene_rgba, base_rgba)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        composed_bgr = cv2.cvtColor(composed, cv2.COLOR_BGRA2BGR)
        ok = cv2.imwrite(
            str(output_path),
            composed_bgr,
            [int(cv2.IMWRITE_JPEG_QUALITY), int(max(1, min(100, request.jpeg_quality)))],
        )
        if not ok:
            raise CompositeRenderError(f"Failed to write composite JPEG: {output_path}")

        return RenderCompositeResult(
            output_jpeg_path=output_path,
            width=w_base,
            height=h_base,
        )

    @staticmethod
    def _alpha_composite(bottom_rgba: np.ndarray, top_rgba: np.ndarray) -> np.ndarray:
        """Alpha composite two BGRA images of same shape."""

        bottom = bottom_rgba.astype(np.float32) / 255.0
        top = top_rgba.astype(np.float32) / 255.0

        alpha_top = top[:, :, 3:4]
        alpha_bottom = bottom[:, :, 3:4]

        out_alpha = alpha_top + alpha_bottom * (1.0 - alpha_top)
        out_rgb = (top[:, :, :3] * alpha_top) + (
            bottom[:, :, :3] * alpha_bottom * (1.0 - alpha_top)
        )

        # Avoid division by zero when normalizing RGB by alpha.
        safe_alpha = np.clip(out_alpha, 1e-6, 1.0)
        out_rgb = out_rgb / safe_alpha

        out = np.dstack((out_rgb, out_alpha))
        return np.clip(out * 255.0, 0, 255).astype(np.uint8)
