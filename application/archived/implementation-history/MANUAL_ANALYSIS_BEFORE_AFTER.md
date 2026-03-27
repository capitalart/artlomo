# Manual Analysis Page - Before & After Comparison

## Layout Structure

### BEFORE: Bootstrap Card Layout

```text
┌─────────────────────────────────────────┐
│ Manual Analysis Workspace               │
│ Slug: test-slug                        │
├─────────────────────────────────────────┤
│ [Export] [Mockup Controls Panel]        │
├─────────────────────────────────────────┤
│ Left Pane (card)          Right Pane    │
│ ┌──────────────────┐    (card)          │
│ │ Artwork preview  │    ┌─────────────┐ │
│ │ (THUMB image)    │    │ Title       │ │
│ │                  │    │ SKU         │ │
│ ├──────────────────┤    │ Description │ │
│ │ Mockups (mt-3)   │    │ Tags        │ │
│ │ [Grid Items]     │    │ Materials   │ │
│ │                  │    │ Price       │ │
│ │                  │    │ Category    │ │
│ │                  │    │ SEO Filename│ │
│ │                  │    └─────────────┘ │
│ └──────────────────┘    [Save][Lock]    │
│                         [Delete]        │
└─────────────────────────────────────────┘
```

## Issues

- ❌ Inconsistent styling vs OpenAI/Gemini pages
- ❌ Uses Bootstrap card classes (forbidden per architecture)
- ❌ Uses analyse_url but displays thumb_url
- ❌ No detail closeup section
- ❌ No custom context fields
- ❌ No field tools (copy buttons, counters)
- ❌ Basic input fields without styling consistency

---

### AFTER: Artlomo Workstation Layout

```text
┌──────────────────────────────────────────────────────────┐
│ Manual Analysis (h1)                                     │
│ Slug: test-slug (p)                                      │
├──────────────────────────────────────────────────────────┤
│ artlomo-workstation (flex layout)                        │
├──────────────────┬───────────────────────────────────────┤
│ artlomo-         │ artlomo-workstation__right             │
│ workstation__    │ (artlomo-workstation__scroll)          │
│ left             │                                        │
│                  │ ┌─────────────────────────────────┐  │
│ artlomo-panel    │ │ Analysis: Manual                │  │
│ [Export]         │ └─────────────────────────────────┘  │
│ [Admin Export]   │                                       │
│                  │ artlomo-panel [Actions]              │
│ artlomo-panel    │ [OpenAI Reanalyse]                  │
│ Artwork preview  │ [Gemini Reanalyse]                  │
│ [ANALYSE image]  │ [Generate Mockups]                  │
│                  │                                       │
│ artlomo-panel    │ Detected Ratio: 4:5                 │
│ ★ Detail Closeup │                                       │
│ [Preview image]  │ artlomo-panel [Metadata Editor]      │
│ [Edit]  [Create] │ Title: [Input with counter]         │
│                  │ Description: [Textarea with counter] │
│ artlomo-panel    │                                       │
│ Mockups          │ artlomo-panel [Metadata & Keywords]  │
│ [Grid Items]     │ Tags: [Textarea with copy button]   │
│                  │ Materials: [Textarea with copy]      │
│                  │                                       │
│                  │ ★ artlomo-panel [Custom Context]    │
│                  │ Location: [Read-only field]         │
│                  │ Sentiment: [Read-only field]        │
│                  │ Original Prompt: [Read-only area]   │
│                  │                                       │
│                  │ [Save Changes] [Lock Artwork]       │
│                  │                                       │
└──────────────────┴───────────────────────────────────────┘
```

## Improvements

- ✅ Matches OpenAI/Gemini workstation pattern
- ✅ Uses artlomo design system (no Bootstrap)
- ✅ Uses analyse_url for primary preview
- ✅ **NEW:** Detail Closeup section with edit/create options
- ✅ **NEW:** Custom Context section (read-only)
- ✅ **NEW:** Field tools (copy buttons, counters, hints)
- ✅ Consistent artlomo-panel styling throughout
- ✅ Proper two-column responsive layout
- ✅ Left pane remains scrollable independently
- ✅ Right pane uses artlomo-workstation__scroll

---

## Field-by-Field Comparison

### Title Field

## BEFORE

```html
<div class="artlomo-data-card mb-3">
  <label class="form-label" for="title">Title</label>
  <input class="form-control" id="title" name="title" type="text"
         value="{{ manual_data.title }}" autocomplete="off">
</div>
```

## AFTER

```html
<div class="artlomo-data-card" style="margin-bottom: 12px;">
  <label class="form-label" for="analysis-title">Title</label>
  <input class="form-control" id="analysis-title" name="title" type="text"
         value="{{ listing_doc.get('title') or manual_data.title or '' }}"
         autocomplete="off">
  <div class="analysis-field-tools" aria-label="Title tools">
    <div class="analysis-field-meta">
      <div class="analysis-counter"
           data-counter-for="analysis-title"
           data-max-chars="140"
           data-max-words="13">
        Characters: 0 / 140 | Words: 0 / 13
      </div>
      <div class="analysis-hint">
        Etsy Tip: 140 chars max, but aim for ~13-14 words
        for the best SEO balance.
      </div>
    </div>
    <button class="artlomo-btn analysis-copy-btn" type="button"
            data-copy-target="analysis-title" aria-label="Copy title">
      <span aria-hidden="true">📋</span>
      COPY
    </button>
  </div>
</div>
```

## Changes

- Added character/word counter
- Added Etsy SEO hint
- Added copy button
- Better styling consistency
- Uses `listing_doc` with fallback chain

---

### Tags Field

BEFORE

```html
<div class="artlomo-data-card mb-3">
  <label class="form-label" for="tags">Tags</label>
  <input class="form-control" id="tags" name="tags" type="text"
         value="{{ manual_data.tags }}" autocomplete="off">
</div>
```

AFTER

```html
<div class="artlomo-data-card metadata-hub__field"
     style="margin-bottom: 12px;">
  <label class="form-label" for="analysis-tags">Tags</label>
  <textarea class="form-control metadata-hub__input"
            id="analysis-tags" name="tags"
            rows="3" autocomplete="off"
            data-sanitize-field>
    {{ (listing_doc.get('tags') or manual_data.tags or '')|string }}
  </textarea>
  <div class="analysis-field-tools" aria-label="Tags tools">
    <div class="analysis-field-meta">
      <small class="text-muted">
        Comma-separated. Hyphens auto-removed on save.
      </small>
    </div>
    <button class="artlomo-btn analysis-copy-btn"
            type="button"
            data-copy-target="analysis-tags"
            aria-label="Copy tags">
      <span aria-hidden="true">📋</span>
      COPY
    </button>
  </div>
</div>
```

Changes

- Changed from single-line input to textarea (3 rows)
- Added helpful hint text
- Added copy button
- Added `data-sanitize-field` attribute
- Consistent field styling

---

### **NEW: Custom Context Section**

## AFTER (New)

```html
{% if seed_context.location or seed_context.sentiment or seed_context.original_prompt %}
  <div class="artlomo-panel" role="group"
       aria-label="Custom context information"
       style="margin-bottom: 12px;">
    <h3 class="artlomo-panel__title" style="margin-bottom: 12px;">
      Custom Context
    </h3>

    {% if seed_context.location %}
      <div class="artlomo-data-card metadata-hub__field"
           style="margin-bottom: 12px;">
        <label class="form-label" for="context-location">
          Location / Country
        </label>
        <input class="form-control" id="context-location" type="text"
               value="{{ seed_context.location }}" disabled readonly>
      </div>
    {% endif %}

    {% if seed_context.sentiment %}
      <div class="artlomo-data-card metadata-hub__field"
           style="margin-bottom: 12px;">
        <label class="form-label" for="context-sentiment">
          Sentiment / Mood
        </label>
        <input class="form-control" id="context-sentiment" type="text"
               value="{{ seed_context.sentiment }}" disabled readonly>
      </div>
    {% endif %}

    {% if seed_context.original_prompt %}
      <div class="artlomo-data-card metadata-hub__field"
           style="margin-bottom: 12px;">
        <label class="form-label" for="context-prompt">
          Original Generation Prompt
        </label>
        <textarea class="form-control" id="context-prompt" rows="3"
                  disabled readonly>{{ seed_context.original_prompt }}</textarea>
        <small class="text-muted" style="display: block; margin-top: 4px;">
          Internal context used for AI analysis guidance.
        </small>
      </div>
    {% endif %}
  </div>
{% endif %}
```

## Features

- Conditionally displays only if fields exist
- Read-only inputs (cannot edit in manual workspace)
- Explanatory text for original_prompt
- Consistent styling with other fields
- Proper accessibility (labels, aria attributes)

---

### **NEW: Detail Closeup Section**

AFTER (New)

```html
{% if has_detail_closeup %}
  <div class="artlomo-panel">
    <h2>Detail Closeup</h2>
    <div class="art-card manual-preview"
         data-analyse-src="{{ detail_closeup_url }}"
         data-fallback-src="{{ detail_closeup_url }}"
         data-title="Detail Closeup - {{ listing_doc.get('title') or slug }}"
         data-artist=""
         data-details="Detail closeup crop for {{ slug }}">
      <img src="{{ detail_closeup_url }}" alt="Detail closeup"
           class="manual-preview__image">
    </div>
    <a href="{{ url_for('artwork.detail_closeup_editor', slug=slug) }}"
       class="artlomo-btn"
       style="margin-top: 8px; display: block; text-align: center;">
      Edit Detail Closeup
    </a>
  </div>
{% else %}
  <div class="artlomo-panel">
    <h2>Detail Closeup</h2>
    <div class="manual-preview__placeholder">No detail closeup yet.</div>
    <a href="{{ url_for('artwork.detail_closeup_editor', slug=slug) }}"
       class="artlomo-btn"
       style="margin-top: 8px; display: block; text-align: center;">
      Create Detail Closeup
    </a>
  </div>
{% endif %}
```

Features

- Two conditional states (has/no crop)
- Uses art-card for modal integration
- Edit/Create buttons link to editor
- Placeholder text when not yet created
- Consistent styling with other panels

---

## Data Source Changes

### manual_data Dictionary Augmentation

## Manual Route (manual_routes.py)

```python
BEFORE
manual_data = load_manual_listing(slug)

# Contains: slug, sku, title, description, tags, materials, price, category, seo_filename

AFTER
manual_data = load_manual_listing(slug)

# [existing data above]

# NEW: Load seed_context

processed_dir = Path(cfg["LAB_PROCESSED_DIR"]) / slug
seed_context = {}
if processed_dir.exists():
    seed_context_file = processed_dir / "seed_context.json"
    if seed_context_file.exists():
        with open(seed_context_file, "r") as f:
            seed_context = json.load(f)

# NEW: Check detail closeup

detail_closeup_service = DetailCloseupService()
has_detail_closeup = detail_closeup_service.has_detail_closeup(slug)
detail_closeup_url = url_for('artwork.detail_closeup_view', slug=slug) if has_detail_closeup else None

# NEW: Add to manual_data

manual_data['seed_context'] = seed_context
manual_data['has_detail_closeup'] = has_detail_closeup
manual_data['detail_closeup_url'] = detail_closeup_url
```

---

## CSS Classes Used

| Class | Usage | Source |
| ------- | ------- | -------- |
| `artlomo-admin-surface` | Outer container | Common |
| `artlomo-workstation` | Two-column flex layout | Common |
| `artlomo-workstation__left` | Left pane (visuals) | Common |
| `artlomo-workstation__right` | Right pane (data) | Common |
| `artlomo-workstation__scroll` | Right pane scrolling container | Common |
| `artlomo-panel` | Styled content section | Common |
| `artlomo-panel__title` | Section heading | Common |
| `artlomo-panel__sub` | Subsection label | Common |
| `artlomo-panel__row` | Horizontal row within panel | Common |
| `artlomo-data-card` | Field container | Common |
| `artlomo-btn` | Action button | Common |
| `artlomo-btn--primary` | Primary button variant | Common |
| `artlomo-btn--secondary` | Secondary button variant | Common |
| `analysis-field-tools` | Field utilities (copy, counter) | Analysis pages |
| `analysis-field-meta` | Counter/hint display | Analysis pages |
| `analysis-counter` | Character/word counter | Analysis pages |
| `analysis-hint` | Field hint text | Analysis pages |
| `analysis-copy-btn` | Copy button | Analysis pages |
| `metadata-hub` | Metadata section container | Analysis pages |
| `metadata-hub__field` | Metadata field wrapper | Analysis pages |
| `metadata-hub__input` | Metadata field input | Analysis pages |
| `art-card` | Artwork preview card | Common |
| `manual-preview` | Artwork preview variant | Manual |
| `manual-preview__image` | Preview image | Manual |
| `manual-preview__placeholder` | Empty state text | Manual |
| `mockup-card` | Mockup grid item | Mockups |
| `form-label` | Input label | Common |
| `form-control` | Input/textarea | Common |
| `form-select` | Select dropdown | Common |

---

## Accessibility Improvements

- ✅ Proper `role` attributes on sections
- ✅ `aria-label` descriptions for all regions
- ✅ `aria-label` on buttons (Copy, Edit, Create)
- ✅ `for` attributes on form labels
- ✅ Semantic HTML headings (h1, h2, h3)
- ✅ Placeholder text for empty states
- ✅ Read-only context fields prevent accidental edits

---

## Summary of Changes

| Aspect | BEFORE | AFTER | Status |
| -------- | -------- | ------- | -------- |
| Layout Framework | Bootstrap cards | Artlomo workstation | ✅ Updated |
| Imagery | THUMB (small) | ANALYSE (large) | ✅ Fixed |
| Detail Closeup | ❌ Missing | ✅ Full section | ✅ Added |
| Custom Fields | ❌ Missing | ✅ Location, Sentiment, Prompt | ✅ Added |
| Field Tools | ❌ Basic inputs | ✅ Counters, copy, hints | ✅ Enhanced |
| Styling | Inconsistent | Consistent with review pages | ✅ Unified |
| Accessibility | Basic | Full ARIA labels | ✅ Improved |
| Data Loading | Basic | Seed context + detail closeup | ✅ Enhanced |

---

**All updates complete and verified!** ✅
