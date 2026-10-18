#!/usr/bin/env python3
"""Image measurements of 18 Oct 2026, pixels only. Each section prints the figures REPORT.md quotes.

usage: ~/venvs/blm-img/bin/python -I oct18_measurements.py MASTER
Sections: A possible wristwatch loop; B thin vertical strokes on the monument vs the wreath plaque;
C tablet outline, axes and feature positions; D top-left and bottom-right artist marks;
E faint tablet marks segmented along their line, with a blank-fill control.
Luminance is Rec.601. Angles: 0 = horizontal, 90 = vertical, y up.
"""
import sys, numpy as np, cv2
from scipy import ndimage as ndi
A = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR).astype(float); Bc, Gc, Rc = A[..., 0], A[..., 1], A[..., 2]
L = 0.114 * Bc + 0.587 * Gc + 0.299 * Rc
E8 = np.ones((3, 3), bool)
ang = lambda d: np.degrees(np.arctan2(-d[1], d[0])) % 180

print('=== A. possible wristwatch loop, window x336..365 y238..269 ===')
x0, y0, x1, y1 = 336, 238, 366, 270; W = L[y0:y1, x0:x1]
print(f'median {np.median(W):.0f}, darkest {W.min():.0f}')
for t in (130, 140, 150, 160, 170):
    ink = W < t; holes = ndi.binary_fill_holes(ink) & ~ink; lab, n = ndi.label(holes); parts = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i); ry, rx = np.nonzero(ndi.binary_fill_holes(ink) & ndi.binary_dilation(lab == i, iterations=3))
        parts.append(f'{len(xs)} px at x{xs.min()+x0}..{xs.max()+x0} y{ys.min()+y0}..{ys.max()+y0} (interior mean {W[lab == i].mean():.0f}), '
                     f'enclosing ink x{rx.min()+x0}..{rx.max()+x0} y{ry.min()+y0}..{ry.max()+y0}')
    print(f'ink < {t}: enclosed holes {n}' + ''.join('\n   ' + p for p in parts))

print('\n=== B. thin vertical dark segments: monument stone vs the wreath plaque ===')
red = (Rc - Gc > 35)
def segments(W, bg, ox, oy, label):
    lab, n = ndi.label(W, structure=E8); out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i); h = ys.max() - ys.min() + 1; w = xs.max() - xs.min() + 1
        widths = [np.sum(lab[y] == i) for y in range(ys.min(), ys.max() + 1)]
        if h >= 6 and np.median(widths) <= 3 and h >= 2 * w:
            out.append((xs.min() + ox, xs.max() + ox, ys.min() + oy, ys.max() + oy, h, float(np.median(widths)), float(bg[lab == i].mean())))
    print(f'{label}: {len(out)} segments (median width <= 3 px, height >= 6 px, height >= 2x width, >= 12 levels darker than the stone beside)')
    for s in sorted(out): print(f'   x{s[0]}..{s[1]} y{s[2]}..{s[3]}  length {s[4]}  width {s[5]:.0f}  contrast {s[6]:.0f}')
X0, Y0, X1, Y1 = 1262, 640, 1495, 1045; W = L[Y0:Y1, X0:X1]; bgH = ndi.median_filter(W, size=(1, 11)); dk = bgH - W
yy, xx = np.mgrid[Y0:Y1, X0:X1]
excl = ndi.binary_dilation(red[Y0:Y1, X0:X1] | ((xx >= 1300) & (xx <= 1455) & (yy >= 812) & (yy <= 910))
                           | ((xx >= 1335) & (xx <= 1445) & (yy >= 655) & (yy <= 775)), iterations=2)
segments((dk >= 12) & ~excl, dk, X0, Y0, 'monument x1262..1494 y640..1044, excluding spray, inscription, wreath')
P0x, P0y, P1x, P1y = 1376, 690, 1406, 714; Wp = L[P0y:P1y, P0x:P1x]; dp = ndi.median_filter(Wp, size=(1, 11)) - Wp
segments(dp >= 12, dp, P0x, P0y, 'wreath plaque x1376..1405 y690..713')

print('\n=== C. tablet outline (darkest-pixel trace), axes, feature positions ===')
def fit(P):
    P = np.array(P, float); c = P.mean(0); _, _, vt = np.linalg.svd(P - c); n = np.array([-vt[0][1], vt[0][0]]); r = (P - c) @ n
    return c, vt[0], len(P), np.abs(r).max(), np.sqrt((r ** 2).mean())
def inter(a, b): t = np.linalg.solve(np.c_[a[1], -b[1]], b[0] - a[0]); return a[0] + t * a[1]
top = fit([(x, y0 + int(np.argmin(L[y0:y0 + 9, x]))) for x in range(262, 304) for y0 in [int(708 + 0.31 * (x - 262))]])
left = fit([(243 + int(np.argmin(L[y, 243:259])), y) for y in range(722, 803)])
right = fit([(298 + int(np.argmin(L[y, 298:313])), y) for y in range(729, 745)])
und = fit([(x, y0 + int(np.argmin(L[y0:y0 + 7, x]))) for x in range(258, 290) for y0 in [int(735 + 0.37 * (x - 258))]])
for n, l in (('top outline', top), ('left outline', left), ('right outline', right), ('BLM underline', und)):
    print(f'{n:14s} {l[2]:3d} pts  {ang(l[1]):6.1f} deg  rms {l[4]:.2f} px')
TL, TR = inter(top, left), inter(top, right); BL = inter((np.array([249.0, 806.0]), top[1]), left); BR = BL + (TR - TL)
print(f'corners TL ({TL[0]:.1f},{TL[1]:.1f})  TR ({TR[0]:.1f},{TR[1]:.1f})  BL ({BL[0]:.1f},{BL[1]:.1f}) [bottom hidden: line through the last visible row, parallel to top]  BR ({BR[0]:.1f},{BR[1]:.1f}) [inferred]')
u, v = BL - TL, TR - TL; tab = lambda p: np.linalg.solve(np.c_[u, v], np.array(p, float) - TL)
ys, xs = np.nonzero(L[721:736, 262:292] < 125.5); blm = (xs.mean() + 262, ys.mean() + 721)
ys, xs = np.nonzero((L[773:800, 256:270] <= 218) & (L[773:800, 256:270] >= 190)); fm = (xs.mean() + 256, ys.mean() + 773)
for n, p in (('BLM letters', blm), ('circle centre', (263.5, 760.5)), ('faint marks centroid', fm), ('faint marks top', (262, 773)), ('faint marks bottom', (258, 799))):
    a, b = tab(p); print(f'{n:22s} ({p[0]:.1f},{p[1]:.1f}) -> along {a:.2f}, across {b:.2f}')

print('\n=== D. artist marks ===')
W = L[38:84, 47:68]; vals, cnt = np.unique(np.round(W), return_counts=True); bg = vals[cnt.argmax()]
ys, xs = np.nonzero(W <= bg - 15)
print(f'top-left, inside the border: background {bg:.0f}, darkest {W.min():.0f} (depth {bg - W.min():.0f}); {len(xs)} px >= 15 below, at x{xs.min()+47}..{xs.max()+47} y{ys.min()+38}..{ys.max()+38}')
Bw = L[1130:1153, 1522:1562]; ys, xs = np.nonzero(Bw < 92)
print(f'bottom-right box: panel 93..113, glyph pixels < 92: {len(xs)} at x{xs.min()+1522}..{xs.max()+1522} y{ys.min()+1130}..{ys.max()+1130}, darkest {Bw.min():.0f}')

print('\n=== E. faint tablet marks along their line (G channel, ink = G <= fill - 4 on the face core) ===')
def line_glyphs(x0, y0, x1, y1, name):
    Lw, Gw = L[y0:y1, x0:x1], Gc[y0:y1, x0:x1]
    lab, _ = ndi.label(Lw >= 200, E8); face = lab == np.bincount(lab.ravel())[1:].argmax() + 1
    core = face & ~ndi.binary_dilation(Lw < 190, E8, iterations=2); fill = np.median(Gw[core]); ink = core & (Gw <= fill - 4)
    ys, xs = np.nonzero(ink); print(f'{name}: x{x0}..{x1-1} y{y0}..{y1-1}; core {int(core.sum())} px; G fill {fill:.0f}; ink {len(xs)} px')
    if len(xs) < 5: print('   no glyphs'); return
    P = np.c_[xs, -ys].astype(float); c = P.mean(0); _, _, vt = np.linalg.svd(P - c); d = vt[0] if vt[0][0] > 0 else -vt[0]
    uu = (P - c) @ d; vv = (P - c) @ np.array([-d[1], d[0]]); ub = np.floor(uu - uu.min()).astype(int); prof = np.bincount(ub)
    print(f'   line {ang(np.array([d[0], -d[1]])):.1f} deg; extent {uu.max()-uu.min():.1f} x {vv.max()-vv.min():.1f} px; profile {" ".join(map(str, prof))}')
    segs, s0 = [], 0
    for g in list(np.nonzero(prof == 0)[0]) + [len(prof)]:
        if g > s0: segs.append((s0, g - 1))
        s0 = g + 1
    for i, (s, e) in enumerate(segs, 1):
        m = (ub >= s) & (ub <= e)
        print(f'   group {i}: steps {s}..{e} ({e-s+1} px), {vv[m].max()-vv[m].min()+1:.0f} px tall, {int(m.sum())} px, x{xs[m].min()+x0}..{xs[m].max()+x0} y{ys[m].min()+y0}..{ys[m].max()+y0}')
line_glyphs(250, 768, 276, 804, 'faint marks')
line_glyphs(272, 731, 296, 744, 'control: blank tablet face right of BLM')
