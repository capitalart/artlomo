# AI Analysis and Review Workflow — File Map

Date: 2026-03-27
Status: Current

## Scope

Trigger OpenAI/Gemini analysis, track status, and render editable review workspace.

## Entry Points

- POST /api/analysis/openai/{slug}
- POST /api/analysis/gemini/{slug}
- GET /api/analysis/status/{slug}
- GET /artwork/{slug}/analysis/openai
- GET /artwork/{slug}/analysis/gemini
- GET /artwork/{slug}/review
- POST /artwork/{slug}/save
- POST /artwork/{slug}/lock

## Primary Files

- application/analysis/api/routes.py
- application/analysis/openai/service.py
- application/analysis/openai/schema.py
- application/analysis/gemini/service.py
- application/analysis/gemini/schema.py
- application/analysis/prompts.py
- application/artwork/routes/artwork_routes.py
- application/common/ui/templates/analysis_workspace.html
- application/common/ui/static/js/analysis_workspace.js
- application/common/ui/static/js/analysis_validation.js

## Outputs

- listing.json and analysis status metadata under processed artwork directory.
