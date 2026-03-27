#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
UNDO_ROOT="${REPO_ROOT}/.copilot-undo/chunks"

dry_run="false"

usage() {
  cat <<'EOF'
Usage:
  chunk_restore.sh [--dry-run] <chunk_id_or_path>

Description:
  Restores files from a checkpoint chunk created by chunk_checkpoint.sh.
  - EXISTED files are restored from backup.
  - MISSING files are removed if they currently exist.

Examples:
  chunk_restore.sh 20260309_143000__forge-routes
  chunk_restore.sh --dry-run 20260309_143000__forge-routes
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "${1:-}" == "--dry-run" ]]; then
  dry_run="true"
  shift
fi

if [[ "$#" -ne 1 ]]; then
  usage
  exit 1
fi

chunk_input="$1"

if [[ -d "${chunk_input}" ]]; then
  chunk_dir="${chunk_input}"
else
  chunk_dir="${UNDO_ROOT}/${chunk_input}"
fi

if [[ ! -d "${chunk_dir}" ]]; then
  echo "ERROR: Chunk not found: ${chunk_input}" >&2
  echo "Available chunks:" >&2
  ls -1 "${UNDO_ROOT}" 2>/dev/null || true
  exit 2
fi

manifest_path="${chunk_dir}/manifest.tsv"
files_dir="${chunk_dir}/files"

if [[ ! -f "${manifest_path}" ]]; then
  echo "ERROR: Invalid chunk (missing manifest): ${chunk_dir}" >&2
  exit 2
fi

echo "Restoring chunk: ${chunk_dir}"
echo "Dry run: ${dry_run}"

while IFS=$'\t' read -r state rel_path; do
  [[ -z "${state}" ]] && continue
  target="${REPO_ROOT}/${rel_path}"

  if [[ "${state}" == "EXISTED" ]]; then
    source_file="${files_dir}/${rel_path}"
    if [[ ! -f "${source_file}" ]]; then
      echo "WARN: Missing backup for ${rel_path}; skipping"
      continue
    fi
    echo "RESTORE ${rel_path}"
    if [[ "${dry_run}" != "true" ]]; then
      mkdir -p "$(dirname "${target}")"
      cp -p "${source_file}" "${target}"
    fi
  elif [[ "${state}" == "MISSING" ]]; then
    if [[ -e "${target}" ]]; then
      echo "DELETE  ${rel_path}"
      if [[ "${dry_run}" != "true" ]]; then
        rm -f "${target}"
      fi
    else
      echo "SKIP    ${rel_path} (already absent)"
    fi
  else
    echo "WARN: Unknown manifest state '${state}' for ${rel_path}; skipping"
  fi
done < "${manifest_path}"

echo "Done."
