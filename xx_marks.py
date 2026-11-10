"""OO-1. A pair of X marks inside a circular element? Executes xx_marks_plan.md.

Plan committed a6ab39a, blob eb6ef14b4d3ae7e6cc07226f6ae7dfbda487c5c9, BEFORE any
pixel was read for this item.

skimage is NOT installed on this machine, so tablet_measure.py and rune_x_check.py
cannot run here. A Zhang-Suen thinning is implemented below and is VOID unless it
reproduces glyph X's published figures (plan sec.3).
"""
import os, sys
import numpy as np
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray

G = load_gray()
H, W = G.shape
EIGHT = np.ones((3, 3), bool)
CUTS = (90, 110, 125, 140, 155, 170, 185)

# ------------------------------------------------------------------ Zhang-Suen
def thin(img):
    I = img.astype(np.uint8).copy()
    def nb(a):
        return [np.roll(np.roll(a, dy, 0), dx, 1) for dy, dx in
                ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1))]
    while True:
        changed = False
        for step in (0, 1):
            P = nb(I)
            B = sum(p.astype(int) for p in P)
            A = sum(((P[k] == 0) & (P[(k+1) % 8] == 1)).astype(int) for k in range(8))
            c1 = (I == 1) & (B >= 2) & (B <= 6) & (A == 1)
            if step == 0:
                cond = c1 & ((P[0]==0)|(P[2]==0)|(P[4]==0)) & ((P[2]==0)|(P[4]==0)|(P[6]==0))
            else:
                cond = c1 & ((P[0]==0)|(P[2]==0)|(P[6]==0)) & ((P[0]==0)|(P[4]==0)|(P[6]==0))
            if cond.any():
                I[cond] = 0; changed = True
        if not changed:
            return I.astype(bool)

def skel_stats(mask):
    sk = thin(mask)
    n = ndi.convolve(sk.astype(int), np.array([[1,1,1],[1,0,1],[1,1,1]]), mode="constant")
    ends = sk & (n == 1)
    jmask = sk & (n >= 3)
    jl, nj = ndi.label(jmask, EIGHT)
    # remove the junction PIXELS only. Dilating here would delete the arms' first
    # pixel as well, which both empties the degree count and shortens every arm.
    arms_mask = sk & ~jmask
    al, na = ndi.label(arms_mask, EIGHT)
    lens = []
    if nj:
        jc = ndi.center_of_mass(jmask, jl, range(1, nj + 1))
        for i in range(1, na + 1):
            py, px = np.nonzero(al == i)
            lens.append(min(np.hypot(py - cy, px - cx).max() for cy, cx in jc))
    degs = []
    for i in range(1, nj + 1):
        jd = ndi.binary_dilation(jl == i, EIGHT)
        degs.append(len(set(al[jd & arms_mask].tolist()) - {0}))
    return sk, int(ends.sum()), nj, degs, sorted(lens, reverse=True), na

def main_comp(mask):
    lab, n = ndi.label(mask, EIGHT)
    return (lab == (np.bincount(lab.ravel())[1:].argmax() + 1)) if n else mask

def is_X(ne, nj, degs):
    """plan sec.3: 4 endpoints, exactly one 4-way junction."""
    return ne == 4 and nj == 1 and degs == [4]

print("OO-1  A PAIR OF X MARKS INSIDE A CIRCULAR ELEMENT?")
print("=" * 86)

# ----------------------------------------------- instrument validation on glyph X
print("\n--- INSTRUMENT VALIDATION (plan sec.3): glyph X, published 92 px / 4 endpoints /")
print("    1 four-way junction / arms 9.5, 7.6, 6.0, 4.8 ---")
Xw = G[38:56, 1530:1561]
xm = np.rot90(main_comp(Xw < 110), k=-1)
sk, ne, nj, degs, lens, na = skel_stats(xm)
print(f"  ink px {int(xm.sum())}   endpoints {ne}   junctions {nj} degrees {degs}   arms {na}")
print(f"  arm lengths {[round(v,1) for v in lens]}")
ok = int(xm.sum()) == 92 and ne == 4 and nj == 1 and degs == [4]
print(f"  reproduces the published topology: {'YES' if ok else 'NO'}")
if not ok:
    print("\n  INSTRUMENT VOID -- reporting NO POWER and stopping, per plan sec.3.")
    sys.exit(0)
print("  stability across cutoffs:")
for c in CUTS:
    m = np.rot90(main_comp(Xw < c), k=-1)
    if not m.sum(): print(f"    t={c:3d}  no ink"); continue
    _, e2, j2, d2, l2, _ = skel_stats(m)
    print(f"    t={c:3d}  px {int(m.sum()):3d}  endpoints {e2}  junctions {j2} {d2}"
          f"  X-signature {'YES' if is_X(e2,j2,d2) else 'no'}")

# ----------------------------------------------- regions
yy, xx = np.ogrid[:H, :W]
def disc(cx, cy, r): return ((xx-cx)**2 + (yy-cy)**2) <= r*r
def box(x0,y0,x1,y1):
    m = np.zeros((H,W), bool); m[max(0,y0):min(H,y1), max(0,x0):min(W,x1)] = True; return m

C1 = disc(646.25, 947.0, 192.5)          # Great Seal disc, E12 box -> inscribed circle
C2 = disc(470, 937, 182)                 # clock dial
REGIONS = [("C1 Great Seal disc", C1), ("C2 clock dial", C2)]
CONTROLS = [("ctrl (900,150)",  box(900,150,1285,535)),
            ("ctrl (1100,430)", box(1100,430,1485,815)),
            ("ctrl (150,150)",  box(150,150,535,535)),
            ("ctrl (1150,800)", box(1150,800,1535,1185))]

def xcount(mask, cut, report=False):
    lab, k = ndi.label((G < cut) & mask, EIGHT)
    if not k: return 0, []
    hits = []
    for sl, i in zip(ndi.find_objects(lab), range(1, k+1)):
        comp = (lab[sl] == i)
        px = int(comp.sum())
        if px < 20 or px > 600: continue          # an X here is ~92 px; bound it generously
        h = sl[0].stop-sl[0].start; w = sl[1].stop-sl[1].start
        if not (6 <= w <= 40 and 6 <= h <= 40): continue
        _, e, j, d, L, _ = skel_stats(comp)
        if is_X(e, j, d):
            hits.append(((sl[1].start+sl[1].stop)/2, (sl[0].start+sl[0].stop)/2, w, h, px,
                         [round(v,1) for v in L]))
    return len(hits), hits

print("\n--- SPECIFICITY CONTROLS (plan sec.4): four 385x385 regions, equal area to C1 ---")
hdr = f"{'region':24s} " + "".join(f"{('<%d'%c):>7s}" for c in CUTS)
print(hdr)
cmax = {c: 0 for c in CUTS}
for nm, m in CONTROLS:
    row = []
    for c in CUTS:
        n, _ = xcount(m, c); row.append(n); cmax[c] = max(cmax[c], n)
    print(f"{nm:24s} " + "".join(f"{v:7d}" for v in row))
print(f"{'MAX over controls':24s} " + "".join(f"{cmax[c]:7d}" for c in CUTS))
void = {c: cmax[c] >= 2 for c in CUTS}
print(f"\n  VOID where a control yields >= 2 X-signature components (plan sec.4):")
print("    " + "  ".join(f"{c}:{'VOID' if void[c] else 'ok  '}" for c in CUTS))

print("\n--- THE CIRCULAR ELEMENTS ---")
print(hdr)
obs = {}
for nm, m in REGIONS:
    row = []
    for c in CUTS:
        n, h = xcount(m, c); row.append(n); obs[(nm, c)] = h
    print(f"{nm:24s} " + "".join(f"{v:7d}" for v in row))

print("\n  every X-signature component found inside a circular element:")
any_found = False
for nm, _ in REGIONS:
    for c in CUTS:
        for cx, cy, w, h, px, L in obs[(nm, c)]:
            any_found = True
            print(f"    {nm}  t={c:3d}  centroid ({cx:7.1f},{cy:7.1f})  {w:2d}x{h:2d}  "
                  f"{px:3d} px  arms {L}")
if not any_found:
    print("    none at any cutoff")

print("\n--- DECISION (plan sec.5) ---")
print("  C3 tablet circle: EXCLUDED FOR A PAIR BY SIZE before any pixel was read")
print("     (17.5 px diameter, interior disc ~135 px of area, 13x10 already taken by the")
print("      single mark the record grades unrecoverable). Its grade is unchanged.")
for nm, _ in REGIONS:
    usable = [c for c in CUTS if not void[c]]
    qual = [c for c in usable if len(obs[(nm, c)]) >= 2 and len(obs[(nm, c)]) > cmax[c]]
    run = best = 0
    for c in usable:
        best = best + 1 if c in qual else 0
        run = max(run, best)
    print(f"\n  {nm}")
    print(f"    usable cutoffs (not void): {usable if usable else 'NONE'}")
    print(f"    cutoffs with >= 2 X-signatures above the control max: {qual or 'none'}")
    print(f"    VERDICT: {'POSITIVE' if run >= 2 else ('NO USABLE CUTOFF' if not usable else 'NEGATIVE')}")
print("\n  plan sec.0: no word enters any config from this item, under any outcome.")
