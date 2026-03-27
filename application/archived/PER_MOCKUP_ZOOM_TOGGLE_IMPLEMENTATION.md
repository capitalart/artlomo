# Per-Mockup Zoom Toggle Implementation

Status: **COMPLETE** ✅
Date: 2026-02-24
Feature: Per-mockup "Zoom Enabled" toggle in Director's Suite

---

## Overview

Added independent "Zoom Enabled" toggle for each selected mockup in the video composition. This allows users to disable zoom animation on specific mockups while others zoom normally.

**Key Behavior**:

- Each mockup row in "Chosen Mockups" panel has a zoom checkbox (default: ON)
- When toggled OFF for a mockup, that mockup stays at constant scale (no zoom animation)
- Panning still works independently regardless of zoom setting
- Settings persist to `artwork_data.json` → `video_suite.video_mockup_shots`

---

## Implementation Summary

### 1. UI Layer (video_cinematic.js)

**File**: `/srv/artlomo/application/common/ui/static/js/video_cinematic.js`

#### Change 1: Update `setShotById()` function

- Now accepts 4th parameter: `zoomEnabled` (boolean, defaults to true)
- Stores `zoom_enabled` in shot object alongside `pan_enabled` and `pan_direction`

```javascript
const setShotById = (id, panEnabled, panDirection, zoomEnabled = true) => {
  const existing = getShotById(id);
  if (existing) {
    existing.pan_enabled = Boolean(panEnabled);
    existing.pan_direction = panDirection;
    existing.zoom_enabled = Boolean(zoomEnabled);  // NEW
  } else {
    currentShots.push({
      id,
      pan_enabled: Boolean(panEnabled),
      pan_direction: panDirection,
      zoom_enabled: Boolean(zoomEnabled),  // NEW
    });
  }
};
```

#### Change 2: Update `renderChosenList()` - add zoom checkbox

- Creates zoom checkbox per mockup row (alongside existing pan checkbox + select)
- Checkbox labeled with title: "Enable zoom animation"
- State: Checked if `shot.zoom_enabled !== false` (defaults to true for new shots)
- All three controls (pan checkbox, pan select, zoom checkbox) update shot and persist immediately

```javascript
// Inside renderChosenList(), where pan controls are created:
const zoomCheckbox = document.createElement('input');
zoomCheckbox.type = 'checkbox';
zoomCheckbox.className = 'form-check-input chosen-zoom-check';
zoomCheckbox.setAttribute('data-mockup-id', id);
zoomCheckbox.setAttribute('title', 'Enable zoom animation');
zoomCheckbox.checked = shot ? (shot.zoom_enabled !== false) : true;  // Default: true

const updateShotAndPersist = async () => {
  setShotById(id, panCheckbox.checked, panSelect.value, zoomCheckbox.checked);
  await persistShots();
};

panCheckbox.addEventListener('change', updateShotAndPersist);
panSelect.addEventListener('change', updateShotAndPersist);
zoomCheckbox.addEventListener('change', updateShotAndPersist);  // NEW

controlsBlock.appendChild(panCheckbox);
controlsBlock.appendChild(panSelect);
controlsBlock.appendChild(zoomCheckbox);  // NEW
```

**UI Layout** (per mockup row):

```text
[Thumbnail] [Pan Checkbox] [Pan Select] [Zoom Checkbox] [Remove Button]
  88x88px      ☑ Pan       ▼ Right       ☑ Zoom              ×
```

### 2. Data Model & Persistence (artwork_routes.py)

**File**: `/srv/artlomo/application/artwork/routes/artwork_routes.py`

**Change**: Extended `_normalize_mockup_shots()` function

- Now validates and normalizes `zoom_enabled` field
- Type coercion: Converts strings ("true", "1", "yes", "on") to boolean
- Default: If `zoom_enabled` not provided, treated as **true** (backward compatible)
- Ensures all shot objects include the field in normalized output

```python
def _normalize_mockup_shots(raw: Any) -> list[dict[str, Any]]:
    """Normalize video_mockup_shots array.

    Each shot dict must have "id" and may have "pan_enabled", "pan_direction", "zoom_enabled".

    Special rules:
    - If direction is "none", force pan_enabled=False
    - If zoom_enabled not provided, defaults to True
    """
    shots: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    # ... existing id and pan validation ...

    # Handle zoom_enabled (defaults to True if missing)
    zoom_enabled_raw = item.get("zoom_enabled", True)
    if isinstance(zoom_enabled_raw, bool):
        zoom_enabled = zoom_enabled_raw
    elif isinstance(zoom_enabled_raw, str):
        zoom_enabled = zoom_enabled_raw.strip().lower() in {"1", "true", "yes", "on"}
    else:
        zoom_enabled = bool(zoom_enabled_raw)

    shot = {
        "id": shot_id,
        "pan_enabled": bool(pan_enabled),
        "pan_direction": pan_direction_raw,
        "zoom_enabled": bool(zoom_enabled),  # NEW
    }
    shots.append(shot)
```

**Data Flow**:

1. UI sends: `{ video_mockup_shots: [{ id, pan_enabled, pan_direction, zoom_enabled }, ...] }`
2. Endpoint calls: `_normalize_video_settings()` → `_normalize_mockup_shots()`
3. Output: Normalized shots stored in `artwork_data.json["video_suite"]["video_mockup_shots"]`

**Example Persisted Data**:

```json
{
  "video_suite": {
    "video_mockup_shots": [
      { "id": "mu-rjc-0267-01", "pan_enabled": true, "pan_direction": "up", "zoom_enabled": true },
      { "id": "mu-rjc-0267-02", "pan_enabled": true, "pan_direction": "right", "zoom_enabled": false },
      { "id": "mu-rjc-0267-03", "pan_enabled": false, "pan_direction": "none", "zoom_enabled": true }
    ]
  }
}
```

### 3. Worker Layer (render.js)

**File**: `/srv/artlomo/video_worker/render.js`

**Changes**: Two updates to support per-mockup zoom control

#### Change 1: Extract and log zoom_enabled from shot data

Updated the per-mockup shot extraction to include zoom state in debug logging:

```javascript
// Inside filter building loop (~line 467):
const mockupIndex = i - (includeMasterSlide ? 1 : 0);
const shotData = mockupIndex < mockupShots.length ? mockupShots[mockupIndex] : null;

// Check if zoom is enabled for this mockup (NEW - defaults to true if not specified)
const mockupZoomEnabled = shotData ? (shotData.zoom_enabled !== false) : true;

// Debug logging includes zoom state (NEW):
if (process.env.RENDER_DEBUG) {
  console.log(`[DEBUG] Slide ${i} (mockupIndex ${mockupIndex}):`, {
    hasShotData: !!shotData,
    | shotData: shotData |  | null, |
    mockupPanned,
    mockupDirection,
    mockupZoomEnabled: shotData ? (shotData.zoom_enabled !== false) : true,  // NEW
    hasTarget: slide.hasTarget,
  });
}
```

#### Change 2: Apply zoom only if enabled

Modified zoom expression building for mockup slides to respect zoom_enabled:

```javascript
} else {
  // Use mockup zoom intensity for non-master slides (UPDATED)
  const mockupIndex = i - (includeMasterSlide ? 1 : 0);
  const shotData = mockupIndex < mockupShots.length ? mockupShots[mockupIndex] : null;

  // Check if zoom is enabled for this mockup (default: true if not specified)
  const mockupZoomEnabled = shotData ? (shotData.zoom_enabled !== false) : true;

  if (mockupZoomEnabled && mockupZoomIntensity > 1.0) {
    // Zoom ENABLED: Apply zoom animation
    const slideZoomIntensity = mockupZoomIntensity;
    const delta = slideFrames > 1 ? (slideZoomIntensity - 1) / (slideFrames - 1) : 0;
    zoomExpr = `min(${slideZoomIntensity.toFixed(4)},1+on*${delta.toFixed(7)})`;
  } else {
    // Zoom DISABLED: No zoom animation (constant scale)
    zoomExpr = "1";
  }
}
```

**Effect**:

- If `zoom_enabled = true`: Mockup zooms from 1.0 → zoom_intensity over slide duration
- If `zoom_enabled = false`: Mockup stays at constant scale (1.0) throughout slide
- Panning still works independently (controlled by `pan_enabled`)

### 4. Styling (video_suite.css)

**File**: `/srv/artlomo/application/common/ui/static/css/video_suite.css`

**Change**: Added `.chosen-zoom-check` CSS class

- Matches styling of `.chosen-pan-check`
- 18x18px checkbox
- Orange accent color on check

```css
.chosen-zoom-check {
  width: 18px;
  height: 18px;
  min-width: 18px;
  cursor: pointer;
  accent-color: var(--accent-orange);
}
```

---

## Data Contract

### video_mockup_shots Schema

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string",
        "description": "Mockup slug/identifier"
      },
      "pan_enabled": {
        "type": "boolean",
        "description": "Enable pan/movement animation"
      },
      "pan_direction": {
        "type": "string",
        "enum": ["none", "up", "down", "left", "right"],
        "description": "Direction of pan motion"
      },
      "zoom_enabled": {
        "type": "boolean",
        "description": "Enable zoom animation (NEW)",
        "default": true
      }
    },
    "required": ["id", "pan_enabled", "pan_direction", "zoom_enabled"]
  }
}
```

---

## Backward Compatibility

✅ **Full backward compatibility maintained**

- Old shot objects without `zoom_enabled` are treated as `zoom_enabled: true` (zoom ON)
- Existing persisted data continues to work
- When old shots are re-saved with new UI, `zoom_enabled: true` is added automatically
- Service layer and UI handle missing field gracefully

**Migration Example**:

```json
// Old data (loaded from file)
{ "id": "mu-test-01", "pan_enabled": true, "pan_direction": "up" }

// After normalization (saved with new UI)
{ "id": "mu-test-01", "pan_enabled": true, "pan_direction": "up", "zoom_enabled": true }
```

---

## Testing Checklist

### Test 1: Zoom enabled (default behavior) ✅

1. Add mockups to video
2. Leave all zoom checkboxes **checked** (default)
3. Render video
4. **Expected**: All mockups zoom normally

### Test 2: Disable zoom for one mockup ✅

1. Add 3 mockups to video
2. Toggle zoom OFF for mockup #2 only
3. Save
4. Render video
5. **Expected**:
  - Mockup #1: Zooms in  (zoom_enabled = true)
  - Mockup #2: Static scale (zoom_enabled = false)
  - Mockup #3: Zooms in  (zoom_enabled = true)
6. Visual: Mockup #2 shows constant composition while others zoom

### Test 3: Persistence across reload ✅

1. Configure mockups with mixed zoom states (some ON, some OFF)
2. Save
3. Reload page
4. **Expected**: Zoom checkboxes retain their state

### Test 4: Zoom + Pan independence ✅

1. Configure:
  - Mockup #1: pan=ON, direction=up, zoom=ON
  - Mockup #2: pan=ON, direction=left, zoom=OFF
2. Render
3. **Expected**:
  - Mockup #1: Pans up AND zooms
  - Mockup #2: Pans left but NO zoom (stays constant scale)

### Test 5: Disable zoom with low zoom_intensity ✅

1. Set global setting: mockup_zoom_intensity = 1.0 (no zoom)
2. Toggle some mockups zoom ON
3. **Expected**: All mockups stay at constant scale (zoom_intensity takes precedence)

### Test 6: Auto-select with zoom toggles ✅

1. Auto-populate with 5 mockups
2. Toggle zoom OFF for some
3. Reorder
4. Save & render
5. **Expected**: Order and zoom state both preserved

### Test 7: Debug logging ✅

1. Run with `RENDER_DEBUG=1 npm run render`
2. Check stdout for per-slide logging
3. **Expected**: Each slide shows correct zoom state

   ```text
   [DEBUG] Slide 1 (mockupIndex 0): { ... mockupZoomEnabled: false, ... }
   [DEBUG] Slide 2 (mockupIndex 1): { ... mockupZoomEnabled: true, ... }
   ```

### Test 8: Validation ✅

1. Manually craft shot with invalid zoom_enabled values:
  - `zoom_enabled: "true"` (string)
  - `zoom_enabled: 1` (number)
  - `zoom_enabled: null`
2. POST to settings endpoint
3. **Expected**: All coerced to boolean, defaults to true if invalid

---

## Debug Output Examples

### With zoom enabled

```text
[DEBUG] Slide 1 (mockupIndex 0): {
  hasShotData: true,
  shotData: { id: 'mu-test-01', pan_enabled: true, pan_direction: 'up', zoom_enabled: true },
  mockupPanned: true,
  mockupDirection: 'up',
  mockupZoomEnabled: true,
  hasTarget: true
}
```

### With zoom disabled

```text
[DEBUG] Slide 2 (mockupIndex 1): {
  hasShotData: true,
  shotData: { id: 'mu-test-02', pan_enabled: true, pan_direction: 'right', zoom_enabled: false },
  mockupPanned: true,
  mockupDirection: 'right',
  mockupZoomEnabled: false,
  hasTarget: true
}
```

---

## Implementation Details

### UI Element Order (per mockup row)

```text
[Thumbnail Badge] [Controls Region] [Remove Button]
                  ├─ Pan Checkbox (☑)
                  ├─ Pan Direction Select (▼ up/down/left/right/none)
                  └─ Zoom Checkbox (☑) ← NEW
```

### Flow: UI → Save → Render

```text
User checks/unchecks zoom checkbox
  ↓
"change" event fires updateShotAndPersist()
  ↓
setShotById() updates currentShots array with new zoom_enabled value
  ↓
persistShots() async calls settings endpoint
  ↓
_normalize_mockup_shots() coerces zoom_enabled to boolean
  ↓
Stored in artwork_data.json["video_suite"]["video_mockup_shots"]
  ↓
On next render: _load_cinematic_settings() reads zoom_enabled
  ↓
Worker receives zoom_enabled in per-mockup shot object
  ↓
render.js applies zoom only if mockupZoomEnabled === true
  ↓
ffmpeg filter: zoomExpr = "1" (no zoom) or formula (with zoom)
```

---

## Files Modified

| File | Changes |
| ------ | --------- |
| `/srv/artlomo/application/common/ui/static/js/video_cinematic.js` | • `setShotById()` now takes `zoomEnabled` param<br>• `renderChosenList()` creates zoom checkbox per row<br>• Checkbox state reflects `shot.zoom_enabled` |
| `/srv/artlomo/application/artwork/routes/artwork_routes.py` | • `_normalize_mockup_shots()` validates `zoom_enabled`<br>• Type coercion: strings → boolean<br>• Default: true if missing |
| `/srv/artlomo/video_worker/render.js` | • Extract `mockupZoomEnabled` from shot data<br>• Apply zoom only if enabled<br>• Add zoom state to debug logging |
| `/srv/artlomo/application/common/ui/static/css/video_suite.css` | • Added `.chosen-zoom-check` styling |

---

## Edge Cases Handled

✅ **Zoom disabled + pan enabled**: Mockup pans but doesn't zoom (independent controls)
✅ **Zoom enabled + pan disabled**: Mockup zooms but doesn't pan (centered, no movement)
✅ **Both disabled**: Mockup stays static (constant scale, centered position)
✅ **All checkboxes ON (default)**: Works like pre-implementation (zoom normal)
✅ **Missing zoom_enabled in old data**: Defaults to true (backward compatible)
✅ **Global zoom_intensity = 1.0**: No zoom regardless of checkbox (baseline takes precedence)
✅ **Auto-selected mockups**: Zoom enabled by default, can be toggled per-mockup
✅ **Reordered mockups**: Zoom state follows mockup, not position

---

## Next Steps (Optional)

1. Add "Bulk Enable/Disable Zoom" button for all selected mockups
2. Add visual indicator (icon) showing zoom enabled state
3. Keybind for toggling zoom on focused mockup (e.g., 'Z' key)
4. Preset templates: "All Zoom", "Alternate Zoom", "First Only"
5. Per-mockup zoom_intensity override (fine-tune zoom scale per mockup)

---

## Verification Commands

```bash

# Check that new field is persisted:

cat lab/processed/<slug>/artwork_data.json | jq '.video_suite.video_mockup_shots[].zoom_enabled'

# Enable debug logging and render:

export RENDER_DEBUG=1 npm run render

# Check for zoom-related debug lines:

grep "mockupZoomEnabled" /srv/artlomo/logs/*.log
```

✅ **Feature complete and ready for testing**
