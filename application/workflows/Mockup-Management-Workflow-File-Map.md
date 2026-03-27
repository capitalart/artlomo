# Mockup Management Workflow — File Map (Current Implementation)

## Scope

Generate mockups, serve thumbs/composites, support per-slot category updates and swap, and keep assets index in sync.

## Entry Points

- `POST /artwork/<slug>/mockups/generate`

- `POST /artwork/<slug>/mockups/<slot>/swap`

- `POST /artwork/<slug>/mockups/<slot>/category`

- `GET /artwork/<slug>/mockups/thumb/<slot>`

- `GET /artwork/<slug>/mockups/composite/<slot>`

- delete endpoints used by workspace JS (`delete-selected`, `delete-all`)

## Primary Files

### Routes / Workflow Orchestration

- `application/mockups/routes/mockup_routes.py`

  - Aspect preflight, template eligibility, generate/swap/category operations, thumb/composite serving.

### Core Generation + Storage

- `application/mockups/pipeline.py`

  - Composite generation and slot write path.

- `application/mockups/storage.py`

  - Output path resolution + atomic JSON writes.

- `application/mockups/config.py`

  - Mockup path/naming constants.

### Catalog + Selection

- `application/mockups/catalog/loader.py`

- `application/mockups/catalog/validation.py`

- `application/mockups/selection/planner.py`

- `application/mockups/assets_index.py`

### Rendering + Transform

- `application/mockups/compositor.py`

- `application/mockups/transforms.py`

- `application/mockups/validation.py`

### UI / Frontend

- `application/common/ui/templates/analysis_workspace.html`

  - Mockup grid card, category selector, swap button, loading overlay.

- `application/common/ui/static/js/manual_mockups.js`

  - Swap/category fetch operations + overlay state.

- `application/common/ui/static/js/mockup_selection.js`

  - Selection and delete flows.

- `application/common/ui/static/js/mockup_carousel.js`

  - Preview navigation.

### Admin Mockup Management

- `application/mockups/admin/routes/mockup_admin_routes.py`

- `application/mockups/admin/services.py`

- `application/mockups/admin/preview.py`

## Data Paths

- Base assets: `application/mockups/catalog/assets/mockups/bases/` (dynamic aspect/category subfolders)

- Per artwork outputs: `lab/processed/<slug>/mockups/`

- Assets index: `lab/processed/<slug>/<slug>-assets.json`

## Notes

- Perspective coordinate contract is v2.0, clockwise TL/TR/BR/BL ordering.

- Composite order remains artwork first, base PNG last.
