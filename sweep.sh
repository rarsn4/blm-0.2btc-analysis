#!/bin/bash
# sweep.sh -- campaign inventory: config | space | checkpoint | pct | hit?
# Joins each log to its checkpoint via the --config name INSIDE the log, so it
# does not depend on logs being named after their config (pool75.log isn't).
#
# The HIT patterns below are a GUESS at the solver's success output. A "no"
# from an unverified pattern is worth nothing. Verify with:
#     grep -rn -A12 'show_hit' *.cu *.cpp *.h
#
ROOT="${1:-$HOME}"
ADDR='1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ'
HIT='HIT|FOUND KEY|SOLVED|MNEMONIC|PRIVKEY|WIF:|xprv'
NOISE='not found|no hit|expected derivations'
any=0

printf '%-24s %15s %15s %8s %5s\n' CONFIG SPACE CHECKPOINT PCT HIT
printf '%.0s-' {1..74}; echo

while IFS= read -r f; do
  t=$(tr -d '\r' < "$f")                       # progress writer emits \r
  sp=$(printf '%s\n' "$t" | grep -om1 'space=[0-9]\+' | cut -d= -f2)
  [ -z "$sp" ] && continue                     # not a solver log
  cf=$(printf '%s\n' "$t" | grep -om1 '\--config [A-Za-z0-9_.-]\+\.conf' | awk '{print $2}')
  cf=${cf:-unknown.conf}
  pf=$(find "$ROOT" -name "progress_${cf%.conf}.txt" 2>/dev/null | head -1)
  ck=$( [ -n "$pf" ] && tr -dc '0-9' < "$pf" || echo 0 )
  pct=$(awk -v a="$ck" -v b="$sp" 'BEGIN{printf "%.2f", b?100*a/b:0}')
  h=$(printf '%s\n' "$t" | grep -iE "$HIT" | grep -viE "$NOISE" | head -1)
  m=no; [ -n "$h" ] && { m=YES; any=1; }
  printf '%-24s %15s %15s %7s%% %5s\n' "${cf%.conf}" "$sp" "$ck" "$pct" "$m"
done < <(find "$ROOT" -type f -name '*.log' 2>/dev/null | sort)

echo
if [ "$any" = 1 ]; then
  echo '!!! CANDIDATE HIT -- do not act on it yet:'
  echo "  1. re-derive on the affine binary, EC_USE_JACOBIAN=0"
  echo "  2. re-derive on a separate BIP32 implementation"
  echo "  3. address must equal, character for character:"
  echo "     $ADDR"
  echo "  4. move the funds with a FRESH OFFLINE key before the phrase"
  echo "     appears in any log, commit, or message"
else
  echo "no candidate hit in any log under $ROOT"
fi
