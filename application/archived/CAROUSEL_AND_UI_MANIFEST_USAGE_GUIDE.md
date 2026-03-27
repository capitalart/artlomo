# Asset Manifest Usage Guide: Implementation for All UI Components

**Date:** March 3, 2026
**Purpose:** Guide for updating all UI components to use the SKU-assets.json manifest as the single source of truth.

---

## Quick Start: Three Key Rules

1. **Always fetch the manifest first** — Load the asset manifest before accessing any files
2. **Use manifest paths** — Reference files via their paths declared in the manifest, not hardcoded patterns
3. **Never assume naming** — Don't guess filenames; read them from the manifest

---

## Backend Endpoint: Asset Manifest API

### Endpoint

```text
GET /artwork/<slug>/assets
```

### Response Format

```json
{
  "sku": "RJC-0279",
  "slug": "rjc-0279",
  "version": 2,
  "files": {
    "master": "rjc-0279-MASTER.jpg",
    "thumb": "rjc-0279-THUMB.jpg",
    "analyse": "rjc-0279-ANALYSE.jpg",
    "closeup_proxy": "rjc-0279-CLOSEUP-PROXY.jpg",
    "metadata": "rjc-0279-metadata.json",
    "qc": "rjc-0279-qc.json",
    "status": "status.json",
    "processing_status": "processing_status.json",
    "metadata_openai": "metadata_openai.json",
    "seo_download": "RJC-0279-Ochre-Songlines-Abstract-Australia.jpg"
  },
  "directories": {
    "mockups": "mockups"
  },
  "mockups": {
    "dir": "mockups",
    "assets": {
      "01": {
        "slot": 1,
        "template_slug": "beach-sunset",
        "composite": "composites/mu-rjc-0279-01.jpg",
        "thumb": "thumbs/mu-rjc-0279-01-THUMB.jpg",
        "category": "product"
      },
      "02": {
        "slot": 2,
        "template_slug": "gallery-wall",
        "composite": "composites/mu-rjc-0279-02.jpg",
        "thumb": "thumbs/mu-rjc-0279-02-THUMB.jpg",
        "category": "interior-design"
      }
    }
  }
}
```

---

## File Serving Endpoint

All files should be served through:

```text
/artwork/<slug>/asset/<relative-path>
```

Where `<relative-path>` is validated against the manifest.

Example:

- `/artwork/rjc-0279/asset/rjc-0279-MASTER.jpg`
- `/artwork/rjc-0279/asset/mockups/composites/mu-rjc-0279-01.jpg`

---

## Component: Carousel Modal (Analysis Workspace)

**File:** `application/common/ui/templates/analysis_workspace.html`

### Current Pattern (NEEDS UPDATE)

```html
<img id="modalImg" src="{{ analyse_url }}" alt="...">
```

### New Pattern: Manifest-Driven

```html
<script>
// Load asset manifest when page initializes
const AssetManifest = {};

async function initializeAssetManifest(slug) {
  try {
    const response = await fetch(`/artwork/${slug}/assets`);
    if (!response.ok) throw new Error('Failed to load manifest');
    Object.assign(AssetManifest, await response.json());
  } catch (error) {
    console.error('Asset manifest load failed:', error);
  }
}

// Call on page load
document.addEventListener('DOMContentLoaded', () => {
  const slug = '{{ slug }}';
  initializeAssetManifest(slug);
});
</script>

<!-- IMAGE DISPLAY -->
<div id="artworkContainer">
  <img
    id="primaryImage"
    alt="Primary Artwork"
    onload="handleImageLoaded()"
  />
</div>

<!-- MODAL CAROUSEL -->
<div id="artPreviewModal" class="modal-gallery hidden">
  <img class="modal-image" id="modalImg" alt="Gallery Preview" />
  <button class="carousel-prev" onclick="previousImage()">❮</button>
  <button class="carousel-next" onclick="nextImage()">❯</button>
</div>

<script>
const slug = '{{ slug }}';
let currentImageIndex = 0;
let imageUrls = [];

async function loadCarouselImages() {
  await initializeAssetManifest(slug);

  // Collect all displayable images from manifest
  imageUrls = [];

  // Add preview image
  if (AssetManifest.files?.analyse) {
    imageUrls.push({
      src: `/artwork/${slug}/asset/${AssetManifest.files.analyse}`,
      type: 'analyse',
      label: 'Analysis View'
    });
  }

  // Add master image
  if (AssetManifest.files?.master) {
    imageUrls.push({
      src: `/artwork/${slug}/asset/${AssetManifest.files.master}`,
      type: 'master',
      label: 'Master Image'
    });
  }

  // Add all mockups
  if (AssetManifest.mockups?.assets) {
    Object.entries(AssetManifest.mockups.assets).forEach(([slot, entry]) => {
      if (entry.composite) {
        imageUrls.push({
          src: `/artwork/${slug}/asset/${entry.composite}`,
          type: 'mockup',
          slot: slot,
          template: entry.template_slug,
          label: `Mockup ${slot}: ${entry.template_slug}`
        });
      }
    });
  }

  // Display first image
  if (imageUrls.length > 0) {
    displayImage(0);
  }
}

function displayImage(index) {
  if (index < 0) index = imageUrls.length - 1;
  if (index >= imageUrls.length) index = 0;

  currentImageIndex = index;
  const img = document.getElementById('modalImg');
  img.src = imageUrls[index].src;
  img.alt = imageUrls[index].label;

  // Update indicators
  updateCarouselIndicators();
}

function nextImage() {
  displayImage(currentImageIndex + 1);
}

function previousImage() {
  displayImage(currentImageIndex - 1);
}

function openModal() {
  const modal = document.getElementById('artPreviewModal');
  if (imageUrls.length === 0) {
    loadCarouselImages().then(() => {
      modal.classList.remove('hidden');
    });
  } else {
    modal.classList.remove('hidden');
  }
}

// Launch when page ready
document.addEventListener('DOMContentLoaded', loadCarouselImages);
</script>
```

---

## Component: Mockup Gallery (Video Suite)

**File:** `application/video/routes/video_routes.py` and related templates

### Backend Changes

```python
from application.mockups.assets_index import AssetsIndex
from application.mockups.artwork_index import resolve_artwork

@video_bp.route('/<slug>/mockups', methods=['GET'])
def list_mockups(slug: str):
    """List all mockups for an artwork from asset manifest."""
    try:
        cfg = current_app.config
        artwork_dir, assets_path, sku = resolve_artwork(
            _resolve_sku_for_slug(Path(cfg["LAB_PROCESSED_DIR"]) / slug),
            master_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
            processed_root=Path(cfg["LAB_PROCESSED_DIR"]),
        )

        assets_index = AssetsIndex(artwork_dir, assets_path)
        assets_doc = assets_index.load()

        mockups_data = {
            "slug": slug,
            "sku": sku,
            "mockups": []
        }

        for slot_key, slot_entry in sorted(assets_doc.get("mockups", {}).get("assets", {}).items()):
            mockups_data["mockups"].append({
                "slot": int(slot_key),
                "thumbnail": slot_entry.get("thumb"),
                "composite": slot_entry.get("composite"),
                "template_slug": slot_entry.get("template_slug"),
                "category": slot_entry.get("category"),
                "aspect_ratio": slot_entry.get("aspect_ratio")
            })

        return jsonify(mockups_data)
    except Exception as exc:
        current_app.logger.exception("video.list_mockups")
        return {"error": str(exc)}, 500
```

### Frontend Changes

```html
<!-- Video Suite Mockup Display -->
<div class="mockup-gallery">
  <div class="mockups-list" id="mockupsList">
    <!-- Generated by JavaScript -->
  </div>
</div>

<script>
const slug = '{{ slug }}';

async function loadMockups() {
  try {
    const response = await fetch(`/video/${slug}/mockups`);
    const data = await response.json();

    const container = document.getElementById('mockupsList');
    container.innerHTML = '';

    data.mockups.forEach(mockup => {
      const item = document.createElement('div');
      item.className = 'mockup-item';
      item.innerHTML = `
        <img
          class="mockup-thumb"
          src="/artwork/${slug}/asset/${mockup.thumbnail}"
          alt="Mockup ${mockup.slot}"
          data-composite="${mockup.composite}"
          data-template="${mockup.template_slug}"
        />
        <div class="mockup-info">
          <span class="mockup-template">${mockup.template_slug}</span>
          <span class="mockup-category">${mockup.category}</span>
        </div>
      `;

      item.addEventListener('click', () => previewMockup(mockup));
      container.appendChild(item);
    });
  } catch (error) {
    console.error('Failed to load mockups:', error);
  }
}

function previewMockup(mockup) {
  const modal = document.getElementById('previewModal');
  const img = document.getElementById('previewImage');
  img.src = `/artwork/${slug}/asset/${mockup.composite}`;
  modal.classList.remove('hidden');
}

// Load on init
document.addEventListener('DOMContentLoaded', loadMockups);
</script>
```

---

## Component: Detail Closeup Editor

**File:** `application/artwork/ui/templates/detail_closeup_editor.html`

### Implementation Pattern

```javascript
async function loadCloseupEditingAssets(slug) {
  // Fetch main manifest
  const mainResponse = await fetch(`/artwork/${slug}/assets`);
  const mainAssets = await mainResponse.json();

  // Get closeup proxy (if available)
  const closeupProxy = mainAssets.files?.closeup_proxy;

  // Build working image URL
  const baseImageUrl = closeupProxy
    ? `/artwork/${slug}/asset/${closeupProxy}`
    : `/artwork/${slug}/asset/${mainAssets.files.master}`;

  return {
    baseImageUrl: baseImageUrl,
    | baseImagePath: closeupProxy |  | mainAssets.files.master, |
    manifest: mainAssets
  };
}
```

---

## Component: QC/Status Dashboard

**File:** `application/admin/**`

### Pattern

```javascript
async function displayQCStatus(slug) {
  const response = await fetch(`/artwork/${slug}/assets`);
  const assetDoc = await response.json();

  // All references are now relative to processed_root/slug/
  // No metadata files are missing anymore because manifest declares them all

  const qcFile = assetDoc.files?.qc;
  const statusFile = assetDoc.files?.status;
  const metadataFile = assetDoc.files?.metadata;

  // Fetch and display
  const qcData = await fetch(`/artwork/${slug}/asset/${qcFile}`).then(r => r.json());
  const statusData = await fetch(`/artwork/${slug}/asset/${statusFile}`).then(r => r.json());
  const metaData = await fetch(`/artwork/${slug}/asset/${metadataFile}`).then(r => r.json());

  // Render dashboard
}
```

---

## Migration Checklist

- [ ] **Carousel Modal** — Load asset manifest, populate image carousel from manifest mockup list
- [ ] **Video Suite** — Create `/video/<slug>/mockups` endpoint, load mockups from manifest
- [ ] **Detail Closeup** — Use `closeup_proxy` from manifest files
- [ ] **QC Dashboard** — Fetch all metadata files via manifest paths
- [ ] **Mockup Generation** — Write slot entries to manifest (already done)
- [ ] **Download Button** — Use `files.seo_download` from manifest
- [ ] **API Endpoints** — Add validation that served files exist in manifest
- [ ] **Error Handling** — Handle missing files gracefully (404 if not in manifest)

---

## Testing Patterns

### Test 1: Manifest Load

```javascript
test('Asset manifest loads correctly', async () => {
  const response = await fetch('/artwork/rjc-0279/assets');
  const manifest = await response.json();

  expect(manifest.sku).toBe('RJC-0279');
  expect(manifest.files.master).toBe('rjc-0279-MASTER.jpg');
  expect(manifest.mockups.assets).toBeDefined();
});
```

### Test 2: File Access

```javascript
test('Files are served only if in manifest', async () => {
  const response = await fetch('/artwork/rjc-0279/asset/rjc-0279-MASTER.jpg');
  expect(response.status).toBe(200);

  // File not in manifest should 404
  const badResponse = await fetch('/artwork/rjc-0279/asset/fake-file.jpg');
  expect(badResponse.status).toBe(404);
});
```

### Test 3: Carousel Rendering

```javascript
test('Carousel loads all images from manifest', async () => {
  // Simulate carousel initialization
  await loadCarouselImages();

  // Should have analyse + master + mockups
  expect(imageUrls.length).toBeGreaterThanOrEqual(2);
  expect(imageUrls[0].type).toBe('analyse');
});
```

---

## Files That Need Updates

| File | Change | Priority |
| ------ | -------- | ---------- |
| `analysis_workspace.html` | Carousel load from manifest | HIGH |
| `video_routes.py` | Add `/video/<slug>/mockups` endpoint | HIGH |
| `video_workspace.html` | Load mockups from endpoint | HIGH |
| `detail_closeup_editor.html` | Use manifest closeup_proxy | MEDIUM |
| QC/Status dashboard | Use manifest for all metadata files | MEDIUM |
| `artwork_routes.py` | Secure file serving endpoint (already done) | DONE |

---

## Common Mistakes to Avoid

❌ **Don't do this:**

```javascript
// ❌ Hardcoding filename patterns
const thumbUrl = `/artwork/${slug}/asset/${slug}-THUMB.jpg`;
const imageUrl = `/artwork/${slug}/asset/mu-${slug}-01.jpg`;

// ❌ Assuming file exists
fetch(`/artwork/${slug}/asset/metadata.json`);

// ❌ Mixed data sources
let filename = assets.files.master;
let backup = `${slug}-MASTER.jpg`; // fallback inconsistency
```

✅ **Do this instead:**

```javascript
// ✅ Load manifest first
const assets = await fetch(`/artwork/${slug}/assets`).then(r => r.json());

// ✅ Use only manifest paths
const thumbUrl = `/artwork/${slug}/asset/${assets.files.thumb}`;
const imageUrl = `/artwork/${slug}/asset/${mockup.composite}`;

// ✅ Validate before access
if (!assets.files.metadata) {
  console.log('Metadata not available');
  return;
}

// ✅ Consistent single source of truth
const path = assets.files[key];
if (path) {
  fetch(`/artwork/${slug}/asset/${path}`);
}
```

---

## Emergency Recovery

If manifest is missing but artwork exists:

```python
def recover_artwork_manifest(slug: str):
    """Scan directory and rebuild manifest if missing."""
    from application.mockups.routes.mockup_routes import _init_fresh_assets_index_for_slug

    result = _init_fresh_assets_index_for_slug(slug)
    if result:
        return result[4]  # Return assets_doc

    raise Exception("Unable to recover manifest for " + slug)
```

---

## Performance Optimization

**Cache manifest in localStorage** (optional for repeated access):

```javascript
const MANIFEST_CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function getAssetManifest(slug) {
  const cacheKey = `asset-manifest-${slug}`;
  const cached = localStorage.getItem(cacheKey);

  if (cached) {
    const { data, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp < MANIFEST_CACHE_TTL) {
      return data;
    }
  }

  const response = await fetch(`/artwork/${slug}/assets`);
  const data = await response.json();

  localStorage.setItem(cacheKey, JSON.stringify({
    data,
    timestamp: Date.now()
  }));

  return data;
}
```

---

## Documentation Resource

See [ASSET_MANAGEMENT_SYSTEM.md](ASSET_MANAGEMENT_SYSTEM.md) for:

- Complete asset type reference
- Architecture overview
- Access patterns
- File serving endpoint details
