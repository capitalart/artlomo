# ArtLomo: Definition of Done (DoD)

A task is not considered "Complete" until it satisfies the following criteria:

**📚 For workflow-specific completion criteria**, see the comprehensive reports in [application/workflows/](../../workflows/) including error handling, logging patterns, and integration points.

## 1. Asset & Resolution Standards

- [ ] **High-Res Check**: All processed images (ANALYSE, MOCKUP, DETAIL) have a long edge of exactly 2048px.

- [ ] **Thumbnail Check**: All thumbnails are center-cropped at 500x500px.

- [ ] **Format Check**: Images are saved as Progressive JPEGs with a quality setting of 85.

## 2. Metadata & Data Integrity

- [ ] **Coordinate Sync**: Every mockup composite has a companion `.json` file containing normalized (0.0 - 1.0) artwork coordinates.

- [ ] **Registry Update**: The `artworks.json` or SQLite database reflects the latest file paths and timestamps.

## 3. UI & Frontend Compliance (Clean-Room v2.0)

- [ ] **Action Bar Check**: Unified sticky action bar is present at top of right pane with exactly 5 buttons (Save Changes, Lock, Re-Analyse, Export, Delete).

- [ ] **Linear Workflow**: User progression is clear—no button clutter, only actions relevant to current task are visible.

- [ ] **Media Panel Layout**: Artwork + Closeup displayed side-by-side (centered, max 500px each), with dashed placeholder if no closeup exists.

- [ ] **Delete Modal Check**: Delete button triggers modal requiring user to type "DELETE" before confirmation button activates.

- [ ] **Re-Analyse Context-Aware**: Re-Analyse button detects `analysis_source` and routes to same provider (no manual AI switching).

- [ ] **Dark Mode Compliance**: All labels/inputs use `var(--text-primary)` or `var(--text-secondary)`, zero white-on-white text.

- [ ] **Glass Morphism Action Bar**: Action bar features `backdrop-filter: blur(10px)` and subtle box-shadow.

- [ ] **Modal Safety**: The overlay modal is appended to the root of `document.body` (no transform nesting).

## 4. Stability & Logging

- [ ] **Error Handling**: FFMPEG failures or image processing errors are caught and return a 400/500 API response.

- [ ] **Log Entry**: A success or failure entry has been written to the appropriate log file in `/srv/artlomo/logs/`.

- [ ] **Cleanup**: Temporary files used during video or image processing have been deleted.

## 5. Documentation & Operational Visibility

- [ ] **Changelog Entry**: Root `CHANGELOG.md` reflects significant shipped changes.

- [ ] **Architecture Sync**: `ARCHITECTURE_INDEX.md`, `SYSTEM_MAP.md`, and `MASTER_FILE_INDEX.md` are updated when ownership/responsibility changes.

- [ ] **Inventory Coverage**: For infrastructure/runtime changes, `tools.sh sysinfo` output is regenerated and reviewed.
