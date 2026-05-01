#!/usr/bin/env bash
set -euo pipefail

# ArtLomo code-only stack export for external analysis.

resolve_repo_root() {
  if git_root=$(git rev-parse --show-toplevel 2>/dev/null); then
    printf "%s\n" "$git_root"
    return 0
  fi

  local dir
  dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  while [[ "$dir" != "/" ]]; do
    if [[ -d "$dir/.git" || -f "$dir/README.md" ]]; then
      printf "%s\n" "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

REPO_ROOT="$(resolve_repo_root)"
if [[ -z "$REPO_ROOT" || ! -d "$REPO_ROOT" ]]; then
  echo "ERROR: Unable to resolve repository root" >&2
  exit 1
fi

TIMESTAMP="$(date +"%Y-%m-%d-%H%M%S")"
ARCHIVE_BASENAME="artlomo-code-stack-${TIMESTAMP}"
EXPORT_DIR="${REPO_ROOT}/exports/code-stack"
ARCHIVE_PATH="${EXPORT_DIR}/${ARCHIVE_BASENAME}.tar.gz"
LATEST_PATH="${EXPORT_DIR}/latest-artlomo-code-stack.tar.gz"

mkdir -p "$EXPORT_DIR"

TMP_ROOT="$(mktemp -d "${EXPORT_DIR}/.tmp-export-${TIMESTAMP}-XXXX")"
trap 'rm -rf "$TMP_ROOT"' EXIT

BUNDLE_ROOT="${TMP_ROOT}/${ARCHIVE_BASENAME}"
FILES_ROOT="${BUNDLE_ROOT}/files"
mkdir -p "$FILES_ROOT"

LARGE_EXCLUDED_REPORT="${BUNDLE_ROOT}/CODE_STACK_LARGE_EXCLUDED_FILES.txt"
MEDIA_EXCLUDED_REPORT="${BUNDLE_ROOT}/CODE_STACK_MEDIA_EXCLUDED_SUMMARY.txt"
MANIFEST_PATH="${BUNDLE_ROOT}/CODE_STACK_MANIFEST.txt"
SHA_PATH="${BUNDLE_ROOT}/CODE_STACK_SHA256SUMS.txt"
TREE_PATH="${BUNDLE_ROOT}/CODE_STACK_FILE_TREE.txt"
ENV_REPORT_PATH="${BUNDLE_ROOT}/CODE_STACK_ENV_SAFETY_REPORT.md"
VIDEO_FOCUS_PATH="${BUNDLE_ROOT}/CODE_STACK_VIDEO_RENDERING_FOCUS.md"
RUNTIME_SNAPSHOT_PATH="${BUNDLE_ROOT}/CODE_STACK_RUNTIME_VERSION_SNAPSHOT.txt"
EXPORT_REPORT_PATH="${BUNDLE_ROOT}/CODE_STACK_EXPORT_REPORT.md"
README_ANALYSIS_PATH="${BUNDLE_ROOT}/README_FOR_ANALYSIS.md"
EXPORT_JSON="${TMP_ROOT}/export_stats.json"

cat > "$README_ANALYSIS_PATH" <<'MD'
# ArtLomo Code-Only Analysis Bundle

This is a code-only analysis bundle.

Media, generated assets, `.env`, virtual environments, databases, `node_modules`, logs, and caches are intentionally excluded.

Use this bundle for:
- code review
- architecture review
- video-rendering workflow review
- prompt and automation analysis

This bundle is not intended to run standalone.
MD

# Build filtered file set using Python for reliable scanning and reporting.
python3 - "$REPO_ROOT" "$FILES_ROOT" "$LARGE_EXCLUDED_REPORT" "$MEDIA_EXCLUDED_REPORT" "$EXPORT_JSON" <<'PY'
import json
import os
import shutil
import sys
from collections import Counter
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
files_root = Path(sys.argv[2]).resolve()
large_report = Path(sys.argv[3]).resolve()
media_report = Path(sys.argv[4]).resolve()
stats_json = Path(sys.argv[5]).resolve()

include_roots = [
    "application",
    "tests",
    "scripts",
    "tools",
    "docs",
    "previous-documents",
]

include_files = [
    "README.md",
    "QUICK-START-GUIDE.md",
    "CHANGELOG.md",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "wsgi.py",
    "db.py",
    ".gitignore",
    ".env.example",
]

required_video_files = [
    "application/video/routes/video_routes.py",
    "application/video/services/video_service.py",
    "application/video_worker/render.js",
    "application/video_worker/processor.js",
    "application/video_worker/package.json",
    "application/video_worker/package-lock.json",
    "application/common/ui/templates/video_workspace.html",
    "application/common/ui/static/js/video_cinematic.js",
    "application/common/ui/static/js/video_workspace_carousel.js",
    "application/common/ui/static/css/video_suite.css",
    "application/artwork/routes/artwork_routes.py",
    "application/tools/verify_ffmpeg_override.py",
    "application/config.py",
    "application/workflows/Video-Generation-Workflow-File-Map.md",
    "application/workflows/Video-Generation-Workflow-Report.md",
    "application/changelog-reports/VIDEO_SUITE_MANIFEST.md",
    "application/archived/VIDEO_SUITE_SETTINGS_CONTRACT.md",
]

exclude_prefixes = [
    ".git/",
    ".idea/",
    ".vscode/",
    ".venv/",
    "venv/",
    "env/",
    "node_modules/",
    "logs/",
    "tmp/",
    "temp/",
    "cache/",
    "application/lab/",
    "application/common/ui/static/uploads/",
    "application/mockups/catalog/assets/",
    "application/mockups/catalog/generated/",
    "application/mockups/catalog/cache/",
    "application/mockups/previews/",
    "application/outputs/",
    "application/var/",
    "application/video_worker/node_modules/",
    "application/copilot-work/",
    "copilot-work/",
    "data/",
    "var/",
    "storage/",
    "backups/",
    "backup/",
    "exports/code-stack/",
]

blocked_dir_names = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    "env",
}

blocked_exact_names = {
    ".env",
    ".DS_Store",
}

blocked_exts = {
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff", ".bmp", ".heic",
    ".psd", ".ai",
    ".zip", ".tar", ".gz", ".7z", ".rar",
    ".sqlite", ".sqlite3", ".db",
    ".log",
}

allowed_text_exts = {
    ".py", ".js", ".cjs", ".mjs", ".ts", ".tsx",
    ".css", ".scss", ".html", ".jinja", ".j2",
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".sh", ".bash", ".zsh", ".ps1", ".sql", ".csv", ".xml",
    ".svg",
}

large_text_scan_exts = {".md", ".txt", ".json", ".py", ".js", ".css", ".html"}
size_limit = 1024 * 1024

required_set = set(include_files + required_video_files)

media_excluded = Counter()
large_excluded = []
suspicious_md = []
included = []
missing_required = []


def rel_posix(path: Path) -> str:
    return path.relative_to(repo).as_posix()


def is_binary_data(data: bytes) -> bool:
    return b"\x00" in data


def is_plain_text(path: Path) -> bool:
    try:
        sample = path.read_bytes()[:65536]
    except Exception:
        return False
    if is_binary_data(sample):
        return False
    try:
        sample.decode("utf-8")
        return True
    except Exception:
        try:
            sample.decode("latin-1")
            return True
        except Exception:
            return False


def should_exclude_path(rel: str, is_dir: bool) -> bool:
    if rel == "":
        return False
    if rel in blocked_exact_names:
        return True
    if rel.startswith(".env.") and rel != ".env.example":
        return True
    for prefix in exclude_prefixes:
        if rel == prefix.rstrip("/") or rel.startswith(prefix):
            return True
    parts = rel.split("/")
    if any(part in blocked_dir_names for part in parts[:-1] if part):
        return True
    name = parts[-1]
    if name in blocked_exact_names:
        return True
    return False


def classify_media_exclusion(rel: str):
    ext = Path(rel).suffix.lower()
    key = ext if ext else "<no_ext>"
    media_excluded[key] += 1


candidates = set()

for root in include_roots:
    abs_root = repo / root
    if not abs_root.exists():
        continue
    for cur, dirs, files in os.walk(abs_root):
        cur_path = Path(cur)
        rel_cur = rel_posix(cur_path)
        # prune directories in-place
        new_dirs = []
        for d in dirs:
            rel_d = f"{rel_cur}/{d}" if rel_cur else d
            if should_exclude_path(rel_d, is_dir=True):
                continue
            if d in blocked_dir_names:
                continue
            new_dirs.append(d)
        dirs[:] = new_dirs

        for f in files:
            rel_f = f"{rel_cur}/{f}" if rel_cur else f
            candidates.add(rel_f)

for item in include_files + required_video_files:
    p = repo / item
    if p.exists() and p.is_file():
        candidates.add(item)
    elif item in required_video_files:
        missing_required.append(item)

for rel in sorted(candidates):
    p = repo / rel
    if not p.exists() or not p.is_file():
        continue
    if should_exclude_path(rel, is_dir=False):
        continue

    name = p.name
    ext = p.suffix.lower()

    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        continue

    # Block obvious archives/db/media/log assets.
    if ext in blocked_exts:
        # allow .svg only under strict rule; ext is .svg not blocked here.
        classify_media_exclusion(rel)
        continue

    # Extra guard for multi-ext archives.
    lower = rel.lower()
    if lower.endswith(".tar.gz") or lower.endswith(".tar.bz2"):
        classify_media_exclusion(rel)
        continue

    # SVG allowlist: only small static UI sources.
    if ext == ".svg":
        if not rel.startswith("application/common/ui/static/"):
            classify_media_exclusion(rel)
            continue
        if p.stat().st_size > size_limit:
            large_excluded.append((rel, p.stat().st_size, "svg_over_1mb"))
            continue

    # Keep only text-like files (unless explicitly required file).
    explicit_required = rel in required_set
    if ext not in allowed_text_exts and not explicit_required:
        classify_media_exclusion(rel)
        continue

    # Large text handling.
    size = p.stat().st_size
    if ext in large_text_scan_exts and size > size_limit:
        plain = is_plain_text(p)
        if rel in required_set and plain:
            # Include required large text source files.
            pass
        else:
            reason = "over_1mb_non_required" if plain else "over_1mb_not_plain_text"
            large_excluded.append((rel, size, reason))
            continue

    # Generic text validation for safety.
    if not is_plain_text(p):
        classify_media_exclusion(rel)
        continue

    out = files_root / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, out)
    included.append(rel)

# Suspicious markdown detection (report only, no repair).
for rel in sorted(included):
    if not rel.lower().endswith(".md"):
        continue
    p = repo / rel
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        continue
    total = len(lines)
    if total < 200:
        continue
    unique = len(set(lines))
    ratio = (unique / total) if total else 1.0
    repeated = 1.0 - ratio
    if ratio < 0.30 or repeated > 0.70:
        suspicious_md.append((rel, total, unique, ratio, repeated))

large_report.parent.mkdir(parents=True, exist_ok=True)
with large_report.open("w", encoding="utf-8") as f:
    f.write("# Large Excluded Text Files\n\n")
    if not large_excluded:
        f.write("None\n")
    else:
        for rel, size, reason in sorted(large_excluded):
            f.write(f"{rel}\t{size}\t{reason}\n")

    f.write("\n# Suspicious Markdown Duplication Signals\n\n")
    if not suspicious_md:
        f.write("None\n")
    else:
        f.write("path\ttotal_lines\tunique_lines\tunique_ratio\trepeated_ratio\n")
        for rel, total, unique, ratio, repeated in sorted(suspicious_md):
            f.write(f"{rel}\t{total}\t{unique}\t{ratio:.4f}\t{repeated:.4f}\n")

with media_report.open("w", encoding="utf-8") as f:
    f.write("# Media/Binary Excluded Summary\n\n")
    if not media_excluded:
        f.write("None\n")
    else:
        for ext, count in sorted(media_excluded.items()):
            f.write(f"{ext}\t{count}\n")

stats = {
    "included_count": len(included),
    "missing_required": missing_required,
    "suspicious_markdown": [
        {
            "path": rel,
            "total_lines": total,
            "unique_lines": unique,
            "unique_ratio": ratio,
            "repeated_ratio": repeated,
        }
        for rel, total, unique, ratio, repeated in sorted(suspicious_md)
    ],
    "large_excluded_count": len(large_excluded),
    "media_excluded_total": int(sum(media_excluded.values())),
    "included_files": sorted(included),
}
stats_json.write_text(json.dumps(stats, indent=2), encoding="utf-8")
PY

# Environment safety report (redacted values only).
python3 - "$REPO_ROOT" "$ENV_REPORT_PATH" <<'PY'
import os
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out_path = Path(sys.argv[2]).resolve()
env_path = repo / ".env"

required_keys = [
    "OPENAI_API_KEY",
    "GEMINI_API_KEY",
    "FLASK_SECRET_KEY",
    "ADMIN_USERNAME",
    "ADMIN_PASSWORD",
    "ARTLOMO_FFMPEG_BIN",
    "ARTLOMO_FFPROBE_BIN",
]

safe_value_keys = {
    "ENVIRONMENT",
    "HOST",
    "PORT",
    "BASE_URL",
    "ARTLOMO_ROOT",
    "ARTLOMO_BASE_DIR",
    "LAB_UNPROCESSED_DIR",
    "LAB_PROCESSED_DIR",
    "LAB_LOCKED_DIR",
    "ARTWORKS_INDEX_PATH",
    "SKU_SEQUENCE_PATH",
    "ARTLOMO_FFMPEG_BIN",
    "ARTLOMO_FFPROBE_BIN",
}

redact_tokens = ["KEY", "SECRET", "PASSWORD", "TOKEN", "ORG", "PROJECT", "CREDENTIAL", "AUTH"]

pairs = {}
if env_path.exists() and env_path.is_file():
    for raw in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        pairs[k.strip()] = v.strip()

with out_path.open("w", encoding="utf-8") as f:
    f.write("# CODE STACK ENV SAFETY REPORT\n\n")
    f.write(f"- .env exists: {'yes' if env_path.exists() else 'no'}\n")
    f.write("- Raw secret values are never exported in this report.\n\n")

    f.write("## Required Key Presence\n\n")
    for key in required_keys:
        f.write(f"- {key}: {'present' if key in pairs and pairs.get(key, '') != '' else 'missing'}\n")

    f.write("\n## Key Snapshot (Redacted)\n\n")
    if not pairs:
        f.write("No .env key-value pairs detected.\n")
    else:
        for key in sorted(pairs):
            value = pairs[key]
            upper = key.upper()
            if key in safe_value_keys:
                shown = value
            elif any(token in upper for token in redact_tokens):
                shown = "REDACTED"
            else:
                shown = "REDACTED"
            f.write(f"- {key}={shown}\n")
PY

# Runtime snapshot (safe, resilient if binaries crash).
{
  echo "ARTLOMO CODE STACK RUNTIME SNAPSHOT"
  echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "Repo: ${REPO_ROOT}"
  echo
  echo "[SYSTEM]"
  uname -a || true
  sw_vers 2>/dev/null || true
  cat /etc/os-release 2>/dev/null || true
  echo
  echo "[GIT]"
  git -C "$REPO_ROOT" rev-parse --show-toplevel 2>/dev/null || true
  git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || true
  git -C "$REPO_ROOT" branch --show-current 2>/dev/null || true
  git -C "$REPO_ROOT" status --short 2>/dev/null || true
  echo
  echo "[PYTHON]"
  command -v python3 || true
  python3 --version 2>/dev/null || true
  if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
    "${REPO_ROOT}/.venv/bin/python" --version || true
    "${REPO_ROOT}/.venv/bin/pip" --version 2>/dev/null || true
    "${REPO_ROOT}/.venv/bin/pip" freeze 2>/dev/null | grep -Ei "flask|werkzeug|jinja|sqlalchemy|openai|google|genai|celery|redis|pillow|opencv|numpy|scipy|pandas|moviepy|imageio|imageio-ffmpeg|gunicorn|pytest" || true
  fi
  echo
  echo "[NODE]"
  command -v node || true
  node -v 2>/dev/null || true
  command -v npm || true
  npm -v 2>/dev/null || true
  if [[ -d "${REPO_ROOT}/application/video_worker/node_modules" && -f "${REPO_ROOT}/application/video_worker/package.json" ]]; then
    (
      cd "${REPO_ROOT}/application/video_worker"
      npm ls --depth=0 2>/dev/null || true
    )
  fi
  echo
  echo "[FFMPEG]"
  ffmpeg_path="$(command -v ffmpeg || true)"
  ffprobe_path="$(command -v ffprobe || true)"
  echo "ffmpeg_path=${ffmpeg_path}"
  if [[ -n "$ffmpeg_path" ]]; then
    "$ffmpeg_path" -hide_banner -version 2>&1 | head -n 5 || echo "ffmpeg invocation failed"
  fi
  echo "ffprobe_path=${ffprobe_path}"
  if [[ -n "$ffprobe_path" ]]; then
    "$ffprobe_path" -hide_banner -version 2>&1 | head -n 5 || echo "ffprobe invocation failed"
  fi
  echo
  echo "[OVERRIDE]"
  if [[ -x "${REPO_ROOT}/.venv/bin/python" && -f "${REPO_ROOT}/application/tools/verify_ffmpeg_override.py" ]]; then
    "${REPO_ROOT}/.venv/bin/python" "${REPO_ROOT}/application/tools/verify_ffmpeg_override.py" || true
  else
    echo "verify_ffmpeg_override.py unavailable"
  fi
} > "$RUNTIME_SNAPSHOT_PATH"

# Video rendering focus report.
python3 - "$REPO_ROOT" "$VIDEO_FOCUS_PATH" "$EXPORT_JSON" <<'PY'
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out_path = Path(sys.argv[2]).resolve()
stats = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
included = set(stats.get("included_files", []))

video_files = [
    "application/video/routes/video_routes.py",
    "application/video/services/video_service.py",
    "application/video_worker/render.js",
    "application/video_worker/processor.js",
    "application/video_worker/package.json",
    "application/video_worker/package-lock.json",
    "application/common/ui/templates/video_workspace.html",
    "application/common/ui/static/js/video_cinematic.js",
    "application/common/ui/static/js/video_workspace_carousel.js",
    "application/common/ui/static/css/video_suite.css",
    "application/artwork/routes/artwork_routes.py",
    "application/tools/verify_ffmpeg_override.py",
    "application/config.py",
    "application/workflows/Video-Generation-Workflow-File-Map.md",
    "application/workflows/Video-Generation-Workflow-Report.md",
    "application/changelog-reports/VIDEO_SUITE_MANIFEST.md",
    "application/archived/VIDEO_SUITE_SETTINGS_CONTRACT.md",
]

present = [p for p in video_files if (repo / p).exists()]
missing = [p for p in video_files if not (repo / p).exists()]
included_present = [p for p in present if p in included]
not_included_present = [p for p in present if p not in included]

questions = [
    "Is render.js using the best FFmpeg graph for smooth professional videos?",
    "Are xfade/concat modes implemented correctly?",
    "Are fps, timebase, duration, keyframes, and pixel formats handled correctly?",
    "Are UI settings mapped correctly to backend render settings?",
    "Are video controls persisted correctly?",
    "Are output MP4s web-compatible and high quality?",
    "Is the FFmpeg override correctly wired?",
    "Are there any VM/iMac parity risks?",
    "Are there any hardcoded paths?",
    "Is the app using the best practical architecture for reliable video generation?",
]

with out_path.open("w", encoding="utf-8") as f:
    f.write("# CODE STACK VIDEO RENDERING FOCUS\n\n")
    f.write("## Architecture Map\n\n")
    f.write("Flask/Python -> VideoService -> Node render.js -> FFmpeg -> MP4\n\n")
    f.write("## FFmpeg Override Variables\n\n")
    f.write("- ARTLOMO_FFMPEG_BIN\n")
    f.write("- ARTLOMO_FFPROBE_BIN\n\n")
    f.write("## Compositor Concerns\n\n")
    f.write("- xfade\n")
    f.write("- concat\n")
    f.write("- fallback behavior\n")
    f.write("- fps/timebase normalization\n\n")

    f.write("## Included Video-Related Files\n\n")
    for p in included_present:
        f.write(f"- {p}\n")
    if not included_present:
        f.write("- None\n")

    f.write("\n## Existing But Not Included\n\n")
    for p in not_included_present:
        f.write(f"- {p}\n")
    if not not_included_present:
        f.write("- None\n")

    f.write("\n## Missing Expected Video-Related Files\n\n")
    for p in missing:
        f.write(f"- {p}\n")
    if not missing:
        f.write("- None\n")

    f.write("\n## Suggested Analysis Questions\n\n")
    for i, q in enumerate(questions, start=1):
        f.write(f"{i}. {q}\n")
PY

# macOS metadata safety: strip all Finder/AppleDouble artifacts before packaging.
find "$BUNDLE_ROOT" -name '.DS_Store' -type f -delete || true
find "$BUNDLE_ROOT" -name '._*'     -type f -delete || true
find "$BUNDLE_ROOT" -name '__MACOSX' -type d -prune -exec rm -rf {} + 2>/dev/null || true

# Manifest, tree, and checksums.
(
  cd "$BUNDLE_ROOT"
  find . -type f | sed 's|^./||' | LC_ALL=C sort > "$MANIFEST_PATH"
  find . -type f | sed 's|^./||' | LC_ALL=C sort > "$TREE_PATH"
  while IFS= read -r path; do
    if [[ -n "$path" ]]; then
      shasum -a 256 "$path"
    fi
  done < "$MANIFEST_PATH" > "$SHA_PATH"
)

# Compute stats for export report.
GIT_BRANCH="$(git -C "$REPO_ROOT" branch --show-current 2>/dev/null || echo "unknown")"
GIT_COMMIT="$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo "unknown")"
GIT_STATUS_SUMMARY="$(git -C "$REPO_ROOT" status --short 2>/dev/null || true)"
FILE_COUNT="$(wc -l < "$MANIFEST_PATH" | tr -d ' ')"
UNCOMPRESSED_BYTES="$(du -sk "$BUNDLE_ROOT" | awk '{print $1 * 1024}')"

# Load Python-generated stats.
readarray -t STATS_KV < <(python3 - "$EXPORT_JSON" <<'PY'
import json
import sys
s = json.load(open(sys.argv[1], encoding="utf-8"))
print(f"included_count={s.get('included_count', 0)}")
print(f"large_excluded_count={s.get('large_excluded_count', 0)}")
print(f"media_excluded_total={s.get('media_excluded_total', 0)}")
print(f"missing_required={len(s.get('missing_required', []))}")
print(f"suspicious_markdown={len(s.get('suspicious_markdown', []))}")
PY
)
for kv in "${STATS_KV[@]}"; do
  eval "$kv"
done

cat > "$EXPORT_REPORT_PATH" <<EOF
# CODE STACK EXPORT REPORT

- export timestamp: ${TIMESTAMP}
- repo root: ${REPO_ROOT}
- git branch: ${GIT_BRANCH}
- git commit hash: ${GIT_COMMIT}
- archive name: ${ARCHIVE_BASENAME}.tar.gz
- file count: ${FILE_COUNT}
- uncompressed bundle size (bytes): ${UNCOMPRESSED_BYTES}
- compressed archive size (bytes): pending
- excluded file/folder categories:
  - secrets and env files
  - media and binary assets
  - generated/runtime outputs
  - virtual environments, node_modules, caches
  - databases, logs, archives
  - large text files over 1 MB (unless required source text)
- secrets excluded: yes
- media excluded: yes
- large files excluded: yes
- modified files warning: $( [[ -n "$GIT_STATUS_SUMMARY" ]] && echo "yes" || echo "no" )

## Git Status Summary

\
${GIT_STATUS_SUMMARY}

## Export Notes

This is a code-only bundle for external analysis. It cannot run by itself without media, runtime data, and environment configuration.

## Counters

- included files (scanner): ${included_count:-0}
- excluded large text files: ${large_excluded_count:-0}
- excluded media/binary files: ${media_excluded_total:-0}
- missing expected video files: ${missing_required:-0}
- suspicious markdown files (duplication signal): ${suspicious_markdown:-0}
EOF

# Archive creation.
(
  cd "$TMP_ROOT"
  COPYFILE_DISABLE=1 tar --exclude='.DS_Store' --exclude='._*' --exclude='__MACOSX' -czf "$ARCHIVE_PATH" "$ARCHIVE_BASENAME"
)

ARCHIVE_SIZE_BYTES="$(wc -c < "$ARCHIVE_PATH" | tr -d ' ')"

# Update report with compressed size.
python3 - "$EXPORT_REPORT_PATH" "$ARCHIVE_SIZE_BYTES" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
size = sys.argv[2]
text = p.read_text(encoding="utf-8")
text = text.replace("compressed archive size (bytes): pending", f"compressed archive size (bytes): {size}")
p.write_text(text, encoding="utf-8")
PY

# Refresh archive after report size update.
(
  cd "$TMP_ROOT"
  COPYFILE_DISABLE=1 tar --exclude='.DS_Store' --exclude='._*' --exclude='__MACOSX' -czf "$ARCHIVE_PATH" "$ARCHIVE_BASENAME"
)

# latest pointer as copy for cross-platform safety.
cp -f "$ARCHIVE_PATH" "$LATEST_PATH"

# Post-archive metadata validation.
APPLE_DOUBLE_HITS="$(tar -tzf "$ARCHIVE_PATH" | grep -Ec '(^|/)\._' || true)"
MACOSX_HITS="$(tar -tzf "$ARCHIVE_PATH" | grep -Ec '(^|/)__MACOSX($|/)' || true)"

# Summary output.
echo "============================================================"
echo "ArtLomo code stack export complete"
echo "============================================================"
echo "Repository root: $REPO_ROOT"
echo "Archive: $ARCHIVE_PATH"
echo "Latest copy: $LATEST_PATH"
echo "File count: $(wc -l < "$MANIFEST_PATH" | tr -d ' ')"
echo "Archive size: $(ls -lh "$ARCHIVE_PATH" | awk '{print $5}')"
echo "Large excluded report: $LARGE_EXCLUDED_REPORT"
echo "Media excluded report: $MEDIA_EXCLUDED_REPORT"
echo "------------------------------------------------------------"
if [[ "$APPLE_DOUBLE_HITS" -eq 0 ]]; then
  echo "VALIDATION: ._* (AppleDouble) files in archive: NONE (pass)"
else
  echo "VALIDATION: ._* (AppleDouble) files in archive: ${APPLE_DOUBLE_HITS} FOUND (FAIL)" >&2
fi
if [[ "$MACOSX_HITS" -eq 0 ]]; then
  echo "VALIDATION: __MACOSX folders in archive: NONE (pass)"
else
  echo "VALIDATION: __MACOSX folders in archive: ${MACOSX_HITS} FOUND (FAIL)" >&2
fi
echo "============================================================"