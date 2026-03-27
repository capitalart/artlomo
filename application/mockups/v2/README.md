# Mockup Engine V2 (Fresh Architecture)

## Purpose

This package implements a strict 5-service mockup base pipeline, isolated from legacy generator logic.

Target flow:

1. Generate mockup base scene (Gemini)
2. Extract exact 4-point coordinates (OpenCV, deterministic)
3. Register base only if all required assets exist
4. Render perspective composite from artwork + base
5. Optional harmonization pass

## Package Layout

- `contracts.py`: strict input/output dataclasses and status enum
- `exceptions.py`: domain errors used across all services
- `services/mockup_generation_service.py`: Service A (Painter)
- `services/coordinate_extraction_service.py`: Service B (Surveyor)
- `services/base_catalog_service.py`: Service C (Librarian)
- `services/composite_render_service.py`: Service D (Builder)
- `services/harmonization_service.py`: Service E (Polisher)
- `pipeline_orchestrator.py`: strict orchestration and lifecycle state transitions
- `tasks_v2.py`: Celery task entry points

## Strict Contracts

See `contracts.py` for exact dataclasses.

### Status Lifecycle

`CatalogState` values:

- `Pending`
- `Generating`
- `Extracting`
- `Review_Required`
- `Catalog_Ready`
- `Failed`

Rules:

- Any generation failure => hard fail (`Failed`)
- Coordinate extraction with not-exactly-4 corners => `Review_Required`
- Catalog registration only when PNG + JSON + thumbnail all exist

## Service Details

### A. MockupGenerationService

- Uses Gemini image generation model (`gemini-2.5-flash-image` default)
- Hard-fail policy: no silent fallback images
- Writes output bytes to requested path

### B. CoordinateExtractionService

- Deterministic OpenCV pipeline:
  - HSV threshold on cyan range
  - contour detection
  - polygon approximation
  - requires exactly 4 points
- Point order is always:
  - `TL`, `TR`, `BR`, `BL`
- Writes:
  - coordinate JSON with pixel + normalized points
  - transparent PNG where marker polygon alpha is zero

### C. BaseCatalogService

- Updates DB job status in `mockup_base_generation_jobs`
- Maintains v2 catalog index JSON at:
  - `/srv/artlomo/var/state/mockup_base_catalog_v2.json`
- Registers only when all three artifacts exist:
  - transparent base PNG
  - coordinates JSON
  - thumbnail PNG

### D. CompositeRenderService

- Loads high-res artwork + transparent base + coordinate JSON
- Computes homography matrix and applies perspective warp
- Alpha-composites base over warped art for realistic frame layering
- Saves high-quality JPEG

### E. HarmonizationService

- Optional pass
- If disabled, performs deterministic pass-through copy
- If enabled, hard-fails on any Gemini failure

## Celery Tasks

`tasks_v2.py` exposes:

- `mockup_v2.generate_base_and_coordinates`
- `mockup_v2.render_composite`

Broker/backend defaults to `CELERY_BROKER_URL` or `redis://localhost:6379/0`.

## Integration Boundaries

This v2 package does not replace legacy routes automatically.
It is designed to be called from route/task adapters associated with:

- `/admin/mockups/gemini-studio`
- `/admin/mockups/basic-mockups`
- `/admin/mockups/ezy-mockups`
- `/admin/mockups/precision-mockups`
- `/admin/mockups/mockup-generator/queue-admin`

## Next Recommended Wiring

1. Add route-level feature flag (legacy vs v2)
2. Submit queue jobs via `mockup_v2.generate_base_and_coordinates`
3. Surface `CatalogState` values in queue admin UI
4. Add manual-review queue for `Review_Required` jobs
5. Wire composite action to `mockup_v2.render_composite`
