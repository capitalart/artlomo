#!/usr/bin/env bash
set -euo pipefail

# System and environment inventory collector for ArtLomo
# Gathers OS, runtime, packages, GCP metadata, and resource information

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="${APP_ROOT_OVERRIDE:-$(cd "${SCRIPT_DIR}/../../.." && pwd)}"
WORKSPACE_ROOT="${WORKSPACE_ROOT_OVERRIDE:-$(cd "${APP_ROOT}/.." && pwd)}"
STACK_DIR="${STACK_DIR_OVERRIDE:-${APP_ROOT}/tools/app-stacks/stacks}"
FILE_PREFIX="${FILE_PREFIX:-application}"
TS="$(date +"%a-%d-%B-%Y-%I-%M-%p" | tr '[:lower:]' '[:upper:]')"
OUT_FILE="${STACK_DIR}/${FILE_PREFIX}-system-inventory-${TS}.md"

log() { echo "$(date +'%F %T') | $*"; }

[[ -d "${STACK_DIR}" ]] || mkdir -p "${STACK_DIR}"

exec > "${OUT_FILE}"

cat <<'HEADER'
# ArtLomo System Inventory Report

This report was auto-generated and captures the complete system environment.

HEADER

echo "**Report Date:** $(date +'%Y-%m-%d %H:%M:%S %Z')"
echo "**Hostname:** $(hostname)"
echo ""
echo "---"
echo ""

# ============================================================================
# SECTION 1: Operating System and Kernel
# ============================================================================
echo "## 1. Operating System and Kernel"
echo ""
echo "### Host Information"
echo ""
echo '```text'
uname -a
echo '```'
echo ""

if [[ -f /etc/os-release ]]; then
  echo "### OS Release"
  echo ""
  echo '```text'
  cat /etc/os-release
  echo '```'
  echo ""
fi

echo "### Uptime and Load"
echo ""
echo '```text'
uptime
echo '```'
echo ""

# ============================================================================
# SECTION 2: Python Environment
# ============================================================================
echo "## 2. Python Environment"
echo ""

if command -v python3 &>/dev/null; then
  echo "### Python Version"
  echo ""
  echo '```text'
  python3 --version
  echo '```'
  echo ""
fi

if [[ -f "${WORKSPACE_ROOT}/requirements.txt" ]]; then
  echo "### Requirements File"
  echo ""
  echo '```text'
  head -100 "${WORKSPACE_ROOT}/requirements.txt"
  echo '```'
  echo ""
fi

if [[ -f "${WORKSPACE_ROOT}/.venv/bin/activate" ]]; then
  echo "### Installed Python Packages (pip list)"
  echo ""
  echo '```text'
  source "${WORKSPACE_ROOT}/.venv/bin/activate" 2>/dev/null && pip list || echo "Failed to activate venv"
  echo '```'
  echo ""
fi

# ============================================================================
# SECTION 3: Node.js Environment
# ============================================================================
echo "## 3. Node.js Environment"
echo ""

if command -v node &>/dev/null; then
  echo "### Node Version"
  echo ""
  echo '```text'
  node --version
  echo '```'
  echo ""
fi

if command -v npm &>/dev/null; then
  echo "### npm Version"
  echo ""
  echo '```text'
  npm --version
  echo '```'
  echo ""
fi

if [[ -f "${WORKSPACE_ROOT}/video_worker/package.json" ]]; then
  echo "### Video Worker package.json"
  echo ""
  echo '```json'
  cat "${WORKSPACE_ROOT}/video_worker/package.json"
  echo '```'
  echo ""
fi

# ============================================================================
# SECTION 4: System Software
# ============================================================================
echo "## 4. System Software"
echo ""

if command -v ffmpeg &>/dev/null; then
  echo "### FFmpeg Version"
  echo ""
  echo '```text'
  ffmpeg -version 2>&1 | head -5
  echo '```'
  echo ""
fi

if command -v gunicorn &>/dev/null; then
  echo "### Gunicorn Version"
  echo ""
  echo '```text'
  gunicorn --version
  echo '```'
  echo ""
fi

# ============================================================================
# SECTION 5: Hardware and Resources
# ============================================================================
echo "## 5. Hardware and Resources"
echo ""

if command -v lscpu &>/dev/null; then
  echo "### CPU Information"
  echo ""
  echo '```text'
  lscpu
  echo '```'
  echo ""
fi

if command -v free &>/dev/null; then
  echo "### Memory Information"
  echo ""
  echo '```text'
  free -h
  echo '```'
  echo ""
fi

if command -v df &>/dev/null; then
  echo "### Disk Usage"
  echo ""
  echo '```text'
  df -hT
  echo '```'
  echo ""
fi

if command -v lsblk &>/dev/null; then
  echo "### Block Devices"
  echo ""
  echo '```text'
  lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,MODEL
  echo '```'
  echo ""
fi

# ============================================================================
# SECTION 6: Network Configuration
# ============================================================================
echo "## 6. Network Configuration"
echo ""

if command -v ip &>/dev/null; then
  echo "### Network Interfaces"
  echo ""
  echo '```text'
  ip -brief address
  echo '```'
  echo ""
  
  echo "### Routing Table"
  echo ""
  echo '```text'
  ip route
  echo '```'
  echo ""
fi

if [[ -f /etc/resolv.conf ]]; then
  echo "### DNS Configuration"
  echo ""
  echo '```text'
  cat /etc/resolv.conf | head -30
  echo '```'
  echo ""
fi

# ============================================================================
# SECTION 7: Google Cloud Metadata (if available)
# ============================================================================
echo "## 7. Google Cloud VM Metadata"
echo ""

if systemd-detect-virt 2>/dev/null | grep -qi google; then
  echo "### Virtualization"
  echo ""
  echo '```text'
  systemd-detect-virt
  echo '```'
  echo ""
  
  echo "### Instance Metadata"
  echo ""
  echo '```text'
  m() { curl -fsS -H 'Metadata-Flavor: Google' "http://metadata.google.internal/computeMetadata/v1/$1" 2>/dev/null || echo "N/A"; }
  echo "Instance Name:      $(m instance/name)"
  echo "Instance ID:        $(m instance/id)"
  echo "Project ID:         $(m project/project-id)"
  echo "Project Number:     $(m project/numeric-project-id)"
  echo "Zone:               $(m instance/zone | awk -F/ '{print $NF}')"
  echo "Machine Type:       $(m instance/machine-type | awk -F/ '{print $NF}')"
  echo "CPU Platform:       $(m instance/cpu-platform)"
  echo "Internal IP:        $(m instance/network-interfaces/0/ip)"
  echo "External IP:        $(m instance/network-interfaces/0/access-configs/0/external-ip)"
  echo "Automatic Restart:  $(m instance/scheduling/automatic-restart)"
  echo "Preemptible:        $(m instance/scheduling/preemptible)"
  echo "On Host Maint:      $(m instance/scheduling/on-host-maintenance)"
  echo '```'
  echo ""
else
  echo "_Not running on Google Cloud Platform_"
  echo ""
fi

# ============================================================================
# SECTION 8: Database Information
# ============================================================================
echo "## 8. Database Information"
echo ""

if [[ -f "${WORKSPACE_ROOT}/db.py" ]]; then
  echo "### Database Schema File"
  echo ""
  echo '```python'
  head -100 "${WORKSPACE_ROOT}/db.py"
  echo '```'
  echo ""
fi

# Check for SQLite database
if command -v sqlite3 &>/dev/null; then
  if [[ -f "${WORKSPACE_ROOT}/data/artlomo.sqlite3" ]]; then
    echo "### Database Tables"
    echo ""
    echo '```text'
    sqlite3 "${WORKSPACE_ROOT}/data/artlomo.sqlite3" ".tables" 2>/dev/null || echo "Could not read database"
    echo '```'
    echo ""
  elif [[ -f "${WORKSPACE_ROOT}/var/db/artlomo.sqlite3" ]]; then
    echo "### Database Tables"
    echo ""
    echo '```text'
    sqlite3 "${WORKSPACE_ROOT}/var/db/artlomo.sqlite3" ".tables" 2>/dev/null || echo "Could not read database"
    echo '```'
    echo ""
  fi
fi

# ============================================================================
# SECTION 9: Running Services
# ============================================================================
echo "## 9. Running Services"
echo ""

if command -v systemctl &>/dev/null; then
  echo "### Active Services (Flask/Gunicorn related)"
  echo ""
  echo '```text'
  systemctl list-units --type=service --state=running | grep -iE "(artlomo|gunicorn|flask|celery|redis)" || echo "No matching services found"
  echo '```'
  echo ""
fi

if command -v ps &>/dev/null; then
  echo "### Python Processes"
  echo ""
  echo '```text'
  ps aux | grep -i python | grep -v grep | head -20 || echo "No Python processes"
  echo '```'
  echo ""
fi

# ============================================================================
# SECTION 10: Environment Variables
# ============================================================================
echo "## 10. Environment Variables (filtered)"
echo ""
echo '```text'
env | grep -iE "(FLASK|ARTLOMO|PYTHON|NODE|PATH)" | sort
echo '```'
echo ""

echo "---"
echo ""
echo "**Report generated:** $(date +'%Y-%m-%d %H:%M:%S %Z')"
echo "**Output file:** ${OUT_FILE}"

log "SUCCESS: System inventory written to ${OUT_FILE}"
