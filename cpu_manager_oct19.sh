#!/bin/bash
# CPU passphrase work of 19 Oct, under the owner's rule: the GPU has priority.
#   1. wait for the running 8/9-passphrase small set (pid $1); stop if it reported a match
#   2. small52: el12 el13 el14 el16 el17 with the 52 Electrum-normalized pw2.txt forms (12 workers, nice 19)
#   3. el18n: el18 with 55 forms, 6 workers, nice 19, checkpointed (passphrase_cpu_el18n.ckpt), and every 5 min:
#        more than 3 GPU thermal pauses in the last hour -> stop, restart on 4 workers from the checkpoint;
#        more than 3 again on 4 workers -> stop, wait until no GPU solver has run for 10 min, resume on 6.
# HIT rule: passphrase_cpu.py prints counts only; a match exits 3 and nothing is restarted.
# Events go to cpu_manager_oct19.log.
B=~/blm-analysis; S="$HOME/Downloads/Brainwallet/files(6)"; TH="$S/free313_thermal.tsv"; LOG=$B/cpu_manager_oct19.log
PY="python3 -I $B/passphrase_cpu.py"
log() { echo "$(date -u '+%FT%TZ') $*" >> "$LOG"; }

tail --pid="$1" -f /dev/null
grep -q 'MATCH COUNT' $B/passphrase_cpu_small.out && { log "small set reported a match: stopping (HIT rule)"; exit 3; }
log "small set done; small52 starts (12 workers, nice 19)"
nice -n 19 $PY "$S" small52 12 > $B/passphrase_cpu_small52.out 2>&1; rc=$?
[ $rc -ne 0 ] && { log "small52 exit $rc: stopping"; exit $rc; }
log "small52 done; el18n starts under the thermal rule"

pauses_since() { awk -F'\t' -v t="$1" '$1 >= t && $8 ~ /PAUSED/' "$TH" | wc -l; }
W=6; STAGE=0
start() { setsid nice -n 19 $PY "$S" el18n $W >> $B/passphrase_cpu_el18n.out 2>&1 & P=$!; T0=$(date -u +%FT%TZ); log "el18n started: $W workers, pid $P, stage $STAGE"; }
stop()  { kill -TERM -- -"$P" 2>/dev/null; sleep 5; kill -KILL -- -"$P" 2>/dev/null; wait "$P" 2>/dev/null; log "el18n stopped (pid $P)"; }
start
while kill -0 "$P" 2>/dev/null; do
  sleep 300
  kill -0 "$P" 2>/dev/null || break
  W60=$(date -u -d '-60 min' +%FT%TZ); [[ "$T0" > "$W60" ]] && W60=$T0
  n=$(pauses_since "$W60")
  if [ "$n" -gt 3 ] && [ $STAGE -eq 0 ]; then
    log "$n GPU pauses in the last hour: el18n cut to 4 workers"; stop; W=4; STAGE=1; start
  elif [ "$n" -gt 3 ] && [ $STAGE -eq 1 ]; then
    log "$n GPU pauses in the last hour at 4 workers: el18n paused until the GPU work is done"; stop; STAGE=2
    idle=0; while [ $idle -lt 600 ]; do sleep 60; if pgrep -x solver2_jac > /dev/null; then idle=0; else idle=$((idle + 60)); fi; done
    log "no GPU solver for 10 min: el18n resumes on 6 workers"; W=6; STAGE=3; start
  fi
done
wait "$P"; rc=$?
log "el18n ended, exit $rc"
