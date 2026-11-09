# Does eye@9 and pyramid@11 come from the pyramid's levels, or from which clock numerals the pyramid covers?

Measured 31 Oct 2026 on the master image, sha256 `d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782`.
Pixels only. Clock centre `(470, 937)` is the pre-existing constant from `even_slot_rules.py:100`; everything else
here is measured fresh. Angles are degrees clockwise from north.

## 0. The dial is drawn rotated, and the hands confirm the frame

The twelve numerals sit on a clean 30° grid whose offset is **18.75°**: numeral **3 is at the top**, not 12.
Numeral 12 sits at 288.75°, so the face is turned about **71° anticlockwise** from a standard clock. Ordering is
normal clockwise 1→12.

The offset is not assumed. Two hand directions were measured independently, as the dark radial run 40–150 px from
the centre, and both land almost exactly on a numeral midpoint:

| measured direction | falls between | fraction between them | sum | template |
|---|---|---|---|---|
| 332.38° | numerals 1 and 2 | 0.45 | **3** | `tower`@3 |
| 302.62° | numerals 12 and 1 | 0.46 | **13** | `moon`@13 |

Both reproduce REPORT 2.17 exactly, which validates the 18.75° frame.

*[CORRECTED 31 Oct, same day.] The first version of this file said the hour hand "was NOT detected". That was
wrong, and the fault was mine: the scan used ink < 205 over radius 40–150, and the hand is fainter than that.*
**The hour hand is there.** At ink < 215 over radius 30–120 it is an unmistakable spoke — a continuous dark run
from **5 to 117 px** out of the hub, **3.5° wide**, weighted centre **238.49°**. It is a hand, not a blob: it
starts at the centre and runs 112 px.

| hand | direction | between | fraction | off midpoint | sum |
|---|---|---|---|---|---|
| minute | 332.38° | 1 and 2 | 0.45 | 1.37° | 3 (`tower`) |
| second | 302.62° | 12 and 1 | 0.46 | 1.13° | 13 (`moon`) |
| **hour** | **238.49°** | **10 and 11** | **0.32** | **5.26°** | **21** |

**Slot 21's basis is confirmed, and it is weaker than the other two.** The hand unambiguously lies between
numerals 10 and 11 — fraction 0.32 is well inside the interval, and no other pair is reachable — so the sum 21
stands. But it sits **5.26° off the midpoint, about four times the error of the other two hands** (1.37° and
1.13°). The minute and second hands sit essentially on their midpoints, as the "sum of two numbers" mechanism
requires; the hour hand does not, to a degree the record does not mention.

## 1. Every clock numeral: position and legibility

Box is 64×64 px centred on the numeral, radius 182 px from the clock centre.

| num | angle | centre (x,y) | box | dark <200 | verdict |
|---|---|---|---|---|---|
| 1 | 318.75° | (350.0, 800.2) | (317,768,381,832) | 3.0% | legible, faint outline |
| 2 | 348.75° | (434.5, 758.5) | (402,726,466,790) | 16.6% | partly covered |
| 3 | 18.75° | (528.5, 764.7) | (496,732,560,796) | 14.5% | partly covered |
| 4 | 48.75° | (606.8, 817.0) | (574,784,638,848) | **35.9%** | **hidden** |
| 5 | 78.75° | (648.5, 901.5) | (616,869,680,933) | **52.7%** | **hidden** |
| 6 | 108.75° | (642.3, 995.5) | (610,963,674,1027) | **52.3%** | **hidden** |
| 7 | 138.75° | (590.0, 1073.8) | (558,1041,622,1105) | 21.8% | partly covered |
| 8 | 168.75° | (505.5, 1115.5) | (473,1083,537,1147) | 2.7% | legible, faint outline |
| 9 | 198.75° | (411.5, 1109.3) | (379,1077,443,1141) | 0.0% | legible, faint outline |
| 10 | 228.75° | (333.2, 1057.0) | (301,1025,365,1089) | 9.9% | partly covered |
| 11 | 258.75° | (291.5, 972.5) | (259,940,323,1004) | 0.0% | legible, faint outline |
| 12 | 288.75° | (297.7, 878.5) | (265,846,329,910) | 10.9% | partly covered |

## 2. What is drawn over each numeral

| num | covered by | overlap |
|---|---|---|
| 1, 8, 9, 11 | nothing | 0–3% dark |
| 2, 12 | nothing drawn; faint ground only | 11–17% |
| 3 | seal-disc ring edge, entering from the lower right | 14.5% |
| **4** | the **eye triangle's radiating rays**, plus ring text `…GERE` of COGNOSCERE | 35.9% |
| **5** | the **pyramid's upper brick courses** | 52.7% |
| **6** | the **pyramid's middle brick courses** | 52.3% |
| 7 | pyramid base band and the ring text `UBI BENE IBI PATRIA` | 21.8% |
| 10 | the rune line `здесь зашифрованы…` crossing it | 9.9% |

Nothing from the Space Needle, flag, statue, bust or figures touches any numeral: the statue is clear of 11 and 12
(both 0–11% dark), and `even_slot_rules.py` already records every calibration object as 236–1084 px from the centre
while the numerals sit at 182 px.

Angular spans from the clock centre, over ink < 205, 1st–99th percentile:

- **eye triangle only**: 45.6° … 72.0° — contains numeral **4** only.
- **eye triangle + radiating rays**: 38.9° … 78.9° — contains numerals **4 and 5** → 4+5 = **9**.
- **pyramid brick body**: 74.0° … 136.6° — contains numerals **5 and 6** → 5+6 = **11**.

## 3. The pyramid's own levels

**14 horizontal mortar lines** detected between y=890 and y=1040, i.e. **13–15 brick courses** (lines at y = 894,
904, 913, 922, 930, 939, 949, 959, 970, 979, 989, 1000, 1011, 1028). 13 is the canonical Great Seal count.

**Nothing is written on any course.** The only text in the pyramid is on the **base band**, mirror-written:
`FIAT JUSTITIA ET PEREAT MUNDUS`. The courses are plain brickwork.

## 4. Which reading the geometry supports

**It supports the clock-numeral reading, and it rules the levels reading out for the eye.**

The decisive fact is structural, not statistical: **the eye is not on the brick courses at all.** It sits in a
separate apex triangle *above* the brick body, spanning 45.6°–72.0° while the brickwork begins at 74.0°. An eye
that lies on no course cannot be derived from "levels 4+5". And with 13–15 courses rather than 6, picking out
levels 4, 5 and 6 has no motivation in the drawing.

The clock-numeral reading reproduces both assignments from measured geometry:

- pyramid body covers numerals 5 and 6 → **11** = `pyramid`@11 ✓
- eye + rays covers numerals 4 and 5 → **9** = `eye`@9 ✓

**Two caveats, both against over-reading this.**

1. **The eye match is knife-edge.** The triangle alone covers only numeral 4. Numeral 5 is reached only once the
   rays are included, and then its centre at 78.75° sits 0.15° inside the measured edge of 78.9°. A slightly
   tighter ink threshold or box drops it. This is a *marginal* match, and I widened the region to get it, which is
   exactly the move that produced earlier retractions in this project. Treat pyramid@11 as measured and eye@9 as
   suggestive only.
2. **An object this size covers two numerals automatically.** The pyramid spans 62.6°, more than two 30°
   intervals, so it is *certain* to cover at least two numeral centres no matter where it sits. The information is
   not "it covers a pair" but "which pair", and that is a single coincidence, not a pattern.

## 5. Every object covering two adjacent numerals

| object | numerals covered | adjacent sums | slot now holds |
|---|---|---|---|
| pyramid brick body | 5, 6 | **11** | `pyramid` — filled, and REPORT 2.17 calls it the template's weakest entry |
| eye triangle + rays | 4, 5 | **9** | `eye` — filled |
| eye triangle alone | 4 | none | — |
| seal disc as a whole | 3–7 | 7, 9, 11, 13 | `liberty`, `eye`, `pyramid`, `moon` |
| rune line | 10 | none | — |

The seal-disc row is a warning rather than a result. A contiguous block of numerals yields consecutive odd sums
automatically, so 7/9/11/13 follows from the disc's size alone. `liberty`@7 and `moon`@13 are not drawn under the
seal — the statue is on the far left and `moon` comes from the second hand — so the disc's sums do **not**
correspond to what is drawn there. Only the two inner objects, the eye and the pyramid, sit where the rule would
put them.

**No new slot is opened.** Every sum the rule produces (7, 9, 11, 13) is already filled, and the rule supplies no
candidate for any open slot.

## 5. [NEGATIVE, 9 Nov 2026] The hands do not encode a clock time — 8:46 and 9:29 are both excluded

Arithmetic only, on the angles already in §0. No new pixels. Recorded so the question
is closed rather than asked again.

**Convention, stated before any conversion.** Angles are **degrees clockwise from
north** (§0 line 5): 0° is straight up on the canvas, positive runs clockwise, range
[0, 360). The numeral grid is `18.75 + 30·((n−3) mod 12)`, which puts **3 at 18.75°**
and **12 at 288.75°** — the face is turned **71.25° anticlockwise** from a standard
one. Grid check: 1 → 318.75°, 10 → 228.75°, 11 → 258.75°, 12 → 288.75°.

**Two readings, because "as drawn" is ambiguous and both deserve a number.**

| reading | hour | minute | second | time |
|---|---|---|---|---|
| as drawn on the canvas, 12 *assumed* at top | 238.49° | 332.38° | 302.62° | **7:56** (7:55:50) |
| dial rotation undone, against the drawn numerals | 309.74° | 43.63° | 13.87° | **10:07** (10:07:02) |

The second row is the honest one: subtracting numeral 12's 288.75° is identical to
reading each hand against the numeral it points at — minute → numeral 1.45, second →
numeral 12.46, hour → numeral 10.32. The rotation does not change the time; it only
moves where the numerals sit on the canvas.

**Uncertainty: ±3.5 min, and it is set by the hour hand alone.** The only hand width
in the record is the hour hand's **3.5°** (§0). Minute and second widths were never
measured; 3.5° is borrowed for them and flagged as borrowed. At ±half-width, ±1.75°:

    minute hand   1 deg = 1/6 min   ->  +-0.29 min  (+-18 s)
    second hand   1 deg = 1/6 s     ->  +-0.29 s
    hour hand     1 deg = 2 min     ->  +-3.5 min

A uniform-bar sd (`3.5/sqrt(12)` = 1.01°) would give ±2.0 min instead. Either way the
hour hand is the limiting term by an order of magnitude, which is the same hand §0
already flags as the loosest of the three.

**Neither candidate time fits, and not narrowly.** Converted first, compared second:

| candidate | a real clock puts hour / minute at | hour error | minute error |
|---|---|---|---|
| **8:46** | 263.00° / 276.00° | **46.74°** = 93.5 min | **127.63°** = 21.3 min |
| **9:29** | 284.50° / 174.00° | **25.24°** = 50.5 min | **130.37°** = 21.7 min |

Against the raw canvas angles instead, for completeness: 8:46 gives 24.51° and 56.38°;
9:29 gives 46.01° and 158.38°. **Every one of these eight errors is at least 7× the
±3.5 min (1.75°) uncertainty**, and the minute-hand errors exceed 127° in the frame
that matters. Neither time is reachable in either frame.

**The stronger finding: it is not a self-consistent timepiece at all.** On a real
clock the hour hand's fractional position must equal minutes/60.

    hour hand fraction 0.325  ->  implies 19.5 min past the hour
    minute hand                  ->  says    7.27 min past
    mismatch 12.2 min = 6.10 deg of hour-hand travel

That 6.10° is the same quantity as the hour hand's **5.26° off-midpoint** error in §0.
So no time can fit, because the hands were not placed to tell one: they sit on numeral
**midpoints** (fractions 0.45, 0.46, 0.32) to make the sums 3, 13 and 21, and a
midpoint is precisely where a time-telling hand would not be except by coincidence.
The dial encodes three numbers, and the rune caption beneath it says so — *Сумма двух
чисел*, "sum of two numbers".

**What this closes and what it does not.** Closed: the clock does not depict 8:46,
9:29, or any consistent time, so no slot word, index or passphrase can be derived from
a time reading. Not touched: the sums 3, 13 and 21 themselves, which rest on the
between-numerals measurement in §0 and are unaffected by this — §0's caveat that slot
21's hand is four times looser than the other two still stands and is still the
weakest part of that chain. **No config was built from this.**
