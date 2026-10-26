#!/bin/bash
# Pre-push check (DO_NOT_PUSH). Checks everything a push of HEAD to origin/main would send:
#   1. the tree of every unpushed commit (git rev-list origin/main..HEAD), plus the current tracked files;
#   2. the message of every unpushed commit.
# Pattern: '^\s*HIT[[:space:]]+index|^\s*phrase[[:space:]]*:'. Allowed matches, by content: the planted
# self-test pair, "HIT   index 2270828" and "phrase : tiger live melody ..." on the line directly after it,
# in README.md and REPORT.md. Any other match, in any tree or any message, blocks.
# If origin/main cannot be resolved: BLOCK, never a fall-back to the current tree only.
# A match's text is never printed (it could be a real phrase): only commit, file, line and kind.
# Exit 0 PASS, 1 BLOCK.
cd "$(dirname "$0")" || exit 1
PAT='^\s*HIT[[:space:]]+index|^\s*phrase[[:space:]]*:'
base=$(git rev-parse --verify -q 'origin/main^{commit}') || { echo "BLOCK: origin/main cannot be resolved"; exit 1; }
commits=$(git rev-list "$base..HEAD") || { echo "BLOCK: git rev-list $base..HEAD failed"; exit 1; }
ncommits=$(printf '%s\n' $commits | grep -c .)

# every line below is <where>:<file>:<line>:<text>; a git error becomes a line that blocks
{
  git grep -n -E "$PAT" | sed 's/^/worktree:/'; [ "${PIPESTATUS[0]}" -gt 1 ] && echo "worktree:(git grep failed):0:"
  for c in $commits; do
    git grep -n -E "$PAT" "$c"; rc=$?; [ $rc -gt 1 ] && echo "$c:(git grep failed):0:"
    git log -1 --format=%B "$c" | grep -n -E "$PAT" | sed "s/^/$c:(commit message):/"
  done
} | awk -v base="$base" -v ncommits="$ncommits" '
  { c = $0; sub(/:.*/, "", c); r = substr($0, length(c) + 2)
    f = r; sub(/:.*/, "", f); r = substr(r, length(f) + 2)
    n = r; sub(/:.*/, "", n); t = substr(r, length(n) + 2)
    doc = (f == "README.md" || f == "REPORT.md"); prev = c ":" f ":" (n - 1)
    if (doc && t ~ /^[ \t]*HIT[ \t]+index[ \t]+2270828[ \t]*$/) { hit[c ":" f ":" n] = 1; next }
    if (doc && t ~ /^[ \t]*phrase[ \t]*:[ \t]*tiger live melody / && (prev in hit)) { ok[prev] = 1; next }
    kind = (t ~ /^[ \t]*HIT/) ? "HIT line" : (t ~ /^[ \t]*phrase/) ? "phrase line" : "error"
    bad++; print "  not allowed: " (c == "worktree" ? c : substr(c, 1, 7)) "  " f ":" n "  (" kind ")" }
  END { for (k in hit) if (!(k in ok)) { split(k, a, ":"); bad++
          print "  not allowed: " (a[1] == "worktree" ? a[1] : substr(a[1], 1, 7)) "  " a[2] ":" a[3] "  (HIT line, no phrase line directly after)" }
        printf "%s: %d unpushed commit(s) after %s (trees and messages) + the current tracked files; %d disallowed match(es)\n",
               (bad ? "BLOCK" : "PASS"), ncommits, substr(base, 1, 7), bad
        exit bad ? 1 : 0 }'
