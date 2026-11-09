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

### 25 Oct, later: `silent` added (a private lead, [ASSUMED], no position evidence)

| run | candidates | band | GPU time |
|---|---|---|---|
| t21_pool57 (t21_readme54 + `black`, `air`, `silent` in the gap pool, 57 words) | 68,592,894,498 | 535,881,988.3 ± 22,680 (stratified, 0.983564) | 1.6-1.7 h |
| t21_silent4 (t21_readme54 with SLOT 4 silent) | 49,589,822,592 | 387,420,489.0 ± 19,283 (stratified, 0.983533) | 1.2 h |
| t21_readme54 passphrases: `silent` added to black_pw.txt (now 10 entries) | 10 x 49,589,822,592 | per pass as above | +1.2 h |

t21_pool57: readme54 part 49,589,822,592; exactly one new word in one gap 16,529,940,864 (inside the loo
runs); truly new 2,473,131,042 (two or more of the three new words in the gaps; closed form and tally2
agree). It contains all of t21_pool56, which is therefore not run separately.
t21_silent4: no overlap with t21_readme54, t21_free4_p1 or t21_alt3 (t21_alt3 already ran on 20 Oct
with SLOT 4 mask|person, so `silent` at 4 gets its own run); entirely new against the 42-run union.

## Queue of 26 Oct 2026: t21_idx2, after the 25 Oct queue, before el22 resumes

| run | candidates | band | GPU time |
|---|---|---|---|
| t21_idx2 (t21_readme54 + 10 index words in the gap pool, 64 words: abandon ability above absent absorb abstract absurd abuse access accident) | 137,438,953,472 | 1,073,741,824.0 ± 31,839 (stratified, 0.975462) | 3.3-3.5 h |

The 10 words are BIP39 numbers 1-12 (clock, buttons, X = 10, VS = 12, 11), counted from 0 and from 1, minus `able`
(already in the pool). None is in any earlier t21 pool (t21_idx, readme54, pool57, free20). The other two words of
that set, `about` and `account`, are only in t21_idx's 80-word pool, and t21_idx is ASSERTED (no log), so they
have no evidenced coverage.
Overlap: readme54 part 49,589,822,592; exactly one new word in one gap 55,099,802,880 (inside the loo runs); truly
new 32,749,328,000 (closed form and tally2 agree). Held by HOLD_EL22_IDX2 until it ends.

### 26 Oct, later: three more runs in the 26 Oct queue (after t21_idx2)

| run | candidates | band | GPU time |
|---|---|---|---|
| t21_colour (t21_readme54 + blue green yellow in the gap pool, 57 words) | 68,592,894,498 | 535,881,988.3 ± 22,673 (stratified, 0.983283) | 1.6-1.8 h |
| t21_title1 (SLOT 1 welcome\|brave\|world; subject removed) | 148,769,467,776 | 1,162,261,467.0 ± 33,399 (stratified, 0.983533) | 3.6-3.9 h |
| t21_readme54 x 2 passphrases (Tuesday, tuesday) | 2 x 49,589,822,592 | 387,420,489.0 ± 19,283 per pass; each pass must equal 387,425,296 | 2.4-2.6 h |

blue, green and yellow are BIP39 (red and white are not; black is in t21_pool57); none is in the pool or a slot list of any of the 66 t21 configs. t21_colour truly new: 2,473,131,042 (two or more colour words in the gaps; closed form and tally2 agree).
t21_title1 overlap: t21_free1_p1 has welcome and world at slot 1 under `second`, 49,589,822,592 (33.3%), on m/44'/0'/0'/0/0 only; t21_swap114 0 (it has subject at slot 14); t21_readme54 0. brave at slot 1 is new on every path.
Tuesday: not in pw2.txt in any casing (count 0); not a BIP39 word, so passphrase only; also run on the CPU (t12full_mp, el12-el17).

### 26 Oct, later: t21_black1 (t21_title1's band was already committed, so it stays as it is)

| run | candidates | band | GPU time |
|---|---|---|---|
| t21_black1 (t21_readme54 with SLOT 1 black, subject removed; black stays at slot 10) | 49,589,822,592 | 387,420,489.0 ± 19,283 (stratified, 0.983533) | 1.2-1.3 h |

None of the 68 t21 configs allowed black at slot 1 (black has been tested at slot 10, in all six gaps via the loo
runs and t21_pool55b/56/57, and as a passphrase). Overlap with t21_readme54, t21_free1_p1, t21_swap114 and
t21_title1: 0; entirely new against the 42-run union.

### 26 Oct, later: t21_glass (t21_colour's band was already committed, so it stays as it is)

| run | candidates | band | GPU time |
|---|---|---|---|
| t21_glass (t21_readme54 + glass doctor in the gap pool, 56 words) | 61,681,958,912 | 481,890,304.0 ± 21,506 (stratified, 0.983554) | 1.5-1.6 h |

Source: the first of the four masked people (top left) wears glasses; a weak lead with no number. glass and doctor
are BIP39 and in none of the 69 t21 configs (pool or slot list) nor in any passphrase list. Overlap: readme54 part
49,589,822,592; exactly one new word in one gap 11,019,960,576 (inside the loo runs); truly new 1,072,175,744
(closed form and tally2 agree).

### 26 Oct, later: t21_food1 and t21_food7 (t21_title1's band was already committed, so it stays as it is)

| run | candidates | band | GPU time |
|---|---|---|---|
| t21_food1 (t21_readme54 with SLOT 1 food, subject removed) | 49,589,822,592 | 387,420,489.0 ± 19,283 (stratified, 0.983533) | 1.2-1.3 h |
| t21_food7 (t21_readme54 with SLOT 7 food, liberty removed) | 49,589,822,592 | 387,420,489.0 ± 19,283 (stratified, 0.983533) | 1.2-1.3 h |

Source (reviewer's reading, not re-measured here): "FOOD" written sideways at the bottom of the Space Needle's inner
column, under 6 dark marks: 1st from the bottom, 7th from the top. In the forward template food was possible at
slot 1 or 7 only in t21_free1_p1 / t21_free7_p1 (path 1, slot 20 = second): overlap 24,794,911,296 (50%) each, on
m/44'/0'/0'/0/0 only. The reversed templates (t21_pool52_rev, t21_rev54) and t21_swap114 also allow food at
slot 1 but are different layouts (0 overlap). New: the apple half on all 4 paths, the second half on paths 2-4.

## 26 Oct, consolidated (Mohammed): replaces this morning's additions

The 26 Oct queue is now: t21_idx2, t21_pool60, t21_slot1, t21_food7, t21_readme54 x Tuesday/tuesday.
Kept as committed: t21_idx2, t21_food7, the Tuesday passes. Dropped (bands stay on record, unused), because each is a
strict subset of a consolidated run: t21_colour and t21_glass (inside t21_pool60); t21_title1, t21_black1 and
t21_food1 (inside t21_slot1).

| run | candidates | band | GPU time |
|---|---|---|---|
| t21_pool60 (t21_readme54 + blue green yellow glass doctor top in the gap pool, 60 words) | 93,312,000,000 | 729,000,000.0 ± 26,428 (stratified, 0.982658) | 2.2-2.5 h |
| t21_slot1 (SLOT 1 welcome\|brave\|world\|black\|food\|top; subject removed) | 297,538,935,552 | 2,324,522,934.0 ± 47,234 (stratified, 0.983533) | 7.1-7.9 h |

Words: top is BIP39 (stop is not). blue, green, yellow, glass, doctor and top were never in an earlier t21 pool or
slot list. At slot 1, brave, black and top were never possible; welcome, world and food only in t21_free1_p1 (path 1,
second) and t21_swap114 (a different layout, 0 overlap).
t21_pool60: readme54 part 49,589,822,592; exactly one new word in one gap 33,059,881,728 (loo runs); new
10,662,295,680 (closed form and tally2 agree).
t21_slot1: overlap with t21_free1_p1 74,384,733,888 (25%, welcome/world/food under second, path 1 only); t21_swap114
0; new, paths not modelled, 223,154,201,664 (closed form and tally2 agree).

## el22, third segment: resumed 27 Oct 2026 13:48:00 UTC, band fixed before any count is read
Resumed by run_queue_oct26.sh after QUEUE DONE, from 12,236,361,826,304 = 3,256 chunks (74.29%); el22_segments.tsv
has the resume row. The survivor counter restarts on resume, so the segment is scored on its own:
segment = 16,470,860,000,000 - 12,236,361,826,304 = 4,234,498,173,696 candidates (Electrum, 22 words, binomial at 17/4096)
band 17,574,821,521.7 +/- 132,295. Wall time 63.5-65.1 h at 18.06-18.53M cand/s: ends Fri 30 Oct, about 05:15-07:00 UTC.
[Corrected 27 Oct 20:15 UTC: the wall time above used 18.06-18.53M cand/s, which is not el22's rate. el22's own
rate is 16.96M/s over its 20-24 Oct segment (wall time) and 16.98M/s over this one (checkpoint boundaries,
13:51-20:07). At 76.64% on 27 Oct 20:07 it ends Fri 30 Oct about 11:00-11:45 UTC. The band is unaffected.]
Score from the segment's final 'exhausted, no match' line only after exit=2. HIT rule: electrum_rerun.log read only with
grep -c '^HIT[[:space:]]+index' and grep '^exit='; an Electrum hit is verified with an Electrum v2 implementation.

## Queue after el22 (run_queue_oct30.sh): t21_pool57v, starts only when el22 ends with exit=2
Committed before launch, 27 Oct 2026. virus (the drawn COVID-19 vial), hour (the clock), mirror (the mirror-written
seal) added to t21_readme54's gap pool, 57 words. All three are BIP39 (#1957, #883, #1133). None is in a POOL, SLOT or
EXTRA line of any of the 75 t21 configs; they appear only in comments and, like every word, in the leave-one-out
runs' @FULL gap slots (6, 8, 14, 15, 18, 21).

| config | candidates | band (survivors) | GPU time |
|---|---|---|---|
| t21_pool57v (t21_readme54 + virus hour mirror in the gap pool, 57 words, 4 paths) | 68,592,894,498 = 57^6 x 2 | 535,881,988.3 +/- 22,660 (stratified, 0.982721) | 1.64-1.73 h |

Overlaps: t21_readme54 49,589,822,592 (72.30%, 4 shared paths), and the same readme54 core with t21_pool57, t21_pool58,
t21_pool60 and t21_idx2 (different extra words). Exactly one new word in exactly one gap, 16,529,940,864, is covered
by the leave-one-out family (loo6/8/14/15/18 under second, the five _apple mirrors under apple, loo21 both).
New = 68,592,894,498 - 49,589,822,592 - 16,529,940,864 = 2,473,131,042 (two or more new words in the gaps);
tally2 against the 50-run EVIDENCED union gives the same 2,473,131,042.

## "top" batch (run_queue_oct30b.sh): after t21_pool57v, starts only on its QUEUE DONE
Committed before launch, 28 Oct 2026. Source: the S of STOP is outside the frame line, so the word inside reads
T-fist-P = `top` (BIP39 #1832); `stop` is not BIP39. No position evidence; slot 6 from the flag's 50-44 star
deficit is [ASSUMED]. Configs written from t21_readme54.conf by exact-line substitution, 4 paths each. Before this
batch `top` is in two lists only: t21_pool60's gap pool and t21_slot1's slot 1.

| config | change from t21_readme54 | candidates | band (survivors) | GPU time |
|---|---|---|---|---|
| t21_top20 | SLOT 20 top (apple, second removed) | 24,794,911,296 = 54^6 | 193,710,244.5 +/- 13,635 (stratified, 0.983533) | 0.6 h |
| t21_top6_loo8 | SLOT 6 top, SLOT 8 @FULL | 34,828,517,376 = 2048 x 54^4 x 2 | 272,097,792.0 +/- 16,160 (stratified, 0.983533) | 0.8-0.9 h |
| t21_top6_loo14 | SLOT 6 top, SLOT 14 @FULL | 34,828,517,376 | 272,097,792.0 +/- 16,160 | 0.8-0.9 h |
| t21_top6_loo15 | SLOT 6 top, SLOT 15 @FULL | 34,828,517,376 | 272,097,792.0 +/- 16,160 | 0.8-0.9 h |
| t21_top6_loo18 | SLOT 6 top, SLOT 18 @FULL | 34,828,517,376 | 272,097,792.0 +/- 16,160 | 0.8-0.9 h |
| t21_top6_loo21 | SLOT 6 top, SLOT 21 @FULL | 34,828,517,376 | must equal 272,097,792 exactly (34,828,517,376 / 128, remainder 0) | 0.8-0.9 h |
| t21_top_at_7 | SLOT 7 top (liberty removed) | 49,589,822,592 = 54^6 x 2 | 387,420,489.0 +/- 19,283 (stratified, 0.983533) | 1.2 h |
| t21_top_at_9 | SLOT 9 top (eye removed) | 49,589,822,592 | 387,420,489.0 +/- 19,283 | 1.2 h |
| t21_top_at_11 | SLOT 11 top (pyramid removed) | 49,589,822,592 | 387,420,489.0 +/- 19,283 | 1.2 h |
| t21_top_at_17 | SLOT 17 top (gold removed) | 49,589,822,592 | 387,420,489.0 +/- 19,283 | 1.2 h |

Batch: 397,296,788,544 candidates, 9.5-10.0 h at 11.0-11.6M cand/s.
Overlaps (union, not sum):
- t21_readme54 and t21_slot1: 0 with every config (slot 6 / 7 / 9 / 11 / 17 / 20 differ from readme54; t21_slot1 has
  top at slot 1 and drops subject, and every config here keeps subject at slot 1).
- t21_pool60: 0 with t21_top20 and t21_top_at_*; 1,020,366,720 = 60 x 54^4 x 2 with each t21_top6_loo* (top at 6 is
  in pool60's gap pool).
- t21_loo6 and t21_loo6_apple (slot 6 @FULL): 459,165,024 = 54^5 each with each t21_top6_loo*: the common core, top
  at 6 with every other gap on the 54-pool, 54^5 x 2 = 918,330,048.
- Within the batch: the five t21_top6_loo* share only that core, so their union is
  5 x 34,828,517,376 - 4 x 918,330,048 = 170,469,266,688; t21_top20 and t21_top_at_* overlap nothing in the batch.
- New against the 50-run EVIDENCED union: t21_top20 and each t21_top_at_* 100%; each t21_top6_loo* 33,910,187,328
  (97.36%). Batch: 397,296,788,544 - 3,673,320,192 (within the batch) - 918,330,048 (the core, in loo6 + loo6_apple)
  = 392,705,138,304, closed form and tally2 agree. With the finished but unadmitted t21_pool60, t21_slot1, t21_idx2
  and t21_food7 also counted: 392,194,954,944 (pool60 covers 6 x 54^4 x 2 = 102,036,672 more per t21_top6_loo*).

## t21_pool60c (run_queue_oct30c.sh): after the "top" batch, starts only on its QUEUE DONE
Committed before launch, 28 Oct 2026. can gasp chest hood voice exhaust added to t21_readme54's gap pool, 60 words.
Source: "I can't BREATHE" on the hoodie (can), and breathing words by association [ASSUMED, no position evidence].
All six are BIP39 (#264, #770, #317, #875, #1964, #636). In an earlier t21 POOL, SLOT or EXTRA line: only `can`, in
t21_ink10x20's slot 10 list (13 words); gasp, chest, hood, voice and exhaust in none of the 86 t21 configs. Like every
word, each was covered alone in one gap by the leave-one-out runs' @FULL slots.

| config | candidates | band (survivors) | GPU time |
|---|---|---|---|
| t21_pool60c (t21_readme54 + can gasp chest hood voice exhaust in the gap pool, 60 words, 4 paths) | 93,312,000,000 = 60^6 x 2 | 729,000,000.0 +/- 26,442 (stratified, 0.983192) | 2.2-2.4 h |

Overlaps: t21_readme54 49,589,822,592 (53.14%, 4 shared paths), the same core with t21_pool60, t21_pool57,
t21_pool57v, t21_idx2 and t21_ink10x20 (`can` sits at slot 10 there, in the gaps here); 0 with the top batch.
Exactly one new word in exactly one gap, 6 x 6 x 54^5 x 2 = 33,059,881,728, is in the leave-one-out family.
New = 93,312,000,000 - 49,589,822,592 - 33,059,881,728 = 10,662,295,680; tally2 against the 50-run EVIDENCED union agrees.

## el22 RESULT (30 Oct 2026): exhausted, no match; third segment in band
Gate applied as the owner set it on 27 Oct: grep -E '^exit=' shows `exit=2 Fri 30 Oct 04:55:56 UTC  END el22
wall=227275.70s` for the segment resumed 27 Oct 13:48:00 (13:48:00 + 227,275.70 s = 04:55:55), and the HIT count is 0.
Only then was the one permitted line read: `exhausted, no match  (survivors 17574712922 of 16470860000000)`.
Third segment, 4,234,498,173,696 candidates: survivors 17,574,712,922 against 17,574,821,521.7 +/- 132,295,
deviation -108,599.7, z -0.821, in band. Segment rate 18.63M cand/s (wall time).
Coverage of the whole space rests on the segment chain in el22_segments.tsv, not on a survivor count: start 0
(14 Oct) -> stop 6,531,571,515,392 = 1,738 chunks (18 Oct, exit=143) -> resume at the same index (20 Oct) -> stop
12,236,361,826,304 = 3,256 chunks (24 Oct, exit=143) -> resume at the same index (27 Oct) -> exit=2 at the end.
Both stops are chunk-aligned and each resume index equals the stop index. The survivor counter restarts on resume, so
the first two segments (39.66% and 34.64% of the space) have no survivor count; the band test covers the third
(25.71%) only.

## Three batches of 31 Oct 2026 (run_queue_oct31.sh): clock rotations, black-as-digit, this@3
Committed before launch. 15 configs, 21 words, 4 paths each, 49,589,822,592 candidates each (= 54^6 x 2, the
t21_readme54 space), 18.8 GPU-h total at 11.0M cand/s (17.8 h at 11.6M). Every one is a strict permutation or
transposition of t21_readme54's slot map, which is WHY the space and band are identical to it.

Band for all 15: 387,420,489.0 survivors, sigma 19,283 (stratified, 0.983533 x binomial) -- EXCEPT t21_clk9, whose
sigma is 19,606 (binomial): it pins `tower` at slot 21, so slot 21 is no longer @POOL and the stratified model does
not apply. Same mu either way, because the space is the same.

Overlaps: ZERO, for every pair and against everything already run. Each config pins a different word at a different
slot, so the boxes are disjoint. New against the 50-run EVIDENCED union: 743,847,338,880 = 100%. New against
EVIDENCED plus the 16 finished-but-unadmitted runs: the same 743,847,338,880. Batch own union = naive sum, inter-box
term 0 (closed form and tally2 agree).

### Batch 1: the eight clock rotations (t21_clk2..t21_clk9)
Reason, stated on the canvas: the rune caption under the clock decodes to `Сумма двух чисел`, "sum of two numbers",
and each hand sits between two numerals which are added -- the mechanism that gives moon@13 (12+1), tower@3 (1+2) and
the empty slot 21 (10+11). WHICH numerals a hand sits between depends on which way is up, and that has never been
tested. Of the 12 orientations, 3 are impossible (they need slot 23, past a 21-word phrase) and 1 is the painted one,
leaving these 8. [ASSUMED] orientation: no evidence selects a rotation.
SWAP construction, as instructed: a strict permutation of the involved slots {3, 13, s, m}, so the space is unchanged.
The drop construction was NOT built (it would be 152 GPU-days each, 3.3 GPU-years for the batch).

| config | rot | moon -> | tower -> | hour hand names | permutation |
|---|---|---|---|---|---|
| t21_clk2 |  60° | 5 | 7 | 13 | 3:police 5:moon 7:tower 13:liberty |
| t21_clk3 |  90° | 7 | 9 | 3 | 3:liberty 7:moon 9:tower 13:eye |
| t21_clk4 | 120° | 9 | 11 | 5 | 3:eye 9:moon 11:tower 13:pyramid |
| t21_clk5 | 150° | 11 | 13 | 7 | 3:pyramid 11:moon 13:tower |
| t21_clk6 | 180° | 13 | 15 | 9 | 3:@POOL 15:tower (moon stays at 13) |
| t21_clk7 | 210° | 15 | 17 | 11 | 3:@POOL 13:gold 15:moon 17:tower |
| t21_clk8 | 240° | 17 | 19 | 13 | 3:gold 13:glove 17:moon 19:tower |
| t21_clk9 | 270° | 19 | 21 | 15 | 3:glove 13:@POOL 19:moon 21:tower |

Two are worth naming. t21_clk6 (180°, upside down) keeps moon at 13 and moves tower to 15: an upside-down clock agrees
with the template on one word and contradicts it on the other. t21_clk9 (270°) puts `tower` at slot 21 -- the slot the
hour hand currently names and leaves empty, and REPORT section 6's open item "a word for slot 21". This is NOT covered
by t21_loo21, which swept all 2048 words at 21 while tower still sat at 3; here slot 3 is vacated instead.

### Batch 2: black as a single digit (t21_blackd2,3,4,5,7,9)
Reason, stated on the canvas: the right-edge rune line reads `чёрный день номер X` -- "black day number X". X is the
single glyph nobody can read; REPORT 7.4 concludes a key is missing, not that the image needs upscaling. So black's
slot is whatever digit X is, and one glyph is one digit. Slot 10 is only one reading of X, and REPORT 2.17 already
rates black@10 as resting on that unreadable glyph. Digits 1, 6 and 8 are already tested (t21_slot1 covers black@1 as
one of six words at slot 1; t21_black6 and t21_black8 are evidenced), leaving 2, 3, 4, 5, 7, 9.
Each is a transposition with slot 10, which takes the displaced word: 2<->camera, 3<->tower, 4<->mask, 5<->police,
7<->liberty, 9<->eye. [ASSUMED] digit value.

### Batch 3: t21_this3
`this` at slot 3, tower removed. Reason: `this` is the ONLY repeated BIP39 word in the display text of the master
image -- 3 occurrences (word_census.tsv, 30 Oct; nothing else in section A exceeds 1 except non-BIP39 function words).
THIS CONTRADICTS tower@3, and tower@3 is one of the three best-supported assignments in the whole template: tower is
WRITTEN on the minute hand and the clock caption supplies its slot (REPORT 2.17). Repetition in the display text is
not a position argument. This run CLOSES the repeated-word idea; it does not back it. [ASSUMED].

## t21_single (after the 31 Oct rotation batch): the single-numeral reading
Committed before launch, 31 Oct 2026. t21_readme54 with SLOT 4 `eye` and SLOT 6 `pyramid`; slots 9 and 11 vacated
to the 54-word gap pool. eye and pyramid are MOVED, not duplicated; `mask` is dropped from slot 4.

| config | candidates | band (survivors) | gaps | GPU time |
|---|---|---|---|---|
| t21_single (4 paths) | 2,677,850,419,968 = 54^7 x 2 | 20,920,706,406.0 +/- 141,701 (stratified, 0.983533) | 7 | 64.1-67.6 h = 2.82 GPU-days |

NOTE THE COST. This is not a 1.3-hour run like the rotation batch. Filling slot 6 while vacating 9 and 11 is a NET
GAIN of one gap, so the space is 54^7 x 2, fifty-four times t21_readme54.

Reason: reads the clock overlap as the SINGLE numeral an object sits on (eye on numeral 4, pyramid on numeral 6)
rather than the sum of the pair.

THREE OBJECTIONS, recorded because this run CLOSES the idea rather than backing it:
1. It contradicts the canvas caption `Сумма двух чисел`, "sum of two numbers", which states the mechanism outright.
2. It contradicts tower@3 and moon@13, which only work as SUMS of a numeral pair. Those are the template's
   best-supported assignments, and the 31 Oct measurement confirms both from hand directions lying within 1.4 deg
   of a numeral midpoint.
3. The same measurement puts the pyramid on numerals 5 and 6 almost equally -- 52.7% vs 52.3% ink over the numeral
   box -- so choosing 6 over 5 has no basis in the pixels.

COVERAGE: never run before. Overlap is ZERO with t21_loo6, t21_free9_p1, t21_free11_p1, t21_free11 and
t21_readme54, and new against the 50-run EVIDENCED union is the full 2,677,850,419,968 = 100%. The reason is slot 4:
every one of those keeps `mask` there, and this config puts `eye` there, so the boxes are disjoint at that slot
alone. t21_loo6 sweeps slot 6 over all 2048 words (so it does include pyramid@6) but still holds mask@4, eye@9 and
pyramid@11, which is a different joint placement.

## t21_nose2 (after t21_single): slot 2 = nose
Committed before launch, 1 Nov 2026. t21_readme54 with SLOT 2 `nose`, camera removed. 4 paths.
49,589,822,592 candidates, band 387,420,489.0 +/- 19,283 (stratified, 0.983533), 1.19 GPU-h, 100% new.

REASON: slot 2 is rated weak in REPORT 2.17 -- `camera` rests on a COUNT, and 2.17 records the even slots
2/4/10/12/16/20 as ink-supported: NONE.
NOT the stated reason: the claim that a digit "2" is drawn near the bust's neck was MEASURED FALSE on 1 Nov. The
band scores -0.009 against the artist's own `1` from 1865 and about zero against every other digit
(three_object_measurement.md addendum). The 1 Nov face measurement also found Liberty's nose UNEXAGGERATED
(nose/face-width 0.333 vs the real statue's 0.450, with the eye undersized alongside it), so there is no image
evidence for the word `nose` either. [ASSUMED], no position evidence. `nose` is BIP39 #1204.

SKIPPED as already covered: food@1. t21_slot1 carries SLOT 1 `welcome|brave|world|black|food|top` and ran on
26-27 Oct (survivors 2,324,505,174, z -0.376), so `food` at slot 1 on all four paths is done.

## PROPOSED, NOT STARTED: close free-one-fixed on paths 2-4 (the REPORT 2.13 [SCOPE] gap)
Priced 1 Nov 2026 from the 31 Oct batch's own 15 wall times: 10.62-11.92M cand/s, mean 11.58M, 4 paths.
AWAITING THE OWNER'S CONFIRMATION OF COST. Bands are committed here; nothing is queued.

Twelve slots are still free-one-fixed on path 1 only: 1, 2, 4, 5, 7, 9, 10, 11, 12, 16, 17, 19. (Of the thirteen
in 2.13's [SCOPE] note, slot 20 was closed by t21_free20 on 24-25 Oct.)

Each config is the 4-path twin of its t21_freeN_p1: identical word box, identical candidate count,
1,363,720,121,280 = 54^6 x 55 (the freed slot takes 55 words; slot 20 stays pinned to `second`).
Band for every one: 10,654,063,447.5 +/- 101,122 (stratified).

IDENTITY, not just a band. Survivors do not depend on the derivation path, so each run MUST reproduce its _p1
counterpart's logged count EXACTLY, exactly as t21_free20 reproduced t21_free20_p1's 10,847,704,031:

| config | must equal | | config | must equal |
|---|---|---|---|---|
| t21_free1 | 10,654,092,960 | | t21_free10 | 10,654,089,154 |
| t21_free2 | 10,653,915,344 | | t21_free11 | 10,654,060,452 |
| t21_free4 | 10,654,138,418 | | t21_free12 | 10,654,012,263 |
| t21_free5 | 10,654,060,538 | | t21_free16 | 10,653,972,836 |
| t21_free7 | 10,653,988,011 | | t21_free17 | 10,653,994,687 |
| t21_free9 | 10,654,207,551 | | t21_free19 | 10,654,167,169 |

COST: 16,364,641,455,360 candidates total.
  4-path configs (as built): 16.4 GPU-days at the mean, range 15.9-17.8 days.
  paths 2-4 only (3-path): T3/T4 = 0.891 from the solver's own model (T4/T1 = 1.484 -> P = 5.198X), so 14.6
  GPU-days -- saves 1.8 days and loses the path-1 control. Recommend the 4-path version.
This is close to REPORT 2.13's own estimate of 377 h ~ 15.7 days for thirteen slots, which is a useful check.

THE LEDGER GAINS NOTHING: new candidates against the 50-run EVIDENCED union = **0**. tally2 counts word boxes and
does not model paths, and every one of these boxes is already in the union via its _p1 twin. What 16.4 GPU-days
buys is the WORD "exhausted": REPORT 2.13's [SCOPE] note says a one-path run does not exhaust its box over the
path set, and that on paths 2-4 a single wrong assigned word is still open at twelve of the fifteen slots. This
run closes that, and with it the a=1 branch's 8.3% of probability mass, which is currently closed on path 1 only.

PROPOSED ORDER, weakest-supported slot first, so the most likely slots are tested earliest:
  1. t21_free11  slot 11 -- 2.17 reports it fits NOTHING; the only slot already tested and failed
  2. t21_free2   slot 2  -- count-only, ink-supported NONE
  3. t21_free4   slot 4  -- count-only, ink-supported NONE
  4. t21_free12  slot 12 -- association only (the .VS. ambigram)
  5. t21_free16  slot 16 -- count-only (the 16 of M16)
  6. t21_free17  slot 17 -- inferred from the chart, both word and slot
  7. t21_free10  slot 10 -- rests on the unreadable glyph X
  8. t21_free19  slot 19 -- count-only (the 19 of CVD19)
  9. t21_free9   slot 9  -- depicted, pyramid 4+5
 10. t21_free5   slot 5  -- depicted, "line five" convention used nowhere else
 11. t21_free7   slot 7  -- depicted, crown points
 12. t21_free1   slot 1  -- `subject` is WRITTEN in the Amendment copy and carries the one underline; strongest
                            of the twelve, so last

---

## Brainwallet CASE axis — banded 2 Nov 2026, BEFORE launch

Reordered **ahead** of the 12-config paths-2-4 closure on the owner's instruction.
The closure is not cancelled: `run_queue_nov.sh` now waits on `queue_brain.log` instead
of `queue_single.log`, so it follows behind unchanged.

**Why it jumped the queue.** `CASE` appears in **1 of 225 configs** in this project and
is set to `lower`. `upper` and `title` have never been run, once, while the artwork is in
capitals and SHA-256 is case-sensitive (§2.12 states the limitation; it was never closed).

**[RETRACTED, 2 Nov 2026, same day]** ~~As-written = `upper`, measured not assumed.~~
Withdrawn. `slogan_lines.py` **normalises casing**: it renders the plinth as `ONLY REAL
BITCOIN` where the pixels read `ONLY real BITCOIN`. Measured from the image, three strings
are mixed-case as drawn — `ONLY real BITCOIN`, `I can't BREATHE`, and the bottom Latin line
`Esse quam niger es, sic dixit caccabus ollae`, which carries one capital and is otherwise
entirely lowercase. The artwork is not "in capitals". See `casing_measurement.md`.

**`CASE upper` is one uniform capitalisation hypothesis among three, not the as-written
reading.** The runs and their cost are UNCHANGED, because "as-written" is *undefined* for
this corpus: `brain_t21_*` builds phrases from the 65-word pool in template slot order, a
sequence nobody ever wrote, so there is no drawn casing to reproduce and a fourth mode
would have nothing to encode. The mixed-case strings that are drawn belong to the
image-text corpus, which already tests them as drawn
(`brain_image_corpus.py:172` includes the as-drawn `base`). No third run, no new cost.

**The casing machinery is verified before use.** `--selftest-brain` passes all 26
known-answer vectors, of which **16–23 cover `upper` and `title` explicitly**
(upper/title × compressed/uncompressed × space/no-space). Run on this binary, 2 Nov 2026.

### Bands — an IDENTITY, not a z-score

A brainwallet has no checksum, so every candidate derives and acceptance is **exactly
1.0**. Both configs:

| | |
|---|---|
| candidates | 65⁶ × 2 = **150,837,781,250** (7 gaps: six `@POOL` + slot 20's two words) |
| survivors | **must equal 150,837,781,250 exactly** |
| acceptance | **1.000000000** |
| addresses | 452,513,343,750 (×3: compressed, uncompressed, hybrid) |
| scalar mults | 1 per candidate (one case bit) |

Space confirmed by the solver itself, not by my arithmetic:
`--count-only` prints `space=150837781250  expected derivations=150837781250` for both.

**Acceptance below 1.0 voids the negative** — it means work was silently dropped — so the
queue STOPS on a miss rather than recording a result. Same control §2.12 calls
load-bearing for the `CASE lower` twin.

### Cost, stated before launch

| run | candidates | cost | basis |
|---|---|---|---|
| `brain_t21_upper` | 150,837,781,250 | **16.2 GPU-h** | 2,582,308 cand/s, measured on the `CASE lower` twin, 2026-09-29 |
| `brain_t21_title` | 150,837,781,250 | **16.2 GPU-h** | same |
| **total new work** | | **32.5 GPU-h = 1.35 days** | |

`CASE lower` is already done (§2.12, 16.23 h, exhausted), so "all three casings" costs
32.5 h of *new* compute, not 48.7.

> **[SCOPE] This is 1.35 days, not "about a day" as budgeted.** Stated rather than
> rounded down. Two further reasons the figure may run long: the rate is from
> 29 Sep, and the GPU has since been in *continuous* SW thermal slowdown
> (`0x20` on 360 of 360 samples, 85–88 °C), so expect 17–19 h each.
> `touch HOLD_BRAIN_title` stops `title` before it starts without touching `upper`.

**Inherited narrowing, NOT closed here:** key variants are `sha256` + space-joined only —
3 addresses per candidate, one quarter of the key-variant space the t18 figure covered.
An `_all` run is what closes that.

**Ledger effect: 0 new candidates admitted.** `tally2.py` counts mnemonic derivations;
these are brainwallet keys, a different object, and §2.12 reports them separately.

## t12full_mp (9 Nov 2026): making §2.2 evidenced instead of asserted

Committed before launch, 9 Nov 2026. **Bands first, then the run.** Self-test gate PASS
(cached) on `solver2_jac` sha256 `2cace98f30d1`, the same bytes as the stamp of
2026-11-02T06:58:13Z.

Why: §2.2 claims the 12-word template is dead over its complete space, but it has NO LOG
anywhere, `t12` appears 0 times in `tally2.py`, and whatever ran predates the 28 Sep
three-encoding change. It reads as [EXHAUSTED] under §0 and rests on prose. The space is
4,194,304 candidates -- under a second of GPU -- so it is cheaper to earn than to caveat.
This does NOT touch the 69-day queue; `t21_free2` keeps running.

### The band model, stated before the numbers

`t12full_mp.conf` holds slot 12 = `vote` **PINNED**, with slots 6 and 8 `@FULL` over all
2048. So the 4-bit checksum is a **filter, not an identity** -- rule 4's third case,
binomial, p = 1/16. It is **not** stratified: stratification arises when the checksum-
bearing slot is a restricted pool, and here the entropy bits vary fully.

```
candidates   2048^2                      = 4,194,304
mu           candidates / 16             =   262,144
sigma        sqrt(4194304 * (1/16)(15/16)) =      495.74
band         262,144 +/- 496  (1 sigma); admit if |z| < 3
```

Independent support for the binomial model, measured before this run: the CPU subset in
`t12_family_check.py` enumerated 10,240 phrases of this same space and found **616
checksum-valid against 640 expected, z -0.98**.

| config | candidates | band (survivors) | ledger derivations (cand/16) | keys derived | paths |
|---|---|---|---|---|---|
| t12full_mp, empty passphrase | 4,194,304 | 262,144 +/- 496 | 262,144 | 3,145,728 | 4 |
| t12full_mp + pw2.txt, 65 passphrases | 4,194,304 | 262,144 +/- 496 | 262,144 | 204,472,320 | 4 |

`keys derived` = survivors x 4 paths x 3 encodings (`derive_multi3`), and x 65 for the
second row. The ledger's `derivations` column is candidates/16 and does not multiply by
paths or encodings, which is the convention every other row in `tally2.py` uses.

### pw2.txt, and a check fixed before running

`pw2.txt` sha256 `a60f9ef34ebe85a6a586fd3876b6c04806d19fb0d582ee04ac14e1e2ccf08c73`,
**65 lines, of which line 1 is EMPTY** -- so the empty passphrase is one of the 65 and
the first row above is a strict subset of the second.

A passphrase does not affect BIP39 checksum validity, only seed derivation, so the
survivor count must be **identical** across both rows. Pre-registered accordingly:

- if the counter reports per phrase-space, run B's survivors must equal run A's exactly;
- if it reports cumulatively, run B's survivors must equal **exactly 65 x run A's**.

Either way the equality is **exact, not statistical**, and a mismatch means the
passphrase loop is not doing what the config says -- which is the §1.9 failure mode and
would be reported before anything else runs.

### Decision rule

In band -> admit both to `EVIDENCED` in `tally2.py` as a 12-word box with its own
divisor (16), kept separate from the 21-word union and floored separately, the way the
24-word tail already is. Out of band, or HIT count non-zero, or the exact equality above
failing -> **stop and report before anything else**. HIT lines read only with
`grep -c -E '^HIT[[:space:]]+index'`.

---

## Old Electrum, `breathe` at two positions — PRE-REGISTERED 9 Nov 2026, NOT YET RUN

Committed before the candidate list was built and before anything was derived. Written in
this order deliberately: the membership test below is a wordlist lookup, not an
enumeration, so it ran first in order to state an exact candidate count here. No seed has
been derived.

### Why this scheme and not BIP39

`breathe` is **not a BIP39 word** — 0 matches in `configs/bip39_en.txt` — so a seed
requiring it at two positions **cannot be BIP39 at any length**. It *is* in the
old-Electrum list, line 245 of 1,626 (`configs/electrum_old_en.txt`). Old Electrum is
therefore the only scheme in which the hypothesis is even expressible, and it is the one
scheme the external ledger (`Desalzes/bnw-0.2btc-analysis`) closed **without compute** —
its own words, *"settled by reasoning and CPU checks; no GPU run, nothing in the ledger."*
Nothing in their repository requires `breathe` at two positions; they use it as a
passphrase, a "25th word", or at a single slot.

Both occurrences are **measured** in our own census, at the coordinates it records:
`census_crops.py:94` hoodie line `(900, 240, 300, 180)`, `census_crops.py:97` bust neck
band `(1355, 528, 75, 17)`.

### The membership test, run before pricing  [MEASURED]

Census words that are in the 1,626-word old-Electrum list:

| census section | distinct words | in the old-Electrum list |
|---|---:|---:|
| `A_display` (measured) | 110 | **32** |
| `B_microtext` (a SAMPLE, not a census — see `word_census.py`) | 41 | 6 |
| union | 144 | 37 |

The 32 from `A_display`: `any`, `been`, `black`, `brave`, `breathe`, `crime`, `end`,
`except`, `exist`, `find`, `first`, `future`, `matter`, `moon`, `more`, `neither`, `new`,
`only`, `order`, `party`, `pay`, `peace`, `picture`, `place`, `real`, `shall`, `stop`,
`subject`, `tower`, `welcome`, `within`, `world`. Excluding `breathe` itself leaves a
**31-word pool** for the other ten positions.

**It is 32, not a handful.** That matters, because it makes the full hypothesis far too
large to run — see the pricing.

### THE BAND IS AN IDENTITY, and a stronger one than "no checksum" implies

Old Electrum is usually described as having no checksum, so that every word combination is
a valid seed. **Our own implementation records that this is not exactly true**
(`old_electrum.py` header): each 3-word group encodes `x < 1626^3 = 4,299,816,375`, and
`'%08x'` overflows to nine hex digits when `x >= 2^32`, which Electrum rejects as
not-a-seed. The surviving fraction is `(2^32 / 1626^3)^4 = 99.55%`.

So the correct pre-registration is **not** `survivors = candidates`. It is better than a
band and better than a statistical identity:

> **Validity is deterministic per candidate and computable in advance.** For any specified
> candidate list, the exact number of valid old-Electrum seeds is counted by testing each
> candidate's four groups for `x < 2^32`, with no derivation. That count is fixed and
> written down BEFORE the run. The run must report **exactly** that number.
>
> **No sigma and no z.** This is the same shape as `t21_top6_loo21`, where slot 21 `@FULL`
> made survivors an exact identity rather than a binomial draw — rule 4.
>
> **Any other survivor count is a machine fault and VOIDS the run.** Not a surprising
> result, a broken tool. This is exactly the role §2.12's acceptance identity plays for
> brainwallets: a brainwallet has no checksum, so acceptance below 1.0 means work was
> silently dropped, the negative does not stand, and nothing is recorded.

### Pricing  [MEASURED, 9 Nov 2026]

Measured cost of our deriver, timed on throwaway word lists through the real
`from_words` path: **106.5 ms per candidate, 9.4 candidates/s.** The 100,000-round SHA256
stretch dominates; there is no GPU path for this scheme and no checksum filter to reduce
the work, so candidates and derivations are 1:1.

**"Checksumless means seconds" does not survive the combinatorics.** The absence of a
1/128 filter is swamped by a per-candidate cost about five orders of magnitude above a
BIP39 derivation in the GPU pipeline.

| shape | candidates | at 9.4/s |
|---|---:|---:|
| **Tier 1.** Ten others FIXED in one order; `breathe` swept over all `C(12,2)` position pairs | **66** | **7 s** |
| **Tier 2.** Ten others permuted, `breathe` positions fixed: `10!` | 3,628,800 | **4.5 CPU-days** |
| **Tier 3.** Full `12!/2!` — `breathe` twice plus ten fixed others, every ordering | 239,500,800 | **295 CPU-days** |
| The actual hypothesis: *which* ten of the 31, times Tier 3 — `C(31,10) = 44,352,165` sets | ~1.06e16 | not runnable |

### What is authorised here

**Tier 1 only, and nothing else.** 66 candidates, about 7 seconds, on the CPU, touching no
GPU and not the queue. Tiers 2 and 3 are priced here so the decision is on the record; they
are **not** authorised and should not be started without a separate committed band.

Pre-conditions, all of which must hold before the first derivation:

1. `python3 old_electrum.py selftest` prints **ALL PASS**. Ran 9 Nov 2026: ALL PASS,
   including the planted-hit test and the two negative controls (the KAT seed against the
   real target gives no hit; against its own h160 it does).
2. The exact valid-candidate count for the 66 is computed and written into this section
   **before** deriving.
3. Target blob per rule 8: the bytes compared must equal
   `ccbd031e54cde2a3189fd59bc49f731367a1779e`, never the word-swapped
   `1e03bdcca3e2cd549bd59f1813739fc49e77a167`.

### Decision rule

Survivor count exactly the pre-computed valid count, and 0 hits → record as **TESTED**,
not EXHAUSTED: 66 candidates is one ordering of one word set, and says nothing about the
other 44 million sets. Admitted to `tally2.py` only if it ever becomes a box worth
carrying, which at Tier 1 it is not — it is a probe.

Any other survivor count → **VOID, stop and report before anything else runs.** Hit count
read only with the format-agnostic detection rule in `DO_NOT_PUSH`; on a nonzero count,
the HIT protocol applies and nothing else happens first.
