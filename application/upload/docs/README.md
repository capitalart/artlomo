# Upload Workflow

Workflow: Upload → QC → `lab/unprocessed/<slug>/`

## Canonical naming

- Slug format: `{artist-slug}-{short-title}-{sku}` (SKU is `RJC-####`).

- Artwork lives under one folder: `lab/unprocessed/<slug>/` (later promoted to processed/locked).<br>

- Filenames inside the folder:

  - `{slug}.jpg` — untouched original (never re-encoded)

  - `{slug}-ANALYSE.jpg` — analysis asset (long edge 2400, sRGB, quality 85, no upscaling, EXIF preserved)

  - `{slug}-THUMB.jpg` — 500×500 gallery thumb

  - `qc.json` — QC payload (see below)

  - `metadata.json` — derived metadata for UI (title, artist, filenames, analyse QC)

 QC also records `uploaded_at` (ISO-8601 with timezone) at upload/QC time; it is immutable.

## QC rules (originals)

- JPEG only; RGB only.

- Long edge ≥ 14400px; DPI ≥ 300 on both axes.

- Aspect ratios matched to the canonical set with ±1.5% tolerance; fallback label `~W:H`.

- Blur thresholds: pass ≥ 120, warn 80–119, fail < 80.

- Color: CMYK = warn, anything else non-RGB = fail.

## qc.json shape (deterministic)

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}
```

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text
{
 "dimensions": {"width": <int>, "height": <int>},
 "dpi": <int>,
 "filesize_mb": <float 1dp>,
 "aspect_ratio": {"label": "3:4", "canonical": true},
 "color": {"mode": "RGB", "icc": true},
 "blur_score": <int>,
 "compression_quality_est": <int>,
 | "qc_status": "pass" | "warn" | "fail" |
}

```text

## UI guardrails

- Filenames never appear in the UI; cards use display titles/IDs and clamp width.

- Metadata block (per card):

  - Aspect Ratio: `<label>` (Square suffix for 1:1)

  - Resolution (Pixels): `W×H`

  - Dots Per Inch (DPI): `<dpi>`

  - Filesize: `<x.x> MB`

  - Uploaded: `D Mon YYYY`

  - Artist: `<configured artist name>`

## Services & routes

- Routes: `application/upload/routes/upload_routes.py` (blueprint at `/upload`).

- Services: `application/upload/services/qc_service.py`, `storage_service.py`, `thumb_service.py`.

- Utilities: shared helpers in `application/common/utilities/` (files, images, slug/sku).

- Derived tags: `derive_qc_tags(qc_data)` in `upload/services/qc_service.py` (view-only; never persisted) produce namespaced tags for ratio/orientation/format/print/QC state.

## Failure handling

- Hard fails (format, RGB, DPI < 300, long edge < 14400) return 400 with flash messages before writing files.

- QC status `fail` is recorded; files are not deleted.

