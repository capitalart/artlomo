# Mockup Engine V2 Implementation Record

Date: 2026-03-24
Owner context: ArtLomo / DreamArtMachine
Scope: Fresh 5-service implementation for mockup pipeline, isolated from legacy logic.

## 1) Why This Was Built
The previous generation flow has mixed concerns and legacy branches. V2 introduces a strict service-per-concern architecture so each stage can be tested, monitored, and replaced independently.

## 2) Services Implemented

### Service A: MockupGenerationService (Painter)
File: `application/mockups/v2/services/mockup_generation_service.py`
- Gemini image generation wrapper with strict hard-fail behavior.
- Uses `gemini-2.5-flash-image` by default.
- Fails when prompt is empty, API key missing, SDK call fails, or no image bytes are returned.

### Service B: CoordinateExtractionService (Surveyor)
File: `application/mockups/v2/services/coordinate_extraction_service.py`
- Pure OpenCV path, no AI.
- Detects cyan marker via HSV threshold + contour extraction.
- Enforces exact 4-corner detection.
- Orders points as TL/TR/BR/BL.
- Produces:
  - coordinate JSON (pixel and normalized points)
  - transparent PNG with alpha punched out in artwork area

### Service C: BaseCatalogService (Librarian)
File: `application/mockups/v2/services/base_catalog_service.py`
- Updates `mockup_base_generation_jobs` lifecycle state.
- Registers catalog entry only if required files exist:
  - transparent base PNG
  - coordinate JSON
  - thumbnail PNG
- Writes v2 catalog index:
  - `/srv/artlomo/var/state/mockup_base_catalog_v2.json`

### Service D: CompositeRenderService (Builder)
File: `application/mockups/v2/services/composite_render_service.py`
- Loads artwork and transparent base.
- Computes homography and warps artwork to target quad.
- Alpha-composites warped layer below base details.
- Writes high-quality JPEG output.

### Service E: HarmonizationService (Polisher)
File: `application/mockups/v2/services/harmonization_service.py`
- Optional final pass.
- If disabled: deterministic copy-through.
- If enabled: strict hard-fail on model failure.

## 3) Orchestration Layer
File: `application/mockups/v2/pipeline_orchestrator.py`

Lifecycle transitions:
- `Pending` -> `Generating` -> `Extracting` -> `Catalog_Ready`

Failure transitions:
- Detection failure (not exactly 4 corners) -> `Review_Required`
- All other processing/call failures -> `Failed`

The orchestrator also creates thumbnail output and enforces strict registration preconditions.

## 4) Queue Integration
File: `application/mockups/v2/tasks_v2.py`

Celery tasks added:
- `mockup_v2.generate_base_and_coordinates`
- `mockup_v2.render_composite`

Purpose:
- Attach to queue-admin and generator dashboards without inheriting old task logic.

## 5) Input / Output Contracts
File: `application/mockups/v2/contracts.py`

Provides dataclasses for all service boundaries:
- generation input/result
- extraction input/result
- composite render input/result
- harmonization input/result
- pipeline orchestration input/result

Status enum (`CatalogState`):
- `Pending`, `Generating`, `Extracting`, `Review_Required`, `Catalog_Ready`, `Failed`

## 6) Isolation from Legacy Code
All v2 implementation is in:
- `application/mockups/v2/`

No legacy route/task/service files were modified by this implementation step.

## 7) Mapping to Requested Admin Pages
The following pages should call v2 adapters incrementally behind a feature flag:
- `/admin/mockups/gemini-studio`
- `/admin/mockups/basic-mockups`
- `/admin/mockups/ezy-mockups`
- `/admin/mockups/precision-mockups`
- `/admin/mockups/mockup-generator/queue-admin`

## 8) Recommended Rollout Sequence
1. Add route flags to switch each page to v2 task calls.
2. Enable v2 on queue-admin first (observability page).
3. Move gemini-studio and basic-mockups to v2 generation task.
4. Move ezy and precision pages to v2 coordinate/composite path.
5. Keep fallback toggle for one release window, then remove legacy wiring.

## 9) Operational Notes
- v2 generation requires `GEMINI_API_KEY` in environment.
- Coordinate extraction assumes cyan marker around `#00FFCC` with HSV tolerance.
- Detection anomalies are intentionally routed to `Review_Required`.
- Catalog registration is blocked unless all required artifacts exist.

## 10) Future Enhancements
- Add dedicated DB table for v2 artifact records with thumbnail path column.
- Add explicit geometry QA metrics (edge angle, rectangular confidence score).
- Add image-conditioned harmonization edit endpoint (instead of prompt-only generation path).
- Add unit tests for:
  - HSV extraction edge cases
  - homography numerical stability
  - state transition correctness
