#!/usr/bin/bash

set -euo pipefail

all=$(printf '%s\n' ./*/*.spec | cut -d/ -f2)

if [ -z "$BASE" ] || ! git cat-file -e "$BASE^{commit}" 2>/dev/null; then
  packages=$all
else
  changed=$(git diff --name-only "$BASE...$HEAD")
  if grep -qE "$REBUILD_ALL_PATTERN" <<<"$changed"; then
    packages=$all
  else
    packages=$(comm -12 <(cut -d/ -f1 <<<"$changed" | sort -u) <(sort <<<"$all"))
  fi
fi

echo "packages=$(jq -cnR '[inputs | select(length > 0)]' <<<"$packages")" >> "$GITHUB_OUTPUT"
