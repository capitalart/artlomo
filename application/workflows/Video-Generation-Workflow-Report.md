# Video Generation Workflow Report

Date: 2026-03-27
Status: Active (dual-path)

## Scope
Generate short promo/kinematic videos from processed artwork assets.

## Entry Points
- POST /artwork/<slug>/video/generate
- GET /artwork/<slug>/video
- DELETE /artwork/<slug>/video
- GET /artwork/<slug>/video-status
- POST /api/video/generate/<slug>
- GET /api/video/status/<slug>

## Core Files
- application/artwork/routes/artwork_routes.py
- application/video/routes/video_routes.py
- application/video/services/video_service.py
- application/common/ui/templates/video_workspace.html
- application/common/ui/static/js/video_cinematic.js
- application/common/ui/static/js/video_workspace_carousel.js

## Runtime Flow
1. Artwork or API trigger starts generation job.
2. Service builds cinematic output from source assets and settings.
3. Status endpoint reports progress.
4. Stream endpoint serves completed video.

## Notes
- Historical references to video_pipeline_service.py are stale; video_service.py is current.
