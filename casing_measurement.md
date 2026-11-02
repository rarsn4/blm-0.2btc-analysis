# Is the artwork "in capitals"? Measured from pixels, 2 Nov 2026

Master image sha256 `d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782`.
Pixels only. Prompted by the owner's challenge that "as-written = upper" had been concluded
from the slogan block alone, and from a transcription that may have been case-normalised.

**The challenge was right. The claim is false and is retracted below.**

## 1. The transcriptions disagree with each other, and one of them is normalised

The project carries the plinth text two ways:

| file | rendering |
|---|---|
| `census_crops.py:44`, `word_census.py:57`, `brain_image_corpus.py:117` | `ONLY real BITCOIN` — as drawn |
| `slogan_lines.py:49`, `brain_image_corpus.py:50` | `ONLY REAL BITCOIN` — **normalised to capitals** |

`slogan_lines.py` is the "transcription of record" I used to conclude as-written = upper.
It is the normalised one. That is exactly the failure mode the owner named.

## 2. [MEASURED] Three strings are genuinely mixed-case as drawn

Read from the pixels, not from any transcription. Letterform is decisive here, not glyph
height: at an 11 px cap height the artist draws lowercase letters nearly full height, so a
height ratio (`real`/caps = 0.91) proves nothing. What proves it is shape — a capital `E`
has three horizontal bars, the drawn glyph has a bowl and one bar; a capital `A` is a peak,
the drawn glyph is a closed round bowl with a right stem.

| string | location | as drawn |
|---|---|---|
| plinth band | x 99–229, y 1051–1062 | **`ONLY real BITCOIN`** — `ONLY` and `BITCOIN` capitals, `real` lowercase letterforms |
| hoodie | x 900–1200, y 240–420 | **`I can't BREATHE`** — capital `I`, lowercase `can't` with apostrophe, capital `BREATHE` |
| bottom Latin line | x 1030–1550, y 1145–1190 | **`Esse quam niger es, sic dixit caccabus ollae`** — one capital `E`, **everything else lowercase** |

The third is the decisive one: it is not "capitals with an exception", it is a
predominantly **lowercase** line. Any claim that the artwork is written in capitals is
false on its face once that line is read.

The slogan block *is* all capitals (`BLACK LIVES MATTER … NOT ONE MORE`), as is
`PAY FOR THE FUTURE. / THIS IS THE FIRST PREDICTION.`, `WELCOME TO THE BRAVE NEW WORLD`,
`FIND THE SEED PHRASE`, `FUCK THIS SHIT` and `.VS.`. The error was generalising from the
block to the canvas.

## 3. [RETRACTED, 2 Nov 2026] "As-written = upper"

> Retracted: the claim, made earlier today in `brain_t21_upper.conf`, in the REPORT §2.12
> note and in the `QUEUE_after_el22.md` band, that **`CASE upper` is the as-written reading
> of the artwork**. It is not. Three strings are drawn mixed-case and one is mostly
> lowercase. `CASE upper` is **one uniform capitalisation hypothesis among three**, with no
> stronger claim on the artwork than `title` or `lower`.
>
> The claim was reached by reading a single all-capitals block in a transcription that had
> normalised the counter-example out. The measurement above is what should have been done
> before asserting it.

## 4. But this does NOT add a third run, and the reason matters

**"As-written" is undefined for the template corpus.** `brain_t21_upper` and
`brain_t21_title` do not derive any string from the artwork. They build phrases from the
65-word pool in template slot order — `subject camera tower mask police …` — a sequence
**nobody ever wrote**. There is no drawn casing for it to reproduce, so a fourth
"as-written" `CASE` mode would have nothing to encode. The solver's three uniform modes are
not a limitation here; they are the whole of the hypothesis space for a constructed phrase.

**The genuinely mixed-case strings belong to the image-text corpus, and are already tested
as drawn.** `brain_image_corpus.py:172` builds `forms = [base, base.lower(), base.upper()]`
plus `base.title()`, where `base` is the as-drawn string. `CENSUS_MISC` carries
`"ONLY real BITCOIN"` and `"I can't BREATHE"` verbatim, and `LATIN_MOTTOS` the Latin line.
So the mixed-case readings are covered — at 22,638 keys, not 150 billion.

**Net effect on the queue: none.** `brain_t21_upper` and `brain_t21_title` run as banded,
32.5 GPU-h, with their justification corrected from "the as-written reading" to "a uniform
capitalisation hypothesis". No third run, no new cost.

## 5. [DEFECT, found 2 Nov 2026] The Latin line is transcribed with the wrong letter

While reading the line for casing: the drawn word is **`caccabus`**, not `caccobus`.

The fourth-from-last glyph is a single-storey `a` — flat-topped with a straight right stem —
and the round `o` of `ollae` sits two words later in the same line for direct comparison.
They are different shapes. `caccabus` is also the correct Latin: *caccabus* is a cooking
pot, and the proverb is the pot calling the kettle black, which is what §7's gloss already
says the line means.

`caccobus` appears in `census_crops.py:46`, `word_census.py:69`, `brain_image_corpus.py:105`,
`REPORT.md` twice (§715, §2999), `expected_output/census_crops.txt` and three lines of
`brain_image_keys.txt`.

**Consequence:** SHA-256 does not forgive one letter, so the brainwallet image-text corpus
tested a string that is not written on the canvas, and **the string that *is* written was
never tested** — in any casing. Cheap to close: `brain_image_corpus.py` rebuilds the whole
corpus in seconds. Not fixed in this file; recorded for a decision.
