# REPORT.md additions — drafted 23 Sep, ready to apply

Everything here is final except the four bracketed tally figures in §3, which
fill in when `free4/16/12/19` land Sunday. Apply with a patch script against the
live `REPORT.md`; don't paste by hand.

Every number in §8 and §9 is reproducible from a script in the project root:
`clock.py` (0.01 s over the full 12-hour cycle, all six hand-to-angle
assignments) and `slogan_lines.py` (needs `mnemonic` only). Both were run
independently on two machines and agree to the digit.

---

## §2.13 — [EXHAUSTED] Free-one-fixed at 21 words: the branch that was never run

Insert after §2.12 (brainwallets), before §3.

> Every t21 sweep before September freed a **gap** — slots 6, 8, 14, 15, 18, 21.
> Not one freed an **assigned** slot. An audit of all twenty t21 configs confirmed
> it: the only assigned slot ever varied was 20, and only as a two-way
> `apple|second` list. Free-one-fixed existed at 18 words and nowhere else.
>
> So "a fixed word is wrong" was not an infeasible branch. It was an untested
> one. You do not need to know *which* word is wrong; you iterate over which.
>
> **This matters more than the count suggests.** At p ≈ 0.75 per assigned word:
>
> | assigned words wrong | probability mass |
> |---|---|
> | 0 | **1.8%** |
> | 1 | 8.3% |
> | 2 | 18% |
> | 3–4 | 46% |
>
> **Roughly 78 billion derivations went into the 1.8% branch**, against
> **138,502,824,811** into the 8.3% branch once free-one-fixed was run. That is
> not a criticism of the work — the branch had to be closed, and closing it is
> what turns a conjecture into a deduction. But stating it plainly is what makes
> the next decision legible.
>
> **[EXHAUSTED] The deduction, stated at full strength.** Let *a* be the number of
> assigned words that are wrong and *g* the number of gap words outside the
> 54-word pool. The completed runs exclude:
>
> ```
> a = 0, g = 0                          t21_readme54
> a = 0, g = 1                          t21_loo_k, six ways
> a = 1, g = 0  (13 slots, 55 cands)    free-one-fixed
> ```
>
> So **a + g ≥ 2** — the answer departs from the README's reading in at least two
> places. One hole remains: `a = 1` at slot 3 (`tower`) or 13 (`moon`), which were
> deliberately never freed, or a replacement outside the 55.
>
> This is stronger than the earlier statement that "at least one gap word is
> outside the pool," which was true but understated: the six leave-one-out runs
> already swept each gap across the entire dictionary, so the single-surprise case
> was closed six ways over.
>
> **Method.** Each run frees one assigned slot to the 54-word README pool plus
> that slot's own table word (55 candidates; 56 at slot 20, which carries both
> `apple` and `second`), with the six gaps over the full pool, `second` pinned at
> slot 20, on the primary path `m/44'/0'/0'/0/0`.
>
> Staging by path rather than running all four costs **1.565× overhead** against a
> break-even at **q > 63.4%**, where *q* is the chance the answer sits on path 1.
> Those figures are from production — `P = 6.209 µs` shared, `X = 1.195 µs` per
> path, derived from `T4/T1 = 1.484` (see §10) — and they **supersede an earlier
> 1.18× and 22.8% taken from a microbenchmark.** The decision still goes the same
> way for a legacy address under BIP44, where `m/44'/0'/0'/0/0` is the dominant
> convention, but it is a much closer call than the original figures implied and
> should not be described as comfortable.
>
> The 89 h quoted below for stage 2 reconciles with these numbers to 2%
> (`3 × (P+3X) × 10,654,063,447 = 87.0 h`), which is what confirms it as a real
> figure rather than a projection.
>
> **Results — thirteen slots freed, all negative.** Each run **21.910 h ± 0.32%**
> (six back-to-back runs, measured from checkpoint mtimes), **284.8 h / 11.9 days**
> for the campaign. Every survivor count is within 1.1σ of its exact binomial
> expectation of **10,654,063,447** (σ = 102,815).
>
> The last four to land were the self-naming slots, run together:
>
> | run | freed | survivors | deviation |
> |---|---|---|---|
> | `free4` | `mask`@4 | 10,654,138,418 | +0.73σ |
> | `free16` | `rifle`@16 | 10,653,972,836 | −0.88σ |
> | `free12` | `vote`@12 | 10,654,012,263 | −0.50σ |
> | `free19` | `glove`@19 | 10,654,167,169 | +1.01σ |
>
> **[MEASURED] What these four do not establish.** Each asks *"is this word wrong,
> and is its replacement among the 55?"* A negative is equally consistent with the
> word being **right** and with it being **wrong while the right word sits outside
> those 55**. The two do not separate, so four negatives return the status quo and
> say nothing about whether the self-naming mechanism is reliable. Only a hit would
> have been informative — and a hit would have solved the puzzle outright.
>
> | slot | word | why it was weak |
> |---|---|---|
> | 10 | `black` | **zero derivation** — rests entirely on the unreadable glyph |
> | 20 | `apple`/`second` | freed across all 56, superseding the provenance question |
> | 11 | `pyramid` | the contested pyramid / Space Needle slot |
> | 1 | `subject` | the README hedges it in writing |
> | 7 | `liberty` | canon-assumed; 5 spikes measured directly, 2 inferred |
> | 5 | `police` | "line five" needs a convention nothing else in the table uses |
> | 17 | `gold` | "17 years" is a chart-span reading, not a count |
> | 9 | `eye` | occluded clock position, inferred from the fit |
> | 2 | `camera` | the README's own `twin` hedge |
> | 4 | `mask` | self-naming — four masked faces |
> | 16 | `rifle` | self-naming — M16 |
> | 12 | `vote` | self-naming — the `.VS.` ambigram |
> | 19 | `glove` | self-naming — the CVD19 vial |
>
> **Two of these settled standing questions rather than merely eliminating
> words.** Freeing slot 20 across all 56 candidates **supersedes** the
> `apple`-versus-`second` provenance argument — neither works, so the argument is
> retired rather than resolved. And `black`@10, load-bearing since 2020 on nothing
> but a glyph nobody can read, is now tested rather than assumed.
>
> **Scope, stated exactly.** What is eliminated is "the assigned word at slot *n*
> is wrong **and** its replacement is one of the 55 README-derived candidates."
> Not "the assigned word at slot *n* is wrong." Freeing to the whole dictionary is
> 1,216 h per run and was not done.
>
> **Two slots were deliberately not freed.** `tower`@3 and `moon`@13 are **written
> on the clock hands themselves**. Freeing them would not test an inference — it
> would test whether the puzzle's own labels are wrong, and if they are, no
> ordering of sweeps recovers from it. Excluded by choice, not oversight.
>
> **Stage 2 was declined.** Paths 2–4 on three slots costs 89 h and covers 0.33%
> of total probability, against 1.4% for the six remaining slots at path 1 — four
> times worse per hour, and the lowest-value run on the board. The argument that
> justified staging by path is the same one that rules out revisiting those paths.

---

## §2.14 — [EXHAUSTED] Two hypotheses the source document itself named

Insert after §2.13.

> The README hedges exactly twice, and both hedges have now been tested.
>
> **Row 1:** *"Appear in the section 1 (13th) or it could be 14?"* Tested as
> `t21_swap114` — `subject` moved from slot 1 to slot 14, slot 1 opened to the
> pool, all four paths. 49,589,822,592 candidates, +0.27σ, negative.
>
> This one mattered because slot 14 had already been closed on the image side by
> both routes the author used elsewhere: a clustering sweep with a passing control
> (45 blobs against a known 44 stars) found no countable object set of size 14,
> and a region-by-region review found no written numeral. The README's own
> question mark was the only documentary candidate left.
>
> **Row 2:** *"Two cameras. Maybe could be 'twin' word?"* Tested by freeing
> slot 2 to 55 candidates including `twin`. Negative.
>
> **[INFERRED] From this point, every remaining hypothesis is one we construct,
> not one the document offers.** That is a different epistemic footing from
> everything preceding it, and the distinction is worth preserving: earlier
> negatives eliminated readings someone could point at; later ones eliminate
> readings we invented.

---

## §3 — Tally: replace the section entirely

The published figure (26,513,178,774) predates the entire free-one-fixed
campaign, and the method that produced it was wrong independently of that.

> **The tally is computed, not maintained.**
>
> It had been kept as a running sum with per-change patches, and it drifted. Two
> independent reconstructions on 23 September differed by 331 M, and tracing the
> gap showed **both** were wrong: one used the solver's *reported* per-run
> expected value instead of exact `space/128` (+194 M), the other omitted ~1.14 B
> of runs. Neither was reproducible from its own inputs.
>
> The deeper defect was double-counting. Every run on the same template shares
> the all-pool core, so summing counts that core once per run — **3.72%** of the
> naive total across the t21 campaign. Of the twelve older t21 runs, **37% was
> already covered** by newer sweeps.
>
> `tally2.py` replaces the sum. It parses the run configs directly — so a row
> cannot drift from the config it claims to describe — and computes the union by
> box disjointification with real set intersections. Run it as
> `python3 tally2.py configs`.
>
> ```
> t21 campaign, 22 evidenced runs     [FIGURE] derivations
> + the twelve older asserted runs    [FIGURE]
>     marginal of the twelve          [FIGURE]
>     at 400 derivations/s            [FIGURE] CPU-days
> ```
>
> **What "derivations" means here, exactly.** A 21-word mnemonic carries seven
> checksum bits, so one sequence in 128 is valid and the ledger reports
> `⌊candidates / 128⌋`. **That is a convention, not a count.** The true number of
> checksum-valid mnemonics inside a given template is a determinate integer that
> nobody has enumerated, and per-run survivor counts scatter binomially around
> `N/128` — which is why every run is z-tested against that expectation rather
> than required to equal it.
>
> The convention has a rounding choice inside it, and the choice is visible:
> `⌊(A−B)/128⌋` and `⌊A/128⌋ − ⌊B/128⌋` differ by one on the current figures
> (3,609,899,906 against 3,609,899,907). Both are defensible in isolation. The
> ledger prints the two totals, so the marginal it quotes **must** be the
> difference of the two printed figures or the three numbers on the page do not
> reconcile. Floor once, at the point of reporting, and derive every difference
> from the reported values.
>
> **No single grand total is quoted, and that is deliberate.** The previously
> published figure (26,513,178,774) was a running sum that already included the
> twelve older t21 runs, and whether it counted them at naive size or with overlap
> removed is unrecorded. Subtracting them to isolate a pre-t21 residual therefore
> rests on an assumption nobody can check — the residual is somewhere between
> roughly zero and the whole 26.5 billion.
>
> The t21 figure above **is** computed, and every digit reproduces from
> `tally2.py configs`. Adding an unverifiable constant to it would make the sum
> less trustworthy than either part. Where one number is needed, **"over 190
> billion derivations eliminated"** is a floor that is computed, in preference to
> an estimate that is not.
>
> **EVIDENCED versus ASSERTED is deliberate.** Runs with logs present in the
> working tree are separated from runs included on report alone. A config is not
> evidence that a run happened, and a ledger that reads configs cannot tell the
> difference.
>
> An earlier size-based inclusion-exclusion (`tally.py`) is retained. It agrees
> with `tally2.py` to the candidate on the declared runs but is **exact only
> where the per-dimension sets nest**, which the older runs do not: `readme54`(54)
> is not inside `trust21`(69), and `trustonly`'s pool is disjoint from every
> other. Taking `min()` there would overstate intersections and so understate the
> union — wrong in the flattering direction.
>
> **This supersedes the hand-derived `5·L − 4·R` subsumption note** previously
> carried in this section for the t18 leave-one-out family. That formula was
> correct for that one family and does not generalise; `tally2.py` computes the
> same quantity for every family without a closed form. One method, stated once.
>
> **One tranche is knowingly excluded.** Three runs on 14 August used an earlier
> CPU solver (`template_solve.py`, 16 workers) in `~/Downloads/puz2/files/` with
> **no config file at all** — the template lived in the Python. All three
> completed and exhausted without a match — **138,707,999 derivations**, 0.096% of
> the ledger. They are not rows and cannot be: the logs print `37 candidates` per slot
> but not *which* 37, and the pool file they were given no longer exists. Without
> the pool there is no set, and hand-entering a guessed one would be exactly the
> maintained-tally failure this section exists to end. **A run with no config is a
> run with no provenance, whatever its log says** — so it is stated here and
> counted nowhere.
>
> Those three were invisible to a config-based audit by construction. They were
> found by inventorying *logs* instead, which is the dual check and the only one
> that can see a run whose config never existed.

---

## §7.7 — NEW subsection, inserted after §7.5 and before §8

**There is no "pattern" section in REPORT.md.** The five observations were made
separately, in §1.4, §2.7, §5, §6 and §7.4, and only later read together as a
deliberate authorial signature. That reading is what is retracted, so it needs a
place of its own rather than an edit to any one of them.

Inserted as `### 7.7` at line 666, immediately before `## 8. Do not use AI
upscaling on this image`, which is **untouched**.

> Five observations in this document were at one point read together as a
> deliberate pattern — the author marks a thing and then withholds it — and an
> inference was drawn from that pattern: that the seed words come from outside the
> image and the artwork supplies only the ordering.
>
> | where | observation |
> |---|---|
> | §1.4 | the phrase **"a trusted"** deleted from the whitepaper micro-text |
> | §2.7, §5 | the **blank clock hand** at the 21st position |
> | §6 | the flag's **star deficit**, 50 − 44 = 6 |
> | §7.3 | the **unreadable final glyph** |
> | §7.4 | **"1865 − 202…?"** |
>
> Four of the five do not survive a base rate, and the rule that removes them is
> now §10's:
>
> | entry | why it fails |
> |---|---|
> | the deleted *"a trusted"* | the artwork has five letter-level typos in ~250 words. One dropped word-pair is unremarkable at that rate, and the phrase surviving twice elsewhere is exactly what a single accidental omission looks like — not evidence against accident. |
> | the unreadable glyph | not the author's absence, ours. Russian needs 33 letters; the Gravity Falls key supplies 26; the author invented the rest and we lack the key. Filing it as withholding assumes an intent nothing supports. |
> | *"1865 − 202…?"* | reads naturally as an open-ended range — abolition to the present and counting. §9 criterion 4 forbids assigning a cryptographic function to punctuation that already has a plain meaning. |
> | the star and course deficits | two deviations across five resolved canonical-count checks is the ordinary yield of hand-drawing. They also **disagree**: 50 − 44 = 6 lands on an open slot, but 13 − 12 = 1 lands on `subject`, which is assigned, freed and eliminated. A real mechanism works twice. |
>
> **[MEASURED] One entry survives: the third clock hand.**
>
> It survives on the **placement** of the hands, not on the absence of a word —
> and that distinction is what makes it testable. A decorative clock needs no
> deliberate placement, because a clock showing a time has three hands determined
> by *one* parameter. So the null hypothesis is: the clock simply shows a time.
>
> It does not. All three hands sit at numeral midpoints (angles ≡ 15 mod 30°),
> and that is impossible on a real clock. With *t* in seconds past twelve:
>
> ```
> second : 6t    ≡ 15 (mod 30)  →  t ≡ 2.5  (mod 5)
> minute : t/10  ≡ 15 (mod 30)  →  t ≡ 150  (mod 300)
> hour   : t/120 ≡ 15 (mod 30)  →  t ≡ 1800 (mod 3600)
> ```
>
> Every *t* ≡ 1800 (mod 3600) is a multiple of 1800, and 1800 and 3600 are both
> ≡ 0 (mod 300) — so the hour condition forces *t* ≡ 0 (mod 300), which can never
> be 150. **Hour and minute are incompatible.** Sanity check: at 10:07:30 the hour
> hand sits at 303.75°, 11.25° from the observed 315°.
>
> Exactness is the weak claim, though, and it is not the one that matters.
> *Approximate* triples of midpoints are common — 7,344 of 4,320,000 samples
> across the 12-hour cycle fall within 1.5° on all three hands, the best being
> 1.186° at 9:27:37.69. **The question was never whether a clock can show three
> midpoints. It is whether it can show *these* three: 12&1, 1&2, 10&11.**
>
> Searching every time in the cycle at 0.01 s resolution, against all six
> hand-to-angle assignments:
>
> ```
> best achievable error : 10.465 deg   at 10:09:04.24
>    hour   304.535   wanted 315.0   (off 10.465)
>    minute  54.424   wanted  45.0   (off  9.424)
>    second  25.440   wanted  15.0   (off 10.440)
> ```
>
> 10.5°, against a measurement precision of ~1.5° — **seven times the fit
> tolerance**, and the canonical assignment is itself the best of the six. No time
> produces this configuration. The three angles are therefore three independent
> choices, not one.
>
> **The prior, since §10's rule applies here too.** Under a null of free
> placement, each hand lands within 1.5° of a midpoint with probability 3/30 = 10%
> — or 3/24 = 12.5% granting an illustrator who keeps hands off the numerals for
> legibility. Three hands: **0.195%, about 1 in 512.**
>
> That figure must then be corrected for look-elsewhere, because midpoints are not
> the only configuration an observer would have flagged: all three on numerals,
> all three coincident, two coincident, all three 120° apart, symmetric about an
> axis. Dividing across four such alternatives gives ~1 in 130, and four is
> conservative. **State it as order 10⁻², not 10⁻³.** That is still the strongest
> number in the section, and it no longer overstates.
>
> **[RETRACTED] The inference the pattern carried.** That the seed words come from
> outside the image and the artwork supplies only the ordering. With one entry
> left, it has no basis and is dropped rather than downgraded. It was the most
> defeatist claim in the document and the least supported — it told every reader
> the answer is not findable in the artwork, on the strength of four observations
> that turned out to be base rate.
>
> **The four retracted entries remain in place where they were made.** Each is a
> correct observation about the artwork; what is withdrawn is reading them as a
> system. §1.4's deleted phrase is still a real deletion and `trust`@21 was still
> tested on the strength of it. This subsection retracts the pattern, not the
> facts.
>
> **A note on how this error was found and on one it concealed.** The pattern was
> assembled in a working document, not here, and for four days it was discussed as
> though it were a section of this report — "§8" — by three parties, none of whom
> looked at what §8 actually contains. The first patch written from that belief
> replaced §8's real content with this retraction, keeping §8's heading, and an
> anchor-checked script applied it faithfully because the line numbers were right
> and the identity behind them was assumed. **A hash verifies which file; an anchor
> verifies what text you are editing; neither verifies that the section is the one
> you think it is.**

---

## §10 — Method: three additions

### The EC rewrite

Inserted after the two-kernel paragraph (line 723), before **Seam validation**.
It opens by dating the rate table above it, which is pre-rewrite.

> **The rate table above predates this rewrite.** Every figure in it was measured
> on the affine pipeline; the combined 125 k/s is now roughly 3× that. The table
> is retained as measured rather than re-scaled, because a scaled number is not a
> measured one — it will be replaced when the suite is re-run end to end.
>
> The pipeline is **~3× faster** since replacing affine double-and-add with
> **Jacobian coordinates**: ~384 modular inversions per scalar multiplication
> down to one, at the final conversion back to affine. **Measured 2.956×
> end-to-end** on a 4-path config (10.08 s → 3.41 s).
>
> **Every rate below is stated with the conditions that produced it**, because
> this project lost an evening to figures whose unit, path count and thermal state
> were unrecorded:
>
> | quantity | value | conditions |
> |---|---|---|
> | pipeline throughput | **135,074 derivations/s** | 22 production runs, sd 0.32%, 1 path |
> | 4-path / 1-path cost | **T4/T1 = 1.484** | `loo` (4-path) against `free` (1-path), both post-Jacobian |
> | shared / per-path split | P = 6.209 µs, X = 1.195 µs | per derivation, from the above |
> | `BIP32 + secp256k1` row | 925 k/s | **per derivation, single path** — not per scalar multiplication |
> | scalar-mult speedup | **5.50× production** | 6.5× is the isolated-kernel figure; production wins |
> | EC share, 4 paths | **43.5% [MEASURED]** post-Jacobian | from P and X directly |
> | EC share, 4 paths | ~81% **[INFERRED]** pre-Jacobian | from a contended A/B, assuming both arms were slowed equally |
> | hardware state | 1605 MHz SM — **51.7% of the card's 3105 MHz max** | 88 °C sustained, 59.7 W of 80 W, `SW Thermal Slowdown` active |
>
> The last row is the reproducibility item. **An unthrottled card should be roughly
> twice as fast**; without that line a reader benchmarking their own solver
> concludes ours is broken.
>
> The two EC-share figures describe **different binaries**, and pairing the
> post-Jacobian cost ratio with the pre-Jacobian share produces an Amdahl
> impossibility. That mistake was made and caught here; the labels exist to stop
> it recurring.
>
> All three scalar multiplications in the derivation are **fixed-base** — the
> hardened BIP32 steps need no public key, and the rest multiply the generator —
> so a comb table was considered and rejected: it adds ~2% against a 5.5× Amdahl
> ceiling that Jacobian alone reaches 87% of. Extra risk surface for nothing.
>
> Verified bit-identical to the affine routine over **122,880 random scalars plus
> k = 1, 2, 3 and n−1**, with the affine implementation retained as the oracle
> rather than replaced. The swap happened mid-sweep, at a chunk boundary; the
> survivor count of the completed run reconciled **exactly** across the two
> segments, proving the swap introduced no gap and no overlap.
>
> Two estimates were wrong in opposite directions and the decision survived both:
> a predicted 30× on the multiply (inversion priced at ~100 multiplies; Cyclone's
> `_ModInv` is divstep and far cheaper) and a recommendation to build the comb
> table first. The robustness table is the only reason — the case never depended
> on hitting the multiplier.

### Bugs 9 through 15

Append to the existing eight.

> 9. **The global checkpoint path.** `progress2.txt` was a fixed filename shared
>    by every invocation, so any second run — a benchmark, a selftest, a config
>    check — destroyed a multi-day sweep's resume point. A crash afterwards would
>    resume from the wrong index and skip candidates silently, voiding the
>    exhaustiveness the project rests on. Audited backward: no completed sweep was
>    affected. Its fix has since prevented two concrete losses.
> 10. **A `uint64_t[4]` passed to a 5-limb `_ModInv`.** Compiles, runs, returns
>    plausible garbage. The affine code never hits it because it routes through a
>    `fieldInv` wrapper. Caught by the differential oracle on first execution.
> 11. **`subtract()` in the ledger discarded already-emitted pieces** on its
>    disjoint-dimension early return, losing real volume. It never fired on the
>    declared runs because in every pair the disjoint dimension is the *first* one
>    where the runs differ, so the discarded list was always still empty. Fixing
>    it left the evidenced figure unchanged and moved the combined figure by
>    68,300,324 derivations.
> 12. **The ledger and the solver disagreed about what a config means.** The
>    solver refuses a pool or slot word that is not in the wordlist and exits 1,
>    in all three positions (`POOL`, a bare `SLOT`, a `SLOT` list) — verified by
>    injection. The ledger's parser filtered the same words with `if w in IDX`,
>    silently shrinking a declared pool. No run could have used such a config, so
>    nothing was miscounted, but the error direction was to **understate coverage
>    with no symptom** — the one direction that never announces itself. A ledger
>    that reads configs must fail on whatever the solver would refuse.
>
>    The first fix was scheme-blind: it checked the BIP39 map alone, so a
>    brainwallet config legally declaring `EXTRA stop freedom` would have made the
>    ledger abort on valid input — a hard stop traded for a silent undercount,
>    which is the worse of the two. It never fired only because the ledger walks an
>    explicit list of declared runs rather than a glob. Containment, not a fix.
>
>    The audit that cleared it was also too narrow: it covered 239 configs in two
>    directories. A correct enumeration of the home directory finds **767 `.conf`
>    files, 735 of them puzzle configs**. Re-run across all 735 — no pool or slot
>    word is neither BIP39 nor `EXTRA`, and all eight `EXTRA`-declaring configs are
>    `scheme=brainwallet`. The conclusion survived; the evidence for it had been a
>    third of what it should have been.
>
>    The *widened* audit was itself wrong first, in the same family. It reported
>    837 files and 667 puzzle configs, because it split `find` output on bare
>    whitespace rather than newlines — shredding every path containing a space into
>    fragments that failed to open and were swallowed by a bare `except: continue`.
>    That **inflated** the file count while **dropping 70 real configs**, all of
>    them under `~/Downloads/real (copy)/`. The discrepancy only surfaced because a
>    later run with a *narrower* content filter returned *more* configs, which is
>    impossible. Two audits of the same tree, and the one that agreed with
>    expectations went unchecked.
> 13. **The fix for bug 12 introduced a collision, by relying on the containment
>    it had just rejected.** Exempting `EXTRA` words meant giving them indices
>    above the wordlist, and the first version enumerated each config's *own* list:
>
>    ```
>    brain_find.conf      EXTRA stop freedom    ->  stop    = 2048
>    brain_selftest.conf  EXTRA battery staple  ->  battery = 2048
>    ```
>
>    `stop` and `battery` became the same element. The ledger's whole purpose is
>    computing unions by real set intersection **across** configs, so a union over
>    two `EXTRA`-declaring rows would have been arithmetic on words with nothing in
>    common. Demonstrated before fixing: two configs sharing no pool word produced
>    identical slot sets.
>
>    It could not fire while no brainwallet config was a declared row — which is
>    the same accidental containment rejected one bug earlier, reintroduced by the
>    fix that makes such rows possible. **A fix inherits the standard applied to
>    the bug.** Now one module-level registry: same word, same integer, every
>    config, matching the solver.
>
>    The related hazard was checked and does not apply — this script's index map is
>    0-based (`zoo` = 2047), so basing at 2048 cannot alias it. Had it followed the
>    report's 1-based convention, the first `EXTRA` word in every config would
>    silently have become `zoo`.
>
>    All three tests written for bug 12 parse a **single** config and so could not
>    see this. Two cross-config cases were added and mutation-tested.
> 14. **The log filter destroyed the record of work that did happen.** The queue
>    script piped solver stdout through `grep -vE "^ +[0-9]+\.[0-9]{2}%"` to keep
>    logs readable, which strips every per-chunk progress line. `t21_free4.log` is
>    108 bytes of header. When a question arose about how much a set of benchmarks
>    had cost a running sweep, the data that would have answered it retrospectively
>    — for free, exactly — had been discarded by design.
>
>    Not a solver defect. The same family as bug 9 and `show_hit`: **tooling that
>    loses the evidence rather than the work.** It cost nothing only because
>    checkpoint mtimes survived independently, which was luck. Replaced by an
>    external poller recording `(epoch, value)` on every checkpoint change — and
>    that poller's first output turned out to contain the whole campaign's run
>    durations, which is where the 21.910 h ± 0.32% figure came from.
> 15. **Two commits claimed work they did not contain.** Publishing this report
>    took four commits to land three changes. `d30d8d3` applied the additions but
>    substituted the wrong section (see §7.7). `9e7ef0d` and `d534547` each carried
>    a message describing the section-8 restoration and **one line of
>    `.gitignore`** — because they were staged with `git add -u <pathspec>`, which
>    git reads as *"update only that pathspec"* rather than *"update everything,
>    and also this"*. `1aad6fe` finally carried the content.
>
>    Same family as bug 9, bug 14 and `show_hit`: **the record said the work
>    happened and the artifact did not change.** Both bad commits reported
>    `1 file changed, 1 insertion(+)` and neither was read. The check that catches
>    it is three lines and confirms the artifact rather than the message:
>
>    ```
>    git show HEAD:REPORT.md | wc -l
>    git show HEAD:REPORT.md | grep -c '\[FIGURE\]'
>    git show --stat HEAD | tail -3
>    ```

### Five rules

§10 has no rules list to append to — this is a NEW subsection, inserted after the
closing "validate against exact expected counts" advice (line 793) and before the
`---` at 795. patch5.py adds the heading.

> - **A number that lands where you expected is the one to check twice.** **Five**
>   instances in a single day, each a figure that agreed with its author and so was
>   never re-run:
>
>   - `$?` after a pipeline or command substitution belongs to the last thing that
>     ran, not the thing under test. It twice reported success where there was
>     failure — a solver that had correctly refused a poisoned config, and a test
>     suite carrying two failures.
>   - An audit split `find` output on bare whitespace instead of newlines,
>     inflating the file count while silently dropping 70 configs. It surfaced only
>     because a later run with a *narrower* filter returned *more*.
>   - A test proposed to prove a run never happened — `grep -c 'chunks'` — counts
>     **lines**, and the progress writer emits `\r`. It returned 1, which would
>     have confirmed the hypothesis it was designed to test. The run had in fact
>     completed all 37 chunks. Counting records instead of lines reversed the
>     conclusion and moved the excluded tranche from 98.6 M to 138.7 M.
>   - Three consecutive progress reports of `~40%`, `~41%`, `~44%` on a run that
>     elapsed time placed at **70–72%**. They incremented smoothly, which is what a
>     number carried forward and nudged looks like, and the ETA riding on them was
>     six hours out. The next measured reading was 71.1%.
>
>   The common shape is not carelessness; it is that **nobody re-runs a check that
>   agrees with them.** A passing check is where a broken harness hides. Every
>   verdict in this project that arrived pre-agreed — the stemmed base rate, the
>   two agreeing tallies, the zero exit codes, the shredded audit — was wrong or
>   unfounded.

> - **A single source of truth kept in two places is a running sum by another
>   name.** The ledger existed as two copies — the published tree and the working
>   tree — and they silently diverged: a patch went into one only, so the other
>   kept an older parser. This is the same failure the maintained tally had, one
>   level up. Whatever computes a figure must exist once, and the copy that gets
>   run must be the copy that gets published.

> - **A pattern match against §8 needs a base rate before it counts.** The artwork
>   is full of numbered sequences, absences and near-misses. "This looks like the
>   author's signature" is a hypothesis with a prior, and the prior is usually high
>   enough to explain the observation on its own. Four of §8's five entries were
>   retired by asking, once, how often the artwork produces that shape by accident.
>   The one that survived did so because it had an independent measurement behind
>   it, not because it looked more like a signature.

> - **A reported elapsed time is a measurement, not a recollection.** **Seven** of
>   this project's wrong numbers have been timings or rates:
>
>   ```
>   a cold chunk reported as a sustained rate
>   a model quoted where a measurement was available
>   an elapsed time never taken
>   a fabricated progress reading (40.8%, invented, with a future timestamp)
>   three consecutive status lines ~30 points below what elapsed time allowed
>   an ETA carried forward for six hours without recomputation
>   microbenchmark staging figures (1.18x, q > 22.8%) quoted as measured
>   ```
>
>   Survivor counts are z-tested against an exact expectation on every run;
>   timings get quoted from memory. Same project, two standards — and it is the
>   unexamined one that keeps failing. **A figure passed between collaborators
>   carries the command that produced it, or it is not reported.** Stated as a
>   producer's duty it failed repeatedly; it holds only when the consumer refuses
>   to compute on a number that arrives as prose.
> - **Agreement between two methods validates only the paths both take — so when
>   two checks agree, compare the intermediate values, not just the verdicts.**
>   Two independent tally implementations agreed to the candidate while sitting on
>   a defect in a branch neither exercised. Separately, two reviewers independently
>   stemmed the same word list and both reached "fewer empty lines than chance";
>   the error surfaced only when the expected counts were placed side by side
>   (1.94 against 3.25). A failed control announces itself. A control that agrees
>   with you is invisible, and agreement on the conclusion is the weakest evidence
>   the two methods can produce.

---

## §9 — Acceptance criteria: one addition

> 7. **An observation needs its control before it is recorded, not after — and
>    the control needs checking too.** A finding that survives only a qualitative
>    caveat has not been tested. Worked example, in three stages, because the first
>    two were both wrong.
>
>    **Stage 1 — the finding.** The protest-slogan block has seven lines; line six
>    was reported as the only one containing no BIP39 word, and slot 6 is an open
>    gap. Striking, and recorded before any control was run.
>
>    **Stage 2 — the bad control.** Two reviewers independently computed the base
>    rate and both **stemmed** before matching (`LIVES`→`live`, `KILLING`→`kill`),
>    giving p ≈ 0.50 and an expectation of **1.94** wordless lines against one
>    observed. Fewer empties than chance: no evidence either way. Right verdict.
>
>    **Stage 3 — the control, checked.** BIP39 matching is exact. `lives` is not
>    `live`; `stop`, `kill`, `killing`, `not` and `us` are not in the wordlist at
>    all. Matching exactly, the block reads:
>
>    | # | colour | words | exact BIP39 hits | n |
>    |---|---|---|---|---|
>    | 1 | black | BLACK | `black`#184 | 1 |
>    | 2 | black | LIVES | — none — | 1 |
>    | 3 | black | MATTER | `matter`#1099 | 1 |
>    | 4 | blue | NO JUSTICE NO PEACE | `peace`#1295 | 4 |
>    | 5 | red | END POLICE BRUTALITY | `end`#589, `police`#1342 | 3 |
>    | 6 | green | STOP KILLING US | — none — | 3 |
>    | 7 | black | NOT ONE MORE | `one`#1238, `more`#1151 | 3 |
>
>    **Two wordless lines, not one** — and line 2 is one of them. The original
>    observation was not merely uncontrolled, it was miscounted.
>
>    **The base rate depends on which text you take as the corpus**, which is a
>    transcription judgement, so it is reported across five choices rather than one:
>
>    | corpus | words | BIP39 | p | E[wordless] | observed |
>    |---|---|---|---|---|---|
>    | headline only | 59 | 23 | 0.390 | 2.65 | 2 |
>    | headline + amendment | 92 | 32 | 0.348 | 2.97 | 2 |
>    | headline + amendment + whitepaper | 118 | 37 | 0.314 | 3.25 | 2 |
>    | slogan block alone | 16 | 7 | 0.438 | 2.32 | 2 |
>    | amendment + whitepaper only *(out-of-sample)* | 59 | 14 | 0.237 | 3.96 | 2 |
>
>    Expectation exceeds the observed 2 under **every** corpus, so the verdict does
>    not depend on the transcription. The first four rows include the slogan block
>    inside the corpus that scores it; that inflates p and so *lowers* E, biasing
>    the test **toward** declaring signal — and it still does not. The last row is
>    the clean out-of-sample estimate and is the least favourable of all.
>
>    Taking the seven lines as independent at p = 0.314, the exact distribution of
>    the wordless-line count is:
>
>    ```
>    0: 0.007   1: 0.062   2: 0.199   3: 0.317   4: 0.266   5: 0.119   6: 0.027   7: 0.002
>    P(exactly 2) = 0.199        P(<= 2) = 0.268
>    ```
>
>    **Three is the modal outcome and two is the second most likely.** The
>    observation is not merely "below expectation" — it is an ordinary draw, at
>    p = 0.27 one-sided. There is nothing here in either direction.
>
>    **What the example is for.** Two reviewers ran the same control independently
>    and both reached the right verdict from a wrong premise. It surfaced only when
>    the expected values were placed side by side — 1.94 against 3.25 — rather than
>    the conclusions. **A control that reaches the right answer from a bad premise
>    is still a control nobody checked.** Bending a written word to reach a wordlist
>    entry is precisely how `breathe`, `trusted`, `stop` and the other eleven
>    entered circulation, and both reviewers did it inside the section documenting
>    it. That costs nothing to do and nothing prompts you to check it, which is why
>    it is a better worked example than any of the thirteen bugs.
>
>    Reproduce with `slogan_lines.py` in the project root (needs `mnemonic` only).
