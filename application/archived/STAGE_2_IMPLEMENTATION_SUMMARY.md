# Stage 2 Implementation Summary

## Scope

Implemented **real AI execution for Stage 1 image analysis only**.

Not implemented in this stage:

- Stage 2 Etsy optimization pipeline
- Stage 3 marketing pack pipeline

All queue, routing, and failure constraints from Stage 1A remain intact.

---

## What Changed

### 1) Real Stage 1 execution in worker

Updated:

- `application/analysis/worker/analysis_worker.py`

Key behavior:

- Replaced simulation with real provider calls:
  - `run_openai_analysis_for_slug(...)`
  - `run_gemini_analysis_for_slug(...)`
- Builds Stage 1 structured output with required keys:
  - `subject`
  - `palette` (list)
  - `lighting`
  - `location_guess`
  - `style`
  - `keywords` (list)
- Validates Stage 1 payload strictly.
- Writes slug-prefixed outputs:
  - `{slug}-analysis-stage1.json`
  - `{slug}-ai-packet.json`
- Registers new files in manifest:
  - `files.analysis_stage1`
  - `files.ai_packet`
- Updates `manifest.analysis` progress for Stage 1 only:
  - running (5/24)
  - success (33)
  - failed (33)
- Job completion semantics for this stage:
  - `AnalysisJob.status = DONE` on Stage 1 success
  - `AnalysisJob.stage = stage1_image`
  - `AnalysisJob.progress = 33`

### 2) Failure contract handling

Updated:

- `application/analysis/worker/analysis_worker.py`

Added handling for structured failure payloads:

- `STATUS: FAILED`
- `REASON`
- `MESSAGE`

Also enforced:

- invalid/missing JSON shape → FAILED
- missing required Stage 1 fields → FAILED
- invalid list/string fields → FAILED

Failure updates:

- `AnalysisJob.status = FAILED`
- `AnalysisJob.reason` and `AnalysisJob.error_message` set
- `manifest.analysis.status = failed`
- `manifest.analysis.reason/message` set

No folder stage movement occurs on failure.

### 3) Status endpoint now reflects manifest analysis state

Updated:

- `application/analysis/api/routes.py`

`GET /api/analysis/status/<slug>` now:

- reads `manifest.analysis` first (canonical queue/worker stage state)
- falls back to legacy listing status only when manifest analysis is missing

### 4) Queued-state manifest updates at enqueue time

Updated:

- `application/analysis/api/routes.py`

Both enqueue endpoints now write queued state to manifest:

- `POST /api/analysis/openai/<slug>`
- `POST /api/analysis/gemini/<slug>`

Manifest fields set on enqueue:

- `analysis.status = queued`
- `analysis.stage = stage1_image`
- `analysis.progress = 0`
- `analysis.provider`
- `analysis.job_id`
- `analysis.queued_at`
- `analysis.updated_at`

---

## Source-of-Truth Compliance

- `application/lab/index/artworks.json` remains global routing truth (worker resolves via index first).
- `{slug}-assets.json` remains canonical asset registry.
- New files are slug-prefixed and registered in `manifest.files`.
- No folder move from processed/unprocessed occurs on failure.

---

## Stage 1 Output Contract

Written file: `{slug}-analysis-stage1.json`

Expected shape:

```json
{
  "subject": "...",
  "palette": ["..."],
  "lighting": "...",
  "location_guess": "...",
  "style": "...",
  "keywords": ["..."]
}
```

Optional packet (implemented): `{slug}-ai-packet.json`

- includes stage blocks under `stages.stage1_image`

---

## Validation Rules (Stage 1)

Required keys:

- `subject`, `lighting`, `location_guess`, `style` → non-empty strings
- `palette`, `keywords` → non-empty lists with non-empty strings

Reasonable list limits:

- `palette`: 1..16
- `keywords`: 1..30

Failure marker detection rejects payloads containing:

- `STATUS: FAILED`
- `STATUS=FAILED`
- `ANALYSIS_FAILED`

---

## Tests Updated

Updated:

- `tests/test_analysis_queue.py`

Coverage now includes:

- enqueue → worker executes Stage 1 with provider mocked
- writes `{slug}-analysis-stage1.json`
- writes `{slug}-ai-packet.json`
- registers files in manifest
- marks job DONE at stage1_image/progress=33
- failure path sets FAILED + reason/message
- failure path does not move folders

Latest run:

```bash
source .venv/bin/activate && pytest -q tests/test_analysis_queue.py
```

Result:

- `7 passed`

---

## How To Run

### 1) Start app

```bash
cd /srv/artlomo
source .venv/bin/activate
python wsgi.py
```

### 2) Start worker

```bash
cd /srv/artlomo
source .venv/bin/activate
python -m application.analysis.worker.analysis_worker
```

### 3) Enqueue Stage 1 job

- Use UI: OpenAI/Gemini analysis buttons
- Or API:

```bash
curl -X POST http://localhost:8013/api/analysis/openai/<slug> \
  -H "X-CSRF-Token: <token>"
```

### 4) Verify outputs

In processed artwork folder:

- `{slug}-analysis-stage1.json` exists
- `{slug}-ai-packet.json` exists
- `{slug}-assets.json` has:
  - `files.analysis_stage1`
  - `files.ai_packet`
  - `analysis.status/stage/progress/provider/job_id/timestamps`

### 5) Verify status endpoint

```bash
curl http://localhost:8013/api/analysis/status/<slug>
```

Should reflect `manifest.analysis` values directly.

---

## Notes

- Stage 2 currently finalizes after Stage 1 success (`job DONE`, `progress=33`) by design.
- Stages 2 and 3 remain intentionally unimplemented in this phase.
