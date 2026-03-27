# Director's Suite Video Rendering - Settings Flow Fix

## Issue

Cinematic settings configured in the Director's Suite UI were not affecting the rendered video output. Settings like artwork panning, mockup-specific panning, zoom levels, and per-mockup controls were being ignored.

## Root Causes & Fixes

### 1. ✓ STEP 1: Save Endpoint (Already Working)

**File**: `/srv/artlomo/application/artwork/routes/artwork_routes.py` (lines 686-715)

**Status**: Working correctly

- Endpoint: `POST /api/artwork/<slug>/video/settings`

- Saves all settings under `artwork_data["video_suite"]` key

- Does NOT overwrite unrelated keys

- Includes all required fields:

  - `video_duration`, `video_fps`, `video_output_size`, `video_encoder_preset`

  - `artwork_zoom_intensity`, `artwork_zoom_duration`, `artwork_pan_enabled`, `artwork_pan_direction`

  - `mockup_zoom_intensity`, `mockup_zoom_duration`, `mockup_pan_enabled`, `mockup_pan_direction`

  - `video_mockup_order`, `video_mockup_shots` (per-mockup settings)

### 2. ✓ STEP 2: Settings Loading in video_service.py

**File**: `/srv/artlomo/application/video/services/video_service.py` (lines 343-361)

**Fix Applied**:

```python

# READ FROM video_suite FIRST, THEN FALL BACK TO ROOT KEYS

payload = dict(full_data.get("video_suite") or {})
if not payload:
    payload = full_data
```

**Why**: Service was reading from `artwork_data.json` root level instead of the new `video_suite` nested key, missing all persisted settings.

### 3. ✓ STEP 3: Mockup Shot Normalization

**File**: `/srv/artlomo/application/artwork/routes/artwork_routes.py` (lines 210-256)

**Fix Applied**:

```python

# RULE: If direction is "none", force pan_enabled to False

if pan_direction_raw == "none":
    pan_enabled = False
```

**Why**: Direction "None" should disable panning entirely. Normalizing this at the data level ensures consistency throughout the pipeline.

### 4. ✓ STEP 4: Worker Payload Handling in render.js

**File**: `/srv/artlomo/video_worker/render.js` (lines 344, 350, 505-519)

**Fixes Applied**:

#### a) Fixed mockupPanEnabled initialization (line 350)

```javascript
// BEFORE: const mockupPanEnabled = Boolean(mockupsSettings.pan_enabled);
// AFTER: Proper fallback like artwork
const mockupPanEnabled = mockupsSettings.pan_enabled !== undefined ? Boolean(mockupsSettings.pan_enabled) : false;
```

**Why**: undefined would become false, but now explicitly falls back to false (disabled by default for mockups).

#### b) Added per-mockup shot validation (lines 425-435)

```javascript
// Use per-mockup shot settings if available, else fall back to global settings
let mockupPanned = shotData ? Boolean(shotData.pan_enabled) : mockupPanEnabled;
let mockupDirection = (shotData && shotData.pan_direction) ? String(shotData.pan_direction) : mockupPanDirection;

// Debug logging for each mockup
if (process.env.RENDER_DEBUG) {
  console.log(`[DEBUG] Slide ${i} (mockupIndex ${mockupIndex}):`, {
    hasShotData: !!shotData,
    | shotData: shotData |  | null, |
    mockupPanned,
    mockupDirection,
    hasTarget: slide.hasTarget,
  });
}
```

**Why**: Ensures explicit False values are respected (not replaced with defaults).

#### c) Added comprehensive debug logging (lines 504-519, 353-360)

```javascript
if (process.env.RENDER_DEBUG) {
  console.log("[DEBUG] === RENDER START ===");
  console.log("[DEBUG] Payload received:", {...});
}
```

**Why**: Help diagnose settings flow issues.

## Data Flow After Fixes

```text
UI (video_cinematic.js)
  ↓ POST video_mockup_shots: currentShots
  ↓ POST artwork_pan_enabled, mockup_pan_enabled, etc.
SAVE ENDPOINT (artwork_routes.py:video_settings_save)
  ↓ normalize_video_settings(payload)
  ↓ _normalize_mockup_shots(video_mockup_shots)
  ↓ WRITE to artwork_data["video_suite"]
RENDER TRIGGER (video_service.py:render)
  ↓ _load_cinematic_settings(slug) ← NOW READS FROM video_suite!
  ↓ cinematic_settings extracted
  ↓ BUILD payload.video with artwork/mockups objects
WORKER (render.js)
  ↓ Extract artworkPanEnabled, mockupPanEnabled
  ↓ For each mockup: use shotData.pan_enabled if available
  ↓ APPLY ffmpeg filter with correct pan/zoom settings
OUTPUT VIDEO ← RESPECTS ALL SETTINGS
```

## Testing Checklist

### Test 1: Disable Artwork Panning

1. Open Director's Suite for an artwork

1. **Uncheck** "Pan Master/Artwork" toggle

1. Save

1. Trigger video render

1. **Expected**: Generated video shows artwork WITHOUT panning (stays centered)

1. **Debug**: `RENDER_DEBUG=1 node render.js payload.json` should show `artworkPanEnabled: false`

### Test 2: Different Mockup Pan Directions

1. Select 2 mockups

1. Set Mockup 1: Pan LEFT

1. Set Mockup 2: Pan RIGHT

1. Save

1. Trigger render

1. **Expected**:

  - Mockup 1 pans left-to-right motion

  - Mockup 2 pans right-to-left motion

1. **Debug**: Check stdout logs for each shot's pan_direction

### Test 3: Direction "None" Disables Panning

1. Select 1 mockup

1. Set Pan Direction to "None"

1. Save

1. Check `artwork_data.json`:

   ```json
   {
     "video_suite": {
       "video_mockup_shots": [
         {
           "id": "mockup-id",
           "pan_enabled": false,  // ← Should be false
           "pan_direction": "none"
         }
       ]
     }
   }
   ```

1. Trigger render

1. **Expected**: Mockup stays centered (no panning motion)

### Test 4: Reload & Re-render (Persistence)

1. Configure all settings (pan, zoom, direction, etc.)

1. Render video → Video 1 generated

1. Close and reopen Director's Suite

1. Verify all settings still shown in UI

1. Re-render → Video 2 generated

1. **Expected**: Video 2 matches Video 1 behavior (settings persisted)

### Test 5: Zoom Settings Apply

1. Increase "Mockup Zoom Intensity" from slider

1. Increase "Mockup Zoom Duration"

1. Save & render

1. **Expected**: Mockups show more aggressive zoom in/duration

1. **Debug**: Check payload for `mockup_zoom_intensity` value

### Test 6: FPS and Output Size Settings

1. Set FPS to 30 (from 24)

1. Set Output Size to 1536 (from 1024)

1. Save & render

1. **Expected**:

  - Video file is larger (1536x1536 vs 1024x1024)

  - May have different file size due to FPS change

1. **Debug**: Check payload for `fps: 30, output_size: 1536`

## Debugging: Enable Debug Logging

### In Python (video_service.py render trigger)

```python
import os
os.environ['RENDER_DEBUG'] = '1'

# Then call: service.render(slug, ...)

```

### In Terminal (direct worker test)

```bash
RENDER_DEBUG=1 node /srv/artlomo/video_worker/render.js '{"slug":"test",...}'
```

### Check Output

```text
[DEBUG] === RENDER START ===
[DEBUG] Payload received: {...}
[DEBUG] Artwork settings: { artworkPanEnabled: true, artworkPanDirection: 'up', ... }
[DEBUG] Mockup settings: { mockupPanEnabled: false, mockupPanDirection: 'up', ... }
[DEBUG] Slide 0 (mockupIndex 0): {
  hasShotData: true,
  shotData: { id: 'mu-xxx-01', pan_enabled: false, pan_direction: 'left' },
  mockupPanned: false,
  mockupDirection: 'left'
}
```

## Files Modified

1. `/srv/artlomo/application/video/services/video_service.py`

  - Line 343-361: Read from `video_suite` first

1. `/srv/artlomo/application/artwork/routes/artwork_routes.py`

  - Line 210-256: _normalize_mockup_shots - handle "none" direction

1. `/srv/artlomo/video_worker/render.js`

  - Line 350: Fix mockupPanEnabled initialization

  - Line 353-360: Add global debug logging

  - Line 425-435: Add per-mockup debug logging

  - Line 504-519: Add payload debug logging

## Expected Outcomes

After these fixes:

- ✓ Disabling artwork pan keeps artwork centered

- ✓ Each mockup can have different pan directions

- ✓ Direction "None" prevents any panning

- ✓ Zoom settings affect output

- ✓ FPS and size settings respected

- ✓ Settings persist across page reload

- ✓ Debug logging available via RENDER_DEBUG env var

## Troubleshooting

### Symptom: Settings still ignored

**Check**:

1. Is `artwork_data.json` under `lab/processed/<slug>/`?

1. Run: `cat lab/processed/<slug>/artwork_data.json | jq '.video_suite'`

1. Should show all settings under `video_suite` key, not root

### Symptom: Per-mockup pans all same direction

**Check**:

1. Each mockup should have entry in `video_mockup_shots` array

1. Enable `RENDER_DEBUG` and check per-mockup log output

1. Verify `shotData` shows correct `pan_direction` for each

### Symptom: "None" direction still pans

**Check**:

1. Verify `artwork_data.json` has `"pan_enabled": false` for that shot

1. If it shows `true`, the _normalize_mockup_shots fix isn't applying

1. Check that saves go to `/video/settings` endpoint, not elsewhere

## Related Files Reference

- UI: `/srv/artlomo/application/common/ui/static/js/video_cinematic.js`

- Save Endpoint: `/srv/artlomo/application/artwork/routes/artwork_routes.py` (line 686)

- Video Service: `/srv/artlomo/application/video/services/video_service.py`

- Worker: `/srv/artlomo/video_worker/render.js`

- Template: `/srv/artlomo/application/common/ui/templates/video_workspace.html`
