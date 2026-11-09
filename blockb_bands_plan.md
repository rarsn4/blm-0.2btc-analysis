# Pre-registration: block B in the bottom bands

Written and committed **before** any pixel in these four regions was counted. Every
number below is geometry taken from measurements already published in this tree; none
of it is a read of the regions under test.

## Why this test, and why it is stronger than the dial negative

`u/Amadeus407`, comments `gpzlri7` and `gpzromb` (2021-03-06), locate the three rune
blocks in his own words: *"runes from above"* (C), **"runes at the bottom"** (B),
*"Runes on the right"* (A). Block A's "on the right" checks out at x 1526–1557. The
existing block-B negative tested **our** guess — a disc around the dial. This one tests
**his**, which is why a negative here closes more than that one did.

## Two facts recorded before the test, because they bound what it can mean

1. **"At the bottom" does NOT exclude the dial region already searched.** The disc
   spans x 288–652, y 755–1119, which lies inside the bottom third of a 1200-tall
   image. The search region and the transcriber's wording were never in conflict. What
   the disc did not cover is area: 96,762 px of the bottom third's 640,000, **15.1%**,
   touching 320 of 400 rows but only 365 of 1600 columns.
2. **The bottom edge has no room beside the two catalogued elements.** The whitepaper
   caption (25, 1138, 1040, 28) and the Latin line (1025, 1140, 530, 50) span
   x 25–1555, leaving **25 px** at the left and **45 px** at the right, against
   **~279 px** needed for 14 glyphs at block A's measured 19.9 px pitch.

## The four regions, fixed here

| id | region | size |
|---|---|---|
| R1 | y 1100–1138, full width | 38 × 1600 |
| R2 | y 1190–1200, full width | 10 × 1600 |
| R3a | x 0–25, y 1138–1190 | 25 × 52 |
| R3b | x 1555–1600, y 1138–1190 | 45 × 52 |

R1 overlaps the dial disc over part of y 1100–1119; R1 is reported both inclusive and
exclusive of the disc.

## The prior, stated before measuring: LOW, and here is the arithmetic

Block A's glyphs are 13 × 20 px at a 19.9 px pitch (§7.4, `runelib.py`). Fourteen of
them need **279 px along the reading axis and at least 20 px across it**.

- **R2 is 10 px tall.** A 20 px glyph does not fit in any horizontal orientation, and
  vertically the region offers 10 px of width. **Geometrically excluded before
  measurement.**
- **R3a is 25 px wide, R3b is 45 px.** Horizontally that is at most 1 and 2 glyphs
  against 14. Vertically both offer 52 px of height, at most 2 glyphs at the pitch.
  **Geometrically excluded before measurement.**
- **R1 is 38 × 1600.** It is the only one of the four that can hold a horizontal
  14-glyph line: 38 px takes one row of 20 px glyphs with 18 px spare, and width is
  not the constraint.

**So one region of four is geometrically capable, and the prior is low accordingly.**
This is recorded now so that a negative cannot later be presented as more surprising
than it is.

## Method

Connected components of `G < cut` over a **threshold sweep**, cut ∈ {90, 110, 130, 150,
170, 190, 215} — not one cutoff. Glyph-sized means a component with bounding box width
6–33 px, height 10–40 px, and 40–600 ink pixels; block A's own glyphs are 13 × 20 px
with 96 ink pixels and sit in the middle of those ranges. **Control: the right-edge
column, x 1526–1557, y 40–1015**, run through the identical method at the identical
cuts, so each region's count profile is read against a region known to contain 42
glyphs.

No even-pitch run test. Last round's attempt established that such a test has a ceiling
of **11** on a grouped inscription, because block A is grouped 1, 5, 4, 6, 2, 8, 11, 5
and the pitch breaks at every three-dot separator. The instrument here is component
**count and sweep profile** against the control.

## Decision rule, fixed before running

- **POSITIVE**: some region yields **≥ 14** glyph-sized components at **two or more
  consecutive cuts**, with a count profile that does not collapse across the sweep —
  the same stability discriminator that disproved the left-edge column (§10, sixth
  rule).
- **NEGATIVE**: anything else, including counts that appear at a single cut and vanish
  at its neighbours.

## What each outcome means, fixed before running

- **A negative closes the transcriber's own location wording for block B.** It is
  stronger than the dial negative because it tests his words rather than our guess.
  Combined with the two bounding facts above — the dial disc already lies in the bottom
  third, and the bottom edge has 25 and 45 px against 279 needed — it leaves "at the
  bottom" with no region that both fits and is unexamined. Block B would remain
  **unlocated**, and §2.17's three scope-marked slots would stay scope-marked.
- **A negative does NOT retract the decode.** It bears on where the block is, not on
  what it says, exactly as the existing scope note states.
- **A positive would locate block B**, and would convert the slots resting on its
  caption from [SCOPE] to measured. It would also need its own re-measurement of the
  decode before anything downstream moved.
