# Phase 2: Template selection

Phase 2 is a decision layer. It chooses which templates to render and then calls
the Phase 1 executor to generate assets. It never touches files directly.

- Catalog: `application/mockups/catalog/catalog.json` declares all templates with

  explicit base/coords paths, categories, roles, and enabled flags. No scanning or
  guessing.

- Policy: code-driven via `SelectionPolicy` specifying total slots, mandatory

  template slugs, and optional categories with optional per-category caps.

- Planner: `plan_slots()` builds a deterministic slot→template map. Mandatory

  templates occupy the lowest slot numbers; optional templates fill the rest in
  deterministic order keyed by SKU.

- Executor: `execute_plan()` invokes `generate_mockups_for_artwork()` for each

  slot. Phase 1 handles compositing, hashing, and asset index updates.

Rules:

- If a template is disabled or missing, it is never selected.

- If the policy cannot be satisfied (e.g., not enough optional templates), a

  `ValidationError` is raised; nothing is written.

- Paths are resolved exactly as declared in the catalog (relative paths are

  resolved against `application/mockups`).
