# Glyph X — measured, from `pictures/20_1.png`

Prompted by PUZZLE_STATE.md §4, which names two tests as valid-but-unperformed.
Everything here is measurement on pixels; no visual judgement is load-bearing.

Source: `BLM_0.2BTC-main/pictures/20_1.png` (797×45), the left-to-right rendering
of the right-edge inscription. Text rows are 5–28; row 29 is the frame bar's
edge and merges every glyph in the left half if included.

## 1. Segmentation reproduces the published token lengths

Ink-profile segmentation over rows 5–28 gives **41 glyph groups and 7
separators**. Group widths ≤5 px are separators (x-centres 98, 315, 466, 508,
628, 707, 779). Token lengths fall out as

    5, 11, 8, 2, 6, 4, 5, 1

which is §3's published segmentation, reproduced independently. One caveat: in
`номер` two glyphs touch and segment as a single 25 px group, so 41 groups carry
42 letters.

## 2. A calibrated discriminator, built from repeated letters

The inscription repeats н (6×), и (3×), а (3×), ы (3×), о (3×), р (3×) and
others. Correlating every pair of observed glyphs after bbox→square
normalisation to 32×32 and z-scoring gives an empirical baseline:

| | n | mean | sd | 5th pct | 95th pct |
|---|---|---|---|---|---|
| **same** letter | 34 | **+0.689** | 0.147 | +0.452 | — |
| **different** letter | 707 | **+0.085** | 0.198 | — | +0.440 |

Separation **3.05 σ**; decision boundary ≈ **+0.45**. This is the piece that was
missing — without it a correlation figure cannot be read as anything.

## 3. Glyph X matches no letter used elsewhere in the text

Glyph X against all 39 other observed glyphs, best score per letter:

    д +0.435   о +0.367   е +0.365   ь +0.343   р +0.254   ё +0.248
    н +0.179   и +0.162   а +0.126   ч +0.094   в +0.065   с +0.030
    й +0.028   ф -0.018   ш -0.021   б -0.029   ы -0.035   к -0.055
    з -0.286   т -0.317

Maximum **+0.435**, under the same-letter 5th percentile of +0.452. **No letter
used in this inscription reaches the match band.** That is the linguistic
exhaustion argument confirmed by measurement rather than by reading plaintexts —
it does not inherit the decodes.

## 4. The composite-ж test: correlation cannot decide it, arm count can

§4 prescribes rendering the composite (saltire + vertical bar) and correlating
*that*. Done: **r = +0.264**.

**That number is not usable.** Calibrating the rendered-template channel against
letters whose observed instances exist gives a true-match band of

    triangle→а +0.710   diamond→с +0.619   Ψ→и +0.509   three-diagonals→е +0.155

— a spread of 0.155 to 0.710. A true match can score +0.155, so +0.264 decides
nothing. The rendered-vs-hand-drawn domain gap is too wide at this resolution.
Reporting +0.264 as evidence either way would repeat, in a new form, exactly the
error §4 withdraws the old test for.

**Arm count does decide it.** Counting ink runs crossing circles at 0.28/0.36/
0.44/0.52 of the normalised glyph radius is aspect-invariant and tolerant of
stroke weight:

| figure | arms @ 0.28 / 0.36 / 0.44 / 0.52 | angles @ 0.44 |
|---|---|---|
| rendered saltire `х` | 4 / 4 / 4 / 4 | 45, 135, 225, 315 |
| rendered composite `ж` (✕ + \|) | **6 / 6 / 6 / 4** | 45, 90, 135, 225, 270, 315 |
| rendered vertical + 1 diagonal | **4 / 4 / 4 / 2** | 90, 135, 270, 315 |
| **observed glyph X** | **4 / 4 / 4 / 2** | **97, 155, 268, 335** |

Glyph X matches "vertical + one diagonal" on arm count at every radius and on
all four angles to within 5–20°. **ж carries two more arms at every radius than
glyph X has.** The composite-ж hypothesis is refuted — by stroke topology, not
by correlation.

The raw ink, 16×10 px, shows the same thing directly: a full-height vertical at
columns 3–4, and one diagonal from (row 4, cols 7–9) to (row 11, cols 0–2).
Two strokes. ж needs three.

`ц` is refuted as well (rendered r = **−0.312**, and its closed U-plus-descender
topology shares no arm structure with glyph X).

**Instrument limitation, stated:** arm counting is stable on open stroke figures
and unstable on closed or curved ones — observed `с` gives 3/1/5/1 across the
same radii. Glyph X is an open stroke figure, so it applies here; do not carry
this instrument to the diamond- or loop-shaped glyphs without re-validating.

## 5. What this does to §4

Of the five letters absent from all three plaintexts — ж ц щ ъ э — the two with
a testable shape prediction are now **measurably refuted**: ж by arm count, ц by
both. The remaining three (щ, ъ, э) are author-invented forms with no reference
shape anywhere in the corpus, so no measurement can address them.

This *strengthens* §4's conclusion rather than moving it. The sentence-context
lever (`номер` wants a number; of the five only ц carries a numeral value) now
points at a letter whose shape is measurably wrong, which was previously "my
eye, not a measurement." Glyph X remains unassignable, and a higher-resolution
scan still does not fix it — the missing thing is a key, not pixels.

## 6. NOT done

The 26-symbol Gravity Falls correlation is **still outstanding**. §4 tags "not
in the GF key at all" as [MEASURED], but that came from visual comparison
against `pictures/11_1.png`; it needs the 26 symbols segmented off the reference
sheet and run through the harness in §2 before it carries that tag. The harness
now exists and is calibrated, so this is a short job — but it has not been done,
and the tag should read [VISUAL] until it is.
