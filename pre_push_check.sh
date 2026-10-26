#!/bin/bash
# Pre-push check (DO_NOT_PUSH). Allowed matches, by content: the planted self-test pair, "HIT   index 2270828"
# and "phrase : tiger live melody ..." on the line directly after it, in README.md and REPORT.md. Anything else: BLOCK.
cd "$(dirname "$0")" || exit 2
git grep -n -E '^\s*HIT[[:space:]]+index|^\s*phrase[[:space:]]*:' | awk '{ f = $0; sub(/:.*/, "", f); r = substr($0, length(f) + 2); n = r; sub(/:.*/, "", n); t = substr(r, length(n) + 2)
  if ((f == "README.md" || f == "REPORT.md") && t ~ /^[ \t]*HIT[ \t]+index[ \t]+2270828[ \t]*$/) hit[f ":" n] = 1; else if (t ~ /^[ \t]*phrase[ \t]*:[ \t]*tiger live melody / && (f ":" (n - 1)) in hit) ok[f ":" (n - 1)] = 1; else { bad++; print "  not allowed: " f ":" n } }
  END { for (k in hit) if (!ok[k]) { bad++; print "  not allowed: " k " (no phrase line directly after)" }; print (bad ? "BLOCK" : "PASS") ": " bad + 0 " disallowed match(es)"; exit bad ? 1 : 0 }'
