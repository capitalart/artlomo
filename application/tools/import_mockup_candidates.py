from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from application.common.utilities.slug_sku import slugify
from application.mockups.admin.services import CatalogAdminService
from application.mockups.errors import ValidationError
from PIL import Image


DEFAULT_CATALOG_PATH = Path("/srv/artlomo/application/mockups/catalog/catalog.json")
DEFAULT_SOURCE_ROOT = Path("/srv/artlomo/application/mockups/catalog/assets/mockups/New-Candidates")


@dataclass
class CandidateItem:
    aspect_ratio: str
    category: str
    slug: str
    png_path: Path
    json_path: Path


@dataclass
class ImportSummary:
    scanned_groups: int = 0
    valid_pairs: int = 0
    imported: int = 0
    skipped_existing: int = 0
    skipped_invalid: int = 0
    failed: int = 0


def _load_catalog_slug_set(service: CatalogAdminService) -> set[str]:
    reserved: set[str] = set()
    try:
        reserved.update(str(t.slug) for t in service.load_catalog())
    except ValidationError:
        pass
    try:
        reserved.update(str(b.slug) for b in service.load_bases())
    except ValidationError:
        pass
    return {s for s in reserved if s}


def _discover_candidates(source_root: Path) -> tuple[list[CandidateItem], list[str]]:
    issues: list[str] = []
    discovered: list[CandidateItem] = []

    if not source_root.exists() or not source_root.is_dir():
        return [], [f"Source root missing or not a directory: {source_root}"]

    for aspect_dir in sorted([p for p in source_root.iterdir() if p.is_dir()]):
        aspect = aspect_dir.name.strip()
        if not aspect:
            continue

        for category_dir in sorted([p for p in aspect_dir.iterdir() if p.is_dir()]):
            category = category_dir.name.strip()
            if not category:
                continue

            for slug_dir in sorted([p for p in category_dir.iterdir() if p.is_dir()]):
                slug_raw = slug_dir.name.strip()
                slug = slugify(slug_raw)
                if not slug:
                    issues.append(f"Invalid slug folder name: {slug_dir}")
                    continue

                expected_png = slug_dir / f"{slug_raw}.png"
                expected_json = slug_dir / f"{slug_raw}.json"

                if expected_png.exists() and expected_json.exists():
                    discovered.append(
                        CandidateItem(
                            aspect_ratio=aspect,
                            category=category,
                            slug=slug,
                            png_path=expected_png,
                            json_path=expected_json,
                        )
                    )
                    continue

                png_files = sorted([p for p in slug_dir.glob("*.png") if p.is_file()])
                json_files = sorted([p for p in slug_dir.glob("*.json") if p.is_file()])
                png_map = {p.stem: p for p in png_files}
                json_map = {p.stem: p for p in json_files}
                common_stems = sorted(set(png_map.keys()) & set(json_map.keys()))

                if len(common_stems) == 1:
                    stem = common_stems[0]
                    discovered.append(
                        CandidateItem(
                            aspect_ratio=aspect,
                            category=category,
                            slug=slug,
                            png_path=png_map[stem],
                            json_path=json_map[stem],
                        )
                    )
                elif len(common_stems) == 0:
                    issues.append(f"No matching PNG/JSON pair in {slug_dir}")
                else:
                    issues.append(f"Multiple PNG/JSON pair candidates in {slug_dir}: {', '.join(common_stems)}")

    return discovered, issues


def _coerce_point_list(raw_points: Any) -> list[dict[str, float]]:
    if not isinstance(raw_points, list) or len(raw_points) != 4:
        return []
    out: list[dict[str, float]] = []
    for point in raw_points:
        if not isinstance(point, dict):
            return []
        x = point.get("x")
        y = point.get("y")
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            return []
        out.append({"x": float(x), "y": float(y)})
    return out


def _adapt_coords_payload_for_artlomo(raw_payload: bytes, *, png_path: Path) -> dict[str, Any]:
    try:
        doc = json.loads(raw_payload.decode("utf-8"))
    except Exception as exc:
        raise ValidationError("Coordinate JSON is invalid") from exc

    if not isinstance(doc, dict):
        raise ValidationError("Coordinate JSON must be an object")

    # Already ArtLomo-compatible contracts.
    if isinstance(doc.get("zones"), list) or isinstance(doc.get("corners"), list) or isinstance(doc.get("regions"), list):
        return doc

    coord_data: dict[str, Any] = {}
    if isinstance(doc.get("coordinates"), dict):
        coordinates_doc = doc.get("coordinates") or {}
        data_doc = coordinates_doc.get("data")
        if isinstance(data_doc, dict):
            coord_data = data_doc

    direct_points = _coerce_point_list(coord_data.get("points"))
    if direct_points:
        return {"zones": [{"points": direct_points}]}

    normalized_points = _coerce_point_list(coord_data.get("normalized_points"))
    if normalized_points:
        width = coord_data.get("width")
        height = coord_data.get("height")
        if not isinstance(width, (int, float)) or not isinstance(height, (int, float)):
            with Image.open(png_path) as img:
                width, height = img.size
        width = float(width)
        height = float(height)
        points = [{"x": p["x"] * width, "y": p["y"] * height} for p in normalized_points]
        return {"zones": [{"points": points}]}

    raise ValidationError("Unable to normalize coordinates payload")


def _validate_candidate_with_temp_service(item: CandidateItem) -> None:
    raw_coords = item.json_path.read_bytes()
    adapted_coords = _adapt_coords_payload_for_artlomo(raw_coords, png_path=item.png_path)
    with tempfile.TemporaryDirectory(prefix="mockup-candidate-validate-") as tmp_dir:
        temp_catalog = Path(tmp_dir) / "catalog" / "catalog.json"
        temp_catalog.parent.mkdir(parents=True, exist_ok=True)
        temp_catalog.write_text(json.dumps({"templates": [], "bases": []}), encoding="utf-8")
        temp_service = CatalogAdminService(catalog_path=temp_catalog)
        temp_service.add_base(
            slug=item.slug,
            original_filename=item.png_path.name,
            category=item.category,
            aspect_ratio=item.aspect_ratio,
            base_image_bytes=item.png_path.read_bytes(),
            coords_payload=adapted_coords,
        )


def _safe_unlink(path: Path) -> None:
    try:
        if path.exists():
            path.unlink()
    except Exception:
        return


def _prune_empty_parents(path: Path, stop_at: Path) -> None:
    cursor = path.parent
    stop_at = stop_at.resolve()
    while True:
        try:
            if not cursor.exists():
                break
            if cursor.resolve() == stop_at:
                break
            cursor.rmdir()
            cursor = cursor.parent
        except Exception:
            break


def import_candidates(
    *,
    source_root: Path,
    catalog_path: Path,
    dry_run: bool,
    move_after_import: bool,
    skip_existing: bool,
    limit: int | None,
) -> dict[str, Any]:
    service = CatalogAdminService(catalog_path=catalog_path)
    reserved_slugs = _load_catalog_slug_set(service)

    candidates, discovery_issues = _discover_candidates(source_root)
    summary = ImportSummary(scanned_groups=len(candidates))
    report: dict[str, Any] = {
        "source_root": str(source_root),
        "catalog_path": str(catalog_path),
        "dry_run": bool(dry_run),
        "move_after_import": bool(move_after_import),
        "skip_existing": bool(skip_existing),
        "discovery_issues": discovery_issues,
        "items": [],
        "summary": {},
    }

    if limit is not None and limit >= 0:
        candidates = candidates[:limit]

    for item in candidates:
        row: dict[str, Any] = {
            "slug": item.slug,
            "aspect_ratio": item.aspect_ratio,
            "category": item.category,
            "png": str(item.png_path),
            "json": str(item.json_path),
            "status": "pending",
            "message": "",
        }

        if skip_existing and item.slug in reserved_slugs:
            summary.skipped_existing += 1
            row["status"] = "skipped_existing"
            row["message"] = "Slug already exists in catalog/bases"
            report["items"].append(row)
            continue

        try:
            if dry_run:
                _validate_candidate_with_temp_service(item)
                summary.valid_pairs += 1
                row["status"] = "validated"
                row["message"] = "PNG/JSON pair validates with ArtLomo add_base contract"
            else:
                raw_coords = item.json_path.read_bytes()
                adapted_coords = _adapt_coords_payload_for_artlomo(raw_coords, png_path=item.png_path)
                service.add_base(
                    slug=item.slug,
                    original_filename=item.png_path.name,
                    category=item.category,
                    aspect_ratio=item.aspect_ratio,
                    base_image_bytes=item.png_path.read_bytes(),
                    coords_payload=adapted_coords,
                )
                summary.imported += 1
                row["status"] = "imported"
                row["message"] = "Imported into catalog bases"
                reserved_slugs.add(item.slug)

                if move_after_import:
                    _safe_unlink(item.png_path)
                    _safe_unlink(item.json_path)
                    _prune_empty_parents(item.png_path, stop_at=source_root)
                    _prune_empty_parents(item.json_path, stop_at=source_root)

        except ValidationError as exc:
            summary.skipped_invalid += 1
            row["status"] = "invalid"
            row["message"] = str(exc)
        except Exception as exc:
            summary.failed += 1
            row["status"] = "failed"
            row["message"] = str(exc)

        report["items"].append(row)

    report["summary"] = {
        "scanned_groups": summary.scanned_groups,
        "valid_pairs": summary.valid_pairs,
        "imported": summary.imported,
        "skipped_existing": summary.skipped_existing,
        "skipped_invalid": summary.skipped_invalid,
        "failed": summary.failed,
    }
    return report


def _write_report(output_path: Path, payload: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate/import mockup base candidate folders (PNG+JSON) into ArtLomo catalog bases"
    )
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--catalog-path", type=Path, default=DEFAULT_CATALOG_PATH)
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument("--move", action="store_true", default=False, help="Move source files after successful import")
    parser.add_argument("--copy", action="store_true", default=False, help="Keep source files after successful import (default)")
    parser.add_argument("--no-skip-existing", action="store_true", default=False, help="Attempt imports even when slug already exists")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("/srv/artlomo/application/docs/mockup-candidate-import-report-29-March-2026.json"),
    )

    args = parser.parse_args()
    move_after_import = bool(args.move and not args.copy)
    dry_run = bool(args.dry_run)
    skip_existing = not bool(args.no_skip_existing)

    result = import_candidates(
        source_root=args.source_root,
        catalog_path=args.catalog_path,
        dry_run=dry_run,
        move_after_import=move_after_import,
        skip_existing=skip_existing,
        limit=args.limit,
    )
    _write_report(args.report, result)

    summary = result.get("summary", {})
    print("Import candidate summary")
    print("source_root=", result.get("source_root"))
    print("catalog_path=", result.get("catalog_path"))
    print("dry_run=", result.get("dry_run"))
    print("move_after_import=", result.get("move_after_import"))
    print("scanned_groups=", summary.get("scanned_groups"))
    print("valid_pairs=", summary.get("valid_pairs"))
    print("imported=", summary.get("imported"))
    print("skipped_existing=", summary.get("skipped_existing"))
    print("skipped_invalid=", summary.get("skipped_invalid"))
    print("failed=", summary.get("failed"))
    print("report=", str(args.report))

    if result.get("discovery_issues"):
        print("discovery_issues=", len(result["discovery_issues"]))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
