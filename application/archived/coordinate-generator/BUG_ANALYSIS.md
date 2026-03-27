# Coordinate Generator Bug Analysis

## Issue Summary

The coordinate generator is incorrectly processing v2 format coordinates, causing corner points to be swapped and creating misaligned artwork placement areas.

## Root Cause

**File:** `application/mockups/validation.py` (lines 49-52 and 56-58)

## The Bug

```python
if is_v2:
    points = [points[0], points[1], points[3], points[2]]  # SWAPS indices 2 and 3!
```

This reordering converts:

- **Input:** `[top-left, top-right, bottom-right, bottom-left]` (indices 0, 1, 2, 3)
- **After swap:** `[top-left, top-right, bottom-left, bottom-right]` (indices 0, 1, 3, 2)

## Data Flow & The Problem

### 1. **processor.js generates points correctly** (video_worker/processor.js, lines 257-263)

```javascript
zone: {
  points: [
    normalizePoint(minX, minY, width, height),  // [0] = top-left ✓
    normalizePoint(maxX, minY, width, height),  // [1] = top-right ✓
    normalizePoint(maxX, maxY, width, height),  // [2] = bottom-right ✓
    normalizePoint(minX, maxY, width, height),  // [3] = bottom-left ✓
  ],
}
```

**Output order:** `[TL, TR, BR, BL]` - This is correct visual corner order!

### 2. **validation.py incorrectly reorders for v2.0** (validation.py, lines 50-52)

```python
if is_v2:
    points = [points[0], points[1], points[3], points[2]]
```

**After swap:** `[TL, TR, BL, BR]` - Now BL and BR are swapped!

### 3. **_parse_corners_list expects [TL, TR, BL, BR]** (validation.py, lines 13-35)

This function expects:

- Index 0 = top-left
- Index 1 = top-right
- Index 2 = bottom-left (expects this position)
- Index 3 = bottom-right (expects this position)

But after it receives the swapped order, it treats:

- Index 0 = top-left ✓
- Index 1 = top-right ✓
- Index 2 = bottom-left (gets bottom-right instead) ✗
- Index 3 = bottom-right (gets bottom-left instead) ✗

## Impact

This causes the artwork placement region to have:

- ✓ Correct top edge
- ✓ Correct left edge
- ✗ Bottom-left and bottom-right corners swapped
- **Result:** Distorted or incorrectly positioned artwork zones

## The V2 Format Confusion

The swap in validation.py appears to be based on a misunderstanding of what format_version 2.0 expects:

- **Assumption:** V2 comes in as `[TL, TR, BL, BR]` and needs conversion
- **Reality:** V2 comes in as `[TL, TR, BR, BL]` which is already correct
- **The swap makes it worse, not better!**

## Solution

## Remove the incorrect reordering in validation.py

Replace:

```python
if isinstance(points, list) and len(points) == 4:
    if is_v2:
        points = [points[0], points[1], points[3], points[2]]
    parsed = _parse_corners_list(points)
```

With:

```python
if isinstance(points, list) and len(points) == 4:
    # REMOVED: The v2 reordering is incorrect - v2 format already uses correct order
    # if is_v2:
    #     points = [points[0], points[1], points[3], points[2]]
    parsed = _parse_corners_list(points)
```

## Also apply fix for corners

```python
if isinstance(corners, list) and len(corners) == 4:
    # REMOVED: The v2 reordering is incorrect - v2 format already uses correct order
    # if is_v2:
    #     corners = [corners[0], corners[1], corners[3], corners[2]]
    points = _parse_corners_list(corners)
```

## Notes

- The v2 reordering code suggests there was confusion about the coordinate format version schema
- The processor.js file generates coordinates in the correct visual order (TL, TR, BR, BL)
- The `_parse_corners_list` function follows the legacy schema which expects (TL, TR, BL, BR)
- The fix requires removing the v2-specific reordering since v2 format correctly uses the processor.js output order

## Files Involved

1. `validation.py` - Contains the bug (incorrect point reordering)
2. `processor.js` - Generates correct point order
3. `admin_services.py` - Uses the reordered points; has correct ordering functions
4. `detail_closeup_service.py` - Generates coordinates for detail crops
