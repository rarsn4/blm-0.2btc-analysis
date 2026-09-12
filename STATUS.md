# 0.2 BTC Puzzle — full status

**11 September 2026.** For both collaborating agents. Supersedes all earlier
handoffs.

Target `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`,
hash160 `ccbd031e54cde2a3189fd59bc49f731367a1779e`.

**Not solved. The compute is finished.** Every hypothesis anyone has been able
to formulate has now been tested. What remains is either infeasible or
undefined, and §7 says which.

---

## 0. Epistemic tags

| tag | meaning |
|---|---|
| **[MEASURED]** | re-derived from the image, wordlist or chain. Reproducible. |
| **[EXHAUSTED]** | a complete space enumerated, empty. |
| **[TESTED]** | a finite corpus tried, empty. **Not** an elimination of the class. |
| **[INFERRED]** | follows from measured facts by a stated argument. |
| **[ASSUMED]** | load-bearing but unproven. The soft spots. |

The [EXHAUSTED]/[TESTED] distinction is the one that matters. Conflating them
would be the only overclaim in this record, and it has been caught twice.

---

## 1. [MEASURED] The rune cipher is solved

Monoalphabetic substitution over **Cyrillic**, not Greek. Both circulating
readings were wrong at the alphabet level: "HELLO : FROM : THEM" maps Φ to both
H and M, and a substitution is a function.

```
Сумма двух чисел  =  ◇⏶ᛗᛗ△ : ⇧⧗⏶⤬ : ⊤Ψ◇⫽ᛉ

С=◇  у=⏶  м=ᛗ  а=△     д=⇧  в=⧗  х=⤬     ч=⊤  и=Ψ  е=⫽  л=ᛉ
я=木  н=⊥  ь=⊤  ю=⧓  б=ᐭ  т=⊔     plus  п р и с ы
```

Evidence: same-letter glyphs correlate **+0.63** against **+0.07** for different
letters; the doubled `м` in `Сумма` uses the identical glyph twice; thirteen
letters verified across two independent inscriptions; token group sizes
(5/11/8/2/6/4/5/1 on the edge, 5/4/5 on the clock) reproduced by ink-profile
segmentation — a wholly different method. This also validated the community's
Russian translation, which nobody had checked.

**Reading geometry.** The right-edge inscription runs **bottom-to-top** on the
master; `pictures/20_1.png` is a cleaner de-rotated render and is what to use.
The clock line reads left-to-right, ink at luminance ~160–200 — use a levels
stretch, not a hard threshold. The two ciphers share shapes with **different
values**: `◇` is `W` in the Gravity Falls Latin cipher and `с` in the Cyrillic
one. Do not cross-apply.

---

## 2. [MEASURED] The position mechanism

The clock assigns slots by summing adjacent numerals. The runes beneath state
it: *"sum of two numbers."*

| source | reading | slot | word |
|---|---|---|---|
| minute hand | 1 + 2 | 3 | `tower` |
| second hand | 12 + 1 | 13 | `moon` |
| hour hand | 10 + 11 | **21** | **blank** |
| `.VS.` flipped **vertically** → `·12·` | | 12 | `vote` |

A geometric fit — centre (470, 937), radius 180, 30°/hour — predicts **all five**
documented readings from a single rotation offset to within 3°.

**The pyramid is an occluder, not a second machine.** The same fit places the
"4+5 = 9" and "5+6 = 11" readings on the clock's own numeral ring, and **clock
numeral 4 is directly visible** through the translucent ray field at (605, 818)
against a predicted (599, 812) — 2.9°, inside fit noise. That converts the
occluder argument from extrapolation to observation, and explains why the
masonry carries no marker at 7×: there was never meant to be one.

**[MEASURED] Parity.** Consecutive integers sum to 2n+1, always odd. The clock
can produce only {3, 5 … 23} and **never an even slot**. Every filled even slot
comes from a count or a written number instead.

**[MEASURED] The self-naming pattern.** Every confirmed slot has the object
supply *both* the number and the word — two cameras → `camera`, four masked
faces → `mask`, M16 → `rifle`, XX and the *second* King → `second`. That is what
makes those assignments non-circular, and it is the test a proposed mechanism
must pass.

**[INFERRED] Length is 21 or 24.** Slot 21 exists, so 12/15/18 are excluded.
Independently: at 12 words order is brute-forceable in minutes, so an author who
built a position machine did so because order cannot be searched.

---

## 3. [MEASURED] Six defects in the community's shared data

| claim in circulation | reality |
|---|---|
| `breathe` is the passphrase / a seed word | **not in BIP39.** Neither is `breath` |
| `they` #1796, `that` #1791, `time` #1810 | off by one — those are 0-based. 1-based: **1797, 1792, 1811** |
| `any` is #84 | **#82** 1-based, #81 0-based |
| `candidates_unplaced.txt` is complete | missing `they`, `that`, `time` |
| `1713 → stock` | correct 1-based; the spec's 0-based encoding gives `stomach`. Test both |
| section 14 lists only letter-typos | **an entire phrase is missing** — "a trusted" is absent from the E of BRAVE, with the `introdue` typo at the exact splice |
| `.VS.` means a 12-word phrase | it is a **slot marker**. Flipped **vertically** it reads `·12·` |

Words in circulating candidate lists that are **not BIP39 words**: `breathe`,
`breath`, `stop`, `freedom`, `hate`, `white`, `death`, `kill`, `war`, `money`,
`buy`, `trusted`, `slave`, `duly`, `convicted`. Check membership before building
on any list.

---

## 4. [EXHAUSTED] What the search has closed

**78,273,080,964 full seed derivations. 2,265 CPU-days.** BIP39 and Electrum v2,
four paths, indices 0–35, every legal template length, pools from 37 to 80
words, template reversal, position offsets, 65 passphrases, leave-one-out over
the entire 2048-word dictionary at every gap, free-one-fixed across all 13 fixed
words, and the all-slots-vary sweep under both schemes.

**7,939,492,344 brainwallet addresses**, counted separately — the unit is ~31×
cheaper than a seed derivation (489,000/s against 15,600/s measured), so folding
them into one total would inflate the figure with work that is not the same work.

### The 21-word campaign, completed this week

| run | scope | result |
|---|---|---|
| `t21_readme54` | all six gaps over the 54-word pool | exhausted |
| `t21_loo21` | slot 21 over **all 2048** | exhausted, survivor count **exact** |
| `t21_loo{6,8,14,15,18}` | each slot over **all 2048**, `second` at 20 | all exhausted, every count within 2σ |
| `t21_written` | 67-word pool incl. the printed words | exhausted, +0.8σ |
| `t24_tail{54,67}` | slots 21–24 = `this/future/first/liberty` | exhausted |

**[INFERRED] The deduction that closes:**

> Given the table as written, **no single out-of-pool word at any gap position
> produces the target address at 21 words.**

`t21_loo21`'s count was **exact** — 11,639,827,456 — because slot 21 is the last
word and carries all 7 checksum bits, so precisely 16 of 2048 pass per prefix.
Zero sampling variance. It also proved the mid-sweep swap to the Jacobian binary
introduced no gap or overlap. **Put the `@FULL` slot last whenever the template
allows it**; it converts the survivor count from a statistical check into an
exact one, for free.

### [MEASURED] Two wordlists are impossible, not untested

Electrum v1's 1626-word list lacks 7 of the 15 table words (`camera`, `police`,
`liberty`, `pyramid`, `vote`, `rifle`, `gold`) and `food`. Russian BIP39 lacks 9
of 20. Both die at the vocabulary stage, before any algorithm is needed.

### [MEASURED] Image and chain are closed

No steganography (LSB 0.498/0.500/0.505), alpha fully opaque, no JPEG history
(block-edge 0.985/0.910), chunks are `IHDR, sBIT, IDAT×293, IEND` — **no sRGB**,
two separate analyses have asserted otherwise. No larger source exists:
`i.redd.it` serves the same 1600×1200 file, md5-identical. No `OP_RETURN` in any
of five transactions; `spent_txo_count: 0`. The funding wallet is `version 1`,
`locktime 0`, `sequence 0xffffffff` — a custodial batcher, so it reveals nothing
about the seed software.

**Do not use AI upscaling.** The signature reads `-yi-` under Lanczos and renders
as a boxed `ER` through VanceAI at 8×.

---

## 5. [ASSUMED] Where the table is weakest

**This is where the answer is, if it is anywhere.**

**`black` at slot 10 has no derivation.** Its entire justification is the rune
sentence `чёрный день номер X` — "black day number X" — and X is the one glyph
nobody can read. The reasoning is: black's slot comes from X → X is unreadable →
10 is a guess. Load-bearing since 2020 and never questioned until now.

Every position of `black` at 18 words was tested (slots 6, 8, 14, 15, 18) and is
eliminated. At 21 words its alternatives are 21–24, and 21 is now exhausted.

**`apple` at slot 20 has no derivation either.** It appears **once** in the
entire README, in the table row, with an empty description column — while §19
gives full provenance for `second` at the same slot (XX on Leopold's head → 20;
Leopold II was the *second* King of the Belgians, #1556). All recent sweeps pin
`second`; the `apple` variant is deferred, not eliminated.

**Slot 14 has no mechanism at all.** A systematic clustering sweep with a
**passing control** (45 blobs against a known 44 stars) found no countable object
set of size 14 anywhere in the artwork. The apparent hits were letter counts in
slogan text — 648 acceptance opportunities across 108 parameter configurations,
which is what multiple comparisons produces for free.

**Slot 11 is contested.** `pyramid` (5+6) versus the Space Needle "marks the 11".
Freeing slot 11 found no candidate fits, which suggests the conflict runs deeper
than a two-way choice. The CCTV junction box bears a pyramid symbol, visually
linking `camera` and `pyramid`.

**Slot 8's mechanism is measured but unsupported.** Leopold's coat has **eight
buttons** — four pairs matching across columns within 1 px, epaulette excluded on
fill density, independently confirmed via `scipy.ndimage.label`. But a coat has
no canonical count to deviate from, the object supplies **no word**, and with
~20 countable sets in the image you would expect ~1.6 hits on an open slot by
chance. **[MEASURED] as a count, [NOT SUPPORTED] as a slot mechanism.**

---

## 6. [MEASURED] The final glyph is unassignable in principle

`номер X` ends the right-hand inscription. The glyph occurs **exactly once** in a
68-glyph corpus, has **no entry in the Gravity Falls key** (checked against both
the pyramid and the Wheel of Intrigue — Russian needs 33 letters and the GF set
supplies 26, so the author invented extras), and every letter it could be is
equally unattested.

**Linguistic exhaustion:** 28 of 33 Cyrillic letters appear across the three
plaintexts. The five absent are `ж ц щ ъ э`. Of those only `ц` carries a Church
Slavonic numeral value (900), and its shape does not support it. **Shape:** a
vertical stroke crossed by a single diagonal, one arm up-right and one down-left.
`ж` is refuted on **arm count — 4 against 6**.

> **A better scan does not fix this.** It renders the shape more crisply and
> still cannot say which letter it is. The missing thing is a key, not pixels.
> **Deprioritise the hunt for a larger source image** — and none exists anyway.

*Dependency:* this argument inherits the published plaintexts. If any word in
them is wrong, the letter inventory shifts and the absent-five set with it.

---

## 7. What is left, and what is not

**Blocked on reading, not compute:**

1. **A derivation for slot 14** — no mechanism, and the clustering sweep says
   there is no countable set of that size to find.
2. **Provenance for `black`@10** — or its removal. This is the most load-bearing
   assumption in the table.
3. **Slot 11 resolved** — `pyramid` versus Space Needle.
4. **A word for slot 21** — the only hand carrying nothing.

**Infeasible:** two out-of-pool words at 21 words is ~875 h even post-Jacobian;
t24 with nine open gaps is ~17 years.

**Do not do:**
- **More words in a gap pool.** Leave-one-out swept every gap against the entire
  dictionary at both 18 and 21 words. No pool addition can succeed unless two or
  more gaps simultaneously need out-of-pool words, and at that point the fixed
  words are the constraint.
- **A higher-resolution image.** See §6.
- **AI upscaling.** See §4.

**[INFERRED] The honest shape of it.** P(all 14 fixed words correct) ≈ 1% by the
table's own confidence ratings. The completed campaign tested the branch where
they are all correct and one gap word is outside the pool. The other branch —
a fixed word is wrong — carries **~99% of the probability and no sweep reaches
it**, because searching it requires knowing which word is wrong, and if you knew
that you would not need to search.

The lock is now understood in detail. The key is no closer.

**[INFERRED] Six years untouched is positive evidence.** Bots sweep weak keys —
small integers, dictionary brainwallets, common constants — within minutes,
continuously, for a decade. That this address is still funded means the key is
unreachable by every generic method. Whatever the rule is, it depends on the
image.

**The bait possibility remains live.** BIP39 permits an optional passphrase
outside the wordlist that completely changes the derived key. If the author used
one, no amount of correct word-finding opens it, and the puzzle would look
exactly as it does.

---

## 8. [MEASURED] The pattern worth naming

The author systematically **marks a thing and withholds it**:

| marked | withheld |
|---|---|
| a third clock hand, precisely at slot 21 | no word on it |
| `introdue` typo at the exact splice | the deleted phrase "a trusted" |
| `номер X` — "number X" | a glyph with no key entry, occurring once |
| `1865 - 202…` | a literal `?` |
| 44 stars where everyone knows 50 | the 6 |

This is the best account of *why* the puzzle resists. It also implies the
positional machinery being over-specified while every word is underdetermined is
**by design** — which would mean the words come from outside the image, and the
artwork only ever supplied the ordering.

---

## 9. The tooling — why the negatives mean something

CUDA pipeline, ~3× faster since replacing affine double-and-add with **Jacobian
coordinates** (~384 modular inversions per scalar multiplication down to one).
All three multiplications are fixed-base; the coordinate change was the win, not
a comb table. Measured 6.5× on the multiply, **2.96–3.05× end-to-end**, EC share
**81.8%** by 1-path vs 4-path timing.

**Two positive controls that require *finding*, not verifying** — blank slots of
a known mnemonic and demand recovery. Single-chunk (`selftest_find`) and
multi-chunk (`selftest_multichunk`, crossing nine boundaries).

**Seam validation** — survivor counts identical at seven chunk sizes down to
`--chunk 7` (599,187 chunks); production count reproduced against a **previous
binary**; the answer found planted first-of-chunk and last-of-chunk.

### Ten bugs, every one producing plausible output with no error or warning

1. SHA-256 schedule error — 6.39% checksum rate against a true 6.25%
2. 24-word HMAC key pre-hashing omitted (RFC 2104)
3. Benchmark timing 20-bit scalars instead of 256-bit
4. Single-block `hmac_sha512`, valid only to 119 bytes
5. Chunk sizing assuming exact rather than binomial survivor counts
6. A canonical address recalled rather than computed
7. `BigInteger.Parse` misparsing odd-length hex
8. **`show_hit` reporting the wrong derivation path** — the only one that
   corrupts a *success*; it fires only on a hit, so nothing but a hit could have
   exposed it
9. **Global checkpoint path** — any second run destroyed a sweep's resume point.
   Audited backward: no completed sweep affected. Its fix has since prevented
   two concrete losses
10. `uint64_t[4]` passed to a 5-limb `_ModInv` — caught by the differential
    oracle on first execution

**Branch on measured length, never word count.** 21-word mnemonics are only
**80.6%** over the 128-byte HMAC threshold — one in five must *not* be
pre-hashed. 24-word is 99.9976%, not 100%.

---

## 10. The rule that keeps earning its keep

> **Run the falsifying check before the result looks reasonable, not after.**

Every failure here has the same shape: a number was produced, it looked
plausible, and the cheap in-domain control that would have killed it went unrun.
The `ж` template, the Gravity Falls harness, the pyramid course count, a
throughput taken from one cold chunk, three failed book discriminators, a
14-sweep with 648 acceptance opportunities.

Two corollaries earned the hard way:

- **A similarity metric must be calibrated on known-answer pairs from the same
  medium.** Correlation across a medium change — hand-drawn against printed,
  composite against component — has no established discriminating power, and a
  number produced without that calibration is not evidence **in either
  direction**. The GF harness ranked the known TUESDAY glyphs 5th, 10th, 21st
  and 14th of 26. It never refuted `ж` either; arm count did.
- **A control needs its own control.** The band-texture test *produced* an error
  rather than catching one, because nobody asked what it returns when pointed at
  a blank region. It manufactures brick texture from empty space.

And: **check boundaries = regions + 1.** The pyramid count was short by one
boundary and would have flagged itself.
