#!/bin/bash
# GPU queue after el22: t21_pool57v only. Starts only once el22 has FINISHED (exit=2 on its END line in
# electrum_rerun.log); a stop/resume of el22 (exit=143) keeps it waiting. Never interrupts el22.
# HIT rule: electrum_rerun.log is read only with grep -c -E '^HIT[[:space:]]+index' and grep -E '^exit=';
# an el22 END with exit=0 means a hit: this queue does not start. queue30_<config>.log is read only with
# grep -c '^HIT' and grep '^exit='. Survivors are extracted only after exit=2, from "exhausted, no match" lines.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
LOG=queue_oct30.log; SC=queue_oct30_scores.tsv
echo "$(date -u '+%a %d %b %H:%M:%S UTC')  WAITING for el22 to finish (exit=2)" >> $LOG
until grep -q -E '^exit=(0|2) .*END el22' electrum_rerun.log 2>/dev/null; do sleep 60; done
if grep -q -E '^exit=0 .*END el22' electrum_rerun.log || [ "$(grep -c -E '^HIT[[:space:]]+index' electrum_rerun.log)" -ne 0 ]; then
  echo "el22 ended with a HIT (HIT rule): QUEUE NOT STARTED" >> $LOG; exit 3; fi
sleep 60
if pgrep -x solver2_jac > /dev/null; then echo "a solver is already running: QUEUE NOT STARTED" >> $LOG; exit 1; fi
setsid ./thermal_guard_queue.sh $$ > /dev/null 2>&1 < /dev/null &
setsid systemd-inhibit --what=sleep:idle:handle-lid-switch --why="queue oct30" tail --pid=$$ -f /dev/null > /dev/null 2>&1 < /dev/null &
[ -f $SC ] || printf 'config\tpass\texit\tsurvivors\tspace\n' > $SC
for spec in "t21_pool57v|"; do
  c=${spec%%|*}; pw=${spec#*|}
  date -u "+%a %d %b %H:%M:%S UTC  START $c${pw:+ (passphrases from $pw)}" >> $LOG
  s=$(date +%s.%N)
  ./solver2_jac --config $c.conf ${pw:+--passphrases $pw} >> queue30_$c.log 2>&1
  rc=$?; e=$(date +%s.%N)
  echo "exit=$rc $(date -u '+%a %d %b %H:%M:%S UTC')  END $c  wall=$(python3 -c "print(f'{$e-$s:.2f}')")s" >> $LOG
  if [ $rc -ne 2 ]; then echo "QUEUE STOPPED after $c (exit=$rc)" >> $LOG; exit $rc; fi
  i=0; grep -oE 'exhausted, no match  \(survivors [0-9]+ of [0-9]+\)' queue30_$c.log | grep -oE '[0-9]+ of [0-9]+' | \
    while read sv _ sp; do i=$((i+1)); printf '%s\t%s\t%s\t%s\t%s\n' "$c" "$i" "$rc" "$sv" "$sp" >> $SC; done
done
echo "QUEUE DONE $(date -u '+%a %d %b %H:%M:%S UTC')" >> $LOG
