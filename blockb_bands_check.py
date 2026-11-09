"""Block B in the bottom bands. Executes blockb_bands_plan.md as written.

Regions, method, glyph criterion, cuts, control and decision rule are all fixed in
that file, committed before this ran (ed862df, plan blob ee814f19).
"""
import os, sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray

G = load_gray()
H, W = G.shape
CX, CY, R = 470, 937, 182
CUTS = (90, 110, 130, 150, 170, 190, 215)
GLYPH_W, GLYPH_H, PITCH, NGLYPH = 13, 20, 19.9, 14
NEED = NGLYPH * PITCH

yy, xx = np.ogrid[:H, :W]
disc = ((xx - CX) ** 2 + (yy - CY) ** 2) <= R * R

def box(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[y0:y1, x0:x1] = True; return m

REGIONS = [
    ("R1  y 1100-1138 full width",        box(0, 1100, 1600, 1138)),
    ("R1' same, minus the dial disc",     box(0, 1100, 1600, 1138) & ~disc),
    ("R2  y 1190-1200 full width",        box(0, 1190, 1600, 1200)),
    ("R3a x 0-25,    y 1138-1190",        box(0, 1138, 25, 1190)),
    ("R3b x 1555-1600, y 1138-1190",      box(1555, 1138, 1600, 1190)),
    ("CONTROL block A x 1526-1557 y 40-1015", box(1526, 40, 1557, 1015)),
]

def glyph_count(mask, cut):
    lab, k = ndimage.label((G < cut) & mask)
    if not k:
        return 0
    n = 0
    for sl, i in zip(ndimage.find_objects(lab), range(1, k + 1)):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if 6 <= w <= 33 and 10 <= h <= 40 and 40 <= int((lab[sl] == i).sum()) <= 600:
            n += 1
    return n

print("glyph-sized components per region, threshold sweep")
print(f"{'region':42s} {'px':>8s} " + "".join(f"{('<%d' % c):>6s}" for c in CUTS))
print("-" * 98)
prof = {}
for name, mask in REGIONS:
    row = [glyph_count(mask, c) for c in CUTS]
    prof[name] = row
    print(f"{name:42s} {int(mask.sum()):8d} " + "".join(f"{v:6d}" for v in row))

print(f"\ndecision rule: >= {NGLYPH} at two or more CONSECUTIVE cuts, profile not collapsing")
for name, _ in REGIONS:
    row = prof[name]
    runs = best = 0
    for v in row:
        best = best + 1 if v >= NGLYPH else 0
        runs = max(runs, best)
    hit = runs >= 2
    tag = "POSITIVE" if hit else "negative"
    if name.startswith("CONTROL"):
        tag += "   <-- control; it must be POSITIVE for the nulls to mean anything"
    print(f"  {name:42s} max consecutive cuts at >={NGLYPH}: {runs}   {tag}")

print(f"\ngeometry fixed in the plan: 14 glyphs need {NEED:.0f} px along the reading axis,"
      f" >= {GLYPH_H} px across")
for name, x0, y0, x1, y1 in (("R1", 0, 1100, 1600, 1138), ("R2", 0, 1190, 1600, 1200),
                             ("R3a", 0, 1138, 25, 1190), ("R3b", 1555, 1138, 1600, 1190)):
    w, h = x1 - x0, y1 - y0
    fits = (w >= NEED and h >= GLYPH_H) or (h >= NEED and w >= GLYPH_H)
    print(f"  {name:4s} {w:5d} x {h:4d}  horizontal line fits: {w >= NEED and h >= GLYPH_H}"
          f"   vertical: {h >= NEED and w >= GLYPH_H}   -> {'CAPABLE' if fits else 'excluded by size'}")
