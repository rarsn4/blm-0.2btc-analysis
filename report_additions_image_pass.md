# REPORT.md additions — image pass, drafted 28 Sep

Section numbering and placement are yours. Section A amends existing text: §6 item 5, which calls a legible view of the final glyph "worth more than any amount of GPU". Everything else is new.

Every number below comes from a script in this bundle. To reproduce:

- Put `0.2-btc-puzzle.png` in the project root, or set `BLM_IMAGE`. Every script checks md5 `7710323461a924987eb35c77055e59f6` and refuses any other file.
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
> | the X marks on the hooded head | two fully resolved X marks, the clean one 17×34 px, darkest pixel 60 on a 195 background, at eye height, **20 px apart = 1.18× the mark's width** | that `XX` is the numeral 20. In the artist's SHIT lettering, gaps run 0.05–0.24× the wider neighbouring letter (S–H: 3 px between 30- and 33-px letters). The marks are spaced like eyes (the crossed-out-eyes convention) rather than like a written numeral. That rests on one reference word, so it is indicative, not decisive. |
>
> **Verdict: the ambiguity lies entirely in the reading and the provenance, not in the ink.** The ink is clear, and it contains neither candidate. It cannot collapse slot 20 to one word. What separates the two candidates is provenance alone: `second` has a stated derivation (resting on an external lookup), and `apple` has none.
>
> **What this means for §2.13.** The runs with `second` pinned covered their branch *for `second`*. The `apple` half of each is open, except in the run that freed slot 20 to all 56 candidates. Suggested wording, which is true whichever word is right and costs no GPU time: *"slot 20 pinned to `second`, the only candidate with a stated derivation; `apple` (a README table entry with no derivation) is covered only by the run that freed slot 20."*

Script: `slot20.py`

---

## F — Readings withdrawn during this pass (calibration record)

> Of 8 first reads taken from upscaled or curved views, **1 survived** re-examination at native resolution.
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
> | `subject` underlined | **survived** (§C) |
>
> **Rule:** nothing enters the record from an upscaled view until it has survived a native-pixel re-measurement, with a control.
