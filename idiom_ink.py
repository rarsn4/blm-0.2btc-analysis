"""Is 'чёрный день' set apart in the ink of the right-edge inscription?

For every word group and every three-dot separator in the column (x1526-1557,
reading bottom-to-top): separator dot count and geometry, the clear gaps on
either side of each separator, glyph size and stroke darkness per word,
letter spacing inside each word, and any ink beside the column next to each
word (a mark set to one side, the vertical-text equivalent of an underline).
"""
import numpy as np

from imgio import load_gray

G = load_gray()
XA, XB, Y0, Y1 = 1526, 1557, 36, 1000
WORDS_TOP_DOWN = ["X", "номер", "день", "чёрный", "на", "биткоины", "зашифрованы"]


def components(mask):
    lab = np.zeros(mask.shape, int)
    n = 0
    for sy, sx in zip(*np.where(mask)):
        if lab[sy, sx]:
            continue
        n += 1
        lab[sy, sx] = n
        st = [(sy, sx)]
        while st:
            cy, cx = st.pop()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = cy + dy, cx + dx
                    if 0 <= yy < mask.shape[0] and 0 <= xx < mask.shape[1] and mask[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n
                        st.append((yy, xx))
    return [np.argwhere(lab == k) for k in range(1, n + 1)]


prof = (G[Y0:Y1, XA:XB] < 130).sum(axis=1)
runs, s = [], None
for i, v in enumerate(prof):
    if v > 0 and s is None:
        s = i
    elif v == 0 and s is not None:
        runs.append((Y0 + s, Y0 + i - 1, int(prof[s:i].max())))
        s = None
items = []   # ('sep'|'glyph', y0, y1)
for a, b, mx in runs:
    items.append(("sep" if (b - a + 1) <= 5 and mx <= 12 else "glyph", a, b))

# group glyphs into words
words, cur = [], []
seps = []
for k, (kind, a, b) in enumerate(items):
    if kind == "sep":
        if cur:
            words.append(cur)
            cur = []
        seps.append((k, a, b))
    else:
        cur.append((a, b))
if cur:
    words.append(cur)

print("1. SEPARATORS (top to bottom), with the clear rows on each side")
print("   %-22s %-10s %-5s %-24s %s" % ("between (reading order)", "rows", "dots", "dot x-centres", "gap above / below"))
for n, (k, a, b) in enumerate(seps):
    dots = components(G[a:b + 1, 1518:1557] < 150)
    dots = [d for d in dots if len(d) >= 2]
    xs = sorted(round(1518 + d[:, 1].mean(), 1) for d in dots)
    above = a - items[k - 1][2] - 1 if k > 0 else None
    below = items[k + 1][1] - b - 1 if k + 1 < len(items) else None
    lower = WORDS_TOP_DOWN[n + 1] if n + 1 < len(WORDS_TOP_DOWN) else "?"
    upper = WORDS_TOP_DOWN[n] if n < len(WORDS_TOP_DOWN) else "?"
    print("   %-22s y%d-%-5d %-5d %-24s %s / %s" % ("%s | %s" % (lower, upper), a, b, len(dots), xs, above, below))

print("\n2. WORDS: glyph size, darkness, spacing (reading order is bottom-to-top)")
print("   %-12s %6s %8s %8s %9s %9s %s" % ("word", "glyphs", "mean h", "mean w", "ink/glyph", "ink mean", "letter gaps (rows)"))
stats = []
for w, g in zip(WORDS_TOP_DOWN, words):
    hs, ws, inks, means = [], [], [], []
    for a, b in g:
        m = G[a:b + 1, XA:XB] < 130
        ys, xs = np.where(m)
        hs.append(b - a + 1)
        ws.append(xs.max() - xs.min() + 1)
        inks.append(m.sum())
        means.append(G[a:b + 1, XA:XB][m].mean())
    gaps = [g[i + 1][0] - g[i][1] - 1 for i in range(len(g) - 1)]
    stats.append((w, np.mean(hs), np.mean(ws), np.mean(inks), np.mean(means), gaps))
    print("   %-12s %6d %8.1f %8.1f %9.1f %9.1f %s" % (w, len(g), np.mean(hs), np.mean(ws), np.mean(inks), np.mean(means), gaps))
allg = [x for s in stats for x in s[5]]
print("   all within-word letter gaps: median %.1f, range %d-%d" % (np.median(allg), min(allg), max(allg)))
for label, idx in (("mean glyph height", 1), ("mean glyph width", 2), ("ink px per glyph", 3), ("ink darkness", 4)):
    v = np.array([s[idx] for s in stats])
    z = {s[0]: (s[idx] - v.mean()) / v.std() for s in stats}
    print("   z-score of %-18s чёрный %+.2f  день %+.2f  (others %s)" % (
        label, z["чёрный"], z["день"],
        ", ".join("%s %+.2f" % (k, z[k]) for k in z if k not in ("чёрный", "день"))))

print("\n3. INK BESIDE THE COLUMN next to each word (x1508-1525, left of the glyphs; pixels < 150)")
for w, g in zip(WORDS_TOP_DOWN, words):
    a, b = g[0][0], g[-1][1]
    side = G[a:b + 1, 1508:1526] < 150
    print("   %-12s y%d-%-4d  side ink %3d px over %d rows" % (w, a, b, side.sum(), b - a + 1))
print("   (the only non-zero entry, beside 'номер', is the CCTV camera's body at x1470-1515)")

print("\n4. CONTROL for 'номер': the same letter inside it vs elsewhere in the column (glyph height, rows)")
bounds = [(w, g[0][0], g[-1][1]) for w, g in zip(WORDS_TOP_DOWN, words)]
labelled = []
for w, g in zip(WORDS_TOP_DOWN, words):
    for (a, b), ch in zip(g, list(w)[::-1]):          # bottom cell = first letter
        labelled.append((ch, w, b - a + 1))
for ch in "номер":
    inside = [h for c, w, h in labelled if c == ch and w == "номер"]
    out = ["%d (%s)" % (h, w) for c, w, h in labelled if c == ch and w != "номер"]
    print("   %s  in номер %s   elsewhere %s" % (ch, inside, ", ".join(out) or "none"))


def segment_row(y0, y1, x0, x1, thr):
    """Horizontal text: runs along x; a separator is <=4 px wide made of >=2 short vertical dots."""
    band = G[y0:y1, x0:x1] < thr
    pr = band.sum(axis=0)
    rr, s0 = [], None
    for i, v in enumerate(pr):
        if v and s0 is None:
            s0 = i
        elif not v and s0 is not None:
            rr.append((s0, i - 1))
            s0 = None
    if s0 is not None:
        rr.append((s0, len(pr) - 1))
    out = []
    for a, b in rr:
        sub = band[:, a:b + 1]
        vr, vs = [], None
        for i in range(sub.shape[0]):
            on = sub[i].any()
            if on and vs is None:
                vs = i
            elif not on and vs is not None:
                vr.append(i - vs)
                vs = None
        if vs is not None:
            vr.append(sub.shape[0] - vs)
        rows = np.where(sub.any(axis=1))[0]
        sep = (b - a + 1) <= 4 and len(vr) >= 2 and max(vr) <= 3
        out.append((sep, x0 + a, x0 + b, rows.max() - rows.min() + 1, G[y0:y1, x0 + a:x0 + b + 1][sub].mean(), len(vr)))
    return out


print("\n5. THE OTHER TWO INSCRIPTIONS: separators, and per-word glyph height / darkness")
INS = [("top-left 1", 44, 64, 200, 450, 170, ["Я", "надеюсь", "что", "сюда"]),
       ("top-left 2", 69, 87, 200, 450, 170, ["будут", "присылать"]),
       ("top-left 3", 90, 109, 200, 450, 170, ["много", "биткоинов"]),
       ("clock", 1024, 1040, 262, 466, 215, ["сумма", "двух", "чисел"])]
per = []
for name, y0, y1, x0, x1, thr, ws in INS:
    seg = segment_row(y0, y1, x0, x1, thr)
    seps = [k for k in seg if k[0]]
    print("   %-10s %d separators for %d word boundaries: %s" % (
        name, len(seps), len(ws) - 1, ", ".join("x%d-%d (%d dots, h%d)" % (k[1], k[2], k[5], k[3]) for k in seps)))
    wi = 0
    acc = {w: [] for w in ws}
    for k in seg:
        if k[0]:
            wi += 1
        else:
            acc[ws[wi]].append((k[3], k[4]))
    for w in ws:
        per.append((name.split()[0], w, np.mean([h for h, _ in acc[w]]), np.mean([d for _, d in acc[w]])))
for grp in ("top-left", "clock"):
    sub = [p for p in per if p[0] == grp]
    H = np.array([p[2] for p in sub])
    D = np.array([p[3] for p in sub])
    print("   %s: " % grp + "; ".join("%s h%.1f (z%+.1f) ink%.0f (z%+.1f)" % (
        p[1], p[2], (p[2] - H.mean()) / H.std(), p[3], (p[3] - D.mean()) / D.std()) for p in sub))
print("   (top-left variation follows the LINE: line 1 ~15 px, lines 2-3 ~12-13 px)")
