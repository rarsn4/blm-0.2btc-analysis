# 0.2 BTC Puzzle — the rune cipher solved, over 191 billion derivations eliminated, and six defects in the shared data

**Target:** `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`
**HASH160:** `ccbd031e54cde2a3189fd59bc49f731367a1779e`

**Status:** the Bitcoin puzzle is **NOT solved.** The address has received
20,107,284 sats across 5 transactions and spent zero — verified on-chain,
untouched since May 2020.

What **is** solved is the **rune cipher**, except for a single glyph. Those are
different claims and this report keeps them separate throughout.

I built a GPU search pipeline covering both BIP39 and Electrum and ran
**191,282,100,350 full seed derivations** — 5,535 days of CPU at typical solver
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
  others pooled. 300 M derivations.

  > **[CORRECTED 2026-09-01] This is narrower than originally stated.** The
  > configs that ran it (`t18_full{6,8,14,15,18}.conf`) drew the *other four*
  > gaps from the old **37-word** pool and carried **no `PATH` lines**, so they
  > ran the single default path. An audit of every config in the project found
  > that **none combines `@FULL` with a pool ≥52 or with 4 paths.**
  >
  > So two regions were never tested: one gap free over all 2048 while another
  > gap holds one of the 17 words added since (`able cause crime exist happy
  > know neither only party peace place that they thing time any verb`), and
  > the entire leave-one-out family on paths 2–4.
  >
  > This matters most for words outside **every** pool. `flag`, `banner`,
  > `nation`, `state`, `eagle`, `field`, `glory` and `salute` are all BIP39 and
  > none has ever been in a gap pool — they are reachable *only* through an
  > `@FULL` sweep, and the `@FULL` sweeps were the weak ones.
  >
  > **[RESOLVED 2026-09-01]** Closed by `t18_loo{6,8,14,15,18}.conf`: each slot
  > free over all 2048 words, the other four over the current 54-word pool, all
  > four paths. 87,071,293,440 candidates, 1,331,791,148 derivations after
  > removing the overlap between runs. All five negative. The claim is now
  > earned at every t18 gap under the current pool and path set.
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

Two scope limits on that corpus, both narrow and both stated rather than
implied. It ran at **t18**, not t21 — this section makes no claim about the
21-word template. And it predates hybrid-key support, so it covers compressed
and uncompressed only; the kernel now hashes all three, but the 7.94 B figure
above was measured before that.

**Casing, which applies to the two corpora differently.** The *template* corpus
is **lowercase only**, verified: every `SLOT`, `POOL` and `EXTRA` word in
`brain_t18_pool63.conf` is lowercase, the BIP39 wordlist is lowercase, and the
phrase builder emitted those bytes verbatim — at the time of that run it had no
casing parameter to pass. SHA-256 is case-sensitive and the artwork is in
capitals, so **no capitalised template sequence has been tested.** The solver now
takes `CASE lower | upper | title | all`, defaulting to `lower` and printing the
setting in the run header, so no future run can be silently lowercase.

The *image-text* corpus is a different matter, and an honest gap. Its
description above claims casing variants, and the claim cannot be checked: no
generator script and no key list for those 22,638 keys survives in this tree, and
no log records them. The figure rests on the report's own prose. It is left as
written rather than amended in either direction, and flagged here as the one
number in §2.12 that is not reproducible from what is published. Everything else
in this section reproduces from a config and a log.

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

### 2.13 [EXHAUSTED] Free-one-fixed at 21 words: the branch that was never run

Every t21 sweep before September freed a **gap** — slots 6, 8, 14, 15, 18, 21.
Not one freed an **assigned** slot. An audit of all twenty t21 configs confirmed
it: the only assigned slot ever varied was 20, and only as a two-way
`apple|second` list. Free-one-fixed existed at 18 words and nowhere else.

So "a fixed word is wrong" was not an infeasible branch. It was an untested
one. You do not need to know *which* word is wrong; you iterate over which.

**This matters more than the count suggests.** At p ≈ 0.75 per assigned word:

| assigned words wrong | probability mass |
|---|---|
| 0 | **1.8%** |
| 1 | 8.3% |
| 2 | 18% |
| 3–4 | 46% |

**The spend by branch, computed from the ledger rather than estimated:**

| branch | probability | derivations | per point of probability |
|---|---|---|---|
| a = 0, gap sweeps only (7 rows) | 1.8% | **50,457,931,465** | 28.0 B |
| a = 1, free-one-fixed (13 rows) | 8.3% | **136,372,012,128** | 16.4 B |

So the least likely branch received **1.71× more compute per point of
probability** than the next one. That is real, and it is much milder than it
looked while an uncomputed "roughly 78 billion" was attached to the 1.8% branch —
that figure was 1.55× too large *and* the wrong quantity, being the whole
project's total as of 11 September across every template length, Electrum,
passphrases and t18 free-one-fixed work. It was borrowed from a status snapshot
and relabelled as a branch figure without being computed.

None of this is a criticism of the work — the branch had to be closed, and
closing it is what turns a conjecture into a deduction. But stating it from the
ledger rather than from a recollection is what makes the next decision legible.

**[EXHAUSTED] The deduction, stated at full strength.** Let *a* be the number of
assigned words that are wrong and *g* the number of gap words outside the
54-word pool. The completed runs exclude:

```
a = 0, g = 0                          t21_readme54
a = 0, g = 1                          t21_loo_k, six ways
a = 1, g = 0  (13 slots, 55 cands)    free-one-fixed
```

So **a + g ≥ 2** — the answer departs from the README's reading in at least two
places. One hole remains: `a = 1` at slot 3 (`tower`) or 13 (`moon`), which were
deliberately never freed, or a replacement outside the 55.

This is stronger than the earlier statement that "at least one gap word is
outside the pool," which was true but understated: the six leave-one-out runs
already swept each gap across the entire dictionary, so the single-surprise case
was closed six ways over.

**Method.** Each run frees one assigned slot to the 54-word README pool plus
that slot's own table word (55 candidates; 56 at slot 20, which carries both
`apple` and `second`), with the six gaps over the full pool, `second` pinned at
slot 20, on the primary path `m/44'/0'/0'/0/0`.

Staging by path rather than running all four costs **1.565× overhead** against a
break-even at **q > 63.4%**, where *q* is the chance the answer sits on path 1.
Those figures are from production — `P = 6.209 µs` shared, `X = 1.195 µs` per
path, derived from `T4/T1 = 1.484` (see §10) — and they **supersede an earlier
1.18× and 22.8% taken from a microbenchmark.** The decision still goes the same
way for a legacy address under BIP44, where `m/44'/0'/0'/0/0` is the dominant
convention, but it is a much closer call than the original figures implied and
should not be described as comfortable.

The 89 h quoted below for stage 2 reconciles with these numbers to 2%
(`3 × (P+3X) × 10,654,063,447 = 87.0 h`), which is what confirms it as a real
figure rather than a projection.

**Results — thirteen slots freed, all negative.** Each run **21.910 h ± 0.32%**
(six back-to-back runs, measured from checkpoint mtimes), **284.8 h / 11.9 days**
for the campaign. Every survivor count is within 1.1σ of its exact binomial
expectation of **10,654,063,447** (σ = 102,815).

The last four to land were the self-naming slots, run together:

| run | freed | survivors | deviation |
|---|---|---|---|
| `free4` | `mask`@4 | 10,654,138,418 | +0.73σ |
| `free16` | `rifle`@16 | 10,653,972,836 | −0.88σ |
| `free12` | `vote`@12 | 10,654,012,263 | −0.50σ |
| `free19` | `glove`@19 | 10,654,167,169 | +1.01σ |

**[MEASURED] What these four do not establish.** Each asks *"is this word wrong,
and is its replacement among the 55?"* A negative is equally consistent with the
word being **right** and with it being **wrong while the right word sits outside
those 55**. The two do not separate, so four negatives return the status quo and
say nothing about whether the self-naming mechanism is reliable. Only a hit would
have been informative — and a hit would have solved the puzzle outright.

| slot | word | why it was weak |
|---|---|---|
| 10 | `black` | **zero derivation** — rests entirely on the unreadable glyph |
| 20 | `apple`/`second` | freed across all 56, superseding the provenance question |
| 11 | `pyramid` | the contested pyramid / Space Needle slot |
| 1 | `subject` | the README hedges it in writing |
| 7 | `liberty` | canon-assumed; 5 spikes measured directly, 2 inferred |
| 5 | `police` | "line five" needs a convention nothing else in the table uses |
| 17 | `gold` | "17 years" is a chart-span reading, not a count |
| 9 | `eye` | occluded clock position, inferred from the fit |
| 2 | `camera` | the README's own `twin` hedge |
| 4 | `mask` | self-naming — four masked faces |
| 16 | `rifle` | self-naming — M16 |
| 12 | `vote` | self-naming — the `.VS.` ambigram |
| 19 | `glove` | self-naming — the CVD19 vial |

**Two of these settled standing questions rather than merely eliminating
words.** Freeing slot 20 across all 56 candidates **supersedes** the
`apple`-versus-`second` provenance argument — neither works, so the argument is
retired rather than resolved. And `black`@10, load-bearing since 2020 on nothing
but a glyph nobody can read, is now tested rather than assumed.

**Scope, stated exactly.** What is eliminated is "the assigned word at slot *n*
is wrong **and** its replacement is one of the 55 README-derived candidates."
Not "the assigned word at slot *n* is wrong." Freeing to the whole dictionary is
1,216 h per run and was not done.

**Two slots were deliberately not freed.** `tower`@3 and `moon`@13 are **written
on the clock hands themselves**. Freeing them would not test an inference — it
would test whether the puzzle's own labels are wrong, and if they are, no
ordering of sweeps recovers from it. Excluded by choice, not oversight.

**Stage 2 was declined.** Paths 2–4 on three slots costs 89 h and covers 0.33%
of total probability, against 1.4% for the six remaining slots at path 1 — four
times worse per hour, and the lowest-value run on the board. The argument that
justified staging by path is the same one that rules out revisiting those paths.

### 2.14 [EXHAUSTED] Two hypotheses the source document itself named

The README hedges exactly twice, and both hedges have now been tested.

**Row 1:** *"Appear in the section 1 (13th) or it could be 14?"* Tested as
`t21_swap114` — `subject` moved from slot 1 to slot 14, slot 1 opened to the
pool, all four paths. 49,589,822,592 candidates, +0.27σ, negative.

This one mattered because slot 14 had already been closed on the image side by
both routes the author used elsewhere: a clustering sweep with a passing control
(45 blobs against a known 44 stars) found no countable object set of size 14,
and a region-by-region review found no written numeral. The README's own
question mark was the only documentary candidate left.

**Row 2:** *"Two cameras. Maybe could be 'twin' word?"* Tested by freeing
slot 2 to 55 candidates including `twin`. Negative.

**[INFERRED] From this point, every remaining hypothesis is one we construct,
not one the document offers.** That is a different epistemic footing from
everything preceding it, and the distinction is worth preserving: earlier
negatives eliminated readings someone could point at; later ones eliminate
readings we invented.

## 3. Tally

**The tally is computed, not maintained.**

It had been kept as a running sum with per-change patches, and it drifted. Two
independent reconstructions on 23 September differed by 331 M, and tracing the
gap showed **both** were wrong: one used the solver's *reported* per-run
expected value instead of exact `space/128` (+194 M), the other omitted ~1.14 B
of runs. Neither was reproducible from its own inputs.

The deeper defect was double-counting. Every run on the same template shares
the all-pool core, so summing counts that core once per run — **3.72%** of the
naive total across the t21 campaign. Of the twelve older t21 runs, **37% was
already covered** by newer sweeps.

`tally2.py` replaces the sum. It parses the run configs directly — so a row
cannot drift from the config it claims to describe — and computes the union by
box disjointification with real set intersections. Run it as
`python3 tally2.py configs`.

```
t21 campaign, 29 evidenced runs     191,282,100,350 derivations
+ the twelve older asserted runs    194,890,996,719
    marginal of the twelve          3,608,896,369
    at 400 derivations/s            5,639 CPU-days
```

**The seven runs added on 27–28 September are why the union matters.** Six were
the black-relocation sweep and one a pool expansion. Added as boxes they
contribute **4,190,694,419** derivations; added as a sum they would contribute
5,105,437,240. The 914,742,821 difference is entirely `t21_pool75`; the six black
runs overlap nothing and contribute their full 387,420,489 each. An addition would
have overstated the total by 0.48% and there would have been nothing in the
arithmetic to reveal it.

**Where pool-75's overlap actually comes from.** Containment of the earlier
pool-54 box is the obvious mechanism and it is not the main one. Marginal
coverage of pool-75's 2,780,914,306, taken from the box definitions:

```
t21_readme54     387,420,489   cumulative   387,420,489   13.93%
t21_loo21        150,663,523                538,084,012   19.35%
t21_loo6          75,331,761                613,415,774
t21_loo8          75,331,761                688,747,536
t21_loo14         75,331,761                764,079,297
t21_loo15         75,331,761                839,411,059
t21_loo18         75,331,761                914,742,821   32.89%
```

`t21_readme54` — the pool-54 run pool-75 strictly contains — accounts for
387,420,489, or 13.93%. The remaining **527,322,332 (18.96%)** is the six
leave-one-out runs, which each swept a gap over all 2048 words and so reach
into pool-75 wherever the rest of the template agrees. The fourteen
free-one-fixed boxes, `t21_swap114` and `t21_written` add **nothing** beyond
what the leave-one-out family already covers.

`t21_loo21` contributes exactly twice the marginal of each of the other five,
and the reason is in the configs, not in any symmetry: `t21_loo21`, `t21_readme54`
and `t21_pool75` all take `SLOT 20 apple|second`, while `t21_loo6/8/14/15/18`
pin `SLOT 20 second`. Two words against one, at one slot, is a factor of two in
the intersection. A uniformity assumption across the six would have been wrong
by that factor — which is why these are computed from the box definitions.

**All three public-key encodings are hashed, so the address-representation
question is closed.** Every derived key is serialised three ways and each is
hashed and compared: compressed (33 B, `0x02`/`0x03`), uncompressed (65 B,
`0x04`) and hybrid (65 B, `0x06`/`0x07`, SEC1 2.3.3). One EC multiply feeds all
three — y is already in hand for the parity byte — so the cost is two extra
SHA-256 + RIPEMD-160 per key. `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ` carries
version byte `0x00`, so it is P2PKH: neither P2SH-wrapped segwit nor bech32 can
be the target. With all three encodings covered, this is **exhausted without
qualification** — not "over the encodings wallets happen to produce".

Three permanent regression configs pin it: `selftest_find.conf`,
`selftest_uncomp.conf` and `selftest_hybrid.conf` are the same phrase at the
same path with the same private key, differing only in serialisation, so any
future miss isolates exactly one code path. All three recover index 2270828.

**The runs before this change were compressed-only, and are not being re-run.**
Measured, not assumed: the pre-patch binary was kept and run against the
uncompressed address of a known phrase, and it exhausted without finding it. So
the 191.3 B carries one scope line — *compressed-pubkey P2PKH* — and that is
sufficient, because BIP32 wallets emit compressed leaf keys at every path
including `m/0/0` and `m/0'/0/0`, while the 2013-era software that produced
uncompressed keys (Electrum v1 old seeds, brainwallets, pre-0.6 Core) never used
BIP32 paths at all. The two populations do not intersect. Everything from here
covers all three regardless, because conditioning the check on that argument
would let the next kernel variant drop back to compressed-only in silence.

**What "derivations" means here, exactly.** A 21-word mnemonic carries seven
checksum bits, so one sequence in 128 is valid and the ledger reports
`⌊candidates / 128⌋`. **That is a convention, not a count.** The true number of
checksum-valid mnemonics inside a given template is a determinate integer that
nobody has enumerated, and per-run survivor counts scatter binomially around
`N/128` — which is why every run is z-tested against that expectation rather
than required to equal it.

The convention has a rounding choice inside it, and the choice is visible:
`⌊(A−B)/128⌋` and `⌊A/128⌋ − ⌊B/128⌋` differ by one on the current figures
(3,608,896,368 against 3,608,896,369). Both are defensible in isolation. The
ledger prints the two totals, so the marginal it quotes **must** be the
difference of the two printed figures or the three numbers on the page do not
reconcile. Floor once, at the point of reporting, and derive every difference
from the reported values.

**No single grand total is quoted, and that is deliberate.** The previously
published figure (26,513,178,774) was a running sum that already included the
twelve older t21 runs, and whether it counted them at naive size or with overlap
removed is unrecorded. Subtracting them to isolate a pre-t21 residual therefore
rests on an assumption nobody can check — the residual is somewhere between
roughly zero and the whole 26.5 billion.

The t21 figure above **is** computed, and every digit reproduces from
`tally2.py configs`. Adding an unverifiable constant to it would make the sum
less trustworthy than either part. Where one number is needed, **"over 191
billion derivations eliminated"** is a floor that is computed, in preference to
an estimate that is not.

**The headline quotes the evidenced figure, not the combined one.** 191,282,100,350
is the union of the 29 runs whose logs are in this tree; 194,890,996,719 adds the
twelve older runs carried on report alone. The larger number is not wrong, but it
inherits the weaker warrant of its weakest component, and a headline that needs a
footnote about which runs have logs is worse than a smaller headline that needs
none. The previous headline had the same dependency and did not disclose it.

**EVIDENCED versus ASSERTED is deliberate.** Runs with logs present in the
working tree are separated from runs included on report alone. A config is not
evidence that a run happened, and a ledger that reads configs cannot tell the
difference.

An earlier size-based inclusion-exclusion (`tally.py`) is retained. It agrees
with `tally2.py` to the candidate on the declared runs but is **exact only
where the per-dimension sets nest**, which the older runs do not: `readme54`(54)
is not inside `trust21`(69), and `trustonly`'s pool is disjoint from every
other. Taking `min()` there would overstate intersections and so understate the
union — wrong in the flattering direction.

**This supersedes the hand-derived `5·L − 4·R` subsumption note** previously
carried in this section for the t18 leave-one-out family. That formula was
correct for that one family and does not generalise; `tally2.py` computes the
same quantity for every family without a closed form. One method, stated once.

**One tranche is knowingly excluded.** Three runs on 14 August used an earlier
CPU solver (`template_solve.py`, 16 workers) in `~/Downloads/puz2/files/` with
**no config file at all** — the template lived in the Python. All three
completed and exhausted without a match — **138,707,999 derivations**, 0.096% of
the ledger. They are not rows and cannot be: the logs print `37 candidates` per slot
but not *which* 37, and the pool file they were given no longer exists. Without
the pool there is no set, and hand-entering a guessed one would be exactly the
maintained-tally failure this section exists to end. **A run with no config is a
run with no provenance, whatever its log says** — so it is stated here and
counted nowhere.

Those three were invisible to a config-based audit by construction. They were
found by inventorying *logs* instead, which is the dual check and the only one
that can see a run whose config never existed.
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

   **[MEASURED] The flag carries 44 stars and 13 stripes.** Star count by
   connected-component analysis inside the canton — every star located, two
   clipped at the fold, visually verified against the detection. Stripe pattern
   `KRTKRTKRTKRTK`: 13, canonical. The flag's only anomaly is the star deficit.

   **50 − 44 = 6**, and 6 is an open even slot. That is a deficit in a
   deliberately-drawn flag, the same kind of count as "four masked faces", and it
   needs no invented operation. (Digit-summing 44 → 8 was proposed and is
   withdrawn: the artwork nowhere identifies digit-summing as an operation, which
   acceptance criterion 5 forbids.)

   **[TESTED] The flag reading is negative.** `flag`, `banner`, `nation`, `state`,
   `eagle`, `field`, `glory` and `salute` are all BIP39 and none has ever been in a
   gap pool, so only an `@FULL` sweep could reach them — and until 2026-09-01 the
   `@FULL` sweep at slot 6 was the weak one (§2.3). `t18_loo6.conf` swept slot 6
   over all 2048 words with the current pool and all four paths. Empty. The chain
   was coherent and it is closed.

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
the remaining plausible Church-Slavonic numerals, and carries no titlo. It is a
hapax — shape fully resolved, meaning unassigned.** The distinction matters and
the earlier wording blurred it: the geometry is *not* in doubt. It is a vertical
stroke crossed by a single diagonal, four arms from the crossing point, verified
identically in the master and in `20_1.png`. What is unassigned is which
character that shape denotes. It occurs exactly once in 68 glyphs, which is
*why* it has never been read.

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


### 7.7 [RETRACTED] The "marked and withheld" reading

Five observations in this document were at one point read together as a
deliberate pattern — the author marks a thing and then withholds it — and an
inference was drawn from that pattern: that the seed words come from outside the
image and the artwork supplies only the ordering.

| where | observation |
|---|---|
| §1.4 | the phrase **"a trusted"** deleted from the whitepaper micro-text |
| §2.7, §5 | the **blank clock hand** at the 21st position |
| §6 | the flag's **star deficit**, 50 − 44 = 6 |
| §7.3 | the **unreadable final glyph** |
| §7.4 | **"1865 − 202…?"** |

Four of the five do not survive a base rate, and the rule that removes them is
now §10's:

| entry | why it fails |
|---|---|
| the deleted *"a trusted"* | the artwork has five letter-level typos in ~250 words. One dropped word-pair is unremarkable at that rate, and the phrase surviving twice elsewhere is exactly what a single accidental omission looks like — not evidence against accident. |
| the unreadable glyph | not the author's absence, ours. Russian needs 33 letters; the Gravity Falls key supplies 26; the author invented the rest and we lack the key. Filing it as withholding assumes an intent nothing supports. |
| *"1865 − 202…?"* | reads naturally as an open-ended range — abolition to the present and counting. §9 criterion 4 forbids assigning a cryptographic function to punctuation that already has a plain meaning. |
| the star and course deficits | two deviations across five resolved canonical-count checks is the ordinary yield of hand-drawing. They also **disagree**: 50 − 44 = 6 lands on an open slot, but 13 − 12 = 1 lands on `subject`, which is assigned, freed and eliminated. A real mechanism works twice. |

**[MEASURED] One entry survives: the third clock hand.**

It survives on the **placement** of the hands, not on the absence of a word —
and that distinction is what makes it testable. A decorative clock needs no
deliberate placement, because a clock showing a time has three hands determined
by *one* parameter. So the null hypothesis is: the clock simply shows a time.

It does not. All three hands sit at numeral midpoints (angles ≡ 15 mod 30°),
and that is impossible on a real clock. With *t* in seconds past twelve:

```
second : 6t    ≡ 15 (mod 30)  →  t ≡ 2.5  (mod 5)
minute : t/10  ≡ 15 (mod 30)  →  t ≡ 150  (mod 300)
hour   : t/120 ≡ 15 (mod 30)  →  t ≡ 1800 (mod 3600)
```

Every *t* ≡ 1800 (mod 3600) is a multiple of 1800, and 1800 and 3600 are both
≡ 0 (mod 300) — so the hour condition forces *t* ≡ 0 (mod 300), which can never
be 150. **Hour and minute are incompatible.** Sanity check: at 10:07:30 the hour
hand sits at 303.75°, 11.25° from the observed 315°.

Exactness is the weak claim, though, and it is not the one that matters.
*Approximate* triples of midpoints are common — 7,344 of 4,320,000 samples
across the 12-hour cycle fall within 1.5° on all three hands, the best being
1.186° at 9:27:37.69. **The question was never whether a clock can show three
midpoints. It is whether it can show *these* three: 12&1, 1&2, 10&11.**

Searching every time in the cycle at 0.01 s resolution, against all six
hand-to-angle assignments:

```
best achievable error : 10.465 deg   at 10:09:04.24
   hour   304.535   wanted 315.0   (off 10.465)
   minute  54.424   wanted  45.0   (off  9.424)
   second  25.440   wanted  15.0   (off 10.440)
```

10.5°, against a measurement precision of ~1.5° — **seven times the fit
tolerance**, and the canonical assignment is itself the best of the six. No time
produces this configuration. The three angles are therefore three independent
choices, not one.

**The prior, since §10's rule applies here too.** Under a null of free
placement, each hand lands within 1.5° of a midpoint with probability 3/30 = 10%
— or 3/24 = 12.5% granting an illustrator who keeps hands off the numerals for
legibility. Three hands: **0.195%, about 1 in 512.**

That figure must then be corrected for look-elsewhere, because midpoints are not
the only configuration an observer would have flagged: all three on numerals,
all three coincident, two coincident, all three 120° apart, symmetric about an
axis. Dividing across four such alternatives gives ~1 in 130, and four is
conservative. **State it as order 10⁻², not 10⁻³.** That is still the strongest
number in the section, and it no longer overstates.

**The same discipline applied to a coincidence in the survivor counts.** In the
six-run black sweep of 27–28 September, `t21_black8` came in at exactly
**+20,301** survivors against the `N/128` expectation and `t21_black21` at
exactly **−20,301** — the same magnitude, opposite signs. Across the 15 pairs
available from six runs, an exact magnitude match is of order 1 in 4,600. That
is noticeable and it is not evidence: no mechanism connects the two runs, they
differ only in where `black` sits, and 1 in 4,600 is the *unconditional* figure
before any correction for the many other coincidences that would equally have
been flagged. Noted and dismissed. It is recorded here rather than omitted
because a reader checking the six counts will find it, and should find it
already accounted for.

**[RETRACTED] The inference the pattern carried.** That the seed words come from
outside the image and the artwork supplies only the ordering. With one entry
left, it has no basis and is dropped rather than downgraded. It was the most
defeatist claim in the document and the least supported — it told every reader
the answer is not findable in the artwork, on the strength of four observations
that turned out to be base rate.

**The four retracted entries remain in place where they were made.** Each is a
correct observation about the artwork; what is withdrawn is reading them as a
system. §1.4's deleted phrase is still a real deletion and `trust`@21 was still
tested on the strength of it. This subsection retracts the pattern, not the
facts.

**A note on how this error was found and on one it concealed.** The pattern was
assembled in a working document, not here, and for four days it was discussed as
though it were a section of this report — "§8" — by three parties, none of whom
looked at what §8 actually contains. The first patch written from that belief
replaced §8's real content with this retraction, keeping §8's heading, and an
anchor-checked script applied it faithfully because the line numbers were right
and the identity behind them was assumed. **A hash verifies which file; an anchor
verifies what text you are editing; neither verifies that the section is the one
you think it is.**

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


7. **An observation needs its control before it is recorded, not after — and
   the control needs checking too.** A finding that survives only a qualitative
   caveat has not been tested. Worked example, in three stages, because the first
   two were both wrong.

   **Stage 1 — the finding.** The protest-slogan block has seven lines; line six
   was reported as the only one containing no BIP39 word, and slot 6 is an open
   gap. Striking, and recorded before any control was run.

   **Stage 2 — the bad control.** Two reviewers independently computed the base
   rate and both **stemmed** before matching (`LIVES`→`live`, `KILLING`→`kill`),
   giving p ≈ 0.50 and an expectation of **1.94** wordless lines against one
   observed. Fewer empties than chance: no evidence either way. Right verdict.

   **Stage 3 — the control, checked.** BIP39 matching is exact. `lives` is not
   `live`; `stop`, `kill`, `killing`, `not` and `us` are not in the wordlist at
   all. Matching exactly, the block reads:

   | # | colour | words | exact BIP39 hits | n |
   |---|---|---|---|---|
   | 1 | black | BLACK | `black`#184 | 1 |
   | 2 | black | LIVES | — none — | 1 |
   | 3 | black | MATTER | `matter`#1099 | 1 |
   | 4 | blue | NO JUSTICE NO PEACE | `peace`#1295 | 4 |
   | 5 | red | END POLICE BRUTALITY | `end`#589, `police`#1342 | 3 |
   | 6 | green | STOP KILLING US | — none — | 3 |
   | 7 | black | NOT ONE MORE | `one`#1238, `more`#1151 | 3 |

   **Two wordless lines, not one** — and line 2 is one of them. The original
   observation was not merely uncontrolled, it was miscounted.

   **The base rate depends on which text you take as the corpus**, which is a
   transcription judgement, so it is reported across five choices rather than one:

   | corpus | words | BIP39 | p | E[wordless] | observed |
   |---|---|---|---|---|---|
   | headline only | 59 | 23 | 0.390 | 2.65 | 2 |
   | headline + amendment | 92 | 32 | 0.348 | 2.97 | 2 |
   | headline + amendment + whitepaper | 118 | 37 | 0.314 | 3.25 | 2 |
   | slogan block alone | 16 | 7 | 0.438 | 2.32 | 2 |
   | amendment + whitepaper only *(out-of-sample)* | 59 | 14 | 0.237 | 3.96 | 2 |

   Expectation exceeds the observed 2 under **every** corpus, so the verdict does
   not depend on the transcription. The first four rows include the slogan block
   inside the corpus that scores it; that inflates p and so *lowers* E, biasing
   the test **toward** declaring signal — and it still does not. The last row is
   the clean out-of-sample estimate and is the least favourable of all.

   The expectation alone understates the case. Taking the seven lines as
   independent, the exact distribution of the wordless-line count gives a
   one-sided probability for the observed 2 under each corpus:

   ```
   corpus                                 p      E     P(=2)   P(<=2)
   slogan block alone                  0.438   2.32    0.340    0.576
   headline only                       0.390   2.65    0.298    0.457
   headline + amendment                0.348   2.97    0.247    0.351
   headline + amendment + whitepaper   0.314   3.25    0.199    0.269
   amendment + whitepaper only         0.237   3.96    0.094    0.115   <- clean
   ```

   **Quote the range, not a row: p = 0.12 to 0.58 one-sided.** Under the corpus
   most often cited (0.314) three is the modal outcome and two the second most
   likely, so the observation is an ordinary draw at p = 0.27.

   Note which way the out-of-sample row cuts. It has the **highest** expectation,
   so 2 sits furthest below it and `P(≤2)` falls to **0.115** — leading with the
   clean estimate makes the observation look *more* notable, not less.

   **And note which tail that is.** `P(≤2) = 0.115` is a **lower**-tail result:
   `P(≥2) = 0.979`, and the mode is **4**. The original claim was that a wordless
   line is notable, which requires wordlessness in *excess*. The artwork contains
   **fewer** wordless lines than chance, not more — so 0.115 cannot support the
   claim it was raised against, in any corpus, and a reader who sees "1 in 9"
   without the direction could conclude the opposite.

   That makes the conservative corpus choice unambiguously right rather than
   merely cautious: it is the row least favourable to the null, the null survives
   it anyway, and the residual deviation points away from the finding. **There is
   nothing here in either direction.**

   **What the example is for.** Two reviewers ran the same control independently
   and both reached the right verdict from a wrong premise. It surfaced only when
   the expected values were placed side by side — 1.94 against 3.25 — rather than
   the conclusions. **A control that reaches the right answer from a bad premise
   is still a control nobody checked.** Bending a written word to reach a wordlist
   entry is precisely how `breathe`, `trusted`, `stop` and the other eleven
   entered circulation, and both reviewers did it inside the section documenting
   it. That costs nothing to do and nothing prompts you to check it, which is why
   it is a better worked example than any of the thirteen bugs.

   Reproduce with `slogan_lines.py` in the project root (needs `mnemonic` only).
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

**The rate table above predates this rewrite.** Every figure in it was measured
on the affine pipeline; the combined 125 k/s is now roughly 3× that. The table
is retained as measured rather than re-scaled, because a scaled number is not a
measured one — it will be replaced when the suite is re-run end to end.

The pipeline is **~3× faster** since replacing affine double-and-add with
**Jacobian coordinates**: ~384 modular inversions per scalar multiplication
down to one, at the final conversion back to affine. **Measured 2.956×
end-to-end** on a 4-path config (10.08 s → 3.41 s).

**Every rate below is stated with the conditions that produced it**, because
this project lost an evening to figures whose unit, path count and thermal state
were unrecorded:

| quantity | value | conditions |
|---|---|---|
| pipeline throughput | **135,074 derivations/s** | 22 production runs, sd 0.32%, 1 path |
| 4-path / 1-path cost | **T4/T1 = 1.484** | `loo` (4-path) against `free` (1-path), both post-Jacobian |
| shared / per-path split | P = 6.209 µs, X = 1.195 µs | per derivation, from the above |
| `BIP32 + secp256k1` row | 925 k/s | **per derivation, single path** — not per scalar multiplication |
| scalar-mult speedup | **5.50× production** | 6.5× is the isolated-kernel figure; production wins |
| EC share, 4 paths | **43.5% [MEASURED]** post-Jacobian | from P and X directly |
| EC share, 4 paths | ~81% **[INFERRED]** pre-Jacobian | from a contended A/B, assuming both arms were slowed equally |
| hardware state | 1605 MHz SM — **51.7% of the card's 3105 MHz max** | 88 °C sustained, 59.7 W of 80 W, `SW Thermal Slowdown` active |

The last row is the reproducibility item. **An unthrottled card should be roughly
twice as fast**; without that line a reader benchmarking their own solver
concludes ours is broken.

The two EC-share figures describe **different binaries**, and pairing the
post-Jacobian cost ratio with the pre-Jacobian share produces an Amdahl
impossibility. That mistake was made and caught here; the labels exist to stop
it recurring.

All three scalar multiplications in the derivation are **fixed-base** — the
hardened BIP32 steps need no public key, and the rest multiply the generator —
so a comb table was considered and rejected: it adds ~2% against a 5.5× Amdahl
ceiling that Jacobian alone reaches 87% of. Extra risk surface for nothing.

Verified bit-identical to the affine routine over **122,880 random scalars plus
k = 1, 2, 3 and n−1**, with the affine implementation retained as the oracle
rather than replaced. The swap happened mid-sweep, at a chunk boundary; the
survivor count of the completed run reconciled **exactly** across the two
segments, proving the swap introduced no gap and no overlap.

Two estimates were wrong in opposite directions and the decision survived both:
a predicted 30× on the multiply (inversion priced at ~100 multiplies; Cyclone's
`_ModInv` is divstep and far cheaper) and a recommendation to build the comb
table first. The robustness table is the only reason — the case never depended
on hitting the multiplier.

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

**Fifteen bugs were caught by exact-value validation**, each producing plausible
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
- a widened bit field in the hit record that eight of twelve control cases were
  structurally unable to see (below)
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

9. **The global checkpoint path.** `progress2.txt` was a fixed filename shared
   by every invocation, so any second run — a benchmark, a selftest, a config
   check — destroyed a multi-day sweep's resume point. A crash afterwards would
   resume from the wrong index and skip candidates silently, voiding the
   exhaustiveness the project rests on. Audited backward: no completed sweep was
   affected. Its fix has since prevented two concrete losses.
10. **A `uint64_t[4]` passed to a 5-limb `_ModInv`.** Compiles, runs, returns
   plausible garbage. The affine code never hits it because it routes through a
   `fieldInv` wrapper. Caught by the differential oracle on first execution.
11. **`subtract()` in the ledger discarded already-emitted pieces** on its
   disjoint-dimension early return, losing real volume. It never fired on the
   declared runs because in every pair the disjoint dimension is the *first* one
   where the runs differ, so the discarded list was always still empty. Fixing
   it left the evidenced figure unchanged and moved the combined figure by
   68,300,324 derivations.
12. **The ledger and the solver disagreed about what a config means.** The
   solver refuses a pool or slot word that is not in the wordlist and exits 1,
   in all three positions (`POOL`, a bare `SLOT`, a `SLOT` list) — verified by
   injection. The ledger's parser filtered the same words with `if w in IDX`,
   silently shrinking a declared pool. No run could have used such a config, so
   nothing was miscounted, but the error direction was to **understate coverage
   with no symptom** — the one direction that never announces itself. A ledger
   that reads configs must fail on whatever the solver would refuse.

   The first fix was scheme-blind: it checked the BIP39 map alone, so a
   brainwallet config legally declaring `EXTRA stop freedom` would have made the
   ledger abort on valid input — a hard stop traded for a silent undercount,
   which is the worse of the two. It never fired only because the ledger walks an
   explicit list of declared runs rather than a glob. Containment, not a fix.

   The audit that cleared it was also too narrow: it covered 239 configs in two
   directories. A correct enumeration of the home directory finds **767 `.conf`
   files, 735 of them puzzle configs**. Re-run across all 735 — no pool or slot
   word is neither BIP39 nor `EXTRA`, and all eight `EXTRA`-declaring configs are
   `scheme=brainwallet`. The conclusion survived; the evidence for it had been a
   third of what it should have been.

   The *widened* audit was itself wrong first, in the same family. It reported
   837 files and 667 puzzle configs, because it split `find` output on bare
   whitespace rather than newlines — shredding every path containing a space into
   fragments that failed to open and were swallowed by a bare `except: continue`.
   That **inflated** the file count while **dropping 70 real configs**, all of
   them under `~/Downloads/real (copy)/`. The discrepancy only surfaced because a
   later run with a *narrower* content filter returned *more* configs, which is
   impossible. Two audits of the same tree, and the one that agreed with
   expectations went unchecked.
13. **The fix for bug 12 introduced a collision, by relying on the containment
   it had just rejected.** Exempting `EXTRA` words meant giving them indices
   above the wordlist, and the first version enumerated each config's *own* list:

   ```
   brain_find.conf      EXTRA stop freedom    ->  stop    = 2048
   brain_selftest.conf  EXTRA battery staple  ->  battery = 2048
   ```

   `stop` and `battery` became the same element. The ledger's whole purpose is
   computing unions by real set intersection **across** configs, so a union over
   two `EXTRA`-declaring rows would have been arithmetic on words with nothing in
   common. Demonstrated before fixing: two configs sharing no pool word produced
   identical slot sets.

   It could not fire while no brainwallet config was a declared row — which is
   the same accidental containment rejected one bug earlier, reintroduced by the
   fix that makes such rows possible. **A fix inherits the standard applied to
   the bug.** Now one module-level registry: same word, same integer, every
   config, matching the solver.

   The related hazard was checked and does not apply — this script's index map is
   0-based (`zoo` = 2047), so basing at 2048 cannot alias it. Had it followed the
   report's 1-based convention, the first `EXTRA` word in every config would
   silently have become `zoo`.

   All three tests written for bug 12 parse a **single** config and so could not
   see this. Two cross-config cases were added and mutation-tested.
14. **The log filter destroyed the record of work that did happen.** The queue
   script piped solver stdout through `grep -vE "^ +[0-9]+\.[0-9]{2}%"` to keep
   logs readable, which strips every per-chunk progress line. `t21_free4.log` is
   108 bytes of header. When a question arose about how much a set of benchmarks
   had cost a running sweep, the data that would have answered it retrospectively
   — for free, exactly — had been discarded by design.

   Not a solver defect. The same family as bug 9 and `show_hit`: **tooling that
   loses the evidence rather than the work.** It cost nothing only because
   checkpoint mtimes survived independently, which was luck. Replaced by an
   external poller recording `(epoch, value)` on every checkpoint change — and
   that poller's first output turned out to contain the whole campaign's run
   durations, which is where the 21.910 h ± 0.32% figure came from.
15. **Two commits claimed work they did not contain.** Publishing this report
   took four commits to land three changes. `d30d8d3` applied the additions but
   substituted the wrong section (see §7.7). `9e7ef0d` and `d534547` each carried
   a message describing the section-8 restoration and **one line of
   `.gitignore`** — because they were staged with `git add -u <pathspec>`, which
   git reads as *"update only that pathspec"* rather than *"update everything,
   and also this"*. `1aad6fe` finally carried the content.

   Same family as bug 9, bug 14 and `show_hit`: **the record said the work
   happened and the artifact did not change.** Both bad commits reported
   `1 file changed, 1 insertion(+)` and neither was read. The check that catches
   it is three lines and confirms the artifact rather than the message:

   ```
   git show HEAD:REPORT.md | wc -l
   git show HEAD:REPORT.md | grep -c '\[FIGURE\]'
   git show --stat HEAD | tail -3
   ```

**A partial pass is not a pass.** Adding hybrid public keys widened the pubkey
index in `hit[1]` from one bit to two, which moved the `sp` and `kd` fields up by
one. The kernel was updated; the selftest's expected-value computation was not.
Twelve cases ran and **eight passed** — every case with `sp = 0` and `kd = 0`,
because at zero the two bit layouts are numerically identical. The suite looked
two-thirds healthy while the field it was checking had moved underneath it, and
the four failures were exactly the cases where the layouts disagree.

Two things made it recoverable. The pre-patch binary had been kept, so
`--selftest-brain` on it returned 12/12 and localised the change to the patch
rather than the hardware or the vectors. And the failure pattern was itself
diagnostic: a fault that spares every case sharing a particular parameter value
is pointing at that parameter. What would *not* have worked is reading "8/12" as
mostly-working. A control suite reports on the code as it was when the suite was
written; when the two drift, the suite's silence is not evidence.

**If you run your own solver: validate against exact expected counts, not
plausible-looking ones.** A 1.2% deviation is invisible to a sanity check and
fatal to correctness.

**Five rules, each learned by getting it wrong first:**

- **A number that lands where you expected is the one to check twice.** **Five**
  instances in a single day, each a figure that agreed with its author and so was
  never re-run:

  - `$?` after a pipeline or command substitution belongs to the last thing that
    ran, not the thing under test. It twice reported success where there was
    failure — a solver that had correctly refused a poisoned config, and a test
    suite carrying two failures.
  - An audit split `find` output on bare whitespace instead of newlines,
    inflating the file count while silently dropping 70 configs. It surfaced only
    because a later run with a *narrower* filter returned *more*.
  - A test proposed to prove a run never happened — `grep -c 'chunks'` — counts
    **lines**, and the progress writer emits `\r`. It returned 1, which would
    have confirmed the hypothesis it was designed to test. The run had in fact
    completed all 37 chunks. Counting records instead of lines reversed the
    conclusion and moved the excluded tranche from 98.6 M to 138.7 M.
  - Three consecutive progress reports of `~40%`, `~41%`, `~44%` on a run that
    elapsed time placed at **70–72%**. They incremented smoothly, which is what a
    number carried forward and nudged looks like, and the ETA riding on them was
    six hours out. The next measured reading was 71.1%.

  The common shape is not carelessness; it is that **nobody re-runs a check that
  agrees with them.** A passing check is where a broken harness hides. Every
  verdict in this project that arrived pre-agreed — the stemmed base rate, the
  two agreeing tallies, the zero exit codes, the shredded audit — was wrong or
  unfounded.

- **A single source of truth kept in two places is a running sum by another
  name.** The ledger existed as two copies — the published tree and the working
  tree — and they silently diverged: a patch went into one only, so the other
  kept an older parser. This is the same failure the maintained tally had, one
  level up. Whatever computes a figure must exist once, and the copy that gets
  run must be the copy that gets published.

- **A pattern match against §8 needs a base rate before it counts.** The artwork
  is full of numbered sequences, absences and near-misses. "This looks like the
  author's signature" is a hypothesis with a prior, and the prior is usually high
  enough to explain the observation on its own. Four of §8's five entries were
  retired by asking, once, how often the artwork produces that shape by accident.
  The one that survived did so because it had an independent measurement behind
  it, not because it looked more like a signature.

- **A reported elapsed time is a measurement, not a recollection.** **Seven** of
  this project's wrong numbers have been timings or rates:

  ```
  a cold chunk reported as a sustained rate
  a model quoted where a measurement was available
  an elapsed time never taken
  a fabricated progress reading (40.8%, invented, with a future timestamp)
  three consecutive status lines ~30 points below what elapsed time allowed
  an ETA carried forward for six hours without recomputation
  microbenchmark staging figures (1.18x, q > 22.8%) quoted as measured
  ```

  Survivor counts are z-tested against an exact expectation on every run;
  timings get quoted from memory. Same project, two standards — and it is the
  unexamined one that keeps failing. **A figure passed between collaborators
  carries the command that produced it, or it is not reported.** Stated as a
  producer's duty it failed repeatedly; it holds only when the consumer refuses
  to compute on a number that arrives as prose.
- **Agreement between two methods validates only the paths both take — so when
  two checks agree, compare the intermediate values, not just the verdicts.**
  Two independent tally implementations agreed to the candidate while sitting on
  a defect in a branch neither exercised. Separately, two reviewers independently
  stemmed the same word list and both reached "fewer empty lines than chance";
  the error surfaced only when the expected counts were placed side by side
  (1.94 against 3.25). A failed control announces itself. A control that agrees
  with you is invisible, and agreement on the conclusion is the weakest evidence
  the two methods can produce.

---

*Published so these paths are not re-walked. If you have a word for slot 21,
evidence placing 22–24, a resolution of slot 11, a genuinely larger source
image, or a legible view of the final rune glyph — that is worth more than any
amount of GPU. A corrected template can be tested in seconds.*
