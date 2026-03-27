#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_index(index_path: Path) -> dict:
    if not index_path.exists() or not index_path.is_file():
        return {"version": 1, "items": {}, "updated_at": _now_iso()}
    data = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("artworks.json must be a JSON object")
    items = data.get("items")
    if not isinstance(items, dict):
        raise ValueError("artworks.json must contain an 'items' mapping")
    return data


def _write_json_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    os.replace(tmp_path, path)


def cleanup_ghost_entries(index_path: Path, processed_root: Path, dry_run: bool = False) -> dict:
    doc = _load_index(index_path)
    items = doc.get("items", {})
    if not isinstance(items, dict):
        raise ValueError("artworks.json 'items' must be a mapping")

    removed: list[dict[str, str]] = []
    kept: dict = {}

    for sku, entry in items.items():
        if not isinstance(entry, dict):
            removed.append({"sku": str(sku), "reason": "invalid_entry"})
            continue

        artwork_dirname = str(entry.get("artwork_dirname") or "").strip()
        slug = str(entry.get("slug") or "").strip()

        if not artwork_dirname:
            removed.append({"sku": str(sku), "slug": slug, "reason": "missing_artwork_dirname"})
            continue

        artwork_dir = processed_root / artwork_dirname
        if not artwork_dir.exists() or not artwork_dir.is_dir():
            removed.append(
                {
                    "sku": str(sku),
                    "slug": slug,
                    "artwork_dirname": artwork_dirname,
                    "reason": "missing_processed_folder",
                }
            )
            continue

        kept[str(sku)] = entry

    if removed and not dry_run:
        doc["items"] = kept
        doc["updated_at"] = _now_iso()
        _write_json_atomic(index_path, doc)

    return {
        "index_path": str(index_path),
        "processed_root": str(processed_root),
        "dry_run": dry_run,
        "removed_count": len(removed),
        "kept_count": len(kept),
        "removed": removed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="One-time cleanup: remove ghost entries from artworks.json when processed folders are missing."
    )
    parser.add_argument(
        "--index-path",
        default="/srv/artlomo/application/lab/index/artworks.json",
        help="Path to artworks.json",
    )
    parser.add_argument(
        "--processed-root",
        default="/srv/artlomo/application/lab/processed",
        help="Path to processed artworks root",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview removals without writing index")
    args = parser.parse_args()

    result = cleanup_ghost_entries(
        index_path=Path(args.index_path),
        processed_root=Path(args.processed_root),
        dry_run=bool(args.dry_run),
    )

    print(f"Index: {result['index_path']}")
    print(f"Processed root: {result['processed_root']}")
    print(f"Dry run: {result['dry_run']}")
    print(f"Removed: {result['removed_count']}")
    print(f"Kept: {result['kept_count']}")
    if result["removed"]:
        print("Details:")
        for item in result["removed"]:
            sku = item.get("sku", "")
            slug = item.get("slug", "")
            reason = item.get("reason", "unknown")
            dirname = item.get("artwork_dirname", "")
            extra = f" dirname={dirname}" if dirname else ""
            print(f"  - sku={sku} slug={slug} reason={reason}{extra}")


if __name__ == "__main__":
    main()
