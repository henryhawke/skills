#!/usr/bin/env bash
# Restore missing tracked skills without overwriting edits or local-only skills.
set -euo pipefail

skills_root="${SKILLS_GUARD_ROOT:-/Users/henry/skills}"
guard_state="${SKILLS_GUARD_STATE_DIR:-/Users/henry/Library/Application Support/SkillsGuard}"
mirror_git="${SKILLS_GUARD_MIRROR:-$guard_state/skills.git}"
repo_gitdir="${SKILLS_REPO_GITDIR:-$guard_state/worktree.git}"
guard_log="$guard_state/guard.log"
guard_lock="$guard_state/.guard-lock"
stage_dir=""
skill_aliases=(
  "/Users/henry/.skills"
  "/Users/henry/.claude/skills"
  "/Users/henry/.codex/skills"
  "/Users/henry/.cursor/skills"
  "/Users/henry/.cursor/skills-cursor"
  "/Users/henry/.agents/skills"
)

mkdir -p "$guard_state"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$guard_log"
}

repair_aliases() {
  local alias_path current_target

  for alias_path in "${skill_aliases[@]}"; do
    if [[ -L "$alias_path" ]]; then
      current_target="$(readlink "$alias_path")"
      if [[ "$current_target" != "$skills_root" ]]; then
        ln -sfn "$skills_root" "$alias_path"
        log "REPAIRED: relinked $alias_path to $skills_root"
      fi
    elif [[ -e "$alias_path" ]]; then
      log "ERROR: refusing to replace non-symlink skills path at $alias_path"
    else
      mkdir -p "$(dirname "$alias_path")"
      ln -s "$skills_root" "$alias_path"
      log "REPAIRED: linked $alias_path to $skills_root"
    fi
  done
}

repair_git_link() {
  local git_link="$skills_root/.git"

  if [[ -d "$repo_gitdir" && ! -e "$git_link" && ! -L "$git_link" ]]; then
    printf 'gitdir: %s\n' "$repo_gitdir" > "$git_link"
    log "REPAIRED: restored external Git metadata link at $git_link"
  fi
}

sanitize_manifest() {
  local manifest="$1"
  local sanitized="${manifest}.tmp.$$"

  [[ -f "$manifest" ]] || return 0

  # A Git metadata directory is not a skill. Keeping it in the inventory lets
  # skill sync/prune treat the repository metadata as disposable content.
  awk '
    $0 == "    \".git\": {" { skip = 1; next }
    skip && $0 == "    }," { skip = 0; next }
    !skip { print }
  ' "$manifest" > "$sanitized"

  if cmp -s "$manifest" "$sanitized"; then
    rm -f "$sanitized"
  else
    mv "$sanitized" "$manifest"
    log "REPAIRED: removed .git from the skills inventory"
  fi
}

if ! mkdir "$guard_lock" 2>/dev/null; then
  exit 0
fi

cleanup() {
  if [[ -n "$stage_dir" && -d "$stage_dir" ]]; then
    rm -rf "$stage_dir"
  fi
  rmdir "$guard_lock" 2>/dev/null || true
}
trap cleanup EXIT

repair_aliases
repair_git_link
sanitize_manifest "$skills_root/.sync-manifest.json"

if ! git --git-dir="$mirror_git" rev-parse --verify HEAD >/dev/null 2>&1; then
  log "ERROR: recovery mirror is unavailable at $mirror_git"
  exit 1
fi

stage_dir="$(mktemp -d "$guard_state/stage.XXXXXX")"
git --git-dir="$mirror_git" archive HEAD | tar -x -C "$stage_dir"
mkdir -p "$skills_root"

missing_skills=0
for skill_manifest in "$stage_dir"/*/SKILL.md; do
  [[ -f "$skill_manifest" ]] || continue
  skill_name="$(basename "$(dirname "$skill_manifest")")"
  if [[ ! -f "$skills_root/$skill_name/SKILL.md" ]]; then
    missing_skills=$((missing_skills + 1))
  fi
done

missing_root_files=0
for root_file in .allowlist .gitignore .sync-manifest.json restore-archived-skill.sh; do
  if [[ -f "$stage_dir/$root_file" && ! -f "$skills_root/$root_file" ]]; then
    missing_root_files=$((missing_root_files + 1))
  fi
done

if (( missing_skills == 0 && missing_root_files == 0 )); then
  exit 0
fi

# --ignore-existing is the safety boundary: restore absence, preserve edits.
rsync -a --ignore-existing "$stage_dir/" "$skills_root/"

# A mass-prune event rewrites this inventory. Restore the pinned GitHub copy
# only while repairing missing skills so the bad inventory cannot persist.
if (( missing_skills > 0 )) && [[ -f "$stage_dir/.sync-manifest.json" ]]; then
  cp "$stage_dir/.sync-manifest.json" "$skills_root/.sync-manifest.json"
  sanitize_manifest "$skills_root/.sync-manifest.json"
fi

log "REPAIRED: restored $missing_skills missing skill directories and $missing_root_files root files"
