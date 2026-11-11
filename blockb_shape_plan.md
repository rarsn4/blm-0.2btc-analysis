# Pre-registration: the block-B shape-matched filter

Written and committed **before** the filter was built or run on any region. Design required
by RR-3, 11 Nov 2026; the measurement it follows up is §1.14 and the contrast sweep whose
count criterion came back **void at every depth**.

## 0. Word consequences, fixed first

**No word enters any config from this, under any outcome.** A located block is a location;
the words would come from a decode that has not been made. A positive would license one
thing only: a fresh pre-registration for reading the glyphs found.

## 1. Why a shape filter, and what killed the last instrument

`blockb_contrast.py` had **full power** at every depth from 10 to 39 levels and its criterion
was **void at every one**, because four 38 × 1600 null strips of this painting yield **39–60**
glyph-sized components. Component *count* cannot work in a band this artwork fills with its
own marks. §10's rule says the way out is a different instrument, not a lower threshold, and
the even-pitch test is already dead at a ceiling of 11 on a grouped inscription. **What is
left is matching the shapes of block A's own 42 glyphs.**

## 2. Block A's 42 glyphs cannot be both template set and control

A filter scored on the glyphs it was built from recovers them by construction — §1.12(b)'s
circularity in a new costume. So the 42 are **split**, and the split is fixed here.

**The touching-pair problem RR-3 anticipated no longer exists.** It was fixed on 9 Nov: with
`y1=1020`, `runelib.groups()` returns **42 glyphs in 8 groups of 1, 5, 4, 6, 2, 8, 11, 5**,
exact against all eight words, and `cells()` asserts it. So the split is by letter **and** by
instance with nothing excluded, which is better than the fallback RR-3 allowed for.

**Measured inventory, before the split:** 42 instances, **22 distinct letters**.
Ten letters repeat — `н`×6, and `р` `е` `о` `ы` `а` `и` ×3 each, `ь` `д` `з` ×2 each — for
**30 instances**; the remaining **12 letters appear once**.

### The split, fixed now

- **For each repeated letter**, instances are dealt alternately top-of-column first:
  `ceil(n/2)` to **TEMPLATE**, the rest to **TEST**. So every repeated letter is present on
  both sides.
- **All 12 singletons go to TEST.** They cannot be split, and putting them in the template
  would waste them; in the test half they are the stratum that matters.
- **Recovery is reported in two strata, never pooled:**
  - **seen** — a test glyph whose letter also has a template instance. The filter has that
    shape and should recover it.
  - **unseen** — a test glyph whose letter the template has never held. The filter must
    generalise from other letters. **A low rate here is expected and is not a failure of
    the filter; it is the measurement of how much of block B's alphabet a 21-template
    filter could ever see.**
  - One pooled rate would hide which of the two it is, which is the whole reason for the
    stratification.

## 3. The filter

- Each glyph is normalised exactly as `runelib.mask()` does: threshold `< 130`, crop to ink,
  centre in **34 × 34**. Native pixels only; nothing is resampled.
- Score = `runelib.iou()`, best intersection-over-union over a **±3 px** shift in both axes.
  Established in this tree, so the channel is not new.
- A candidate scores against **every** template and takes its **best** match.
- **Threshold ladder, fixed here: IoU ≥ 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60.** Reported
  as a curve, never as one cutoff, because the decision below is about *relative* rates.
- **No rotation or reflection.** `d8()` exists in `runelib` and is deliberately not used: a
  block of text has one orientation, and allowing eight would multiply the false-positive
  rate for a freedom the hypothesis does not need.

## 4. Candidate regions, and the controls

- **R1** — y 1100–1138, full width, the one band geometry permits (§2.17). Also `R1'`,
  minus the dial disc.
- **The four null strips declared in `blockb_contrast_plan.md` §5**, unchanged:
  y 160–198, 420–458, 600–638, 980–1018.
- Candidates in any region are connected components of `G < 130` — the same threshold the
  templates use — sized `6 ≤ w ≤ 40`, `6 ≤ h ≤ 40`, ink 20–600 px, which brackets block A's
  own glyphs (13 × 20, ~96 ink).

## 5. Which side of §10's asymmetry the control is expected to land on

**Pre-registered expectation: the nulls will OVER-fire, and this test will probably be VOID
in the blocking sense.** Stated plainly because §10 now requires it.

The reasoning, before the numbers: IoU at 34 × 34 on marks of 6–40 px is a weak
discriminator — small blobs resemble small blobs — and the null strips already supply 39–60
glyph-sized components each. So the likely outcome is that the nulls reach whatever bar R1
reaches, which is **§1.14's blocking case, not the X-marks case.**

**That makes the test worth running anyway, and here is the condition that would make it
informative:** the filter is a *stricter* criterion than size, so if it drives the null
counts **down** far enough that R1's count can be distinguished from them, the gap the
contrast sweep could not close becomes closeable. The measurement is therefore **the null
rate itself**, and it is reported whether or not R1 shows anything.

## 6. Decision rule, fixed before the numbers

- **NO POWER** — the test half is not recovered in the **seen** stratum at a given
  threshold. No absence may be claimed at that threshold.
- **VOID** — the maximum null-strip match count at a threshold is **≥ 14**, the glyph count
  block B is said to carry. Neither presence nor absence may be claimed there.
- **POSITIVE** — R1 or `R1'` yields **≥ 14** matches at **two or more consecutive non-void
  thresholds**, exceeding the **maximum** null count at each, with the seen stratum
  recovered at those thresholds.
- **NEGATIVE** — seen stratum recovered, nulls below 14, R1 below 14. This would close the
  gap left open by the contrast sweep.

Published either way, including every void and no-power cell, and including the null curve
on its own merits.
