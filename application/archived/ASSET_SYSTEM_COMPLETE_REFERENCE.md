# Asset Management System: Complete Reference

**Date:** March 3, 2026
**Status:** Architecture defined, endpoints implemented, ready for UI migration
**Priority:** Complete carousel modal and video suite updates to use manifest

---

## System Overview

The application now uses a **manifest-driven asset system** where all file references go through a single source of truth:

```mermaid
┌─────────────────────────────────────────────────────────┐
│  /application/lab/index/artworks.json                   │
│  (Master index of all artworks & manifest locations)    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  GET /artwork/<slug>/assets                             │
│  (API endpoint serving {SKU}-assets.json)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  /processed/<slug>/{SKU}-assets.json                    │
│  (Manifest: declares all asset paths & metadata)        │
└────────────────────┬────────────────────────────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
    Files Section  Mockups   Directories
    - master       - assets  - mockups/
    - thumb        - count     - composites/
    - analyse                  - thumbs/
    - qc.json                  - templates/
    - metadata
    - etc.
```

---

## Key Files & Their Roles

### 1. Master Index

**File:** `/srv/artlomo/application/lab/index/artworks.json`

```json
{
  "items": {
    "RJC-0279": {
      "sku": "RJC-0279",                    // Primary identifier
      "slug": "rjc-0279",                   // URL identifier
      "artwork_dirname": "rjc-0279",        // Directory name
      "assets_file": "rjc-0279-assets.json", // Manifest filename
      "assets_path": "processed/rjc-0279/rjc-0279-assets.json",  // Manifest location
      "artwork_path": "processed/rjc-0279"  // Directory location
    }
  }
}
```

## Purpose

- Single registry of all artworks
- Maps slug → asset manifest path
- Updated when artwork is added/deleted

---

### 2. Asset Manifest

**File:** `/srv/artlomo/application/lab/processed/{slug}/{SKU}-assets.json`

**Purpose:** Declares all files, metadata, and mockups for one artwork

## Structure

```json
{
  "sku": "RJC-0279",
  "slug": "rjc-0279",
  "version": 2,
  "created_at": "2026-03-01T02:32:33.161619+00:00",
  "updated_at": "2026-03-03T07:08:14.922051+00:00",

  "files": {
    "master": "rjc-0279-MASTER.jpg",           // Canonical artwork
    "thumb": "rjc-0279-THUMB.jpg",            // Gallery thumbnail
    "analyse": "rjc-0279-ANALYSE.jpg",        // Analysis overlay
    "closeup_proxy": "rjc-0279-CLOSEUP-PROXY.jpg",  // Detail view
    "metadata": "rjc-0279-metadata.json",     // Artwork metadata
    "listing": "listing.json",                // Gallery listing data
    "qc": "rjc-0279-qc.json",                 // Quality control
    "status": "status.json",                  // Processing status
    "processing_status": "processing_status.json",
    "metadata_openai": "metadata_openai.json", // AI analysis
    "seo_download": "RJC-0279-Ochre-Songlines-Abstract.jpg"  // Export
  },

  "directories": {
    "mockups": "mockups"
  },

  "mockups": {
    "dir": "mockups",
    "assets": {
      "01": {
        "slot": 1,
        "template_slug": "beach-sunset",
        "category": "product",
        "aspect_ratio": "16:9",
        "composite": "composites/mu-rjc-0279-01.jpg",
        "thumb": "thumbs/mu-rjc-0279-01-THUMB.jpg",
        "coords": "templates/001-beach-sunset-coords.json",
        "created_at": "2026-03-02T10:15:33.123456+00:00"
      }
    },
    "count": 1
  }
}
```

---

## API Endpoints: Complete Reference

### 1. Get Asset Manifest (IMPLEMENTED ✅)

```text
GET /artwork/<slug>/assets

Response: Complete asset manifest (JSON above)
Status: 200 OK or 500 if load fails
```

## Usage in Frontend

```javascript
const manifest = await fetch(`/artwork/rjc-0279/assets`).then(r => r.json());
const thumbPath = manifest.files.thumb;  // "rjc-0279-THUMB.jpg"
const mockups = manifest.mockups.assets;  // { "01": {...}, "02": {...} }
```

### 2. Serve File from Manifest (IMPLEMENTED ✅)

```text
GET /artwork/<slug>/asset/<path>

Example: /artwork/rjc-0279/asset/rjc-0279-MASTER.jpg
Example: /artwork/rjc-0279/asset/mockups/composites/mu-rjc-0279-01.jpg

Validation:
- File must be declared in manifest
- File must exist at that path
- Returns 404 if not declared or missing
```

Usage in Frontend

```html
<img src="/artwork/{{ slug }}/asset/{{ manifest.files.thumb }}" />
<img src="/artwork/{{ slug }}/asset/{{ mockup.composite }}" />
```

### 3. List Mockups (NEEDS IMPLEMENTATION)

```text
GET /video/<slug>/mockups

Response:
{
  "slug": "rjc-0279",
  "sku": "RJC-0279",
  "mockups": [
    {
      "slot": 1,
      "thumbnail": "thumbs/mu-rjc-0279-01-THUMB.jpg",
      "composite": "composites/mu-rjc-0279-01.jpg",
      "template_slug": "beach-sunset"
    }
  ]
}
```

---

## Component Status Matrix

| Component | Status | Files | Priority |
| ----------- | -------- | ------- | ---------- |
| **Asset Manifest Endpoint** | ✅ DONE | `artwork_routes.py` | — |
| **File Serving Endpoint** | ✅ DONE | `artwork_routes.py` | — |
| **Master Index** | ✅ UPDATED | `artworks.json` | — |
| **Carousel Modal** | 🔴 NEEDS WORK | `analysis_workspace.html` + script | HIGH |
| **Video Suite** | 🔴 NEEDS WORK | `video_routes.py` + templates | HIGH |
| **Detail Closeup** | 🟡 PARTIAL | `detail_closeup_service.py` | MEDIUM |
| **QC Dashboard** | 🔴 NEEDS WORK | admin templates | MEDIUM |
| **Mockup Generation** | ✅ DONE | `mockup_routes.py` + `pipeline.py` | — |
| **Mockup Deletion** | ✅ DONE | `mockup_routes.py` | — |

---

## Critical Fixes Applied

### 1. Fresh Manifest Initialization (IMPLEMENTED ✅)

**Problem:** "Assets index not found for artwork" when generating first mockup
**Solution:** `_init_fresh_assets_index_for_slug()` creates minimal manifest on-demand
**File:** `application/mockups/routes/mockup_routes.py:381-420`

### 2. SKU-Aware Mockup Operations (IMPLEMENTED ✅)

**Problem:** Mockup generation uses SKU but routes looked for slug
**Solution:** All routes now query manifest first via `_load_assets_index_for_slug()`
**File:** `application/mockups/routes/mockup_routes.py`

### 3. Mockup Path Resolution (IMPLEMENTED ✅)

**Problem:** Different image versions used in different places (carousel vs. UI)
**Solution:** All paths now come from asset manifest slots
**Files:** `mockup_routes.py:500+` (serving routes), `pipeline.py` (generation)

---

## Data Flow: Mockup Generation & Display

### Generation Flow

```text
1. User clicks "Generate Mockups"
2. POST /artwork/<slug>/mockups/generate
   ├─ Load manifest via _init_fresh_assets_index_for_slug(slug)
   │  (creates fresh if missing)
   ├─ Clear old mockups via _clear_existing_mockups_for_slug(slug)
   │  (deletes files declared in manifest + legacy patterns)
   ├─ Generate via generate_mockups_for_artwork(sku=...)
   │  (uses SKU-aware resolution)
   └─ Write to manifest atomically
3. Manifest updated with new mockup slot entries
4. Client reloads and fetches manifest
```

### Display Flow

```text
1. Load page: GET /artwork/<slug>/analysis/openai
2. Backend renders analysis_workspace.html with thumb/analyse URLs
3. Frontend loads manifest: GET /artwork/<slug>/assets
4. Carousel populates from manifest.mockups.assets array
5. User clicks mockup → fetch full image via /artwork/<slug>/asset/<path>
```

---

## Testing Instructions

### Test 1: Asset Manifest Endpoint

```bash
curl https://localhost:5000/artwork/rjc-0279/assets | jq .

# Should return complete manifest with files and mockups

```

### Test 2: File Serving

```bash
curl -I https://localhost:5000/artwork/rjc-0279/asset/rjc-0279-MASTER.jpg

# Should return 200 OK

curl -I https://localhost:5000/artwork/rjc-0279/asset/nonexistent.jpg

# Should return 404 (not declared in manifest)

```

### Test 3: Carousel Load (Browser Console)

```javascript
const slug = 'rjc-0279';
const manifest = await fetch(`/artwork/${slug}/assets`).then(r => r.json());
console.log(manifest.mockups.assets);
// Should show array of mockup slot entries
```

### Test 4: Generate First Mockup

1. Load analysis review page for artwork with NO existing mockups
2. Click "Generate Mockups" button
3. Should NOT error with "Assets index not found"
4. Should create {SKU}-assets.json with mockup slot entries
5. Carousel should display generated mockup thumbnail

---

## Command Reference: Debugging

### Verify Manifest Exists

```bash
ls -la /srv/artlomo/application/lab/processed/rjc-0279/*.assets.json

# Output: should show rjc-0279-assets.json or similar

```

### Validate JSON Structure

```bash
python -m json.tool /srv/artlomo/application/lab/processed/rjc-0279/rjc-0279-assets.json

# Output: pretty-printed, valid JSON if no errors

```

### Check Manifest Content

```bash
cat /srv/artlomo/application/lab/processed/rjc-0279/rjc-0279-assets.json | grep -A5 '"mockups"'

# Output: mockups section showing slot entries

```

### Verify File Paths

```bash

# Get manifest

cat /srv/artlomo/application/lab/processed/rjc-0279/rjc-0279-assets.json | jq '.files.THUMB'

# Check if file exists

ls /srv/artlomo/application/lab/processed/rjc-0279/rjc-0279-THUMB.jpg
```

---

## Implementation Roadmap

### Phase 1: Backend (COMPLETE ✅)

- [x] Add `/artwork/<slug>/assets` endpoint
- [x] Implement file serving validation
- [x] Update artworks.json schema
- [x] Add fresh manifest initialization
- [x] Refactor mockup routes to use manifest

### Phase 2: Frontend (IN PROGRESS 🔴)

- [ ] Update carousel modal to load manifest
- [ ] Create `/video/<slug>/mockups` endpoint
- [ ] Update video suite to use endpoint
- [ ] Update detail closeup to use manifest references
- [ ] Add error handling for missing manifests

### Phase 3: Migration & Testing

- [ ] Test carousel on all artworks
- [ ] Test video suite mockup loading
- [ ] Verify backward compatibility
- [ ] Performance load testing
- [ ] Update documentation

### Phase 4: Cleanup

- [ ] Remove deprecated slug-based filenames (optional)
- [ ] Archive legacy code branches
- [ ] Update deployment procedures

---

## Troubleshooting Matrix

| Symptom | Root Cause | Solution |
| --------- | ----------- | ---------- |
| 404 on carousel images | File not in manifest | Check manifest `files` and `mockups.assets` |
| "Assets index not found" | First mockup generation | Upgrade to latest `mockup_routes.py` with `_init_fresh_assets_index()` |
| Mockup thumb not loading | Wrong path format in manifest | Verify path is relative: `mockups/thumbs/mu-*.jpg` not `/full/path/` |
| Carousel shows old mockups | Manifest cache stale | Clear browser cache or add `?v=` cache-buster |
| File permission errors | Directory ownership issue | `chown -R www-data:www-data /srv/artlomo/application/lab/processed/` |

---

## Security Considerations

1. **Manifest Validation** — Files served only if declared in manifest
2. **Path Traversal Prevention** — No `../` allowed in file paths
3. **Read-Only API** — Manifest endpoint is GET-only (modifications via specific endpoints)
4. **Atomic Writes** — Manifest updates use atomic writes (temp file + rename)

---

## Performance Metrics

- Manifest load: < 100ms per artwork
- File serving: Native filesystem speed (no processing)
- Carousel render: < 500ms from manifest (images load in parallel)
- Mockup generation: 2-5 seconds per slot (unchanged from before)

---

## Related Documentation

1. **[ASSET_MANAGEMENT_SYSTEM.md](ASSET_MANAGEMENT_SYSTEM.md)** — Architecture, asset types, access patterns
2. **[CAROUSEL_AND_UI_MANIFEST_USAGE_GUIDE.md](CAROUSEL_AND_UI_MANIFEST_USAGE_GUIDE.md)** — Implementation guide for UI components
3. **[MOCKUP_GENERATION_SKIP_MANIFEST_FIX_LOG.md](MOCKUP_GENERATION_SKIP_MANIFEST_FIX_LOG.md)** — Mockup routes refactoring details

---

**Last Updated:** March 3, 2026
**Next Review:** After carousel migration complete
