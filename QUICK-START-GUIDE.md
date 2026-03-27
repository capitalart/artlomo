# QUICK START GUIDE - ARTLOMO ANALYSIS SYSTEM

## March 7, 2026 Update

- For current system-level documentation, review:

  - `application/docs/ARTLOMO_OVERVIEW_2026-03-07.md`

  - `application/docs/ARTLOMO_SYSTEM_SOFTWARE_REPORT_2026-03-07.md`

  - `application/docs/GOOGLE_CLOUD_VM_SPECS_REPORT_2026-03-07.md`

  - `application/docs/TOOLS_SH_COVERAGE_REPORT_2026-03-07.md`

- For automated environment snapshots, run:

  - `application/tools/app-stacks/files/tools.sh sysinfo`

  - `application/tools/app-stacks/files/tools.sh all`

- For a single curated AI handoff file, run:

  - `application/tools/app-stacks/files/tools.sh gemini`

  - Output: `application/tools/app-stacks/stacks/application-gemini-code-stack-<TIMESTAMP>.md`

## 📦 Files Created

### Main Deliverables

1. **`artlomo-analysis-complete-package.tar.gz`** (72 KB)

- Complete analysis system source code

- Comprehensive technical documentation

- All prompts, schemas, and utilities

1. **`Artwork-Analysis-Report.md`** (also included in archive)

- 14-section technical deep-dive

- Architecture diagrams

- Performance metrics

- Enhancement recommendations

1. **`ANALYSIS-PACKAGE-README.md`** (also included in archive)

- Package contents manifest

- How to use the archive

- Configuration reference

- Troubleshooting guide

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Extract the Archive

```bash
tar -xzf artlomo-analysis-complete-package.tar.gz
```

### Step 2: Read the Overview

```bash

# Start here for 10-minute overview

less ANALYSIS-PACKAGE-README.md

# Or jump to specific sections:

# - "PACKAGE CONTENTS" → Understand file structure

# - "HOW TO USE THIS PACKAGE" → Next steps

# - "CRITICAL IMPLEMENTATION DETAILS" → Key info

```

### Step 3: Review the Full Report

```bash

# Comprehensive technical documentation

less Artwork-Analysis-Report.md

# Key sections to read in order:

# 1. SYSTEM OVERVIEW (what it does)

# 2. ARCHITECTURE & DATA FLOW (how it works)

# 3. IMAGE PROCESSING PIPELINE (technical details)

# 4. AI MODEL INTEGRATION (OpenAI & Gemini)

# 5. PROMPTING STRATEGY (the secret sauce)

# 6. OUTPUT SCHEMA & VALIDATION (expected output)

```

### Step 4: Examine Source Code

```bash

# Prompts & system instructions

cat application/analysis/prompts.py

# OpenAI implementation (778 lines)

cat application/analysis/openai/service.py

# Gemini implementation (928 lines)

cat application/analysis/gemini/service.py

# REST API endpoints

cat application/analysis/api/routes.py

# Etsy output guidelines

cat application/analysis/instructions/MASTER_ETSY_DESCRIPTION_ENGINE.md
```

---

## 📊 System at a Glance

### What It Does

```text
User Uploads Artwork Image
           ↓
AI Analyzes Image (OpenAI GPT-4o or Google Gemini)
           ↓
Generates Etsy Listing Metadata:
  - Professional title (≤140 chars, SEO-optimized)
  - Compelling description (art-first + technical specs)
  - 13 SEO tags (max 20 chars each)
  - Visual analysis (subject, palette, mood, dot rhythm)
  - Color identification (primary + secondary)
  - Material specifications
  - SEO filename (max 70 chars excluding .jpg)
           ↓
User Reviews & Edits in ArtLomo Workspace
           ↓
Ready to Publish or Lock
```

### Key Features

✅ **Two AI Providers:** OpenAI (primary) + Gemini (alternative)
✅ **Smart Fallback:** Auto-retry on different models if first fails
✅ **Image Optimization:** 4000px → 1024px with quality-stepping JPEG
✅ **Heritage Respectful:** No colonial appropriation, proper custodian acknowledgement
✅ **Museum-Grade:** Emphasizes 14,400px resolution + 300 DPI
✅ **Fully Customizable:** Prompts, boilerplate, constraints all configurable
✅ **Production Ready:** Error handling, logging, atomic file I/O

---

## 🏗️ Architecture in 60 Seconds

```text
┌─────────────────────────────────────────┐
│   USER UPLOADS ARTWORK (Flask Route)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  IMAGE OPTIMIZATION (PIL)               │
│  • Resize 1024px max                    │
│  • Quality-step JPEG (95→90→85)         │
│  • Preserve EXIF/DPI/ICC                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  BACKGROUND WORKER (Async Thread)       │
│  • Load artist context (seed_info)      │
│  • Encode image to base64               │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
    ┌────────┐    ┌────────┐
    │ OpenAI │ OR │ Gemini │
    │ API    │    │ API    │
    └────┬───┘    └───┬────┘
         │            │
         └──────┬─────┘
                ▼
    ┌──────────────────────┐
    │ STRUCTURED PARSING   │
    │ (JSON Validation)    │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ BOILERPLATE INJECT   │
    │ + Sanitization       │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ Write JSON Files:    │
    │ • metadata_*.json    │
    │ • listing.json       │
    │ • status.json        │
    └──────────────────────┘
```

---

## 🎯 What Each File Does

### Core Services

| File | Lines | Purpose |
| --- | --- | --- |
| `application/analysis/openai/service.py` | 778 | OpenAI API integration, image optimization, error handling |
| `application/analysis/gemini/service.py` | 928 | Gemini API integration, singleton client, JSON parsing |
| `application/analysis/prompts.py` | 300+ | System prompts, context builders, profile loading |
| `application/analysis/api/routes.py` | 335 | REST endpoints, worker threads, status management |

### Instructions & Guidelines

| File | Purpose |
| --- | --- |
| `MASTER_ETSY_DESCRIPTION_ENGINE.md` | Merchant mode rules, field constraints, quality standards |
| `MASTER-ARTWORK-ANALYSIS-LISTING-DESCRIPTION-EXAMPLE.md` | Target output example (Pioneer standard) |

### Utilities

| File | Purpose |
| --- | --- |
| `application/utils/ai_services.py` | OpenAI & Gemini client initialization |
| `application/utils/house_prompts.py` | LISTING_BOILERPLATE, seed context helpers |
| `application/utils/ai_utils.py` | JSON parsing, text sanitization |

---

## 📐 Configuration Quick Reference

### Required Environment Variables

```bash
export OPENAI_API_KEY=sk-...
export GEMINI_API_KEY=AIza...
export OPENAI_DEFAULT_MODEL=gpt-4o
export TEMPERATURE=0.2
export ARTWORK_ANALYSIS_MAX_OUTPUT_TOKENS=2000
export OPENAI_IMAGE_MAX_MB=20
export LAB_PROCESSED_DIR=./var/lab/processed
```

### Configurable Parameters

```python

# Model fallback sequence

OPENAI_MODEL_STACK = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]

# Sampling temperature (lower = more consistent)

TEMPERATURE = 0.2

# Max tokens for response

MAX_COMPLETION_TOKENS = 2000

# Image optimization

MAX_LONG_EDGE = 1024
MAX_IMAGE_SIZE_MB = 20
QUALITY_STEPS = [95, 90, 85]

# Timeouts and retries

API_TIMEOUT = 60.0
API_RETRIES = 1
```

---

## 🔍 How to Analyze & Improve

### 1. Review Prompts

```bash
cat application/analysis/prompts.py | grep -A 50 "HERITAGE_FIRST_SYSTEM_PROMPT"
```

## What to Look For

- Artist persona and voice

- Visual analysis requirements

- Geographic accuracy rules

- Heritage acknowledgement protocol

- Output format constraints

### 2. Study the OpenAI Service

```bash
cat application/analysis/openai/service.py | head -200
```

## Key Sections

- Image optimization loop (lines 200-250)

- Model selection logic (lines 450-500)

- Error classification (lines 50-100)

- Structured output handling (lines 600-650)

### 3. Examine Error Handling

```bash
grep -n "ERR_" application/analysis/openai/service.py
grep -n "ERR_" application/analysis/gemini/service.py
```

## Error Codes to Understand

- `ERR_AUTH` - API key issues

- `ERR_RATE_LIMIT` - Quota exceeded

- `ERR_TIMEOUT` - Network issues

- `ERR_MODEL` - Model unavailable

- `ERR_PARSE` - Invalid JSON response

### 4. Check Validation Rules

```bash
cat application/analysis/instructions/MASTER_ETSY_DESCRIPTION_ENGINE.md
```

## Key Constraints

- Title ≤140 chars (pipe-separated)

- Tags: exactly 13, ≤20 chars each

- SEO Filename: ≤70 chars (excluding .jpg)

- Materials: exactly 13 standardized items

---

## 📈 Performance Benchmarks

```text
| Operation | Time | Bottleneck |
─────────────────────────────────────────────
| Image Optimization | 0.5-2s | PIL processing |
| OpenAI API Call | 5-15s | Model inference |
| Gemini API Call | 8-20s | Model inference (slower) |
| JSON Validation | 0.1s | Fast (Pydantic) |
| Boilerplate Inject | 0.2s | String ops |
| Atomic File Write | 0.2-0.3s | Disk I/O |
─────────────────────────────────────────────
| TOTAL (OpenAI) | 6-18s | API latency |
| TOTAL (Gemini) | 9-22s | API latency |
```

### Optimization Tips

1. Use OpenAI by default (faster than Gemini)

1. Lower temperature (0.2) reduces variance in quality

1. Image optimization is critical (max 1024px)

1. Batch requests if possible (future enhancement)

---

## 🐛 Common Issues & Solutions

### Issue: "Rate limit exceeded"

```text
Error Code: ERR_RATE_LIMIT
Root Cause: OpenAI/Gemini API quota exhausted
Solution:
  1. Wait 60+ seconds
  2. Check API billing account
  3. Switch to alternative provider
  4. Implement retry backoff in config
```

### Issue: "Model gpt-4o not available"

```text
Error Code: ERR_MODEL
Root Cause: Model name typo or discontinuation
Solution:
  1. Verify OPENAI_DEFAULT_MODEL in config
  2. System auto-fallbacks to gpt-4, then 3.5-turbo
  3. Check OpenAI docs for latest models
```

### Issue: "Image too large after optimization"

```text
Error Code: ERR_UNKNOWN (in optimization loop)
Root Cause: Source image > 20MB after compression
Solution:
  1. Increase OPENAI_IMAGE_MAX_MB in config (not recommended)
  2. Upload smaller source images
  3. Image dimensions already reduced to 1024px
```

### Issue: "Temperature unsupported for model"

```text
Error Code: (auto-handled internally)
Root Cause: o1/o3 models don't support temperature parameter
Solution: Auto-retries with temperature=1.0 (built-in)
```

---

## 🚢 Deployment Checklist

- [ ] Extract archive and review documentation

- [ ] Read Artwork-Analysis-Report.md (all 14 sections)

- [ ] Set environment variables (API keys, config)

- [ ] Test with OpenAI first (faster, cheaper)

- [ ] Test with Gemini as fallback

- [ ] Monitor logs in `application/logging_config.py`

- [ ] Set up error alerting for `ERR_BALANCE`, `ERR_AUTH`

- [ ] Test retry logic with artificial rate limits

- [ ] Validate output quality against MASTER_ETSY_DESCRIPTION_ENGINE.md

- [ ] Deploy to production

- [ ] Collect feedback for prompt refinement

---

## 📚 Documentation Roadmap

### For Developers

1. **Quick Start:** This file (you're reading it!)

1. **Technical Deep-Dive:** Artwork-Analysis-Report.md (sections 2-10)

1. **Source Code:** application/analysis/, application/utils/

1. **Error Handling:** application/analysis/openai/service.py (lines 50-100)

### For Product Managers

1. **System Overview:** Artwork-Analysis-Report.md (section 1)

1. **Features & Benefits:** ANALYSIS-PACKAGE-README.md

1. **Performance Metrics:** Artwork-Analysis-Report.md (section 12)

1. **Roadmap:** Artwork-Analysis-Report.md (section 14)

### For Data Scientists

1. **Prompting Strategy:** Artwork-Analysis-Report.md (section 5)

1. **Prompt Templates:** application/analysis/prompts.py

1. **Output Schema:** application/analysis/openai/schema.py

1. **Example Output:** MASTER-ARTWORK-ANALYSIS-LISTING-DESCRIPTION-EXAMPLE.md

---

## 🎓 Key Learnings

### The "Art-First" Principle

Description should lead with visual emotion and aesthetics, THEN bring in technical specs. This maximizes collector appeal.

### Geographic Specificity

Never generalize specific places (e.g., "Bool Lagoon" → "Limestone Coast"). Specificity drives better SEO and authenticity.

### Heritage Respectfulness

Acknowledge Traditional Custodians appropriately, but NEVER claim ownership or invent sacred knowledge. Use phrases like "inspired by" or "honouring traditions."

### Museum-Grade Justification

The 14,400px × 300 DPI spec is a key differentiator. Lead with this technical value in paragraph 2 of description.

### Boilerplate is Essential

Every listing needs standard sections (LIMITED EDITION, TECHNICAL SPECS, HOW TO PRINT, ABOUT THE ARTIST, ACKNOWLEDGEMENT). This builds trust and professionalism.

---

## 🔗 File Reference Map

```text
START HERE:
  ├─ Artwork-Analysis-Report.md        [14 sections]
  └─ ANALYSIS-PACKAGE-README.md        [This file]

UNDERSTAND THE FLOW:
  ├─ application/analysis/api/routes.py        [REST API]
  ├─ application/analysis/openai/service.py    [Main logic]
  └─ application/analysis/gemini/service.py    [Alternative]

CUSTOMIZE BEHAVIOR:
  ├─ application/analysis/prompts.py           [System prompts]
  ├─ application/analysis/instructions/        [Output rules]
  └─ application/config.py                     [Settings]

INTEGRATE:
  ├─ application/utils/ai_services.py          [Clients]
  ├─ application/utils/ai_utils.py             [Helpers]
  └─ application/upload/services/              [Storage]
```

---

## 🤝 Next Steps

1. **Extract Archive:** `tar -xzf artlomo-analysis-complete-package.tar.gz`

1. **Read Documentation:** Start with ANALYSIS-PACKAGE-README.md

1. **Deep Dive:** Review Artwork-Analysis-Report.md (sections 2-5)

1. **Test Locally:** Use provided source code with sample artwork

1. **Customize:** Adapt prompts for your artist's unique voice

1. **Monitor:** Track API costs and response quality

1. **Iterate:** Collect feedback and refine outputs (section 14)

---

**Package Complete & Ready for Analysis** ✅
**Generated:** March 1, 2026
**Archive Size:** 72 KB (compressed)
**Total Documentation:** 10,000+ words
**Code Lines:** 3,000+ (analysis + utilities)
