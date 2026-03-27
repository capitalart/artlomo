# ArtLomo Rules & Parameters

Note: Video Generation & Kinematic Intelligence sections are included below.

## Operational Inventory Rule (March 7, 2026)

- Any significant environment/runtime/tooling change must be reflected in:

  - `CHANGELOG.md`

  - `application/docs/TOOLS_SH_COVERAGE_REPORT_2026-03-07.md` (or latest successor)

- Generate a fresh environment snapshot with:

  - `./application/tools/app-stacks/files/tools.sh` with command `sysinfo`

- For full docs refresh, use:

  - `./application/tools/app-stacks/files/tools.sh` with command `all`

## Clean-Room Analysis Workspace Standards (v2.0)

### Action Bar Specification

The unified action bar implements a "command center" pattern with exactly 5 buttons:

| Position | Button | Class | Width | Behavior |
| --- | --- | --- | --- | --- |
| 1 | Save Changes | `btn-primary` | flex: 1 | POST `/artwork/{slug}/save` |
| 2 | Lock | `btn-success` | flex: 1 | POST `/artwork/{slug}/lock` |
| 3 | Re-Analyse | `btn-outline-secondary` | flex: 1 | Route based on `data-source` (OpenAI/Gemini) |
| 4 | Export | `btn-outline-secondary` | flex: 1 | POST `/artwork/{slug}/admin-export/etsy` |
| 5 | Delete | `btn-danger` | flex: 1 | Trigger delete modal with confirmation |

- **Sticky Positioning**: `position: sticky; top: 10px; z-index: 100`

- **Glass Morphism**: `backdrop-filter: blur(10px)`; `background: var(--color-card-bg)`

- **Borders**: `1px solid rgba(128,128,128,0.1)` (subtle)

- **Padding**: `14px 18px` (compact, professional)

- **Responsive**: Wraps on smaller screens; no button is hidden

### Media Panel Specification (Left, 45%)

## Artwork Preview Row

- Layout: CSS Grid, 2 columns, equal width

- Artwork Container: max-width 500px, centered, aspect-ratio 1:1

- Closeup Container: max-width 500px, centered, aspect-ratio 1:1 (or dashed placeholder)

- Placeholder (if no closeup): `border: 2px dashed rgba(128,128,128,0.2)`

## Generate Video Panel

- Dedicated `.panel-card`: minimal, single button focus

- Button text: "Generate Video"

- Helper text: "Generates 15-second vertical promo video"

- Margin: 12px top below preview row

## Mockup Panel

- Category selector: `<select>` with options: Lifestyle, Studio, Frame, Modern Interior

- Generate button: tied to form submission

- Grid: CSS Grid, 5 columns (responsive: 4 columns @1400px, 3 columns @1000px)

- SWAP button on each card: `position: absolute; bottom: 8px; right: 8px; width: 32px; height: 32px; border-radius: 50%`

- Spinner overlay: centered, z-index: 99

### Mockup Admin Bases — Emergency Vertical Stack Contract (Feb 20, 2026)

- **Template:** `application/mockups/admin/ui/templates/mockups/bases.html`

- **Grid (XL):** Must remain `row-cols-xl-6` (hard ceiling of 6 cards per row; no 7-across behavior).

- **Control stack rule:** One row, one action. No side-by-side controls except final Preview/Delete row.

- **Required sequence per card:**

  1. `CATEGORY` label (`<small class="fw-bold text-muted d-block mb-1">`)

  1. Full-width category selector

  1. Full-width `MOVE TO CATEGORY` (`btn-outline-secondary w-100 mt-2`)

  1. `ASPECT RATIO` label (`<small class="fw-bold text-muted d-block mb-1 mt-3">`)

  1. Full-width aspect selector

  1. Full-width `OVERRIDE ASPECT` (`btn-outline-secondary w-100 mt-2`)

  1. Divider: `<hr class="my-4">`

  1. Full-width primary action: `REGENERATE COORDINATES` (`btn-warning w-100 py-2 fw-bold`)

  1. Final utility row only: `div.d-flex.gap-2.mt-2` with 50/50 `PREVIEW` + `DELETE`

- **CSS fallback safety net:**

  - `.mockup-card .btn { display:block; width:100%; margin-bottom:10px; padding:10px; }`

  - Final preview/delete row overrides bottom margin for compact pair layout.

### Delete Modal Specification

- **Container**: `#deleteModal` overlay with `position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px)`

- **Dialog**: `.modal-dialog` centered, max-width: 500px

- **Header**: `<h3>` + close button (×)

- **Body**: Text + input field (`#deleteConfirmInput`)

- **Input Validation**: JavaScript monitors input; button disabled until value === "DELETE"

- **Footer**: Cancel + Confirm buttons

### Dark Mode Compliance

- **All Text**: Use `var(--text-primary)` for headings/labels; `var(--text-secondary)` for help text

- **Zero White-on-White**: Test all form labels, inputs, help text in dark mode

- **Borders**: Never use `#fff` or `#000`; always use `rgba(128,128,128,0.1)` or similar

- **Background**: Forms use `var(--color-bg-primary)`; cards use `var(--color-card-bg)`

### Closeup Proxy Standards

- **Service**: `application/artwork/services/detail_closeup_service.py`

- **Path**: `DETAIL_PROXY_LONG_EDGE = 7200` pixels

- **Quality**: 90% JPEG

- **Filename**: `{slug}-CLOSEUP-PROXY.jpg`

- **Generation**: Automatic via `ensure_proxy_available()` when editor loads

- **Use Case**: Detail crop canvas in editor; high-res carousel source

## Image Generation & Processing Standards

### Derivative Image Sizes

| Derivative | Long Edge | Format | Purpose |
| --- | --- | --- | --- |
| **ANALYSE** | 2400px | JPEG | AI analysis, high-res carousel source, video source |
| **THUMB** | 500x500px | JPEG | Thumbnail grids (crop/center) |
| **MOCKUP COMPOSITE** | 2048px | JPEG | Full-resolution mockup composites for review and video |
| **DETAIL CLOSEUP** | 2048px | JPEG | High-res detail crop for galleries and kinematic zoom |

### Generation Parameters

- **Analyse Image**: Generated by `application/common/utilities/images.py::generate_analyse_image()`

  - Target long edge: `2400px`

  - Config key: `ANALYSE_LONG_EDGE` in `application/config.py::AppConfig`

  - Quality: 85

  - Color space: sRGB with ICC profile

  - Progressive JPEG with subsampling 0

- **Thumbnails**: Generated by `application/common/utilities/images.py::generate_thumbnail()`

  - Size: `500x500px`

  - Config key: `THUMB_SIZE` in `application/config.py::AppConfig`

  - Method: Center crop

  - Quality: 85

- **Detail Closeups**: Generated by `application/artwork/services/detail_closeup_service.py`

  - Target size: `500x500px` for proxy/thumbnail

  - Full resolution: **2048px** long edge

  - Stored in: `application/lab/processed/<slug>/<slug>-closeup.jpg`

- **Mockup Composites**: Generated by mockup pipeline

  - Full resolution: **2048px** long edge

  - Thumbnail: `500x500px`

## Carousel Modal Standards

### Asset Source Logic

The carousel modal (`mockup_carousel.js` or `manual_workspace.js`) serves three types of assets:

1. **Artwork** (data-carousel-artwork):

  - Source: `data-analyse-src` attribute

  - Resolution: **2048px** ANALYSE version

  - Purpose: High-quality artwork preview

1. **Detail Closeups** (data-carousel-detail):

  - Source: `data-analyse-src` attribute

  - Resolution: **2048px** full version

  - Purpose: High-res detail inspection

1. **Mockups** (data-mockup-thumb):

  - Source: `data-full-image` or `data-analyse-src` attribute

  - Resolution: **2048px** composite version

  - Purpose: Full mockup preview

### Display Constraints

- Modal container: `max-width: 90vw`

- Image: `max-height: 85vh`

- No fixed pixel limits - allows full 2048px display on large screens

- Responsive scaling maintains aspect ratio

- **Implementation Note**: Modal must be placed at the root of `<body>` to avoid CSS transform/overflow "traps" observed in `manual_workspace.html`.

## CSS Standards

### Modal Image Sizing

```css
.mockup-carousel__card {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  max-width: 90vw;
  width: auto;
}

.mockup-carousel__image {
  max-width: 100%;
  max-height: 85vh;
  width: auto;
  height: auto;
  object-fit: contain;
  background: var(--color-bg-primary);
}
```

**Critical**: Never impose fixed pixel width/height limits on carousel images. Use viewport-relative units to allow native resolution display.

## Workflow Integration

### Carousel Activation

To make an image carousel-enabled, add the appropriate data attribute:

```html
<div data-carousel-artwork
     data-analyse-src="/path/to/analyse-2048px.jpg"
     data-title="Artwork Title">
  <img src="/path/to/thumb.jpg" alt="Artwork">
</div>

<div data-carousel-detail
     data-analyse-src="/path/to/closeup-2048px.jpg"
     data-title="Detail Closeup">
  <img src="/path/to/closeup-thumb.jpg" alt="Detail">
</div>
<div data-mockup-thumb
     data-full-image="/path/to/composite-2048px.jpg"
     data-mockup-name="Mockup 1">
  <img src="/path/to/composite-thumb.jpg" alt="Mockup">
</div>
```

For carousel functionality, include:

```html
<script src="{{ url_for('static', filename='js/mockup_carousel.js') }}"></script>
```

### Required Modals

The carousel requires a modal container in the template:

```html
<div class="modal-sheet" data-carousel-modal>
  <div class="modal-card mockup-carousel__card">
    </div>
</div>
```

## Migration Notes

- **Legacy 1024px/2000px limits**: Deprecated and replaced as of Feb 2026.

- **New 2048px standard**: Applies to all ANALYSE, MOCKUP, and DETAIL derivatives going forward.

- **Backwards compatibility**: Existing 1024px images still work; carousel scales appropriately.

- **Detail Closeups**: Now first-class carousel assets alongside artwork and mockups.

## See Also

- `application/docs/ARCHITECTURE_INDEX.md` - Overall system architecture

- `application/config.py` - Configuration parameters

- `application/common/utilities/images.py` - Image generation logic

- `application/common/ui/static/js/mockup_carousel.js` - Carousel implementation

## Video Generation Standards (Kinematic Preview)

### Video Specifications

- **Resolution**: 2048x2048px (1:1 Aspect Ratio).

- **Format**: MP4 (H.264 codec via FFMPEG).

- **Source Assets**: Must use **2048px** ANALYSE, MOCKUP, and DETAIL images for lossless cross-fades.

- **Duration**: 10-15 seconds loop.

### Kinematic Intelligence

- **Zoom Logic**: The generator must pull `center_x` and `center_y` from `coordinates.json`.

- **Mockup Panning**: When displaying a room mockup, the "camera" must pan from the image center toward the Artwork's center-point coordinates.

- **Detail Transition**: The video must transition to the DETAIL CLOSEUP using a "Match-Cut" zoom based on the coordinates.

- **Metadata Requirement**: Every mockup composite MUST save a companion `.json` file recording the artwork's placement coordinates (normalized 0.0 to 1.0) within the room frame to enable targeted video panning.

- **UI Trigger**: A "Generate Video" button in `manual_workspace.html` calls the `VideoService` via the API.

## File Size & Upload Limits

### Upload Constraints (ArtLomo Services 2026)

| Setting | Size | Application | Notes |
| --- | --- | --- | --- |
| **Per-File Browser Limit** | 50 MB | `application/common/ui/static/js/upload.js` | Client-side enforcement via MAX_BYTES |
| **Server Content Limit** | 250 MB | `application/config.py::MAX_CONTENT_LENGTH` | Flask/Nginx limit for complete uploads |
| **Nginx Proxy Block** | 250 MB | `/etc/nginx/sites-available/artlomo.com` | `client_max_body_size 250M;` directive |
| **Form Data Max** | 250 MB | Gunicorn worker timeout: 120s | Sufficient for all derivative generation |

### Image Processing Limits

- **PIL Image Max Pixels**: `Image.MAX_IMAGE_PIXELS = None` in `application/artwork/services/detail_closeup_service.py`

  - Allows processing of master images up to 14400px long edge

  - No artificial pixel count restriction for large artwork files

### Rationale

- **50MB per file** (browser): User feedback loop, prevents accidental bulk uploads

- **250MB total payload** (server): Covers multiple uploads in batch + metadata overhead

- **No PIL limit**: Detail closeup service requires processing full-resolution master
