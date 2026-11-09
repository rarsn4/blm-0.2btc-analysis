#!/bin/bash
# POSITIVE CONTROL for the shape arm of the log-reading rule (DO_NOT_PUSH).
#
# The rule's detection has two arms and only one of them had a control:
#   wording arm  grep -c -i -w -E 'hit|hits|commit=|phrase[[:space:]]*:'
#                controlled by st_selftest_find/uncomp/hybrid.log, 2 matches each
#   shape arm    grep -c -E '[0-9a-fA-F]{64}|[0-9a-fA-F]{40}|\b[5KL][1-9A-HJ-NP-Za-km-z]{50,51}\b|xprv|xpub'
#                UNCONTROLLED until this script: measured 2026-11-09 over 101 logs,
#                not one contained a hex64, a WIF or an extended key, so three of its
#                five alternatives had never fired and could not be shown to fire.
#
# This script manufactures the artifact deliberately. brain_image_corpus.py
# --selftest-plant replaces the target with the planted string's own hash160, so the
# real hit branch emits a real commit=<sha256> -- the first hex64 in any log here. The
# commitment is to the literal string "blm-corpus-planted-selftest" and says nothing
# about the puzzle.
#
# Four assertions, in order of what they are worth:
#   1  the control produces exactly one hit (the branch is reachable at all)
#   2  the SHAPE arm returns nonzero on the log it wrote (the arm fires on a hex64)
#   3  the log is gitignored and untracked (it cannot be committed by a plain git add)
#   4  pre_push_check.sh still PASSes with that file sitting on disk
# Assertion 4 is the prize: it tests the gate against a file containing exactly the
# thing the gate exists to stop.
set -u
cd "$(dirname "$0")" || exit 1
LOG=st_shapearm_control.log          # *.log ONLY. .txt/.out/.md are NOT ignored.
SHAPE='[0-9a-fA-F]{64}|[0-9a-fA-F]{40}|\b[5KL][1-9A-HJ-NP-Za-km-z]{50,51}\b|xprv|xpub'
WORD='hit|hits|commit=|phrase[[:space:]]*:'
fail=0
say(){ printf '  %-6s %s\n' "$1" "$2"; [ "$1" = FAIL ] && fail=1; return 0; }

case "$LOG" in *.log) ;; *) echo "BLOCK: capture path is not a *.log"; exit 1;; esac

python3 -I brain_image_corpus.py --selftest-plant > "$LOG" 2>&1
rc=$?
echo "shape-arm positive control -- $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
[ "$rc" -eq 0 ] && say PASS "1  control exits 0: exactly one planted hit" \
                || say FAIL "1  control exited $rc: the hit branch did not fire"

ns=$(grep -c -E "$SHAPE" "$LOG"); nw=$(grep -c -i -w -E "$WORD" "$LOG")
n64=$(grep -c -E '[0-9a-fA-F]{64}' "$LOG")
[ "$ns" -gt 0 ] && say PASS "2  shape arm fires: $ns line(s), of which hex64 $n64" \
                || say FAIL "2  shape arm returned 0 on a log containing commit=<sha256>"
[ "$nw" -gt 0 ] && say PASS "   wording arm also fires: $nw line(s)" \
                || say FAIL "   wording arm returned 0"

git check-ignore -q "$LOG" && say PASS "3  $LOG is gitignored" \
                           || say FAIL "3  $LOG is NOT ignored -- a plain git add would commit it"
git ls-files --error-unmatch "$LOG" >/dev/null 2>&1 \
  && say FAIL "   $LOG is TRACKED" || say PASS "   $LOG is untracked"

# "Untracked now" is not "never committed": a file can be absent from the index today and
# sitting in a commit from an hour ago, which a push would still carry. So check every
# unpushed commit's TREE as well, not just the current index.
base=$(git rev-parse --verify -q 'origin/main^{commit}')
if [ -z "$base" ]; then
  say FAIL "   origin/main cannot be resolved -- cannot check unpushed trees"
else
  ntrees=0
  for c in $(git rev-list "$base..HEAD"); do
    git ls-tree -r --name-only "$c" | grep -qx "$LOG" && ntrees=$((ntrees + 1))
  done
  nhist=$(git log --oneline --all -- "$LOG" | wc -l)
  [ "$ntrees" -eq 0 ] \
    && say PASS "   absent from all $(git rev-list --count "$base..HEAD") unpushed commit tree(s)" \
    || say FAIL "   present in $ntrees unpushed commit tree(s) -- a push would carry it"
  [ "$nhist" -eq 0 ] \
    && say PASS "   and never committed on any ref" \
    || say FAIL "   has $nhist commit(s) touching it somewhere in history"
fi

./pre_push_check.sh >/dev/null 2>&1
g=$?
[ "$g" -eq 0 ] && say PASS "4  pre_push_check.sh PASSes with the file on disk" \
               || say FAIL "4  pre_push_check.sh exited $g with the file on disk"

# 5 is the assertion that found REPORT 1.10, and the only one that tests the gate in the
# direction that matters. Assertion 4 passing proves the gate does not false-alarm, but it
# passes because the gate never looks at ignored files -- it would pass just as happily
# with a broken pattern. So force the file INTO the index and require a BLOCK. Without
# this, the control is the thing section 10 warns about: a check that passes either way.
trap 'git rm --cached -q st_shapearm_control.log 2>/dev/null' EXIT
git add -f "$LOG" 2>/dev/null
./pre_push_check.sh >/dev/null 2>&1
g2=$?
git rm --cached -q "$LOG" 2>/dev/null
[ "$g2" -ne 0 ] && say PASS "5  gate BLOCKs when the same file is force-added (git add -f)" \
                || say FAIL "5  gate PASSED a TRACKED file containing a real hit -- the pattern is blind"

[ "$fail" -eq 0 ] && echo "  ALL PASS -- the shape arm has a positive control" \
                  || echo "  CONTROL FAILED -- the shape arm is not controlled"
exit "$fail"
