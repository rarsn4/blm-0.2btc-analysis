"""Great Seal ring text: how many words are on it, and is anything occluded?

1. Fit the seal's border circle (grid search, then refine); report radial residuals.
2. Radial profile: where the text band sits inside the border.
3. Unwrap the band into a straight strip by NEAREST-neighbour polar sampling,
   one column per pixel of arc at rho 167 -- every strip value is a source pixel.
4. Word blocks = runs of columns separated by >= 4 columns of paper
   (no pixel < 150 in the band and column mean > 200). Report blocks, gaps,
   and the paper arcs between the text and the scroll's curled ends.
5. Two instruments that FAILED their positive controls, reported so nobody
   re-derives a letter count or letter identity from them:
   a. glyph counting by column profile, tested on the scroll (known
      UBI BENE IBI PATRIA, 3-4-3-6);
   b. letter identity by mask IoU, calibrated on letters that repeat inside
      the two undisputed ring words.
6. Writes seal_ring_strip.png (the text arc, straightened, x4, nearest) for an
   independent reading. The text is mirror-written.
"""
import itertools

import numpy as np
from PIL import Image

from imgio import load_gray

G = load_gray()
H, W = G.shape

# ---- 1. border circle ------------------------------------------------------
dark = G < 110
th = np.linspace(0, 2 * np.pi, 1440, endpoint=False)
S_, C_ = np.sin(th), np.cos(th)


def score(cx, cy, r):
    x = np.rint(cx + r * S_).astype(int)
    y = np.rint(cy - r * C_).astype(int)
    ok = (x >= 0) & (x < W) & (y >= 0) & (y < H)
    return dark[y[ok], x[ok]].mean()


best = (0, None)
for r in np.arange(170, 216, 2):
    for cx in np.arange(600, 702, 2):
        for cy in np.arange(900, 1012, 2):
            s = score(cx, cy, r)
            if s > best[0]:
                best = (s, (cx, cy, r))
s0, (cx, cy, R) = best
for step in (1.0, 0.5, 0.25):
    for _ in range(3):
        s0, (cx, cy, R) = max((score(cx + a, cy + b, R + c), (cx + a, cy + b, R + c))
                              for a in (-step, 0, step) for b in (-step, 0, step) for c in (-step, 0, step))
res = []
for deg in range(0, 360, 10):
    t = np.radians(deg)
    rr = np.arange(R - 8, R + 8.5, 0.5)
    xs = np.rint(cx + rr * np.sin(t)).astype(int)
    ys = np.rint(cy - rr * np.cos(t)).astype(int)
    if ((xs < 0) | (xs >= W) | (ys < 0) | (ys >= H)).any():
        continue
    v = G[ys, xs]
    if v.min() < 110:
        res.append(rr[np.argmin(v)] - R)
print("1. border circle: centre (%.2f, %.2f)  r %.2f ; residual over %d locatable sectors: max |%.1f| px"
      % (cx, cy, R, len(res), np.abs(res).max()))


def sample(rho, t):
    x = np.rint(cx + rho * np.sin(t)).astype(int)
    y = np.rint(cy - rho * np.cos(t)).astype(int)
    return G[y, x]


# ---- 2. radial profile -----------------------------------------------------
tu = np.radians(np.arange(-75, 75.01, 0.25))
print("2. radial profile over the upper arc (-75..+75 deg): fraction of pixels < 170")
for rho in (194, 192, 190, 186, 182, 179, 178, 170, 160, 157, 155, 152):
    print("   rho %3d  %.2f" % (rho, (sample(rho, tu) < 170).mean()))

# ---- 3. unwrap -------------------------------------------------------------
RHO = np.arange(186.0, 149.0, -1.0)           # row i <-> rho 186 - i
RM = 167.0
NC = int(round(2 * np.pi * RM))
TH = np.arange(NC) / RM                       # clockwise from 12 o'clock
X = np.rint(cx + RHO[:, None] * np.sin(TH)[None, :]).astype(int)
Y = np.rint(cy - RHO[:, None] * np.cos(TH)[None, :]).astype(int)
strip = G[Y, X]
ROLL = 350                                    # rolled col 0 = orig 699: text arc and both scroll curls contiguous
Sr = np.roll(strip, ROLL, axis=1)
print("3. strip %d rows x %d cols (%.3f deg per column); analysis rolled by %d cols"
      % (strip.shape[0], NC, 360 / NC, ROLL))


def orig(c):
    return (c - ROLL) % NC


# ---- 4. word blocks --------------------------------------------------------
band = Sr[186 - 176:186 - 159 + 1, :]         # rho 176..159
inkc = (band < 150).sum(axis=0)
paper = (inkc == 0) & (band.mean(axis=0) > 200)
lo, hi = 0, 650                               # rolled cols 0..649 = orig 699 -> 299
blocks, c = [], lo
while c < hi:
    if paper[c]:
        c += 1
        continue
    s = c
    while c < hi and not (paper[c] and paper[c:c + 4].all()):
        c += 1
    if c - s >= 5:
        blocks.append((s, c - 1))
outer = Sr[0:7, :] < 150                      # rho 186..180, outside the text band
inner = Sr[32:37, :] < 150                    # rho 154..150
print("4. ink blocks in the ring text band (rho 159-176), original strip columns:")
TOP = (0 + ROLL) % NC                         # rolled column of 12 o'clock
curls = []
for a, b in blocks:
    out_px = outer[:, a:b + 1].sum() + inner[:, a:b + 1].sum()
    if out_px > 5:
        curls.append((a, b))
    print("   cols %4d-%-4d  width %3d px  (%.1f-%.1f deg)  ink outside band %3d px%s"
          % (orig(a), orig(b), b - a + 1, orig(a) * 360 / NC, orig(b) * 360 / NC, out_px,
             "  -> scroll curl" if out_px > 5 else ""))
lcurl = max(b for a, b in curls if b < TOP)   # scroll curl left of 12 o'clock
rcurl = min(a for a, b in curls if a > TOP)   # scroll curl right of 12 o'clock
text = [(a, b) for a, b in blocks if a > lcurl and b < rcurl and (a, b) not in curls]
print("   ring text = blocks between the scroll curls ending at col %d and starting at col %d"
      % (orig(lcurl), orig(rcurl)))
for (a1, b1), (a2, b2) in zip(text, text[1:]):
    seg = band[:, b1 + 1:a2]
    print("   gap between words, cols %4d-%-4d  %2d px  ink px %d  mean %.0f"
          % (orig(b1 + 1), orig(a2 - 1), a2 - b1 - 1, (seg < 150).sum(), seg.mean()))
first, last = text[0][0], text[-1][1]
flank_ink = 0
for name, a, b in (("curl to first word", lcurl + 1, first), ("last word to curl", last + 1, rcurl)):
    seg = band[:, a:b]
    flank_ink += (seg < 150).sum()
    print("   %-17s cols %4d-%-4d  %3d px  ink px %d  min column mean %.0f"
          % (name, orig(a), orig(b - 1), b - a, (seg < 150).sum(), seg.mean(axis=0).min()))
print("   -> %d word blocks of ring text; flanks to the scroll curls carry %d ink px"
      % (len(text), flank_ink))
blocks = text

# ---- 5a. FAILED instrument: glyph counting, control on the scroll -----------
print("5a. glyph counting by column profile, control = scroll UBI BENE IBI PATRIA (expect 3-4-3-6)")
sb = strip[186 - 183:186 - 153 + 1, :]
for thr in (140, 150, 160):
    prof = (sb < thr).sum(axis=0)
    rs, s = [], None
    for c in range(380, 700):
        if prof[c] > 0 and s is None:
            s = c
        elif prof[c] == 0 and s is not None:
            rs.append((s, c - 1))
            s = None
    if s is not None:
        rs.append((s, 699))
    grp, cur = [], [rs[0]]
    for a, b in rs[1:]:
        if a - cur[-1][1] - 1 >= 7:
            grp.append(cur)
            cur = []
        cur.append((a, b))
    grp.append(cur)
    print("   ink<%d: group sizes %s" % (thr, [len(g) for g in grp]))
print("   -> FAILS: hollow outlined letters fragment or merge; no letter count is claimed")

# ---- 5b. FAILED instrument: letter identity by mask IoU ---------------------
KNOWN = [("S", 850, 868), ("A", 869, 886), ("S", 887, 903), ("U", 904, 920), ("A", 921, 936), ("C", 937, 958),
         ("E", 965, 985), ("R", 986, 1003), ("E", 1004, 1020), ("C", 1021, 1040), ("S", 1041, 1053),
         ("O", 5, 20), ("N", 21, 37), ("G", 38, 55), ("O", 56, 69), ("C", 70, 89)]   # boundaries set by eye


def lmask(a, b):
    ra = (a + ROLL) % NC
    m = Sr[186 - 180:186 - 155 + 1, ra:ra + (b - a) + 1] < 160
    ys, xs = np.where(m)
    m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    c = np.zeros((30, 34), bool)
    h, w = min(30, m.shape[0]), min(34, m.shape[1])
    c[(30 - h) // 2:(30 - h) // 2 + h, (34 - w) // 2:(34 - w) // 2 + w] = m[:h, :w]
    return c


def iou(p, q, sh=3):
    best = 0.0
    for dy in range(-sh, sh + 1):
        for dx in range(-sh, sh + 1):
            r = np.roll(np.roll(q, dy, 0), dx, 1)
            u = (p | r).sum()
            if u:
                best = max(best, (p & r).sum() / u)
    return best


K = [(ch, lmask(a, b)) for ch, a, b in KNOWN]
same, diff = [], []
for (c1, m1), (c2, m2) in itertools.combinations(K, 2):
    (same if c1 == c2 else diff).append(iou(m1, m2))
print("5b. letter identity by IoU, calibrated on CAUSAS + COGNOSCERE (16 cells)")
print("   same-letter n=%d median %.2f range %.2f-%.2f | diff-letter n=%d median %.2f max %.2f"
      % (len(same), np.median(same), min(same), max(same), len(diff), np.median(diff), max(diff)))
print("   -> FAILS: distributions overlap; letter identity on the ring rests on reading, not measurement")

# ---- 6. strip for independent reading ----------------------------------------
a, b = blocks[0][0] - 15, blocks[-1][1] + 15
seg = Sr[186 - 182:186 - 153 + 1, a:b + 1]
v = np.clip((seg - 110) / (215 - 110) * 255, 0, 255).astype(np.uint8)
Image.fromarray(v).resize((v.shape[1] * 4, v.shape[0] * 4), Image.NEAREST).save("seal_ring_strip.png")
print("6. wrote seal_ring_strip.png (orig cols %d-%d, mirror-written, outer edge at top)" % (orig(a), orig(b)))
