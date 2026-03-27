# Per-Mockup Zoom Toggle - Quick Start Guide

## What's New?

Each mockup in your Director's Suite now has an independent **Zoom** toggle, allowing you to disable zoom animation on specific mockups while others zoom normally.

---

## How to Use

### Step 1: Select Mockups

1. Open Director's Suite
2. Check the mockups you want in your video
3. They appear in the **"Chosen Mockups (Video Order)"** panel

### Step 2: Configure Zoom Per Mockup

In the Chosen Mockups panel, each mockup row shows:

```text
[Thumbnail] [Pan Toggle] [Pan Direction] [Zoom Toggle] [Remove]
```

- **Pan Toggle**: Enable/disable panning (movement)
- **Pan Direction**: Direction of pan (up/down/left/right/none)
- **Zoom Toggle**: Enable/disable zoom animation ← **NEW**

### Step 3: Toggle Zoom

- **Checkbox checked** (default): Mockup zooms during playback
- **Checkbox unchecked**: Mockup stays at constant scale (no zoom)

### Step 4: Save & Render

1. Click "Save Settings" (saves your zoom preferences)
2. Click "Start Render" (generates video with your zoom settings)
3. Play video and verify

---

## Examples

### Example 1: All Zoom (Default)

```text
Mockup 1: Zoom ☑ Pan ☑ (Direction: Up)
Mockup 2: Zoom ☑ Pan ☑ (Direction: Right)
Mockup 3: Zoom ☑ Pan ☑ (Direction: Down)
```

**Result**: All three mockups zoom from 1.0 → 1.1 (or configured intensity) during playback

### Example 2: Mixed Zoom

```text
Mockup 1: Zoom ☑ Pan ☑ (Direction: Up)      ← Zooms in
Mockup 2: Zoom ☐ Pan ☑ (Direction: Right)   ← NO ZOOM, just pans
Mockup 3: Zoom ☑ Pan ☑ (Direction: Down)    ← Zooms in
```

**Result**: Mockup 2 stays at constant size while others zoom around it

### Example 3: Zoom Only (No Pan)

```text
Mockup 1: Zoom ☑ Pan ☐ (Direction: None)
Mockup 2: Zoom ☑ Pan ☐ (Direction: None)
```

**Result**: Both mockups zoom in place without panning

### Example 4: Static (No Zoom, No Pan)

```text
Mockup 1: Zoom ☐ Pan ☐ (Direction: None)
```

**Result**: Mockup 1 stays completely static (constant scale, centered)

---

## Common Questions

**Q: Does turning off Zoom affect my Pan settings?**
A: No! Zoom and Pan are independent. You can have any combination:

- Zoom ON + Pan ON ✓
- Zoom ON + Pan OFF ✓
- Zoom OFF + Pan ON ✓
- Zoom OFF + Pan OFF ✓

**Q: What if I don't toggle it?**
A: By default, Zoom is **enabled** (checked). All mockups will zoom unless you explicitly disable it.

**Q: Can I toggle zoom for multiple mockups at once?**
A: Not yet! Toggle each one individually. Future versions may support bulk operations.

**Q: Do my zoom settings persist?**
A: Yes! When you reload the page, your zoom toggles remain checked/unchecked as you set them.

**Q: How does this affect my overall zoom_intensity setting?**
A: The global `mockup_zoom_intensity` (e.g., 1.1) is the **maximum zoom** applied to each mockup. Per-mockup zoom toggle only **enables/disables** this animation:

- If mockup zoom toggle is ON: applies zoom_intensity (e.g., 1.0 → 1.1)
- If mockup zoom toggle is OFF: stays at 1.0 (no zoom)

**Q: Can I set different zoom amounts per mockup?**
A: Not yet! The slider "Mockup Zoom Intensity" applies to all mockups equally. The per-mockup toggle only enables/disables this global setting for each mockup.

---

## Visual Guide

### Mockup Row Anatomy

```text
┌─────────────────────────────────────────────────────────┐
│ [1] [Thumbnail: 88×88px] │  Controls  │ [×] Remove     │
│                          ├─ ☑ Pan toggle                │
│                          ├─ ▼ Pan direction (Drop)     │
│                          ├─ ☑ Zoom toggle ← NEW        │
│                          │                             │
└─────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

**Problem**: Zoom toggle stays checked even though I unchecked it
**Solution**: Refresh the page. The toggle should reflect your last saved state.

**Problem**: All mockups still zoom even with toggle OFF
**Solution**: Check if global `mockup_zoom_intensity` is set to 1.0 (no zoom). The per-mockup toggle only controls whether to apply the global intensity.

**Problem**: I don't see the zoom checkbox
**Solution**: Make sure your mockups are selected (in the "Chosen Mockups" panel). Unchecking a mockup removes it from the video.

**Problem**: Zoom setting not saving
**Solution**: Make sure you see "Settings saved" message after toggling. Check browser console for errors (F12).

---

## Tips & Tricks

💡 **Tip 1: Emphasis without zoom**
Use Pan ON + Zoom OFF for a mockup to draw attention through movement without the zoom effect. Great for highlighting specific details.

💡 **Tip 2: Slow motion effect**
Turn OFF zoom on every other mockup to create a "pulsing" effect where composition alternates between zoomed and static.

💡 **Tip 3: Detail showcase**
Set first mockup to Zoom OFF + Pan ON, then rest to Zoom ON to emphasize the opening composition.

💡 **Tip 4: Reset all**
Want all mockups to zoom? Leave all zoom checkboxes checked (default state).

---

## Data Storage

Your zoom preferences are stored in:

```text
artwork_data.json
└─ video_suite
   └─ video_mockup_shots (array)
      └─ { id, pan_enabled, pan_direction, zoom_enabled }
```

Example:

```json
{
  "video_mockup_shots": [
    { "id": "mu-test-01", "pan_enabled": true, "pan_direction": "up", "zoom_enabled": true },
    { "id": "mu-test-02", "pan_enabled": true, "pan_direction": "right", "zoom_enabled": false },
    { "id": "mu-test-03", "pan_enabled": false, "pan_direction": "none", "zoom_enabled": true }
  ]
}
```

---

## Debug Mode

For technical troubleshooting, enable debug logging:

```bash

# In terminal:

export RENDER_DEBUG=1
npm run render

# View output to see zoom flags per slide:

# [DEBUG] Slide 1 (mockupIndex 0): { ... mockupZoomEnabled: false, ... }

# [DEBUG] Slide 2 (mockupIndex 1): { ... mockupZoomEnabled: true, ... }

```

---

**Feature Status**: ✅ Fully implemented and ready to use
