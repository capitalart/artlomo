import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from application.mockups.routes import mockup_routes


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _touch(path: Path, content: str = "x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _seed_artwork_with_assets(app, slug: str, sku: str) -> Path:
    processed_dir = Path(app.config["LAB_PROCESSED_DIR"]) / slug
    processed_dir.mkdir(parents=True, exist_ok=True)

    _write_json(
        Path(app.config["ARTWORKS_INDEX_PATH"]),
        {
            "items": {
                sku: {
                    "slug": slug,
                    "artwork_dirname": slug,
                    "assets_file": f"{slug}-assets.json",
                }
            }
        },
    )

    # Minimal required files for AssetsIndex validation
    _touch(processed_dir / f"{sku.lower()}-master.jpg")
    _touch(processed_dir / f"{sku.lower()}-thumb.jpg")
    _touch(processed_dir / f"{sku.lower()}-metadata.json", '{"sku": "' + sku + '"}')
    _touch(processed_dir / f"{sku.lower()}-qc.json")
    _touch(processed_dir / f"{slug}-ANALYSE.jpg")

    assets_doc = {
        "slug": slug,
        "sku": sku,
        "files": {
            "master": f"{sku.lower()}-master.jpg",
            "thumb": f"{sku.lower()}-thumb.jpg",
            "metadata": f"{sku.lower()}-metadata.json",
            "qc": f"{sku.lower()}-qc.json",
            "analyse": f"{slug}-ANALYSE.jpg",
        },
        "mockups": {
            "dir": "mockups",
            "assets": {
                "01": {
                    "template_slug": "tpl-1",
                    "category": "living-room",
                    "aspect_ratio": "3x4",
                    "composite": f"mockups/mu-{slug}-01.jpg",
                    "thumb": f"mockups/thumbs/mu-{slug}-01-THUMB.jpg",
                },
                "02": {
                    "template_slug": "tpl-2",
                    "category": "bedroom",
                    "aspect_ratio": "3x4",
                    "composite": f"mockups/mu-{slug}-02.jpg",
                    "thumb": f"mockups/thumbs/mu-{slug}-02-THUMB.jpg",
                },
            },
        },
    }
    _write_json(processed_dir / f"{slug}-assets.json", assets_doc)

    _touch(processed_dir / "mockups" / f"mu-{slug}-01.jpg")
    _touch(processed_dir / "mockups" / f"mu-{slug}-02.jpg")
    _touch(processed_dir / "mockups" / "thumbs" / f"mu-{slug}-01-THUMB.jpg")
    _touch(processed_dir / "mockups" / "thumbs" / f"mu-{slug}-02-THUMB.jpg")

    return processed_dir


def test_delete_all_clears_assets_index_and_files(app, app_client):
    slug = "rjc-0001"
    sku = "RJC-0001"
    processed_dir = _seed_artwork_with_assets(app, slug=slug, sku=sku)

    resp = app_client.post(
        f"/artwork/{slug}/mockups/delete-all",
        json={"csrf_token": app_client.csrf_token},
        headers={"Accept": "application/json", "X-CSRFToken": app_client.csrf_token},
    )

    assert resp.status_code == 200
    body = resp.get_json()
    assert body["status"] == "ok"

    updated = json.loads((processed_dir / f"{slug}-assets.json").read_text(encoding="utf-8"))
    assert updated["mockups"]["assets"] == {}

    assert not (processed_dir / "mockups" / f"mu-{slug}-01.jpg").exists()
    assert not (processed_dir / "mockups" / f"mu-{slug}-02.jpg").exists()
    assert not (processed_dir / "mockups" / "thumbs" / f"mu-{slug}-01-THUMB.jpg").exists()
    assert not (processed_dir / "mockups" / "thumbs" / f"mu-{slug}-02-THUMB.jpg").exists()


def test_generate_writes_slot_via_assets_index(app, app_client, monkeypatch, tmp_path):
    slug = "rjc-0002"
    sku = "RJC-0002"
    processed_dir = Path(app.config["LAB_PROCESSED_DIR"]) / slug
    processed_dir.mkdir(parents=True, exist_ok=True)
    assets_path = processed_dir / f"{slug}-assets.json"
    _write_json(assets_path, {"slug": slug, "sku": sku, "mockups": {"dir": "mockups", "assets": {}}})

    writes: list[str] = []

    class FakeAssetsIndex:
        def guard_generate(self, _assets_doc, _slot_key):
            return None

        def write_slot(self, _assets_doc, slot_key, _slot_entry):
            writes.append(slot_key)

        def load(self):
            return {"slug": slug, "sku": sku, "mockups": {"dir": "mockups", "assets": {}}}

    monkeypatch.setattr(mockup_routes, "_promote_to_processed", lambda _slug: None)
    monkeypatch.setattr(
        mockup_routes,
        "resolve_artwork_aspect_for_preflight",
        lambda _slug: {"match_key": "3x4", "detected": "3:4 Matched", "source": "qc.json"},
    )
    monkeypatch.setattr(mockup_routes, "_eligible_template_count", lambda aspect: 1 if aspect == "3x4" else 0)
    monkeypatch.setattr(mockup_routes, "_clear_existing_mockups_for_slug", lambda slug: 0)
    monkeypatch.setattr(
        mockup_routes,
        "_init_fresh_assets_index_for_slug",
        lambda _slug: (sku, processed_dir, assets_path, FakeAssetsIndex(), {"slug": slug, "sku": sku, "mockups": {"dir": "mockups", "assets": {}}}),
    )

    import application.mockups.catalog.loader as catalog_loader
    import application.mockups.pipeline as pipeline

    monkeypatch.setattr(
        catalog_loader,
        "load_physical_bases",
        lambda aspect=None, category=None: [
            SimpleNamespace(slug="tpl-a", aspect_ratio=aspect or "3x4", category=category or "living-room", base_image=tmp_path / "base.png", coords=tmp_path / "base.json")
        ],
    )
    monkeypatch.setattr(
        pipeline,
        "generate_mockups_for_artwork",
        lambda **kwargs: {
            "template_slug": kwargs["template_slug"],
            "category": kwargs["category"],
            "aspect_ratio": kwargs["aspect_ratio"],
            "composite": f"mockups/mu-{slug}-01.jpg",
            "thumb": f"mockups/thumbs/mu-{slug}-01-THUMB.jpg",
        },
    )

    resp = app_client.post(
        f"/artwork/{slug}/mockups/generate",
        data={"mockup_count": "1", "csrf_token": app_client.csrf_token},
        headers={"Accept": "application/json", "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": app_client.csrf_token},
    )

    assert resp.status_code == 200
    body = resp.get_json()
    assert body["ok"] is True
    assert writes == ["01"]


def test_swap_returns_slot_payload_and_updates_paths(app, app_client, monkeypatch, tmp_path):
    slug = "rjc-0003"
    sku = "RJC-0003"
    processed_dir = Path(app.config["LAB_PROCESSED_DIR"]) / slug
    processed_dir.mkdir(parents=True, exist_ok=True)
    _touch(processed_dir / f"{sku.lower()}-metadata.json", '{"sku": "' + sku + '"}')

    class FakeAssetsIndex:
        def current_slot_entry(self, _assets_doc, slot_key):
            return {"template_slug": "existing"} if slot_key == "01" else None

    monkeypatch.setattr(
        mockup_routes,
        "resolve_artwork_aspect_for_preflight",
        lambda _slug: {"match_key": "3x4", "detected": "3:4 Matched", "source": "qc.json"},
    )
    monkeypatch.setattr(
        mockup_routes,
        "_load_assets_index_for_slug",
        lambda _slug: (sku, processed_dir, processed_dir / f"{slug}-assets.json", FakeAssetsIndex(), {"slug": slug, "sku": sku}),
    )

    import application.mockups.catalog.loader as catalog_loader
    import application.mockups.pipeline as pipeline

    monkeypatch.setattr(
        catalog_loader,
        "load_physical_bases",
        lambda aspect=None, category=None: [
            SimpleNamespace(slug="tpl-swap", aspect_ratio=aspect or "3x4", category=category or "living-room", base_image=tmp_path / "base.png", coords=tmp_path / "base.json")
        ],
    )
    monkeypatch.setattr(
        pipeline,
        "generate_mockups_for_artwork",
        lambda **kwargs: {
            "template_slug": kwargs["template_slug"],
            "category": kwargs["category"],
            "composite": f"mockups/mu-{slug}-01.jpg",
            "thumb": f"mockups/thumbs/mu-{slug}-01-THUMB.jpg",
        },
    )

    resp = app_client.post(
        f"/artwork/{slug}/mockups/1/swap",
        json={"category": "living-room", "csrf_token": app_client.csrf_token},
        headers={"Accept": "application/json", "X-CSRFToken": app_client.csrf_token},
    )

    assert resp.status_code == 200
    body = resp.get_json()
    assert body["status"] == "ok"
    assert body["slot"] == 1
    assert body["template_slug"] == "tpl-swap"
    assert body["thumb_url"].endswith(f"/artwork/{slug}/mockups/thumb/1")
    assert body["composite_url"].endswith(f"/artwork/{slug}/mockups/composite/1")
