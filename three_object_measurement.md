# Three measurements: Liberty's nose, numerals on the Space Needle, the bust's neck band

Measured 1 Nov 2026 on the master image, sha256 `d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782`.
Pixels only, no GPU. Report only — no configs built.

## 1. The Statue of Liberty's face: the nose is NOT exaggerated

Feature positions, read from a row profile of the face interior (ink < 165) and from the lit-face mask
(pale cyan: B>170, G>170, R<G−5), master coordinates:

| feature | measurement |
|---|---|
| eye line (dark eye marks, y 611–618) | y ≈ **614.5** |
| left eye, horizontal extent | x 168–176, **≈ 8 px wide** |
| nose, vertical stroke | x 177–178, y 616–624 |
| nose base / nostril flare | y 625–627, x 177–186, **10 px wide** |
| mouth | y 631–637 |
| chin (lit face ends; width collapses 34 → 12 px at y 641) | y ≈ **641** |
| face width at the cheekbones (y 620–626) | x 154–192, **≈ 37.5 px** |
| face width at eye level (right side in shadow) | x 155–184, ≈ 30 px |

Derived: **eye-line to chin = 26.5 px**, **nose length (eye line to base) = 12.5 px**, nose width 10 px.

**Against the real statue's published dimensions** (nose 4 ft 6 in; face width 10 ft; eye width 2 ft 6 in; head
chin-to-cranium 17 ft 3 in):

| ratio | drawn | real statue | difference |
|---|---|---|---|
| nose length / face width | 12.5/37.5 = **0.333** | 4.5/10 = **0.450** | drawn 26% smaller |
| eye width / face width | 8/37.5 = **0.213** | 2.5/10 = **0.250** | drawn 15% smaller |
| nose length / eye width | 12.5/8 = **1.56** | 4.5/2.5 = **1.80** | drawn 13% smaller |
| nose length / eye-line to chin | 12.5/26.5 = **0.472** | not published | — |

**Verdict: within normal variation; no deliberate exaggeration.** The drawn nose is *smaller* than the real
proportion, not larger — the wrong direction for a feature being flagged. More decisively, **the eye is
undersized by a similar factor in the same direction** (15% against the nose's 26%), so the nose is not singled
out: the whole face is drawn slightly tight relative to its width. Nose length / eye-line-to-chin at 0.472 is an
ordinary value for any face, stylised or not.

**Precision limit, stated plainly.** The entire face is 37.5 px wide and the nose is 12.5 px long, so ±1 px at
each endpoint is ±8% on the nose and about ±0.03 on the ratios. The nose/face-width gap (0.12) is larger than
that, but it is not nose-specific, which is what the question turns on. At this resolution a claim that one
feature was deliberately altered would need a far larger and more isolated deviation than anything measured here.

## 2. The Space Needle: `FOOD` is there, and there is no numeral

**First, a correction to the premise.** The task said "you already found FOOD in the inner column". **There is no
such finding anywhere in this tree** — `grep -rn -i 'inner column'` returns nothing, and `food` enters the record
in §2.17's provenance table as a **Reddit community hint** (u/meserit, 2021-01-31), which the report explicitly
calls "a community hint rather than an assignment". So there was no prior method to repeat, and I defined my own.

**The text is nevertheless real.** In the Needle's inner column, master **x 1188–1212, y 645–690**, there is faint
lettering running **bottom-to-top** (legible when rotated clockwise). Contrast-stretched to the 2nd–98th
percentile of a 24×45 px window, it reads **`FOOD`** — four letters. It is far fainter than the architecture: the
glyph ink sits within the column's own grey range, which is why it is invisible at normal contrast.

**No numeral anywhere on the tower.** Scanning the whole Needle box (x 1060–1340, y 410–900) for compact dark
marks (ink < 140, ≥ 6 px, bounding box ≤ 60 px) returns 49 components. Every one is either part of the
architecture — the ribs, the spire, the saucer's tick-marks, the elevator track's dashed line — or lies outside
the tower on the box edge (the dark blue `N` and green `S` of the surrounding lettering at y = 410). **No digit
is drawn in or on the Space Needle.** The only writing on the tower is the word `FOOD`.

## 3. The bust's neck band: `BREATHE` only

The band is at master **x ≈ 1355–1430, y ≈ 528–545**, a red sash across the throat of the hooded bust, below the
two red X marks over the eyes and above the painted blood.

Contrast-stretched at ×14, it reads **`BREATHE`** in spaced capitals and nothing else. **No numeral, no other
mark.** The marks at either end of the band are the physical knot and its trailing ends, not glyphs: the left end
is the folded hood edge, the right end a tied knot with two tails. The dark vertical streaks below the band are
the drawn blood, not writing.

## What this does and does not change

Nothing here opens a slot or supplies a word.

- `nose` is BIP39, and an altered nose would have been a reason to try it. **The measurement gives no such
  reason**: the nose is slightly *under*-sized and the eye is under-sized with it.
- `food` is BIP39 and already in the 54-word gap pool, so it is covered by every run that sweeps the gaps; what
  is new here is only that the word is **physically written in the artwork**, which the record did not say. That
  is a provenance fact, not a position: nothing places `food` at a slot.
- `BREATHE` is not BIP39 (REPORT §2.6), and the band carries no number, so it supplies neither a word nor a slot.

## Addendum, 1 Nov: are the spire and the neck band drawn digits `1` and `2`?

Asked whether the Needle's spire is a written `1` and the bust's neck band a written `2`. Tested against the
artist's OWN digits, taken from `1865` beside the statue, with the harness used for glyph X (ink bbox -> 32x32,
z-scored, Pearson).

Calibration, different digits by the same hand: 8/6 +0.484, 1/6 +0.378, 1/8 +0.362, 6/5 +0.200, 1/5 +0.058.

| shape | vs `1` | vs `8` | vs `6` | vs `5` |
|---|---|---|---|---|
| Needle spire (x1181-1194, y365-425) | **+0.071** | +0.298 | +0.208 | +0.287 |
| neck band (x1360-1425, y528-546) | **-0.009** | -0.021 | -0.078 | +0.167 |

**Neither is a digit.** The spire's WORST match of the four is `1` itself: it resembles `8` and `5` more than the
digit it is supposed to be, and +0.071 sits at the floor for different digits (1 vs 5 = +0.058). The band scores
about zero against everything and is not a glyph at all. Structurally the artist's `1` carries a flag at the
top-left and a thick tapering body; the spire is a bare thin line with neither.

The spire is the tower's antenna, continuous with the structure below it, and the band is the `BREATHE` sash.
Recorded because a shape resembling a digit is not a digit, and this project has retracted one such reading
before on base-rate grounds while `.VS.` -> `·12·` survived on measurement.
