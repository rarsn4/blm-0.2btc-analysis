# STOP — R10 set C is closed

Written 2026-09-29, before anyone has asked to reopen it.

## The rule

No further analysis of **R10 set C** (the face-level elements) may be used as evidence that the artwork is laid out on the clock dial. The same applies to **any other R10 element set**.

**The R10 data cannot be reused.** Any future dial-layout test, face-level or otherwise, needs a **fresh pre-registration** with all of these:

1. A **new element list**, defined by a written rule before any angle is computed. It must be independent of R10: ideally drawn up by someone who has not seen R10's per-element angles.
2. A **new hash** of that list, recorded before scoring.
3. The **decision rule written into the file** before scoring: the sets, the tolerances, the nulls, the alpha, and the correction for multiple comparisons.

## Why

**Two justified corrections have already moved set C in the same direction:**

1. **The E24 box fix** (`r10_erratum.md`) was necessary: the pre-registered face box could not contain the left X mark that `slot20.py` places independently. It moved set C at 0.5° from **p 0.13 / 0.11 to 0.069 / 0.032**.
2. **Re-centring the pyramid eye on its iris** was offered in the R10 write-up with the words "would likely flip that hit". It is the same move a second time.

Each correction is defensible on its own. Together they are how an honest pipeline arrives at a false positive, and the only thing that stops it is a rule written down before anyone wants to break it.

## Not allowed

- Any further box correction to sets derived from `r10_elements.json`.
- Re-centring the pyramid eye, or any other element, after seeing R10's numbers.
- Any tolerance, subset, null or statistic chosen after seeing R10's numbers.

## What stands

- R10's pre-registered primary verdict: **NOT SIGNIFICANT** (set A, `r10_layout.py`).
- The erratum, recorded as a post-hoc note that does not change the primary result.
