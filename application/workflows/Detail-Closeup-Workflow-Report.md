# Detail Closeup Workflow Report

Date: 2026-03-27
Status: Active

## Scope
Generate and edit detail closeup assets from processed artworks using normalized coordinates.

## Entry Points
- GET /artwork/<slug>/detail-closeup/editor
- POST /artwork/<slug>/detail-closeup/save
- POST /artwork/<slug>/detail-closeup/freeze
- GET /artwork/<slug>/detail-closeup/proxy
- GET /artwork/<slug>/detail-closeup
- GET /artwork/<slug>/detail-closeup-thumb

## Core Files
- application/artwork/routes/artwork_routes.py
- application/artwork/services/detail_closeup_service.py
- application/artwork/services/processing_service.py
- application/common/ui/static/js/detail_closeup.js
- application/common/ui/static/js/detail_closeup_init.js
- application/docs/schema_coordinates.json

## Runtime Flow
1. Editor route ensures source assets exist and prepares proxy image if needed.
2. UI captures coordinate focus region.
3. Save route writes coordinate metadata and renders closeup image variants.
4. Freeze route finalizes coordinate state for downstream workflows.
5. Asset routes serve proxy, full closeup, and thumbnail.

## Outputs
- Coordinate metadata JSON
- Closeup image
- Closeup thumbnail

## Notes
- Coordinate schema remains normalized and compatible with video generation inputs.
