# ArtLomo System Context and Freshness Summary

**Generated:** 2026-03-11 | **Updated:** 2026-03-19 (Gemini 3 Migration Active)
**Workspace:** `/srv/artlomo`
**Purpose:** Single root-level reference for system context, software specs,
workflow docs, and freshness status.

## 1. Quick Assurance

No repository file was replaced by the saved memory note.
The Copilot memory file exists outside the repo at `/memories/...`.

## 2. Authoritative Source Set Reviewed

1. `/srv/artlomo/application/docs/ARCHITECTURE_INDEX.md`

1. `/srv/artlomo/application/docs/SYSTEM_MAP.md`

1. `/srv/artlomo/application/docs/STRUCTURAL_VERIFICATION_REPORT.md`

1. `/srv/artlomo/application/docs/schema_coordinates.json`

1. `/srv/artlomo/application/docs/GOOGLE_CLOUD_VM_SPECS_REPORT_2026-03-07.md`

1. `/srv/artlomo/application/docs/ARTLOMO_SYSTEM_SOFTWARE_REPORT_2026-03-07.md`

1. `/srv/artlomo/application/docs/ARTLOMO_OVERVIEW_2026-03-07.md`

1. `/srv/artlomo/application/workflows/INDEX.md`

1. `/srv/artlomo/application/workflows/WORKFLOW_INDEX.md`

1. Workflow file-map and workflow-report docs listed in your request

## 3. System and Architecture Summary

ArtLomo is a modular Flask system with strict workflow isolation and layered
boundaries:

1. Layer 1: Core utilities, config, and logging.

1. Layer 2: Services and workflow business logic.

1. Layer 3: Routes and HTTP orchestration.

1. Layer 4: UI templates and static assets.

Dependency direction remains one-way (UI -> Routes -> Services -> Core).
No architecture drift was observed in the reviewed docs.

## 4. VM Infrastructure Snapshot

Source: `GOOGLE_CLOUD_VM_SPECS_REPORT_2026-03-07.md`.

- Cloud: Google Compute Engine

- Hostname: `ezy`

- Zone: `australia-southeast2-b`

- Machine type: `n2d-standard-4`

- CPU platform: `AMD Milan`

- vCPU: `4`

- RAM: `15 GiB`

- Disk: `128 GB` persistent disk

- OS: Debian GNU/Linux 12 (bookworm)

- Kernel: `6.1.0-43-cloud-amd64`

- Internal IP: `10.192.0.2`

## 5. Software Stack Snapshot

Source: `ARTLOMO_SYSTEM_SOFTWARE_REPORT_2026-03-07.md` plus live checks on
2026-03-11.

### 5.1 Runtime Versions

- Python: `3.11.2`

- Node.js: `v20.20.0`

- npm: `10.8.2`

### 5.2 Key Python Packages (live check)

- `flask==3.1.2`

- `gunicorn==23.0.0`

- `openai==1.108.1`

- `google-genai==1.56.0`

- `sqlalchemy==2.0.43`

- `pillow==11.3.0`

- `opencv-python-headless==4.12.0.88`

- `numpy==2.2.6`

- `moviepy==1.0.3`

- `celery==5.5.3`

- `redis==6.4.0`

### 5.3 Up-to-date Check Result

The live runtime and package versions sampled above match the March 7 software
report values for these core components.

## 6. Workflow Documentation Summary

### 6.1 Current implementation file maps

- AI analysis and review routes, status polling, and review orchestration.

- Manual workspace edit/save/lock flows.

- Upload ingestion, QC, derivatives, and DB/path sync.

- Mockup generation, slot swap/category updates, index sync.

- Detail closeup proxy/editor/save pipeline.

- Export async ZIP generation and download/status endpoints.

- Video generation in two active paths (promo and kinematic API).

### 6.2 Deep workflow reports

Legacy detailed reports (many dated 2026-02-15) still provide broad logic
coverage and behavior intent, while index files were refreshed on 2026-03-09.

## 7. File Freshness Audit (Requested Set)

Legend:

- Freshly touched: filesystem modified on `2026-03-09`

- Older model/schema artifact: not recently modified

- Content date older than mtime: doc likely reviewed/touched without full

  narrative rewrite

### 7.1 Core docs

- `application/docs/ARCHITECTURE_INDEX.md`: mtime `2026-03-09`, in-doc updated

  marker `March 9, 2026`.

- `application/docs/SYSTEM_MAP.md`: mtime `2026-03-09`, in-doc date

  `March 9, 2026`.

- `application/docs/STRUCTURAL_VERIFICATION_REPORT.md`: mtime `2026-03-09`,

  report date `March 7, 2026`.

- `application/docs/schema_coordinates.json`: mtime `2026-02-08`, version `2.0`.

- `application/docs/GOOGLE_CLOUD_VM_SPECS_REPORT_2026-03-07.md`: mtime

  `2026-03-09`, report date `2026-03-07`.

- `application/docs/ARTLOMO_SYSTEM_SOFTWARE_REPORT_2026-03-07.md`: mtime

  `2026-03-09`, report date `2026-03-07`.

- `application/docs/ARTLOMO_OVERVIEW_2026-03-07.md`: mtime `2026-03-09`, report

  date `2026-03-07`.

### 7.2 Workflow docs in your list

All files below were present and have filesystem mtime `2026-03-09`:

- `application/workflows/AI-Analysis-and-Review-Workflow-File-Map.md`

- `application/workflows/AI-Analysis-Management-and-Edit-System-Implementation.md`

- `application/workflows/Analysis-Workflow-Report.md`

- `application/workflows/Closeup-Detail-Generation-Workflow-File-Map.md`

- `application/workflows/Detail-Closeup-Workflow-Report.md`

- `application/workflows/Export-Workflow-File-Map.md`

- `application/workflows/Export-Workflow-Report.md`

- `application/workflows/INDEX.md`

- `application/workflows/Manual-Analysis-and-Review-Workflow-File-Map.md`

- `application/workflows/Mockup-Management-Workflow-File-Map.md`

- `application/workflows/Mockup-management-Workflow-report.md`

- `application/workflows/Upload-Workflow-File-Map.md`

- `application/workflows/Upload-Workflow-Report.md`

- `application/workflows/Video-Generation-Workflow-File-Map.md`

- `application/workflows/Video-Generation-Workflow-Report.md`

- `application/workflows/WORKFLOW_ANALYSIS_REPORT.md`

- `application/workflows/WORKFLOW_INDEX.md`

- `application/workflows/WORKFLOW_MOCKUP_GENERATION_REPORT.md`

- `application/workflows/WORKFLOW_UPLOAD_REPORT.md`

Documents with explicit older narrative dates in headers:

- `Analysis-Workflow-Report.md` (`2026-02-15`)

- `Detail-Closeup-Workflow-Report.md` (`2026-02-15`)

- `Export-Workflow-Report.md` (`2026-02-15`)

- `Mockup-management-Workflow-report.md` (`2026-02-15`)

- `Upload-Workflow-Report.md` (`2026-02-15`)

- `Video-Generation-Workflow-Report.md` (`2026-02-15`)

- `WORKFLOW_ANALYSIS_REPORT.md` (`date: March 1, 2026`)

- `WORKFLOW_MOCKUP_GENERATION_REPORT.md` (`Last Updated: March 1, 2026`)

## 8. Recommended Refresh Priority

1. Refresh dated workflow narrative reports first (the six Feb 15 reports),

then re-check route/service references against current files.

1. Regenerate system inventory reports via tools scripts when runtime changes are

made (or weekly cadence if preferred).

1. Keep `schema_coordinates.json` under explicit version-control review whenever

coordinate contract changes are introduced.

## 9. Informative One-Paragraph Summary

ArtLomo currently presents as structurally healthy and well documented at the
index/system level, with March 9 updates aligning architecture and workflow
navigation docs, while core VM/software report values from March 7 still match
live runtime checks as of March 11; the main documentation gap is that several
detailed workflow narrative reports retain February dates and should be refreshed
for full "current-state" confidence even though their files were recently touched.
