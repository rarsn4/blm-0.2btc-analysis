"""Baseline-free thin-line detector for the hand-copied 13th Amendment.

Window of W columns in one row: uniform (std <= 8) at handwriting darkness,
lighter by >= 10 one row above (window means). CLEAN if the row below is also
lighter by >= 10; SPRAY-ADJ if instead spray (<90) starts within 2 rows below,
which a T-crossbar's soft top edge can mimic, so those are inconclusive.
Positive control: the 'subject' underline, y902, x1402-1453.
Known false-positive mode: flat baselines where rounded letter bottoms touch
(y842 under 'servitude'), which have no lighter row between line and letters.
"""
import numpy as np

from imgio import load_gray

G = load_gray()
W = 10


def scan(x0, x1, y0, y1, label, hi=122, quiet=False):
    found = {}
    for y in range(y0 + 1, y1 - 2):
        for x in range(x0, x1 - W):
            ln, up = G[y, x:x + W], G[y - 1, x:x + W]
            dn, dn2 = G[y + 1, x:x + W], G[y + 2, x:x + W]
            if not (85 <= ln.mean() <= hi and ln.std() <= 8 and ln.max() <= hi + 10):
                continue
            if up.mean() - ln.mean() < 10:
                continue
            if dn.mean() - ln.mean() >= 10:
                kind = "CLEAN"
            elif min(dn.mean(), dn2.mean()) < 90:
                kind = "SPRAY-ADJ"
            else:
                continue
            found.setdefault((y, kind), []).append(x)
    runs = []
    for (y, kind), xs in found.items():
        xs.sort()
        s = p = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == p + 1:
                p = x
                continue
            runs.append((y, s, p + W - 1, kind))
            if x is not None:
                s = p = x
    runs.sort()
    if not quiet:
        print("%s  x%d-%d y%d-%d : %d runs" % (label, x0, x1, y0, y1, len(runs)))
        for y, s, e, kind in runs:
            print("   y%d  x%d-%d  len %2d  %s" % (y, s, e, e - s + 1, kind))
    return runs


if __name__ == "__main__":
    scan(1296, 1496, 800, 918, "AMENDMENT BLOCK")
