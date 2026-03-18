#!/usr/bin/env bash
# sync-skills.sh — Pulls latest skills from origin if there are remote changes.
# Designed to run via cron at 7 AM and 7 PM daily.

set -euo pipefail

SKILLS_DIR="${SKILLS_DIR:-$HOME/skills}"
LOG_FILE="${SKILLS_DIR}/scripts/.sync.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"; }

if [ ! -d "$SKILLS_DIR/.git" ]; then
  log "ERROR: $SKILLS_DIR is not a git repository"
  exit 1
fi

cd "$SKILLS_DIR"

# Fetch latest from origin
git fetch origin --quiet 2>/dev/null || { log "ERROR: git fetch failed"; exit 1; }

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master)

if [ "$LOCAL" = "$REMOTE" ]; then
  log "OK: already up to date ($LOCAL)"
else
  log "SYNC: pulling changes ($LOCAL -> $REMOTE)"
  git pull --ff-only origin main --quiet 2>/dev/null || {
    log "ERROR: git pull failed (local changes?). Attempting stash + pull."
    git stash --quiet
    git pull --ff-only origin main --quiet
    git stash pop --quiet 2>/dev/null || true
  }
  log "SYNC: complete (now at $(git rev-parse HEAD))"
fi
