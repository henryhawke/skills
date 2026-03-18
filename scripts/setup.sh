#!/usr/bin/env bash
# setup.sh — Installs a cron job that syncs the skills repo at 7 AM and 7 PM daily.
#
# Usage:
#   ./scripts/setup.sh           # Install the cron job
#   ./scripts/setup.sh --remove  # Remove the cron job

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SYNC_SCRIPT="$SCRIPT_DIR/sync-skills.sh"
CRON_TAG="# skills-repo-sync"

# Ensure sync script is executable
chmod +x "$SYNC_SCRIPT"

if [ "${1:-}" = "--remove" ]; then
  crontab -l 2>/dev/null | grep -v "$CRON_TAG" | crontab -
  echo "Removed skills sync cron job."
  exit 0
fi

# Build the cron lines
CRON_AM="0 7 * * * $SYNC_SCRIPT $CRON_TAG"
CRON_PM="0 19 * * * $SYNC_SCRIPT $CRON_TAG"

# Check if already installed
if crontab -l 2>/dev/null | grep -q "$CRON_TAG"; then
  echo "Cron job already installed. Updating..."
  crontab -l 2>/dev/null | grep -v "$CRON_TAG" | crontab -
fi

# Append new cron lines
(crontab -l 2>/dev/null; echo "$CRON_AM"; echo "$CRON_PM") | crontab -

echo "Skills sync cron job installed:"
echo "  7:00 AM — pull latest skills"
echo "  7:00 PM — pull latest skills"
echo ""
echo "Logs: $SCRIPT_DIR/.sync.log"
echo "Remove: $SCRIPT_DIR/setup.sh --remove"
