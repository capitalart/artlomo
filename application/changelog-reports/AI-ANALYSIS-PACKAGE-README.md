# AI Analysis Workflow Package

**Package:** `ai-analysis-workflow.tar.gz`
**Created:** March 3, 2026
**Size:** 145 KB
**Files Included:** 77 items

## Overview

This package contains all files related to AI-powered artwork analysis (OpenAI and Gemini) in ArtLomo, including prompts, instructions, services, routes, UI components, and configuration.

---

## Package Contents

### 1. **Analysis Core** (`application/analysis/`)

#### OpenAI Service

- `openai/service.py` - Main OpenAI API integration and analysis execution

- `openai/schema.py` - Structured output schema for OpenAI responses

#### Gemini Service

- `gemini/service.py` - Main Gemini API integration and analysis execution

- `gemini/schema.py` - Structured output schema for Gemini responses

#### Instructions & Prompts

- `prompts.py` - System prompts and prompt generation logic

- `instructions/master-analysis-prompt.md` - Master analysis prompt template

- `instructions/MASTER_ETSY_DESCRIPTION_ENGINE.md` - Etsy-specific description generation rules

- `instructions/MASTER-ARTWORK-ANALYSIS-LISTING-DESCRIPTION-EXAMPLE.md` - Example analysis outputs

#### Manual Analysis Workflow

- `manual/` - Complete manual analysis workflow

  - `manual_service.py` - Manual analysis submission and processing

  - `manual_routes.py` - Routes for manual analysis endpoints

  - `manual_workspace.css` - UI styling

  - `forms.py` - Form definitions for manual input

#### Services

- `services/preset_service.py` - Analysis preset management (temperature, tokens, models)

#### API & Routes

- `api/routes.py` - RESTful API endpoints for analysis operations

- `routes.py` - Main analysis workflow routes

- `ui/templates/etsy_rules_reference.html` - Etsy rule reference UI

---

### 2. **Artwork Routes** (`application/artwork/routes/`)

- `artwork_routes.py` - Contains analysis-triggering routes:

  - `openai_analysis()` - Route to start OpenAI analysis

  - `gemini_analysis()` - Route to start Gemini analysis

  - Review endpoints for analysis results

  - Re-analysis endpoints

---

### 3. **Configuration & Utilities**

#### Configuration

- `config.py` - Contains all analysis-related configuration:

  - OpenAI API settings

  - Gemini API settings

  - Model selections

  - Temperature and token limits

  - Retry policies

#### Utilities

- `utils/` - Shared utilities used by analysis:

  - `auth_decorators.py` - Authorization checks

  - `template_engine.py` - Template rendering

  - `image_urls.py` - Image URL handling

  - `house_style.py` - Brand-specific styling rules

  - `env.py` - Environment variable management

---

### 4. **Documentation**

- `application/workflows/Analysis-Workflow-Report.md` - Complete analysis workflow documentation

- `application/docs/MASTER_WORKFLOWS_INDEX.md` - Workflow index with analysis section

---

## Analysis Workflow Summary

### How It Works

1. **Trigger Analysis**

  - User clicks "OpenAI Analysis" or "Gemini Analysis" button on unprocessed artwork

  - Frontend calls `artwork.openai_analysis(slug)` or `artwork.gemini_analysis(slug)`

1. **Prepare Request**

  - `openai/service.py` or `gemini/service.py` reads artwork image

  - `prompts.py` generates system + user prompts

  - Instructions from `instructions/` folder guide analysis

1. **Send to AI**

  - OpenAI/Gemini API receives:

  - System prompt (brand voice, output format)

  - User prompt (analyze this specific artwork)

  - High-res artwork image (2048px)

  - Structured output schema (JSON format)

1. **Process Response**

  - Parse structured output from AI

  - Validate against schema (`openai/schema.py` or `gemini/schema.py`)

  - Save analysis to database

  - Move artwork from unprocessed → processed

1. **Review & Export**

  - User reviews analysis results

  - Can re-analyze if needed

  - Can export as Etsy listing description

---

## Key Files to Understand

### Prompts & Instructions

- **`prompts.py`** - Start here to see how prompts are constructed

- **`master-analysis-prompt.md`** - Core instructions sent to all AI models

- **`MASTER_ETSY_DESCRIPTION_ENGINE.md`** - Etsy-specific formatting rules

Services

- **`openai/service.py`** (1274 lines) - Full OpenAI integration with retries, fallbacks, validation

- **`gemini/service.py`** - Similar Gemini implementation

- **`manual/manual_service.py`** - Manual analysis input handling

### Routes

- **`artwork_routes.py`** - Entry points for triggering analysis

- **`api/routes.py`** - JSON API endpoints for analysis polling/status

---

## Configuration Highlights

From `config.py`:

- Multiple OpenAI models supported (gpt-4o, gpt-4-turbo, etc.)

- Multiple Gemini models supported

- Configurable temperature, max tokens, timeout

- Fallback model stack (tries preferred model → fallback → gpt-4o)

- Retry logic with exponential backoff

---

## Database Integration

Analysis results stored in SQLite:

- `Artwork` table: status, analysis_source, metadata

- `AnalysisJob` table: job tracking for async operations

- Double-write pattern: Updates both JSON files and database

---

## Error Handling

- Detailed error logging in `/srv/artlomo/logs/`

- Graceful fallback to next model if one fails

- User-friendly error messages in UI

- Full request/response logs for debugging

---

## Extending the Analysis

### To Add a New AI Provider (e.g., Claude)

1. Create `application/analysis/claude/`

1. Implement `service.py` with same interface as `openai/service.py`

1. Create `schema.py` for structured output

1. Update `prompts.py` to handle Claude-specific prompting

1. Add route in `artwork_routes.py` → `def claude_analysis(slug)`

1. Add config in `config.py`

### To Modify Analysis Output

1. Edit `instructions/master-analysis-prompt.md`

1. Update schema definitions in `openai/schema.py` and `gemini/schema.py`

1. Update `config.py` if adding new fields

---

## Important Constants

- **Artwork image size:** 2048px long edge (set in `config.py`)

- **Default temperature:** 0.0 (deterministic)

- **Max tokens:** 4000 (configurable per model)

- **Timeout:** 60 seconds (configurable)

- **Retries:** 3 attempts per model

---

## Security Considerations

- API keys stored in environment variables (not in code)

- CSRF tokens required on all analysis endpoints

- All analysis requests logged with user ID

- Input validation on all uploaded images

- Rate limiting on API calls

---

## Usage

Extract the package:

```bash
tar -xzf ai-analysis-workflow.tar.gz
```

This will create:

```text
application/
├── analysis/              # Complete analysis workflow
├── artwork/routes/        # Analysis route entry points
├── config.py              # Configuration
├── utils/                 # Shared utilities
└── docs/                  # Documentation
```

---

## Questions?

Refer to:

- `application/workflows/Analysis-Workflow-Report.md` - Complete workflow details

- `application/docs/ARCHITECTURE_INDEX.md` - System architecture

- Individual service files for implementation details
