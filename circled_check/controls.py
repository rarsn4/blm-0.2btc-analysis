#!/usr/bin/env python3
"""Negative and positive controls for align_diff.py. Run before trusting it on a real source.

usage: ~/venvs/blm-img/bin/python -I controls.py MASTER WORKDIR

Builds eight synthetic "sources" from the master (four clean, four with planted edits at
known master-pixel coordinates), runs align_diff.py on each, and checks: clean -> zero
regions; planted -> every planted box overlapped by a reported region, and nothing else.
Sets A/B shaped the method; set C/D were held out and run once after it was fixed.
"""
import sys, os, json, subprocess, numpy as np, cv2

master, work = sys.argv[1], sys.argv[2]
os.makedirs(work, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ALIGN = os.path.join(HERE, '..', 'align_diff.py')
M = cv2.imread(master, cv2.IMREAD_COLOR)

def resample(img, s, rot, persp, crop, interp_up, interp_rot):
    h, w = img.shape[:2]
    big = cv2.resize(img, None, fx=s, fy=s, interpolation=interp_up)
    H = np.vstack([cv2.getRotationMatrix2D((w * s / 2, h * s / 2), rot, 1.0), [*persp, 1]])
    big = cv2.warpPerspective(big, H, (int(w * s), int(h * s)), flags=interp_rot, borderValue=(255, 255, 255))
    t, b, l, r = crop
    return big[t:-b, l:-r]

def A(img): return resample(img, 2.5, 1.2, (1e-6, -2e-6), (40, 40, 40, 40), cv2.INTER_CUBIC, cv2.INTER_CUBIC), 85
def B(img): return cv2.resize(img, (800, 600), interpolation=cv2.INTER_AREA), 75
def C(img): return resample(img, 1.6, -0.7, (-2e-6, 1e-6), (25, 60, 70, 15), cv2.INTER_LANCZOS4, cv2.INTER_LINEAR), 70
def D(img): return cv2.resize(img, (1024, 768), interpolation=cv2.INTER_AREA), 80

def pA(img):
    img = img.copy()
    cv2.line(img, (259, 758), (267, 763), (40, 40, 40), 1, cv2.LINE_AA)
    cv2.rectangle(img, (296, 733), (298, 735), (235, 235, 235), -1)
    return img, [(259, 758, 268, 764), (296, 733, 299, 736)]
def pB(img):
    img = img.copy(); cv2.line(img, (256, 790), (266, 790), (30, 30, 30), 3)
    return img, [(255, 789, 268, 792)]
def pC(img):
    img = img.copy(); img[752, 263:265] = img[745, 263]; img[785, 255] = (120, 120, 120)
    return img, [(263, 752, 265, 753), (255, 785, 256, 786)]
def pD(img):
    img = img.copy(); img[794:797, 249:252] = (60, 60, 60)
    return img, [(249, 794, 252, 797)]

def overlaps(r, p, tol=1.0):
    x0, y0, x1, y1 = r
    return not (x1 < p[0] - tol or x0 > p[2] + tol or y1 < p[1] - tol or y0 > p[3] + tol)

ok_all = True
for name, tf, plant in [('A', A, pA), ('B', B, pB), ('C', C, pC), ('D', D, pD)]:
    for kind in ('neg', 'pos'):
        img, planted = (M, []) if kind == 'neg' else plant(M)
        out, q = tf(img)
        src = os.path.join(work, f'{kind}_{name}.jpg'); cv2.imwrite(src, out, [cv2.IMWRITE_JPEG_QUALITY, q])
        od = os.path.join(work, f'out_{kind}_{name}')
        subprocess.run([sys.executable, '-I', ALIGN, master, src, od], check=True, capture_output=True)
        regs = [r['master_box'] for r in json.load(open(os.path.join(od, 'regions.json')))['regions']]
        found = all(any(overlaps(r, p) for r in regs) for p in planted)
        extra = [r for r in regs if not any(overlaps(r, p) for p in planted)]
        ok = found and not extra
        ok_all &= ok
        print(f"{kind}_{name}  planted {len(planted)}  reported {len(regs)}  "
              f"{'PASS' if ok else 'FAIL'}" + (f"  extra {extra}" if extra else '') + ('' if found else '  MISSED'))
print('ALL PASS' if ok_all else 'FAILURES PRESENT')
sys.exit(0 if ok_all else 1)
