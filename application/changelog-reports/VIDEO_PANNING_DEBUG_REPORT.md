# Video Panning Direction Debug Report

**Date:** February 26, 2026
**Issue:** Video generation not adhering to chosen panning direction settings or "AIM TOWARD ARTWORK" toggle

---

## Problem Statement

The Director's Suite video workflow allows users to configure:

1. **Global pan directions** for artwork slide and mockup slides (up/down/left/right)

1. **Per-mockup pan directions** that override global settings

1. **"AIM TOWARD ARTWORK" toggle** (per-mockup) that automatically calculates pan direction toward artwork center based on coordinates

**Current Issue:** Generated videos may not respect these settings, defaulting to incorrect pan directions or ignoring the aim-toward-artwork feature.

---

## Architecture Overview

### Data Flow

```text
UI (HTML/JS)
  → User selects pan directions + aim toggles
  → Auto-save to backend (600ms debounce)
  → Persisted in artwork_data.json (video_suite key)
  → Read by video_service.py when rendering
  → Passed as JSON payload to render.js
  → Translated to FFmpeg zoompan filter expressions
  → Video rendered with pan/zoom effects
```

### Key Components

1. **Frontend**: User configures settings

1. **Backend**: Validates and persists settings

1. **Render Worker**: Generates video using settings

---

## File Inventory & Responsibilities

### 1. Frontend (User Interface)

#### `/srv/artlomo/application/common/ui/templates/video_workspace.html`

**Purpose:** HTML structure for video controls

## Key Elements

- **Lines 248-260**: Artwork pan direction buttons (up/down/left/right)

  - Attribute: `data-artwork-pan-direction`

  - Persisted as: `artwork_pan_direction`

- **Lines 302-314**: Mockup pan direction buttons (global default)

  - Attribute: `data-mockup-pan-direction`

  - Persisted as: `mockup_pan_direction`

- Per-mockup controls are generated dynamically by JavaScript (see video_cinematic.js)

#### `/srv/artlomo/application/common/ui/static/js/video_cinematic.js`

**Purpose:** Manages UI state, auto-save, and per-mockup settings

## Critical Functions

1. **Lines 189-203: `updateMockupShot()`**

  - Updates per-mockup shot properties

  - Sets: `pan_direction`, `pan_to_artwork_center`, `auto_target`

   ```javascript
   existing.pan_direction = panDirection;
   existing.pan_to_artwork_center = Boolean(panToArtworkCenter);
   existing.auto_target = Boolean(panToArtworkCenter); // Alias
   ```

1. **Lines 327-331: Reading persisted settings**

   ```javascript
   | artwork_pan_direction: persistedVideoSuite.artwork_pan_direction |  | 'up', |
   | mockup_pan_direction: persistedVideoSuite.mockup_pan_direction |  | 'up', |
   ```

1. **Lines 1042-1060: Per-mockup shot property controls**

  - Creates dropdown for pan direction per mockup

  - Creates checkbox for "AIM TOWARD ARTWORK" (labeled exactly as such)

  - Reads from shot: `shot.pan_direction`, `shot.pan_to_artwork_center`, `shot.auto_target`

1. **Lines 716-727: Shot property display badges**

  - Shows current pan direction

  - Shows aim-toward-artwork status

**Data Saved:** Sends to backend via POST to `/artwork/{slug}/video-save-suite`

---

### 2. Backend (Persistence & Validation)

#### `/srv/artlomo/application/artwork/routes/artwork_routes.py`

**Purpose:** Saves video suite settings to artwork_data.json

## Critical Sections

1. **Lines 95-97: Artwork pan direction validation**

   ```python
   artwork_pan_direction = str(payload.get("artwork_pan_direction", "up") or "up").strip().lower()
   if artwork_pan_direction not in {"up", "down", "left", "right"}:
       artwork_pan_direction = "up"
   ```

1. **Lines 121-123: Mockup pan direction validation**

   ```python
   mockup_pan_direction = str(payload.get("mockup_pan_direction", "up") or "up").strip().lower()
   if mockup_pan_direction not in {"up", "down", "left", "right"}:
       mockup_pan_direction = "up"
   ```

1. **Lines 226-232: Saved to artwork_data.json**

   ```python
   "artwork": {
       "pan_direction": str(artwork_pan_direction),
       ...
   },
   "mockups": {
       "pan_direction": str(mockup_pan_direction),
       ...
   }
   ```

1. **Lines 252-310: `_normalize_video_mockup_shots()`**

  - Validates per-mockup shot array

  - **Lines 282-284**: Validates per-shot pan_direction

   ```python
   pan_direction_raw = str(item.get("pan_direction", "up") or "up").strip().lower()
   if pan_direction_raw not in {"none", "up", "down", "left", "right"}:
       pan_direction_raw = "up"
   ```

- **Lines 300-301**: Reads aim-toward-artwork setting

   ```python
   aim_raw = item.get("pan_to_artwork_center") or item.get("auto_target")
   ```

- **Lines 287-298**: Pan disable logic (if "none" or disabled)

   ```python
   if pan_direction_raw == "none":
       pan_enabled = False
       pan_direction_raw = "up"  # Store normalized value
   ```

**Persisted Location:** `/srv/artlomo/var/processed/{slug}/artwork_data.json` under key `video_suite`

#### `/srv/artlomo/application/video/routes/video_routes.py`

**Purpose:** Additional validation endpoint for video mockup shots

## Lines 44-100: `_normalize_video_mockup_shots()`

- Same validation logic as artwork_routes.py

- Ensures data integrity before render

---

### 3. Video Generation (Backend → Worker Coordination)

#### `/srv/artlomo/application/video/services/video_service.py`

**Purpose:** Builds render payload and spawns Node.js worker

Critical Sections

1. **Lines 490-492: Read artwork pan direction**

   ```python
   artwork_pan_direction = str(artwork_settings.get("pan_direction")
                               or suite.get("artwork_pan_direction", "up")
                               or "up").strip().lower()
   if artwork_pan_direction not in {"up", "down", "left", "right", "none"}:
       artwork_pan_direction = "up"
   ```

1. **Lines 517-519: Read mockup pan direction**

   ```python
   mockup_pan_direction = str(mockups_settings.get("pan_direction")
                              or suite.get("mockup_pan_direction", "up")
                              or "up").strip().lower()
   if mockup_pan_direction not in {"up", "down", "left", "right", "none"}:
       mockup_pan_direction = "up"
   ```

1. **Lines 608-614: Pan directions added to payload**

   ```python
   "artwork": {
       "pan_direction": artwork_pan_direction,
       ...
   },
   "mockups": {
       "pan_direction": mockup_pan_direction,
       ...
   }
   ```

1. **Lines 1000-1020: Build mockup_shots array with coordinates**

   ```python
   for mockup_id in final_ids:
       shot = shot_by_id.get(mockup_id) or {
           "id": mockup_id,
           "pan_enabled": True,
           "pan_direction": "up",  # Default
       }

       # Load mockup-specific coordinates for aim-toward-artwork
       coords = self._load_mockup_coordinates(slug, mockup_id)
       if coords:
           shot["coordinates"] = coords

       mockup_shots.append(shot)
   ```

1. **Lines 1081-1092: Spawn render.js worker**

   ```python
   worker_args = [
       node_bin,
       "/srv/artlomo/video_worker/render.js",
       json.dumps(payload, ensure_ascii=True, separators=(",", ":")),
   ]
   ```

## Payload Structure Sent to render.js

```json
{
  "video": {
    "mockup_shots": [
      {
        "id": "mu-slug-01",
        "pan_enabled": true,
        "pan_direction": "up",
        "pan_to_artwork_center": false,
        "auto_target": false,
        "zoom_enabled": true,
        "coordinates": {
          "artwork_x_normalized": 0.5,
          "artwork_y_normalized": 0.3
        }
      }
    ],
    "artwork": {
      "pan_direction": "up"
    },
    "mockups": {
      "pan_direction": "right"
    }
  }
}
```

---

### 4. Video Rendering (Node.js + FFmpeg)

#### `/srv/artlomo/video_worker/render.js`

**Purpose:** Translates settings into FFmpeg filter expressions and generates video

Critical Functions

1. **Lines 219-244: `computeArtworkDirection(artworkRect)`**

  - Calculates pan direction toward artwork center

  - Input: Normalized coordinates (0..1)

  - Output: Direction string ("up", "down", "left", "right")

   ```javascript
   function computeArtworkDirection(artworkRect) {
     const x = clamp01(artworkRect.artwork_x_normalized);
     const y = clamp01(artworkRect.artwork_y_normalized);

     const dx = Math.abs(x - 0.5);
     const dy = Math.abs(y - 0.5);

     if (dy > dx) {
       return (y < 0.5) ? "down" : "up";
     } else {
       return (x < 0.5) ? "right" : "left";
     }
   }
   ```

1. **Lines 373-378: Read global pan directions from payload**

   ```javascript
   | const artworkPanDirection = String(artworkSettings.pan_direction |  | "up"); |
   | const mockupPanDirection = String(mockupsSettings.pan_direction |  | "up"); |
   ```

1. **Lines 430-560: `buildFilter()` - Main filter construction**

  - Loops through each slide (artwork + mockups)

  - Applies zoom and pan expressions

1. **Lines 497-510: Per-mockup shot pan direction logic**

   ```javascript
   // Use shot's pan_direction if available
   let mockupDirection = (shotData && shotData.pan_direction)
                         ? String(shotData.pan_direction)
                         : mockupPanDirection;

   // If coordinates available and auto_target enabled, compute direction
   const shotAutoTarget = shotData ? Boolean(shotData.auto_target) : false;
   if (shotAutoTarget && artworkRect) {
     const computedDir = computeArtworkDirection(artworkRect);
     console.log(`Shot ${i}: AIM TOWARD ARTWORK enabled`, {
       computed: computedDir,
       originalDirection: shotData.pan_direction
     });
     mockupDirection = computedDir;  // Override with computed direction
   }
   ```

1. **Lines 246-390: `buildPanExpressions()` and `buildMasterExpressions()`**

  - Translates direction strings into FFmpeg zoompan x/y expressions

  - Creates animated panning over time

  - Pan offset: 40% of available space

## FFmpeg Filter Output

```text
zoompan=z='...':x='...':y='...'
```

Where x and y expressions determine pan direction based on settings.

---

## Debugging Checklist

### Step 1: Verify Frontend

- [ ] Check browser console for JavaScript errors

- [ ] Verify pan direction buttons update `data-pan-direction` attribute

- [ ] Confirm per-mockup controls show correct initial values

- [ ] Test auto-save triggers (600ms after change)

- [ ] Check network tab: POST to `/artwork/{slug}/video-save-suite` succeeds

### Step 2: Verify Persistence

- [ ] Open `/srv/artlomo/var/processed/{slug}/artwork_data.json`

- [ ] Check `video_suite.artwork.pan_direction` matches UI

- [ ] Check `video_suite.mockups.pan_direction` matches UI

- [ ] Check `video_suite.video_mockup_shots` array exists

- [ ] For each shot, verify:

  - `pan_direction` field present

  - `auto_target` or `pan_to_artwork_center` matches checkbox

### Step 3: Verify Backend Reading

- [ ] Add logging to `video_service.py` lines 490-519

- [ ] Log the payload being sent to render.js (line 1082)

- [ ] Verify `cinematic_settings` dict contains correct values

- [ ] Check if `mockup_shots` array built correctly (lines 1000-1020)

- [ ] Confirm coordinates loaded when aim-toward-artwork enabled

### Step 4: Verify Render Worker

- [ ] Add console.log in render.js at line 373-378 (global directions)

- [ ] Add console.log at line 497-510 (per-shot logic)

- [ ] Check if `shotAutoTarget` evaluates to true when expected

- [ ] Verify `computeArtworkDirection()` returns correct direction

- [ ] Confirm final `mockupDirection` variable used in pan expressions

### Step 5: Test FFmpeg Output

- [ ] Inspect generated FFmpeg filter string (console output)

- [ ] Verify zoompan x/y expressions match intended direction

- [ ] Check if pan animation moves in correct direction

---

## Common Failure Points

### 1. **Frontend not sending data**

- **Symptom:** Settings visible in UI but not saved

- **Check:** Browser network tab, auto-save debounce, JavaScript errors

- **Fix:** Verify event listeners attached, check `updateMockupShot()` called

### 2. **Backend normalization stripping fields**

- **Symptom:** Settings saved but missing from JSON

- **Check:** `_normalize_video_mockup_shots()` in artwork_routes.py

- **Fix:** Ensure all fields copied to normalized output (lines 295-298)

### 3. **Coordinate loading failure**

- **Symptom:** Aim-toward-artwork doesn't work

- **Check:** `_load_mockup_coordinates()` returns valid data

- **Fix:** Verify coordinates file exists at `/srv/artlomo/var/processed/{slug}/coordinates/{mockup_id}.json`

### 4. **Render worker not reading shot settings**

- **Symptom:** All mockups use same direction despite different settings

- **Check:** `shotData` variable in render.js line 497

- **Fix:** Ensure payload.video.mockup_shots indexed correctly by slide number

### 5. **Auto-target not overriding manual direction**

- **Symptom:** Manual direction used even when aim toggle enabled

- **Check:** Lines 500-510 in render.js

- **Fix:** Verify `shotAutoTarget` boolean evaluates correctly, check coordinate presence

### 6. **Direction string mismatch**

- **Symptom:** Invalid direction value causes default behavior

- **Check:** Valid values: "up", "down", "left", "right", "none"

- **Fix:** Add validation logging, ensure lowercase comparison

---

## Test Case Example

## Expected Behavior

1. User selects mockup #1, sets pan direction to "left"

1. User enables "AIM TOWARD ARTWORK" for mockup #1

1. Artwork coordinates: x=0.7, y=0.5 (right side)

1. Computed direction should be "left" (toward artwork)

1. Video should pan left during mockup #1 slide

## Verification

- Check `artwork_data.json`: `video_mockup_shots[0].auto_target === true`

- Check render.js console: "AIM TOWARD ARTWORK enabled, computed: left"

- Check video: Mockup #1 slide pans left (not up/down/right)

---

## Payload Example (Correct)

```json
{
  "video": {
    "mockup_shots": [
      {
        "id": "mu-example-01",
        "pan_enabled": true,
        "pan_direction": "right",
        "zoom_enabled": true,
        "pan_to_artwork_center": true,
        "auto_target": true,
        "coordinates": {
          "artwork_x_normalized": 0.3,
          "artwork_y_normalized": 0.5
        }
      },
      {
        "id": "mu-example-02",
        "pan_enabled": true,
        "pan_direction": "up",
        "zoom_enabled": false,
        "pan_to_artwork_center": false,
        "auto_target": false
      }
    ],
    "artwork": {
      "pan_direction": "down"
    },
    "mockups": {
      "pan_direction": "right"
    }
  }
}
```

## Expected Result

- Mockup #1: Pan LEFT (computed from coordinates, artwork at x=0.3)

- Mockup #2: Pan UP (manual setting, no auto-target)

- Artwork slide: Pan DOWN (global setting)

---

## Files to Review

### Must Review (Core Logic)

1. `/srv/artlomo/video_worker/render.js` - Lines 373-378, 497-510 (pan direction selection)

1. `/srv/artlomo/application/video/services/video_service.py` - Lines 1000-1020 (payload construction)

1. `/srv/artlomo/application/artwork/routes/artwork_routes.py` - Lines 282-301 (normalization)

### Should Review (Data Flow)

1. `/srv/artlomo/application/common/ui/static/js/video_cinematic.js` - Lines 189-203, 1042-1060

1. `/srv/artlomo/video_worker/render.js` - Lines 219-244 (computeArtworkDirection)

### Optional Review (UI/Templates)

1. `/srv/artlomo/application/common/ui/templates/video_workspace.html` - Lines 248-314

---

## Logging Recommendations

Add these debug logs to trace data flow:

## In video_service.py (line 1015)

```python
logger.info(f"Shot {mockup_id}: pan_direction={shot.get('pan_direction')}, auto_target={shot.get('auto_target')}")
```

## In render.js (line 498)

```javascript
console.log(`Processing slide ${i}:`, {
  shotData: shotData,
  hasCoordinates: !!artworkRect,
  autoTarget: shotAutoTarget,
  computedDirection: shotAutoTarget && artworkRect ? computeArtworkDirection(artworkRect) : null,
  finalDirection: mockupDirection
});
```

---

## Summary

The pan direction flow involves 4 layers:

1. **UI** captures user choices

1. **Backend** validates and persists to JSON

1. **Service** reads JSON and builds render payload

1. **Worker** translates payload to FFmpeg expressions

**Most likely failure point:** Lines 497-510 in render.js where per-shot settings override global settings, especially the auto-target logic that computes direction from coordinates.

**Quick fix test:** Add console.log statements in render.js to see actual values being processed during render.
