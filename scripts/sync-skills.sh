#!/usr/bin/env bash

# Safely synchronize the canonical skills library in both directions.
# Local changes are committed before remote integration; conflicts abort
# without stashing or dropping either side.

set -euo pipefail

script_dir="$(cd "$(dirname "$0")" && pwd -P)"
skills_dir="${SKILLS_DIR:-$(cd "$script_dir/.." && pwd -P)}"
user_home="$(dirname "$skills_dir")"
git_dir="$skills_dir/.git"
log_file="$git_dir/skills-sync.log"
lock_dir="$git_dir/skills-sync.lock"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S %z')" "$*" | tee -a "$log_file"
}

fail() {
  log "ERROR: $*"
  exit 1
}

if [ ! -d "$git_dir" ]; then
  printf 'ERROR: %s is not a Git repository\n' "$skills_dir" >&2
  exit 1
fi

if ! mkdir "$lock_dir" 2>/dev/null; then
  fail "another skills sync is already running"
fi
trap 'rmdir "$lock_dir" 2>/dev/null || true' EXIT INT TERM

cd "$skills_dir"

if [ "$(git branch --show-current)" != main ]; then
  fail "the canonical repository must be on main"
fi

for consumer in "$user_home/.agents/skills" "$user_home/.claude/skills" "$user_home/.codex/skills"; do
  if [ ! -L "$consumer" ]; then
    fail "$consumer is not a symbolic link to the canonical skills directory"
  fi
  if [ "$(cd "$consumer" && pwd -P)" != "$skills_dir" ]; then
    fail "$consumer does not resolve to $skills_dir"
  fi
done

git fetch --prune origin

# Guard the automatic upload path against common credential filenames,
# high-confidence secret formats, and unexpectedly large new files.
while IFS= read -r -d '' relative_path; do
  absolute_path="$skills_dir/$relative_path"
  lower_path="$(printf '%s' "$relative_path" | tr '[:upper:]' '[:lower:]')"

  case "$lower_path" in
    *.env|*.env.*|*credentials*|*private_key*|*private-key*|*id_rsa*|*id_ed25519*|*token.json)
      fail "refusing to upload suspicious path: $relative_path"
      ;;
  esac

  if [ -f "$absolute_path" ] && [ ! -L "$absolute_path" ]; then
    file_size="$(wc -c < "$absolute_path" | tr -d ' ')"
    if [ "$file_size" -gt 26214400 ]; then
      fail "refusing to upload file larger than 25 MiB: $relative_path"
    fi

    if LC_ALL=C grep -I -E -q '(-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|sk-[A-Za-z0-9]{32,})' "$absolute_path"; then
      fail "refusing to upload a probable secret in: $relative_path"
    fi
  fi
done < <(git ls-files --modified --others --exclude-standard -z)

git add -A

if ! git diff --cached --quiet; then
  sync_timestamp="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  git commit -m "chore: sync local skills $sync_timestamp"
fi

if ! git rebase origin/main; then
  git rebase --abort
  fail "remote changes conflict with local commits; both histories were preserved"
fi

if ! git push origin main; then
  log "push raced with a remote update; retrying once"
  git fetch --prune origin
  if ! git rebase origin/main; then
    git rebase --abort
    fail "remote changes conflict after the push retry; both histories were preserved"
  fi
  git push origin main || fail "push failed after one safe retry"
fi

git fetch --prune origin
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]; then
  fail "local and remote main do not match after synchronization"
fi

log "OK: local and remote main match at $(git rev-parse --short HEAD)"
