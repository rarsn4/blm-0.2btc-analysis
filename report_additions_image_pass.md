# REPORT.md additions — image pass, drafted 28 Sep, extended 29 Sep

Section numbering and placement are yours. Two sections amend existing text; everything else is new.
- **A** amends §6 item 5, which calls a legible view of the final glyph "worth more than any amount of GPU".
- **H** amends §2.17: `rifle @16` moves from the counted class to "no in-image derivation".

Every number below comes from a script in this bundle. To reproduce:

- The puzzle image ships in the bundle as `0.2-btc-puzzle.png`: md5 `7710323461a924987eb35c77055e59f6`, sha256 `d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782`. It is byte-identical to the original poster's upload at `https://i.redd.it/n1x7g8ceaur51.png`. Every script checks the md5 and refuses any other file.
- Install numpy and Pillow. `slogan_lines.py` also needs `mnemonic`.
- Reference outputs are in `expected_output/`.
- Verified from a clean directory on Python 3.12.10, numpy 2.5.3 and Pillow 12.3.0.

---

## A — [MEASURED] The terminal glyph of "номер X" is a hapax, not a pixel block

Replaces the claim that a better source image would resolve it.

> **It is one glyph.** Between the three-dot separators, the right-edge column splits into groups of **1, 5, 4, 6, 2, 8, 11** glyphs. Read bottom to top, that is exactly X / номер / день / чёрный / на / биткоины / зашифрованы. (`здесь` does not segment cleanly, because below y1000 its group merges with ink that isn't part of the inscription. Nothing depends on it.)
>
> **It is fully resolved at native resolution:**
> - size 13×20 px, 96 ink pixels, strokes 3–4 px wide
> - contrast 248 levels (background 248, darkest pixel 0)
> - 4 clear rows between it and the border above, and 5 between it and the separator below
> - **0 ink pixels in the titlo band**
>
> It is complete and untruncated, and it carries no numeral mark.
>
> **Its shape settles its identity without any statistics.** It is a straight stem crossed by one oblique stroke. The five letters it could be are the ones the plaintexts never use: ж, ц, щ, ъ, э. The shape matches none of them. ж is a three-branch symmetric figure and ц is a U with a descender. It is therefore a symbol the author invented, it has no key entry, and it occurs once. By inspection, it is also unlike all ten of the artist's own digits: the 1 is a stem with a flag at its end, the 4 has a closed counter, the 7 is crossed but has a top bar, and the rest are curved.
>
> **The template check supports this, but the verdict doesn't rest on it.** Shift-tolerant mask IoU was computed against all 36 labelled cells in the same column:
>
> | reference | where the glyph's best score (0.46) falls |
> |---|---|
> | pairwise, same letter (n=31, median 0.60) | bottom 6.5% |
> | pairwise, different letters (n=599, median 0.32) | 93.5th percentile |
> | best match, if the letter is absent from the column (n=36, median 0.49, range 0.42–0.71) | 31st percentile: ordinary |
> | best match, if the letter repeats in the column (n=23, median 0.69, range 0.48–0.73) | below all 23 |
>
> Pairwise, the two tails are symmetric, so on that framing the score is equally surprising either way. The best-match rows are the like-for-like comparison, because the observed score is itself a maximum over 36 cells. The 23 repeat entries are not independent: a letter with two instances contributes twice.
>
> **Control:** assigning the letters in the wrong reading direction collapses the same-letter median from 0.60 to 0.31, the same as the different-letter median of 0.33. Glyph shapes alone therefore confirm the decode and the bottom-to-top reading.
>
> **Consequences:**
> - A better source file would render the same two strokes. What's missing is a crib, not pixels.
> - No Cyrillic-numeral reading gives a slot number: of the five candidates, only ц has a value, and it is 900.
> - So the README's "10" can't be derived from the inscription, and the glyph can't narrow the black-relocation run.

Script: `t4_ctrl.py`

---

## B — [MEASURED] The circled mark on the BLM card is the one genuine resolution limit

> **Geometry:**
> - The circle was fitted as the ring darker than both its inner and outer neighbours: centre (263.5, 760.5), **diameter 17.5 px**.
> - The interior mark measures 13×10 px.
>
> **Stroke width.** A stroke narrower than one pixel never reaches the pen's full darkness, so the ratio (background − darkest) ÷ (background − pen) estimates the widest stroke's width. On this card the background is 222, and the pen is 29, taken from the BLM capitals on the same card.
>
> | feature | darkest pixel | peak stroke coverage | pixels past half-pen darkness |
> |---|---|---|---|
> | interior mark | 76 | **0.76 px** | 17 |
> | ring | 118 | **0.54 px** | 2 |
> | BLM capitals, same card (legible control) | 29 | full | 135 |
> | rune glyph (resolved control) | 0 | full | — |
>
> Strokes narrower than a pixel merge, so a junction and a near-miss render the same. The mark's topology can't be recovered from this file.
>
> **It is not the artist's STOP emblem drawn small.** That emblem is the solid fist that stands in for the O of STOP. Shrunk to 18 px by box-averaging, it keeps **74** pixels below 90; the card mark has **4**. A line-drawn fist, a circled A and similar shapes cannot be told apart at this size.
>
> **Consequence:** the report has called two readings pixel-blocked, and this is the only one that is. A higher-resolution source can unblock one reading, not two. Sub-pixel strokes are what a larger working file produces when it is downsampled, so such an original probably exists.

Script: `t2_cov.py`

---

## C — [MEASURED] Underline census of the hand-copied 13th Amendment: one mark

> The census covers 34 tokens: the 32 body words plus the heading `Section 1.`.
>
> - A word counts as **obscured** if spray paint covers at least 40% of its underline band (1–4 rows below its baseline).
> - A word counts as **marked** only if the thin-line detector finds a run covering at least 50% of the word, and at least one of those runs is clean.
>
> | status | count |
> |---|---|
> | underlined | **1** (`subject`) |
> | visible, unmarked | 24 (12 under a strict 25% spray rule) |
> | obscured, so uncheckable | 7 (`except`, `a`, `punishment`, `shall`, `have`, `States,`, `any`) |
> | heading `Section 1.` | indeterminate: its line fragments can't be separated from the letter bottoms |
>
> That is one mark in 25 checkable words, or one in 13 under the strict rule. No word in the text is boxed or circled (checked by inspection).
>
> `subject` is BIP39 **#1728** and is the template's **assigned** word for slot 1. It is in neither pool. The underline is therefore not a new candidate: it is the first physical, in-image corroboration of any template assignment in this project.
>
> **Why `subject` is a drawn underline and not spray-paint halo.** The table gives column means per row (paper ~140, handwriting 90–125, spray 55–75):
>
> | columns | y901 | **y902** | y903 | y904 |
> |---|---|---|---|---|
> | under `su`, plus the I/T gap | 122 | **106** | 131 | 112 |
> | I/T gap only, no spray within 3 rows | 118 | **104** | 139 | 129 |
> | control: `place`, above the H | 113 | 119 | 103 | 91 |
> | control: `any`, above the S | 97 | 95 | 87 | 75 |
>
> The line has a paper-level row directly beneath it, and it runs on over a gap with no spray underneath at all. The two control words on the same line also sit directly above spray, yet their values only darken steadily into it, with no separate line.
>
> **Detector checks:**
> - Positive control: the `subject` line itself is detected.
> - Known false-positive mode: a flat baseline where rounded letter bottoms touch, e.g. y842 under `servitude`. There is no lighter row between that line and its letters.
>
> An earlier note said `except` was not underlined. The correct entry is **uncheckable**: its band lies under the crossbar of the T in THIS.

Scripts: `t3_lines.py`, `t3_census.py`

---

## D — [TESTED, by inspection] Letter-substitution census: 1 in 331

> **Question:** how many letters in the artwork are drawn as objects instead of written?
>
> **Criterion:** a letter counts only if a depicted object occupies its place in the word. Outlined, textured, micrography-filled and mirror-written letterforms all count as written.
>
> **Scope:** 331 letters examined glyph by glyph in nearest-neighbour views at ×2–×8. That covers every element large enough that an object the size of a letter would be identifiable:
> - the title words
> - the FIND THE SEED PHRASE watermark
> - the five slogans
> - the hoodie text
> - the BLM card
> - FUCK THIS SHIT
> - `.VS.`
> - the seal ring and scroll
> - the clock-hand words
> - the address
> - the plinth
> - the ghost text beside the address
> - the Latin line at the bottom right
>
> Text of ~5–8 px was screened as blocks only: the bottom caption, the amendment copy, the pyramid base, the vial label and the micrography.
>
> **Result: exactly one.** The O of STOP is a clenched fist (neither `stop` nor `fist` is a BIP39 word). `SHIT` is fully lettered: the I is written, not drawn as an object. All ten of the artist's digits are written.
>
> **Verdict:** the fist is a one-off, not a system.

Script: `census_crops.py` regenerates every view the census was judged from and prints the table. The judgment itself is visual and cannot be computed.

---

## E — The seal ring carries three words; record it as a motto, not an omission

> **[MEASURED] Word count.**
> - The ring's text band (ρ 159–176 from the fitted border, centre (646.25, 947.0), r 192.5) was unwrapped by nearest-neighbour polar sampling. Every strip value is therefore a source pixel.
> - Between the scroll's two curled ends it holds **three word blocks**, 105, 171 and 104 px wide.
> - They are separated by ink-free gaps of 10 and 15 px.
> - There are **86 and 81 px of ink-free paper** between the text and the two curls, so nothing is occluded.
>
> Virgil's line, *Felix qui potuit rerum cognoscere causas*, has six words. The ring carries three.
>
> **[READ once, unverified] Which three.** The text is mirror-written. Read right to left, it gives **RERUM · COGNOSCERE · CAUSAS**, the last three words of the line. A small mark sits between the first two letters of RERUM in reading order. It is noted here but not interpreted.
>
> An earlier read, made on the curved image, took the right-hand word for `FELIX`. It was wrong. Letter identity rests on reading because both objective instruments failed their controls:
> - Glyph counting by ink profile, tested on the scroll's known `UBI BENE IBI PATRIA` (3-4-3-6), never recovered that pattern. The hollow letters fragment or merge.
> - Letter identity by mask IoU, calibrated on the letters repeated within CAUSAS and COGNOSCERE, separates poorly: same-letter median 0.29 against 0.25 for different letters, with overlapping ranges.
>
> A **blind** read of `expected_output/seal_ring_strip.png`, by someone who hasn't seen this transcription, is still pending.
>
> **Why this is not an omission.** *Rerum cognoscere causas* is a standard motto in its own right; the London School of Economics uses it, for one. Its base rate makes it unfit as evidence of a deliberate deletion alongside "a trusted". It changes no search, since no Latin word is in BIP39.

Script: `seal_ring.py` (also writes `seal_ring_strip.png`)

---

## G — [MEASURED] Slot 20: the ink cannot decide between `apple` and `second`

> **Neither word is in the image.** The letter census (§D) found no `apple`, `second`, `2nd` or `II` in any display lettering. Slot 20 has no glyph group, so there is nothing to resolve. (Slot 20 is an *assigned* slot with a two-way list, as §2.13 says; it is not one of the six gaps.)
>
> **The README disagrees with itself.**
> - Table row 20 gives `apple` with an empty description, and there is **no derivation of `apple` anywhere in the README**.
> - §19 derives `second` in two steps. The number comes from the "XX" on Leopold's head, read as 20. The word comes from the external fact that Leopold II was the second King of the Belgians. The enumeration rule excludes that kind of lookup.
>
> **The two physical features §19 rests on, measured:**
>
> | feature | what the ink holds | what is a reading |
> |---|---|---|
> | wreath plaque below the bust (frame x1380–1402, y692–710) | two matched strokes, each 2 px wide and ~7 px tall (y697/698–703), each flanked by light columns (139–158); a third, darker stroke runs to y707 and merges into a full-height shaded block, so it is shading | that the pair is the numeral `II`: with no serifs at 7 px, the ink cannot tell `II` from two hatching strokes |
> | the X marks on the hooded head | two fully resolved X marks at eye height, 34–36 and 30–31 px tall, darkest pixels 60 and 86 on a 195 background. Closest-ink gap 20–21 px. **Gap ÷ height 0.597–0.656**, stable over thresholds 90–120. (Hood shading between the marks reaches 126, so higher thresholds would bridge them.) | that `XX` is the numeral 20 (see the spacing test below) |
>
> **[MEASURED] Spacing test.** How widely does the artist space adjacent letters and numerals within a word?
>
> **Method:**
> - A glyph is a connected ink component. Fragments under 40% of the median height are dropped, judged by height, never by gap.
> - Gap = the clear pixels between the closest ink of two neighbours. This measures slanted and rotated text the same way as upright text.
> - Height = the glyph's full ink extent across its line of text, taken over its whole span along the line. This matters for the spray letters, which break where the paint is lighter.
> - A set is used only if segmentation yields exactly the known character count **and** the boxes in `slot20_segmentation.png` show one glyph per box.
> - Both checks proved necessary. FUCK and THIS once matched their counts by coincidence: a merged pair plus a sliver of the pedestal edge. NO JUSTICE NO PEACE matches its count but leaves the I of JUSTICE unsegmented.
>
> **Sets used:** 7 (SHIT, LIVES, MATTER, STOP KILLING US, NOT ONE MORE, 11.03.20, .VS.), giving **33 within-word pairs**. Rejected: FUCK, THIS, BLACK, END POLICE BRUTALITY and 05.25.20 on count; NO JUSTICE NO PEACE on inspection.
>
> | reference | widest gap ÷ height | X marks (0.597, conservative) as a multiple |
> |---|---|---|
> | SHIT, at measured cap heights 70–72 px: SH 0.030, HI 0.128, IT 0.028 | 0.128 | 4.7× |
> | the artist's numerals, 11.03.20 (3 pairs) | 0.194 | 3.1× |
> | all 33 pairs: median 0.182 | — | 3.3× the median |
> | all 33 pairs: widest, IN of KILLING (marker capitals) | 0.291 | **2.1×** |
>
> **No letter or numeral pair in the artist's hand is spaced as widely as the X marks: 0 of 33.** Reading `XX` as the numeral 20 therefore requires a spacing the artist uses nowhere else. The crossed-out-eyes reading is supported by complete separation. The margin is 2.1× over the single widest pair, 3.1× over the artist's own numerals, and 4.7× over SHIT.
>
> An earlier figure of 6.8× divided by the 87-px search band instead of measured cap heights and used SHIT alone as the reference. It is superseded.
>
> **Verdict: the ambiguity lies entirely in the reading and the provenance, not in the ink.** The ink is clear, and it contains neither candidate. It cannot collapse slot 20 to one word.
>
> **What this means for §2.13.** The table and §19 disagree, and §19's derivation rests on a lookup the enumeration rule excludes. So there is **no README value at slot 20**, *a* is undefined there, and every §2.13 branch claim is stated per reading: slot 20 = `second`, and slot 20 = `apple`. The spacing result also weakens §19's own step from "XX" to the number 20.

Script: `slot20.py`

---

## H — [MEASURED] No even-slot rule exists in this image; rifle 16 has no in-image derivation

**Amends §2.17.** Move `rifle @16` out of the counted class and into **"no in-image derivation"**, beside `black @10`.

> **The rule hunt.** Twelve candidate numbering rules were each applied to the whole picture:
> - counts of depicted objects (all objects, or repeated ones only)
> - numbers written in ink (all of them, or only those labelling an object)
> - the parts of written dates
> - line numbers (in every multi-line text, or the slogans only)
> - a vertical flip that turns lettering into a numeral
> - counts of an object's sub-parts
> - the single dial numeral nearest an element
> - number words in the rune plaintexts
> - one disjunction of two of the above
>
> **The pass criterion:** a rule must fill each slot at most once, and reproduce at least two of camera 2, mask 4, rifle 16 and subject 1. The inputs were fixed first: the pre-registered depicted-object counts, the census's list of written numbers, and the measured multi-line texts.
>
> **Result: 0 of 12 rules pass.**
> - **Counting** is the only rule family that reaches camera 2 and mask 4, and it fails on its own output: **slot 2 holds camera, lens and suit**, which are all BIP39 words and all counted 2.
> - **Numbers labelling an object** form the one collision-free rule, but that rule reproduces only subject 1 (and glove 19, which is outside the calibration set).
> - **The disjunction** reaches 3 of 4 calibration words, but it was joined after seeing the template, and the script's output says so.
>
> **Rifle 16.**
> - The rifle's only mark is on its receiver: **7×7 px at 26 levels** of contrast (darkest pixel 220 on a background of 246). It is illegible.
> - No count of 16 exists anywhere in the picture.
> - The 16 therefore comes from identifying the model as an M16 **by its shape**, which is outside knowledge.
> - So **two assigned slots rest on nothing the picture states: rifle @16 and black @10.**
>
> Taken together, the template's non-clock slots need at least three unrelated mechanisms: counts for 2 and 4, labelling numbers for 1 and 19, and a flip for 12. Slot 16 needs outside identification on top of that.

Script: `even_slot_rules.py`

---

## I — [MEASURED] The artwork is not laid out on the clock dial (R10)

> **Pre-registration.**
> - `r10_elements.json`, sha256 `3634036d4e0d785b2f2efbe5cb34c6a2ca69528f73a316c16c9d31c0e2b49b88`, fixed before any angle was computed.
> - It holds 28 whole-object elements, each an object or text block carrying a word from the enumeration.
> - Hub (473.75, 940.0), θ12 = 162.30°, and a grid of 24 directions every 15°.
> - Nulls: rotating θ12, and a random hub inside the frame, with 10,000 draws each.
> - Decision rule, stated in code before running: p < 0.05 under **both** nulls, on the primary set.
>
> **Result: NOT SIGNIFICANT.**
> - The primary set has **3 of 28** elements within 0.5° (1.9 expected), p 0.28 / 0.28.
> - At 1.0° it has **4 of 28** (3.7 expected), p 0.50 / 0.51.
>
> The clock governs the hands and the seal only. The non-clock half of the phrase has no layout rule this image can recover.
>
> **Erratum** (`r10_erratum.md`).
> - E24's boxes were shifted about 60–90 px right, because a grid line was misread. The pre-registration file is left as it was.
> - **Post hoc**, with the boxes corrected: the primary set is unchanged. The face-level set becomes 5 of 28 (p 0.069 / 0.032) and 8 of 28 (p 0.119 / 0.024). That still fails the both-nulls rule. Across 8 comparisons it would also need p < 0.00625.
>
> **Set C is closed** (`STOP_R10_SET_C.md`).

Scripts: `r10_layout.py` + `r10_elements.json`; `r10_erratum_check.py`

---

## F — Readings withdrawn during this pass (calibration record)

> Of 9 first reads or first measurements, **1 survived** re-examination at native resolution.
>
> | first read | outcome |
> |---|---|
> | `-IGHT` on the BLM card | not text: flat row profile, 35 levels of contrast against 193 for the BLM capitals |
> | `SHT`, missing its I | `SHIT` is complete |
> | `except` underlined | spray edge; the word is uncheckable |
> | `DAY FOR THE FUTURE` | it reads `PAY`, so `day` stays translation-only |
> | `wich` for "which" | indeterminate: the ascender band lies under the frame stripe |
> | `Section 1.` underlined | indeterminate |
> | `FELIX` on the seal ring | it is `RERUM` |
> | SHIT letter spacing, first measurement: "no difference from the X marks" | the T was cropped below its crossbar and measured as an 8-px stem. With full letters, every letter gap is narrower than the X gap (§G). |
> | `subject` underlined | **survived** (§C) |
>
> **Rule:** nothing enters the record from an upscaled view until it has survived a native-pixel re-measurement, with a control.
