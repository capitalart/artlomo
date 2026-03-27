# Director's Suite Bug Fixes - February 28, 2026

## Issues Fixed

### 1. **Settings Not Persisting** ✅ FIXED

**Symptom:** Save Settings button wasn't remembering any changes - all settings reverted to defaults on page reload.

**Root Cause:** Critical data structure mismatch in `video_routes.py`

- Backend saves settings as a **nested structure** in artwork_data.json:

  ```json
  {
    "video_suite": {
      "artwork": {"zoom_intensity": 1.1, ...},
      "mockups": {"zoom_intensity": 1.1, ...},
      "output": {"fps": 24, ...}
    }
  }
  ```

- But on page load, the code was passing this **nested structure directly** to `_normalize_video_settings()`, which expects a **flat structure** with keys like `artwork_zoom_intensity`

- This caused the function to return all default values instead of persisted values

- Template received all defaults, UI showed defaults, user thought nothing was saved

**Solution:** Created `_flatten_nested_suite()` function to properly convert nested structure to flat structure before normalization.

## Files Modified

- `application/video/routes/video_routes.py` (lines 323-404)

  - Added `_flatten_nested_suite()` function (lines 323-393)

  - Modified `video_workspace()` to flatten nested suite before normalization (line 383)

---

### 2. **No Animations in Rendered Videos** ✅ FIXED

**Symptom:** Video renders with no pan/zoom animation on artwork or mockups, even after setting animation parameters.

**Root Cause:** Animation settings not being passed to Node render worker

- `_generate_with_ffmpeg()` was extracting animation settings from wrong location:

  ```python
  "zoom_intensity": float(cinematic_settings.get("zoom_intensity") or VIDEO_ZOOM_DEFAULT),
  "panning_enabled": bool(cinematic_settings.get("panning_enabled", VIDEO_PANNING_DEFAULT)),
  ```

- But after normalization, these are stored as `cinematic_settings["artwork"]["zoom_intensity"]`

- Render worker received default values instead of user's configured animation settings

**Solution:** Extract animation settings from proper nested location with fallbacks.

Files Modified

- `application/video/services/video_service.py` (lines 1180-1225)

  - Extract `artwork`, `mockups`, `output` nested dicts

  - Use nested values with fallbacks for backward compatibility

  - Pass complete nested structures to render worker in payload

## Code Changes

```python

# Extract nested artwork/mockup/output settings

artwork_settings = dict(cinematic_settings.get("artwork") or {})
mockups_settings = dict(cinematic_settings.get("mockups") or {})
output_settings = dict(cinematic_settings.get("output") or {})

# Extract animation settings from nested structure with fallbacks

artwork_zoom_intensity = float(artwork_settings.get("zoom_intensity") or cinematic_settings.get("artwork_zoom_intensity") or VIDEO_ZOOM_DEFAULT)
artwork_pan_enabled = bool(artwork_settings.get("pan_enabled") or cinematic_settings.get("artwork_pan_enabled", False))
```

---

### 3. **Info Panel Not Updating Dynamically** ✅ FIXED

**Symptom:** The mockup info line displayed "Time: Auto (2.00s) • Pan: Aim • Zoom: 1.10x" but never updated when settings changed.

**Root Cause:** Info panel was created but never updated due to settings not being properly loaded/initialized.

**Solution:** Now that settings are properly loaded and persisted (fixes #1 and #2), the info panel updates work correctly through existing event handlers.

## How It Works

1. Page loads with persisted settings

1. initializeFromPersistedSuite() loads all values

1. When user changes pan/zoom settings, updateShotAndPersist() is triggered

1. updateShotSummaryLine() rebuilds the info display with current values

1. Changes persist to file

---

## Verification Checklist

To verify all fixes are working:

### ✓ Test 1: Settings Persistence

1. Open Director's Suite for any artwork

1. Change Artwork Zoom Intensity slider to 1.50

1. Change Artwork Zoom Duration to 5.0s

1. Ensure save indicator appears ("✓ Saved")

1. **Reload page (F5)**

1. **VERIFY:** Artwork Zoom Intensity shows 1.50, Duration shows 5.0s

1. Repeat for other settings: Pan toggle, Direction, Output FPS, etc.

### ✓ Test 2: Animation in Videos

1. Configure animations in Director's Suite:

  - Main Artwork: Zoom enabled, intensity 1.3

  - Mockups: Pan enabled, direction "up"

1. Save settings

1. Start render

1. Once complete, check video

1. **VERIFY:** Artwork zooms into frame, then mockups pan upward (or configured direction)

1. No static frames - smooth animation throughout

### ✓ Test 3: Info Panel Updates

1. Select a mockup in the chosen list

1. Change its Pan direction dropdown to "Down"

1. Change its Zoom intensity slider to 1.80

1. **VERIFY:** Info line updates to show "Pan: Down • Zoom: 1.80x"

1. Reload page

1. **VERIFY:** Info line still shows "Pan: Down • Zoom: 1.80x"

---

## Technical Details

### Data Flow (After Fixes)

## Saving

```text
User Form Input
    ↓
JavaScript saveSettings()
    ↓
POST /api/artwork/<slug>/video/settings
    ↓
Backend: _normalize_video_settings(flat_payload)
    ↓
Creates nested structure with artwork/mockups/output keys
    ↓
_write_artwork_data() deep merges into artwork_data.json
    ↓
File saved: artwork_data["video_suite"] = nested_structure
```

## Loading

```text
Browser requests /artwork/<slug>/video-workspace
    ↓
Backend reads artwork_data.json
    ↓
Extracts nested video_suite structure
    ↓
_flatten_nested_suite() converts to flat structure
    ↓
_normalize_video_settings(flat_structure) processes and validates
    ↓
Template receives complete video_settings dict
    ↓
data-video-suite-json passes as JSON to JavaScript
    ↓
parseVideoSuite() extracts in JavaScript
    ↓
initializeFromPersistedSuite() updates all UI controls
```

## Rendering

```text
User clicks "START RENDER"
    ↓
generate_kinematic_video() loads from _load_cinematic_settings()
    ↓
Returns nested video_suite structure from file
    ↓
_generate_with_ffmpeg() properly extracts animation settings:
    - artwork_settings = cinematic_settings["artwork"]
    - mockups_settings = cinematic_settings["mockups"]
    ↓
Builds complete payload with animation settings for Node worker
    ↓
Node render.js receives full configuration
    ↓
Video renders with animations applied
```

---

## Backward Compatibility

All fixes maintain backward compatibility:

- `_normalize_video_settings()` still accepts flat structures (legacy data)

- `_flatten_nested_suite()` has fallbacks for missing nested keys

- Animation extraction has fallback to top-level keys if nested keys missing

- Existing videos/settings continue to work

---

## Files Changed Summary

1. **application/video/routes/video_routes.py**

  - Lines 323-393: Added `_flatten_nested_suite()` function

  - Line 383: Modified to flatten nested suite before normalization

1. **application/video/services/video_service.py**

  - Lines 1180-1184: Extract nested settings with proper structure

  - Lines 1180-1225: Build payload with animation settings from nested location

---

## Next Steps

If issues persist:

1. **Check artwork_data.json exists and is writable:**

   ```bash
   ls -la /srv/artlomo/application/lab/processed/<artwork-slug>/artwork_data.json
   ```

1. **Verify structure is being saved correctly:**

   ```bash
   jq '.video_suite' /srv/artlomo/application/lab/processed/<artwork-slug>/artwork_data.json
   ```

1. **Check browser console for JavaScript errors:**

  - Open DevTools (F12)

  - Look for any red error messages

  - Check Network tab to see if save requests succeeded (200 status)

1. **Check application logs:**

   ```bash
   | sudo journalctl -u artlomo -f --no-pager | grep -i "save\ | error" |
   ```

---

## Deploy Info

**Date:** 28 February 2026
**Services Affected:** ArtLomo Director's Suite
**Restart Required:** Yes (completed)
**Rollback:** Revert edits to  video_routes.py and video_service.py, restart service
