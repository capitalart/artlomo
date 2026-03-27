# Workflow Analysis Report (Consolidated)

Date: 2026-03-27
Status: Rebuilt

This file replaces a corrupted oversized dump and now points to authoritative docs:

- AI analysis report: Analysis-Workflow-Report.md
- AI analysis map: AI-Analysis-and-Review-Workflow-File-Map.md
- Manual analysis map: Manual-Analysis-and-Review-Workflow-File-Map.md
- Preset implementation map: AI-Analysis-Management-and-Edit-System-Implementation.md

## Current System Snapshot
- API analysis routes exist in application/analysis/api/routes.py.
- Manual routes exist in application/analysis/manual/routes/manual_routes.py.
- Shared review/save/lock endpoints are in application/artwork/routes/artwork_routes.py.
- UI workspace is served from application/common/ui/templates/analysis_workspace.html.
