#!/usr/bin/env bash
set -euo pipefail

# Safe Celery queue maintenance helper for ArtLomo.
#
# Modes:
#   status       Show queue/backlog health only (default)
#   purge-ready  Purge ready messages from queue using Celery purge command
#   purge-hard   Stop worker, archive queue+unacked keys, restart worker
#
# Examples:
#   ./application/tools/celery_queue_maintenance.sh status
#   ./application/tools/celery_queue_maintenance.sh purge-ready --yes
#   ./application/tools/celery_queue_maintenance.sh purge-hard --yes

MODE="status"
ASSUME_YES="0"
REDIS_DB="0"
QUEUE_NAME="celery"
WORKER_SERVICE="artlomo-celery"
CELERY_APP="application.mockups.tasks_mockup_generator.celery"
BACKUP_TTL_SECONDS="86400"

while [[ $# -gt 0 ]]; do
  case "$1" in
    status|purge-ready|purge-hard)
      MODE="$1"
      shift
      ;;
    --yes|-y)
      ASSUME_YES="1"
      shift
      ;;
    --redis-db)
      REDIS_DB="${2:-0}"
      shift 2
      ;;
    --queue)
      QUEUE_NAME="${2:-celery}"
      shift 2
      ;;
    --worker-service)
      WORKER_SERVICE="${2:-artlomo-celery}"
      shift 2
      ;;
    --help|-h)
      sed -n '1,40p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing command: $1" >&2
    exit 2
  }
}

require_cmd redis-cli
require_cmd celery
require_cmd sudo

worker_state() {
  sudo systemctl is-active "$WORKER_SERVICE" 2>/dev/null || true
}

queue_len() {
  redis-cli -n "$REDIS_DB" LLEN "$QUEUE_NAME" | tr -d '\r'
}

count_unacked_keys() {
  redis-cli -n "$REDIS_DB" --raw KEYS '*unacked*' | sed '/^$/d' | wc -l | awk '{print $1}'
}

list_unacked_keys() {
  redis-cli -n "$REDIS_DB" --raw KEYS '*unacked*' | sed '/^$/d'
}

show_status() {
  local state qlen unacked_count
  state="$(worker_state)"
  qlen="$(queue_len)"
  unacked_count="$(count_unacked_keys)"

  echo "Celery Queue Status"
  echo "- worker service: ${WORKER_SERVICE} (${state:-unknown})"
  echo "- redis db: ${REDIS_DB}"
  echo "- queue: ${QUEUE_NAME}"
  echo "- ready queue length: ${qlen}"
  echo "- unacked key count: ${unacked_count}"

  if [[ "$unacked_count" != "0" ]]; then
    echo "- unacked keys:"
    list_unacked_keys | sed 's/^/  * /'
  fi
}

confirm_or_exit() {
  local prompt="$1"
  if [[ "$ASSUME_YES" == "1" ]]; then
    return 0
  fi
  read -r -p "$prompt [y/N]: " ans
  case "$ans" in
    y|Y|yes|YES) return 0 ;;
    *)
      echo "Aborted."
      exit 1
      ;;
  esac
}

purge_ready() {
  local before after
  before="$(queue_len)"
  echo "Ready queue before purge: ${before}"

  if [[ "$before" == "0" ]]; then
    echo "Queue already empty; nothing to purge."
    return 0
  fi

  confirm_or_exit "Purge ready messages from queue '${QUEUE_NAME}' on Redis DB ${REDIS_DB}?"
  celery -A "$CELERY_APP" purge -Q "$QUEUE_NAME" -f >/dev/null

  after="$(queue_len)"
  echo "Ready queue after purge: ${after}"
}

archive_key() {
  local key="$1"
  local ts backup
  ts="$(date +%Y%m%d_%H%M%S)"
  backup="backup:${QUEUE_NAME}:${ts}:${key}"

  if [[ "$(redis-cli -n "$REDIS_DB" EXISTS "$key" | tr -d '\r')" == "0" ]]; then
    return 0
  fi

  redis-cli -n "$REDIS_DB" RENAME "$key" "$backup" >/dev/null
  redis-cli -n "$REDIS_DB" EXPIRE "$backup" "$BACKUP_TTL_SECONDS" >/dev/null
  echo "Archived key '${key}' -> '${backup}' (ttl=${BACKUP_TTL_SECONDS}s)"
}

purge_hard() {
  show_status
  confirm_or_exit "Run HARD purge (stop worker, archive queue/unacked keys, restart worker)?"

  echo "Stopping worker service ${WORKER_SERVICE}..."
  sudo systemctl stop "$WORKER_SERVICE"

  echo "Archiving queue key..."
  archive_key "$QUEUE_NAME"

  echo "Archiving unacked keys..."
  while IFS= read -r key; do
    [[ -z "$key" ]] && continue
    archive_key "$key"
  done < <(list_unacked_keys)

  echo "Starting worker service ${WORKER_SERVICE}..."
  sudo systemctl start "$WORKER_SERVICE"

  show_status
}

case "$MODE" in
  status)
    show_status
    ;;
  purge-ready)
    show_status
    purge_ready
    ;;
  purge-hard)
    purge_hard
    ;;
  *)
    echo "Unsupported mode: $MODE" >&2
    exit 2
    ;;
esac
