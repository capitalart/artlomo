from __future__ import annotations
from pathlib import Path

import logging

from flask import Blueprint, current_app, jsonify, request, send_file

from application.common.utilities.slug_sku import is_safe_slug
from application.utils.csrf import require_csrf_or_400

from application.export.service import ExportError, ExportService


logger = logging.getLogger(__name__)


export_api_bp = Blueprint("export_api", __name__)


def _path_from_config(key: str) -> Path:
    value = current_app.config.get(key)
    if value is None:
        raise RuntimeError(f"Missing config: {key}")
    return value if isinstance(value, Path) else Path(value)


def _export_service() -> ExportService:
    cfg = current_app.config
    exports_root = cfg.get("EXPORTS_DIR")
    exports_root_path = exports_root if isinstance(exports_root, Path) else Path(exports_root) if exports_root else None
    if exports_root_path is None:
        raise RuntimeError("EXPORTS_DIR not configured")

    return ExportService(
        exports_root=exports_root_path,
        artworks_index_path=_path_from_config("ARTWORKS_INDEX_PATH"),
        processed_root=_path_from_config("LAB_PROCESSED_DIR"),
    )


@export_api_bp.post("/export/<sku>")  # type: ignore[misc]
def trigger_export(sku: str):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    payload = request.get_json(silent=True) or {}
    include_mockups = bool(payload.get("include_mockups", True))
    enforce_required = bool(payload.get("enforce_required", False))

    sku_clean = str(sku or "").strip()
    if not sku_clean or not is_safe_slug(sku_clean):
        return jsonify({"status": "error", "message": "Invalid sku"}), 404

    try:
        svc = _export_service()
        export_count = svc.increment_export_count(sku_clean, limit=10)
        export_id = svc.start_export_async(sku_clean, include_mockups=include_mockups, enforce_required=enforce_required)
        return jsonify({"status": "ok", "sku": sku_clean, "export_id": export_id, "export_count": export_count})
    except ExportError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 429
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception(
            "Failed to start export",
            extra={"sku": sku_clean, "include_mockups": include_mockups, "enforce_required": enforce_required},
        )
        return jsonify({"status": "error", "message": str(exc)}), 500


@export_api_bp.get("/export/has-mockups/<sku>")
def check_has_mockups(sku: str):
    sku_clean = str(sku or "").strip()
    if not sku_clean or not is_safe_slug(sku_clean):
        return jsonify({"status": "error", "message": "Invalid sku", "has_mockups": False}), 404

    try:
        svc = _export_service()
        artwork_dir, assets_path = svc.artworks_index.resolve(sku_clean)
        
        if not artwork_dir.exists() or not artwork_dir.is_dir():
            return jsonify({"status": "error", "message": "Artwork not found", "has_mockups": False}), 404

        import json
        assets_doc = {}
        if assets_path.exists():
            try:
                assets_doc = json.loads(assets_path.read_text(encoding="utf-8"))
            except Exception:
                assets_doc = {}

        mockups = assets_doc.get("mockups") or {}
        mockups_dirname = mockups.get("dir") if isinstance(mockups, dict) else None
        has_mockups = False

        if mockups_dirname:
            mockups_dir = artwork_dir / str(mockups_dirname)
            if mockups_dir.exists() and mockups_dir.is_dir():
                # Check if there are any files in the mockups directory
                mockup_files = list(mockups_dir.glob("*"))
                has_mockups = len(mockup_files) > 0

        return jsonify({"status": "ok", "sku": sku_clean, "has_mockups": has_mockups})
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Failed to check mockups for sku", extra={"sku": sku_clean})
        return jsonify({"status": "error", "message": str(exc), "has_mockups": False}), 500


@export_api_bp.get("/export/status/<sku>")
def export_status(sku: str):
    sku_clean = str(sku or "").strip()
    if not sku_clean or not is_safe_slug(sku_clean):
        return jsonify({"stage": "invalid", "message": "Invalid sku", "done": True, "error": "invalid sku"}), 400

    svc = _export_service()
    export_id = svc.latest_export_id(sku_clean)
    if not export_id:
        return jsonify({"stage": "not_started", "message": "No export found", "done": False, "error": None}), 404

    manifest = svc.read_manifest(sku_clean, export_id)
    stage = manifest.get("stage") or "unknown"
    done = bool(manifest.get("done"))
    error = manifest.get("error")

    payload = {
        "sku": sku_clean,
        "export_id": export_id,
        "stage": stage,
        "message": manifest.get("message"),
        "done": done,
        "error": error,
    }

    zip_name = manifest.get("zip_filename")
    if done and not error and zip_name:
        payload["download_url"] = f"/api/export/download/{sku_clean}/{export_id}"

    return jsonify(payload)


@export_api_bp.get("/export/download/<sku>/<export_id>")
def download_export(sku: str, export_id: str):
    sku_clean = str(sku or "").strip()
    export_id_clean = str(export_id or "").strip()

    if not sku_clean or not is_safe_slug(sku_clean):
        return jsonify({"status": "error", "message": "Invalid sku"}), 404
    if not export_id_clean or not is_safe_slug(export_id_clean):
        return jsonify({"status": "error", "message": "Invalid export_id"}), 404

    svc = _export_service()
    manifest = svc.read_manifest(sku_clean, export_id_clean)
    if not manifest:
        return jsonify({"status": "error", "message": "Export not found"}), 404

    zip_path = svc.zip_path(sku_clean, export_id_clean)
    if not zip_path.exists():
        return jsonify({"status": "error", "message": "Zip not ready"}), 404

    return send_file(zip_path, as_attachment=True)
