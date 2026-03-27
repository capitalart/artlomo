# Stage 3 Implementation Summary

## Scope

Implemented **real Stage 2 Etsy listing generation** in the queued AI worker pipeline.

Context status now:

- Stage 1A: queue + worker + job APIs + header indicator ✅
- Stage 2: real Stage 1 image analysis ✅
- Stage 3 (this phase): real Stage 2 Etsy generation ✅
- Stage 4 (future): Stage 3 marketing pack ⏳

No UI button endpoint contracts were changed.

---

## Pipeline Behavior (Current)

Worker flow per job:

1. Stage 1 image analysis (`stage1_image`, progress up to 33)
2. Stage 2 Etsy listing generation (`stage2_etsy`, progress up to 66)

Provider persistence:

- Provider selected at enqueue (`openai` or `gemini`) is stored on `AnalysisJob.provider`
- Same provider is used for Stage 1 and Stage 2 execution within the job
- No automatic provider switching unless a new job is created

---

## Files Updated

### Worker orchestration

- `application/analysis/worker/analysis_worker.py`

Key additions:

- Stage 2 prerequisite check:
  - Requires `{slug}-analysis-stage1.json`
  - Missing/invalid Stage 1 => `ERR_MISSING_STAGE1` / `ERR_STAGE1_INVALID`
- Stage 2 output extraction and generation:
  - Produces structured Etsy payload:
  - `title`
  - `description`
  - `seo_keywords`
  - `tags` (optional)
  - `sizes` (optional guidance)
  - `disclaimers`
- Stage 2 validation rules:
  - Reject HTML tags (`<...>`)
  - Require digital-download clarity
  - Require print quality statement (14400px / up to 48")
  - Require personal-use/copyright language
  - Flag long unbroken lines (heuristic)
- Review outcomes:
  - `failed` for unusable output
  - `needs_review` for minor quality issues (preferred)
- Failure contract support:
  - Structured model failures handled:
  - `STATUS: FAILED`
  - `REASON`
  - `MESSAGE`
  - malformed/missing critical fields treated as failure

### Status endpoint semantics

- `application/analysis/api/routes.py`

Changes:

- `/api/analysis/status/<slug>` now treats `needs_review` as done
- returns `status: warning` when manifest analysis is `needs_review`

### Review UI exposure of Etsy output

- `application/artwork/routes/artwork_routes.py`
- `application/common/ui/templates/analysis_workspace.html`

Changes:

- Loads `{slug}-copy-etsy.json` into review rendering context (`copy_etsy`)
- Adds Etsy Output panel (read-only) showing:
  - generated title
  - generated description
  - SEO keywords
  - disclaimers

### Running-stage UI feedback

- `application/common/ui/static/js/analysis-loading.js`

Changes:

- Overlay text now shows pipeline stage labels while polling:
  - `RUNNING — Stage 1/3`
  - `RUNNING — Stage 2/3`
  - `RUNNING — Stage 3/3` (reserved for next phase)

---

## Canonical File + Manifest Compliance

### Stage 2 output file

Writes:

- `{slug}-copy-etsy.json`

### Manifest registration

Updates `{slug}-assets.json`:

- `files.copy_etsy = "{slug}-copy-etsy.json"`

### Analysis status block

Updates `manifest.analysis` during Stage 2:

- `stage = stage2_etsy`
- progress in `34..66` (implemented: 40, 58, 66)
| - `status = running | success | failed | needs_review` |
- provider, job_id, attempts, timestamps, reason/message

No folder moves occur on failure.

---

## Job Row Behavior

On Stage 2 success:

- `AnalysisJob.status = DONE`
- `AnalysisJob.stage = stage2_etsy`
- `AnalysisJob.progress = 66`

On Stage 2 needs-review:

- Job remains `DONE` with
  - `reason = WARN_STAGE2_REVIEW`
  - `error_message` carrying review notes
- Manifest status set to `needs_review`

On failure:

- `AnalysisJob.status = FAILED`
- reason/message populated
- manifest status set to `failed`

---

## Tests Added/Updated

Updated:

- `tests/test_analysis_queue.py`

Coverage now includes:

- Stage 2 success creates `{slug}-copy-etsy.json`
- Manifest `files.copy_etsy` registration
- Stage 2 failure sets `failed` with reason/message (no folder moves)
- Stage 2 minor issues set `needs_review`
- Provider selection persists into Stage 2 execution (gemini job uses gemini calls only)

Latest verification:

```bash
source .venv/bin/activate && pytest -q tests/test_analysis_queue.py
```

Result:

- `9 passed`

---

## How to Verify Manually

1) Start app + worker

```bash
cd /srv/artlomo
source .venv/bin/activate
python wsgi.py
```

```bash
cd /srv/artlomo
source .venv/bin/activate
python -m application.analysis.worker.analysis_worker
```

1) Trigger from unprocessed gallery using existing buttons:

- `OpenAI Analysis`
- `Gemini Analysis`

1) Observe running overlay/status:

- Stage indicator shows `RUNNING — Stage 1/3` then `RUNNING — Stage 2/3`

1) Check outputs in processed artwork folder:

- `{slug}-analysis-stage1.json`
- `{slug}-copy-etsy.json`
- `{slug}-ai-packet.json`

1) Check manifest:

- `files.analysis_stage1`
- `files.copy_etsy`
- `files.ai_packet`
- `analysis.stage = stage2_etsy`
- `analysis.progress = 66` (or failed/needs_review state)

1) Check status endpoint:

```bash
curl http://localhost:8013/api/analysis/status/<slug>
```

- reflects manifest analysis state
- `needs_review` returns warning status

---

## Notes / Next Stage

- Stage 3 marketing generation is intentionally deferred.
- Current pipeline is now production-ready through Etsy generation with canonical manifest registration, deterministic validation, and queue-safe failure behavior.
