#!/bin/bash
# Chunk-boundary deltas from the checkpoint file's MTIME, not from poll time.
# A 60 s poll against a ~315 s chunk carries up to 19% error on one interval;
# mtime is the exact moment the solver wrote the boundary. Rate is dv/dt over
# the interval, so the chunk quantization cancels instead of accumulating.
OUT=free313_boundaries.tsv
[ -f "$OUT" ] || printf 'config\tvalue\tmtime_utc\tdt_s\tdv\trate_cand_s\n' > "$OUT"
declare -A lastv lastm
while :; do
  for f in progress_t21_free3.txt progress_t21_free13.txt progress_t21_tarot_j10x20.txt progress_t21_tarot_j17x19.txt progress_t21_ink10x20.txt progress_t21_needle11.txt progress_t21_amend1415.txt progress_t21_flag6_apple.txt progress_t21_loo6_apple.txt progress_t21_loo8_apple.txt progress_t21_loo14_apple.txt progress_t21_loo15_apple.txt progress_t21_loo18_apple.txt progress_el21.txt progress_el22.txt progress_t21_rev54.txt progress_t21_pool58.txt progress_t21_food11.txt progress_el21_rev.txt progress_t21_slot1_line.txt progress_t21_alt3.txt progress_t21_free20.txt progress_t21_readme54.txt progress_t21_pool55b.txt progress_t21_pool56.txt progress_t21_pool57.txt progress_t21_silent4.txt progress_t21_idx2.txt progress_t21_colour.txt progress_t21_title1.txt progress_t21_black1.txt progress_t21_glass.txt progress_t21_food1.txt progress_t21_food7.txt progress_t21_pool60.txt progress_t21_slot1.txt progress_t21_pool57v.txt; do
    [ -f "$f" ] || continue
    c=${f#progress_}; c=${c%.txt}
    v=$(cut -d' ' -f2 "$f" 2>/dev/null); m=$(stat -c %Y "$f" 2>/dev/null)
    [ -z "$v" ] && continue
    if [ "${lastv[$c]}" != "$v" ]; then
      if [ -n "${lastm[$c]}" ]; then
        dt=$((m-lastm[$c])); dv=$((v-lastv[$c]))
        [ "$dt" -gt 0 ] && printf '%s\t%d\t%s\t%d\t%d\t%d\n' \
          "$c" "$v" "$(date -u -d @$m +%FT%TZ)" "$dt" "$dv" "$((dv/dt))" >> "$OUT"
      fi
      lastv[$c]=$v; lastm[$c]=$m
    fi
  done
  sleep 5
done
