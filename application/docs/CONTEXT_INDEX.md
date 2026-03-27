# ArtLomo Context Index: Feature-to-File Map

This index provides a direct mapping of application features to their respective source files to streamline development and troubleshooting.

## March 19, 2026 Context Update

- **Gemini 3 Image Generation Migration:**

  - Service file: `application/mockups/services/gemini_service.py` (completely rewritten with system instruction architecture)

  - Database model: `GeminiStudioJob` in `db.py` (added March 19)

  - Celery task: `tasks_mockup_generator.process_gemini_studio_job` (full lifecycle queue processing)

  - Admin routes: `application/mockups/admin/routes/mockup_admin_routes.py` (Studio queue UI with form, cards, carousel, delete, add-to-library)

  - Frontend UI: `application/mockups/admin/ui/templates/mockups/gemini_studio.html`, `application/mockups/admin/ui/static/js/gemini_studio.js`, `application/mockups/admin/ui/static/css/gemini_studio.css`

  - Configuration: `.env` has 4 new variables for model IDs, thinking level, output size

  - Comprehensive guide: `application/changelog-reports/GEMINI_3_MIGRATION_19MAR2026.md`

## March 7, 2026 Context Updates

- Operational inventory tooling:

  - `application/tools/app-stacks/files/system-inventory.sh`

  - `application/tools/app-stacks/files/tools.sh` (`sysinfo`, `all` integration)

- New dated reference documents:

  - `application/docs/ARTLOMO_OVERVIEW_2026-03-07.md`

  - `application/docs/ARTLOMO_SYSTEM_SOFTWARE_REPORT_2026-03-07.md`

  - `application/docs/GOOGLE_CLOUD_VM_SPECS_REPORT_2026-03-07.md`

  - `application/docs/TOOLS_SH_COVERAGE_REPORT_2026-03-07.md`

## March 9, 2026 Context Updates

- Added curated AI handoff command:

  - `./application/tools/app-stacks/files/tools.sh` with command `gemini`

- Preferred external AI handoff output:

  - `application/tools/app-stacks/stacks/application-gemini-code-stack-<TIMESTAMP>.md`

- Stack collection now excludes nested dependency/cache folders and excludes `.env` by default.

**📚 For comprehensive workflow documentation**:

- Complete Detail Closeup Generator system handoff: [application/docs/closeup-detail-generator.md](./closeup-detail-generator.md) (1,261 lines, Feb 17, 2026)

- 6 detailed workflow reports in [application/workflows/](../../workflows/) covering Upload, Analysis, Mockup, Export, and Video Generation with code examples and data flows

## 1. Image Processing & Asset Generation

- **Core Generation Logic:** `application/common/utilities/images.py`

- **Detail Closeup Service:** `application/artwork/services/detail_closeup_service.py`

- **Detail Closeup Complete Reference:** [application/docs/closeup-detail-generator.md](./closeup-detail-generator.md) (comprehensive system handoff)

- **Configuration Constants:** `application/config.py` (Refer to `ANALYSE_LONG_EDGE`)

## 2. Mockup & Composite Pipeline

- **Mockup Generation:** `application/mockups/pipeline.py`

- **Compositing Engine:** `application/mockups/compositor.py`

- **Coordinate & Transform Logic:** `application/mockups/transforms.py`

- **Base Catalog Source:** `application/mockups/catalog/assets/mockups/bases/`

- **Output Directory:** `application/lab/processed/<slug>/mockups/`

- **🆕 Gemini 3 Image Generation Service (March 19, 2026):**

  - **File:** `application/mockups/services/gemini_service.py`

  - **Status:** Production-active with system instruction architecture

  - **Models:** `gemini-3.1-flash-image-preview` (generation), `gemini-3-pro-image-preview` (edit)

  - **Features:** Thinking mode enabled, immutable artwork guardrail, camera/perspective guidance

  - **Migration Details:** `application/changelog-reports/GEMINI_3_MIGRATION_19MAR2026.md`

- **🆕 Studio Queue System (March 19, 2026):**

  - **Celery Task:** `tasks_mockup_generator.process_gemini_studio_job`

  - **Database Model:** `GeminiStudioJob` in `db.py`

  - **Admin UI:** `admin/mockups/routes.py` (gemini_studio GET/POST routes)

  - **Frontend:** `admin/mockups/templates/gemini_studio.html`

## 3. UI, Carousel & Workspace (Clean-Room v2.0)

- **Analysis Workspace Template:** `application/common/ui/templates/analysis_workspace.html`

  - Unified Action Bar (sticky): Save Changes, Lock, Re-Analyse, Export, Delete

  - Media Preview Row: Artwork + Closeup side-by-side (max 500px each)

  - Generate Video panel: Dedicated button with clear label

  - Mockup Panel: Category selector, SWAP buttons, delete controls

  - Delete Modal: Requires typed "DELETE" confirmation

- **Carousel Script:** `application/common/ui/static/js/mockup_carousel.js`

- **Manual Workspace UI:** `application/common/ui/templates/analysis_workspace.html`

- **Workspace Logic:** `application/common/ui/static/js/analysis_workspace.js`

- **Global Styles:** `application/common/ui/static/css/darkroom.css`

## 4. Video & Kinematic Preview

- **Video Generation Service:** `application/video/services/video_service.py`

- **Kinematic Logic (FFMPEG):** `application/video/services/video_service.py`

- **Metadata Storage:** `application/lab/processed/<slug>/coordinates.json`

## 5. System State & Data

- **Database File:** `var/db/artlomo.db`

- **Session Registry:** `var/state/session_registry.json`

- **Logs:** `/srv/artlomo/logs/` (Mapped via `LOG_CONFIG` in `config.py`)
