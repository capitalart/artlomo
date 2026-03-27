from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image

from ...common.utilities import images

ASPECT_TOLERANCE = 0.015
BLUR_WARN_MIN = 80.0
BLUR_PASS_MIN = 120.0

CANONICAL_RATIOS = {
    "1:1": 1.0,
    "2:3": 2 / 3,
    "3:2": 3 / 2,
    "3:4": 3 / 4,
    "4:3": 4 / 3,
    "4:5": 4 / 5,
    "5:4": 5 / 4,
    "5:7": 5 / 7,
    "7:5": 7 / 5,
    "9:16": 9 / 16,
    "16:9": 16 / 9,
    "70:99": 70 / 99,
    "99:70": 99 / 70,
}

MM_PER_INCH = 25.4
A_SERIES_SIZES_MM = {
    "A0": (841, 1189),
    "A1": (594, 841),
    "A2": (420, 594),
    "A3": (297, 420),
    "A4": (210, 297),
    "A5": (148, 210),
}


class QCResult:
    def __init__(self, info: images.ImageInfo | None, reasons: list[str], status: str = "fail") -> None:
        self.info = info
        self.reasons = reasons
        self.status = status

    @property
    def passed(self) -> bool:
        return self.status == "pass" and not self.reasons


class QCService:
    def __init__(self, required_long_edge: int, required_dpi: int, allowed_extensions: set[str]) -> None:
        self.required_long_edge = required_long_edge
        self.required_dpi = required_dpi
        self.allowed_extensions = {ext.lower() for ext in allowed_extensions}

    def validate_upload(self, file_bytes: bytes, filename: str) -> QCResult:
        reasons: list[str] = []
        ext = Path(filename).suffix.lower().lstrip(".")
        if ext not in self.allowed_extensions:
            reasons.append("Only JPG uploads are accepted.")

        info: images.ImageInfo | None = None
        try:
            info = images.read_image_info(file_bytes)
        except Exception:
            reasons.append("Uploaded file is not a readable image.")
            return QCResult(info, reasons, status="fail")

        if info and not images.is_jpeg_format(info.fmt):
            reasons.append("Image format must be JPEG.")
        if info and info.long_edge < self.required_long_edge:
            reasons.append(f"Long edge must be at least {self.required_long_edge}px; got {info.long_edge}.")
        if info and (info.dpi_x is None or info.dpi_y is None or info.dpi_x < self.required_dpi or info.dpi_y < self.required_dpi):
            reasons.append(f"DPI must be at least {self.required_dpi} and present in both axes.")
        if info and info.mode.upper() != "RGB":
            reasons.append(f"Image mode must be RGB; got {info.mode}.")

        status = "pass" if not reasons else "fail"
        return QCResult(info, reasons, status=status)

    @staticmethod
    def qc_payload(file_bytes: bytes, *, min_long_edge: int, min_dpi: int) -> dict[str, Any]:
        payload = extract_qc(
            file_bytes,
            min_long_edge=min_long_edge,
            min_dpi=min_dpi,
            max_long_edge=None,
        )
        payload["uploaded_at"] = datetime.now(timezone.utc).isoformat()
        return payload

    @staticmethod
    def analyse_qc(image_bytes: bytes, target_long_edge: int = 2048) -> dict[str, Any]:
        return extract_qc(
            image_bytes,
            min_long_edge=None,
            max_long_edge=target_long_edge,
            min_dpi=None,
        )


def detect_aspect_ratio(width: int, height: int, tolerance: float = ASPECT_TOLERANCE) -> dict[str, Any]:
    if width <= 0 or height <= 0:
        return {"label": "~0:0", "canonical": False}

    actual = width / height
    for label, ratio in CANONICAL_RATIOS.items():
        if abs(actual - ratio) / ratio <= tolerance:
            return {"label": label, "canonical": True}

    return {"label": f"~{width}:{height}", "canonical": False}


def extract_qc(
    image_bytes: bytes,
    *,
    min_long_edge: int | None,
    max_long_edge: int | None,
    min_dpi: int | None,
) -> dict[str, Any]:
    info = images.read_image_info(image_bytes)
    blur_score = images.laplacian_variance(image_bytes)
    aspect = detect_aspect_ratio(info.width, info.height)
    compression_quality = _estimate_jpeg_quality(image_bytes)
    if compression_quality is None:
        compression_quality = 85

    palette_hexes = _dominant_hexes(image_bytes, count=5)
    primary_name, secondary_name = _etsy_colour_names(palette_hexes)
    luminance_category = _luminance_category(image_bytes)
    edge_safety = _edge_safety(image_bytes)

    status = _initial_status(info, min_long_edge=min_long_edge, max_long_edge=max_long_edge, min_dpi=min_dpi)
    status = _merge_status(status, _status_from_blur(blur_score))
    status = _merge_status(status, _status_from_color(info.mode))

    payload: dict[str, Any] = {
        "dimensions": {"width": int(info.width), "height": int(info.height)},
        "dpi": _dpi_value(info),
        "filesize_mb": round(len(image_bytes) / (1024 * 1024), 1),
        "aspect_ratio": aspect,
        "color": {"mode": info.mode, "icc": bool(info.icc_present)},
        "palette": {
            "dominant_hex": palette_hexes,
            "primary": primary_name,
            "secondary": secondary_name,
        },
        "luminance": {
            "category": luminance_category,
        },
        "edge_safety": edge_safety,
        "blur_score": int(round(blur_score)),
        "compression_quality_est": compression_quality,
        "qc_status": status,
    }
    return payload


def _dominant_hexes(image_bytes: bytes, *, count: int = 5) -> list[str]:
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            img = img.convert("RGB")
            img_small = img.resize((160, 160))
            pal = img_small.convert("P", palette=Image.Palette.ADAPTIVE, colors=max(1, int(count)))
            palette = pal.getpalette() or []
            color_counts = pal.getcolors() or []
            pairs: list[tuple[int, tuple[int, int, int]]] = []
            for c, idx in sorted(color_counts, key=lambda x: int(x[0]), reverse=True):
                if isinstance(idx, (int, float)):
                    i = int(idx) * 3  # type: ignore[arg-type]
                    if i + 2 < len(palette):
                        rgb = (int(palette[i]), int(palette[i + 1]), int(palette[i + 2]))
                        pairs.append((int(c), rgb))
            out: list[str] = []
            for _c, (r, g, b) in pairs[:count]:
                out.append(f"#{r:02X}{g:02X}{b:02X}")
            return out
    except Exception:
        return []


def _hex_to_rgb(hex_code: str) -> tuple[int, int, int] | None:
    txt = str(hex_code or "").strip().lstrip("#")
    if len(txt) != 6:
        return None
    try:
        r = int(txt[0:2], 16)
        g = int(txt[2:4], 16)
        b = int(txt[4:6], 16)
        return r, g, b
    except Exception:
        return None


def _etsy_colour_names(hexes: list[str]) -> tuple[str | None, str | None]:
    if not hexes:
        return None, None

    palette: list[tuple[str, tuple[int, int, int]]] = []
    for h in hexes:
        rgb = _hex_to_rgb(h)
        if rgb is not None:
            palette.append((h, rgb))
    if not palette:
        return None, None

    etsy = {
        "Terracotta": (204, 102, 85),
        "Sage": (138, 154, 91),
        "Ochre": (204, 153, 51),
        "Eucalyptus": (76, 120, 104),
        "Sand": (214, 198, 172),
        "Cream": (241, 234, 219),
        "Charcoal": (54, 54, 54),
        "Black": (20, 20, 20),
        "White": (245, 245, 245),
        "Navy": (28, 44, 84),
        "Indigo": (55, 66, 115),
        "Teal": (44, 120, 126),
        "Blue": (60, 110, 180),
        "Green": (60, 130, 80),
        "Olive": (98, 106, 55),
        "Gold": (190, 156, 70),
        "Rust": (170, 76, 46),
        "Rose": (198, 120, 140),
        "Lavender": (160, 130, 190),
        "Grey": (135, 135, 135),
    }

    def nearest_name(rgb: tuple[int, int, int]) -> str:
        best = None
        best_d = None
        for name, ref in etsy.items():
            dr = rgb[0] - ref[0]
            dg = rgb[1] - ref[1]
            db = rgb[2] - ref[2]
            d = dr * dr + dg * dg + db * db
            if best_d is None or d < best_d:
                best_d = d
                best = name
        return str(best or "")

    primary = nearest_name(palette[0][1])
    secondary = None
    for _h, rgb in palette[1:]:
        cand = nearest_name(rgb)
        if cand and cand != primary:
            secondary = cand
            break
    return primary or None, secondary or None


def _luminance_category(image_bytes: bytes) -> str | None:
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            img = img.convert("RGB").resize((160, 160))
            px = list(img.getdata())
            if not px:
                return None
            lums: list[float] = []
            for r, g, b in px:
                l = (0.2126 * (r / 255.0)) + (0.7152 * (g / 255.0)) + (0.0722 * (b / 255.0))
                lums.append(l)
            avg = sum(lums) / max(1, len(lums))
            if avg >= 0.68:
                return "Bright/Airy"
            if avg <= 0.38:
                return "Dark/Moody"
            return "Balanced"
    except Exception:
        return None


def _edge_safety(image_bytes: bytes) -> dict[str, Any]:
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            img = img.convert("L")
            w, h = img.size
            if w <= 0 or h <= 0:
                return {}
            img_small = img.resize((320, int(round(320 * (h / w))))) if w >= h else img.resize((int(round(320 * (w / h))), 320))
            w2, h2 = img_small.size
            px = list(img_small.getdata())
            if not px:
                return {}
            arr = [int(v) for v in px]

            def at(x: int, y: int) -> int:
                return arr[y * w2 + x]

            mags: list[int] = [0] * (w2 * h2)
            for y in range(1, h2 - 1):
                for x in range(1, w2 - 1):
                    gx = (
                        -at(x - 1, y - 1)
                        + at(x + 1, y - 1)
                        - 2 * at(x - 1, y)
                        + 2 * at(x + 1, y)
                        - at(x - 1, y + 1)
                        + at(x + 1, y + 1)
                    )
                    gy = (
                        -at(x - 1, y - 1)
                        - 2 * at(x, y - 1)
                        - at(x + 1, y - 1)
                        + at(x - 1, y + 1)
                        + 2 * at(x, y + 1)
                        + at(x + 1, y + 1)
                    )
                    mags[y * w2 + x] = abs(int(gx)) + abs(int(gy))

            threshold = max(60, int(sorted(mags)[int(len(mags) * 0.92)])) if mags else 60
            xs: list[int] = []
            ys: list[int] = []
            for y in range(h2):
                row_off = y * w2
                for x in range(w2):
                    if mags[row_off + x] >= threshold:
                        xs.append(x)
                        ys.append(y)

            if not xs or not ys:
                return {
                    "margin_pct": 5,
                    "subject_bbox": None,
                    "too_close": False,
                    "signature_zone_activity": False,
                }

            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            margin_x = int(round(w2 * 0.05))
            margin_y = int(round(h2 * 0.05))

            too_close = bool(
                min_x <= margin_x
                or min_y <= margin_y
                or (w2 - 1 - max_x) <= margin_x
                or (h2 - 1 - max_y) <= margin_y
            )

            sig_w0 = int(round(w2 * 0.85))
            sig_h0 = int(round(h2 * 0.85))
            sig_vals: list[int] = []
            for y in range(sig_h0, h2):
                off = y * w2
                for x in range(sig_w0, w2):
                    sig_vals.append(mags[off + x])
            sig_avg = (sum(sig_vals) / max(1, len(sig_vals))) if sig_vals else 0.0
            signature_zone_activity = bool(sig_avg >= threshold)

            return {
                "margin_pct": 5,
                "subject_bbox": {
                    "x0": int(min_x),
                    "y0": int(min_y),
                    "x1": int(max_x),
                    "y1": int(max_y),
                    "w": int(w2),
                    "h": int(h2),
                },
                "too_close": too_close,
                "signature_zone_activity": signature_zone_activity,
            }
    except Exception:
        return {}


def derive_qc_tags(qc_data: dict[str, Any]) -> list[str]:
    dims = qc_data.get("dimensions") or {}
    width = int(dims.get("width", 0) or 0)
    height = int(dims.get("height", 0) or 0)
    aspect_info = qc_data.get("aspect_ratio") or {}
    aspect_label = aspect_info.get("label")
    aspect_canonical = bool(aspect_info.get("canonical")) if aspect_info else False
    dpi = int(qc_data.get("dpi", 0) or 0)
    qc_status = (qc_data.get("qc_status") or "").lower()

    tags: list[str] = []

    # Aspect ratio tags
    canonical_label = aspect_label if aspect_canonical else None
    if canonical_label and canonical_label in CANONICAL_RATIOS:
        tags.append(f"ratio:{canonical_label.replace(':', 'x')}")
    else:
        tags.append("ratio:custom")

    # Orientation
    orientation = _orientation(width, height)
    tags.append(f"orientation:{orientation}")

    # Format shape
    fmt = _format_shape(canonical_label, orientation)
    tags.append(f"format:{fmt}")

    # Shape aliases
    if orientation == "portrait":
        tags.append("shape:vertical")
    elif orientation == "landscape":
        tags.append("shape:horizontal")
    else:
        tags.append("shape:square")

    # Print readiness
    long_edge = max(width, height)
    if dpi >= 300:
        tags.append("print:300dpi")
    else:
        tags.append("print:low-dpi")

    if long_edge >= 14400:
        tags.append("print:large-format")
    elif long_edge >= 9000:
        tags.append("print:poster")
    else:
        tags.append("print:small")

    if dpi >= 300 and long_edge >= 14400:
        tags.append("print:ready")

    # QC status
    if qc_status in {"warn", "fail", "pass"}:
        tags.append(f"qc:{qc_status}")
    else:
        tags.append("qc:fail")

    return tags


def derive_max_print_sizes(qc_data: dict[str, Any]) -> dict[str, Any]:
    if not qc_data:
        return {}

    dims = qc_data.get("dimensions") or {}
    width_px = int(dims.get("width", 0) or 0)
    height_px = int(dims.get("height", 0) or 0)
    dpi = int(qc_data.get("dpi", 0) or 0)
    if width_px <= 0 or height_px <= 0 or dpi < 300:
        return {}

    orientation = _orientation(width_px, height_px)

    printable_w_in = width_px / dpi
    printable_h_in = height_px / dpi

    a_choice = _select_a_series(printable_w_in, printable_h_in, orientation)

    inches_w, inches_h = _oriented_pair(printable_w_in, printable_h_in, orientation)
    inches_w_rounded = int(round(inches_w))
    inches_h_rounded = int(round(inches_h))

    cm_w = inches_w * 2.54
    cm_h = inches_h * 2.54
    cm_w_rounded = int(round(cm_w))
    cm_h_rounded = int(round(cm_h))

    tags: list[str] = []
    if a_choice:
        tags.append(f"print:{a_choice.lower()}")

    max_in_dim = max(inches_w, inches_h)
    if max_in_dim >= 40:
        tags.append("print:large-format")
    elif max_in_dim >= 24:
        tags.append("print:poster")

    return {
        "a_series": a_choice,
        "inches": {"width": inches_w_rounded, "height": inches_h_rounded},
        "cm": {"width": cm_w_rounded, "height": cm_h_rounded},
        "tags": tags,
        "orientation": orientation,
    }


def _initial_status(
    info: images.ImageInfo,
    *,
    min_long_edge: int | None,
    max_long_edge: int | None,
    min_dpi: int | None,
) -> str:
    if not images.is_jpeg_format(info.fmt):
        return "fail"

    if min_long_edge is not None and info.long_edge < min_long_edge:
        return "fail"
    if max_long_edge is not None and info.long_edge > max_long_edge:
        return "fail"

    if min_dpi is not None:
        if info.dpi_x is None or info.dpi_y is None:
            return "fail"
        if info.dpi_x < min_dpi or info.dpi_y < min_dpi:
            return "fail"

    return "pass"


def _status_from_blur(blur_score: float) -> str:
    if blur_score < BLUR_WARN_MIN:
        return "fail"
    if blur_score < BLUR_PASS_MIN:
        return "warn"
    return "pass"


def _status_from_color(mode: str) -> str:
    upper = mode.upper()
    if upper == "CMYK":
        return "warn"
    if upper != "RGB":
        return "fail"
    return "pass"


def _merge_status(current: str, incoming: str) -> str:
    order = {"pass": 0, "warn": 1, "fail": 2}
    return current if order[current] >= order[incoming] else incoming


def _dpi_value(info: images.ImageInfo) -> int:
    if info.dpi_x is None and info.dpi_y is None:
        return 0
    if info.dpi_x is None:
        return int(round(float(info.dpi_y or 0)))  # type: ignore[arg-type]
    if info.dpi_y is None:
        return int(round(float(info.dpi_x or 0)))  # type: ignore[arg-type]
    return int(round((float(info.dpi_x) + float(info.dpi_y)) / 2.0))


def _estimate_jpeg_quality(image_bytes: bytes) -> int | None:
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            if img.format != "JPEG":
                return None
            quant = getattr(img, "quantization", None)
            if not quant:
                return None
            values: list[int] = []
            for table in quant.values():
                values.extend(table)
            if not values:
                return None
            avg_q = sum(values) / len(values)
            if avg_q <= 0:
                return None
            estimated = int(max(1, min(100, round(5000.0 / avg_q))))
            return estimated
    except Exception:
        return None
    return None


def _select_a_series(width_in: float, height_in: float, orientation: str) -> str | None:
    for label in ["A0", "A1", "A2", "A3", "A4", "A5"]:
        mm_w, mm_h = A_SERIES_SIZES_MM[label]
        a_w_in = mm_w / MM_PER_INCH
        a_h_in = mm_h / MM_PER_INCH
        if _fits_size(width_in, height_in, a_w_in, a_h_in, orientation):
            return label.lower()
    return None


def _fits_size(img_w: float, img_h: float, size_w: float, size_h: float, orientation: str) -> bool:
    if orientation == "landscape":
        return img_w <= size_h and img_h <= size_w
    if orientation == "portrait":
        return img_w <= size_w and img_h <= size_h
    # square orientation uses tighter fit
    return img_w <= min(size_w, size_h) and img_h <= min(size_w, size_h)


def _oriented_pair(width: float, height: float, orientation: str) -> tuple[float, float]:
    if orientation == "landscape":
        if width >= height:
            return width, height
        return height, width
    if orientation == "portrait":
        if height >= width:
            return width, height
        return height, width
    return width, height


def _orientation(width: int, height: int) -> str:
    if width == height:
        return "square"
    return "landscape" if width > height else "portrait"


def _format_shape(canonical_label: str | None, orientation: str) -> str:
    if canonical_label:
        mapping = {
            "1:1": "square",
            "2:3": "tall",
            "3:4": "tall",
            "4:5": "tall",
            "5:7": "tall",
            "70:99": "tall",
            "9:16": "tall",
            "3:2": "standard",
            "4:3": "standard",
            "5:4": "standard",
            "7:5": "standard",
            "16:9": "wide",
            "99:70": "wide",
        }
        mapped = mapping.get(canonical_label)
        if mapped:
            return mapped
    if orientation == "square":
        return "square"
    return "tall" if orientation == "portrait" else "wide"
