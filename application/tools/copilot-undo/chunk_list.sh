#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
UNDO_ROOT="${REPO_ROOT}/.copilot-undo/chunks"

mkdir -p "${UNDO_ROOT}"

echo "Chunk checkpoints in ${UNDO_ROOT}:"

if [[ -z "$(ls -A "${UNDO_ROOT}" 2>/dev/null)" ]]; then
  echo "(none)"
  exit 0
fi

for chunk_dir in "${UNDO_ROOT}"/*; do
  [[ -d "${chunk_dir}" ]] || continue
  name="$(basename "${chunk_dir}")"
  manifest="${chunk_dir}/manifest.tsv"
  count="0"
  if [[ -f "${manifest}" ]]; then
    count="$(wc -l < "${manifest}" | tr -d ' ')"
  fi
  echo "- ${name} (${count} file entries)"
done
