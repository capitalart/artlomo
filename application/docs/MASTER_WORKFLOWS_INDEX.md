# ArtLomo: Master Workflows Index

**Date:** March 7, 2026
**Purpose:** Complete technical explanation of core workflow logic, data flows, and integration patterns
**Audience:** Developers, system architects, AI specialists

## Latest Additions

- Complete Detail Closeup Generator system handoff (1,261 lines, Feb 17, 2026)

- Complete workflow report suite (6 comprehensive reports with code examples)

- Operational tooling coverage references added (Mar 7, 2026):

  - `application/tools/app-stacks/files/system-inventory.sh`

  - `application/docs/TOOLS_SH_COVERAGE_REPORT_2026-03-07.md`

---

## 🔗 COMPREHENSIVE WORKFLOW REPORTS

**For in-depth analysis of each workflow**, refer to the dedicated comprehensive reports in `application/workflows/`:

| Workflow | Report | Coverage | Lines |
| ----------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ----- |
| Upload | [Upload-Workflow-Report.md](../../workflows/Upload-Workflow-Report.md) | File ingestion, QC, derivative generation, status tracking | 801 |
| Analysis | [Analysis-Workflow-Report.md](../../workflows/Analysis-Workflow-Report.md) | Gemini, OpenAI, Manual analysis with structured logging & 6-stage pipeline | 1,411 |
| Mockup Management | [Mockup-management-Workflow-report.md](../../workflows/Mockup-management-Workflow-report.md) | Catalog, selection, composition, asset management | 1,230 |
| Detail Closeup | [Detail-Closeup-Workflow-Report.md](../../workflows/Detail-Closeup-Workflow-Report.md) | 7-stage coordinate transformation pipeline with mathematical explanations | 1,333 |
| Export | [Export-Workflow-Report.md](../../workflows/Export-Workflow-Report.md) | 3 export modes (Etsy/Admin/Merchant) with ZIP orchestration | 1,015 |
| Video Generation | [Video-Generation-Workflow-Report.md](../../workflows/Video-Generation-Workflow-Report.md) | 15-sec vertical promo video generation with FFMPEG encoding | 788 |

**Total Documentation:** 6,578 lines of production-ready workflow documentation (✅ 0 linting errors)

---

## Table of Contents

1. WORKFLOW 1: UPLOAD WORKFLOW

1. WORKFLOW 2: AI ARTWORK ANALYSIS

1. WORKFLOW 3: MOCKUP MANAGEMENT

1. WORKFLOW 4: COMPOSITE MOCKUP GENERATION

1. WORKFLOW 5: COMMERCIAL ARTWORK PROCESSING (DUAL ENGINE)

---

---

## WORKFLOW 1: UPLOAD WORKFLOW

## Overview

The Upload Workflow is the **entry point** for artwork into the ArtLomo system. It handles:

- File ingestion (JPG/JPEG validation)

- Metadata extraction (dimensions, DPI, color profile)

- Quality control (QC) scanning with museum-grade extensions

- Derivative generation (thumbnails for UI, ANALYSE images for AI)

- Status tracking with multi-stage progression

- Storage organization (atomic directory structure)

**Key Constraint:** Upload is **non-blocking**—the endpoint returns immediately, triggering async background processing.

---

## Workflow Stages (Sequential)

````text
┌─────────────────────────────────────────────────────────────────────┐
│ USER UPLOADS FILE(S) via /artworks/upload (POST)                    │
│ Browser: drag/drop or click file input                              │
│ Format: JPG/JPEG only, max 50MB per file                            │
│ Validation: MIME type check, size check (UI-enforced)               │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓ AJAX (no page reload)
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 1: QUEUED (Backend file received)                             │
│ - Backend stores JPG to temp location                               │
│ - Generates slug from SKU sequence + filename                       │
│ - Creates lab/unprocessed/`slug`/ directory                         │
│ - Writes initial processing_status.json (stage=queued, done=false)  │
│ - Returns immediately: {status, slug, thumb_url, unprocessed_url}   │
│ Response time: < 100ms (non-blocking)                               │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
      [Background processing begins; UI polls status]
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 2: PREPARING (Background task spawned)                        │
│ - Validates file integrity (Pillow can open, not corrupted)         │
│ - Updates processing_status.json (stage=preparing)                  │
│ - No UI change (spinner continues)                                  │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 3: UPLOADING (File processing underway)                       │
│ - Stores original JPG as MASTER image                               │
│ - Stores to: lab/unprocessed/`slug`/`slug`-MASTER.jpg              │
│ - Updates processing_status.json (stage=uploading)                  │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 4: UPLOAD_COMPLETE (File committed)                           │
│ - All file I/O complete, ready for analysis                         │
│ - Updates processing_status.json (stage=upload_complete)            │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 5: PROCESSING (Multi-phase analysis begins)                   │
│ - QC analysis (dimensions, DPI, filesize, blur, compression)        │
│ - Museum-grade extensions (palette, luminance, edge_safety)         │
│ - Updates processing_status.json (stage=processing)                 │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 6: QC (Quality control results available)                     │
│ - Outputs: lab/unprocessed/`slug`/qc.json                           │
│ - Contains: dimensions, DPI, filesize, aspect_ratio, color, etc.    │
│ - Updates processing_status.json (stage=qc)                         │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 7: THUMBNAIL (Derivative generation)                          │
│ - Generates THUMB: 500px long edge (gallery preview)                │
│ - Generates ANALYSE: 2048px long edge (AI vision models)            │
│ - Output: lab/unprocessed/`slug`/`slug`-THUMB.jpg                  │
│ - Output: lab/unprocessed/`slug`/`slug`-ANALYSE.jpg                │
│ - Updates processing_status.json (stage=thumbnail)                  │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 8: DERIVATIVES (Additional formats / outputs)                 │
│ - Reserved for future: additional image sizes, format conversions   │
│ - Currently minimal; may expand in Phase 2                          │
│ - Updates processing_status.json (stage=derivatives)                │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 9: WRITING_METADATA / METADATA (Index registration)           │
│ - Creates metadata.json: {slug, filename, aspect_ratio, etc.}       │
│ - Registers in master index: lab/index/artworks.json                │
│ - Updates processing_status.json (stage=writing_metadata|metadata)  │
│ - Artwork now queryable via /artworks/unprocessed                   │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 10: FINALIZING (Post-processing cleanup)                      │
│ - Verifies all files created correctly                              │
│ - Cleans temp files (if any)                                        │
│ - Updates processing_status.json (stage=finalizing)                 │
└──────────────────┬──────────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 11: COMPLETE (Ready for analysis)                             │
│ - Updates processing_status.json (stage=complete, done=true)        │
│ - Artwork appears in /artworks/unprocessed gallery                  │
│ - UI modal closes; card is interactive (can trigger AI analysis)    │
| │ - Artist can now: OpenAI Analysis | Gemini Analysis | Manual        │ |
└─────────────────────────────────────────────────────────────────────┘
```text

---

## Key Data Structures

### Processing Status File

**Location:** `lab/unprocessed/`slug`/processing_status.json`

```json
{
  "id": "ART-001",
  "stage": "complete",
  "message": "Processing complete",
  "done": true,
  "error": null,
  "created_at": "2026-02-04T10:30:00Z",
  "updated_at": "2026-02-04T10:30:15Z",
  "duration_seconds": 15
}
```text

**Legacy Support:** `done: true` is normalized to `stage: "complete"` in frontend polls.

### QC Output File

**Location:** `lab/unprocessed/`slug`/qc.json`

```json
{
  "dimensions": {
    "width": 3840,
    "height": 2880,
    "unit": "pixels"
  },
  "dpi": 300,
  "filesize_mb": 8.5,
  "aspect_ratio": "4:3",
  "color": {
    "profile": "sRGB",
    "space": "RGB"
  },
  "blur_score": 15,
  "compression_quality_est": 95,
  "qc_status": "PASS",
  "palette": {
    "dominant_hex": ["#D4A574", "#8B7355", "#A0826D"],
    "primary": "Tan",
    "secondary": "Brown"
  },
  "luminance": {
    "category": "Balanced"
  },
  "edge_safety": {
    "too_close": false,
    "signature_zone_activity": 0.12
  }
}
```text

### Metadata File

**Location:** `lab/unprocessed/`slug`/metadata.json`

```json
{
  "slug": "ART-001-Dreaming-Colors",
  "uploaded_filename": "dreaming_colors.jpg",
  "aspect_ratio": "4:3",
  "width": 3840,
  "height": 2880,
  "dpi": 300,
  "uploaded_at": "2026-02-04T10:30:00Z",
  "file_size_mb": 8.5
}
```text

---

## Frontend Status Polling Logic

**Endpoint:** `GET /artworks/`slug`/status`
**Poll Interval:** 1000ms (1 second)
**Condition to Close Modal:** `done === true` AND `stage === "complete"` OR error present

### Stage Mapping (UI Labels)

```javascript
const stageLabels = {
  "queued": "Preparing uploads…",
  "preparing": "Preparing uploads…",
  "uploading": "Uploading files…",
  "upload_complete": "Upload complete. Processing…",
  "processing": "Upload complete. Processing…",
  "qc": "Quality checking artwork…",
  "thumbnail": "Generating thumbnails…",
  "derivatives": "Generating artwork files…",
  "writing_metadata": "Writing metadata…",
  "metadata": "Writing metadata…",
  "finalizing": "Finalizing artwork…",
  "complete": "Processing complete",
  "error": "Error"
};
```text

**Key Rule:** No percent progress bars shown. Modal is spinner-only until completion.

---

## Error Handling

### File Validation Errors

- **MIME type mismatch:** Return 400, "Only JPG/JPEG files accepted"

- **File size exceeds limit:** Return 413, "File too large (max 50MB)"

- **Corrupted file (Pillow can't read):** Set stage=error, message="File is not a valid image"

### Processing Errors

- **Disk full during save:** stage=error, message="Insufficient disk space"

- **QC failure (blur_score > threshold):** stage=qc, qc_status="FAIL" (but doesn't block progression)

- **Index write failure:** stage=error, message="Failed to register artwork"

**Error Persistence:** If error occurs, `processing_status.json` contains error state; frontend displays human-friendly message and disables retry without user intervention.

---

## Atomic Operations & Safety Invariants

### Single-Copy Invariant

- Each slug exists in exactly ONE location: `lab/unprocessed/`slug`/` OR `lab/processed/`slug`/` OR `lab/locked/`slug`/`

- Never duplicated; promotions are atomic moves (not copies)

### Atomic Directory Creation

```python

# Pseudocode

mkdir_p(lab/unprocessed/`slug`)  # Idempotent
write_json_atomic(processing_status.json)  # Temp+rename
write_jpg(MASTER.jpg)  # Direct write (crash-safe if filename is atomic)
write_jpg(THUMB.jpg)
write_jpg(ANALYSE.jpg)
write_json_atomic(qc.json)
write_json_atomic(metadata.json)
update_index_atomic(artworks.json)  # Last—if it succeeds, upload is committed
```text

### Cleanup on Failure

- If any stage fails, the directory remains but marked with error state

- Operator can retry via `/artworks/unprocessed/`slug`/retry` (future endpoint)

- Or delete via modal confirmation

---

## Seed Context Integration (Custom Input Preparation)

**Feature:** Artist can optionally provide Location, Sentiment, and Original Prompt before analysis.

## Flow:

1. On unprocessed card, artist clicks "Custom Input"

1. Modal opens with form: Location/Country, General Info/Sentiment, Original Generation Prompt

1. Artist submits → stored as `seed_context.json` in `lab/unprocessed/`slug`/`

1. When analysis is triggered (OpenAI/Gemini):

  - Artwork is promoted to `lab/processed/`slug`/` (atomic move, includes seed_context.json)

  - Analysis service loads seed_context.json

  - Injects Location and Sentiment into AI system prompt

  - Original Prompt remains private (used only for AI understanding, not exposed in output)

**Location:** `lab/unprocessed/`slug`/seed_context.json`

```json
{
  "location": "The Coorong, South Australia",
  "sentiment": "Ethereal",
  "original_prompt": "Oil painting of watercolors with soft edges...",
  "created_at": "2026-02-04T10:30:00Z",
  "updated_at": "2026-02-04T10:30:00Z"
}
```text

---

## Storage Organization

```text
lab/
├── unprocessed/
│   └── ART-001-Dreaming-Colors/
│       ├── ART-001-Dreaming-Colors-MASTER.jpg       [Original upload]
│       ├── ART-001-Dreaming-Colors-THUMB.jpg        [500px gallery preview]
│       ├── ART-001-Dreaming-Colors-ANALYSE.jpg      [2048px for AI analysis]
│       ├── processing_status.json                    [Current stage & done flag]
│       ├── metadata.json                             [Basic artwork metadata]
│       ├── qc.json                                   [Quality control results]
│       └── seed_context.json                         [Optional artist context]
│
├── processed/
│   └── [Same slug structure, post-analysis]
│
├── locked/
│   └── [Same slug structure, immutable/no re-analysis]
│
└── index/
    └── artworks.json                                 [Master index of all slugs]
```text

---

## Performance Characteristics

| Operation | Time | Notes |
| ----------- | ------ | ------- |
| File receipt + initial status | < 100ms | Non-blocking response |
| QC analysis | 2-5s | Depends on image size |
| Thumbnail generation (2 images) | 1-3s | LANCZOS resampling |
| Index registration | < 500ms | Atomic JSON write |
| **Total end-to-end** | 5-15s | Includes all stages |

---

## Integration Points

### Outbound

- **Upload routes** → **Storage service:** `store_artwork()`

- **Upload routes** → **Processing service:** `process_uploaded_artwork()`

- **Processing service** → **QC service:** `analyze_qc()`

- **Processing service** → **Thumb service:** `generate_thumbnails()`

- **Processing service** → **Index service:** `register_artwork()`

### Inbound

- **Manual workflow** reads from `lab/unprocessed/`slug`/` or `lab/processed/`slug`/`

- **Analysis services** (Gemini/OpenAI) read ANALYSE image from processed folder

---

---

## WORKFLOW 2: AI ARTWORK ANALYSIS

Overview

The AI Artwork Analysis Workflow is the **core intelligence** of ArtLomo. It transforms uploaded artwork into merchant-ready Etsy listings with:

- Heritage-First copywriting (Robin Custance persona, Boandik/Bindjali protocol)

- Museum-quality standard enforcement (14,400px, 300 DPI)

- Visual analysis (subject, dot_rhythm, palette, mood)

- SEO optimization (13 exact tags, 140-char title, filename slug)

- Limited edition framing (25-copy concept)

- Cross-model compatibility (Gemini + OpenAI)

**Key Philosophy:** AI provides initial analysis; human review refines metadata before merchant export.

---

## Workflow Stages (Two Parallel Paths)

```text
┌─────────────────────────────────────────────────────────────┐
│ ARTIST INITIATES ANALYSIS                                   │
│ On /artworks/unprocessed card, clicks:                      │
│ - "OpenAI Analysis" → POST /api/analysis/openai/`slug`     │
│ - "Gemini Analysis" → POST /api/analysis/gemini/`slug`     │
│ - "Manual Analysis" → POST /analysis/manual/`slug` [locked] │
└──────────────────┬──────────────────────────────────────────┘
                   │
        [Two parallel paths branch here]
        ┌───────────┴───────────┐
        │                       │
        ↓ PATH A               ↓ PATH B
   (GEMINI/OPENAI)          (MANUAL)
        │                       │
        ↓                       ↓
```text

---

## PATH A: GEMINI/OPENAI ANALYSIS (Automated)

```text
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: ARTWORK PROMOTION                                      │
│ - Artwork moves: lab/unprocessed/`slug`/ → lab/processed/`slug`/│
│ - Atomic move (not copy)                                         │
│ - seed_context.json travels with it                             │
│ - unprocessed folder is deleted (single-state invariant)         │
│ - Status: Artwork now in "processed" state                       │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: CONTEXT INJECTION                                       │
│ - Load seed_context.json from processed folder                  │
│ - Extract: location, sentiment, original_prompt (if provided)   │
│ - build_seed_context() → create context injection string        │
│ - If sentiment="Ethereal", inject: "infuse ethereal quality"    │
│ - Original_prompt remains private (not exposed in output)       │
│ - Result: Enhanced system_prompt with artist intent             │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: LOAD ANALYSE IMAGE                                      │
│ - Read: lab/processed/`slug`/`slug`-ANALYSE.jpg (2048px)        │
│ - Verify image integrity and dimensions                         │
│ - Prepare for API submission (base64 encode for Gemini/OpenAI)  │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: API CALL WITH INJECTED CONTEXT                          │
│ - System prompt: HERITAGE_FIRST_SYSTEM_PROMPT + context inject  │
│ - Persona: Robin Custance (People of the Reeds descendant)       │
│ - Requirements injected:                                         │
│   • "14,400px museum standard" (cite in description)            │
│   • "13 exact tags" (including "people of the reeds")           │
│   • "140 character title max"                                   │
│   • "Visual analysis: subject, dot_rhythm, palette, mood"       │
│   • "Limited edition: 25 copies"                                │
│   • Location (if provided): "set in [Location]"                 │
│   • Sentiment (if provided): "infuse [sentiment] into prose"    │
│ - Image: ANALYSE JPG                                             │
│ - Model: Gemini 2.0 Flash or OpenAI GPT-4 Vision                │
│ - Response format: JSON (structured output)                     │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 5: RESPONSE SANITIZATION                                   │
│ - Use ai_utils.clean_json_response() to strip markdown blocks   │
│ - Remove BOM characters, extraneous formatting                   │
│ - Attempt json.loads() via safe_parse_json()                    │
│ - Log diagnostic if parse fails; emit:                          │
│   --- GEMINI DIAGNOSTIC START ---                               │
│   Error: [details]                                              │
| │   Classification: [auth | quota | payload | network]                  │ |
│   --- GEMINI DIAGNOSTIC END ---                                 │
│ - Destination: /srv/artlomo/logs/ai_processing.log              │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 6: SCHEMA VALIDATION (Pydantic)                            │
│ - Validate response against GeminiArtworkAnalysis or equivalent  │
│ - Enforce:                                                       │
│   • etsy_title: max 140 characters ✅                            │
│   • etsy_tags: exactly 13 items ✅                               │
│   • etsy_description: required (no length limit)                 │
│   • visual_analysis.subject: required                            │
│   • visual_analysis.dot_rhythm: required                         │
│   • visual_analysis.palette: required                            │
│   • visual_analysis.mood: required                               │
│   • materials: exactly 13 items                                  │
│   • primary_colour, secondary_colour: required                   │
│   • seo_filename_slug: max 61 characters                         │
│ - If validation fails: return 400 with constraint violation      │
│ - If validation passes: continue to persistence                  │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 7: PERSISTENCE TO listing.json                             │
│ - Create/update: lab/processed/`slug`/listing.json               │
│ - Write all 8 GeminiArtworkAnalysis fields:                      │
│   {                                                              │
│     "etsy_title": "[Subject] [Style] at Museum Quality",         │
│     "etsy_description": "[Full prose with heritage + 14.4k]",    │
│     "etsy_tags": ["people of the reeds", "...", "..."],         │
│     "visual_analysis": {                                         │
│       "subject": "Abstract dot patterns",                        │
│       "dot_rhythm": "Energetic, fast-paced",                     │
│       "palette": "Earth tones, warm ochre",                      │
│       "mood": "Contemplative, spiritual"                         │
│     },                                                           │
│     "materials": ["Digital Oil", "14400px Resolution", ...],     │
│     "primary_colour": "Ochre",                                   │
│     "secondary_colour": "Brown",                                 │
│     "seo_filename_slug": "dreaming-ochre-coorong-max-61"         │
│   }                                                              │
│ - Also write provider snapshot: metadata_gemini.json or similar  │
│ - analysis_source set to: "gemini" or "openai"                  │
│ - write_json_atomic() for crash safety                           │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 8: MANUAL WORKSPACE REDIRECT                               │
│ - Return: {status: "success", slug, listing_data}               │
│ - Frontend redirects to: GET /analysis/workspace/`slug`/gemini  │
│ - Workspace template loads listing.json                          │
│ - Artist can now review and edit all fields                      │
│ - Visual analysis cards displayed (read-only initially)          │
└─────────────────────────────────────────────────────────────────┘
```text

---

## PATH B: MANUAL ANALYSIS (Direct Workspace Entry)

```text
┌──────────────────────────────────────────────────────────────────┐
│ STAGE 1: SAME AS PATH A (ARTWORK PROMOTION)                      │
│ - Unprocessed → Processed (atomic move)                          │
│ - seed_context.json travels                                      │
│ - single-state invariant maintained                              │
└──────────────────┬─────────────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────────────┐
│ STAGE 2: CREATE EMPTY LISTING.JSON                               │
│ - Artist is responsible for filling in metadata manually         │
│ - Initialize: lab/processed/`slug`/listing.json                  │
│ - With skeleton structure (empty fields for manual entry)        │
│ - analysis_source set to: "manual"                               │
└──────────────────┬─────────────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────────────┐
│ STAGE 3: MANUAL WORKSPACE                                         │
│ - Load workspace template with all 8 editable fields             │
│ - Artist enters: title, tags, description, visual_analysis, etc. │
│ - No AI guidance; pure human curation                            │
│ - Save triggers POST /manual/workspace/`slug`/save               │
└──────────────────┬─────────────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────────────┐
│ STAGE 4: PERSISTENCE                                              │
│ - Update listing.json with user-entered fields                   │
│ - Validate against same schema (etsy_title max 140, etc.)        │
│ - Set metadata.json analysis_source = "manual"                   │
│ - Lock state (prevent re-analysis) set optionally by artist      │
└──────────────────────────────────────────────────────────────────┘
```text

---

## System Prompt Anatomy (Heritage-First Protocol)

**Source File:** `application/analysis/prompts.py`
**Size:** ~1,300 words

## Key Sections:

```text
1. PERSONA SETUP
   "You are Robin Custance, a digital artist and descendant of
    the 'People of the Reeds' (Boandik/Bunganditj)..."

2. HERITAGE PROTOCOL
   "'People of the Reeds' are the lifeblood of my artistic practice.
    You MUST acknowledge this heritage..."

3. TECHNICAL STANDARD
   "The artwork is rendered at 14,400px on the long edge at 300 DPI,
    equivalent to a 48-inch (121.9cm) museum-quality print..."

4. STRUCTURE REQUIREMENT
   "HOOK: [Subject] [Style] at Museum Quality [14,400px Benefits]
    HEART: [Emotional Impact and Narrative]
    BRAIN: [Technical Achievement and Heritage Acknowledgement]"

5. CONSTRAINTS
   "- Title: MUST be ≤ 140 characters
    - Tags: MUST be exactly 13 tags including 'people of the reeds'
    - Description: MUST cite 14,400px museum-quality standard
    - Materials: MUST list exactly 13 digital craft materials
    - Limited Edition: MUST frame as 25-copy worldwide limit"

6. VISUAL ANALYSIS INJECTION
   "Analyze and provide:
    - subject: What is depicted (e.g., 'Aboriginal dot patterns')
    - dot_rhythm: Pattern of visual movement
    - palette: Color scheme (e.g., 'Earth tones, warm ochre')
    - mood: Emotional tone (e.g., 'Contemplative, spiritual')"

7. SEED CONTEXT INJECTION (Dynamic)
   If location provided: "Set this artwork in [Location]"
   If sentiment provided: "Infuse [Sentiment] quality into the prose"
   If original_prompt: "Consider this internal style guide: [prompt]"
```text

---

## Boilerplate Standardization (LISTING_BOILERPLATE)

**Source File:** `application/utils/house_prompts.py`

All AI descriptions **must** append standardized boilerplate:

```markdown
---
🏆 LIMITED EDITION
[25-copy worldwide limit notice]
---
📏 TECHNICAL SPECIFICATIONS
14,400px at 300 DPI
11520 × 14400 pixels
sRGB color space
---
🖨️ PRINTING NOTES
[Professional lab guidance]
---
🎨 ABOUT THE ARTIST
[Robin Custance bio with Boandik/Bindjali heritage]
---
❤️ ACKNOWLEDGEMENT OF COUNTRY
[Bindjali/Boandik land acknowledgement]
---
📐 PRINT SIZE GUIDE
[5 standard sizes]
---
🛒 HOW TO PRINT
[5-step purchasing workflow]
```text

**Enforcement Rule:** All AI responses are appended with boilerplate before final storage.

---

## Visual Analysis Data Model

## Persisted to listing.json as:

```json
"visual_analysis": {
  "subject": "Aboriginal dot patterns depicting the Coorong wetlands",
  "dot_rhythm": "Energetic, fast-paced; suggests movement and flow",
  "palette": "Earth tones, warm ochre, cool blues; represents water",
  "mood": "Contemplative, spiritual; invokes connection to Country"
}
```text

## Usage:

- Manual workspace renders each field as a read-only card for artist review

- Mockup preview grid may filter/sort by visual_analysis attributes (future)

- SEO metadata extraction uses these fields for dynamic tag generation

---

## Error Handling & Diagnostics

### Error Classification Pattern (Updated February 6, 2026)

## Enhanced Exception Handling in Gemini Service:

All `GeminiAnalysisError` exceptions now carry `error_code` and `error_detail` attributes for proper classification and debugging:

```python

# Error Classification Codes

ERR_AUTH        # Authentication failures (missing API key, client not available)
ERR_BAD_REQUEST # Validation failures (missing directories, missing images)
ERR_UNKNOWN     # Unknown/unclassified errors (default fallback)

# Usage Pattern

raise GeminiAnalysisError(
    "User-friendly message",
    error_code="ERR_AUTH",
    error_detail=str(original_exception)
)

# Exception Handler Pattern

try:
    # Gemini analysis call
except GeminiAnalysisError as exc:
    error_code = getattr(exc, 'error_code', 'ERR_UNKNOWN')
    error_detail = getattr(exc, 'error_detail', str(exc))
    # Route error_code to appropriate user message
```text

### API Failure Classification

## On Gemini/OpenAI error:

```text
IF error_code == "ERR_AUTH": Classification = "auth"
  → Log: "Invalid API key or client not available"
  → User message: "Analysis service authentication failed"

ELIF response_code == 429: Classification = "quota"
  → Log: "Rate limit exceeded or quota exhausted"
  → User message: "Analysis service quota exceeded; try again later"

ELIF error_code == "ERR_BAD_REQUEST": Classification = "payload"
  → Log: "Request validation failed or schema mismatch"
  → User message: "Analysis request rejected; check image format"

ELIF response_code == 5xx OR timeout: Classification = "network"
  → Log: "Service unreachable or timeout"
  → User message: "Analysis service temporary unavailable"
```text

### Diagnostic Logging Block

**Destination:** `/srv/artlomo/logs/ai_processing.log`

```text
--- GEMINI DIAGNOSTIC START ---
Timestamp: 2026-02-04T10:45:30Z
Slug: ART-001
Model: Gemini 2.0 Flash
Request Size: 2048x1536 JPEG
Error Type: ERR_AUTH
Error Code: ERR_AUTH
Error Details: Gemini API key is not configured
Classification: auth
Recommendation: Configure API key in environment variables
--- GEMINI DIAGNOSTIC END ---
```text

---

## Reanalysis Workflow

**Trigger:** Artist clicks "Reanalyze with Gemini" on existing processed artwork

```text
1. Load current listing.json (preserves human edits)
2. Load seed_context.json (same artist intent)
3. Call API with same enriched system prompt
4. Update listing.json with new AI response
5. Preserve user-edited fields? NO—overwrites with new AI output
   [Decision: AI analysis is authoritative; manual edits apply only after]
6. Redirect to workspace for user review of new analysis
```text

---

## Data Flow Diagram

```text
         ARTIST INITIATES ANALYSIS
                    │
                    ↓
         ┌──────────┴──────────┐
         │                     │
    GEMINI/OPENAI          MANUAL
         │                     │
    [API CALL]           [MANUAL ENTRY]
         │                     │
    [VALIDATION]           [VALIDATION]
         │                     │
    ┌────┴─────┐          ┌────┴─────┐
    │           │          │           │
 PASS        FAIL        PASS        FAIL
    │           │          │           │
    ↓           ↓          ↓           ↓
[PERSIST]  [ERROR]    [PERSIST]  [ERROR]
    │           │          │           │
    └────┬──────┘          └────┬──────┘
         │                      │
    [LISTING.JSON UPDATED]
         │
         ↓
    [MANUAL WORKSPACE RENDERED]
         │
         ├─→ [EDIT FIELDS]
         │        │
         │        ↓
         │   [SAVE CHANGES]
         │        │
         │        ↓
         │   [LOCK (optional)]
         │
         └─→ [GENERATE MOCKUPS (optional)]
              │
              ↓
         [COMPOSITE MOCKUP WORKFLOW]
```text

---

---

## WORKFLOW 2B: ANALYSIS LOADING UX & CLIENT-SIDE POLLING

Overview

The Analysis Loading UX provides **unified visual feedback** during asynchronous AI analysis processing across multiple entry points (custom input form, unprocessed gallery, review pages, manual workspace). The workflow ensures users understand that analysis is in progress and provides a smooth transition to the review page upon completion.

**Key Principle:** Analysis is background processing; UX must indicate progress without page reload, then redirect automatically on completion.

---

## Infrastructure Components

### JavaScript Module: `analysis-loading.js`

- **Location:** `application/common/ui/static/js/analysis-loading.js`

- **Purpose:** Reusable module for showing overlay and polling status endpoint

- **Key Functions:**

  - `AnalysisLoader.show(provider)` → Create dark overlay with animated spinner and pulsing dots

  - `AnalysisLoader.poll(slug, provider, maxWaitMs)` → Poll status endpoint every 1 second

  - `AnalysisLoader.showAndWait(slug, provider)` → Combined operation

  - `AnalysisLoader.hide()` → Clean up overlay and stop polling

- **Timeout:** 5 minutes (300000ms) safety fallback with automatic redirect

### CSS Stylesheet: `analysis-loading.css`

- **Location:** `application/common/ui/static/css/analysis-loading.css`

- **Features:**

  - Dark overlay: `rgba(0,0,0,0.85)` with backdrop blur (4px)

  - Z-index: 9999 (above all content)

  - SVG spinner: 2-second continuous rotation animation

  - Pulsing dots: 3 dots with staggered timing for rhythm

  - Theme-aware: dark mode and light mode support

  - Smooth fade transitions: 0.3s ease

### Status Polling Endpoint

- **Path:** `/api/analysis/status/`slug``

- **Location:** `application/analysis/api/routes.py` line 235

- **Response Contract:**

  ```json
  {
    "status": "processing|complete",
    "slug": "artwork-slug",
    "sku": "ART-001",
    | "stage": "analyzing | generating_description | ...", |
    "message": "Analyzing artwork...",
    "done": true|false,
    "error": null|"error message",
    | "source": "openai | gemini | manual", |
    "updated_at": "2026-02-04T10:30:00Z"
  }
````

- **Polling Logic:** Client checks `done === true` to determine completion; if `error` field is populated, shows alert

---

## Workflow: Entry Points & Implementations

### PATH 1: Custom Input Form (custom_input.html)

````text
┌─────────────────────────────────────────────────────────┐
│ ARTIST FILLS CUSTOM INPUT FORM                          │
│ - Location (optional): "Sydney, NSW"                    │
│ - Sentiment (optional): "Ethereal"                      │
│ - Original Prompt (optional): "Focus on dot rhythm"     │
│ - Buttons: "Save Only", "Analyze OpenAI", "Analyze..."  │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴───────────┬─────────────┐
        │                      │             │
        ↓ Save Only            ↓ Analyze     ↓ Analyze
     (No Analysis)          (OpenAI)       (Gemini)
        │                      │             │
        │ Form posts           │ JavaScript  │ JavaScript
        │ normally             │ intercepts  │ intercepts
        │                      │             │
        ↓                      ↓             ↓
    (Redirect        ┌────────────────────────────┐
    to /processed)   │ 1. PREVENT DEFAULT         │
                     │    (no page reload)        │
                     │                            │
                     │ 2. SHOW OVERLAY            │
                     │    AnalysisLoader.show()   │
                     │    - Dark background       │
                     │    - Spinner animation     │
                     │    - "OpenAI Analysis in   │
                     │      Progress" text        │
                     │                            │
                     │ 3. POST FORM DATA          │
                     │    fetch("/unprocessed/    │
                     │    `slug`/seed-context")   │
                     │    with FormData()         │
                     │                            │
                     │ 4. POLL STATUS             │
                     │    Every 1 second:         │
                     │    GET /api/analysis/      │
                     │    status/`slug`           │
                     │                            │
                     │ 5. CHECK COMPLETION        │
                     │    if done === true:       │
                     │      - Hide overlay        │
                     │      - Redirect to:        │
                     │        /artwork/`slug`/    │
                     │        review/openai       │
                     │                            │
                     │ 6. ERROR HANDLING          │
                     │    if error field:         │
                     │      - Show alert          │
                     │      - Hide overlay        │
                     │      - Return to form      │
                     │                            │
                     │ 7. TIMEOUT SAFETY          │
                     │    if > 5 minutes:         │
                     │      - Fallback redirect   │
                     │      - Show warning        │
                     └────────────────────────────┘
                            │
                            ↓
                     [REVIEW PAGE LOADED]
```text

### PATH 2: Unprocessed Gallery (unprocessed.html)

```text
┌─────────────────────────────────────────────────────────┐
│ ARTIST BROWSES UNPROCESSED GALLERY                      │
│ - Card for each artwork with action buttons             │
│ - "OpenAI Analysis" button → <a href>                  │
│ - "Gemini Analysis" button → <a href>                  │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ↓ Click OpenAI        ↓ Click Gemini
   handleAnalysisClick()  handleAnalysisClick()
   (event, 'openai',      (event, 'gemini',
    slug)                  slug)
        │                     │
        ├─────────┬───────────┤
        │         │           │
        ↓         ↓           ↓
   (Both execute same flow with different provider)
        │
        ├─ Prevent default (no immediate navigation)
        │
        ├─ Extract provider from function parameter
        │
        ├─ Show overlay:
        │  AnalysisLoader.show(provider)
        │  - Dark overlay
        │  - Spinner + dots
        │  - "Gemini Analysis in Progress"
        │
        ├─ Poll status endpoint:
        │  Every 1 second: GET /api/analysis/status/`slug`
        │
        ├─ Check completion:
        │  if done === true:
        │    - Redirect to /artwork/`slug`/review/gemini
        │  if error:
        │    - Alert user
        │    - Return to gallery
        │
        └─ Timeout: 5 minutes fallback
```text

### PATH 3: Review Pages (artwork_analysis.html)

**Status:** Infrastructure available for future re-analysis triggers

- **Current Role:** Displays completed analysis results (listing.json metadata)

- **Infrastructure Present:**

  - `analysis-loading.js` imported (can trigger re-analysis if button added)

  - `analysis-loading.css` imported (styling available)

  - SVG icon definition included

- **Potential Future Use:** Add "Re-analyze with different provider" button if needed

### PATH 4: Manual Workspace (manual_workspace.html)

**Status:** Infrastructure available for complementary manual analysis flows

- **Current Role:** Human-in-the-loop review of AI or empty listing.json

- **Infrastructure Present:**

  - `analysis-loading.js` imported

  - `analysis-loading.css` imported

- **Potential Future Use:** Add analysis trigger alongside manual editing if needed

---

## Form Submission & Provider-Aware Routing

### Custom Input Form Flow

```javascript
// Form interception pattern (custom_input.html)
form.addEventListener("submit", async (e) => {
  const action = e.submitter.getAttribute("data-action");

  if (action === "save_only") {
    // Allow normal form submission
    return;
  }

  | if (action === "analyze_openai" |  | action === "analyze_gemini") { |
    e.preventDefault();
    const provider = action === "analyze_openai" ? "OpenAI" : "Gemini";

    // Show overlay
    AnalysisLoader.show(provider);

    // Post form data
    const response = await fetch(form.action, {
      method: "POST",
      body: new FormData(form)
    });

    // Poll and redirect
    await AnalysisLoader.poll(slug, provider);
    window.location.href = `/artwork/${slug}/review/${provider === "OpenAI" ? "openai" : "gemini"}`;
  }
});
```text

### Unprocessed Gallery Flow

```javascript
// Onclick handler pattern (unprocessed.html)
function handleAnalysisClick(event, provider, slug) {
  event.preventDefault();

  const providerTitle = provider === 'openai' ? 'OpenAI' : 'Gemini';
  AnalysisLoader.show(providerTitle);

  // Poll endpoint
  const pollPromise = AnalysisLoader.poll(slug, provider);

  pollPromise.then(() => {
    // Redirect to provider-specific review page
    window.location.href = `/artwork/${slug}/review/${provider}`;
  }).catch(() => {
    // On error or timeout
    alert(`Analysis failed. Please try again.`);
    AnalysisLoader.hide();
  });
}
```text

---

## Critical Design Decisions

1. **Prevent Premature Redirect:** Form submissions and button clicks are intercepted to ensure analysis is polled before redirect.

1. **Provider Awareness:** Both custom form and gallery buttons pass provider info to determine correct review page redirect (`/review/openai` vs `/review/gemini`).

1. **Timeout Safety:** 5-minute maximum wait prevents indefinite loading screens if backend fails silently.

1. **Error Propagation:** Status endpoint `error` field is checked; errors are shown to user in alert.

1. **Reusable Module:** Single `AnalysisLoader` module used across all entry points for consistency.

1. **Theme Support:** CSS includes dark/light mode variants for accessibility.

---

---

## WORKFLOW 3: MOCKUP MANAGEMENT

Overview

The Mockup Management Workflow handles:

- **Base ingestion:** Upload mockup PNGs (e.g., mug, shirt, poster frames)

- **Coordinate generation:** Auto-detect artwork placement zones (perspective-aware)

- **Catalog organization:** Category/aspect taxonomy for selection

- **Metadata persistence:** Coordinate JSON v2.0 schema (zones with 4-point control)

- **Admin maintenance:** Filename sanitization, thumbnail generation, catalog sync

**Key Philosophy:** Bases are **externally authored** PNGs; ArtLomo only ingests coordinates and manages categories.

---

## Base Ingestion Flow (Admin Upload)

```text
┌──────────────────────────────────────────────────────────────┐
│ ADMIN UPLOADS BASE PNG                                       │
│ Endpoint: POST /admin/mockups/bases/upload                   │
│ File: Base PNG (e.g., mug_front.png)                         │
│ Format: RGBA PNG, 500×500px (recommended)                    │
│ Validation: File size < 5MB, dimensions reasonable           │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────────┐
│ STAGE 1: FILE STORAGE                                         │
│ - Store PNG to: application/mockups/catalog/assets/mockups/  │
│                 bases/<aspect>/<category>/                   │
│ - Example path: bases/4x3/Kitchen/4x3-Kitchen-MU-0042.png   │
│ - Filename convention: [aspect]-[CATEGORY]-MU-[ID].png       │
│ - ID auto-generated from sequence counter                     │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────────┐
│ STAGE 2: THUMBNAIL GENERATION                                │
│ - Create 500×500 JPG thumbnail from PNG                      │
│ - White background (no transparency)                         │
│ - Path: bases/<aspect>/<category>/4x3-Kitchen-MU-THUMB-42.jpg │
│ - Used for admin UI gallery preview                          │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────────┐
│ STAGE 3: COORDINATE DETECTION                                │
│ - Analyze PNG to detect artwork placement zone               │
│ - Use vision/ML heuristics (or manual hints if provided)      │
│ - Generate coordinate JSON (v2.0 format):                    │
│   {                                                          │
│     "format_version": "2.0",                                 │
│     "zones": [                                               │
│       {                                                      │
│         "name": "mug_front",                                 │
│         "points": [                                          │
│           {x: 50, y: 100},    // TL (Top Left)              │
│           {x: 450, y: 120},   // TR (Top Right)             │
│           {x: 440, y: 400},   // BR (Bottom Right)          │
│           {x: 60, y: 380}     // BL (Bottom Left)           │
│         ]                                                    │
│       }                                                      │
│     ]                                                        │
│   }                                                          │
│ - Save: bases/<aspect>/<category>/4x3-Kitchen-MU-0042.json  │
│ - coordinate_type: "Perspective" (auto-detected zones)       │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────────┐
│ STAGE 4: CATALOG REGISTRATION                                │
│ - Update catalog.json with new base entry:                   │
│   {                                                          │
│     "id": 42,                                                │
│     "aspect": "4x3",                                         │
│     "category": "Kitchen",                                   │
│     "name": "Mug Front",                                     │
│     "base_filename": "4x3-Kitchen-MU-0042.png",             │
│     "thumbnail_filename": "4x3-Kitchen-MU-THUMB-0042.jpg",  │
│     "coordinate_filename": "4x3-Kitchen-MU-0042.json",      │
│     "dimensions": {width: 500, height: 500},                │
│     "coordinate_type": "Perspective",                       │
│     "created_at": "2026-02-04T10:45:00Z"                    │
│   }                                                          │
│ - Path: application/mockups/catalog/catalog.json             │
│ - catalog.json is source of truth; scans directory for UI    │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────────┐
│ STAGE 5: ADMIN UI CONFIRMATION                               │
│ - Base now visible in /admin/mockups/bases/                  │
│ - Category counts auto-computed by directory scan            │
│ - Admin can view thumbnail, edit category, delete if needed  │
│ - Generate Mockups button now available for this base        │
└──────────────────────────────────────────────────────────────┘
```text

---

## Coordinate System (v2.0 Schema)

## Authoritative Format:

```json
{
  "format_version": "2.0",
  "base_png": "4x3-Kitchen-MU-0042.png",
  "base_dimensions": {
    "width": 500,
    "height": 500
  },
  "zones": [
    {
      "name": "artwork_placement_zone",
      "points": [
        {"x": 50, "y": 100},    // TL
        {"x": 450, "y": 120},   // TR
        {"x": 440, "y": 400},   // BR
        {"x": 60, "y": 380}     // BL
      ]
    }
  ]
}
```text

## Key Rules:

- **Points order:** TL → TR → BR → BL (clockwise)

- **Exactly 4 points** per zone

- **Perspective warp:** Artwork is warped to fit these 4 corners

- **No scaling logic:** Artwork is resized to zone dimensions, then pasted exactly

---

## Sanitize & Sync Operation

**Admin Endpoint:** `POST /admin/mockups/bases/sanitize-sync`
**Destructive:** YES—normalizes filenames; should run in maintenance window

```text
FOR EACH base PNG in directory tree:
  1. Normalize filename to: [aspect]-[CATEGORY]-MU-[ID].png
  2. Generate thumbnail if missing: [filename]-THUMB.jpg
  3. Generate/update coordinate JSON if missing
  4. Validate coordinate JSON schema (v2.0 format)
  5. Remove any orphaned files (coordinates without base, etc.)

AFTER all files processed:
  1. Regenerate catalog.json from directory structure
  2. Verify catalog.json entries match files on disk
  3. Log summary: X bases, Y thumbnails, Z coordinates
  4. Return {status: "success", details: {...}}
```text

---

## Category & Aspect System

**Aspects:** Layout orientation (e.g., 4x3, 16x9, Portrait)
**Categories:** Product types (e.g., Kitchen, Bedroom, Living Room, Poster)

## Storage Hierarchy:

```text
application/mockups/catalog/assets/mockups/bases/
├── 4x3/
│   ├── Kitchen/
│   │   ├── 4x3-Kitchen-MU-0001.png
│   │   ├── 4x3-Kitchen-MU-0001.json
│   │   ├── 4x3-Kitchen-MU-0002.png
│   │   ├── 4x3-Kitchen-MU-0002.json
│   │   └── ... (all bases for Kitchen category)
│   │
│   ├── Bedroom/
│   │   ├── 4x3-Bedroom-MU-0021.png
│   │   └── ... (all bases for Bedroom category)
│   │
│   └── ... (other 4x3 categories)
│
├── 16x9/
│   ├── Living\ Room/
│   │   └── ... (all bases for 16x9 Living Room)
│   └── ...
│
└── ...
```text

## Admin UI Display:

```text
Kitchen (8)          ← Count auto-computed from directory
├─ 4x3 Mug Front     ← Clickable; opens detail view
├─ 4x3 Poster Frame
├─ 16x9 Photo Frame
└─ ...

Bedroom (5)
├─ 4x3 Wall Canvas
└─ ...
```text

---

## Category Counts Computation

**Endpoint:** `GET /admin/mockups/bases`

```python
def get_category_counts():
    counts = {}
    for aspect_dir in bases_root.iterdir():
        if aspect_dir.is_dir():
            for category_dir in aspect_dir.iterdir():
                if category_dir.is_dir():
                    png_count = len(list(category_dir.glob("*.png")))
                    key = f"{aspect_dir.name}/{category_dir.name}"
                    counts[key] = png_count
    return counts
```text

## Result:

- NO JSON index used for counts; live scan of filesystem

- Ensures counts always reflect current state

- If file deleted manually, count auto-updates

---

---

## WORKFLOW 4: COMPOSITE MOCKUP GENERATION

Overview

Composite Mockup Generation is the **visual merchandising** workflow. It:

- Selects appropriate base mockups for artwork aspect ratio

- Applies perspective warp to artwork to fit zone coordinates

- Composites warped artwork onto base PNG

- Generates mockup asset manifest for storage/serving

- Supports admin mockup swap operations (change category, regenerate)

**Key Technical Detail:** **Strict zone stretching**—artwork is resized to exact zone dimensions with NO aspect preservation, then pasted exactly at (x, y).

---

## End-to-End Generation Flow

```text
┌─────────────────────────────────────────────────────────┐
│ ARTIST TRIGGERS MOCKUP GENERATION                       │
│ On review page (Analysis workspace), clicks:            │
│ "Generate Mockups"                                      │
│ Endpoint: POST /artwork/`slug`/mockups/generate         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 1: LOAD ARTWORK METADATA                           │
│ - Read: lab/processed/`slug`/listing.json               │
│ - Extract: aspect_ratio, dimensions                     │
│ - Load ANALYSE image: `slug`-ANALYSE.jpg                │
│ - Verify dimensions and color space                     │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 2: SELECT MOCKUP BASES (Planning)                  │
│ - Query catalog by artwork aspect ratio                 │
│ - Selection policy: Category affinity scoring            │
│   (Kitchen bases favored for domestic art, etc.)         │
│ - Diversity constraint: avoid duplicate categories       │
│ - Plan 3-5 slots (configurable)                         │
│ - Output: [(base_id, category, slot), ...]              │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 3: FOR EACH BASE SELECTED                          │
│ A) Load Base PNG                                         │
│    - Path: bases/<aspect>/<category>/[base].png         │
│    - Verify RGBA format, dimensions                     │
│                                                         │
│ B) Load Coordinates                                      │
│    - Path: bases/<aspect>/<category>/[base].json        │
│    - Parse zones array (v2.0 format)                    │
│    - Verify 4 points per zone                           │
│                                                         │
│ C) Compute Zone Bounds                                   │
│    - From 4-point zone, compute bounding box:          │
│      x_min, x_max, y_min, y_max                         │
│    - Compute zone width, zone height                    │
│                                                         │
│ D) Resize Artwork (Strict Zone Stretching)              │
│    - Resize ANALYSE image to exact zone dimensions:     │
│      new_width = zone_width                             │
│      new_height = zone_height                           │
│    - Use LANCZOS resampling (high quality)              │
│    - NO aspect preservation; may stretch/squeeze        │
│    - Output: resized_artwork (RGB mode)                 │
│                                                         │
│ E) Apply Perspective Warp                                │
│    - Warp resized artwork to fit 4 control points       │
│    - Method: PIL.Image.transform with PERSPECTIVE      │
│    - Input: 4 corners of resized image                  │
│    - Output: 4 zone corners (may be non-rectangular)    │
│    - Result: warped_artwork                             │
│                                                         │
│ F) Composite onto Base                                   │
│    - Create copy of base PNG (RGBA)                      │
│    - Paste warped_artwork at position (x_min, y_min)    │
│    - Respect alpha channel (artwork transparency)       │
│    - Result: composite image (RGBA)                     │
│                                                         │
│ G) Base PNG Foreground                                   │
│    - Paste base PNG AGAIN over composite                │
│    - This ensures template shadows, reflections, frames │
│      remain VISIBLE and FOREGROUND                      │
│                                                         │
│ H) Convert to JPG & Save                                 │
│    - Convert RGBA → RGB (sRGB color space)              │
│    - Compress as JPG (quality=95)                       │
│    - Save: lab/processed/`slug`/mockups/                 │
│             mu-`slug`-<slot:02d>.jpg                    │
│    - Also generate thumbnail:                           │
│             mu-`slug`-<slot:02d>-THUMB.jpg              │
│             (500px long edge, white background)         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 4: GENERATE ASSETS MANIFEST                        │
│ - Create: lab/processed/`slug`/`slug`-assets.json       │
│ - Array of MockupAsset objects:                          │
│   [                                                      │
│     {                                                    │
│       "slot": 0,                                         │
│       "category": "Kitchen",                             │
│       "base_id": 42,                                     │
│       "base_name": "Mug Front",                          │
│       "composite_filename": "mu-`slug`-00.jpg",          │
│       "thumbnail_filename": "mu-`slug`-00-THUMB.jpg",   │
│       "url": "/artwork/`slug`/mockups/mu-`slug`-00.jpg"  │
│     },                                                   │
│     ...                                                  │
│   ]                                                      │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 5: UPDATE LISTING.JSON                             │
│ - Add "mockups" field to listing.json                    │
│ - Reference manifest or inline asset array              │
│ - Enable manual workspace to render mockup carousel     │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 6: UI REFRESH                                      │
│ - Return: {status: "success", mockups: [...]}           │
│ - Manual workspace mockup grid reloads                  │
│ - Each mockup card shows:                               │
│   - Thumbnail image                                      │
│   - Category selector dropdown                           │
│   - Swap button (change to different base)              │
└─────────────────────────────────────────────────────────┘
```text

---

## Perspective Warp Algorithm (Technical Detail)

## Input:

- `resized_artwork`: Image resized to exact zone dimensions (width × height)

- `zone_points`: 4-point array [TL, TR, BR, BL] from coordinate JSON

## Process:

```python
def apply_perspective_warp(resized_artwork, zone_points):
    # Compute source (normalized) and destination (zone) coefficients
    src_coords = [
        (0, 0),                              # TL of resized image
        (resized_artwork.width, 0),          # TR
        (resized_artwork.width, resized_artwork.height),  # BR
        (0, resized_artwork.height)          # BL
    ]

    dst_coords = [
        (zone_points[0]['x'], zone_points[0]['y']),  # TL (zone)
        (zone_points[1]['x'], zone_points[1]['y']),  # TR (zone)
        (zone_points[2]['x'], zone_points[2]['y']),  # BR (zone)
        (zone_points[3]['x'], zone_points[3]['y'])   # BL (zone)
    ]

    # Compute perspective transform coefficients
    transform = find_coeffs(src_coords, dst_coords)

    # Apply perspective warp using PIL
    warped = resized_artwork.transform(
        size=(base_width, base_height),  # Output canvas
        method=Image.PERSPECTIVE,
        data=transform,
        Image.LANCZOS
    )

    return warped
```text

## Key Points:

- **Non-rectangular zones:** If zone points are not axis-aligned, result is skewed/perspective-warped

- **LANCZOS resampling:** High-quality downsampling (no banding artifacts)

- **Output canvas:** Base PNG dimensions (e.g., 500×500)

---

## Mockup Asset Manifest Structure

**File:** `lab/processed/`slug`/`slug`-assets.json`

```json
[
  {
    "slot": 0,
    "category": "Kitchen",
    "base_id": 42,
    "base_name": "Mug Front",
    "composite_filename": "mu-ART-001-00.jpg",
    "thumbnail_filename": "mu-ART-001-00-THUMB.jpg",
    "url": "/artwork/ART-001-Dreaming-Colors/mockups/mu-ART-001-00.jpg",
    "thumb_url": "/artwork/ART-001-Dreaming-Colors/mockups/mu-ART-001-00-THUMB.jpg",
    "created_at": "2026-02-04T10:50:00Z"
  },
  {
    "slot": 1,
    "category": "Bedroom",
    "base_id": 87,
    "base_name": "Canvas Large",
    "composite_filename": "mu-ART-001-01.jpg",
    "thumbnail_filename": "mu-ART-001-01-THUMB.jpg",
    "url": "/artwork/ART-001-Dreaming-Colors/mockups/mu-ART-001-01.jpg",
    "thumb_url": "/artwork/ART-001-Dreaming-Colors/mockups/mu-ART-001-01-THUMB.jpg",
    "created_at": "2026-02-04T10:50:00Z"
  },
  ...
]
```text

---

## Mockup Swap Operation

**Trigger:** Artist clicks "Swap" on a mockup card in manual workspace

**Endpoint:** `POST /artwork/`slug`/mockups/<slot>/swap`

```text
┌───────────────────────────────────────────────────┐
│ ARTIST CLICKS SWAP ON MOCKUP CARD (slot 1)        │
│ (Currently showing Bedroom Canvas)                 │
└──────────────┬────────────────────────────────────┘
               │
               ↓
┌───────────────────────────────────────────────────┐
│ STAGE 1: LOAD CURRENT MANIFEST                     │
│ - Read `slug`-assets.json                          │
│ - Find entry with slot==1                          │
│ - Current category: "Bedroom"                      │
└──────────────┬────────────────────────────────────┘
               │
               ↓
┌───────────────────────────────────────────────────┐
│ STAGE 2: SELECT REPLACEMENT BASE                   │
│ - Query catalog bases for same aspect ratio       │
│ - Filter to category != "Bedroom" (diversity)     │
│ - Randomly select OR allow user choice             │
│ - Example: Choose "Kitchen" category base          │
└──────────────┬────────────────────────────────────┘
               │
               ↓
┌───────────────────────────────────────────────────┐
│ STAGE 3: REGENERATE COMPOSITE                      │
│ - Load new base PNG & coordinates                  │
│ - Load artwork (ANALYSE image)                     │
│ - Execute composite generation steps (same as     │
│   STAGE 3 in main generation flow)                 │
│ - Output: new mu-`slug`-01.jpg                    │
│ - Overwrite old mockup file                        │
└──────────────┬────────────────────────────────────┘
               │
               ↓
┌───────────────────────────────────────────────────┐
│ STAGE 4: UPDATE MANIFEST                           │
│ - Modify `slug`-assets.json entry for slot 1:     │
│   - category: "Kitchen"                            │
│   - base_id: [new kitchen base ID]                │
│   - base_name: [new kitchen base name]             │
│   - composite_filename: mu-`slug`-01.jpg           │
│ - Write manifest atomically                        │
└──────────────┬────────────────────────────────────┘
               │
               ↓
┌───────────────────────────────────────────────────┐
│ STAGE 5: RESPONSE TO FRONTEND                      │
│ - Return: {status: "success", slot: 1,             │
│            new_url: "/artwork/.../mu-...-01.jpg"}  │
│ - Frontend updates card thumbnail & category text  │
│ - No full page reload needed                       │
└───────────────────────────────────────────────────┘
```text

---

## Mockup Category Change (Without Regeneration)

**Trigger:** Artist clicks category dropdown on mockup card → selects new category

**Endpoint:** `POST /artwork/`slug`/mockups/<slot>/category`

```text
Request body: {category: "Living Room"}

┌─────────────────────────────────────────────┐
│ STAGE 1: UPDATE MANIFEST ONLY                 │
│ - Modify `slug`-assets.json slot entry:     │
│   category: "Living Room"                    │
│ - NOTE: base_id/composite_filename unchanged │
│ - This is METADATA-ONLY change (UX label)    │
│ - Composite image NOT regenerated             │
└─────────────────────────────────────────────┘

Response: {status: "success", slot: 1}

FRONTEND:
- Category dropdown updates to "Living Room"
- Thumbnail unchanged (still old image)
- User sees: "Changed category to Living Room"
  (on next swap, new category applied)
```text

---

## Selection Policy Algorithm

**Goal:** Choose 3-5 diverse bases that complement the artwork

```python
def plan_mockup_selections(artwork_metadata, num_slots=3):
    aspect_ratio = artwork_metadata.aspect_ratio

    # Query: Find all bases matching aspect ratio
    matching_bases = catalog.find_bases(aspect=aspect_ratio)

    # Scoring: For each base, compute affinity score
    scored_bases = []
    for base in matching_bases:
        score = 0

        # Category affinity (heuristic)
        if artwork_topic == "abstract":
            if base.category in ["Living Room", "Gallery"]:
                score += 100
        elif artwork_topic == "nature":
            if base.category in ["Bedroom", "Kitchen"]:
                score += 100

        # Diversity bonus (prefer bases from different categories)
        if base.category not in already_selected_categories:
            score += 50

        scored_bases.append((base, score))

    # Select: Top-scored bases
    selected = sorted(scored_bases, key=lambda x: x[1], reverse=True)[:num_slots]

    return selected
```text

---

Storage Organization

```text
lab/processed/`slug`/
├── `slug`-MASTER.jpg
├── `slug`-THUMB.jpg
├── `slug`-ANALYSE.jpg
├── listing.json
├── metadata.json
├── qc.json
├── `slug`-assets.json                [Mockup manifest]
│
└── mockups/                           [Mockup storage]
    ├── mu-`slug`-00.jpg               [Composite 0]
    ├── mu-`slug`-00-THUMB.jpg         [Thumbnail 0]
    ├── mu-`slug`-01.jpg               [Composite 1]
    ├── mu-`slug`-01-THUMB.jpg         [Thumbnail 1]
    └── ... (more slots)
```text

---

Performance Characteristics

| Operation | Time | Notes |
| ----------- | ------ | ------- |
| Load metadata + artwork | < 500ms | File I/O |
| Perspective warp per base | 2-4s | LANCZOS resampling |
| Composite onto base PNG | 1-2s | Alpha blending |
| Thumbnail generation | 0.5s per image | Resize + JPG compress |
| **3-slot full generation** | 15-25s | Sequential processing |
| **Swap operation** | 5-10s | Regenerates 1 composite |

---

Error Handling

### Missing Assets

```text
ERROR: Base PNG not found at [path]
→ Return 404, message: "Base not found; may have been deleted"
→ Log to ai_processing.log

ERROR: Coordinate JSON malformed
→ Return 400, message: "Coordinate schema invalid"
→ Suggest admin run Sanitize & Sync
```text

### Dimension Mismatches

```text
ERROR: Artwork too small for zone
→ WARNING log: "Artwork 1500px; zone requires 2000px"
→ Allow operation; image will be upsampled (quality loss possible)
→ Display warning in UI: "Image upsampling may cause quality loss"

ERROR: Zone points out of base bounds
→ Return 400, message: "Coordinate points exceed base dimensions"
→ Admin must re-verify coordinate JSON
```text

---

## Integration with Export Workflow

## Export includes mockups:

```text
outputs/exports/`sku`/<export_id>/
├── manifest.json
├── listing.json
├── assets/
│   ├── ART-001-MASTER.jpg
│   ├── ART-001-THUMB.jpg
│   ├── ART-001-ANALYSE.jpg
│   └── mockups/
│       ├── mu-ART-001-00.jpg
│       ├── mu-ART-001-00-THUMB.jpg
│       ├── mu-ART-001-01.jpg
│       └── ...
└── [export].zip
```text

---

---

## WORKFLOW 5: COMMERCIAL ARTWORK PROCESSING (DUAL ENGINE)

Overview

The Commercial Artwork Processing Workflow uses the **Commercial Engine preset** to generate marketplace-optimized Etsy listings with conversion-focused copy, SEO tags, and high-volume pricing strategy. This workflow targets mid-tier pricing ($15–$45 range) and Etsy marketplace distribution.

**Key Differentiator:** Commercial works emphasize benefit, value proposition, and product appeal over artistic significance.

**Key Constraint:** Once analyzed via Commercial preset, a work MUST NOT be re-categorized to Collector Tier.

## Workflow Steps

```text
┌─────────────────────────────────────────────────────┐
│ STEP 1: ARTIST UPLOADS ARTWORK                      │
│ - Navigate to /artworks/upload                      │
│ - Drag/drop or select JPG file (max 50MB)           │
│ - File stored to lab/unprocessed/`slug`/            │
│ - Status updates visible in real-time               │
│ - Artwork ready for analysis                        │
└────────────┬────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────┐
│ STEP 2: SELECT COMMERCIAL PRESET                    │
│ - Artist clicks "Analyze" button on unprocessed     │
│ - Modal/dropdown shows available presets            │
│ - Artist selects: "OpenAI - Commercial Engine v1"   │
│   or "Gemini - Commercial Engine v1"                │
│ - Selection persists in UI during session           │
│ - Triggers POST /api/analysis/<provider>/`slug`     │
│ - Loading overlay shows analysis in progress        │
└────────────┬────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────┐
│ STEP 3: AI GENERATES COMMERCIAL LISTING             │
│ - System prompt loaded from preset:                 │
│   "Conversion-focused, benefit-driven, accessible"  │
│ - Artwork analyzed for marketplace appeal           │
│ - Title: SEO-optimized, benefit-rich (max 140 chars)│
│ - Description: HOOK (benefit) → HEART (appeal) →   │
│   BRAIN (specs + 14,400px standard)                │
│ - Tags: 13 marketplace-friendly tags (incl.         │
│   "people of the reeds" brand signature)            │
│ - Visual analysis: color psychology, trend fit,     │
│   market category, mood for filtering               │
│ - Pricing frame: mid-tier ($15–$45 suggested)       │
└────────────┬────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────┐
│ STEP 4: REVIEW & EDIT IN MANUAL WORKSPACE           │
│ - Artwork promoted to lab/processed/`slug`/         │
│ - Manual workspace displays all 8 listing fields    │
│ - Artist reviews AI-generated title, description,   │
│   tags, visual analysis                             │
│ - Can edit any field before locking                 │
│ - Heritage acknowledgement included in description  │
│ - 14,400px quality standard visible in copy         │
│ - Optional: upload mockups for product preview      │
└────────────┬────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────┐
│ STEP 5: LOCK & EXPORT TO ETSY                       │
│ - Artist clicks "Lock" to finalize listing          │
│ - Artwork moved to lab/locked/`slug`/ (immutable)   │
│ - Cannot re-analyze once locked                     │
│ - Export bundle created via `/api/export/`sku``     │
│ - Bundle includes:                                  │
│   - listing.json (title, desc, tags, materials)     │
│   - THUMB + ANALYSE images for gallery              │
│   - Optional: composite mockup images               │
│ - Manual copy/paste fields into Etsy listing form   │
│ - Publish to Etsy marketplace                       │
└─────────────────────────────────────────────────────┘
```text

## Commercial Engine Guardrails

**CRITICAL:** Commercial works must NOT be tagged as Collector Tier and must NOT be moved to high-ticket inventory.

## Enforcement Rules:

- Preset selector shows "Commercial Engine" label with warning: "This will optimize for marketplace sales. Cannot be changed to Collector Tier after analysis."

- Database tracks `engine_type: "commercial"` in listing metadata

- Admin tools prevent re-analysis of commercial works with Collector preset

- Export destination: Etsy marketplace only (no private collector hand-off)

- Price range enforced: $15–$45 suggested (artist can override but UI warns)

## Workflow Exit Points:

- **Normal Exit:** Artwork locked, exported, published to Etsy

- **Reanalysis:** Only via Commercial preset (same or different provider)

- **Manual Edit:** Artist can fine-tune fields in manual workspace before locking

- **Discard:** Delete from unprocessed before analysis (no penalty)

---

## WORKFLOW 6: COLLECTOR SERIES PROCESSING (DUAL ENGINE)

Overview

The Collector Series Processing Workflow uses the **Collector Engine preset** to generate curatorial-grade listings optimized for high-ticket collector positioning, series archival, and prestige preservation. This workflow targets high-value ($200–$1,500+ range) and private/gallery distribution.

**Key Differentiator:** Collector works emphasize artistic vision, cultural significance, and scarcity over mass-market appeal.

**Key Constraint:** Once a work enters Collector Tier, it MUST NOT be reused in Commercial Tier. Collector integrity is sacrosanct.

Workflow Steps

```text
┌─────────────────────────────────────────────────────┐
│ STEP 1: ARTIST UPLOADS ARTWORK                      │
│ - Navigate to /artworks/upload                      │
│ - Drag/drop or select JPG file (max 50MB)           │
│ - File stored to lab/unprocessed/`slug`/            │
│ - Status updates visible in real-time               │
│ - Artwork ready for analysis                        │
└────────────┬────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────┐
│ STEP 2: MARK AS COLLECTOR SERIES                    │
│ - Artist provides series context before analysis    │
│ - Series name: "People of the Reeds – Series 3"     │
│ - Edition info: "Single Edition" OR "1 of 5"        │
│ - Series metadata stored in seed_context.json       │
│ - Database records: `series_name`, `edition_type`   │
│ - Signals downstream workflows: this is high-ticket │
└────────────┬────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────┐
│ STEP 3: SELECT COLLECTOR PRESET                     │
│ - Artist clicks "Analyze" button on unprocessed     │
│ - Modal/dropdown shows available presets            │
│ - Artist selects: "Gemini - Collector Engine v1"    │
│   or "OpenAI - Collector Engine v1"                 │
│ - UI warns: "This will lock this work to Collector  │
│   Tier. It cannot be sold via Etsy marketplace."    │
│ - Triggers POST /api/analysis/<provider>/`slug`     │
│ - Loading overlay shows analysis in progress        │
└────────────┬────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────┐
│ STEP 4: AI GENERATES CURATORIAL LISTING             │
│ - System prompt loaded from preset:                 │
│   "Scholarly, poetic, heritage-first, curatorial"   │
│ - Artwork analyzed for artistic & cultural merit    │
│ - Title: Poetic, series-aware (max 140 chars)       │
│ - Description: HOOK (artistic vision) →             │
│   HEART (series context + heritage) →               │
│   BRAIN (edition concept + no Etsy boilerplate)     │
│ - Tags: 13 curatorial tags (incl. "people of reeds"│
│   + series + cultural significance markers)         │
│ - Visual analysis: artistic technique, cultural     │
│   meaning, historical reference, craftsmanship      │
│ - Pricing frame: high-ticket ($200–$1,500+ range)   │
│ - NO commercial listing_boilerplate injected        │
│ - Series metadata woven into narrative              │
└────────────┬────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────┐
│ STEP 5: REVIEW & REFINE IN MANUAL WORKSPACE         │
│ - Artwork promoted to lab/processed/`slug`/         │
│ - Manual workspace displays all 8 listing fields    │
│ - Artist reviews AI-generated curatorial copy       │
│ - Edition type displayed prominently (Single/Limited)│
│ - Series name and context visible in description    │
│ - Can edit any field for tone refinement            │
│ - Heritage acknowledgement comprehensive            │
│ - 14,400px quality standard cited                   │
│ - Optional: upload mockups (gallery canvas concept) │
│ - NO "Export to Etsy" button in this workflow       │
└────────────┬────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────┐
│ STEP 6: LOCK & ARCHIVE AS HIGH-TICKET INVENTORY     │
│ - Artist clicks "Lock" to finalize listing          │
│ - Artwork moved to lab/locked/`slug`/ (immutable)   │
│ - Database records: `tier: "collector"`, locked=true│
│ - Cannot re-analyze once locked                     │
│ - Artwork archived as high-ticket inventory item    │
│ - Manual promotion pathway:                         │
│   - Gallery contact list (private)                  │
│   - Auction house submission (via export bundle)    │
│   - Collector network (via private email)           │
│   - Institution/museum inquiry (curatorial copy)    │
│ - Export bundle created via `/api/export/`sku``     │
│ - Bundle includes:                                  │
│   - listing.json (curatorial copy, no Etsy fields)  │
│   - THUMB + ANALYSE images (high-res reference)     │
│   - Optional: composite mockup (canvas/frame)       │
│ - Artist manually curates distribution channels     │
│ - NO automatic Etsy publication                     │
└─────────────────────────────────────────────────────┘
```text

## Collector Engine Guardrails

**CRITICAL:** Collector Integrity Rule — Once a work enters Collector Tier, it MUST NOT be reused in Commercial Tier.

Enforcement Rules:

- Database immutability: tier field, once set to "collector", cannot be changed

- Audit logging: all tier changes logged with timestamp, user, rationale

- Re-analysis prevention: Collector works CANNOT be reanalyzed with Commercial preset

- UI enforcement: "Lock as Collector" button visually distinct (gold/premium styling)

- Export paths: Collector exports go to `outputs/exports/`sku`/collector/` subfolder (distinct from commercial)

- Series tagging mandatory: every Collector work must have `series_name` in metadata

Workflow Exit Points:

- **Normal Exit:** Artwork locked, exported, distributed via manual curator channels

- **Reanalysis:** Only via Collector preset (same provider or switch)

- **Manual Edit:** Artist can refine curatorial tone in manual workspace before locking

- **Series Update:** Can change series context before initial lock (not after)

- **Discard:** Delete from unprocessed before analysis (no penalty)

## Forbidden Actions:

- Converting Collector → Commercial (immutable tier)

- Exporting Collector works to Etsy

- Changing edition type after lock

- Removing series attribution

---

## Dual Engine Comparison Matrix

| Aspect | Commercial Engine | Collector Engine |
| -------- | ------------------- | ------------------ |
| **Preset Examples** | OpenAI/Gemini - Commercial v1 | OpenAI/Gemini - Collector v1 |
| **Target Audience** | Etsy buyers, art enthusiasts | Gallery curators, collectors |
| **Pricing** | Mid-tier ($15–$45) | High-ticket ($200–$1,500+) |
| **Distribution** | Etsy marketplace (auto) | Private/gallery (manual) |
| **Description Tone** | Benefit-driven, accessible | Poetic, scholarly, curatorial |
| **Narrative Focus** | Value + Heritage accent | Vision + Heritage-first |
| **Series Context** | Optional tag | Mandatory metadata |
| **Edition Concept** | Limited 25-copy standard | Custom (1/1, Limited, etc.) |
| **14,400px Standard** | Technical spec mention | Museum-quality prestige |
| **Boilerplate** | Commercial Etsy structure | Curatorial statement, no Etsy |
| **Lock Behavior** | locked/ folder | locked/ folder + collector flag |
| **Tier Immutability** | Commercial tier (permanent) | Collector tier (permanent) |
| **Guardrail Strength** | Warning on selection | Confirmation + tier lock |

---

## Cross-Engine Rules & Constraints

## Single-Assignment Rule:

- Each artwork (slug) analyzed once per engine type

- Changing engines requires deletion of old analysis + restart

- Prevents "hedged bets" or test analysis

## Tier Immutability:

- Commercial → (no change) - stays commercial forever

- Collector → (no change) - stays collector forever

- Prevents exploitation of tier advantages

- Audit trail enforces (database + logging)

## Preset Versioning:

- Presets versioned (v1, v2, v3...) to track evolution

- Re-analysis can use newer preset version

- Old presets remain available for historical works

- Breaking prompt changes increment major version

## Provider Flexibility:

- Artists can switch between OpenAI ↔ Gemini within same engine

- Both providers output identical schema

- Provider choice is independent of engine choice

- Allows redundancy & cost optimization

---

                      UPLOAD WORKFLOW
                            ↓
                   (File → QC → Metadata)
                            ↓
                      lab/unprocessed/`slug`/
                            ↓
                    ┌───────┴────────┐
                    │                │
            AI ANALYSIS WORKFLOW     MANUAL ANALYSIS
            (Gemini/OpenAI)          (Human Entry)
                    │                │
                    └───────┬────────┘
                            ↓
                      lab/processed/`slug`/
                      (listing.json created)
                            ↓
                ┌───────────────────────────┐
                │                           │
         MANUAL WORKSPACE            MOCKUP GENERATION
         (Edit Fields)               (Select Bases)
                │                           │
                ├─→ Save Edits             │
                │                           │
                └─→ Lock (optional)         │
                                           ↓
                                  COMPOSITE GENERATION
                                  (Warp + Paste)
                                           ↓
                                   lab/processed/`slug`/
                                   mockups/ (`slug`-assets.json)
                                           ↓
                                   Manual Workspace Mockup Grid
                                   (Review + Swap/Category)
                                           ↓
                                     LOCK ARTWORK
                                   (Immutable state)
                                           ↓
                                     EXPORT WORKFLOW
                                  (Bundle assets + ship)
```text

## WORKFLOW 5: CLEAN-ROOM ANALYSIS WORKSPACE (UI/UX Pattern)

Overview

The Clean-Room Analysis Workspace (v2.0) implements a professional, distraction-free workflow for reviewing and editing artwork metadata. It follows the principle: **"User never wonders what button to click next—context-aware actions only."**

The pattern eliminates button clutter through:
- **Unified Action Bar:** 5 semantically clear actions (Save, Lock, Re-Analyse, Export, Delete)
- **Linear Workflow:** Metadata editing → Save → Lock → Export progression
- **Media-First Layout:** 45/55 dual-pane grid (stationary media left, scrolling actions/forms right)
- **Context-Aware Logic:** Re-Analyse detects current AI provider; no manual switching
- **High-Safety Deletions:** Modal requires typed "DELETE" confirmation

## Architecture

### Layout Structure (2400px max width)

```text
┌─────────────────────────────────────┬──────────────────────────────────────┐
│  LEFT PANE (45%, STATIONARY)        │  RIGHT PANE (55%, SCROLLING)         │
├─────────────────────────────────────┼──────────────────────────────────────┤
│                                     │  [UNIFIED ACTION BAR - STICKY]       │
│  MEDIA PREVIEW ROW:                 │  ┌──────────────────────────────────┐ │
│  ┌─────────────┐  ┌──────────────┐  │  │ Save Changes │ Lock (green)      │ │
│  │  Artwork    │  │   Closeup    │  │  │ Re-Analyse   │ Export │ Delete  │ │
│  │ Preview     │  │   Preview    │  │  │ (context-    │ (Etsy) │ (modal) │ │
│  │ (500px max) │  │ (500px max)  │  │  │  aware)      │        │         │ │
│  │             │  │   OR dashed  │  │  └──────────────────────────────────┘ │
│  │             │  │  placeholder │  │  [SCROLLABLE FORM BELOW]             │
│  └─────────────┘  └──────────────┘  │  ┌──────────────────────────────────┐ │
│                                     │  │ metadata form fields:            │ │
│  VIDEO PANEL:                       │  │  - Title                         │ │
│  ┌──────────────────────────────────│  │  - Description                   │ │
│  │ [Generate Video Button]          │  │  - Tags                          │ │
│  │ 15-sec vertical promo            │  │  - Materials                     │ │
│  └──────────────────────────────────│  │  - Visual Analysis               │ │
│                                     │  │    (subject, palette, mood)      │ │
│  MOCKUPS PANEL:                     │  │  - Location / Context            │ │
│  ┌──────────────────────────────────│  │  - Colours                       │ │
│  │ Category: [Lifestyle ▼]          │  │                                  │ │
│  │ Count: [10x] [Generate]          │  │  [QC Panel - read-only]          │ │
│  │                                  │  │  - Palette, Luminance, Safety   │ │
│  │ #### MOCKUP GRID ####            │  └──────────────────────────────────┘ │
│  │ [card] [card] [card] [card]      │                                        │
│  │ [SWAP↻] [SWAP↻] [SWAP↻] [SWAP↻]  │  SELECT: ☐ Selection counts...       │
│  │ [card] [card] [card] [card]      │  DELETE SELECTED | DELETE ALL         │
│  │ [SWAP↻] [SWAP↻] [SWAP↻] [SWAP↻]  │                                        │
│  └──────────────────────────────────│                                        │
│                                     │                                        │
└─────────────────────────────────────┴──────────────────────────────────────┘
```text

### Action Bar (Unified Command Center)

The action bar provides exactly 5 semantically distinct buttons:

| Action | Class | Behavior | Purpose |
| -------- | ------- | ---------- | --------- |
| **Save Changes** | `btn-primary` | POST `/artwork/{slug}/save` with metadata | Persist all edits |
| **Lock** | `btn-success` (green) | POST `/artwork/{slug}/lock` | Finalize listing, make immutable |
| **Re-Analyse** | `btn-outline-secondary` | Route to `/artwork/{slug}/[openai\ | gemini]-analysis` based on `data-source` | Re-run current AI provider (no switching) |
| **Export** | `btn-outline-secondary` | POST `/artwork/{slug}/admin-export/etsy` | Export to Etsy only (simplified) |
| **Delete** | `btn-danger` | Trigger `#deleteModal` | Destructive action (high safety) |

### Media Panel (Left, 45%)

## Artwork Preview Row:

- Artwork and Detail Closeup positioned side-by-side (max 500px each, centered)
- If no closeup exists: dashed 500px border placeholder
- Clicking either image opens fullscreen gallery modal with carousel
- Button: "Generate Closeup" (replaces legacy "Edit")

## Generate Video Panel:

- Dedicated button with clear single-purpose label
- Positioned between preview row and mockups
- Generates 15-second vertical promo video
- Button text: "Generate Video"

## Mockup Panel:

- Category Selector: Lifestyle, Studio, Frame, Modern Interior
- Generate button tied to category selection
- Mockup Grid: configurable count (1-20), 5-column layout (responsive down to 3 columns)
- **SWAP Button** on each card: arrows-clockwise icon, triggers regeneration with spinning overlay
- Selection checkboxes: bulk delete controls at bottom

### JavaScript Integration

```javascript
// Context-aware Re-Analyse detection
const reanalyseBtn = document.querySelector("[data-reanalyse]");
const source = reanalyseBtn.dataset.source; // "OpenAI" or "Gemini"
// Routes to: /artwork/{slug}/(openai|gemini)-analysis

// Delete modal pattern
const deleteInput = document.getElementById("deleteConfirmInput");
const confirmBtn = document.getElementById("confirmDeleteBtn");
deleteInput.addEventListener("input", () => {
  confirmBtn.disabled = deleteInput.value.trim() !== "DELETE";
});

// Mockup SWAP with spinner overlay
const swapBtn = document.querySelector("[data-mockup-swap]");
swapBtn.addEventListener("click", async () => {
  overlay.classList.remove("hidden"); // Show spinner
  try {
    const resp = await postJson(`/artwork/{slug}/mockups/swap`, {slot});
    // Reload image with cache-bust timestamp
    img.src = img.src.split('?')[0] + '?t=' + Date.now();
  } finally {
    overlay.classList.add("hidden"); // Hide spinner
  }
});
```text

### CSS Features (Dark-Mode Compliant)

- **Text:** All labels/inputs use `var(--text-primary)` or `var(--text-secondary)` (zero white-on-white)
- **Glass Morphism:** Action bar: `backdrop-filter: blur(10px)` + `background: var(--color-card-bg)`
- **Borders:** Subtle `1px solid rgba(128,128,128,0.1)`
- **Button Colors:**
  - Primary (Save): `var(--accent-color, #0066cc)` with hover darkening
  - Success (Lock): `#28a745` (green) with hover darkening
  - Danger (Delete): `#dc3545` (red) with contrast
- **Modal:** Overlay with backdrop blur, centered dialog, semantic layering (z-index: 10000)
- **Responsive:** Single column layout below 1200px

### Backend Integration

## Required Endpoints:

- `POST /artwork/{slug}/save` — Persist metadata
- `POST /artwork/{slug}/lock` — Finalize artwork
- `POST /artwork/{slug}/admin-export/etsy` — Export to Etsy
- `POST /artwork/{slug}/delete` — Delete artwork
- `POST /artwork/{slug}/openai-analysis` — Re-analyze with OpenAI
- `POST /artwork/{slug}/gemini-analysis` — Re-analyze with Gemini
- `POST /artwork/{slug}/mockups/swap` — Swap/regenerate mockup (ready for implementation)

## Image Assets (Pre-Generated):

- Detail Closeup Proxy: 7200px long edge @ 90% quality (auto-generated via `detail_closeup_service.py`)
- ANALYSE Image: 2048px long edge (for carousel display)
- Mockup Composites: 2048px long edge
- Thumbnails: 500x500px (center-crop)

### UX Benefits (Clean-Room Pattern)

| Benefit | How Achieved |
| --------- | ------------- |
| **Linear Workflow** | User path: Edit → Save → Lock → Export; no back-and-forth |
| **No Decision Paralysis** | Only 5 actions; each context-appropriate for stage |
| **Reduced Cognitive Load** | No searching for buttons; layout is consistent |
| **Professional Aesthetic** | Glass morphism, semantic colors (green=lock, red=delete), smooth transitions |
| **Mobile-Friendly** | Responsive grid collapses to single column <1200px |
| **High Safety** | Delete requires modal + typed confirmation |
| **Context Awareness** | Re-Analyse auto-detects current AI provider |

### File Location & Deployment

- **Template:** `/srv/artlomo/application/common/ui/templates/analysis_workspace.html`
- **Status:** ✅ Deployed February 14, 2026, 20:14 ACDT
- **Error Free:** No template rendering issues, no dark mode violations
- **Documentation:** See [CLEAN_ROOM_WORKSPACE_REFACTOR.md](/srv/artlomo/CLEAN_ROOM_WORKSPACE_REFACTOR.md) for detailed architecture

---

## WORKFLOW 5 (Prev): LOCKING & FINALIZATION

Overview

Locking is the final step before Export. It signifies that the artwork's metadata and assets are final and ready for archiving or distribution. It enforces immutability and optimizes filenames for SEO.

## Process

1. **Trigger:** Artist clicks "Lock" in Manual Workspace or Review page (`POST /`slug`/lock`).
2. **Atomic Move:** Folder moves from `lab/processed/`slug`/` to `lab/locked/`slug`/`.
3. **SEO Renaming (Critical):**
   - System reads `listing.json` to find `seo_filename` (e.g., `sku-seo-slug.jpg`).
   - Renames the master file (`[slug]-MASTER.jpg` or `[slug].jpg`) to `seo_filename`.
   - Ensures the final asset has the exact SEO-optimized name required for Etsy.
4. **Immutability:** Locked artworks cannot be re-analyzed or edited.
5. **Detail Closeup Support:** The Detail Closeup service automatically resolves the master file by checking `seo_filename` if the standard master name is missing.

---

## Summary Table: Workflow Triggers & Outputs

| Workflow | Trigger | Output | Next Step |
| ---------- | --------- | -------- | ----------- |
| **Upload** | File drag/drop | unprocessed/`slug`/ | Analysis or Manual |
| **AI Analysis** | "Gemini/OpenAI" button | processed/`slug`/listing.json | Manual Workspace |
| **Manual Analysis** | "Manual Analysis" button | processed/`slug`/listing.json (empty) | Manual Workspace |
| **Manual Workspace** | "Save" button | Updated listing.json | Mockup Generation or Lock |
| **Mockup Generation** | "Generate Mockups" button | processed/`slug`/`slug`-assets.json | Mockup Grid Review |
| **Mockup Swap** | "Swap" on mockup card | Updated composite + manifest | Manual Workspace refresh |
| **Lock Artwork** | "Lock" button | Artwork moved to locked/ | Export (or review-only) |
| **Export** | "Export to Etsy" button | outputs/exports/`sku`/<export_id>/ | Hand-off to Etsy |
| **Detail Closeup** | "Add Detail Closeup" link | /`slug`/detail-closeup/editor | Interactive zoom/pan editor |
```text

**Date Created:** February 4, 2026
**Status:** ✅ COMPLETE
**Last Updated:** February 4, 2026
**Intended Audience:** System architects, AI specialists, developers implementing extensions
````

---

## UPDATES (February 24, 2026): Director's Suite Video Generation Enhancements

Overview

The Director's Suite Video Rendering system received comprehensive enhancements to improve reliability, error reporting, and user experience. See [Video-Generation-Workflow-Report.md](../../workflows/Video-Generation-Workflow-Report.md) for complete technical details.

### Key Enhancements

#### 1. **Master Artwork Always Included**

**Change:** Videos now always start with the master artwork as the first frame/segment, regardless of mockup selection.

**Rationale:** Provides context and bookending for the promo video, ensuring complete visual story.

**Implementation:** `video_service.py::_generate_kinematic_video()` always prepends master artwork to video sequence.

#### 2. **Pan Direction Cycling**

**Change:** Each mockup now pans in a different direction when "Auto Alternate Pan" is enabled.

## Pan Directions

- **Up:** Pans from bottom frame to focal point
- **Down:** Pans from top frame to focal point
- **Left:** Pans from right frame to focal point
- **Right:** Pans from left frame to focal point

**Pattern:** Up → Down → Left → Right → (repeat)

**Implementation:** New function `buildPanExpressions()` in `render.js` applies per-mockup direction expressions.

### 3. **Rendering Overlay UI**

**Change:** Visual feedback during video generation with animated spinner overlay.

## Components

- Semi-transparent dark overlay on video preview
- Animated spinner with orange accent top border
- "Rendering Video..." text status message
- Automatically appears on START RENDER click
- Automatically dismisses when rendering completes or fails

**Implementation:** CSS spinner in `video_suite.css`, JS control in `video_cinematic.js`.

### 4. **Robust Error Reporting**

**Change:** Action Center now displays actual error messages instead of generic "Failed to save settings."

## Error Details Captured

- HTTP status code (400, 500, etc.)
- Server error message (KeyError, validation error, etc.)
- Raw response text if JSON parsing fails
- Full stack trace in browser console

**Implementation:** Enhanced `postJson()` wrapper in `video_cinematic.js` with detailed error parsing.

### 5. **Storyboard Selection UI Sync**

**Change:** "Chosen Mockups (Video Order)" panel now populates on page load and updates live.

## Behavior

- Calls `renderChosenList()` on page load after initialization
- Auto-selects 5 mockups if none selected
- Live updates checkbox changes
- Fallback to `data-filename` if `data-mockup-id` missing

**Implementation:** Improved initialization sequence in `video_cinematic.js`.

### 6. **URL Data Attributes (404 Fix)**

**Change:** Fixed 404 errors when clicking START RENDER by passing URLs via `data-*` attributes instead of Jinja templates in static JS.

**Problem:** Static JS file contained literal template strings (`{{ settings_url }}`) which became 404 requests.

**Solution:** Template passes all URLs as `data-*` attributes on root element:

- `data-status-url="/api/artwork/{slug}/status"`
- `data-generate-url="/api/artwork/{slug}/video/generate"`
- `data-delete-url="/api/artwork/{slug}/video/delete"`
- `data-settings-url="/api/artwork/{slug}/video/settings"`

**Implementation:** Updated `video_workspace.html` with data attributes, updated `video_cinematic.js` to read at runtime.

#### 7. **CSS Refactoring**

**Change:** analysis_workspace.html styles moved to dedicated stylesheet.

## Benefits

- Eliminates inline styles (architectural requirement)
- Improves cache busting potential
- Maintains CSS variable consistency
- Pure template without styling logic

**Implementation:** New file `analysis_workspace.css`, template uses `workflow_css` macro.

### 8. **Footer Link Theming**

**Change:** Footer links now properly themed for dark/light mode with correct color contrast.

## Colors

- **Light Mode:** Text `#1a1a1a` (dark gray), Hover `#e76a25` (orange)
- **Dark Mode:** Text `#FFFFFF` (white), Hover `#e76a25` (orange)

**Implementation:** Updated `sidebar.css` with theme-specific selectors.

### Files Modified

| File | Layer | Change |
| ------ | ------- | -------- |
| `video_service.py` | 2 (Services) | Master artwork inclusion logic |
| `artwork_routes.py` | 2 (Services) | Error normalization improvements |
| `video_routes.py` | 3 (Routes) | URL data attribute preparation |
| `video_cinematic.js` | 4 (UI) | Error parsing, overlay control, storyboard sync |
| `render.js` | 4 (UI) | Pan direction cycling expressions |
| `video_workspace.html` | 4 (UI) | Data attributes, overlay markup |
| `video_suite.css` | 4 (UI) | Overlay styles, spinner animation |
| `analysis_workspace.css` | 4 (UI) | NEW: Dedicated stylesheet |
| `analysis_workspace.html` | 4 (UI) | Removed inline styles |
| `sidebar.css` | 4 (UI) | Footer theme colors |

### Testing Status

✅ All 8 improvements verified manually
✅ No regression in existing video generation
✅ Error messages now actionable
✅ Rendering overlay improves UX
✅ No 404 errors on START RENDER

### Documentation

For complete technical reference, see:

- [todays-work-24-FEB-2026.md](../../changelog-reports/todays-work-24-FEB-2026.md) - Implementation details
- [QUICK_REFERENCE.md](../../changelog-reports/QUICK_REFERENCE.md) - Updated feature summary
- [Video-Generation-Workflow-Report.md](../../workflows/Video-Generation-Workflow-Report.md) - Complete workflow reference

---
