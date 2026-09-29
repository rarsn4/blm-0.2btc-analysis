"""Premise audit, image side: two dated elements.

1. The date on the portrait's hoodie: tight crop, contrast.
2. The gold chart (top left): gridline spacing, the drawn 2011 peak, and where
   the series ends. The series is a light line on a starred sky, so the peak
   windows are kept tight around the spikes; a loose window picks up star and
   figure edges instead.

External fact used in the interpretation (not computed here): gold's monthly
price first exceeded its 2011 high in July 2020.

With --onchain, also re-fetches the funding transaction from mempool.space.
"""
import sys

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from imgio import load_gray

G = load_gray()

print("1. HOODIE DATE (x988-1072, y366-388)")
sub = G[366:388, 988:1072]
ink = sub < 80
bgv = np.median(sub[sub >= 100])
print("   ink (<80) px %d, ink median %.0f, darkest %.0f; background median %.0f -> contrast %.0f levels"
      % (ink.sum(), np.median(sub[ink]), sub.min(), bgv, bgv - np.median(sub[ink])))
cols = ink.sum(axis=0)
runs, s = [], None
for i, v in enumerate(cols):
    if v and s is None:
        s = i
    elif not v and s is not None:
        runs.append((988 + s, 988 + i - 1))
        s = None
print("   ink column runs: %s  (reads 05.25.20 on inspection)" % runs)

print("\n2. GOLD CHART")
strip = G[180:450, 330:380]
rm = strip.mean(axis=1)
base = np.convolve(rm, np.ones(9) / 9, mode="same")
grid = [180 + i for i in range(2, len(rm) - 2)
        if base[i] - rm[i] > 10 and rm[i] <= rm[i - 1] and rm[i] <= rm[i + 1]]
print("   gridline rows (x330-380, depth > 10): %s" % grid)
step = np.median(np.diff(grid))
print("   median spacing %.1f px per gridline step" % step)


def line_top(x0, x1, y0, y1):
    """Topmost pixel of the light series line: brighter than its 7x7 local median by > 18."""
    s = G[y0:y1, x0:x1]
    med = np.median(sliding_window_view(np.pad(s, 3, mode="edge"), (7, 7)), axis=(2, 3))
    ys, xs = np.where((s - med) > 18)
    i = np.argmin(ys)
    return y0 + ys[i], x0 + xs[i]


y11, x11 = line_top(236, 246, 240, 300)       # the 2011 spike only
yend, xend = line_top(448, 462, 215, 300)     # the final rise and hook
top = grid[0] if base[grid[0] - 180] - rm[grid[0] - 180] > 10 else grid[1]
print("   top gridline (labelled ..800, i.e. 1800 behind the axis bar): y%d" % top)
print("   drawn 2011 peak : x%d y%d" % (x11, y11))
print("   drawn final peak: x%d y%d  -> %d px above the 2011 peak = %.1f gridline steps"
      % (xend, yend, y11 - yend, (y11 - yend) / step))
print("   with 1800 at y%d and $200 per step: 2011 peak ~$%.0f, final peak ~$%.0f"
      % (top, 1800 + (top - y11) * 200 / step, 1800 + (top - yend) * 200 / step))

if "--onchain" in sys.argv:
    import json
    import urllib.request
    url = "https://mempool.space/api/tx/fcee21d44ee94c09869947c74b61669bf928358e9c2d1699fb075bb6ebf5d043"
    tx = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "blm-audit"})))
    print("\n3. FUNDING TX: version %d, locktime %d, block %d, block_time %d, sequences %s, outputs %s"
          % (tx["version"], tx["locktime"], tx["status"]["block_height"], tx["status"]["block_time"],
             sorted({"0x%08x" % i["sequence"] for i in tx["vin"]}),
             [(o["scriptpubkey_type"], o["value"]) for o in tx["vout"]]))
