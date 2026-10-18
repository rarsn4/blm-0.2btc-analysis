#!/usr/bin/env python3
"""Faint tablet marks: is the first glyph closer to the artist's S or G? Pixels only.

usage: ~/venvs/blm-img/bin/python -I sht_compare.py MASTER

The first glyph is the lower-left part of the faint marks (steps 0-6 along their line, tablet_measure /
sht_glyphs.out), rotated so the line (62.1 deg) is horizontal. Each reference letter is cropped from the
artist's own lettering, turned upright, reduced to an ink map relative to its own background, then
area-resized to the faint glyph's box. Score: Pearson correlation of the two ink maps. A yardstick is
printed alongside: how well S and G separate from each other at this size, and how much the score moves
when the faint glyph box shifts by one pixel.
"""
import sys, numpy as np, cv2
A = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR).astype(np.float32)
B, G, R = A[..., 0], A[..., 1], A[..., 2]
L = 0.114 * B + 0.587 * G + 0.299 * R

def ink_map(img, bg_pct=90):
    bg = np.percentile(img, bg_pct); return np.clip((bg - img) / max(bg - img.min(), 1), 0, 1)

def faint_glyph(du=0, dv=0):
    """Sample the first glyph on a grid aligned with the marks' own line; ink only on the face core."""
    from scipy import ndimage as ndi
    x0, y0, x1, y1 = 248, 766, 278, 806
    Lw, Gw = L[y0:y1, x0:x1], G[y0:y1, x0:x1]
    lab, _ = ndi.label(Lw >= 200, np.ones((3, 3), bool)); face = lab == np.bincount(lab.ravel())[1:].argmax() + 1
    core = face & ~ndi.binary_dilation(Lw < 190, np.ones((3, 3), bool), iterations=2)
    m = core & (Gw <= 231); ys, xs = np.nonzero(m)
    P = np.c_[xs, -ys].astype(float); c = P.mean(0); _, _, vt = np.linalg.svd(P - c); d = vt[0] if vt[0][0] > 0 else -vt[0]
    n = np.array([-d[1], d[0]]); u = (P - c) @ d; v = (P - c) @ n
    first = u <= u.min() + 6.5
    ink = np.where(core, np.clip((235 - Gw) / 14, 0, 1), 0).astype(np.float32)
    U = np.linspace(u.min() + du, u.min() + du + 6.5, 7); V = np.linspace(v[first].max() + dv, v[first].min() + dv, 9)
    gx = c[0] + U[None, :] * d[0] + V[:, None] * n[0]; gy = -(c[1] + U[None, :] * d[1] + V[:, None] * n[1])
    return cv2.remap(ink, gx.astype(np.float32), gy.astype(np.float32), cv2.INTER_LINEAR, borderValue=0)

def ref(x0, y0, x1, y1, rot=0, red=False):
    if red: img = (R - G)[y0:y1, x0:x1]; img = img.max() - img            # spray letters: ink = redness
    else: img = L[y0:y1, x0:x1]
    m = ink_map(img)
    if rot: m = np.rot90(m, k=rot)
    ys, xs = np.nonzero(m > 0.35); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return cv2.resize(m, (7, 9), interpolation=cv2.INTER_AREA)

def corr(a, b):
    a = a.ravel() - a.mean(); b = b.ravel() - b.mean(); return float(a @ b / np.sqrt((a @ a) * (b @ b)))

REFS = {'S (STOP)': ref(14, 462, 36, 512), 'S (SHIT, spray)': ref(1298, 888, 1344, 1004, red=True),
        'S (LIVES)': ref(1145, 210, 1173, 245, rot=-1), 'G (KILLING)': ref(1255, 163, 1293, 203, rot=-1),
        'T (STOP)': ref(40, 462, 70, 512)}
F = faint_glyph()
print('first faint glyph, ink map 9x7 (rows top->bottom):')
for row in F: print('   ' + ' '.join(f'{v:.1f}' for v in row))
print('\ncorrelation with each reference letter:')
for k, r in REFS.items():
    if r is None: continue
    print(f'   {k:18s} {corr(F, r):+.3f}')
print('\nyardstick, references against each other at 9x7:')
names = [k for k in REFS if REFS[k] is not None]
for i, a in enumerate(names):
    for b in names[i + 1:]: print(f'   {a:18s} vs {b:18s} {corr(REFS[a], REFS[b]):+.3f}')
print('\nstability: first glyph box shifted by one pixel, correlation with S (STOP) / G (KILLING):')
for du, dv in ((1, 0), (-1, 0), (0, 1), (0, -1), (0.5, 0.5)):
    f = faint_glyph(du, dv); print(f'   shift ({du:+.1f},{dv:+.1f}): {corr(f, REFS["S (STOP)"]):+.3f} / {corr(f, REFS["G (KILLING)"]):+.3f}')
