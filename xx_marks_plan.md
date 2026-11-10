# Pre-registration: the XX marks, and whether XX-for-OO is a convention

Brief OO, 10 Nov 2026. Written and committed **before** any pixel was read for this item
and before the membership query was run.

## 0. Word consequences, fixed first — and stricter than the last six items

**NO WORD ENTERS ANY CONFIG FROM THIS ITEM, UNDER ANY OUTCOME.**

This gate is tighter than `choke`'s or `devil`'s, and the reason is the opposite of
reassuring: **`shoot` IS BIP39** (and old Electrum #780), so unlike `choke`, `hit`,
`devil`, `murder` and `silence` it *could* actually be slotted. A hypothesis that can be
acted on needs a stricter gate than one that cannot, not a looser one.

A config follows **only if both** of the following hold, and then only after its own
separate pre-registration:

1. **OO-1 finds the marks** — a *pair* of X marks inside a circular element; and
2. **OO-2 finds a second instance** — some other doubled letter in this painting written
   with XX or an explicit stand-in.

**One instance is not a cipher.** A rule invented to explain its only example explains
nothing, and this project already grades that shape: it is what `apple`@20 is.

## 1. What the record already establishes, so this starts from it

- **Glyph X** (`glyphX_measurement.md`, §7.4) is in **block A**, the right-edge Cyrillic
  inscription at x 1529–1555 — a single glyph in a linear text, **not inside any circle**.
  Measured: **92 ink px, 4 endpoints, one 4-way crossing, 2 strokes at 56°**, arm lengths
  **9.5 / 7.6 / 6.0 / 4.8**, stable at every cutoff from 90 to 185. It is an oblique
  cross. **This is the only X in this painting that has ever been measured.**
- **The tablet (BLM card) circle** is already measured: centre **(263.5, 760.5)**,
  **diameter 17.5 px**, with **one** interior mark of 13 × 10 px. Both its strokes are
  **sub-pixel** (peak coverage 0.76 px for the mark, 0.54 px for the ring), and the record
  states outright that *"the mark's topology cannot be recovered from this file at all"*
  and *"the test can neither confirm nor exclude that the circle contains X."*
- **The faint marks below that circle** span x 256–268, y 773–799, at most **11 levels**
  below the 222 fill. `sht_compare.py` showed the S-or-G test **has no power** there.

## 2. The circular elements, enumerated with coordinates before measuring

| id | element | geometry | source |
|---|---|---|---|
| C1 | **Great Seal disc** | box [453.75, 754.5, 838.75, 1139.5], ~385 px across | `r10_elements.json` E12 (`coin`) |
| C2 | **clock dial** | centre (470, 937), r 182 → x 288–652, y 755–1119 | `blockb_bands_check.py`; hub (473.75, 940.0) in `r10_layout.py` |
| C3 | **tablet circle** | centre (263.5, 760.5), **diameter 17.5 px** | REPORT §6, measured |
| C4 | **the tablet / BLM card** | (248, 712, 86, 80) — *not circular*, included because the brief names it | `census_crops.py` DRAWN |

### C3 is excluded for a PAIR by size, before any pixel is read

The one measured X in this painting occupies **92 ink px** with a 4-way crossing. C3's
whole interior is a disc of radius **6.55 px** — about **135 px of area** — and **13 × 10
px of it is already taken** by the single mark that is there. Two resolvable X marks do not
fit, and the mark that *is* there has already been graded unrecoverable. **So a pair inside
C3 is excluded geometrically**, exactly as `blockb_bands_plan.md` excluded R2/R3a/R3b, and
nothing measured here changes the existing grade of the single mark.

**The live question is therefore C1 and C2 only**, which are large enough to hold two.

## 3. Instrument, and a problem with it recorded in advance

The validated discriminator is **stroke topology, not correlation.**
`glyphX_measurement.md` §4 is explicit that correlation cannot decide this —
a rendered-template match can score as low as +0.155 — and that **arm count does decide
it.** So: skeleton endpoints, junction count and degree, plus arms crossing circles at
**0.28 / 0.36 / 0.44 / 0.52** of normalised glyph radius.

**An X requires: 4 endpoints, exactly one 4-way junction, 2 strokes.**

**`tablet_measure.py` and `rune_x_check.py` cannot run on this machine** — both
`from skimage.morphology import skeletonize`, and **skimage is not installed**. Their
committed `.out` files preserve the results but the scripts are not reproducible here.
This is recorded as a [DEFECT] candidate in its own right. For this item a **Zhang–Suen
thinning is implemented in-repo**, and it is **void unless it reproduces glyph X's
published figures** — 92 ink px, 4 endpoints, 1 four-way junction, arms 9.5 / 7.6 / 6.0 /
4.8 — at the same cutoffs. If it does not, this measurement reports NO POWER and stops.

**Ink cutoffs:** 90, 110, 125, 140, 155, 170, 185 — the same ladder §6 used on the circle
interior, for comparability.

## 4. Specificity control, because §1.14 happened today

A detector for "4 endpoints and a 4-way junction" will fire on any crossing of two painted
lines, and this painting is full of them. **Four control regions, equal in area to C1 and
declared now**, away from both discs: boxes at (900, 150), (1100, 430), (150, 150) and
(1150, 800), each 385 × 385 clipped to the canvas.

- A cutoff where a **control region yields two or more X-signature components** is
  **VOID**: the signature does not discriminate there and neither presence nor absence may
  be claimed.
- Reported either way, per-cutoff, including every void cell.

## 5. Decision rule, fixed before the numbers

- **POSITIVE** — two components **inside the same circular element**, each with 4
  endpoints and exactly one 4-way junction, at **two or more consecutive non-void
  cutoffs**, with glyph X recovered at those cutoffs, and the count exceeding the maximum
  control count there.
- **NEGATIVE** — control recovered, cutoffs not void, no such pair. **Then OO-1's own
  words apply: the rest of the item is void and no config follows.**
- **VOID / NO POWER** — per §3 and §4.

## 6. OO-2, the test that decides the convention

Enumerate **every** word in `word_census.tsv` containing a doubled letter — `moon` at
minimum, and every OO, LL, EE, TT, SS, FF, PP, RR, NN, MM, DD, GG, CC, OO. For each, ask
whether it is painted with **XX** or any mark standing in for the doubled letter.

Evidence, named in advance: `census_crops.py`'s **`DRAWN`** table gives the measured
painted box for each string, and its **`ELEMENTS`** table's third field is already a
**letter-substitution census** — it is where `STOP`'s *"O → clenched fist"* and `SHIT`'s
*"the I of SHIT is written"* are recorded. A doubled letter rendered as XX would be a
substitution of exactly that kind and would belong in that field. Words with no measured
box are reported as **unexamined**, not as negative.

**PRE-REGISTERED DIRECTION: the expected result is NONE.** Published either way.

- **IF NONE** → XX-for-OO is **not a convention of this painting**. The hypothesis
  collapses to its single-instance version and is graded **[EXTERNAL/PROPOSED,
  UNSUPPORTED]**, the same grade as `apple`@20. Stated in those words.
- **IF ANY** → that is a **second instance**, a rule with two instances is a cipher rather
  than an excuse, and it is **reported loudly** — and still gated by §0, which requires
  OO-1 as well.

## 7. OO-3 and OO-5

**OO-3.** Membership for **`shoot`** (BIP39 **and** old Electrum #780) and **`shot`**
(in neither list) over all **227** configs, NAMED and ADMITTED **reported separately**.
`shoot` is admissible by any `@FULL` slot, so `@FULL` must not be allowed to inflate it —
the EE-1 rule, already enforced in `config_word_membership.py`. `shot` is queried so the
record states **why the reading has to be `SHOOT` if it is anything**: a word in neither
ledger cannot be a candidate under any scheme.

**OO-5.** This goes in the **same entry** as the existing SHT dispute, not a new thread.
§2.16 quotes `u/Accomplished_Weird36`, `gn69cqa`, 2021-02-13: *"The Statue of Liberty book
doesn't say SHT."* If the marks are SHT+XX rather than SHT, that 2021 objection and this
proposal concern **the same marks from opposite directions**, and both belong together.
