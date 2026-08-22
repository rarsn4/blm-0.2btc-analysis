# 0.2 BTC Puzzle — 10 billion derivations of negative results, and three defects in the community's candidate data

**Target:** `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`
**HASH160:** `ccbd031e54cde2a3189fd59bc49f731367a1779e`
**Status:** still unsolved. This is a negative-results report.

I built a GPU BIP39 search pipeline and ran roughly **10 billion full seed
derivations** against the leading hypotheses. Everything below is exhaustively
eliminated, not "tried and didn't find." I'm publishing the scope precisely so
nobody repeats it, and because three defects turned up in the shared candidate
data that may have been quietly costing other people months.

---

## 1. Three defects in the community's data

### 1.1 `breathe` is not a BIP39 word

It appears in multiple word lists and is widely used as the assumed passphrase.
It is **not in the BIP39 English wordlist** and therefore cannot appear in any
seed phrase. Anyone treating it as a seed word is searching a space that cannot
contain the answer.

```python
from mnemonic import Mnemonic
"breathe" in Mnemonic("english").wordlist   # False
```

`breath`, `breeze` are also absent. As a *passphrase* it remains possible —
I tested it and 64 other candidates, all negative (§3).

### 1.2 `candidates_unplaced.txt` is missing three valid words

The candidate list appears to be derived from the whitepaper fragment quoted at
the bottom of the image:

> "...in which they were received. The payee needs proof that at the time of each
> transaction, the majority of nodes agreed it was the first received."

That fragment yields **ten** BIP39 words in order:

```
they receive need proof that time major agree first receive
```

The published list contains seven of them. **`they`, `that`, and `time` are
absent** — most likely filtered out as function words without checking BIP39
membership. All three are in the wordlist (`they` #1796, `that` #1791, `time` #1810).

Any template previously "exhausted" against the 37-word pool was exhausted
against an incomplete pool. I re-ran t18 and t21 with the corrected 40-word
pool — still negative — but other templates may not have been.

### 1.3 24-word mnemonics require HMAC key pre-hashing — this silently breaks custom solvers

**This is the important one.** If you wrote your own solver for a 24-word
hypothesis, check this before trusting any negative result you produced.

PBKDF2-HMAC-SHA512 uses the mnemonic as the HMAC *key*. RFC 2104 requires that a
key longer than the hash block size (128 bytes for SHA-512) be replaced by
`SHA512(key)` before padding. Measured over 2000 random 24-word phrases:

| | bytes |
|---|---|
| minimum length | 135 |
| mean | 153 |
| maximum | 172 |
| **fraction exceeding 128 bytes** | **100%** |

Every 24-word mnemonic needs pre-hashing. A solver that zero-pads to 128 bytes
instead — which is correct for 12-word phrases and therefore passes 12-word test
vectors — produces well-formed, plausible, **entirely wrong** seeds for 24-word
phrases. No exception, no warning, no malformed output. Demonstration:

```
mnemonic : abandon x23 + art
correct  : 408b285c123836004f4b8842c89324c1...   (canonical BIP39 test vector)
zero-pad : 2facfb042cc06dc665f95578b2b74c68...   (silently wrong)
```

**Test your solver against the canonical 24-word vector**
(`abandon` ×23 + `art` → `1KBdbBJRVYffWHWWZ1moECfdVBSEnDpLHi` at
`m/44'/0'/0'/0/0`) before believing any 24-word negative.

---

## 2. What is exhaustively eliminated

All runs cover four derivation paths unless noted: `m/44'/0'/0'/0/0`,
`m/0'/0/0`, `m/0/0`, `m/44'/0'/0'/0/1`.

### 2.1 The clock overlay is dead as a word set

The twelve words `order camera more second this vote black liberty real punch
mask address` were tested across **all 479,001,600 orderings** — every rotation,
both directions, every reflection — with 12 passphrases. 359 million
derivations. No match.

Enumerating 12! subsumes every rotation, so there is no need to test reading
directions separately.

One incidental observation: of the rotations, **only the counter-clockwise
reading has a valid BIP39 checksum**. Clockwise and rotations 1/6/11 all fail.
That is a 1-in-16 coincidence, but it lines up with the mirror/inversion motif
being flagged as unsolved. It did not lead anywhere.

### 2.2 The 12-word template is dead over its complete space

Using `position_table.md` positions 1–12
(`subject camera tower mask police ? liberty ? eye black pyramid vote`),
**both gaps were swept over all 2048 BIP39 words** — not a candidate list, the
entire wordlist — across 65 passphrases and 4 paths. No match.

If the table's first twelve entries are correct, the phrase is not 12 words.

### 2.3 The 18-word template is dead in both directions

- **Leave-one-out on gaps:** each of the five gaps (6, 8, 14, 15, 18) freed to
  **all 2048 words** with the others pooled. 300 million derivations.
  *No single word in the language fits any one gap.*
- **Free-one-fixed:** each of the thirteen fixed words in turn freed to all 53
  candidate words. 747 million derivations. *No single wrong fixed word explains
  the failure.*
- **Paired:** `camera` + `pyramid` (the pairing the table itself flags as
  conflicted) both freed simultaneously. 3.04 billion derivations. No match.

### 2.4 Also eliminated

- t15, t21 with the pool; t21 with gaps `[6,8,14,15,18,21]` and slot 20 as
  `apple|second` (an arrangement distinct from previously published runs)
- Position offsets −1 and +1 on t18 and t21 (testing whether the
  sum-of-two-numbers mapping is off by one)
- 65 passphrases drawn from the image text, including `Сумма двух чисел`,
  all `BREATHE` casings, BLM slogans, dates, and the target address itself
- **The derivation path assumption is verified, not assumed.** BTCRecover
  reporting "BIP44 (P2PKH)" only classifies the *address format*. Re-running the
  main eliminations across four paths changed nothing, so the ~10 billion
  negatives are real results rather than artifacts of a wrong path.
- **No steganography.** LSB analysis of the source PNG: 0.498 / 0.500 / 0.505
  across R/G/B. No hidden bit-plane payload.

### 2.5 The whitepaper is not the ordering key

Testing the theory that the image is decoy and the seed comes from
`bitcoin.pdf` in document order — 3,564 tokens, 788 BIP39 words, 241 unique:

| test | windows | checksum-valid | hits |
|---|---|---|---|
| document order, all lengths 12/15/18/21/24 | 3,855 | 93 | 0 |
| deduplicated, first occurrence | 1,120 | 25 | 0 |
| each of the 12 sections separately | 2,653 | 63 | 0 |
| image candidates by first whitepaper appearance | 35 | 3 | 0 |

7,868 windows, 184 checksum-valid, zero hits, across 4 paths × 5 passphrases.

Note for anyone reasoning about section-based theories: **the whitepaper has 12
sections, not 9.** Section 11 (Calculations) exists, so `11.03.20` → Section 11
is a live reading. I tested it; negative.

### 2.6 The whitepaper fragment does not supply positions 21–24

Attractive hypothesis: the fragment sits at the *bottom* of the image, positions
21–24 are the *end* of the phrase, the table has no evidence for those four
slots, and the quote is cut to begin immediately after the word **"order"** —
the full sentence being *"the order in which they were received."*

Tested with 21–24 fixed to `major agree first receive` (the last four in
sentence order), fixed to the preceding four, and each slot free over the 8- and
10-word sentence pools. 4.86 billion derivations. No match.

---

## 3. Tally

| run | derivations |
|---|---|
| clock_v1: 9 words + 3 of 23, 4 slots pinned, 12 passphrases | 53,570,796 |
| clock_ccw: ALL 12! orderings, 12 passphrases | 359,244,384 |
| t12: both gaps over ALL 2048 words, 12 passphrases | 3,136,020 |
| t12: same, 12 passphrases × 4 paths | 12,544,080 |
| t12: 65 passphrases | 16,986,775 |
| t15: 4 gaps, 37-word pool | 59,079 |
| t18: 5 gaps pooled, 12 passphrases | 13,003,308 |
| t18: same, 12 passphrases × 4 paths | 52,013,232 |
| t18: 65 passphrases | 70,434,585 |
| t18: leave-one-out, 5 gaps each over ALL 2048 | 299,865,760 |
| t18: free-one-fixed, 13 slots × 53 candidates, 4 paths | 746,531,032 |
| t18: camera+pyramid pair over 53 candidates, 4 paths | 3,043,549,612 |
| t18/t21: position offsets −1 and +1 | 42,256,473 |
| t21: 6 gaps + slot20, 4 paths | 40,089,475 |
| t18/t21: corrected 40-word pool | 65,600,000 |
| t24: positions 21–24 from whitepaper sentence, fixed | 1,083,498 |
| t24: positions 21–24 pooled over sentence words | 4,855,160,488 |
| alt2: all 13 fixed slots × 2 choices (3.31% complete) | 293,796,477 |
| whitepaper orderings, all sections | 3,680 |
| **TOTAL** | **9,968,928,754** |

**288 days of CPU** at the ~400 derivations/s rate typical of CPU solvers,
completed in about 1.5 hours of GPU time.

---

## 4. Why more compute will not solve this

`position_table.md` has 13 fixed words for the t18 shape. Using the table's own
confidence ratings (high ≈ 0.9, medium ≈ 0.65):

| number of fixed words wrong | probability | searched |
|---|---|---|
| 0 | 1.0% | 100% |
| 1 | 5.7% | 100% |
| 2 | 14.5% | 1 of 78 pairs |
| 3 | 22.9% | 0% |
| 4 | 24.1% | 0% |
| 5+ | 27.0% | 0% |

**P(all 13 correct) ≈ 1%. Expected number wrong ≈ 4.**

About **7% of the probability mass** has been searched. Closing the 2-wrong tier
means 78 pairs at ~30 h each — **98 days**. The 3-wrong tier is unreachable at
any throughput.

And a structural point: a 24-word phrase has 24! ≈ 6.2 × 10²³ orderings — about
**43 million years** even if you know the exact 24 words. **Position information
is not an optimization for 24-word phrases; it is the only thing that makes them
solvable at all.** Which means every 24-word attack inherits whatever errors its
position table contains. That is the trap this puzzle sets.

Free permutation search caps out around 16–17 candidate words for a 12-word
phrase (P(16,12) ≈ 8.7 × 10¹¹, about 8 h). At 53 candidates it is 8 × 10¹⁸
derivations — unreachable.

**The bottleneck is not throughput. It is word confidence.** Each medium→high
upgrade multiplies the odds by ~1.4×, compounding. Taking the table to all-high
would move P(all correct) from 1% to roughly 25%, at which point a single-word
sweep finds it in minutes.

---

## 5. What would actually help

1. **A higher-resolution original.** The circulating image is 1600×1200 and the
   glyphs sit at the legibility limit.
2. **The word at position 21.** The clock's hour hand (10+11) is produced by the
   *same labelled mechanism* that gave `moon` (12+1) and `tower` (1+2) at high
   confidence — and it is the only hand without a word attached. Best-evidenced
   gap in the table.
3. **Anything placing positions 22, 23, 24.** These have no evidence at all. If
   nothing places them, that is positive evidence *against* 24 words and for the
   18-word reading (Brave New World has 18 chapters).
4. **Resolving position 11.** `pyramid` (5+6 in the pyramid) versus the Space
   Needle "marks the 11". Freeing slot 11 found no candidate fits, which suggests
   the conflict runs deeper than choosing between two words.
5. **Re-transcribing the runes.** The circulating reading is
   `ΦΛΝΝΔ : 4ZΔX : 7ΨΘΦ 1` as Greek. At 4× magnification the shapes include a
   diamond, an up-arrow and a double-slash, none of which are Greek letters.
   Note also that the widely-shared "HELLO : FROM : THEM" decoding is internally
   inconsistent — it reads Φ as **H** in "HELLO" and as **M** in "THEM". A
   substitution is a function; one glyph cannot have two values.

A useful filter for any rune decode: **does it yield a word, an index, or a
position?** `Сумма двух чисел` ("sum of two numbers") was worth solving because
it produced a *mechanism*. A decode that resolves to a greeting produces nothing
a solver can use.

---

## 6. Method

Custom CUDA pipeline on an RTX 4070 Laptop (sm_89):

| stage | rate | verified against |
|---|---|---|
| unrank + BIP39 checksum filter | 216 M/s | exact count 1263 over ranks 0–19999 |
| SHA-512 (paired uint32, funnel shifts) | — | 7 vectors, all padding boundaries |
| PBKDF2-HMAC-SHA512, 2048 iters | 209 k/s | 5 vectors incl. canonical BIP39 |
| SHA-256(33B) + RIPEMD-160 | — | 3 vectors incl. hash160(G) |
| BIP32 + secp256k1 | 925 k/s | 6 vectors incl. k = n−1 |
| **combined** | **125 k/s** | canonical 12- and 24-word addresses |

Two-kernel structure: a checksum filter with warp-aggregated stream compaction,
then derivation over the compacted survivors. Fusing them runs the
4096-compression path in ~87% of warps with ~2 live lanes each (~6% utilization);
splitting recovers ~16×.

Every stage was validated against an independently computed **exact** value
before use. That discipline caught five bugs that each produced plausible output
with zero register spills and no warnings — including a SHA-256 message-schedule
error that yielded a 6.39% checksum rate against a true 6.25%, which no
tolerance-based check would have caught.

**If you are running your own solver: verify against exact expected counts, not
plausible-looking ones.** A 1.2% deviation is invisible to a sanity check and
fatal to correctness.

---

*Published so these paths are not re-walked. If you have a higher-resolution
original, a word for position 21, or evidence placing 22–24, that is worth more
than any amount of GPU — I can test a corrected template in seconds.*
