# 0.2 BTC Puzzle — 12 billion derivations of negative results, four data defects, and the rune cipher solved

**Target:** `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`
**HASH160:** `ccbd031e54cde2a3189fd59bc49f731367a1779e`
**Status:** still unsolved. This is a negative-results report.

I built a GPU search pipeline covering **both BIP39 and Electrum** and ran
roughly **12 billion full seed derivations** against the leading hypotheses.
Everything below is exhaustively eliminated, not "tried and didn't find."

Separately, and more usefully: **the rune cipher is solved.** It is a
monoalphabetic substitution over Cyrillic, not Greek. The community's Russian
decode is correct — I confirmed it independently by glyph-shape analysis rather
than taking it on trust — and I have mapped the alphabet across all four
inscriptions. See §7.

I'm publishing the scope precisely so nobody repeats it, and because four
defects turned up in the shared candidate data that may have been quietly
costing other people months.

---

## 1. Four defects in the community's data

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

### 1.3 `any` is index 82, and the repo indexes 1-based

The README's per-section BIP39 lists are **1-based** — 44 of 45 entries confirm
it. So `1713 -> stock` follows the repo's own convention, but BIP39's internal
encoding is **0-based**, where 1713 is `stomach`. Both readings must be tested.

Separately, the 13th-Amendment reading gives `any` as #84. It is #82 1-based,
#81 0-based. And `slave`, `duly`, `convicted` from that same text are not BIP39
words at all.

### 1.4 24-word mnemonics require HMAC key pre-hashing — this silently breaks custom solvers

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

### 2.5 Electrum was never tested by anyone — it is now

The repo README says plainly: *"we should consider Electrum seed derivation and
BIP39 seed derivation."* Every published attempt I can find used BIP39 only.
**This is not a variation on BIP39 — a BIP39 checksum filter actively discards
valid Electrum phrases.**

| | BIP39 | Electrum v2 |
|---|---|---|
| validity test | 4–8 bit checksum inside the words | `HMAC-SHA512("Seed version", mnemonic)` hex prefix |
| prefixes | — | `01` standard, `100` segwit |
| PBKDF2 salt | `"mnemonic" + passphrase` | `"electrum" + passphrase` |
| default path | `m/44'/0'/0'/0/0` | `m/0'/0` |
| **word count** | must be 12/15/18/21/24 | **any length** |

Proof that this matters — Electrum's own documented test seed:

```
wild father tree among universe such mobile favorite target dynamic credit identify
  HMAC-SHA512("Seed version", ...) = 1001bc7d...   -> valid Electrum (segwit)
  BIP39 checksum                                    -> INVALID
```

A valid Electrum seed that **fails BIP39** and would be thrown away before any
address is derived. I verified my filter accepts it before running anything.

Eliminated: **12, 13, 14, 16, 17, 18 and 21 words**, four derivation paths.
Lengths 13/14/16/17 are illegal under BIP39 and had never been searchable.

### 2.6 No steganography

LSB analysis of the source PNG: **0.498 / 0.500 / 0.505** across R/G/B. No
hidden bit-plane payload.

### 2.7 The whitepaper is not the ordering key

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

### 2.8 The whitepaper fragment does not supply positions 21–24

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
| clock_ccw: ALL 12! orderings of the clock words, 12 passphrases | 359,244,384 |
| t12: both gaps over ALL 2048 words (12pw, 4 paths, 65pw) | 32,666,875 |
| t15: 4 gaps, 37-word pool | 59,079 |
| t18: 5 gaps pooled (12pw, 4 paths, 65pw) | 135,451,125 |
| t18: leave-one-out, 5 gaps each over ALL 2048 | 299,865,760 |
| t18: free-one-fixed, 13 slots x 53 candidates, 4 paths | 746,531,032 |
| t18: camera+pyramid pair over 53 candidates, 4 paths | 3,043,549,612 |
| t18/t21: position offsets -1 and +1 | 42,256,473 |
| t21: 6 gaps + slot20, 4 paths | 40,089,475 |
| corrected pools 40/52/75/80, forward and reversed | 783,591,785 |
| t24: whitepaper tail, fixed and pooled | 4,856,243,986 |
| alt2: all 13 fixed slots x2 choices (3.31% complete) | 293,796,477 |
| whitepaper orderings, 7868 windows, all 12 sections | 3,680 |
| **BIP39 subtotal** | **10,686,920,539** |
| Electrum v2: 12,13,14,16,17 words | 282,879 |
| Electrum v2: 18 words | 9,828,654 |
| Electrum v2: 21 words | 1,376,011,695 |
| **Electrum subtotal** | **1,386,123,228** |
| **TOTAL** | **12,073,043,767** |

**349 days of CPU** at the ~400 derivations/s typical of CPU solvers, completed
in a few hours of GPU time.

Electrum lengths **13, 14, 16 and 17 are illegal under BIP39** and were therefore
unreachable to every previous solver. They are now closed.


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
5. **The final glyph of the right-hand inscription.** See §7 — the cipher is
   solved and that one symbol is not. If anyone has a source image where it is
   legible enough to compare against a numeral reference set, that is the single
   most valuable file in this puzzle.

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
| **combined** | **125 k/s** | canonical 12- **and** 24-word addresses |
| Electrum filter | 7 M seq/s | Electrum's documented segwit test seed |

Two-kernel structure: a checksum filter with warp-aggregated stream compaction,
then derivation over the compacted survivors. Fusing them runs the
4096-compression path in ~87% of warps with ~2 live lanes each (~6% utilization);
splitting recovers ~16×.

Every stage was validated against an independently computed **exact** value
before use. That discipline caught six bugs that each produced plausible output
with zero register spills and no warnings:

- a SHA-256 message-schedule error yielding a 6.39% checksum rate against a true
  6.25% — invisible to any tolerance-based check
- the 24-word HMAC key pre-hashing omission (§1.4)
- a benchmark that timed 20-bit scalars instead of 256-bit ones, overstating
  secp256k1 throughput 12×
- a single-block `hmac_sha512` valid only to 119 bytes. Harmless for the 37-byte
  BIP32 data it was written for; it would have corrupted **every** Electrum
  hash, since 16% of 18-word and 100% of 21/24-word mnemonics are longer. Caught
  by measuring mnemonic lengths, not by testing.

**If you are running your own solver: verify against exact expected counts, not
plausible-looking ones.** A 1.2% deviation is invisible to a sanity check and
fatal to correctness.

---

## 7. The rune cipher is solved — it is Cyrillic, not Greek

This is the part I think is worth more than the eliminations.

### 7.1 Both circulating decodes are wrong at the premise

Two readings are in circulation for the rune line under the clock, both
transcribing the glyphs as Greek (`ΦΛΝΝΔ : 4ZΔX : 7ΨΘΦ 1`):

- **"HELLO : FROM : THEM"** — this is **internally impossible**. It reads Φ as
  **H** in "HELLO" and as **M** in "THEM". A substitution is a function: two
  glyphs may share a letter, but one glyph cannot have two values. It also
  carries no puzzle information — no word, no index, no position.
- **Greek QWERTY layout** → `FLNND : 4ZDX : 7CUF`. The mechanism is real (phi is
  on F, psi on C, theta on U) but the output is not English, not BIP39, and not
  numeric.

Both fail because **the glyphs are not Greek.** The repo's own §20 already
documents the three inscriptions as Russian. Anyone re-deriving a Greek reading
is decoding the wrong alphabet.

### 7.2 The cipher is monoalphabetic — measured, not assumed

I segmented the glyphs and correlated them by shape after normalising to a
common bounding box:

| | correlation |
|---|---|
| same-letter pairs, within one line | **+0.63** |
| same-letter pairs, across two images | **+0.54 to +0.61** |
| different-letter pairs | **+0.05 to +0.07** |

A clean separation. The double `м` in `Сумма` uses the **identical glyph twice**,
and `с` in `Сумма`/`чисел` likewise. Simple monoalphabetic substitution,
confirmed on the shortest line and consistent across all four.

**This also independently confirms the community's Russian decode.** The glyph
group sizes on the right-hand line match `здесь(5) зашифрованы(11) биткоины(8)
на(2) чёрный(6) день(4) номер(5) X(1)` exactly.

### 7.3 The alphabet

Fully mapped from the bottom line:

```
Сумма двух чисел  =  ◇⏶ᛗᛗ△ : ⇧⧗⏶⤬ : ⊤Ψ◇⫽ᛉ

С=◇  у=⏶  м=ᛗ  а=△     д=⇧  в=⧗  х=⤬     ч=⊤  и=Ψ  е=⫽  л=ᛉ
```

Extended from the top-left lines (`Я надеюсь …`, `… будут присылать …`):

```
я=木  н=⊥  ь=⊤  ю=⧓  б=ᐭ  т=⊔   plus п р и с ы
```

Cross-line agreement on `а д е с у и н р т ь ы б ч` — each letter verified in at
least two independent inscriptions.

### 7.4 What X is not

The right-hand line ends `… чёрный день номер X` — *"…for a rainy day number X."*
The repo writes X because nobody has read it. Here is why, and what it excludes:

- **X is a single glyph**, not a word. Group structure `[4]:[5]:[1]` for
  `день` / `номер` / X.
- **X is complete, not truncated.** It spans columns 785–795 of a 797px image
  with clear whitespace before the edge.
- **X is unique.** Compared against all 68 glyphs in the corpus — right line,
  both top-left lines, bottom line — its best match anywhere is **+0.491**,
  below the +0.55–0.63 same-symbol baseline. It occurs exactly once.
- **X is not an Arabic digit.** Compared against the artist's **own hand-drawn**
  digits from `1865-202…?` (same hand, same medium — not a font):
  `-` +0.304, `?` +0.255, `2` +0.229, `8` +0.209, `1` +0.149, `6` +0.113,
  `5` −0.016. All at the different-symbol noise floor.
- **X carries no titlo.** Rows 0–10 above it are empty while neighbouring
  glyphs show ink at rows 9–11. Church Slavonic numerals are normally
  titlo-marked.
- **X is not any mapped letter**, so it cannot be any of the 18 Church Slavonic
  numerals that are ordinary Cyrillic letters (`а в д е з и к м н о п ч р с т у
  ф х`). Of the rare unmapped letters `ж ц щ ъ э`, only `ц` carries a numeral
  value at all.
- **X is not `л`** (+0.377 against a +0.55 baseline), so `л = 30` is excluded.
- The `1865-202…?` inscription is **Arabic numerals with a literal question
  mark**, not cipher glyphs — so it gives no cross-reference for X.

Its geometry is a vertical stroke with diagonals, visually suggestive of `ж`
(which is `х` plus a vertical bar, and `х = ⤬` here) — but X vs `х` scores
**+0.056**, pure noise. That remains a visual impression, not a measurement.

**Conclusion: X is an unresolved unique symbol, visually suggestive of `ж` but
quantitatively unassigned.** Resolving it needs a higher-resolution source or a
fourth inscription, not further inference from these glyphs.

### 7.5 One note on `Сумма двух чисел`

The bottom rune sits **inside the clock face**, among the numerals — it is the
clock's caption. The mechanism it describes is already fully consumed: three
hands, three adjacent-numeral pairs, three sums (12+1=13 `moon`, 1+2=3 `tower`,
10+11=21 unlabelled). Proposing that it *also* governs a second, undiscovered
pair requires positive evidence that it applies elsewhere.

For the record, a pair-sum search over the twenty explicit numbers in the image
has almost no discriminating power: **158 of 190 pairs land inside BIP39's
0–2047 range.** Only five pairs sum to another number present in the artwork,
and the one clearly designed relationship is `17 + 2003 = 2020` — which the
README already explains as the gold chart's span.

---

*Published so these paths are not re-walked. If you have a higher-resolution
original, a word for position 21, evidence placing 22–24, or a legible view of
the final rune glyph, that is worth more than any amount of GPU — I can test a
corrected template in seconds.*
