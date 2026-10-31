#!/bin/bash
# GPU queue: t21_single, after the 15-config batch of 31 Oct (run_queue_oct31.sh).
# Starts only on "QUEUE DONE" in queue_oct31.log; "QUEUE STOPPED" there means this does not start either.
# Hold pattern: refuses while any HOLD_SINGLE* file exists, so it can be stopped without killing anything.
# Band and the three objections committed before launch (~/blm-analysis/QUEUE_after_el22.md, commit 6b50fb8).
# 2,677,850,419,968 candidates = 54^7 x 2, band 20,920,706,406.0 +/- 141,701, about 2.82 GPU-days.
# HIT rule: queuesingle_<config>.log is read only with grep -c -E '^HIT[[:space:]]+index' and grep -E '^exit='.
# Survivors are extracted only after exit=2, only from "exhausted, no match" lines.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
LOG=queue_single.log; SC=queue_single_scores.tsv
echo "$(date -u '+%a %d %b %H:%M:%S UTC')  WAITING for the 31 Oct batch to finish" >> $LOG
until grep -q -E 'QUEUE DONE|QUEUE STOPPED|QUEUE NOT STARTED' queue_oct31.log 2>/dev/null; do sleep 60; done
if ! grep -q 'QUEUE DONE' queue_oct31.log; then echo "the 31 Oct batch did not finish cleanly: QUEUE NOT STARTED" >> $LOG; exit 1; fi
for h in HOLD_SINGLE*; do [ -e "$h" ] && { echo "on hold ($h: $(head -1 "$h")): QUEUE NOT STARTED" >> $LOG; exit 0; }; done
sleep 30
if pgrep -x solver2_jac > /dev/null; then echo "a solver is already running: QUEUE NOT STARTED" >> $LOG; exit 1; fi
setsid ./thermal_guard_queue.sh $$ > /dev/null 2>&1 < /dev/null &
setsid systemd-inhibit --what=sleep:idle:handle-lid-switch --why="queue single" tail --pid=$$ -f /dev/null > /dev/null 2>&1 < /dev/null &
[ -f $SC ] || printf 'config\tpass\texit\tsurvivors\tspace\n' > $SC
for c in t21_single; do
  date -u "+%a %d %b %H:%M:%S UTC  START $c" >> $LOG
  s=$(date +%s.%N)
  ./solver2_jac --config $c.conf >> queuesingle_$c.log 2>&1
  rc=$?; e=$(date +%s.%N)
  echo "exit=$rc $(date -u '+%a %d %b %H:%M:%S UTC')  END $c  wall=$(python3 -c "print(f'{$e-$s:.2f}')")s" >> $LOG
  if [ $rc -ne 2 ]; then echo "QUEUE STOPPED after $c (exit=$rc)" >> $LOG; exit $rc; fi
  i=0; grep -oE 'exhausted, no match  \(survivors [0-9]+ of [0-9]+\)' queuesingle_$c.log | grep -oE '[0-9]+ of [0-9]+' | \
    while read sv _ sp; do i=$((i+1)); printf '%s\t%s\t%s\t%s\t%s\n' "$c" "$i" "$rc" "$sv" "$sp" >> $SC; done
done
echo "QUEUE DONE $(date -u '+%a %d %b %H:%M:%S UTC')" >> $LOG
