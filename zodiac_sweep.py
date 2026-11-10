#!/usr/bin/env python3
"""II-1. Sweep the whole painting for four uncommon Gravity Falls zodiac symbols.

Executes zodiac_sweep_plan.md as written. That file was committed in 6f1c1cd,
blob 39fc08a926506750c90553ec8cb5055337139b27, before this script ran, and it
fixes the targets, the contrast levels, the component filter, the per-target
criteria, the control and the decision rule.

Swept:     llama, pine tree, ice bag, pentagram.
Not swept: star, heart, hand, moon, glasses, question mark -- free in any
           crowded painting, so finding them would measure nothing.

ABSENCE IS THE EXPECTED RESULT and is recorded either way. Absence is claimed
only at the sizes and cuts where that target's PLANTED CONTROL was recovered;
everywhere else the honest result is "no power".
"""
import hashlib, os, sys, subprocess
import numpy as np
from scipy import ndimage
from scipy.spatial import ConvexHull, QhullError

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from imgio import load_gray

PLAN_BLOB = "39fc08a926506750c90553ec8cb5055337139b27"
CUTS = (90, 110, 130, 150, 170, 190, 215)
AREA_MIN, BB_MIN, BB_MAX = 40, 12, 400
S8 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], bool)

# ------------------------------------------------------------------ shape metrics
def metrics(sub):
    """sub: boolean submask of one component, cropped to its bbox."""
    h, w = sub.shape
    area = int(sub.sum())
    ys, xs = np.nonzero(sub)
    cy, cx = ys.mean(), xs.mean()
    bnd = sub & ~ndimage.binary_erosion(sub, S8)
    by, bx = np.nonzero(bnd)
    pts = np.column_stack([bx, by]).astype(float)
    try:
        hull = ConvexHull(pts)
        hull_area = hull.volume
    except (QhullError, ValueError):
        hull_area = float(area)
    sol = area / hull_area if hull_area > 0 else 1.0

    # radial extremity profile, 72 bins of 5 deg, from the centroid
    ang = (np.degrees(np.arctan2(by - cy, bx - cx)) + 360.0) % 360.0
    rad = np.hypot(bx - cx, by - cy)
    bins = (ang // 5).astype(int)
    r = np.zeros(72)
    for b in range(72):
        m = bins == b
        if m.any():
            r[b] = rad[m].max()
    # circular 3-wide moving average, then circular local maxima
    rs = (np.roll(r, 1) + r + np.roll(r, -1)) / 3.0
    peaks = [i for i in range(72)
             if rs[i] > rs[(i - 1) % 72] and rs[i] >= rs[(i + 1) % 72]]
    pk = np.array([rs[i] for i in peaks]) if peaks else np.array([0.0])
    troughs = [i for i in range(72)
               if rs[i] < rs[(i - 1) % 72] and rs[i] <= rs[(i + 1) % 72]]
    tr = np.array([rs[i] for i in troughs]) if troughs else np.array([1.0])
    ratio = pk.mean() / tr.mean() if tr.mean() > 0 else 99.0

    # 5-fold regularity: best rotational fit of the peak angles to 72 deg spacing
    reg = 999.0
    if len(peaks) == 5:
        pa = np.sort(np.array(peaks) * 5.0)
        off = np.linspace(0, 72, 289)
        err = np.array([max(min(abs(((pa - (o + 72 * k)) % 360 + 180) % 360 - 180)
                                for k in range(5)) for pa_ in [0]) for o in off]) \
            if False else None
        best = 999.0
        for o in off:
            grid = (o + 72 * np.arange(5)) % 360
            d = np.abs(((pa[:, None] - grid[None, :] + 180) % 360) - 180)
            best = min(best, d.min(axis=1).max())
        reg = best

    # width profile by row extent
    wprof = np.array([(np.nonzero(sub[y])[0].max() - np.nonzero(sub[y])[0].min() + 1)
                      if sub[y].any() else 0 for y in range(h)], float)
    nz = wprof > 0
    slope = r2 = 0.0
    if nz.sum() >= 4:
        yy = np.nonzero(nz)[0].astype(float)
        ww = wprof[nz]
        A = np.polyfit(yy, ww, 1)
        slope = A[0]
        pred = np.polyval(A, yy)
        ss = ((ww - ww.mean()) ** 2).sum()
        r2 = 1.0 - ((ww - pred) ** 2).sum() / ss if ss > 0 else 0.0
    dec = max(1, h // 10)
    top_w = wprof[:dec][wprof[:dec] > 0].mean() if (wprof[:dec] > 0).any() else 0.0
    bot_w = wprof[-dec:][wprof[-dec:] > 0].mean() if (wprof[-dec:] > 0).any() else 0.0

    # neck: a local minimum of width in the upper third, with ink above it
    up = wprof[: max(2, h // 3)]
    neck = (up[up > 0].min() / wprof.max()) if (up > 0).any() and wprof.max() > 0 else 1.0

    # legs: separated runs in the bottom fifth, and an off-centre top protrusion
    band = sub[-max(2, h // 5):]
    cols = band.any(axis=0)
    runs, inrun = 0, False
    widths = []
    cur = 0
    for c in cols:
        if c:
            cur += 1; inrun = True
        else:
            if inrun: runs += 1; widths.append(cur); cur = 0
            inrun = False
    if inrun: runs += 1; widths.append(cur)
    legs = sum(1 for x in widths if x <= 0.25 * w)
    t3 = sub[: max(2, h // 3)]
    tx = np.nonzero(t3)[1]
    topoff = abs(tx.mean() - cx) / w if len(tx) else 0.0
    topw = (np.nonzero(t3.any(axis=0))[0].max() - np.nonzero(t3.any(axis=0))[0].min() + 1) \
        if t3.any() else 0

    return dict(area=area, h=h, w=w, sol=sol, npk=len(peaks), ratio=ratio, reg=reg,
                slope=slope, r2=r2, top_w=top_w, bot_w=bot_w, neck=neck,
                runs=runs, legs=legs, topoff=topoff, topw=topw)

# ------------------------------------------------------------------ the four criteria
def is_pentagram(m):
    return (0.30 <= m["sol"] <= 0.80 and m["npk"] == 5 and m["ratio"] >= 1.25
            and m["reg"] <= 10.0)

def is_pine(m):
    return (m["sol"] >= 0.55 and m["slope"] > 0 and m["r2"] >= 0.45
            and m["bot_w"] > 0 and m["top_w"] <= 0.35 * m["bot_w"]
            and 0.7 <= m["h"] / m["w"] <= 3.0)

def is_icebag(m):
    return (m["sol"] >= 0.55 and m["neck"] <= 0.55 and m["h"] / max(m["w"], 1) <= 2.5)

def is_llama(m):
    return (0.7 <= m["w"] / max(m["h"], 1) <= 2.2 and m["legs"] == 4
            and m["topoff"] >= 0.15 and m["topw"] <= 0.5 * m["w"])

TARGETS = [("pentagram", is_pentagram), ("pine tree", is_pine),
           ("ice bag", is_icebag), ("llama", is_llama)]

# ------------------------------------------------------------------ one pass
def sweep(G, cuts=CUTS, label=""):
    H, W = G.shape
    found = {t: [] for t, _ in TARGETS}
    stats = []
    for cut in cuts:
        lab, n = ndimage.label(G < cut, structure=S8)
        if n == 0:
            stats.append((cut, 0, 0)); continue
        objs = ndimage.find_objects(lab)
        sizes = ndimage.sum(np.ones_like(lab, dtype=np.int32), lab,
                            index=np.arange(1, n + 1))
        kept = 0
        for i, sl in enumerate(objs):
            if sl is None: continue
            hh = sl[0].stop - sl[0].start; ww = sl[1].stop - sl[1].start
            if sizes[i] < AREA_MIN: continue
            if max(hh, ww) > BB_MAX or max(hh, ww) < BB_MIN: continue
            sub = lab[sl] == (i + 1)
            kept += 1
            m = metrics(sub)
            for tname, test in TARGETS:
                if test(m):
                    found[tname].append(dict(cut=cut, x0=sl[1].start, y0=sl[0].start,
                                             x1=sl[1].stop, y1=sl[0].stop, **m))
        stats.append((cut, n, kept))
    return found, stats

# ------------------------------------------------------------------ synthetic controls
def draw_pentagram(img, cx, cy, size, val=40):
    R = size / 2.0
    pts = [(cx + R * np.sin(np.radians(72 * k)), cy - R * np.cos(np.radians(72 * k)))
           for k in range(5)]
    order = [0, 2, 4, 1, 3, 0]
    stroke = max(1, int(round(size / 20)))
    for a, b in zip(order, order[1:]):
        x0, y0 = pts[a]; x1, y1 = pts[b]
        nstep = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 2
        for t in np.linspace(0, 1, nstep):
            x, y = int(round(x0 + t * (x1 - x0))), int(round(y0 + t * (y1 - y0)))
            img[max(0, y - stroke):y + stroke + 1, max(0, x - stroke):x + stroke + 1] = val

def draw_pine(img, cx, cy, size, val=40, trunk=False):
    H = size; Wd = int(size * 0.8)
    for i in range(H):
        halfw = int(Wd / 2 * (i / max(H - 1, 1)))
        y = cy - H // 2 + i
        img[y, cx - halfw:cx + halfw + 1] = val
    if trunk:
        tw = max(1, size // 10)
        img[cy + H // 2:cy + H // 2 + max(2, size // 5), cx - tw:cx + tw + 1] = val

def draw_icebag(img, cx, cy, size, val=40):
    ry, rx = size * 0.35, size * 0.32
    yy, xx = np.ogrid[:img.shape[0], :img.shape[1]]
    body = ((xx - cx) ** 2 / rx ** 2 + (yy - (cy + size * 0.12)) ** 2 / ry ** 2) <= 1
    img[body] = val
    nw = max(1, int(size * 0.09))
    img[int(cy - size * 0.42):int(cy + size * 0.05), cx - nw:cx + nw + 1] = val
    cw = max(2, int(size * 0.18))
    img[int(cy - size * 0.50):int(cy - size * 0.40), cx - cw:cx + cw + 1] = val

def draw_llama(img, cx, cy, size, val=40):
    bw, bh = int(size * 0.62), int(size * 0.34)
    img[cy - bh // 2:cy + bh // 2, cx - bw // 2:cx + bw // 2] = val
    lw = max(1, int(size * 0.07)); lh = int(size * 0.30)
    for k, fx in enumerate((-0.42, -0.22, 0.18, 0.38)):
        x = int(cx + fx * size)
        img[cy + bh // 2:cy + bh // 2 + lh, x - lw:x + lw + 1] = val
    nw = max(1, int(size * 0.09)); nh = int(size * 0.34)
    nx = int(cx - 0.34 * size)
    img[cy - bh // 2 - nh:cy - bh // 2, nx - nw:nx + nw + 1] = val
    img[cy - bh // 2 - nh - max(2, int(size * 0.10)):cy - bh // 2 - nh,
        nx - nw - max(1, int(size * 0.06)):nx + nw + 1] = val

DRAW = {"pentagram": draw_pentagram, "pine tree": draw_pine,
        "ice bag": draw_icebag, "llama": draw_llama}
SIZES = (20, 40, 80, 160)

def blank_spots(G, k=4, box=220):
    """The k brightest, most uniform box x box blocks -- the easiest possible
    ground for a planted control. Stated in the plan as 'four locations'."""
    H, W = G.shape
    cand = []
    for y in range(0, H - box, box // 2):
        for x in range(0, W - box, box // 2):
            blk = G[y:y + box, x:x + box]
            cand.append((blk.mean() - blk.std(), x + box // 2, y + box // 2))
    cand.sort(reverse=True)
    out = []
    for _, x, y in cand:
        if all(abs(x - a) > box or abs(y - b) > box for a, b in out):
            out.append((x, y))
        if len(out) == k: break
    return out

def main():
    here = subprocess.run(["git", "hash-object", "zodiac_sweep_plan.md"],
                          cwd=HERE, capture_output=True, text=True).stdout.strip()
    print("PLAN  zodiac_sweep_plan.md blob %s" % here)
    print("      pre-registered blob      %s  -> %s"
          % (PLAN_BLOB, "MATCH" if here == PLAN_BLOB else "*** PLAN CHANGED SINCE PRE-REGISTRATION ***"))
    G = load_gray()
    print("IMAGE %s, %dx%d, verified sha256" % ("0.2-btc-puzzle.png", G.shape[1], G.shape[0]))
    print("CUTS  %s   area>=%d   bbox %d..%d px" % (list(CUTS), AREA_MIN, BB_MIN, BB_MAX))
    print()

    print("=" * 78)
    print("PASS 1 OF 2 -- THE CONTROL (what this method can and cannot find)")
    print("=" * 78)
    spots = blank_spots(G)
    print("  planted at the four brightest, most uniform blocks: %s" % (spots,))
    print()
    power = {}
    for tname, _ in TARGETS:
        rows = []
        for size in SIZES:
            C = G.copy()
            for (sx, sy) in spots:
                try:
                    DRAW[tname](C, sx, sy, size)
                except Exception as e:
                    pass
            f, _ = sweep(C, label="control")
            base, _ = (None, None)
            hits = [h for h in f[tname]
                    if any(abs((h["x0"] + h["x1"]) / 2 - sx) < size and
                           abs((h["y0"] + h["y1"]) / 2 - sy) < size for sx, sy in spots)]
            cuts_ok = sorted(set(h["cut"] for h in hits))
            rows.append((size, len(hits), cuts_ok))
        power[tname] = rows
        print("  %-10s  %s" % (tname, "  ".join(
            "%dpx:%s" % (s, ("RECOVERED@" + ",".join(str(c) for c in cu)) if n else "miss")
            for s, n, cu in rows)))
    # the trunked conifer, to show where the pine criteria lose power
    C = G.copy()
    for (sx, sy) in spots:
        draw_pine(C, sx, sy, 80, trunk=True)
    f, _ = sweep(C)
    tr = [h for h in f["pine tree"]
          if any(abs((h["x0"] + h["x1"]) / 2 - sx) < 80 and
                 abs((h["y0"] + h["y1"]) / 2 - sy) < 80 for sx, sy in spots)]
    print("  %-10s  80px WITH A TRUNK: %s" % ("pine tree",
          "recovered" if tr else "MISSED -- the rising-width criterion fails on a trunk"))
    print()

    print("=" * 78)
    print("PASS 2 OF 2 -- THE PAINTING ITSELF, WHOLE IMAGE, SEVEN CUTS")
    print("=" * 78)
    found, stats = sweep(G)
    print("  cut   components   in size band")
    for cut, n, kept in stats:
        print("  %3d %12d %15d" % (cut, n, kept))
    print()
    for tname, _ in TARGETS:
        rec = [s for s, n, cu in power[tname] if n]
        cuts_with_power = sorted(set(c for s, n, cu in power[tname] for c in cu))
        hits = found[tname]
        print("  %s" % tname.upper())
        if not rec:
            print("    NO POWER: the planted control was not recovered at any size, so")
            print("    this sweep makes NO absence claim for this target.")
        elif not hits:
            print("    ABSENT AT ALL LEVELS SWEPT. Control recovered at sizes %s, cuts %s."
                  % (rec, cuts_with_power))
            print("    0 of %d size-band components at any of the seven cuts met the"
                  % sum(k for _, _, k in stats))
            print("    pre-registered criteria.")
        else:
            print("    %d CANDIDATE(S) -- presence is a candidate for visual confirmation,"
                  % len(hits))
            print("    never a confirmed symbol:")
            for h in sorted(hits, key=lambda z: -z["area"])[:12]:
                print("      cut %3d  bbox x %4d-%4d y %4d-%4d  area %5d  sol %.2f  "
                      "peaks %d  legs %d" % (h["cut"], h["x0"], h["x1"], h["y0"],
                                             h["y1"], h["area"], h["sol"], h["npk"],
                                             h["legs"]))
        print()

    print("=" * 78)
    print("WHAT THIS DOES NOT SETTLE")
    print("=" * 78)
    print("  The synthetic llama and ice bag are crude silhouettes drawn by this")
    print("  script. Recovering them shows the pipeline works on THAT shape; it does")
    print("  not show it would catch a hand-painted llama in a crowded scene, and no")
    print("  absence claim here is stronger than its control.")
    print("  Nothing in this sweep revives the words form of the hypothesis, which is")
    print("  closed on the wordlist alone, and nothing in it grades the locator/order")
    print("  form above [UNTESTED]: a hit would be an object in a painting, not a")
    print("  measured link to a slot or a word.")

if __name__ == "__main__":
    main()
