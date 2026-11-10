"""Block B below the detection floor. Executes blockb_contrast_plan.md as written.

Plan committed 9534b04, blob 7de2cf0d469872f8338dbb1e78128d4ca1503d50, BEFORE any
pixel of the regions under test was read by this detector.

The absolute cut of the old sweep is replaced by DEPTH BELOW A LOCAL BACKGROUND,
because a global cut cannot reach 19 levels without flooding any region whose local
background is darker than the cut. Everything else -- the glyph-size criterion, the
control column, the decision logic -- is kept identical for comparability.
"""
import os, sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray

G = load_gray()
H, W = G.shape
CX, CY, R = 470, 937, 182
WIN = 41                                  # plan sec.3: wider than a 13x20 glyph
DEPTHS = (10, 15, 19, 25, 30, 39)         # plan sec.3, fixed by principle
NGLYPH = 14
GW, GH = (6, 33), (10, 40)
INK = (40, 600)

yy, xx = np.ogrid[:H, :W]
disc = ((xx - CX) ** 2 + (yy - CY) ** 2) <= R * R

def box(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[y0:y1, x0:x1] = True; return m

PRIMARY = [
    ("R1   y 1100-1138 full width",      box(0, 1100, 1600, 1138)),
    ("R1'  same, minus the dial disc",   box(0, 1100, 1600, 1138) & ~disc),
]
SECONDARY = [
    ("BOTTOM THIRD y 800-1200 (secondary)", box(0, 800, 1600, 1200)),
]
NULLS = [
    ("null y 160-198",  box(0, 160, 1600, 198)),
    ("null y 420-458",  box(0, 420, 1600, 458)),
    ("null y 600-638",  box(0, 600, 1600, 638)),
    ("null y 980-1018", box(0, 980, 1600, 1018)),
]
CTRL_X, CTRL_Y = (1526, 1557), (40, 1015)
CONTROL = ("CONTROL block A x 1526-1557 y 40-1015", box(CTRL_X[0], CTRL_Y[0], CTRL_X[1], CTRL_Y[1]))

def depth_map(img):
    """Local background by median filter, then depth below it. Dark ink -> positive."""
    return ndimage.median_filter(img, size=WIN) - img

def glyph_count(D, mask, d):
    lab, k = ndimage.label((D >= d) & mask)
    if not k: return 0
    n = 0
    for sl, i in zip(ndimage.find_objects(lab), range(1, k + 1)):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if GW[0] <= w <= GW[1] and GH[0] <= h <= GH[1] and INK[0] <= int((lab[sl] == i).sum()) <= INK[1]:
            n += 1
    return n

print("BLOCK B BELOW THE DETECTION FLOOR")
print("=" * 92)
print(f"  detector: depth below a {WIN}px local-median background; depths {DEPTHS}")
print(f"  glyph-sized: w {GW[0]}-{GW[1]}, h {GH[0]}-{GH[1]}, ink {INK[0]}-{INK[1]} (unchanged)")

D = depth_map(G)

hdr = f"{'region':40s} {'px':>8s} " + "".join(f"{('>=%d' % d):>7s}" for d in DEPTHS)
print("\n--- POWER CONTROL (plan sec.4): block A's own column attenuated to each depth ---")
sub = G[CTRL_Y[0]:CTRL_Y[1], CTRL_X[0]:CTRL_X[1]]
bg, dk = float(np.median(sub)), float(sub.min())
print(f"  column background {bg:.0f}, darkest {dk:.0f}, as-drawn contrast {bg-dk:.0f} levels")
print(f"\n{'attenuated to':40s} {'':>8s} " + "".join(f"{('>=%d' % d):>7s}" for d in DEPTHS))
power = {}
for lv in list(DEPTHS) + [int(bg - dk)]:
    att = G.copy()
    att[CTRL_Y[0]:CTRL_Y[1], CTRL_X[0]:CTRL_X[1]] = bg - (bg - sub) * (lv / (bg - dk))
    Da = depth_map(att)
    row = [glyph_count(Da, CONTROL[1], d) for d in DEPTHS]
    power[lv] = row
    tag = "  POWER" if max(row) >= NGLYPH else "  NO POWER"
    lbl = f"{lv} levels" + (" (as drawn)" if lv == int(bg - dk) else "")
    print(f"  {lbl:38s} {'':>8s} " + "".join(f"{v:7d}" for v in row) + tag)

# a depth has power if the control attenuated TO that depth is recovered AT that depth
has_power = {d: power[d][DEPTHS.index(d)] >= NGLYPH for d in DEPTHS}
print("\n  power by depth (control attenuated to d, counted at d):")
print("    " + "  ".join(f"{d}:{'YES' if has_power[d] else 'no '}" for d in DEPTHS))

print("\n--- SPECIFICITY CONTROLS (plan sec.5): four 38x1600 null strips ---")
print(hdr)
nullmax = {d: 0 for d in DEPTHS}
for name, m in NULLS:
    row = [glyph_count(D, m, d) for d in DEPTHS]
    for d, v in zip(DEPTHS, row): nullmax[d] = max(nullmax[d], v)
    print(f"{name:40s} {int(m.sum()):8d} " + "".join(f"{v:7d}" for v in row))
print(f"{'MAX over the four nulls':40s} {'':>8s} " + "".join(f"{nullmax[d]:7d}" for d in DEPTHS))
void = {d: nullmax[d] >= NGLYPH for d in DEPTHS}
print(f"\n  VOID where a null reaches >= {NGLYPH} (plan sec.5):")
print("    " + "  ".join(f"{d}:{'VOID' if void[d] else 'ok  '}" for d in DEPTHS))

print("\n--- REGIONS UNDER TEST ---")
print(hdr)
obs = {}
for name, m in PRIMARY + SECONDARY:
    row = [glyph_count(D, m, d) for d in DEPTHS]
    obs[name] = row
    print(f"{name:40s} {int(m.sum()):8d} " + "".join(f"{v:7d}" for v in row))

print("\n--- DECISION (plan sec.6) ---")
for name, _ in PRIMARY + SECONDARY:
    row = obs[name]
    usable = [(d, v) for d, v in zip(DEPTHS, row) if has_power[d] and not void[d]]
    qual = [d for d, v in usable if v >= NGLYPH and v > nullmax[d]]
    runlen = best = 0
    ud = [d for d, _ in usable]
    for d in ud:
        best = best + 1 if d in qual else 0
        runlen = max(runlen, best)
    verdict = "POSITIVE" if runlen >= 2 else "NEGATIVE"
    print(f"\n  {name}")
    print(f"    usable depths (power and not void): {ud if ud else 'NONE'}")
    print(f"    depths meeting >= {NGLYPH} AND above the null max: {qual if qual else 'none'}")
    print(f"    longest consecutive run of those: {runlen}")
    if not ud:
        print("    VERDICT: NO USABLE DEPTH -- neither presence nor absence may be claimed")
    else:
        print(f"    VERDICT: {verdict}")

print("\n--- CONSISTENCY with the old sweep ---")
oldR1 = [8, 8, 7, 7, 13, 11, 5]
print(f"  old absolute sweep, R1 at cuts (90..215): {oldR1}")
print(f"  new detector, R1 at depth >= 39 (the old floor): {obs[PRIMARY[0][0]][DEPTHS.index(39)]}")
print(f"  old sweep's deepest reach: 254 - 215 = 39 levels; the two should be comparable.")
print("\n  Plan sec.7: no word enters any config from this test, under any outcome.")
