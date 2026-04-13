# ArtLomo -> DreamArtMachine Copilot Handoff Brief
Date stamp: 29 March 2026, 12:00 (local)
Scope: Implementation brief for /srv/dreamartmachine
Source context: /srv/artlomo reference audit and transition blueprint

## 1) Operating truth (read first)
- DreamArtMachine is the active mockup generation and preparation engine.
- ArtLomo is reference-only for workflow patterns and decommission posture.
- Do not copy ArtLomo mockup runtime paths directly.
- Gemini is for scene generation/editing only.
- Coordinate extraction and compositing truth must remain deterministic and local.
- "Processed" means promoted into managed library state with metadata and logs, not just file movement.

## 2) Product direction
### Studio
- Purpose: generation/review queue only.
- Add Approved checkbox on each preview card.
- Add Process Approved action (single and bulk).
- Processed/promoted items must disappear from Studio.
- Remove Export Bases from Studio.

### Mockup Management
- Purpose: managed library of processed/promoted assets.
- Move Export Bases action here.
- Add filtering by:
  - aspect ratio
  - category
  - aspect ratio + category combined
- Support category reassignment.
- Show lineage and promotion metadata.

## 3) Required pipeline stages
Implement as explicit state machine with strict transitions:
- IntakeQueued
- SceneGenerationRequested
- SceneGenerated
- CoordinateExtraction
- CompositeValidation
- ReviewPending
- ApprovedForProcessing
- ProcessedToManagedLibrary
- ExportReady
- Terminal: Failed, Cancelled

Each item/job must persist:
- job_id
- source_asset_id or source_slug
- category
- placeholder_aspect_ratio
- canvas_aspect_ratio
- generation_model
- generation_mode
- fallback_flags
- coordinates_source
- status
- reason_code
- error_message
- created_at, updated_at, finished_at

## 4) Non-negotiable engineering rules
1. No silent critical fallbacks.
- Every fallback emits structured event metadata.

2. Deterministic boundary enforcement.
- AI output cannot become coordinate/compositing truth automatically.

3. Promotion gate.
- Block promotion when deterministic checks fail.

4. Contract-first test discipline.
- Lock call contracts at service boundaries.
- Update tests and code in the same change set.

## 5) Implementation order (minimal-risk)
### Phase A: Contracts and state machine
- Define enums, transition graph, guards.
- Add tests for allowed and denied transitions.

### Phase B: Studio queue refactor
- Add Approved checkbox.
- Add Process Approved endpoint/action.
- Remove Export Bases from Studio.
- Ensure promoted items are removed from Studio list.

### Phase C: Mockup Management module
- Build promoted-only listing.
- Add export action.
- Add filters and category reassignment.
- Add promotion lineage display.

### Phase D: Deterministic processing integration
- Wire local coordinate extraction.
- Wire local composite validation.
- Persist coordinates_source and validation result.

### Phase E: Observability
- Structured stage transition logs.
- fallback_flags taxonomy (model_fallback, guide_fallback, coordinate_fallback).
- Metrics counters per failure class.

## 6) Immediate acceptance checklist
- Studio only shows generation/review queue.
- Approved checkbox exists on preview cards.
- Process Approved action works for single and bulk.
- Processed/promoted items no longer appear in Studio.
- Mockup Management contains promoted library only.
- Export Bases is in Mockup Management only.
- Filtering works by aspect ratio, category, and combined.
- Category reassignment works and is audited.
- Processed state writes managed-library metadata.
- Deterministic coordinate/compositing truth is enforced.
- Fallback events are explicit and queryable.

## 7) Ready-to-run Copilot prompts
1. "Implement a strict mockup pipeline state machine in DreamArtMachine with explicit stage transitions, guards, terminal states, and tests for invalid transitions."
2. "Refactor Studio into a queue-only surface; add Approved checkboxes and a Process Approved bulk action; hide promoted items from Studio."
3. "Create Mockup Management for promoted assets only; move Export Bases here; add filters for aspect ratio/category/combined and category reassignment with audit logging."
4. "Enforce deterministic local coordinate extraction and compositing validation before promotion; persist coordinates_source and validation metadata."
5. "Add structured fallback event logging and reason_code taxonomy; remove silent critical fallback paths."

## 8) Guardrails for the implementation pass
- Treat ArtLomo as reference behavior, not direct source to transplant.
- Avoid broad refactors during initial migration.
- Keep PRs small, contract-focused, and test-backed.
- Require green stage-specific tests before moving to next phase.
