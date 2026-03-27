# Admin Hub

The Admin Hub hosts minimal controls for the clean-room workflows.

## Pages

- `/admin/hub/` — landing page with links.

- `/admin/hub/style` — style preset editor. Saves a JSON preset to `var/themes/<name>.json` and generates a modular preset stylesheet at `application/common/ui/static/css/presets/<name>.css`.

## Theme pipeline

- Defaults live in `application/admin/hub/services/style_service.py` (`DEFAULTS`).

- Admin saves/applies a preset, `StyleService` writes a standalone preset stylesheet in `common/ui/static/css/presets/`.

- The base template links only the active preset CSS (`css/presets/<active>.css`).

## Assets

- Templates under `application/admin/hub/aui/templates/`.

- Static assets under `application/admin/hub/aui/static/`.

## Callers

- Routes defined in `application/admin/hub/routes/hub_routes.py` mount the templates and static assets.

- Admin navbar links from `common/ui/templates/components/navbar.html` point to the hub and style editor.
