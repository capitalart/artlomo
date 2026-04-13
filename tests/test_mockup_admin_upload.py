from __future__ import annotations

import json
from io import BytesIO

from PIL import Image

from application.mockups.admin.services import CatalogAdminService
from application.mockups.admin.routes import mockup_admin_routes


def _png_bytes(size: tuple[int, int] = (64, 64)) -> bytes:
    buffer = BytesIO()
    Image.new("RGBA", size, (255, 255, 255, 0)).save(buffer, format="PNG")
    return buffer.getvalue()


def test_upload_bases_accepts_coordinate_json(app_client, tmp_path, monkeypatch):
    catalog_path = tmp_path / "catalog" / "catalog.json"
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps({"templates": [], "bases": []}), encoding="utf-8")
    service = CatalogAdminService(catalog_path=catalog_path)
    monkeypatch.setattr(mockup_admin_routes, "_catalog_service", lambda: service)

    response = app_client.post(
        "/admin/mockups/bases/upload",
        data={
            "slug": "4x5-display-001",
            "category": "display",
            "aspect_ratio": "4x5",
            "base_image": (BytesIO(_png_bytes()), "4x5-display-001.png"),
            "coords_json": (
                BytesIO(
                    json.dumps(
                        {
                            "corners": [
                                {"x": 8, "y": 8},
                                {"x": 56, "y": 8},
                                {"x": 8, "y": 56},
                                {"x": 56, "y": 56},
                            ]
                        }
                    ).encode("utf-8")
                ),
                "4x5-display-001.json",
            ),
        },
        headers={
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["slugs"] == ["4x5-display-001"]

    catalog_payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    assert len(catalog_payload["bases"]) == 1
    assert catalog_payload["bases"][0]["slug"] == "4x5-display-001"


def test_upload_bases_accepts_dam_sidecar_and_preserves_metadata_2048(app_client, tmp_path, monkeypatch):
    catalog_path = tmp_path / "catalog" / "catalog.json"
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps({"templates": [], "bases": []}), encoding="utf-8")
    service = CatalogAdminService(catalog_path=catalog_path)
    monkeypatch.setattr(mockup_admin_routes, "_catalog_service", lambda: service)

    sidecar_payload = {
        "schema_version": "2.0",
        "asset_slug": "4x5-gallery-001",
        "aspect_ratio": "4x5",
        "category": "gallery",
        "coordinates": {
            "available": True,
            "data": {
                "width": 2048,
                "height": 2048,
                "point_order": ["TL", "TR", "BR", "BL"],
                "points": [
                    {"x": 320.0, "y": 280.0},
                    {"x": 1710.0, "y": 300.0},
                    {"x": 1695.0, "y": 1755.0},
                    {"x": 305.0, "y": 1738.0},
                ],
            },
        },
    }

    response = app_client.post(
        "/admin/mockups/bases/upload",
        data={
            "slug": "4x5-gallery-001",
            "category": "",
            "aspect_ratio": "",
            "base_image": (BytesIO(_png_bytes((2048, 2048))), "4x5-gallery-001.png"),
            "coords_json": (
                BytesIO(json.dumps(sidecar_payload).encode("utf-8")),
                "4x5-gallery-001.json",
            ),
        },
        headers={
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["slugs"] == ["4x5-gallery-001"]

    catalog_payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    assert len(catalog_payload["bases"]) == 1
    entry = catalog_payload["bases"][0]
    assert entry["aspect_ratio"] == "4x5"
    assert entry["category"] == "gallery"

    coords_path = catalog_path.parent / entry["coordinates_path"]
    coords_payload = json.loads(coords_path.read_text(encoding="utf-8"))
    assert "zones" in coords_payload
    assert len(coords_payload["zones"]) == 1