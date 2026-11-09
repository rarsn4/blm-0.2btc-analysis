#!/bin/bash
# Sync the solver's config copies to the published ones, COMMENTS ONLY.
#
# The published set under blm-analysis/configs/ is what tally2.py parses; the solver
# directory's copies are what the runs parse. On 9 Nov 2026 the published copies gained
# [MODEL CORRECTED] notes on 36 configs, so the two sets diverged in comments.
#
# SAFETY, in order:
#   1. config_sync_check.py must report ZERO substance divergence before anything is
#      copied. Substance is every SLOT, POOL, PATH, WORDS and TARGET line. If the two
#      sets disagree there, the ledger describes a different box than the one that ran
#      -- REPORT 1.8's shape at the config level -- and this script refuses to paper
#      over it by copying.
#   2. Each file is written to a temp file in the DESTINATION directory and moved into
#      place with mv, which is an atomic rename on one filesystem. A solver reading a
#      config during the swap sees the whole old file or the whole new one, never a
#      partial one.
#   3. Nothing keys on config bytes: verified 9 Nov 2026 that neither run_queue_nov.sh
#      nor selftest_gate.sh hashes a config (the only sha256 is of the BINARY), and the
#      queue's identity check is on survivor counts. So a comment-only change cannot
#      alter a box, a band, a checkpoint or a gate.
# It is therefore safe to run with a solver mid-run, which matters because the queue is
# chained -- nine configs follow t21_free4 back to back, so there is no idle window for
# about thirteen days, and until the sync the runs read the UNMARKED configs while the
# ledger carries the marked ones.
set -u
cd "$(dirname "$0")" || exit 1
PUB=configs
SOL='/home/soul/Downloads/Brainwallet/files(6)'

python3 -I config_sync_check.py >/dev/null 2>&1 || {
  echo "BLOCK: config_sync_check.py reports substance divergence. Nothing copied."
  python3 -I config_sync_check.py | sed -n '/SUBSTANCE DIVERGENCE/,$p'
  exit 1
}
echo "gate: 0 substance divergences -- comment-only sync is safe"

# REVERSIBILITY. Before any file is replaced, every config this script would touch is
# archived as it currently stands. The sync is then undoable with one tar -x, without
# needing git, and the archive names the date so repeated runs do not clobber it.
BK="$SOL/configs_presync_$(date -u '+%Y%m%dT%H%M%SZ').tar"
list=$(mktemp) || exit 1
trap 'rm -f "$list"' EXIT
for p in "$PUB"/*.conf; do
  f=$(basename "$p")
  [ -f "$SOL/$f" ] && ! cmp -s "$p" "$SOL/$f" && echo "$f" >> "$list"
done
if [ ! -s "$list" ]; then echo "nothing to sync: already identical"; exit 0; fi
tar -c -f "$BK" -C "$SOL" -T "$list" || { echo "BLOCK: backup failed, nothing copied"; exit 1; }
echo "backup: $(wc -l < "$list") file(s) archived to $BK"
tar -t -f "$BK" >/dev/null || { echo "BLOCK: backup unreadable, nothing copied"; exit 1; }
echo "backup verified readable; restore with: tar -x -f $BK -C $SOL"

n=0
for p in "$PUB"/*.conf; do
  f=$(basename "$p"); s="$SOL/$f"
  [ -f "$s" ] || continue
  cmp -s "$p" "$s" && continue
  t=$(mktemp "$SOL/.sync.$f.XXXXXX") || { echo "BLOCK: cannot stage in $SOL"; exit 1; }
  cat "$p" > "$t" && chmod --reference="$s" "$t" 2>/dev/null
  mv -f "$t" "$s" || { echo "BLOCK: atomic move failed for $f"; rm -f "$t"; exit 1; }
  n=$((n + 1))
done
echo "synced $n config(s) published -> solver"

python3 -I config_sync_check.py | sed -n '1,7p'
