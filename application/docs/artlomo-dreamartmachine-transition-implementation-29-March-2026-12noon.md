# ArtLomo -> DreamArtMachine Transition Implementation Blueprint
Date stamp: 29 March 2026, 12:00 (local)
Prepared from: /srv/artlomo reference audit
Target: /srv/dreamartmachine (planning only; no code changes in this pass)

## Purpose
Use ArtLomo as reference architecture (not copy) to implement missing workflows into DreamArtMachine while preserving DreamArtMachine as a cleaner, production-focused mockup engine.

## Strategic position
- DreamArtMachine = primary mockup-base generation + preparation engine.
- ArtLomo = richer reference system for proven workflows and operational patterns; it is not the active mockup generation runtime.
- Pipeline doctrine:
  - Gemini handles scene generation/editing only.
  - Coordinate truth and compositing truth remain deterministic and local.
  - Mockup bases are managed assets with auditable state transitions.

## Non-negotiable architecture principles
1. Strict staged pipeline
- Every stage must have explicit inputs, outputs, status, timestamps, and reason codes.
- No hidden jumps between stages.

2. Deterministic coordinate/compositing boundary
- AI can suggest or generate scene pixels.
- Final placement coordinates and compositing decisions come from local deterministic services.

3. Explicit fallback policy
- Fallbacks allowed only when logged and state-tagged.
- No silent fallback for critical production artifacts.

4. Managed-asset lifecycle
- "Processed" means promotion into managed library state (not just file move).
- Promotion must write catalog metadata, lineage, and verification data.

## Target operating model for DreamArtMachine

### Stage map (recommended)
- Stage 0: IntakeQueued
- Stage 1: SceneGenerationRequested (Gemini generate/edit)
- Stage 2: SceneGenerated
- Stage 3: CoordinateExtraction (deterministic local)
- Stage 4: CompositeValidation (deterministic local checks)
- Stage 5: ReviewPending
- Stage 6: ApprovedForProcessing
- Stage 7: ProcessedToManagedLibrary
- Stage 8: ExportReady
- Terminal states: Failed, Cancelled

### Required state payload fields per item
- job_id
- source_slug / source_asset_id
- category
- aspect_ratio_placeholder
- aspect_ratio_canvas
- generation_model
- generation_mode
- fallback_flags (array)
- coordinates_source (extracted|fallback) where relevant
- status
- reason_code
- error_message
- created_at / updated_at / finished_at

## UX direction: Studio vs Mockup Management

### Studio (generation/review queue only)
Must include:
- Queue-focused cards with preview, status, reason, timestamps
- Approved checkbox on preview cards
- Process Approved action (bulk + single)
- No long-term library management actions on Studio

Must remove from Studio:
- Export Bases action
- Processed managed items list

### Mockup Management (managed library state)
Must include:
- Promoted/processed items only
- Export Bases action moved here
- Filtering:
  - by aspect ratio
  - by category
  - by aspect ratio + category combined
- Category reassignment action
- Visibility of lineage and promotion metadata

Interpretation rule:
- "Processed" means promoted into managed library state, with catalog registration and audit metadata.

## Workflow modules to implement in DreamArtMachine (from ArtLomo reference patterns)

Important context:
- Use ArtLomo as architecture reference only.
- Do not assume active ArtLomo mockup generation execution paths; treat mockup-related modules as legacy/decommission/admin reference unless explicitly validated otherwise.

1. Queue and job-state orchestration
Reference areas in ArtLomo:
- application/analysis/worker/analysis_worker.py
- application/mockups/tasks_mockup_generator.py (reference only)

What to bring conceptually:
- Explicit stage transitions and manifest-like status updates
- Error classification with reason codes
- Cancellation-safe cleanup boundaries

2. Deterministic coordinate extraction/compositing boundary
Reference areas:
- tests/test_composite_coordinate_service.py
- application/mockups/services/precision_service.py (reference only)
- application/mockups/services/MockupCoordinateService.py (reference only)

What to bring:
- Local geometry extraction as source of truth
- Coordinates_source tagging and strict validation

3. Managed catalog promotion and admin workflows
Reference areas:
- application/mockups/admin/routes/mockup_admin_routes.py
- application/mockups/assets_index.py
- application/mockups/assets_sync.py

What to bring:
- Promotion into managed catalog, dedupe handling, metadata reconciliation

4. Decommission-safe route discipline
Reference areas:
- tests/test_decommission_routes.py
- application/mockups/admin/routes/generator_routes.py

What to bring:
- Preserve intentional removals with regression tests to prevent accidental route resurrection

## Proposed DreamArtMachine implementation plan (Copilot-ready)

Phase A: Contracts first
1. Define canonical job schema and stage enum.
2. Define state-transition rules and allowed edges.
3. Define fallback taxonomy and mandatory logging fields.
4. Add tests for state transitions and invalid transitions.

Phase B: Studio queue behavior
1. Build/adjust Studio card model to include Approved checkbox.
2. Add Process Approved endpoint/action.
3. Ensure processed/promoted items are removed from Studio feed.
4. Keep Studio strictly generation/review queue.

Phase C: Mockup Management area
1. Create dedicated managed-library view.
2. Move Export Bases functionality to this area.
3. Add filters by aspect ratio, category, and combined filters.
4. Add category reassignment workflow with audit log.

Phase D: Deterministic processing pipeline
1. Wire Stage 3 coordinate extraction to local deterministic services.
2. Wire Stage 4 composite validation checks before promotion.
3. Write coordinates_source and verification metadata on each processed item.
4. Block promotion when deterministic checks fail.

Phase E: Reliability and observability
1. Add structured logs per stage transition.
2. Add reason_code taxonomy and dashboard summaries.
3. Add explicit fallback event logging (not just warning text).
4. Add operational metrics counters per failure class.

## Copilot execution prompts (ready to use)

Prompt 1: State machine foundation
"Implement a strict mockup pipeline state machine for DreamArtMachine with stages IntakeQueued -> SceneGenerationRequested -> SceneGenerated -> CoordinateExtraction -> CompositeValidation -> ReviewPending -> ApprovedForProcessing -> ProcessedToManagedLibrary -> ExportReady, including terminal Failed/Cancelled states. Add guards preventing invalid transitions and unit tests for allowed/denied transitions."

Prompt 2: Studio queue UX changes
"Refactor Studio so it only shows generation/review queue items. Add an Approved checkbox on each preview card and a Process Approved bulk action. When an item is processed/promoted, remove it from Studio results."

Prompt 3: Mockup Management feature set
"Create a Mockup Management area for processed/promoted items only. Move Export Bases action from Studio to Mockup Management. Add filters by aspect ratio, category, and both combined. Add category reassignment with audit logging."

Prompt 4: Deterministic coordinate/compositing boundary
"Ensure coordinate extraction and final compositing decisions are deterministic and local. AI-generated scene content must not be treated as coordinate truth. Persist coordinates_source and validation metadata on every processed item."

Prompt 5: Fallback governance
"Introduce explicit fallback policy with typed fallback events (model_fallback, guide_fallback, coordinate_fallback). Every fallback must be logged and persisted in job metadata; remove silent critical fallbacks."

## Acceptance criteria checklist
- Studio contains only queue/review items.
- Studio supports Approved checkbox and Process Approved action.
- Processed/promoted items no longer appear in Studio.
- Mockup Management contains processed/promoted library only.
- Export Bases available in Mockup Management, not Studio.
- Mockup Management filters work for aspect ratio, category, and both.
- Category reassignment works and is audited.
- Processed state writes managed-library metadata (not just file move).
- Coordinate/composite truth remains deterministic/local.
- Fallback events are explicit and queryable.

## Risks and mitigations

Risk: Reintroducing silent fallbacks during migration
- Mitigation: enforce fallback-event schema + tests requiring event emission.

Risk: Contract drift between tests and service layers
- Mitigation: lock interface contracts (prompt handling, config shape, signature compatibility) with adapter tests.

Risk: Legacy coupling leakage from ArtLomo patterns
- Mitigation: treat ArtLomo as behavior reference only; rewrite clean modules in DreamArtMachine.

Risk: Treating legacy mockup references as active ArtLomo source of truth
- Mitigation: prioritize ArtLomo analysis/admin lifecycle patterns and decommission tests; implement DreamArtMachine mockup generation as first-class native workflow.

## Phase-two ArtLomo reference files to review while implementing
- application/analysis/worker/analysis_worker.py
- application/mockups/tasks_mockup_generator.py
- application/mockups/services/gemini_service.py
- application/mockups/services/precision_service.py
- application/mockups/services/MockupCoordinateService.py
- application/mockups/admin/routes/mockup_admin_routes.py
- tests/test_analysis_queue.py
- tests/test_mockup_base_generation_stage2a.py
- tests/test_composite_coordinate_service.py
- tests/test_decommission_routes.py

## Final implementation note
This transition should preserve ArtLomo-proven workflow depth while enforcing DreamArtMachine clarity:
- stricter contracts
- cleaner queue/management separation
- deterministic local truth for coordinates/compositing
- auditable promotion lifecycle for reusable production mockup bases
