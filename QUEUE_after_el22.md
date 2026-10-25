# Queue: prepared runs

*[19 Oct 2026] The owner moved the queue forward: it runs NOW, while el22 is paused at 39.66%, in the order
t21_rev54 -> t21_pool58 -> t21_food11 -> el21_rev -> t21_slot1_line -> t21_alt3, then el22 resumes.
The queue stops on any exit code other than 2. Log: queue_oct19.log, read only with the two HIT-rule greps.*

Owner decides "after el22" or "now". Figures from `queue_prep.py` (output in `queue_prep.out`),
rates measured from free313_boundaries.tsv: BIP39 21-word 11.0-11.6M cand/s, Electrum 18.1-18.5M.
A run is scored only on completion and admitted to EVIDENCED only if in band.

| # | config | candidates | band (survivors) | new vs 42-run union | GPU time |
|---|---|---|---|---|---|
| 1 | t21_slot1_line | 247,949,112,960 | 1,937,102,445.0 ± 43,118 | 70.0% | 5.9-6.3 h |
| 2 | t21_rev54 | 49,589,822,592 | 387,420,489.0 ± 19,606 (binomial: slot 21 pinned) | 100% | 1.2 h |
| 3 | el21_rev | 235,298,000,000 | 976,578,613.3 ± 31,185 | (Electrum; 0 overlap with el21) | 3.5-3.6 h |
| 4 | t21_pool58 | 76,137,385,088 | 594,823,321.0 ± 23,874 | 5.9% | 1.8-1.9 h |
| 5 | t21_alt3 | 396,718,580,736 | 3,099,363,912.0 ± 54,541 | 87.5% | 9.5-10.0 h |
| 6 | t21_food11 | 148,769,467,776 | 1,162,261,467.0 ± 33,399 | see below | 3.6-3.8 h |

Total about 25.5-26.8 h of GPU time.

Overlaps, stated:
- t21_slot1_line vs t21_free1_p1: first/future/predict at slot 1 = 74,384,733,888 candidates (30%),
  covered on m/44'/0'/0'/0/0 ONLY. On the other three paths all five slot-1 words are new.
  trust and this are new on every path. No overlap with t21_readme54 (slot 1 there is `subject`).
- t21_rev54 vs t21_pool52_rev: 52^6 x 2 = 39,541,219,328 (79.74%), but t21_pool52_rev is ASSERTED
  (no log), so against the evidenced ledger t21_rev54 is entirely new.
- t21_pool58 vs t21_readme54: 54^6 x 2 = 49,589,822,592 (65.1%). Beyond that, every candidate with
  exactly one new word at one gap is inside a `loo` run, so only 4,507,641,344 are new. The run
  still processes the full box.
- t21_alt3 vs t21_readme54: 1/8 = 49,589,822,592.
- el21_rev vs el21: 0 (slot 1 of el21_rev is the 70-pool, which does not contain `subject`).
- t21_food11 (SLOT 11 pyramid|food|space): the `pyramid` third (49,589,822,592) is t21_readme54, done on
  4 paths. food/space at 11 were covered only by t21_free11_p1: path 1, slot 20 = `second`, compressed key
  only. New: food/space under `second` on paths 2-4, and food/space under `apple` on all 4 paths.
  (tally2's "33% new" ignores paths.) t21_needle11 has pyramid|eye|tower at 11, so it adds nothing here.

## Queue of 24 Oct 2026 (el22 stopped for it, then resumed)

Owner's order: t21_free20, then t21_readme54 with the BREATHE-type passphrases from pw2.txt
(8 entries, any casing; the list itself is not printed), then el22 resumes. Bands and identity
checks, stated before launch:

| run | candidates | band | identity check | GPU time |
|---|---|---|---|---|
| t21_free20 (slot 20 over 56 words, 4 paths) | 1,388,515,032,576 | 10,847,773,692.0 ± 102,037 | must equal t21_free20_p1's logged 10,847,704,031 (same box; survivors do not depend on paths) | 33-38 h |
| t21_readme54 x 8 passphrases | 8 x 49,589,822,592 | 387,420,489.0 ± 19,283 per pass | every pass must equal t21_readme54's logged 387,425,296 (the BIP39 checksum ignores the passphrase; the counter resets per pass) | about 8 x 72-80 min |

Overlap: t21_free20 is 100% inside t21_free20_p1's box, but that ran on m/44'/0'/0'/0/0 only and
compressed key only; paths 2-4 are new for 54 of the 56 words, and all three key formats are new on
path 1. The apple|second slice (3.57%) is t21_readme54. The 65 pw2.txt passphrases had run only on
the t12/t18 templates; the 8 BREATHE-type entries are new on t21.


## Queue of 25 Oct 2026: two "black" tests, after the 24 Oct queue, before el22 resumes

Bands and identity checks, stated before launch:

| run | candidates | band | identity check | GPU time |
|---|---|---|---|---|
| t21_readme54 x 9 "black" passphrases (black_pw.txt: black, Black, BLACK, the three casings of "black lives matter", blacklivesmatter, BLM, blm; 4 already in pw2.txt but never run on t21) | 9 x 49,589,822,592 | 387,420,489.0 ± 19,283 per pass | every pass must equal t21_readme54's logged 387,425,296 | about 9 x 72-75 min |
| t21_pool55b (t21_readme54 + `black` in the gap pool, 55 words) | 55,361,281,250 | 432,510,009.8 ± 20,378 (stratified, 0.983689) | — | 1.3-1.4 h |

t21_pool55b overlap: 49,589,822,592 is t21_readme54; the 5,509,980,288 with exactly one `black` among the
six gaps are inside the loo runs (each gap over all 2048 words, the rest on the 54-pool; under `second`
those were compressed-key only, so this run adds the other two formats there). Truly new: phrases with
`black` in two or more gaps, 261,478,370 (0.47%), confirmed by tally2 against the 42-run union.
el22 is held (HOLD_EL22) until this queue ends, then resumed by it.

### 25 Oct, later: t21_pool56 replaces t21_pool55b

| run | candidates | band | GPU time |
|---|---|---|---|
| t21_pool56 (t21_readme54 + `black` and `air` in the gap pool, 56 words) | 61,681,958,912 | 481,890,304.0 ± 21,503 (stratified, 0.983411) | 1.5-1.6 h |

Overlap: 49,589,822,592 is t21_readme54; the 11,019,960,576 with exactly one new word (black or air) in
one gap are inside the loo runs; truly new: a new word in two or more gaps, 1,072,175,744 (closed form
and tally2 agree). t21_pool55b's 55,361,281,250 candidates are all inside t21_pool56, so t21_pool55b
is not run separately (it would repeat 1.4 h); its committed band above stays on record, unused.
