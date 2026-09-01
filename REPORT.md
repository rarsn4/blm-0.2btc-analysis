# 0.2 BTC Puzzle — the rune cipher solved, 25.2 billion derivations eliminated, and six defects in the shared data

**Target:** `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`
**HASH160:** `ccbd031e54cde2a3189fd59bc49f731367a1779e`

**Status:** the Bitcoin puzzle is **NOT solved.** The address has received
20,107,284 sats across 5 transactions and spent zero — verified on-chain,
untouched since May 2020.

What **is** solved is the **rune cipher**, except for a single glyph. Those are
different claims and this report keeps them separate throughout.

I built a GPU search pipeline covering both BIP39 and Electrum and ran
**25,188,563,424 full seed derivations** — 729 days of CPU at typical solver
rates — plus 7,939,492,344 brainwallet addresses counted separately (§2.12).
Everything in §2.1–2.11 is exhaustively eliminated, not "tried and didn't find";
§2.12 is a tested corpus, which is a weaker claim and is marked as such."

Code, configs and every hypothesis tested:
https://github.com/rarsn4/blm-0.2btc-analysis

---

## 0. Epistemic status

Claims below are tagged. Do not promote a tag without new evidence.

| Tag | Meaning |
|---|---|
| **[MEASURED]** | Re-derived from the image, the wordlist, or the chain. Reproducible. |
| **[EXHAUSTED]** | A complete search space enumerated, empty. |
| **[TESTED]** | A finite corpus tried, empty. **Not** an elimination of the class. |
| **[INFERRED]** | Follows from measured facts by a stated argument. |
| **[ASSUMED]** | Load-bearing but unproven. The soft spots. |

The distinction between [EXHAUSTED] and [TESTED] is the one that matters: §2.1–2.11
are the first, §2.12 is the second, and conflating them would be the only overclaim
in this document.

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

- `m/44'/0'/0'/0/0` through `/35` — well past the standard BIP44 gap limit of 20.
  Index **21** was checked specifically: the positional argument in §5 points there
  and it sat one past the original sweep
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

### 2.12 [TESTED] Brainwallets — a class nobody had touched

`priv = SHA256(phrase)` directly: no BIP39 checksum, no PBKDF2, no BIP32, no path.
Common in 2020-era puzzles and never tested against this target.

**Two corpora, both negative.**

*Image text*, 22,638 keys: every text string in the image (Latin mottos, Russian
plaintexts, BLM slogans, dates, the 13th Amendment, whitepaper fragments, the target
address itself), casing / punctuation-stripped / whitespace-stripped variants, each
individual word of the Russian plaintexts, all 2048 BIP39 words singly, and pairwise
concatenations of 33 salient phrases under three joiners. Plus SHA256 and SHA256² of
the PNG file and of the concatenated IDAT payload.

*Template sequences*, 992,436,543 candidates → **7,939,492,344 addresses**: the t18
template over a 63-word pool (the 52-word pool plus the eleven image words that are
**not** BIP39 — `stop freedom hate white death kill war bleed shut money buy`, which
a brainwallet permits and a mnemonic cannot). All four key variants — SHA256 and
double-SHA256, space-joined and concatenated — each as compressed and uncompressed.

> **This is [TESTED], not [EXHAUSTED].** The brainwallet class is every possible
> string and is unbounded. The honest claim is "the phrases present in the image, plus
> the template sequences over a 63-word pool". It is **not** filed with the GPU sweeps
> in §3 for the same reason: a brainwallet address is ~31× cheaper than a seed
> derivation (489,000/s against 15,600/s measured), so folding 7.9 billion of them
> into a total headed "full seed derivations" would inflate the figure with work that
> is not the same work.

Neither corpus touches orderings outside the template. For a brainwallet, order matters
exactly as much as for BIP39 — the same wall, and the position machinery is still what
you would need.

**Control, mandatory here.** A brainwallet has no checksum: every candidate passes the
filter by construction, so a wrong SHA-256 produces a full run of plausible garbage and
reports "exhausted, no match" exactly like a correct run. Nothing else in the pipeline
would notice. 12/12 vectors pass — six variants of `correct horse battery staple`, plus
three multi-block phrases at 124 bytes (`len%64=60`, forcing the extra pad block), 128
bytes (`len%64=0`) and 157 bytes. The canonical vector is 28 bytes, a single block, and
cannot reach the multi-block path an 18- or 24-word phrase needs.

Note `battery` and `staple` are not BIP39 words, so the control cannot be assembled
without an arbitrary-word table. That made the table mandatory, not optional.

**Self-validation:** acceptance came out exactly 1.0 — survivors == candidates in both
runs. With no checksum, anything less would mean the filter was silently dropping
candidates, and this is only visible because of the cumulative survivor counter added
during the seam work (§10).

---

## 3. Tally

See the repository for per-run configs. Summary:

Comparable units — a full seed derivation is PBKDF2-HMAC-SHA512 ×2048, then BIP32
CKDpriv, then secp256k1, then hash160:

| | derivations |
|---|---|
| BIP39 | 19,841,556,074 |
| Electrum v2 | 5,347,007,350 |
| **TOTAL** | **25,188,563,424** |

**729 days of CPU** at the ~400 derivations/s typical of CPU solvers, completed in a
few days of GPU time on an RTX 4070 Laptop.

Counted separately, because the unit is not the same:

| | |
|---|---|
| brainwallet candidates (distinct) | 992,436,543 |
| brainwallet addresses | 7,939,492,344 |

A brainwallet address is SHA-256 once, then secp256k1 and hash160 — measured at
489,000/s against 15,600/s for a seed derivation, ~31× cheaper. In
seed-derivation-equivalents the brainwallet work is ~163 M, not 7.9 B. Adding the two
columns would produce a larger number that means less.

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
the mechanic outright.

**[MEASURED] The clock can only produce ODD slots.** Consecutive integers *n* and
*n+1* sum to 2*n*+1, always odd; the wrap pair 12+1 = 13 is odd too. So the twelve
adjacent pairs yield exactly {3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23} and nothing
even, ever.

This is consistent with every filled entry in the table: the clock slots (3, 13, 21)
are odd, and every **even** slot comes from a count or a written number instead —
`camera` at 2 (two cameras), `mask` at 4 (four masked faces), `black` at 10 ("black
day number X"), `vote` at 12 (the mirrored `.VS.`), `rifle` at 16 (M16), `apple` at
20 (the XX on Leopold's head).

**Consequence for the unfilled slots.** Of 6, 8, 14, 15, 18, 21, 22, 23, 24:

| | slots | mechanism |
|---|---|---|
| odd | 15, 21, 23 | clock-reachable, but only three hands exist and they are spent |
| even | 6, 8, 14, 18, 22, 24 | **cannot** come from the clock — need a count or a number written in the artwork |

That is a real narrowing: six of the nine open slots are provably outside the one
mechanism the puzzle states outright, and the README's twenty-one sections supply no
count or number that produces any of them. The `.VS.` ambigram adds a fourth: slot **12** → `vote`.

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
4. **A count or a written number producing slot 6, 8, 14, 18, 22 or 24.** Per §5
   these cannot come from the clock, and the README's twenty-one sections supply no
   mechanism for any of them. This is where the mechanism inventory is actually
   incomplete.

**Deprioritised, with reasons:**

- **A larger source image.** Per §7.6 the final glyph is unassignable in principle
  from this corpus — a perfect scan does not fix a missing key. And per §2.9 no
  larger source exists anyway: `i.redd.it` serves the same 1600×1200 file,
  md5-identical.
- **More compute against the current template.** It is exhausted. A corrected
  template can be tested in seconds; an uncorrected one cannot be rescued by scale.

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

**Reading geometry.** The right-edge inscription runs **bottom-to-top** on the master
(x 1529–1554, y 29–1014); the same text reads left-to-right in `pictures/20_1.png`,
which is a cleaner de-rotated render and is far more legible than anything
extractable from the 1600×1200 master. Use it for glyph work. The clock line reads
left-to-right, and its ink sits at luminance ~160–200 against a light background — a
hard threshold near 120 finds nothing, so use a levels stretch rather than a contrast
multiply.

Note also that the two ciphers share some shapes with **different values**: `◇` is
`W` in the Gravity Falls Latin cipher and `с` in the Cyrillic one. Do not
cross-apply them.

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
| is it `ж`? | **refuted on arm count: 4 against 6** |

**A withdrawn test.** An earlier version of this table reported "X vs `х` = +0.056,
noise" as evidence against `ж`. That test does not discriminate and is withdrawn:
if `ж` were drawn as `х` plus an added stroke, the extra stroke changes the
bounding-box normalisation and the overlap, so a low correlation against bare `х` is
expected whether or not the hypothesis holds. Correlation is the wrong instrument for
a compositional hypothesis.

The valid test is structural. X has **four** arms from its crossing point; `ж` has
**six**. That refutes it on shape, which correlation could not do.

Its geometry is a vertical stroke crossed by a single diagonal, one arm up-right and
one down-left — verified identically in the master and in `20_1.png`.

**X matches neither the mapped alphabet, nor the artist's Arabic numerals, nor
the remaining plausible Church-Slavonic numerals, and carries no titlo. It is an
unresolved unique symbol, visually suggestive of `ж` but quantitatively
unassigned.** It occurs exactly once in 68 glyphs, which is *why* it has never
been read.

### 7.6 [MEASURED] Linguistic exhaustion — an independent route to the same wall

Reached by letter inventory rather than shape correlation, so it does not inherit
§7.4's method.

Across the three decoded plaintexts, **28 of the 33 Cyrillic letters appear**. The
five that never do:

```
ж   ц   щ   ъ   э
```

X must be one of those — and because none of them occurs anywhere else in the corpus,
**there is no second instance to triangulate from**. Of the five, only `ц` carries a
Church Slavonic numeral value (900); `ж`, `щ`, `ъ` and `э` have none. So `номер X`
resolves to a number only if the glyph is `ц`, and its shape does not support that —
`ц` is a U with a descender.

**[MEASURED]** The glyph is also **not in the Gravity Falls key at all**, checked
against both the pyramid layout and the Wheel of Intrigue. That is expected: Russian
needs 33 letters and the GF set supplies 26, so the author invented extras. This is
one of them.

> **Dependency.** This argument inherits the published plaintexts. The group sizes
> were confirmed independently by ink-profile segmentation (5/11/8/2/6/4/5/1 on the
> edge, 5/4/5 on the clock), and `е`, `с` and the doubled `м` were verified
> glyph-by-glyph — but not all 68 glyphs were re-derived. If any word in the
> plaintexts is wrong, the letter inventory shifts and the absent-five set with it.

**[INFERRED] X is unassignable from this corpus in principle.** No key entry, one
occurrence, and every candidate letter equally unattested. A higher-resolution scan
renders the shape more crisply and still cannot say which letter it is. The missing
thing is a key, not pixels.

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

**Seam validation.** Chunking is where an exhaustive claim can quietly fail: an
off-by-one dropping one candidate per join loses N−1 of 25 billion — numerically
irrelevant, fatal to the word "exhaustive". Three instruments, all green:

1. **Count invariance.** The survivor total is a pure function of the config, so
   chunking cannot change it. `seam_count.conf` reports an identical 262,250 at seven
   chunk sizes down to `--chunk 7` — 599,187 chunks over 4.2 M candidates. A single
   candidate lost per join would show as a shortfall of 599,186.
2. **Cross-binary match at production scale.** `t18_pool52` reports **5,941,047**
   survivors at four chunkings — the same value logged by three full runs of the
   *previous* binary. That is not self-consistency: it validates the historical runs
   and proves the refactor did not move filter semantics.
3. **The answer planted on a seam.** `--seam N` truncates the chunk containing N−1 to
   end exactly at N. The known answer HITs when placed first-of-chunk and
   last-of-chunk, at both small indices and past 2³².

A note on a broken test: the obvious form — set `--chunk` equal to the hit index —
cannot run. At 4,650,657,157 candidates and 1/16 acceptance that is 290 M survivors
against a 33,554,432 buffer, and the run aborts on `survivor overflow` before
reaching the seam. Chunk *size* and boundary *position* are different parameters.
The abort is itself a validation: the guard fired rather than truncating silently.

**Positive control.** Reproducing a known mnemonic proves little; the solver
must *find* an unknown one. A config blanks two slots of a known phrase to all
2048 words and requires recovery:

```
./solver2 --config selftest_find.conf
HIT   index 2270828
phrase : tiger live melody inject guitar nose route obtain ball diesel snow radar
```

262,144 derivations, `melody` and `snow` recovered.

That control is single-chunk. A second, `selftest_multichunk.conf`, blanks three
slots — 8,589,934,592 sequences, 536,870,912 derivations — and recovers the answer at
index 4,650,657,157, which sits in chunk 10 at offset 422,798,725 with a chunk size of
469,762,048. Nine boundaries crossed. Together with the seam instruments above, this
is what licenses the negative results.

**Eight bugs were caught by exact-value validation**, each producing plausible
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
- `BigInteger.Parse(hex, NumberStyles.HexNumber)` misparsing an **odd-length**
  string. A curve constant written as `"0" + 64 hex chars` comes back 4 bits shifted;
  PBKDF2 and BIP32 master stay byte-perfect against test vectors while every derived
  address is wrong. Build curve constants from byte arrays.
- **`show_hit` reporting the wrong derivation path.** It printed
  `m/44'/0'/0'/0/0` unconditionally, so any config with multiple `PATH` lines —
  `t18_pool52` has four, `t18_pathc` has eight — would have misreported which path
  produced a hit. **This is the only member of the family that corrupts a success
  rather than a negative:** the other seven produce a wrong "no match", this one
  produces a wrong answer to "which path found it", on the single run that would ever
  have mattered. It fires only on success, so nothing but a hit could have exposed
  it. `k_derive` now records the path index alongside the hit.

**If you run your own solver: validate against exact expected counts, not
plausible-looking ones.** A 1.2% deviation is invisible to a sanity check and
fatal to correctness.

---

*Published so these paths are not re-walked. If you have a word for slot 21,
evidence placing 22–24, a resolution of slot 11, a genuinely larger source
image, or a legible view of the final rune glyph — that is worth more than any
amount of GPU. A corrected template can be tested in seconds.*
