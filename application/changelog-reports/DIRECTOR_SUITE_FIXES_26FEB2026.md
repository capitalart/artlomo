# Director's Suite Bug Fixes - February 26, 2026

## Overview

This document summarizes all bug fixes and improvements made to the ArtLomo Director's Suite video workflow on February 26, 2026. These fixes resolve critical issues with per-mockup settings persistence, rendering, and UI text.

---

## Issues Fixed

### Issue 1: Image Squashing (FIXED)

**Problem:** 3:4 aspect ratio artwork (5424x7200px) was being squashed into the 1024x1024px square video preview instead of covering the full width.

**Root Cause:** CSS property `object-fit: contain` was scaling the entire image to fit within bounds, adding letterboxing instead of filling the square.

**Solution:** Changed to `object-fit: cover` to fill the square width, cropping vertical edges when necessary.

## Files Modified

- `/srv/artlomo/application/common/ui/static/css/video_suite.css` (line 106)

## Code Change

```css
/* Before */
.suite-player-wrap video,
.suite-player-wrap img {
  object-fit: contain;  /* Letterboxes the image */
}

/* After */
.suite-player-wrap video,
.suite-player-wrap img {
  object-fit: cover;  /* Fills square, crops if needed */
}
```

---

### Issue 2: Per-Mockup Settings Not Persisting on Page Reload (FIXED)

**Problem:** When manually selecting 5 mockups and changing per-mockup settings (pan direction, zoom, aim), reloading the page would lose all settings and revert to auto-selected mockups.

**Root Cause:** Multiple issues combined:

1. Per-mockup shot settings (`video_mockup_shots`) were being normalized but fields like `zoom_enabled` and `pan_to_artwork_center` (aim) were being stripped out

1. Per-mockup timing settings (`video_mockup_timings`) and main artwork duration (`main_artwork_seconds`) were not being persisted at all

1. Two different `_normalize_mockup_shots` functions existed (one in `artwork_routes.py` and one in `video_routes.py`) with different logic

## Solution

1. Updated both `_normalize_mockup_shots` functions to preserve all shot properties:

  - `id` (mockup ID)

  - `pan_enabled` (whether panning is enabled)

  - `pan_direction` (up/down/left/right)

  - `zoom_enabled` (whether zoom animation is enabled)

  - `pan_to_artwork_center` (AIM TOWARD ARTWORK feature)

  - `auto_target` (alias for pan_to_artwork_center for backward compatibility)

1. Updated `_normalize_video_settings` to extract and return:

  - `main_artwork_seconds` (duration of main artwork slide)

  - `video_mockup_timings` (per-mockup duration locks)

1. Ensured consistency between all three locations:

  - `/srv/artlomo/application/video/routes/video_routes.py`

  - `/srv/artlomo/application/artwork/routes/artwork_routes.py`

  - `/srv/artlomo/application/video/services/video_service.py`

Files Modified

- `/srv/artlomo/application/video/routes/video_routes.py` (lines 41-86, 240-289)

- `/srv/artlomo/application/artwork/routes/artwork_routes.py` (lines 249-320)

- `/srv/artlomo/application/video/services/video_service.py` (lines 429-650)

## Key Code Changes

```python

# OLD: Only preserved id, pan_enabled, pan_direction

shot = {
    "id": shot_id,
    "pan_enabled": bool(pan_enabled),
    "pan_direction": pan_direction_raw,
}

# NEW: Preserves all properties including zoom and aim

shot = {
    "id": shot_id,
    "pan_enabled": bool(pan_enabled),
    "pan_direction": pan_direction_raw,
    "zoom_enabled": bool(zoom_enabled),
    "pan_to_artwork_center": bool(pan_to_artwork_center),
    "auto_target": bool(pan_to_artwork_center),
}
```

---

### Issue 3: Incorrect UI Text Label (FIXED)

**Problem:** The per-mockup aim/pan-to-artwork-center toggle was labeled "Aim Toward Center" instead of the intended "AIM TOWARD ARTWORK".

**Solution:** Updated the label text in the JavaScript UI component creation.

Files Modified

- `/srv/artlomo/application/common/ui/static/js/video_cinematic.js` (line 1057)

Code Change

```javascript
// Before
const { wrapper: aimToggle, checkbox: aimCheckbox } = createToggleControl(
  'Aim Toward Center',  // Incorrect label
  panToArtworkCenterValue,
  id,
  'Aim pan toward artwork center (from coordinates)'
);

// After
const { wrapper: aimToggle, checkbox: aimCheckbox } = createToggleControl(
  'AIM TOWARD ARTWORK',  // Correct label
  panToArtworkCenterValue,
  id,
  'Aim pan toward artwork center (from coordinates)'
);
```

---

### Issue 4: Pan Direction Direction Inconsistencies (FIXED)

**Problem:** Pan directions (up, down, left, right) were not being respected consistently:

- Frontend JavaScript defaulted to "up"

- Backend defaulted to "right" in multiple places

- Render worker expected "up"

- This caused all pans to go left and up regardless of selected direction

**Root Cause:** Default pan direction was inconsistently set to "right" in:

1. `video_service.py` when creating default shots

1. `video_routes.py` _normalize_mockup_shots

1. `artwork_routes.py` _normalize_mockup_shots

1. `video_service.py` _load_cinematic_settings

**Solution:** Standardized all pan direction defaults to "up" across all files to match JavaScript and render worker expectations.

Files Modified

- `/srv/artlomo/application/video/routes/video_routes.py` (line 74)

- `/srv/artlomo/application/artwork/routes/artwork_routes.py` (line 282)

- `/srv/artlomo/application/video/services/video_service.py` (lines 517, 1013)

## Code Changes

```python

# BEFORE: Defaults to "right"

pan_direction_raw = str(item.get("pan_direction", "right") or "right").strip().lower()
if pan_direction_raw not in {"none", "up", "down", "left", "right"}:
    pan_direction_raw = "right"

# AFTER: Defaults to "up"

pan_direction_raw = str(item.get("pan_direction", "up") or "up").strip().lower()
if pan_direction_raw not in {"none", "up", "down", "left", "right"}:
    pan_direction_raw = "up"
```

---

## Technical Details

### Persistence Flow

The new persistence flow for per-mockup settings:

1. **Frontend** (`video_cinematic.js`): User changes per-mockup settings via checkboxes/selects

1. **Auto-Save** (`saveSettings()`): Debounced function sends all settings to backend

1. **Backend Settings Save** (`artwork.video_settings_save`): Stores in `artwork_data.json` under `video_suite` key

1. **Backend Render** (`generate_kinematic_video`): Loads settings from `video_suite`, passes to render worker

1. **Render Worker** (`render.js`): Uses per-mockup shots for individual mockup panning/zooming

### Key Data Structures

## Per-Mockup Shot Object

```json
{
  "id": "mu-slug-01",
  "pan_enabled": true,
  "pan_direction": "up",
  "zoom_enabled": true,
  "pan_to_artwork_center": false,
  "auto_target": false
}
```

## Video Suite Settings (persisted)

```json
{
  "video_duration": 15,
  "main_artwork_seconds": 4.0,
  "video_mockup_shots": [...],
  "video_mockup_timings": {"mu-slug-01": 2.0, ...},
  "artwork": {
    "zoom_intensity": 1.1,
    "pan_direction": "up",
    "pan_enabled": true
  },
  "mockups": {
    "zoom_intensity": 1.1,
    "pan_direction": "up",
    "pan_enabled": false
  }
}
```

---

## Testing Checklist

- [ ] **Image Aspect Ratio**

  - Load artwork with 3:4 aspect ratio

  - Verify image fills full width of 1024x1024 square

  - Verify no letterboxing or distortion

- [ ] **Per-Mockup Settings Persistence**

  - Select 5 mockups manually

  - Change pan direction for each to different directions (up, down, left, right)

  - Enable AIM TOWARD ARTWORK for some mockups

  - Change zoom enable/disable settings

  - Reload page

  - Verify all 5 mockups still selected

  - Verify each mockup retained its pan direction

  - Verify AIM TOWARD ARTWORK state persisted

- [ ] **Auto-Save Without Manual Button**

  - Change mockup order by dragging

  - Change global settings (duration, zoom, pan direction)

  - Wait 600ms (auto-save debounce time)

  - Reload page

  - Verify all changes persisted

- [ ] **UI Labels**

  - Open mockup settings in chosen list

  - Verify toggle shows "AIM TOWARD ARTWORK" label

- [ ] **Pan Direction Consistency**

  - Select pan direction "down" globally

  - Generate render

  - Verify pans move downward

  - Try "left", "right", "up" and verify each direction works

- [ ] **Render Overlay**

  - Generate video

  - Verify overlay appears with spinner and message

  - Reload during render

  - Verify overlay still shows and polling continues

---

## Backward Compatibility

All changes maintain backward compatibility:

- Old `auto_target` field is still supported (mapped to `pan_to_artwork_center`)

- Missing fields default to sensible values (pan enabled=true, zoom enabled=true, zoom_direction="up")

- Nested structure in `video_suite` is optional; legacy root-level keys still work

---

## Environment Setup Notes

**Default Pan Direction:** "up"
**Object Fit Mode:** "cover" (for square containers with non-square images)
**Auto-Save Debounce:** 600ms
**Render Status Poll Interval:** 1500ms

---

## Files Modified Summary

| File | Lines | Changes |
| ------ | ------- | --------- |
| `video_routes.py` | 41-86, 240-289 | Updated _normalize_mockup_shots,_normalize_video_settings |
| `artwork_routes.py` | 249-320 | Updated _normalize_mockup_shots |
| `video_service.py` | 429-650, lines 517, 1013 | Updated default pan directions, _load_cinematic_settings |
| `video_cinematic.js` | 1057 | Updated AIM label text |
| `video_suite.css` | 106 | Changed object-fit from contain to cover |

---

## Known Limitations

1. **Pan Direction Locked on Aim Frame**: When rendering, if "AIM TOWARD ARTWORK" is enabled, it overrides the manual pan direction to compute direction toward artwork center. This is by design.

1. **Render Worker Coordinates**: Aim-toward-artwork requires `.coords.json` files with `artwork_rect_norm` data. If coordinates are missing, pan defaults to manual direction setting.

1. **Synchronization Requirement**: Frontend and backend normalization functions must stay in sync. Changes to one require updating all three locations mentioned in "Files Modified Summary".

---

## Future Improvements

- [ ] Consolidate _normalize_mockup_shots into a shared utility module

- [ ] Add validation UI for per-mockup settings (visual preview of pan directions)

- [ ] Add batch edit for per-mockup settings

- [ ] Track which fields have unsaved changes with visual indicator

---

**Last Updated:** February 26, 2026
**QA Status:** Ready for testing
