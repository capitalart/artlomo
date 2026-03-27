# ArtLomo System Map: 4-Layer Architecture

**Date:** March 9, 2026
**Purpose:** Visual structural map showing how data flows from core utilities up through services, routes, and UI
**Status:** ✅ Consolidated from ARCHITECTURE_INDEX, MASTER_FILE_INDEX, MASTER_WORKFLOWS_INDEX, and CONTEXT_INDEX

## March 9, 2026 Addendum: Curated AI Handoff Snapshot

- Added `tools.sh gemini` command to generate a single curated handoff file for external AI review:

  - `application/tools/app-stacks/stacks/application-gemini-code-stack-<TIMESTAMP>.md`

- Stack generation now supports profile-based behavior (`full`, `gemini`) in `code-stacker.sh`.

- Nested dependency and cache folders are pruned at any depth to prevent stack bloat.

- `.env` is excluded from generated stack files by default.

## March 7, 2026 Addendum: Operational Documentation Layer

- Added operational inventory tooling at `application/tools/app-stacks/files/system-inventory.sh`.

- Updated orchestrator `application/tools/app-stacks/files/tools.sh` with `sysinfo` command and inclusion in `all`.

- New documentation outputs now include system/runtime/environment inventory under `application/tools/app-stacks/stacks/`.

- This addendum does not change core 4-layer dependency rules; it extends observability and documentation coverage.

---

## 🎯 ARCHITECTURAL PRINCIPLE: LAYERED DEPENDENCY FLOW

ArtLomo is a **modular monolith** built on Flask, organized into 4 distinct architectural layers. Data and dependencies flow **upward only**—lower layers never import from upper layers.

```text
┌─────────────────────────────────────────────────────────────┐
│ LAYER 4: UI (Templates, Static, Frontend)                   │
│ "The Skin" - User interface, CSS, JavaScript                │
└──────────────────────┬──────────────────────────────────────┘
                       │ ▲ Consumes data from Layer 3
                       ↓ │
┌─────────────────────────────────────────────────────────────┐
│ LAYER 3: ROUTES (Orchestration, HTTP Endpoints)             │
│ "The Brain" - URL handling, request/response coordination    │
└──────────────────────┬──────────────────────────────────────┘
                       │ ▲ Calls business logic from Layer 2
                       ↓ │
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2: SERVICES (Business Logic, Workflows)               │
│ "The Muscles" - AI integration, file processing, data logic  │
└──────────────────────┬──────────────────────────────────────┘
                       │ ▲ Uses utilities from Layer 1
                       ↓ │
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: CORE (Utils, Common, Config)                       │
│ "The Heart" - Image processing, logging, auth, constants     │
└─────────────────────────────────────────────────────────────┘
```

**Golden Rule:** Lower layers provide capabilities; upper layers consume them. **No circular dependencies.**

---

## 🔹 LAYER 1: THE CORE (Utils, Common, Config)

**Responsibility:** Foundation utilities, image processing, logging, security, configuration constants.

## Characteristics

- **Zero workflow knowledge** - Cannot import from workflows

- **Pure utility functions** - No business logic

- **Shared infrastructure** - Used by all layers above

### 1.1 Low-Level Utilities (`application/utils/`)

**Purpose:** Cross-cutting helpers with no domain coupling

```text
application/utils/
├── ai_utils.py              # AI response sanitization (clean_json_response, safe_parse_json)
├── ai_services.py           # OpenAI/Gemini client wrappers
├── ai_context.py            # Seed context construction for AI prompts
├── house_prompts.py         # Pioneer Engine v1.0 (13-paragraph Etsy SEO structure)
├── house_style.py           # Listing boilerplate standardization
├── image_utils.py           # Low-level image operations (PIL wrappers)
├── image_processing_utils.py # Derivative generation (THUMB, ANALYSE, MOCKUP)
├── image_urls.py            # URL construction for artwork assets
├── artwork_files.py         # File path resolution for artwork assets
├── artwork_db.py            # Database operations for artwork records
├── art_index.py             # Master artwork index management
├── file_utils.py            # File system operations (copy, move, delete)
├── json_util.py             # JSON read/write with error handling
├── env.py                   # Environment variable loading
├── logger_utils.py          # Logging configuration + security event logging
├── security.py              # CSRF, session management, auth decorators
├── categories.py            # Category/aspect ratio mappings
├── aspect_loader.py         # Aspect ratio calculations
├── sku_assigner.py          # SKU sequence generation
├── content_blocks.py        # Content block rendering
├── template_helpers.py      # Jinja2 helper functions
├── template_engine.py       # Template rendering utilities
├── auth_decorators.py       # @admin_required, @login_required
├── csrf.py                  # CSRF token generation/validation
└── session_tracker.py       # Admin session tracking (max concurrent sessions)
```

## Dependency Rules

- ✅ **CAN IMPORT:** stdlib, third-party libraries, other `application/utils/` files

- ❌ **CANNOT IMPORT:** workflows (`upload`, `analysis`, `artwork`, etc.), `application/common` domain logic

---

### 1.2 Domain-Friendly Helpers (`application/common/utilities/`)

**Purpose:** Shared utilities that understand artwork/mockup domain but remain reusable

```text
application/common/utilities/
├── images.py         # High-level image generation (calls image_processing_utils)
├── files.py          # Artwork-aware file operations
├── paths.py          # Path construction for lab/ structure
├── slug_sku.py       # Slug/SKU generation and validation
└── indexer.py        # Artwork index read/write operations
```

Dependency Rules

- ✅ **CAN IMPORT:** `application/utils/`, `config.py`

- ❌ **CANNOT IMPORT:** workflows (`upload`, `analysis`, `artwork`, etc.)

---

### 1.3 Configuration (`application/config.py`)

**Purpose:** Application-wide constants and environment bindings

## Key Constants

- `ANALYSE_LONG_EDGE = 2048` - AI vision model image size

- `THUMB_SIZE = 500` - Gallery thumbnail size

- `MOCKUP_LONG_EDGE = 2048` - Mockup composite size

- `DETAIL_CLOSEUP_SIZE = 2000` - Detail closeup size

- `MASTER_PROXY_LONG_EDGE = 7200` - High-res proxy for detail closeup editor

- `LOG_CONFIG` - Structured logging paths and formats

Dependency Rules

- ✅ **CAN IMPORT:** stdlib, safe helpers from `application/utils/`

- ❌ **CANNOT IMPORT:** workflow business logic

---

### 1.4 Logging Configuration (`application/logging_config.py`)

**Purpose:** Centralized logging setup for all workflows

## Log Destinations

- `/srv/artlomo/logs/ai_processing.log` - AI service calls and diagnostics

- `/srv/artlomo/logs/security.log` - Security events (login, role changes, deletes)

- `/srv/artlomo/logs/app.log` - General application logs

Dependency Rules

- ✅ **CAN IMPORT:** stdlib only

- ❌ **CANNOT IMPORT:** any application code

---

## 🔹 LAYER 2: THE SERVICES (Business Logic, Workflows)

**Responsibility:** Domain-specific business logic, AI integration, file processing, data transformations

Characteristics

- **Workflow isolation** - Workflows cannot import from each other

- **Service modules** - Pure functions with clear inputs/outputs

- **No HTTP knowledge** - Services don't know about Flask requests/responses

### 2.1 Analysis Workflow (`application/analysis/`)

**Purpose:** AI-driven analysis integration (Gemini/OpenAI) and Etsy listing generation

```text
application/analysis/
├── prompts.py                      # Heritage-First system prompts (14,400px, 13 tags, People of the Reeds)
├── gemini/
│   ├── service.py                  # Gemini API calls, schema validation, listing persistence
│   └── schema.py                   # GeminiArtworkAnalysis Pydantic model (8 fields + visual_analysis)
├── openai/
│   ├── service.py                  # OpenAI API calls (parallel to Gemini)
│   └── schema.py                   # OpenAIArtworkAnalysis Pydantic model
├── manual/
│   └── services/
│       └── manual_service.py       # Manual workspace operations (lock, save, metadata updates)
├── api/
│   └── routes.py                   # Analysis API endpoints (LAYER 3 - included here for context)
└── instructions/
    ├── MASTER_ETSY_DESCRIPTION_ENGINE.md      # Etsy copywriting protocol (source of truth)
    └── MASTER-ARTWORK-ANALYSIS-LISTING-DESCRIPTION-EXAMPLE.md  # Few-shot example
```

## Key Services

- `GeminiAnalysisService.analyze(slug)` → Returns validated `GeminiArtworkAnalysis` object

- `OpenAIAnalysisService.analyze(slug)` → Returns validated `OpenAIArtworkAnalysis` object

- `ManualService.save_workspace(slug, data)` → Persists manual edits to `listing.json`

- `ManualService.lock_artwork(slug)` → Marks artwork as immutable (prevents re-analysis)

## Output Contract (8 fields)

1. `etsy_title` (max 140 chars)

1. `etsy_description` (formatted with line breaks)

1. `etsy_tags` (exactly 13 tags)

1. `visual_analysis` (4 fields: subject, dot_rhythm, palette, mood)

1. `seo_filename_slug` (max 61 chars)

1. `materials` (exactly 13 items)

1. `primary_colour`

1. `secondary_colour`

Dependency Rules

- ✅ **CAN IMPORT:** `application/common`, `application/utils`, `config.py`

- ❌ **CANNOT IMPORT:** `upload`, `artwork`, `mockups`, `admin` workflows

---

### 2.2 Upload Workflow (`application/upload/`)

**Purpose:** File ingestion, quality control, derivative generation, status tracking

```text
application/upload/
└── services/
    ├── storage_service.py     # File storage, folder management, metadata persistence
    ├── qc_service.py          # Quality control analysis (dimensions, DPI, blur, compression)
    └── thumb_service.py       # Thumbnail generation (THUMB, ANALYSE derivatives)
```

Key Services

- `StorageService.store_artwork(file, slug)` → Stores MASTER, generates derivatives

- `QCService.analyze(slug)` → Produces `qc.json` (dimensions, DPI, palette, luminance, edge_safety)

- `ThumbService.generate(slug)` → Creates THUMB (500px) and ANALYSE (2048px) images

## Workflow Stages (11 stages)

1. QUEUED → 2. PREPARING → 3. UPLOADING → 4. UPLOAD_COMPLETE → 5. PROCESSING → 6. QC → 7. THUMBNAIL → 8. DERIVATIVES → 9. METADATA → 10. FINALIZING → 11. COMPLETE

Dependency Rules

- ✅ **CAN IMPORT:** `application/common`, `application/utils`, `config.py`

- ❌ **CANNOT IMPORT:** `analysis`, `artwork`, `mockups`, `admin` workflows

---

### 2.3 Artwork Workflow (`application/artwork/`)

**Purpose:** Artwork domain operations (detail closeup, processing orchestration)

```text
application/artwork/
└── services/
    ├── detail_closeup_service.py   # Detail closeup generation (2048px crop + 7200px proxy)
    └── processing_service.py       # Processing orchestration (promotes unprocessed → processed)
```

Key Services

- `DetailCloseupService.generate(slug, coordinates)` → Creates detail closeup from normalized coordinates

- `ProcessingService.process(slug, provider)` → Orchestrates analysis workflow, updates artwork status

Dependency Rules

- ✅ **CAN IMPORT:** `application/common`, `application/utils`, `config.py`

- ❌ **CANNOT IMPORT:** `upload`, `analysis`, `mockups`, `admin` workflows

---

### 2.4 Mockup Workflow (`application/mockups/`)

**Purpose:** Mockup generation, catalog management, selection pipeline, perspective transforms

```text
application/mockups/
├── compositor.py          # Mockup composition (artwork overlay on scenes)
├── transforms.py          # Perspective transform calculations (4-point TL/TR/BR/BL)
├── storage.py             # Mockup asset storage and retrieval
├── validation.py          # Mockup data validation (bow-tie prevention, bleed standards)
├── loader.py              # Mockup loading and caching
├── catalog/
│   ├── loader.py          # Catalog JSON loading
│   ├── models.py          # Mockup catalog data models
│   └── validation.py      # Catalog validation
└── selection/
    ├── planner.py         # Mockup selection logic
    ├── policy.py          # Selection policy enforcement
    ├── models.py          # Selection data models
    └── validation.py      # Selection validation
```

Key Services

- `Compositor.generate(slug, scene_id, coordinates)` → Creates mockup composite

- `SelectionPlanner.plan(slug, category, count)` → Selects appropriate mockup scenes

- `CatalogLoader.load()` → Loads mockup catalog from JSON

## Coordinate Schema (v2.0)

- 4-point perspective: TL (top-left), TR (top-right), BR (bottom-right), BL (bottom-left)

- Normalized coordinates (0.0 - 1.0)

- Bow-tie prevention (no crossed quads)

- 4px outward bleed standard

Dependency Rules

- ✅ **CAN IMPORT:** `application/common`, `application/utils`, `config.py`

- ❌ **CANNOT IMPORT:** `upload`, `analysis`, `artwork`, `admin` workflows

---

### 2.5 Export Workflow (`application/export/`)

**Purpose:** Export processed artwork to ZIP bundles for deployment/handoff

```text
application/export/
└── service.py     # Export bundle creation (3 modes: Etsy, Admin, Merchant)
```

Key Services

- `ExportService.export_artwork(slug, mode)` → Creates ZIP with assets + metadata

- **Modes:** Etsy (listing-ready), Admin (full assets), Merchant (print-ready)

Dependency Rules

- ✅ **CAN IMPORT:** `application/common`, `application/utils`, `config.py`

- ❌ **CANNOT IMPORT:** `upload`, `analysis`, `artwork`, `mockups` workflows

---

### 2.6 Video Generation (`application/video/`)

**Purpose:** 15-second vertical promo video generation from artwork

```text
application/video/
└── services/
    └── video_service.py    # Video generation (FFMPEG encoding, kinematic panning)
```

Key Services

- `VideoService.generate_video(slug)` → Encodes MP4 video with kinematic panning/zoom

Dependency Rules

- ✅ **CAN IMPORT:** `application/common`, `application/utils`, `config.py`

- ❌ **CANNOT IMPORT:** other workflows

---

## 🔹 LAYER 3: THE ROUTES (Orchestration, HTTP Endpoints)

**Responsibility:** URL handling, request/response coordination, calling Layer 2 services

Characteristics

- **Thin orchestration layer** - No business logic, only coordination

- **HTTP boundaries** - Handles Flask requests/responses/sessions

- **Service composition** - Calls multiple services to fulfill requests

### 3.1 Analysis Routes (`application/analysis/api/routes.py`)

**Purpose:** HTTP endpoints for triggering AI analysis and checking status

```text
Endpoints:
├── POST /api/analysis/gemini/<slug>      # Trigger Gemini analysis
├── POST /api/analysis/openai/<slug>      # Trigger OpenAI analysis
└── GET  /api/analysis/status/<slug>      # Polling endpoint (returns done, stage, error)
```

## Responsibilities

- Validates slug exists

- Calls `GeminiAnalysisService.analyze()` or `OpenAIAnalysisService.analyze()`

- Returns JSON status for polling

---

### 3.2 Manual Analysis Routes (`application/analysis/manual/routes/manual_routes.py`)

**Purpose:** HTTP endpoints for manual workspace operations

```text
Endpoints:
├── GET  /manual/workspace/<slug>          # Render manual workspace
├── POST /manual/workspace/<slug>/save     # Save manual edits
└── POST /manual/workspace/<slug>/lock     # Lock artwork (immutable)
```

Responsibilities

- Renders workspace template with `listing.json` data

- Calls `ManualService.save_workspace()` on edits

- Calls `ManualService.lock_artwork()` on lock

- Handles locked artwork errors ("locked and cannot be edited")

---

### 3.3 Upload Routes (`application/upload/routes/upload_routes.py`)

**Purpose:** HTTP endpoints for file upload, status polling, gallery views

```text
Endpoints:
├── POST /artworks/upload                     # File ingestion (dropzone)
├── GET  /artworks/<slug>/status              # Processing status polling
├── GET  /artworks/unprocessed                # Unprocessed gallery (+ analysis buttons)
├── GET  /artworks/processed                  # Processed gallery (+ review buttons)
├── GET  /artworks/locked                     # Locked gallery (review-only)
├── POST /artworks/<slug>/seed-context        # Save artist-provided context
├── DELETE /artworks/<slug>/unprocessed       # Delete unprocessed artwork + folder
└── DELETE /artworks/<slug>/processed         # Delete processed artwork + folder
```

Responsibilities

- Calls `StorageService.store_artwork()` on upload

- Calls `QCService.analyze()` and `ThumbService.generate()` in background

- Returns processing status for polling

- Handles physical folder deletion with `shutil.rmtree()`

---

### 3.4 Artwork Routes (`application/artwork/routes/artwork_routes.py`)

**Purpose:** HTTP endpoints for artwork operations (save, lock, detail closeup)

```text
Endpoints:
├── POST /artwork/<slug>/save                 # Save metadata edits
├── POST /artwork/<slug>/lock                 # Lock artwork (rename to SEO filename)
├── GET  /artwork/<slug>/review/<provider>    # Review page (AI analysis results)
└── GET  /artwork/detail_closeup_editor       # Detail closeup editor UI
```

Responsibilities

- Calls `ProcessingService.process()` for status updates

- Calls `DetailCloseupService.generate()` for detail closeups

- Handles SEO filename renaming on lock

---

### 3.5 Mockup Routes (`application/mockups/routes/`)

**Purpose:** HTTP endpoints for mockup generation and management

```text
Endpoints:
├── POST /mockups/generate/<slug>             # Generate mockups (category + count)
└── POST /mockups/swap/<slug>                 # Regenerate single mockup slot
```

Responsibilities

- Calls `SelectionPlanner.plan()` for mockup selection

- Calls `Compositor.generate()` for rendering

- Returns status + mockup URLs

---

### 3.6 Admin Routes (`application/admin/`)

**Purpose:** HTTP endpoints for admin operations (hub, users, profile, settings, theme editor)

```text
Endpoints:
├── GET  /admin/hub                           # Admin hub (control panel)
├── GET  /admin/users                         # User management
├── POST /admin/users/create                  # Create user
├── GET  /admin/profile                       # Artist profile editor
├── POST /admin/profile/save                  # Save profile data
├── GET  /admin/settings                      # System settings
└── GET  /admin/theme                         # Darkroom theme editor
```

Responsibilities

- User management (create, role assignment, password resets)

- Profile management (artist identity, bio, heritage)

- Theme presets (Darkroom, Lighthouse, Autumn, Midnight)

- Security logging for admin actions

---

### 3.7 Auth Routes (`application/routes/auth_routes.py`)

**Purpose:** HTTP endpoints for authentication (login, logout, password reset)

```text
Endpoints:
├── GET  /auth/login                          # Login page
├── POST /auth/login                          # Login authentication
├── GET  /auth/logout                         # Logout (session clear)
├── GET  /auth/forgot-password                # Password reset request
└── POST /auth/reset-password                 # Password reset execution
```

Responsibilities

- Session management (login, logout, rotation)

- CSRF token generation/validation

- Password complexity validation

- Security event logging

---

### 3.8 Site Routes (`application/site/`)

**Purpose:** HTTP endpoints for public pages (privacy, terms, sitemap)

```text
Endpoints:
├── GET  /privacy                             # Privacy policy
├── GET  /terms                               # Terms of service
└── GET  /sitemap                             # Sitemap (placeholder)
```

Responsibilities

- Renders static content pages

- No business logic

---

## 🔹 LAYER 4: THE UI (Templates, Static, Frontend)

**Responsibility:** User interface, CSS styling, JavaScript interactions

Characteristics

- **Zero business logic** - Only presentation and interaction

- **Theme-aware** - Dark mode support via CSS variables

- **Modular components** - Reusable templates and macros

### 4.1 Shared UI (`application/common/ui/`)

**Purpose:** Global templates, CSS, JavaScript shared across all workflows

```text
application/common/ui/
├── templates/
│   ├── base.html                  # Global layout shell (sidebar + content panes)
│   ├── macros/
│   │   └── help_tooltip.html      # Tooltip macro system (help_icon, help_tooltip, field_with_help)
│   └── site/
│       ├── privacy.html           # Privacy policy page
│       └── terms.html             # Terms of service page
└── static/
    ├── css/
    │   ├── darkroom.css           # Global styles (Dark/Light mode variables)
    │   ├── base.css               # Base layout (sidebar, content panes)
    │   ├── admin.css              # Admin hub styles (elevated glass header)
    │   ├── analysis-loading.css   # Loading overlay styles
    │   └── components/
    │       └── tooltip.css        # Tooltip component styles (glass morphism)
    ├── js/
    │   ├── sidebar.js             # Sidebar collapse/expand (localStorage persistence)
    │   ├── mockup_carousel.js     # Carousel modal (shared by analysis + manual workspaces)
    │   ├── analysis-loading.js    # Loading overlay + status polling
    │   └── tooltip-system.js      # Tooltip interaction logic (click-toggle, keyboard nav)
    └── icons/
        └── arrows-clockwise-dark.svg  # Spinner icon for loading states
```

## Key UI Patterns

- **Fixed Sidebar Layout:** `.app-sidebar` fixed + scrollable, `.app-content` scrollable independently

- **Modal System:** Gallery carousel, delete confirmations (append to `document.body` root)

- **Dark Mode:** CSS variables (`--text-primary`, `--text-secondary`, `--bg-primary`, etc.)

- **Glass Morphism:** `backdrop-filter: blur(10px)` for modern aesthetic

- **Loading Overlays:** Dark overlay + spinning icon + polling status updates

---

### 4.2 Analysis Workspace UI (`application/analysis/ui/`)

**Purpose:** Clean-Room v2.0 analysis workspace (unified action bar, media panel, scrollable form)

```text
application/analysis/ui/
├── templates/
│   └── analysis_workspace.html    # Clean-Room v2.0 workspace (1637 lines)
└── static/
    ├── css/
    │   └── analysis_workspace.css # Workspace-specific styles
    └── js/
        └── workspace.js           # Workspace interactions (save dirty state, modal triggers)
```

## Clean-Room v2.0 Features

- **Unified Action Bar (Sticky):** 5 context-aware buttons (Save Changes, Lock, Re-Analyse, Export, Delete)

- **45/55 Grid Layout:** 45% left stationary media panel, 55% right scrollable form

- **Media Panel:** Artwork + Detail Closeup side-by-side (max 500px each), Generate Video panel, Mockup grid with SWAP buttons

- **Context-Aware Re-Analyse:** Button detects `analysis_source` and routes to same AI provider

- **Delete Modal Safety:** Requires typed "DELETE" confirmation before action activates

- **Dark Mode Compliance:** All text uses CSS variables

---

### 4.3 Manual Workspace UI (`application/analysis/manual/ui/`)

**Purpose:** Manual review and editing interface for AI-generated metadata

```text
application/analysis/manual/ui/
├── templates/
│   └── manual_workspace.html      # Manual workspace (dual-pane layout)
└── static/
    ├── css/
    │   └── manual_workspace.css   # Manual workspace styles
    └── js/
        └── manual_workspace.js    # Manual workspace interactions
```

## Key Features

- **Dual-Pane Layout:** Left pane (artwork preview + mockup carousel), Right pane (editable forms)

- **Visual Analysis Cards:** Subject, Dot Rhythm, Palette, Mood as `<textarea>` elements

- **Lock/Unlock Controls:** Prevents re-analysis of locked artwork

- **Save Hooks:** Title, tags, description, visual_analysis fields

---

### 4.4 Upload Gallery UI (`application/upload/ui/`)

**Purpose:** Artwork gallery views (unprocessed, processed, locked)

```text
application/upload/ui/
├── templates/
│   ├── unprocessed.html           # Unprocessed gallery + analysis action buttons
│   ├── processed.html             # Processed gallery + review action buttons
│   ├── locked.html                # Locked gallery (review-only)
│   └── custom_input.html          # Artist-provided context form (Location, Sentiment, Prompt)
└── static/
    ├── css/
    │   └── upload_gallery.css     # Gallery card styles
    └── js/
        └── upload_gallery.js      # Upload interactions (analysis triggers, loading overlays)
```

Key Features

- **Card Layout:** Thumbnail preview, metadata, action buttons

- **Analysis Buttons:** OpenAI Analysis, Gemini Analysis (trigger loading overlay + polling)

- **Custom Input Form:** Location, Sentiment, Original Prompt fields (human-in-the-loop pattern)

- **Status Badges:** Unprocessed (blue), Processed (green), Locked (gray)

---

### 4.5 Admin UI (`application/admin/ui/`)

**Purpose:** Admin control panel, user management, profile editor, theme editor

```text
application/admin/ui/
├── templates/
│   ├── hub.html                   # Admin hub (control panel)
│   ├── users.html                 # User management
│   ├── profile.html               # Artist profile editor
│   └── theme.html                 # Darkroom theme editor
└── static/
    ├── css/
    │   └── admin.css              # Admin-specific styles (elevated glass header)
    └── js/
        └── admin.js               # Admin interactions
```

Key Features

- **Elevated Glass Header:** Sticky control panel with `backdrop-filter: blur(12px)`

- **Theme-Aware:** Dark/Light mode toggle with smooth transitions

- **User Management:** Create users, assign roles (admin/artist/viewer), password resets

- **Profile Editor:** Artist identity, bio, heritage (People of the Reeds)

- **Theme Presets:** Darkroom, Lighthouse, Autumn, Midnight

---

## 📊 DATA FLOW: UPLOAD → ANALYSIS → MANUAL WORKSPACE

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. USER UPLOADS FILE (LAYER 4)                              │
│    Browser: /artworks/upload (dropzone)                     │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. UPLOAD ROUTE (LAYER 3)                                   │
│    application/upload/routes/upload_routes.py               │
│    POST /artworks/upload                                    │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. STORAGE SERVICE (LAYER 2)                                │
│    application/upload/services/storage_service.py           │
│    store_artwork() → lab/unprocessed/<slug>/                │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. IMAGE PROCESSING UTILS (LAYER 1)                         │
│    application/utils/image_processing_utils.py              │
│    generate_derivatives() → THUMB (500px), ANALYSE (2048px) │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. QC SERVICE (LAYER 2)                                     │
│    application/upload/services/qc_service.py                │
│    analyze() → qc.json (dimensions, DPI, palette, etc.)     │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. USER TRIGGERS ANALYSIS (LAYER 4)                         │
│    Browser: /artworks/unprocessed → "Gemini Analysis"       │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. ANALYSIS ROUTE (LAYER 3)                                 │
│    application/analysis/api/routes.py                       │
│    POST /api/analysis/gemini/<slug>                         │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. GEMINI SERVICE (LAYER 2)                                 │
│    application/analysis/gemini/service.py                   │
│    analyze() → Gemini API call + schema validation          │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. PROMPTS (LAYER 2)                                        │
│    application/analysis/prompts.py                          │
│    HERITAGE_FIRST_SYSTEM_PROMPT (14,400px, 13 tags, etc.)   │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 10. SCHEMA VALIDATION (LAYER 2)                             │
│     application/analysis/gemini/schema.py                   │
│     GeminiArtworkAnalysis (8 fields + visual_analysis)      │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 11. PERSISTENCE (LAYER 2)                                   │
│     listing.json → lab/processed/<slug>/                    │
│     {etsy_title, etsy_description, etsy_tags, visual_analysis, ...} │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 12. MANUAL WORKSPACE (LAYER 4)                              │
│     Browser: /manual/workspace/<slug>                       │
│     Renders AI results + editable forms                     │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 13. USER EDITS & SAVES (LAYER 4)                            │
│     Browser: Edit title, tags, description → Save Changes   │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 14. MANUAL ROUTE (LAYER 3)                                  │
│     application/analysis/manual/routes/manual_routes.py     │
│     POST /manual/workspace/<slug>/save                      │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 15. MANUAL SERVICE (LAYER 2)                                │
│     application/analysis/manual/services/manual_service.py  │
│     save_workspace() → Update listing.json                  │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 16. JSON UTIL (LAYER 1)                                     │
│     application/utils/json_util.py                          │
│     safe_write_json() → Atomic write with error handling    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔒 ARCHITECTURAL BOUNDARIES & RULES

### 1. **Workflow Isolation (Horizontal Boundaries)**

**Rule:** Workflows at Layer 2 **CANNOT** import from each other.

```text
✅ ALLOWED:
   application/analysis/gemini/service.py
   ├─ from application.common.utilities.images import generate_derivative
   ├─ from application.utils.ai_utils import safe_parse_json
   └─ from application.config import ANALYSE_LONG_EDGE

❌ FORBIDDEN:
   application/analysis/gemini/service.py
   └─ from application.upload.services.storage_service import store_artwork  # VIOLATION!
```

**Enforcement:** Workflows integrate via Layer 3 routes or shared Layer 1/2 services only.

---

### 2. **Upward Dependency Flow (Vertical Boundaries)**

**Rule:** Lower layers **CANNOT** import from upper layers.

```text
✅ ALLOWED:
   LAYER 4 (UI) → imports from → LAYER 3 (Routes)
   LAYER 3 (Routes) → imports from → LAYER 2 (Services)
   LAYER 2 (Services) → imports from → LAYER 1 (Core)

❌ FORBIDDEN:
   LAYER 1 (Core) → imports from → LAYER 2 (Services)  # VIOLATION!
   LAYER 2 (Services) → imports from → LAYER 3 (Routes)  # VIOLATION!
```

**Enforcement:** Dependency direction is **always upward**.

---

### 3. **Business Logic Placement**

**Rule:** Business logic **MUST** reside in Layer 2 (Services), **NOT** in routes or UI.

```text
✅ ALLOWED:
   application/analysis/gemini/service.py
   def analyze(slug):
       # Business logic: Validate, call API, parse response, persist data
       ...

❌ FORBIDDEN:
   application/analysis/api/routes.py
   @app.route("/api/analysis/gemini/<slug>", methods=["POST"])
   def analyze_gemini(slug):
       # ❌ Business logic in route (should call service instead)
       response = gemini_client.send_prompt(...)
       ...
```

**Enforcement:** Routes are **thin orchestration layers**—they call services, handle HTTP, and return responses.

---

### 4. **UI Zero Business Logic**

**Rule:** Templates and JavaScript **CANNOT** contain business logic.

```text
✅ ALLOWED:
   analysis_workspace.html
   <button data-analysis-export>Export</button>  # UI trigger only

   workspace.js
   document.querySelector("[data-analysis-export]").addEventListener("click", () => {
       window.location.href = `/artwork/${slug}/admin-export/etsy`;  # Navigation only
   });

❌ FORBIDDEN:
   workspace.js
   document.querySelector("[data-analysis-export]").addEventListener("click", () => {
       // ❌ Business logic in UI (should call API route instead)
       const data = { title, tags, description };
       fs.writeFileSync("listing.json", JSON.stringify(data));  # VIOLATION!
   });
```

**Enforcement:** UI is **presentation and interaction only**—business logic lives in services.

---

## 🛡️ ARCHITECTURAL INVARIANTS (NON-NEGOTIABLE)

### Invariant 1: Single-State Principle

**Rule:** An artwork **MUST** exist in exactly ONE state at a time.

```text
States: lab/unprocessed/<slug>/ OR lab/processed/<slug>/ OR lab/locked/<slug>/

✅ VALID: Artwork exists in lab/processed/<slug>/
❌ INVALID: Artwork exists in BOTH lab/unprocessed/ AND lab/processed/
```

**Enforcement:** Promotions are **atomic moves** (never copies/symlinks).

---

### Invariant 2: Heritage-First Protocol

**Rule:** All AI analysis outputs **MUST** include "People of the Reeds" heritage acknowledgement.

```text
✅ ENFORCED:
   - prompts.py: HERITAGE_FIRST_SYSTEM_PROMPT (3 explicit mentions)
   - schema.py: etsy_tags (min_length=13, max_length=13, includes "people of the reeds")
   - MASTER_ETSY_DESCRIPTION_ENGINE.md: Mandatory acknowledgement protocol

❌ VIOLATION: AI output without heritage acknowledgement
```

**Enforcement:** Schema validation + prompt requirements.

---

### Invariant 3: Museum-Quality Standard

**Rule:** All AI descriptions **MUST** cite 14,400px (48 inches @ 300 DPI) as museum-quality standard.

```text
✅ ENFORCED:
   - prompts.py: "MUST cite 14,400px museum-quality standard"
   - prompts.py: "14,400px long edge = up to 48 inches (121.9 cm)"
   - config.py: Constants for derivative sizes (ANALYSE_LONG_EDGE = 2048)

❌ VIOLATION: AI output without 14,400px mention
```

**Enforcement:** Prompt requirements + manual review.

---

### Invariant 4: Image Resolution Standards

**Rule:** All image derivatives **MUST** follow exact size specifications.

```text
✅ ENFORCED:
   - MASTER: Original resolution (stored as-is)
   - ANALYSE: 2048px long edge @ 85% quality (AI vision models)
   - THUMB: 500px long edge @ 85% quality (gallery previews)
   - MOCKUP: 2048px long edge @ 85% quality (composites)
   - DETAIL: 2048px crop @ 85% quality (detail closeup)
   - PROXY: 7200px long edge @ 90% quality (detail closeup editor)

❌ VIOLATION: Derivative with incorrect dimensions
```

**Enforcement:** `config.py` constants + `image_processing_utils.py` validation.

---

## 📖 HOW TO USE THIS MAP

### Scenario 1: "Where should I add new mockup generation logic?"

**Answer:** Layer 2 (Services) → `application/mockups/compositor.py` or `application/mockups/selection/planner.py`

**Why:** Business logic belongs in services, not routes or UI.

---

### Scenario 2: "Can I import `upload/storage_service.py` from `analysis/gemini/service.py`?"

**Answer:** ❌ **NO** - Workflows cannot import from each other.

**Solution:** Use Layer 1 shared utilities (`application/utils/` or `application/common/utilities/`) or coordinate via Layer 3 routes.

---

### Scenario 3: "Where should I add a new API endpoint for triggering video generation?"

**Answer:** Layer 3 (Routes) → `application/video/routes/video_routes.py`

## Pattern

```python
@app.route("/api/video/generate/<slug>", methods=["POST"])
def generate_video(slug):
    # Thin orchestration layer - call service
    video_service = VideoService()
    result = video_service.generate_video(slug)  # Layer 2 service
    return jsonify(result)
```

---

### Scenario 4: "Can I add business logic to `analysis_workspace.html`?"

**Answer:** ❌ **NO** - UI layer (Layer 4) cannot contain business logic.

**Solution:** Add logic to Layer 2 service (`application/analysis/manual/services/manual_service.py`), expose via Layer 3 route (`application/analysis/manual/routes/manual_routes.py`), and call from UI via AJAX.

---

## 🚨 COMMON VIOLATIONS & FIXES

### Violation 1: Cross-Workflow Import

```python

# ❌ WRONG: application/analysis/gemini/service.py

from application.upload.services.storage_service import store_artwork

# ✅ RIGHT: Use shared utility

from application.common.utilities.files import store_file
```

---

### Violation 2: Business Logic in Route

```python

# ❌ WRONG: application/upload/routes/upload_routes.py

@app.route("/artworks/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    # ❌ Business logic in route
    image = Image.open(file)
    image.thumbnail((500, 500))
    image.save(f"lab/unprocessed/{slug}/{slug}-THUMB.jpg")
    ...

# ✅ RIGHT: Call service

@app.route("/artworks/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    slug = generate_slug()
    # ✅ Thin orchestration - call service
    storage_service.store_artwork(file, slug)
    return jsonify({"status": "success", "slug": slug})
```

---

### Violation 3: Lower Layer Importing Upper Layer

```python

# ❌ WRONG: application/utils/image_utils.py (Layer 1)

from application.upload.services.storage_service import store_artwork  # Layer 2

# ✅ RIGHT: Layer 1 cannot import Layer 2

# Solution: Pass service as parameter or use dependency injection

```

---

## 📚 RELATED DOCUMENTATION

| Document | Purpose | Location |
| --------------------------------- | -------------------------------------------- | ------------------------------------------ |
| ARCHITECTURE_INDEX.md | Detailed workflow boundaries and ownership | application/docs/ARCHITECTURE_INDEX.md |
| MASTER_FILE_INDEX.md | File-level inventory (138 Python files) | application/docs/MASTER_FILE_INDEX.md |
| MASTER_WORKFLOWS_INDEX.md | Workflow data flows and integration patterns | application/docs/MASTER_WORKFLOWS_INDEX.md |
| CONTEXT_INDEX.md | Feature-to-file mapping | application/docs/CONTEXT_INDEX.md |
| DEFINITION_OF_DONE.md | Quality assurance checklist | application/docs/DEFINITION_OF_DONE.md |
| rules-&-parameters.md | Technical specifications | application/docs/rules-&-parameters.md |
| MASTER_ETSY_DESCRIPTION_ENGINE.md | Etsy copywriting protocol | application/analysis/instructions/ |
| Upload-Workflow-Report.md | Upload workflow deep-dive (801 lines) | application/workflows/ |
| Analysis-Workflow-Report.md | Analysis workflow deep-dive (1,411 lines) | application/workflows/ |
| Mockup-management-Workflow-report | Mockup workflow deep-dive (1,230 lines) | application/workflows/ |
| Detail-Closeup-Workflow-Report.md | Detail closeup workflow (1,333 lines) | application/workflows/ |
| Export-Workflow-Report.md | Export workflow (1,015 lines) | application/workflows/ |
| Video-Generation-Workflow-Report | Video generation workflow (788 lines) | application/workflows/ |

---

## ✅ SYSTEM MAP STATUS

**Date:** February 15, 2026
**Status:** ✅ **CONSOLIDATED & VALIDATED**
**Coverage:** 4-layer architecture, all workflows documented, data flows mapped
**Next Steps:** Update `.copilotrules` with CONTEXT INJECTION PROTOCOL

---

## END OF SYSTEM MAP
