# Per-Mockup Timing — Quick Reference

## How Users Control Timing

### 1. Set Main Artwork Duration

- **Location**: Cinematic Settings panel → "Main Artwork" section → "Duration (Seconds)" range slider

- **OR**: Timing summary bar → "Main Artwork:" input field

- **Range**: 1.0s to 10.0s (0.5 step)

- **Effect**: Reduces available time for mockups proportionally

- **Default**: 4.0s

### 2. Lock Individual Mockup Durations

- **Location**: Chosen mockups list → each row has "TIME" control group

- **Dropdown**: Select from [Auto, 1.0s, 1.5s, 2.0s, 2.5s, 3.0s, 3.5s, 4.0s]

- **Default**: Auto (splits remaining time)

- **Effect**: Takes that mockup out of auto-split pool

- **Saves immediately** (debounced to backend)

### 3. Quick-Lock to 4.0s

- **Button**: "Info" button next to timing dropdown

- **Effect**: Instantly locks that mockup to 4.0s

- **Shortcut**: Saves one click vs. opening dropdown and selecting 4.0s

### 4. Monitor Auto-Split

- **Timing summary bar** shows:

  - Auto count: "N mockups"

  - Per-mockup share: "Zs each" (e.g., "2.20s each")

  - Whether overflow is happening with scale factor

### 5. Reorder Mockups

- **Drag mockups** in chosen list to reorder

- **Timings follow mockup IDs** (not affected by order)

- **Drift correction applies to last mockup** in new order

- **Automatically recalculates** after reorder

---

## How The Math Works

### Available Time for Mockups

```text
available_for_mockups = total_duration - main_artwork_seconds
```

Example: 15s total - 4s main = 11s for mockups

### Split Auto Mockups Evenly

```text
each_auto = available_for_mockups / count_of_autos
```

Example: 11s ÷ 5 autos = 2.20s per mockup

### Handle Overflow (Locked > Available)

```text
If sum(locked) > available_for_mockups:
  scale = available_for_mockups / sum(locked)
  each_locked_scaled = locked_duration * scale
```

Example: 4 mockups × 4.0s = 16s < 11s available

- Scale: 11s ÷ 16s = 0.6875

- Each becomes: 4.0s × 0.6875 = 2.75s

- UI shows warning: "Scaled to fit: ×0.69"

### Round to Frame Boundaries

```text
frame_duration = 1.0 / fps
rounded_duration = round(duration / frame_duration) * frame_duration
```

Example at 24fps (frame = 0.0417s):

- 2.20s → 53 frames → 2.208s (rounded)

### Drift Correction

Last mockup adjusted so total = exactly available_for_mockups

- Prevents cumulative rounding error

- Ensures render length matches UI promise

---

## Data Flow

### 1. User Changes Timing

```text
UI Dropdown/Input → updateTimingAndPersist() → videoMockupTimings dict updated
         ↓
updateTimingSummary() → computeTimingBreakdown() → recompute all durations
         ↓
Display effective times on each mockup row + summary bar stats
         ↓
persistTimings() → POST to /artwork/<slug>/video/settings
```

### 2. Backend Receives Settings

```text
POST /artwork/<slug>/video/settings
{
  "main_artwork_seconds": 4.0,
  "video_mockup_timings": {
    "mu-rjc-0267-05": 4.0,
    "mu-rjc-0267-09": 2.0
  }
}
         ↓
_normalize_video_settings() → clamp/round values
         ↓
Stored in artwork_data.json under video_suite key
```

### 3. Render Starts

```text
generate_kinematic_video(slug)
         ↓
_generate_with_ffmpeg() loads cinematic_settings
         ↓
_compute_mockup_durations() → computes final effective durations with rounding
         ↓
payload.video.computed_mockup_durations = {
  "mu-rjc-0267-05": 1.75,
  ...
}
         ↓
Node worker receives in render payload
         ↓
buildFilter() uses payload.video.computed_mockup_durations
         ↓
Applies duration to each mockup segment
```

---

## Key Constants

| Setting | Min | Default | Max | Step |
| --------- | ----- | --------- | ----- | ------ |
| Main Artwork Seconds | 1.0 | 4.0 | 10.0 | 0.5 |
| Per-Mockup Locked Duration | 1.0 | N/A | 4.0 | 0.5 |
| Total Video Duration | 10 | 15 | 20 | 5 |
| FPS (affects rounding) | 24 | 24 | 60 | N/A |

---

## Persistence

### Where It's Stored

- **File**: `/srv/artlomo/application/artwork/lab/processed/<slug>/artwork_data.json`

- **Key path**: `video_suite.main_artwork_seconds` and `video_suite.video_mockup_timings`

### What Persists Across Reload

- ✅ Main artwork duration

- ✅ Per-mockup locked durations (only if user manually set them)

- ✅ "Auto" status for unlocked mockups

- ✅ Mockup order

### What Does NOT Persist (recalculated on load)

- Effective computed durations (recalculated from formula)

- Width-relative offsets

- Rounding artifacts (may vary with fps changes)

---

## Warnings & Edge Cases

### Overflow Warning

**When**: Sum of locked durations exceeds available time
**What happens**: All locked durations scaled down proportionally
**User sees**: "Locked time exceeds available. Scaled to fit: ×0.88"
**Action**: Can either reduce locked durations or increase main video duration

### No Mockups Selected

**Effect**: Timing summary bar hidden, auto-split disabled
**Behavior**: Defaults to equal split of total duration

### Change FPS

**Effect**: Rounding changes (frame boundaries recalculated)
**Result**: UI durations may shift by ~1-2 milliseconds
**Action**: Automatic; no user action needed

### Reorder After Manual Timings

**What happens**: Timings stay attached to mockup IDs
**Drift correction**: Applies to NEW last mockup in order
**Result**: Last mockup may gain/lose few milliseconds for alignment

---

## Testing Quick Checklist

### Basic Flow

- [ ] Load video workspace for artwork with mockups

- [ ] Select 3+ mockups

- [ ] Timing summary bar appears

- [ ] Timing controls visible in each mockup row

### Set Timings

- [ ] Click dropdown → select "2.0s" → "Info" button shows scaling

- [ ] Click "Info" button → locks to 4.0s instantly

- [ ] Summary recalculates → Auto mockups split new amount equally

- [ ] Effective times update on each row

### Main Artwork Seconds

- [ ] Change main artwork slider → all timings recalculate

- [ ] Summary shows new available time

- [ ] Persist settings → reload page → values persist

### Overflow

- [ ] Lock all 4 mockups to 4.0s → total 16s > 11s available

- [ ] Warning appears: "Scaled to fit: ×0.6875"

- [ ] Each mockup shows "= 2.75s" (scaled)

- [ ] Render should respect scaled durations

### Reorder

- [ ] Drag mockups to new order

- [ ] Timings follow mockup IDs (not positions)

- [ ] Summary recalculates

- [ ] Render uses new order + associated timings

### Frame Rounding

- [ ] At 24 fps: 2.20s → 52-53 frames

- [ ] At 30 fps: 2.20s → 66 frames

- [ ] At 60 fps: 2.20s → 132 frames

- [ ] (Check in worker logs if RENDER_DEBUG=1)

---

## Troubleshooting

### Timings not persisting?

- **Check**: POST status code (should be 200, status: "ok")

- **Check**: Network tab → payload sent correctly

- **Check**: Browser console for errors

- **Fix**: Clear cache, reload page

### Summary bar not showing?

- **Check**: Mockups selected (checkboxes checked)

- **Check**: renderChosenList() was called (console logs)

- **Fix**: Select/deselect mockups to trigger render

### Wrong effective times displayed?

- **Check**: Auto-math recalculated on last change

- **Check**: updateTimingSummary() called

- **Fix**: Change a different timing to trigger recalc

### Render ignores timings?

- **Check**: `payload.video.computed_mockup_durations` in worker payload

- **Check**: Worker received `selected_mockups` array

- **Check**: Video worker logs (RENDER_DEBUG=1)

- **Fix**: Verify Python service called _compute_mockup_durations()

---

## Code Locations Quick Map

| Feature | Files |
| --------- | ------- |
| UI Controls | `video_workspace.html`, `video_cinematic.js` |
| Styling | `video_suite.css` |
| Auto-Math | `video_cinematic.js` (JS) + `video_service.py` (Python) |
| Persistence | `artwork_routes.py` (backend save) |
| Render | `render.js` (worker applies durations) |
| Normalization | `artwork_routes.py` (_normalize_video_settings) |

---

**Last Updated**: 2026-02-25
**Version**: 1.0.0
