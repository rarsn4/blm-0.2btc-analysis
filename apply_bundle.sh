#!/usr/bin/env bash
# Verify this bundle, then copy it into a git checkout and stage it.
# Commits only when given --commit. Never pushes. Stops, copying nothing, if a
# file of the same name already exists in the repo with different content.
#
#   bash apply_bundle.sh /path/to/repo            # dry run: check, copy, stage
#   bash apply_bundle.sh /path/to/repo --commit   # the same, then commit
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="${1:?usage: bash apply_bundle.sh /path/to/repo [--commit]}"
mode="${2:-}"
[ -d "$repo/.git" ] || { echo "not a git checkout: $repo"; exit 1; }

echo "== verifying bundle"
( cd "$here" && sha256sum -c --quiet MANIFEST.sha256 ) || { echo "manifest check FAILED"; exit 1; }
echo "   all $(grep -c . "$here/MANIFEST.sha256") entries OK"

names=()
while read -r digest name; do names+=("$name"); done < "$here/MANIFEST.sha256"
names+=("MANIFEST.sha256")

echo "== checking for conflicts in $repo"
conflicts=0
for name in "${names[@]}"; do
  dest="$repo/$name"
  if [ -e "$dest" ] && ! cmp -s "$here/$name" "$dest"; then
    echo "   CONFLICT: $name already exists with different content"
    conflicts=1
  fi
done
[ "$conflicts" -eq 0 ] || { echo "stopping: nothing copied; resolve the conflicts first"; exit 1; }

echo "== copying ${#names[@]} files"
for name in "${names[@]}"; do
  mkdir -p "$repo/$(dirname "$name")"
  cp "$here/$name" "$repo/$name"
done

cd "$repo"
git add -- "${names[@]}"
echo "== staged:"
git status --short -- "${names[@]}"
if [ "$mode" = "--commit" ]; then
  git commit -m "Add image-measurement bundle: census, even-slot rules, R10 + erratum, set-C stop rule" -- "${names[@]}"
  echo "committed (not pushed)"
else
  echo "dry run: staged but not committed. Re-run with --commit to commit."
fi
