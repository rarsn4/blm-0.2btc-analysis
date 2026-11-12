#!/usr/bin/env bash
# AAI-1. Reproducibility check for a generator that writes untracked output.
#
# The defect this exists to prevent (REPORT 1.21): running the generator in place and then
# diffing before against after makes "identical" the result of the generator writing NOTHING.
# A crash satisfies the pass condition, and the stale bytes are destroyed in the same stroke.
#
# This moves the output aside first and regenerates into an EMPTY directory, so
#   - the previous bytes survive for comparison and for forensics, and
#   - a generator that does not run leaves an empty directory, which cannot read as identical.
#
# usage: ./regen_check.sh <output-dir> <generator ...>
#   e.g. ./regen_check.sh census_crops python3 census_crops.py
set -u
die() { echo "regen_check: $*" >&2; exit 2; }
[ $# -ge 2 ] || die "usage: ./regen_check.sh <output-dir> <generator ...>"
OUT="${1%/}"; shift
[ -d "$OUT" ] || die "no such directory: $OUT"
PREV=".regen_prev/$(basename "$OUT")-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$(dirname "$PREV")" || die "cannot create .regen_prev"
mv "$OUT" "$PREV" || die "cannot move $OUT aside"
mkdir -p "$OUT"
echo "regen_check: previous output preserved in $PREV"
echo "regen_check: running: $*"
"$@" > /dev/null; rc=$?
n_new=$(find "$OUT" -type f | wc -l); n_old=$(find "$PREV" -type f | wc -l)
echo "regen_check: generator exit=$rc;  files before $n_old, after $n_new"
[ "$rc" -eq 0 ] || die "generator FAILED (exit $rc). No comparison is reported. $OUT is left as produced."
[ "$n_new" -gt 0 ] || die "generator produced NO files. A comparison here would be vacuous."
same=0; diff_f=0; missing=0; extra=0
while IFS= read -r f; do
  rel="${f#$PREV/}"
  if [ -f "$OUT/$rel" ]; then
    if cmp -s "$f" "$OUT/$rel"; then same=$((same+1)); else
      diff_f=$((diff_f+1)); echo "  DIFFERS: $rel  (was $(sha256sum "$f" | cut -c1-16)…)"
    fi
  else missing=$((missing+1)); echo "  NOT REGENERATED: $rel"; fi
done < <(find "$PREV" -type f | sort)
while IFS= read -r f; do
  rel="${f#$OUT/}"; [ -f "$PREV/$rel" ] || { extra=$((extra+1)); echo "  NEW: $rel"; }
done < <(find "$OUT" -type f | sort)
echo "regen_check: identical $same, differing $diff_f, not regenerated $missing, new $extra"
if [ "$diff_f" -eq 0 ] && [ "$missing" -eq 0 ] && [ "$extra" -eq 0 ]; then
  echo "regen_check: PASS — every file reproduced byte-for-byte, over $same file(s)"; exit 0
fi
echo "regen_check: FAIL — the previous bytes are kept in $PREV for comparison"; exit 1
