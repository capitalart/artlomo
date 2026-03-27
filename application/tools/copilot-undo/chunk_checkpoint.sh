#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
UNDO_ROOT="${REPO_ROOT}/.copilot-undo/chunks"

usage() {
  cat <<'EOF'
Usage:
  chunk_checkpoint.sh <chunk_name> <file1> [file2 ...]

Description:
  Creates a named checkpoint chunk for the listed files before making edits.
  Each chunk stores file backups plus a manifest that can be restored later.

Examples:
  chunk_checkpoint.sh forge-routes application/mockups/admin/routes/forge_routes.py
  chunk_checkpoint.sh ui-pass \
    application/mockups/admin/ui/templates/mockups/forge.html \
    application/mockups/admin/ui/static/css/forge.css
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "$#" -lt 2 ]]; then
  usage
  exit 1
fi

chunk_name="$1"
shift

safe_name="${chunk_name//[^a-zA-Z0-9._-]/_}"
timestamp="$(date +"%Y%m%d_%H%M%S")"
chunk_dir="${UNDO_ROOT}/${timestamp}__${safe_name}"
files_dir="${chunk_dir}/files"
manifest_path="${chunk_dir}/manifest.tsv"
meta_path="${chunk_dir}/meta.env"

mkdir -p "${files_dir}"

current_head="$(git -C "${REPO_ROOT}" rev-parse --short HEAD 2>/dev/null || echo "NO_GIT")"
{
  printf 'CHUNK_NAME=%s\n' "${chunk_name}"
  printf 'CREATED_AT=%s\n' "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  printf 'REPO_ROOT=%s\n' "${REPO_ROOT}"
  printf 'GIT_HEAD=%s\n' "${current_head}"
} > "${meta_path}"

: > "${manifest_path}"

for rel_path in "$@"; do
  if [[ "${rel_path}" == /* ]]; then
    abs_path="${rel_path}"
    case "${abs_path}" in
      "${REPO_ROOT}"/*) rel_path="${abs_path#"${REPO_ROOT}/"}" ;;
      *)
        echo "ERROR: Path outside repo is not allowed: ${abs_path}" >&2
        exit 2
        ;;
    esac
  fi

  abs_path="${REPO_ROOT}/${rel_path}"
  if [[ -d "${abs_path}" ]]; then
    echo "ERROR: Directories are not allowed in checkpoint list: ${rel_path}" >&2
    exit 2
  fi

  if [[ -f "${abs_path}" ]]; then
    mkdir -p "${files_dir}/$(dirname "${rel_path}")"
    cp -p "${abs_path}" "${files_dir}/${rel_path}"
    printf 'EXISTED\t%s\n' "${rel_path}" >> "${manifest_path}"
    echo "Checkpointed: ${rel_path}"
  else
    printf 'MISSING\t%s\n' "${rel_path}" >> "${manifest_path}"
    echo "Marked missing (will be deleted on restore if created): ${rel_path}"
  fi
done

echo ""
echo "Chunk created: ${chunk_dir}"
echo "Restore with: ${SCRIPT_DIR}/chunk_restore.sh ${timestamp}__${safe_name}"
