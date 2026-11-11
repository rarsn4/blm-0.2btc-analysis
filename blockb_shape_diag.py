"""AAB. Diagnostics on blockb_shape.py: control contamination, detector recall, the
size-window deviation, ink normalisation, and the R1-prime arm.

Measurement only. Nothing here changes blockb_shape.py's output; it characterises it.
"""
import os, sys, collections
import numpy as np
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runelib as R
from imgio import load_gray

G = load_gray(); H, W = G.shape
EIGHT = np.ones((3, 3), bool)
THR = 130
LADDER = (0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60)
XA, XB = R.XA, R.XB

# rebuild the identical split
cells = R.cells()
by_letter = collections.OrderedDict()
for ch, a, b in cells: by_letter.setdefault(ch, []).append((a, b))
TEMPLATE, TEST = [], []
for ch, inst in by_letter.items():
    if len(inst) == 1:
        TEST.append((ch, *inst[0]))
    else:
        k = -(-len(inst) // 2)
        for i, (a, b) in enumerate(inst):
            (TEMPLATE if i < k else TEST).append((ch, a, b))
TMASK = [R.mask(a, b) for _, a, b in TEMPLATE]
def best_iou(m): return max(R.iou(m, tm) for tm in TMASK)
TSET = {(a, b) for _, a, b in TEMPLATE}

print("AAB  DIAGNOSTICS ON THE BLOCK-B SHAPE FILTER")
print("=" * 94)
print(f"  image {H} x {W};  rune column x {XA}-{XB}, y 36-1020 (runelib)")
print(f"  TEMPLATE {len(TEMPLATE)} instances, TEST {len(TEST)}")

def box(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[max(0,y0):min(H,y1), max(0,x0):min(W,x1)] = True; return m

def cands(mask, keep34=True):
    """blockb_shape.candidates(), with the 34-px cut switchable for AAB-3."""
    lab, k = ndi.label((G < THR) & mask, EIGHT)
    out, dropped34 = [], 0
    if not k: return out, 0
    for sl, i in zip(ndi.find_objects(lab), range(1, k + 1)):
        comp = (lab[sl] == i); px = int(comp.sum())
        if px < 20 or px > 600: continue
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if not (6 <= w <= 40 and 6 <= h <= 40): continue
        if comp.shape[0] > 34 or comp.shape[1] > 34:
            dropped34 += 1
            if keep34: continue
            continue                       # cannot centre in 34x34 either way
        m = np.zeros((34, 34), bool)
        oy, ox = (34 - comp.shape[0]) // 2, (34 - comp.shape[1]) // 2
        m[oy:oy + comp.shape[0], ox:ox + comp.shape[1]] = comp
        out.append(dict(iou=best_iou(m), xc=(sl[1].start + sl[1].stop) / 2,
                        y0=sl[0].start, y1=sl[0].stop - 1, w=w, h=h, px=px))
    return out, dropped34

NULLS = [("y 160-198", 160, 198), ("y 420-458", 420, 458),
         ("y 600-638", 600, 638), ("y 980-1018", 980, 1018)]

def overlaps_cell(y0, y1):
    for ch, a, b in cells:
        if y1 >= a and y0 <= b:
            return ch, a, b, ("TEMPLATE" if (a, b) in TSET else "TEST")
    return None

# ---------------------------------------------------------------- AAB-1
print("\n" + "-" * 94)
print("AAB-1  EVERY NULL CANDIDATE, and whether it is block A")
tot = incol = 0
contam_iou = []
for nm, y0, y1 in NULLS:
    cs, _ = cands(box(0, y0, 1600, y1))
    print(f"\n  {nm}  ({len(cs)} candidates)")
    print(f"    {'x-centre':>9s} {'y-range':>11s} {'IoU':>6s} {'in col':>7s}  block-A cell")
    for c in sorted(cs, key=lambda d: -d["iou"]):
        inc = XA <= c["xc"] <= XB
        ov = overlaps_cell(c["y0"], c["y1"])
        tag = f"{ov[0]} y{ov[1]}-{ov[2]} {ov[3]}" if (inc and ov) else ("-- in column, no cell --" if inc else "")
        tot += 1; incol += (1 if (inc and ov) else 0)
        if inc and ov: contam_iou.append(c["iou"])
        print(f"    {c['xc']:9.1f} {c['y0']:5d}-{c['y1']:<5d} {c['iou']:6.3f} {str(inc):>7s}  {tag}")
print(f"\n  total null candidates {tot};  block-A glyphs among them {incol}")
print(f"  PREDICTION was 4-7 of 57. candidates={tot}, contaminated={incol} -> "
      f"{'HOLDS' if 4 <= incol <= 7 else 'FAILS'}")

print("\n  cross-tabulation against the ladder: matches that ARE block A")
print(f"    {'IoU >=':>8s} {'all nulls':>10s} {'block-A':>9s} {'clean':>7s}")
for t in LADDER:
    allm = sum(1 for nm, y0, y1 in NULLS for c in cands(box(0,y0,1600,y1))[0] if c["iou"] >= t)
    bam = sum(1 for v in contam_iou if v >= t)
    print(f"    {t:8.2f} {allm:10d} {bam:9d} {allm-bam:7d}")

# hard check: a TEMPLATE instance inside a strip must score exactly 1.000
print("\n  HARD CHECK: any TEMPLATE instance falling in a strip must score best_iou = 1.000")
hard = []
for nm, y0, y1 in NULLS:
    for ch, a, b in TEMPLATE:
        if b >= y0 and a <= y1 - 1:
            hard.append((nm, ch, a, b, best_iou(R.mask(a, b))))
if hard:
    for nm, ch, a, b, v in hard:
        print(f"    {nm}: TEMPLATE {ch} y{a}-{b}  best_iou = {v:.6f}  "
              f"{'PASS' if abs(v-1.0) < 1e-9 else 'FAIL'}")
else:
    print("    no TEMPLATE instance lies inside any strip")

# ---------------------------------------------------------------- AAB-2
print("\n" + "-" * 94)
print("AAB-2  DETECTOR RECALL: candidates() over the rune column itself")
col, drop34col = cands(box(XA, 36, XB, 1020))
print(f"  components passing the gate: {len(col)}   (dropped by the 34-px cut: {drop34col})")
one2one, split, missed = [], [], []
for ch, a, b in cells:
    hit = [c for c in col if min(b, c["y1"]) - max(a, c["y0"]) + 1 >= 0.5 * (b - a + 1)]
    if len(hit) == 1: one2one.append((ch, a, b, hit[0]))
    elif len(hit) > 1: split.append((ch, a, b, len(hit)))
    else: missed.append((ch, a, b))
print(f"  of {len(cells)} cells: {len(one2one)} recovered 1:1, {len(split)} split, {len(missed)} dropped")
print(f"  RECALL = {len(one2one)}/{len(cells)} = {100*len(one2one)/len(cells):.1f}%")
if split:
    print("  split:   " + ", ".join(f"{ch} y{a}-{b} -> {n} parts" for ch, a, b, n in split))
if missed:
    print("  dropped: " + ", ".join(f"{ch} y{a}-{b}" for ch, a, b in missed))
print("\n  match curve of the RECOVERED set (detector + matcher end to end):")
rec_iou = [h["iou"] for _, _, _, h in one2one]
print(f"    {'IoU >=':>8s} " + "".join(f"{t:>8.2f}" for t in LADDER))
print(f"    {'recovered':>8s} " + "".join(f"{sum(1 for v in rec_iou if v >= t):>8d}" for t in LADDER))
print(f"    of {len(rec_iou)} recovered")

# ---------------------------------------------------------------- AAB-3, AAB-4, AAB-5
print("\n" + "-" * 94)
print("AAB-3  the 34-px cut the plan did not authorise, per region")
print("AAB-4  equal area and ink, not equal label")
print(f"\n  {'region':16s} {'rows':>5s} {'cols':>5s} {'ink px':>9s} {'cands':>6s} {'drop34':>7s} {'cand/1k ink':>12s}")
REGIONS = [("R1", 0, 1100, 1600, 1138), ("R1'", 0, 1100, 1600, 1138)] + \
          [(nm, 0, y0, 1600, y1) for nm, y0, y1 in NULLS] + \
          [("rune column", XA, 36, XB, 1020)]
CX, CY, RAD = 470, 937, 182
yy, xx = np.ogrid[:H, :W]
disc = ((xx-CX)**2 + (yy-CY)**2) <= RAD*RAD
for nm, x0, y0, x1, y1 in REGIONS:
    m = box(x0, y0, x1, y1)
    if nm == "R1'": m = m & ~disc
    rows = min(H, y1) - max(0, y0)
    ink = int(((G < THR) & m).sum())
    cs, d34 = cands(m)
    rate = 1000 * len(cs) / ink if ink else float("nan")
    print(f"  {nm:16s} {rows:5d} {min(W,x1)-max(0,x0):5d} {ink:9d} {len(cs):6d} {d34:7d} {rate:12.3f}")

print("\nAAB-5  is R1-prime a second arm?")
r1, _ = cands(box(0, 1100, 1600, 1138))
r1p, _ = cands(box(0, 1100, 1600, 1138) & ~disc)
print(f"  R1 {len(r1)} candidates, R1-prime {len(r1p)};  the disc removed {len(r1)-len(r1p)}")
print(f"  disc pixels inside R1: {int((box(0,1100,1600,1138) & disc).sum()):,}")
print(f"  -> {'NOT a second arm: identical candidate set' if len(r1)==len(r1p) else 'genuinely different'}")
print("\n  R1 per-candidate match rate against the busiest strip (AAB-7e):")
busiest = max(NULLS, key=lambda n: len(cands(box(0,n[1],1600,n[2]))[0]))
bc, _ = cands(box(0, busiest[1], 1600, busiest[2]))
for t in (0.30, 0.60):
    print(f"    IoU >= {t:.2f}: R1 {sum(1 for c in r1 if c['iou']>=t)}/{len(r1)}"
          f"   {busiest[0]} {sum(1 for c in bc if c['iou']>=t)}/{len(bc)}")

# ---------------------------------------------------------------- per-strip clean maxima
print("\n" + "-" * 94)
print("AAB-6  the published 'max over the four nulls' row, with block A removed")
print(f"  {'IoU >=':>8s} {'published':>10s} {'clean max':>10s} {'R1':>5s}")
rows = {}
for nm, y0, y1 in NULLS:
    cs, _ = cands(box(0, y0, 1600, y1))
    rows[nm] = [(c, XA <= c["xc"] <= XB and overlaps_cell(c["y0"], c["y1"]) is not None) for c in cs]
r1c, _ = cands(box(0, 1100, 1600, 1138))
PUB = [10, 10, 9, 6, 4, 2, 2]
for i, t in enumerate(LADDER):
    allmax = max(sum(1 for c, _ in rows[nm] if c["iou"] >= t) for nm in rows)
    cleanmax = max(sum(1 for c, bad in rows[nm] if c["iou"] >= t and not bad) for nm in rows)
    assert allmax == PUB[i], (t, allmax, PUB[i])
    print(f"  {t:8.2f} {allmax:10d} {cleanmax:10d} {sum(1 for c in r1c if c['iou']>=t):5d}")
print("  (the published row is reproduced exactly, so this is a re-scope and not a correction)")
