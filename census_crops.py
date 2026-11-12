"""Task 1: letter-substitution census -- the views it was judged from.

The census itself is a visual judgment (is each letter a letterform, or an
object standing in for one?), so no script can compute it. What this script
makes reproducible is the evidence: it writes every nearest-neighbour crop the
census was read from into ./census_crops/, and prints the element table with
the letter counts and the finding, so anyone can re-inspect exactly what was
inspected.

Criterion: a letter counts as drawn-as-object only if a depicted object
occupies that letter's position in a word. Outlined, textured, micrography-
filled and mirror-written letterforms count as written.
Nearest-neighbour scaling only: every output pixel is a source pixel.
"""
import os
import sys

import numpy as np
from PIL import Image

# AAI-1: without this the script cannot run under `python3 -I`, which drops the script's own
# directory from sys.path, and `from imgio import load_gray` fails with ModuleNotFoundError.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray

G = load_gray()
OUT = "census_crops"
os.makedirs(OUT, exist_ok=True)

# (element, letters examined, drawn as object, crops: (x, y, w, h, scale, rotate, lo_pct, hi_pct))
ELEMENTS = [
    ("STOP (Liberty)", 4, "O -> clenched fist", [(0, 440, 190, 100, 4, 0, 1, 99)]),
    ("FIND THE SEED PHRASE", 17, "-", [(495, 15, 400, 390, 1, 0, 1, 99), (530, 25, 340, 145, 2, 0, 1, 97)]),
    ("IN THE THIS PICTURE", 16, "-", [(510, 345, 420, 65, 2, 0, 1, 97)]),
    ("WELCOME TO THE / BRAVE / NEW WORLD", 25, "-",
     [(515, 378, 440, 82, 2, 0, 1, 99), (420, 395, 660, 305, 1, 0, 1, 99),
      (420, 578, 330, 120, 2, 0, 1, 99), (740, 578, 340, 120, 2, 0, 1, 99)]),
    ("BLACK LIVES MATTER ... NOT ONE MORE", 73, "-",
     [(1100, 80, 240, 360, 2, -90, 1, 99), (1180, 40, 80, 60, 4, 0, 1, 99)]),
    ("I can't BREATHE", 12, "-", [(900, 240, 300, 180, 2, 0, 1, 99)]),
    ("BLM (card)", 3, "-", [(250, 715, 80, 75, 8, 0, 2, 98)]),
    ("FUCK THIS SHIT", 12, "- (the I of SHIT is written)", [(1290, 770, 210, 245, 4, 0, 2, 98)]),
    (".VS.", 2, "-", [(1000, 1045, 100, 80, 5, 0, 1, 99)]),
    ("Seal ring + scroll", 37, "-", [(470, 770, 390, 150, 2, 0, 1, 99), (470, 1000, 390, 130, 2, 0, 1, 99)]),
    ("Clock hands TOWER, MOON", 9, "-", [(330, 790, 170, 120, 3, 0, 1, 99)]),
    ("Address (letters of 34 chars)", 31, "-",
     [(40, 560, 44, 290, 3, -90, 1, 99), (40, 845, 44, 290, 3, -90, 1, 99)]),
    ("ONLY real BITCOIN", 15, "-", [(110, 1030, 170, 50, 4, 0, 1, 99)]),
    ("PAY FOR THE FUTURE. / THIS IS THE FIRST PREDICTION.", 39, "-", [(70, 780, 120, 330, 3, -90, 5, 95)]),
    ("Esse quam niger es, sic dixit caccabus ollae", 36, "-", [(1030, 1145, 520, 45, 2, 0, 1, 99)]),
]
# The four long canvas texts, written out here INDEPENDENTLY of brain_image_corpus.py.
# That independence is the point: corpus_gate.py reconciles these two statements of what
# is painted, and a disagreement is a finding rather than a merge conflict. Whitespace is
# collapsed by the corpus's own variants(), so the line breaks here are for reading only.
BLOCK_TEXT = ("BLACK LIVES MATTER NO JUSTICE NO PEACE END POLICE BRUTALITY "
              "STOP KILLING US NOT ONE MORE")

AMENDMENT_TEXT = ("Section 1. "
                  "Neither slavery nor involuntary servitude, except as a punishment "
                  "for crime whereof the party shall have been duly convicted shall exist "
                  "within the United States, or any place subject to their jurisdiction.")

CAPTION_TEXT = ("in which they were received. The payee needs proof that at the time of each "
                "transaction, the majority of nodes agreed it was the first received")

MICRO_TEXT = ("common solution is to introdue cent ral au thority, or mini.that "
              "checks every tran sacti ons. For double spen ding. After")

# ---------------------------------------------------------------------------- DRAWN
# [ADDED 2026-11-02] The canvas census, machine-readable: every string this project has
# measured as PAINTED ON THE IMAGE, with its box and where the measurement lives.
#
# ELEMENTS above is a letter-substitution census -- its first field is a human label
# ("BLACK LIVES MATTER ... NOT ONE MORE", "WELCOME TO THE / BRAVE / NEW WORLD"), not a
# verbatim string -- so it cannot be reconciled against a hash corpus by machine. DRAWN
# can. It exists because `caccobus` was hashed for five weeks, and because 05.25.20,
# 11.03.20, UBI BENE IBI PATRIA, BREATHE and CHR were each measured and written down
# elsewhere in this tree and never reached the brainwallet corpus at all. See
# REPORT 1.8 and letterform_audit.md.
#
# `corpus_gate.py` REFUSES to let the brainwallet queue start if any string here is
# missing from, or differs from, what brain_image_corpus.py generates.
#
# status:
#   measured      read off the master image, native pixels or an unambiguous glyph
#   magnified     read under magnification only; honest but below REPORT 9's bar
#   indeterminate a reading that may be right and may not; carried, never substituted
#   inferred      argued from measurement rather than read directly
#   cipher        a rune decode, not a Latin letterform -- a different measurement
#
# (label, as-drawn string, (x, y, w, h), status, where the measurement lives)
DRAWN = [
    ("STOP (Liberty, O -> fist)", "STOP", (0, 440, 190, 100), "measured", "census_crops ELEMENTS 1"),
    ("headline", "FIND THE SEED PHRASE IN THE THIS PICTURE", (495, 15, 435, 395), "measured", "census_crops ELEMENTS 2,3"),
    ("statue base caption", "Order and stability", (640, 70, 380, 50), "measured", "letterform_audit 4"),
    ("COVID sign", "COVID 19 IS A HOAX 5G IS THE KILLER", (30, 330, 150, 95), "measured", "letterform_audit 1.1"),
    ("hoodie line", "I can't BREATHE", (900, 240, 300, 180), "measured", "census_crops ELEMENTS 6"),
    ("hoodie date", "05.25.20", (992, 370, 77, 18), "measured", "premise_audit.md; chronology.py 1"),
    ("BLM protest block", BLOCK_TEXT, (1095, 75, 250, 370), "measured", "census_crops ELEMENTS 5"),
    ("bust neck band", "BREATHE", (1355, 528, 75, 17), "measured", "three_object_measurement.md 3"),
    ("BRAVE NEW WORLD headline", "WELCOME TO THE BRAVE NEW WORLD", (420, 390, 660, 310), "measured", "census_crops ELEMENTS 4"),
    ("tablet", "BLM", (248, 712, 86, 80), "measured", "census_crops ELEMENTS 7"),
    ("pedestal spray", "FUCK THIS SHIT", (1290, 770, 210, 245), "measured", "census_crops ELEMENTS 8"),
    ("ambigram", ".VS.", (1021, 1055, 68, 33), "measured", "census_crops ELEMENTS 9"),
    ("ambigram, interpunct reading", "\u00b7VS\u00b7", (1021, 1055, 68, 33), "indeterminate", "letterform_audit 2"),
    ("date under the ambigram", "11.03.20", (1012, 1098, 86, 24), "measured", "slot20.py:129"),
    ("seal ring (mirror)", "RERUM COGNOSCERE CAUSAS", (470, 770, 390, 160), "measured", "seal_ring.py"),
    ("seal scroll (mirror)", "UBI BENE IBI PATRIA", (470, 1040, 390, 95), "measured", "seal_ring.py:13"),
    ("pyramid base (mirror)", "FIAT JUSTITIA ET PEREAT MUNDUS", (552, 1026, 190, 20), "measured", "census_crops SCREENED 3"),
    ("clock hand (minute)", "TOWER", (325, 785, 180, 125), "measured", "census_crops ELEMENTS 11"),
    ("clock hand (second)", "MOON", (325, 785, 180, 125), "measured", "census_crops ELEMENTS 11"),
    ("vial label", "CVD19", (130, 230, 50, 60), "measured", "census_crops SCREENED 4"),
    ("left-edge address", "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ", (38, 555, 46, 585), "measured", "census_crops ELEMENTS 12"),
    ("statue plinth band", "ONLY real BITCOIN", (95, 1045, 140, 25), "measured", "census_crops ELEMENTS 13"),
    ("plinth caption line 1", "PAY FOR THE FUTURE.", (76, 782, 13, 195), "measured", "census_crops ELEMENTS 14"),
    ("plinth caption line 1, Roman-V reading", "PAY FOR THE FVTURE.", (76, 782, 13, 195), "indeterminate", "letterform_audit 2"),
    ("plinth caption line 2", "THIS IS THE FIRST PREDICTION.", (93, 782, 15, 215), "measured", "census_crops ELEMENTS 14"),
    ("bottom Latin line", "Esse quam niger es, sic dixit caccabus ollae", (1025, 1140, 530, 50), "measured", "census_crops ELEMENTS 15; letterform_audit 1.2"),
    ("date beside Liberty", "1865-202...?", (205, 615, 170, 110), "measured", "letterform_audit 1.6"),
    ("bottom-right monogram", "CHR", (1520, 1125, 70, 40), "inferred", "REPORT 9"),
    ("13th Amendment copy", AMENDMENT_TEXT, (1296, 775, 205, 150), "magnified", "letterform_audit 1.3"),
    ("bottom whitepaper caption", CAPTION_TEXT, (25, 1138, 1040, 28), "magnified", "letterform_audit 1.5"),
    ("E-of-BRAVE micro-text", MICRO_TEXT, (885, 468, 90, 117), "measured", "letterform_audit 1.4"),
    # [BOXES CORRECTED 9 Nov 2026] All four 'cipher' boxes were wrong. Measured on the
    # master image at its pinned sha256. The STRINGS ARE UNCHANGED: corpus_gate.py matches
    # on the string and never on the box, so no gate verdict moves -- but its cache keys on
    # file content, so this edit forces it to re-prove.
    #
    # What was wrong. Three of the four shared (1560, 40, 40, 1120) = x 1560-1600. That is
    # the FRAME LINE: x 1560-1564 each carry 1,124 ink px, the full height of the band, and
    # x 1568-1599 is blank margin. The glyphs are at x 1529-1555. runelib.py's
    # XA,XB = 1526,1557 was right all along and this list silently disagreed with it.
    # 'clock caption (rune)' pointed at (330, 790, 170, 120), which holds 95 ink px at 0.5%
    # density across 13 of its 170 columns -- nothing is there.
    #
    # Only ONE of the four can be given a measured box with its text attributed.
    ("right-edge line (rune)", "\u0437\u0434\u0435\u0441\u044c \u0437\u0430\u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u044b \u0431\u0438\u0442\u043a\u043e\u0438\u043d\u044b \u043d\u0430 \u0447\u0451\u0440\u043d\u044b\u0439 \u0434\u0435\u043d\u044c \u043d\u043e\u043c\u0435\u0440", (1526, 40, 31, 975), "cipher", "REPORT 7; box measured 9 Nov: 42 glyphs + 7 three-dot separators"),
    # [CORRECTED AGAIN 9 Nov 2026 -- the entry committed in 49e7c2a was WRONG, and it was
    # mine.] That entry gave these two fragments the box (50, 627, 36, 484) and called it
    # "a SECOND rune column ... 29 glyph-sized runs whose ink and height match the right
    # column's profile". A threshold sweep disproves it. Over x 50-86, full height:
    #
    #     ink<     130   150   180   200   215        right column, same sweep
    #     runs      48    44    24     2     1          49    50    49    38    25
    #     glyphs    33    33    14     1     1          42    42    41    32    20
    #     seps       3     2     3     0     0           7     8     7     5     4
    #     pitch   23.7  25.9  47.4   577  1200        19.9  19.6  20.0  25.8  39.2
    #
    # The right column is STABLE across 50 grey levels; the left band COLLAPSES to a single
    # run. Three more measurements say why: paper fraction (pixels >200) is 10.2% there
    # against 57.2% in the right column; there is NO x-margin, ink being continuous from
    # x 10-14 to x 139 at every threshold, where the right column has zero ink at
    # x 1568-1599; and x 40-43 is a solid frame line, ~1,137 of 1,200 rows.
    #
    # So the 29 runs were GAPS IN ARTWORK, not glyphs separated by whitespace. A
    # glyph-sized-component scan finds glyph-sized blobs in any textured region; that is
    # what happened. Both fragments are therefore [BOX UNVERIFIED: not located], the same
    # treatment as the clock caption, and the box below is the band searched.
    ("rune fragment [BOX UNVERIFIED: not located]", "\u042f \u043d\u0430\u0434\u0435\u044e\u0441\u044c", (50, 0, 36, 1200), "cipher", "REPORT 7; search region, not a location -- see the 9 Nov note"),
    ("rune fragment [BOX UNVERIFIED: not located]", "\u0431\u0443\u0434\u0443\u0442 \u043f\u0440\u0438\u0441\u044b\u043b\u0430\u0442\u044c", (50, 0, 36, 1200), "cipher", "REPORT 7; search region, not a location -- see the 9 Nov note"),
    # The clock caption was SEARCHED FOR AND NOT FOUND. The box is the region searched, not
    # a location. Three boxes around the dial (centre (470,937), radius ~182) at thresholds
    # <130/<180/<215 give ZERO glyph-sized components (ink 80-260 px, box 10-26 px) and no
    # line of ~14 similar small marks; the small components that do exist are scattered over
    # x 295-692, y 760-1123 and are dial marks and numerals. This does not say the block is
    # absent -- REPORT 7.3 transcribes 14 glyphs for it -- it says the recorded box is wrong
    # and that a defined search did not relocate it.
    ("clock caption (rune) [BOX UNVERIFIED: not located]", "\u0421\u0443\u043c\u043c\u0430 \u0434\u0432\u0443\u0445 \u0447\u0438\u0441\u0435\u043b", (250, 760, 450, 440), "cipher", "REPORT 7; search region, not a location"),
]

SCREENED = [  # ~5-8 px text: a letter-sized object would be unidentifiable; screened as blocks only
    ("bottom caption (whitepaper, cursive)", "~115", [(30, 1140, 1020, 30, 2, 0, 1, 99)]),
    ("13th Amendment copy", "~179", [(1296, 780, 200, 140, 4, 0, 1, 99)]),
    ("pyramid base FIAT JUSTITIA ET PEREAT MUNDUS", "26", [(470, 1000, 390, 130, 2, 0, 1, 99)]),
    ("vial CVD19", "3", [(135, 235, 40, 55, 8, 0, 1, 99)]),
]


def crop(tag, i, x, y, w, h, k, rot, lo_p, hi_p):
    sub = G[y:y + h, x:x + w]
    lo, hi = np.percentile(sub, lo_p), np.percentile(sub, hi_p)
    v = np.clip((sub - lo) / max(1e-6, hi - lo) * 255, 0, 255).astype(np.uint8)
    im = Image.fromarray(v).resize((w * k, h * k), Image.NEAREST)
    if rot:
        im = im.rotate(rot, Image.NEAREST, expand=True, fillcolor=255)
    name = "%s_%d.png" % (tag, i)
    im.save(os.path.join(OUT, name))
    return name


total = 0
print("%-52s %7s  %s" % ("element (examined glyph by glyph)", "letters", "drawn as object"))
for n, (el, count, found, crops) in enumerate(ELEMENTS, 1):
    names = [crop("e%02d" % n, i, *c) for i, c in enumerate(crops)]
    total += count
    print("%-52s %7d  %s   [%s]" % (el, count, found, ", ".join(names)))
print("%-52s %7d  1" % ("TOTAL", total))
print("\nscreened as blocks only:")
for n, (el, count, crops) in enumerate(SCREENED, 1):
    names = [crop("s%02d" % n, i, *c) for i, c in enumerate(crops)]
    print("   %-50s %6s letters   [%s]" % (el, count, ", ".join(names)))
