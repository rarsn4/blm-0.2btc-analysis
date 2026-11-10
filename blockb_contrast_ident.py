"""POST-HOC, beyond blockb_contrast_plan.md, whose own rule returned VOID.

The published bands negative rests on IDENTIFYING all 13 of R1's components as
catalogued features, not only on 13 < 14. That standard does not depend on a count
threshold, so it survives the void. Apply it to the components the contrast-targeted
detector finds at each depth, using the SAME catalogued boxes the old pass used.
"""
import numpy as np, sys
from scipy import ndimage
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray
G = load_gray(); H, W = G.shape
WIN = 41; DEPTHS = (10, 15, 19, 25, 30, 39)
CX, CY, R = 470, 937, 182
yy, xx = np.ogrid[:H, :W]
disc = ((xx-CX)**2 + (yy-CY)**2) <= R*R
R1 = np.zeros((H,W), bool); R1[1100:1138, 0:1600] = True

BOXES = [("ambigram date", 1012, 1098, 1098, 1122),
         ("seal scroll",    470, 1040,  860, 1135),
         ("left frame line", 37, 1090,   46, 1138)]

B = ndimage.median_filter(G, size=WIN)
D = B - G
print("R1 COMPONENTS AT EACH DEPTH, IDENTIFIED AGAINST THE CATALOGUED BOXES")
print("(post-hoc; the pre-registered count rule returned VOID at every depth)\n")
for d in DEPTHS:
    lab, k = ndimage.label((D >= d) & R1)
    rows = []
    for sl, i in zip(ndimage.find_objects(lab), range(1, k+1)):
        h = sl[0].stop-sl[0].start; w = sl[1].stop-sl[1].start
        ink = int((lab[sl]==i).sum())
        if not (6<=w<=33 and 10<=h<=40 and 40<=ink<=600): continue
        cy = (sl[0].start+sl[0].stop)/2; cx = (sl[1].start+sl[1].stop)/2
        who = next((n for n,x0,y0,x1,y1 in BOXES if x0<=cx<=x1 and y0<=cy<=y1), None)
        rows.append((cx, cy, w, h, ink, who, bool(disc[int(cy), int(cx)])))
    named = sum(1 for r in rows if r[5])
    unk = [r for r in rows if not r[5]]
    print(f"  depth >= {d:2d}: {len(rows):2d} components   {named:2d} catalogued   "
          f"{len(unk):2d} NOT in any catalogued box")
    for cx, cy, w, h, ink, _, ind in unk:
        print(f"        ({cx:6.1f},{cy:6.1f})  {w:2d}x{h:2d}  ink {ink:3d}"
              f"  {'inside dial disc' if ind else 'outside the disc'}")
