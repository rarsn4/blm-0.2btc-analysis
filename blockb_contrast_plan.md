# Pre-registration: block B below the detection floor

Written and committed **before** any pixel of the regions under test was read by the new
detector. Brief MM-2, 10 Nov 2026. This test exists because the previous one measured its
own blindness and published it.

## 1. The gap this closes, quoted from our own output

`blockb_bands_sensitivity.out`, Z-1, attenuated copies of block A's **own** column — 42
glyphs present in every row, ink depth the only thing changed:

| contrast of the copy | verdict under the old sweep |
|---|---|
| as drawn, 254 levels | SEEN |
| circled mark, 146 levels | SEEN |
| vial-19 level, 110 levels | SEEN |
| 45 levels | SEEN |
| 35 levels | **BLIND** |
| rifle-16 level, **19 levels** | **BLIND** |

**The floor has an exact and mechanical cause**: the sweep's deepest cut is `G < 215`
against a 254 background, so it can only see ink reaching `254 − 215 = 39` levels. The
rifle-receiver mark in this same image is measured at **19 levels** (§6 item 6), so a
block drawn below the floor is not hypothetical — it is drawn at a depth this image
demonstrably uses.

**So the previous negative is sound for ink deeper than 39 levels and says nothing
below it.** That is the whole of what is being reopened.

## 2. Scope: R1 only, and why the other three stay closed

`blockb_bands_plan.md` excluded R2 (10 px tall), R3a (25 px wide) and R3b (45 px) **by
geometry** — 14 glyphs need 279 px along the reading axis and ≥20 px across it. A
geometric exclusion does not depend on how deep the ink is, so **those three remain
closed and are not retested.** Only **R1** (y 1100–1138, full width) was ever excluded by
*detection*, so only R1 is reopened, with `R1'` (minus the dial disc) reported separately
as before.

**Secondary, and labelled secondary throughout:** the **whole bottom third**
(y 800–1200, full width). The bands plan records that the dial disc covers only
**15.1%** of it. A 400 × 1600 region will carry far more components than R1 and its
criterion may well be void (see §5); it is included because the contrast gap applies to
every region any absolute-threshold detector has ever searched, including the disc, and
excluding it would understate what the old floor left unmeasured.

## 3. The detector, and why the cuts have to go

An absolute cut cannot work at 19 levels: a global `G < 235` would flood any region whose
local background is darker than 235. **The cut is therefore replaced by depth below a
locally estimated background.**

- Local background `B` = median filter of `G`, window **41 px** — wider than a glyph
  (13 × 20) in both axes, so a glyph cannot contaminate its own background estimate.
- Depth map `D = B − G`, in grey levels.
- Detection mask at depth `d`: `D >= d`.
- **Depth ladder, fixed here: `d ∈ {10, 15, 19, 25, 30, 39}`.** Chosen by principle, not
  from the data: **19** is the rifle mark's measured depth, the thing that must be
  visible; **39** is the old floor, so the new detector can be checked against the old
  result; 25 and 30 bracket between them; 10 and 15 go deliberately *below* the target to
  find where the detector loses specificity rather than assuming it does not.
- **Glyph-sized** keeps the previous definition exactly, for comparability: bounding box
  width 6–33 px, height 10–40 px, ink 40–600 px. Block A's glyphs are 13 × 20 with 96 ink.

## 4. Power control, fixed before running

Block A's column (x 1526–1557, y 40–1015), 42 known glyphs, **attenuated to each depth**
in the ladder and run through the identical detector. **A depth at which the attenuated
control does not recover ≥14 glyph-sized components is a depth at which this test has NO
POWER, and no absence may be claimed there** — the rule that governed the llama sweep's
no-power result, applied in advance rather than after.

## 5. Specificity controls, which are the real risk here

Lowering a detector to 19 levels is exactly how a false positive arrives. The zodiac
sweep's ice-bag criterion passed 1,466 of 2,167 components and measured nothing; that
must not happen again unnoticed, so the nulls are fixed here:

**Four null strips, each 38 × 1600, the same shape as R1, declared now and chosen away
from every catalogued inscription:** y 160–198, y 420–458, y 600–638, y 980–1018.

At each depth the null strips give a false-positive count. Then:

- A depth where **any null strip reaches ≥14** glyph-sized components is **VOID**: the
  criterion no longer discriminates, and **neither presence nor absence may be claimed at
  that depth.** Reported as void, not as a negative.
- A depth where the nulls stay below 14 is a depth where the criterion means something.

## 6. Decision rule, fixed before the numbers

- **POSITIVE** — R1 (or R1') yields **≥14** glyph-sized components at **two or more
  consecutive non-void depths**, **and** its count exceeds the **maximum** null-strip
  count at each of those depths, **and** the profile does not collapse across the ladder.
- **NEGATIVE** — the power control recovers at a depth, the nulls are below 14 there, and
  R1 is below 14. This is a real absence and it closes the contrast gap.
- **VOID** — the nulls reach 14, per §5.
- **NO POWER** — the attenuated control fails to recover, per §4.

Reported either way, including every void and no-power cell. A ladder that returns void
at 10 and 15 and negative at 19, 25, 30 and 39 would be a **success**: it would close the
gap down to the rifle's own depth.

## 7. What each outcome means, and what it does not license

- **A negative at 19 levels closes the live gap.** Combined with the geometric exclusions
  of §2, "at the bottom" would then have no region that both fits and is unexamined at
  any depth this image is known to use. Block B stays **unlocated** and §2.17's three
  slots stay `[SCOPE]`.
- **A negative does not retract the decode**, exactly as the existing scope note says. It
  bears on where the block is, not what it says.
- **A positive locates block B and nothing more.** It would **not** convert §2.17's slots:
  the caption's decode would need its own fresh measurement first, and the glyphs found
  would have to be read before any word followed from them.
- **NO WORD ENTERS ANY CONFIG FROM THIS TEST, under any outcome.** A located block is a
  location; the words would come from a decode that has not been made.
