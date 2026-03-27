# Stage C: Unified Persistence Layer - Implementation Complete

**Status**: ✅ COMPLETE
**Date**: February 20, 2026
**Objective**: Ensure all Director's Suite settings persist in a unified `video_suite` key within `artwork_data.json` and are restored on page reload

## Overview

The Director's Suite now implements a centralized, unified persistence model:

- All settings stored under single `video_suite` key in `artwork_data.json`

- Deep merge logic prevents data loss when updating

- Full UI initialization from persisted state on page load

- Complete round-trip: Change → Save → Persist → Reload → Restore

## Architecture

### Data Model

```text
artwork_data.json
└── video_suite (object, all Director's Suite settings)
    ├── video_duration (int: 10-20s)
    ├── artwork_zoom_intensity (float: 1.0-1.35x)
    ├── artwork_zoom_duration (float: 0.0-8.0s)
    ├── artwork_pan_enabled (bool)
    | ├── artwork_pan_direction (string: up | down | left | right) |
    ├── mockup_zoom_intensity (float: 1.0-1.2x)
    ├── mockup_zoom_duration (float: 0.0-8.0s)
    ├── mockup_pan_enabled (bool)
    | ├── mockup_pan_direction (string: up | down | left | right) |
    ├── mockup_pan_auto_alternate (bool)
    | ├── video_fps (int: 24 | 30 | 60) |
    | ├── video_output_size (int: 1024 | 1536 | 1920 | 2560 | 3840) |
    | ├── video_encoder_preset (string: fast | medium | slow) |
    | ├── video_artwork_source (string: auto | closeup_proxy | master) |
    ├── selected_mockups (array of strings)
    ├── video_mockup_order (array of strings)
    └── video_mockup_shots (array of {id, pan_enabled, pan_direction})
```

### Data Flow

```text
User Interface (Director's Suite)
    ↓
Form Submission (POST /api/artwork/<slug>/video-settings)
    ↓
Backend Normalization (_normalize_video_settings)
    ↓
video_settings_save Endpoint
    ├─ Wraps normalized settings in {"video_suite": {...}}
    └─ Calls _write_artwork_data({"video_suite": {...}})
        ├─ Reads current artwork_data.json
        ├─ Deep merges video_suite key
        ├─ Preserves all other top-level keys
        └─ Writes back to artwork_data.json
    ↓
Response to Client {"video_suite": {...}}
    ↓
Page Reload or Navigation
    ↓
video_workspace() Route Handler
    ├─ Reads artwork_data.json
    ├─ Extracts video_suite
    ├─ Normalizes it
    └─ Passes to template as video_settings
    ↓
Template (video_workspace.html)
    ├─ Creates data-video-suite-json='{{video_settings | tojson}}'
    ├─ Creates data-auto-mockup-ids='{{auto_mockup_ids | tojson}}'
    └─ Renders to HTML
    ↓
JavaScript (video_cinematic.js)
    ├─ Parses data-video-suite-json → persistedVideoSuite
    ├─ Calls initializeFromPersistedSuite()
    ├─ Sets all UI controls from persistedVideoSuite
    │  ├─ Duration buttons
    │  ├─ Artwork/Mockup zoom inputs
    │  ├─ Pan toggles and direction buttons
    │  ├─ Output settings selectors
    │  ├─ Mockup selection checkboxes
    │  └─ Mockup order and shots
    └─ User ready to edit/render with restored settings
```

## Code Changes

### 1. Backend: Deep Merge for unified `video_suite` key

**File**: `/srv/artlomo/application/artwork/routes/artwork_routes.py`

#### `_write_artwork_data()` (Lines 260-285)

- Added special handling for `video_suite` key

- Deep merges video_suite dict instead of overwriting

- Preserves all other top-level artwork_data keys

- Applies remaining patch keys normally

#### `video_settings_save()` (Lines 680-730)

- Normalizes incoming settings with `_normalize_video_settings()`

- Wraps normalized settings as `{"video_suite": normalized}`

- Calls `_write_artwork_data()` with video_suite wrapper

- Reads back from persisted data

- Returns single `video_suite` object in response (not split keys)

### 2. Route Handler: Prefer `video_suite` with legacy fallback

**File**: `/srv/artlomo/application/video/routes/video_routes.py`

#### `video_workspace()` (Lines 310-365)

- Reads `artwork_data.json`

- Prefers `video_suite` key if it exists and is non-empty

- Falls back to top-level keys for legacy data without breaking

- Normalizes settings safely

- Passes `video_settings` to template

- Passes computed `auto_mockup_ids` as separate data attribute

### 3. Template: Consolidated data attributes

**File**: `/srv/artlomo/application/common/ui/templates/video_workspace.html`

#### Video Suite Data Attributes (Lines 5-11)

- `data-video-suite-json='{{ video_settings | tojson }}'`

  - Single consolidated data attribute

  - Contains all 17 settings as JSON

  - Replaces 3 separate attributes (video_mockup_order, auto_mockup_ids, video_mockup_shots)

- `data-auto-mockup-ids='{{ auto_mockup_ids | tojson }}'`

  - Passed separately (computed per render, not persisted)

  - Used by `getAutoIds()` function for auto mode detection

### 4. JavaScript: Full UI Initialization from Persisted State

**File**: `/srv/artlomo/application/common/ui/static/js/video_cinematic.js`

#### Persistence Variables (Lines 65-70, 120-145)

- `parseVideoSuite()`: Safely parses JSON from template

- `persistedVideoSuite`: Variable holding parsed settings

- Updated mockup order/shots loading to prefer persisted values

#### Current Settings Default Values (Lines 185-210)

- All currentSettings properties default to persistedVideoSuite if available

- Falls back to DOM element values if no persisted state

- Ensures clean initialization on first page visit

- Ensures restoration on reload visits

#### Initialization Function (Lines 653-730)

```javascript
const initializeFromPersistedSuite = () => {
  // Duration
  if (persistedVideoSuite.video_duration) {
    setDuration(persistedVideoSuite.video_duration);
  }

  // Artwork zoom intensity/duration
  // Artwork pan toggle/direction
  // (Similar pattern repeated for all 17 settings)

  // Output settings
  // Mockup selection

  // Restore checklist and order
  if (currentOrderIds.length > 0) {
    mockupCards.forEach((card) => {
      const id = card.dataset.mockupId;
      const checkbox = card.querySelector('[data-storyboard-checkbox]');
      const isSelected = currentOrderIds.includes(id);
      if (checkbox) checkbox.checked = isSelected;
    });
  }
};

// Called immediately after DOM setup
initializeFromPersistedSuite();
```

## Features Implemented

✅ **Centralized Storage**: Single `video_suite` object instead of scattered top-level keys
✅ **Deep Merge**: Updates don't wipe other artwork_data keys
✅ **Backward Compatibility**: Falls back to legacy top-level keys if video_suite missing
✅ **Full Round-Trip Persistence**: Change → Save → Persist → Reload → Restore
✅ **Type Safety**: All settings normalized to correct types before storage
✅ **Array Preservation**: Mockup order and shots arrays preserved exactly
✅ **UI State Restoration**: ALL 17 settings restored when page loads
✅ **Auto Mode Support**: Auto mockup IDs passed as separate data attribute
✅ **Form Control Binding**: Duration buttons, zoom inputs, toggles, selectors initialize from state

## Testing

### Persistence Flow Validation

Run `/srv/artlomo/test_persistence_flow.py`:

```bash
python test_persistence_flow.py
```

Results:

- ✅ Video Suite Structure: All 17 required keys present, type checks passed

- ✅ Array Structures: valid JSON serialization of complex nested structures

- ✅ Deep Merge Logic: Correctly updates video_suite without wiping parent keys

- ✅ JSON Serialization: Full round-trip parse/stringify

### Integration Flow Validation

Run `/srv/artlomo/test_integration_flow.py`:

```bash
python test_integration_flow.py
```

Results:

- ✅ Settings normalized to correct types

- ✅ Backend serialization works (JSON)

- ✅ Template data attributes correctly formed

- ✅ JavaScript can parse and initialize from data attributes

- ✅ All UI controls can be initialized from persisted state

- ✅ Order and shots arrays properly preserved

## Manual Testing Checklist

### Single Setting Test

1. Open Director's Suite for any artwork

1. Change video duration from 15s to 20s

1. Verify button highlight changes

1. Click "Save Settings" (or auto-save if implemented)

1. Reload page

1. ✅ Duration should be 20s

### Multi-Setting Test

1. Open Director's Suite

1. Change multiple settings:

  - Duration: 15s → 20s

  - Artwork zoom: 1.1x → 1.25x

  - Pan direction: up → left

  - FPS: 24 → 60

  - Output size: 1024 → 1920

1. Save settings

1. Reload page

1. ✅ All 5 settings should be restored

### Mockup Selection Test

1. Select 3 mockups from storyboard

1. Reorder them via drag-n-drop

1. Save settings

1. Reload page

1. ✅ Same 3 mockups should be selected

1. ✅ Order should be preserved

### Per-Mockup Pan Test

1. Enable mockup pan

1. Select 2 mockups

1. Set mockup-01 pan direction to "left"

1. Set mockup-02 pan direction to "right"

1. Save settings

1. Reload page

1. ✅ Pan settings for each mockup should be preserved

## Backward Compatibility

If artwork_data.json exists from previous version with top-level keys:

```json
{
  "video_duration": 15,
  "video_fps": 24,
  ...
}
```

**Route handler behavior**:

- Checks for `video_suite` key first (new format)

- If missing or empty, normalizes from top-level keys (legacy)

- `_write_artwork_data()` will create `video_suite` on next save

- Graceful migration without data loss

## Performance Notes

- ✅ No additional DB queries (uses existing artwork_data.json)

- ✅ Minimal JSON memory overhead (single consolidated object)

- ✅ Browser local state restored instantly on page load

- ✅ No network round-trips needed for UI initialization

## Future Enhancements

1. **Auto-Save**: Save settings after each control change (deferred)

1. **Undo/Redo**: Track setting history in separate key

1. **Presets**: Store common setting combinations

1. **Export/Import**: Allow sharing settings between artworks

1. **Analytics**: Track which settings users prefer

## Related Issues

- Stage A: Per-mockup pan controls ✅

- Stage B: Render pipeline integration ✅

- Stage C: Unified persistence ✅

## Files Modified

1. `/srv/artlomo/application/artwork/routes/artwork_routes.py` - Deep merge, endpoint response

1. `/srv/artlomo/application/video/routes/video_routes.py` - Route handler preference logic

1. `/srv/artlomo/application/common/ui/templates/video_workspace.html` - Data attributes

1. `/srv/artlomo/application/common/ui/static/js/video_cinematic.js` - Initialization function

## Summary

The Director's Suite persistence layer is now:

- **Unified**: Single `video_suite` key instead of scattered settings

- **Reliable**: Deep merge prevents data loss

- **Complete**: All 17 settings persist and restore

- **Flexible**: Backward compatible with legacy data

- **Fast**: No additional network overhead

- **Type-safe**: Normalized and validated before storage

Ready for end-to-end testing and render integration!
