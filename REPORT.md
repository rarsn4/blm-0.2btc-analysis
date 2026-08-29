# 0.2 BTC Puzzle — the rune cipher solved, 24.7 billion derivations eliminated, and six defects in the shared data

**Target:** `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`
**HASH160:** `ccbd031e54cde2a3189fd59bc49f731367a1779e`

**Status:** the Bitcoin puzzle is **NOT solved.** The address has received
20,107,284 sats across 5 transactions and spent zero — verified on-chain,
untouched since May 2020.

What **is** solved is the **rune cipher**, except for a single glyph. Those are
different claims and this report keeps them separate throughout.

I built a GPU search pipeline covering both BIP39 and Electrum and ran
**24,767,853,989 full seed derivations** — 717 days of CPU at typical solver
rates. Everything in §2 is exhaustively eliminated, not "tried and didn't find."

Code, configs and every hypothesis tested:
https://github.com/rarsn4/blm-0.2btc-analysis

---

## 1. Six defects in the shared data

### 1.1 `breathe` is not a BIP39 word

It appears in circulating word lists and is the widely-assumed passphrase. It is
**not in the BIP39 English wordlist** and cannot appear in any seed phrase.

```python
from mnemonic import Mnemonic
"breathe" in Mnemonic("english").wordlist   # False
```

`breath` is also absent. As a *passphrase* it remains possible — tested, along
with 64 others, negative (§2.4).

### 1.2 `candidates_unplaced.txt` is missing three valid words

The list appears to derive from the whitepaper fragment quoted at the bottom of
the image. That fragment yields **ten** BIP39 words in order:

```
they receive need proof that time major agree first receive
```

The published list has seven. **`they`, `that` and `time` are absent** —
presumably filtered as function words without checking membership. All three
are valid (`they` #1796, `that` #1791, `time` #1810, 1-based).

### 1.3 `any` is #82, and the repo indexes 1-based

The README's per-section BIP39 indices are **1-based** — 44 of 45 confirm it.
BIP39's own encoding is **0-based**, so `1713 → stock` follows the repo's
convention while the spec gives `stomach`. Both need testing.

The 13th-Amendment reading gives `any` as #84; it is **#82** 1-based, #81
0-based. `slave`, `duly` and `convicted` from the same text are not BIP39 at all.

### 1.4 A whole phrase is missing from the "BRAVE NEW WORLD" micro-text

Section 14 of the README documents only letter-level typos (`introdue`,
`participans`, `doudle`, `sing`, `abcense`). It misses that an entire phrase is
absent.

Inside the **E of BRAVE**, the micro-text reads:

> common solution / is to introdue / cent / ral au / thority / or mint that /
> checks every / transac / tion / for double spen / ding. After

The whitepaper reads:

> A common solution is to introduce **a trusted** central authority, or mint,
> that checks every transaction for double spending.

**"a trusted" is absent.** Note the typo `introdue` sits exactly at the splice.
Whether this is deliberate or the same carelessness that produced the other
typos is open — but `trust` (#1870) was tested at every gap and pinned at slot
21, negative (§2.7).

### 1.5 The `.VS.` ambigram flips **vertically**, not horizontally

Confirmed by direct extraction: mirrored across the **horizontal axis**,
`.VS.` renders as a clean `·12·`. It is a deliberate ambigram.

This is a **slot marker**, not a phrase length. Reading it as "the seed is 12
words" is likely the single most common wrong turn in this puzzle (§5).

### 1.6 24-word mnemonics require HMAC key pre-hashing — this silently breaks solvers

**Check this before trusting any 24-word negative you have produced.**

PBKDF2-HMAC-SHA512 uses the mnemonic as the HMAC *key*. RFC 2104 requires a key
longer than the 128-byte block be replaced by `SHA512(key)`. Measured over 2000
random 24-word phrases:

| | bytes |
|---|---|
| minimum | 135 |
| mean | 153 |
| maximum | 172 |
| **fraction exceeding 128 bytes** | **100%** |

A solver that zero-pads instead is **correct for 12 words** — it passes every
12-word test vector — and derives well-formed, plausible, **entirely wrong**
seeds for 24 words. No error, no malformed output.

```
abandon x23 + art
correct  : 408b285c123836004f4b8842c89324c1...
zero-pad : 2facfb042cc06dc665f95578b2b74c68...
```

Canonical check: `abandon` ×23 + `art` → `1KBdbBJRVYffWHWWZ1moECfdVBSEnDpLHi`
at `m/44'/0'/0'/0/0`.

---

## 2. What is exhaustively eliminated

All runs cover four derivation paths unless noted.

### 2.1 The clock overlay is dead as a word set

The twelve words `order camera more second this vote black liberty real punch
mask address` across **all 479,001,600 orderings** — every rotation, both
directions, every reflection — with 12 passphrases. 359 million derivations.

Enumerating 12! subsumes every rotation; reading directions need no separate test.

### 2.2 The 12-word template is dead over its complete space

Positions 1–12 of the position table with **both gaps swept over all 2048 BIP39
words** — not a candidate list, the entire wordlist — across 65 passphrases and
4 paths.

### 2.3 The 18-word template is dead in both directions

- **Leave-one-out:** each of the five gaps freed to **all 2048 words** with the
  others pooled. 300 M derivations. *No single word in the language fits any one
  gap.*
- **Free-one-fixed:** each of the thirteen fixed words freed to all 53
  candidates. 747 M derivations. *No single wrong fixed word explains it.*
- **Paired:** `camera` + `pyramid` — the pairing the table itself flags as
  conflicted — both freed. 3.04 B derivations.

### 2.4 Also eliminated

- t15 and t21 across pools of 37, 40, 52, 61, 67, 69, 71, 75 and 80 words
- Template reversal (slot order) for t18 and t21
- Position offsets −1 and +1
- 65 passphrases from the image text, including `Сумма двух чисел`, all
  `BREATHE` casings, BLM slogans, dates, and the target address itself
- The gold-chart y-axis values as BIP39 indices — `1800 1600 1400 1200 1000 800
  600 400 200` → `thought side puzzle nominee language glue enough cradle body`
  (1-based, all nine correct), tested both as an exclusive gap pool and merged
  into the 52-word pool

### 2.5 Every derivation path in the standard gap limit

This was a live assumption underneath every other result. Now closed:

- `m/44'/0'/0'/0/0` through `/19` — the full BIP44 gap limit
- change chain `m/44'/0'/0'/1/0`, `/1`
- accounts `m/44'/0'/1'/0/0`, `m/44'/0'/2'/0/0`
- bare BIP32 `m/0/0`, `m/0/1`, `m/0/2`, `m/0'/0/0`, `m/0'/0/1`, `m/0'/0/2`

`m/49'` and `m/84'` are excluded by the address format — they produce `3…` and
`bc1…`, and the target is legacy `1…`.

### 2.6 Electrum v2 — never tested by anyone before this

The repo README says "we should consider Electrum seed derivation and BIP39 seed
derivation." Every published attempt used BIP39 only. **A BIP39 checksum filter
actively discards valid Electrum phrases.**

| | BIP39 | Electrum v2 |
|---|---|---|
| validity | 4–8 bit checksum in the words | `HMAC-SHA512("Seed version", mnemonic)` prefix |
| prefixes | — | `01` standard, `100` segwit |
| PBKDF2 salt | `"mnemonic" + passphrase` | `"electrum" + passphrase` |
| default path | `m/44'/0'/0'/0/0` | `m/0'/0` |
| **word count** | 12/15/18/21/24 only | **any length** |

Proof it matters — Electrum's own documented seed:

```
wild father tree among universe such mobile favorite target dynamic credit identify
  HMAC-SHA512("Seed version", ...) = 1001bc7d...   -> valid Electrum (segwit)
  BIP39 checksum                                    -> INVALID
```

A valid Electrum seed that fails BIP39 and would be discarded before any address
is derived. My filter was verified to accept it before any run.

Eliminated: **12, 13, 14, 16, 17, 18 and 21 words**, four paths, plus 65
passphrases and the all-slots-vary sweep. Lengths 13/14/16/17 are illegal under
BIP39 and had never been searchable by anyone.

### 2.7 The all-slots-vary sweep — both schemes

The strongest structural test in the project. All 13 fixed words varied
**simultaneously** across 8,192 combinations of {table word, alternative}, with
the gaps pooled:

```
subject|section  camera|twin  tower|clock   mask|face    police|order
liberty|torch    eye|pyramid  black|night   pyramid|space
vote|debate      moon|month   rifle|gun     gold|price
```

This covers 0, 1, 2 … 13 wrong words at once rather than one tier at a time.
Run under **BIP39** (8.88 B derivations) and **Electrum v2** (3.32 B). Both
exhausted.

Also tested: `trust` pinned at slot 21 — the blank clock hand — with pools of 52
and 69 words. Negative. The two manufactured absences (the unlabelled hand and
the deleted "a trusted") do not combine this way.

### 2.8 Two wordlists are impossible, not merely untested

- **Electrum v1** (1626-word list): seven of the fifteen fixed table words do
  not exist in it — `camera`, `police`, `liberty`, `pyramid`, `vote`, `rifle`,
  `gold`. So does `food`. No v1 seed on this table is possible regardless of
  derivation.
- **Russian BIP39**: nine of twenty core words have no Russian equivalent —
  `camera`, `mask`, `black`, `vote`, `rifle`, `gold`, `real`, `world`, `proof`.
  The table cannot be translated. (Russian is also not in the official BIP-39
  spec; it is a community addition.)

Both die at the vocabulary stage, before any algorithm needs implementing.

### 2.9 The image is closed

- **No steganography.** LSB across R/G/B: 0.498 / 0.500 / 0.505.
- **No hidden layer.** The PNG is RGBA; alpha is fully opaque, zero non-opaque
  pixels.
- **No JPEG history.** 8×8 block-edge ratio 0.985 / 0.910 — never compressed.
- **No metadata.** Chunks are `IHDR`, `sBIT`, `IDAT` only.
- **No larger source exists.** `i.redd.it/n1x7g8ceaur51.png` serves 1600×1200,
  md5 `7710323461a924987eb35c77055e59f6`, byte-identical to the circulating
  copy. `preview.redd.it` at 2048/3000/4096 returns nothing.

### 2.10 The chain is closed

- **No `OP_RETURN`** in any of the five transactions. No on-chain message.
- **Never spent.** `spent_txo_count: 0`.
- The extra 107,284 sats are three dust payments plus one deliberate 0.001 BTC
  deposit on 2024-12-13.
- **Change address `39rEPyWKE9Ej…` untouched since 2020** — funded once, never
  spent.
- The funding transaction is `version 1`, `locktime 0`, `sequence 0xffffffff` on
  all four P2SH inputs. That rules out Bitcoin Core (v2 + anti-fee-sniping
  locktime) and Electrum (v2 + RBF sequence). It is a **custodial service or
  exchange batcher** — so the funding wallet is not the puzzle wallet and
  reveals nothing about which software produced the seed.

### 2.11 The whitepaper is not the ordering key

3,564 tokens, 788 BIP39 words, 241 unique:

| test | windows | checksum-valid | hits |
|---|---|---|---|
| document order, lengths 12/15/18/21/24 | 3,855 | 93 | 0 |
| deduplicated, first occurrence | 1,120 | 25 | 0 |
| each of the 12 sections separately | 2,653 | 63 | 0 |
| image candidates by first appearance | 35 | 3 | 0 |

For anyone reasoning about section numbers: **the whitepaper has 12 sections,
not 9.** Section 11 (Calculations) exists, so `11.03.20` → Section 11 is a live
reading. Tested; negative.

---

## 3. Tally

See the repository for per-run configs. Summary:

| | derivations |
|---|---|
| BIP39 | 19,420,846,639 |
| Electrum v2 | 5,347,007,350 |
| **TOTAL** | **24,767,853,989** |

**717 days of CPU** at the ~400 derivations/s typical of CPU solvers, completed
in a few days of GPU time on an RTX 4070 Laptop.

---

## 4. Why more compute will not solve this

The position table has 13 fixed words for t18. Using its own confidence ratings
(high ≈ 0.9, medium ≈ 0.65):

**P(all 13 correct) ≈ 1%. Expected number wrong ≈ 4.**

The all-slots-vary sweep (§2.7) covers every combination of {table word, *my*
alternative} — 8,192 of them, in both schemes. It cannot help if the correct
word at any slot is neither.

And there is a harder structural limit. With ~5 candidates across 24 slots the
space is 5²⁴ ≈ 6 × 10¹⁶, and **being right about 23 words out of 24 pays exactly
nothing** — there is no way to test a partial answer. Candidate lists cannot
converge. Every slot must be pinned to one word by reasoning.

Scale, for contrast:

- 12-word free permutation over 16 candidates: P(16,12) ≈ 8.7 × 10¹¹ — 8 hours
- over 53 candidates: 8 × 10¹⁸ — unreachable
- 24-word, exact words known, order unknown: 24! ≈ 6.2 × 10²³ — **43 million
  years**

**Position information is not an optimization for long phrases; it is the only
thing that makes them solvable.** Which means every 24-word attack inherits
whatever errors its position table contains.

---

## 5. The length argument

The clock is a position machine. Measured rather than eyeballed: all three hands
sit midway between two adjacent numerals, within ~1.5°.

| hand | between | sum | label |
|---|---|---|---|
| seconds | 12 and 1 | **13** | `moon` |
| minutes | 1 and 2 | **3** | `tower` |
| hours | 10 and 11 | **21** | *(blank)* |

The runes beneath decode to `Сумма двух чисел` — "sum of two numbers" — stating
the mechanic outright. The `.VS.` ambigram adds a fourth: slot **12** → `vote`.

**The clock is not mirrored.** Reading the numerals clockwise gives 8→9→10→11→
12→1→2→3, i.e. increasing. A mirrored face would decrease. The digits merely
look odd because they are hand-drawn along the rim. (This refutes a mirroring
correction I proposed earlier, which would have moved the unknown to slot 3.)

Slot 21 therefore exists, and valid BIP39 lengths are 12/15/18/21/24 — so the
phrase is **21 or 24 words**.

There is a second, independent reason it cannot be 12. At 12 words, order is
brute-forceable: 12! = 479,001,600 arrangements, ~29.9 M after the 4-bit
checksum, which is minutes of compute. **If you had the right twelve words you
would not need the clock at all.** An author who built an elaborate
position-marking system did so because order cannot be searched — which is only
true at 21 or 24.

---

## 6. What would actually help

1. **A word for slot 21.** The hour hand is produced by the same labelled
   mechanism that gave `moon` (12+1) and `tower` (1+2) at high confidence, and
   it is the only hand with no word on it. Checked at four contrast settings —
   it is a plain wedge, not faint writing.
2. **Anything placing 22, 23, 24.** These have no evidence at all.
3. **Resolving slot 11.** `pyramid` (5+6 in the pyramid) versus the Space Needle
   "marks the 11". Freeing slot 11 found no candidate fits, which suggests the
   conflict runs deeper than a two-way choice. Note also that the CCTV junction
   box bears a pyramid symbol, visually linking `camera` and `pyramid`.
4. **A genuinely larger source image.** Not a re-upload — see §2.9; the
   circulating file is the original. It would have to come from the artist's own
   export. The `-yi-` signature in the bottom-right corner is the legibility
   benchmark: it is the same physical size as the unresolved glyph.
5. **The final glyph of the right-hand inscription.** See §7.

---

## 7. The rune cipher is solved — it is Cyrillic, not Greek

### 7.1 Both circulating decodes are wrong at the premise

- **"HELLO : FROM : THEM"** is **internally impossible**: it reads Φ as **H** in
  "HELLO" and as **M** in "THEM". A substitution is a function; one glyph cannot
  have two values. It also carries no word, index or position.
- **Greek QWERTY** yields `FLNND : 4ZDX : 7CUF` — a real mechanism, but the
  output is not English, not BIP39, not numeric.

Both fail because the glyphs are **not Greek**.

### 7.2 The cipher is monoalphabetic — measured

Glyphs segmented and correlated after normalising to a common bounding box:

| | correlation |
|---|---|
| same-letter, within one line | **+0.63** |
| same-letter, across two images | **+0.54 to +0.61** |
| different-letter | **+0.05 to +0.07** |

The double `м` in `Сумма` uses the **identical glyph twice**; so does `с` in
`Сумма`/`чисел`. This also **independently confirms** the repo's Russian decode:
the glyph group sizes on the right-hand line match `здесь(5) зашифрованы(11)
биткоины(8) на(2) чёрный(6) день(4) номер(5) X(1)` exactly.

### 7.3 The alphabet

```
Сумма двух чисел  =  ◇⏶ᛗᛗ△ : ⇧⧗⏶⤬ : ⊤Ψ◇⫽ᛉ

С=◇  у=⏶  м=ᛗ  а=△     д=⇧  в=⧗  х=⤬     ч=⊤  и=Ψ  е=⫽  л=ᛉ
```

Extended from the top-left lines (`Я надеюсь …`, `… будут присылать …`):

```
я=木  н=⊥  ь=⊤  ю=⧓  б=ᐭ  т=⊔    plus  п р и с ы
```

Cross-line agreement on `а д е с у и н р т ь ы б ч` — each verified in at least
two independent inscriptions.

### 7.4 The falsification chain for X

The right-hand line ends `… чёрный день номер X`. Ten tests, ten negatives:

| test | result |
|---|---|
| truncated at the image edge? | no — cols 785–795 of 797, whitespace after |
| matches any of 68 corpus glyphs? | no — best +0.491 vs +0.55–0.63 baseline |
| matches the artist's own hand-drawn digits? | no — all at the +0.05 noise floor |
| carries a titlo (numeral marker)? | no — rows 0–10 above are empty |
| is it `л` = 30? | no — +0.377 vs +0.55 baseline |
| any Church-Slavonic numeral that is a mapped letter? | excluded — 18 of 27 are letters X does not match |
| the archaic numerals `ѕ ѳ і ѯ ѱ ѡ`? | no shape match established |
| a rare modern letter `ж ц щ ъ э`? | possible, but only `ц` carries a numeral value |
| does `1865-202…?` share the glyph? | no — that is Arabic numerals and a literal `?` |
| is it `ж` (= `х` + vertical bar, `х = ⤬`)? | visually suggestive; X vs `х` = **+0.056**, noise |

Its geometry is a vertical stroke with diagonals, suggestive of `ж` — recorded
as an observation, not a decoding.

**X matches neither the mapped alphabet, nor the artist's Arabic numerals, nor
the remaining plausible Church-Slavonic numerals, and carries no titlo. It is an
unresolved unique symbol, visually suggestive of `ж` but quantitatively
unassigned.** It occurs exactly once in 68 glyphs, which is *why* it has never
been read.

### 7.5 `Сумма двух чисел` is the clock's caption

The bottom rune sits **inside the clock face**, among the numerals. The
mechanism it describes is fully consumed by the three hands. Proposing a second
application requires positive evidence.

For the record, a pair-sum search over the twenty explicit numbers in the image
has almost no discriminating power: **158 of 190 pairs land inside BIP39's
0–2047 range.** Only five pairs sum to another number present in the artwork,
and the one clearly designed relationship is `17 + 2003 = 2020` — the gold
chart's span, which the README already explains.

---

## 8. Do not use AI upscaling on this image

Generative upscalers invent detail; they do not recover it.

The artist's signature in the bottom-right reads `-yi-` under plain LANCZOS
interpolation. Run through VanceAI at 8×, the same region renders as a boxed
`ER`. The model **replaced** characters it could not read with letterforms it
found more plausible — cleanly, confidently, and wrongly.

Across the rune region, 6.5% of pixels differ by more than 30 levels from a
plain interpolation, with strokes reshaped and terminals sharpened.

**Any reading of X taken from an upscaled image is a reading of the upscaler's
guess.**

---

## 9. Acceptance criteria

So that "solved" means the same thing to everyone:

1. **Consistency.** A candidate plaintext must map every occurrence of each
   glyph to the same letter. One glyph, one value.
2. **X must be independently justified** — not inferred from the answer it
   produces.
3. **It must derive the address.** HASH160
   `ccbd031e54cde2a3189fd59bc49f731367a1779e` under a stated path.
4. **No post-hoc transformations** unless the image independently indicates
   them. "Reduce modulo 2048 because the result was too large" is not a
   mechanism the artwork specifies.
5. **A numerical coincidence is not evidence** unless the image identifies both
   the operands and the operation (§7.5).
6. **Check every candidate word against the wordlist before building on it.**
   Widely-circulated candidate lists contain `breathe`, `stop`, `freedom`,
   `hate`, `white`, `death`, `kill`, `war`, `money`, `buy` and `trusted` — none
   of which are BIP39 words.

---

## 10. Method

Custom CUDA pipeline, RTX 4070 Laptop (sm_89):

| stage | rate | verified against |
|---|---|---|
| unrank + checksum filter | 216 M/s | exact count 1263 over ranks 0–19999 |
| SHA-512 (paired uint32) | — | 7 vectors, all padding boundaries |
| PBKDF2-HMAC-SHA512, 2048 iters | 209 k/s | 5 vectors incl. canonical BIP39 |
| SHA-256(33B) + RIPEMD-160 | — | 3 vectors incl. hash160(G) |
| BIP32 + secp256k1 | 925 k/s | 6 vectors incl. k = n−1 |
| Electrum HMAC filter | 7 M seq/s | Electrum's documented segwit test seed |
| **combined** | **125 k/s** | canonical 12- and 24-word addresses |

Two-kernel structure: checksum filter with warp-aggregated stream compaction,
then derivation over the survivors. Fusing them runs the 4096-compression path
in ~87% of warps with ~2 live lanes each (~6% utilization); splitting recovers
~16×.

**Positive control.** Reproducing a known mnemonic proves little; the solver
must *find* an unknown one. A config blanks two slots of a known phrase to all
2048 words and requires recovery:

```
./solver2 --config selftest_find.conf
HIT   index 2270828
phrase : tiger live melody inject guitar nose route obtain ball diesel snow radar
```

262,144 derivations, `melody` and `snow` recovered. This is what licenses the
negative results.

**Six bugs were caught by exact-value validation**, each producing plausible
output with zero register spills and no warnings:

- a SHA-256 message-schedule error yielding a 6.39% checksum rate against a true
  6.25% — invisible to any tolerance-based check
- the 24-word HMAC key pre-hashing omission (§1.6)
- a benchmark timing 20-bit scalars instead of 256-bit, overstating secp256k1
  throughput 12×
- a single-block `hmac_sha512` valid only to 119 bytes — harmless for the
  37-byte BIP32 data it was written for, fatal for Electrum, since 16% of
  18-word and 100% of 21/24-word mnemonics are longer
- a chunk-sizing assumption that survivor counts are exact rather than binomial
- an incorrect canonical 24-word address recalled rather than computed

**If you run your own solver: validate against exact expected counts, not
plausible-looking ones.** A 1.2% deviation is invisible to a sanity check and
fatal to correctness.

---

*Published so these paths are not re-walked. If you have a word for slot 21,
evidence placing 22–24, a resolution of slot 11, a genuinely larger source
image, or a legible view of the final rune glyph — that is worth more than any
amount of GPU. A corrected template can be tested in seconds.*
