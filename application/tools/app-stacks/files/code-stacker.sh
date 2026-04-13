#!/usr/bin/env bash
set -euo pipefail

# Code stack generator for ArtLomo.
# Supports profile-based output:
# - full:   broad developer stack (code + selected docs)
# - gemini: curated single-file context for external AI review

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="${APP_ROOT_OVERRIDE:-$(cd "${SCRIPT_DIR}/../../.." && pwd)}"
WORKSPACE_ROOT="${WORKSPACE_ROOT_OVERRIDE:-$(cd "${APP_ROOT}/.." && pwd)}"
STACK_DIR="${STACK_DIR_OVERRIDE:-${APP_ROOT}/tools/app-stacks/stacks}"
FILE_PREFIX="${FILE_PREFIX:-application}"
STACK_PROFILE="${STACK_PROFILE:-full}"
INCLUDE_ENV_IN_STACK="${INCLUDE_ENV_IN_STACK:-false}"
STACK_OUTPUT_FORMAT="${STACK_OUTPUT_FORMAT:-md}"
TS="$(date +"%a-%d-%B-%Y-%I-%M-%p" | tr '[:lower:]' '[:upper:]')"

case "${STACK_OUTPUT_FORMAT}" in
  md|txt) ;;
  *)
    echo "Invalid STACK_OUTPUT_FORMAT: ${STACK_OUTPUT_FORMAT} (expected: md or txt)" >&2
    exit 1
    ;;
esac

OUT_EXT="${STACK_OUTPUT_FORMAT}"
OUT_FILE="${STACK_DIR}/${FILE_PREFIX}-code-stack-${TS}.${OUT_EXT}"

log() { echo "$(date +'%F %T') | $*"; }

[[ -d "${APP_ROOT}" ]] || { echo "Application root not found: ${APP_ROOT}" >&2; exit 1; }
mkdir -p "${STACK_DIR}"

if [[ "${STACK_OUTPUT_FORMAT}" == "md" ]]; then
  echo "# CODE STACK (${TS})" > "${OUT_FILE}"
  echo "" >> "${OUT_FILE}"
  echo "Profile: ${STACK_PROFILE}" >> "${OUT_FILE}"
  echo "" >> "${OUT_FILE}"
  echo "## WORKSPACE ROOT FILES" >> "${OUT_FILE}"
  echo "" >> "${OUT_FILE}"
else
  {
    echo "CODE STACK (${TS})"
    echo "Profile: ${STACK_PROFILE}"
    echo ""
    echo "WORKSPACE ROOT FILES"
    echo "============================================================"
  } > "${OUT_FILE}"
fi

# Map file paths to markdown fence languages so embedded file content
# is treated as literal content rather than parsed markdown structure.
detect_fence_lang() {
  local file_path="$1"
  local basename
  basename="$(basename "${file_path}")"

  case "${basename}" in
    *.py) echo "python" ;;
    *.js) echo "javascript" ;;
    *.ts) echo "typescript" ;;
    *.css) echo "css" ;;
    *.html) echo "html" ;;
    *.json) echo "json" ;;
    *.toml) echo "toml" ;;
    *.yaml|*.yml) echo "yaml" ;;
    *.sh) echo "bash" ;;
    *.ini|*.cfg) echo "ini" ;;
    *.md) echo "markdown" ;;
    .gitignore|.copilotrules) echo "text" ;;
    *) echo "text" ;;
  esac
}

append_content_block() {
  local display_path="$1"
  local abs_path="$2"
  local fence_lang

  [[ -f "${abs_path}" ]] || return 0
  fence_lang="$(detect_fence_lang "${display_path}")"

  if [[ "${STACK_OUTPUT_FORMAT}" == "md" ]]; then
    printf "\n\n## %s\n\n\`\`\`\`%s\n" "${display_path}" "${fence_lang}" >> "${OUT_FILE}"
    cat "${abs_path}" >> "${OUT_FILE}"
    printf "\n\`\`\`\`\n" >> "${OUT_FILE}"
  else
    {
      echo ""
      echo "------------------------------------------------------------"
      echo "FILE: ${display_path}"
      echo "LANG: ${fence_lang}"
      echo "------------------------------------------------------------"
      cat "${abs_path}"
      echo ""
    } >> "${OUT_FILE}"
  fi
}

write_group_heading() {
  local title="$1"

  if [[ "${STACK_OUTPUT_FORMAT}" == "md" ]]; then
    echo "" >> "${OUT_FILE}"
    echo "## ${title}" >> "${OUT_FILE}"
    echo "" >> "${OUT_FILE}"
  else
    {
      echo ""
      echo "${title}"
      echo "============================================================"
    } >> "${OUT_FILE}"
  fi
}

# Add key workspace-root files.
# Optional files are included when present and skipped silently when absent.
append_workspace_file() {
  local root_file="$1"
  local root_file_path="${WORKSPACE_ROOT}/${root_file}"

  [[ -f "${root_file_path}" ]] || return 0
  append_content_block "${root_file} (workspace root)" "${root_file_path}"
  log "INFO: Included ${root_file} from workspace root"
}

append_repo_file() {
  local rel_path="$1"
  local abs_path="${WORKSPACE_ROOT}/${rel_path}"

  [[ -f "${abs_path}" ]] || return 0
  append_content_block "${rel_path}" "${abs_path}"
  log "INFO: Included ${rel_path}"
}

append_abs_file() {
  local abs_path="$1"
  local rel_path

  [[ -f "${abs_path}" ]] || return 0
  rel_path="${abs_path#${WORKSPACE_ROOT}/}"
  append_content_block "${rel_path}" "${abs_path}"
  log "INFO: Included ${rel_path}"
}

declare -a OPTIONAL_ROOT_FILES=()
declare -a REQUIRED_ROOT_FILES=()
declare -a CURATED_CONTEXT_FILES=()
declare -a GEMINI_REFERENCE_MD_DIRS=()

if [[ "${STACK_PROFILE}" == "gemini" ]]; then
  OPTIONAL_ROOT_FILES=(
    ".copilotrules"
    "README.md"
    "CHANGELOG.md"
    "QUICK-START-GUIDE.md"
    "requirements.txt"
    "pytest.ini"
    "db.py"
    "wsgi.py"
  )

  CURATED_CONTEXT_FILES=(
    "application/docs/ARCHITECTURE_INDEX.md"
    "application/docs/SYSTEM_MAP.md"
    "application/docs/DEFINITION_OF_DONE.md"
    "application/docs/rules-&-parameters.md"
    "application/docs/MASTER_FILE_INDEX.md"
    "application/docs/MASTER_WORKFLOWS_INDEX.md"
  )
else
  OPTIONAL_ROOT_FILES=(
    ".copilotrules"
    "README.md"
    "CHANGELOG.md"
    "QUICK-START-GUIDE.md"
    "requirements.txt"
    "pytest.ini"
    "db.py"
    "wsgi.py"
    ".gitignore"
  )
fi

if [[ "${INCLUDE_ENV_IN_STACK}" == "true" ]]; then
  OPTIONAL_ROOT_FILES+=(".env")
fi

for root_file in "${OPTIONAL_ROOT_FILES[@]}"; do
  append_workspace_file "${root_file}"
done

for root_file in "${REQUIRED_ROOT_FILES[@]}"; do
  root_file_path="${WORKSPACE_ROOT}/${root_file}"
  if [[ -f "${root_file_path}" ]]; then
    append_workspace_file "${root_file}"
  else
    log "INFO: Skipped ${root_file} (not found at ${root_file_path})"
  fi
done

if (( ${#CURATED_CONTEXT_FILES[@]} > 0 )); then
  write_group_heading "CURATED CONTEXT FILES"

  for context_file in "${CURATED_CONTEXT_FILES[@]}"; do
    append_repo_file "${context_file}"
  done
fi

if [[ "${STACK_PROFILE}" == "gemini" ]]; then
  GEMINI_REFERENCE_MD_DIRS=(
    "${APP_ROOT}/docs"
    "${APP_ROOT}/workflows"
    "${APP_ROOT}/changelog-reports"
    "${WORKSPACE_ROOT}/changelog-reports"
  )

  write_group_heading "GEMINI REFERENCE MARKDOWN"

  while IFS= read -r md_file; do
    append_abs_file "${md_file}"
  done < <(
    for md_dir in "${GEMINI_REFERENCE_MD_DIRS[@]}"; do
      [[ -d "${md_dir}" ]] || continue
      find "${md_dir}" \
        -name "__pycache__" -prune -o \
        -name "node_modules" -prune -o \
        -name ".pytest_cache" -prune -o \
        -name ".mypy_cache" -prune -o \
        -name ".ruff_cache" -prune -o \
        -path "${APP_ROOT}/tools/app-stacks/backups" -prune -o \
        -path "${APP_ROOT}/tools/app-stacks/stacks" -prune -o \
        -type f -name "*.md" -print
    done | sort -u
  )
fi

write_group_heading "SOURCE TREE"

collect_source_files() {
  local root="$1"
  [[ -d "$root" ]] || return 0

  find "$root" \
    -name "__pycache__" -prune -o \
    -name "node_modules" -prune -o \
    -name ".pytest_cache" -prune -o \
    -name ".mypy_cache" -prune -o \
    -name ".ruff_cache" -prune -o \
    -path "$root/tools/app-stacks/backups" -prune -o \
    -path "$root/tools/app-stacks/stacks" -prune -o \
    -path "$root/lab/locked" -prune -o \
    -path "$root/lab/processed" -prune -o \
    -path "$root/lab/unprocessed" -prune -o \
    -type f \( \
      -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.css" -o \
      -name "*.html" -o -name "*.json" -o -name "*.txt" -o \
      -name "*.toml" -o -name "*.yaml" -o -name "*.yml" -o -name "*.sh" -o \
      -name "*.ini" -o -name "*.cfg" \
    \) -print
}

log "INFO: Building code stack from workspace ${WORKSPACE_ROOT}"
declare -a INCLUDE_ROOTS=()

if [[ "${STACK_PROFILE}" == "gemini" ]]; then
  INCLUDE_ROOTS=(
    "${APP_ROOT}/admin"
    "${APP_ROOT}/analysis"
    "${APP_ROOT}/artwork"
    "${APP_ROOT}/upload"
    "${APP_ROOT}/mockups"
    "${APP_ROOT}/export"
    "${APP_ROOT}/video"
    "${APP_ROOT}/video_worker"
    "${APP_ROOT}/common"
    "${APP_ROOT}/utils"
    "${APP_ROOT}/routes"
    "${WORKSPACE_ROOT}/tests"
  )

  # Ensure top-level app files are included in gemini profile.
  for top_file in \
    "application/app.py" \
    "application/config.py" \
    "application/logging_config.py" \
    "application/__init__.py" \
    "application/_legacy_guard.py"; do
    append_repo_file "${top_file}"
  done
else
  INCLUDE_ROOTS=(
    "${APP_ROOT}/admin"
    "${APP_ROOT}/analysis"
    "${APP_ROOT}/artwork"
    "${APP_ROOT}/upload"
    "${APP_ROOT}/mockups"
    "${APP_ROOT}/export"
    "${APP_ROOT}/video"
    "${APP_ROOT}/video_worker"
    "${APP_ROOT}/common"
    "${APP_ROOT}/utils"
    "${APP_ROOT}/routes"
    "${APP_ROOT}/docs"
    "${APP_ROOT}/workflows"
    "${WORKSPACE_ROOT}/tests"
  )

  # Include top-level application bootstrap files in full profile.
  for top_file in \
    "application/app.py" \
    "application/config.py" \
    "application/logging_config.py" \
    "application/__init__.py" \
    "application/_legacy_guard.py"; do
    append_repo_file "${top_file}"
  done
fi

while IFS= read -r file; do
  rel_path="${file#${WORKSPACE_ROOT}/}"
  append_content_block "${rel_path}" "${file}"
done < <(
  for root in "${INCLUDE_ROOTS[@]}"; do
    collect_source_files "$root"
  done | sort -u
)

log "SUCCESS: Code stack written to ${OUT_FILE}"
