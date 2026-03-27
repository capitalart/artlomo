from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from application.mockups.admin.services import CatalogAdminService


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_upsert_generated_base_deduplicates_existing_slug_collisions(tmp_path):
    catalog_dir = tmp_path / "catalog"
    catalog_path = catalog_dir / "catalog.json"

    duplicate_slug = "5x4-study-mu-1"
    _write_json(
        catalog_path,
        {
            "templates": [],
            "bases": [
                {
                    "id": "base-a",
                    "slug": duplicate_slug,
                    "source_job_id": "old-job-a",
                    "original_filename": "a.png",
                    "base_image": "assets/mockups/bases/5x4/study/a.png",
                    "coordinates_path": "assets/mockups/bases/5x4/study/a.json",
                    "category": "study",
                    "aspect_ratio": "5x4",
                    "status": "disabled",
                    "region_count": 1,
                    "created_at": "2026-01-01T00:00:00+00:00",
                    "updated_at": "2026-01-01T00:00:00+00:00",
                },
                {
                    "id": "base-b",
                    "slug": duplicate_slug,
                    "source_job_id": "old-job-b",
                    "original_filename": "b.png",
                    "base_image": "assets/mockups/bases/5x4/study/b.png",
                    "coordinates_path": "assets/mockups/bases/5x4/study/b.json",
                    "category": "study",
                    "aspect_ratio": "5x4",
                    "status": "disabled",
                    "region_count": 1,
                    "created_at": "2026-01-01T00:00:00+00:00",
                    "updated_at": "2026-01-01T00:00:00+00:00",
                },
            ],
        },
    )

    generated_image = tmp_path / "generated.png"
    Image.new("RGB", (100, 100), (200, 200, 200)).save(generated_image, format="PNG")

    source_coords = tmp_path / "generated-coords.json"
    _write_json(
        source_coords,
        {
            "points": [
                {"x": 10, "y": 10},
                {"x": 90, "y": 10},
                {"x": 90, "y": 90},
                {"x": 10, "y": 90},
            ]
        },
    )

    service = CatalogAdminService(catalog_path=catalog_path)

    result = service.upsert_generated_base(
        job_id="job-bathroom-v1",
        aspect_ratio="5x4",
        category="bathroom",
        variation_index=1,
        generated_image_path=str(generated_image),
        source_coordinates_path=str(source_coords),
    )

    assert result.slug == "5x4-bathroom-mu-1"

    catalog_payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    slugs = [entry.get("slug") for entry in catalog_payload.get("bases", []) if isinstance(entry, dict)]
    assert slugs.count(duplicate_slug) == 1
    assert slugs.count("5x4-bathroom-mu-1") == 1
