# DQX Puzzle Scanner

`dqx_scan.py` is the fixed and rebuilt version of DEUS‑QUANTUM‑X. It is a single file that uses only the Python standard library (Python 3.8+, on Linux, macOS or Windows). It searches the ~1000 BTC puzzle ranges #71–#100 (#66–#70 are built in as solved test cases), or any range and address you set.

```bash
python dqx_scan.py selftest            # do this first: proves it finds the solved #67/#68 keys
python dqx_scan.py bench               # your real keys/s and expected times
python dqx_scan.py list                # puzzles #71-#100, ranges, prizes
python dqx_scan.py list --online       # + live balances (mempool.space)

python dqx_scan.py scan --puzzle 71                      # random chunks of #71
python dqx_scan.py scan --puzzle 71-100                  # every unsolved puzzle #71-#100
python dqx_scan.py scan --puzzle 71 --mode sequential    # in order, resumable
python dqx_scan.py scan --puzzle 71 --start 50% --end 51%                 # set a range
python dqx_scan.py scan --puzzle 71 --start 0x5a0000000000000000 --end 0x5affffffffffffffff
python dqx_scan.py scan --puzzle 71 --shard 3/8          # split the work across 8 machines
python dqx_scan.py scan --address 1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9 \
                        --start 730fc235c1942c1a0 --end 730fc235c1942c2ae
```

* **Range format:** `--start` and `--end` take hex (with or without `0x`), `dec:<decimal>`, or a percentage of the puzzle range. Both ends are inclusive.
* **Stopping and resuming:** stop with Ctrl+C, `kill`, or by creating a file named `STOP`. Progress is saved in `dqx_state.db`, and running the same command again resumes. Progress is stored per exact range and chunk size, so a changed range starts fresh instead of reusing a stale position.
* **If a key is found:** it is re-verified, appended to `FOUND_KEYS.txt` with its WIF (and fsync'ed), and all workers stop. `FOUND_KEYS.txt` is git‑ignored on purpose. **Never** spend through the public mempool: the spend reveals the public key, and bots can recover a key this small with kangaroo and replace your transaction. Submit privately to a mining pool.

## Speed and odds

* The scanner uses batched point addition with one shared inverse per 4097 keys (C ± iG). It measured about 270k keys/s per core, compared with about 21k for the original code.
* At 1M keys/s, a full scan of #71 (2^70 keys) takes about 37 million years. Each higher puzzle doubles that.
* The public GPU pools run at about 10^11 keys/s. Treat a CPU run as a lottery ticket.
* If you scan several puzzles at once, keep in mind that a key checked in #71 is 2^(n−71) times more likely to win than a key in #n.
