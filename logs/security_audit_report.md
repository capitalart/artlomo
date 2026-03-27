# Security Audit Report (Legend Directive)

Generated: 2026-01-22

## Critical

### Open Redirect via `next=` parameter
- **Path**: `application/routes/auth_routes.py`
- **Lines**: 65-75, 150-171, 189-196
- **Issue**: Unvalidated `next` could redirect to attacker-controlled URLs.
- **Fix**: Implemented `_safe_next_url()` and applied it to admin + viewer login and logout redirects.

- **Path**: `application/app.py`
- **Lines**: 181-193
- **Issue**: `/login` and `/logout` aliases forwarded `next` without validation.
- **Fix**: Sanitized `next` before passing into `url_for()`.

### CSRF gaps on mutating endpoints
- **Path**: `application/routes/auth_routes.py`
- **Lines**: 93-99
- **Issue**: Login POST accepted credentials without CSRF.
- **Fix**: Enforced `require_csrf_or_400()` for login POST and added `csrf_token` hidden field in `application/common/ui/templates/auth/login.html`.

- **Path**: `application/upload/routes/upload_routes.py`
- **Lines**: 34-52
- **Issue**: Upload POST (`/artworks/upload`) is mutating and required CSRF.
- **Fix**: Enforced `require_csrf_or_400()` early (JSON-safe error for XHR).

- **Path**: `application/analysis/manual/routes/manual_routes.py`
- **Lines**: 33-47, 98-124
- **Issue**: Manual workflow state changes (promotion, metadata save) needed CSRF.
- **Fix**: 
  - Moved state-changing `/manual/process/<slug>` to POST-only.
  - Added CSRF enforcement on `/manual/process/<slug>` POST and `/manual/workspace/<slug>` POST.
  - Updated UI links to POST forms with CSRF.

- **Path**: `application/mockups/admin/routes/mockup_admin_routes.py`
- **Lines**: 535-705 (multiple endpoints)
- **Issue**: Several POST JSON endpoints were missing CSRF checks.
- **Fix**: Added `require_csrf_or_400()` to batch + per-base mutation endpoints and to base upload POST.

- **Paths (templates)**:
  - `application/analysis/manual/ui/templates/manual_workspace.html`
  - `application/common/ui/templates/mockups/upload_bases.html`
  - `application/common/ui/templates/mockups/upload_template.html`
  - `application/mockups/admin/ui/templates/mockups/upload_bases.html`
  - `application/mockups/admin/ui/templates/mockups/upload_template.html`
  - `application/common/ui/templates/artworks/unprocessed.html`
  - `application/artwork/ui/templates/artwork_analysis.html`
  - `application/common/ui/templates/mockups/categories.html`
  - `application/common/ui/templates/mockups/policy.html`
  - `application/mockups/admin/ui/templates/mockups/categories.html`
  - `application/mockups/admin/ui/templates/mockups/policy.html`
- **Issue**: POST forms missing CSRF token.
- **Fix**: Added hidden `csrf_token` fields.

## Warnings

### Path traversal risk via unsanitized `slug` path params
- **Paths**:
  - `application/upload/routes/upload_routes.py`
  - `application/mockups/routes/mockup_routes.py`
  - `application/analysis/manual/services/manual_service.py`
- **Issue**: Building filesystem paths from user-controlled `slug` could allow traversal (`../`).
- **Fix**:
  - Added `slug_sku.is_safe_slug()` and enforced it in upload + mockup routes.
  - Enforced strict slug validation in manual service `_require_slug()`.

### Secrets in `.env`
- **Path**: `.env`
- **Issue**: Real API keys/passwords exist in `.env` on disk.
- **Status**: `.env` is ignored in `.gitignore`.
- **Recommendation**:
  - Ensure `.env` is never copied into repositories/backups that are shared.
  - Rotate exposed keys if this file has ever been committed or shared.

## Informational (no issues found)

### Shell execution / code injection
- **Searched**: `os.system`, `subprocess.*(shell=True)`, `eval`, `exec`
- **Result**: No matches in application code.

### Unsafe serialization
- **Searched**: `pickle`, unsafe `yaml.load`
- **Result**: No matches in application code.

### Raw SQL string formatting
- **Searched**: `text()`, `.execute()`, and common raw SQL patterns
- **Result**: No matches in application code.

### XSS (`|safe`)
- **Searched**: `|safe`, `Markup(`
- **Result**: No matches in templates/application code.

### Dependencies
- **File**: `requirements.txt`
- **Notes**: Flask/Werkzeug/Jinja2/itsdangerous are pinned and appear modern.
- **Recommendation**: Run a periodic dependency vulnerability scan (pip-audit) in CI.
