# Export Workflow Report

Date: 2026-03-27
Status: Active

## Scope
Asynchronous listing bundle export with status polling and downloadable archive.

## Entry Points
- POST /api/export/<sku>
- GET /api/export/status/<sku>
- GET /api/export/download/<sku>/<export_id>
- GET /api/export/has-mockups/<sku>
- GET /artwork/<slug>/admin-export/<provider>

## Core Files
- application/export/api/routes.py
- application/export/service.py
- application/artwork/routes/artwork_routes.py

## Runtime Flow
1. Export request validates SKU and prerequisite assets.
2. Export service builds manifest and archive in background task.
3. Status endpoint reports progress state.
4. Download endpoint serves completed archive by export id.

## Outputs
- Export bundle (zip)
- Export metadata and status

## Notes
- Artwork-level admin export route remains available for provider-specific actions.
