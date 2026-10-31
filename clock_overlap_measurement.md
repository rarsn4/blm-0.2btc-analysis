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

Both reproduce REPORT 2.17 exactly, which validates the 18.75° frame. **The hour hand at 10+11 = 21 was NOT
detected** by the same scan; nothing radial appears near 243.75°. That is a gap in this measurement, not a
refutation — the hour hand is short and the statue crosses that sector — but it is recorded as unconfirmed here.

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
