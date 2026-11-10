#!/usr/bin/env python3
"""KK-1. Three tests on the collar form at the Leopold bust.

Executes collar_form_plan.md, committed in 4cd5eab, blob
ffda5dd6a1578431b411c87d644d02286c304b1d, BEFORE this script ran. The boxes, the
methods, the controls and the decision rules are fixed in that file, as are the
word consequences, which are fixed whatever this returns.

  (a) symmetry, against a garment-patch control distribution
  (b) hue, against SHADOWED bandana rather than lit bandana
  (c) the glint, against comparable highlight clusters on the same garment

Each test can return "cloth". Absence of a result is reported as such.
"""
import os, sys, subprocess
import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from imgio import image_path
from PIL import Image

PLAN_BLOB = "ffda5dd6a1578431b411c87d644d02286c304b1d"
FX0, FY0, FX1, FY1 = 1349, 509, 1373, 541          # the FORM
BUST = (1270, 500, 1500, 660)                      # search window for the garment
COAT = (1310, 545, 1480, 640)                      # the coat, below the bandana
S8 = np.ones((3, 3), bool)
rng = np.random.default_rng(20261110)

def rgb_to_hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-9
    idx = m & (mx == r); h[idx] = ((g - b)[idx] / d[idx]) % 6
    idx = m & (mx == g); h[idx] = ((b - r)[idx] / d[idx]) + 2
    idx = m & (mx == b); h[idx] = ((r - g)[idx] / d[idx]) + 4
    h = (h / 6.0) % 1.0
    s = np.where(mx > 1e-9, d / np.maximum(mx, 1e-9), 0.0)
    return h, s, mx

def q(v):
    return np.percentile(v, [25, 50, 75])

def pearson(a, b):
    a = a.astype(float).ravel(); b = b.astype(float).ravel()
    a = a - a.mean(); b = b - b.mean()
    da, db = np.sqrt((a * a).sum()), np.sqrt((b * b).sum())
    return float((a * b).sum() / (da * db)) if da > 0 and db > 0 else 0.0

def main():
    blob = subprocess.run(["git", "hash-object", "collar_form_plan.md"],
                          cwd=HERE, capture_output=True, text=True).stdout.strip()
    print("PLAN  collar_form_plan.md blob %s" % blob)
    print("      pre-registered          %s  -> %s" % (PLAN_BLOB,
          "MATCH" if blob == PLAN_BLOB else "*** PLAN CHANGED SINCE PRE-REGISTRATION ***"))
    im = Image.open(image_path()).convert("RGB")
    A = np.asarray(im).astype(float) / 255.0
    H, S, V = rgb_to_hsv(A)
    L = 0.299 * A[..., 0] + 0.587 * A[..., 1] + 0.114 * A[..., 2]
    print("IMAGE 0.2-btc-puzzle.png, verified sha256, %dx%d" % (A.shape[1], A.shape[0]))
    print()

    F = L[FY0:FY1, FX0:FX1]
    fh, fs, fv = H[FY0:FY1, FX0:FX1], S[FY0:FY1, FX0:FX1], V[FY0:FY1, FX0:FX1]
    bh, bw = F.shape
    print("FORM  x %d-%d  y %d-%d  (%d x %d px)" % (FX0, FX1, FY0, FY1, bw, bh))
    print()

    # ---------------- masks
    red = ((H < 0.055) | (H > 0.92)) & (S >= 0.35)
    band = np.zeros_like(red); band[505:560, 1340:1440] = True
    bandana = red & band
    cx0, cy0, cx1, cy1 = COAT
    coatbox = np.zeros_like(red); coatbox[cy0:cy1, cx0:cx1] = True
    sky = (H > 0.45) & (H < 0.65) & (S > 0.12)
    garment = coatbox & ~red & ~sky
    print("MASKS bandana %d px (red, in the collar band); garment %d px of the %d-px coat box"
          % (bandana.sum(), garment.sum(), coatbox.sum()))
    print()

    # ================================================== (a) SYMMETRY
    print("=" * 78)
    print("(a) SYMMETRY, WITH A GARMENT CONTROL")
    print("=" * 78)
    best = (-2, None)
    curve = []
    for twoA in range(2748, 2821):
        x0 = twoA - FX1
        if x0 < 0 or x0 + bw > L.shape[1]: continue
        P = L[FY0:FY1, x0:x0 + bw]
        r = pearson(F, np.fliplr(P))
        curve.append((twoA / 2.0, x0, r))
        if r > best[0]: best = (r, (twoA / 2.0, x0))
    r_best, (A_best, px0) = best
    print("  mirrored-partner search, axis x = 1374.0 to 1410.0 step 0.5")
    print("  BEST r = %+.3f at axis x = %.1f, partner box x %d-%d"
          % (r_best, A_best, px0, px0 + bw))
    top = sorted(curve, key=lambda t: -t[2])[:5]
    print("  top five: %s" % "  ".join("x%.1f r%+.3f" % (a, r) for a, _, r in top))
    # control: garment patches, same size, same flip
    cand = []
    ys, xs = np.nonzero(garment)
    for _ in range(4000):
        i = rng.integers(0, len(ys))
        y0, x0 = int(ys[i]) - bh // 2, int(xs[i]) - bw // 2
        if y0 < cy0 or x0 < cx0 or y0 + bh > cy1 or x0 + bw > cx1: continue
        sub = garment[y0:y0 + bh, x0:x0 + bw]
        if sub.mean() < 0.95: continue
        cand.append((y0, x0))
    seen, ctrl = set(), []
    for y0, x0 in cand:
        k = (y0 // 4, x0 // 4)
        if k in seen: continue
        seen.add(k)
        ctrl.append(pearson(F, np.fliplr(L[y0:y0 + bh, x0:x0 + bw])))
    ctrl = np.array(ctrl)
    print("  control: %d garment patches, %d x %d, same flip" % (len(ctrl), bw, bh))
    print("    mean %+.3f  sd %.3f  min %+.3f  max %+.3f  95th %+.3f"
          % (ctrl.mean(), ctrl.std(), ctrl.min(), ctrl.max(), np.percentile(ctrl, 95)))
    pct = 100.0 * (ctrl < r_best).mean()
    z = (r_best - ctrl.mean()) / ctrl.std() if ctrl.std() > 0 else 0
    print("    the partner's r is at the %.1f-th percentile of this distribution, z = %+.2f"
          % (pct, z))
    sym = r_best > ctrl.max()
    print()
    print("  VERDICT: %s" % ("symmetry established -- the mirrored partner beats every "
                             "garment patch" if sym else
                             "SYMMETRY IS NOT ESTABLISHED. The mirrored partner sits INSIDE "
                             "the\n           garment-control distribution, so the cloth "
                             "reading loses its\n           only support."))
    print()

    # ================================================== (b) HUE
    print("=" * 78)
    print("(b) HUE -- AGAINST SHADOWED BANDANA, NOT LIT BANDANA")
    print("=" * 78)
    bv = V[bandana]
    cut = np.percentile(bv, 25)
    shad = bandana & (V <= cut)
    lit = bandana & (V > np.percentile(bv, 75))
    P = (slice(FY0, FY1), slice(px0, px0 + bw))
    rows = [("FORM", fh.ravel(), fs.ravel(), fv.ravel()),
            ("best partner", H[P].ravel(), S[P].ravel(), V[P].ravel()),
            ("bandana, lit (top quartile V)", H[lit], S[lit], V[lit]),
            ("bandana, SHADOWED (bottom quartile V)", H[shad], S[shad], V[shad]),
            ("garment (coat)", H[garment], S[garment], V[garment])]
    print("  %-38s %6s  %-20s %-20s" % ("region", "n", "saturation 25/50/75", "value 25/50/75"))
    for name, h, s, v in rows:
        print("  %-38s %6d  %5.3f %5.3f %5.3f    %5.3f %5.3f %5.3f"
              % (name, len(s), *q(s), *q(v)))
    s_form = np.median(fs)
    s_shad_lo = np.percentile(S[shad], 5)
    print()
    print("  FORM median saturation %.3f;  shadowed bandana 5th percentile %.3f"
          % (s_form, s_shad_lo))
    not_bandana = s_form < s_shad_lo
    in_garment = (np.percentile(S[garment], 5) <= s_form <= np.percentile(S[garment], 95))
    print("  VERDICT: %s" % ("the FORM is desaturated below even the darkest bandana cloth, so "
                             "it is\n           NOT bandana under any lighting."
                             if not_bandana else
                             "the FORM's saturation is NOT below the shadowed bandana "
                             "distribution,\n           so shadowed red cloth is not excluded "
                             "by hue alone."))
    print("           It is %s the garment's own saturation range."
          % ("INSIDE" if in_garment else "OUTSIDE"))
    print()

    # ================================================== (c) THE GLINT
    print("=" * 78)
    print("(c) THE GLINT")
    print("=" * 78)
    lo, hi = np.percentile(F, 10), np.percentile(F, 90)
    dl, dn = ndimage.label(F <= lo, structure=S8)
    if dn == 0:
        print("  no dark cluster found"); return
    sizes = ndimage.sum(np.ones_like(dl), dl, np.arange(1, dn + 1))
    di = int(np.argmax(sizes)) + 1
    dmask = dl == di
    dy, dx = ndimage.center_of_mass(dmask)
    print("  dark cluster ('the eye'): %d px, centroid x %.1f y %.1f, median level %.0f/255"
          % (dmask.sum(), FX0 + dx, FY0 + dy, 255 * np.median(F[dmask])))
    near = ndimage.binary_dilation(dmask, S8, iterations=6) & ~dmask
    glint = near & (F >= hi)
    if glint.sum() == 0:
        print("  NO bright cluster adjacent to the dark cluster. The 'glint' is not there.")
        gcon = None
    else:
        gl, gn = ndimage.label(glint, structure=S8)
        gs = ndimage.sum(np.ones_like(gl), gl, np.arange(1, gn + 1))
        gi = int(np.argmax(gs)) + 1
        gm = gl == gi
        ring = ndimage.binary_dilation(gm, S8, iterations=3) & ~gm
        gcon = 255 * (np.median(F[gm]) - np.median(F[ring]))
        print("  glint: %d px adjacent to the dark cluster, contrast %+.1f levels over its "
              "local surround" % (gm.sum(), gcon))
    # comparable clusters on the garment
    gv = L[garment]
    ghi = np.percentile(gv, 90)
    gl2, gn2 = ndimage.label((L >= ghi) & garment, structure=S8)
    sz = ndimage.sum(np.ones_like(gl2), gl2, np.arange(1, gn2 + 1))
    target = gm.sum() if gcon is not None else 4
    comp = [i + 1 for i, s in enumerate(sz) if target / 2.0 <= s <= target * 2.0]
    cons = []
    for i in comp:
        m = gl2 == i
        ring = ndimage.binary_dilation(m, S8, iterations=3) & ~m
        if ring.sum() == 0: continue
        cons.append(255 * (np.median(L[m]) - np.median(L[ring])))
    cons = np.array(cons)
    print("  comparable bright clusters on the same garment (%d-%d px): %d found"
          % (max(1, target // 2), target * 2, len(cons)))
    if len(cons):
        print("    their contrast: median %+.1f, max %+.1f levels" % (np.median(cons), cons.max()))
        if gcon is not None:
            n_ge = int((cons >= gcon).sum())
            print("    %d of %d reach the glint's contrast (%.0f%%)"
                  % (n_ge, len(cons), 100.0 * n_ge / len(cons)))
    # the conjunction: dark cluster with a bright cluster beside it
    glo = np.percentile(gv, 10)
    dl2, dn2 = ndimage.label((L <= glo) & garment, structure=S8)
    dsz = ndimage.sum(np.ones_like(dl2), dl2, np.arange(1, dn2 + 1))
    dtarget = dmask.sum()
    dcomp = [i + 1 for i, s in enumerate(dsz) if dtarget / 2.0 <= s <= dtarget * 2.0]
    conj = 0
    for i in dcomp:
        m = dl2 == i
        nr = ndimage.binary_dilation(m, S8, iterations=6) & ~m
        if (nr & (L >= ghi)).sum() > 0:
            conj += 1
    print("  THE CONJUNCTION -- a dark cluster of comparable size with a bright cluster")
    print("  beside it, which is the pair that reads as an eye:")
    print("    %d comparable dark clusters on the garment, %d of them have one (%s)"
          % (len(dcomp), conj,
             "%.0f%%" % (100.0 * conj / len(dcomp)) if dcomp else "n/a"))
    print()
    print("  VERDICT: %s" % (
        "the glint-and-eye pair is COMMON on this garment -- it repeats across\n"
        "           the folds, so it is a highlight, not a feature of a distinct object."
        if dcomp and conj / max(len(dcomp), 1) > 0.25 else
        "the glint-and-eye pair is RARE or unique on this garment at this\n"
        "           scale, which favours a distinct object over a fold highlight."))
    print()
    print("=" * 78)
    print("WORD CONSEQUENCES -- fixed in the plan BEFORE this ran, and unchanged by it")
    print("=" * 78)
    print("  No word enters any config from this under any outcome. If the three tests")
    print("  favour an object, the next step is identifying the animal FROM THE PIXELS,")
    print("  not choosing among BIP39 animal names; if the pixels cannot settle the")
    print("  species the result is 'an unidentified form' and no word follows. The")
    print("  leopard/Leopold pun is quarantined: a reason for a stricter test, never a")
    print("  candidate. The zodiac locator grade stays [TESTED, NEGATIVE for 2 of 10].")

main()
