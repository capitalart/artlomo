import json
from pathlib import Path

from application.artwork.services.processing_service import ProcessingService
from application.upload.services import storage_service
from application.artwork.errors import RequiredAssetMissingError


def _make_unprocessed(tmp_path: Path, slug: str) -> Path:
    src = tmp_path / "unprocessed" / slug
    src.mkdir(parents=True)
    sku = f"SKU-{slug}"
    (src / storage_service.master_name(slug)).write_text("master")
    (src / storage_service.analyse_name(slug)).write_text("analyse")
    (src / storage_service.thumb_name(slug)).write_text("thumb")
    (src / storage_service._meta_name(sku)).write_text(json.dumps({"sku": sku, "artwork_id": sku}))
    (src / storage_service._qc_name(sku)).write_text(json.dumps({"qc": True}))
    return src


def test_process_moves_unprocessed_into_processed(tmp_path):
    unprocessed_root = tmp_path / "unprocessed"
    processed_root = tmp_path / "processed"
    index_path = tmp_path / "index" / "artworks.json"
    slug = "sample-slug"
    _make_unprocessed(tmp_path, slug)

    svc = ProcessingService(
        unprocessed_root=unprocessed_root,
        processed_root=processed_root,
        artworks_index_path=index_path,
    )

    dest = svc.process(slug)

    assert not (unprocessed_root / slug).exists()
    assert dest.exists()
    assets_doc = json.loads((dest / f"sku-{slug}-assets.json").read_text())
    assert assets_doc["slug"] == slug
    assert (index_path).exists()


def test_process_requires_assets(tmp_path):
    unprocessed_root = tmp_path / "unprocessed"
    processed_root = tmp_path / "processed"
    index_path = tmp_path / "index" / "artworks.json"
    slug = "missing"
    # Create directory without required files
    (unprocessed_root / slug).mkdir(parents=True)

    svc = ProcessingService(
        unprocessed_root=unprocessed_root,
        processed_root=processed_root,
        artworks_index_path=index_path,
    )

    try:
        svc.process(slug)
    except RequiredAssetMissingError:
        pass
    else:
        raise AssertionError("Expected RequiredAssetMissingError for missing assets")
