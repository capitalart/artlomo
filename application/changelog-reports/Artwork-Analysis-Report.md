# ARTLOMO ARTWORK ANALYSIS SYSTEM REPORT

**Report Date:** March 1, 2026
**System:** AI-Powered Artwork Analysis Engine for Etsy Listings
**Artist:** Robin Custance (South Australian Digital Landscape Artist)

---

## TABLE OF CONTENTS

1. [System Overview](#1-system-overview)

1. [Architecture & Data Flow](#2-architecture--data-flow)

1. [Image Processing Pipeline](#3-image-processing-pipeline)

1. [AI Model Integration](#4-ai-model-integration)

1. [Prompting Strategy](#5-prompting-strategy)

1. [Output Schema & Validation](#6-output-schema--validation)

1. [Error Handling & Recovery](#7-error-handling--recovery)

1. [File Structure & Dependencies](#8-file-structure--dependencies)

1. [Configuration & Parameters](#9-configuration--parameters)

1. [API Endpoints](#10-api-endpoints)

1. [Data Storage & Persistence](#11-data-storage--persistence)

1. [Performance Metrics & Optimization](#12-performance-metrics--optimization)

1. [Security & Authentication](#13-security--authentication)

1. [Recommendations & Enhancement Opportunities](#14-recommendations--enhancement-opportunities)

---

## 1. SYSTEM OVERVIEW

### Purpose

The ArtLomo Artwork Analysis System automatically analyzes digital artwork images and generates competition-ready Etsy product listings with:

- Professional titles and descriptions

- SEO-optimized filenames

- Heritage-respectful cultural context

- Visual analysis metadata (subject, palette, mood, dot rhythm)

- Material specifications

- Primary and secondary color identification

### Scope

- **Supported AI Models:** OpenAI GPT-4o (primary), GPT-4 (fallback) | Google Gemini (native)

- **Input Format:** JPEG/PNG artwork images (optimized to ~1024px long edge for API)

- **Output Format:** Structured JSON with nested art analysis metadata

- **Processing:** Asynchronous background workers with status polling

### Key Design Principles

1. **Art-First Hierarchy:** Visual emotion and aesthetics lead, followed by technical specs

1. **Geographic Specificity:** Preserve specific place names (e.g., Bool Lagoon) without generalization

1. **Heritage Respectful:** Acknowledge Traditional Custodians appropriately without claiming ownership

1. **Museum-Grade Quality:** Emphasize 14,400px resolution and 300 DPI museum-standard output

1. **Limited Edition Concept:** Cap at 25 copies max to create exclusivity

---

## 2. ARCHITECTURE & DATA FLOW

### High-Level Flow

```text
User Upload (artwork_master.jpg)
    ↓
[Image Optimization & Validation]
    ↓
[Seed Context Extraction] (artist story, location hints)
    ↓
[AI Analysis Request]
    ├─→ OpenAI GPT-4o (Primary)
    │   ├─→ Model Fallback Stack (gpt-4, gpt-3.5-turbo)
    │   └─→ Temperature/Max-Tokens Adaptation
    │
    └─→ Gemini (Alternative)
        ├─→ Native JSON mode
        └─→ Fallback parsing

    ↓
[Structured Output Parsing & Validation]
    ↓
[Metadata Enrichment]
    ├─→ Etsy boilerplate injection
    ├─→ Gold standard blocks (print size guide, how-to-print)
    ├─→ Title sanitization (max 140 chars)
    ├─→ Tag validation (exactly 13, max 20 chars each)
    └─→ SEO filename constraint (max 70 chars including .jpg)

    ↓
[Listing.json Persistence]
    ├─→ metadata_{provider}.json (raw analysis)
    ├─→ listing.json (final enriched payload)
    └─→ status.json (processing status)

    ↓
[Display in Analysis Workspace]
    └─→ Manual review & editing before finalization
```

### Component Responsibilities

| Component | Layer | File(s) | Responsibility |
| --- | --- | --- | --- |
| **Routes** | 3 (HTTP) | `analysis/api/routes.py` | REST endpoints, worker threading, status responses |
| **OpenAI Service** | 2 (Business) | `analysis/openai/service.py` | Image encoding, API calls, model fallback, structured parsing |
| **Gemini Service** | 2 (Business) | `analysis/gemini/service.py` | Image encoding, Gemini API integration, error classification |
| **Prompts** | 1 (Core) | `analysis/prompts.py` | System prompt templates, seed context injection |
| **Storage** | 1 (Core) | `upload/services/storage_service.py` | File paths, image naming conventions |
| **Utilities** | 1 (Core) | `utils/ai_services.py` | OpenAI/Gemini client initialization |

---

## 3. IMAGE PROCESSING PIPELINE

### Image Optimization Strategy

#### Input Handling

```python
Source Image (e.g., 4000x3000 pixels)
    ↓
[PIL.Image.open() + EXIF/DPI/ICC Preservation]
    ↓
[Thumbnail to 1024px max long edge (LANCZOS resampling)]
    ↓
[RGB Color Space Conversion]
    ↓
[Quality-stepping JPEG encoding]
    ├─→ Quality 95: Measure bytes
    ├─→ Quality 90: If still oversize, retry
    └─→ Quality 85: Final fallback

    ↓
[Base64 Encoding for API]
    ↓
[Data URL Injection: data:image/jpeg;base64,{...}]
```

### Quality Control Metrics

- **Max Long Edge (Vision API):** 1024 pixels

- **Max File Size:** 20 MB (configurable via `OPENAI_IMAGE_MAX_MB`)

- **Preserved Metadata:** EXIF, DPI, XMP, ICC color profile

- **Output Format:** JPEG (optimized), RGB color space

### Configuration Parameters

```text
OPENAI_IMAGE_MAX_MB = 20          # Max image size for OpenAI
MAX_LONG_EDGE = 1024              # Max resolution for vision API
JPEG_QUALITY_STEPS = [95, 90, 85] # Progressive quality reduction
RESAMPLING_FILTER = LANCZOS       # High-quality downsampling
```

---

## 4. AI MODEL INTEGRATION

### OpenAI Integration

#### OpenAI Client Initialization

```python
from openai import OpenAI
client = OpenAI(api_key=config.OPENAI_API_KEY)
```

#### Model Stack Strategy

1. **Primary Model:** `gpt-4o` (recommended for vision + structured output)

1. **Fallback Stack:** `["gpt-4o", "gpt-4", "gpt-3.5-turbo"]`

1. **Auto-fallback Triggers:**

  - 404 Model Not Found

  - 429 Rate Limit

  - 503 Service Unavailable

  - Parameter incompatibility (max_tokens, temperature)

#### Temperature & Sampling

- **Default Temperature:** 0.2 (low randomness for consistency)

- **Max Completion Tokens:** 2000 (sufficient for full listing metadata)

- **Response Format:** `OpenAIArtworkAnalysis` (Pydantic model with structured output)

#### Structured Output Contract

```python
response_format = OpenAIArtworkAnalysis

# OpenAI enforces strict JSON schema matching

```

### Gemini Integration

#### Gemini Client Initialization

```python
from google import genai
client = genai.Client(api_key=config.GEMINI_API_KEY)
```

#### Features

- **Native JSON Mode:** Built-in structured output

- **Model:** `gemini-2.0-flash` (default) or `gemini-pro-vision`

- **Singleton Client:** Reused across requests to minimize handshake overhead

- **Safety Settings:** Configured to allow creative content

#### Response Handling

```python

# Gemini returns raw JSON text

parsed_json = json.loads(response.text)

# Safe parsing with fallback error handling

```

### Error Classification System

#### OpenAI Error Codes

| Code | Meaning | Recovery |
| --- | --- | --- |
| `ERR_AUTH` | Invalid API key | Check credentials, retry |
| `ERR_RATE_LIMIT` | Quota exceeded | Wait & retry later |
| `ERR_TIMEOUT` | Request timed out | Retry with longer timeout |
| `ERR_BALANCE` | Billing quota exceeded | Check billing account |
| `ERR_MODEL` | Model not found | Try fallback model |
| `ERR_BAD_REQUEST` | Invalid parameters | Fix request payload |
| `ERR_UNKNOWN` | Unexpected error | Log & escalate |

#### Gemini Error Codes

| Code | Meaning | Recovery |
| --- | --- | --- |
| `ERR_AUTH` | Unauthorized | Verify API key |
| `ERR_RATE_LIMIT` | Quota exhausted | Wait & retry |
| `ERR_TIMEOUT` | Deadline exceeded | Retry |
| `ERR_BALANCE` | Insufficient quota | Check billing |
| `ERR_MODEL` | Model unavailable | Use fallback |
| `ERR_BAD_REQUEST` | Invalid input | Validate input |

---

## 5. PROMPTING STRATEGY

### System Prompt Templates

#### OpenAI/GPT-4o System Prompt (HERITAGE_FIRST_SYSTEM_PROMPT)

## Role Definition

```text
"You are a world-renowned Art Curator & Professional Etsy Copywriter,
specialising in Australian digital landscape art."
```

## Critical Identity

- Persona: `{artist_name}`, South Australian artist

- Voice: Warm, contemporary, trustworthy

- Spelling: Australian (Colour, Grey, Recognise)

- Heritage Protocol: Respectful, no sacred knowledge claims

## Visual Analysis Requirements

1. **Subject:** Primary subject + explicit named place (e.g., Bool Lagoon)

1. **Dot Rhythm:** Rhythm description (sunbursts, ripples, currents)

1. **Palette:** Evocative color names

1. **Mood:** Emotional tone (tranquil, luminous, contemplative)

## Geographic Accuracy Rules

- DO NOT generalize specific places to broader regions

  - Example: Keep "Bool Lagoon" not "Limestone Coast"

- DO NOT introduce uncertain region names

- Prefer specific place names or keep neutral

## Traditional Custodians (Dynamic)

- Naracoorte → Bindjali

- Bool Lagoon → Boandik

- If unsure, use respectful generic acknowledgement

## Output Format (JSON Only)

```json
{
  "etsy_title": "...",           // <= 140 chars, pipe-separated
  "etsy_description": "...",     // Line breaks, multiple paragraphs
  "etsy_tags": ["tag1", ...],    // Exactly 13, max 20 chars each
  "seo_filename_slug": "...",    // Lowercase, hyphens, max 61 chars
  "visual_analysis": {
    "subject": "...",
    "dot_rhythm": "...",
    "palette": ["color1", ...],
    "mood": "..."
  },
  "materials": ["material1", ...], // Exactly 13 items
  "primary_colour": "...",
  "secondary_colour": "..."
}
```

#### Gemini System Prompt (PIONEER_GEMINI_SYSTEM_PROMPT)

## Differences from OpenAI

- Stricter JSON enforcement (no markdown/labelled sections)

- NO quotation marks at all ("and ')

- Hero metric justification: 14,400px + 300 DPI

- Description format: "Impressionistic Section --- LISTING_BOILERPLATE"

- Each paragraph must be >= 250 characters

### Prompt Injection Points

#### 1. Artist Story Context

```python
seed_info = load_seed_context(processed_dir)

# Provides artist_story, location hints, initial context

system_prompt = get_system_prompt(seed_info=seed_info)
```

#### 2. Merchant Mode Instructions

```text
MERCHANT MODE INSTRUCTIONS (SOURCE OF TRUTH):
{MASTER_ETSY_DESCRIPTION_ENGINE.md content}
```

#### 3. Few-Shot Example

```text
FEW-SHOT TARGET EXAMPLE (PIONEER STANDARD):
{MASTER-ARTWORK-ANALYSIS-LISTING-DESCRIPTION-EXAMPLE.md}
```

### User Prompt Structure

```text
"Analyse the following artwork image and produce structured listing fields.
Return ONLY a JSON object matching the required schema.
SKU: {sku}
Aspect ratio: {aspect_ratio}
Original filename: {original_filename}"

[Image data as base64 JPEG]
```

---

## 6. OUTPUT SCHEMA & VALIDATION

### Pydantic Schema (OpenAI)

**File:** `analysis/openai/schema.py`

```python
class VisualAnalysis(BaseModel):
    subject: str
    dot_rhythm: str
    palette: list[str]
    mood: str

class OpenAIArtworkAnalysis(BaseModel):
    etsy_title: str                # <= 140 chars
    description: str               # Multi-paragraph, line-break formatted
    tags: list[str]               # Exactly 13 items, max 20 chars each
    seo_filename_slug: str         # Lowercase, hyphens, max 61 chars
    visual_analysis: VisualAnalysis
    materials: list[str]           # Exactly 13 strings
    primary_colour: str
    secondary_colour: str
```

### Validation Rules

#### Title (`etsy_title`)

- Max 140 characters

- Contains "Digital Download" and "Large 48 Inch Print" (preferred)

| - Pipe-separated keywords (e.g., "Subject | Keyword | Location | Artist") |

- Aim for 13-14 words total

#### Description (`description`)

- Structured as: `[Generated Text]\n---\n[LISTING_BOILERPLATE]`

- Boilerplate includes:

  - LIMITED EDITION (25 copies)

  - TECHNICAL SPECIFICATIONS (14,400px, 300 DPI)

  - PRINTING NOTES (Officeworks, Printful, Gelato)

  - ABOUT THE ARTIST

  - ACKNOWLEDGEMENT OF COUNTRY

  - PRINT SIZE GUIDE (responsive to aspect ratio)

  - HOW TO PRINT

#### Tags (`tags`)

- Exactly 13 tags

- Each max 20 characters

- No special characters (alphanumeric + spaces only)

- Sanitization removes duplicates, hyphens, invalid chars

- Filler tags added if needed: "digital download", "printable art", "wall decor", etc.

#### SEO Filename (`seo_filename_slug`)

- Lowercase, hyphens only

- Max 61 characters (before `.jpg` extension)

- Format: `{short-title}-{location}-robin-custance` or `{sku}-{title}`

- Final output: `{slug}.jpg`

#### Materials (`materials`)

Standard list (always 13):

1. Digital Oil

1. 14400px Resolution

1. 300 DPI

1. High Res JPG

1. Virtual Acrylic

1. Digital Dotwork

1. Museum Quality File

1. Digital file

1. Instant download

1. RGB colour profile

1. Printable wall art

1. High resolution

1. Gallery-ready file

#### Colors

- `primary_colour`: Standard color name (e.g., "Gold", "Blue")

- `secondary_colour`: Standard color name (e.g., "Indigo")

- No hex codes or technical color spaces in public output

---

## 7. ERROR HANDLING & RECOVERY

### Retry Logic

#### OpenAI Retry Strategy

```text
For each model in [selected_model, ...fallback_stack, "gpt-4o"]:
    For each attempt in [1...max_retries]:
        Try calling OpenAI API

        If temperature unsupported:
            Retry once with temperature=1.0

        If should_fallback (404, 429, 503):
            Try next model

        If authentication/balance error:
            Raise immediately (no retry)

        If success:
            Break and process response
```

#### Gemini Retry Strategy

```text
Try Gemini API
If NotFound (404) or ResourceExhausted (429):
    Fallback to alternative model
If ServiceUnavailable:
    Retry immediately
If auth error:
    Raise immediately
```

### Error Responses

#### API Error Response Format

```json
{
  "error": "Analysis failed",
  "slug": "artwork-slug",
  "error_code": "ERR_RATE_LIMIT",
  "message": "OpenAI request failed: Rate limit exceeded"
}
```

#### Status File Updates

```json
{
  "status": "error",
  "slug": "artwork-slug",
  "stage": "error",
  "message": "Analysis failed",
  "error": "Rate limit exceeded",
  "error_code": "ERR_RATE_LIMIT",
  "source": "openai"
}
```

### Fallback Mechanisms

1. **Model Fallback:** If GPT-4o fails, try GPT-4, then GPT-3.5-turbo

1. **Provider Fallback:** If OpenAI fails, user can select Gemini

1. **Temperature Fallback:** If temperature unsupported (o1/o3), set to 1.0

1. **Manual Fallback:** User can manually trigger reanalysis with different provider

---

## 8. FILE STRUCTURE & DEPENDENCIES

### Directory Structure

```text
application/
├── analysis/
│   ├── __init__.py
│   ├── prompts.py                          # System prompts & context builders
│   ├── routes.py                           # Flask blueprint (rules-reference)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                       # REST endpoints (POST /api/analysis/{provider}/{slug})
│   │
│   ├── openai/
│   │   ├── __init__.py
│   │   ├── schema.py                       # Pydantic model for OpenAI response
│   │   └── service.py                      # OpenAI analysis implementation
│   │
│   ├── gemini/
│   │   ├── __init__.py
│   │   ├── schema.py                       # Gemini response validation
│   │   └── service.py                      # Gemini analysis implementation
│   │
│   ├── manual/
│   │   ├── ...                             # Manual analysis UI (no AI)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── preset_service.py               # Analysis preset management
│   │
│   ├── instructions/
│   │   ├── MASTER_ETSY_DESCRIPTION_ENGINE.md      # Merchant mode guidelines
│   │   └── MASTER-ARTWORK-ANALYSIS-LISTING-DESCRIPTION-EXAMPLE.md  # Target example
│   │
│   └── ui/
│       └── templates/
│           └── etsy_rules_reference.html   # Public Etsy rules reference page
│
├── utils/
│   ├── ai_services.py                      # OpenAI & Gemini client initialization
│   ├── ai_utils.py                         # JSON parsing, sanitization helpers
│   └── house_prompts.py                    # LISTING_BOILERPLATE, seed context builders
│
├── upload/
│   └── services/
│       └── storage_service.py              # File naming, path management
│
└── artwork/
    └── routes/
        └── artwork_routes.py               # Analysis workspace rendering
```

### Key Dependencies

```text
External:
- openai>=1.0.0                    # OpenAI Python SDK
- google-genai                     # Google Generative AI
- pydantic>=2.0                    # Schema validation
- Pillow (PIL)                     # Image processing

Internal:
- application.utils.ai_services    # Client initialization
- application.utils.ai_utils       # JSON parsing
- application.upload.services      # Storage paths
- application.common.utilities     # Atomic file writing
```

---

## 9. CONFIGURATION & PARAMETERS

### Environment Variables & Config

| Parameter | Type | Default | Purpose |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | string | *required* | OpenAI API authentication |
| `OPENAI_DEFAULT_MODEL` | string | `gpt-4o` | Primary model for analysis |
| `OPENAI_MODEL_STACK` | string/list | `["gpt-4o", "gpt-4"]` | Fallback model sequence |
| `OPENAI_IMAGE_MAX_MB` | int | `20` | Max image size (MB) for vision API |
| `OPENAI_API_TIMEOUT` | float | `60.0` | Request timeout (seconds) |
| `OPENAI_API_RETRIES` | int | `1` | Retry attempts per model |
| `ARTWORK_ANALYSIS_MAX_OUTPUT_TOKENS` | int | `2000` | Max response length |
| `TEMPERATURE` | float | `0.2` | Sampling temperature (creativity) |
| `GEMINI_API_KEY` | string | *required* | Google Gemini API key |
| `LAB_PROCESSED_DIR` | path | `./var/lab/processed` | Processed artwork storage |
| `LAB_UNPROCESSED_DIR` | path | `./var/lab/unprocessed` | Raw uploads |
| `LAB_LOCKED_DIR` | path | `./var/lab/locked` | Finalized listings |

### Boilerplate Content

```python

# From application/utils/house_prompts.py

LISTING_BOILERPLATE = """
[LIMITED EDITION STATEMENT]
Only 25 copies will ever be released to preserve exclusivity.

[TECHNICAL SPECIFICATIONS]
- Ultra-High Resolution: 14,400 pixels on the long edge
- Print up to 48 inches (121.9 cm) wide without quality loss
- 300 DPI (dots per inch) for museum-grade quality
- RGB colour profile for digital/screen display

[PRINTING NOTES]
For the most authentic 'fine art' feel, print on heavyweight matte paper or fine art canvas.

[ABOUT THE ARTIST]
Robin Custance is a South Australian digital landscape artist...

[ACKNOWLEDGEMENT OF COUNTRY]
I acknowledge the Traditional Custodians of [location], the [custodian name] people.

[PRINT SIZE GUIDE]
Optimized for 15+ standard frame sizes in multiple aspect ratios.

[HOW TO PRINT]
For Australia: Officeworks, professional photo labs.
For International: Printful, Gelato, Staples.
"""
```

---

## 10. API ENDPOINTS

### Analysis Trigger Endpoints

#### POST `/api/analysis/openai/{slug}`

**Purpose:** Trigger OpenAI analysis asynchronously
**Method:** POST
**Auth:** CSRF required

## Request

```json
{}
```

## Response (Immediate)

```json
{
  "status": "ok",
  "message": "OpenAI analysis queued",
  "slug": "artwork-slug",
  "analysis_source": "openai"
}
```

## Worker Process

- Promotes to processed (if needed)

- Loads seed context

- Encodes image to base64

- Calls OpenAI API with system prompt + image

- Validates structured output

- Writes `metadata_openai.json` + `listing.json`

- Returns status: "complete" or "error"

#### POST `/api/analysis/gemini/{slug}`

**Purpose:** Trigger Gemini analysis asynchronously

## Similar to OpenAI endpoint, but uses Gemini API

### Status Polling Endpoints

#### GET `/api/analysis/status/{slug}`

**Purpose:** Poll analysis progress

## Response

```json
{
  "status": "ok",
  "slug": "artwork-slug",
  | "stage": "processing | complete | error", |
  "message": "Running OpenAI analysis",
  "done": false,
  "error": null,
  "error_code": null,
  | "source": "openai | gemini | manual" |
}
```

#### GET `/artworks/{slug}/status`

**Purpose:** Get overall artwork status

## Response includes

- analysis_status

- processing_stage

- last_updated_at

---

## 11. DATA STORAGE & PERSISTENCE

### JSON File Artifacts

#### `metadata_openai.json`

```json
{
  "source": "openai",
  "model": "gpt-4o",
  "slug": "artwork-slug",
  "sku": "RJC-0270",
  "original_filename": "artwork.jpg",
  "image": {
    "src_w": 4000,
    "src_h": 3000,
    "dst_w": 1024,
    "dst_h": 768,
    "bytes": 245000,
    "quality": 95
  },
  "analysis": {
    "etsy_title": "...",
    "etsy_description": "...",
    "etsy_tags": ["..."],
    "seo_filename_slug": "...",
    "visual_analysis": {...},
    "materials": [...],
    "primary_colour": "Gold",
    "secondary_colour": "Indigo"
  },
  "created_at": "2026-03-01T10:30:00Z",
  "prompt_id": "abc123...",
  "temperature": 0.2
}
```

#### `listing.json`

```json
{
  "slug": "artwork-slug",
  "sku": "RJC-0270",
  "title": "Bool Lagoon Impressionist - Digital Download",
  "description": "...[AI-generated + boilerplate]...",
  "tags": ["digital download", "printable art", "..."],
  "materials": ["Digital Oil", "14400px Resolution", ...],
  "price": "29.95",
  "quantity": 25,
  "seo_filename": "RJC-0270-bool-lagoon-impressionist.jpg",
  "primary_colour": "Gold",
  "secondary_colour": "Indigo",
  "visual_analysis": {
    "subject": "Bool Lagoon wetlands",
    "dot_rhythm": "radiating sunbursts",
    "palette": ["Gold", "Indigo", "Ochre"],
    "mood": "tranquil, luminous"
  },
  "analysis_source": "openai",
  "analysis_status": {
    "stage": "complete|error",
    "message": "Analysis complete",
    "done": true,
    "error": null,
    "source": "openai",
    "updated_at": "2026-03-01T10:30:00Z"
  },
  "created_at": "2026-03-01T10:25:00Z",
  "updated_at": "2026-03-01T10:30:00Z"
}
```

#### `status.json`

```json
{
  "status": "ok|error",
  "slug": "artwork-slug",
  | "stage": "processing | complete | error", |
  "message": "Analysis complete",
  "done": true,
  "error": null,
  "error_code": null,
  | "source": "openai | gemini | manual" |
}
```

### File Atomicity

```python

# All JSON writes are atomic (write to temp file, then move)

write_json_atomic(path, data)

# Ensures no partial/corrupted files if process crashes

```

---

## 12. PERFORMANCE METRICS & OPTIMIZATION

### Typical Response Times

| Operation | Time | Notes |
| --- | --- | --- |
| Image optimization (PIL) | 0.5-2s | Resize, JPEG quality loop |
| OpenAI API request | 5-15s | Model inference, complexity |
| Gemini API request | 8-20s | Typically slower than OpenAI |
| JSON validation | 0.1s | Pydantic schema check |
| Boilerplate injection | 0.2s | String templating |
| File I/O (JSON parse/write) | 0.1-0.3s | Atomic operations |
| **Total (OpenAI)** | **6-18s** | Network + inference |
| **Total (Gemini)** | **9-22s** | Network + inference |

### Optimization Techniques

1. **Image Optimization:**

  - PIL thumbnail with LANCZOS (high-quality downsampling)

  - Progressive quality reduction (95 → 90 → 85) to binary search file size

  - Preserve EXIF, DPI, ICC profile for quality tracking

1. **API Caching:**

  - No caching of AI responses (unique per artwork)

  - Metadata cached in memory during session

1. **Concurrent Processing:**

  - Background worker threads per slug

  - No blocking on main Flask thread

  - Status polling via separate endpoint

1. **Gemini Singleton Client:**

  - Single client instance reused across requests

  - Avoids repeated authentication handshakes

  - Per-worker-process initialization

1. **Model Stack Strategy:**

  - Try faster/cheaper models first

  - Fallback to premium models only on failure

  - Minimize total API calls

### Load Testing Recommendations

- **Concurrent Analyses:** Test with 5-10 simultaneous uploads

- **Image Sizes:** Test 2-8MB range (typical artwork downloads)

- **Rate Limiting:** Monitor OpenAI/Gemini quota exhaustion

- **Database:** Monitor listing.json update lock contention

---

## 13. SECURITY & AUTHENTICATION

### API Security

1. **CSRF Protection:**

  - All POST requests require CSRF token

  - Token validated via `require_csrf_or_400()` decorator

1. **Input Validation:**

  - Slug validation via `is_safe_slug()` helper

  - Image path sandboxing within `LAB_PROCESSED_DIR`

1. **API Key Management:**

  - OpenAI key from environment: `config.OPENAI_API_KEY`

  - Gemini key from environment: `config.GEMINI_API_KEY`

  - Never logged or exposed in responses

1. **Error Message Sanitization:**

  - No sensitive data in public error messages

  - Full error details logged server-side only

  - User sees only generic "Analysis failed" messages

### Data Privacy

1. **Image Processing:**

  - Images optimized but never permanently stored externally

  - Metadata (image dimensions, quality) logged for debugging

  - No image upload to external services except AI vendor APIs

1. **Listing Data:**

  - JSON files stored locally (not synced to cloud)

  - User has full ownership of generated content

  - Can edit/delete before publishing to Etsy

1. **AI Vendor Data:**

  - Images sent to OpenAI/Gemini APIs over HTTPS

  - Vendors may use data per their privacy policies

  - User should review AI provider terms

---

## 14. RECOMMENDATIONS & ENHANCEMENT OPPORTUNITIES

### Short-Term Improvements

1. **Prompt Refinement:**

  - A/B test system prompts with different phrasings

  - Measure output consistency across model versions

  - Collect user feedback on generated titles/descriptions

1. **Error Handling Enhancements:**

  - Implement exponential backoff for rate limit recovery

  - Add human-readable error messages for common failures

  - Provide recovery suggestions (e.g., "Try again in 60 seconds")

1. **Image Processing:**

  - Test WEBP format for better compression

  - Implement progressive JPEG for faster transmission

  - Add HEIC/HEIF support for mobile uploads

1. **Monitoring & Observability:**

  - Track model success/failure rates per provider

  - Monitor API latency trends

  - Alert on quota exhaustion before hitting limits

### Medium-Term Enhancements

1. **Multi-Language Support:**

  - Extend prompts to support French, German, Spanish

  - Localize Etsy boilerplate for regional markets

  - Geographic custodian mapping for international artists

1. **Advanced Image Analysis:**

  - Implement color histogram analysis (palette verification)

  - Use OpenAI Vision to auto-detect aspect ratio

  - Validate artwork content (e.g., confirm landscape/portrait)

1. **Custom Presets:**

  - Allow artists to create analysis presets

  - Store preferred prompts/tone/style templates

  - Support rapid re-analysis with custom instructions

1. **Structured Data Versioning:**

  - Track analysis version history

  - Allow rollback to previous versions

  - Compare changes between AI providers

### Long-Term Strategic Opportunities

1. **In-House Fine-Tuning:**

  - Collect successful analysis outputs

  - Fine-tune custom GPT or smaller open-source model

  - Reduce dependency on expensive API calls

1. **Batch Processing:**

  - Implement batch API endpoints for multi-artwork analyses

  - Reduce per-call overhead with volume discounts

  - Schedule batch jobs during low-cost hours

1. **Hybrid Human-AI Workflow:**

  - AI generates initial draft

  - Human expert refines and approves

  - Feedback loop improves model outputs

1. **Analytics Dashboard:**

  - Artist can view analysis metrics (titles/descriptions generated)

  - Track which prompts generate best Etsy performance

  - Rate AI suggestions and influence future outputs

1. **Integration with Etsy API:**

  - Auto-publish listings directly to Etsy upon approval

  - Sync inventory and pricing

  - Collect performance metrics (views, sales) back into system

---

## APPENDIX: EXAMPLE REQUEST/RESPONSE CYCLE

### 1. User Triggers Analysis

```bash
POST /api/analysis/openai/blue-wren-songlines
X-CSRFToken: abc123...

{}
```

### 2. Immediate Response

```json
{
  "status": "ok",
  "message": "OpenAI analysis queued",
  "slug": "blue-wren-songlines"
}
```

### 3. Background Worker Processes

```text
[ai_processing] slug=blue-wren-songlines
[ai_processing] Loading seed context...
[ai_processing] Image size: 4096x3072, optimizing...
[ai_processing] Encoded to base64 (245KB)
[ai_processing] OpenAI request: model=gpt-4o, tokens=2000
[ai_processing] Response received (3.2s)
[ai_processing] Validation passed
[ai_processing] Boilerplate injected
[ai_processing] metadata_openai.json written
[ai_processing] listing.json written
[SUCCESS] Analysis complete
```

### 4. User Polls Status

```bash
GET /api/analysis/status/blue-wren-songlines
```

```json
{
  "status": "ok",
  "slug": "blue-wren-songlines",
  "stage": "complete",
  "message": "OpenAI analysis complete",
  "done": true,
  "source": "openai"
}
```

### 5. Analysis Workspace Displays Results

```html
| Title: Blue Wren Songlines | Large 48 Inch Digital Download | Robin Custance |
Description:
  Bring the songlines of the Blue Wren into your home...
  [+ boilerplate]
Primary Colour: Sapphire Blue
Secondary Colour: Ochre Gold
Tags: [13 tags listed]
Visual Analysis:
  Subject: Blue Wren at sunset, songlines narrative
  Dot Rhythm: Flowing concentric ripples
  Palette: Sapphire blue, Ochre gold, ...
  Mood: Spiritual, luminous, meditative
```

### 6. User Review & Edit

```text
[User edits title, adds location detail, adjusts colors]
Click "Save"
→ listing.json updated
→ Ready for publication
```

---

## CONCLUSION

The ArtLomo Artwork Analysis System represents a sophisticated blend of:

- **Specialized AI prompt engineering** for art curation

- **Robust error handling and fallback mechanisms**

- **Image optimization for vision APIs**

- **Structured data validation** with Pydantic

- **Respectful heritage integration** avoiding cultural appropriation

- **Museum-quality technical specifications** as core value proposition

The system is production-ready for high-volume artist uploads while maintaining the art-first aesthetic and ethical heritage protocols required for authentic Australian digital landscape representation.

---

**Report Generated:** March 1, 2026
**System Status:** Operational (OpenAI + Gemini)
**Last Updated:** 2026-03-01T14:30:00Z
