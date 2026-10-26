#!/bin/bash
# GPU queue of 26 Oct 2026: waits for the 25 Oct queue, runs t21_idx2, then resumes el22.
# el22 is held by HOLD_EL22_IDX2 meanwhile (resume_el22.sh refuses while any HOLD_EL22* exists).
# HIT rule: queue26_<config>.log is read only with grep -c -E '^HIT[[:space:]]+index' and grep -E '^exit='.
# Survivors are extracted only after exit=2, only from "exhausted, no match" lines.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
LOG=queue_oct26.log; SC=queue_oct26_scores.tsv
until grep -q -E 'QUEUE DONE|QUEUE STOPPED' queue_oct25.log 2>/dev/null; do sleep 60; done
if grep -q 'QUEUE STOPPED' queue_oct25.log; then echo "25 Oct queue stopped: not starting; el22 stays held" >> $LOG; exit 1; fi
sleep 20
if pgrep -x solver2_jac > /dev/null; then echo "a solver is already running: not starting" >> $LOG; exit 1; fi
setsid ./thermal_guard_queue.sh $$ > /dev/null 2>&1 < /dev/null &
setsid systemd-inhibit --what=sleep:idle:handle-lid-switch --why="queue oct26" tail --pid=$$ -f /dev/null > /dev/null 2>&1 < /dev/null &
[ -f $SC ] || printf 'config\tpass\texit\tsurvivors\tspace\n' > $SC
for spec in "t21_idx2|" "t21_pool60|" "t21_slot1|" "t21_food7|" "t21_readme54|tuesday_pw.txt"; do
  c=${spec%%|*}; pw=${spec#*|}
  date -u "+%a %d %b %H:%M:%S UTC  START $c${pw:+ (passphrases from $pw)}" >> $LOG
  s=$(date +%s.%N)
  ./solver2_jac --config $c.conf ${pw:+--passphrases $pw} >> queue26_$c.log 2>&1
  rc=$?; e=$(date +%s.%N)
  echo "exit=$rc $(date -u '+%a %d %b %H:%M:%S UTC')  END $c  wall=$(python3 -c "print(f'{$e-$s:.2f}')")s" >> $LOG
  if [ $rc -ne 2 ]; then echo "QUEUE STOPPED after $c (exit=$rc); el22 stays held" >> $LOG; exit $rc; fi
  i=0; grep -oE 'exhausted, no match  \(survivors [0-9]+ of [0-9]+\)' queue26_$c.log | grep -oE '[0-9]+ of [0-9]+' | \
    while read sv _ sp; do i=$((i+1)); printf '%s\t%s\t%s\t%s\t%s\n' "$c" "$i" "$rc" "$sv" "$sp" >> $SC; done
done
echo "QUEUE DONE $(date -u '+%a %d %b %H:%M:%S UTC'); lifting HOLD_EL22_IDX2 and resuming el22" >> $LOG
rm -f HOLD_EL22_IDX2
./resume_el22.sh > queue_oct26_resume.txt 2>&1
