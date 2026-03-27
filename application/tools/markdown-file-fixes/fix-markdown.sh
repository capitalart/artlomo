#!/usr/bin/env bash
# QUICK RUN COMMANDS (project-wide markdown lint/fix)
#
# From workspace root `/srv/artlomo`:
#
# 1) Check markdown issues only (no changes):
#    ./application/tools/markdown-file-fixes/fix-markdown.sh --check
#
# 2) Auto-fix markdown issues across project (default mode):
#    ./application/tools/markdown-file-fixes/fix-markdown.sh --auto
#
# 3) Include generated app-stacks markdown files too:
#    ./application/tools/markdown-file-fixes/fix-markdown.sh --auto --include-stacks
#
# 4) Preview semi-automatic changes without modifying files:
#    ./application/tools/markdown-file-fixes/fix-markdown.sh --auto --dry-run
#
# Which script to use?
# - Use `fix-stacks-markdown.py` for generated stack snapshots only.
# - Use `fix-markdown.sh` for full project markdown lint/fix passes.
#
# fix-markdown.sh - Safely fix common markdown linting errors in ArtLomo project
# Scans ALL .md files recursively (excluding build/dependency directories)
# Handles: MD001 (check-only), MD022, MD024, MD031, MD032, MD036, MD038, MD040
# Usage: ./fix-markdown.sh [options]
# Options:
#   ./fix-markdown.sh --auto       Run automatic fixes + MD036 conversion for all .md files
#   ./fix-markdown.sh --all        Same as --auto (compatibility alias)
#   ./fix-markdown.sh --check      Check errors without fixing
#   ./fix-markdown.sh --dry-run    Show what would change (only affects semi-automatic fixes)
#   ./fix-markdown.sh --include-stacks  Include generated stacks files (usually excluded)
#   ./fix-markdown.sh --help       Show this help message

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find all .md files recursively, excluding common build/dependency directories
get_all_markdown_files() {
  local find_cmd="find \"$SCRIPT_DIR\" -type f -name \"*.md\" \
    -not -path \"*/node_modules/*\" \
    -not -path \"*/.venv/*\" \
    -not -path \"*/__pycache__/*\" \
    -not -path \"*/archived/legacy_backup_*/*\""
  
  # Only exclude stacks if not explicitly included
  if [[ "${INCLUDE_STACKS:-false}" != "true" ]]; then
    find_cmd="$find_cmd -not -path \"*/application/tools/app-stacks/stacks/*\""
  fi
  
  find_cmd="$find_cmd -not -path \"*/.git/*\" \
    -not -path \"*/outputs/*\" \
    -not -path \"*/logs/*\" \
    2>/dev/null || true"
  
  eval "$find_cmd"
}

MODE="--auto"
DRY_RUN="false"
INCLUDE_STACKS="false"
REPORT_FILE=""

# Parse all arguments - separate mode from flags
for arg in "$@"; do
  case "$arg" in
    --auto|--all|--check|--help)
      MODE="$arg"
      ;;
    --dry-run)
      DRY_RUN="true"
      ;;
    --include-stacks)
      INCLUDE_STACKS="true"
      ;;
    --report=*)
      REPORT_FILE="${arg#*=}"
      ;;
  esac
done

# Generate file list AFTER parsing flags (so INCLUDE_STACKS is set)
TARGET_FILES_DEFAULT="$(get_all_markdown_files | tr '\n' ' ')"
TARGET_FILES="${TARGET_FILES:-$TARGET_FILES_DEFAULT}"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() { echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n${BLUE}$1${NC}\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; }
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }

show_help() {
  cat << 'EOF'
fix-markdown.sh - Safely fix common markdown linting errors

Scans ALL .md files recursively in the project
(excludes: node_modules, .venv, __pycache__, archived backups, .git, outputs, logs)

USAGE:
  ./fix-markdown.sh [OPTIONS]

OPTIONS:
  --auto        Run safe auto-fixes + MD036 conversion
  --all         Same as --auto (compatibility alias)
  --check       Check errors without fixing
  --dry-run     Do not modify files for semi-automatic steps; show what would change
  --include-stacks  Include generated stacks files (usually excluded)
  --report=PATH Write a report of MD036 conversions to PATH
  --help        Show this help message

FIXES HANDLED:
- MD001: Heading levels should increment by one level at a time (check-only, manual fix required)
- MD022: Headings should be surrounded by blank lines
- MD024: Duplicate headings (allows in different sections via siblings_only)
- MD031: Fenced code blocks should be surrounded by blank lines
- MD032: Lists should be surrounded by blank lines
- MD036: Emphasis used as heading (semi-automatic with --all)
- MD038: Spaces inside code span elements
- MD040: Fenced code blocks should have a language specified

NOTES:
- Safe auto-fixes are handled by markdownlint-cli2 --fix.
- MD036 conversion is semi-automatic and must be reviewed.
- MD024 config allows duplicate headings in different sections.
- Generated app-stacks snapshots are excluded by default.

EOF
}

check_dependencies() {
  if ! command -v npx >/dev/null 2>&1; then
    print_error "npx not found. Install Node.js."
    return 1
  fi
  if ! command -v sed >/dev/null 2>&1; then
    print_error "sed not found."
    return 1
  fi
  if ! command -v python3 >/dev/null 2>&1; then
    print_error "python3 not found."
    return 1
  fi
  return 0
}

# Cross-platform sed -i
sed_inplace() {
  local expr="$1"
  local file="$2"
  if sed --version >/dev/null 2>&1; then
    # GNU sed
    sed -i "$expr" "$file"
  else
    # BSD/macOS sed
    sed -i '' "$expr" "$file"
  fi
}

append_report() {
  local line="$1"
  if [[ -n "$REPORT_FILE" ]]; then
    printf "%s\n" "$line" >> "$REPORT_FILE"
  fi
}

looks_like_heading_line() {
  # Heuristic: bold-only line, 3..80 chars inside, no trailing punctuation, not a sentence.
  # Allowed: letters/numbers/spaces/basic punctuation like & - /
  local inner="$1"
  local len="${#inner}"

  [[ "$len" -ge 3 && "$len" -le 80 ]] || return 1
  [[ "$inner" =~ [\.\!\?]$ ]] && return 1
  [[ "$inner" =~ ^[[:space:]]*$ ]] && return 1
  return 0
}

_normalize_heading_key() {
  local value="$1"
  value="${value,,}"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  # Collapse repeated internal whitespace
  value="$(printf '%s' "$value" | tr -s '[:space:]' ' ')"
  printf '%s' "$value"
}

fix_emphasis_as_headings_file() {
  # Convert lines that are ONLY **Title** into "## Title"
  # Strict: only if inner text looks like a heading (heuristic).
  local file="$1"
  local changed="false"

  local lineno=0
  while IFS= read -r line; do
    lineno=$((lineno + 1))

    if [[ "$line" =~ ^\*\*([^\*].*[^\*])\*\*$ ]]; then
      local inner="${BASH_REMATCH[1]}"
      # Trim
      inner="${inner#"${inner%%[![:space:]]*}"}"
      inner="${inner%"${inner##*[![:space:]]}"}"

      if looks_like_heading_line "$inner"; then
        changed="true"
        append_report "$file:$lineno  **$inner**  ->  ## $inner"
      fi
    fi
  done < "$file"

  if [[ "$changed" != "true" ]]; then
    return 0
  fi

  print_warning "MD036 candidate conversions in: $file"
  if [[ "$DRY_RUN" == "true" ]]; then
    print_warning "Dry run enabled; not modifying $file"
    return 0
  fi

  # Portable replacement pass (bash-only): avoids awk dialect issues across distros.
  local tmp_file
  tmp_file="${file}.tmp"
  : > "$tmp_file"

  local converted="false"
  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" =~ ^\*\*([^\*].*[^\*])\*\*$ ]]; then
      local inner="${BASH_REMATCH[1]}"
      inner="${inner#"${inner%%[![:space:]]*}"}"
      inner="${inner%"${inner##*[![:space:]]}"}"

      if looks_like_heading_line "$inner"; then
        printf '## %s\n' "$inner" >> "$tmp_file"
        converted="true"
        continue
      fi
    fi

    printf '%s\n' "$line" >> "$tmp_file"
  done < "$file"

  if [[ "$converted" == "true" ]]; then
    mv "$tmp_file" "$file"
    print_success "Converted bold-only headings in $file"
  else
    rm -f "$tmp_file"
  fi
}

fix_duplicate_headings_file() {
  # Convert duplicate markdown headings into plain text labels to satisfy MD024.
  # Keeps first heading instance intact, demotes later duplicates within same file.
  local file="$1"
  local tmp_file="${file}.tmp"
  local dup_report="${file}.dup_report.tmp"

  if [[ "$DRY_RUN" == "true" ]]; then
    python3 - "$file" "$dup_report" <<'PY'
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
report = Path(sys.argv[2])

lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
seen = {}
dups = []

heading_re = re.compile(r'^(#{1,6})\s+(.+?)\s*$')

def norm(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip().lower())

for idx, line in enumerate(lines, start=1):
    m = heading_re.match(line.rstrip('\n'))
    if not m:
        continue
    heading_text = m.group(2).strip()
    key = norm(heading_text)
    if key in seen:
        dups.append((idx, heading_text))
    else:
        seen[key] = idx

if dups:
    report.write_text("\n".join(f"{ln}\t{text}" for ln, text in dups) + "\n", encoding="utf-8")
else:
    report.write_text("", encoding="utf-8")
PY

    if [[ -s "$dup_report" ]]; then
      print_warning "MD024 duplicate heading candidates in: $file"
      while IFS=$'\t' read -r lineno heading_text; do
        [[ -n "$lineno" ]] && append_report "$file:$lineno  duplicate heading demoted -> $heading_text"
      done < "$dup_report"
    fi
    rm -f "$dup_report"
    return 0
  fi

  python3 - "$file" "$tmp_file" "$dup_report" <<'PY'
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
report = Path(sys.argv[3])

lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
seen = {}
changed = False
report_rows = []
out = []

heading_re = re.compile(r'^(#{1,6})\s+(.+?)\s*$')

def norm(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip().lower())

for idx, line in enumerate(lines, start=1):
    original = line
    stripped_nl = line[:-1] if line.endswith('\n') else line
    m = heading_re.match(stripped_nl)
    if m:
        heading_text = m.group(2).strip()
        key = norm(heading_text)
        if key in seen:
            line = heading_text + ('\n' if original.endswith('\n') else '')
            changed = True
            report_rows.append(f"{idx}\t{heading_text}")
        else:
            seen[key] = idx
    out.append(line)

if changed:
    dst.write_text(''.join(out), encoding='utf-8')
    report.write_text('\n'.join(report_rows) + ('\n' if report_rows else ''), encoding='utf-8')
else:
    report.write_text('', encoding='utf-8')
PY

  if [[ -f "$tmp_file" ]]; then
    mv "$tmp_file" "$file"
    print_success "Demoted duplicate headings in $file"
  fi

  if [[ -s "$dup_report" ]]; then
    while IFS=$'\t' read -r lineno heading_text; do
      [[ -n "$lineno" ]] && append_report "$file:$lineno  duplicate heading demoted -> $heading_text"
    done < "$dup_report"
  fi
  rm -f "$dup_report"
}

run_markdownlint_fix() {
  cd "$SCRIPT_DIR"
  npx markdownlint-cli2 --fix $TARGET_FILES 2>&1 || print_warning "Some files may have unfixable lint errors"
}

run_markdownlint_check() {
  cd "$SCRIPT_DIR"
  npx markdownlint-cli2 $TARGET_FILES 2>&1 || true
}

run_md036_conversions() {
  # Scan all markdown files in the project (excluding build/dependency directories)
  if [[ -n "$REPORT_FILE" ]]; then
    : > "$REPORT_FILE"
    append_report "MD036 conversion report - $(date)"
    append_report "Dry run: $DRY_RUN"
    append_report "----------------------------------------"
  fi

  # Build find command dynamically based on INCLUDE_STACKS flag
  local find_cmd="find \"$SCRIPT_DIR\" -type f -name \"*.md\" \
    -not -path \"*/node_modules/*\" \
    -not -path \"*/.venv/*\" \
    -not -path \"*/__pycache__/*\" \
    -not -path \"*/archived/legacy_backup_*/*\""
  
  # Only exclude stacks if not explicitly included
  if [[ "${INCLUDE_STACKS:-false}" != "true" ]]; then
    find_cmd="$find_cmd -not -path \"*/application/tools/app-stacks/stacks/*\""
  fi
  
  find_cmd="$find_cmd -not -path \"*/.git/*\" \
    -not -path \"*/outputs/*\" \
    -not -path \"*/logs/*\" \
    -print0 2>/dev/null"

  # Process all .md files found
  while IFS= read -r -d '' file; do
    if [[ -f "$file" ]]; then
      fix_emphasis_as_headings_file "$file"
      fix_duplicate_headings_file "$file"
    fi
  done < <(eval "$find_cmd")

  if [[ -n "$REPORT_FILE" ]]; then
    print_success "Wrote MD036 report to: $REPORT_FILE"
  fi
}

run_mode() {
  case "$MODE" in
    --auto)
      print_header "Running Auto-Fixes for All Markdown"
      echo "Fixes applied (via markdownlint --fix): MD022, MD032, MD031, MD040, MD038"
      echo "Plus MD036 conversion: bold-only lines -> headings"
      echo "Check-only (manual fix required): MD001 (heading level increments)"
      echo ""
      run_markdownlint_fix
      run_md036_conversions
      print_success "Auto-fixes complete"
      ;;
    --all)
      print_header "Running Auto-Fixes for All Markdown"
      echo "Includes MD036 conversions (bold-only lines -> headings). Review changes!"
      echo ""
      run_markdownlint_fix
      run_md036_conversions
      print_warning "Review changes: git diff"
      ;;
    --check)
      print_header "Checking for Markdown Errors (No Fixes)"
      echo "Includes MD001 (heading levels) - requires manual fixes if violated"
      echo ""
      run_markdownlint_check
      ;;
    --help)
      show_help
      ;;
    *)
      print_error "Unknown option: $MODE"
      echo "Use --help for usage information"
      return 1
      ;;
  esac
}

main() {
  print_header "ArtLomo Markdown Linter"
  echo ""
  check_dependencies

  echo "Mode: $MODE"
  echo "Scanning: All .md files recursively (excluding build/dependency dirs)"
  echo "Include stacks: $INCLUDE_STACKS"
  echo "Dry run: $DRY_RUN"
  [[ -n "$REPORT_FILE" ]] && echo "Report: $REPORT_FILE"
  echo ""

  run_mode

  echo ""
  print_header "Complete"
}

main "$@"