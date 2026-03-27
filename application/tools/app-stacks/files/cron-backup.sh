#!/usr/bin/env bash
set -euo pipefail

# Minimal backup script for the new application only.
# - Archives everything under application/, excluding patterns in backup_excludes.txt.
# - Writes archives to application/tools/app-stacks/backups.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="${APP_ROOT_OVERRIDE:-$(cd "${SCRIPT_DIR}/../../.." && pwd)}"
WORKSPACE_ROOT="${WORKSPACE_ROOT_OVERRIDE:-$(cd "${APP_ROOT}/.." && pwd)}"
BACKUP_DIR="${BACKUP_DIR_OVERRIDE:-${APP_ROOT}/tools/app-stacks/backups}"
INCLUDES_FILE="${INCLUDES_FILE_OVERRIDE:-${SCRIPT_DIR}/backup_includes.txt}"
EXCLUDES_FILE="${EXCLUDES_FILE_OVERRIDE:-${SCRIPT_DIR}/backup_excludes.txt}"
FILE_PREFIX="${FILE_PREFIX:-application}"
TS="$(date +"%a-%d-%B-%Y-%I-%M-%p" | tr '[:lower:]' '[:upper:]')"
ARCHIVE_PATH="${BACKUP_DIR}/${FILE_PREFIX}-backup_${TS}.tar.gz"

log() { echo "$(date +'%F %T') | $*"; }

[[ -d "${APP_ROOT}" ]] || { echo "Application root not found: ${APP_ROOT}" >&2; exit 1; }
[[ -d "${WORKSPACE_ROOT}" ]] || { echo "Workspace root not found: ${WORKSPACE_ROOT}" >&2; exit 1; }
[[ -f "${INCLUDES_FILE}" ]] || { echo "Includes file missing: ${INCLUDES_FILE}" >&2; exit 1; }
[[ -f "${EXCLUDES_FILE}" ]] || { echo "Excludes file missing: ${EXCLUDES_FILE}" >&2; exit 1; }

mkdir -p "${BACKUP_DIR}"

log "INFO: Starting backup from workspace root ${WORKSPACE_ROOT}"
log "INFO: Writing archive to ${ARCHIVE_PATH}"

# Create archive relative to WORKSPACE_ROOT so include/exclude paths are stable.
(
  cd "${WORKSPACE_ROOT}" &&
  tar -czf "${ARCHIVE_PATH}" --exclude-from "${EXCLUDES_FILE}" --files-from "${INCLUDES_FILE}" \
    2> >(grep -v "tar: Removing leading" >&2)
)

[[ -f "${ARCHIVE_PATH}" ]] && log "SUCCESS: Backup complete" || { log "ERROR: Archive missing after tar run"; exit 1; }

BYTES=$(stat -c%s "${ARCHIVE_PATH}" 2>/dev/null || stat -f%z "${ARCHIVE_PATH}" 2>/dev/null || echo 0)
log "INFO: Archive size: ${BYTES} bytes"
