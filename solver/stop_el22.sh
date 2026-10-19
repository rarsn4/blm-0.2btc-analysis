#!/bin/bash
# Stop el22 cleanly, right after a checkpoint, so only seconds of work are lost.
# usage: ./stop_el22.sh            stop at the next checkpoint (waits up to ~4 min)
#        ./stop_el22.sh --dry-run  show what would happen, change nothing
# HIT rule: reads electrum_rerun.log only with grep -c / grep '^exit='. Appends one marker line.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
DRY=0; [ "$1" = "--dry-run" ] && DRY=1
pid=$(ps -eo pid,args | awk '$2 ~ /solver2_jac$/ && $3=="--config" && $4=="el22.conf"{print $1}')
[ -z "$pid" ] && { echo "el22 is not running; nothing to stop."; exit 1; }
hits=$(grep -c -E '^HIT[[:space:]]+index' electrum_rerun.log)
[ "$hits" -ne 0 ] && { echo "HIT count $hits. Not touching anything: HIT rule in DO_NOT_PUSH."; exit 2; }
inh=$(ps -eo pid,args | awk '$2 ~ /systemd-inhibit$/ && /el22 run/{print $1}')
echo "el22 solver pid $pid; checkpoint now $(cut -d' ' -f2 progress_el22.txt); sleep blocker pid ${inh:-none}"
[ $DRY = 1 ] && { echo "dry run: would wait for the next checkpoint, stop the solver, save the checkpoint, release the sleep blocker."; exit 0; }
m0=$(stat -c %Y progress_el22.txt)
echo "waiting for the next checkpoint (every ~3.5 min)..."
while [ "$(stat -c %Y progress_el22.txt)" = "$m0" ]; do sleep 1; done
v=$(cut -d' ' -f2 progress_el22.txt)
echo "$(date -u '+%a %d %b %H:%M:%S UTC')  STOP el22 by owner at checkpoint $v" >> electrum_rerun.log
kill "$pid"
while kill -0 "$pid" 2>/dev/null; do sleep 1; done
cp -p progress_el22.txt el22_saved_checkpoint.txt
printf '%s\tstop\t%s\n' "$(date -u +%FT%TZ)" "$v" >> el22_segments.tsv
[ -n "$inh" ] && kill $inh 2>/dev/null
echo "stopped at $v ($(python3 -c "print(f'{$v/16470860000000:.2%}')") of el22). Saved to el22_saved_checkpoint.txt."
echo "Sleep blocker released; the PC may sleep or shut down. Restart with ./resume_el22.sh"
