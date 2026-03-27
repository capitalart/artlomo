# ArtLomo System and Software Report

**Report Date:** 2026-03-07
**System Scope:** `/srv/artlomo`
**Environment Type:** Google Cloud VM, Debian Linux, production Flask stack

## Executive Summary

ArtLomo is a modular Flask application with workflow-based architecture for artwork processing, AI-assisted analysis, media generation, and export packaging.

The system uses a Python-first stack with targeted Node.js tooling for video processing and a layered architecture to separate utilities, services, routes, and UI.

## Runtime and Platform

- Operating system: Debian GNU/Linux 12 (bookworm).

- Kernel: Linux 6.1.0-43-cloud-amd64.

- Python: 3.11.2.

- Node.js: v20.20.0.

- npm: 10.8.2.

## Core Backend Frameworks

- Flask 3.1.2.

- Werkzeug 3.1.3.

- Jinja2 3.1.6.

- Flask-Login 0.6.3.

- Gunicorn 23.0.0.

- python-dotenv 1.1.1.

## Database and Persistence

- Primary database: SQLite (`artlomo.sqlite3`).

- ORM: SQLAlchemy 2.0.43.

- Core tracked entities include users, artwork records, site settings, and analysis jobs.

The application uses a file-plus-database model where artwork filesystem state and DB status remain synchronized.

## AI and Analysis Stack

- OpenAI SDK: 1.108.1.

- Google GenAI SDK: 1.56.0.

- google-api-python-client: 2.182.0.

- pydantic: 2.11.9.

Provider support includes OpenAI and Gemini pathways, with configurable model stacks and fallback behavior through configuration.

## Async and Queueing

- Celery 5.5.3.

- Redis 6.4.0.

- kombu 5.5.4.

- billiard 4.2.2.

These components support asynchronous background processing and job state handling for heavier operations.

## Image and Vision Stack

- Pillow 11.3.0.

- OpenCV (headless) 4.12.0.88.

- NumPy 2.2.6.

- ImageHash 4.3.2.

- SciPy 1.16.2.

- scikit-learn 1.7.2.

This stack powers derivative generation, perspective transforms, composite workflows, and image validation.

## Video and Media Stack

- FFmpeg (system package).

- moviepy 1.0.3.

- Node video worker dependencies:

- `canvas` 3.2.1.

- `ffcreator` 7.5.8.

- `sharp` 0.34.5.

Video workflows are split across Python orchestration and Node-based rendering helpers.

## Frontend and UI

- Server-rendered Jinja templates.

- Vanilla JavaScript modules.

- Modular CSS architecture with shared theme variables.

- Font Awesome via CDN for iconography.

The UI follows a clean-room workflow style and strict styling rules with global variable-driven themes.

## Security and Request Safety

- CSRF enforcement on mutating endpoints.

- Session-based authentication and role handling.

- Slug and path validation through safe helper utilities.

- Structured security event logging.

## Logging and Observability

Application logging is categorized by domain areas such as startup, database, security, upload, delete, analysis providers, route activity, and general logs.

Primary log root:

- `/srv/artlomo/logs/`

## Architecture Model

ArtLomo follows a 4-layer architecture:

1. Core utilities and shared low-level modules.

1. Service layer for workflow business logic.

1. Route layer for HTTP orchestration.

1. UI layer for templates and static assets.

Dependency direction is upward only.

This keeps responsibilities clear and reduces architectural drift.

## Key Operational Characteristics

- Workflow isolation by domain areas such as upload, analysis, artwork, mockups, export, admin, and video.

- Single-state artwork invariant across unprocessed, processed, and locked paths.

- Config-driven paths and environment settings.

- Asynchronous long-running operations with status polling in UI.

## Notable Tooling in Repository

- pytest for testing.

- black, isort, and ruff for formatting and linting.

- selenium and webdriver-manager for browser automation support.

## Conclusion

ArtLomo runs on a modern Python production stack with targeted Node and FFmpeg capabilities for media-intensive workflows.

Its design emphasizes workflow isolation, data-state discipline, and practical automation for artwork-to-listing production at scale.
