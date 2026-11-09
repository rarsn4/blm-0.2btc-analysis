"""Z-1 and Z-2: what R1's components actually ARE, and what contrast the test can see.

Z-2  identify R1's 13 components at ink<170 by centroid, against catalogued elements.
Z-1  sensitivity floor: attenuate block A's OWN column to the vial-19 and rifle-16
     contrast levels and re-run the identical glyph count. If the attenuated control
     reads near-zero, the Y-1 negative excludes only a block B drawn at block A's
     contrast, and says nothing about a faint one.
"""
import os, sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray

G = load_gray()
H, W = G.shape
CUTS = (90, 110, 130, 150, 170, 190, 215)

def glyph_comps(img, mask, cut):
    lab, k = ndimage.label((img < cut) & mask)
    out = []
    if not k:
        return out
    for sl, i in zip(ndimage.find_objects(lab), range(1, k + 1)):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        n = int((lab[sl] == i).sum())
        if 6 <= w <= 33 and 10 <= h <= 40 and 40 <= n <= 600:
            out.append(((sl[1].start + sl[1].stop) / 2.0,
                        (sl[0].start + sl[0].stop) / 2.0, w, h, n))
    return out

# ---------------------------------------------------------------- Z-2
print("=== Z-2. what R1's peak actually is ===")
R1 = np.zeros((H, W), bool); R1[1100:1138] = True
KNOWN = [("ambigram date", 1012, 1098, 1098, 1122),
         ("seal scroll",    470, 1040,  860, 1135)]
comps = glyph_comps(G, R1, 170)
print(f"R1 at ink<170: {len(comps)} glyph-sized components")
print(f"{'#':>3s} {'centroid x':>11s} {'y':>7s} {'w':>4s} {'h':>4s} {'px':>5s}  accounted for by")
acc = {n: 0 for n, *_ in KNOWN}
unacc = []
for j, (cx, cy, w, h, n) in enumerate(sorted(comps), 1):
    where = [nm for nm, x0, y0, x1, y1 in KNOWN if x0 <= cx <= x1 and y0 <= cy <= y1]
    for nm in where:
        acc[nm] += 1
    if not where:
        unacc.append((cx, cy))
    print(f"{j:3d} {cx:11.1f} {cy:7.1f} {w:4d} {h:4d} {n:5d}  "
          f"{', '.join(where) if where else '-- not in either box --'}")
print()
for nm, x0, y0, x1, y1 in KNOWN:
    print(f"  inside {nm:14s} (x {x0}-{x1}, y {y0}-{y1}): {acc[nm]}")
print(f"  in neither box: {len(unacc)}")
if unacc:
    print("  their centroids:", ", ".join(f"({x:.0f},{y:.0f})" for x, y in unacc))

# ---------------------------------------------------------------- Z-1
print("\n=== Z-1. what contrast the test can see ===")
CTRL = np.zeros((H, W), bool); CTRL[40:1015, 1526:1557] = True
sub = G[40:1015, 1526:1557]
bg, dk = float(sub.max()), float(sub.min())
print(f"block A column: background {bg:.0f}, darkest {dk:.0f}, {bg-dk:.0f} levels (full pen)")
print("attenuated copies of THAT SAME COLUMN, same method, same cuts:\n")
print(f"{'contrast of the copy':34s} " + "".join(f"{('<%d'%c):>6s}" for c in CUTS))
LEVELS = [("as drawn, 254 levels (block A)", bg - dk),
          ("circled mark, 146 levels",       146.0),
          ("vial-19 level, 110 levels",      110.0),
          ("80 levels",                       80.0),
          ("60 levels",                       60.0),
          ("45 levels",                       45.0),
          ("35 levels",                       35.0),
          ("25 levels",                       25.0),
          ("rifle-16 level, 19 levels",       19.0)]
for label, levels in LEVELS:
    att = G.copy()
    scaled = bg - (bg - sub) * (levels / (bg - dk))
    att[40:1015, 1526:1557] = scaled
    row = [len(glyph_comps(att, CTRL, c)) for c in CUTS]
    seen = max(row) >= 14
    print(f"{label:34s} " + "".join(f"{v:6d}" for v in row)
          + ("   SEEN" if seen else "   BLIND"))
print("\n(42 glyphs are known to be present in every row above: the ONLY thing changed")
print(" is ink depth. A row of near-zeros is the test failing to see them.)")

print()
print("The floor has an exact cause: the sweep's top cut is <215 and this column's")
print("background is 254, so the test can only see ink that reaches 254-215 = 39 levels")
print("deep. 45 levels -> darkest 209, visible. 35 levels -> darkest 219, invisible.")
print("The rifle-receiver mark in this same image is 19 levels (REPORT 6 item 6), so a")
print("block drawn below this floor is not a hypothetical.")
print()
print("R1 observed, for comparison:   " + "".join(f"{v:6d}" for v in (8,8,7,7,13,11,5)))
