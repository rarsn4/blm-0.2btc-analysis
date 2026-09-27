"""Right-edge rune column: segmentation, labelling and mask comparison.
Native pixels only; nothing is resampled before measurement."""
import numpy as np

from imgio import load_gray

G = load_gray()
XA, XB = 1526, 1557
WORDS = ["X", "номер", "день", "чёрный", "на", "биткоины", "зашифрованы"]


def groups(y0=36, y1=1000):
    """Glyph runs between three-dot separators, top of the column first."""
    prof = (G[y0:y1, XA:XB] < 130).sum(axis=1)
    runs, s = [], None
    for i, v in enumerate(prof):
        if v > 0 and s is None:
            s = i
        elif v == 0 and s is not None:
            runs.append((y0 + s, y0 + i - 1, i - s, int(prof[s:i].max())))
            s = None
    out, cur = [], []
    for a, b, L, mx in runs:
        if L <= 5 and mx <= 12:          # three-dot separator
            out.append(cur)
            cur = []
        else:
            cur.append((a, b))
    out.append(cur)
    return [g for g in out if g]


def cells(reverse=True):
    """(letter, y0, y1). reverse=True: bottom cell of each word is its first letter."""
    res = []
    for g, w in zip(groups()[:7], WORDS):
        assert len(g) == len(w), (w, len(g))
        letters = list(w)[::-1] if reverse else list(w)
        res += [(ch, a, b) for (a, b), ch in zip(g, letters)]
    return res


def mask(a, b, xa=XA, xb=XB, thr=130, size=34):
    m = G[a:b + 1, xa:xb] < thr
    ys, xs = np.where(m)
    m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    c = np.zeros((size, size), bool)
    oy, ox = (size - m.shape[0]) // 2, (size - m.shape[1]) // 2
    c[oy:oy + m.shape[0], ox:ox + m.shape[1]] = m
    return c


def iou(p, q, shift=3):
    best = 0.0
    for dy in range(-shift, shift + 1):
        for dx in range(-shift, shift + 1):
            r = np.roll(np.roll(q, dy, 0), dx, 1)
            u = (p | r).sum()
            if u:
                best = max(best, (p & r).sum() / u)
    return best


def d8(m):
    out = []
    for k in range(4):
        r = np.rot90(m, k)
        out += [r, np.fliplr(r)]
    return out


def pair_scores(C, lab):
    same, diff = [], []
    for i in range(1, len(C)):
        for j in range(i + 1, len(C)):
            (same if lab[i] == lab[j] else diff).append(iou(C[i], C[j]))
    return np.array(same), np.array(diff)
