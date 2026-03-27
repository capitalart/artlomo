# Manual Analysis and Review Workflow — File Map

Date: 2026-03-27
Status: Current

## Scope
Process artwork without AI, edit metadata manually, then save/lock/export.

## Entry Points
- GET /manual/process/<slug>
- POST /manual/process/<slug>
- GET /manual/workspace/<slug>
- POST /manual/workspace/<slug>
- GET /manual/asset/<slug>/<filename>
- POST /artwork/<slug>/save
- POST /artwork/<slug>/lock

## Primary Files
- application/analysis/manual/routes/manual_routes.py
- application/analysis/manual/services/manual_service.py
- application/artwork/routes/artwork_routes.py
- application/common/ui/templates/analysis_workspace.html
- application/common/ui/static/js/analysis_workspace.js
- application/common/ui/static/js/manual_mockups.js

## Notes
- Manual workflow uses the shared analysis workspace template and shared JS layer.
