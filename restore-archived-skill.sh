#!/usr/bin/env bash
# Restore one skill from ~/skills-archive back into ~/skills
set -euo pipefail
name="${1:-}"
if [[ -z "$name" ]]; then
  echo "Usage: $0 <skill-folder-name>" >&2
  exit 1
fi
src="$HOME/skills-archive/$name"
dst="$HOME/skills/$name"
if [[ ! -d "$src" ]]; then
  echo "Not found in archive: $src" >&2
  exit 1
fi
if [[ -e "$dst" ]]; then
  echo "Already active: $dst" >&2
  exit 1
fi
mv "$src" "$dst"
echo "Restored $name"
