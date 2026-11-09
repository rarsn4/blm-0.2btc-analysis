"""Block B at "the bottom": is there an unsearched region that could hold 14 glyphs?

Every constraint is a measurement already in the tree:
  - the only block-B search so far: disc, centre (470,937) r 182   (REPORT 2.17)
  - whitepaper caption  box (25, 1138, 1040, 28)                   (census_crops DRAWN)
  - Latin line          box (1025, 1140, 530, 50)                  (census_crops DRAWN)
  - block A: 42 glyphs, 13x20 px each, pitch 19.9 px/run           (REPORT 7.4, runelib)
  - the transcriber's own wording, "runes at the bottom"           (gpzlri7, gpzromb)

Part 1  how much of the bottom third the dial search actually covered.
Part 2  the bottom EDGE strip: is there room beside the two text blocks?
Part 3  a glyph-component search over the bottom third outside the disc, with
        block A's own column as the positive control, then a collinear-at-pitch
        test for a 14-glyph line.
"""
import os, sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray

G = load_gray()
H, W = G.shape
CX, CY, R = 470, 937, 182
THIRD = H // 3 * 2
BOXES = [("whitepaper caption", 25, 1138, 1040, 28),
         ("Latin line",        1025, 1140, 530, 50)]
GW, GH, PITCH, NGLYPH = 13, 20, 19.9, 14
NEED = NGLYPH * PITCH
CUTS = (130, 180, 215)

yy, xx = np.ogrid[:H, :W]
disc = ((xx - CX) ** 2 + (yy - CY) ** 2) <= R * R

print("=== 1. what the dial search covered ===")
bt = slice(THIRD, H)
print(f"bottom third      y {THIRD}-{H}, {(H-THIRD)*W:,} px")
print(f"disc              x {CX-R}-{CX+R}  y {CY-R}-{CY+R}")
print(f"  rows touched    {disc[bt].any(axis=1).sum()} of {H-THIRD}")
print(f"  cols touched    {disc[bt].any(axis=0).sum()} of {W}")
print(f"  AREA covered    {disc[bt].sum():,} px = {100*disc[bt].mean():.1f}% of the bottom third")
print(f"  so UNSEARCHED   {(~disc[bt]).sum():,} px = {100*(~disc[bt]).mean():.1f}%")

print("\n=== 2. the bottom edge strip ===")
for n, x, y, w, h in BOXES:
    print(f"  {n:20s} x {x}-{x+w}  y {y}-{y+h}")
xs = min(b[1] for b in BOXES); xe = max(b[1] + b[3] for b in BOXES)
print(f"  union spans x {xs}-{xe} of {W}: free {xs} px left, {W-xe} px right")
print(f"  {NGLYPH} glyphs at {PITCH} px pitch need {NEED:.0f} px -> neither gap is close")

print("\n=== 3. glyph-component search ===")
def glyphs(region_mask, cut):
    """components whose size and bbox are glyph-like, as block A's are."""
    lab, k = ndimage.label((G < cut) & region_mask)
    if not k:
        return []
    out = []
    for sl, i in zip(ndimage.find_objects(lab), range(1, k + 1)):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        n = int((lab[sl] == i).sum())
        if 0.5 * GW <= w <= 2.5 * GW and 0.5 * GH <= h <= 2.0 * GH and 40 <= n <= 600:
            out.append(((sl[1].start + sl[1].stop) / 2, (sl[0].start + sl[0].stop) / 2))
    return out

control = np.zeros((H, W), bool); control[40:1015, 1526:1557] = True
search  = np.zeros((H, W), bool); search[bt] = True; search &= ~disc
for _, x, y, w, h in BOXES:
    search[y:y + h, x:x + w] = False

def pitch_runs(pts, axis):
    """longest run of >=NGLYPH points evenly spaced at ~PITCH along one axis."""
    best = 0
    key = (lambda p: p[1]) if axis == 'y' else (lambda p: p[0])
    other = (lambda p: p[0]) if axis == 'y' else (lambda p: p[1])
    pts = sorted(pts, key=key)
    for i, p in enumerate(pts):
        lane = [q for q in pts if abs(other(q) - other(p)) <= GW]
        lane.sort(key=key)
        run = 1
        for a, b in zip(lane, lane[1:]):
            run = run + 1 if abs((key(b) - key(a)) - PITCH) <= 0.35 * PITCH else 1
            best = max(best, run)
    return best

for name, mask in (("block A column (POSITIVE CONTROL)", control),
                   ("bottom third outside the disc", search)):
    print(f"  {name}")
    for cut in CUTS:
        pts = glyphs(mask, cut)
        v = pitch_runs(pts, 'y'); hh = pitch_runs(pts, 'x')
        print(f"    ink<{cut:3d}: glyph-like components {len(pts):4d}   "
              f"longest run at {PITCH} px pitch: vertical {v:3d}  horizontal {hh:3d}"
              f"{'   <-- 14+ FOUND' if max(v, hh) >= NGLYPH else ''}")
