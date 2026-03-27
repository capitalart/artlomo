---
description: Windsurf startup context check
---

# Windsurf Startup Context Check

Use this workflow at session start (or before any large change) to align with ArtLomo rules.

1. Open and read these files in order:
  - `/srv/artlomo/.windsurfrules`
  - `/srv/artlomo/README.md`
  - `/srv/artlomo/application/docs/ARCHITECTURE_INDEX.md`
  - `/srv/artlomo/application/docs/SYSTEM_MAP.md`
  - `/srv/artlomo/application/docs/DEFINITION_OF_DONE.md`
  - `/srv/artlomo/application/docs/rules-&-parameters.md`

2. Identify the workflow scope for the task:
  - upload, analysis, artwork, mockups, manual, export, admin, or shared.

3. Confirm boundaries before coding:
  - business logic in services
  - routes orchestrate only
  - UI has no business logic
  - no cross-workflow direct imports

4. If changing structure/ownership:
  - update `application/docs/ARCHITECTURE_INDEX.md` in the same task.

5. Run fast validation before finalizing:
  - `python3 -m py_compile <touched_python_files>`
  - check behavior against `DEFINITION_OF_DONE.md`.
