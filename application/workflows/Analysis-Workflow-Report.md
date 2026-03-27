# Analysis Workflow Report

Date: 2026-03-27
Status: Active

## Scope
AI analysis (OpenAI/Gemini), manual analysis, status lifecycle, review workspace, save/lock transitions.

## Entry Points
- POST /api/analysis/openai/<slug>
- POST /api/analysis/gemini/<slug>
- GET /api/analysis/status/<slug>
- GET /manual/process/<slug>
- POST /manual/process/<slug>
- GET /manual/workspace/<slug>
- POST /manual/workspace/<slug>
- GET /artwork/<slug>/review

## Core Files
- application/analysis/api/routes.py
- application/analysis/openai/service.py
- application/analysis/openai/schema.py
- application/analysis/gemini/service.py
- application/analysis/gemini/schema.py
- application/analysis/prompts.py
- application/analysis/manual/routes/manual_routes.py
- application/analysis/manual/services/manual_service.py
- application/artwork/routes/artwork_routes.py
- application/common/ui/templates/analysis_workspace.html
- application/common/ui/static/js/analysis_workspace.js

## Runtime Flow
1. API trigger validates slug and current stage.
2. Async worker performs provider call and normalizes payload.
3. listing.json and status metadata are written under processed slug directory.
4. Review workspace renders analysis output for edits.
5. Save and lock routes persist final listing and advance lifecycle.

## Outputs
- listing.json (analysis metadata)
- provider snapshots (where configured)
- status updates consumed by polling endpoint

## Notes
- OpenAI parser module path documented in older files is obsolete; schema + service are current.
- Manual workspace JS/templates are now centralized under common UI.
