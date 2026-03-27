from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
    flash,
)

from application.artwork.errors import ArtworkProcessingError, IndexValidationError, RequiredAssetMissingError
from application.artwork.services.index_service import ArtworksIndex
from application.artwork.services.processing_service import ProcessingService
from application.mockups.admin.services import ManualMockupService
from application.mockups.errors import ValidationError, IndexLookupError, IoError
from application.mockups.artwork_index import resolve_artwork
from application.mockups.assets_index import AssetsIndex
from application.common.utilities.files import write_json_atomic
from application.upload.services import storage_service
from application.utils.csrf import get_csrf_token, require_csrf_or_400

logger = logging.getLogger(__name__)

manual_artworks_bp = Blueprint("manual_artworks_admin", __name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _path_from_config(key: str):
    value = current_app.config.get(key)
    if value is None:
        return None
    return value if isinstance(value, Path) else Path(value)


def _service() -> ManualMockupService:
    return ManualMockupService(
        catalog_path=_path_from_config("MOCKUP_CATALOG_PATH"),
        master_index_path=_path_from_config("MOCKUP_MASTER_INDEX_PATH"),
        processed_root=_path_from_config("MOCKUP_PROCESSED_ROOT"),
    )


def _load_metadata(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_metadata(path: Path, payload: Dict[str, Any]) -> None:
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json_atomic(path, payload)


def _find_unprocessed_slug(artwork_id: str, unprocessed_root: Path) -> str | None:
    if not unprocessed_root.exists():
        return None
    for slug_dir in sorted(p for p in unprocessed_root.iterdir() if p.is_dir()):
        meta_path = slug_dir / storage_service.META_NAME
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        meta_sku = str(meta.get("sku") or meta.get("artwork_id") or "").strip()
        if meta_sku == artwork_id:
            return slug_dir.name
    return None


def _ensure_processed_artwork(artwork_id: str) -> None:
    unprocessed_root = _path_from_config("LAB_UNPROCESSED_DIR")
    processed_root = _path_from_config("LAB_PROCESSED_DIR") or _path_from_config("MOCKUP_PROCESSED_ROOT")
    index_path = _path_from_config("ARTWORKS_INDEX_PATH") or _path_from_config("MOCKUP_MASTER_INDEX_PATH")
    if not unprocessed_root or not processed_root or not index_path:
        return

    artworks_index = ArtworksIndex(index_path, processed_root)
    doc = artworks_index.load()
    if artwork_id in (doc.get("items") or {}):
        return

    slug = _find_unprocessed_slug(artwork_id, unprocessed_root)
    if not slug:
        raise RequiredAssetMissingError(f"Artwork {artwork_id} not found in unprocessed directory")

    processor = ProcessingService(
        unprocessed_root=unprocessed_root,
        processed_root=processed_root,
        artworks_index_path=index_path,
    )
    processor.process(slug)


def _safe_asset_response(artwork_id: str, rel_path: str):
    service = _service()
    artwork_dir, _, _, _ = service._resolve_artwork(artwork_id)  # type: ignore[attr-defined]
    target = (artwork_dir / rel_path).resolve()
    if not target.exists():
        abort(404)
    if artwork_dir.resolve() not in target.parents and target != artwork_dir.resolve():
        abort(404)
    return send_file(target)


def _build_state(service: ManualMockupService, artwork_id: str) -> Dict[str, Any]:
    artwork_dir, assets_index, assets_doc, slug = service._resolve_artwork(artwork_id)  # type: ignore[attr-defined]
    files = assets_doc.get("files", {})
    metadata_path = artwork_dir / files.get("metadata", "metadata.json")
    metadata = _load_metadata(metadata_path)
    analyse_rel = files.get("analyse")
    analyse_url = None
    if analyse_rel:
        analyse_url = url_for("manual_artworks_admin.asset", artwork_id=artwork_id, rel_path=analyse_rel)
    aspect = service._artwork_aspect(artwork_dir / analyse_rel) if analyse_rel else None

    catalog_map = service._catalog_map()
    categories = sorted({tpl.category for tpl in catalog_map.values()})

    mockups_list = []
    assets_map = assets_index.assets_map(assets_doc)
    for slot_key, entry in sorted(assets_map.items()):
        try:
            slot_num = int(slot_key)
        except Exception:
            continue
        tpl_slug = entry.get("template_slug")
        tpl = catalog_map.get(tpl_slug)
        category = tpl.category if tpl else entry.get("category")
        mockups_list.append(
            {
                "slot": slot_num,
                "template_slug": tpl_slug,
                "category": category,
                "aspect_ratio": entry.get("aspect_ratio"),
                "thumb_url": url_for("manual_artworks_admin.asset", artwork_id=artwork_id, rel_path=entry.get("thumb", "")) if entry.get("thumb") else None,
                "composite_url": url_for("manual_artworks_admin.asset", artwork_id=artwork_id, rel_path=entry.get("composite", "")) if entry.get("composite") else None,
            }
        )

    return {
        "artwork_id": artwork_id,
        "slug": slug,
        "metadata_path": metadata_path,
        "metadata": metadata,
        "analyse_url": analyse_url,
        "aspect": aspect,
        "categories": categories,
        "mockups": mockups_list,
        "locked": bool(metadata.get("manual_lock")),
    }


def _extract_metadata(form) -> Dict[str, Any]:
    tags_raw = form.get("tags", "")
    materials_raw = form.get("materials", "")
    return {
        "title": (form.get("title") or "").strip(),
        "description": (form.get("description") or "").strip(),
        "tags": [t.strip() for t in tags_raw.split(",") if t.strip()],
        "materials": [m.strip() for m in materials_raw.split(",") if m.strip()],
        "price": (form.get("price") or "").strip(),
        "currency": (form.get("currency") or "AUD").strip() or "AUD",
        "quantity": (form.get("quantity") or "").strip(),
        "primary_colour": (form.get("primary_colour") or "").strip(),
        "secondary_colour": (form.get("secondary_colour") or "").strip(),
        "category": (form.get("category") or "").strip(),
        "seo_filename": (form.get("seo_filename") or "").strip(),
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@manual_artworks_bp.route("/admin/artworks/<artwork_id>/assets/<path:rel_path>", methods=["GET"])
def asset(artwork_id: str, rel_path: str):
    try:
        _ensure_processed_artwork(artwork_id)
    except ArtworkProcessingError:
        abort(404)
    return _safe_asset_response(artwork_id, rel_path)


@manual_artworks_bp.route("/admin/artworks/<artwork_id>/manual", methods=["GET", "POST"])  # type: ignore[misc]
def manual_edit(artwork_id: str):
    service = _service()
    try:
        _ensure_processed_artwork(artwork_id)
        state = _build_state(service, artwork_id)
    except (ValidationError, IndexLookupError, IoError, ArtworkProcessingError, IndexValidationError) as exc:
        flash(str(exc), "danger")
        abort(404)

    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            return resp
        action = request.form.get("action") or "save"
        if state["locked"] and action not in {"delete"}:
            flash("Artwork is locked; unlock to modify.", "warning")
            return redirect(url_for("manual_artworks_admin.manual_edit", artwork_id=artwork_id))

        metadata = state["metadata"].copy()
        metadata_path = state["metadata_path"]

        try:
            if action == "generate":
                count_raw = request.form.get("mockup_count") or "0"
                try:
                    count = int(count_raw)
                except Exception:
                    count = 0
                category = request.form.get("mockup_category") or None
                service.generate_mockups_for_artwork(sku=artwork_id, count=count, category=category)
                flash(f"Generated {count} mockup(s).", "success")

            elif action == "lock":
                metadata["manual_lock"] = True
                _write_metadata(metadata_path, metadata)
                flash("Artwork locked from edits.", "info")

            elif action == "delete":
                metadata["deleted"] = True
                metadata["manual_lock"] = True
                _write_metadata(metadata_path, metadata)
                flash("Artwork flagged for deletion.", "info")

            elif action in {"analyse_openai", "analyse_gemini"}:
                metadata["analysis_request"] = "openai" if action == "analyse_openai" else "gemini"
                _write_metadata(metadata_path, metadata)
                flash("Analysis request recorded.", "info")

            else:  # save
                metadata.update(_extract_metadata(request.form))
                _write_metadata(metadata_path, metadata)
                flash("Changes saved.", "success")
        except ValidationError as exc:
            flash(str(exc), "danger")
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Manual workflow error")
            flash("Unexpected error while processing request", "danger")

        return redirect(url_for("manual_artworks_admin.manual_edit", artwork_id=artwork_id))

    csrf_token = get_csrf_token()
    count_options = [1, 2, 3, 4, 5, 10, 15, 20]
    return render_template(
        "admin/artworks/manual_edit.html",
        state=state,
        count_options=count_options,
        csrf_token=csrf_token,
    )


@manual_artworks_bp.post("/admin/artworks/<artwork_id>/manual/mockups/<int:slot>/swap")  # type: ignore[misc]
def swap_mockup(artwork_id: str, slot: int):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    try:
        _ensure_processed_artwork(artwork_id)
    except ArtworkProcessingError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 404
    body = request.get_json(silent=True) or {}
    category = body.get("category") or None
    service = _service()

    # Check lock
    try:
        artwork_dir, assets_index, assets_doc, _ = service._resolve_artwork(artwork_id)  # type: ignore[attr-defined]
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"status": "error", "message": str(exc)}), 404
    metadata_path = artwork_dir / (assets_doc.get("files", {}).get("metadata", "metadata.json"))
    metadata = _load_metadata(metadata_path)
    if metadata.get("manual_lock"):
        return jsonify({"status": "error", "message": "Artwork is locked"}), 403

    try:
        service.regenerate_single_mockup(sku=artwork_id, slot=slot, new_category=category)
        assets_doc = assets_index.load()
        slot_entry = assets_index.current_slot_entry(assets_doc, f"{slot:02d}") or {}
        catalog_map = service._catalog_map()
        template_slug = slot_entry.get("template_slug", "")
        tpl = catalog_map.get(template_slug) if template_slug else None
        return jsonify(
            {
                "status": "ok",
                "slot": slot,
                "template_slug": slot_entry.get("template_slug"),
                "category": tpl.category if tpl else category,
                "thumb_url": url_for("manual_artworks_admin.asset", artwork_id=artwork_id, rel_path=slot_entry.get("thumb", "")) if slot_entry.get("thumb") else None,
                "composite_url": url_for("manual_artworks_admin.asset", artwork_id=artwork_id, rel_path=slot_entry.get("composite", "")) if slot_entry.get("composite") else None,
            }
        )
    except ValidationError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Swap failed")
        return jsonify({"status": "error", "message": "Swap failed"}), 500
