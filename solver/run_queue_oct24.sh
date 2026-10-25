#!/bin/bash
# GPU queue of 24 Oct 2026, run while el22 is stopped. Stops on any exit code but 2, then resumes el22.
# Each run's output goes to queue24_<config>.log. HIT rule: those logs are read only with
#   grep -c -E '^HIT[[:space:]]+index'  and  grep -E '^exit='.
# Survivor counts are extracted here, only after exit=2, only from "exhausted, no match" lines
# (one per passphrase pass), into queue_oct24_scores.tsv.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
LOG=queue_oct24.log; SC=queue_oct24_scores.tsv
[ -f $SC ] || printf 'config\tpass\texit\tsurvivors\tspace\n' > $SC
for spec in "t21_free20|" "t21_readme54|breathe_pw.txt"; do
  c=${spec%%|*}; pw=${spec#*|}
  date -u "+%a %d %b %H:%M:%S UTC  START $c${pw:+ (passphrases from $pw)}" >> $LOG
  s=$(date +%s.%N)
  ./solver2_jac --config $c.conf ${pw:+--passphrases $pw} >> queue24_$c.log 2>&1
  rc=$?; e=$(date +%s.%N)
  echo "exit=$rc $(date -u '+%a %d %b %H:%M:%S UTC')  END $c  wall=$(python3 -c "print(f'{$e-$s:.2f}')")s" >> $LOG
  if [ $rc -ne 2 ]; then echo "QUEUE STOPPED after $c (exit=$rc); el22 NOT resumed" >> $LOG; exit $rc; fi
  i=0; grep -oE 'exhausted, no match  \(survivors [0-9]+ of [0-9]+\)' queue24_$c.log | grep -oE '[0-9]+ of [0-9]+' | \
    while read sv _ sp; do i=$((i+1)); printf '%s\t%s\t%s\t%s\t%s\n' "$c" "$i" "$rc" "$sv" "$sp" >> $SC; done
done
echo "QUEUE DONE $(date -u '+%a %d %b %H:%M:%S UTC'); resuming el22" >> $LOG
./resume_el22.sh > queue_oct24_resume.txt 2>&1
