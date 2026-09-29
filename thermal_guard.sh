#!/bin/bash
# Log temp/clock beside the checkpoint, and duty-cycle the solver if it gets hot.
# No root here, so nvidia-smi -lgc and -pl are both refused; the only
# privilege-free throttle is SIGSTOP/SIGCONT, which is safe because the solver
# checkpoints and loses at most a chunk.
OUT=free313_thermal.tsv
HOT=90          # act at this temperature
COOL=84         # resume once back below this
PAUSE=20        # seconds paused per cycle
[ -f "$OUT" ] || printf 'utc\tconfig\tcheckpoint\ttemp\tclock\tpower\tthrottle\taction\n' > "$OUT"
while :; do
  pid=$(pgrep -x solver2_jac | head -1)
  [ -z "$pid" ] && { printf '%s\t-\t-\t-\t-\t-\t-\tsolver_gone\n' "$(date -u +%FT%TZ)" >> "$OUT"; exit 0; }
  read t c p th < <(nvidia-smi --query-gpu=temperature.gpu,clocks.sm,power.draw,clocks_throttle_reasons.active \
                    --format=csv,noheader,nounits | tr -d ',' )
  cfg=$(tr '\0' ' ' < /proc/$pid/cmdline | grep -oP '(?<=--config )\S+' | sed 's/\.conf//')
  ck=$(cut -d' ' -f2 progress_${cfg}.txt 2>/dev/null || echo 0)
  act=ok
  if [ "${t:-0}" -ge $HOT ]; then
    kill -STOP $pid 2>/dev/null; act="PAUSED_${PAUSE}s@${t}C"
    for _ in $(seq $PAUSE); do sleep 1; done
    kill -CONT $pid 2>/dev/null
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$cfg" "$ck" "$t" "$c" "$p" "$th" "$act" >> "$OUT"
  sleep 60
done
