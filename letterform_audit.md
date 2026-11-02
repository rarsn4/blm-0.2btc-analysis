# Re-reading every string in the image-text brainwallet corpus against the drawn letterforms

Measured 2 Nov 2026 on the master image, sha256
`d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782`, 1600x1200.

**Why.** `caccobus` was wrong for five weeks because nobody re-read the pixels after the first
transcription. This pass re-reads **every** canvas string the image-text corpus claims to carry,
from the image, by letterform — not by height, and **not against any existing transcription
file**. Each crop was cut from the master by coordinate, magnified, and read; where a reading was
marginal it was taken back to native pixels with a control, per REPORT 9's own rule.

**Audit unit** = one painted element, as `word_census.py`'s `ELEMENT_SOURCE` (22) +
`MICRO_SOURCE` (2) + `NON_WORD` (2) define them: 26 units. Four are rune decodes, which are a
cipher rather than Latin letterforms and are out of scope for a letterform re-read, so
**22 units were re-read**.

## 0. Result

| | units |
|---|---|
| **DIFFER from the corpus, confirmed** | **6** |
| flagged, below the confidence bar | 2 |
| match the corpus exactly | 14 |
| out of scope (rune decodes) | 4 |

Separately, **5 drawn strings are on the canvas and in no corpus string at all.**

Every absence below was tested against the corpus itself, not by eye: `build(MAXIMAL)` — the
union of all 64 readings §2.12's sentence admits, 29,408 distinct key strings — contains none of
them.

## 1. The six that differ

| # | element | corpus holds | drawn on the canvas | kind |
|---|---|---|---|---|
| 1 | COVID sign, x30-180 y330-425 | `COVID IS A HOAX IS THE KILLER` | **`COVID 19 IS A HOAX 5G IS THE KILLER`** | **content: two whole tokens missing** |
| 2 | bottom Latin line, x1030-1550 y1145-1190 | `…caccobus ollae` | **`…caccabus ollae`** | spelling, 1 letter |
| 3 | 13th Amendment copy, x1296-1500 y775-925 | `Section Neither slavery…jurisdiction` | **`Section 1.`** as a heading, then the body with `servitude,` `States,` `jurisdiction.` | content (`1`) + punctuation |
| 4 | E-of-BRAVE micro-text, x885-975 y468-585 | `…checks every transac tion for double spen ding. After` | **`…checks every / tran / sacti / ons. / For double spen / ding. After`** | spelling (singular→plural), line split, punctuation, casing |
| 5 | bottom whitepaper caption, x25-1065 y1138-1166 | `…were received The payee…each transaction the majority…` | **`…were received. The payee…each transaction, the majority…`** | punctuation |
| 6 | dates, x205-375 y615-725 | `1865-202?`, `1865 - 202?`, `1865–202?` | **`1865-202...?`** — three dots, then a red `?` | punctuation |

Each row is one tested string that is **not** on the canvas and one canvas string that was
**never tested**.

### Evidence, row by row

**1. The COVID sign.** Hand-lettered in two columns; read across, `COVID 19` / `IS A` /
`HOAX` / `5G IS` / `THE` / `KILLER`. `19` and `5G` are four full-size glyphs, not a letterform
call. The corpus's version drops both and reads as a different sentence.

**2. `caccabus`.** The 5th glyph is a single-storey `a` — flat top, straight right stem — against
the closed round `o` of `ollae` two words later as the control. `caccabus` is also the correct
Latin (*caccabus*, cooking pot), matching REPORT 7's own gloss.
*The `u` was checked too and is a `u`*: this hand draws `u` narrow and nearly pointed, but
`quam` in the same line fixes that shape as `u`, since `qu` is the only Latin reading there.

**3. `Section 1.`** The heading carries an underlined numeral `1`. This is not new to the
project — `expected_output/even_slot_rules.txt` already names "amendment heading 'Section 1.'"
as a slot-1 digit source — but `AMENDMENT` in `brain_image_corpus.py` drops it, and runs
`Section` straight into `Neither`. The body's commas and final period are legible at 9x; they
were not taken to native pixels, so they are carried here at the strength of the rest of the
Amendment transcription, no more.

**4. The micro-text, measured natively.** Line widths in the block, at 4.4 px/char calibrated
from `common solution` (66 px / 15 ch) and `is to introdue` (62/14):

| line | y | ink width | chars implied | reads |
|---|---|---|---|---|
| … | 541-547 | 19 px | 4.3 | `tran` |
| … | 549-555 | 19 px | 4.3 | `sacti` |
| … | 557-562 | 15 px | 3.4 | `ons.` |

The corpus splits the same word `transac` (7 ch ≈ 31 px) + `tion` (4 ch ≈ 18 px). **A 31 px line
is not there.** Three short lines are. So the canvas word is **`transactions.`**, plural and
stopped, and the corpus's `transac tion` is a word the artist did not write. The following line
begins `For` with a capital F (magnified read).

**5. The caption.** `received.` takes a full stop before `The payee`; `transaction,` takes a
comma. Both legible at 14x. The corpus has neither, and `variants()` only ever *strips*
punctuation, so the pointed form is in the corpus and the drawn form is not.

**6. The ellipsis, measured natively.** Between the final `2` and the red `?`, three ink blobs:
14 px at x318-321 y707-711, 13 px at x323-326 y712-715, 13 px at x328-331 y716-719 — evenly
stepped, each ~4x4. The `?`'s own dot is a separate red blob at x334-337 y724-727. **Three dots,
then the question mark.** No corpus form carries them.

## 2. The two flagged, and why they are not counted

Both fail REPORT 9's rule: *nothing enters the record from an upscaled view until it has survived
a native-pixel re-measurement, with a control.*

| element | the read | why it is not confirmed |
|---|---|---|
| `PAY FOR THE FUTURE.` (x77-87, y782-975, vertical) | under LANCZOS it reads **`FVTURE`** — a pointed V in position 2 against a flat-bottomed U in position 4, the control being inside the same word and the same hand | at native resolution, threshold `bg-10`, the whole word is **one merged blob** across y873-931 with no inter-letter gaps. The V/U call exists only in the upscale. **INDETERMINATE.** If it is a V, `PAY FOR THE FVTURE.` is an untested canvas string. |
| `.VS.` (x1021-1089, y1055-1088) | the two dots are **not baseline full stops**: left dot centre y1079.6, right y1064.8, against a baseline at y1088 and cap height 33 px — 9 px and 23 px above the baseline, diagonally opposed, as a 180° ambigram requires | whether that makes the string `·VS·` (U+00B7) rather than `.VS.` is a transcription convention, not a measurement. Recorded, not counted. |

`wich` for `which` in the caption was re-read at 34x and again favours `wich`. **It stays
INDETERMINATE**, for exactly the reason REPORT 9 already gave: measured here, rows y1154-1160 are
the dark frame stripe (61 of 67 px below 110), and that is precisely the ascender band. The
record does not change.

## 3. Five drawn strings the corpus does not contain at all

Tested against `build(MAXIMAL)`, 29,408 strings — all five ABSENT:

| drawn string | where | already in the record? |
|---|---|---|
| `05.25.20` | hoodie, x992-1069 y370-388 | yes — `premise_audit.md`, `even_slot_rules.py:47` |
| `11.03.20` | under `.VS.`, x1012-1098 y1098-1122 | yes — `even_slot_rules.py:48`, `slot20.py:129` |
| `UBI BENE IBI PATRIA` | seal scroll, mirror-written | yes — `seal_ring.py:13`, used as a glyph-count control |
| `BREATHE` | the bust's neck band, x1355-1430 y528-545 | yes — `three_object_measurement.md` §3 |
| `CHR` | boxed monogram, bottom right x1520-1590 y1125-1165 | yes — REPORT 3335, [INFERRED] |

Not one of these is a new reading. **Every one was already measured and written down elsewhere
in this project, and none of them reached the corpus.** That is the shape of the defect: the
corpus was built once from two transcription files and never reconciled against the element
census the project kept building afterwards.

`FOOD` (Space Needle inner column) is **not** on this list: it is a BIP39 word, so the 2048-word
group carries it in every casing already. `TOWER`, `MOON` and `STOP` are likewise covered.

The twelve clock-dial numerals are drawn text and are in no corpus string either; they are left
off the list above because single digits are not obviously phrase material, and because
`even_slot_rules.py` already treats them as slot sources rather than as text.

## 4. The fourteen that match

`FIND THE SEED PHRASE IN THE THIS PICTURE` (including the doubled article, as drawn) ·
`Order and stability` (cursive, capital O only) · `I can't BREATHE` (capital I, lowercase
`can't`, capital `BREATHE`) · the `BLACK LIVES MATTER … NOT ONE MORE` block, all seven lines ·
`WELCOME TO THE BRAVE NEW WORLD` · `ONLY real BITCOIN` (re-confirmed at 16x: `r`, `e`, `a` are
lowercase forms) · `THIS IS THE FIRST PREDICTION.` · `FUCK THIS SHIT` · `STOP` (O drawn as a
fist in a prohibition sign) · `BLM` · `TOWER` · `MOON` · `CVD19` · `RERUM COGNOSCERE CAUSAS` ·
`FIAT JUSTITIA ET PEREAT MUNDUS` · the target address, all 34 characters.

One caveat on the pyramid band: at 12 px mirror-written, the `P` of `PEREAT` closes into a `D`
form. `PEREAT` is recorded as matching because `DEREAT` is not a word and the phrase is fixed,
but the glyph itself is at the resolution limit.

## 5. On casing, since this pass settles it

Counting `Order and stability`, the drawn mixed-case strings are now **four**, not three:
`ONLY real BITCOIN`, `I can't BREATHE`, `Esse quam niger es, sic dixit caccabus ollae`, and
`Order and stability`. The retraction in `casing_measurement.md` stands and is strengthened.

A letterform note that nearly cost a second error: in the `BLACK LIVES MATTER` block and in the
COVID sign the artist draws **E as a rounded `e`-form at full cap height** — `PEACe`, `MORe`,
`THe`, `KILLeR`. That is an alternate glyph inside an all-capitals setting, not a case
difference: every letter sits at cap height, and a real case difference shows as an x-height
glyph, which is exactly what `real` and `can't` do. Those strings are **all caps** and the corpus
is right about them.

## 6. Scope, stated plainly

- The four rune decodes (`Сумма двух чисел`, `здесь зашифрованы…`, `Я надеюсь`,
  `будут присылать`) were **not** re-read. They are a cipher, not Latin letterforms; re-reading
  them is a different measurement with a different method.
- The 13th Amendment body and the whitepaper caption are ~6-8 px tall and partly under spray
  paint and a frame stripe. Their **punctuation** differences are magnified reads. Their
  **content** differences (`Section 1.`) rest on the project's own prior measurement.
- No key was derived and no run was started from this file.
