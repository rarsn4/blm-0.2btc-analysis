#!/bin/bash
# Restart el22 from its saved checkpoint (after ./stop_el22.sh, a crash, or a reboot).
# usage: ./resume_el22.sh            resume
#        ./resume_el22.sh --dry-run  show the resume point and checks, change nothing
# Never use run_el22.sh to restart: it has no --resume, so it would start from 0 and
# overwrite the checkpoint. HIT rule: reads electrum_rerun.log only with grep -c / grep '^exit='.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
DRY=0; [ "$1" = "--dry-run" ] && DRY=1
if [ -e HOLD_EL22 ]; then echo "el22 is on hold (HOLD_EL22: $(head -1 HOLD_EL22)); not resuming. Remove HOLD_EL22 to allow it."; exit 0; fi
N=16470860000000; CHUNK=3758096384
pid=$(ps -eo pid,args | awk '$2 ~ /solver2_jac$/ && $3=="--config" && $4=="el22.conf"{print $1}')
[ -n "$pid" ] && { echo "el22 is already running (pid $pid). Nothing to resume."; [ $DRY = 1 ] || exit 1; }
hits=$(grep -c -E '^HIT[[:space:]]+index' electrum_rerun.log)
[ "$hits" -ne 0 ] && { echo "HIT count $hits. Not resuming: HIT rule in DO_NOT_PUSH."; exit 2; }
done22=$(grep -E '^exit=2 .*END el22' electrum_rerun.log | wc -l)
hit22=$(grep -E '^exit=0 .*END el22' electrum_rerun.log | wc -l)
[ "$hit22" -ne 0 ] && { echo "an el22 segment ended with exit=0 (count $hit22). Not resuming: HIT rule."; exit 2; }
[ "$done22" -ne 0 ] && { echo "el22 already finished (exit=2). Nothing to resume."; exit 1; }
# resume point: the highest of the live checkpoint, the saved copy, and the logger's history
cands=$(cut -d' ' -f2 progress_el22.txt 2>/dev/null; cut -d' ' -f2 el22_saved_checkpoint.txt 2>/dev/null;
        awk -F'\t' '$1=="el22"{v=$2} END{print v}' free313_boundaries.tsv)
v=$(printf '%s\n' $cands | sort -n | tail -1)
echo "resume candidates: $(printf '%s ' $cands)-> using $v"
[ -z "$v" ] && { echo "no checkpoint found"; exit 1; }
[ $((v % CHUNK)) -ne 0 ] && { echo "checkpoint $v is not chunk-aligned; refusing."; exit 1; }
[ "$v" -ge $N ] && { echo "checkpoint $v is at or past the end; refusing."; exit 1; }
echo "will resume at $v = $((v / CHUNK)) chunks ($(python3 -c "print(f'{$v/$N:.2%}')") of el22)"
[ $DRY = 1 ] && { echo "dry run: no changes made."; exit 0; }
cat > run_el22_resume.sh <<EOS
#!/bin/bash
cd ~/Downloads/Brainwallet/files\\(6\\) || exit 1
date -u "+%a %d %b %H:%M:%S UTC  START el22 (resume from $v)" >> electrum_rerun.log
s=\$(date +%s.%N)
./solver2_jac --config el22.conf --resume $v >> electrum_rerun.log 2>&1
rc=\$?; e=\$(date +%s.%N)
echo "exit=\$rc \$(date -u '+%a %d %b %H:%M:%S UTC')  END el22  wall=\$(python3 -c "print(f'{\$e-\$s:.2f}')")s" >> electrum_rerun.log
EOS
chmod +x run_el22_resume.sh
printf '%s\tresume\t%s\n' "$(date -u +%FT%TZ)" "$v" >> el22_segments.tsv
setsid nohup ./run_el22_resume.sh > /dev/null 2>&1 < /dev/null &
sleep 5
ps -eo args | awk '$1 ~ /bash$/ && $2 ~ /boundary_log\.sh$/' | grep -q . || setsid nohup ./boundary_log.sh > /dev/null 2>&1 < /dev/null &
setsid nohup ./thermal_guard.sh > /dev/null 2>&1 < /dev/null &
runpid=$(ps -eo pid,args | awk '$2 ~ /bash$/ && $3 ~ /run_el22_resume\.sh$/{print $1}')
ps -eo args | awk '$1 ~ /systemd-inhibit$/ && /el22 run/' | grep -q . || \
  setsid nohup systemd-inhibit --what=sleep:idle:handle-lid-switch --why="el22 run" tail --pid="$runpid" -f /dev/null > /dev/null 2>&1 < /dev/null &
sleep 2
echo "running:"; ps -eo pid,args | awk '$2 ~ /solver2_jac$/ || ($2 ~ /bash$/ && $3 ~ /(run_el22_resume|thermal_guard|boundary_log)\.sh$/) || ($2 ~ /systemd-inhibit$/ && /el22 run/)'
