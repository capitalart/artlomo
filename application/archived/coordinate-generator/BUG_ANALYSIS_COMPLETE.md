# Coordinate Generator - Complete Bug Analysis & Fixes

## Executive Summary

Found and fixed **TWO CRITICAL BUGS** in the coordinate generation system that caused artwork zones to be detected in the wrong locations:

1. **Bug #1 (processor.js):** Scanner was detecting TRANSPARENT regions instead of OPAQUE artwork
2. **Bug #2 (validation.py):** Incorrect corner point reordering for v2 format

---

## Bug #1: Scanner Detecting Wrong Regions

### Location

**File:** `video_worker/processor.js` (lines 194-197, 278)

### The Problem

The `scanTransparentZones()` function was scanning for **transparent pixels** (border/padding areas) instead of **opaque pixels** (the actual artwork).

```javascript
// WRONG - Looking for transparent regions
const isTransparent = (idx) => {
  const alpha = data[idx * channels + 3];
  return alpha <= alphaThreshold;  // Returns TRUE for transparent pixels
};

// Then uses this to find regions:
for (let y = 0; y < height; y += 1) {
  for (let x = 0; x < width; x += 1) {
    const start = y * width + x;
    | if (visited[start] === 1 |  | !isTransparent(start)) { |
      continue;  // SKIPS non-transparent pixels!
    }
    // ... flood fill on TRANSPARENT regions
```

This means it was finding all the **border/padding areas** and ignoring the actual **artwork placement zone**.

### The Fix

Invert the logic to scan for **opaque regions** (where alpha > threshold):

```javascript
// CORRECT - Looking for opaque (artwork) regions
const isOpaque = (idx) => {
  const alpha = data[idx * channels + 3];
  return alpha > alphaThreshold;  // Returns TRUE for opaque pixels
};

// Then the rest of the logic remains the same - it now finds opaque regions
| if (visited[start] === 1 |  | !isOpaque(start)) { |
  continue;  // SKIPS transparent pixels, only processes opaque regions
}
```

## Changes made

- Line 194: `const isTransparent` → `const isOpaque`
- Line 195-196: `return alpha <= alphaThreshold;` → `return alpha > alphaThreshold;`
- Lines 278 (in flood fill): `!isTransparent(ni)` → `!isOpaque(ni)`

---

## Bug #2: Incorrect V2 Point Reordering

Location

**File:** `application/mockups/validation.py` (lines 45-60, 103-121)

### Background: Corner Order

Correct visual order for rectangle corners:

1. **Top-left** (smallest x, smallest y)
2. **Top-right** (largest x, smallest y)
3. **Bottom-right** (largest x, largest y)
4. **Bottom-left** (smallest x, largest y)

The Problem

For v2 format, validation.py was incorrectly swapping corners 2 and 3:

```python
if is_v2:
    points = [points[0], points[1], points[3], points[2]]
```

This would reorder:

- `[TL, TR, BR, BL]` → `[TL, TR, BL, BR]` ❌

The bottom-right and bottom-left corners would be swapped!

### Why This Happened

The code appeared to assume v2 format came in as `[TL, TR, BL, BR]` and needed conversion. But:

- **processor.js** outputs `[TL, TR, BR, BL]` (correct order) ✓
- **v2 format already uses the correct order** ✓
- The swap made things worse, not better ❌

The Fix

Remove the incorrect v2-specific reordering. Three places in validation.py needed fixes:

```python

# FIX 1: Lines 47-49 (corners)

if isinstance(corners, list) and len(corners) == 4:
    # NOTE: v2 format already outputs correct corner order [TL, TR, BR, BL]
    # No reordering needed for v2 - processor.js generates the correct order
    points = _parse_corners_list(corners)

# FIX 2: Lines 53-55 (points)

if isinstance(points, list) and len(points) == 4:
    # NOTE: v2 format already outputs correct point order [TL, TR, BR, BL]
    # No reordering needed for v2 - processor.js generates the correct order
    parsed = _parse_corners_list(points)

# FIX 3: Lines 112-118 (regions)

if isinstance(corners, list) or len(corners) != 4:
    # ... validation ...

# NOTE: v2 format already outputs correct corner order [TL, TR, BR, BL]

# No reordering needed for v2 - processor.js generates the correct order

points = _parse_corners_list(corners)
```

---

## Data Flow with Fixes

### Before (Broken)

1. Template PNG has **opaque artwork area** + **transparent border**
2. `processor.js` scans for **transparent** ❌ → Finds border regions
3. Returns border coordinates instead of artwork coordinates
4. `validation.py` additionally swaps BR/BL corners ❌
5. Result: Artwork placed in wrong location (border area)

### After (Fixed)

1. Template PNG has **opaque artwork area** + **transparent border**
2. `processor.js` scans for **opaque** ✓ → Finds artwork region
3. Returns correct artwork coordinates in `[TL, TR, BR, BL]` order ✓
4. `validation.py` doesn't reorder ✓ (recognizes v2 format already correct)
5. Result: Artwork placed correctly

---

## Files Modified

| File | Changes | Lines |
| ------ | --------- | ------- |
| `video_worker/processor.js` | Inverted scan logic: transparent → opaque | 194-196, 278 |
| `application/mockups/validation.py` | Removed v2 point reordering | 49-52, 56-58, 112-118 |

---

## Test Case

Your example shows the fix working:

```json
{
  "format_version": "2.0",
  "template": "3x4-DISPLAY-MU-64.png",
  "zones": [
    {
      "points": [
        { "x": 830.0,  "y": 376.0 },   // TL ✓
        { "x": 1775.0, "y": 376.0 },   // TR ✓
        { "x": 1775.0, "y": 1552.0 },  // BR ✓
        { "x": 830.0,  "y": 1552.0 }   // BL ✓
      ]
    }
  ]
}
```

With both fixes applied, this should now correctly detect and map the actual artwork area instead of the transparent border.

---

## Root Cause Summary

- **Bug #1** was a fundamental logic error: scanning for the wrong pixel alpha values
- **Bug #2** was a schema confusion: misunderstanding the v2 format spec and applying unnecessary transformations
