# The yellow polyline, measured as a structure

Measured 3 Nov 2026 on the master image, sha256
`d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782` (1600 × 1200).
Pixels only, no GPU. Report only — no configs built. Script: `yellow_polyline.py`.

The device had only ever been described as surveillance imagery. This pass measures it
as a drawn structure: where it goes, what it meets, and whether its geometry carries a
number.

**Detector and its control.** Yellowness `Y = min(R,G) − B`. Paper sits at **Y 0–1**;
the device's ink at **Y 20–142**. There is nothing between 1 and 20, so the threshold
is not a judgement call. Every figure below is read at native resolution; the magnified
renders were used only to decide where to point a measurement, per §9's rule.

**Closure: this is all of it.** At Y ≥ 20 the device resolves into **16 8-connected
components totalling 6,831 px** (a component is not the same thing as a part — a
bracket and the run leaving it are one component). Every other Y ≥ 20 component in the
image is brown, not yellow: skin and hair at median RGB (189,158,120) and stone at
(75,59,35), against the device's (212–233, 207–227, 76–147). Sweeping the whole artwork
for the device's own hue (R > 180, R−B > 60, G−B > 50, |R−G| < 30) finds **42 further
pixels**, all inside x 912–998, y 883–929 — highlights in Trump's hair. **Nothing else
in the artwork is drawn in this yellow,** so the path below is complete: there is no
branch somewhere else that I failed to follow.

## 1. The full path

Eleven elements, left to right. **There is no arrowhead at either end** — perpendicular
stroke width is 3.0–3.6 px and uniform, and neither terminus widens — so the device
states no direction. "Left to right" below is my reading order, not a measured arrow.

| # | element | master coords | the line's relation to it |
|---|---|---|---|
| 1 | **face box A** — man with glasses | x 116–185, y 55–136 (69 × 81) | **terminates.** Three of its four brackets carry nothing; the line leaves the **bottom-right** arm at (184, 123.6). This is the device's only attachment on a bottom corner, and nothing exists left of x = 116. |
| 2 | ruled run 1 | (185, 123.6) → (252, 145.1) | 70.4 px, bearing **+17.79°** |
| 3 | **face box B** — woman | x 252–309, y 139–200 (57 × 61) | **stops and restarts.** Arrives at the top-left arm (y 145.1), nothing crosses the box, departs the top-right arm (y 146.0) |
| 4 | ruled run 2 | (309, 146.0) → (381, 106.6) | 82.0 px, bearing **−28.65°** |
| 5 | **face box C** — man, centre | x 381–445, y 92–174 (64 × 82) | stops and restarts (y 106.6 in, y 104.1 out) |
| 6 | ruled run 3 | (445, 104.1) → (473, 107.9) | 28.2 px, bearing **+7.60°** |
| 7 | **face box D** — man, right | x 473–522, y 100–165 (49 × 65) | stops and restarts (y 107.9 in, y 109.3 out) |
| 8 | leader L1 | (522, 109.3) → (674, 105.3) | 152.1 px, bearing **−1.49°** |
| 9 | **`Order and stability`** (cursive) | x 674–994, y 70–120 | **passes through.** The stroke is continuous at the writing baseline; see §3 |
| 10 | leader L2 | (994, 97.4) → (1320, 91.6) | 326.1 px, bearing **−1.02°** |
| 11 | **camera lens** | lens element x 1311–1328, y 77–100 | **terminates on it**, 3.3 px from the element's centroid (1319.4, 88.2). Nothing beyond x = 1320 |

Ruled length 658.8 px; the cursive spans 320 px between L1 and L2; end to end
x 185 → 1320 = 1,135 px.

**Pass through, or stop at — the answer is not the same for all three kinds of element,
and that is the finding.** The line *stops at* every box (28–41 px of each box edge is
empty, and **zero** yellow pixels lie inside any box outside its own brackets). It
*passes through* the cursive. It *terminates on* the camera, and the camera is the one
object it is drawn in front of.

**Turns.** −46.43° at box B, +36.25° at box C, −9.09° at box D, +0.46° at the end of the
word. All four direction changes are at an element; **no run bends between elements.**

**Every run is ruled, not freehand.** Least-squares residuals: rms **0.022, 0.042,
0.037, 0.105, 0.093 px**, max |r| ≤ 0.23 px. A 320-px freehand stroke does not hold
0.1 px. The cursive, by contrast, is plainly hand-written. Two different drawing acts
in one device.

**The boxes are corner brackets only.** Sixteen L-brackets, four per box, all four edges
open. The line always attaches at **mid-arm**, never at a corner vertex: 46%, 51%, 58%,
66%, 51%, 53%, 62% down the respective vertical arm (mean 55%). That consistency is a
drafting convention and is further evidence the whole thing is one deliberate device.

**All four faces in the crowd are boxed.** There is no unboxed face and no empty box.

## 2. What else it touches

| neighbouring element | minimum clearance | verdict |
|---|---|---|
| camera body and lens | **0.0 px** (overlaps, x 1296–1320) | **touched**, and the only one |
| slogan block (`END POLICE BRUTALITY` / `STOP KILLING US`) | **1.0 px** at (1247, 95) | threads between two letters; does not touch |
| rune line 3 | 6.4 px | clear |
| rune line 2 | 9.8 px | clear |
| rune line 1 | 37.0 px | clear |

Against the grey pencil drawing (ink < 150, desaturated), dilating the device by one
pixel finds **144 contacting pixels in total**, of which **46 are the camera**. Every
other contact is ≤ 11 px — a bracket arm abutting a head outline, which is what a box
drawn around a head does. **The device touches nothing in the artwork except the
camera.**

Two near-misses are worth recording because they are not accidents of scale:

- At x 1220–1259 the slogan's rotated capitals rise to y 85, **above** the line at
  y 92–95, and the line still clears them by 1 px. It threads the gap between two of
  that word's rotated letters rather than crossing either.
- The cursive is written across the first line of the `FIND THE SEED PHRASE…` watermark
  (watermark ink 43 levels below paper, bbox x 640–1000, y 36–140, the same window as
  the script). The watermark is a separate layer and is not touched; it is passed over.

**No branch, no stray vertex.** Seven T-junctions where a run meets a bracket arm, one
free terminus at the lens, and the pixel budget closes exactly. Nowhere does the line
split.

## 3. The underline under `Order and stability` — §9 does **not** need correcting

Three measurements settle it, and they point the same way.

**(a) There is no break between the leaders and the word.** Of the 825 columns from
x 505 to x 1329, the only ones with no device ink are x 505–511 and x 1321–1329 — that
is, everything from box D's bracket to the lens is continuous ink. The stroke does not
start and stop at the word.

**(b) The stroke is at the baseline, not below it, and the letters ride it.** Over
x 655–1034 (380 columns, the word plus a margin at each end), **244 are a single run** — the letter and the "underline" are
one stroke with no paper between them. §9's own discriminator names this exact case as
the known false positive: *"a flat baseline where rounded letter bottoms touch … is
distinguished by the absence of a lighter row between line and letters."* Here the
lighter row is absent for two columns in three. At 11× the capital `O`'s exit stroke is
visibly the horizontal line, and the final `y` of `stability` hands the stroke off to
L2 at y 96–99.

**(c) The two leaders are not one line passing behind the text.** L1 and L2 are each
dead straight (rms 0.105 and 0.093 px) but they are **not collinear**: L1 extended to
x = 1320 misses L2 by **3.04 px**, L2 extended back to x = 523 misses L1 by **3.41 px**,
and the bearings differ by 0.46°. A single ruled line passing behind a word would not
change slope at the word.

So it is **one continuous stroke: leader → handwriting → leader.** It is not an
underline, and it is not a rule with words sitting on it.

**And §9's claim is correctly scoped anyway.** §9 measures *"One underline in 25
checkable words"* over *"the hand-copied 13th Amendment … censused across 34 tokens."*
`Order and stability` is not in that census universe — it is the top-band caption. The
claim at REPORT line 1459, "carries the census's one underline (§9)", is sound as
worded. **No retraction is required.** One wording note for a future reader: "the
census's one underline" reads as project-wide if §9 is not open beside it.

**A label error, not a measurement error, found on the way.** `word_census.py:62` and
`census_crops.py:92` both call this element the **"statue base caption"**. Its recorded
box, (640, 70, 380, 50), is right and matches my x 674–994, y 70–120 — but the Statue of
Liberty's head is at x 154–192, y 611–641 (`three_object_measurement` §1) and its
pedestal lower still. The caption is in the top band, some 500 px above the statue's
face and on the far side of the picture, and it is the terminal of this polyline. The coordinates are correct and
the transcription is correct (`letterform_audit` §4 re-verified it); only the name is
wrong, and the name is what hid its structural role.

## 4. Does the path yield a number?

**Nothing in the device is a drawn numeral.** Zero yellow ink lies inside any box
outside its brackets. A compact-dark-mark scan of the four interiors (ink < 140,
component 6–400 px, bounding box ≤ 30 px — the detector used on the Space Needle in
`three_object_measurement` §2) returns **58 marks**; 45 are part of the face line-work
by connectivity at ink < 175, and the remaining **13 sit at eyes, eyebrows, glasses
rims and mask folds**, checked one by one against the drawing at 9×. **No digit, and no
isolated mark on clear ground, inside any box.**

What the structure does yield is counts, and here they are, with the tests that fail:

| count | value |
|---|---|
| face boxes | **4** |
| corner brackets | **16** |
| ruled straight runs | **5** |
| direction changes | **4** |
| elements on the path | **6** (4 boxes, the caption, the camera) |

- **Turn angles are not round.** −46.43°, +36.25°, −9.09°, +0.46°.
- **Box centres are not evenly spaced.** x-spacings 130.0, 132.5, 84.5 px.
- **Box sizes are not in integer ratios.** Widths 69, 57, 64, 49 (ratios 1.408, 1.163,
  1.306, 1.000); heights 81, 61, 82, 65. They track apparent head size in perspective —
  A is the nearest figure and the largest box, D the furthest and the smallest.
- **Run lengths are not in integer ratios.** 70.4, 82.0, 28.2, 152.1, 326.1 px
  (2.491, 2.904, 1.000, 5.383, 11.542 against the shortest).
- **Extending the path yields nothing.** Run 1 extended left lands inside box A; L2 stops
  at the lens and nothing lies beyond.

**So: no number is encoded by the geometry.** The only numbers available are the counts
above, and a count is only a candidate if something outside the device says which count
to take — the device itself does not single one out. `4` is the count a reader reaches
for, and I record that it is a *choice among five counts*, not a reading.

## 5. What this does and does not change

Nothing here opens a slot or supplies a word, and no config follows from it.

- **The caption's words were already covered.** `order` is in the current 54-word gap
  pool (`t21_single.conf`) and is **BIP39 #1250**, so every run that sweeps the gaps
  already carries it. `stability` is nine letters; the list's longest word is eight, so
  it is not BIP39 and cannot be one. The image-text brainwallet corpus already
  holds `Order and stability` as drawn (`letterform_audit` §4, re-run 2 Nov). This pass
  adds no string.
- **The structural claim is new and it is negative.** The device is one drafted object —
  five ruled runs to 0.1 px, sixteen matched brackets, uniform mid-arm attachment — and
  it carries no numeral, no arrow and no extractable number. Measured as a mechanism, it
  does not behave like one.
- **What it does establish** is the three-way asymmetry in §1: it *stops at* every face,
  *passes through* the caption, and *terminates on* the camera lens, 3.3 px from its
  centre. That is a statement about the picture's meaning, and this project's record on
  meaning-derived candidates is the reason the pass was asked for in the first place. It
  is recorded as structure, not as a source.
- `Order and stability` keeps its [MEASURED] status as text. Its element label is wrong
  in two scripts; the fix is a rename, not a retraction, and it is not made here because
  this pass is report-only.

## 6. Scope and limits

- Everything above is native-pixel. The 4×–11× renders in the scratchpad were used to
  aim measurements, never to read a value.
- The 3.3 px between the line's terminus and the lens centroid is **not** evidence of
  deliberate aim on its own: the lens element is 18 × 24 px, so a stroke ending anywhere
  in its middle third would score similarly. What is measured is that the line ends
  *inside* the lens and nowhere else.
- Box edges are quoted as the outer extent of the corner brackets at Y ≥ 20; ±1 px.
- The reading order (A → camera) is a convention. The device has no arrowhead.
