#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# tools.sh - ArtLomo Documentation & System Inventory Orchestrator
# ============================================================================
#
# Unified command runner for generating documentation snapshots, code stacks,
# backups, and system inventory reports.
#
# AVAILABLE COMMANDS:
#   tree       - Generate folder structure snapshot (tree diagram)
#   stack      - Generate complete code stack (all source files concatenated)
#   stack-txt  - Generate complete code stack as plain text (.txt)
#   gemini     - Generate curated single-file Gemini context stack
#   gemini-txt - Generate Gemini context stack as plain text (.txt)
#   backup     - Create timestamped backup archive (.tar.gz)
#   sysinfo    - Generate comprehensive system inventory report
#   all        - Run all four commands in sequence (tree → stack → backup → sysinfo)
#
# USAGE:
#   ./tools.sh tree      # Generate folder tree only
#   ./tools.sh stack     # Generate code stack only
#   ./tools.sh stack-txt # Generate code stack only as plain text
#   ./tools.sh gemini    # Generate Gemini-ready curated stack only
#   ./tools.sh gemini-txt # Generate Gemini stack only as plain text
#   ./tools.sh backup    # Create backup only
#   ./tools.sh sysinfo   # Generate system inventory only
#   ./tools.sh all       # Run complete documentation suite (recommended)
#
# OUTPUTS:
#   All files are written to: application/tools/app-stacks/stacks/
#   Backups are written to:   application/tools/app-stacks/backups/
#
# DEPENDENCIES:
#   - generate_folder_tree.py (Python 3)
#   - code-stacker.sh (Bash)
#   - cron-backup.sh (Bash)
#   - system-inventory.sh (Bash)
#
# ============================================================================

# Helper wrapper for the new application's stack and backup utilities.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="${APP_ROOT_OVERRIDE:-$(cd "${SCRIPT_DIR}/../../.." && pwd)}"
WORKSPACE_ROOT="${WORKSPACE_ROOT_OVERRIDE:-$(cd "${APP_ROOT}/.." && pwd)}"
STACK_DIR="${STACK_DIR_OVERRIDE:-${APP_ROOT}/tools/app-stacks/stacks}"
BACKUP_DIR="${BACKUP_DIR_OVERRIDE:-${APP_ROOT}/tools/app-stacks/backups}"
FILE_PREFIX="${FILE_PREFIX:-application}"
INCLUDES_FILE_DEFAULT="${SCRIPT_DIR}/backup_includes.txt"

TREE_SCRIPT="${SCRIPT_DIR}/generate_folder_tree.py"
STACK_SCRIPT="${SCRIPT_DIR}/code-stacker.sh"
BACKUP_SCRIPT="${SCRIPT_DIR}/cron-backup.sh"
SYSINFO_SCRIPT="${SCRIPT_DIR}/system-inventory.sh"

log() { echo "$(date +'%F %T') | $*"; }

usage() {
  cat <<EOF
Usage: $(basename "$0") [command]
Commands:
  tree       Generate folder structure snapshot
  stack      Generate code stack
  stack-txt  Generate code stack as plain text (.txt)
  gemini     Generate curated Gemini context stack
  gemini-txt Generate curated Gemini context stack as plain text (.txt)
  backup     Create backup archive
  sysinfo    Generate system inventory report
  all        Run tree + stack + backup + sysinfo
EOF
}

run_tree() {
  APP_ROOT_OVERRIDE="${APP_ROOT}" \
  WORKSPACE_ROOT_OVERRIDE="${WORKSPACE_ROOT}" \
  STACK_DIR_OVERRIDE="${STACK_DIR}" \
  FILE_PREFIX="${FILE_PREFIX}" \
  python3 "${TREE_SCRIPT}"
}

run_stack() {
  APP_ROOT_OVERRIDE="${APP_ROOT}" \
  WORKSPACE_ROOT_OVERRIDE="${WORKSPACE_ROOT}" \
  STACK_DIR_OVERRIDE="${STACK_DIR}" \
  FILE_PREFIX="${FILE_PREFIX}" \
  bash "${STACK_SCRIPT}"
}

run_stack_txt() {
  APP_ROOT_OVERRIDE="${APP_ROOT}" \
  WORKSPACE_ROOT_OVERRIDE="${WORKSPACE_ROOT}" \
  STACK_DIR_OVERRIDE="${STACK_DIR}" \
  FILE_PREFIX="${FILE_PREFIX}" \
  STACK_OUTPUT_FORMAT="txt" \
  bash "${STACK_SCRIPT}"
}

run_gemini_stack() {
  APP_ROOT_OVERRIDE="${APP_ROOT}" \
  WORKSPACE_ROOT_OVERRIDE="${WORKSPACE_ROOT}" \
  STACK_DIR_OVERRIDE="${STACK_DIR}" \
  FILE_PREFIX="${FILE_PREFIX}-gemini" \
  STACK_PROFILE="gemini" \
  INCLUDE_ENV_IN_STACK="false" \
  bash "${STACK_SCRIPT}"
}

run_gemini_stack_txt() {
  APP_ROOT_OVERRIDE="${APP_ROOT}" \
  WORKSPACE_ROOT_OVERRIDE="${WORKSPACE_ROOT}" \
  STACK_DIR_OVERRIDE="${STACK_DIR}" \
  FILE_PREFIX="${FILE_PREFIX}-gemini" \
  STACK_PROFILE="gemini" \
  INCLUDE_ENV_IN_STACK="false" \
  STACK_OUTPUT_FORMAT="txt" \
  bash "${STACK_SCRIPT}"
}

run_backup() {
  local includes_source="${INCLUDES_FILE_OVERRIDE:-${INCLUDES_FILE_DEFAULT}}"
  local includes_runtime
  includes_runtime="$(mktemp)"
  trap 'rm -f "${includes_runtime}"' RETURN

  if [[ ! -f "${includes_source}" ]]; then
    echo "Includes file missing: ${includes_source}" >&2
    return 1
  fi

  while IFS= read -r line || [[ -n "${line}" ]]; do
    local trimmed
    trimmed="${line//[$'\t\r ']}"
    if [[ -z "${trimmed}" ]]; then
      continue
    fi
    [[ "${line}" == \#* ]] && continue

    if [[ -e "${WORKSPACE_ROOT}/${line}" ]]; then
      printf '%s\n' "${line}" >> "${includes_runtime}"
    else
      log "INFO: Skipping missing backup include entry: ${line}"
    fi
  done < "${includes_source}"

  if ! grep -qxF '.' "${includes_runtime}" 2>/dev/null; then
    printf '.\n' >> "${includes_runtime}"
  fi

  APP_ROOT_OVERRIDE="${APP_ROOT}" \
  WORKSPACE_ROOT_OVERRIDE="${WORKSPACE_ROOT}" \
  BACKUP_DIR_OVERRIDE="${BACKUP_DIR}" \
  FILE_PREFIX="${FILE_PREFIX}" \
  INCLUDES_FILE_OVERRIDE="${includes_runtime}" \
  bash "${BACKUP_SCRIPT}"
}

run_sysinfo() {
  APP_ROOT_OVERRIDE="${APP_ROOT}" \
  WORKSPACE_ROOT_OVERRIDE="${WORKSPACE_ROOT}" \
  STACK_DIR_OVERRIDE="${STACK_DIR}" \
  FILE_PREFIX="${FILE_PREFIX}" \
  bash "${SYSINFO_SCRIPT}"
}

case "${1:-}" in
  tree) run_tree ;;
  stack) run_stack ;;
  stack-txt) run_stack_txt ;;
  gemini) run_gemini_stack ;;
  gemini-txt) run_gemini_stack_txt ;;
  backup) run_backup ;;
  sysinfo) run_sysinfo ;;
  all)
    run_tree
    run_stack
    run_backup
    run_sysinfo
    ;;
  *) usage; exit 1 ;;
 esac
