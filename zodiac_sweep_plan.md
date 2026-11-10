# II-1 — sweep the whole image for four uncommon zodiac symbols

Written and committed **before the sweep ran**, as `blockb_bands_plan.md` was. Regions,
contrast levels, component filter, per-target criteria, control and decision rule are all
fixed here. Nothing below was chosen after seeing a result.

## What is being tested, and what is not

The Gravity Falls zodiac wheel has ten pictograms. One form of the hypothesis — *the ten
symbols are the ten words* — is **closed** by a wordlist measurement that needs no image
(§2.16: `llama` and `pentagram` have no BIP39 token, and `star` is not BIP39). That is not
what this sweep is about.

This sweep tests a **different and open** form: are any of those symbols **drawn in the
painting**, where they could serve as locators or as an order? Nothing in this project has
ever looked. **Absence is the expected result and is recorded either way.**

## Targets — four, and only four

| target | why it is worth sweeping |
|---|---|
| **llama** | highest value: nothing else in a BLM protest scene looks like one |
| **pine tree** | a conifer silhouette is not otherwise part of this scene |
| **ice bag** | a tied bag is a specific object, not scene furniture |
| **pentagram** | a five-pointed *line* figure, distinct from a filled star |

**Deliberately NOT swept: star, heart, hand, moon, glasses, question mark.** Those six are
free in any crowded painting: the artwork already contains a question mark (§2.16), hands,
and stars on a flag. Finding them would measure nothing, and reporting them as hits would be
§1.7's shape — a count nobody made earn anything.

## Image, passes and levels — the same as the block-B sweep

- Image: the master PNG only, `sha256 d0b04378…`, through `imgio.load_gray()`.
- Region: **the whole image**, 1600 x 1200, no mask.
- Contrast levels: the block-B cuts, `CUTS = (90, 110, 130, 150, 170, 190, 215)`, dark-ink
  thresholds `G < cut`, seven passes.
- Components: `scipy.ndimage.label` 8-connected; keep components with area >= 40 px and
  bounding box between 12 and 400 px on its longest side. Larger or smaller than that, no
  zodiac pictogram could be drawn legibly in this artwork.

## Per-target criteria, fixed before running

A component is a candidate for a target only if it passes **every** row for that target.

- **pentagram**: hull solidity in [0.30, 0.80]; the radial extremity profile r(theta) over
  72 bins of 5 deg has **exactly 5** circular local maxima with peak/trough >= 1.25; the five
  peak angles lie within +/- 10 deg of a regular 72 deg spacing.
- **pine tree**: solidity >= 0.55; width profile w(y) rising, least-squares slope > 0 with
  R^2 >= 0.45; top-decile width <= 0.35 x bottom-decile width; height/width in [0.7, 3.0].
- **ice bag**: solidity >= 0.55; width profile has a local minimum in the upper third at
  <= 0.55 x the maximum width, with ink above that minimum; body aspect <= 2.5.
- **llama**: width/height in [0.7, 2.2]; **four** separated downward protrusions in the
  bottom fifth of rows, each <= 0.25 x the component width; and one upward protrusion in the
  top third, off-centre (a neck).

## CONTROL — the power test, and the only thing that licenses "absent"

For each target, a synthetic instance is rendered at **four sizes (20, 40, 80, 160 px)** into
a copy of the image at four locations, and the identical pipeline is run over it.

**A target counts as swept only at the sizes and cuts where its planted control was
recovered.** Where a control is not recovered, the result for that target is **"no power"**,
not "absent". A detector that cannot find a shape it was handed cannot be cited as evidence
that the shape is missing, and the faint-group work (§2.16) is in this report precisely
because that distinction was once missed.

The synthetic llama and ice bag are **crude silhouettes drawn by this script**, not the
Gravity Falls art. Recovering a synthetic shape shows the pipeline works on that shape; it
does **not** show the pipeline would catch a hand-painted llama in a crowded scene. That gap
is stated in the result and is not closed by this sweep.

## Decision rule

- **Presence**: one or more components passing a target's criteria at any swept cut. Report
  bounding box, centroid, the cut, and the component's contrast against the ring of pixels
  around it. Presence is a candidate for visual confirmation, never a confirmed symbol.
- **Absence**: zero such components at every cut where that target's control was recovered.
  Reported as "absent at all levels swept", with the levels and sizes named.
- **No power**: the control was not recovered at any size for that target. No absence claim
  is made.

Nothing in this sweep can make the words form of the hypothesis live again, and nothing in it
grades the locator/order form above `[UNTESTED]` — a hit here would be an object in a
painting, not a measured link to a slot or a word.
