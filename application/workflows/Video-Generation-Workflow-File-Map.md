# Video Generation Workflow — File Map

Date: 2026-03-27
Status: Current (dual-path)

## Scope
Generate and serve artwork promo videos through artwork and API paths.

## Entry Points
- POST /artwork/<slug>/video/generate
- GET /artwork/<slug>/video
- GET /artwork/<slug>/video-status
- POST /api/video/generate/<slug>
- GET /api/video/status/<slug>

## Primary Files
- application/artwork/routes/artwork_routes.py
- application/video/routes/video_routes.py
- application/video/services/video_service.py
- application/common/ui/templates/video_workspace.html
- application/common/ui/static/js/video_cinematic.js
- application/common/ui/static/js/video_workspace_carousel.js

## Notes
- Historical references to video_pipeline_service.py and manual video JS files are deprecated.
