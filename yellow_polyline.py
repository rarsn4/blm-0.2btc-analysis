"""The yellow polyline in the top band, measured as a structure.

Native pixels on the master, sha256 d0b04378...a782 (1600x1200). No upscaled view
enters the numbers below; the magnified renders were used only to decide where to
point the measurements, per REPORT 9's rule.

Yellowness Y = min(R,G) - B. Paper sits at Y 0-1, the device's ink at Y 20-142,
so the threshold Y>=20 is not a judgement call -- there is nothing in between.

Outputs, in order:
  1. every connected component of the device, and the closure proof that the
     component list IS the device (pixel budget, and a sweep for the same hue
     elsewhere in the artwork)
  2. the sixteen corner brackets and the four box rectangles
  3. the five ruled runs, least-squares, with residuals
  4. the collinearity test across 'Order and stability'
  5. clearances to every neighbouring element
"""
import math
import numpy as np
from PIL import Image

MASTER = "0.2-btc-puzzle.png"

# The device, as fourteen 8-connected components at Y>=20 plus the two i-dots.
# Labels are assigned by the scan order in components(); see the printout.
BRACKET = {
    "A.TL": (116, 138,  55,  74), "A.TR": (167, 185,  55,  74),
    "A.BL": (116, 137, 113, 136), "A.BR": (166, 184, 113, 136),
    "B.TL": (252, 268, 139, 151), "B.TR": (297, 309, 139, 151),
    "B.BL": (252, 268, 188, 200), "B.BR": (297, 309, 188, 200),
    "C.TL": (382, 397,  92, 114), "C.TR": (430, 445,  93, 115),
    "C.BL": (381, 397, 156, 174), "C.BR": (430, 445, 156, 174),
    "D.TL": (473, 481, 100, 115), "D.TR": (512, 522, 100, 115),
    "D.BL": (473, 481, 151, 164), "D.BR": (512, 522, 151, 165),
}
BOX = {"A": (116, 185, 55, 136), "B": (252, 309, 139, 200),
       "C": (381, 445, 92, 174), "D": (473, 522, 100, 165)}

# (name, fit window, y window, left end, right end) -- the fit windows exclude the
# brackets and the cursive, so each fit is over clean single-stroke columns only.
RUN = [("seg1  A -> B",   192,  246, 115, 155, 185,  252),
       ("seg2  B -> C",   315,  375, 100, 150, 309,  381),
       ("seg3  C -> D",   449,  470, 100, 114, 445,  473),
       ("L1    D -> word", 527,  640, 100, 118, 522,  674),
       ("L2    word -> lens", 1100, 1300, 86, 102, 994, 1320)]


def yellowness(path=MASTER):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    return a, np.minimum(a[:, :, 0], a[:, :, 1]) - a[:, :, 2]


def components(Y, T=20):
    from collections import deque
    m = Y >= T
    H, W = m.shape
    lab = np.zeros((H, W), np.int32)
    cur = 0
    out = []
    nbr = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for y0, x0 in zip(*np.nonzero(m)):
        if lab[y0, x0]:
            continue
        cur += 1
        q = deque([(y0, x0)])
        lab[y0, x0] = cur
        px = []
        while q:
            y, x = q.popleft()
            px.append((y, x))
            for dy, dx in nbr:
                ny, nx = y + dy, x + dx
                if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = cur
                    q.append((ny, nx))
        p = np.array(px)
        out.append((cur, len(px), int(p[:, 1].min()), int(p[:, 1].max()),
                    int(p[:, 0].min()), int(p[:, 0].max())))
    return lab, out


def centroid_fit(Y, x0, x1, ylo, yhi, T=20):
    xs, ys = [], []
    for x in range(x0, x1 + 1):
        col = Y[ylo:yhi + 1, x].astype(float).copy()
        col[col < T] = 0
        if col.sum() <= 0:
            continue
        xs.append(x)
        ys.append((np.arange(ylo, yhi + 1) * col).sum() / col.sum())
    xs, ys = np.array(xs, float), np.array(ys)
    a, b = np.polyfit(xs, ys, 1)
    r = ys - (a * xs + b)
    return a, b, r.std(), np.abs(r).max(), len(xs)


def _blobs(m):
    """8-connected components of a boolean mask, as arrays of (y, x)."""
    from collections import deque
    H, W = m.shape
    seen = np.zeros_like(m)
    out = []
    for y0, x0 in zip(*np.nonzero(m)):
        if seen[y0, x0]:
            continue
        q, grp = deque([(y0, x0)]), []
        seen[y0, x0] = True
        while q:
            y, x = q.popleft()
            grp.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if (0 <= ny < H and 0 <= nx < W and m[ny, nx] and not seen[ny, nx]):
                        seen[ny, nx] = True
                        q.append((ny, nx))
        out.append(np.array(grp))
    return out


def main():
    a, Y = yellowness()
    lab, comps = components(Y)

    # ---- 1. the device, and the proof that this is all of it -----------------
    device = [c for c in comps
              if c[1] >= 10 and c[4] < 210 and c[2] >= 110 and c[3] <= 1325]
    ids = [c[0] for c in device]
    poly = np.isin(lab, ids)
    print("1. THE DEVICE")
    for cid, n, x0, x1, y0, y1 in sorted(device, key=lambda c: c[2]):
        print(f"   comp {cid:3d}  n={n:5d}  x {x0:4d}..{x1:4d}  y {y0:3d}..{y1:3d}")
    print(f"   {len(device)} components, {int(poly.sum())} px")
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    stray = (R > 180) & (R - B > 60) & (G - B > 50) & (np.abs(R - G) < 30) & ~poly
    ys, xs = np.nonzero(stray)
    print(f"   same-hue ink elsewhere in the artwork: {len(xs)} px"
          + (f", all within x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}"
             if len(xs) else ""))

    # ---- 2. brackets and boxes ----------------------------------------------
    print("\n2. SIXTEEN BRACKETS, FOUR OPEN BOXES")
    for k, (x0, x1, y0, y1) in BOX.items():
        w, h = x1 - x0, y1 - y0
        gaps = []
        for name, (ax0, ax1, ay0, ay1) in (
                ("top", (x0, x1, y0 - 2, y0 + 4)), ("bottom", (x0, x1, y1 - 4, y1 + 2)),
                ("left", (x0 - 2, x0 + 4, y0, y1)), ("right", (x1 - 4, x1 + 2, y0, y1))):
            band = Y[ay0:ay1 + 1, ax0:ax1 + 1]
            cov = band.max(0) >= 20 if name in ("top", "bottom") else band.max(1) >= 20
            g = c = 0
            for v in cov:
                c = 0 if v else c + 1
                g = max(g, c)
            gaps.append(f"{name} {g}")
        inside = np.zeros_like(poly)
        inside[y0:y1 + 1, x0:x1 + 1] = True
        for bk, (bx0, bx1, by0, by1) in BRACKET.items():
            if bk[0] == k:
                inside[by0 - 3:by1 + 4, bx0 - 3:bx1 + 4] = False
        print(f"   box {k}: x {x0}..{x1} y {y0}..{y1}  {w}x{h} px  centre "
              f"({(x0+x1)/2:.1f},{(y0+y1)/2:.1f})  open gaps: {', '.join(gaps)}  "
              f"ink inside, outside the brackets: {int((poly & inside).sum())} px")

    # ---- 3. the five ruled runs ---------------------------------------------
    print("\n3. FIVE RULED RUNS")
    fits, total = {}, 0.0
    for name, fx0, fx1, ylo, yhi, ex0, ex1 in RUN:
        s, b, rms, mx, n = centroid_fit(Y, fx0, fx1, ylo, yhi)
        fits[name] = (s, b)
        y0, y1 = s * ex0 + b, s * ex1 + b
        L = math.hypot(ex1 - ex0, y1 - y0)
        total += L
        print(f"   {name:18s} ({ex0:4d},{y0:6.1f}) -> ({ex1:4d},{y1:6.1f})  len {L:6.1f} px"
              f"  bearing {math.degrees(math.atan(s)):+6.2f} deg"
              f"  fit rms {rms:.3f} px, max|r| {mx:.2f} (n={n})")
    print(f"   ruled length {total:.1f} px; the cursive spans x 674..994 between L1 and L2")
    order = [r[0] for r in RUN]
    print("   turns:", ", ".join(
        f"{math.degrees(math.atan(fits[order[i]][0])) - math.degrees(math.atan(fits[order[i-1]][0])):+.2f} deg"
        for i in range(1, 5)))

    # ---- 4. is the stroke under the words one line passing behind them? -----
    print("\n4. COLLINEARITY ACROSS 'Order and stability'")
    (s1, b1), (s2, b2) = fits["L1    D -> word"], fits["L2    word -> lens"]
    print(f"   L1 extended to x=1320: y={s1*1320+b1:.2f} vs L2's {s2*1320+b2:.2f}"
          f"   ({s1*1320+b1-(s2*1320+b2):+.2f} px)")
    print(f"   L2 extended to x= 523: y={s2*523+b2:.2f} vs L1's {s1*523+b1:.2f}"
          f"   ({s2*523+b2-(s1*523+b1):+.2f} px)")
    gap = [x for x in range(505, 1330) if not (Y[85:120, x] >= 20).any()]
    print(f"   columns with no device ink between x=505 and x=1329: "
          f"{gap if gap else 'none in x 512..1320'}")

    # ---- 5. clearances -------------------------------------------------------
    print("\n5. CLEARANCES")
    g = a.mean(2)
    py, px = np.nonzero(poly)

    def clear(name, x0, x1, y0, y1, thr, extra=None):
        sub = (g[y0:y1, x0:x1] < thr) if extra is None else extra[y0:y1, x0:x1]
        ys, xs = np.nonzero(sub)
        if not len(xs):
            print(f"   {name}: no ink")
            return
        ys, xs = ys + y0, xs + x0
        best, at, to = 1e18, None, None
        for yy, xx in zip(ys, xs):
            d2 = (py - yy) ** 2 + (px - xx) ** 2
            i = int(d2.argmin())
            if d2[i] < best:
                best, at, to = d2[i], (int(xx), int(yy)), (int(px[i]), int(py[i]))
        print(f"   {name:34s} n={len(xs):5d}  min clearance {math.sqrt(best):5.1f} px"
              f"   {at} -> device{to}")

    clear("rune line 3 (x245-377)", 245, 378, 84, 106, 170)
    clear("rune line 2", 250, 400, 56, 84, 170)
    clear("rune line 1", 240, 420, 30, 56, 170)
    sat = ((a.max(2) - a.min(2)) > 40) & ~poly
    clear("slogan block (coloured caps)", 1080, 1270, 85, 300, 0, sat)
    clear("camera body and lens", 1280, 1400, 60, 140, 160)

    # the lens element the line stops on
    from collections import deque
    win = g[66:122, 1294:1348] < 105
    seen = np.zeros_like(win)
    for y0, x0 in zip(*np.nonzero(win)):
        if seen[y0, x0]:
            continue
        q, grp = deque([(y0, x0)]), []
        seen[y0, x0] = True
        while q:
            y, x = q.popleft()
            grp.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if (0 <= ny < win.shape[0] and 0 <= nx < win.shape[1]
                            and win[ny, nx] and not seen[ny, nx]):
                        seen[ny, nx] = True
                        q.append((ny, nx))
        gg = np.array(grp)
        if (len(gg) >= 50 and 1308 <= 1294 + gg[:, 1].mean() <= 1332
                and 80 <= 66 + gg[:, 0].mean() <= 96):
            cx, cy = 1294 + gg[:, 1].mean(), 66 + gg[:, 0].mean()
            print(f"   lens element: x {1294+gg[:,1].min()}..{1294+gg[:,1].max()} "
                  f"y {66+gg[:,0].min()}..{66+gg[:,0].max()}  centroid ({cx:.1f},{cy:.1f})")
            lx = max(x for x in range(1300, 1340) if (Y[85:100, x] >= 20).any())
            col = np.nonzero(Y[85:100, lx] >= 20)[0] + 85
            ly = (col.min() + col.max()) / 2
            print(f"   line terminus ({lx},{ly:.1f})  ->  {math.hypot(lx-cx, ly-cy):.1f} px "
                  f"from the lens centroid; nothing beyond x={lx}")

    # ---- 6. is a numeral drawn inside any box? ------------------------------
    print("\n6. COMPACT DARK MARKS INSIDE THE BOXES")
    for k, (x0, x1, y0, y1) in BOX.items():
        sub = g[y0:y1 + 1, x0:x1 + 1]
        strict, loose = _blobs(sub < 140), _blobs(sub < 175)
        face = set(map(tuple, max(loose, key=len)))
        compact = [c for c in strict if 6 <= len(c) <= 400
                   and c[:, 1].ptp() <= 30 and c[:, 0].ptp() <= 30]
        free = [c for c in compact if not any(tuple(p) in face for p in c)]
        print(f"   box {k}: {len(compact)} compact marks, {len(free)} not connected to "
              f"the face line-work:")
        for c in free:
            print(f"      x {x0+c[:,1].min():4d}..{x0+c[:,1].max():4d} "
                  f"y {y0+c[:,0].min():4d}..{y0+c[:,0].max():4d}  n={len(c)}")

    # arrowheads
    print("\n   stroke width, perpendicular, by run (no end widens -> no arrowhead):")
    for name, fx0, fx1, ylo, yhi, _, _ in RUN:
        s = fits[name][0]
        w = np.array([(Y[ylo:yhi + 1, x] >= 20).sum() for x in range(fx0, fx1 + 1)],
                     float) * math.cos(math.atan(s))
        print(f"      {name:18s} mean {w.mean():.2f} px  min {w.min():.2f}  max {w.max():.2f}")


if __name__ == "__main__":
    main()
