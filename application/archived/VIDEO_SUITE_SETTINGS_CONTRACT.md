# VIDEO_SUITE SETTINGS CONTRACT

Version: 2.0 (Director's Suite Phase 2)
Status: Foundation for all video rendering operations
Last Updated: 2026-02-24

## Overview

All cinematic settings for Director's Suite are stored in a single canonical location within artwork_data.json under the `video_suite` key. This document defines the exact contract expected by all components: UI save form, backend service, and Node.js render worker.

## Storage Schema

Location: `{lab_processed_dir}/{slug}/artwork_data.json`

Structure:

```json
{
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "video_suite": {
    "duration_seconds": 15,

    "artwork": {
      "zoom_intensity": 1.10,
      "zoom_duration": 3.0,
      "pan_enabled": false,
      "pan_direction": "none"
    },

    "mockups": {
      "zoom_intensity": 1.10,
      "zoom_duration": 2.0,
      "pan_enabled": true,
      "auto_alternate_pan": false
    },

    "video_mockup_order": [
      "mu-slug-01",
      "mu-slug-02"
    ],

    "video_mockup_shots": [
      {
        "id": "mu-slug-01",
        "enabled": true,
        "pan_enabled": true,
        "pan_direction": "up",
        "zoom_intensity": 1.10,
        "zoom_duration": 2.0
      },
      {
        "id": "mu-slug-02",
        "enabled": true,
        "pan_enabled": false,
        "pan_direction": "none",
        "zoom_intensity": 1.05,
        "zoom_duration": 1.5
      }
    ],

    "output": {
      "fps": 24,
      "size": 1024,
      "encoder_preset": "fast",
      "artwork_source": "auto"
    }
  },

  "other_data": {}
}
```

## Field Definitions & Validation

### Duration

- **duration_seconds**: number
  - Allowed: 10, 15, 20
  - Default: 15
  - Used by: Worker to slice/join video timeline

### Artwork Settings

- **artwork.zoom_intensity**: float
  - Range: 1.0 - 1.35
  - Default: 1.10
  - Meaning: Factor by which to zoom into master/artwork during slide

- **artwork.zoom_duration**: float
  - Range: 0.5 - 10.0
  - Default: 3.0
  - Meaning: Seconds over which to apply zoom motion

- **artwork.pan_enabled**: boolean
  - Default: false
  - Meaning: If false, artwork stays centered; if true, uses pan_direction

- **artwork.pan_direction**: string
  | - Allowed: "up" | "down" | "left" | "right" | "none" |
  - Default: "none"
  - Rule: If direction is "none", pan_enabled must be false
  - Meaning: Direction of camera movement during artwork slide

### Mockups Settings (Global Defaults)

- **mockups.zoom_intensity**: float
  - Range: 1.0 - 1.20
  - Default: 1.10
  - Meaning: Global zoom for mockups (overridable per-shot)

- **mockups.zoom_duration**: float
  - Range: 0.5 - 10.0
  - Default: 2.0

- **mockups.pan_enabled**: boolean
  - Default: true
  - Meaning: Global pan enable (overridable per-shot)

- **mockups.auto_alternate_pan**: boolean
  - Default: false
  - Meaning: If true, alternate pan direction between consecutive mockups

### Mockup Order

- **video_mockup_order**: array of strings
  - Elements: Mockup base IDs like "mu-slug-NN"
  - Max length: 50
  - Deduped: Yes, order preserved
  - Meaning: Explicit ordering for selected mockups
  - Used by: Service to order selected mockups; if empty, service picks auto 5

### Per-Mockup Controls

- **video_mockup_shots**: array of objects
  - Max items: 50
  - Each item:
  - **id**: string (required, unique)
  - **enabled**: boolean (default: true)
  - **pan_enabled**: boolean (default: inherit from mockups.pan_enabled)
  - **pan_direction**: string (default: inherit from mockups.pan_direction)
  - **zoom_intensity**: float (default: inherit from mockups.zoom_intensity)
  - **zoom_duration**: float (default: inherit from mockups.zoom_duration)
  - Rule: If pan_direction is "none", pan_enabled must be false
  - Deduped: By id
  - Meaning: Per-mockup overrides for any cinematic parameter

### Output Settings

- **output.fps**: integer
  - Allowed: 24, 30, 60
  - Default: 24

- **output.size**: integer
  - Allowed: 1024, 1536, 1920, 2560, 3840
  - Default: 1024
  - Meaning: Output video resolution (square, e.g., 1024x1024)

- **output.encoder_preset**: string
  | - Allowed: "fast" | "medium" | "slow" |
  - Default: "fast"
  - Meaning: ffmpeg encoding quality/speed tradeoff

- **output.artwork_source**: string
  | - Allowed: "auto" | "master" | "closeup_proxy" |
  - Default: "auto"
  - Meaning: Which artwork image to use for master slide

## Service → Worker Payload

When the video service renders, it MUST build payload exactly as:

```json
{
  "slug": "artwork-slug",
  "master_path": "/path/to/MASTER.jpg",
  "mockup_paths": ["/path/1", "/path/2"],
  "output_path": "/path/to/output.mp4",
  "ffmpeg_bin": "/usr/bin/ffmpeg",
  "render_status_path": "/path/to/status.json",
  "video": {
    "fps": 24,
    "output_size": 1024,
    "duration_seconds": 15,
    "artwork": {
      "zoom_intensity": 1.10,
      "zoom_duration": 3.0,
      "pan_enabled": false,
      "pan_direction": "none"
    },
    "mockups": {
      "zoom_intensity": 1.10,
      "zoom_duration": 2.0,
      "pan_enabled": true,
      "auto_alternate_pan": false
    },
    "mockup_order": ["mu-slug-01", "mu-slug-02"],
    "mockup_shots": [
      { "id": "mu-slug-01", "pan_enabled": true, "pan_direction": "up", ... }
    ],
    "encoder_preset": "fast",
    "artwork_source": "auto"
  }
}
```

## Normalization Rules (All Components)

### For All Values

1. Sanitize/type-cast to expected type
2. Clamp numeric values to allowed ranges
3. Lowercase string enums
4. Skip null/undefined → use default

### For Directions

```text
if pan_direction in ["up", "down", "left", "right"]:
    keep as-is
else if pan_direction == "none":
    set pan_direction = "none"
    FORCE pan_enabled = false
else:
    set pan_direction = default
```

### For Mockup Order

```text
seen = {}
deduplicated = []
for id in video_mockup_order:
    if id not in seen:
        deduplicated.append(id)
        seen.add(id)
take first 50 items
```

### For Mock Shots

```text
shots = {}
for shot in video_mockup_shots:
    if shot.id not in shots and len(shots) < 50:
        normalize all fields in shot
        shots[shot.id] = shot

Result: array in original order, deduplicated by id
```

## Save Endpoint Contract

**Route**: `POST /api/artwork/<slug>/video/settings` (or equivalent)

**Input**: JSON from UI form

```json
{
  "duration_seconds": 15,
  "artwork_zoom_intensity": 1.10,
  "artwork_zoom_duration": 3.0,
  "artwork_pan_enabled": false,
  "artwork_pan_direction": "none",
  "mockup_zoom_intensity": 1.10,
  "mockup_zoom_duration": 2.0,
  "mockup_pan_enabled": true,
  "mockup_pan_auto_alternate": false,
  "video_mockup_order": ["mu-slug-01"],
  "video_mockup_shots": [...],
  "video_fps": 24,
  "video_output_size": 1024,
  "video_encoder_preset": "fast",
  "video_artwork_source": "auto"
}
```

**Processing**:

1. Flatten UI input into video_suite nested structure
2. Normalize all values per rules above
3. Deep-merge into artwork_data["video_suite"] (preserve other keys in artwork_data)
4. Write back to artwork_data.json
5. Return persisted video_suite object

**Output**: JSON

```json
{
  "status": "ok",
  "slug": "artwork-slug",
  "video_suite": { ... normalized, persisted structure ... }
}
```

## Phase Diagram

```text
UI (video_cinematic.js)
   ↓ POST /api/artwork/<slug>/video/settings
SAVE ENDPOINT (artwork_routes.py)
   ↓ normalize_video_settings(payload)
   ↓ deep_merge into artwork_data["video_suite"]
FILESYSTEM (artwork_data.json)
   ↓
SERVICE RENDER TRIGGER (video_service.py)
   ↓ _load_cinematic_settings(slug)
   ↓ read from video_suite
   ↓ build payload.video = {...}
WORKER (render.js)
   ↓ extract and apply all settings
   ↓ RESPECT explicit False values
   ↓ LOG all decisions with RENDER_DEBUG
OUTPUT VIDEO (.mp4)
```

## Debugging Checklist

**Enable debug logging**:

```bash
RENDER_DEBUG=1 npm run video:render
```

**Verify data at each stage**:

1. **After UI Save**:
  - Check `artwork_data.json` exists under `video_suite` key
  - Verify structure matches schema above

2. **At Service Load**:
  - Add logging in `_load_cinematic_settings()`:

     ```python
     logger.info(f"Loaded cinematic_settings: {json.dumps(cinematic_settings, indent=2)}")
     ```

3. **Worker Receives Correct Payload**:
  - Enable `RENDER_DEBUG=1`
  - Check stdout for:

     ```text
     [DEBUG] Video payload received:
     artwork.pan_enabled: false
     mockup_shots[0].pan_direction: up
     ...
     ```

4. **Worker Applies Settings**:
  - Check stdout for per-scene logs:

     ```text
     [DEBUG] Scene 0 (master): pan_enabled=false, using center-only coords
     [DEBUG] Scene 1 (mockup):
       Shot data: pan_enabled=true, pan_direction=up
       Filter expr: x=..., y=...
     ```

## Backward Compatibility

**Reading**: If `video_suite` is empty or missing, service may optionally read from root-level keys as fallback.

**Writing**: Always write to `video_suite`. Do NOT use root-level keys going forward.

**No Migration Required**: Service will gracefully fall back on old data; new saves always go to video_suite.

## Example: Full State Lifecycle

### Initial State (Empty)

```json
{ "video_suite": {} }
```

### After First Save (UI fills form)

```json
{
  "video_suite": {
    "duration_seconds": 15,
    "artwork": { "zoom_intensity": 1.1, ... },
    "mockups": { "zoom_intensity": 1.1, ... },
    "video_mockup_shots": [
      { "id": "mu-slug-01", "pan_enabled": true, "pan_direction": "up" }
    ],
    "output": { "fps": 24, "size": 1024, ... }
  }
}
```

### After Re-render with Different Settings

```json
{
  "video_suite": {
    "duration_seconds": 20,
    "artwork": { "zoom_intensity": 1.2, ... },
    ...persisted correctly...
  }
}
```

## Related Files

- Frontend form: `/srv/artlomo/application/common/ui/static/js/video_cinematic.js`
- Save endpoint: `/srv/artlomo/application/artwork/routes/artwork_routes.py` (route: `video_settings_save`)
- Service: `/srv/artlomo/application/video/services/video_service.py` (method: `_load_cinematic_settings`)
- Worker: `/srv/artlomo/video_worker/render.js` (entry point: `run()`)
