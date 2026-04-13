# ArtLomo Integrity Audit Report
Date stamp: 29 March 2026, 12:00 (local)
Repository: /srv/artlomo
Audit mode: Evidence-first, report-first (no opportunistic refactor)

## Scope and guardrails
- Full integrity and code audit executed against /srv/artlomo.
- Operator correction applied: ArtLomo does not run an active production mockup generation pipeline; mockup-related code in this repository is treated as legacy, decommission, admin, or reference surface.
- Protected pre-existing unstaged files were not modified in this pass:
  - application/artwork/routes/artwork_routes.py
  - application/common/ui/static/js/video_cinematic.js
  - application/common/ui/templates/video_workspace.html
  - application/video/services/video_service.py
  - application/video_worker/render.js
- /srv/dreamartmachine was not touched.
- No code files were modified in this phase; this report captures findings and phase-two touchpoints.

## Audit execution evidence

### Environment/tooling
- Python environment used for test execution: /srv/artlomo/.venv/bin/python
- ripgrep availability check: not installed on host (fallback to grep)

### Integrity checks run
1. Full test suite
   - Command: /srv/artlomo/.venv/bin/python -m pytest -q --maxfail=30
   - Result: 7 failed, 170 passed, 1 skipped in 45.06s
2. Targeted analysis tests
   - Command: /srv/artlomo/.venv/bin/python -m pytest -q tests/test_analysis_queue.py tests/test_analysis_service.py tests/test_analysis_response_contract.py --maxfail=20
   - Result: 2 failed, 34 passed in 2.33s
3. Targeted route/provider/coordinate tests
   - Command: /srv/artlomo/.venv/bin/python -m pytest -q tests/test_decommission_routes.py tests/test_artwork_review_provider.py tests/test_composite_coordinate_service.py --maxfail=20
   - Result: 34 passed in 4.00s
4. Python compile integrity (runtime scope)
   - Scope: application/ excluding archives/vendor-like directories
   - Result: compile_errors=0
5. Broad compile scan (unfiltered) produced non-runtime noise
   - Errors found under extract snapshots and node_modules Python2 stubs, not active runtime modules:
     - application/tools/app-stacks/stacks/mockup-handoff/.../extracts/*.py
     - application/video_worker/node_modules/gl/angle/.../*.py

## Confirmed issues (reproducible)

### 1) Analysis Stage 2 contract drift under single-pass mode
Severity: High
Evidence:
- tests/test_analysis_queue.py (failing tests):
  - test_worker_stage2_failure_marks_failed_without_moving_folder
  - test_provider_selection_persists_into_stage2_execution
- Runtime behavior logged from application/analysis/worker/analysis_worker.py around stage2 flow:
  - single-pass default enabled via ANALYSIS_SINGLE_PASS default True
  - stage2_provider_result reuses stage1 payload (no second provider call)
  - log line: "Stage 2 using single-pass provider payload (no second AI call)"
- Consequence:
  - Expected stage2 failure path does not trigger in test scenario that assumes a second call with invalid stage2 payload.
  - Provider call count expectation (2) no longer matches execution (1).
Impact:
- Test contract and runtime contract are out of sync.
- Potentially masks stage2-specific degradation if stage1 payload is reused too aggressively.
Primary files:
- application/analysis/worker/analysis_worker.py (around 619-644)
- tests/test_analysis_queue.py (around 329 and 479 assertions)

### 2) Legacy/mockup-reference contract drift in Gemini service prompt handling
Severity: Medium (reference-surface)
Evidence:
- Failing tests in tests/test_mockup_base_generation_stage2a.py:
  - test_prompt_service_output_compatible_with_gemini_service
  - test_stage2a_uses_cyan_reference_guide_when_available
- Runtime code prepends hard-edge/system guidance before API call:
  - HARD_EDGE_PROMPT_PREFIX constant and _build_generation_prompt / _build_inpaint_prompt
  - generate_image path calls _call_gemini_generate_images / _call_gemini_edit_image using transformed prompt
- Consequence:
  - Tests expecting call["prompt"] == original prompt fail.
Impact:
- Prompt contract changed from pass-through to wrapped/enriched prompt.
- Any downstream tooling expecting raw prompt will diverge.
- Context note: this is not treated as an active ArtLomo production pipeline defect; it is a reference-surface contract issue.
Primary files:
- application/mockups/services/gemini_service.py (HARD_EDGE_PROMPT_PREFIX around 165; builders around 901+)
- tests/test_mockup_base_generation_stage2a.py (assertions around 456 and 595)

### 3) Legacy/mockup-reference config contract drift (typed config vs dict)
Severity: Medium (reference-surface)
Evidence:
- Failing tests in tests/test_mockup_base_generation_stage2a.py:
  - test_stage2a_uses_generation_aspect_override_for_canvas
  - test_stage2a_maps_unsupported_aspect_ratio_to_nearest_supported
- Runtime call path currently passes config as plain dict to generate_images:
  - _invoke_generate_images sets api_kwargs["config"] = config_kwargs where config_kwargs is dict
- Tests expect config object type (_FakeGenerateImagesConfig / _FakeEditImageConfig).
Impact:
- Interface drift with tests and potentially with SDK assumptions when monkeypatched typed wrappers are expected.
- Context note: this is scoped to mockup reference modules, not active ArtLomo production workflow.
Primary files:
- application/mockups/services/gemini_service.py (_invoke_generate_images around 612+)
- tests/test_mockup_base_generation_stage2a.py (assert isinstance(config, _FakeGenerateImagesConfig))

### 4) Legacy/mockup-reference backward-compatibility break from thought_signature parameter
Severity: Medium (reference-surface)
Evidence:
- Failing test in tests/test_mockup_base_generation_stage2a.py:
  - test_stage2a_contract_all_categories_and_aspects
- Runtime now calls:
  - _call_gemini_generate_images(..., thought_signature=...)
- Test monkeypatch lambda signature only accepts (self, prompt, aspect_ratio), causing TypeError.
Impact:
- Existing monkeypatch/test doubles and older internal call shims break unless signature updated or kwargs tolerated.
Primary files:
- application/mockups/services/gemini_service.py (generate_image around 323)
- tests/test_mockup_base_generation_stage2a.py (lambda monkeypatch around 808+)

### 5) Legacy/mockup-reference forced generation aspect ratio defaults to 1:1
Severity: Medium (reference-surface)
Evidence:
- gemini_service.py sets FORCE_GENERATION_ASPECT_RATIO default to 1:1
- Failing test evidence shows aspect_ratio in API config as 1:1 even for 2x3 mapping case.
Impact:
- Can invalidate expected "nearest supported aspect" mapping behavior for non-square requests.
- Produces hidden policy override unless explicitly documented and tested as intentional.
Primary files:
- application/mockups/services/gemini_service.py (FORCE_GENERATION_ASPECT_RATIO around 156)
- tests/test_mockup_base_generation_stage2a.py (3:4 mapping expectation around 548)

## Suspected issues (needs confirmation)

### A) High broad-exception density may mask operational errors
Evidence:
- Extensive except Exception usage across active runtime modules, especially:
  - application/analysis/openai/service.py
  - application/analysis/gemini/service.py
  - application/mockups/admin/services.py
  - application/mockups/routes/mockup_routes.py
Risk:
- Differentiation between expected degraded paths and real defects is hard.
- Silent or downgraded failures may propagate inconsistent state.

### B) Silent-read helpers can suppress data quality defects
Evidence:
- application/analysis/prompts.py:_read_text_silent returns "" on any exception.
- application/mockups/routes/mockup_routes.py:_read_json_silent returns {} on any exception.
Risk:
- Missing/corrupt prompt/config/metadata files may be interpreted as valid empty state.
- Operational alerts can be missed unless downstream validators are strict.

### C) Multiple fallback chains increase non-determinism in stage logic
Evidence:
- Metadata/QC fallback to legacy files in analysis/mockups routes.
- Gemini generation/edit model fallback stacks.
- Coordinate fallback generation paths in tasks_mockup_generator.
Risk:
- Runtime behavior can differ significantly by environment and available assets.
- Harder to guarantee deterministic compositing truth unless fallback boundaries are explicit and auditable.

## Weak points and architecture concerns

1. Contract drift between implementation and tests in core pipelines
- Analysis Stage 2 moved to single-pass semantics, while tests still encode dual-call expectations.
- Mockup Stage 2A prompt/config call shape changed without fully aligned contract tests.

2. Fallback-rich architecture without strict "decision ledger" in all paths
- Some paths log fallback usage well (example: coordinates_source), others rely on generic error catches.
- Stronger state transition observability is needed for production-grade pipeline guarantees.

3. Legacy surface area remains large
- Legacy guide dirs, legacy metadata/qc fallbacks, and decommissioned route stubs are still present by design.
- This is manageable but increases migration complexity and accidental coupling risk.

4. Determinism boundary is present but not uniformly enforced
- Positive: coordinate/composite workflows are largely local and tested in targeted suite.
- Risk: generation fallbacks can still alter scene-generation assumptions in ways that impact downstream extraction robustness.

## Dead paths / decommission posture

Confirmed healthy:
- Decommission regression tests pass (tests/test_decommission_routes.py).
- Decommissioned route intent is documented in:
  - application/mockups/admin/routes/generator_routes.py
  - application/mockups/admin/routes/mockup_admin_routes.py
- Operator context aligns with code posture: ArtLomo mockup generation paths are decommissioned/non-primary and should not be treated as active production runtime.

Observed dead-or-non-runtime noise:
- Compile failures in application/tools/.../extracts and application/video_worker/node_modules/... are not active runtime modules.
- These should be excluded from integrity compile gates to reduce false positives.

## Recommended fixes (phase-two, prioritized)

Priority 0 (stability blockers)
1. Reconcile Analysis Stage 2 contract:
   - Decide canonical behavior: strict single-pass or dual-call stage2.
   - Align tests and runtime together.
   - If single-pass stays: rewrite failing tests to validate stage2 extraction/validation from single payload only.
2. (Reference-only) Reconcile Gemini prompt/config API contract:
   - Decide whether service should pass raw prompt or enriched prompt to low-level call.
   - Decide whether config should be typed object or dict in test harness and runtime.
   - Update tests + implementation consistently.
3. (Reference-only) Add compatibility shim for _call_gemini_generate_images signature:
   - Accept extra kwargs safely in test doubles/adapter layer.

Priority 1 (determinism and observability)
4. Introduce explicit fallback decision records in job metadata for all critical fallbacks.
5. Tighten silent helper behavior:
   - Keep non-throwing behavior where needed, but log structured warnings with context IDs.

Priority 2 (migration hardening)
6. Isolate legacy file fallbacks behind explicit feature flags.
7. Restrict compile/test gates to runtime code roots, excluding archive/vendor snapshots by default.

## Files to touch later (phase two)

Core fixes:
- application/analysis/worker/analysis_worker.py
- tests/test_analysis_queue.py
- application/mockups/services/gemini_service.py
- tests/test_mockup_base_generation_stage2a.py

Fallback and observability hardening:
- application/analysis/prompts.py
- application/mockups/routes/mockup_routes.py
- application/mockups/tasks_mockup_generator.py
- application/analysis/openai/service.py
- application/analysis/gemini/service.py

De-scope/noise control (optional but recommended):
- application/tools/app-stacks/... (exclude from runtime compile gates)
- application/video_worker/node_modules/... (exclude from Python compile gates)

## Strategic context alignment

This audit aligns with the strategic direction:
- DreamArtMachine should become the cleaner mockup-base generation and preparation engine.
- ArtLomo should remain the richer reference system for proven workflows and decommission patterns, not an active mockup generation runtime.
- Mockup workflow should be operated as a strict staged pipeline.
- Gemini should be used for scene generation/editing, not coordinate truth or compositing truth.
- Coordinate extraction and final compositing should remain deterministic and local wherever possible.
- Production-ready mockup bases should become reusable managed assets with strong logging and explicit state transitions.

## Protected-file impact check
- No failing integrity evidence in this pass required edits to protected pre-existing unstaged files.
- No edits were made to protected files.

## Audit conclusion
- Runtime Python syntax integrity in live application scope: PASS.
- Core active regression surface: concentrated in Analysis Stage 2 contract.
- Additional reference-surface regressions: legacy/mockup Stage 2A Gemini call-contract drift.
- Route decommission integrity and coordinate/provider targeted tests: PASS.
- Recommended next action: execute phase-two contract reconciliation in focused PR(s), then rerun full suite.
