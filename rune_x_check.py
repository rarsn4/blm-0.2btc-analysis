#!/usr/bin/env python3
"""Glyph X against rendered runes: structure first, then the correlation harness. Pixels only.

usage: ~/venvs/blm-img/bin/python -I rune_x_check.py   (run from ~/blm-analysis; needs FreeMono with Runic)

1. Structure, measured the same way on X and on rendered U+16C5 (long-branch ar) and U+16BE (naudiz):
   skeleton endpoints and junctions, and the direction of the non-vertical stroke (/ or \\).
2. Harness of glyphX_measurement.md section 2, re-implemented: ink bbox stretched to 32x32, z-scored,
   Pearson correlation. Its scale is re-calibrated here on the right-edge column's repeated letters
   (runelib.cells), then X (rotated 90 deg clockwise into its reading frame, as in REPORT 7.4) is scored
   against every Younger and Elder Futhark rune rendered in FreeMono, and the rank of each is reported.
"""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from skimage.morphology import skeletonize
import runelib as R

FONT = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'
YOUNGER = 'ᚠᚢᚦᚬᚱᚴᚼᚾᛁᛅᛋᛏᛒᛘᛚᛦ'
ELDER = 'ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ'
E8 = np.ones((3, 3), bool)

def render(ch, size=160):
    f = ImageFont.truetype(FONT, size); im = Image.new('L', (size * 2, size * 2), 255)
    ImageDraw.Draw(im).text((size // 2, size // 4), ch, font=f, fill=0)
    m = np.asarray(im) < 128; ys, xs = np.nonzero(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def norm32(m):
    ys, xs = np.nonzero(m); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.float32)
    v = cv2.resize(m, (32, 32), interpolation=cv2.INTER_AREA); return (v - v.mean()) / (v.std() + 1e-9)

def corr(a, b): return float((a * b).mean())

def structure(m):
    sk = skeletonize(m); nb = ndi.convolve(sk.astype(int), np.ones((3, 3), int), mode='constant') - 1
    ends = int((sk & (nb == 1)).sum()); jl, nj = ndi.label(ndi.binary_dilation(sk & (nb >= 3), E8) & sk, E8)
    # the stave: the longest near-vertical run; the diagonal: skeleton pixels away from the stave column
    col = np.bincount(np.nonzero(sk)[1]).argmax()
    ys, xs = np.nonzero(sk & (np.abs(np.arange(sk.shape[1])[None, :] - col) > max(2, sk.shape[1] // 12)))
    slope = np.polyfit(xs, -ys, 1)[0] if len(xs) > 3 else float('nan')   # y up
    return ends, nj, ('/' if slope > 0 else '\\'), float(np.degrees(np.arctan(abs(slope))))

# X, native pixels, reading frame
cells = R.cells(); xa, xb = [c[1:] for c in cells if c[0] == 'X'][0]
Xm = np.rot90(R.G[xa:xb + 1, R.XA:R.XB] < 130, k=-1)
lab, n = ndi.label(Xm, E8); Xm = lab == (np.bincount(lab.ravel())[1:].argmax() + 1)
print('1. STRUCTURE (endpoints, junctions, diagonal direction, diagonal angle from horizontal)')
e, j, d, a = structure(Xm); print(f'   X, master x{R.XA}..{R.XB - 1} y{xa}..{xb}, ink<130, reading frame: endpoints {e}, junctions {j}, diagonal {d} at {a:.0f} deg')
for ch, name in (('ᛅ', 'U+16C5 long-branch ar (Younger)'), ('ᚾ', 'U+16BE naudiz/naudr')):
    e, j, d, a = structure(render(ch)); print(f'   {ch} {name:32s} FreeMono: endpoints {e}, junctions {j}, diagonal {d} at {a:.0f} deg')

print('\n2. HARNESS (bbox -> 32x32, z-scored, Pearson)')
C = [(ch, norm32(np.rot90(R.G[y0:y1 + 1, R.XA:R.XB] < 130, k=-1))) for ch, y0, y1 in cells]
same = [corr(p[1], q[1]) for i, p in enumerate(C) for q in C[i + 1:] if p[0] == q[0]]
diff = [corr(p[1], q[1]) for i, p in enumerate(C) for q in C[i + 1:] if p[0] != q[0]]
print(f'   calibration on the right-edge column: same letter n={len(same)} mean {np.mean(same):+.3f} sd {np.std(same):.3f}; '
      f'different n={len(diff)} mean {np.mean(diff):+.3f} sd {np.std(diff):.3f}, 95th pct {np.percentile(diff, 95):+.3f}')
print('   (glyphX_measurement.md section 2, whole inscription: same +0.689, different +0.085, boundary about +0.45)')
Xn = norm32(Xm)
runes = sorted(set(YOUNGER + ELDER))
scores = sorted(((corr(Xn, norm32(render(ch))), ch) for ch in runes), reverse=True)
print(f'   X against {len(runes)} distinct runes (Younger + Elder Futhark) rendered in FreeMono; top 6:')
for s, ch in scores[:6]: print(f'      {ch}  U+{ord(ch):04X}  {s:+.3f}')
for ch in ('ᛅ', 'ᚾ'):
    rk = [c for _, c in scores].index(ch) + 1; s = dict((c, v) for v, c in scores)[ch]
    print(f'   {ch} U+{ord(ch):04X}: {s:+.3f}, rank {rk} of {len(runes)}')
print('   Font glyphs are not hand-drawn: a score is read against the calibration above, and rank matters more than size.')
