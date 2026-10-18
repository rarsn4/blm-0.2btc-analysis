# Queue: runs prepared to start after el22 (none started)

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

Total about 22-23 h of GPU time.

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
