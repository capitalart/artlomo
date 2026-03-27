# Upload Workflow Report

Date: 2026-03-27
Status: Active

## Scope
Artwork ingestion, QC, derivative generation, stage galleries, and lifecycle transitions.

## Entry Points
- GET /upload
- POST /upload
- GET /unprocessed
- GET /processed
- GET /locked
- GET /trash
- POST /unprocessed/<slug>/delete
- POST /processed/<slug>/delete
- POST /trash/<slug>/restore
- POST /trash/<slug>/permanent-delete

## Core Files
- application/upload/routes/upload_routes.py
- application/upload/services/qc_service.py
- application/upload/services/storage_service.py
- application/upload/services/thumb_service.py
- application/common/ui/templates/artworks/upload.html
- application/common/ui/static/js/upload.js

## Runtime Flow
1. Upload route validates file and creates slug workspace.
2. QC service computes quality checks and metadata.
3. Storage service writes source + derivatives atomically.
4. Gallery routes expose stage-specific views.
5. Delete/restore endpoints maintain lifecycle integrity.

## Outputs
- Processed artwork folder structure
- Thumbnail/analyse derivatives
- QC and metadata files
