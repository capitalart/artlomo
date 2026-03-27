# Director's Suite - Complete Architecture Design

## 🎯 SYSTEM OVERVIEW

The Director's Suite lets users configure per-artwork cinematic video rendering:

- Where to zoom/pan in main artwork
- What mockups to include and in what order
- Per-mockup zoom/pan settings

**Goal:** All settings persist → get sent to render worker → produce consistent videos.

---

## 📊 DATA FLOW (End-to-End)

```text
┌─────────────────────────────────────────────────────────────────┐
│                      BROWSER (video_cinematic.js)               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ UI Controls (sliders, checkboxes, buttons)              │  │
│  │  • Duration (10/15/20s)                                 │  │
│  │  • Main artwork pan/zoom                                │  │
│  │  • Mockup pan/zoom (global)                             │  │
│  │  • Per-mockup overrides                                 │  │
│  │  • Select 5 mockups, drag to reorder                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                  │
│                       Auto-save on change                       │
│                              ↓                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ currentSettings object in memory:                        │  │
│  │ {                                                         │  │
│  │   video_duration: 15,                                    │  │
│  │   artwork_pan_enabled: true,                             │  │
│  │   artwork_pan_direction: "up",                           │  │
│  │   mockup_pan_enabled: true,                              │  │
│  │   mockup_pan_direction: "right",                         │  │
│  │   video_mockup_order: ["mu-01", "mu-02", ...],          │  │
│  │   video_mockup_shots: {                                  │  │
│  │     "mu-01": { pan_enabled: true, pan_direction: "up" }, │  │
│  │     "mu-02": { pan_enabled: false, pan_direction: null }│  │
│  │   }                                                      │  │
│  │ }                                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                  │
│                 User clicks "START RENDER"                      │
│                              ↓                                  │
│            POST /video-settings-save (JSON payload)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              FLASK BACKEND (artwork_routes.py)                  │
│                                                                 │
│  video_settings_save(slug):                                    │
│    1. Receive JSON from frontend                               │
│    2. Validate + normalize via _normalize_video_settings()     │
│    3. Write to artwork_data.json:                              │
│       {                                                         │
│         "video_suite": {                                        │
│           "video_duration": 15,                                │
│           "artwork_pan_enabled": true,                         │
│           "artwork_pan_direction": "up",                       │
│           ...                                                  │
│         }                                                      │
│       }                                                        │
│    4. Return { status: "ok", video_suite: {...} }             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                   User clicks "GENERATE"
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│           FLASK BACKEND (video_routes.py)                       │
│                                                                 │
│  generate_kinematic_video(slug):                               │
│    1. Call VideoService.generate_kinematic_video(slug)         │
│    2. Return { success: true, video_url: "..." }              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│        PYTHON SERVICE (video_service.py)                        │
│                                                                 │
│  generate_kinematic_video(slug):                               │
│    1. _load_cinematic_settings(slug)  ← Load from artwork_data │
│    2. Load coordinates.json                                    │
│    3. Determine mockup order                                   │
│    4. Build render payload:                                    │
│       {                                                         │
│         "slug": "rjc-0267",                                     │
│         "video": {                                              │
│           "fps": 24,                                            │
│           "output_size": 1024,                                  │
│           "artwork": {                                          │
│             "pan_enabled": true,                               │
│             "pan_direction": "up",                             │
│             "zoom_intensity": 1.1                              │
│           },                                                   │
│           "mockups": {                                          │
│             "pan_enabled": true,                               │
│             "pan_direction": "right"                           │
│           },                                                   │
│           "mockup_shots": [                                     │
│             {                                                  │
│               "id": "mu-01",                                   │
│               "image": "/path/mu-01.jpg",                      │
│               "pan_enabled": true,                             │
│               "pan_direction": "right",                        │
│               "pan_target": {x: 0.52, y: 0.44},              │
│               "zoom_intensity": 1.15                           │
│             },                                                 │
│             ...                                                │
│           ]                                                    │
│         }                                                      │
│       }                                                        │
│    5. Call _generate_with_ffmpeg() with payload               │
│    6. Spawn Node.js render.js with payload as JSON arg        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│          NODE.JS WORKER (video_worker/render.js)               │
│                                                                 │
│  Receive payload as CLI arg:                                   │
│    1. Parse JSON                                               │
│    2. For each slide (master + mockups):                       │
│       - If slide.pan_enabled === false:                        │
│         zoom_expr = "1"  (no zoom)                             │
│         x_expr = "(iw-iw/zoom)/2"  (center, no pan)            │
│       - Else:                                                  │
│         zoom_expr = calc based on slide.zoom_intensity         │
│         x_expr, y_expr = calc based on pan_direction           │
│         If slide.pan_target exists:                            │
│           bias motion towards pan_target {x, y}                │
│    3. Build ffmpeg filter graph using expressions              │
│    4. Execute ffmpeg with xvfb-run                             │
│    5. Write output to video_output/<slug>.mp4                  │
│    6. Write status to render_status.json                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              BROWSER (polling for completion)                   │
│                                                                 │
│  pollStatus():                                                 │
│    Every 1.5s:                                                 │
│    GET /video-status/<slug>                                    │
│    → Returns { status: "success", video_url: "..." }           │
│    → Update progress bar                                        │
│    → When success: play video in <video> element               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 FILES & RESPONSIBILITIES

| File | Purpose | Key Function |
| ------ | --------- | -------------- |
| `video_workspace.html` | UI layout | Renders controls, mockup grid, chosen panel |
| `video_cinematic.js` | UI controller | Collects settings, auto-saves, manages chosen list |
| `video_suite.css` | Styling | Layout, theme variables |
| `artwork_routes.py` | Save endpoint | `video_settings_save()` normalizes + persists |
| `video_routes.py` | Render endpoint | `generate_kinematic_video()` initiates render |
| `video_service.py` | Service logic | Loads settings, builds payload, spawns worker |
| `render.js` | Video generation | FFmpeg filter math, animation expressions |

---

## 🔧 KEY CLASSES & OBJECTS

### `currentSettings` (in video_cinematic.js)

```javascript
{
  video_duration: 15,                           // seconds
  artwork_zoom_intensity: 1.1,                  // 1.0-1.35
  artwork_zoom_duration: 3.0,                   // seconds
  artwork_pan_enabled: true,                    // boolean
  | artwork_pan_direction: "up",                  // "up" | "down" | "left" | "right" |

  mockup_zoom_intensity: 1.1,                   // 1.0-1.2 (global default)
  mockup_zoom_duration: 2.0,                    // seconds (global default)
  mockup_pan_enabled: true,                     // global toggle
  mockup_pan_direction: "right",                // global default
  mockup_pan_auto_alternate: false,             // alternate direction per mockup

  | video_fps: 24,                                // 24 | 30 | 60 |
  video_output_size: 1024,                      // pixels
  | video_encoder_preset: "fast",                 // "fast" | "medium" | "slow" |
  | video_artwork_source: "auto",                 // "auto" | "closeup_proxy" | "master" |
}
```

### `video_mockup_shots` (per-mockup settings)

```javascript
{
  "mu-rjc-0267-01": {
    id: "mu-rjc-0267-01",
    pan_enabled: true,
    pan_direction: "right",                     // override global
    zoom_intensity: 1.15,                       // override global
    zoom_duration: 2.5,
    zoom_enabled: true,
    pan_target: { x: 0.52, y: 0.44 }           // normalized artwork center
  },
  "mu-rjc-0267-02": {
    id: "mu-rjc-0267-02",
    pan_enabled: false,                         // disable panning for this one
    pan_direction: null,
    ...
  }
}
```

### Payload to Worker (render.js)

```javascript
{
  slug: "rjc-0267",
  video: {
    fps: 24,
    output_size: 1024,
    duration_seconds: 15,
    artwork: {
      zoom_intensity: 1.1,
      zoom_duration: 3.0,
      pan_enabled: true,
      pan_direction: "up"
    },
    mockups: {
      zoom_intensity: 1.1,
      zoom_duration: 2.0,
      pan_enabled: true,
      pan_direction: "right",
      auto_alternate: false
    },
    mockup_shots: [  // per-slide override
      {
        id: "mu-01",
        image: "/path/mu-01.jpg",
        pan_enabled: true,
        pan_direction: "right",
        pan_target: { x: 0.52, y: 0.44 },
        zoom_intensity: 1.15,
        zoom_duration: 2.5
      }
    ]
  }
}
```

---

## 🔗 COORDINATE SYSTEM

### Global Coordinates (artwork_data.json)

```json
{
  "coordinates": {
    "center_x": 0.6166,      // 0..1 normalized (on 2048x2048 canvas)
    "center_y": 0.7904,
    "width_pct": 0.1888,     // art region as % of canvas
    "height_pct": 0.1422
  }
}
```

### Per-Mockup Coordinates (NEW: mockups/mu-01.coords.json)

```json
{
  "mockup_id": "mu-rjc-0267-01",
  "artwork_bounds": {        // WHERE the art appears IN THIS MOCKUP composite
    "center_x": 0.6166,      // center as 0..1 on mockup composite
    "center_y": 0.7904,
    "width_pct": 0.1888,
    "x_px": 1261,            // also in pixels for debugging
    "y_px": 1615,
    "w_px": 386,
    "h_px": 291
  },
  "template": "3x4-BATHROOM-MU-1"
}
```

---

## 🎬 RENDERING PROCESS (render.js)

### For MASTER (artwork) slide

```javascript
if (artworkPanEnabled) {
  if (artworkPanDirection === "up") {
    // pan FROM bottom-center TO top-center (y slides from high to low)
    y = `max(0, min(ih-ih/zoom, (ih-ih/zoom)*(frameProgress)))`
  } else if (artworkPanDirection === "down") {
    y = `max(0, min(ih-ih/zoom, (ih-ih/zoom)*(1-frameProgress)))`
  } // ... left/right similar
} else {
  // no pan, just zoom at center
  x = "(iw-iw/zoom)/2"
  y = "(ih-ih/zoom)/2"
}
```

### For MOCKUP slides

```javascript
if (slide.pan_enabled === false) {
  // No panning or zooming
  x = "(iw-iw/zoom)/2"
  y = "(ih-ih/zoom)/2"
  zoom = "1"
} else {
  // Apply pan direction
  const { x, y } = buildPanExpressions(
    slide.pan_target,        // { x: 0.52, y: 0.44 } ← AIM HERE
    | slide.pan_direction,     // "right" | "left" | "up" | "down" |
    frameCount
  )

  // Apply zoom
  zoom = slide.zoom_intensity (with easing)
}
```

---

## ✅ ACCEPTANCE CRITERIA BY STAGE

### STAGE 1

- [ ] Load page → chosen panel shows 5 auto mockups
- [ ] Click checkbox → chosen panel updates immediately
- [ ] Reload page → settings persist in browser session
- [ ] No console errors

### STAGE 2

- [ ] Disable main artwork pan → rendered video has NO pan on artwork
- [ ] Change mockup direction → next render shows different direction
- [ ] Render uses latest saved settings

### STAGE 3

- [ ] Mockup 1: auto-aim at artwork → visibly pans toward art region
- [ ] Mockup 2: fixed center → pans uniform (old behavior)
- [ ] Swap mockup → its coordinates swap with it

### STAGE 4

- [ ] Click mockup in chosen panel → per-mockup controls appear
- [ ] Change one mockup's direction → only that mockup differs in render

### STAGE 5

- [ ] Non-square artwork → no letterbox at start
- [ ] Fills 1:1 frame fully (CSS object-fit: cover behavior)

---

## 🚨 COMMON FAILURE MODES

| Symptom | Cause | Fix |
| --------- | ------- | ----- |
| Panel shows nothing | mockupMap empty OR autoIds not parsed | Check console debug logs |
| Settings ignored | Backend drops values in normalization | Add missing keys to _normalize |
| All mockups pan same | Per-mockup settings not in payload | Load video_mockup_shots from artwork_data |
| Artwork pans when disabled | Worker doesn't check pan_enabled | Add `if(!pan_enabled) { center_only }` |
| No artwork targeting | Coordinates not loaded or sent | Load coords, resolve target, include in mockup_shot |
