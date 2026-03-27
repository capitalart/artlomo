# Mockup Management Workflow Report

Date: 2026-03-27
Status: Active

## Scope
Mockup generation, slot updates, category assignment, composite/thumb serving, and cleanup.

## Entry Points
- POST /artwork/<slug>/mockups/generate
- POST /artwork/<slug>/mockups/<slot>/swap
- POST /artwork/<slug>/mockups/<slot>/category
- POST /artwork/<slug>/mockups/delete-all
- POST /artwork/<slug>/mockups/delete-selected
- GET /artwork/<slug>/mockups/thumb/<slot>
- GET /artwork/<slug>/mockups/composite/<slot>

## Core Files
- application/mockups/routes/mockup_routes.py
- application/mockups/pipeline.py
- application/mockups/storage.py
- application/mockups/catalog/
- application/mockups/services/
- application/mockups/tasks_mockup_generator.py
- application/mockups/v2/

## Runtime Flow
1. Route validates aspect ratio and mockup prerequisites.
2. Generation pipeline composes outputs and metadata per slot.
3. Storage layer writes assets atomically.
4. Serving routes expose slot thumbnails and composites.
5. Delete routes remove selected/all slot outputs and refresh indexes.

## Outputs
- Mockup composite images
- Slot thumbnails
- Mockup metadata/index files

## Notes
- V2 services under application/mockups/v2 are active for newer engine paths.
