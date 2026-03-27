# Video Suite Backup Manifest

**Created:** February 24, 2026
**Archive:** video-suite-backup-20260224-123441-final.tar.gz
**Size:** 37KB
**Total Files:** 15

## Contents

### Backend Python Services

- `application/video/` - Complete video module

  - `routes/video_routes.py` - Video generation API endpoints

  - `services/video_service.py` - Core video generation service with FFmpeg integration

### Frontend JavaScript/CSS

- `application/common/ui/static/js/video_cinematic.js` - Director's Suite UI controller (1073 lines)

  - Mockup selection and ordering

  - Pan/zoom settings management

  - Per-mockup shot configuration

  - Real-time settings persistence

- `application/common/ui/static/css/video_suite.css` - Director's Suite styling

### Templates

- `application/common/ui/templates/video_workspace.html` - Director's Suite UI layout

### Video Worker (Node.js)

- `video_worker/render.js` - FFmpeg video rendering engine (617 lines)

  - Cover-mode artwork scaling

  - Pan/zoom animation expressions

  - Per-mockup shot settings support

  - Artwork pan direction support (up/down/left/right)

- `video_worker/processor.js` - Video processing pipeline

- `video_worker/package.json` - Node.js dependencies

## Recent Fixes (Feb 24, 2026)

### Bug Fixes

1. **Empty panel bug** - Fixed JavaScript syntax error and function ordering

1. **Per-mockup settings not working** - Added `video_mockup_shots` loading in `_load_cinematic_settings()`

1. **Artwork pan direction ignored** - Modified `buildMasterExpressions()` to accept and use pan direction

1. **Artwork pans when disabled** - Fixed enabled/disabled checks combined with direction support

### Features

- 5 auto-selected mockups on page load

- Individual pan settings per mockup

- User-controlled artwork pan direction

- Settings persistence across reloads

## Restoration

To restore these files:

```bash
cd /srv/artlomo
tar -xzf video-suite-backup-20260224-123441-final.tar.gz
```

## Dependencies

- Python 3.x with Flask

- Node.js v14+

- FFmpeg

- xvfb-run (for headless rendering)
