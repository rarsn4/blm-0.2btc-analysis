"""Block B by shape matching against block A's own glyphs. Executes
blockb_shape_plan.md, committed 76aeb4a, blob fddd6d66862753513a8ce0cb61c9c209b9f53c8f,
BEFORE the filter was built or run on any region.

The split, the thresholds, the regions, the nulls, the expected side of section 10's
asymmetry and the decision rule are all fixed in that file. No rotation or reflection.
"""
import os, sys, collections
import numpy as np
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runelib as R
from imgio import load_gray

G = load_gray(); H, W = G.shape
EIGHT = np.ones((3, 3), bool)
THR = 130                                  # same as the templates, plan sec.4
LADDER = (0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60)
NEED = 14
CX, CY, RAD = 470, 937, 182

# ---------------------------------------------------------------- the split
cells = R.cells()                          # (letter, y0, y1) x 42, asserts 8 groups
assert len(cells) == 42, len(cells)
by_letter = collections.OrderedDict()
for ch, a, b in cells:
    by_letter.setdefault(ch, []).append((a, b))

TEMPLATE, TEST = [], []
for ch, inst in by_letter.items():
    if len(inst) == 1:
        TEST.append((ch, *inst[0], "unseen"))          # plan sec.2: singletons -> TEST
    else:
        k = -(-len(inst) // 2)                          # ceil(n/2) -> TEMPLATE
        for i, (a, b) in enumerate(inst):
            (TEMPLATE if i < k else TEST).append((ch, a, b, "seen"))
seen_letters = {c[0] for c in TEMPLATE}
TEST = [(ch, a, b, ("seen" if ch in seen_letters else "unseen")) for ch, a, b, _ in TEST]

print("BLOCK B BY SHAPE MATCHING AGAINST BLOCK A's OWN GLYPHS")
print("=" * 88)
print(f"  block A: {len(cells)} glyph instances, {len(by_letter)} distinct letters")
print(f"  TEMPLATE {len(TEMPLATE):2d} instances over {len({c[0] for c in TEMPLATE})} letters")
print(f"  TEST     {len(TEST):2d} instances: "
      f"{sum(1 for c in TEST if c[3]=='seen')} seen, {sum(1 for c in TEST if c[3]=='unseen')} unseen")
assert len(TEMPLATE) + len(TEST) == 42

TMASK = [R.mask(a, b) for _, a, b, _ in TEMPLATE]

def best_iou(m):
    return max(R.iou(m, tm) for tm in TMASK)

# ---------------------------------------------------------------- power control
print("\n--- POWER CONTROL (plan sec.6): is the held-out half recovered? ---")
scores = {"seen": [], "unseen": []}
for ch, a, b, strat in TEST:
    scores[strat].append(best_iou(R.mask(a, b)))
print(f"  {'threshold':>10s} " + "".join(f"{t:>8.2f}" for t in LADDER))
rec = {}
for strat in ("seen", "unseen"):
    s = scores[strat]
    row = [sum(1 for v in s if v >= t) for t in LADDER]
    rec[strat] = row
    print(f"  {strat:>10s} " + "".join(f"{v:>4d}/{len(s):<3d}" for v in row))
print(f"  best IoU per stratum: seen max {max(scores['seen']):.3f} "
      f"median {np.median(scores['seen']):.3f}; "
      f"unseen max {max(scores['unseen']):.3f} median {np.median(scores['unseen']):.3f}")
has_power = {t: rec["seen"][i] >= 1 for i, t in enumerate(LADDER)}

# ---------------------------------------------------------------- regions
yy, xx = np.ogrid[:H, :W]
disc = ((xx - CX) ** 2 + (yy - CY) ** 2) <= RAD * RAD
def box(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[max(0,y0):min(H,y1), max(0,x0):min(W,x1)] = True; return m

REG = [("R1   y 1100-1138", box(0, 1100, 1600, 1138)),
       ("R1'  minus the disc", box(0, 1100, 1600, 1138) & ~disc)]
NULLS = [("null y 160-198", box(0, 160, 1600, 198)),
         ("null y 420-458", box(0, 420, 1600, 458)),
         ("null y 600-638", box(0, 600, 1600, 638)),
         ("null y 980-1018", box(0, 980, 1600, 1018))]

def candidates(mask):
    lab, k = ndi.label((G < THR) & mask, EIGHT)
    out = []
    if not k: return out
    for sl, i in zip(ndi.find_objects(lab), range(1, k + 1)):
        comp = (lab[sl] == i); px = int(comp.sum())
        if px < 20 or px > 600: continue
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if not (6 <= w <= 40 and 6 <= h <= 40): continue
        m = np.zeros((34, 34), bool)
        oy, ox = (34 - comp.shape[0]) // 2, (34 - comp.shape[1]) // 2
        if comp.shape[0] > 34 or comp.shape[1] > 34: continue
        m[oy:oy + comp.shape[0], ox:ox + comp.shape[1]] = comp
        out.append((best_iou(m), (sl[1].start + sl[1].stop) / 2, (sl[0].start + sl[0].stop) / 2, w, h, px))
    return out

def curve(sc): return [sum(1 for v in sc if v[0] >= t) for t in LADDER]

print("\n--- SPECIFICITY: the four null strips ---")
print(f"  {'region':22s} {'cands':>6s} " + "".join(f"{('>='+format(t,'.2f')):>8s}" for t in LADDER))
nullmax = [0] * len(LADDER)
for nm, m in NULLS:
    sc = candidates(m); row = curve(sc)
    nullmax = [max(a, b) for a, b in zip(nullmax, row)]
    print(f"  {nm:22s} {len(sc):6d} " + "".join(f"{v:>8d}" for v in row))
print(f"  {'MAX over nulls':22s} {'':>6s} " + "".join(f"{v:>8d}" for v in nullmax))
void = {t: nullmax[i] >= NEED for i, t in enumerate(LADDER)}
print(f"\n  VOID where a null reaches >= {NEED} (plan sec.6):")
print("    " + "  ".join(f"{t:.2f}:{'VOID' if void[t] else 'ok  '}" for t in LADDER))

print("\n--- THE REGION UNDER TEST ---")
print(f"  {'region':22s} {'cands':>6s} " + "".join(f"{('>='+format(t,'.2f')):>8s}" for t in LADDER))
obs = {}
for nm, m in REG:
    sc = candidates(m); obs[nm] = sc
    print(f"  {nm:22s} {len(sc):6d} " + "".join(f"{v:>8d}" for v in curve(sc)))

print("\n--- DECISION (plan sec.6) ---")
for nm, _ in REG:
    row = curve(obs[nm])
    usable = [t for i, t in enumerate(LADDER) if has_power[t] and not void[t]]
    qual = [t for i, t in enumerate(LADDER)
            if t in usable and row[i] >= NEED and row[i] > nullmax[i]]
    run = best = 0
    for t in usable:
        best = best + 1 if t in qual else 0
        run = max(run, best)
    print(f"\n  {nm}")
    print(f"    usable thresholds (power, not void): {[f'{t:.2f}' for t in usable] or 'NONE'}")
    print(f"    thresholds with >= {NEED} above the null max: {[f'{t:.2f}' for t in qual] or 'none'}")
    if not usable:
        print("    VERDICT: NO USABLE THRESHOLD -- neither presence nor absence may be claimed")
    else:
        print(f"    VERDICT: {'POSITIVE' if run >= 2 else 'NEGATIVE'}")
print("\n  plan sec.0: no word enters any config from this, under any outcome.")
