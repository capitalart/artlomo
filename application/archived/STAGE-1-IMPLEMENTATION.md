# STAGE 1 IMPLEMENTATION: Fix Chosen Mockups Panel Population

**Goal:** When page loads, the "Chosen Mockups (Video Order)" panel displays 5 auto-selected mockups, OR user-selected mockups if any exist.

---

## STEP 1.1: Verify Template Data Attributes ✅

**Status:** Template is CORRECT

```html
<!-- Root element passes auto IDs as JSON -->
<div class="video-suite"
  data-auto-mockup-ids='{{ auto_mockup_ids | tojson }}'>

<!-- Each mockup card -->
<article class="storyboard-item mockup-card"
  data-storyboard-item
  data-mockup-id="{{ item.mockup_id }}"
  data-filename="{{ item.filename }}">

  <!-- Checkbox for selection -->
  <input type="checkbox" class="form-check-input"
    data-storyboard-checkbox
    value="{{ item.filename }}"
    {% if item.selected %}checked{% endif %}>

<!-- Chosen panel (empty, JS populates) -->
<div class="chosen-panel" data-chosen-panel>
  <div class="chosen-list" data-chosen-list></div>
  <div class="chosen-empty" data-chosen-empty hidden>...</div>
</div>
```

## Finding

- mockup_id uses stem (e.g., "mu-rjc-0267-05")
- filename uses full name (e.g., "mu-rjc-0267-05.jpg")
- checkbox.value = filename
- auto IDs come as JSON array of stems

---

## STEP 1.2: Frontend JS (video_cinematic.js) - Fix Data Parsing

## Current Issues

1. Auto IDs might not be parsed correctly
2. renderChosenList might not run after data is ready
3. Mock map might have mismatched IDs (filename vs stem)

**Action:** Update the following functions in `/srv/artlomo/application/common/ui/static/js/video_cinematic.js`

```javascript
// AT TOP OF IIFE - Add debug flag
window.__VIDEO_DEBUG = window.__VIDEO_DEBUG !== false; // true unless explicitly disabled

function initVideoSuite()
{
  const root = document.querySelector('[data-video-suite]');
  if (!root) {
    console.error('[Video Suite] Root element [data-video-suite] not found');
    return;
  }

  // === PARSE AUTO IDS ===
  | const autoMockupIdsRaw = root.dataset.autoMockupIds |  | '[]'; |
  let storedAutoIds = [];
  try {
    const parsed = JSON.parse(autoMockupIdsRaw);
    storedAutoIds = Array.isArray(parsed) ? parsed : [];
    if(__VIDEO_DEBUG) console.log('[Video Suite] Parsed auto IDs:', storedAutoIds);
  } catch (err) {
    console.error('[Video Suite] Failed to parse auto mockup IDs:', err, autoMockupIdsRaw);
    storedAutoIds = [];
  }

  // === BUILD MOCKUP MAP ===
  const mockupCards = Array.from(root.querySelectorAll('[data-storyboard-item]'));
  const mockupMap = new Map();

  mockupCards.forEach((card) => {
    // Use data-mockup-id (stem, e.g., "mu-rjc-0267-05")
    | const id = (card.dataset.mockupId |  | '').trim(); |

    if (!id) {
      if(__VIDEO_DEBUG) console.warn('[Video Suite] Card missing data-mockup-id:', card);
      return;
    }

    mockupMap.set(id, {
      id,
      card,
      checkbox: card.querySelector('[data-storyboard-checkbox]'),
      | thumbUrl: card.dataset.thumbUrl |  | '', |
      | fullUrl: card.dataset.fullUrl |  | '', |
      label: id, // use ID as display label
    });
  });

  if(__VIDEO_DEBUG) {
    console.log('[Video Suite] mockupCards:', mockupCards.length);
    console.log('[Video Suite] mockupMap size:', mockupMap.size);
    console.log('[Video Suite] mockupMap keys:', Array.from(mockupMap.keys()).slice(0, 5));
  }

  // === GET SELECTED IDS ===
  const getSelectedIds = () => {
    return mockupCards
      .filter((card) => {
        const checkbox = card.querySelector('[data-storyboard-checkbox]');
        return checkbox && checkbox.checked;
      })
      .map((card) => {
        | const id = (card.dataset.mockupId |  | '').trim(); |
        return id && mockupMap.has(id) ? id : null;
      })
      .filter(Boolean);
  };

  // === GET AUTO IDS (with fallback) ===
  const getAutoIds = () => {
    // Filter stored auto IDs to only ones we have mockups for
    const filtered = storedAutoIds.filter((id) => mockupMap.has(id));

    if (filtered.length > 0) {
      if(__VIDEO_DEBUG) console.log('[Video Suite] Using stored auto IDs:', filtered);
      return filtered;
    }

    // Fallback: take first 5 from mockupMap
    const all = Array.from(mockupMap.keys());
    const selected = all.slice(0, 5);

    if(__VIDEO_DEBUG) console.log('[Video Suite] Auto-selecting first 5:', selected);

    if (!selected.length && __VIDEO_DEBUG) {
      console.warn('[Video Suite] No mockups available for auto-selection!', {
        mockupCardsCount: mockupCards.length,
        mockupMapSize: mockupMap.size,
        storedAutoIdsCount: storedAutoIds.length,
      });
    }

    return selected;
  };

  // === RENDER CHOSEN LIST ===
  const chosenList = root.querySelector('[data-chosen-list]');
  const chosenPanel = root.querySelector('[data-chosen-panel]');
  const chosenEmpty = root.querySelector('[data-chosen-empty]');
  const chosenNoMockups = root.querySelector('[data-chosen-no-mockups]');

  const renderChosenList = () => {
    if (!chosenList) {
      console.error('[Video Suite] Missing [data-chosen-list]');
      return;
    }

    // Early exit: no mockups at all
    if (mockupMap.size === 0) {
      if(__VIDEO_DEBUG) console.log('[Video Suite] No mockups available');
      chosenList.innerHTML = '';
      if (chosenEmpty) chosenEmpty.hidden = true;
      if (chosenNoMockups) chosenNoMockups.hidden = false;
      return;
    }

    // Hide no-mockups message since we have mockups
    if (chosenNoMockups) chosenNoMockups.hidden = true;

    // Determine what to display
    const selectedIds = getSelectedIds();
    const autoMode = selectedIds.length === 0; // if nothing selected, use auto
    const idsToDisplay = autoMode ? getAutoIds() : selectedIds;

    if(__VIDEO_DEBUG) {
      console.log('[Video Suite] renderChosenList:', {
        selectedCount: selectedIds.length,
        autoMode,
        displayCount: idsToDisplay.length,
      });
    }

    // Clear list
    chosenList.innerHTML = '';

    // Update header
    const chosenTitle = root.querySelector('[data-chosen-title]');
    const chosenSubtitle = root.querySelector('[data-chosen-subtitle]');

    if (chosenTitle) {
      chosenTitle.textContent = autoMode
        ? 'Auto-selected (Drag to set order)'
        : 'Chosen Mockups (Video Order)';
    }
    if (chosenSubtitle) {
      chosenSubtitle.textContent = autoMode
        ? 'Drag to set preferred order.'
        : 'Drag to reorder.';
    }

    // Show empty state if no IDs
    if (!idsToDisplay.length) {
      if (chosenEmpty) chosenEmpty.hidden = false;
      if(__VIDEO_DEBUG) console.log('[Video Suite] No mockups to display - showing empty state');
      return;
    }

    if (chosenEmpty) chosenEmpty.hidden = true;

    // Build items
    idsToDisplay.forEach((id, index) => {
      const info = mockupMap.get(id);
      if (!info) {
        if(__VIDEO_DEBUG) console.warn('[Video Suite] Mockup not in map:', id);
        return;
      }

      const item = document.createElement('div');
      item.className = 'chosen-item';
      item.setAttribute('draggable', 'true');
      item.dataset.mockupId = id;

      // Thumbnail
      const thumb = document.createElement('img');
      thumb.src = info.thumbUrl;
      thumb.alt = `Mockup ${id}`;
      thumb.className = 'chosen-thumb';
      item.appendChild(thumb);

      // Badge with order number
      const badge = document.createElement('span');
      badge.className = 'chosen-badge';
      badge.dataset.orderBadge = '';
      badge.textContent = String(index + 1);
      item.appendChild(badge);

      // Label
      const label = document.createElement('span');
      label.className = 'chosen-label';
      label.textContent = id;
      item.appendChild(label);

      chosenList.appendChild(item);
    });

    if(__VIDEO_DEBUG) {
      console.log('[Video Suite] Rendered', idsToDisplay.length, 'mockups');
    }
  };

  // === ATTACH CHECKBOX LISTENERS ===
  mockupCards.forEach((card) => {
    const checkbox = card.querySelector('[data-storyboard-checkbox]');
    if (checkbox && !checkbox.dataset.listenerAttached) {
      checkbox.dataset.listenerAttached = 'true';
      checkbox.addEventListener('change', () => {
        if(__VIDEO_DEBUG) console.log('[Video Suite] Checkbox changed');
        renderChosenList(); // Re-render on any change
      });
    }
  });

  // === INITIAL RENDER ===
  if(__VIDEO_DEBUG) console.log('[Video Suite] Performing initial render...');
  renderChosenList();

  if(__VIDEO_DEBUG) console.log('[Video Suite] Initialization complete');
}

// Call on DOMContentLoaded
document.addEventListener('DOMContentLoaded', initVideoSuite);
```

---

## STEP 1.3: Verify Backend is Passing Auto IDs

**File:** `/srv/artlomo/application/video/routes/video_routes.py`

## Current code (SHOULD ALREADY EXIST)

```python
auto_mockup_ids: list[str] = []
try:
    auto_paths = svc._get_ordered_mockup_paths(slug_clean, max_count=MAX_MOCKUP_SLIDES)
    auto_mockup_ids = [path.stem for path in auto_paths]  # ← MUST USE .stem (base name without ext)
except Exception:
    auto_mockup_ids = []

return render_template(
    "video_workspace.html",
    ...
    auto_mockup_ids=auto_mockup_ids,  # ← MUST PASS IT
)
```

## Verify

```bash
python3 << 'EOF'
from pathlib import Path
p = Path("/srv/artlomo/application/lab/processed/rjc-0267/mockups/mu-rjc-0267-05.jpg")
print("Path:", p)
print("name:", p.name)       # mu-rjc-0267-05.jpg
print("stem:", p.stem)       # mu-rjc-0267-05 ← USE THIS
print("suffix:", p.suffix)   # .jpg
EOF
```

---

## TEST CHECKLIST ✅

After implementing these changes:

1. **Open browser DevTools** (F12 → Console)
2. **Type:** `window.__VIDEO_DEBUG = true; location.reload();`
3. **Watch console** for these messages in order:

```text
✓ [Video Suite] Parsed auto IDs: ["mu-rjc-0267-01", "mu-rjc-0267-02", ...]
✓ [Video Suite] mockupCards: 20
✓ [Video Suite] mockupMap size: 20
✓ [Video Suite] mockupMap keys: ["mu-rjc-0267-01", "mu-rjc-0267-02", ...]
✓ [Video Suite] renderChosenList: {selectedCount: 0, autoMode: true, displayCount: 5}
✓ [Video Suite] Rendered 5 mockups
✓ [Video Suite] Initialization complete
```

1. **Visually verify:**
  - [ ] "Chosen Mockups" panel shows 5 thumbnails with numbers (1-5)
  - [ ] Clicking checkbox on a mockup → panel updates immediately
  - [ ] Clicking 5 checkboxes → chosen panel shows exactly those 5
  - [ ] Reload page → chosen panel repopulates with auto 5 (since you deselected)

---

## ACCEPTANCE CRITERIA

- ✅ No console errors
- ✅ Panel shows 5 auto mockups on page load
- ✅ Checkboxes immediately update panel
- ✅ Settings reload after browser refresh
