# GitHub Copilot Instructions for ArtLomo

## ⚠️ MANDATORY PRE-WORK DIRECTIVE

## All GitHub Copilot interactions on this repository MUST begin with

1. **READ `.copilotrules`** (workspace root)

  - Contains all operating protocols, mandatory rules, and constraints

  - Defines the "Golden Loop" (pre-flight → execution → post-flight)

  - Lists 7 critical constraints that must never be violated

1. **READ `.clinerules`, `.cursorrules`, `.windsurfrules`** (if specialized context needed)

  - System-level architectural rules

  - Tool-specific operating parameters

  - Non-negotiable project standards

1. **CONSULT `application/docs/DEFINITION_OF_DONE.md`** before completing ANY task

  - Quality assurance checklist

  - Determines "task complete" status

  - Mandatory verification for image processing, UI, logging, and stability

1. **REFERENCE `application/docs/ARCHITECTURE_INDEX.md`** for all structural decisions

  - Authoritative system design documentation

  - Workflow boundaries and allowed imports

  - Current state audit and deviations

## How This Works

When you're asked to work on ArtLomo, **automatically**:

1. Open and display `.copilotrules` from workspace root

1. Review the section most relevant to the task (Phase 1: Pre-Flight checklist)

1. Verify task against ARCHITECTURE_INDEX.md

1. Execute work while adhering to Golden Loop (pre-flight → code → post-flight)

1. Update documentation per Phase 3 (POST-FLIGHT) before marking complete

## Context Integration

These rules are **always applicable**:

- **Workflow Isolation:** No cross-workflow imports without explicit documentation

- **Single-State Invariant:** Artwork slugs exist in only one `lab/` state at a time

- **Business Logic in Services:** Routes = orchestration only, no UI logic

- **CSS Variables:** Never hardcode colors; use `var(--text-primary)` patterns

- **Image Standards:** ANALYSE (2048px), THUMB (500x500px), DETAIL (7200px)

- **Dark Mode:** Zero white-on-white violations; all text uses CSS variables

- **Documentation as Code:** Update ARCHITECTURE_INDEX.md, APP-AUDIT.md, and DEFINITION_OF_DONE.md together with code changes

## Questions?

If anything in `.copilotrules` is unclear:

1. Cross-reference `application/docs/MASTER_WORKFLOWS_INDEX.md` (technical deep-dives)

1. Check `README.md` for high-level context

1. Review `application/docs/MASTER_FILE_INDEX.md` for file ownership and patterns

## Enforcement

This file is referenced in:

- `.vscode/extensions.json` (extension recommendation note)

- `.vscode/tasks.json` (automated task to display .copilotrules)

- `README.md` (prominent "COPILOT INSTRUCTIONS" section)

## All three create redundant enforcement paths to ensure these rules are never overlooked.
