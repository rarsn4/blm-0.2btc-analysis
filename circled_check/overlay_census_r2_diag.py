#!/usr/bin/env python3
"""POST-HOC diagnostic for round 2 (run after the registered result; changes no status or decision).
Checks what the two eligible non-subject rows that SHOW actually measured, and the subject's depth source.
usage: ~/venvs/blm-img/bin/python -I overlay_census_r2_diag.py MASTER"""
import sys, numpy as np; from PIL import Image; from scipy import ndimage as ndi
im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
L = np.round(0.299 * im[..., 0] + 0.587 * im[..., 1] + 0.114 * im[..., 2]).astype(int); E = np.ones((3, 3), bool)
def diag(name, x0, y0, x1, y1, fill=222):
    W = L[y0:y1 + 1, x0:x1 + 1]; mk = W <= fill - 4; near = ndi.binary_dilation(mk, E, iterations=2); far = ~near
    v, c = np.unique(W, return_counts=True); top = sorted(zip(c, v), reverse=True)[:4]
    fy, fx = np.nonzero(far); by, bx = np.nonzero(near & ~mk & (W >= fill + 1))
    print(f'{name}: window {W.size} px; commonest values {[(int(b), int(a)) for a, b in top]}; median {np.median(W):.0f}')
    print(f'   far region {int(far.sum())} px, rows {sorted(set((fy + y0).tolist()))}')
    for y, x in zip(by, bx):
        Y, X = y + y0, x + x0
        nb = [(int(X + dx), int(Y + dy), int(L[Y + dy, X + dx])) for dy in range(-2, 3) for dx in range(-2, 3)
              if L[Y + dy, X + dx] <= fill - 4 and x0 <= X + dx <= x1 and y0 <= Y + dy <= y1]
        print(f'   brighter neighbour ({X},{Y}) = {L[Y, X]}; mask pixels within 2 px: {nb}')
diag('O1 ONLY real BITCOIN', 93, 1050, 228, 1063)
diag('C2 circle', 251, 748, 276, 773)
W = L[772:798, 256:271]; m = W <= 218
print('S1: darkest mask pixel', int(W[m].min()), 'at', [(int(x + 256), int(y + 772)) for y, x in zip(*np.nonzero(W == W[m].min()))][:3])
by, bx = np.nonzero(ndi.binary_dilation(m, E, iterations=2) & ~m & (W >= 223))
print('S1 brighter pixels:', sorted((int(x + 256), int(y + 772)) for y, x in zip(by, bx)))
