#!/bin/bash
#
# ArtLomo Backup Script
# =====================
# Creates timestamped compressed archives of the ArtLomo application.
# Excludes virtual environments, Python caches, and existing archives.
#
# USAGE:
#   ./backup_artlomo.sh
#   bash /srv/artlomo/application/tools/backup_artlomo.sh
#
# OUTPUT:
#   /srv/backups/artlomo-backup-DD-MMMM-YYYY-HH-MM.tar.gz
#
# EXCLUDES:
#   - .venv/ (virtual environments)
#   - __pycache__/ (Python bytecode)
#   - .pytest_cache/ (test cache)
#   - *.tar.gz, *.tar (prior archives)
#
# NOTES:
#   - Requires read access to /srv/artlomo
#   - Requires write access to /srv/backups
#   - Run with sudo if permission denied
#
set -Eeuo pipefail

SOURCE_DIR="/srv/artlomo"
BACKUP_DIR="/srv/backups"
TIMESTAMP="$(date +"%d-%B-%Y-%H-%M")"
BACKUP_FILE="artlomo-backup-${TIMESTAMP}.tar.gz"
DEST_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

echo "Starting ArtLomo backup..."
echo "Source: ${SOURCE_DIR}"
echo "Destination: ${DEST_PATH}"

mkdir -p "${BACKUP_DIR}"

# Archive /srv/artlomo while excluding virtual environments, caches, and prior archives.
tar -czf "${DEST_PATH}" \
  --exclude='artlomo/.venv' \
  --exclude='artlomo/.venv/*' \
  --exclude='*/__pycache__' \
  --exclude='*/__pycache__/*' \
  --exclude='*/.pytest_cache' \
  --exclude='*/.pytest_cache/*' \
  --exclude='*.tar.gz' \
  --exclude='*.tar' \
  -C /srv artlomo

echo "Backup complete: ${DEST_PATH}"
