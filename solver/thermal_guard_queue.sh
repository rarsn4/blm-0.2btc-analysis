#!/bin/bash
# Thermal guard for the 19 Oct queue: as thermal_guard.sh, but it lives as long as the queue script
# (pid $1), so the gaps between runs do not end it. pgrep -x matches the process name exactly.
cd ~/Downloads/Brainwallet/files\(6\) || exit 1
OUT=free313_thermal.tsv; HOT=90; PAUSE=20; Q=$1
while kill -0 "$Q" 2>/dev/null; do
  pid=$(pgrep -x solver2_jac | head -1)
  if [ -z "$pid" ]; then printf '%s\t-\t-\t-\t-\t-\t-\tbetween_runs\n' "$(date -u +%FT%TZ)" >> "$OUT"; sleep 20; continue; fi
  read t c p th < <(nvidia-smi --query-gpu=temperature.gpu,clocks.sm,power.draw,clocks_throttle_reasons.active \
                    --format=csv,noheader,nounits | tr -d ',')
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
printf '%s\t-\t-\t-\t-\t-\t-\tqueue_gone\n' "$(date -u +%FT%TZ)" >> "$OUT"
