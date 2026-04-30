# Copilot Engineering Prompt: ArtLomo Etsy Analysis + Failure Handling Pipeline

Use this prompt in VS Code Copilot Agent Mode.

```text
Mission: Etsy Analysis Failsafe Pipeline

Project root:
/Users/robin/ART/new-art-machine/new-art-machine

Context:
ArtLomo / Dream Art Machine generates Etsy-ready listing text from artwork metadata, AI image analysis, and technical file details. The current source prompts and guides contained duplicated/corrupted text, so the implementation must rely on the cleaned master standard only.

Goal:
Implement a deterministic Etsy listing description generation pipeline with robust analysis failure handling, integrated with artwork lifecycle stages: unprocessed, processed, locked.

Evidence:
Use this cleaned reference as the source of truth:
application/analysis/instructions/MASTER-ETSY-LISTING-DESCRIPTION-STANDARD-CLEAN.md

Inspect first:
- application/artwork/services/processing_service.py
- application/artwork/services/index_service.py
- application/artwork/routes/artwork_routes.py
- application/upload/routes/upload_routes.py
- application/analysis/api/routes.py
- application/mockups/artwork_index.py
- application/lab/index/artworks.json
- existing tests for artwork processing, analysis, upload, index, and mockups

Constraints:
- Keep changes minimal and deterministic.
- No inline CSS or JS.
- Do not introduce HTML into Etsy listing descriptions.
- Preserve existing stage-aware index behaviour.
- Preserve backward compatibility with existing manifests.
- Do not overwrite locked artwork assets.
- Do not leave files or index records in a partially moved state.
- Fail closed, not silently.
- Stop after the requested scope is implemented and tested.

Required output:
1. Exact files created or modified.
2. Patch summary grouped by backend, frontend, tests, and docs.
3. Validation commands run.
4. Test results.
5. Migration or rollback notes.
6. Known risks or follow-up work.

Required implementation:

1. Deterministic generator
Create or refactor a generator module that accepts:
- artwork metadata: sku, slug, title, location/context, category
- AI image analysis result
- technical file details: dimensions, file type, long edge
- optional artist/shop configuration

Return exactly:
STATUS:
TITLE:
DESCRIPTION:
SEO_KEYWORDS:
ARTWORK_DETAILS:

2. Output parser and validator
Add a parser/validator layer that:
- validates success output shape
- detects malformed or incomplete responses
- detects missing digital-download disclosure
- detects missing no-physical-shipping disclosure
- detects unsupported physical-product wording
- normalises failures to:
  STATUS: FAILED
  REASON: <message>
- accepts the legacy marker:
  ANALYSIS_FAILED
  REASON: <message>

3. Failure detection and recovery flow
On failure, backend must:
- mark analysis_status = failed
- move artwork lifecycle back to unprocessed if safe
- ensure files are moved from processed artwork path to unprocessed artwork path only when required
- update artworks index using the existing index service
- log failure in logs/artwork-analysis-errors.log
- expose UI state for FAILED ANALYSIS badge
- allow retry to requeue analysis safely

4. Atomic state consistency
Use a transactional pattern:
a) validate source and destination
b) prepare target paths
c) move or copy files safely
d) update index
e) persist analysis_status
f) emit/log event

If any step fails:
- rollback where possible
- log compensating action
- never delete the original source asset unless replacement is confirmed

5. UI requirements
- Add FAILED ANALYSIS badge where artwork status is shown.
- Add retry action that requeues analysis.
- Retry must clear stale transient error state.
- Retry must write a new attempt timestamp.
- Keep styling in static CSS only.

6. Logging
Write structured lines to logs/artwork-analysis-errors.log with:
timestamp, sku, slug, stage_before, stage_after, reason, exception_type

7. Tests
Implement or extend tests for:
- valid SUCCESS parsing
- malformed AI response becomes FAILED
- timeout/refusal becomes FAILED
- missing digital-download disclosure becomes FAILED
- missing no-physical-shipping disclosure becomes FAILED
- processed-to-unprocessed recovery on failure
- index path update correctness
- retry returns artwork to the analysis queue
- idempotency when failure handling is triggered twice
- locked artwork is never modified by failure recovery

Validation commands:
Run the smallest relevant test set first, then the wider affected suite. Include exact commands in the final report.

Definition of done:
- Generator returns the exact required fields.
- Failure outputs are normalised and logged.
- UI clearly shows failed analysis and retry.
- Retry is safe and idempotent.
- Tests pass.
- Final report includes files changed, commands run, results, and any follow-up risks.
```
