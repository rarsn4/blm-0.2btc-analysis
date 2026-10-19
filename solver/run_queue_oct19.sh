#!/bin/bash
# GPU queue of 19 Oct 2026, run while el22 is paused. One run after another; stops on any exit code but 2.
# Each run's solver output goes to its own queue_<config>.log. HIT rule: those logs are read only with
#   grep -c -E '^HIT[[:space:]]+index'  and  grep -E '^exit='.
# The survivor count is extracted HERE, automatically, only after exit=2 (no hit possible), and only by a
# pattern that matches nothing but the "exhausted, no match" line. Scores go to queue_oct19_scores.tsv.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
LOG=queue_oct19.log; SC=queue_oct19_scores.tsv
[ -f $SC ] || printf 'config\texit\tsurvivors\tspace\n' > $SC
for c in t21_rev54 t21_pool58 t21_food11 el21_rev t21_slot1_line t21_alt3; do
  date -u "+%a %d %b %H:%M:%S UTC  START $c" >> $LOG
  s=$(date +%s.%N)
  ./solver2_jac --config $c.conf >> queue_$c.log 2>&1
  rc=$?; e=$(date +%s.%N)
  echo "exit=$rc $(date -u '+%a %d %b %H:%M:%S UTC')  END $c  wall=$(python3 -c "print(f'{$e-$s:.2f}')")s" >> $LOG
  if [ $rc -ne 2 ]; then echo "QUEUE STOPPED after $c (exit=$rc); el22 NOT resumed" >> $LOG; exit $rc; fi
  sv=$(grep -oE 'exhausted, no match  \(survivors [0-9]+ of [0-9]+\)' queue_$c.log | grep -oE '[0-9]+ of [0-9]+' | tail -1)
  printf '%s\t%s\t%s\t%s\n' "$c" "$rc" "${sv%% of *}" "${sv##* of }" >> $SC
done
echo "QUEUE DONE $(date -u '+%a %d %b %H:%M:%S UTC'); resuming el22" >> $LOG
./resume_el22.sh > queue_oct19_resume.txt 2>&1
