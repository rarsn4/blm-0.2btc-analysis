"""Slot 20: can the ink decide between `apple` and `second`?

Neither word is written or encoded anywhere in the image (letter census,
census_crops.py). The README derives slot 20 from two physical features only:
the 'XX' on the hooded head of the Leopold II bust (-> the number 20) and, for
the word `second`, the fact that Leopold II was the second King of the
Belgians. `apple` has no derivation in the README at all. This script
measures the two features:

1. the wreath plaque below the bust: is there an in-image 'II'?
2. the two X marks on the head: are they spaced like numeral letters or like eyes?
   Reference: letter gaps in the artist's own FUCK THIS SHIT lettering.
"""
import numpy as np

from imgio import load_gray

G = load_gray()

print("1. WREATH PLAQUE (outer frame x1380/x1402, y692/y709-710)")
print("   column means over the panel rows y697-706 (panel light ~150-160):")
for x in range(1381, 1402):
    print("     x%d  %5.1f" % (x, G[697:707, x].mean()))
print("   vertical extent of each stroke column (value < 135), panel rows y696-708:")
for x in (1386, 1387, 1389, 1390, 1392, 1393, 1395, 1398):
    runs, s = [], None
    for y in range(696, 709):
        on = G[y, x] < 135
        if on and s is None:
            s = y
        elif not on and s is not None:
            runs.append((s, y - 1))
            s = None
    if s is not None:
        runs.append((s, 708))
    print("     x%d  %s  min %3.0f" % (x, " ".join("y%d-%d" % r for r in runs), G[696:709, x].min()))

print("\n2. X MARKS ON THE HEAD")
y0, y1, x0, x1 = 430, 490, 1345, 1425
ink = G[y0:y1, x0:x1] < 90
lab = np.zeros(ink.shape, int)
n = 0
for sy, sx in zip(*np.where(ink)):
    if lab[sy, sx]:
        continue
    n += 1
    lab[sy, sx] = n
    stack = [(sy, sx)]
    while stack:
        cy, cx = stack.pop()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                yy, xx = cy + dy, cx + dx
                if 0 <= yy < ink.shape[0] and 0 <= xx < ink.shape[1] and ink[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n
                    stack.append((yy, xx))
comps = []
for k in range(1, n + 1):
    ys, xs = np.where(lab == k)
    if len(ys) >= 40:
        comps.append((x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max(), len(ys),
                      G[y0:y1, x0:x1][lab == k].min()))
comps.sort()
bg = np.percentile(G[y0:y1, 1360:1420], 90)
for c in comps:
    print("   mark x%d-%d y%d-%d  %d x %d px  %d ink px  darkest %.0f  (background %.0f)"
          % (c[0], c[1], c[2], c[3], c[1] - c[0] + 1, c[3] - c[2] + 1, c[4], c[5], bg))
a, b = comps[0], comps[1]
wl = a[1] - a[0] + 1
gap = b[0] - a[1] - 1
print("   gap between marks %d px = %.2f x the left mark's width (%d px; the right mark"
      " touches the head outline, so only the left width is clean)" % (gap, gap / wl, wl))

print("\n3. REFERENCE: letter gaps in the artist's SHIT lettering (spray < 80, full letter height)")
for word, ya, yb, xa, xb in (("SHIT", 903, 990, 1318, 1462),):
    prof = (G[ya:yb, xa:xb] < 80).sum(axis=0)
    runs, s = [], None
    for i, v in enumerate(prof):
        if v >= 3 and s is None:
            s = i
        elif v < 3 and s is not None:
            runs.append((xa + s, xa + i - 1))
            s = None
    if s is not None:
        runs.append((xa + s, xb - 1))
    runs = [r for r in runs if r[1] - r[0] >= 3]
    widths = [e - s + 1 for s, e in runs]
    gaps = [runs[i + 1][0] - runs[i][1] - 1 for i in range(len(runs) - 1)]
    narrow = [g / min(widths[i], widths[i + 1]) for i, g in enumerate(gaps)]
    wide = [g / max(widths[i], widths[i + 1]) for i, g in enumerate(gaps)]
    print("   %s rows y%d-%d: letter widths %s  gaps %s" % (word, ya, yb, widths, gaps))
    print("   gap / narrower letter %s   gap / wider letter %s"
          % (["%.2f" % r for r in narrow], ["%.2f" % r for r in wide]))
print("   X marks: gap / left mark (17 px) = %.2f; the marks are the same shape, so there is"
      " no narrower/wider distinction to make" % (gap / wl))
