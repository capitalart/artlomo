# Export Workflow — File Map (Current Implementation)

## Scope

Create asynchronous export bundles (ZIP), expose status polling, and provide download endpoint. Includes artwork-route admin export path.

## Entry Points

- API export path:

  - `POST /api/export/<sku>`

  - `GET /api/export/status/<sku>`

  - `GET /api/export/download/<sku>/<export_id>`

  - `GET /api/export/has-mockups/<sku>`

- Artwork admin export path:

  - `GET /artwork/<slug>/admin-export/<provider>`

## Primary Files

### API Routes

- `application/export/api/routes.py`

  - Trigger async export, status polling, download, mockup presence check.

### Service Layer

- `application/export/service.py`

  - ExportService worker thread, manifest updates, bundle copy, zip creation, cleanup.

### Artwork Integration

- `application/artwork/routes/artwork_routes.py`

  - Admin export route uses `AdminExportService` and security logging.

### Frontend

- `application/common/ui/static/js/export_async.js`

- `application/common/ui/templates/analysis_workspace.html` (export buttons)

### Shared Dependencies

- `application/artwork/services/index_service.py` (`ArtworksIndex`)

- `application/common/utilities/files.py` (atomic/dir operations)

- `application/utils/csrf.py` (mutating request safety)

## Export Data Locations

- Root: `var/exports/<sku>/<export_id>/`

- Manifest: `manifest.json`

- Bundle temp tree: `bundle/`

- Final archive: `<sku>-<export_id>.zip`

## Notes

- Workflow is non-blocking and manifest-driven.

- Includes optional mockup copy and required asset enforcement modes.
