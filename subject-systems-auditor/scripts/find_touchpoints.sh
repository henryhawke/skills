#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  find_touchpoints.sh "<term1,term2,term3>" [search_root]

Examples:
  find_touchpoints.sh "payments,stripe,checkout" .
  find_touchpoints.sh "friend request,social graph" /path/to/repo

Description:
  Run a first-pass discovery for subject touchpoints using ripgrep.
  Output directory-level counts, matched files, and a line-level sample.
EOF
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

if ! command -v rg >/dev/null 2>&1; then
  echo "Error: rg (ripgrep) is required but not installed." >&2
  exit 2
fi

terms_input="$1"
search_root="${2:-.}"

if [[ ! -d "$search_root" ]]; then
  echo "Error: search_root is not a directory: $search_root" >&2
  exit 1
fi

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

escape_regex() {
  local value="$1"
  value="$(printf '%s' "$value" | sed -E 's/[][(){}.^$*+?|\\/]/\\&/g')"
  printf '%s' "$value"
}

IFS=',' read -r -a raw_terms <<<"$terms_input"
terms=()
for raw in "${raw_terms[@]}"; do
  term="$(trim "$raw")"
  if [[ -n "$term" ]]; then
    terms+=("$term")
  fi
done

if [[ ${#terms[@]} -eq 0 ]]; then
  echo "Error: no usable terms provided." >&2
  usage
  exit 1
fi

regex_parts=()
for term in "${terms[@]}"; do
  regex_parts+=("$(escape_regex "$term")")
done

regex="$(IFS='|'; echo "${regex_parts[*]}")"
root_abs="$(cd "$search_root" && pwd)"

ignore_globs=(
  --glob '!**/.git/**'
  --glob '!**/.hg/**'
  --glob '!**/.svn/**'
  --glob '!**/.DS_Store'
  --glob '!**/.taskmaster/**'
  --glob '!**/node_modules/**'
  --glob '!**/.venv/**'
  --glob '!**/dist/**'
  --glob '!**/build/**'
  --glob '!**/coverage/**'
  --glob '!**/.next/**'
  --glob '!**/.dart_tool/**'
  --glob '!**/.idea/**'
  --glob '!**/archive/**'
  --glob '!**/artifacts/**'
)

tmp_matches="$(mktemp)"
tmp_files="$(mktemp)"
trap 'rm -f "$tmp_matches" "$tmp_files"' EXIT

(
  cd "$root_abs"
  rg -n -i -S --no-heading "${ignore_globs[@]}" "$regex" . || true
) >"$tmp_matches"

echo "Subject terms: ${terms[*]}"
echo "Search root: $root_abs"
echo "Regex: $regex"
echo

if [[ ! -s "$tmp_matches" ]]; then
  echo "No touchpoints found."
  exit 0
fi

line_matches="$(wc -l <"$tmp_matches" | tr -d ' ')"
cut -d: -f1 "$tmp_matches" \
  | sed 's#^\./##' \
  | sort -u >"$tmp_files"
unique_files="$(wc -l <"$tmp_files" | tr -d ' ')"
max_files="${TOUCHPOINT_MAX_FILES:-200}"
if [[ ! "$max_files" =~ ^[0-9]+$ ]]; then
  max_files=200
fi

echo "Line matches: $line_matches"
echo "Unique files: $unique_files"
echo

echo "Matched files by top-level directory:"
cut -d: -f1 "$tmp_matches" \
  | sed 's#^\./##' \
  | awk -F/ '{print $1}' \
  | sort \
  | uniq -c \
  | sort -nr

echo
if (( unique_files > max_files )); then
  echo "Matched files (first $max_files of $unique_files):"
  head -n "$max_files" "$tmp_files"
  echo "... (set TOUCHPOINT_MAX_FILES to increase limit)"
else
  echo "Matched files:"
  cat "$tmp_files"
fi

echo
echo "First 120 line matches:"
head -n 120 "$tmp_matches"
