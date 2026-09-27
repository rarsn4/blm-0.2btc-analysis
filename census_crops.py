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

import numpy as np
from PIL import Image

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
    ("Esse quam niger es, sic dixit caccobus ollae", 36, "-", [(1030, 1145, 520, 45, 2, 0, 1, 99)]),
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
