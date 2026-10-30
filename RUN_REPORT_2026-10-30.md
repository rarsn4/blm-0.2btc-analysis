# Search report, 14–30 October 2026

Target `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`, hash160 `ccbd031e54cde2a3189fd59bc49f731367a1779e`.
Local file, not for publication (DO_NOT_PUSH). Every figure below was recomputed on 30 Oct from the configs and
the score files, not copied from earlier messages.

## 1. Bottom line

- **No match anywhere.** The search found nothing in el22 or in any of the 28 queue steps since 19 Oct. Every
  log has 0 HIT lines.
- **Every count passed its check.** There are 24 band tests (z-scores), and all fall inside ±3 σ. There are 23
  identity checks, and all are exact.
- **el22 is finished.** This is the 22-word Electrum search, ended `exit=2` on Fri 30 Oct 04:55:56 UTC.
- **The GPU is idle.** Nothing is queued.

## 2. el22 (Electrum, 22 words)

The template is the 21-word one plus a 22nd slot. It has seven gaps over a 70-word pool, two words at slot 20,
and four paths (`m/0'/0`, `m/0'/0/0`, `m/0/0`, `m/44'/0'/0'/0/0`). That gives 70^7 x 2 = 16,470,860,000,000
candidates.

| segment | from | to | ended | GPU time |
|---|---|---|---|---|
| 1 | 0 (14 Oct) | 6,531,571,515,392 = 1,738 chunks | stopped 18 Oct, exit=143 | 97.9 h |
| 2 | 6,531,571,515,392 (20 Oct) | 12,236,361,826,304 = 3,256 chunks | stopped 24 Oct, exit=143 | 93.4 h |
| 3 | 12,236,361,826,304 (27 Oct) | 16,470,860,000,000 (end) | **exit=2**, 30 Oct 04:55:56 | 63.1 h |

- **Coverage of the whole space.** It rests on the segment chain. Each resume index equals the stop index, and
  both stops are on chunk boundaries.
- **Score of segment 3 (25.71% of the space).** The survivors were 17,574,712,922 against
  17,574,821,521.7 ± 132,295, so **z = −0.821, in band**. The survivor counter restarts on resume, so segments 1
  and 2 have no count.
- **How the count was read.** The owner set a gate on 27 Oct. First, el22's END line showed `exit=2` and the HIT
  count was 0. Only then was the one permitted line read (`grep -oE 'exhausted, no match …'`). Nothing else was
  read from the log.
- **Size.** About 68.4 billion Electrum seeds were derived over the whole run, at 16,470,860,000,000 x 17/4096.
  That is an expected value, because only segment 3 was counted. Total GPU time was 254.5 h (10.6 days).

## 3. Queue runs, 19–30 October (BIP39 unless marked; 4 paths each)

Every band was committed before launch (`QUEUE_after_el22.md`). Survivors are taken from each run's own log,
after `exit=2`.

| when | run | candidates | survivors | band | result |
|---|---|---|---|---|---|
| 19–20 Oct | t21_rev54 | 49,589,822,592 | 387,420,823 | 387,420,489.0 ± 19,606 | z +0.017 |
| 19–20 Oct | t21_pool58 | 76,137,385,088 | 594,824,477 | 594,823,321.0 ± 23,874 | z +0.048 |
| 19–20 Oct | t21_food11 | 148,769,467,776 | 1,162,260,604 | 1,162,261,467.0 ± 33,399 | z −0.026 |
| 19–20 Oct | el21_rev (Electrum) | 235,298,000,000 | 976,591,446 | 976,578,613.3 ± 31,185 | z +0.411 |
| 19–20 Oct | t21_slot1_line | 247,949,112,960 | 1,936,982,003 | 1,937,102,445.0 ± 43,118 | z −2.793 |
| 19–20 Oct | t21_alt3 | 396,718,580,736 | 3,099,279,830 | 3,099,363,912.0 ± 54,541 | z −1.542 |
| 24–25 Oct | t21_free20 | 1,388,515,032,576 | 10,847,704,031 | 10,847,773,692.0 ± 102,037 | z −0.683; equals free20_p1 exactly |
| 25–26 Oct | t21_pool57 (black, air, silent) | 68,592,894,498 | 535,897,636 | 535,881,988.3 ± 22,680 | z +0.690 |
| 25–26 Oct | t21_silent4 | 49,589,822,592 | 387,414,920 | 387,420,489.0 ± 19,283 | z −0.289 |
| 26–27 Oct | t21_idx2 | 137,438,953,472 | 1,073,739,482 | 1,073,741,824.0 ± 31,839 | z −0.074 |
| 26–27 Oct | t21_pool60 | 93,312,000,000 | 729,015,479 | 729,000,000.0 ± 26,428 | z +0.586 |
| 26–27 Oct | t21_slot1 | 297,538,935,552 | 2,324,505,174 | 2,324,522,934.0 ± 47,234 | z −0.376 |
| 26–27 Oct | t21_food7 | 49,589,822,592 | 387,432,088 | 387,420,489.0 ± 19,283 | z +0.602 |
| 30 Oct | t21_pool57v (virus, hour, mirror) | 68,592,894,498 | 535,893,025 | 535,881,988.3 ± 22,660 | z +0.487 |
| 30 Oct | t21_top20 | 24,794,911,296 | 193,728,375 | 193,710,244.5 ± 13,635 | z +1.330 |
| 30 Oct | t21_top6_loo8 | 34,828,517,376 | 272,117,975 | 272,097,792.0 ± 16,160 | z +1.249 |
| 30 Oct | t21_top6_loo14 | 34,828,517,376 | 272,096,716 | 272,097,792.0 ± 16,160 | z −0.067 |
| 30 Oct | t21_top6_loo15 | 34,828,517,376 | 272,097,569 | 272,097,792.0 ± 16,160 | z −0.014 |
| 30 Oct | t21_top6_loo18 | 34,828,517,376 | 272,109,740 | 272,097,792.0 ± 16,160 | z +0.739 |
| 30 Oct | t21_top6_loo21 | 34,828,517,376 | 272,097,792 | must equal 272,097,792 | **exact** |
| 30 Oct | t21_top_at_7 | 49,589,822,592 | 387,413,240 | 387,420,489.0 ± 19,283 | z −0.376 |
| 30 Oct | t21_top_at_9 | 49,589,822,592 | 387,435,144 | 387,420,489.0 ± 19,283 | z +0.760 |
| 30 Oct | t21_top_at_11 | 49,589,822,592 | 387,423,207 | 387,420,489.0 ± 19,283 | z +0.141 |
| 30 Oct | t21_top_at_17 | 49,589,822,592 | 387,446,324 | 387,420,489.0 ± 19,283 | z +1.340 |
| 30 Oct | t21_pool60c (can, gasp, chest, hood, voice, exhaust) | 93,312,000,000 | 728,994,018 | 729,000,000.0 ± 26,442 | z −0.226 |

There are 24 z-scores. Their mean is +0.081 and the largest is |z| 2.793 (`t21_slot1_line`, discussed in
REPORT §2). The `silent` lead is [ASSUMED], with no position evidence.

**Passphrase passes on `t21_readme54`: 20 passes, all exact.** The BIP39 checksum ignores the passphrase, so
every pass must give `t21_readme54`'s 387,425,296, and all 20 do.

| passes | list |
|---|---|
| 8 | BREATHE-type: `breathe_pw.txt` (24–25 Oct) |
| 10 | black / BLM / silent: `black_pw.txt` (25–26 Oct) |
| 2 | Tuesday, tuesday: `tuesday_pw.txt` (26–27 Oct) |

The queues used 119.8 h of GPU over 28 steps. Total GPU time since 14 Oct, el22 included, is about 374 h
(15.6 days).

## 4. Safety and machine

- **HIT lines.** There are 0 in all 28 queue logs and 0 in `electrum_rerun.log`. No phrase was ever printed,
  read or stored.
- **Thermal.** There was one pause in the whole period. On 30 Oct at 14:06:45 there was a 20 s pause at 91 °C,
  21 s after `t21_top_at_11` started, caused by a start-up clock boost. The solver resumed from its checkpoint
  with no loss. Otherwise it ran at 86–89 °C, capped at 1,605–1,650 MHz.
- **Speeds.** BIP39 ran at 10.5–11.7M candidates/s. el22 (Electrum) ran at 17.0–19.3M/s, faster at night.
- **Hold and hand-off.** Every queue started on its predecessor's `QUEUE DONE`. el22 was never interrupted after
  27 Oct.
- **Publication.** Nothing was pushed. There are 54 local commits after `073834d`. `pre_push_check.sh` prints
  BLOCK, which is the intended state: pattern 0, private deny-list 0, phrase guard 656.

## 5. Ledger (tally2.py)

- **Now.** There are 50 EVIDENCED runs, giving **284,280,833,673 derivations**, or 287,144,978,142 with the
  twelve asserted runs.
- **Not yet admitted.** These are 16 finished, in-band BIP39 runs: idx2, pool60, slot1, food7, pool57v, the ten
  top configs, and pool60c.
- **What admitting them would do.** Admitted as boxes, they would add 696,691,118,306 candidates against a naive
  1,137,081,394,658. The inter-box term is 440,390,276,352. The evidenced figure would go to
  **289,723,733,035** (+5,442,899,362) and the combined figure to 292,587,877,504. The marginal of the twelve
  would be unchanged at 2,864,144,469, and the CPU-days would be 8,383 / 8,466.
- **Not in tally2.** The 21-word ledger does not carry the Electrum runs (el21_rev, el22) or the passphrase
  passes.

## 6. Open decisions (owner / Mohammed)

1. **Admit the 16 runs to the ledger.** This would move the headline to 289,723,733,035.
2. **Record el22 in REPORT §2.6.** It is 22-word Electrum, exhausted on this template, with the segment-3 score.
3. **el21 with the 52 normalized Electrum passphrases.** Still open and unscheduled, about 7.7 GPU-days.
4. **Exact-blob allow-list for the pre-push check.** On hold until a decision to publish.
5. **Next GPU work.** The GPU is idle.
