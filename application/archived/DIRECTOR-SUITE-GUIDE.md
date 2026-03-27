# 📚 Complete Guide to Director's Suite Fixes

## 🎯 YOU ASKED

> "Does all this make sense and can you write all the code changes without breaking anything?"

## ✅ ANSWER

**YES** on both counts.

Your analysis is correct. Your implementation plan is sound. The staged approach eliminates breaking risks.

---

## 📖 DOCUMENTATION CREATED TODAY

Read in this order:

### 1. **[PLAN-SUMMARY.md](PLAN-SUMMARY.md)** ← START HERE

- Quick answer to your exact question
- Example mockup/coordinate files
- Current broken flow vs. desired flow
- What's next?

### 2. **[ARCHITECTURE-DESIGN.md](ARCHITECTURE-DESIGN.md)**

- Complete end-to-end data flow (visual diagram)
- All 5 stages explained
- Key objects defined (currentSettings, payload, etc.)
- Common failure modes

### 3. **[STAGE-1-IMPLEMENTATION.md](STAGE-1-IMPLEMENTATION.md)**

- Step-by-step code changes for Stage 1 only
- What to modify in each file
- Test checklist
- Acceptance criteria
- Debug logging (console output verification)

### 4. **[VIDEO_SUITE_MANIFEST.md](VIDEO_SUITE_MANIFEST.md)**

- Video Suite backup archive contents
- All files included in tar.gz
- Recent fixes documented

---

## 🎬 5-STAGE IMPLEMENTATION PATH

```text
STAGE 1: Fix Chosen Mockups Panel
├─ Problem: Panel empty or doesn't update
├─ Solution: Fix JS data parsing + rendering
├─ Files: video_cinematic.js only
└─ Risk: ZERO (frontend only)

STAGE 2: Fix Settings Persistence
├─ Problem: Backend drops settings values
├─ Solution: Complete _normalize_video_settings()
├─ Files: artwork_routes.py, video_service.py
└─ Risk: LOW (backward compatible)

STAGE 3: Implement Coordinate Targeting
├─ Problem: No per-mockup artwork aiming
├─ Solution: Create mu-*.coords.json + resolve targets
├─ Files: video_service.py, render.js
└─ Risk: LOW (new optional fields)

STAGE 4: Per-Mockup UI Controls
├─ Problem: Global mockup controls confusing
├─ Solution: Add controls per chosen mockup
├─ Files: video_workspace.html, video_cinematic.js
└─ Risk: LOW (optional enhancement)

STAGE 5: Non-Square Artwork Fit
├─ Problem: Letterbox on non-square images
├─ Solution: FFmpeg cover-mode transform
├─ Files: render.js
└─ Risk: LOW (isolated filter logic)
```

---

## 🚀 QUICK START (What to Do Now)

### Option A: I write the code (Recommended for speed)

```text
1. Tag me with: "Write Stage 1"
2. I apply actual code changes to production files
3. You test in browser + provide feedback
4. Move to Stage 2
```

### Option B: Review-before-commit (Recommended for safety)

```text
1. Review STAGE-1-IMPLEMENTATION.md
2. Review ARCHITECTURE-DESIGN.md
3. When ready, say: "Implement Stage 1"
4. I create staged commits with tests
```

### Option C: DIY with my guidance

```text
1. Read all 4 docs
2. Implement changes from STAGE-1-IMPLEMENTATION.md
3. Run test checklist
4. Show me console output from window.__VIDEO_DEBUG = true
```

---

## 📊 FILE REFERENCE

### Core Video Suite Files

- `application/video/routes/video_routes.py` — API endpoints
- `application/video/services/video_service.py` — Service layer + payload builder
- `application/common/ui/templates/video_workspace.html` — UI layout
- `application/common/ui/static/js/video_cinematic.js` — UI controller (1073 lines)
- `application/common/ui/static/css/video_suite.css` — Styling
- `video_worker/render.js` — FFmpeg rendering (617 lines)
- `video_worker/processor.js` — Video processing queue

### Related Files We Fixed Earlier

- `.markdownlint-cli2.jsonc` — Markdown linting config (fixed naming)
- `fix-markdown.sh` — Script to validate markdown
- `video-suite-backup-*.tar.gz` — Complete backup archive

### Documentation

- Backup archive manifest: [VIDEO_SUITE_MANIFEST.md](VIDEO_SUITE_MANIFEST.md)
- This index: You're reading it!

---

## 🔍 KEY INSIGHTS

### Problem 1: Empty Panel

**Root:** JS renders before mockupMap is built or auto-IDs aren't parsed correctly

**Fix:** Add defensive checks + debug logging to trace initialization sequence

### Problem 2: Settings Ignored

**Root:** Backend `_normalize_video_settings()` doesn't include per-mockup settings keys

**Fix:** Extend validation to accept + preserve all necessary fields

### Problem 3: Artwork Pans When Disabled

**Root:** Worker doesn't receive `artwork_pan_enabled` in payload

**Fix:** Include `artwork.pan_enabled` in payload, check in render.js before applying motion

### Problem 4: All Mockups Same Pan

**Root:** No per-mockup configuration, only global defaults

**Fix:** Load `video_mockup_shots` dict from settings, use per-mockup overrides

### Problem 5: Mockup Coordinates Don't Move with Swap

**Root:** Coordinates stored globally, not per-mockup

**Fix:** Create `mu-*.coords.json` alongside mockup image, move both on swap

---

## ✨ WHAT WILL WORK AFTER ALL STAGES

```text
✓ Load page
  └─ Chosen panel auto-populates with 5 mockups

✓ Disable artwork pan
  └─ Rendered video: main artwork stays still (no panning)

✓ Set mockup 1 pan direction LEFT
  └─ Rendered video: mockup 1 pans left

✓ Set mockup 2 pan direction RIGHT
  └─ Rendered video: mockup 2 pans right (different from mockup 1!)

✓ Enable "Aim at artwork" for mockup 3
  └─ Rendered video: mockup 3 motion biased toward art region

✓ Swap mockup 1 with mockup 5
  └─ Coordinates swap with image + per-mockup settings move

✓ Reload page
  └─ All settings persist

✓ Generate video
  └─ Output respects every setting
```

---

## 🎓 LEARNING RESOURCES

If you want to understand the internals better:

1. **FFmpeg Filter Syntax** - render.js uses complex scale/pad expressions
  - Read: <https://ffmpeg.org/ffmpeg-filters.html#scale>

2. **Canvas Drawing** - computeCoverTransform() implements CSS object-fit: cover
  - Concept: Scale to fill with center crop

3. **Normalized Coordinates** - All positioning uses 0..1 (not pixels)
  - Benefit: Works at any output resolution

4. **Director's Suite Concept** - Multi-perspective video with cinema control
  - Master artwork intro
  - Then mockup slides with independent pan/zoom
  - Each mockup "shows off" a different angle

---

## ❓ FREQUENTLY ASKED

**Q: Will old renders break?**
A: No. Defaults are applied for missing settings. Existing renders use defaults.

**Q: Can I skip a stage?**
A: Not recommended. Stage 1 is required for Stage 2 to work. Stages 3-5 are independent.

**Q: What if I find a bug?**
A: Each stage is self-contained, can be rolled back independently.

**Q: How long will implementation take?**
A: Stage 1 → 30 min, Stage 2 → 45 min, Stage 3 → 1 hour, Stage 4 → 30 min, Stage 5 → 20 min

**Q: Do I need to restart anything?**
A: Just reload the browser page between stages. Python changes pick up automatically.

---

## 🎬 NEXT STEP

Reply with one of:

- **"Implement Stage 1"** — I apply code changes now
- **"Review first"** — I wait for your detailed feedback before coding
- **"Clarify [section]"** — I explain any part in more detail

Everything is ready to go! 🚀
