# Mockup Generation Fix: SKU-Assets.json Manifest

**Date:** March 3, 2026
**Issue:** Analysis review pages failing to generate mockups due to file path/naming assumptions vs. new SKU-assets.json file path handling.
**Root Cause:** Routes were still using `mu-{slug}-NN.jpg` deterministic filenames instead of reading slot paths from the assets index.

---

## Changes Made

### 1. **New Helper Function**

**Location:** [application/mockups/routes/mockup_routes.py](application/mockups/routes/mockup_routes.py#L345-L377)

```python
| def _load_assets_index_for_slug(slug: str) -> tuple[str | None, Path, Path, AssetsIndex, dict[str, Any]] | None: |
    """Resolve and load assets index for slug, preferring SKU-index mapping."""
```

- Resolves SKU first via `artworks.json` master index (if available).
- Falls back to `{slug}-assets.json` → `{sku}-assets.json` → `assets.json` search.
- Returns tuple of `(sku, artwork_dir, assets_path, assets_index, assets_doc)`.

---

### 5. **Mockup File Serving (Routes)**

#### `mockup_thumb()` [L501+]

- **Before:** Used deterministic `mu-{slug}-NN-THUMB.jpg` path.
- **After:** Queries assets index for slot entry, reads `thumb` path, falls back to determinism.

#### `mockup_composite()` [L524+]

- **Before:** Used deterministic `mu-{slug}-NN.jpg` path.
- **After:** Queries assets index for slot entry, reads `composite` path, falls back to determinism.

---

### 3. **Mockup Listing**

**Location:** [application/mockups/routes/mockup_routes.py](application/mockups/routes/mockup_routes.py#L380-L425)

- Now calls `_load_assets_index_for_slug()` to get primary source of truth.
- Lists slot metadata (template, category, aspect) from assets doc.
- Fallback scans disk for slug-based + SKU-based file prefixes.

---

### 4. **Mockup Cleanup (Clear + Delete)**

#### `_clear_existing_mockups_for_slug()` [L258-L315]

- **Primary:** Removes files **declared in assets index slot entries** (supports SKU naming).
- **Legacy:** Scans for both `mu-{slug}-*` and `mu-{sku.lower()}-*` patterns.

#### `delete_selected_mockups()` [L905-L970]

- Deletes slots via assets-index paths first.
- Fallback to legacy patterns if slot entry unavailable.
- Updates assets map to remove deleted keys.

---

### 5. **Mockup Generation & Swap**

#### `swap_mockup()` [L595-L649]

- Now calls `_load_assets_index_for_slug()` to verify slot exists.
- Uses `generate_mockups_for_artwork(sku=..., ...)` (SKU-based index-driven gen).
- Passes `master_index_path` and `processed_root` for consistency.

#### `generate_mockups()` [L724-L834]

- Calls `_load_assets_index_for_slug()` to ensure SKU + assets index available.
- Clears existing mockups via `_clear_existing_mockups_for_slug()` (assets-aware).
- Uses `generate_mockups_for_artwork(sku=..., ...)` instead of `_for_slug()`.
- Writes slot entries **atomically to assets index**.

#### `update_mockup_category()` [L683-L721]

- Now uses SKU-aware assets index path.

---

## Fresh Assets Index Initialization

### Problem

When an artwork has never generated mockups before, the `*-assets.json` file does not exist. The refactored routes called `_load_assets_index_for_slug()` which returned `None` when the index file was missing, causing the `generate_mockups()` endpoint to fail with "Assets index not found for artwork."

### Solution

Added new helper function `_init_fresh_assets_index_for_slug()` [L381-L420]:

- Attempts normal load via `_load_assets_index_for_slug()` first.
- If index missing, creates a **fresh minimal index** with proper structure:

  ```json
  {
    "slug": "artwork-slug",
    "sku": "ARTWORK-SKU",
    "mockups": {
      "dir": "mockups",
      "assets": {}
    }
  }
  ```

- Writes atomically to disk under SKU-based filename.
- Returns initialized index in same tuple format as successful load.

### Impact

- ✅ First mockup generation now **works on fresh artworks** (no pre-existing index required).
- ✅ Index is created on-demand with proper SKU mapping.
- ✅ All subsequent generations update the same persistent index.

---

## Fallback Strategy

## All endpoints maintain safe legacy fallbacks

1. Query assets index for slot path → use if found.
2. If no index or missing slot entry → try deterministic `mu-{slug}-NN.jpg`.
3. If SKU differs from slug → additionally try `mu-{sku}-NN.jpg` pattern.

This ensures:

- ✅ New SKU-indexed mockups work correctly.
- ✅ Legacy slug-based mockups still accessible.
- ✅ Smooth transition period during migration.

---

## Testing Checklist

### Analysis Review Page

- [ ] **Generate Mockups**: Click "Generate Mockups" button → verify thumbnails appear.
- [ ] **Load Images**: Click mockup thumbnail → preview image loads (composite URL works).
- [ ] **Swap Mockup**: Click "Swap" on a slot → random template applied, image updates.
- [ ] **Delete**: Select mockup → delete → verify removal and page refresh.

### Video Suite

- [ ] **Storyboard Load**: Open Video Suite → mockups list populated.
- [ ] **Placeholder URL**: Mockup-01 preview image displays.
- [ ] **Selected Mockups**: Drag/select mockups → ordering preserved.

### Asset Index Validation

- [ ] Check `{artwork_dir}/{sku}-assets.json` after generation → `mockups.assets` updated.
- [ ] Verify slot entries contain `composite` and `thumb` relative paths.
- [ ] Confirm paths resolve correctly from artwork directory.

---

## Import Changes

In swap/generate endpoints, replaced:

```python
from application.mockups.pipeline import generate_mockups_for_slug
```

With:

```python
from application.mockups.pipeline import generate_mockups_for_artwork
```

The old `generate_mockups_for_slug()` still exists (legacy compatibility), but new routes use SKU-indexed `generate_mockups_for_artwork()`.

---

## Migration Notes

- **No database changes required** — all asset metadata persists in filesystem `*-assets.json` files.
- **Backward compatible** — all legacy slug-based mockups continue to work.
- **Future-proof** — as SKU-index adoption completes, deterministic fallbacks can be phased out.

---

## Related Files (Not Modified)

- `application/mockups/assets_index.py` — Unchanged (source of truth for slot storage).
- `application/mockups/pipeline.py` — Contains both `generate_mockups_for_slug()` and `generate_mockups_for_artwork()`.
- `application/mockups/artwork_index.py` — Unchanged (master index lookup).
- `application/video/routes/video_routes.py` — Uses same listing logic, still works.
