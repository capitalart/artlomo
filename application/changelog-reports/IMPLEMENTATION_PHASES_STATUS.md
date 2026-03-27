# DIRECTOR'S SUITE - IMPLEMENTATION PHASES COMPLETE

## Status: PHASES 1-3 Complete ✓

### PHASE 1: Data Model Standardization ✓

- **Contract Document**: `/srv/artlomo/VIDEO_SUITE_SETTINGS_CONTRACT.md`

- **Key Changes**:

  - All settings now stored under `artwork_data["video_suite"]` key

  - Nested structure with `artwork`, `mockups`, `output` sections

  - Backward compatibility: Falls back to root keys if video_suite empty

### PHASE 2: Backend Fixes ✓

- **File**: `/srv/artlomo/application/artwork/routes/artwork_routes.py`

  - `_normalize_video_settings()` now builds nested structure (lines 199-228)

  - `_normalize_mockup_shots()` enforces "none" direction rule (lines 244)

  - Save endpoint properly deep-merges to video_suite

- **File**: `/srv/artlomo/application/video/services/video_service.py`

  - `_load_cinematic_settings()` reads from video_suite first (lines 343-481)

  - Falls back to legacy root keys for backward compatibility

  - Returns properly structured dict for payload building

### PHASE 3: Worker Strictness ✓

- **File**: `/srv/artlomo/video_worker/render.js`

  - Lines 344: mockupPanEnabled properly handles undefined → false

  - Lines 350-360: Global settings debug logging

  - Lines 425-440: Per-mockup shot validation and debug logging

  - Lines 503-519: Payload received debug logging

**Debug Command**:

```bash
RENDER_DEBUG=1 npm run render
```

## REMAINING WORK: PHASES 4-5

### PHASE 4: Coordinate-Driven Panning (NOT YET IMPLEMENTED)

**Requirement**:

- Mockups should pan/zoom toward the artwork area identified in coordinates

- Coordinates stored in `/srv/artlomo/application/lab/processed/<slug>/mockups/mu-<slug>-NN.coords.json`

- Format:

  ```json
  {
    "artwork_rect_norm": { "x": 0.32, "y": 0.18, "w": 0.42, "h": 0.55 }
  }
  ```

**Implementation Steps (TODO)**:

1. Modify service to load .coords.json for each mockup

1. Include coords data in payload sent to worker

1. In render.js buildPanExpressions(), accept target coordinates

1. Compute pan direction toward artwork center

1. Override user-selected direction if coordinates suggest different movement

### PHASE 5: COVER Framing for Non-Square Artwork (NOT YET IMPLEMENTED)

**Current Issue**:

- `force_original_aspect_ratio=increase` uses CONTAIN mode (letterboxing)

- Need COVER mode (fill canvas, crop edges if needed)

**Implementation**:
In render.js buildFilter() around line 460, replace:

```javascript
`scale=${width}:${height}:force_original_aspect_ratio=increase,`
```

With logic that computes cover scale:

```javascript
// For COVER: scale ensures image fills canvas
const coverScale = Math.max(width / imgW, height / imgH);
// Then apply zoom on top
```

**User Story**:

- 7200px tall closeup proxy rendered to 1024x1024

- Currently shows full image (small) with black letterbox

- Should show zoomed version filling frame, cropping less essential areas

---

## Quick Test: Settings Pipeline End-to-End

```bash

# 1. Enable debug logging

export RENDER_DEBUG=1

# 2. In Director's Suite UI:

#    - Disable "Pan Master/Artwork"

#    - Set Mockup1 to "UP", Mockup2 to "DOWN"

#    - Select 3 mockups, reorder them

#    - Save

# 3. Check artwork_data.json structure:

cat lab/processed/<slug>/artwork_data.json | jq '.video_suite'

# 4. Check worker received correct payload:

grep "Payload received" render_output.log

# 5. Verify render output:

#    - Artwork should NOT pan

#    - Mockups should pan differently

#    - Video order should match reordered selection

```

---

## Files Ready for Phase 4-5 Work

### Files Already Updated

1. ✓ `/srv/artlomo/application/artwork/routes/artwork_routes.py`

  - Normalization to nested structure ready

1. ✓ `/srv/artlomo/application/video/services/video_service.py`

  - Loading and payload building ready

  - Ready to add coords file loading

1. ✓ `/srv/artlomo/video_worker/render.js`

  - Debug logging present

  - Ready to receive and use coords data

  - Scale logic can be enhanced for COVER mode

### Implementation Hooks

**In video_service.py render() method** (around line 880):

```python

# TODO: Load coordinates for each mockup

# mockup_coords = self._load_mockup_coords(slug, mockup_ids)

# payload["video"]["mockup_coords"] = mockup_coords

```

**In render.js buildFilter()** (around line 460):

```javascript
// TODO: Replace CONTAIN-mode scale with COVER-mode scale
// const coverScale = Math.max(width / slideWidth, height / slideHeight);
// Use coverScale for canvas-filling behavior
```

---

## Acceptance Tests (From Original Spec)

These should now pass with PHASES 1-3:

- ✓ Disable artwork panning → render → artwork stays static

- ✓ Set mockup 1 = Up, mockup 2 = Down, mockup 3 = None → render → each behaves differently

- ✓ Reorder chosen mockups panel → render → video scene order matches exactly

- ✓ No selected mockups → auto 5 populate → reorder → render uses that order

- ? Non-square artwork (proxy) → render starts filled (no letterbox) → **NEEDS PHASE 5**

- ? If coords exist for a mockup → mockup movement trends toward artwork location → **NEEDS PHASE 4**

- ✓ With RENDER_DEBUG=1 logs show correct settings received and applied

---

## Next Steps

When ready, implement:

1. **PHASE 4**: Add `_load_mockup_coords()` in video_service.py

1. **PHASE 5**: Fix COVER scaling in render.js buildFilter()

Both phases maintain backward compatibility (optional coords, graceful degradation).
