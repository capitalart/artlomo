# Closeup Detail Generation Workflow — File Map (Current Implementation)

## Scope

Generate 7200px proxy, open editor, map normalized center coordinates, render 2048x2048 detail closeup, and expose closeup assets for workspace/export.

## Entry Points

- `GET /artwork/<slug>/detail-closeup/editor`

- `POST /artwork/<slug>/detail-closeup/save`

- `GET /artwork/<slug>/detail-closeup/proxy`

- `GET /artwork/<slug>/detail-closeup`

- `GET /artwork/<slug>/detail-closeup-thumb`

## Primary Files

### Routes

- `application/artwork/routes/artwork_routes.py`

  - Editor render and save endpoint, proxy/detail/thumb serving.

### Service Layer

- `application/artwork/services/detail_closeup_service.py`

  - Proxy generation, crop rendering, closeup existence checks, thumb generation.

- `application/artwork/services/processing_service.py`

  - Promotion-time integration and proxy guard behavior.

### Frontend

- `application/artwork/ui/templates/detail_closeup_editor.html`

- `application/common/ui/static/js/detail_closeup.js`

- `application/common/ui/static/css/detail_closeup.css`

### Workspace Integration

- `application/common/ui/templates/analysis_workspace.html`

  - Detail tile and links to editor/view/thumb.

## Data/Asset Outputs

- Proxy: `lab/processed/<slug>/<slug>-CLOSEUP-PROXY.jpg` (long edge 7200)

- Detail full: `lab/processed/<slug>/mockups/<slug>-detail-closeup.jpg`

- Detail thumb: `lab/processed/<slug>/mockups/thumbs/<slug>-detail-closeup.jpg`

## Contract Notes

- Frontend normalization uses rendered dimensions (`offsetWidth/offsetHeight`).

- Save payload includes `norm_x`, `norm_y`, `scale`.

- Backend crop output remains 2048x2048.
