# ArtLomo

![Repository](https://img.shields.io/badge/repository-artlomo-0a7ea4)
![Branch](https://img.shields.io/badge/branch-main-2ea44f)
![Status](https://img.shields.io/badge/status-bootstrap-stable)

Modular, workflow-oriented Flask application. All contributors (humans and AI) **must** follow the architectural contract defined here and in application/docs/ARCHITECTURE_INDEX.md.

## Hard Rules (must read before changes)

- Codex (and any AI) must read this README and application/docs/ARCHITECTURE_INDEX.md before modifying code.

- Any architectural change must update application/docs/ARCHITECTURE_INDEX.md in the same task.

- Artwork single-state invariant: a slug can exist only in one of `lab/unprocessed/<slug>/` or `lab/processed/<slug>/` at any time; promotions are moves, never copies; reanalysis never creates new folders.

- Delete ownership: each workflow owns its delete UX; no global delete handlers may attach outside their scope.

- No global UI handlers without explicit scoping/guards.

## ⚠️ AI ASSISTANT STARTUP INSTRUCTIONS (READ FIRST)

**Windsurf/Cascade and any AI assistant MUST execute this sequence before starting work:**

1. **OPEN & DISPLAY:** `.windsurfrules` (workspace root)

- **Contains:** Windsurf Golden Loop, architecture boundaries, mockup perspective contract, security constraints

- **Why:** Defines non-negotiable project standards for this repository

1. **CONSULT:** `application/docs/DEFINITION_OF_DONE.md`

- **Contains:** Task completion criteria (asset resolution, UI compliance, logging, cleanup)

- **Why:** Determines when work is actually "done"

1. **REFERENCE:** `application/docs/ARCHITECTURE_INDEX.md`

- **Contains:** System design, workflow boundaries, allowed imports, current state

- **Why:** Prevents architectural violations and broken imports

1. **OPTIONAL (LEGACY / TOOL-SPECIFIC):** `.copilotrules`, `.clinerules`, `.cursorrules`, `.github/COPILOT.md`

- **Contains:** Copilot-specific or legacy guidance retained for compatibility

## Auto-Reminders

- `.vscode/tasks.json` — On folder open, prints `.windsurfrules`

- `.vscode/tasks.json` — Manual task available: "📋 Show Legacy Copilot Rules (.copilotrules)"

## Bottom Line

Unless you've read `.windsurfrules`, you're not ready to code on ArtLomo. This is non-negotiable.

---

## Project Overview

- Production Flask app scoped to `/srv/artlomo/application`.

- Workflows are isolated by folder (e.g., upload, mockups, artwork, admin, lab, tools, backups).

- Shared layers live in `application/common` (UI/shared helpers) and `application/utils` (low-level utilities). No legacy paths are permitted.

- **Comprehensive Workflow Documentation:** Detailed reports for each workflow are available in `/application/workflows/` with code examples, data flows, and logging patterns (see [MASTER_WORKFLOWS_INDEX.md](application/docs/MASTER_WORKFLOWS_INDEX.md#-comprehensive-workflow-reports)).

## AI Handoff Snapshot

Use these commands when you need one clean artifact to share with Gemini or another external AI reviewer.

```bash
cd /srv/artlomo

# Preferred single-file handoff (curated, excludes noisy/archived areas)

./application/tools/app-stacks/files/tools.sh gemini

# Optional full operational snapshot

./application/tools/app-stacks/files/tools.sh all
```

Outputs:

- Gemini handoff file: `application/tools/app-stacks/stacks/application-gemini-code-stack-<TIMESTAMP>.md`

- Full stack file: `application/tools/app-stacks/stacks/application-code-stack-<TIMESTAMP>.md`

- Folder structure, backup, and system inventory files in the same `app-stacks` output folders

Security note:

- The Gemini stack excludes `.env` by default. Keep it that way when sharing files externally.

## Project Goals

- Automated generation of museum-quality, Etsy-compliant digital listings.

- Robust Multi-Model AI Analysis with automatic JSON sanitization for cross-model compatibility (OpenAI + Gemini).

- **Pioneer Engine v1.0:** Advanced Etsy SEO generation with 13-point story structure and cultural guardrails.

- **Museum-Grade Standard:** Native support for 14,400px / 300 DPI exports enabling 48-inch gallery prints.

- **Standardized Multi-Provider AI Analysis:** Centralized `LISTING_BOILERPLATE` ensures identical description structure from OpenAI and Gemini (Limited Edition, Technical Specs, Size Guide, Acknowledgement of Country).

- **Theme-Aware Admin Hub:** Elevated Glass headers with `backdrop-filter: blur(12px)` and seamless Light/Dark mode transitions.

- **Human-in-the-Loop AI Pipeline:** Artist-provided metadata (Location, Sentiment, Original Prompt) is injected into AI system prompts before visual analysis.

- **Sentiment-Driven Analysis:** Guided Creative Engine extrapolates single-word sentiments (e.g., "Ghostly", "Ethereal") into full narrative tone and vocabulary.

- **High-Detail AI Vision:** ANALYSE images standardized at 2048px long edge for optimal AI model processing.

- **seed_context.json Bridge:** Artist intent travels atomically with artwork from unprocessed → processed during promotion; internal generation prompts inform style but are stripped from public listings.

- **Standardized Digital Release Format:** Every listing includes Acknowledgement of Country, Limited Edition notice, and Technical Specifications.

- **Detail Closeup Editor v2.1:** Non-destructive, resolution-independent cropping with normalized coordinates (0.0-1.0) for perfect alignment across proxy (7200px) and master (14400px+) images. Features Focal Point Zooming (preserves viewport center), Direct Cut snap button for 1:1 pixel mapping, and smooth pan/zoom with real-time preview updates.

## Workflow Lifecycle (text diagram)

| - Flow: Upload → Analysis (OpenAI | Gemini | Manual) → Processed → Review/Delete. |

- Single-copy invariant: promotions move the slug from `lab/unprocessed/<slug>/` to `lab/processed/<slug>/` and remove the source; reanalysis edits the processed copy in place.

- Triggers: any analysis entrypoint (OpenAI/Gemini/Manual) performs the promotion before rendering.

## Merchant Mode Checklist (12-day sprint)

- Day 1–3: Export bundles per SKU (include mockups).

- Day 4–6: Rename files using the Pioneer v2.0 SEO filename contract (SKU-Short-Title-Location, <= 70 chars).

- Day 7–9: Bulk upload to Etsy (assets + thumbnails + mockups).

- Day 10–12: Copy/paste listing fields (title, description, tags, materials) from `listing.json` into Etsy.

## Setup

- Required env:

  - `FLASK_SECRET_KEY`

  - `ADMIN_USERNAME`

  - `ADMIN_PASSWORD`

- AI keys (optional but needed for analysis):

  - `OPENAI_API_KEY`

  - `GEMINI_API_KEY`

- Profile system:

  - Create `application/var/profile.json` (or visit `/admin/profile`) to set `artist_name`, `artist_story`, and optional `profile_image_path`.

  - The profile is loaded at runtime and is used by the Heritage-First system prompt.

## Linear Workflow (Clean-Room UI/UX)

- **Upload** → **QC** → **AI Analysis** (OpenAI | Gemini) or **Manual** → **Processed** → **Review [Single Action Bar]** → (optional) **Locked**

- **Analysis Workspace Progression**:

  - Edit metadata fields in scrollable right pane

  - Click **Save Changes** to persist edits

  - Click **Lock** to finalize listing (moves to locked state)

  - Click **Re-Analyse** to re-run current AI provider (context-aware)

  - Click **Export** to export to Etsy (Etsy only, no multi-provider clutter)

  - Click **Delete** to trigger modal-protected deletion

- **No Decision Paralysis**: User never wonders what button to click next—action context is clear.

## Workstation Layout (Analysis Lab) — Clean-Room Edition (v2.0)

- Analysis/edit pages are built as a **dual-pane, distraction-free workstation**:

  - Container: capped at 2400px.

  - Grid: 45% left pane (media/imagery — stationary) | 55% right pane (forms/actions — scrolling).

  - Left pane: Artwork preview + Detail Closeup (side-by-side, max 500px each), Video panel, Mockups panel.

  - Right pane: **Unified sticky Action Bar** at top + scrollable form/data below.

- **Unified Action Bar (Linear Workflow)**:

  | - Contains exactly 5 actions: **Save Changes** | **Lock** (green) | **Re-Analyse** (context-aware) | **Export** (Etsy) | **Delete** (modal with typed confirmation). |

- No button clutter: only actions relevant to current task are visible.

  - Sticky positioning ensures action bar remains accessible during form scrolling.

- **Media Panel Design**:

  - Artwork Preview + Detail Closeup displayed side-by-side (centered, max 500px each).

  - If no closeup exists: dashed border placeholder (500px).

  - "Generate Closeup" button replaces legacy "Edit" button.

  - Generate Video panel positioned between preview row and mockups grid.

  - Mockup cards feature SWAP buttons (arrows-clockwise icon) for regeneration.

- **Context-Aware Logic**:

  - Re-Analyse button detects `analysis_source` (OpenAI/Gemini) and routes to same provider.

  - No manual AI switching—streamlined re-analysis workflow.

- **Delete Safety**:

  - Delete button triggers modal requiring user to type the word "DELETE" before confirming.

  - High-safety UX for destructive actions.

- **Universal thumbnail interaction**:

  - Any image thumbnail opens the overlay carousel modal (`#artPreviewModal`) with previous/next navigation.

## AI Analysis (OpenAI + Gemini)

- Async triggers (CSRF-protected POST):

  - `/api/analysis/openai/<slug>`

  - `/api/analysis/gemini/<slug>`

- Status polling (GET):

  - `/api/analysis/status/<sku>`

- Outputs (written into `lab/processed/<slug>/`):

  - `listing.json` (enriched with AI fields + `analysis_source` and `analysis_status`)

  - `metadata_openai.json` / `metadata_gemini.json`

## Analysis Loading UX & Polling

The application provides **unified visual feedback** during asynchronous AI analysis processing:

- **Dark Overlay Interface:** Dark transparent overlay with animated spinning arrows icon and pulsing dots indicates analysis is in progress

- **Provider-Aware Routing:** OpenAI and Gemini analysis buttons correctly route to provider-specific review pages (`/artwork/<slug>/review/openai` vs `/review/gemini`)

- **Multiple Entry Points:** Consistent loading overlay used across:

  - Custom analysis form (with Location/Sentiment/Prompt fields)

  - Unprocessed gallery thumbnails (direct analysis trigger)

  - Review pages (infrastructure available for re-analysis)

  - Manual workspace (infrastructure available for complementary flows)

- **Client-Side Polling:** JavaScript module (`analysis-loading.js`) polls `/api/analysis/status/<slug>` every 1 second until completion

- **Timeout Safety:** 5-minute maximum wait (300000ms) prevents indefinite loading if backend fails silently

- **Error Handling:** Status endpoint errors are shown to user in alerts; user can retry

- **Smooth Transition:** On completion, overlay hides and page automatically redirects to analysis review page

## Infrastructure Files

- `application/common/ui/static/js/analysis-loading.js` → AnalysisLoader module with show/hide/poll/showAndWait methods

- `application/common/ui/static/css/analysis-loading.css` → Dark overlay styles with spinner animation and theme support

See [ARCHITECTURE_INDEX.md](application/docs/ARCHITECTURE_INDEX.md#analysis-loading-ux--polling-infrastructure) and [MASTER_WORKFLOWS_INDEX.md](application/docs/MASTER_WORKFLOWS_INDEX.md#workflow-2b-analysis-loading-ux--client-side-polling) for detailed documentation.

### AI Configuration

- `OPENAI_API_KEY` (required for OpenAI)

- `GEMINI_API_KEY` (required for Gemini)

- Optional:

  - `OPENAI_MODEL`

  - `GEMINI_MODEL`

### Analysis Preset Management

The system uses **Analysis Presets** as strategy containers to support multiple market approaches without code changes:

## Admin Hub: `/admin/analysis-management`

- **Dark-Themed Editor:** Form with 5 configurable prompt fields:

  - System Prompt (AI role and instructions)

  - Full Analysis Prompt (complete artwork analysis)

  - Section Edit Prompt (for re-analyzing individual sections)

  - Listing Boilerplate (standard footer text)

  - Metadata Analysis Prompt (JSON extraction)

- **Save as New:** Checkbox to create preset copies with new names (preserving originals for safe experimentation)

- **Export Preset:** Download any preset as JSON file for external modification and team sharing

- **Import Preset:** Upload JSON files to populate form fields (supports externally modified presets)

- **Provider Support:** Separate OpenAI and Gemini preset tabs with independent default presets

- **Default Preset Protection:** Default presets cannot be deleted (prevents accidental workflow breakage)

## Export Format

```json
{
  "provider": "openai",
  "name": "Pioneer Engine v1.0",
  "system_prompt": "You are a Senior Art Curator...",
  "user_full_prompt": "ARTWORK\n- Title: {title}...",
  "user_section_prompt": "Edit the following section...",
  "listing_boilerplate": "---\n🏆 LIMITED EDITION...",
  "analysis_prompt": "Extract metadata in JSON format...",
  "is_default": true
}
```

## Workflow

1. Admin customizes preset in the dark-themed editor

1. Tests new prompts by running analysis on test artwork

1. Exports preset for version control / team review

1. Team modifies externally and uploads back

1. Admin re-imports and deploys as new default

### Listing Strategy: Heritage-First Etsy Protocol

The application embeds a Heritage-First etsy listing generation approach centered on the cultural legacy of the **People of the Reeds** (Boandik/Bunganditj, Limestone Coast, South Australia). This shapes every etsy description and tag output.

### Listing Strategy: Merchant Mode / Pioneer v2.0

- Primary competitive advantage: **14,400px long edge @ 300 DPI**, enabling pin-sharp prints up to **48 inches (121.9 cm)**.

- Etsy outputs are designed to be compliance-first and export-ready for bulk listing workflows.

## Heritage & Authenticity

- Every etsy description **must** include the mandatory Boandik/Bindjali acknowledgement: "I acknowledge the Traditional Custodians of the land on which I live and create, the Bindjali people of the Naracoorte district and the Boandik people of the wider Limestone Coast."

- "People of the Reeds" is the unique brand signature and **must** appear as a tag in all etsy_tags output (exactly 13 tags total, including "people of the reeds").

- Persona: Robin Custance, South Australian artist and descendant of the People of the Reeds.

## Museum-Quality Digital Standard

- 14,400px long edge = up to 48 inches (121.9 cm) wide @ 300 DPI.

- Supports professional gallery and museum-quality printing.

- Every etsy_description **must** cite this standard (e.g., "Museum-quality digital download at 14,400px long edge for gallery-ready prints up to 48 inches wide @ 300 DPI").

## Inverted Pyramid Description Structure

All etsy_description outputs follow this 3-part structure for maximum engagement and searchability:

1. **HOOK** (Opening sentence): Subject + Style + 14,400px quality + Benefit

- Example: "Blue Wren in radiating sunbursts: a 14,400px museum-quality digital print celebrating the People of the Reeds."

1. **HEART** (Emotional narrative, 2-3 paragraphs): Emotive storytelling, cultural context, and heritage acknowledgement

- Weave in the Boandik/Bindjali acknowledgement naturally.

- Connect subject to mood and palette.

- Invite the buyer into the emotional experience.

1. **BRAIN** (Technical specs & sizing guide, bullet points): Materials, sizing guide, printing recommendations, color profile notes

- Exact dimensions, file format (typically PNG @ 300 DPI).

- Advice on printing (professional print shops, gallery canvas, etc.).

- Limited edition concept: "Only 25 copies allowed per artwork."

## Visual Analysis Fields

AI analysis output captures 4 required visual analysis fields for use in the manual workspace and downstream UIs (mood filters, palette previews, subject cards):

- `subject`: Artwork subject (e.g., "Blue Wren", "Red Kangaroo", "Bool Lagoon Sunset")

- `dot_rhythm`: Pattern/rhythm style (e.g., "radiating sunbursts", "fluid songlines", "concentric ripples")

- `palette`: Evocative color names (e.g., "Ochre, Sunrise Gold, Eucalyptus Green, Midnight Indigo")

- `mood`: Emotional tone (e.g., "tranquil", "vibrant", "introspective")

These fields ensure that the AI analysis output slots perfectly into the manual workspace listing.json structure for review, editing, and export.

## Asset Export Engine

- Trigger export (CSRF-protected POST):

  - `/api/export/<sku>`

- Status (GET):

  - `/api/export/status/<sku>`

- Download (GET):

  - `/api/export/download/<sku>/<export_id>`

- Outputs:

  - Export bundles are written under `outputs/exports/<sku>/<export_id>/`.

## Upload & Processing Lifecycle

- Upload is metadata-free: JPG/JPEG only, max 50MB per file, sequential uploads via a bespoke dropzone.

- Dropzone contract: `<div id="uploadDropzone">` with keyboard (Enter/Space) + click forwarding to `<input id="uploadFileInput" type="file" accept="image/jpeg" multiple hidden>`. Drag/drop handlers prevent browser navigation and keep the zone responsive.

- JS controller: `application/common/ui/static/js/upload.js` (UploadController) binds click/keyboard/drag events, validates type/size, posts to `/artworks/upload` with `X-Requested-With: XMLHttpRequest`, and never scans the filesystem. Theme-aware spinners swap icons per `data-theme`.

- Immediate, honest feedback: selecting files opens the modal instantly with “Uploading files…” and a spinning arrows icon (theme-aware: light/dark variants). No fake delays or percentages.

- Backend upload responds with JSON `{status, slug, thumb_url, unprocessed_url}` when invoked via AJAX; non-AJAX falls back to flash + redirect.

- Post-upload results list is session-local on the upload page: rows show the returned thumb + slug, status “Unprocessed”, and link back to `/artworks/unprocessed` without reloading.

- Stage truth only: each artwork row shows thumbnail + slug + stage text derived from `processing_status.json` message (fallback map: queued/preparing/uploading → “Preparing uploads…” or “Uploading files…”, upload_complete/processing → “Upload complete. Processing…”, qc → “Quality checking artwork…”, thumbnail → “Generating thumbnails…”, derivatives → “Generating artwork files…”, writing_metadata/metadata → “Writing metadata…”, finalizing → “Finalizing artwork…”, complete → “Processing complete”, error → “Error”). Active rows use the spinning arrows icon; no progress bars.

- Polling model: each slug is polled every 1000ms via `/artworks/<slug>/status`, which reads only `lab/unprocessed/<slug>/processing_status.json` (single source of truth). If the slug folder or status file is not present yet, the endpoint returns HTTP 200 with `{stage:"preparing", done:false}` so the UI can keep polling without 404 stalls.

- Completion: the modal is batch-gated. It only closes when (1) the batch has seen all expected slugs for the user-selected files and (2) every slug reports completion (`done:true` or `stage === "complete"`). Progress logs to the console as `Batch status: X of Y complete`. “Close” and “Run in background” hide the modal without canceling backend work; polling continues until completion to allow deterministic cleanup.

## Admin Hub Overlay & Navigation

- Single Admin Hub overlay replaces all legacy overlays; sections: Artwork Management (Upload Artwork, Unprocessed, Processed, Locked), Mockup Management (Mockup Bases, Mockup Upload), App Management (Users/Permissions/Site Styling marked "Coming Soon").

- Overlay locks scroll, closes on ESC and backdrop/outside click, and runs on local CSS/JS only with z-index above modals.

## Public Site Pages

- Placeholder informational routes (content-only templates):

  - `/about`, `/artists`, `/contact`, `/resources`, `/security`, `/privacy`, `/terms`, `/sitemap`

## Darkroom Style Editor (Theme Presets)

- Admin route: `hub.style_editor` (`/admin/hub/style-editor`).

- UI renderer: `application/admin/hub/aui/static/js/style_editor.js` (the template is intentionally minimal; JS builds the full dual-pane Light/Dark editor).

- Bootstrap JSON: `GET /admin/hub/style/data` returns `{defaults, current, presets}`.

- Save endpoint: `POST /admin/hub/style/save` accepts twin payloads `{name, light, dark, mode}`.

- Contract: the editor always edits a twin preset (`light` + `dark`) and supports live preview + reset to last loaded state.

### Clone a Site Style (Import)

- Use **Import Preset** in the Style Editor to upload a `.json` configuration file.

- The JSON is parsed client-side and immediately populates the Light/Dark panes.

- For sites that rely on bespoke selectors, paste additional rules into **Custom CSS Override**; these overrides are persisted with the preset and appended to the generated modular preset CSS file.

## Modular Preset CSS (No Global Theme Files)

- Source of truth for presets is JSON under `application/var/themes/` (root/system/user).

- Active preset state is stored under `application/var/themes/user/current_style.json`.

- CSS output is modular per preset:

  - `application/common/ui/static/css/presets/<preset>.css`

- Templates link only the active preset CSS (no global theme CSS files).

- Any change that reintroduces global theme CSS files is considered a defect.

## Typography Lock (Outfit)

- Global font is locked to Outfit via `application/common/ui/static/css/fonts.css`.

- Preset defaults use `font_family` / `font_heading` values that resolve to Outfit.

- Do not reintroduce legacy font families in preset JSON or generated preset CSS.

## Artwork State Pages

- Routes: `/artworks/upload`, `/artworks/unprocessed`, `/artworks/processed`, `/artworks/locked` (no `/upload/gallery`).

- Upload page is metadata-free (no artist/title inputs); unprocessed listing shows OpenAI Analysis, Gemini Analysis, Manual Analysis, then a full-width Delete row (no Review); processed listing shows a full-width Review row only; locked listing shows Review only.

- Gallery control panels include a top-right **"+ UPLOAD NEW ARTWORK"** action (Stark primary button) linking to `https://artlomo.com/artworks/upload`.

| - Processed listing cards render an analysis source badge (e.g. `SOURCE: OPENAI | GEMINI | MANUAL`) when the source is known. |

- Metadata DOM order: Title, Artist, ID, Uploaded Date, Aspect Ratio, Resolution, DPI, File Size, Max Print Size. Print size values are stored raw; the label renders once in UI.

- Generate Mockups never appears on listing cards; mockup actions stay in the mockup admin flows.

- State movement: any analysis (OpenAI/Gemini/Manual) promotes `lab/unprocessed/<slug>/` → `lab/processed/<slug>/` (single copy). Locked lives under `lab/locked/<slug>/`, blocks re-analysis, and hides delete.

## Upload UX & Limits

- Custom dropzone (`application/common/ui/static/js/upload.js`) supports click + drag/drop.

- JPG/JPEG only; max 50MB per file; multiple files allowed (sequential POST to `upload.handle_upload`).

- No artist/name/title inputs; SKU-driven slugging only. Metadata entry happens during analysis/review.

- Dropzone highlights on drag-over; status/error copy renders in the upload status element; there are no progress bars anywhere and no external libraries.

## Mockup Bases (Folder Source of Truth)

- Base storage root:

  - `application/mockups/catalog/assets/mockups/bases/<aspect>/<category>/`

- Physical inventory counts:

  - Category counts shown in admin dropdowns are derived by scanning the filesystem for `*.png` files under the bases tree.

  - This is the source of truth for inventory; no legacy JSON index is used for category counts.

### Current Status

- As of Jan 31, 2026, the mockup coordinate standard is **4-Point Perspective (v2.0)**.

- Coordinate JSON uses `format_version: "2.0"` and `zones[].points` (TL, TR, BR, BL).

- `catalog.json` base entries track `coordinate_type: "Perspective"` for generated coordinates.

### MU Naming Convention (Bases)

After running **Sanitize & Sync** in `/admin/mockups/bases`, base assets are normalized to:

- Base PNG: `[aspect]-[CATEGORY]-MU-[ID].png`

- Base JSON: `[aspect]-[CATEGORY]-MU-[ID].json`

- Base thumb JPG (500×500, white background): `[aspect]-[CATEGORY]-MU-THUMB-[ID].jpg`

### Sanitize & Sync

- UI: `/admin/mockups/bases` → `Sanitize & Sync`

- Effect: renames base PNG/JSON to the MU convention, rewrites the JSON `template` field to match the PNG filename, generates 500×500 JPG thumbs with a white background, and updates the catalog base entries to match disk.

## Modal & Delete UX

- Artworks pages use a custom delete modal (`#uploadDeleteModal`), Bootstrap-free. Confirmation requires typing `DELETE`, posts via fetch to `/artworks/unprocessed/<slug>/delete` or `/artworks/processed/<slug>/delete`, and never navigates.

- Accessibility: body scroll locks while open, focus is trapped/restored, and ESC/backdrop/close dismiss safely.

- Z-index strategy: backdrop 900, modal container 1000, dialog 1001; body lock via `overlay-lock`/`upload-modal-open`.

## Security Standards

- Passwords are hashed using PBKDF2 (`pbkdf2:sha256`) with **600,000 iterations**.

- **Password Complexity:** Minimum 12 characters, at least one uppercase, one lowercase, one number, and one special character (!@#$%^&\* etc).

- Session hardening includes secure cookie flags, targeted session reset on login (preserves CSRF token), and absolute/inactivity timeouts (12hr/30min).

- Role-Based Access Control (RBAC): UI and routes gate admin-only surfaces under the `admin` role. Database users with `role='admin'` get full admin access.

- CSRF: all mutating POST endpoints must enforce CSRF validation (`require_csrf_or_400`), and any HTML POST form must include a `csrf_token` hidden field. CSRF errors redirect to login with a friendly message.

- Cache-busting headers applied to auth pages (`no-store, no-cache, must-revalidate`).

- Open redirect prevention: any `next=` redirect parameter must be sanitized to an internal relative path (`auth_routes._safe_next_url`).

- Path traversal prevention: any route accepting a slug must validate it with strict syntax (`application/common/utilities/slug_sku.py`).

## User Management

- Admin route: `/admin/users` (admin-only)

- Supports creating users with roles: `admin`, `artist`, `viewer`

- Artists are restricted to viewing only their own artworks (filtered by `owner_id`)

- Admins can view all artworks

- Users cannot self-escalate their role

## Forgot Password

- Link available on login page (`/auth/forgot-password`)

- Generates secure token stored in `data/reset_tokens.json` (1-hour expiry)

- Reset URL logged to server console for manual delivery

- Reset password page enforces the same complexity rules

## Database Migration

- Run `python3 patch_db.py` to add missing columns (`email`, `role`, `created_at`) to the users table

- Safe to run multiple times (idempotent)

- Sets default role to 'artist' for existing users

## Strategic Positioning Update (2026)

### Dual-Market Positioning

ArtLomo now supports **two distinct market strategies** within the same system architecture:

1. **Marketplace Revenue Layer (Commercial Engine)**

- Target: High-volume Etsy sales ($15–$45 range)

- Strategy: Conversion-focused, benefit-driven copy

- Distribution: Automated Etsy marketplace export

- Output: Marketplace-optimized listing with SEO tags

- Preset: "OpenAI/Gemini - Commercial Engine v1"

1. **Collector Prestige Layer (Collector Engine)**

- Target: High-ticket collector sales ($200–$1,500+ range)

- Strategy: Curatorial-grade, heritage-first narrative

- Distribution: Manual gallery/collector/auction pathways

- Output: Curatorial listing with series/edition context

- Preset: "OpenAI/Gemini - Collector Engine v1"

### Preset-Driven Architecture

Rather than implementing separate code branches, ArtLomo uses **Analysis Presets** as strategy containers:

- **No schema changes:** Both engines output identical `listing.json` structure

- **No service branching:** Same `AnalysisPresetService` orchestrates all analysis

- **Provider agnostic:** OpenAI and Gemini remain interchangeable

- **Backwards compatible:** Existing workflows unaffected

- **Future-proof:** New market strategies are new presets, not code refactors

### Key Guarantees

✅ **Stability:** Dual engines operate via preset selection, not runtime logic changes
✅ **Backwards Compatibility:** All existing artworks and workflows continue functioning
✅ **Extensibility:** New market strategies require only preset creation, no code changes
✅ **Artist Control:** Artists choose engine and preset at analysis time
✅ **Immutability:** Once locked to a tier (Commercial or Collector), the tier cannot be changed

### How It Works

1. **Upload:** Artist uploads artwork

1. **Preset Selection:** Artist chooses Commercial or Collector preset before analysis

1. **AI Analysis:** Preset's system prompt, boilerplate, and provider shape the output

1. **Same Output Schema:** Both engines produce identical `listing.json` fields

1. **Tier Locking:** Work locked to its engine tier (Commercial → Etsy only; Collector → gallery only)

1. **Export:** Different export pathways based on tier

### Roadmap (Future Enhancement)

## Potential (Post-2026)

- Automated Tier Locking: prevent accidental Commercial → Collector reclassification

- Multi-Series Management: batch operations on series collections

- Preset Templates: starter templates for niche markets (luxury, sustainable, cultural)

- Analytics: market performance metrics per engine type

## Archive & Historical Reference (February 14, 2026)

As the codebase matures, implementation documentation and work-in-progress notes are archived to maintain clarity and reduce information clutter. All archived files remain accessible for historical reference, learning, and audit trails.

## Archived Categories

### Migration Scripts (`/archived/migration-scripts/`)

One-time data migration utilities—run once during past deployments and retained for historical reference:

- `patch_db.py` — Database schema migration (adds user table columns: email, role, created_at)

- `sync_assets.py` — Asset directory synchronization and metadata validation

- `test_gemini_key.py` — Gemini API key validation utility (moved for setup reference)

**When to use:** Only if re-running historical migrations or reviewing past upgrade procedures.

### Work Notes (`/archived/work-notes/`)

Previous development session notes and task documentation:

- `2026-02-14-cline-work-01.txt` — Cline session notes for layout refactoring (pre-Clean-Room)

**When to use:** Historical context on implementation approach and reasoning.

### Incident Reports (`/archived/incidents/`)

Past incidents and their resolutions—documented for learning and future prevention:

- `2026-02-05-INCIDENT_REPORT_502_FIX.md` — 502 Bad Gateway root cause (import errors in analysis preset routes) and remediation

**When to use:** Troubleshooting similar import/initialization issues.

### Implementation History (`/archived/implementation-history/`)

Detailed before/after/summary documentation for completed features—consolidated for reference:

- `2026-02-08-CSS_REFACTOR_SUMMARY.md` — CSS variable centralization (darkroom.css refactor)

- `ANALYSIS_PRESET_MANAGEMENT_BEFORE_AFTER.md` — Dark theme fix for preset management UI

- `ANALYSIS_PRESET_MANAGEMENT_ENHANCEMENTS.md` — Enhancement specifications

- `ANALYSIS_PRESETS_IMPLEMENTATION_SUMMARY.md` — Comprehensive feature breakdown

- `DETAIL_CLOSEUP_COORDINATE_FIX.md` — Coordinate system alignment fix

- `DETAIL_CLOSEUP_IMPLEMENTATION_SUMMARY.md` — Detail closeup feature overview

- `FEATURES_PRESET_UPLOAD_ADMIN_EXPORT.md` — Feature specification

- `IMPLEMENTATION_SUMMARY_UPLOAD_EXPORT.md` — Upload/export workflow summary

- `KINEMATIC_VIDEO_IMPLEMENTATION_SUMMARY.md` — Video generation feature overview

- `MANUAL_ANALYSIS_ALIGNMENT_SUMMARY.md` — Manual workspace alignment details

- `MANUAL_ANALYSIS_BEFORE_AFTER.md` — UI improvements for manual workspace

- `MANUAL_ANALYSIS_INTEGRATION_CHECKLIST.md` — Comprehensive integration verification

**Consolidated Entry (See MASTER_FILE_INDEX.md):** All implementation history is now tracked via single consolidated entries in [application/docs/MASTER_FILE_INDEX.md](application/docs/MASTER_FILE_INDEX.md) with references to archived detailed documentation.

**When to use:** Deep-dive into feature history, understanding past decisions, or reviewing checklists from integration work.

### Access & Navigation

All archived files are organized by date prefix (YYYY-MM-DD) for chronological sorting:

```text
archived/
  ├── migration-scripts/ → One-time database/asset utilities
  ├── work-notes/ → Development session notes
  ├── incidents/ → Past issues and resolutions
  └── implementation-history/ → Feature before/after/summary docs
```

Reference archived files from main documentation via cross-links:

- **Within README.md:** "See archived incident reports in `/archived/incidents/`"

- **Within MASTER_FILE_INDEX.md:** "Implementation details in `/archived/implementation-history/`"

- **Within ARCHITECTURE_INDEX.md:** "Historical context in `/archived/`"

---

## Wishlist

- AI-Driven Mockup Pairing

- Cloudflare Tunnel Integration

## MANDATORY RULES FOR ALL CONTRIBUTORS (INCLUDING AI)

- Before any task, you **must read**:

  - README.md (this file)

  - application/docs/ARCHITECTURE_INDEX.md

- application/docs/ARCHITECTURE_INDEX.md is the **single source of truth** for:

  - folder responsibilities

  - workflow boundaries

  - allowed imports

  - ownership rules

- ANY change that adds, removes, or moves a file; introduces a workflow; or changes responsibilities **must update** application/docs/ARCHITECTURE_INDEX.md in the same task.

- NO cross-workflow imports are allowed. Workflows may only depend on:

  - application/common

  - application/utils

  - shared configuration

- Business logic **must** live in services.

- Routes **must** orchestrate only.

- UI **must not** contain business logic.

- application/utils **must not** import workflow code.

- application/common **must not** become a dumping ground.

- Any violation of these rules is considered a defect.

## Codex Operating Contract

- Respect workflow isolation at all times.

- Keep files small and tightly scoped.

- Never introduce legacy paths or imports.

- Update architecture documentation whenever structure or responsibilities change.
