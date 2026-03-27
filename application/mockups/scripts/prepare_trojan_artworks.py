"""Prepare bordered outlined-artwork reference images for mockup generation.

This utility reads artwork placeholder images from:
    /srv/artlomo/application/mockups/catalog/assets/mockups/artwork-placeholders/artwork-placeholders-V1/

For each source image it adds a strict 60px fiducial border with stripes:
    - 30px inner black (#000000)
    - 30px outer cyan  (#00FFFF)

It also neutralizes cyan-like pixels inside the artwork itself before bordering
to avoid accidental cyan detections from image content.

Outputs are written to:
    /srv/artlomo/application/mockups/catalog/assets/mockups/reference-guides/outlined-artworks/

Output naming follows the worker expectation:
    <aspect>-outlined-artwork.png
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps

SOURCE_DIR = Path(
    "/srv/artlomo/application/mockups/catalog/assets/mockups/artwork-placeholders/artwork-placeholders-V1"
)
OUTPUT_DIR = Path(
    "/srv/artlomo/application/mockups/catalog/assets/mockups/reference-guides/outlined-artworks"
)

# Explicit input list requested by operator.
INPUT_FILES = (
    "1x1-artwork-placeholder.png",
    "2x3-artwork-placeholder.png",
    "3x2-artwork-placeholder.png",
    "3x4-artwork-placeholder.png",
    "4x3-artwork-placeholder.png",
    "4x5-artwork-placeholder.png",
    "5x4-artwork-placeholder.png",
    "5x7-artwork-placeholder.png",
    "7x5-artwork-placeholder.png",
    "9x16-artwork-placeholder.png",
    "16x9-artwork-placeholder.png",
    "70x99-artwork-placeholder.png",
    "99x70-artwork-placeholder.png",
)

INNER_BLACK_BORDER_PX = 30
OUTER_CYAN_BORDER_PX = 30

BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
ANTI_CYAN_REPLACEMENT = (255, 64, 64)


@dataclass
class ProcessResult:
    source: Path
    output: Path
    created: bool
    message: str


def _replace_cyan_like_pixels(image: Image.Image) -> Image.Image:
    """Replace cyan-like artwork pixels so only fiducial border remains cyan."""
    rgb = image.convert("RGB")
    hsv = rgb.convert("HSV")

    rgb_data = list(rgb.getdata())
    hsv_data = list(hsv.getdata())

    # Broad cyan window: H in [78, 104], S >= 90, V >= 70
    for i, (h, s, v) in enumerate(hsv_data):
        if 78 <= h <= 104 and s >= 90 and v >= 70:
            rgb_data[i] = ANTI_CYAN_REPLACEMENT

    out = Image.new("RGB", rgb.size)
    out.putdata(rgb_data)
    return out


def _add_trojan_border(image: Image.Image) -> Image.Image:
    """Add the required 30px cyan outer + 30px black inner border to an image."""
    rgb = image.convert("RGB")

    # Inner black (touching artwork), then outer cyan.
    bordered = ImageOps.expand(rgb, border=INNER_BLACK_BORDER_PX, fill=BLACK)
    bordered = ImageOps.expand(bordered, border=OUTER_CYAN_BORDER_PX, fill=CYAN)
    return bordered


def _iter_inputs(source_dir: Path) -> Iterable[Path]:
    for name in INPUT_FILES:
        yield source_dir / name


def _output_name_for_source(source_path: Path) -> str:
    stem = source_path.stem
    suffix = "-artwork-placeholder"
    aspect = stem[:-len(suffix)] if stem.endswith(suffix) else stem
    return f"{aspect}-outlined-artwork.png"


def _process_one(source_path: Path, output_dir: Path, *, dry_run: bool) -> ProcessResult:
    output_path = output_dir / _output_name_for_source(source_path)

    if not source_path.exists() or not source_path.is_file():
        return ProcessResult(
            source=source_path,
            output=output_path,
            created=False,
            message="missing source file",
        )

    if dry_run:
        return ProcessResult(
            source=source_path,
            output=output_path,
            created=False,
            message="dry-run",
        )

    with Image.open(source_path) as src:
        sanitized = _replace_cyan_like_pixels(src)
        bordered = _add_trojan_border(sanitized)

    output_dir.mkdir(parents=True, exist_ok=True)
    bordered.save(output_path, format="PNG")

    return ProcessResult(
        source=source_path,
        output=output_path,
        created=True,
        message="ok",
    )


def run(*, source_dir: Path, output_dir: Path, dry_run: bool) -> int:
    results: list[ProcessResult] = []
    missing_count = 0

    for source_path in _iter_inputs(source_dir):
        result = _process_one(source_path, output_dir, dry_run=dry_run)
        results.append(result)
        if result.message == "missing source file":
            missing_count += 1

    print("Trojan Border Preparation")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    print(f"Dry run: {dry_run}")
    print("-")

    for result in results:
        print(f"{result.source.name}: {result.message} -> {result.output}")

    created_count = sum(1 for r in results if r.created)
    print("-")
    print(f"total listed: {len(results)}")
    print(f"created: {created_count}")
    print(f"missing: {missing_count}")

    return 1 if missing_count else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Neutralize cyan-like artwork pixels and add 30px cyan outer + 30px black inner fiducial borders.",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=SOURCE_DIR,
        help=f"Source directory (default: {SOURCE_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Output directory (default: {OUTPUT_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print plan without writing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run(source_dir=args.source_dir, output_dir=args.output_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
