# ArtLomo Application Audit

**Date:** March 7, 2026
**Scope:** Comprehensive audit of `application/` directory including Detail Closeup System v2.1 Verification and documentation tooling synchronization
**Sources:** README.md, ARCHITECTURE_INDEX.md, MASTER_FILE_INDEX.md, closeup-detail-generator.md

## New Documentation & Tooling Updates (March 7, 2026)

- Added system environment inventory generator:

  - `application/tools/app-stacks/files/system-inventory.sh`

- Updated orchestration tooling:

  - `application/tools/app-stacks/files/tools.sh` now supports `sysinfo` and includes it in `all`

- Added dated documentation set in `application/docs/`:

  - `ARTLOMO_OVERVIEW_2026-03-07.md`

  - `ARTLOMO_SYSTEM_SOFTWARE_REPORT_2026-03-07.md`

  - `GOOGLE_CLOUD_VM_SPECS_REPORT_2026-03-07.md`

  - `TOOLS_SH_COVERAGE_REPORT_2026-03-07.md`

These updates close prior visibility gaps by capturing runtime, infrastructure, and service-state details alongside source-level documentation.

## New Documentation (Feb 17, 2026)

- Complete Detail Closeup Generator handoff: 1,261 lines (application/docs/closeup-detail-generator.md)

- Mathematical audit: 445 lines (DETAIL_CLOSEUP_MATH_AUDIT_17-FEB-2026.md)

- Cache busting verification: 400 lines (CACHE_BUSTING_VERIFICATION_17-FEB-2026.md)

- Plus 6 comprehensive workflow reports in `application/workflows/` (6,578 total lines, 0 linting errors)

**See:** [MASTER_WORKFLOWS_INDEX.md](MASTER_WORKFLOWS_INDEX.md#-comprehensive-workflow-reports) for complete reference.

---

## Recent Updates (February 20, 2026)

### Emergency UI Correction — Mockup Base Control Stacking

- **File:** `application/mockups/admin/ui/templates/mockups/bases.html`

- **Grid enforcement:** Maintains strict 6-across at XL via `row-cols-xl-6`.

- **Card control contract:** Updated to an absolute vertical stack with only one horizontal row allowed (final Preview/Delete row).

- **Control sequence now enforced per card:**

  1. `CATEGORY` label + full-width selector + full-width `MOVE TO CATEGORY`

  1. `ASPECT RATIO` label + full-width selector + full-width `OVERRIDE ASPECT`

  1. `<hr class="my-4">`

  1. Full-width emphasized `REGENERATE COORDINATES`

  1. Final `d-flex gap-2 mt-2` row for `PREVIEW` and `DELETE`

### CSS Safety Net — Vertical Button Forcing

- **File:** `application/mockups/admin/ui/static/css/mockups_admin.css`

- Added hard fallback to force button stack even if future HTML drifts:

  - `.mockup-card .btn { display:block; width:100%; margin-bottom:10px; padding:10px; }`

  - Final preview/delete row keeps zero bottom margin override.

### Director's Suite Layout Consistency

- **File:** `application/common/ui/templates/video_workspace.html`

- Storyboard panel remains under the video player inside the left column.

- Storyboard cards use compact analysis-style class pattern and now enforce fixed 120px card width for uniformity.

- Right column (`.suite-right`) is sticky (`position: sticky; top: 10px`) for always-accessible controls while left content scrolls.

### Sharp Migration Confirmation (Targeted Workflows)

- `application/utils/image_utils.py` routes upload thumbnail and SEO master generation through Node/Sharp bridge actions.

- `application/mockups/admin/services.py` routes thumb generation through Node/Sharp and preserves 4px coordinate bleed (`COORDINATE_BLEED_PX = 4`).

- Auxiliary cleanup removed legacy PIL imports from:

  - `application/app.py`

  - `application/mockups/admin/routes/mockup_admin_routes.py`

  - `application/tools/video/service.py`

  - `application/mockups/routes/mockup_routes.py`

---

## 1. Architectural Rules (Mandatory)

### 1.1 Core Invariants (from README.md & ARCHITECTURE_INDEX.md)

| Rule | Description | Status |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| **Artwork Single-State Invariant** | A slug exists in only one of `lab/unprocessed/<slug>/`, `lab/processed/<slug>/`, or `lab/locked/<slug>/` at any time. Promotions are moves, never copies. Reanalysis edits in place. | ✅ Enforced |
| **Delete Ownership** | Each workflow owns its delete UX; no global delete handlers outside scope. | ✅ Compliant |
| **No Global UI Handlers** | Global handlers require explicit scoping/guards. | ✅ Compliant |
| **Workflow Isolation** | Workflows may only depend on `application/common`, `application/utils`, and shared configuration. No cross-workflow imports. | ✅ Generally compliant |
| **Business Logic in Services** | Routes orchestrate only; UI contains no business logic. | ✅ Compliant |

### 1.2 Folder Responsibilities (Verified)

- **admin** — Hub, theme/style editor, profile, users, settings, analysis preset management

- **upload** — Ingest, QC, storage, thumbnails, status polling

- **artwork** — Routes, index, processing, detail closeup, admin export

- **analysis** — AI (Gemini/OpenAI), manual workspace, API routes, preset service

- **mockups** — Catalog, selection, pipeline, compositor, admin bases

- **manual** — Manual analysis workspace (routes under `/manual`)

- **export** — Export bundles and API

- **lab** — Data only (no runtime code)

- **common** — Shared UI, templates, static assets

- **utils** — Low-level cross-cutting helpers

### 1.3 Memory Safety & Resource Management (New — February 15, 2026)

**Objective:** Prevent OOM (Out of Memory) kills on 2-CPU VMs with limited RAM (7.8GiB).

#### Implementation Details

| Component | Change | Location |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **Sequential Upload Processing** | Added `threading.Lock()` to ensure only one artwork is processed at a time. Prevents concurrent image processing from exhausting memory. | `application/upload/routes/upload_routes.py:32` |
| **Memory Logging (Pre-Stage 8)** | Log available RAM before DERIVATIVES stage: `[MEMORY] Available RAM: {MB:.2f} MB, Stage: DERIVATIVES, Slug: {slug}` | `application/upload/routes/upload_routes.py:119` |
| **Explicit Buffer Cleanup (Post-Stage 8)** | Delete large byte arrays after Stage 8 (DERIVATIVES): `del analyse_bytes`, `del thumb_bytes`. Then call `images.cleanup_memory()` (gc.collect). | `application/upload/routes/upload_routes.py:137` |
| **Final Cleanup** | Delete remaining buffers (`file_bytes`, `analyse_qc`) after metadata write, before finalization. Call `gc.collect()` a second time. | `application/upload/routes/upload_routes.py:158` |
| **Garbage Collection Function** | Added `cleanup_memory()` in `application/common/utilities/images.py` — explicit `gc.collect()` for high-memory stages. | `application/common/utilities/images.py:159` |
| **PIL Context Managers** | All image operations use `with Image.open(...) as img:` for immediate file handle closure. No leaked image objects. | `application/common/utilities/images.py` (all) |

#### Rationale

- **Lock Ensures Serialization:** Flask can handle concurrent requests; without the lock, multiple uploads could compete for memory simultaneously.

- **Memory Logging:** Provides telemetry to diagnose OOM conditions; `psutil.virtual_memory().available` shows free RAM at critical stages.

- **Explicit Deletions:** Python's garbage collector is non-deterministic; large PIL/cv2/numpy buffers may persist in memory even after function returns. Force deletion ensures immediate release.

- **gc.collect() Calls:** Explicitly trigger CPython garbage collection to reclaim cycles and move freed objects to the system.

#### Testing & Validation

- Verified lock is acquired before processing and released in finally block (even on exception).

- Confirmed all `Image.open()` calls use context managers (no resource leaks).

- Tested deletion sequence: buffers deleted only after all usages complete.

- Memory logging compatible with existing logging infrastructure (`_logger.info()`).

### 1.4 UI/UX Updates (February 16, 2026)

#### High-Visibility Red Cross Selection (Gallery Checkboxes)

**Objective:** Improve artwork selection visibility with bold red cross indicator replacing subtle teal background.

## Implementation

| Component | Change | Location |
| ------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------- |
| **Checkbox Size** | Increased from 20px to 24px for better visibility and touch targets | `application/common/ui/static/css/gallery.css:208` |
| **Selection Indicator** | Bold red cross (✕) using `::after` pseudo-element with `#ff4444` color | `application/common/ui/static/css/gallery.css:231` |
| **Text Shadow** | Added `text-shadow: 0 0 3px rgba(0,0,0,0.8)` for visibility on both light/dark backgrounds | `application/common/ui/static/css/gallery.css:240` |
| **Card Border Highlight** | 2px red outline on card when checkbox is checked using `:has()` selector | `application/common/ui/static/css/gallery.css:245` |
| **Positioning** | Updated `.card-select` to use flex layout for proper centering | `application/common/ui/static/css/gallery.css:197` |

Rationale

- **High Contrast:** Red cross (`#ff4444`) is more visible than teal background (`#00bcd4`) across all themes

- **Clear Intent:** Cross symbol universally recognized for selection/marking

- **Accessibility:** Larger checkbox (24px vs 20px) improves touch/click targets

- **Dark Mode Safe:** Text shadow ensures visibility on both light and dark backgrounds

- **Visual Feedback:** Card outline provides secondary confirmation of selection state

## Files Modified

- `application/common/ui/static/css/gallery.css` (lines 197-248)

## Templates Using This Component

- `application/common/ui/templates/artworks/unprocessed.html`

- `application/common/ui/templates/artworks/processed.html`

- `application/common/ui/templates/artworks/trash.html`

- `application/common/ui/templates/artworks/locked.html`

### High-Contrast Light Mode UI Hardening (February 16, 2026)

**Objective:** Improve border visibility and card definition in light theme for high-resolution displays.

**New CSS File Created:** `application/common/ui/static/css/darkroom.css`

Implementation

| Component | Change | Location |
| ------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **CSS Variables - Light Theme** | Increased `--color-border-subtle` from `rgba(0,0,0,0.1)` to `rgba(0,0,0,0.2)` (2x visibility) | `application/common/ui/static/css/darkroom.css:9` |
| **Card Shadow Variable** | Added `--color-card-shadow: 0 4px 12px rgba(0,0,0,0.08)` for consistent depth | `application/common/ui/static/css/darkroom.css:11` |
| **Checkbox Border** | Added `--checkbox-border: #333333` for darker checkbox borders in light mode | `application/common/ui/static/css/darkroom.css:12` |
| **Gallery Card Borders** | Updated `.gallery-card` to use `var(--color-border-subtle)` and `var(--color-card-shadow)` variables | `application/common/ui/static/css/gallery.css:141` |
| **Card Hover Enhancement** | Added shadow transition: `0 8px 24px rgba(0,0,0,0.12)` on hover (3x depth) | `application/common/ui/static/css/gallery.css:150` |
| **Checkbox Visibility** | Updated checkbox background from `rgba(0,0,0,0.6)` to `rgba(255,255,255,0.9)` in light mode | `application/common/ui/static/css/gallery.css:213` |
| **Base Template Integration** | Linked `darkroom.css` between `base.css` and `admin.css` in stylesheet cascade | `application/common/ui/templates/base.html:22` |

Rationale

- **Enhanced Visibility:** 2x border opacity ensures card boundaries are clear on high-DPI displays

- **Professional Depth:** Shadow variable provides consistent "lift" effect across all card components

- **Theme Safety:** Dark mode remains subtle with `rgba(255,255,255,0.1)` borders (unchanged)

- **Centralized Control:** CSS variables enable theme-wide consistency and easy adjustments

Files Modified

- `application/common/ui/static/css/darkroom.css` (created, 25 lines)

- `application/common/ui/static/css/gallery.css` (lines 138-151, 208-227)

- `application/common/ui/templates/base.html` (line 22)

#### Carousel Visual Refactor — Minimalist Museum Style (February 16, 2026)

**Objective:** Transform image carousel from boxed layout to immersive museum-style viewing experience with professional navigation controls.

## Templates Modified

- `application/common/ui/templates/analysis_workspace.html` (Primary shared workspace template)

## Museum Layout Implementation

| Component | Specification | Location |
| ----------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **Backdrop Blur** | Enhanced from `rgba(0,0,0,0.95)` to `rgba(0,0,0,0.85)` with `backdrop-filter: blur(15px)` | Both `analysis_workspace.html` templates (~line 793) |
| **Container De-Boxing** | Removed all borders, backgrounds, and shadows from modal container for transparency | CSS inline styles (~line 793) |
| **Image Centering** | Set `max-height: 80vh` (reduced from 90vh) and removed all borders/rounded corners | CSS inline styles (~line 813) |
| **Cursor Affordance** | Set backdrop `cursor: pointer`, image `cursor: default` to indicate clickable areas | CSS inline styles (~line 806, 832) |

## Pro High-Contrast Navigation

| Component | Specification | Location |
| -------------------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **Circular Glass Buttons** | 60px diameter circles with `rgba(0,0,0,0.4)` background and `backdrop-filter: blur(5px)` | CSS inline styles (~line 836) |
| **Size & Visibility** | Increased from previous rectangular design; font-size 28px for arrow glyphs (`&lsaquo;`/`&rsaquo;`) | CSS inline styles (~line 848) |
| **Glass Morphism** | 1px white border `rgba(255,255,255,0.2)` with subtle blur creates depth | CSS inline styles (~line 843) |
| **Hover Transformation** | Inverts to white background `rgba(255,255,255,0.9)` with black text, scales to 1.15x | CSS inline styles (~line 853) |
| **Shadow Enhancement** | Adds `box-shadow: 0 0 20px rgba(0,0,0,0.3)` on hover for dramatic lift | CSS inline styles (~line 856) |
| **Smooth Easing** | Uses `cubic-bezier(0.4, 0, 0.2, 1)` for professional animation curve | CSS inline styles (~line 851) |
| **Z-Index Layering** | Set to 10050 (above backdrop 10000, below close button 10100) | CSS inline styles (~line 850) |
| **Positioning** | Left button at 30px from edge, right button at 30px (increased spacing from 20px) | CSS inline styles (~line 858, 861) |

## High-Visibility Close Button

| Component | Specification | Location |
| --------------------- | ------------------------------------------------------------------------------------- | --------------------------------- |
| **Red Pill Design** | `rgba(255, 44, 44, 0.9)` background with 50px border-radius | CSS inline styles (~line 866) |
| **Dual Label** | `::before` pseudo-element "✕" (20px) + `::after` "CLOSE" text (14px, font-weight 900) | CSS inline styles (~line 884-892) |
| **Fixed Positioning** | Changed from `absolute` to `fixed` at top: 30px, right: 40px | CSS inline styles (~line 866-868) |
| **Hover Scale** | Scales to 1.1x and brightens to `#ff0000` on hover | CSS inline styles (~line 879-882) |
| **Z-Index Priority** | Set to 10100 (highest layer, above all carousel content) | CSS inline styles (~line 873) |
| **Shadow Depth** | `box-shadow: 0 4px 15px rgba(0,0,0,0.4)` for prominence | CSS inline styles (~line 876) |
| **Text Hiding** | `font-size: 0` hides HTML text content, pseudo-elements provide visible labels | CSS inline styles (~line 877) |

## Click-Outside-to-Close Functionality

| Component | Implementation | Location |
| -------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------- |
| **Backdrop Click Handler** | New `handleBackdropClick(event)` function checks `event.target.id` matches modal backdrop | JavaScript inline (~line 1020) |
| **Modal Click Attribute** | Added `onclick="handleBackdropClick(event)"` to modal backdrop div | HTML template (~line 347) |
| **Navigation Protection** | Nav buttons use `event.stopPropagation()` to prevent accidental carousel closure | HTML template (~line 349, 351) |
| **Image Protection** | Image element uses `event.stopPropagation()` to prevent clicks from bubbling to backdrop | HTML template (~line 350) |
| **Keyboard Navigation** | Escape key and arrow keys still functional (existing behavior preserved) | JavaScript inline (existing code) |

## Behavioral Changes

- **Before:** Only Escape key or explicit close button dismissed carousel

- **After:** Clicking blurry black backdrop area (left/right of image) instantly closes carousel

- **Protected:** Clicking navigation arrows or image itself does NOT close carousel

- **Enhanced UX:** Intuitive dismissal matches modern gallery patterns (Lightbox, PhotoSwipe)

## Visual Impact

- **Museum Clean:** No borders, no containers—image floats in space against blurred background

- **Pro Navigation:** Large circular buttons with glass effect are impossible to miss

- **Clear Hierarchy:** Red close button dominates top-right; white nav buttons flank image

- **Theme Compliance:** All colors use appropriate alpha channels for light/dark mode compatibility

Files Modified

- `application/common/ui/templates/analysis_workspace.html` (carousel and overlay styling sections)

- `application/common/ui/templates/analysis_workspace.html` (lines 347-355, 792-894, 997-1027)

Templates Using This Component

- Artwork analysis workspace (Gemini/OpenAI routes via `/artwork/<slug>/workspace`)

- Manual analysis workspace (via `/manual/workspace/<slug>`)

## Service Status

- ✅ Service restarted successfully February 16, 2026 at 10:23:06 ACDT

- ✅ Zero linting errors in modified templates

- ✅ Gunicorn workers: 4 active (PIDs: 6915, 6916, 6917, 6919)

---

## 2. Workflow Mapping (Current State)

### 2.1 Upload Workflow

| Stage | Route / Action | Status |
| ------------------- | ------------------------------------------------ | ---------------------------------- |
| Upload page | `GET /artworks/upload` | ✅ |
| Handle upload | `POST /artworks/upload` | ✅ |
| Unprocessed gallery | `GET /artworks/unprocessed` | ✅ |
| Per-slug view | `GET /artworks/unprocessed/<slug>` | ✅ |
| Custom input form | `GET /artworks/unprocessed/<slug>/custom-input` | ✅ |
| Seed context save | `POST /artworks/unprocessed/<slug>/seed-context` | ✅ |
| Status polling | `GET /artworks/<slug>/status` | ✅ |
| Processed gallery | `GET /artworks/processed` | ✅ |
| Locked gallery | `GET /artworks/locked` | ✅ |
| Delete unprocessed | `POST /artworks/unprocessed/<slug>/delete` | ✅ (with physical `shutil.rmtree`) |
| Delete processed | `POST /artworks/processed/<slug>/delete` | ✅ (with physical `shutil.rmtree`) |

### 2.2 Analysis Workflow

| Stage | Route / Action | Status |
| ----------------------- | ------------------------------------- | ------ |
| OpenAI analysis trigger | `POST /api/analysis/openai/<slug>` | ✅ |
| Gemini analysis trigger | `POST /api/analysis/gemini/<slug>` | ✅ |
| Analysis status | `GET /api/analysis/status/<slug>` | ✅ |
| OpenAI analysis page | `GET /artwork/<slug>/analysis/openai` | ✅ |
| Gemini analysis page | `GET /artwork/<slug>/analysis/gemini` | ✅ |
| Manual analysis page | `GET /artwork/<slug>/analysis/manual` | ✅ |
| Review (auto-resolve) | `GET /artwork/<slug>/review` | ✅ |
| OpenAI review | `GET /artwork/<slug>/review/openai` | ✅ |
| Gemini review | `GET /artwork/<slug>/review/gemini` | ✅ |
| Manual workspace | `GET /manual/workspace/<slug>` | ✅ |
| Manual workspace save | `POST /manual/workspace/<slug>/save` | ✅ |
| Manual workspace lock | `POST /manual/workspace/<slug>/lock` | ✅ |

### 2.3 Mockups Workflow

| Stage | Route / Action | Status |
| ---------------- | ---------------------------------------------- | ------ |
| Mockup bases | `GET /admin/mockups/bases` | ✅ |
| Upload bases | `GET /admin/mockups/bases/upload` | ✅ |
| Sanitize & sync | `POST /admin/mockups/bases/sanitize-sync` | ✅ |
| Generate mockups | `POST /artwork/<slug>/mockups/generate` | ✅ |
| Mockup thumb | `GET /artwork/<slug>/mockups/<slot>/thumb` | ✅ |
| Mockup composite | `GET /artwork/<slug>/mockups/<slot>/composite` | ✅ |
| Category change | `POST /artwork/<slug>/mockups/<slot>/category` | ✅ |
| Swap mockup | `POST /artwork/<slug>/mockups/<slot>/swap` | ✅ |

### 2.4 Manual Workspace Workflow

| Component | Location | Status |
| ------------------------ | --------------------------------------------- | ------ |
| Workspace template | `manual_workspace.html` | ✅ |
| Detail Closeup tile | Manual workspace (Create/Edit links) | ✅ |
| Save/Lock/Delete actions | Action grid | ✅ |
| Visual analysis fields | Editable (subject, dot_rhythm, palette, mood) | ✅ |
| Museum QC panel | Present | ✅ |
| Mockup grid | Category/swap controls | ✅ |

---

## 3. Dead Code & Deviations

### 3.1 No Legacy `/upload/gallery` Route

Per README and ARCHITECTURE_INDEX: "There is no `/upload/gallery`." Confirmed — no such route exists. All gallery pages use `/artworks/unprocessed`, `/artworks/processed`, `/artworks/locked`.

### 3.2 Video Generator — Implemented

**Status:** Video Generator service is implemented.

- **Service:** `application/tools/video/service.py`

- **Functionality:** Generates mp4 previews from master/analyse images.

- **Integration:** Used by `video_generate` route in `artwork_routes.py`.

---

## 4. Summary of Findings

### Compliant

- Artwork single-state invariant enforced

- Upload → Analysis → Processed → Review flow intact

- Physical folder deletion on delete (unprocessed/processed)

- Analysis loading overlay and polling infrastructure

- Dual Engine (Commercial/Collector) preset architecture

- Manual workspace layout aligned with artwork_analysis.html

- Visual analysis panel (editable) in both review and manual workspace

- CSRF protection on mutating endpoints

- Slug validation via `is_safe_slug()`

- Detail Closeup tile present in `artwork_analysis.html` (verified)

- Documentation paths aligned (MASTER_FILE_INDEX.md)

### Deviations Requiring Attention

_None identified._

---

## 5. Recent Architecture Updates (Completed)

### 5.1 Master File Standardization

- **Rule:** All master files must use `-MASTER.jpg` suffix.

- **Constraint:** .jpg only (no .png) to meet Etsy 20MB limit.

- **Legacy Support:** `DetailCloseupService` and `ProcessingService` handle legacy `[slug].jpg` files by renaming or fallback.

### 5.2 SEO Renaming & Locking

- **Workflow:** When an artwork is locked (`POST /<slug>/lock`), the master file is renamed to the SEO-optimized filename from `listing.json`.

- **Double Extension Fix:** Logic added to prevent `.jpg.jpg` errors in SEO filename generation.

- **Detail Closeup:** `DetailCloseupService` searches for master files in order: `[slug]-MASTER.jpg` → `seo_filename` → `[slug].jpg`.

### 5.3 Detail Closeup Editor Polish

- **Zoom & Quality:** Increased max zoom to 600% and proxy generation to 7000px long edge.

- **Theme Compatibility:** Fixed UI color clashes for light/dark themes using CSS variables.

- **Loading Overlay:** Added animated `arrows-clockwise-dark.svg` overlay during image preparation.

- **Integration:** Added Detail Closeup tile to `artwork_analysis.html`.

### 5.4 Navigation & Branding

- **Breadcrumbs:** Replaced "Dashboard" header with breadcrumb navigation (Dashboard / [Page Title]).

- **Links:** Logo and Dashboard breadcrumb now link to `<https://artlomo.com/`.>

### 5.5 Analysis Overlay Animation

- **Visuals:** Updated OpenAI/Gemini analysis overlay to use animated `arrows-clockwise-dark.svg` icon.

---

## 6. Clean-Room Workspace Refactor Audit (February 14, 2026)

### 6.1 Unified Action Bar Implementation

| Component | Specification | Status |
| ---------------------- | -------------------------------------------------------------- | -------------- |
| **Action Bar Buttons** | Exactly 5 buttons (Save, Lock, Re-Analyse, Export, Delete) | ✅ Compliant |
| **Save Changes** | `btn-primary`, POST `/artwork/{slug}/save` | ✅ Implemented |
| **Lock** | `btn-success` (green), POST `/artwork/{slug}/lock` | ✅ Implemented |
| **Re-Analyse** | `btn-outline-secondary`, context-aware (detects `data-source`) | ✅ Implemented |
| **Export** | `btn-outline-secondary`, Etsy only, no multi-provider clutter | ✅ Implemented |
| **Delete** | `btn-danger`, triggers modal with typed "DELETE" confirmation | ✅ Implemented |
| **Sticky Positioning** | `position: sticky; top: 10px; z-index: 100` | ✅ Compliant |
| **Glass Morphism** | `backdrop-filter: blur(10px)` on action bar | ✅ Compliant |

### 6.2 Media Panel & Dark Mode

| Component | Specification | Status |
| ---------------------- | ---------------------------------------------------------------------- | -------------- |
| **Text Colors** | All labels/inputs use `var(--text-primary)` or `var(--text-secondary)` | ✅ Compliant |
| **White-on-White** | Zero instances in action bar, forms, or modals | ✅ Compliant |
| **Preview Row Layout** | Artwork + Closeup side-by-side (max 500px each) | ✅ Implemented |
| **SWAP Buttons** | arrows-clockwise icon, regenerates with spinner | ✅ Implemented |

### 6.3 Delete Modal & Closeup Proxy

| Item | Specification | Status |
| -------------------- | ----------------------------------------------------------- | -------------- |
| **Modal Trigger** | Delete button opens modal with input field | ✅ Implemented |
| **Input Validation** | Requires exact text "DELETE" before confirmation | ✅ Implemented |
| **Closeup Proxy** | 7200px long edge @ 90% quality (auto-generated) | ✅ Verified |
| **Backend Service** | `detail_closeup_service.py` with `ensure_proxy_available()` | ✅ Verified |

### 6.4 Deployment Status

| Check | Result |
| ------------------------ | ------------------------------------ |
| **Service Restart** | ✅ Successful (Feb 14 20:14 ACDT) |
| **Template Rendering** | ✅ No errors in logs |
| **Dark Mode Compliance** | ✅ All CSS variables properly scoped |
| **Responsive Layout** | ✅ 45/55 grid works below 1200px |

---

## Recent Updates (Completed)

- **`artwork_analysis.html` JavaScript Refactor**: Modified JavaScript in `artwork_analysis.html` to introduce temporary variables for `querySelectorAll` results on lines 547 and 917. This change is a workaround for a linter issue reporting "Expression expected." errors, without altering the core functionality.

- **UI/Layout Restoration & Refinement**: Reverted broken UI changes and restored `manual_workspace.html`, `artwork_analysis.html`, and `edit_listing.css` from backups. Refined the 2-column 'Pro Layout' to use the correct variables and Blueprint names (e.g., `manual.static` for `url_for`). Fixed layout issues in `artwork_analysis.html` by applying the `.workspace-grid` class.

---

## Recent Updates (Pro Layout & UI Polish)

- **Pro Layout Implementation (2400px)**: Refactored `edit_listing.css`, `manual_workspace.html`, and `artwork_analysis.html` to implement the 2400px 2-column "Pro Layout".

- **Sticky Visuals & Reordering**: Reordered left column (Artwork → Video → Detail Closeup → Mockups) and right column (Control Panel → Metadata → Custom Input). Visuals are sticky.

- **Smart UI Features**: Added Title Word/Char counter, Universal Copy Buttons (📋) with feedback, and Unsaved Changes Protection (`isDirty` flag).

- **Universal Mockup Cards**: Upgraded mockup cards with a Swap button, Category Selector, and Loading state across AI and manual analysis pages.

- **Data Binding & New Fields**: Added backend support and UI fields for Materials Used, SEO Filename, Location, Sentiment, and Original Prompt. Data is persisted to `listing.json` and `seed_context.json`.

- **UI Enhancements**: Added live char/word counters for Title, help text for all fields, and one-click "Copy" buttons.

- **Detail Closeup Thumbnailing**: Backend now automatically generates 500x500px thumbnails for detail closeups.

- **Relaxed Pioneer Validation**: Modified Pioneer block validation to pad short responses with empty strings instead of crashing, ensuring UI stability even with incomplete AI outputs.

- **Manual Route Patch**: Secured mockup data retrieval in the manual workspace route to prevent 500 errors when mockup images are missing or keys are inconsistent.

---

## Recent Emergency Fixes (February 13, 2026)

- **Crash Fix: `common.static` BuildError**

  - Verified `application/common/**init**.py` exports `common_bp` via `from application.common.ui import common_bp`.

  - Ensured `application/app.py` imports and registers the Common blueprint so templates can safely call `url_for('common.static', ...)`.

- **AI Provider Default: OpenAI**

  - Set `DEFAULT_AI_PROVIDER = "openai"` in `application/config.py`.

  - Set `VISION_MODEL = "gpt-4o"` in `application/config.py`.

---

## 7. Archive & Historical Documentation (February 14, 2026)

### Purpose

The ArtLomo codebase is maturing, and implementation-specific documentation and work-in-progress notes are being consolidated and archived to maintain repository clarity and improve information discoverability.

### Archive Structure

**Location:** `/archived/` (root level)

## Subdirectories

- **migration-scripts/** — One-time database/asset migration utilities

  - patch_db.py (database schema migration)

  - sync_assets.py (asset directory synchronization)

  - test_gemini_key.py (Gemini API key validation)

- **work-notes/** — Development session notes with date prefixes

  - 2026-02-14-cline-work-01.txt (layout refactoring notes)

- **incidents/** — Past incident reports with date prefixes

  - 2026-02-05-INCIDENT_REPORT_502_FIX.md (502 error root cause and resolution)

- **implementation-history/** — Feature before/after/summary documentation (15+ files)

  - 2026-02-08-CSS_REFACTOR_SUMMARY.md

  - ANALYSIS*PRESET_MANAGEMENT*\*.md (3 files)

  - DETAIL*CLOSEUP*\*.md (2 files)

  - MANUAL*ANALYSIS*\*.md (3 files)

  - And others (see README.md Archive section for complete list)

### Consolidation Strategy

**Before:** 15+ documentation files dispersed at root level
**After:** All archived to `/archived/` with consolidated references in main docs

### Reference Integration

## Cross-References Added to

- **README.md** — "Archive & Historical Reference" section with guide to all categories

- **ARCHITECTURE_INDEX.md** — References to incident reports and historical context

- **MASTER_FILE_INDEX.md** — Consolidated feature entries with archive links

### Compliance & Access

✅ **All files retained:** No data loss; archived files remain accessible
✅ **Historical searchability:** Date-prefixed organization enables chronological searching
✅ **Documentation integrity:** Cross-links from main docs prevent lost references
✅ **Knowledge preservation:** Detailed implementation history secured for learning and auditing

### Date of Consolidation

**February 14, 2026** — Implementation history consolidation and archive restructuring complete.
