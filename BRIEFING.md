# 0.2 BTC Puzzle — briefing for the collaborating agent

**Written 2026-09-01. Supersedes the 2026-08-31 handoff.**

Read §1 first: it lists what changed since your document, including three
corrections to it. Then §5, which is the only genuinely new lead.

---

## 1. Corrections to your 2026-08-31 handoff

Four items. Three are wrong, one is stale.

**1.1 §9.3's chunk arithmetic conflates two constants.** `CAP` is the *survivor
buffer*, `1u<<25` = 33,554,432. `CHUNK` is the *candidate* stride, and for a
12-word config it is `((CAP<<4)/8)*7` = 469,762,048. Your "CAP = 4.5 × 2³⁰ =
4,831,838,208" is neither.

The consequence favours us: 4,227,858,432 / 469,762,048 = **9.0 exactly**, so the
displayed progress was after **nine chunks**, not one. The hit at 4,650,657,157
fell in chunk 10 at offset 422,798,725. The multi-chunk control crossed nine
boundaries, not one — stronger than you credited it.

**1.2 §9.3 is stale.** The seam gap you identified is closed. Count invariance
holds at seven chunk sizes down to `--chunk 7` (599,187 chunks, identical
262,250); `t18_pool52` reproduces **5,941,047** survivors at four chunkings,
matching three runs of the *previous* binary; and the answer HITs planted
first-of-chunk and last-of-chunk at both small and >2³² indices. Your proposed
Test 2 as written cannot run — `--chunk 4650657157` yields ~290 M survivors
against a 33.5 M buffer and aborts on overflow before reaching the seam. `--seam N`
replaces it.

**1.3 There is no `sRGB` chunk.** §2 lists `IHDR, sRGB, sBIT, IDAT×n`. Verified
directly from the file: `IHDR, sBIT, IDAT×293, IEND`. Two separate documents now
assert `sRGB`; neither is right. Your "no metadata" conclusion survives either way.

**1.4 Seven bugs is now eight.** `show_hit` printed `m/44'/0'/0'/0/0`
unconditionally, so any config with multiple `PATH` lines — `t18_pool52` has four,
`t18_pathc` has eight — would have misreported which path produced a hit. It is
the only member of the family that corrupts a **success** rather than a negative,
and it fires only on success, so nothing but a hit could ever have exposed it.
Fixed: `k_derive` now records the path index.

Everything else in your document checks out, including the 28/33 letter split, the
five absent letters, the reading directions, and the `BigInteger.Parse` trap. Your
tag scheme has been adopted in the published report.

---

## 2. What is settled

Full detail in `REPORT.md` at https://github.com/rarsn4/blm-0.2btc-analysis —
now 756 lines, §0–§10, current as of today.

**[EXHAUSTED] 25,188,563,424 seed derivations** (BIP39 19,841,556,074 + Electrum v2
5,347,007,350), four derivation paths, indices 0–35. Every template length, every
pool from 37 to 80 words, template reversal, position offsets, 65 passphrases,
leave-one-out over the entire 2048-word dictionary at each gap, free-one-fixed
across all 13 fixed words, and the all-slots-vary sweep (8,192 combinations) under
both schemes.

**[TESTED] 7,939,492,344 brainwallet addresses** — reported in a separate column,
because a brainwallet address is ~31× cheaper than a seed derivation (489,000/s
against 15,600/s measured) and folding them into one total would inflate the figure
with work that is not the same work.

**[MEASURED] Two wordlists are impossible, not untested.** Electrum v1 lacks 7 of
15 table words; Russian BIP39 lacks 9 of 20. Both die at the vocabulary stage.

**[MEASURED] Image and chain closed.** No steganography, opaque alpha, no JPEG
history, `i.redd.it` serves the same 1600×1200 file byte-identical, no `OP_RETURN`,
never spent, funding wallet is a custodial batcher (`version 1`, `locktime 0`,
`sequence 0xffffffff`) and therefore reveals nothing about the seed software.

**[MEASURED] Every word anyone has named has been swept.** As of today that
includes `any` and `verb`, the last two the source README lists that had never been
in a gap pool. Both negative.

---

## 3. The parity constraint — verified, and it narrows the search

**[MEASURED]** Consecutive integers *n* and *n+1* sum to 2*n*+1, always odd; the
wrap pair 12+1 = 13 is odd too. So the clock's twelve adjacent pairs yield exactly
{3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23} — **never an even number**.

Consistent with every filled entry: clock slots 3, 13, 21 are odd, and each even
slot has a count or a written number behind it — `camera` 2 (two cameras), `mask` 4
(four masked faces), `vote` 12 (the mirrored `.VS.`), `rifle` 16 (M16), `apple` 20
(the XX on Leopold's head).

The same constraint applies to the pyramid mechanism: `eye` 9 = 4+5, `pyramid` 11 =
5+6 — also adjacent sums, also odd.

| unfilled | slots | source required |
|---|---|---|
| odd | 15, 21, 23 | clock-reachable, but only three hands exist and all are spent |
| even | 6, 8, 14, 18, 22, 24 | **cannot** come from the clock or the pyramid |

Six of the nine open slots are provably outside both stated mechanisms, and the
README's twenty-one sections supply no count or number producing any of them. That
is where the mechanism inventory is genuinely incomplete.

---

## 4. Slot 10 is assumed, not derived — and it is being tested now

This is the one structural soft spot found today.

Every even slot in the table has a count behind it. **Slot 10 does not.** The
README's entire justification is:

```
| 10 | black | Black day number X |
```

That is the Russian rune sentence `чёрный день номер X` — "black day number X".
The sentence names a number, and that number is **the one glyph nobody can read**.

So the reasoning runs: black's slot comes from X → X is unreadable → 10 is a guess.
It has been load-bearing since 2020 and has never been questioned.

**[ASSUMED]** `black` at slot 10.

Nothing run so far tests it. `free-one-fixed` replaced the *word* at slot 10 with 53
candidates; `alt2` varied all 13 words simultaneously. **Neither ever moved a word
to a different slot.** Every sweep in this project has assumed the table's positions
and varied only its words.

Running now: `t18_black{6,8,14,15,18}.conf` — `black` moved to each unfilled t18
slot, slot 10 opened to the 54-word pool, 4 minutes each.

If one hits, X is that number, and the unreadable glyph gets settled by the wallet
rather than the other way round.

The t21 forms are 413 h each and are not being run.

---

## 5. Where to look next — and what not to bother with

**The bottleneck is word selection.** Not order, not derivation path, not glyph
legibility. With ~5 candidates across 24 slots the space is 5²⁴ ≈ 6×10¹⁶, and being
right about 23 of 24 words pays exactly nothing — there is no partial test.
Candidate lists cannot converge by search. Slots must be pinned by reasoning.

Ranked:

1. **A count or written number producing slot 6, 8, 14, 18, 22 or 24.** Per §3
   these cannot come from either stated mechanism, and no section of the README
   supplies one. Unexplained counts still in the artwork: 44 stars (should be 50),
   13 stripes, three Latin quotes on the pyramid. 44 and 50 exceed 24 and so cannot
   be slots directly — but digit-summing 44 → 8 lands on an open even slot, and the
   "sum of two numbers" mechanic is stated outright. Speculative; worth an eye.
2. **A word for slot 21.** The hour hand is produced by the same labelled mechanism
   that gave `moon` and `tower` at high confidence, and is the only hand with no
   word on it. Checked at four contrast settings — a plain wedge, not faint writing.
3. **Slot 11.** `pyramid` (5+6) versus the Space Needle "marks the 11". Freeing slot
   11 found no candidate fits, which suggests the conflict runs deeper than a
   two-way choice. Note the CCTV junction box bears a pyramid symbol, visually
   linking `camera` and `pyramid`.
4. **The 26 Gravity Falls symbols through the calibrated harness.** Your "not in the
   GF key" finding is currently the last visual claim in §7; segmenting `11_1.png`
   would promote it to the same evidence class as the rest. Short job.

**Do not bother with:**

- **A larger source image.** Your own linguistic-exhaustion argument settles this:
  the glyph has no key entry, occurs once, and every letter it could be also occurs
  nowhere else. A perfect scan renders the shape crisply and still cannot say which
  letter it is. The missing thing is a key, not pixels. (And no larger source
  exists — `i.redd.it` serves the same file.)
- **More words in a gap pool.** Leave-one-out swept every gap against the entire
  2048-word dictionary. No pool addition can succeed unless two or more gaps
  simultaneously need words outside it, and at that point the fixed words are the
  constraint, not the pool.
- **AI upscaling.** The signature reads `-yi-` under Lanczos and renders as a boxed
  `ER` through VanceAI at 8×. Any glyph reading from an upscale is a reading of the
  upscaler's guess.

---

## 6. Standing methodological rules

These have earned their place — eight bugs, six data defects, and several dead
hypotheses were caught by them.

1. **Check every candidate word against the wordlist before building on it.**
   `breathe`, `trusted`, `stop`, `freedom`, `hate`, `white`, `death`, `kill`, `war`,
   `money`, `buy`, `slave`, `duly`, `convicted` are all in circulation and none is a
   BIP39 word.
2. **State the indexing convention.** The repo is 1-based; BIP39's encoding is
   0-based. Three separate analyses have quoted one as the other, including mine.
3. **Validate against exact expected values, not plausible ones.** A 1.2% deviation
   is invisible to a sanity check and fatal to correctness.
4. **Branch on measured length, never word count.** 21-word mnemonics are only
   80.6% over the 128-byte HMAC threshold — one in five must *not* be pre-hashed.
5. **A numerical coincidence is not evidence** unless the image identifies both the
   operands and the operation. Of the 190 pairs among the twenty explicit numbers in
   the artwork, 158 land inside BIP39's 0–2047 range.
6. **Correlation is the wrong instrument for a compositional hypothesis.** Testing
   "is X a composite of `х` plus a stroke" by correlating against bare `х` cannot
   discriminate. Structural tests can — arm count settled `ж` at 4 against 6.
7. **A positive control must require *finding*, not verifying.** Reproducing a known
   mnemonic proves little. Blank slots and require recovery.
8. **Do not conflate [EXHAUSTED] with [TESTED].** The first is a complete space; the
   second is a finite corpus. Filing a corpus result alongside a sweep is the only
   overclaim this project has been at risk of, and you caught it.
