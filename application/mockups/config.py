"""Central configuration for the mockup backend (Phase 1).

All values are deterministic and should not be mutated at runtime. Future phases
may allow overrides via env/config, but Phase 1 keeps a fixed contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Dict, List

# Base paths (derived from this file location to allow testing in temp roots)
BASE_DIR = Path(__file__).resolve().parents[1]
LAB_DIR = BASE_DIR / "lab"
PROCESSED_DIR = LAB_DIR / "processed"
MASTER_INDEX_PATH = LAB_DIR / "index" / "artworks.json"

# I/O and storage
MOCKUPS_SUBDIR = "mockups"
THUMBS_SUBDIR = "thumbs"
ASSETS_BASENAME_TEMPLATE = "{slug}-assets.json"
COMPOSITE_BASENAME = "mu-{slug}-{slot:02d}.jpg"
THUMB_BASENAME = "mu-{slug}-{slot:02d}-THUMB.jpg"

# Image handling
ALLOWED_ART_EXTS = {".jpg", ".jpeg", ".png"}
TARGET_IMAGE_NAME_SUFFIX = "-CLOSEUP-PROXY.jpg"
JPEG_PARAMS = {
    "format": "JPEG",
    "quality": 95,
    "subsampling": 0,
    "optimize": False,
}
THUMB_MAX_DIM = 600  # px, max(width, height) after resize
MAX_LONG_EDGE = 16000  # safety guard to avoid OOM on extreme assets
MAX_REGIONS = 6

# Hashing
HASH_ALGO = "sha256"

# Mockup base defaults
DEFAULT_MOCKUP_ASPECT = "UNSET"
DEFAULT_MOCKUP_CATEGORY = "uncategorised"

# Mockup base generation statuses (Stage 1 contract)
MOCKUP_BASE_GENERATION_STATUSES = (
    "Pending",
    "Generating",
    "ProcessingCoordinates",
    "Completed",
    "Failed",
)


@dataclass(frozen=True)
class MockupBaseGenerationCatalog:
    """Single source of truth for mockup base generation dimensions and domains."""

    ASPECT_RATIOS: ClassVar[tuple[str, ...]] = (
        "1x1",
        "2x3",
        "3x2",
        "3x4",
        "4x3",
        "4x5",
        "5x4",
        "5x7",
        "7x5",
        "9x16",
        "16x9",
        "70x99",
        "99x70",
    )

    CATEGORIES: ClassVar[tuple[str, ...]] = (
        "bathroom",
        "bedroom-adults",
        "bedroom-kids",
        "cafe",
        "closeup",
        "dining",
        "display",
        "gallery",
        "games",
        "gift",
        "hallway",
        "kitchen",
        "living-room",
        "meeting-room",
        "music-room",
        "nursery",
        "outdoors",
        "restaurant",
        "sitting-room",
        "stairs",
        "study",
        "waiting-room",
        "workplace",
    )

    VARIATION_MIN_INDEX: ClassVar[int] = 1
    VARIATION_MAX_INDEX: ClassVar[int] = 20

    @classmethod
    def as_dict(cls) -> Dict[str, object]:
        return {
            "aspect_ratios": list(cls.ASPECT_RATIOS),
            "categories": list(cls.CATEGORIES),
            "variation_min_index": cls.VARIATION_MIN_INDEX,
            "variation_max_index": cls.VARIATION_MAX_INDEX,
            "variations_per_combination": cls.VARIATION_MAX_INDEX,
            "statuses": list(MOCKUP_BASE_GENERATION_STATUSES),
        }


# Backward-compatible aliases used by existing mockup modules.
STANDARD_MOCKUP_BASE_CATEGORIES: List[str] = list(MockupBaseGenerationCatalog.CATEGORIES)
STANDARD_MOCKUP_ASPECT_RATIOS: List[str] = list(MockupBaseGenerationCatalog.ASPECT_RATIOS)
MOCKUP_BASE_GENERATION_CONFIG: Dict[str, object] = MockupBaseGenerationCatalog.as_dict()

# Mockup asset roots
MOCKUPS_DIR = BASE_DIR / "mockups"
MOCKUP_CATALOG_DIR = MOCKUPS_DIR / "catalog"
MOCKUP_ASSETS_DIR = MOCKUP_CATALOG_DIR / "assets" / "mockups"
MOCKUP_BASES_DIR = MOCKUP_ASSETS_DIR / "bases"
MOCKUP_TESTS_DIR = MOCKUP_ASSETS_DIR / "mockup-tests"

# Deterministic constants
PERSPECTIVE_INTERPOLATION = "linear"  # mapped to cv2.INTER_LINEAR
BORDER_MODE = "constant"  # mapped to cv2.BORDER_CONSTANT

__all__ = [
    "BASE_DIR",
    "LAB_DIR",
    "PROCESSED_DIR",
    "MASTER_INDEX_PATH",
    "MOCKUPS_SUBDIR",
    "THUMBS_SUBDIR",
    "ASSETS_BASENAME_TEMPLATE",
    "COMPOSITE_BASENAME",
    "THUMB_BASENAME",
    "ALLOWED_ART_EXTS",
    "TARGET_IMAGE_NAME_SUFFIX",
    "JPEG_PARAMS",
    "THUMB_MAX_DIM",
    "MAX_LONG_EDGE",
    "MAX_REGIONS",
    "HASH_ALGO",
    "DEFAULT_MOCKUP_ASPECT",
    "DEFAULT_MOCKUP_CATEGORY",
    "MOCKUP_BASE_GENERATION_STATUSES",
    "MockupBaseGenerationCatalog",
    "MOCKUP_BASE_GENERATION_CONFIG",
    "STANDARD_MOCKUP_BASE_CATEGORIES",
    "STANDARD_MOCKUP_ASPECT_RATIOS",
    "MOCKUPS_DIR",
    "MOCKUP_CATALOG_DIR",
    "MOCKUP_ASSETS_DIR",
    "MOCKUP_BASES_DIR",
    "MOCKUP_TESTS_DIR",
    "PERSPECTIVE_INTERPOLATION",
    "BORDER_MODE",
]
