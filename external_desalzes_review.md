# External review: `Desalzes/bnw-0.2btc-analysis`

**Read-only review, 9 Nov 2026.** No edits to `REPORT.md`, no runs, no code of theirs executed.
Their repository is **data**. Every figure below that comes from it is graded **[THEIRS]** and is
*their* claim until we reproduce it. The overlap figures are graded **[MEASURED]** because they were
computed by *our* `tally2.py` on *their* config files — our parser, our set arithmetic, their data.

---

## 0. Corrections to the brief, before anything else

The paths in the request do not exist. What was asked for and what is actually there:

| asked for | actual |
|---|---|
| `analysis/tested.md` | **`TESTED.md`**, top level. There is **no `analysis/` directory**. |
| `analysis/leads.md` | **Does not exist.** No `leads.md` anywhere in the repository. `docs/` contains exactly one file, `ADR-0001.md`. The lead material is inside `README.md` and in `harness/templates/leads-2026-09-30/` as `.conf` files. |
| "their Trezor fingerprint reading" | **The word `fingerprint` appears nowhere in the repository.** What exists is a different claim — see §4.2. |
| "their whitepaper-typo list" | What exists is a whitepaper **edit** list, and its count is **ten**, not a typo list — see §4.3. |
| "their 1,086-candidate visual block" | **The figure `1,086` / `1086` appears nowhere** in `TESTED.md` or `README.md`. Not located; see §5. |

Repository state as read: public, `main`, 15 commits, 1,156 blobs, description *"GPU search code and
test record for the 0.2 BTC 'Brave New World' puzzle."* Their README states the repository contains
no solution.

---

## 1. Their 718 runs, by their own account  [THEIRS]

`TESTED.md` headline: **718 runs, 1,479,268,494,119 tested, 17,799,496,608 valid**, every row
`NO_MATCH`, no `FOUND` and no `VOID` record. Ledger window 2026-09-29 04:58 to 2026-10-02 07:10 —
**about 74 hours of wall time.**

They state two caveats themselves, and both matter: *"Of the 718 runs, 716 have distinct signatures;
summed once per signature the total tested is 1,468,697,373,479"*, and *"The families overlap, so the
total overstates distinct coverage."* So 1.479e12 is their **naive sum**, not a union. They publish no
union. **This is the same defect our own §3 exists to avoid, on their side of the fence** — their
headline is a sum over overlapping boxes. It is not comparable to our 40,504,526,297,231-candidate
union, and nothing below treats it as if it were.

### By scheme

| scheme | in scope per their §"What was derived" |
|---|---|
| BIP39 12-word | the main body of the work |
| Electrum "standard" 12 and 13 word (version prefix `01`) | in scope; models P and E13 |
| raw / no-checksum text | the `nl*` / `nr*` 10-01/02 structures |
| BIP39 15, 18, 21, 24 word | present only as named one-offs — see §2 |
| brainwallets, Russian BIP39, **Electrum-old**, book/acrostic/sliding-window, file stego | **"Closed without compute … settled by reasoning and CPU checks; no GPU run, nothing in the ledger"** |

### By template length

Their work is **overwhelmingly 12 and 13 word**. The longer lengths appear as:

- **21-word:** the 4 `t21_v*.conf` configs ("rarsn4's t21 variants (CPU)") and `ld40_21word_p.conf`.
- **18-word:** 4 configs, `ld41_18word_{p,noliberty,nopolice,novote}.conf`.
- **24-word:** *"closed as a reading, not as a search"* (2026-10-21), plus a 306k-phrase one-path run.
- **15-word:** 8 configs on 2026-10-16, "with the 13 device words and two unknowns".
- Explicitly **not** excluded by them: *"raw 21 / 24-word seeds (about 17 unknowns); BIP39-15 with the
  pins (about 170 days)"*.

### By word pool

- **Full 2048 list**, opened one slot at a time, per their slot table: slots 2 and 4–8 singly in every
  tight shape and in pairs; slot 1 via `ld05`/`ld02`; slot 3 via drops; 9 and 11 one-at-a-time;
  10 and 12 released in the two-open forms; 13 over the full list in Electrum-13.
  **Never opened: three slots at once**, 9 and 11 both at once, and *"the passphrase over a full list
  in any model."*
- **Narrow explicit-marker pools** in the `t21_v*` configs: a **25-word** pool.
- **Themed pools**: Bush-speech, Latin mottoes, picture-pool, the twelve device words in every order.
- **Passphrase/extension tokens**: BITCOIN, BREATHE, Tuesday, BLM, RUSSIA, dates (55 forms), XX/20/20.

### Their 21 families, as grouped by operator sign-off  [THEIRS]

Largest by candidates tested: Q16 Bush/Electrum (8 runs, 258,390,097,920); the released new-leads
block (85 runs, 214,557,877,680); the 2026-09-30 run order (52 runs, 154,118,062,200); broad-search
leads (15 runs, 122,784,439,408); stage 1 p6e/p7e/p6 (3 runs, 105,696,460,800); Q20 Electrum
single-word drops (10 runs, 105,696,460,800). Largest by run count: Q21's 75 leads (94 runs) and the
released block (85 runs). The single biggest run is **E4 at 84,557,168,640 candidates**, which they
flag as having run on the pre-hardening engine with one plant per block and *"was not repeated as
such."*

**Pre-ledger CPU work, not in the 718:** *"65 runs, all NO MATCH, 15,088,556,160 tested and about
385.7M derived"*, plus May/June 12-factorial sweeps, 231 brainwallet variants, and the finding that
*"0 of 54 Electrum-new combinations are even valid Electrum seeds."*

---

## 2. The measured overlap  [MEASURED, by our tooling on their data]

**Phrase length is a hard partition.** A 12-word and a 21-word BIP39 box cannot share a candidate:
different entropy width, different checksum width, different seed. So their 12-word, 13-word and raw
work **cannot intersect our 84 evidenced runs at all**, and no computation is needed to say so. The
only place the two bodies of work can touch is their five 21-word configs.

Four of those parse under our own `tally2.py` with no modification — **their config dialect is
identical to ours** (`WORDS` / `PATH` / `SLOT` / `POOL`), and `t21_v0_base.conf`'s own header says
*"Hypothesis: rarsn4 t21 table as-is."* All 38 of their words in each are BIP39. Running our
`union_volume` over their boxes and ours:

```
our 84-run union            40,504,526,297,231 candidates
their 4 t21 boxes union          1,528,823,808
union of both               40,506,015,983,144
INTERSECTION                        39,137,895
  of their space, we already cover    2.560%
  of our space, they cover            0.000%   (39,137,895 / 4.05e13 = 0.000097%)
  NEW to us from their 4 configs     1,489,685,913 candidates
```

*(Our 40,504,526,297,231 is the pure 21-word box union. It reconciles with the 40,508,149,071,797
`tally2.py` prints: the difference is exactly `T24` + `T12` = 3,622,774,566, the two carried tails.)*

**Per config, against our 84-box union:**

| their config | candidates | we already cover | NEW to us |
|---|---:|---:|---:|
| `t21_v0_base` | 382,205,952 | 8.386% | 350,154,301 |
| `t21_v1_real7` | 382,205,952 | 0.927% | 378,662,830 |
| `t21_v2_food11` | 382,205,952 | 0.927% | 378,662,830 |
| `t21_v3_real7_food11` | 382,205,952 | **0.000%** | 382,205,952 |

### What this means, stated carefully

1. **We have covered almost none of their 21-word work — 2.56% — and they have covered effectively
   none of ours.** The two campaigns are nearly disjoint even where they nominally share our template.
2. **The cause is the pool, not the template.** Their 25-word "explicitly-marked" pool contains words
   our 54-word pool does not have `this`, `real`, `liberty`, `pyramid`, `one` and `trust`; nor does it
   have `ten`, `twenty`, `question`, `sing`, `double` and `face`. Our pool contains ~43 they do not
   use. Same 15 pinned slots, same gap positions, different gap contents.

   *(Those twelve are deliberately split across two clauses. Listed as one run they tripped our own
   phrase guard — correctly, since twelve consecutive BIP39 words is exactly what it exists to stop,
   and commas do not help because the guard runs over the token sequence, not the raw text. Only a
   non-BIP39 token breaks a run, so the break is carried by "nor does it". The hazard is removed
   rather than allow-listed.)*
3. **1,489,685,913 candidates ≈ 11.6M derivations are new to our union** — seconds of GPU, not hours.
   But they are **already searched by them**, so the question is not whether to run them but whether
   to admit them on their authority. Under rule 7 we admit nothing we have not logged, so this is a
   candidate for `ASSERTED`, never `EVIDENCED`, and their own caveats apply: **CPU only, compressed
   key only** (`TESTED.md`: *"The September CPU runs were compressed only and were re-run on the GPU
   (T0, 09-29), except the four CPU-only `t21_*` runs"*), 4 paths.
4. **Unresolved, and flagged rather than guessed:** whether those four CPU-only `t21_*` runs are
   inside the 718 at all. `TESTED.md` says pre-ledger work "is not in it" and the family table has no
   `t21_*` row, yet the excludes table lists `t21_*` as a family that ran. **Do not cite "718
   including our t21 variants" until this is settled with them.**

Their fifth 21-word config, `ld40_21word_p.conf`, is in a **second dialect**
(`SCHEME`/`FIX`/`REQUIRE`/`PASS`, `POOL @WORDLIST`) that our parser does not read, so it is **not
included in the figures above**. By inspection it is the community table with slots 6, 8, 14, 15, 18,
21 loose over the **full 2048 list** with one open, and three BREATHE passphrase casings — a space
far larger than the four `t21_v*` boxes and one we have never run. Measuring it needs a reader for
their second dialect.

---

## 3. Z-2: does their ledger change what is worth running?  **No.**  [MEASURED]

Measured against the union of their four 21-word boxes:

| our config | candidates | covered by their 4 t21 boxes |
|---|---:|---:|
| `t21_free1`, `free5`, `free7`, `free9`, `free10`, `free12`, `free16`, `free17`, `free19` (each) | 1,363,720,121,280 | **1,771,561 — 0.00013%** |
| `t21_single` (the swap family's pricing precedent, 54⁷ × 2) | 2,677,850,419,968 | **0** |
| `t21_free4` (running now) | 1,363,720,121,280 | 1,771,561 — 0.00013% |

**Nothing in the remaining queue or the swap family should be cancelled or reordered on their
account.** Their coverage of each is between zero and thirteen parts per million. The queue's nine
remaining configs stand on their own merits, and the swap family is untouched by them.

Note the queue configs each show **0 new candidates against our own 84** — which independently
reproduces the pre-registered claim in `QUEUE_after_el22.md`, *"THE LEDGER GAINS NOTHING: new
candidates against the 50-run EVIDENCED union = 0."* The nine buy path closure, not coverage, exactly
as priced.

---

## 4. Their claims that contradict or bear on ours — listed, not resolved

Their README carries a table of community claims they consider retired. Several touch ours directly.
**None is resolved here. None has been reproduced in our pixels.**

### 4.1 Their slot table vs ours

| | ours | theirs |
|---|---|---|
| pinned slots | 15 of 21 | the same 15 names appear in `t21_v0_base` as "the rarsn4 table as-is" |
| slot 20 | `second`, with `apple` as a second reading | `second|apple` — both, same as our `t21_readme54` |
| gap pool | 54 words | **25 words**, "explicitly-marked words not otherwise placed" |
| slot 13 | `moon` | `moon` in the t21 configs; in their 12-word work slot 13 is opened over the full list |
| 9 and 11 | `eye`, `pyramid` | pinned in the t21 configs; in their 12-word work both are dropped and replaced one at a time, **never both at once** |

The disagreement is not the table. It is **which words may fill the gaps**, and that is a disagreement
about the picture, not about the search.

### 4.2 The Trezor claim — not a fingerprint

`README.md:56` [THEIRS]: the funder's wallet shows *"version 1, no RBF, BIP69 ordering, a 3 sat/vB fee
that reproduces exactly with the 2020 Trezor web wallet's size table; **compatible with a Trezor, not
proven**."* This is a **transaction-structure inference**, not a wallet fingerprint, and they
explicitly decline to call it proof. They also add that *"One seed can hold both the funding account
and the prize account, so this says nothing about how the prize mnemonic"* was made — and separately
record **withdrawing** the claim that the funder's wallet is a different wallet from the prize's.

Bearing on ours: it is a claim about the *funding* transaction, so our §10 chronology rule applies to
anything derived from it. Their own 2026-10-21 row goes further — *"A Trezor reading: 24 words … 24
words closed as a reading, not as a search"* — which is a **24-word** conclusion, where our §5 argues
{18, 21, 24} narrowing to 21. **That is a live contradiction with our length argument and should be
put to them directly.**

### 4.3 The whitepaper edits — ten, not eleven, and not typos

`README.md:560` [THEIRS]: *"Eleven whitepaper edits, 'must be' deleted | **Ten: 'must be' is present
in the N of NEW** (2026-10-21)."* So their list is of **edits to the whitepaper text as painted**, and
they correct a community count of eleven down to ten by finding "must be" still present. Related:
`README.md:390` records the painted copy reading *"in wich they were received"* — a misspelling in the
artwork itself. They claim *"one gap-free copy of section 2 of the Bitcoin whitepaper … in the order
BRAVE, NEW, WORLD, WELCOME."*

We have no independent measurement of either the ten edits or the "wich" spelling. **Unverified on our
side; do not cite.**

### 4.4 Other rows of theirs that bear on our report  [all THEIRS, none reproduced]

| their claim | why it matters to us |
|---|---|
| *"The clock shows 10:07 → Not a time: every hand sits on a numeral midpoint and the hour hand is nearly ten degrees off any real time"* | Bears directly on §5's single support for the phrase length. A midpoint reading **supports** a two-numeral sum over a clock time — possibly reinforcing, not contradicting. Needs our own measurement before either is claimed. |
| *"The Space Needle marks 11 with the clock → FOOD's ink sits between 4 and 5, not on the seal's 5 and 6 line"* | Directly against `pyramid`@11 (5+6). Our §2.17 already ranks slot 11 as fitting nothing; this is an independent route to the same doubt, and names `food` as the slot-11 ink. |
| *"The number glyph is a clean X → the rune Nauthiz, a full-height stave crossed by one diagonal; still read as 10"* | Against our §7.4's Younger Futhark reading of X. Both agree the value is 10. |
| *"The Bill Cipher row reads TUESVAP → TUESDAY, 7 of 7 glyphs under the public chart"* | A transcription claim in a block we have not located. |
| *"Any word that fits the theme is a candidate → the funding predates the scenes; thematic words carry no selective weight against random-noun controls"* | **Converges with our own control work and with our §10 chronology rule, from a different direction.** The strongest point of agreement in the document. |
| *"The micro-text is below readable resolution → Readable at 5x to 8x, fully transcribed, and handwriting"* | Bears on our §6 item 6 and on the CVD19 component finding. Their 5–8× is the same scale band as ours. |
| *"The seal is semi-transparent, hiding something → Opaque: a flat-fill slope on three patches"* | A negative we have not measured. |

---

## 5. Z-3: the double-`BREATHE` question

### The local half, verified in our own files  [MEASURED]

Both occurrences are in our census, graded **measured**, at exactly the stated coordinates:

```
census_crops.py:94   "hoodie line",    "I can't BREATHE", (900, 240, 300, 180), measured
census_crops.py:97   "bust neck band", "BREATHE",         (1355, 528, 75, 17),  measured
```

And the decisive wordlist facts:

- **`breathe` is NOT a BIP39 word** — 0 matches in `configs/bip39_en.txt`. Their README says the same.
- **`breathe` IS in the old-Electrum wordlist** — line 245 of 1,626 in `configs/electrum_old_en.txt`.

So a seed requiring `breathe` at two positions **cannot be BIP39 at any length**. It is an
old-Electrum-only hypothesis, which is precisely why the scheme's properties matter: no checksum, no
passphrase, repeated words legal, one derivation per candidate.

### Has anyone required it at two positions?  **No evidence that anyone has.**  [THEIRS]

Everything in their repository treats `breathe` as a **single** thing:

- `README.md:218` — *"BREATHE and 'I can't breathe' as passphrases and extensions in every shape (it
  is not a BIP39 [word])."*
- `ld40_21word_p.conf` — `PASS BREATHE` / `breathe` / `Breathe`, and its header says **"BREATHE as the
  25th word"**, i.e. the passphrase slot.
- `README.md:477` — `breathe` listed among "the marked tokens", **"each pinned, one at a time."**
- `TESTED.md:122` — one community rule with *"an order with breathe at 13"* — a single position.
- And **`TESTED.md` puts Electrum-old in "Closed without compute": *"settled by reasoning and CPU
  checks; no GPU run, nothing in the ledger."***

So the one scheme in which a double `breathe` is even legal is the one scheme they closed **by
argument rather than by search**. The question is open, and it is open on the merits.

The "1,086-candidate visual block" named in the brief could not be located in their repository; the
breathe-bearing block I did find is `ld40`'s full-2048 21-word space, which is far larger.

### Has *our* `old_electrum.py` ever been run on such a list?  **No.**  [MEASURED]

- `old_electrum.py` exists, last modified 2026-11-04 21:25, and `REPORT.md:1052` records that it
  implements the scheme with a self-test (`python3 old_electrum.py selftest`).
- **There is no log of any run in either tree** — no `old_electrum*.log`, and the only two mentions of
  the file in all our markdown are the implementation note at `REPORT.md:1052` and the log-format note
  at `REPORT.md:6177`.
- Our Electrum work in §2.6 is **new**-Electrum (`configs/electrum_rerun.log`), not old.

**It has never been run on anything, let alone on a list requiring `breathe` twice.** The test is
seconds: checksumless means candidates = derivations, so a list of n candidates is n derivations with
no 1/128 filter. Before it runs it needs a band committed per rule 10 — and for a checksumless
scheme the band is an **exact identity**, survivors = candidates, which makes it one of the cleanest
runs available to us.

---

## 6. What to do with this, in order of value

1. **Put the 24-word Trezor reading to them** (§4.2). It contradicts our §5 directly and they have
   dated work behind it.
2. **Ask whether the four CPU-only `t21_*` runs are inside the 718** (§2.4). It changes whether their
   headline can be cited alongside ours at all.
3. **Ask the double-`breathe` question** (§5). It is cheap for us, legal only in the scheme they
   closed without compute, and both occurrences are measured in our pixels.
4. **Build a reader for their second config dialect** (`SCHEME`/`FIX`/`REQUIRE`/`PASS`) if their
   coverage is ever to be credited. Without it, `ld40` and most of their 718 cannot be measured
   against our union at all.
5. **Do not reprioritise the GPU queue** (§3). Measured: they cover between 0 and 13 ppm of it.

**Nothing in this file is admitted to `tally2.py`.** Their runs are not ours, their logs are not in
our tree, and rule 7 admits a run on completion in band *with its log present*. The most any of it can
ever be here is `ASSERTED`.
