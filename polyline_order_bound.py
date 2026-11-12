#!/usr/bin/env python3
"""AAM-5: the ordering bound of the yellow polyline, against this record's own objects.

A brief of 12 Nov 2026 proposed pre-registering the polyline as an ORDERING mechanism and
stated its size limit as "3 face boxes + 1 camera is FOUR points ... roughly 7% of the
order's entropy ... leaves 2.1e18 orderings untouched".

This script recomputes that limit. Three substitutions, each sourced:

  (a) the path's element count is SIX, not four -- yellow_polyline.md section 4,
      measured 3 Nov 2026: "elements on the path | 6 (4 boxes, the caption, the camera)".
      There are four face boxes (A-D), not three, and the cursive caption is on the path.
  (b) the orderable object in this record is 15!, not 21!. REPORT.md: "the order space is
      touched at 28 points out of 15! = 1,307,674,368,000" and "the order is [ASSUMED] for
      twelve of fifteen slots". The phrase is 21 words; fifteen of them are named template
      words and the rest are swept pools, so 21! is not a count of anything here.
  (c) an ordering mechanism must order DISTINCT WORDS. Of the six elements, four are the
      four masked faces -- the same four whose cardinality assigns `mask`@4 -- so they are
      four tokens of ONE word, and the caption's word `order` is in the 54-word gap pool,
      not the fifteen-word template. Two distinct template words are touched.

No solver run. Pixels are not re-measured here; the geometry is quoted from the 3 Nov pass.
"""

import os
from math import factorial, log2

HERE = os.path.dirname(os.path.abspath(__file__))
BIP39 = os.path.join(HERE, "configs", "bip39_en.txt")
ELECTRUM = os.path.join(HERE, "configs", "electrum_old_en.txt")

# AAM-1 and AAM-3: the words the brief places in, or outside, the two ledgers.
AAM_WORDS = ["war", "stop", "needle", "breathe", "map", "russia", "rifle", "rain"]
AAM_CLAIMED = {"war": ("electrum", 307), "stop": ("electrum", 76),
               "needle": ("electrum", 1305), "breathe": ("electrum", 245),
               "map": ("neither", None), "russia": ("neither", None),
               "rifle": ("bip39", None), "rain": ("bip39", None)}

# The 16-rune Younger Futhark row, long-branch, in its canonical order (AAM-1).
FUTHARK16 = ["f", "u", "th", "a", "r", "k", "h", "n", "i", "ar",
             "s", "t", "b", "m", "l", "R"]

# The six measured elements of the polyline, left to right, with the template word each
# one belongs to. yellow_polyline.md section 1 (the path) and REPORT.md section 2.17
# (`camera`@2 "a count of cameras" = two cameras; `mask`@4 "a count of masked faces" =
# four masked faces).
ELEMENTS = [("face box A", "mask", 4), ("face box B", "mask", 4),
            ("face box C", "mask", 4), ("face box D", "mask", 4),
            ("`Order and stability` caption", "order (gap pool, not the template)", None),
            ("camera lens (1 of 2 cameras)", "camera", 2)]


def load(path):
    with open(path) as fh:
        return [w.strip() for w in fh if w.strip()]


def ledgers():
    b, e = load(BIP39), load(ELECTRUM)
    print("  bip39      %d words, %d unique" % (len(b), len(set(b))))
    print("  electrum   %d words, %d unique" % (len(e), len(set(e))))
    bi = {w: i + 1 for i, w in enumerate(b)}
    ei = {w: i + 1 for i, w in enumerate(e)}
    print()
    print("  %-9s %-12s %-12s %s" % ("word", "bip39", "old electrum", "brief's claim"))
    for w in AAM_WORDS:
        where, idx = AAM_CLAIMED[w]
        got = "bip39 #%d" % bi[w] if w in bi else ("electrum #%d" % ei[w] if w in ei else "neither")
        want = where if idx is None else "%s #%d" % (where, idx)
        ok = "CONFIRMED" if (("bip39 #%d" % bi[w] if w in bi else
                             ("electrum #%d" % ei[w] if w in ei else "neither")).startswith(
                                 where if where != "neither" else "neither")) else "MISMATCH"
        if idx is not None:
            ok = "CONFIRMED" if got == "%s #%d" % (where, idx) else "MISMATCH"
        print("  %-9s %-12s %-12s %-16s %s"
              % (w, ("#%d" % bi[w]) if w in bi else "-",
                 ("#%d" % ei[w]) if w in ei else "-", want, ok))


def runes():
    i = FUTHARK16.index("ar") + 1
    print("  16-rune row: %s" % " ".join(FUTHARK16))
    print("  long-branch `ar` is ordinal %d of %d -- %s"
          % (i, len(FUTHARK16), "CONFIRMED (tenth)" if i == 10 else "MISMATCH"))


def ordering():
    f15, f21, f12 = factorial(15), factorial(21), factorial(12)
    print("  15! = %-24s log2 = %.4f bits   <- this record's order space" % (format(f15, ","), log2(f15)))
    print("  21! = %-24s log2 = %.4f bits   <- the brief's denominator" % (format(f21, ","), log2(f21)))
    print("  12! = %-24s                      <- already exhausted whole, section 2.1" % format(f12, ","))
    print()
    print("  %-34s %6s %8s  %8s %-24s" % ("mechanism size", "k!", "bits", "of 15!", "orderings left of 15!"))
    for k, lab in ((4, "the brief: 3 boxes + 1 camera"),
                   (6, "measured: elements on the path"),
                   (3, "distinct objects on the path"),
                   (2, "distinct TEMPLATE words touched")):
        bits = log2(factorial(k))
        print("  %-34s %6d %8.4f  %7.2f%% %-24s"
              % (lab, factorial(k), bits, 100 * bits / log2(f15), format(f15 // factorial(k), ",")))
    print()
    bits4 = log2(factorial(4))
    print("  the brief's own figures reproduce exactly under its own objects:")
    print("    4 points against 21!  ->  %.2f%% of the entropy, %s orderings left"
          % (100 * bits4 / log2(f21), format(f21 // factorial(4), ",")))
    print("    which is the brief's 7% and its 2.1e18. The arithmetic is right;")
    print("    the objects are not this record's.")


def elements():
    print("  %-32s %s" % ("element on the path", "template word it belongs to"))
    for name, word, slot in ELEMENTS:
        print("  %-32s %s%s" % (name, word, "" if slot is None else "@%d" % slot))
    words = sorted({w for _, w, s in ELEMENTS if s is not None})
    print()
    print("  distinct template words touched: %d  %s" % (len(words), words))
    print("  the four boxes are four TOKENS of one word (`mask`@4 is a count of them),")
    print("  so their traversal order is the order of four copies of one word: no ordering.")
    print()
    print("  and the two words it does touch are ALREADY ordered by the template:")
    print("    camera@2 precedes mask@4.")
    print("  the path traversed A->camera gives mask before camera, which CONTRADICTS it;")
    print("  traversed camera->A it AGREES. yellow_polyline.md section 6: \"The reading")
    print("  order (A -> camera) is a convention. The device has no arrowhead.\" -- so the")
    print("  one bit the mechanism could carry is unsigned, and either verdict is")
    print("  available by choosing a direction the measurement does not fix.")


def twelve_word_scope():
    """AAO-1: why an ordering mechanism is worth something only for the fifteen-word template.

    Section 2.1 enumerated the 12-word clock set over ALL 12! orderings, so for twelve words
    the order is not assumed -- it is exhausted. The ratio of orderings is NOT a ratio of work,
    and this prints both so a later reader cannot read one as the other.
    """
    f12, f15 = factorial(12), factorial(15)
    T21 = 1363720121280          # candidates in one ordering of the t21 template, six gaps swept
    valid = f12 // 16            # 1 in 16 orderings carry a valid BIP39 checksum
    derivs12 = valid * 12        # section 2.1: 12 passphrases
    derivs_one = T21 // 128      # 21 words: derivations = candidates / 128, and it floors
    print("  12! = %-20s SWEPT WHOLE  (section 2.1: every rotation, both" % format(f12, ","))
    print("                             directions, every reflection)")
    print("  15! = %-20s ASSUMED      (section 2.13: twelve of fifteen slots)" % format(f15, ","))
    print("  15! / 12! = %d  (exact: 15 x 14 x 13)" % (f15 // f12))
    print()
    print("  BUT THE 2730x IS A RATIO OF ORDERINGS, NOT OF WORK:")
    print("    the whole 12-word order space cost %s derivations" % format(derivs12, ","))
    print("      = %s orderings / 16 checksum-valid x 12 passphrases" % format(f12, ","))
    print("      and section 2.1 reports 359 million -- reconstructed exactly")
    print("    ONE ordering of the current template costs %s candidates" % format(T21, ","))
    print("      = %s derivations (candidates/128, 21 words, floors)" % format(derivs_one, ","))
    print("    so one ordering of the fifteen is %.2fx the ENTIRE twelve-word sweep"
          % (derivs_one / derivs12))
    print("    and the full 15! sweep is %.3e candidates -- the 5.5e9 GPU-years." % (f15 * T21))
    print("    (printed in scientific notation and never re-rendered as digits, per section 10)")


if __name__ == "__main__":
    for title, fn in (("1. THE TWO LEDGERS (AAM-1, AAM-3)", ledgers),
                      ("2. THE RUNE ORDINAL (AAM-1)", runes),
                      ("3. THE ORDERING SPACE (AAM-5)", ordering),
                      ("4. WHAT THE PATH ACTUALLY TOUCHES (AAM-5)", elements),
                      ("5. THE 12-WORD SCOPE (AAO-1)", twelve_word_scope)):
        print("=" * 78)
        print(title)
        print("=" * 78)
        fn()
        print()
