from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path


CANONICAL_STEM_RE = re.compile(
    r"^(?P<category>[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)-(?P<descriptor>[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)-(?P<number>\d+)$"
)


def _safe_token(value: str, fallback: str) -> str:
    token = re.sub(r"[^a-z0-9]+", "-", str(value or "").strip().lower()).strip("-")
    return token or fallback


def _parse_template_category_descriptor(template_slug: str) -> tuple[str, str]:
    parts = [part for part in str(template_slug or "").split("-") if part]
    if not parts:
        return ("uncategorised", "mockup")

    aspect = _safe_token(parts[0], "square")
    upper = [part.upper() for part in parts]
    try:
        mu_idx = upper.index("MU")
    except ValueError:
        mu_idx = -1

    if mu_idx > 1:
        category = _safe_token("-".join(parts[1:mu_idx]), "uncategorised")
    else:
        category = _safe_token(parts[0], "uncategorised")
    return (category, aspect)


def _derive_target_stem(stem: str, slug: str, slot_to_template: dict[str, str], fallback_number: int) -> str:
    if CANONICAL_STEM_RE.match(stem):
        return stem

    mu_prefix = f"mu-{slug}-"
    if stem.startswith(mu_prefix):
        slot_text = stem[len(mu_prefix) :]
        if slot_text.isdigit():
            slot = f"{int(slot_text):02d}"
            template_slug = slot_to_template.get(slot, "")
            category, descriptor = _parse_template_category_descriptor(template_slug)
            return f"{category}-{descriptor}-{slot}"

    parts = [part for part in stem.split("-") if part]
    category = _safe_token(parts[0] if parts else "uncategorised", "uncategorised")
    descriptor = _safe_token(parts[1] if len(parts) > 1 else "mockup", "mockup")
    return f"{category}-{descriptor}-{fallback_number:02d}"


def _read_assets_map(artwork_dir: Path, slug: str) -> dict[str, str]:
    assets_path = artwork_dir / f"{slug}-assets.json"
    if not assets_path.exists() or not assets_path.is_file():
        return {}
    try:
        payload = json.loads(assets_path.read_text(encoding="utf-8"))
        assets = payload.get("mockups", {}).get("assets", {})
        result: dict[str, str] = {}
        if isinstance(assets, dict):
            for slot, data in assets.items():
                if not isinstance(data, dict):
                    continue
                slot_key = f"{int(slot):02d}" if str(slot).isdigit() else str(slot)
                template_slug = str(data.get("template_slug") or "").strip()
                if template_slug:
                    result[slot_key] = template_slug
        return result
    except Exception:
        return {}


def _log_line(log_file: Path, line: str) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def _rename_file(old_path: Path, new_path: Path, log_file: Path) -> None:
    if old_path == new_path:
        return
    if new_path.exists():
        _log_line(log_file, f"SKIP_EXISTS {old_path} -> {new_path}")
        return
    os.rename(str(old_path), str(new_path))
    _log_line(log_file, f"RENAMED {old_path} -> {new_path}")


def migrate_mockups(processed_root: Path, coordinates_root: Path, log_file: Path) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    _log_line(log_file, f"=== MIGRATION START {timestamp} ===")
    _log_line(log_file, f"processed_root={processed_root}")
    _log_line(log_file, f"coordinates_root={coordinates_root}")

    for artwork_dir in sorted(processed_root.iterdir()):
        if not artwork_dir.is_dir():
            continue

        slug = artwork_dir.name
        mockups_dir = artwork_dir / "mockups"
        if not mockups_dir.exists() or not mockups_dir.is_dir():
            continue

        slot_to_template = _read_assets_map(artwork_dir, slug)
        mockup_files = sorted(
            path
            for path in mockups_dir.glob("*.jpg")
            if path.is_file() and "THUMB" not in path.stem.upper() and "DETAIL" not in path.stem.upper()
        )

        fallback_number = 1
        for old_path in mockup_files:
            old_stem = old_path.stem
            new_stem = _derive_target_stem(old_stem, slug, slot_to_template, fallback_number)
            fallback_number += 1

            new_path = old_path.with_name(f"{new_stem}{old_path.suffix}")
            _rename_file(old_path, new_path, log_file)

            old_coord_name = f"{old_stem}.json"
            new_coord_name = f"{new_stem}.json"
            if old_coord_name == new_coord_name:
                continue

            for coord_old in coordinates_root.rglob(old_coord_name):
                coord_new = coord_old.with_name(new_coord_name)
                _rename_file(coord_old, coord_new, log_file)

    _log_line(log_file, f"=== MIGRATION END {datetime.now().isoformat(timespec='seconds')} ===")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Temporary utility to rename mockup JPG/JSON assets into Category-Descriptor-Number format."
    )
    parser.add_argument(
        "--processed-root",
        default="/srv/artlomo/application/lab/processed",
        help="Path to processed artwork root.",
    )
    parser.add_argument(
        "--coordinates-root",
        default="/srv/artlomo/application/var/coordinates",
        help="Path to coordinates root.",
    )
    parser.add_argument(
        "--log-file",
        default="/srv/artlomo/application/tools/video/migration.log",
        help="Path to migration log file.",
    )

    args = parser.parse_args()
    migrate_mockups(
        processed_root=Path(args.processed_root),
        coordinates_root=Path(args.coordinates_root),
        log_file=Path(args.log_file),
    )


if __name__ == "__main__":
    main()
