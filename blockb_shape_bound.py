"""AAG. Two checks on the AAF entry's area-inflation clause.

(1) The worst-case centroid offset for overlap-keep, derived correctly. Admission is by
    CENTROID, so the reachable offset is (h-1)/2, not h-1. Tallest component that can sit
    mostly outside is h = pad + 1.
(2) Whether overlap-keep's clean-and-in-band row is a SECOND reading or the SAME SET as
    centroid-keep. Set identity would make the agreement arithmetic, not corroboration.

Measurement only. Nothing here re-runs the verdict.
"""
import os, sys
import numpy as np
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runelib as R
from imgio import load_gray

G = load_gray(); H, W = G.shape
EIGHT = np.ones((3, 3), bool)
THR = 130
LADDER = (0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60)
# the identical split, rebuilt as blockb_shape_diag.py rebuilds it
import collections
cells = R.cells()
by_letter = collections.OrderedDict()
for ch, a, b in cells: by_letter.setdefault(ch, []).append((a, b))
TEMPLATE = []
for ch, inst in by_letter.items():
    if len(inst) > 1:
        k = -(-len(inst) // 2)
        for i, (a, b) in enumerate(inst):
            if i < k: TEMPLATE.append((ch, a, b))
TMASK = [R.mask(a, b) for _, a, b in TEMPLATE]
def best_iou(m): return max(R.iou(m, tm) for tm in TMASK)

PAD = max(b - a + 1 for _, a, b in cells)
NULLS = [("y 160-198", 160, 198), ("y 420-458", 420, 458),
         ("y 600-638", 600, 638), ("y 980-1018", 980, 1018)]
BANDH = 38

def comps(y0, y1, pad):
    big = np.zeros((H, W), bool)
    big[max(0, y0 - pad):min(H, y1 + pad), :] = True
    lab, k = ndi.label((G < THR) & big, EIGHT)
    out = []
    for sl, i in zip(ndi.find_objects(lab), range(1, k + 1)):
        comp = (lab[sl] == i); px = int(comp.sum())
        if px < 20 or px > 600: continue
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if not (6 <= w <= 40 and 6 <= h <= 40): continue
        if comp.shape[0] > 34 or comp.shape[1] > 34: continue
        m = np.zeros((34, 34), bool)
        oy, ox = (34 - comp.shape[0]) // 2, (34 - comp.shape[1]) // 2
        m[oy:oy + comp.shape[0], ox:ox + comp.shape[1]] = comp
        a, b = sl[0].start, sl[0].stop - 1          # inclusive row span
        out.append(dict(a=a, b=b, h=h, yc_script=(sl[0].start + sl[0].stop) / 2,
                        cen=(a + b) / 2, m=m))
    return out

# AAH-2(b): nothing below this line runs on import. An importer gets the split and
# best_iou -- which is how a later reader would reach the matcher -- and no measurement.
if __name__ == "__main__":
    print("=" * 94)
    print("AAG-1  the worst-case centroid offset, derived correctly")
    print("=" * 94)
    print(f"  dilation pad                     {PAD} px   (max rune-cell height)")
    print(f"  band height                      {BANDH} rows")
    print(f"  offset-MAXIMISING configuration  {PAD} px above the edge + 1 px inside,")
    print(f"                                   so h = {PAD + 1}. This caps the OFFSET, not the")
    print(f"                                   height: a taller component with more rows inside")
    print(f"                                   can also fall outside, at a smaller offset.")
    print(f"  EDGE offset   h - 1            = {PAD + 1 - 1:.1f} px   <- what the brief used")
    print(f"  CENTROID offset (h - 1) / 2    = {(PAD + 1 - 1) / 2:.1f} px   <- what admission tests")
    print()
    for lbl, off in (("brief's bound, edge offset 22", 22.0),
                     ("CORRECTED bound, centroid (h-1)/2", (PAD) / 2),
                     ("pixel reach of the label region", float(PAD))):
        print(f"  {lbl:36s} {BANDH + 2*off:6.0f} rows   factor {(BANDH + 2*off)/BANDH:.2f}")
    print(f"\n  note: 38 + 2 x 23 = {BANDH + 2*PAD} rows is the PIXEL reach of the dilated label")
    print(f"  region, not an admission height. The brief's 82 is neither that nor the centroid")
    print(f"  bound of {BANDH + PAD}: it is 38 + 2 x (h-1) with h = {PAD}, an edge offset for a component")
    print(f"  one pixel shorter than the tallest reachable one.")

    print()
    print("=" * 94)
    print("AAG-1  what the measurement is, per edge, in both conventions")
    print("=" * 94)
    rows = {}
    for nm, y0, y1 in NULLS:
        keep = []
        for c in comps(y0, y1, PAD):
            if c["b"] + 1 <= y0 or c["a"] >= y1: continue      # >= 1 px overlap
            c["iou"] = best_iou(c["m"])
            c["inband"] = (y0 <= c["yc_script"] < y1)
            c["edge"] = None if c["inband"] else ("top" if c["yc_script"] < y0 else "bottom")
            # script convention (yc = slice midpoint, bottom referenced to y1-1)
            c["off_script"] = (y0 - c["yc_script"]) if c["yc_script"] < y0 else (c["yc_script"] - (y1 - 1))
            # pixel-centre convention, the one the 11.5 bound is stated in
            c["off_centre"] = (y0 - c["cen"]) if c["cen"] < y0 else (c["cen"] - (y1 - 1))
            keep.append(c)
        rows[nm] = keep
    out = [c for v in rows.values() for c in v if not c["inband"]]
    tot = sum(len(v) for v in rows.values())
    print(f"  overlap-keep null candidates {tot}, centroid outside the band {len(out)}, "
          f"in-band {tot - len(out)}")
    for edge in ("top", "bottom"):
        e = [c for c in out if c["edge"] == edge]
        if e:
            print(f"    {edge:7s} n={len(e):2d}   max offset {max(c['off_script'] for c in e):5.1f} px "
                  f"(script)   {max(c['off_centre'] for c in e):5.1f} px (pixel-centre)   "
                  f"max component height {max(c['h'] for c in e)} px")
    ms = max(c["off_script"] for c in out); mc = max(c["off_centre"] for c in out)
    print(f"\n  max offset, script convention        {ms:4.1f} px -> "
          f"{BANDH + 2*ms:.0f} rows, factor {(BANDH + 2*ms)/BANDH:.2f}")
    print(f"  max offset, pixel-centre convention  {mc:4.1f} px -> "
          f"{BANDH + 2*mc:.0f} rows, factor {(BANDH + 2*mc)/BANDH:.2f}")
    print(f"  corrected bound                      {PAD/2:4.1f} px -> "
          f"{BANDH + PAD:.0f} rows, factor {(BANDH + PAD)/BANDH:.2f}")
    print(f"  measurement inside the corrected bound: "
          f"{'YES' if mc <= PAD/2 else 'NO'}  ({mc:.1f} <= {PAD/2:.1f}), "
          f"at {100*mc/(PAD/2):.0f}% of it, not half")
    worst = max(out, key=lambda c: c["off_centre"])
    for nm, y0, y1 in NULLS:
        if worst in rows[nm]:
            above = max(0, y0 - worst["a"]) if worst["edge"] == "top" else max(0, worst["b"] - (y1 - 1))
            inside = worst["h"] - above
            print(f"\n  the max-offset candidate: {nm}, h = {worst['h']} px = {above} px outside the "
                  f"{worst['edge']} edge + {inside} px inside.")
            print(f"  It ATTAINS the pad limit of {PAD} px outside. It falls short of {PAD/2:.1f} only")
            print(f"  on the overlap depth: offset = (p + 1 - k) / 2, and each extra row inside pulls")
            print(f"  the centroid in by 0.5 px, so {PAD/2:.1f} - 0.5 x ({inside} - 1) = "
                  f"{PAD/2 - 0.5*(inside-1):.1f} px, the measured figure.")
            print(f"  Not a height effect: the tallest out-of-band component is "
                  f"{max(c['h'] for c in out)} px, above {PAD+1}.")

    print()
    print("=" * 94)
    print("AAG-2  is overlap-keep's clean-and-in-band row a second reading, or the same set?")
    print("=" * 94)
    same = True
    for nm, y0, y1 in NULLS:
        ov_in = sorted((round(c["iou"], 9), c["a"], c["b"]) for c in rows[nm] if c["inband"])
        cen = []
        for c in comps(y0, y1, PAD):
            if not (y0 <= c["yc_script"] < y1): continue
            cen.append((round(best_iou(c["m"]), 9), c["a"], c["b"]))
        cen = sorted(cen)
        ok = ov_in == cen
        same &= ok
        print(f"  {nm:12s} overlap-keep in-band {len(ov_in):3d}   centroid-keep {len(cen):3d}   "
              f"identical: {'yes' if ok else 'NO'}")
    print(f"\n  SET IDENTITY over all four null strips: {'YES' if same else 'NO'}")
    print("  centroid-in-band implies >= 1 px overlap, so centroid-keep is a SUBSET of")
    print("  overlap-keep and the in-band filter recovers it exactly. The two rows are")
    print("  therefore identical BY CONSTRUCTION -- arithmetic, not two independent readings.")
    print("  The independent pair is clipped (pad 0) vs centroid-kept (pad 23): different")
    print("  labellings, different candidate sets, clean maxima 8 and 7.")
