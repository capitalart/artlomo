from __future__ import annotations

import json
import logging
import os
import shutil
import threading
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from application.artwork.services.index_service import ArtworksIndex
from application.common.utilities.files import ensure_dir, write_json_atomic

logger = logging.getLogger(__name__)


class ExportError(RuntimeError):
    pass


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json_silent(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        return doc if isinstance(doc, dict) else {}
    except Exception:
        return {}


def _safe_export_id() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y%m%dT%H%M%SZ")


def _resolve_seo_download_name(artwork_dir: Path, files: dict[str, Any]) -> str:
    seo_from_assets = str(files.get("seo_download") or "").strip()
    if seo_from_assets:
        return seo_from_assets

    listing_doc = _read_json_silent(artwork_dir / "listing.json")
    seo_from_listing = str(listing_doc.get("seo_filename") or "").strip()
    if seo_from_listing:
        return seo_from_listing

    return ""


class ExportService:
    def __init__(
        self,
        *,
        exports_root: Path,
        artworks_index_path: Path,
        processed_root: Path,
    ) -> None:
        self.exports_root = exports_root
        self.artworks_index = ArtworksIndex(artworks_index_path, processed_root)
        self.processed_root = processed_root

    def exports_dir_for_sku(self, sku: str) -> Path:
        return self.exports_root / sku

    def export_dir(self, sku: str, export_id: str) -> Path:
        return self.exports_dir_for_sku(sku) / export_id

    def manifest_path(self, sku: str, export_id: str) -> Path:
        return self.export_dir(sku, export_id) / "manifest.json"

    def zip_path(self, sku: str, export_id: str) -> Path:
        return self.export_dir(sku, export_id) / f"{sku}-{export_id}.zip"

    def latest_export_id(self, sku: str) -> str | None:
        sku_dir = self.exports_dir_for_sku(sku)
        if not sku_dir.exists() or not sku_dir.is_dir():
            return None
        candidates = [p.name for p in sku_dir.iterdir() if p.is_dir()]
        if not candidates:
            return None
        return sorted(candidates)[-1]

    def read_manifest(self, sku: str, export_id: str) -> dict[str, Any]:
        return _read_json_silent(self.manifest_path(sku, export_id))

    def increment_export_count(self, sku: str, *, limit: int = 10) -> int:
        artwork_dir, _assets_path = self.artworks_index.resolve(sku)
        meta_path = artwork_dir / "metadata.json"
        meta = _read_json_silent(meta_path)
        if not isinstance(meta, dict):
            meta = {}
        current = meta.get("export_count")
        current_num = int(current) if isinstance(current, int) else 0
        if current_num >= int(limit):
            raise ExportError(f"Export limit reached ({int(limit)}).")
        next_count = current_num + 1
        meta["export_count"] = int(next_count)
        write_json_atomic(meta_path, meta)
        return int(next_count)

    def start_export_async(self, sku: str, *, include_mockups: bool = True, enforce_required: bool = False) -> str:
        export_id = _safe_export_id()
        export_dir = self.export_dir(sku, export_id)
        try:
            ensure_dir(self.exports_root)
            ensure_dir(export_dir)
        except PermissionError as exc:
            raise ExportError(f"Exports directory is not writable: {export_dir}") from exc
        except OSError as exc:
            raise ExportError(f"Failed to create export directory: {export_dir} ({exc})") from exc

        if not os.access(export_dir, os.W_OK):
            raise ExportError(f"Exports directory is not writable: {export_dir}")

        write_json_atomic(
            self.manifest_path(sku, export_id),
            {
                "sku": sku,
                "export_id": export_id,
                "options": {
                    "include_mockups": bool(include_mockups),
                    "enforce_required": bool(enforce_required),
                },
                "stage": "queued",
                "message": "Export queued",
                "done": False,
                "error": None,
                "created_at": _now_iso(),
                "updated_at": _now_iso(),
            },
        )

        thread = threading.Thread(
            target=self._export_worker,
            args=(sku, export_id),
            kwargs={"include_mockups": include_mockups, "enforce_required": enforce_required},
            daemon=True,
        )
        thread.start()
        return export_id

    def _update_manifest(self, *, sku: str, export_id: str, **updates: Any) -> None:
        path = self.manifest_path(sku, export_id)
        current = _read_json_silent(path)
        payload: dict[str, Any] = {**current, **updates}
        payload.setdefault("sku", sku)
        payload.setdefault("export_id", export_id)
        payload["updated_at"] = _now_iso()
        write_json_atomic(path, payload)

    def _export_worker(self, sku: str, export_id: str, *, include_mockups: bool, enforce_required: bool) -> None:
        try:
            self._update_manifest(sku=sku, export_id=export_id, stage="resolving", message="Resolving artwork", done=False)
            artwork_dir, assets_path = self.artworks_index.resolve(sku)
            if not artwork_dir.exists() or not artwork_dir.is_dir():
                raise ExportError("Processed artwork directory not found")

            self._update_manifest(sku=sku, export_id=export_id, stage="copying", message="Copying assets", done=False)
            bundle_root = self.export_dir(sku, export_id) / "bundle"
            ensure_dir(bundle_root)

            assets_doc = _read_json_silent(assets_path)
            if not assets_doc:
                raise ExportError("Assets index missing or invalid")

            slug = str(assets_doc.get("slug") or "").strip() or artwork_dir.name
            self._update_manifest(sku=sku, export_id=export_id, slug=slug)

            files = assets_doc.get("files") or {}
            if not isinstance(files, dict) or not files:
                raise ExportError("Assets index contains no files")

            required_names = [str(name) for name in files.values() if name]
            required_names.append(assets_path.name)

            seo_download_name = _resolve_seo_download_name(artwork_dir, files)
            if seo_download_name:
                required_names.append(seo_download_name)

            optional_names = [
                "listing.json",
                "metadata.json",
                "metadata_openai.json",
                "metadata_gemini.json",
                "metadata_manual.json",
            ]

            copied_files: list[str] = []
            missing_required: list[str] = []
            missing_optional: list[str] = []

            for name in sorted(set(required_names)):
                src = artwork_dir / name
                if not src.exists() or not src.is_file():
                    missing_required.append(name)
                    continue
                dest = bundle_root / src.name
                ensure_dir(dest.parent)
                shutil.copy2(src, dest)
                copied_files.append(dest.relative_to(bundle_root).as_posix())

            for name in sorted(set(optional_names)):
                src = artwork_dir / name
                if not src.exists() or not src.is_file():
                    missing_optional.append(name)
                    continue
                dest = bundle_root / src.name
                ensure_dir(dest.parent)
                shutil.copy2(src, dest)
                copied_files.append(dest.relative_to(bundle_root).as_posix())

            self._update_manifest(
                sku=sku,
                export_id=export_id,
                options={"include_mockups": bool(include_mockups), "enforce_required": bool(enforce_required)},
                copied_files=sorted(set(copied_files)),
                missing_required=sorted(set(missing_required)),
                missing_optional=sorted(set(missing_optional)),
            )

            if enforce_required and missing_required:
                raise ExportError(f"Missing required assets: {', '.join(sorted(set(missing_required)))}")

            mockups = assets_doc.get("mockups") or {}
            mockups_dirname = mockups.get("dir") if isinstance(mockups, dict) else None
            if include_mockups and mockups_dirname:
                mockups_src = artwork_dir / str(mockups_dirname)
                if mockups_src.exists() and mockups_src.is_dir():
                    mockups_dest = bundle_root / str(mockups_dirname)
                    if mockups_dest.exists():
                        shutil.rmtree(mockups_dest, ignore_errors=True)
                    shutil.copytree(mockups_src, mockups_dest)

            mockups_files = []
            if include_mockups and mockups_dirname:
                mockups_dest = bundle_root / str(mockups_dirname)
                if mockups_dest.exists() and mockups_dest.is_dir():
                    mockups_files = [p.relative_to(bundle_root).as_posix() for p in mockups_dest.rglob("*") if p.is_file()]
                    self._update_manifest(
                        sku=sku,
                        export_id=export_id,
                        copied_mockups_count=int(len(mockups_files)),
                    )

            self._update_manifest(sku=sku, export_id=export_id, stage="zipping", message="Creating zip", done=False)
            zip_path = self.zip_path(sku, export_id)
            if zip_path.exists():
                zip_path.unlink(missing_ok=True)

            try:
                with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                    for path in sorted(bundle_root.rglob("*")):
                        if path.is_file():
                            arcname = path.relative_to(bundle_root).as_posix()
                            zf.write(path, arcname=arcname)
            except PermissionError as exc:
                raise ExportError(f"Permission denied creating zip: {zip_path}") from exc
            except OSError as exc:
                raise ExportError(f"Failed creating zip: {zip_path} ({exc})") from exc

            zip_size = 0
            try:
                zip_size = int(zip_path.stat().st_size)
            except Exception:
                zip_size = 0

            self._update_manifest(
                sku=sku,
                export_id=export_id,
                stage="complete",
                message="Export complete",
                done=True,
                error=None,
                zip_filename=zip_path.name,
                zip_size_bytes=zip_size,
            )
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Export worker failed", extra={"sku": sku, "export_id": export_id})
            self._update_manifest(
                sku=sku,
                export_id=export_id,
                stage="error",
                message="Export failed",
                done=True,
                error=str(exc),
            )


def cleanup_old_exports(exports_root: Path, max_age_minutes: int = 60) -> tuple[int, int]:
    """
    Delete export folders and ZIP files older than max_age_minutes.
    Returns (deleted_count, error_count).
    """
    if not exports_root or not exports_root.exists():
        return 0, 0

    deleted = 0
    errors = 0
    now = datetime.now(timezone.utc)
    max_age_seconds = max_age_minutes * 60

    for sku_dir in exports_root.iterdir():
        if not sku_dir.is_dir():
            continue

        for export_dir in sku_dir.iterdir():
            if not export_dir.is_dir():
                continue

            manifest_path = export_dir / "manifest.json"
            should_delete = False

            if manifest_path.exists():
                try:
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    created_at = manifest.get("created_at")
                    if created_at:
                        created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                        age_seconds = (now - created_dt).total_seconds()
                        if age_seconds > max_age_seconds:
                            should_delete = True
                except Exception:
                    stat = export_dir.stat()
                    age_seconds = (now - datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)).total_seconds()
                    if age_seconds > max_age_seconds:
                        should_delete = True
            else:
                try:
                    stat = export_dir.stat()
                    age_seconds = (now - datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)).total_seconds()
                    if age_seconds > max_age_seconds:
                        should_delete = True
                except Exception:
                    pass

            if should_delete:
                try:
                    shutil.rmtree(export_dir)
                    deleted += 1
                    logger.info(f"Cleaned up old export: {export_dir}")
                except Exception as e:
                    logger.error(f"Failed to delete export {export_dir}: {e}")
                    errors += 1

        if sku_dir.exists() and not any(sku_dir.iterdir()):
            try:
                sku_dir.rmdir()
            except Exception:
                pass

    return deleted, errors
