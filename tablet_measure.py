#!/usr/bin/env python3
"""Two pixel measurements on the BLM tablet. No reading of what the marks say.

usage: ~/venvs/blm-img/bin/python -I tablet_measure.py MASTER

A. Faint strokes below the circle: bounding box, luminance against the tablet face,
   connected components after a levels stretch, and ink-vs-shading discriminators
   (stroke width, edge contrast, spatial scale) against two references on the same
   card: the BLM capitals (known ink) and the face's own large-scale gradient.
B. Skeleton structure of the circle's interior, measured exactly as glyph X was
   (§7.4: ink < 110, main component, skeletonized), with X re-measured first as the
   positive control, then both swept across thresholds.
Luminance: Rec.601, 0.299 R + 0.587 G + 0.114 B.
"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.morphology import skeletonize

im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
L = 0.299 * im[..., 0] + 0.587 * im[..., 1] + 0.114 * im[..., 2]
EIGHT = np.ones((3, 3), bool)

# ---------------------------------------------------------------- A. faint strokes
print('=== A. faint strokes below the circle ===')
CX, CY, R_OUT = 263.5, 760.5, 17.5 / 2
x0, y0, x1, y1 = 248, 772, 280, 808            # window below the circle, master px (x1, y1 exclusive)
W = L[y0:y1, x0:x1]
light = W >= 200
lab, n = ndi.label(light, EIGHT)
face = lab == (np.bincount(lab.ravel())[1:].argmax() + 1)           # the tablet face below the circle
edge = W < 190                                                      # tablet edge, hand, their ramps
core = face & ~ndi.binary_dilation(edge, EIGHT, iterations=2)       # >= 3 px from any edge pixel
vals, cnts = np.unique(np.round(W[core]), return_counts=True)
BG = vals[cnts.argmax()]
print(f'face core (>= 3 px from any pixel < 190): {int(core.sum())} px; mode luminance {BG:.0f} '
      f'held by {cnts.max()} px ({cnts.max() / core.sum():.0%})')
depth = BG - W
print(f'core pixels below {BG:.0f}: {int((core & (depth >= 1)).sum())}; above {BG:.0f}: {int((core & (depth <= -1)).sum())}')

lo = float(W[core].min())
print(f'levels stretch on the face core: {lo:.0f} -> 0, {BG:.0f} -> 255 (each level = {255 / (BG - lo):.1f} stretched)')
for d in (2, 4, 6, 8, 10, 12):
    m = core & (depth >= d)
    labm, nm = ndi.label(m, EIGHT)
    sizes = sorted(np.bincount(labm.ravel())[1:].tolist(), reverse=True)
    print(f'  depth >= {d:2d} levels (stretched value <= {255 - d * 255 / (BG - lo):5.1f}): {nm:2d} components, '
          f'{int(m.sum()):3d} px, sizes {sizes}')

D = 4
m = core & (depth >= D)
labm, nm = ndi.label(m, EIGHT)
ys, xs = np.nonzero(m)
print(f'\nat depth >= {D}: {nm} components, {int(m.sum())} px, union bbox x {xs.min() + x0}..{xs.max() + x0}, '
      f'y {ys.min() + y0}..{ys.max() + y0}; depth max {depth[m].max():.0f}, mean {depth[m].mean():.1f} levels; '
      f'luminance min {W[m].min():.0f}')
dist_edge = ndi.distance_transform_edt(~edge)
for i in range(1, nm + 1):
    sel = labm == i
    py, px = np.nonzero(sel)
    if sel.sum() >= 3:
        w_, V = np.linalg.eigh(np.cov(np.c_[px, py].T))
        ang = np.degrees(np.arctan2(-V[1, 1], V[0, 1])) % 180     # 0 = horizontal, 90 = vertical (y up)
        axis = f'axis {ang:3.0f} deg  elong {np.sqrt(w_[1] / max(w_[0], 1e-9)):4.1f}'
    else:
        axis = 'axis  -'
    print(f'  comp {i:2d}: {int(sel.sum()):2d} px  bbox x {px.min() + x0}..{px.max() + x0} y {py.min() + y0}..{py.max() + y0}  '
          f'lum min {W[sel].min():.0f}  depth max {depth[sel].max():2.0f}  {axis}')
over = core & (depth <= -1)
adj = ndi.binary_dilation(core & (depth >= 1), EIGHT)
print(f'core pixels brighter than {BG:.0f}: {int(over.sum())}, of which 8-adjacent to a darker-than-{BG:.0f} pixel: '
      f'{int((over & adj).sum())}; max {W[over].max() if over.any() else BG:.0f}')

# shading reference: the ramp along the tablet's left edge, row by row
print('\nshading reference, tablet left edge (rows 772..800): first column reaching >= 218, ramp width, monotonic?')
widths, starts, mono = [], [], 0
for y in range(772, 801):
    row = L[y, 248:262]
    j218 = int(np.argmax(row >= 218)); j150 = int(np.argmax(row >= 150))
    widths.append(j218 - j150); starts.append(248 + j150)
    mono += bool(np.all(np.diff(row[j150:j218 + 1]) >= -1))
print(f'  ramp 150 -> 218 width: median {np.median(widths):.0f} px (range {min(widths)}..{max(widths)}); '
      f'start column {min(starts)}..{max(starts)}; monotonic in {mono} of {len(widths)} rows')
print(f'  ramp gradient ~{(218 - 150) / max(np.median(widths), 1):.0f} levels/px, contiguous with the edge')

# discriminators that do not depend on the core mask
def valley(img, gap=2, k=2):
    """pixel has a brighter pixel (by >= gap) within k steps on BOTH sides along some direction"""
    out = np.zeros(img.shape, bool); H, Wd = img.shape
    P = np.pad(img, k, mode='edge')
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        side = []
        for sgn in (1, -1):
            best = np.full(img.shape, -1e9)
            for t in range(1, k + 1):
                best = np.maximum(best, P[k + sgn * t * dy:k + sgn * t * dy + H, k + sgn * t * dx:k + sgn * t * dx + Wd])
            side.append(best >= img + gap)
        out |= side[0] & side[1]
    return out
V = valley(W)
ramp = np.zeros(W.shape, bool)
for y in range(772, 801):
    for x in range(248, 257):
        if 150 <= L[y, x] <= 218: ramp[y - y0, x - x0] = True
print(f'\nvalley test (darker than a pixel within 2 steps on BOTH sides, by >= 2 levels, in some direction):')
print(f'  faint-mark pixels (core, depth >= {D}): {int((V & m).sum())} of {int(m.sum())} are valleys')
print(f'  left-edge ramp pixels (rows 772..800, 150..218): {int((V & ramp).sum())} of {int(ramp.sum())} are valleys')
fullface = (W >= 150) & ~edge
vm = fullface & V & (depth >= D)
lv, nv = ndi.label(vm, EIGHT)
touch = ndi.binary_dilation(edge, EIGHT)
print(f'  over the whole face incl. the 2-px edge zone: {nv} valley components at depth >= {D}, sizes '
      f'{sorted(np.bincount(lv.ravel())[1:].tolist(), reverse=True)}; touching an edge pixel (< 190): '
      f'{sum(bool((touch & (lv == i)).any()) for i in range(1, nv + 1))}')
ysv, xsv = np.nonzero(vm)
print(f'  their union bbox: x {xsv.min() + x0}..{xsv.max() + x0}, y {ysv.min() + y0}..{ysv.max() + y0}')

flat = core & ~ndi.binary_dilation(m | (core & (depth >= 1)), EIGHT)
print(f'\nfill flatness: core pixels not within 1 px of any below-{BG:.0f} pixel: {int(flat.sum())}, '
      f'of which exactly {BG:.0f}: {int((np.round(W[flat]) == BG).sum())}')
def overshoot_near(mask_dark, img, bg):
    ring_ = ndi.binary_dilation(mask_dark, EIGHT) & ~mask_dark
    return int((ring_ & (img > bg + 0.5)).sum()), int(ring_.sum())
o1 = overshoot_near(m, W, BG)
o2 = overshoot_near(ramp, W, BG)
BLMw = L[715:745, 255:300]; o3 = overshoot_near(BLMw < 200, BLMw, BG)
print(f'overshoot (> {BG:.0f}) among 1-px neighbours: faint marks {o1[0]}/{o1[1]}, left-edge ramp {o2[0]}/{o2[1]}, '
      f'BLM capitals {o3[0]}/{o3[1]}')

rgb = im[y0:y1, x0:x1]
fill = np.median(rgb[flat], axis=0) if flat.any() else np.median(rgb[core], axis=0)
mins = rgb[m].min(axis=0)
print(f'per channel, fill R G B = {fill[0]:.0f} {fill[1]:.0f} {fill[2]:.0f}; darkest mark pixel per channel '
      f'{mins[0]:.0f} {mins[1]:.0f} {mins[2]:.0f}; depth {fill[0] - mins[0]:.0f} {fill[1] - mins[1]:.0f} {fill[2] - mins[2]:.0f}')
mn = rgb.min(axis=2); print(f'min(R,G,B): fill {np.median(mn[flat]):.0f}, darkest mark {mn[m].min():.0f}, depth {np.median(mn[flat]) - mn[m].min():.0f}')

# orientation of the nearest edge (hand), for comparison with the mark axes
ey, ex = [], []
for y in range(772, 806):
    row = L[y, 256:280]; idx = np.nonzero(row < 190)[0]
    if len(idx): ey.append(y); ex.append(256 + idx[0])
c1 = np.polyfit(ey, ex, 1)
print(f'hand edge (first pixel < 190 from the left, rows 772..805): x = {c1[0]:.3f} y + {c1[1]:.1f}; '
      f'axis {np.degrees(np.arctan2(1, -c1[0])) % 180:.0f} deg (same convention as the mark axes)')

blm = L[722:742, 255:300]; blm_mask = blm < (222 + 29) / 2
print(f'\nreference ink, BLM capitals (x255..299, y722..741): luminance min {blm.min():.0f}, depth below 222 '
      f'up to {222 - blm.min():.0f} levels, max stroke width {2 * ndi.distance_transform_edt(blm_mask).max() - 1:.0f} px')

# ---------------------------------------------------------------- B. skeletons
print('\n=== B. skeleton structure: glyph X (control) and the circle interior ===')
def skel_stats(mask):
    sk = skeletonize(mask)
    nb = ndi.convolve(sk.astype(int), np.ones((3, 3), int), mode='constant') - 1
    ends = sk & (nb == 1); br = sk & (nb >= 3)
    jl, nj = ndi.label(ndi.binary_dilation(br, EIGHT, iterations=1) & sk, EIGHT)   # merge adjacent branch px
    arms_mask = sk & (jl == 0)
    al, na = ndi.label(arms_mask, EIGHT)
    juncs = []
    for j in range(1, nj + 1):
        touch = set(np.unique(al[ndi.binary_dilation(jl == j, EIGHT)])) - {0}
        cy, cx = np.argwhere(jl == j).mean(0); juncs.append(((cx, cy), len(touch), touch))
    arms = []
    for a_ in range(1, na + 1):
        pts = np.argwhere(al == a_)
        e = [tuple(p) for p in np.argwhere(ends & (al == a_))]
        arms.append((a_, len(pts), e, pts))
    return sk, int(ends.sum()), juncs, arms

def describe(name, mask):
    sk, ne, juncs, arms = skel_stats(mask)
    deg = [d for _, d, _ in juncs]
    out = f'{name}: ink px {int(mask.sum())}, skeleton px {int(sk.sum())}, endpoints {ne}, junctions {len(juncs)} degrees {deg}'
    strokes, angle = None, None
    four = [j for j in juncs if j[1] == 4]
    if len(juncs) == 1 and four:
        (cx, cy), _, touch = four[0]
        dirs = {}
        for a_, ln, e, pts in arms:
            if a_ in touch:
                far = pts[np.argmax(((pts - [cy, cx]) ** 2).sum(1))]
                dirs[a_] = (np.array([far[1] - cx, -(far[0] - cy)]), np.hypot(far[1] - cx, far[0] - cy))
        ks = list(dirs)
        best = min(((p, q) for i, p in enumerate(ks) for q in ks[i + 1:]),
                   key=lambda pq: np.dot(dirs[pq[0]][0], dirs[pq[1]][0]) /
                   (np.linalg.norm(dirs[pq[0]][0]) * np.linalg.norm(dirs[pq[1]][0])))
        other = [k for k in ks if k not in best]
        def axis(p, q): v = dirs[p][0] - dirs[q][0]; return v / np.linalg.norm(v)
        a1, a2 = axis(*best), axis(*other)
        angle = np.degrees(np.arccos(abs(np.dot(a1, a2))))
        strokes = 2
        lens = sorted((round(float(dirs[k][1]), 1) for k in ks), reverse=True)
        out += f'; strokes {strokes} (arms paired through the crossing); angle between strokes {angle:.0f} deg; arm lengths {lens}'
    else:
        out += '; no single 4-way crossing'
    print(out)
    return ne, len(juncs), deg, angle

# X: §7.4 window, ink < 110, main component, rotated 90 deg clockwise into the reading frame
Xw = L[38:56, 1530:1561]
def main_comp(mask):
    lab, n = ndi.label(mask, EIGHT)
    return (lab == (np.bincount(lab.ravel())[1:].argmax() + 1)) if n else mask
xm = np.rot90(main_comp(Xw < 110), k=-1)
print(f'X window x1530..1560 y38..55, ink < 110: main component {int(xm.sum())} px (§7.4 records 92)')
describe('X  @110', xm)

# circle interior: inside the ring's inner edge, image frame
Cw = L[750:772, 252:276]
yy2, xx2 = np.mgrid[750:772, 252:276]
inner = (xx2 - CX) ** 2 + (yy2 - CY) ** 2 < (R_OUT - 2.2) ** 2      # ring is ~1.5-2 px wide
print(f'circle interior: disc r < {R_OUT - 2.2:.2f} px about ({CX}, {CY}); darkest pixel {Cw[inner].min():.0f}; '
      f'pixels < 110: {int((inner & (Cw < 110)).sum())}, < 90: {int((inner & (Cw < 90)).sum())}')
describe('interior @110', main_comp(inner & (Cw < 110)))

print('\nthreshold sweep (same method at each threshold):')
for t in (90, 110, 125, 140, 155, 170, 185):
    for nm_, msk in (('X', np.rot90(main_comp(Xw < t), k=-1)), ('interior', main_comp(inner & (Cw < t)))):
        if msk.sum() == 0:
            print(f'  t={t:3d}  {nm_:8s} no ink'); continue
        sk, ne, juncs, arms = skel_stats(msk)
        lab_all, ncomp = ndi.label(inner & (Cw < t) if nm_ == 'interior' else Xw < t, EIGHT)
        py_, px_ = np.nonzero(msk)
        if len(px_) >= 3:
            w_, V_ = np.linalg.eigh(np.cov(np.c_[px_, py_].T))
            ax = f'axis {np.degrees(np.arctan2(-V_[1, 1], V_[0, 1])) % 180:3.0f} deg elong {np.sqrt(w_[1] / max(w_[0], 1e-9)):4.1f}'
        else:
            ax = 'axis   -'
        print(f'  t={t:3d}  {nm_:8s} components {ncomp:2d}  main px {int(msk.sum()):3d}  endpoints {ne}  '
              f'junctions {len(juncs)} degrees {[d for _, d, _ in juncs]}  {ax}')
