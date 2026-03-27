# Upload Workflow — File Map

Date: 2026-03-27
Status: Current

## Scope
Ingest artwork files, run QC/derivative generation, and manage lifecycle galleries.

## Entry Points
- GET/POST /upload
- GET /unprocessed
- GET /processed
- GET /locked
- GET /trash
- lifecycle delete/restore endpoints under upload routes

## Primary Files
- application/upload/routes/upload_routes.py
- application/upload/services/qc_service.py
- application/upload/services/storage_service.py
- application/upload/services/thumb_service.py
- application/common/ui/templates/artworks/upload.html
- application/common/ui/static/js/upload.js
- application/common/ui/static/js/upload_gallery.js
