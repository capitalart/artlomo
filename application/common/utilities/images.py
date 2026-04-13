# CLINE_DIRECTIVE: Always use AppConfig for resolutions. All high-res exports MUST follow ANALYSE_LONG_EDGE (2400px).

import gc
import logging
from dataclasses import dataclass
from io import BytesIO
from typing import Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageCms, ImageOps

Image.MAX_IMAGE_PIXELS = None
logger = logging.getLogger(__name__)


_SRGB_PROFILE_CACHE: bytes | None = None


@dataclass
class ImageInfo:
    width: int
    height: int
    fmt: str
    dpi_x: Optional[int]
    dpi_y: Optional[int]
    mode: str
    icc_present: bool
    icc_profile_name: Optional[str]

    @property
    def long_edge(self) -> int:
        return max(self.width, self.height)


def read_image_info(image_bytes: bytes) -> ImageInfo:
    with Image.open(BytesIO(image_bytes)) as img:
        dpi: Optional[Tuple[int, int]] = img.info.get("dpi")
        dpi_x = dpi[0] if dpi else None
        dpi_y = dpi[1] if dpi else None
        icc_name = _icc_profile_name(img.info.get("icc_profile"))
        return ImageInfo(
            width=img.width,
            height=img.height,
            fmt=img.format or "",
            dpi_x=dpi_x,
            dpi_y=dpi_y,
            mode=img.mode,
            icc_present=bool(img.info.get("icc_profile")),
            icc_profile_name=icc_name,
        )


def generate_thumbnail(image_bytes: bytes, size: tuple[int, int]) -> bytes:
    with Image.open(BytesIO(image_bytes)) as img:
        img.thumbnail(size, Image.Resampling.LANCZOS)
        thumb_io = BytesIO()
        img.convert("RGB").save(thumb_io, format="JPEG", quality=85, optimize=True)
        return thumb_io.getvalue()


def generate_analyse_image(image_bytes: bytes, target_long_edge: int = 2400) -> bytes:
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            exif_bytes = img.info.get("exif")
            img = ImageOps.exif_transpose(img)
            img = _convert_to_srgb(img)

            # Pillow's thumbnail only downsizes; it will not upscale smaller assets.
            img.thumbnail((target_long_edge, target_long_edge), Image.Resampling.LANCZOS)

            output = BytesIO()
            save_kwargs = {
                "format": "JPEG",
                "quality": 85,
                "subsampling": 0,
                "optimize": True,
                "progressive": True,
                "icc_profile": _srgb_profile_bytes(),
            }
            if exif_bytes:
                save_kwargs["exif"] = exif_bytes

            img.save(output, **save_kwargs)
            return output.getvalue()
    except Exception:
        logger.exception("Failed to generate analyse image")
        raise


def is_jpeg_format(fmt: str) -> bool:
    return fmt.lower() in {"jpeg", "jpg", "jfif"}


def laplacian_variance(image_bytes: bytes) -> float:
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0.0
    return float(cv2.Laplacian(img, cv2.CV_64F).var())


def has_exif(image_bytes: bytes) -> bool:
    with Image.open(BytesIO(image_bytes)) as img:
        exif = img.getexif()
        return bool(exif and len(exif.items()) > 0)


def icc_is_srgb(image_bytes: bytes) -> bool:
    with Image.open(BytesIO(image_bytes)) as img:
        icc = img.info.get("icc_profile")
        if not icc:
            return True
        try:
            profile = ImageCms.ImageCmsProfile(BytesIO(icc))
            return ImageCms.getProfileName(profile).lower().startswith("srgb")
        except Exception:
            return False


def _convert_to_srgb(img: Image.Image) -> Image.Image:
    icc = img.info.get("icc_profile")
    if icc:
        try:
            src_profile = ImageCms.ImageCmsProfile(BytesIO(icc))
            dst_profile = ImageCms.createProfile("sRGB")
            converted_img = ImageCms.profileToProfile(img, src_profile, dst_profile, outputMode="RGB")  # type: ignore[assignment]
            img = converted_img if converted_img is not None else img
            img.info["icc_profile"] = dst_profile.tobytes()
        except Exception:
            img = img.convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")
    if "icc_profile" not in img.info:
        img.info["icc_profile"] = _srgb_profile_bytes()
    return img


def _icc_profile_name(icc_profile: Optional[bytes]) -> Optional[str]:
    if not icc_profile:
        return None
    try:
        profile = ImageCms.ImageCmsProfile(BytesIO(icc_profile))
        return ImageCms.getProfileName(profile)
    except Exception:
        return None


def _srgb_profile_bytes() -> bytes:
    # Cache sRGB profile bytes so Pillow doesn't rebuild them on every call.
    global _SRGB_PROFILE_CACHE
    if _SRGB_PROFILE_CACHE is None:
        profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
        _SRGB_PROFILE_CACHE = profile.tobytes()
    return _SRGB_PROFILE_CACHE


def cleanup_memory() -> None:
    """Explicitly trigger garbage collection to free image buffers from memory.
    
    Call this after completing high-memory image processing stages.
    Particularly important on memory-constrained systems (e.g., 2-CPU VMs with 7.8GiB RAM).
    """
    gc.collect()
