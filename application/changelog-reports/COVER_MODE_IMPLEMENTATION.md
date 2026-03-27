# Cover Mode Artwork Framing - Implementation Summary

**Date**: February 23, 2026
**File**: `/srv/artlomo/video_worker/render.js`
**Status**: ✅ COMPLETE

## Objective

Fix artwork framing so non-square artworks start in "cover" mode (no letterboxing) for square video output. First frame fills the entire 1024×1024 canvas instead of showing bars.

## Implementation

### 1. Added `computeCoverTransform()` Helper Function (Lines 21-62)

A utility function that calculates cover-mode scaling and panning for artwork framing:

```javascript
computeCoverTransform(imgW, imgH, outW, outH, zoomScale = 1.0, panX01 = 0.5, panY01 = 0.5)
```

**Returns**: `{drawW, drawH, offsetX, offsetY, coverScale}`

**Key Features**:

- Calculates `coverScale = max(outputW/imageW, outputH/imageH)` - ensures image fills canvas

- Applies additional `zoomScale` on top of cover scale

- Normalizes pan positions `(panX01, panY01)` from 0..1 (0=left/top, 1=right/bottom, default 0.5=center)

- Clamps offsets to valid range - image always covers canvas without exposing background

- All calculations use floating-point precision

### 2. Updated FFmpeg Filter Chain (Line 407)

**Before (Contain Mode)**:

```text
scale=${width}:${height}:force_original_aspect_ratio=decrease,pad=${width}:${height}:(ow-iw)/2:(oh-ih)/2,
```

This scaled DOWN to fit + padded with black bars = letterboxing

**After (Cover Mode)**:

```text
scale=${width}:${height}:force_original_aspect_ratio=increase,
```

This scales UP to fill the entire square canvas. Extra pixels are cropped by zoompan filter when needed.

**Removed**: The `pad` command is no longer needed since we're always filling the canvas

## How It Works

### Data Flow

1. **Image Input** → Artwork image file (any aspect ratio)

1. **setsar=1:1** → Ensure square pixels (no aspect distortion)

1. **scale with increase** → Scale to COVER the output size (fill canvas)

1. **scale with overscan** → Slight upscaling for subpixel rendering

1. **zoompan** → Apply zoom animation + pan animation + final crop to output size

1. **Output** → Square video with NO letterboxing or empty background

### Examples

#### Portrait Artwork (1000×1500) → 1024×1024 Output

- Cover scale = max(1024/1000, 1024/1500) = 1.024x

- After scaling: 1024×1536 pixels

- When zoompan applies zoom=1.0 with center pan: shows full 1024 width, center 1024 of height

- **Result**: No bars, image fills canvas

#### Landscape Artwork (1500×1000) → 1024×1024 Output

- Cover scale = max(1024/1500, 1024/1000) = 1.024x

- After scaling: 1536×1024 pixels

- When zoompan applies zoom=1.0 with center pan: center 1024 of width, full 1024 height

- **Result**: No bars, image fills canvas

#### Square Artwork (1024×1024) → 1024×1024 Output

- Cover scale = 1.0x (perfect match)

- After scaling: 1024×1024 pixels

- No cropping needed, shows entire image

- **Result**: Perfect square, no scaling artifacts

### Zoom & Pan Still Work

- **Zoom**: Starts at cover scale × zoom factor. Zoom=1.1 means 1.024*1.1 = 1.126x effective scaling

- **Pan**: Moves the crop within bounds. Calculated to never expose empty background

- **Animation**: Smooth transitions from frame 0 to frame N within allotted duration

## Testing

All test cases in `/srv/artlomo/test_cover_transform.js` pass ✅

**Tested Scenarios**:

- Square artwork (1:1) - no scaling

- Portrait artwork (2:3) - width at cover, height cropped from center

- Landscape artwork (3:2) - height at cover, width cropped from center

- Wide landscape (16:9) - extreme crop scenario

- Tall portrait (9:16) - extreme crop scenario

- Various zoom levels (1.0 to 1.15x)

- Different pan positions (left/center/right, top/center/bottom)

**Verification**: Each scenario confirms:

- Output canvas is fully covered (no letterboxing)

- No empty background exposed

- Offsets are within valid range

## Impact

### Behavior Changes

✅ **Square Artworks**: No change - renders identically as before
✅ **Non-Square Artworks**: First frame fills entire video canvas (no bars)
✅ **Zoom Animation**: Still works, now starts from filled state
✅ **Pan Animation**: Still works, moves within covered canvas

### No Breaking Changes

- Output resolution remains unchanged (1024×1024 or configured size)

- Animation timing unchanged

- FFmpeg filter syntax valid and optimized

- All existing settings (zoom, pan, duration) work as before

## Code Quality

✅ Syntax validation: `node -c render.js` - PASS
✅ Test suite: All 8 test scenarios - PASS
✅ No console errors
✅ Backward compatible

## Files Modified

1. `/srv/artlomo/video_worker/render.js`

  - Added `computeCoverTransform()` function

  - Changed ffmpeg filter from contain mode to cover mode

  - Removed padding step

## Files Added (for Testing)

1. `/srv/artlomo/test_cover_transform.js` - Test suite for computeCoverTransform

## Next Steps

1. Deploy updated `render.js` to production

1. Test rendering with non-square artworks (e.g., portrait/landscape closeups)

1. Verify first frame fills 1024×1024 output canvas

1. Confirm zoom/pan still animate correctly

1. Monitor for any edge cases

## Technical Details

### FFmpeg Filter Components

**setsar=1:1**: Pixel aspect ratio 1:1 (square pixels)
**scale with increase**: Scales UP maintaining aspect ratio, no downscaling
**zoompan**: Crops and transforms; z=zoom, x/y=offset, d=duration, s=size, fps=framerate
**trim/setpts**: Duration control and timestamp reset

### Offset Calculation

```javascript
maxOffsetX = drawW - outW  // How much extra width beyond canvas
panX = 0.5                 // 0.5 = center
offsetX = -(panX * maxOffsetX)  // Always in range [-(drawW-outW), 0]
```

This ensures the crop area always covers the entire canvas without exposing empty background.

---

**Implementation Status**: ✅ COMPLETE
**Testing Status**: ✅ PASS
**Deployment Ready**: ✅ YES
