# Mockup admin (Phase 3A)

Purpose: manage mockup bases (upload, coordinate generation, categorization) without touching
per-artwork assets or generation logic.

- Bases are RGBA PNGs.

- Coordinates are generated automatically on upload and stored alongside the base.

- Bases are stored under `application/mockups/catalog/assets/mockups/bases/<aspect>/<category>/<slug>.{png,json}`.

Forbidden:

- Generating mockups or editing per-artwork assets.

- Guessing paths or scanning directories.

- Disabling mandatory templates.

## UI wiring (Phase 3B)

- Blueprint: `/admin/mockups` (mockup admin UI lives under `ui/templates/mockups/`).

- Bases screen: `/admin/mockups/bases` shows all bases with filters, bulk actions, and preview tooling.

- Upload screen: `/admin/mockups/bases/upload` ingests base PNGs and generates coordinates automatically.

- Categories: `/admin/mockups/categories` renames categories without touching assets.

- Artwork viewer: `/admin/mockups/artworks/<sku>/mockups` is read-only and pulls slots from `<sku>-assets.json`; thumbnails are served directly from the processed artwork folder.
