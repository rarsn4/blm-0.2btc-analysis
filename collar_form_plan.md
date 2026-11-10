# KK — the collar form at the Leopold bust: three tests, and what may follow from them

Written and committed **before any of the three tests ran**. The word consequences in §2 were
fixed first, deliberately, because they are the part that can be rationalised afterwards.

## 0. What this is about, and one correction owed before anything is measured

The 10 Nov contact sheet (§2.16) found one form in the whole painting that reads as an animal
head: a grey shape at the Leopold bust's collar, with a tapering snout or beak, a dark spot
reading as an eye, and a bright glint beside it. It was recorded as **"almost certainly the
knotted end of the red bandana"**, on a symmetry argument.

**That description was wrong on its own terms, and the error is recorded here before it is
tested.** The form is **grey**; the bandana is **red**. A grey object is not the end of a red
cloth. The cloth hypothesis that survives colour is a different one — **the statue's own coat
collar**, which is grey, which the bandana is tied over, and which would plausibly show a
corner on each side of the knot. The tests below are run against *that* hypothesis, not the
one first written down. The coordinates were also eyeballed and are corrected here from
x 1330-1375, y 505-545 to the measured extent.

| object | box, measured from a gridded crop |
|---|---|
| **FORM** | x 1349-1373, y 509-541 (24 x 32 px) |
| **claimed partner** (grey shape on the other side of the knot) | found by search, see 1a |
| bandana | red pixels, hue outside 0.08-0.92 with S >= 0.35 |
| garment | the bust's grey coat: S < 0.25, inside the bust box, excluding bandana and sky |

## 1. The three tests, each able to return "cloth"

### (a) Symmetry, with a control

The cloth reading rests entirely on the claim that a matching shape sits mirrored on the far
side of the knot. That claim is tested, not assumed.

1. Mirror the FORM box about a vertical axis at `x = A`, for every `A` from 1374 to 1410 in
   0.5 px steps, and correlate (Pearson, on luminance, mean-centred) with the pixels there.
   **Report the best correlation and the axis that produced it** — this is deliberately
   generous to the cloth hypothesis, since it lets the partner sit wherever it fits best.
2. Correlate the FORM against **at least 10** unrelated patches of the **same garment**, same
   size, drawn from the same hue and saturation band, each mirrored the same way.
3. **Decision rule.** Symmetry is established only if the mirrored-partner correlation
   **exceeds the garment-control distribution**. If it sits inside that distribution,
   **SYMMETRY IS NOT ESTABLISHED and the cloth reading loses its only support.** Both numbers
   are reported either way.

### (b) Hue

Sample the FORM, the best partner, the **lit** bandana, and the **shadowed** bandana — the
latter defined as bandana pixels in the lowest quartile of value, so that "it is just cloth in
shadow" is tested against shadowed cloth rather than against lit cloth. Report median hue,
saturation and value with interquartile ranges for all four, and the garment for reference.

**Decision rule.** If the FORM's saturation lies below the **shadowed** bandana distribution,
it is not bandana cloth under any lighting. If it lies inside the garment's distribution, it
is consistent with the coat.

### (c) The glint

1. Find the dark cluster inside the FORM algorithmically — the largest connected component
   below the 10th percentile of the FORM's value — not by hand-picked pixels.
2. Find the brightest cluster within 6 px of it, above the 90th percentile, and measure its
   contrast against its own local surround, in 0-255 levels.
3. **Scan the whole garment for bright clusters of comparable size** and measure the same
   contrast for each. Report how many reach the glint's contrast.
4. Also report the **conjunction**: how often a dark cluster of comparable size on the same
   garment has a bright cluster adjacent to it, since the eye-and-glint pair is the feature
   that reads as a face, not either part alone.

**Decision rule.** A glint that repeats across the garment's folds is a highlight. A glint
that is unique on that garment at that scale is a different object. The conjunction count
decides it, not the glint alone.

## 2. What may follow in words — fixed now, not after

- **NO WORD ENTERS ANY CONFIG FROM THIS, under any outcome**, until the shape is identified
  independently of what word would be convenient.
- **If all three tests favour an object rather than cloth, the next step is IDENTIFYING the
  animal from the pixels — not choosing among BIP39 animal names.** If the pixels cannot
  settle the species, the result is **"an unidentified form"**, and **no word follows**. The
  wordlist holds dozens of animal nouns; **a form that admits several of them admits none**.
- **THE LEOPARD/LEOPOLD PUN IS NOTED AND QUARANTINED.** The bust is of Leopold II, `leopard`
  is a BIP39 word, and the resemblance of the two names is **a reason for a stricter test, not
  a candidate**. It is excluded from the identification by this paragraph, written before the
  measurement. If `leopard` were ever proposed because the pun is pleasing rather than because
  the pixels show spots and a feline skull, that would be §2.16's `apple@20` happening a
  second time with a better story — a seven-link chain with one trivial link measured.
- **This is not the zodiac llama under any outcome.** The Gravity Falls llama is a full-body
  pictogram; a head alone is a different object. **The locator grade stays
  `[TESTED, NEGATIVE for 2 of 10]` whatever these three tests return.**

## 3. The inventory gap, which is real whatever the form turns out to be

`r10_elements.json` carries the Leopold bust as **`E24`, one box for the whole bust**. The
collar detail sits inside that box and has **never been separately measured**. A feature of
roughly 24 x 32 px inside a pre-registered element box, unexamined for six weeks while the box
itself was used in a layout test, is a gap in the inventory independent of what the feature
is. It is recorded in §6 on that basis alone.
