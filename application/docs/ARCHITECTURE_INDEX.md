# Architecture Index

This document is the authoritative architectural map for the ArtLomo production Flask system. It defines responsibilities, boundaries, allowed imports, and ownership rules. ANY structural or responsibility change MUST update this file. Failure to do so invalidates the change.

**Last Updated:** March 9, 2026 - Curated AI Handoff Stack and App-Stacks Refinement

## Recent Architectural Changes (March 9, 2026)

### Curated AI Handoff and Stack Profiling (v2.3)

- **Date:** March 9, 2026

- **Scope:** Refined app-stacks tooling to support compact, reusable AI handoff artifacts and reduce non-essential stack payload.

- **Key Improvements:**

  - Added `gemini` command to `application/tools/app-stacks/files/tools.sh` for one-file curated AI context generation.

  - Added profile-based behavior in `application/tools/app-stacks/files/code-stacker.sh`:

  - `full` profile for developer-oriented stack snapshots.

  - `gemini` profile for external AI handoff.

  - Excluded `.env` from stack output by default (opt-in via environment flag).

  - Fixed stack bloat by pruning nested dependency/cache directories (notably `node_modules`) at any depth.

- **Architectural Compliance:**

  - ✅ No changes to 4-layer runtime dependency flow.

  - ✅ Tooling remains in operational/support layer (`application/tools`) and does not alter workflow ownership.

  - ✅ Existing route/service/UI boundaries unchanged.

## Recent Architectural Changes (March 7, 2026)

### System Inventory Tooling Integration (v2.2)

- **Date:** March 7, 2026

- **Scope:** Added system-level environment capture into the documentation pipeline and synchronized architecture documentation set.

- **Key Improvements:**

  - **New inventory script:** `application/tools/app-stacks/files/system-inventory.sh` added to capture runtime, infrastructure, and service-state data.

  - **Orchestration update:** `application/tools/app-stacks/files/tools.sh` now supports `sysinfo` and includes it in `all` runs.

  - **Infrastructure visibility:** Generated reports now include OS, Python/Node runtime versions, hardware, network, database, and GCP metadata.

  - **Documentation synchronization:** March 7 report suite added under `application/docs/` to align stakeholder, technical, and VM-level views.

- **Files Added/Updated:**

  - `application/tools/app-stacks/files/system-inventory.sh` (new)

  - `application/tools/app-stacks/files/tools.sh` (sysinfo integration)

  - `application/docs/ARTLOMO_OVERVIEW_2026-03-07.md`

  - `application/docs/ARTLOMO_SYSTEM_SOFTWARE_REPORT_2026-03-07.md`

  - `application/docs/GOOGLE_CLOUD_VM_SPECS_REPORT_2026-03-07.md`

  - `application/docs/TOOLS_SH_COVERAGE_REPORT_2026-03-07.md`

- **Architectural Compliance:**

  - ✅ No layer boundary violations

  - ✅ Tooling remains operational/support layer and does not alter workflow ownership

  - ✅ Existing 4-layer dependency model unchanged

  - ✅ Documentation now reflects production environment state as of March 7, 2026

---

## Recent Architectural Changes (February 24, 2026)

### Director's Suite Video Rendering Enhancements (v2.0)

- **Date:** February 24, 2026

- **Scope:** Enhanced error reporting, video rendering pipeline improvements, CSS refactoring, and UI synchronization

- **Key Improvements:**

  - **Robust Error Reporting:** `postJson()` in video_cinematic.js now parses actual server errors instead of generic messages

  - **Master Artwork Inclusion:** `video_service.py` always prepends master artwork to video sequences

  - **Pan Direction Cycling:** New `buildPanExpressions()` in render.js applies per-mockup pan directions (Up→Down→Left→Right)

  - **Rendering Overlay:** Visual feedback (spinner, text) during video generation in video_suite.css

  - **Storyboard UI Sync:** `renderChosenList()` executes on page load to populate "Chosen Mockups" panel

  - **URL Data Attributes:** Fixed 404 errors by passing URLs via `data-*` attributes instead of Jinja templates in static JS

  - **CSS Consolidation:** analysis_workspace.html styles moved to dedicated stylesheet (analysis_workspace.css)

  - **Footer Theming:** Added dark/light mode support to footer links with proper color contrast

- **Files Modified:**

  - Layer 2 (Services): `video_service.py` (master artwork logic)

  - Layer 2 (Services): `artwork_routes.py` (error normalization)

  - Layer 3 (Routes): `video_routes.py` (URL data preparation)

  - Layer 4 (UI): `video_cinematic.js`, `render.js`, `video_workspace.html`, `video_suite.css`, `sidebar.css`, `analysis_workspace.css` (new), `analysis_workspace.html`

- **Architectural Compliance:**

  - ✅ No circular dependencies introduced

  - ✅ Layer boundaries maintained (1→2→3→4 dependency flow)

  - ✅ All CSS uses variables (zero hardcoded colors)

  - ✅ All error handling returns structured data

  - ✅ UI/template separation preserved (no business logic in JS)

- **Testing Status:** ✅ Verified manually with all 9 fixes working correctly

- **Documentation:** See [todays-work-24-FEB-2026.md](../../changelog-reports/todays-work-24-FEB-2026.md) for full implementation details

---

## Recent Architectural Changes (February 17, 2026)

### Comprehensive System Verification & Production Deployment (v2.1 Final)

- **Date:** February 17, 2026 (Final phase)

- **Scope:** Complete verification of Detail Closeup coordinate system, cache busting, and production readiness

- **Deliverables:**

  - Comprehensive 1,261-line handoff document with all system details

  - Mathematical audit (445 lines) proving all calculations correct

  - Cache busting verification with visual proof markers deployed

  - Complete testing procedures and troubleshooting guide

- **Key Verification Results:**

  - ✅ Frontend normalization uses `offsetWidth` (rendered size) - CORRECT

  - ✅ Focal point zoom preserves center pixel - CORRECT

  - ✅ Backend proportional mapping - CORRECT

  - ✅ Crop box clamping handles all edge cases - CORRECT

  - ✅ Scale constants Photoshop-calibrated - CORRECT

  - ✅ All services running cleanly - VERIFIED

- **Testing Status:** 15+ edge cases tested, all passed

- **Documentation:** 3 comprehensive guides created (1,261 + 445 + 400 lines)

- **Status:** ✅ **PRODUCTION READY - ZERO OUTSTANDING ISSUES**

## Previous Architectural Changes (February 17, 2026 - Earlier)

### Detail Closeup Coordinate Normalization (v2.1 - Initial Implementation)

- **Date:** February 17, 2026

- **Scope:** Refactor of `detail_closeup.js`, `detail_closeup_editor.html`, and `artwork_routes.py`

- **Template Source of Truth:** `application/artwork/ui/templates/detail_closeup_editor.html` (served by artwork blueprint, NOT analysis)

- **Change:** Shifted from "Pixel Offset" tracking to "Normalized Coordinate" (0.0 - 1.0) tracking.

- **Reasoning:**

  - Ensures crops are resolution-independent (works on 7200px proxy and 14400px master).

  - Aligns with `DEFINITION_OF_DONE.md` requirement for coordinate sync.

  - Fixes "Top-Left" default bug by defaulting to 0.5 (Center) instead of 0.0.

  - Single-source-of-truth coordinate system eliminates coordinate drift.

- **Key Files:**

  - `application/artwork/ui/templates/detail_closeup_editor.html` - Template with footer-positioned back button

  - `application/common/ui/static/js/detail_closeup.js` - Uses `offsetWidth` for rendered dimensions with v2.1 debug logging

  - `application/artwork/routes/artwork_routes.py` - Accepts `norm_x`/`norm_y` with 0.5 defaults and full error context

  - `application/common/ui/static/css/detail_closeup.css` - Updated button styling for visibility

- **Math Verification:** Normalized coordinate calculation uses `imageElement.offsetWidth` (rendered size) as denominator, never `naturalWidth` (prevents top-left crop bug)

- **Impact:** Detail Closeup crops now perfectly aligned across all zoom/pan states and image resolutions

- **Testing:** Verified with focal point zoom, edge cases, and coordinate handshake logging with "Coordinate Sync v2.1 Active" console marker

## Recent Architectural Changes (February 15, 2026)

### Comprehensive Workflow Documentation Suite

- **Date:** February 15, 2026

- **Scope:** 6 comprehensive workflow reports created covering all major workflows

- **Location:** `application/workflows/`

- **Coverage:** Upload (801 lines), Analysis (1,411 lines), Mockup (1,230 lines), Detail Closeup (1,333 lines), Export (1,015 lines), Video Generation (788 lines)

- **Total:** 6,578 lines of production-ready technical documentation

- **Format:** Each report includes: executive summary, architecture overview, stage breakdowns with code examples, structured logging patterns, error handling, performance characteristics, integration points, and data flow diagrams

- **Quality:** All reports validated with 0 markdown linting errors

- **Purpose:** Provide developers, AI assistants, and system architects with complete technical reference for each workflow

### Clean-Room Analysis Workspace Refactor (v2.0)

- **File (canonical):** `application/common/ui/templates/analysis_workspace.html`

- **Scope:** Complete UI/UX restructure for professional, distraction-free analysis workflow

- **Key Changes:**

  - **Unified Action Bar (Sticky):** Single row of 5 context-aware actions (Save Changes, Lock, Re-Analyse, Export, Delete)

  - **Linear Workflow:** Eliminates button clutter; user never wonders what to do next

  - **Media Panel Redesign:** Side-by-side Artwork + Detail Closeup (max 500px each), dedicated Video panel, mockup SWAP buttons

  - **Context-Aware Re-Analyse:** Button detects `analysis_source` and routes to same AI provider (no manual switching)

  - **Delete Modal Safety:** Requires user to type "DELETE" before confirmation button activates

  - **Dark Mode Compliant:** All text uses `var(--text-primary)` / `var(--text-secondary)`, zero white-on-white issues

  - **Glass Morphism:** Action bar features `backdrop-filter: blur(10px)` for modern aesthetic

  - **Backend:** Closeup proxy generation already implemented (7200px @ 90% quality in `detail_closeup_service.py`)

- **Impact:** 45/55 grid layout (45% stationary left, 55% scrolling right) reduces cognitive load, improves merchant workflow efficiency

- **Documentation:** See [CLEAN_ROOM_WORKSPACE_REFACTOR.md](../../CLEAN_ROOM_WORKSPACE_REFACTOR.md) for detailed breakdown

### Etsy Rules Reference + Workspace Validation Layer (February 18, 2026)

- **Route:** `GET /analysis/rules-reference`

- **Route file:** `application/analysis/routes.py`

- **Template:** `application/analysis/ui/templates/etsy_rules_reference.html`

- **Workspace integration:**

  - Canonical workspace (`application/common/ui/templates/analysis_workspace.html`) adds per-field Etsy Rules links and mandatory badges.

  - Frontend validation script (`application/common/ui/static/js/analysis_validation.js`) provides live title/tags counters and Etsy compliance warning tooltip on Save.

- **Responsibility split:**

  - `analysis/routes.py` owns serving documentation reference pages.

  - Canonical shared workspace template owns UI wiring for cross-workflow review pages.

### 1. Enhanced Error Handling in Gemini Analysis Service

- **File:** `application/analysis/gemini/service.py`

- **Change:** `GeminiAnalysisError` exception class now carries `error_code` and `error_detail` attributes

- **Pattern:** All error raises now include error classification:

  - `ERR_AUTH` - Authentication failures (missing API key, client not available)

  - `ERR_BAD_REQUEST` - Validation failures (missing directories, missing images)

  - `ERR_UNKNOWN` - Unknown errors (fallback default)

- **Impact:** Enables proper error categorization in API response handlers without losing exception context

- **Usage:** `raise GeminiAnalysisError("message", error_code="ERR_AUTH", error_detail=str(exc))`

### 2. Video Generation Service (New)

- **File:** `application/tools/video/service.py`

- **Purpose:** Generates mp4 video previews from artwork master/analyse images.

- **Pattern:** Service-based generation; encapsulated FFMPEG/OpenCV logic.

- **Usage:** `VideoService().generate_video(slug)`

### 3. Master File Standardization & SEO Renaming

- **File:** `application/upload/services/storage_service.py` & `application/artwork/routes/artwork_routes.py`

- **Change:** Enforced `-MASTER.jpg` suffix for all master files.

- **Lock Logic:** When artwork is locked (`POST /<slug>/lock`), the master file (`[slug]-MASTER.jpg` or legacy `[slug].jpg`) is renamed to the generated `seo_filename` (e.g., `sku-seo-slug.jpg`).

- **Detail Closeup:** `DetailCloseupService` supports finding master files via search order: `[slug]-MASTER.jpg` -> `seo_filename` -> `[slug].jpg`.

### 4. Physical Folder Deletion in Upload Routes

- **File:** `application/upload/routes/upload_routes.py`

- **Routes:** `delete_unprocessed()` and `delete_processed()`

- **Change:** Added `shutil.rmtree()` calls before database soft-delete to ensure physical folder removal

- **Pattern:** Physical deletion → database state update → security logging → status return

- **Impact:** Resolves orphaned artwork folders (62 total resolved by this change)

### 3. CSS Animation Support for Processing Indicators

- **File:** `application/common/ui/static/css/analysis-loading.css`

- **Change:** Added `.spinning` class for backward compatibility with existing JavaScript

- **Pattern:** `.analysis-spinner.spinning` applies `animation: spin 2s linear infinite;`

- **Impact:** All processing overlays now support animated indicators across all workflows

---

## 1. Architecture Overview

- Modular monolith built on Flask, organized by workflow folders under `application/`.

- Workflows are isolated; they communicate only through shared layers (`application/common`, `application/utils`, and configuration).

- Shared layers:

  - `application/common` for shared UI, shared utilities that are domain-friendly.

  - `application/utils` for low-level, cross-cutting helpers with no domain coupling.

- Entrypoint:

  - `application/app.py` initializes the Flask app, registers blueprints, wires configuration.

  - `application/config.py` holds configuration defaults and environment loading.

- Runtime protection: `application/_legacy_guard.py` enforces cleanliness and blocks legacy/unsafe paths.

### Mandatory Reading: Image Processing Standards

**All developers must review `application/docs/rules-&-parameters.md` before modifying image generation, carousel, or derivative processing logic.**

This document defines:

- ANALYSE (2048px), THUMB (500x500px), MOCKUP (2000px), and DETAIL CLOSEUP (2000px) size standards

- Carousel modal asset source logic (artwork vs detail vs mockup differentiation)

- CSS responsive image sizing constraints

- Template integration requirements for carousel functionality

Failure to follow these standards will result in image scaling regressions and broken carousel behavior.

## 1A. Fixed Sidebar Layout (UI Shell)

- The global UI shell is defined in `application/common/ui/templates/base.html`.

- Layout strategy:

  - `.app-sidebar` is fixed and scrolls independently (`height: 100vh` + `overflow-y: auto`).

  - `.app-content` is the main pane and scrolls independently (`height: 100vh` + `overflow-y: auto`).

  - The shell uses `overflow: hidden` to prevent double-scroll and ensure the two panes are the only scroll containers.

- Sidebar collapse:

  - A toggle button collapses the sidebar to icons-only width.

  - State is persisted in `localStorage` via `application/common/ui/static/js/sidebar.js`.

## 2. Workflow Inventory

- **admin**

  - Purpose: administrative surfaces (hub) and oversight flows.

  - Owns: admin routes, admin UI, admin-specific services.

  - Must NOT own: shared utilities, other workflow business logic.

  - Theme/style ownership:

  - Owns the Darkroom Style Editor UI and theme preset services.

  - Presets are JSON under `application/var/themes/` and compile to modular CSS under `application/common/ui/static/css/presets/`.

  - Profile identity management:

  - Admin Profile Editor → `admin_profile.profile_page` (`/admin/profile`)

  - Storage: `application/var/profile.json`

  - Purpose: provide artist identity + story used by Heritage-First prompts at runtime.

  - Profile image uploads:

  - Uploaded assets are stored under `application/common/ui/static/uploads/profiles/` and referenced via web path `/static/uploads/profiles/<filename>` in `profile.json`.

- **upload**

  - Purpose: ingest assets, run QC, store originals/derivatives, generate thumbnails.

  - Owns: upload routes, upload services (QC/storage/thumb), upload UI assets.

  - Must NOT own: mockups/artwork business logic, cross-workflow orchestration.

  - UI safety: upload gallery delete is guarded by a modal confirmation (client-side only); backend delete semantics remain unchanged.

  - QC output contract (`lab/*/<slug>/qc.json`):

  - Existing core fields: `dimensions`, `dpi`, `filesize_mb`, `aspect_ratio`, `color`, `blur_score`, `compression_quality_est`, `qc_status`.

  - Museum-grade extensions:

  - `palette.dominant_hex`: list of dominant colors as hex strings.

  - `palette.primary` / `palette.secondary`: Etsy-friendly color names derived from the palette.

  - `luminance.category`: one of `Bright/Airy`, `Balanced`, `Dark/Moody`.

  - `edge_safety`: heuristic edge/subject safety metrics for print margins (includes `too_close` and `signature_zone_activity`).

- **artwork**

  - Purpose: artwork-domain flows (records, errors, services, UI for artwork operations).

  - Owns: artwork routes, services, UI templates/static, artwork errors.

  - Must NOT own: upload/mockups logic, global utilities.

- **mockups**

  - Purpose: mockup generation, catalog/selection pipeline, admin mockup tasks.

  - Owns: mockup routes (admin/manual), catalog readers/models/services, selection planners/policies, pipeline/storage/validation, compositor/transforms, mockup-specific UI.

  - Must NOT own: upload/artwork logic, unrelated admin responsibilities.

- **manual**

  - Purpose: manual analysis workflow for uploaded artwork initiated from the upload gallery.

  - Owns: manual routes, services, errors, workspace UI/static assets.

  - Must NOT own: upload/mockups/admin/artwork business logic or shared utilities.

  - Storage: manual assets live in `lab/processed/<slug>/` (no `processed/manual` subfolder); promotions move the entire folder from `lab/unprocessed/<slug>/` → `lab/processed/<slug>/` and never duplicate data.

  - Asset routing: `/manual/asset/<slug>/<filename>` serves manual assets (thumb/analyse and allowed mockup files) from the processed root; UI must use `url_for('manual.asset', ...)` and must not construct paths manually.

  - Asset roles: MASTER is never displayed in manual UI; THUMB is used for preview; ANALYSE is used for modal/carousel; manual workflow does not scan directories and resolves assets deterministically.

  - UI reuse: manual workspace reuses the shared gallery modal/carousel behavior (no duplicated JS); only thumb feeds preview, analyse feeds modal; mockups may append after analyse.

- **export**

  - Purpose: export processed artwork assets + listing/metadata into deterministic bundles for deployment/hand-off.

  - Owns: export services and export API routes.

  - Must NOT own: upload/artwork/mockups business logic.

  - Storage: exports are written under `outputs/exports/<sku>/<export_id>/`.

- **lab** (data-centric)

  - Purpose: sandboxed data for experimentation/reference (locked/processed/unprocessed/index datasets).

  - Owns: data samples only.

  - Must NOT own: application code or runtime logic.

- **tools**

  - Purpose: operational helpers and stack utilities (e.g., app-stacks/backups/files/stacks).

  - Owns: tooling scripts under workflow boundary.

  - Must NOT own: runtime business logic or web routes.

- **backups** (placeholder)

  - Purpose: reserved for backup workflow.

  - Owns: none yet.

  - Must NOT own: active business logic until defined.

- **routes** (auth – infrastructure workflow)

  - Purpose: auth endpoints and related infrastructure routes.

  - Owns: `routes/auth_routes.py` and supporting auth glue.

  - Must NOT own: domain business logic or UI.

- **site**

  - Purpose: public/legal informational pages and sitemap scaffolding.

  - Owns: `application/site/` blueprint and placeholder templates under `application/common/ui/templates/site/`.

  - Must NOT own: workflow business logic; templates are content-only.

## 3. Shared Layers

- **application/common**

  - Role: shared UI fragments/static assets and domain-friendly shared helpers.

  - Subfolders:

  - `application/common/ui`: shared templates/static assets (CSS/JS), layout fragments.

  - `application/common/utilities`: shared domain-level helpers (files, images, paths, indexing, slug/sku helpers).

- **application/utils**

  - Role: low-level, cross-cutting utilities (logging, security, image processing helpers, auth decorators, env handling, template helpers, AI service helpers, etc.).

- Dependency direction:

  - workflows → application/common → application/utils.

  - workflows → application/utils.

  - application/utils MUST NOT import workflows or `application/common` domain logic.

  - application/common SHOULD NOT import workflows; it may use application/utils.

## 4. Detailed Folder & File Index

- **application/app.py**

  - Type: infrastructure / entrypoint.

  - Responsibility: create Flask app, register blueprints, wire configs/extensions.

  - Allowed imports: workflows, application/common, application/utils, config.

  - Forbidden imports: none beyond avoiding legacy paths; must not hide business logic.

- **application/config.py**

  - Type: infrastructure / configuration.

  - Responsibility: configuration defaults and environment binding.

  - Allowed imports: stdlib, safe helpers from application/utils.

  - Forbidden imports: workflow business logic.

- **application/\_legacy_guard.py**

  - Type: infrastructure / runtime protection.

  - Responsibility: enforce cleanliness and block legacy/unsafe access.

  - Allowed imports: minimal standard/config utilities.

  - Forbidden imports: workflow business logic.

- **application/admin/**

  - Type: workflow.

  - Responsibility: admin routes/UI/services.

  - Allowed imports: application/common, application/utils, config.

  - Forbidden imports: other workflows' business logic.

- **application/artwork/**

  - Type: workflow.

  - Responsibility: artwork domain routes/services/UI and errors.

  - Allowed imports: application/common, application/utils, config.

  - Forbidden imports: upload/mockups/admin business logic.

- **application/manual/**

  - Type: workflow.

  - Responsibility: manual analysis routes, services, errors, workspace UI/static.

  - Allowed imports: application/common, application/utils, config.

  - Forbidden imports: upload/mockups/admin/artwork business logic.

  - UI responsibilities: manual workflow assets live in `application/analysis/manual/ui` and shared workspace assets live in `application/common/ui`; they are UI-only with no side effects.

  - Asset responsibilities: manual assets are served via the manual asset route; templates/js must not concatenate paths.

  - Asset resolution: services expose deterministic thumb/analyse resolution; MASTER is excluded from serving; invalid kinds return 404.

- **application/analysis/**

  - Type: workflow.

  - Responsibility: AI-driven analysis integration (Gemini/OpenAI) and Etsy listing generation (Pioneer v2.0 / Merchant Mode) via prompts, schema, and API services.

  - Allowed imports: application/common, application/utils, config.

  - Forbidden imports: upload/mockups/admin/artwork/manual business logic (integrates via services only).

  - Museum-quality standard: 14,400px long edge (48 inches / 121.9 cm @ 300 DPI) is the primary technical competitive advantage and must be surfaced early in descriptions.

  - Instructions source of truth:

  - `application/analysis/instructions/MASTER_ETSY_DESCRIPTION_ENGINE.md` defines the Merchant Mode / Pioneer v2.0 listing rules.

  - `application/analysis/instructions/MASTER-ARTWORK-ANALYSIS-LISTING-DESCRIPTION-EXAMPLE.md` provides the few-shot Pioneer Standard target example.

  - Output Contract (base schema):

  - `etsy_title`: string, max 140 characters.

  - `etsy_description`: string, formatted with line breaks.

  - `etsy_tags`: list of exactly 13 strings.

  - `visual_analysis`: object with 4 required fields: `subject`, `dot_rhythm`, `palette`, `mood`.

  - `seo_filename_slug`: max 61 characters.

  - `materials`: list of exactly 13 strings.

  - `primary_colour`: dominant colour name.

  - `secondary_colour`: secondary colour name.

  - Visual Analysis ensures manual workspace and downstream UIs can render subject cards, mood filters, and palette previews without re-analysis.

  - Service owns: schema validation (Pydantic), API integration (Gemini/OpenAI calls), response mapping to listing.json metadata, preservation of visual_analysis for manual workspace consumption.

  - Gemini structured output note:

  - Gemini requests use `responseMimeType="application/json"` and rely on internal Pydantic validation.

  - Do NOT send `responseSchema` in the Gemini SDK request config (Gemini rejects schemas that include `additional_properties`).

  - Gemini diagnostic logging:

  - Destination: `/srv/artlomo/logs/ai_processing.log` (logger: `ai_processing`).

  - On API failures, the service emits a diagnostic block between markers:

  - `--- GEMINI DIAGNOSTIC START ---`

  - `--- GEMINI DIAGNOSTIC END ---`

  - The block includes error type/details and a best-effort classification (auth vs quota vs payload vs network).

- **application/upload/**

  - Type: workflow.

  - Responsibility: upload routes, services (QC/storage/thumb), UI templates/static, config/docs.

  - Allowed imports: application/common, application/utils, config.

  - Forbidden imports: artwork/mockups/admin business logic.

- **application/mockups/**

  - Type: workflow.

  - Responsibility: mockup admin routes, catalog/selection models and services, pipeline/storage/validation, compositor/transforms, errors, loader, UI/static/templates.

  - Allowed imports: application/common, application/utils, config.

  - Forbidden imports: upload/artwork/admin business logic.

- **application/export/**

  - Type: workflow.

  - Responsibility: create export bundles + zip archives from processed artwork folders.

  - Allowed imports: application/common, application/utils, config.

  - Forbidden imports: workflow business logic from others.

- **application/lab/**

  - Type: data.

  - Responsibility: datasets for experimentation/reference; no runtime code.

  - Allowed imports: n/a (data only).

  - Forbidden imports: n/a (must not add runtime code here).

- **application/common/**

  - Type: shared.

  - Responsibility: shared UI and domain-friendly utilities.

  - Allowed imports: application/utils, config.

  - Forbidden imports: workflow business logic.

- **application/utils/**

  - Type: shared low-level utilities.

  - Responsibility: cross-cutting helpers (AI, auth, security, logging, image processing, templates, etc.).

  - Allowed imports: stdlib, third-party libs, other utils (acyclic), config.

  - Forbidden imports: workflows, application/common domain logic.

- **application/routes/**

  - Type: infrastructure workflow (auth).

  - Responsibility: auth routes only.

  - Allowed imports: application/common, application/utils, config.

  - Forbidden imports: workflow business logic from others.

- **application/tools/**

  - Type: workflow (operational tooling).

  - Responsibility: tooling/stacks helpers; not runtime business logic.

  - Allowed imports: application/utils, config.

  - Forbidden imports: workflow business logic.

- **/srv/artlomo/logs/**

  - Type: data/log artifacts.

  - Responsibility: log outputs.

  - Allowed imports: n/a (data only).

  - Forbidden imports: code placement.

- **application/var/**

  - Type: data/state.

  - Responsibility: runtime data (coordinates, sku sequence, themes, etc.).

  - Allowed imports: n/a (data only); code should read via services/utils.

  - Forbidden imports: code placement.

## 5. Ownership & Boundary Rules

- Each workflow owns its routes, services, UI, and domain-specific models within its folder.

- Manual workflow owns manual analysis entrypoints, services, errors, and workspace UI; it must not mutate other workflows directly and integrates via services/configured queues only.

- Business logic resides in services within the owning workflow; routes only orchestrate.

- Shared UI belongs in `application/common/ui`; workflow-specific UI stays within the workflow.

- Shared domain helpers belong in `application/common/utilities`; low-level helpers belong in `application/utils`.

- `application/utils` must stay free of workflow or domain coupling.

- State mutation and irreversible actions must occur inside workflow services or clearly named operational tooling (under tools), never in routes or UI.

## 6. Integration & Extension Rules

- Adding a new workflow: create a top-level folder under `application/`, define routes/services/UI internally, register blueprint in `application/app.py`, and document boundaries here before or with the change.

- UI integration: workflows may consume shared templates/assets from `application/common/ui`; they must not place business logic in UI.

- Shared utilities evolution: prefer adding to `application/utils` when logic is low-level and workflow-agnostic; use `application/common/utilities` for shared domain-level helpers; avoid creating generic dumping grounds.

- Codex (and all automation) must respect workflow isolation, keep files small/scoped, avoid legacy paths, and update this document whenever structure or responsibilities change.

## 6A. Security Logging & Audit Trail

- `application/utils/logger_utils.py` provides `log_security_event(user_id, action, details)` for security/audit logging.

- Audit log destination is `/srv/artlomo/logs/security.log` (rotating handler). Sensitive actions (role changes, destructive deletes) must log an entry.

## 6B. SessionTracker & Session Rotation

- Auth is session-based. On successful login, user-specific session keys are cleared (targeted reset) while preserving the CSRF token.

- Admin sessions are tracked by `application/utils/session_tracker.py` (max concurrent sessions).

- Login registers a new `session_id` via SessionTracker; logout removes that tracker entry and performs full `session.clear()`.

- Timeouts are enforced globally: 12h absolute session lifetime and 30m inactivity.

- Database users with `role='admin'` receive full admin access (`is_admin=True`).

## 6C. Password Security & User Management

- Passwords are validated against complexity rules: minimum 12 characters, at least one uppercase, one lowercase, one number, and one special character.

- Password hashing uses PBKDF2 with SHA256 and 600,000 iterations.

- User management routes (`/admin/users`) are admin-only and support creating users with roles (admin/artist/viewer).

- Forgot password flow generates tokens stored in `data/reset_tokens.json` with 1-hour expiry; reset URLs are logged to console.

## 6D. CSRF & Cache Control

- CSRF tokens are preserved during login (targeted session reset removes only user keys, not CSRF).

- CSRF validation errors redirect to login with a friendly flash message.

- Cache-busting headers (`no-store, no-cache, must-revalidate`) are applied to auth pages (`/auth/login`, `/admin/users`, `/logout`).

## 7. Maintenance Rule (Critical)

ANY structural or responsibility change MUST update this file. Failure to do so invalidates the change.

## 7A. Test Suite Policy

- Legacy tests under `tests/legacy/` have been removed after core test verification.

- All active automated tests must live under `tests/`.

## 8. Storage & Processing Lifecycle (Lab)

- Canonical layout: `lab/unprocessed/<slug>/`, `lab/processed/<slug>/`, `lab/locked/<slug>/`. A slug may only exist in one tier at a time.

- Promotions are atomic moves (never copies/symlinks) to avoid duplicate folders and broken URLs; legacy `lab/processed/manual/` is retired and migrated into `lab/processed/<slug>/`.

- **Database Status Synchronization (Critical):** When an artwork is promoted from unprocessed to processed via ANY analysis entrypoint (Manual, OpenAI, or Gemini), the artwork's status in the SQLite database MUST be updated from `"unprocessed"` to `"processed"`. This ensures database consistency with the filesystem and prevents artwork from appearing on `/artworks/unprocessed` after analysis is initiated.

  - Manual analysis: `promote_unanalysed_to_manual()` in `application/analysis/manual/services/manual_service.py` calls `update_artwork_status(sku, "processed")`.

  - OpenAI/Gemini analysis: `ProcessingService.process()` in `application/artwork/services/processing_service.py` calls `update_artwork_status(sku, "processed")`.

- Manual analysis runs in-place on `lab/processed/<slug>/` and sets `analysis_source=manual`; analysis flows (OpenAI/Gemini/manual) may update metadata/assets but must not duplicate or relocate artwork folders.

- Any analysis entrypoint (OpenAI, Gemini, Manual) promotes the slug from `lab/unprocessed/<slug>/` → `lab/processed/<slug>/` before rendering; the source folder is removed so only the processed copy remains.

- Asset serving resolves from the processed root only; master/print images remain excluded from manual UI.

## 8A. Metadata & Analysis Pipeline

- Analysis is run via the Analysis workflow (`application/analysis`) and produces structured listing metadata for merchant export.

- Outputs are written into `lab/processed/<slug>/`:

  - `listing.json` (authoritative, editable)

  - `metadata_openai.json` / `metadata_gemini.json` (provider snapshots)

- Merchant Mode instructions live in:

  - `application/analysis/instructions/MASTER_ETSY_DESCRIPTION_ENGINE.md`

  - `application/analysis/instructions/MASTER-ARTWORK-ANALYSIS-LISTING-DESCRIPTION-EXAMPLE.md`

### Analysis Loading UX & Polling Infrastructure

- Purpose: Provide unified, visual feedback to users during asynchronous AI analysis processing with dark overlay, animated spinner, and automatic redirect on completion.

- Entry Points:

  1. **Custom Input Form** (`/upload/<slug>/custom-input`): Form submission intercepted; shows loading overlay while analysis processes.

  1. **Unprocessed Gallery** (`/artworks/unprocessed`): OpenAI/Gemini buttons trigger provider-aware analysis with overlay.

  1. **Review Pages** (`/artwork/<slug>/review/<provider>`): Infrastructure available for future re-analysis triggers.

  1. **Manual Workspace** (`/analysis/manual/workspace/<slug>`): Infrastructure available for complementary manual analysis flows.

- Infrastructure:

  - **Module:** `application/common/ui/static/js/analysis-loading.js` (221 lines)

  - `AnalysisLoader.show(provider)`: Creates and displays dark overlay with spinning arrows icon (arrows-clockwise-dark.svg), loading text "{Provider} Analysis in Progress", and animated pulsing dots.

  - `AnalysisLoader.poll(slug, provider, maxWaitMs)`: Polls `/api/analysis/status/<slug>` endpoint every 1 second, checking `done` field. Returns promise that resolves on completion or rejects after max wait time (default 5 minutes).

  - `AnalysisLoader.showAndWait(slug, provider)`: Combines show/poll/hide into single operation; returns promise.

  - `AnalysisLoader.hide()`: Removes overlay and stops polling.

  - **Stylesheet:** `application/common/ui/static/css/analysis-loading.css` (77 lines)

  - `.analysis-loading-overlay`: Fixed positioning (z-index 9999), dark background (`rgba(0,0,0,0.85)`), backdrop blur (4px), prevents body scroll.

  - `.analysis-spinner`: SVG icon rotation animation (2-second cycle).

  - `.analysis-loading-dots`: Three pulsing dots with staggered timing for visual rhythm.

  - Theme-aware styling for dark and light color modes.

- Provider-Aware Routing:

  - Form/button handlers detect provider (openai vs gemini) from submission context or onclick parameter.

  - Polling includes provider in status check: `/api/analysis/status/<slug>?provider={provider}` (when provider-specific status is needed).

  - Redirect is constructed dynamically: `window.location.href = /artwork/${slug}/review/${provider}` to ensure OpenAI analysis routes to `/review/openai` and Gemini to `/review/gemini`.

- Status Endpoint Contract:

  - **Path:** `/api/analysis/status/<slug>` (located in `application/analysis/api/routes.py` line 235).

  - **Response:** JSON object with fields `{status, sku, slug, stage, message, done, error, source, updated_at}`.

  - **Polling Logic:** Check `done === true` to detect completion; if `error` field is present, show alert with error message.

  - **Timeout Safety:** 5-minute maximum wait (300000ms) before fallback redirect; prevents indefinite loading screens if backend process fails silently.

- Form Interception Pattern (custom_input.html):

  1. Form submit event intercepted by JavaScript.

  1. Check button's `data-action` attribute: `save_only` allows normal submission; `analyze_openai` / `analyze_gemini` triggers async flow.

  1. Prevent default form submission.

  1. Show loading overlay with provider name.

  1. POST form data to `/unprocessed/<slug>/seed-context` endpoint (located in `application/upload/routes/upload_routes.py` line 514).

  1. Poll `/api/analysis/status/<slug>` until completion.

  1. Redirect to `/artwork/<slug>/review/<provider>`.

- Onclick Handler Pattern (unprocessed.html):

  1. Button/link click intercepted by `handleAnalysisClick(event, provider, slug)` function.

  1. Prevent default navigation.

  1. Show loading overlay with provider name.

  1. Poll `/api/analysis/status/<slug>` until completion.

  1. Redirect to `/artwork/<slug>/review/<provider>`.

### Etsy Listing Engine (Pioneer v2.0)

- The system operates in **Merchant Mode** for Etsy listings.

- The **14,400px long edge @ 300 DPI (up to 48 inches / 121.9 cm)** standard is the primary technical competitive advantage and must be surfaced early in descriptions.

#### 21-Field Data Contract (Standard Output)

The Pioneer v2.0 listing engine standardises a 21-field contract for merchant operations and consistent export.

1. Title

1. Description

1. Primary Colour

1. Secondary Colour

1. Price

1. SEO Filename

1. Quantity

1. Category

1. Mockup Category

1. Hero Image

1. Thumbnail Image

1. Analyse Image

1. Mockups

1. Visual Subject

1. Visual Dot Rhythm

1. Visual Palette

1. Visual Mood

1. SEO Tags

1. SEO Filename Slug

1. Limited Edition Count

1. Materials

#### Field Matching Logic (Enforced)

- **Field 6 (SEO Filename):** enforce 70-character limit and the `SKU-Title-Location` format.

- **Field 18 (SEO Tags):** enforce exactly 13 tags and 20 characters per tag.

- **Field 21 (Materials):** standardise the high-fidelity string:

  - `Digital Oil, 14400px Resolution, 300 DPI, High Res JPG, Virtual Acrylic, Digital Dotwork, Museum Quality File`

### AI Response Sanitization Layer

- Located in `application/utils/ai_utils.py`

- Provides cross-model compatibility for OpenAI and Gemini response parsing

- Key functions:

  - `clean_json_response(text)`: Strips markdown code blocks (`\`\`\`json ... \`\`\``), BOM characters, and extraneous formatting

  - `safe_parse_json(text)`: Calls cleaner, attempts `json.loads()`, returns `None` on failure (prevents crashes)

- All AI analysis services must use `safe_parse_json` instead of direct `json.loads()` on model responses

- Errors are logged with context (line/column for JSON decode errors) but do not crash the system

### The Pioneer Engine (Listing Generation)

- Located in `application/utils/house_prompts.py`

- Version: Pioneer Engine v1.0

- Role: "Senior Art Curator & Etsy Specialist for Robin Custance"

#### 13-Paragraph SEO Structure

The Pioneer Engine enforces a strict 13-paragraph description format for maximum Etsy SEO indexing:

1. 🎨 About the Artist – Robin Custance

1. ✨ Did You Know? Aboriginal Art & the Spirit of Dot Painting

1. 🖼 4:5 (Vertical)

1. 📐 Printing Tips

1. 🏪 Top 10 Print-On-Demand Services (optional)

1. ⚠️ Important Notes

1. 📏 Museum-Quality Technical Specs (MUST cite 14,400px and 300 DPI)

1. ❓ Frequently Asked Questions

1. 🚀 Explore My Work

1. 💫 Why You'll Love This Artwork

1. 🛒 How To Buy & Print

1. 🙌 Thank You

1. ❤️ People of the Reeds Acknowledgement

#### Pioneer Execution Rules

- **Paragraph Separator:** Use `---` as the ONLY separator between paragraphs (no blank lines)

- **Character Density:** Every paragraph MUST be at least 250 characters for SEO indexing

- **Technical Authority:** Block 7 MUST cite "14,400px" and "300 DPI" as the museum-quality standard

- **Heritage Guard:** Artist bio section MUST mention "People of the Reeds" (Boandik/Bindjali)

- **No Quotes:** Never wrap field values in quotation marks

- **No AI Meta:** Never include "As an AI" or external artist names (Monet, Picasso, etc.)

#### Cultural Guardrails

- Respectful of Aboriginal culture; never claim sacred/secret knowledge

- Do not invent Dreaming details; only state heritage/Country provided by the user

- Links: only Etsy URLs allowed; no email, phone, QR codes, or third-party links

### Listing Template Standardization (LISTING_BOILERPLATE)

- Located in `application/utils/house_prompts.py`

- Provides a centralized, standardized boilerplate that is appended to all AI-generated descriptions

- Ensures identical output structure from both OpenAI and Gemini providers

#### Boilerplate Sections (Appended Automatically)

1. **🏆 LIMITED EDITION** — 25-copy worldwide limit notice

1. **📏 TECHNICAL SPECIFICATIONS** — 14,400px @ 300 DPI, 11520×14400 pixels, sRGB

1. **🖨️ PRINTING NOTES** — Professional print lab guidance

1. **🎨 ABOUT THE ARTIST** — Robin Custance bio with Boandik/Bindjali heritage

1. **❤️ ACKNOWLEDGEMENT OF COUNTRY** — Bindjali/Boandik acknowledgement

1. **📐 PRINT SIZE GUIDE** — 5 standard sizes from desk to gallery-grade

1. **🛒 HOW TO PRINT** — 5-step purchase and printing workflow

#### Description Structure Rule

All AI analysis outputs MUST follow:

```text
[Generated Impressionistic Description]
---
[LISTING_BOILERPLATE]
```

### Theme-Aware Admin Hub (Elevated Glass Header)

- Control panel CSS in `application/common/ui/static/css/admin.css`

- **Elevated Glass Effect**: `position: sticky; top: 0; z-index: 100;` — content scrolls beneath header

- **Dark Mode**: `background: rgba(15, 15, 15, 0.85); backdrop-filter: blur(12px);` with subtle white border

- **Light Mode**: `background: rgba(255, 255, 255, 0.95);` with dark border accent

- Theme transitions: 0.2s ease for seamless toggle experience

- CSS selectors: `.hub-controls`, `.admin-hub-header`, `.artlomo-control-panel`

#### Human-in-the-Loop Metadata Injection

The Lab Hub implements a "Human-in-the-Loop" pattern where artist-provided context (Location, Sentiment, Original Prompt) is injected into the AI system prompt **before** visual analysis begins. This ensures:

1. Factual accuracy for geographic and cultural references

1. Consistent emotional tone driven by artist intent

1. Stylistic intelligence without exposing raw generation prompts

### High-Detail Artist-Guided Analysis

#### Image Resolution Standard

- **ANALYSE image**: 2048px at long edge (standardized for AI vision models)

- **THUMB image**: 500px at long edge (gallery previews)

- Configuration: `config.py` → `ANALYSE_LONG_EDGE`, `THUMB_SIZE`

### Visual Analysis Panel (Editable)

- **Subject**, **Dot Rhythm**, **Palette**, **Mood** fields are rendered as editable `<textarea>` elements in the shared analysis workspace template (`application/common/ui/templates/analysis_workspace.html`) for AI and Manual review flows.

- Fields are populated from `listing.json → visual_analysis` (AI-generated or manually entered).

- Save endpoints (`/artwork/<slug>/save` and manual `workspace_post`) perform an **atomic merge** — only overwrite keys that are present in the current save, preserving existing values for keys not included.

- Form field names: `va_subject`, `va_dot_rhythm`, `va_palette`, `va_mood`.

### Guided Creative Engine (Sentiment-Driven Analysis)

The "Custom Input" workflow implements a **Guided Creative Engine** that prioritizes artist-provided sentiment over pure visual inference, enabling the AI to interpret artwork through emotional and contextual anchors.

#### The Extrapolation Engine

When an artist provides even a single evocative word (e.g., "Ethereal", "Ghostly", "Luminous"), the AI:

- Treats it as the **PRIMARY CREATIVE ANCHOR**

- Extrapolates that sentiment into vocabulary, rhythm, and emotional texture

- Does not repeat the sentiment word; uses it to choose the vocabulary and cadence of the prose

- **EMBODIES** it throughout the description

#### Empty Field Handling (Robustness)

The `build_seed_context()` function handles missing fields gracefully:

- **Location empty**: Field omitted entirely; AI does not mention location

- **Sentiment empty**: AI instructed to use its own emotional interpretation based on visual observation

- **Original Prompt empty**: AI proceeds with visual-only stylistic analysis

#### Context Injection Hierarchy

1. **Location / Country** — Factual setting woven naturally into narrative (optional)

1. **General Info / Sentiment** — Primary creative anchor for tone extrapolation (optional)

1. **Original Prompt** — Internal stylistic intelligence for texture, brushwork, medium (optional, private)

#### Data Flow: seed_context.json Bridge

1. Artist clicks "Custom Input" on unprocessed artwork card

1. Form collects: Location/Country, General Info/Sentiment, Original Generation Prompt

1. Data saved to `seed_context.json` in `lab/unprocessed/<slug>/`

1. On analysis trigger (OpenAI or Gemini button):

- Artwork folder is **atomically moved** from `unprocessed/` → `processed/`

- `seed_context.json` travels with the folder

1. Analysis service loads seed context from `processed/` directory

1. `build_seed_context()` dynamically builds prompt injection based on provided fields

1. AI extrapolates sentiment into full narrative; original prompt remains internal

#### Files Involved

- **Storage**: `application/upload/services/storage_service.py` — `store_seed_context()`, `load_seed_context()`

- **Prompts**: `application/utils/house_prompts.py` — `build_seed_context()`

- **Analysis**: `application/analysis/prompts.py` — `get_system_prompt(seed_info)`, `get_gemini_system_prompt(seed_info)`

- **Routes**: `application/upload/routes/upload_routes.py` — `/unprocessed/<slug>/custom-input`, `/unprocessed/<slug>/seed-context`

- **Template**: `application/common/ui/templates/artworks/custom_input.html`

#### Privacy Rule (Critical)

The "Original Generation Prompt" is **internal stylistic intelligence only**:

- Used to understand brushwork, medium, and artistic intent

- Informs descriptions like "painterly texture" or "soft impressionistic strokes"

- **NEVER** output as raw text in customer-facing descriptions

- Stripped from final `listing.json` output

#### seed_context.json Schema

```json
{
  "location": "The Coorong, SA",
  "sentiment": "Ghostly",
  "original_prompt": "Oil painting style, golden hour...",
  "created_at": "2026-02-03T00:30:00Z",
  "updated_at": "2026-02-03T00:30:00Z"
}
```

## 9. Global Navigation

- Single Admin Hub overlay replaces all legacy overlays and lives in `application/common/ui/templates/overlays/menu_overlay.html`; styling is in `application/common/ui/static/css/overlays.css` and JS in `application/common/ui/static/js/overlay-menus.js`.

- Overlay behavior: locks background scroll, closes on ESC/outside click, no Bootstrap involvement, z-index above modals.

- Workspace navigation:

  - Primary workflow navigation is rendered as a persistent left sidebar in `application/common/ui/templates/base.html`.

  - Sidebar styling lives in `application/common/ui/static/css/sidebar.css`.

  - Sidebar reads artist identity from `application/var/profile.json` via a safe context processor.

- Menu → route map:

  - Admin Hub → `hub.home` (`/admin/hub/`)

  - Upload Artwork → `upload.upload_page` (`/artworks/upload`)

  - Unprocessed Artwork → `upload.unprocessed` (`/artworks/unprocessed`)

  - Unprocessed Artwork (per-slug view) → `upload.unprocessed_item` (`/artworks/unprocessed/<slug>`)

  - Processed Artwork → `upload.processed` (`/artworks/processed`)

  - Locked Artwork → `upload.locked` (`/artworks/locked`)

  - Mockup Bases → `mockups_admin.bases` (`/admin/mockups/bases`)

  - Upload Mockup Bases → `mockups_admin.upload_bases` (`/admin/mockups/bases/upload`)

  - Style → `hub.style_editor` (`/admin/hub/style`)

## 9A. Modular Theme System (Darkroom Presets)

- Source of truth for theme presets is JSON, stored under `application/var/themes/`:

  - Root presets: `application/var/themes/<name>.json`

  - System presets: `application/var/themes/system/<name>.json`

  - User presets: `application/var/themes/user/<name>.json`

- Active preset state:

  - `application/var/themes/user/current_style.json` (twin preset with `light` and `dark` values)

- CSS generation:

  - Each preset compiles to `application/common/ui/static/css/presets/<preset>.css`.

  - Templates link only the active preset CSS file; there is no global theme CSS pipeline.

- Admin hub ownership:

  - Template: `application/admin/hub/aui/templates/style_editor.html` (minimal container only)

  - UI renderer: `application/admin/hub/aui/static/js/style_editor.js` (sole renderer)

  - Bootstrap data endpoint: `GET /admin/hub/style/data` returns `{defaults, current, presets}`.

  - Save endpoint: `POST /admin/hub/style/save` accepts twin payloads `{name, light, dark, mode}`.

- Typography rule:

  - Global UI uses Outfit; preset `font_family`/`font_heading` values must resolve to Outfit.

- Bootstrap removal rule:

  - Bootstrap layout classes and assets are forbidden on admin/artwork templates; use `artlomo-admin-surface` and `artlomo-workstation-grid`.

## 10. Mockups Admin Scope (Updated)

- Mockup bases are externally authored RGBA PNGs; the app ingests them, generates coordinates, and manages category/aspect/state only.

- Template generation is deprecated and removed; there is no in-app template/catalog browser.

- Supported admin surfaces:

  - Upload Mockup Bases → `mockups_admin.upload_bases` (`/admin/mockups/bases/upload`)

  - Mockup Bases → `mockups_admin.bases` (`/admin/mockups/bases`)

- Categories/coordinate tooling operate on bases; any legacy template semantics are out of scope.

### Mockup Engine: Coordinate Standard (Authoritative)

- Coordinate JSON schema is v2.0 and is the only supported write format.

- Format:

  - `format_version: "2.0"`

  - `zones[].points`: exactly 4 points ordered TL, TR, BR, BL (clockwise).

- Metadata:

  - `catalog.json` base entries record `coordinate_type: "Perspective"` when coordinates are generated via high-fidelity detection.

- Compositing:

  - Artwork is warped/placed first; base PNG is composited last so the template frame hides bleed and remains foreground.

### Mockup Generation: Strict Zone Stretching (Authoritative)

- When a coordinate entry defines an axis-aligned zone (rectangle via `x/y/w/h` or equivalent corners), the engine must:

  - Resize the artwork to the exact zone dimensions (`w × h`) using high-quality resampling.

  - Paste starting exactly at `(x, y)` (no centering offsets).

  - Perform no cropping and no aspect-preserving fit logic; the artwork may stretch/squeeze to meet the zone corners.

- The base PNG is composited last so template shadows/reflections/foreground remain visible.

### Mockup Bases: Physical Inventory + Naming (Authoritative)

- Physical source of truth for base inventory is the folder tree under:

  - `application/mockups/catalog/assets/mockups/bases/` (aspect/category subfolders)

- UI category counts (e.g. `Kitchen (0)`) are computed by scanning physical folders for `*.png` files; no legacy JSON index is used for inventory counts.

- The `Sanitize & Sync` operation is a destructive filesystem maintenance action exposed only in the mockup bases admin UI:

  - Endpoint: `POST /admin/mockups/bases/sanitize-sync` (CSRF required)

  - Responsibilities: normalize filenames, ensure 500×500 JPG thumbs exist, and sync `catalog.json` base entries to match disk.

- Naming convention after `Sanitize & Sync`:

  - Base PNG: `[aspect]-[CATEGORY]-MU-[ID].png`

  - Base JSON: `[aspect]-[CATEGORY]-MU-[ID].json` with `template: "[aspect]-[CATEGORY]-MU-[ID].png"`

  - Base thumb JPG (500×500, white background): `[aspect]-[CATEGORY]-MU-THUMB-[ID].jpg`

## 11. Artwork States & Button Layout (Authoritative)

- State pages: `/artworks/upload` (upload only, metadata-free), `/artworks/unprocessed`, `/artworks/processed`, `/artworks/locked`. There is no `/upload/gallery`.

- Unprocessed actions (per card, fixed order): OpenAI Analysis, Gemini Analysis, Manual Analysis, then a full-width Delete row (no Review).

- Processed actions: full-width Review row only. Locked actions: Review only; no delete/re-analysis from locked.

- Layout rule: unprocessed cards stack full-width rows for the three analysis buttons and a single full-width Delete row; processed cards show a single full-width Review row; locked cards show a single full-width Review button. No inline widths or wrapping.

- Control panel rule: unprocessed/processed/locked pages include a top-right **"+ UPLOAD NEW ARTWORK"** action in the sticky control panel.

  - Templates: `application/common/ui/templates/artworks/unprocessed.html`, `processed.html`, `locked.html`.

  - Styling: `application/common/ui/static/css/upload_gallery.css` (`.btn-stark-primary`).

- Metadata DOM order on cards: Title, Artist, ID, Uploaded Date, Aspect Ratio, Resolution, DPI, File Size, Max Print Size (single label; values stored raw).

  - Upload UI: metadata-free dropzone; accepts JPG/JPEG only, max 50MB per file, multiple files allowed (sequential posts). No artist/title inputs; slug derives from SKU.

  - Upload UI (upload page): `application/common/ui/static/js/upload.js` (UploadController) binds `#uploadDropzone` and `#uploadFileInput`, handles click/Enter/Space + drag/drop with preventDefault/stopPropagation guards (no browser file-open), validates JPG/JPEG and size (50MB UI cap), posts with `X-Requested-With` set, and never scans the filesystem. Feedback is modal-only and stage-based (no percent bars or fake progress); spinners swap icons based on `data-theme`.

  - Upload response for AJAX includes `{status, slug, thumb_url, unprocessed_url}`; the page renders a session-local results list (thumb + slug + status) and clears it on the next batch. Links always return to `/artworks/unprocessed` (list view), not per-slug pages. No DOM or filesystem inference is permitted.

  - Processing status: single source of truth is `lab/unprocessed/<slug>/processing_status.json`. Public read-only endpoint `/artworks/<slug>/status` (owned by upload routes/blueprint) returns `{id, stage, message, done, error}` from that file; if the slug folder or status file is missing it returns HTTP 200 with `{stage:"preparing", done:false}` to avoid UI stalls. Legacy `stage="done"` is normalized to `complete` for the UI. Frontend polls every 1000ms, renders human-friendly text derived from the status message (fallback map: queued/preparing/uploading → Preparing uploads… or Uploading files…, upload_complete/processing → Upload complete. Processing…, qc → Quality checking artwork…, thumbnail → Generating thumbnails…, derivatives → Generating artwork files…, writing_metadata/metadata → Writing metadata…, finalizing → Finalizing artwork…, complete → Processing complete, error → Error), treats missing status as “Preparing uploads…”, ignores percent, and shows spinners only when stage is neither complete nor error.

### Artwork Upload & Processing Lifecycle

- Upload vs processing separation: the upload request saves the file, writes an initial `processing_status.json` (`stage=queued`, `done=false`), triggers background processing, and returns immediately—no waiting for QC/derivatives/metadata.

- Modal-first UX: on file select/drop, the modal opens instantly with “Uploading files…” and a spinning arrows icon (theme-aware: light/dark). Once uploads finish, it reads “Upload complete. Processing…” with no percent displays.

- Polling: every 1000ms per slug against `/artworks/<slug>/status` until `stage == "complete"` (legacy `done` is normalized) or `error` is present; stage mapping follows the status message with the fallback map noted above. Percent never gates UI. Missing status continues polling with “Preparing uploads…”.

- Completion: the modal is batch-gated. It only closes when (1) the batch has seen all expected slugs for the user-selected files and (2) every slug reports completion (`done:true` or `stage == "complete"`). Progress logs to the console as `Batch status: X of Y complete`. Close/Background hides the modal without canceling backend processing; polling continues until completion to allow deterministic cleanup.

### Artwork Upload Pipeline

- Flow: Upload → QC → Thumbnail/Derivatives → Metadata → Finalizing → Complete (reflected in `lab/unprocessed/<slug>/processing_status.json`, with legacy `done` supported for compatibility).

- UI polls `/artworks/<slug>/status` every 1000ms and renders stage labels/messages only; percent progress and fake timing are intentionally removed to keep the UI truthful and deterministic.

### Processed Gallery: Analysis Source Labeling

| - Processed listings may display a source badge: `SOURCE: OPENAI | GEMINI | MANUAL`. |

- Source plumbing:

  - `application/upload/routes/upload_routes.py` enriches each processed listing item with `analysis_source`.

  - Resolution order:

  - Preferred: `lab/processed/<slug>/listing.json` `analysis_source`.

  - Fallbacks: `metadata_manual.json` / `metadata_openai.json` / `metadata_gemini.json`.

  - Final fallback: `metadata.json` `analysis_source`.

  - Rendered in `application/common/ui/templates/artworks/processed.html` (badge is conditional).

  - Styled in `application/common/ui/static/css/upload_gallery.css` (`.analysis-source-badge`).

### Gallery Card Vertical Alignment

- Gallery cards must align action blocks across the grid.

- Rule: card info is a flex column and `.artwork-actions` is pushed to the bottom using `margin-top: auto`.

- Implementation lives in `application/common/ui/static/css/upload_gallery.css` under `[data-gallery-minimal]`.

## 11A. Dual Analysis Engine Architecture

### Overview

ArtLomo implements a **Dual Analysis Engine** that supports two distinct market strategies without modifying runtime code or database schema. The architecture uses **Analysis Presets** as strategy containers, allowing the same AI infrastructure to serve both Commercial (Marketplace) and Collector (High-Ticket) positioning.

### Core Concept: Preset Strategy Layer

Rather than implementing separate code paths for Commercial vs Collector analysis, the system uses presets as **strategy containers**. Each preset encapsulates:

- System prompt tone and intent (conversion-focused vs perception-focused)

- Output structure and style guide

- Narrative framing (commercial vs curatorial)

- Provider (OpenAI / Gemini)

This design maintains:

- **No schema changes:** Both engines output identical listing.json format

- **No service branching:** Same `AnalysisPresetService` orchestrates all analysis

- **Provider abstraction:** OpenAI and Gemini remain interchangeable

- **Backwards compatibility:** Existing workflows unaffected

- **Future extensibility:** New market strategies are new presets, not code changes

### Commercial Engine (Marketplace Mode)

**Purpose:** Generate SEO-rich, conversion-focused Etsy listings optimized for marketplace discoverability and sales volume.

## Preset Characteristics

- **Tone:** Sales-oriented, benefit-driven, accessible

- **Intent:** Maximize conversion funnel (clicks → adds to cart → purchases)

- **Output Style:** Product-first narrative with heritage accent

- **Description Focus:** Value proposition, use cases, shipping/returns integration

- **Visual Analysis:** Commercial attributes (trendiness, color psychology, market category)

- **Pricing Framework:** Mid-tier ($15–$45 range, volume-based)

- **Export Target:** Direct Etsy listing upload or marketplace partner APIs

## Data Flow

1. Artist uploads artwork

1. Selects Commercial preset (e.g., "OpenAI - Commercial Engine v1")

1. AI analysis generates conversion-focused title, description, tags

1. Output routed to `listing.json` with `engine_type: "commercial"`

1. Export bundle includes commercial `listing_boilerplate`

1. Artist can push to Etsy

## Key Constraint

- Commercial works must NOT be tagged as Collector Tier

- No re-categorization to Collector after commercial analysis

### Collector Engine (High-Ticket / Series Mode)

**Purpose:** Generate curatorial-grade, perception-driven listings optimized for series positioning and high-value collector sales.

Preset Characteristics

- **Tone:** Scholarly, poetic, heritage-first

- **Intent:** Convey artistic vision, scarcity, and cultural significance

- **Output Style:** Curatorial narrative with full heritage protocol

- **Description Focus:** Artistic intent, series context, limited edition philosophy

- **Visual Analysis:** Curatorial attributes (cultural meaning, historical reference, craft detail)

- **Edition Framing:** Single or limited (e.g., "1 of 5" or "Single Edition")

- **Pricing Framework:** High-ticket ($200–$1,500+ range, scarcity-based)

- **Export Target:** Gallery inventory, private collector contact, auction platforms

Data Flow

1. Artist uploads artwork

1. Marks as part of a series (e.g., "People of the Reeds – Series 3")

1. Selects Collector preset (e.g., "Gemini - Collector Engine v1")

1. AI analysis generates curatorial listing without commercial boilerplate

1. Output routed to `listing.json` with `engine_type: "collector"`

1. NO automatic export to Etsy; archives to high-ticket inventory

1. Manual promotion to gallery/collector network

## Key Constraints

- Once a work enters Collector Tier, it must NOT be reused in Commercial Tier

- Collector works do NOT include commercial `listing_boilerplate`

- No Etsy export for Collector tier (manual curation only)

- Series tagging mandatory for Collector analysis

### Preset Strategy Implementation Details

#### Storage & Selection

- Presets stored in database table `AnalysisPreset` (or JSON fallback under `application/var/analysis_presets/`)

- Service: `application/analysis/services/preset_service.py` handles load/save/query

- Selection: Admin preset editor at `/admin/analysis-management` allows artist or curator to create/edit/select presets

- Admin Hub Features:

  - **Edit Preset:** Dark-themed form with 5 prompt fields (system, full analysis, section analysis, boilerplate, metadata extraction)

  - **Save as New:** Checkbox option to create preset copies with new names (preserving originals)

  - **Export Preset:** Download any preset as JSON file for external modification and re-import

  - **Import Preset:** Upload JSON files to populate form fields (supports modified exported presets)

- Activation: Artist selects preset before triggering analysis (UI dropdown on analysis trigger button)

#### Provider Abstraction

- Each preset specifies `provider: "openai" | "gemini"`

- Service routes analysis request to correct API based on preset selection

- Response schemas identical; provider is transparent to downstream workflows

#### Prompt Composition

- System prompt loaded from preset's `system_prompt` field

- User prompt assembled from preset's `user_full_prompt` and optional `user_section_prompt`

- Listing boilerplate injected from preset's `listing_boilerplate` field

- Result: same schema, different narrative tone

### Preset Naming Convention Standard

Recommended naming format for clarity and versioning:

```text
{Provider} - {Engine Type} Engine v{Version}

Examples:
  OpenAI - Commercial Engine v1
  OpenAI - Collector Engine v1
  Gemini - Commercial Engine v1
  Gemini - Collector Engine v1
```

## Naming Rules

- Provider: `OpenAI` or `Gemini` (title case)

- Engine Type: `Commercial` or `Collector` (title case)

- Version: Integer starting at `v1`

- Pattern: `[Provider] - [Engine Type] Engine v[Version]`

## Versioning Strategy

- Increment version when preset prompt/boilerplate changes significantly

- Keep old versions available for re-analysis of historical artworks

- Document changes in preset description field

- Legacy presets can be marked deprecated but not deleted

### Integration with Heritage-First Protocol

Both engines leverage the Heritage-First system prompt as a foundation:

- Robin Custance persona remains constant

- Boandik/Bunganditj acknowledgement required in both

- "People of the Reeds" brand appears in all outputs

- 14,400px museum-quality standard mentioned in both

## Differentiation

- Commercial: Heritage framed as "authentic Australian artist tradition"

- Collector: Heritage framed as "custodianship and cultural continuity"

### No Schema Changes Required

The Dual Engine architecture achieves market differentiation through **presets alone**, not through schema changes:

- `listing.json` structure remains identical

- `metadata.json` format unchanged

- `visual_analysis` object consistent across engines

- Database schema unaffected (presets stored in `AnalysisPreset` table, existing artworks table unchanged)

- Export bundle format identical

This constraint ensures:

- Existing workflows remain compatible

- Archive integrity preserved (all artworks queryable uniformly)

- Migration risk minimized

- Future engine additions require only new presets, not code refactoring

### 11B. Detail Closeup Feature (Interactive Image Editor)

#### Purpose

Detail Closeup is an interactive image editor that lets artists zoom and pan within their artwork to select a zoomed region, which is then rendered as a high-quality 2000x2000px derivative suitable for detailed product photography, close-up gallery views, or Etsy variant listings.

#### Architecture: Proxy vs Master Split

The feature employs a **two-stage rendering strategy** to balance responsiveness with quality:

1. **Proxy Preview (UI Stage):** Editor loads a 3500px long-edge proxy image in a 500x500px viewport

- Fast, low-bandwidth for interactive zoom/pan

- User sees real-time feedback at 1:7 scale

- No master image transferred to browser

1. **Master Rendering (Save Stage):** Crop applied to full 14400px master image

- Perfect quality output: exactly 2000x2000px

- Transforms computed server-side from viewport parameters

- All heavy lifting deferred to POST /save endpoint

#### Routes & Endpoints

## Serving Proxy

- `GET /<slug>/detail-closeup/proxy` → Returns 3500px long-edge JPEG (auto-generated on first access)

- Cache: File persisted as `lab/processed/<slug>/<slug>-CLOSEUP-PROXY.jpg`

- Fallback: If proxy missing, service generates it from master on-demand

## Editor UI

- `GET /<slug>/detail-closeup/editor` → Renders interactive editor template

- Includes viewport (500x500px), zoom ±10% buttons, drag-to-pan, FREEZE button, SAVE button

- Template: `application/artwork/ui/templates/detail_closeup_editor.html`

- JavaScript module: `application/artwork/ui/static/js/detail_closeup.js` (`DetailCloseupEditor` class)

- Styling: `application/artwork/ui/static/css/detail_closeup.css`

## Preview (Freeze)

- `POST /<slug>/detail-closeup/freeze` → Render and return preview as base64 data URL

- JSON body: `{"scale": 1.5, "offset_x": 100, "offset_y": 50}`

- Response: `{"status": "ok", "preview_data": "data:image/jpeg;base64,..."}`

- Non-destructive: does NOT persist to disk

- Used for client-side preview before final save

## Save Final Crop

- `POST /<slug>/detail-closeup/save` → Render crop from master and persist

- JSON body: `{"scale": 1.5, "offset_x": 100, "offset_y": 50}`

- Response: `{"status": "ok", "url": "/<slug>/detail-closeup"}`

- Output file: `lab/processed/<slug>/mockups/<slug>-detail-closeup.jpg` (2000x2000px)

- Registered in mockup metadata as slot=999 for future expansion

- Redirects artist to review page on success

## View Saved Crop

- `GET /<slug>/detail-closeup` → Return saved 2000x2000px JPEG or 404 if not saved

- Served directly with appropriate image headers

### Service Layer

**Class:** `DetailCloseupService` (file: `application/artwork/services/detail_closeup_service.py`)

## Methods

- `generate_proxy_preview(slug)` → Creates 3500px long-edge proxy from master (one-time)

- `render_detail_crop(slug, scale, offset_x, offset_y)` → Renders 2000x2000px crop from master with transforms

  - Input validation: scale ∈ [0.1, 10.0], offsets clamped to valid region

  - Returns file path on success, None on failure

- `has_detail_closeup(slug)` → Checks if saved crop exists

- `get_detail_closeup_url(slug)` → Returns URL if saved, None otherwise

## Algorithm (Render Detail Crop)

```text
1. Load master image (14400x14400px)
2. Compute crop region from scale/offsets:
   - viewport_size = 2000 (output target)
   - crop_width = ceil(viewport_size / scale)  # zoom 2x = half the image
   - crop_x = clamp(offset_x / scale, 0, 14400 - crop_width)
   - crop_y = clamp(offset_y / scale, 0, 14400 - crop_height)
3. Extract crop region from master
4. Resize to exactly 2000x2000px (LANCZOS resampling)
5. Save as JPEG (quality=95) to mockups/<slug>-detail-closeup.jpg
```

### Editor JavaScript (`DetailCloseupEditor` Class)

## Initialization

- Loads proxy image into 500x500px viewport

- Sets up drag-to-pan, zoom buttons, keyboard shortcuts

- State: `scale` (1.0–3.0), `offset_x`, `offset_y`

## Interactions

- **Zoom In (+10%):** `scale += 0.1`, clamp to max 3.0

- **Zoom Out (−10%):** `scale -= 0.1`, clamp to min 1.0

- **Drag Pan:** Track mouse movement, update offsets, clamp to bounds

- **FREEZE:** POST scale/offsets to `/freeze` → display base64 preview

- **SAVE:** POST scale/offsets to `/save` → redirect to review on success

- **Keyboard:** `+`/`-` zoom, SPACE freeze, ENTER save

## Bounds Clamping

- Prevent pan outside visible region (user sees whole viewport)

- At scale 1.0: offsets locked to 0 (no pan below fit)

- At scale >1.0: offsets clamped to `[-(viewport_display - 500), 0]`

### Storage Integration

## File Locations

- Master: `lab/processed/<slug>/<slug>-MASTER.jpg` (14400x14400px, unchanged)

- Proxy: `lab/processed/<slug>/<slug>-CLOSEUP-PROXY.jpg` (3500px long-edge, auto-generated)

- Saved Crop: `lab/processed/<slug>/mockups/<slug>-detail-closeup.jpg` (2000x2000px)

## Metadata

- Slot assignment: detail closeup registered as slot 999 in existing mockup metadata

- No new schema fields; integrates with existing mockup infrastructure

### Security & Validation

- **CSRF Protection:** All POST routes require `X-CSRF-Token` header

- **Slug Validation:** Uses `slug_sku.is_safe_slug()` on all routes; rejects path traversal

- **Scale Bounds:** Rejected if outside [0.1, 10.0]

- **Offset Clamping:** Automatically clamped to valid region; no truncation errors

#### Non-Destructive Design

- Master, ANALYSE, THUMB, and listing.json are **never modified**

- Detail closeup is an additional derivative (like mockups)

- Can be regenerated or deleted without affecting other workflows

- Artist can re-edit by visiting `/detail-closeup/editor` again (overwrites previous)

#### Integration with Review Page

The Review page (`analysis_workspace.html` from `application/common/ui/templates`) includes:

- Detail Closeup tile (if exists): preview image + "Edit" link to `/detail-closeup/editor`

- No tile if not yet created; can be accessed via direct URL to `/detail-closeup/editor`

#### Static Assets (Relocated)

- `detail_closeup.css` and `detail_closeup.js` live in `application/common/ui/static/css/` and `application/common/ui/static/js/` respectively.

- Templates use `url_for('static', filename='css/detail_closeup.css')` and `url_for('static', filename='js/detail_closeup.js')` which resolve via the global static endpoint.

#### Testing

File: `tests/test_detail_closeup.py`

Coverage:

- Proxy generation from master

- Crop rendering with zoom/pan transforms

- Scale bounds validation (reject <0.1, >10.0)

- Offset clamping to valid region

- Exact 2000x2000px output verification

- Route handlers (slug validation, CSRF protection, 404 for unsaved)

- Full workflow (proxy → freeze → save → view)

### 11C. Video Generator (Promo Video)

#### Video Purpose

Generates a 15-second vertical (1080×1920) promo video from artwork assets for social media or Etsy listings.

#### Video Routes & Endpoints

- `POST /artwork/<slug>/video/generate` (CSRF required) — triggers video generation, returns JSON `{status, message, video_url}`.

- `GET /artwork/<slug>/video` — serves the generated `promo_video.mp4`.

#### Service

- **File:** `application/tools/video/service.py`

- **Function:** `generate_promo_video(processed_dir: Path, slug: str) -> Optional[Path]`

#### Assets Used

- Main artwork: ANALYSE image (fallback to THUMB)

- Detail Closeup: `mockups/<slug>-detail-closeup.jpg` (if exists)

- Top 2 mockups: composites from `mockups/mu-<slug>-*.jpg` (excluding THUMB)

#### Text Overlay

- Pulls Pioneer Engine 13-point story snippets from `listing.json` (etsy_description split by `---`, etsy_title, visual_analysis subject/mood).

- Kinetic text overlay: one snippet per segment.

#### Output

- **Path:** `lab/processed/<slug>/promo_video.mp4` (Single-State Invariant; video stays with artwork)

- Format: 1080×1920, 15 seconds, 24 fps, H.264

#### UI Integration

- "Generate Promo Video" button in the left media panel of the shared `analysis_workspace.html`.

- Button triggers POST to generate endpoint; on success opens video in new tab.

## 12. Artwork Lifecycle & Single-State Invariant

- Only one location is valid for a slug at any time: `lab/unprocessed/<slug>/`, `lab/processed/<slug>/`, OR `lab/locked/<slug>/` (never more than one).

- First successful analysis (OpenAI, Gemini, Manual) moves the folder from unprocessed → processed (atomic move, not copy) and updates the artworks index.

- Locked slugs reside under `lab/locked/<slug>/`; they are immutable, not deletable by default, and block re-analysis.

- Reanalysis operates in place on `lab/processed/<slug>/` and never creates duplicate folders or assets.

- Registry/index is authoritative for processed lookups; scanning or inferring paths is forbidden.

## 12A. Export Engine (Processed → Export Bundle)

- Export API (registered under `/api`):

  - `POST /api/export/<sku>` (CSRF required) starts a background export.

  - `GET /api/export/status/<sku>` returns the latest export manifest + download URL when ready.

  - `GET /api/export/download/<sku>/<export_id>` downloads the zip for an export.

- Export contents:

  - Copies canonical assets from `lab/processed/<slug>/` (as defined by `<slug>-assets.json`) into an export bundle.

  - Writes a `manifest.json` and a `*.zip` into `outputs/exports/<sku>/<export_id>/`.

## 13. Analysis/Edit Page Actions

- Analysis pages (OpenAI, Gemini, Manual) must present: Reanalyse with OpenAI, Reanalyse with Gemini, Go to Manual Analysis.

- Review is editable; metadata edits happen in-place on processed storage.

- Generate Mockups is allowed only from analysis/edit contexts, never from the upload gallery.

### Analysis Workstation UI Standard (Authoritative)

- Ultra-wide container: analysis/edit surfaces use `artlomo-admin-surface` with a 2400px max width.

- Two-column workstation: analysis/edit pages use `artlomo-workstation` with a 45% left pane (preview + mockups) and 55% right pane (forms/data).

- Scroll behavior: the right pane is the primary scroll container (`artlomo-workstation__scroll`) so the left preview remains visible.

- Utility exception: `.stark-nav-btn.theme-toggle` (and its child `.theme-icon`) is a permanent high-visibility exception and must remain 150×50px.

### Universal Overlay Carousel Modal (Required)

- All analysis/edit pages must include the overlay carousel modal markup `#artPreviewModal`.

- Any `.art-card` thumbnail (preview or mockup) must be clickable to open the modal.

- The modal provides previous/next navigation across all `.art-card` elements on the page.

### Lab Action Strip (Authoritative)

- Analysis/edit pages (OpenAI, Gemini, Manual) use a single horizontal action strip for primary actions:

  - Reanalyse with OpenAI

  - Reanalyse with Gemini

  - Go to Manual Analysis

- The legacy "Review" button is not used on analysis/edit pages.

### Workstation Action Suite (Required)

- AI analysis review pages (OpenAI/Gemini) must provide a workstation-scoped action suite:

  - Save Changes (persists listing fields)

  - Lock Artwork (moves processed → locked)

  - Delete Artwork (destructive; requires confirmation)

### Workstation Button Dimension Standard (42px)

- All action buttons inside `artlomo-workstation__left` and `artlomo-workstation__right` must be exactly 42px tall.

- Header navigation controls are explicitly excluded from this rule; header sizing is governed globally and must not be overridden by workstation rules.

### Mockup Preview Grid Standard (Authoritative)

- All mockup preview grids (Manual workspace, OpenAI review, Gemini review) must provide management controls on every mockup card:

  - Category selector (dropdown)

  - Swap action

- DOM hook standard:

  - Cards use `.mockup-card[data-slot]`

  - Category selector uses `[data-category]`

  - Swap trigger uses `[data-swap]`

  - Grid root uses `#mockup-grid[data-slug]`

- Behavior:

  - Changing category must persist immediately via an AJAX POST to `/artwork/<slug>/mockups/<slot>/category`.

  - Swap must POST to `/artwork/<slug>/mockups/<slot>/swap` and update the card thumb/composite URLs without requiring a full page reload.

## 14. Delete Flows & Ownership

- Artworks delete uses a modal-only flow that requires typing DELETE and issues AJAX POST to `/artworks/unprocessed/<slug>/delete` or `/artworks/processed/<slug>/delete`; the DOM card is removed without navigation.

- Locked items are non-destructive by default; no delete action is exposed.

- Global delete handlers must not bind on `/artworks/*`; pages own their delete UX (one modal per page, no overlapping listeners).

- Placeholder delete pages must not load underneath modals.

## 17. Artworks Delete Modal (Custom, Bootstrap-free)

- Artworks pages share a single custom modal (`#uploadDeleteModal`) with bespoke classes (`upload-modal`, `upload-modal-backdrop`, `upload-modal-dialog`); `.modal`/`.modal-backdrop` are forbidden here.

- Bootstrap JS/CSS must not drive the modal. Stack: backdrop z-index 900, container 1000, dialog 1001.

- Behavior: body scroll lock via `overlay-lock`/`upload-modal-open`, focus trap inside the dialog, ESC/backdrop/close button dismiss, and focus restoration to the trigger.

- Confirmation requires typing `DELETE` and posts via fetch; on success the card is removed in DOM with no navigation.

## 15. Mockup System Boundaries (Bases Only)

- Mockup templates are removed; only base ingestion and base management remain.

- Valid admin pages: `/admin/mockups/bases/upload` (base upload surface) and `/admin/mockups/bases` (base management).

- Bases are uploaded as PNGs; coordinates are generated automatically; no template catalog is kept.

- Mockups are not generated automatically from the upload gallery; mockup actions remain confined to the admin bases flows.

## 16. File System Invariants

- No duplicated artwork folders; promotions are atomic moves.

- No parallel manual/processed copies; edits update the single processed folder.

- Mockup catalog assets may be excluded from backups; backups must respect configured excludes.
