#!/bin/bash
# GPU queue t21_pool60c: runs after run_queue_oct30b.sh (the "top" batch), which waits for t21_pool57v, which waits
# for el22 to finish.
# Starts only on "QUEUE DONE" in queue_oct30b.log; "QUEUE STOPPED" or "QUEUE NOT STARTED" there means this batch
# does not start either. Never interrupts el22, t21_pool57v or the top batch.
# HIT rule: queue30c_<config>.log is read only with grep -c -E '^HIT[[:space:]]+index' and grep -E '^exit='.
# Survivors are extracted only after exit=2, only from "exhausted, no match" lines.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
LOG=queue_oct30c.log; SC=queue_oct30c_scores.tsv
echo "$(date -u '+%a %d %b %H:%M:%S UTC')  WAITING for queue_oct30b (top batch) to finish" >> $LOG
until grep -q -E 'QUEUE DONE|QUEUE STOPPED|QUEUE NOT STARTED' queue_oct30b.log 2>/dev/null; do sleep 60; done
if ! grep -q 'QUEUE DONE' queue_oct30b.log; then echo "queue_oct30b did not finish cleanly: QUEUE NOT STARTED" >> $LOG; exit 1; fi
sleep 30
if pgrep -x solver2_jac > /dev/null; then echo "a solver is already running: QUEUE NOT STARTED" >> $LOG; exit 1; fi
setsid ./thermal_guard_queue.sh $$ > /dev/null 2>&1 < /dev/null &
setsid systemd-inhibit --what=sleep:idle:handle-lid-switch --why="queue oct30c" tail --pid=$$ -f /dev/null > /dev/null 2>&1 < /dev/null &
[ -f $SC ] || printf 'config\tpass\texit\tsurvivors\tspace\n' > $SC
for c in t21_pool60c; do
  date -u "+%a %d %b %H:%M:%S UTC  START $c" >> $LOG
  s=$(date +%s.%N)
  ./solver2_jac --config $c.conf >> queue30c_$c.log 2>&1
  rc=$?; e=$(date +%s.%N)
  echo "exit=$rc $(date -u '+%a %d %b %H:%M:%S UTC')  END $c  wall=$(python3 -c "print(f'{$e-$s:.2f}')")s" >> $LOG
  if [ $rc -ne 2 ]; then echo "QUEUE STOPPED after $c (exit=$rc)" >> $LOG; exit $rc; fi
  i=0; grep -oE 'exhausted, no match  \(survivors [0-9]+ of [0-9]+\)' queue30c_$c.log | grep -oE '[0-9]+ of [0-9]+' | \
    while read sv _ sp; do i=$((i+1)); printf '%s\t%s\t%s\t%s\t%s\n' "$c" "$i" "$rc" "$sv" "$sp" >> $SC; done
done
echo "QUEUE DONE $(date -u '+%a %d %b %H:%M:%S UTC')" >> $LOG
