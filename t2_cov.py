"""Task 2: is the circled mark under BLM (on the card Liberty holds) at the
resolution limit?

Peak stroke coverage: a stroke narrower than one pixel never reaches the pen's
full darkness, so (bg - darkest) / (bg - pen) estimates the widest stroke's
width in pixels, capped at 1. Below 1, adjacent strokes merge and a junction
reads the same as a near-miss. Pen value comes from the BLM capitals on the
same card; the circle is located by fitting, not by eye.
"""
import numpy as np
from PIL import Image

from imgio import load_gray, image_path

G = load_gray()
H, W = G.shape

# locate the circle: the ring that is darkest RELATIVE to its inner and outer
# neighbours (a plain 'darkest ring' objective is pulled onto the black hand and
# the BLM underline at the upper right, which are dark but not ring-shaped)
th = np.linspace(0, 2 * np.pi, 120, endpoint=False)


def ringval(cx, cy, r):
    x = np.rint(cx + r * np.sin(th)).astype(int)
    y = np.rint(cy - r * np.cos(th)).astype(int)
    return G[y, x].mean()


RS, XS, YS = np.arange(7.0, 12.01, 0.25), np.arange(256.0, 274.01, 0.5), np.arange(750.0, 770.01, 0.5)
best = (1e9, None)
for r in RS:
    for cx in XS:
        for cy in YS:
            c = ringval(cx, cy, r) - 0.5 * (ringval(cx, cy, r - 2.5) + ringval(cx, cy, r + 2.5))
            if c < best[0]:
                best = (c, (cx, cy, r))
contrast, (cx, cy, R) = best
edge = cx in (XS[0], XS[-1]) or cy in (YS[0], YS[-1]) or R in (RS[0], RS[-1])
print("circle fit: centre (%.1f, %.1f)  radius %.2f  -> diameter %.1f px  (ring %.0f levels darker than "
      "its neighbours)%s" % (cx, cy, R, 2 * R, -contrast, "  ** ON GRID EDGE -- fit not trusted **" if edge else ""))

card = G[745:775, 250:282]
bg = np.percentile(card, 95)
pen = G[722:742, 262:292].min()           # BLM strokes, same card, same pass
print("card background (95th pct) %.0f ; pen value from BLM capitals %.0f" % (bg, pen))

yy, xx = np.mgrid[0:H, 0:W]
win = (slice(int(cy) - 14, int(cy) + 15), slice(int(cx) - 14, int(cx) + 15))
rr = np.hypot(yy[win] - cy, xx[win] - cx)
sub = G[win]
inner = rr < R - 2.0
ring = np.abs(rr - R) <= 1.5
faint = sub < bg - 0.25 * (bg - pen)
iy, ix = np.where(faint & inner)
print("interior mark extent (darker than bg - 25%% of pen depth, r < R-2): %d x %d px"
      % (ix.max() - ix.min() + 1, iy.max() - iy.min() + 1))
for name, m in (("interior mark", inner), ("ring", ring)):
    d = sub[m].min()
    print("%-14s darkest %3.0f  peak coverage %.2f px  pixels past half-pen darkness: %d"
          % (name, d, (bg - d) / (bg - pen), (sub[m] < bg - 0.5 * (bg - pen)).sum()))
blm = G[722:742, 262:292]
print("%-14s pixels past half-pen darkness: %d  (legible control, same card)"
      % ("BLM capitals", (blm < bg - 0.5 * (bg - pen)).sum()))
rune = G[37:57, 1526:1558]
print("%-14s darkest %3.0f  (resolved control; strokes 3-4 px)" % ("rune glyph", rune.min()))

# the artist's own fist emblem (the O of STOP), redrawn at this circle's size
stop = Image.open(image_path()).convert("L").crop((72, 456, 137, 527))
n = int(round(2 * R))
small = np.asarray(stop.resize((n, n), Image.BOX)).astype(np.float32)
sy, sx = np.mgrid[0:n, 0:n]
srr = np.hypot(sy - (n - 1) / 2, sx - (n - 1) / 2)
print("\nSTOP emblem %dx%d px box-averaged to %d px: interior pixels < 90: %d"
      % (stop.size[0], stop.size[1], n, (small[srr < R - 3.5] < 90).sum()))
print("card mark, same interior radius:               pixels < 90: %d"
      % (sub[rr < R - 3.5] < 90).sum())
