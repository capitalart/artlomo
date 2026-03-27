#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = PROJECT_ROOT / "application"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from application.config import get_config
from application.artwork.services.index_service import ArtworksIndex
from application.utils.artwork_db import get_all_artworks, update_artwork_status


@dataclass
class RepairResult:
    sku: str
    slug: str
    db_status_before: str
    inferred_status: str
    moved: str | None
    db_updated: bool
    index_action: str
    notes: str


def _assets_file_for_dir(artwork_dir: Path) -> str:
    candidates = sorted(artwork_dir.glob("*-assets.json"))
    if candidates:
        return candidates[0].name
    legacy = artwork_dir / "assets.json"
    if legacy.exists():
        return legacy.name
    return ""


def _infer_status(cfg, slug: str) -> tuple[str, dict[str, Path]]:
    locations = {
        "unprocessed": Path(cfg.LAB_UNPROCESSED_DIR) / slug,
        "processed": Path(cfg.LAB_PROCESSED_DIR) / slug,
        "locked": Path(cfg.LAB_LOCKED_DIR) / slug,
    }
    found = [name for name, path in locations.items() if path.exists() and path.is_dir()]
    if len(found) == 1:
        return found[0], locations
    if len(found) == 0:
        return "missing", locations
    return "ambiguous", locations


def _move_if_requested(*, cfg, slug: str, target_status: str | None, apply: bool) -> str | None:
    if target_status not in {"processed", "locked"}:
        return None

    processed_dir = Path(cfg.LAB_PROCESSED_DIR) / slug
    locked_dir = Path(cfg.LAB_LOCKED_DIR) / slug

    if target_status == "locked":
        if locked_dir.exists() and locked_dir.is_dir():
            return "already_locked"
        if not processed_dir.exists() or not processed_dir.is_dir():
            return "cannot_move_missing_processed"
        if apply:
            processed_dir.replace(locked_dir)
        return "processed_to_locked"

    if processed_dir.exists() and processed_dir.is_dir():
        return "already_processed"
    if not locked_dir.exists() or not locked_dir.is_dir():
        return "cannot_move_missing_locked"
    if apply:
        locked_dir.replace(processed_dir)
    return "locked_to_processed"


def repair(*, skus: list[str] | None, target_status: str | None, apply: bool) -> list[RepairResult]:
    cfg = get_config(APP_ROOT)
    expected_lab = (APP_ROOT / "lab").resolve()
    if Path(cfg.LAB_DIR).resolve() != expected_lab:
        raise RuntimeError(f"Unexpected LAB_DIR: {cfg.LAB_DIR} (expected {expected_lab})")
    index = ArtworksIndex(Path(cfg.ARTWORKS_INDEX_PATH), Path(cfg.LAB_PROCESSED_DIR))

    all_artworks = get_all_artworks()
    by_sku = {str(a.get("sku") or a.get("id") or "").strip(): a for a in all_artworks}

    target_skus = [s.strip().upper() for s in (skus or []) if s and s.strip()]
    if not target_skus:
        target_skus = sorted(k for k in by_sku.keys() if k)

    results: list[RepairResult] = []

    for sku in target_skus:
        artwork = by_sku.get(sku)
        if not artwork:
            results.append(
                RepairResult(
                    sku=sku,
                    slug=sku.lower(),
                    db_status_before="missing",
                    inferred_status="missing",
                    moved=None,
                    db_updated=False,
                    index_action="none",
                    notes="sku_not_found_in_db",
                )
            )
            continue

        slug = str(artwork.get("slug") or sku.lower()).strip() or sku.lower()
        db_status = str(artwork.get("status") or "").strip() or "unknown"

        moved = _move_if_requested(cfg=cfg, slug=slug, target_status=target_status, apply=apply)
        inferred_status, locations = _infer_status(cfg, slug)

        db_updated = False
        if inferred_status in {"unprocessed", "processed", "locked"} and inferred_status != db_status:
            if apply:
                db_updated = bool(update_artwork_status(sku, inferred_status))
            else:
                db_updated = True

        index_action = "none"
        if inferred_status == "processed":
            processed_dir = locations["processed"]
            assets_file = _assets_file_for_dir(processed_dir)
            if assets_file:
                if apply:
                    index.upsert(sku=sku, slug=slug, artwork_dirname=slug, assets_file=assets_file)
                index_action = f"upsert:{assets_file}"
            else:
                index_action = "skip_upsert:no_assets_file"
        elif inferred_status in {"locked", "unprocessed", "missing"}:
            if apply:
                index.remove_by_sku(sku)
            index_action = "remove"

        notes = "ok"
        if inferred_status == "missing":
            notes = "folder_missing_in_all_roots"
        elif inferred_status == "ambiguous":
            notes = "folder_found_in_multiple_roots"

        results.append(
            RepairResult(
                sku=sku,
                slug=slug,
                db_status_before=db_status,
                inferred_status=inferred_status,
                moved=moved,
                db_updated=db_updated,
                index_action=index_action,
                notes=notes,
            )
        )

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Repair artwork DB status/index drift from actual folder location, with optional move action."
    )
    parser.add_argument(
        "--sku",
        action="append",
        default=[],
        help="SKU to repair (repeatable). If omitted, repairs all DB artworks.",
    )
    parser.add_argument(
        "--move-to",
        choices=["processed", "locked"],
        default=None,
        help="Optional move step before reconciliation (for selected SKUs).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes. Without this flag, runs as dry-run preview.",
    )
    args = parser.parse_args()

    results = repair(
        skus=args.sku,
        target_status=args.move_to,
        apply=bool(args.apply),
    )

    print(f"apply={bool(args.apply)} move_to={args.move_to or '-'}")
    print(f"items={len(results)}")
    for item in results:
        print(
            " | ".join(
                [
                    f"sku={item.sku}",
                    f"slug={item.slug}",
                    f"db_before={item.db_status_before}",
                    f"inferred={item.inferred_status}",
                    f"moved={item.moved or '-'}",
                    f"db_update={'yes' if item.db_updated else 'no'}",
                    f"index={item.index_action}",
                    f"notes={item.notes}",
                ]
            )
        )


if __name__ == "__main__":
    main()
