# Asset Management System Architecture

**Date:** March 3, 2026
**Purpose:** Define single source of truth for all artwork assets and their usage across the application.

---

## Overview

The application uses a **manifest-driven asset system** where:

1. **Master Index**: `/srv/artlomo/application/lab/index/artworks.json` lists all artworks and points to their asset manifests
2. **Asset Manifest**: `{SKU}-assets.json` in each artwork directory is the **single source of truth** for all asset paths and metadata
3. **All Access**: Every component (UI, API, routes) must query the asset manifest before accessing files

---

## Directory Structure

```text
/srv/artlomo/application/lab/
├── index/
│   └── artworks.json                    # Master artwork index (points to manifests)
└── processed/
    ├── rjc-0279/                        # artwork directory (named by slug)
    │   ├── rjc-0279-assets.json         # Asset manifest (named by SKU lowercase)
    │   ├── rjc-0279-MASTER.jpg          # Canonical artwork (high-res source)
    │   ├── rjc-0279-THUMB.jpg           # List/gallery thumbnail
    │   ├── rjc-0279-ANALYSE.jpg         # Analysis overlay version
    │   ├── rjc-0279-CLOSEUP-PROXY.jpg   # Closeup view proxy image
    │   ├── metadata.json                # Artwork metadata/attributes
    │   ├── metadata_openai.json         # OpenAI analysis results
    │   ├── listing.json                 # Listing/gallery metadata
    │   ├── qc.json                      # Quality control flags
    │   ├── status.json                  # Processing status
    │   ├── processing_status.json       # Current pipeline status
    │   ├── RJC-0279-Ochre-Songlines-..jpg  # SEO-friendly export (full name)
    │   └── mockups/                     # Mockup artifacts directory
    │       ├── composites/              # Full resolution mockups
    │       │   ├── mu-rjc-0279-01.jpg
    │       │   ├── mu-rjc-0279-02.jpg
    │       │   └── ...
    │       ├── thumbs/                  # Mockup thumbnails
    │       │   ├── mu-rjc-0279-01-THUMB.jpg
    │       │   ├── mu-rjc-0279-02-THUMB.jpg
    │       │   └── ...
    │       └── templates/               # Template data (JSON coords)
    │           ├── 001-beach-sunset-coords.json
    │           └── ...
    │
    └── rjc-0288/
        ├── rjc-0288-assets.json
        ├── rjc-0288-MASTER.jpg
        └── ...
```

---

## Asset Manifest Schema (`{SKU}-assets.json`)

```json
{
  "sku": "RJC-0279",
  "slug": "rjc-0279",
  "version": 2,
  "created_at": "2026-03-01T02:32:33.161619+00:00",
  "updated_at": "2026-03-03T07:08:14.922051+00:00",

  "files": {
    "master": "rjc-0279-MASTER.jpg",
    "thumb": "rjc-0279-THUMB.jpg",
    "analyse": "rjc-0279-ANALYSE.jpg",
    "closeup_proxy": "rjc-0279-CLOSEUP-PROXY.jpg",
    "metadata": "rjc-0279-metadata.json",
    "listing": "listing.json",
    "qc": "rjc-0279-qc.json",
    "status": "status.json",
    "processing_status": "processing_status.json",
    "metadata_openai": "metadata_openai.json",
    "seo_download": "RJC-0279-Ochre-Songlines-Abstract-Australia-RJC-0279.jpg"
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
        "category": "product",
        "aspect_ratio": "16:9",
        "composite": "composites/mu-rjc-0279-01.jpg",
        "thumb": "thumbs/mu-rjc-0279-01-THUMB.jpg",
        "coords": "templates/001-beach-sunset-coords.json",
        "created_at": "2026-03-02T10:15:33.123456+00:00"
      },
      "02": {
        "slot": 2,
        "template_slug": "gallery-wall",
        "category": "interior-design",
        "aspect_ratio": "1:1",
        "composite": "composites/mu-rjc-0279-02.jpg",
        "thumb": "thumbs/mu-rjc-0279-02-THUMB.jpg",
        "coords": "templates/002-gallery-wall-coords.json",
        "created_at": "2026-03-02T10:16:45.234567+00:00"
      }
    },
    "count": 2
  }
}
```

---

## Master Artwork Index (`artworks.json`)

**Location:** `/srv/artlomo/application/lab/index/artworks.json`

```json
{
  "items": {
    "RJC-0279": {
      "sku": "RJC-0279",
      "slug": "rjc-0279",
      "artwork_dirname": "rjc-0279",
      "assets_file": "rjc-0279-assets.json",
      "assets_path": "processed/rjc-0279/rjc-0279-assets.json",
      "artwork_path": "processed/rjc-0279",
      "created_at": "2026-03-01T02:32:33.161619+00:00",
      "updated_at": "2026-03-03T07:08:14.922051+00:00",
      "version": 1
    },
    "RJC-0288": {
      "sku": "RJC-0288",
      "slug": "rjc-0288",
      "artwork_dirname": "rjc-0288",
      "assets_file": "rjc-0288-assets.json",
      "assets_path": "processed/rjc-0288/rjc-0288-assets.json",
      "artwork_path": "processed/rjc-0288",
      "created_at": "2026-03-03T03:38:03.864110+00:00",
      "updated_at": "2026-03-03T03:38:03.864110+00:00",
      "version": 1
    }
  },
  "updated_at": "2026-03-03T07:08:14.922051+00:00"
}
```

## Key fields

- `sku` — Unique stock keeping unit (primary identifier)
- `slug` — URL-safe identifier
- `assets_file` — Filename of the manifest (relative to artwork directory)
- `assets_path` — Full relative path to manifest from `LAB_PROCESSED_DIR`
- `artwork_path` — Directory path from `LAB_PROCESSED_DIR`

---

## Asset Types and Usage

### Image Assets

| Asset Key | Filename Pattern | Purpose | Size/Format | Used By |
| ----------- | ------------------ | --------- | ------------- | --------- |
| `master` | `{SKU}-MASTER.jpg` | Canonical high-res artwork | Large JPEG | Analysis, export, reference |
| `thumb` | `{SKU}-THUMB.jpg` | Gallery/list thumbnail | ~100KB JPEG | Gallery views, carousels, lists |
| `analyse` | `{SKU}-ANALYSE.jpg` | Analysis overlay version | Medium JPEG | Analysis page display |
| `closeup_proxy` | `{SKU}-CLOSEUP-PROXY.jpg` | Closeup/detail view | Large JPEG | Detail carousel, zoom views |
| `seo_download` | `{SKU}-{Title}-{Author}.jpg` | SEO-friendly export | High-res JPEG | Downloads, sharing |

### Metadata Files

| Asset Key | Typical Filename | Purpose | Content |
| ----------- | ------------------ | --------- | --------- |
| `metadata` | `{slug}-metadata.json` | Artwork attributes | Title, artist, dimensions, materials, etc. |
| `listing` | `listing.json` | Gallery listing data | Collection, price, availability |
| `qc` | `{slug}-qc.json` | Quality control | Color accuracy, compression ratio, issues |
| `status` | `status.json` | Processing status | Complete/in-review/draft |
| `processing_status` | `processing_status.json` | Pipeline state | Current task, error messages |
| `metadata_openai` | `metadata_openai.json` | AI analysis | Tags, description, style analysis |
| `seed_context` | `seed_context.json` | Generation context | For AI-generated artwork metadata |

### Mockup Assets

| Asset Key | Path Pattern | Purpose | Content |
| ----------- | -------------- | --------- | --------- |
| `mockups.assets[slot].composite` | `composites/mu-{slug}-{NN}.jpg` | Full mockup | Artwork rendered in chosen template |
| `mockups.assets[slot].thumb` | `thumbs/mu-{slug}-{NN}-THUMB.jpg` | Mockup thumbnail | Small preview for UI |
| `mockups.assets[slot].coords` | `templates/{NNN}-{template}-coords.json` | Template coords | Placement/scaling data for rendering |

---

## Asset Access Patterns

### 1. Load Artwork by SKU (Server-side)

```python
from application.mockups.artwork_index import resolve_artwork

artwork_dir, assets_path, sku = resolve_artwork(
    sku="RJC-0279",
    master_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
    processed_root=Path(cfg["LAB_PROCESSED_DIR"])
)

# Load manifest

from application.mockups.assets_index import AssetsIndex
assets_index = AssetsIndex(artwork_dir, assets_path)
assets_doc = assets_index.load()

# Access master image

master_rel = assets_doc["files"]["master"]
master_path = artwork_dir / master_rel
```

### 2. Serve File to Client

```python
@app.route('/artwork/<sku>/master')
def get_master_image(sku):
    artwork_dir, assets_path, _ = resolve_artwork(sku, ...)
    assets_index = AssetsIndex(artwork_dir, assets_path)
    assets_doc = assets_index.load()

    master_filename = assets_doc["files"]["master"]
    return send_file(artwork_dir / master_filename)
```

### 3. Generate Mockup

```python
from application.mockups.pipeline import generate_mockups_for_artwork

slot_entry = generate_mockups_for_artwork(
    sku="RJC-0279",
    template_slug="beach-sunset",
    aspect_ratio="16:9",
    category="product",
    base_image_path=artwork_dir / assets_doc["files"]["master"],
    coords_path=...,
    slot=1,
    master_index_path=Path(cfg["ARTWORKS_INDEX_PATH"]),
    processed_root=Path(cfg["LAB_PROCESSED_DIR"])
)

# slot_entry now contains:

# {

#   "composite": "composites/mu-rjc-0279-01.jpg",

#   "thumb": "thumbs/mu-rjc-0279-01-THUMB.jpg",

#   "template_slug": "beach-sunset",

#   "category": "product",

#   ...

# }

# Write to manifest atomically

assets_index.write_slot(assets_doc, "01", slot_entry)
```

### 4. Access from Frontend (Carousel Modal)

```html
<!-- Template: artwork_carousel.html -->
<script>
const artworkSku = '{{ artwork.sku }}';

// Fetch asset manifest
const response = await fetch(`/api/artwork/${artworkSku}/assets`);
const assets = await response.json();

// Display master image
document.getElementById('primary-image').src = `/artwork/${artworkSku}/file/${assets.files.master}`;

// Display thumb
document.getElementById('thumb').src = `/artwork/${artworkSku}/file/${assets.files.thumb}`;

// Display mockups
assets.mockups.assets.forEach(slot => {
  const img = document.createElement('img');
  img.src = `/artwork/${artworkSku}/file/${slot.composite}`;
  mockupCarousel.appendChild(img);
});
</script>
```

---

## File Serving Endpoint (Router)

All file access should be routed through a central endpoint that validates access and serves from the manifest:

```python
@app.route('/artwork/<sku>/file/<path:file_rel>')
def serve_artwork_file(sku: str, file_rel: str):
    """Serve a file from artwork directory, validated against asset manifest."""
    artwork_dir, assets_path, _ = resolve_artwork(sku, ...)
    assets_index = AssetsIndex(artwork_dir, assets_path)
    assets_doc = assets_index.load()

    # Validate file_rel against manifest (security check)
    all_valid_paths = []
    for file_key, file_rel_in_manifest in assets_doc["files"].items():
        all_valid_paths.append(file_rel_in_manifest)

    for mockup_slot in assets_doc["mockups"]["assets"].values():
        all_valid_paths.append(mockup_slot.get("composite"))
        all_valid_paths.append(mockup_slot.get("thumb"))

    if file_rel not in all_valid_paths:
        abort(404)

    file_path = artwork_dir / file_rel
    if not file_path.exists():
        abort(404)

    return send_file(file_path)
```

---

## Required Migration

**Current State:** Various parts of the code access files directly via assumptions about naming patterns.

**Target State:** All file access goes through:

1. Lookup SKU from artworks.json
2. Load {SKU}-assets.json manifest
3. Query manifest for file path
4. Access file at that path

## Components Requiring Update

- [ ] Carousel modal (image loading)
- [ ] Analysis review page (image display)
- [ ] Video suite (mockup listing)
- [ ] API endpoints (file serving)
- [ ] Mockup generation (image reading)
- [ ] Mockup deletion (file cleanup)
- [ ] QC/status reporting (metadata access)

---

## Best Practices

1. **Never hardcode filenames** — Always read from `{SKU}-assets.json`
2. **Never assume naming patterns** — File relationships are only defined in the manifest
3. **Always use SKU for lookup** — Slug is for URLs; SKU is for internal resolution
4. **Validate against manifest** — Before serving files, check manifest for declared paths
5. **Use AssetsIndex class** — All manifest I/O should go through this central interface
6. **Atomic writes** — Always use `atomic_write_json()` when updating manifests
7. **Relative paths** — All paths in manifests are relative to artwork directory
8. **Consistent case** — SKU is uppercase; slug is lowercase; use consistently

---

## Troubleshooting

### "Assets index not found" Error

1. Check that `{SKU}-assets.json` exists in `/srv/artlomo/application/lab/processed/{slug}/`
2. Verify artworks.json points to correct assets file and path
3. Check file permissions (must be readable)
4. Verify JSON is valid (use `json.tool`)

### "File not found" Error

1. Check that asset path in manifest actually points to an existing file
2. Verify file has correct permissions
3. Reconstruct path: `artwork_dir / manifest[file_key]`
4. Use `_init_fresh_assets_index_for_slug()` to regenerate manifest if necessary

### Carousel not loading images

1. Verify `/api/artwork/{sku}/assets` endpoint returns valid manifest
2. Check browser console for 404 errors on image URLs
3. Verify manifest paths are correct and files exist
4. Ensure carousel is using asset manifest, not hardcoded filename patterns
