"""Service C: BaseCatalogService (The Librarian).

Registers assets only when PNG, JSON, and thumbnail are all present.
Writes lifecycle state into DB job record and a v2 catalog JSON index.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from db import MockupBaseGenerationJob, SessionLocal

from ..contracts import CatalogState
from ..exceptions import CatalogRegistrationError


class BaseCatalogService:
    """Maintain strict catalog integrity with explicit lifecycle states."""

    def __init__(self, catalog_path: Path | None = None):
        self._catalog_path = Path(
            catalog_path or "/srv/artlomo/var/state/mockup_base_catalog_v2.json"
        )

    def set_state(
        self,
        job_id: str,
        state: CatalogState,
        *,
        reason: str | None = None,
        error_message: str | None = None,
    ) -> None:
        with SessionLocal() as session:
            job = (
                session.query(MockupBaseGenerationJob)
                .filter(MockupBaseGenerationJob.job_id == job_id)
                .first()
            )
            if not job:
                raise CatalogRegistrationError(f"Job not found for state update: {job_id}")

            job.status = state.value
            job.reason = reason
            job.error_message = error_message
            job.updated_at = datetime.utcnow()
            if state in {CatalogState.CATALOG_READY, CatalogState.FAILED}:
                job.finished_at = datetime.utcnow()
            session.commit()

    def register_if_complete(
        self,
        *,
        job_id: str,
        base_png_path: Path,
        coordinates_json_path: Path,
        thumbnail_path: Path,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        missing = [
            str(path)
            for path in (base_png_path, coordinates_json_path, thumbnail_path)
            if not Path(path).exists()
        ]
        if missing:
            raise CatalogRegistrationError(
                f"Catalog registration blocked; missing assets: {', '.join(missing)}"
            )

        self._upsert_catalog_entry(
            job_id=job_id,
            base_png_path=Path(base_png_path),
            coordinates_json_path=Path(coordinates_json_path),
            thumbnail_path=Path(thumbnail_path),
            metadata=metadata or {},
        )

    def _upsert_catalog_entry(
        self,
        *,
        job_id: str,
        base_png_path: Path,
        coordinates_json_path: Path,
        thumbnail_path: Path,
        metadata: dict[str, Any],
    ) -> None:
        self._catalog_path.parent.mkdir(parents=True, exist_ok=True)

        payload: dict[str, Any]
        if self._catalog_path.exists():
            try:
                payload = json.loads(self._catalog_path.read_text(encoding="utf-8"))
            except Exception:
                payload = {}
        else:
            payload = {}

        if not isinstance(payload, dict):
            payload = {}

        entries = payload.get("entries")
        if not isinstance(entries, dict):
            entries = {}
            payload["entries"] = entries

        entries[job_id] = {
            "job_id": job_id,
            "base_png_path": str(base_png_path),
            "coordinates_json_path": str(coordinates_json_path),
            "thumbnail_path": str(thumbnail_path),
            "state": CatalogState.CATALOG_READY.value,
            "metadata": metadata,
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }

        self._catalog_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
