#!/usr/bin/env python3
"""Align a candidate source image to the master and report pixel differences on the BLM card.

usage: align_diff.py MASTER SOURCE OUTDIR [--box L,T,R,B] [--k 6]

Run with the image venv and -I:  ~/venvs/blm-img/bin/python -I align_diff.py ...
SOURCE is untrusted: keep it in its own directory and pass its path; nothing here executes it.

Method
  1. SIFT matches source <-> master, homography by MAGSAC.
  2. Compare at the LOWER of the two resolutions: a larger source is area-downsampled
     into the master frame; a smaller one has the master area-downsampled into its frame.
     Either way the reference never gains pixels it does not have.
  3. ECC refinement on the card neighbourhood, then a linear gain/offset fit there.
  4. Blur matching (Gaussian on the sharper side, sigma chosen on the ring), then
     |difference| on the card box. Noise grows with edge strength (resampling, JPEG
     ringing), so it is modelled on a ring around the card as |D| ~ b0 + b1*|grad|,
     and each pixel is scored z = |D| / expected. Threshold: median + k*1.4826*MAD of
     z on the ring traces region extents; a region is reported only if its peak z
     exceeds the largest z anywhere on the clean ring, i.e. beyond anything noise
     produced there. Coordinates are MASTER pixels. Pixels only; no reading of what
     they show.
"""
import sys, os, json, argparse
import numpy as np, cv2

ap = argparse.ArgumentParser()
ap.add_argument('master'); ap.add_argument('source'); ap.add_argument('outdir')
ap.add_argument('--box', default='242,704,314,812', help='card box in master px: L,T,R,B (R,B exclusive)')
ap.add_argument('--k', type=float, default=6.0, help='noise threshold in robust sigmas')
ap.add_argument('--ring', type=int, default=48, help='ring width (master px) for the noise floor')
a = ap.parse_args()
L, T, R, B = map(int, a.box.split(','))
os.makedirs(a.outdir, exist_ok=True)

def gray(p):
    im = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    if im is None: sys.exit(f'cannot read {p}')
    if im.ndim == 2: return im.astype(np.float32)
    return cv2.cvtColor(im[..., :3], cv2.COLOR_BGR2GRAY).astype(np.float32)

M = gray(a.master); S = gray(a.source)

# 1. global homography, source -> master
sift = cv2.SIFT_create(nfeatures=20000)
k1, d1 = sift.detectAndCompute(S.astype(np.uint8), None)
k2, d2 = sift.detectAndCompute(M.astype(np.uint8), None)
if d1 is None or d2 is None: sys.exit('no features')
mt = cv2.BFMatcher(cv2.NORM_L2).knnMatch(d1, d2, k=2)
good = [m for m, n in (p for p in mt if len(p) == 2) if m.distance < 0.75 * n.distance]
if len(good) < 12: sys.exit(f'only {len(good)} ratio-test matches; cannot align')
ps = np.float32([k1[m.queryIdx].pt for m in good]); pm = np.float32([k2[m.trainIdx].pt for m in good])
H, inl = cv2.findHomography(ps, pm, cv2.USAC_MAGSAC, 2.0)
if H is None: sys.exit('homography failed')
inl = inl.ravel().astype(bool)
proj = cv2.perspectiveTransform(ps[inl].reshape(-1, 1, 2), H).reshape(-1, 2)
rmse = float(np.sqrt(((proj - pm[inl]) ** 2).sum(1).mean()))
scale = float(np.sqrt(abs(np.linalg.det(H[:2, :2]))))      # master px per source px

# 2. common frame = the lower resolution; Gm maps master px -> comparison px
def Rf(f):  # pixel-centre map of a resize by f: x' = (x + 0.5) f - 0.5
    return np.array([[f, 0, 0.5 * f - 0.5], [0, f, 0.5 * f - 0.5], [0, 0, 1.0]])
if scale <= 1.0:          # source larger or equal: shrink source into master frame
    s = scale
    Ssm = cv2.resize(S, None, fx=s, fy=s, interpolation=cv2.INTER_AREA) if s < 1 else S
    Hc = H @ np.linalg.inv(Rf(s)) if s < 1 else H         # small-source px -> master px
    Gm = np.eye(3)
    ref = M
    mov = cv2.warpPerspective(Ssm, Hc, (M.shape[1], M.shape[0]), flags=cv2.INTER_LINEAR, borderValue=np.nan)
else:                     # source smaller: shrink master into source frame
    s = 1 / scale
    Msm = cv2.resize(M, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    Gm = Rf(s)
    Hc = Gm @ H                                             # source px -> small-master px
    ref = Msm
    mov = cv2.warpPerspective(S, Hc, (Msm.shape[1], Msm.shape[0]), flags=cv2.INTER_LINEAR, borderValue=np.nan)

def to_cmp(x, y):  # master px -> comparison px
    v = Gm @ np.array([x, y, 1.0]); return v[0] / v[2], v[1] / v[2]
def to_master(x, y):
    v = np.linalg.inv(Gm) @ np.array([x, y, 1.0]); return v[0] / v[2], v[1] / v[2]

pad = a.ring
x0, y0 = map(int, np.floor(to_cmp(L - pad, T - pad))); x1, y1 = map(int, np.ceil(to_cmp(R + pad, B + pad)))
x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, ref.shape[1]), min(y1, ref.shape[0])
bx0, by0 = map(int, np.floor(to_cmp(L, T))); bx1, by1 = map(int, np.ceil(to_cmp(R, B)))

# 3. local ECC refinement on the card neighbourhood, then gain/offset
rr = ref[y0:y1, x0:x1].copy(); mm = mov[y0:y1, x0:x1].copy()
if np.isnan(mm).mean() > 0.05: sys.exit('source does not cover the card neighbourhood')
mm = np.nan_to_num(mm, nan=float(np.nanmedian(mm)))
W = np.eye(2, 3, dtype=np.float32); ecc = None
try:
    ecc, W = cv2.findTransformECC(rr, mm, W, cv2.MOTION_AFFINE,
                                  (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 3)
    mm = cv2.warpAffine(mm, W, (mm.shape[1], mm.shape[0]), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                        borderMode=cv2.BORDER_REPLICATE)
except cv2.error:
    pass
ring = np.ones_like(rr, bool); ring[by0 - y0:by1 - y0, bx0 - x0:bx1 - x0] = False
e = 3; ring[:e] = ring[-e:] = False; ring[:, :e] = ring[:, -e:] = False   # drop blur-border pixels

def fit(r, m):
    g, o = np.linalg.lstsq(np.c_[m[ring], np.ones(ring.sum())], r[ring], rcond=None)[0]
    return g, o, float(np.mean((r[ring] - (g * m[ring] + o)) ** 2))
def blur(x, sg): return x if sg == 0 else cv2.GaussianBlur(x, (0, 0), sg)
# blur matching: soften whichever side is sharper, by the sigma that best explains the ring
best = (fit(rr, mm)[2], 0.0, 'none')
for sg in np.arange(0.1, 2.01, 0.1):
    best = min(best, (fit(blur(rr, sg), mm)[2], sg, 'master'), (fit(rr, blur(mm, sg))[2], sg, 'source'))
_, blur_sigma, blur_side = best
if blur_side == 'master': rr = blur(rr, blur_sigma)
if blur_side == 'source': mm = blur(mm, blur_sigma)
gain, off, _ = fit(rr, mm)
mm = gain * mm + off

# 4. difference; noise modelled against local edge strength on the ring; regions in the box
D = rr - mm                                               # >0: source darker than master
absD = np.abs(D)
G = cv2.magnitude(cv2.Sobel(rr, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(rr, cv2.CV_32F, 0, 1, ksize=3))
qs = np.quantile(G[ring], np.linspace(0, 1, 11))
gc, nl = [], []
for lo, hi in zip(qs[:-1], qs[1:]):
    sel = ring & (G >= lo) & (G <= hi)
    if sel.sum() >= 50: gc.append(float(np.median(G[sel]))); nl.append(float(np.median(absD[sel])))
b1, b0 = np.polyfit(gc, nl, 1)                           # expected |D| ~ b0 + b1 * G
b0 = max(b0, 0.25); b1 = max(b1, 0.0)
Z = absD / (b0 + b1 * G)                                  # residual in units of expected noise
zmed = float(np.median(Z[ring])); zmad = float(np.median(np.abs(Z[ring] - zmed)))
thr = zmed + a.k * 1.4826 * zmad
med, mad = zmed, zmad
box = np.zeros_like(ring); box[by0 - y0:by1 - y0, bx0 - x0:bx1 - x0] = True
ring_false = int((Z[ring] > thr).sum())
zmax_ring = float(Z[ring].max())                          # the worst the clean ring produced
mask = ((Z > thr) & box).astype(np.uint8)                 # low threshold: traces region extent
n, lab, st, cen = cv2.connectedComponentsWithStats(mask, 8)
regions = []; noise_level = 0
for i in range(1, n):
    cx, cy, w, h, area = st[i]
    sel = lab == i
    if Z[sel].max() <= zmax_ring:                         # within what noise did on the ring
        noise_level += 1; continue
    mx0, my0 = to_master(cx + x0, cy + y0); mx1, my1 = to_master(cx + w + x0, cy + h + y0)
    regions.append(dict(master_box=[round(float(v), 1) for v in (mx0, my0, mx1, my1)],
                        area_cmp_px=int(area), peak=round(float(absD[sel].max()), 1),
                        mean=round(float(absD[sel].mean()), 1), peak_z=round(float(Z[sel].max()), 1),
                        sign='source darker' if D[sel].mean() > 0 else 'source lighter'))
regions.sort(key=lambda r: -r['peak'] * r['area_cmp_px'])

# outputs
f = 8 if scale <= 1 else max(8, int(round(8 * scale)))
def up(img): return cv2.resize(img, None, fx=f, fy=f, interpolation=cv2.INTER_NEAREST)
cv2.imwrite(os.path.join(a.outdir, 'ref_card.png'), up(np.clip(rr, 0, 255).astype(np.uint8)))
cv2.imwrite(os.path.join(a.outdir, 'src_card_aligned.png'), up(np.clip(mm, 0, 255).astype(np.uint8)))
heat = cv2.applyColorMap(np.clip(Z / (thr * 2) * 255, 0, 255).astype(np.uint8), cv2.COLORMAP_INFERNO)
heat[~box] //= 3
cv2.imwrite(os.path.join(a.outdir, 'absdiff_card.png'), up(heat))
summary = dict(source=a.source, source_size=[int(S.shape[1]), int(S.shape[0])],
               matches=len(good), inliers=int(inl.sum()), reproj_rmse_px=round(rmse, 3),
               scale_master_per_source=round(scale, 4),
               compared_at='master resolution' if scale <= 1 else f'source resolution (master x{s:.4f})',
               ecc=None if ecc is None else round(float(ecc), 5), gain=round(float(gain), 4), offset=round(float(off), 2),
               blur_matched=f'{blur_side} sigma {blur_sigma:.1f}', noise_model=f'|D| ~ {b0:.2f} + {b1:.4f}*grad',
               z_median=round(med, 3), z_mad=round(mad, 3), z_threshold=round(thr, 2), k=a.k,
               ring_pixels_above_threshold=ring_false, ring_pixels=int(ring.sum()),
               ring_max_z=round(zmax_ring, 2), noise_level_regions_discarded=noise_level,
               card_box_master=[L, T, R, B], regions=regions)
json.dump(summary, open(os.path.join(a.outdir, 'regions.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'regions'}, indent=1))
print(f'regions beyond noise (peak z > ring max {zmax_ring:.1f}) inside the card box: {len(regions)}'
      f'   [noise-level regions not reported: {noise_level}]')
for r in regions:
    print(f"  master box {r['master_box']}  area {r['area_cmp_px']}  peak |D| {r['peak']}  peak z {r['peak_z']}  {r['sign']}")
