"""Task 4: the terminal glyph after 'номер' -- resolved or pixel-blocked?

Reproduces: the column's word-length signature; the glyph's native size,
contrast and clear margins; and the template calibration against every
labelled cell of its own column (pairwise tails on both sides, the
best-match statistic under both hypotheses, and the wrong-direction control).
"""
import numpy as np

from runelib import G, WORDS, groups, cells, mask, iou, d8, pair_scores

print("1. SEGMENTATION -- glyph groups between separators, top of column first")
gs = groups()
for g, w in zip(gs, WORDS + ["-"] * 9):
    n = len(w) if w != "-" else None
    print("   y%4d-%-4d  %2d glyphs   expected %-12s %s"
          % (g[0][0], g[-1][1], len(g), w, "OK" if n == len(g) else ""))

print("\n2. TERMINAL GLYPH at native resolution")
cell = G[37:57, 1526:1558]
ink = cell < 130
ys, xs = np.where(ink)
print("   ink bbox y%d-%d x%d-%d = %d x %d px, %d ink px"
      % (37 + ys.min(), 37 + ys.max(), 1526 + xs.min(), 1526 + xs.max(),
         ys.max() - ys.min() + 1, xs.max() - xs.min() + 1, ink.sum()))
bg = np.percentile(cell, 90)
print("   background %.0f, darkest %.0f -> contrast %.0f levels" % (bg, cell.min(), bg - cell.min()))
col = G[26:64, 1526:1558] < 130
rows = np.where(col.any(axis=1))[0] + 26
border_end = max(r for r in rows if r <= 36)
glyph_top, glyph_bot = 37 + ys.min(), 37 + ys.max()
sep_top = min(r for r in rows if r > glyph_bot)
print("   clear rows above (to border, y%d): %d   below (to separator, y%d): %d"
      % (border_end, glyph_top - border_end - 1, sep_top, sep_top - glyph_bot - 1))
print("   ink in titlo band y36-39: %d px" % (G[36:40, 1526:1558] < 130).sum())

print("\n3. TEMPLATE CALIBRATION on the 36 labelled cells of the same column")
cs = cells(reverse=True)
C = [mask(a, b) for _, a, b in cs]
lab = [ch for ch, _, _ in cs]
same, diff = pair_scores(C, lab)
print("   same-letter pairs n=%d  median %.2f  min %.2f" % (len(same), np.median(same), same.min()))
print("   diff-letter pairs n=%d  median %.2f  95th %.2f  max %.2f"
      % (len(diff), np.median(diff), np.percentile(diff, 95), diff.max()))

obs_any = max(max(iou(t, C[i]) for t in d8(C[0])) for i in range(1, len(C)))
obs = max(iou(C[0], C[i]) for i in range(1, len(C)))
top = sorted(((iou(C[0], C[i]), lab[i], cs[i][1]) for i in range(1, len(C))), reverse=True)[:3]
print("   terminal glyph best IoU: %.2f as drawn, %.2f over 8 orientations; top: %s"
      % (obs, obs_any, ", ".join("%s y%d %.2f" % (ch, y, s) for s, ch, y in top)))

print("\n4. WHERE THAT SCORE SITS")
print("   pairwise : <= %.1f%% of same-letter pairs; >= the %.1fth pct of diff-letter pairs"
      % (100 * (same <= obs).mean(), 100 * (diff < obs).mean()))
best_other, best_same = [], []
for i in range(1, len(C)):
    best_other.append(max(iou(C[i], C[j]) for j in range(1, len(C)) if j != i and lab[j] != lab[i]))
    partners = [iou(C[i], C[j]) for j in range(1, len(C)) if j != i and lab[j] == lab[i]]
    if partners:
        best_same.append(max(partners))
best_other, best_same = np.array(best_other), np.array(best_same)
print("   best-match, H0 letter absent from column: n=%d median %.2f range %.2f-%.2f  P(<=obs) %.0f%%"
      % (len(best_other), np.median(best_other), best_other.min(), best_other.max(),
         100 * (best_other <= obs).mean()))
print("   best-match, H1 letter repeats in column : n=%d median %.2f range %.2f-%.2f  P(<=obs) %.0f%%"
      % (len(best_same), np.median(best_same), best_same.min(), best_same.max(),
         100 * (best_same <= obs).mean()))
print("   (H1 entries are not independent: a letter with two instances contributes twice)")

print("\n5. CONTROL -- same masks, letters assigned in the WRONG reading direction")
lab_r = [ch for ch, _, _ in cells(reverse=False)]
same_r, diff_r = pair_scores(C, lab_r)
print("   correct : same median %.2f  diff median %.2f" % (np.median(same), np.median(diff)))
print("   reversed: same median %.2f  diff median %.2f" % (np.median(same_r), np.median(diff_r)))
