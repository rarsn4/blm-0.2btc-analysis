#!/bin/bash
# GPU queue of Nov 2026: t21_nose2, then the 12-config paths-2-4 closure of REPORT 2.13's [SCOPE] gap.
# Runs after t21_single (run_queue_single.sh). Bands committed before launch in
# ~/blm-analysis/QUEUE_after_el22.md, commit 548e7b2.
#
# IDENTITY STOP: each t21_freeN is the 4-path twin of t21_freeN_p1 and MUST reproduce its logged survivor
# count EXACTLY, because survivors do not depend on the derivation path. A miss means the MACHINE is wrong,
# not the hypothesis, so the queue halts immediately and reports rather than carrying on.
#
# Hold pattern: refuses while any HOLD_NOV* file exists.
# HIT rule: queuenov_<config>.log is read only with grep -c -E '^HIT[[:space:]]+index' and grep -E '^exit='.
# Survivors are extracted only after exit=2, only from "exhausted, no match" lines.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
LOG=queue_nov.log; SC=queue_nov_scores.tsv

# identity targets: the logged survivor count of each _p1 twin
declare -A IDENT=(
  [t21_free1]=10654092960  [t21_free2]=10653915344  [t21_free4]=10654138418
  [t21_free5]=10654060538  [t21_free7]=10653988011  [t21_free9]=10654207551
  [t21_free10]=10654089154 [t21_free11]=10654060452 [t21_free12]=10654012263
  [t21_free16]=10653972836 [t21_free17]=10653994687 [t21_free19]=10654167169
)

echo "$(date -u '+%a %d %b %H:%M:%S UTC')  WAITING for t21_single to finish" >> $LOG
until grep -q -E 'QUEUE DONE|QUEUE STOPPED|QUEUE NOT STARTED' queue_single.log 2>/dev/null; do sleep 60; done
if ! grep -q 'QUEUE DONE' queue_single.log; then echo "t21_single did not finish cleanly: QUEUE NOT STARTED" >> $LOG; exit 1; fi
for h in HOLD_NOV*; do [ -e "$h" ] && { echo "on hold ($h: $(head -1 "$h")): QUEUE NOT STARTED" >> $LOG; exit 0; }; done
sleep 30
if pgrep -x solver2_jac > /dev/null; then echo "a solver is already running: QUEUE NOT STARTED" >> $LOG; exit 1; fi
setsid ./thermal_guard_queue.sh $$ > /dev/null 2>&1 < /dev/null &
setsid systemd-inhibit --what=sleep:idle:handle-lid-switch --why="queue nov" tail --pid=$$ -f /dev/null > /dev/null 2>&1 < /dev/null &
[ -f $SC ] || printf 'config\tpass\texit\tsurvivors\tspace\tidentity\n' > $SC

for c in t21_nose2 \
         t21_free11 t21_free2 t21_free4 t21_free12 t21_free16 t21_free17 \
         t21_free10 t21_free19 t21_free9 t21_free5 t21_free7 t21_free1; do
  date -u "+%a %d %b %H:%M:%S UTC  START $c" >> $LOG
  s=$(date +%s.%N)
  ./solver2_jac --config $c.conf >> queuenov_$c.log 2>&1
  rc=$?; e=$(date +%s.%N)
  echo "exit=$rc $(date -u '+%a %d %b %H:%M:%S UTC')  END $c  wall=$(python3 -c "print(f'{$e-$s:.2f}')")s" >> $LOG
  if [ $rc -ne 2 ]; then echo "QUEUE STOPPED after $c (exit=$rc)" >> $LOG; exit $rc; fi
  sv=$(grep -oE 'exhausted, no match  \(survivors [0-9]+ of [0-9]+\)' queuenov_$c.log | grep -oE 'survivors [0-9]+' | awk '{print $2}' | tail -1)
  sp=$(grep -oE 'exhausted, no match  \(survivors [0-9]+ of [0-9]+\)' queuenov_$c.log | grep -oE 'of [0-9]+' | awk '{print $2}' | tail -1)
  want=${IDENT[$c]}
  if [ -n "$want" ]; then
    if [ "$sv" = "$want" ]; then id=EXACT; else id=MISS; fi
  else
    id=n/a
  fi
  printf '%s\t1\t%s\t%s\t%s\t%s\n' "$c" "$rc" "$sv" "$sp" "$id" >> $SC
  if [ "$id" = "MISS" ]; then
    echo "IDENTITY MISS on $c: got $sv, the _p1 twin logged $want (difference $((sv - want)))." >> $LOG
    echo "QUEUE STOPPED: survivors cannot depend on the derivation path, so this is a MACHINE fault, not a result. Nothing after $c was run." >> $LOG
    exit 9
  fi
done
echo "QUEUE DONE $(date -u '+%a %d %b %H:%M:%S UTC')" >> $LOG
