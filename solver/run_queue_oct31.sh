#!/bin/bash
# GPU queue of 31 Oct 2026: the three batches. 8 clock rotations, black-as-digit x6, this@3.
# Bands committed before launch in ~/blm-analysis/QUEUE_after_el22.md (commit 352617f).
# HIT rule: queue31_<config>.log is read only with grep -c -E '^HIT[[:space:]]+index' and grep -E '^exit='.
# Survivors are extracted only after exit=2, only from "exhausted, no match" lines.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
LOG=queue_oct31.log; SC=queue_oct31_scores.tsv
if pgrep -x solver2_jac > /dev/null; then echo "a solver is already running: QUEUE NOT STARTED" >> $LOG; exit 1; fi
setsid ./thermal_guard_queue.sh $$ > /dev/null 2>&1 < /dev/null &
setsid systemd-inhibit --what=sleep:idle:handle-lid-switch --why="queue oct31" tail --pid=$$ -f /dev/null > /dev/null 2>&1 < /dev/null &
[ -f $SC ] || printf 'config\tpass\texit\tsurvivors\tspace\n' > $SC
for c in t21_clk2 t21_clk3 t21_clk4 t21_clk5 t21_clk6 t21_clk7 t21_clk8 t21_clk9 \
         t21_blackd2 t21_blackd3 t21_blackd4 t21_blackd5 t21_blackd7 t21_blackd9 \
         t21_this3; do
  date -u "+%a %d %b %H:%M:%S UTC  START $c" >> $LOG
  s=$(date +%s.%N)
  ./solver2_jac --config $c.conf >> queue31_$c.log 2>&1
  rc=$?; e=$(date +%s.%N)
  echo "exit=$rc $(date -u '+%a %d %b %H:%M:%S UTC')  END $c  wall=$(python3 -c "print(f'{$e-$s:.2f}')")s" >> $LOG
  if [ $rc -ne 2 ]; then echo "QUEUE STOPPED after $c (exit=$rc)" >> $LOG; exit $rc; fi
  i=0; grep -oE 'exhausted, no match  \(survivors [0-9]+ of [0-9]+\)' queue31_$c.log | grep -oE '[0-9]+ of [0-9]+' | \
    while read sv _ sp; do i=$((i+1)); printf '%s\t%s\t%s\t%s\t%s\n' "$c" "$i" "$rc" "$sv" "$sp" >> $SC; done
done
echo "QUEUE DONE $(date -u '+%a %d %b %H:%M:%S UTC')" >> $LOG
