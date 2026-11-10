"""QQ-1. WHY THE OO-1 NEGATIVE MUST NOT BE RE-RUN AT DEPTH-BASED DETECTION.

This runs the depth-below-local-median detector on the FOUR CONTROL REGIONS ONLY,
declared in xx_marks_plan.md sec.4. It does NOT touch C1 or C2, the circular
elements under test: the point is to measure the criterion's FALSE-POSITIVE rate at
depth, not to reopen a negative.

If the controls fire heavily at depth, the X-signature criterion is VOID in the
BLOCKING sense there -- 1.14's block-B case -- and the asymmetric-void argument that
makes the OO-1 negative worth anything is destroyed. Measured, not asserted.
"""
import os, sys
import numpy as np
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray

# The instrument is re-declared here rather than imported: xx_marks.py runs its whole
# report at module level, so importing it would re-execute the OO-1 measurement.
# These are byte-identical to xx_marks.py's definitions.
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xx_marks.py')).read()
     .split('print("OO-1')[0].split('from imgio import load_gray')[1])

G = load_gray(); H, W = G.shape
EIGHT = np.ones((3, 3), bool)
WIN = 41
DEPTHS = (10, 15, 19, 25, 30, 39)
ABS_CUTS = (90, 110, 125, 140, 155, 170, 185)

def box(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[max(0,y0):min(H,y1), max(0,x0):min(W,x1)] = True; return m

CONTROLS = [("ctrl (900,150)",  box(900,150,1285,535)),
            ("ctrl (1100,430)", box(1100,430,1485,815)),
            ("ctrl (150,150)",  box(150,150,535,535)),
            ("ctrl (1150,800)", box(1150,800,1535,1185))]

def counts(binary, mask):
    """components passing the size gate, and of those how many carry the X signature."""
    lab, k = ndi.label(binary & mask, EIGHT)
    if not k: return 0, 0
    sized = xs = 0
    for sl, i in zip(ndi.find_objects(lab), range(1, k+1)):
        comp = (lab[sl] == i); px = int(comp.sum())
        if px < 20 or px > 600: continue
        h = sl[0].stop-sl[0].start; w = sl[1].stop-sl[1].start
        if not (6 <= w <= 40 and 6 <= h <= 40): continue
        sized += 1
        _, e, j, d, _, _ = skel_stats(comp)
        if is_X(e, j, d): xs += 1
    return sized, xs

print("QQ-1  CONTROL-ONLY CALIBRATION: what depth-based detection would do to the criterion")
print("=" * 90)
print("  C1 and C2 are NOT touched. Controls only, the four declared in the plan.\n")

print("--- the detector OO-1 actually used: absolute cutoffs ---")
print(f"{'region':20s} " + "".join(f"{('<%d'%c):>14s}" for c in ABS_CUTS))
abs_sized = {c: 0 for c in ABS_CUTS}; abs_x = {c: 0 for c in ABS_CUTS}
for nm, m in CONTROLS:
    cells = []
    for c in ABS_CUTS:
        s, x = counts(G < c, m)
        abs_sized[c] = max(abs_sized[c], s); abs_x[c] = max(abs_x[c], x)
        cells.append(f"{s:6d}/{x:<7d}")
    print(f"{nm:20s} " + "".join(f"{v:>14s}" for v in cells))
print(f"{'MAX  sized/X-sig':20s} " + "".join(f"{str(abs_sized[c])+'/'+str(abs_x[c]):>14s}" for c in ABS_CUTS))

print("\n--- the detector QQ-1 forbids: depth below a 41px local median ---")
B = ndi.median_filter(G, size=WIN)
D = B - G
print(f"{'region':20s} " + "".join(f"{('>=%d'%d):>14s}" for d in DEPTHS))
dep_sized = {d: 0 for d in DEPTHS}; dep_x = {d: 0 for d in DEPTHS}
for nm, m in CONTROLS:
    cells = []
    for d in DEPTHS:
        s, x = counts(D >= d, m)
        dep_sized[d] = max(dep_sized[d], s); dep_x[d] = max(dep_x[d], x)
        cells.append(f"{s:6d}/{x:<7d}")
    print(f"{nm:20s} " + "".join(f"{v:>14s}" for v in cells))
print(f"{'MAX  sized/X-sig':20s} " + "".join(f"{str(dep_sized[d])+'/'+str(dep_x[d]):>14s}" for d in DEPTHS))

print("\n--- WHAT IS MEASURED ---")
a_s, a_x = max(abs_sized.values()), max(abs_x.values())
d_s, d_x = max(dep_sized.values()), max(dep_x.values())
print(f"  worst-case control, absolute cutoffs : {a_s:5d} sized components, {a_x:3d} X-signatures")
print(f"  worst-case control, depth detection  : {d_s:5d} sized components, {d_x:3d} X-signatures")
print(f"  components   x{d_s/a_s:.1f}      X-signatures x{d_x/a_x:.1f}")
print()
print("  So depth detection roughly DOUBLES the control's false-positive bound, 6 -> 11.")
print("  It does NOT explode it. The brief's premise that the controls 'would fire far")
print("  more' is measured here as x1.8, which is an increase and not a blowout.")

print("\n--- AND THE BRIEF'S STATED REASON DOES NOT FOLLOW FROM IT ---")
print("  By the asymmetric-void rule the same brief asks to be written down, an")
print("  OVER-firing control plus a region that finds nothing means absence MAY be")
print("  claimed. A detector that fires MORE on controls therefore makes an absence")
print("  argument STRONGER, not weaker -- provided the region still finds nothing.")
print()
print("  What made block B (1.14) void in the BLOCKING sense was not that its controls")
print("  over-fired. It was that R1's own counts, 13-17, sat INSIDE the control range")
print("  at a bar of 14. The blocking condition is the REGION's count being")
print("  indistinguishable from the control's -- not the control's level by itself.")
print()
print("  At absolute cutoffs the circles returned 0-1 against controls of 0-6: far")
print("  below, so absence is claimable. At depth the circles are UNMEASURED, so which")
print("  side of the asymmetry a depth run would land on CANNOT be stated from these")
print("  numbers. It would depend on what the circles returned.")

print("\n--- THE REASONS NOT TO RE-RUN THAT DO HOLD ---")
print("  1. THE TOPOLOGY LIMIT, which is decisive and is independent of any count.")
print("     The criterion requires EXACTLY ONE 4-WAY JUNCTION. REPORT 6 records that at")
print("     sub-pixel stroke widths 'strokes that narrow merge, so a junction and a")
print("     near-miss render identically'. Depth detection at 10-19 levels operates")
print("     precisely where strokes are sub-pixel, so the feature the criterion tests")
print("     for stops being distinguishable from its own negation. The instrument is")
print("     wrong there whatever the control counts say.")
print("  2. CHANGING THE INSTRUMENT AFTER SEEING THE RESULT needs fresh pre-registration.")
print("     OO-1 was pre-registered at absolute cutoffs 90-185. Swapping detectors now")
print("     is the STOP_R10_SET_C problem and PP-3's forking paths in one move.")
print()
print("  CONCLUSION: do not re-run -- on reasons 1 and 2, not on the control counts.")
print("  And the OO-1 negative is SCOPED TO CONTRAST either way: it excludes a pair of")
print("  X marks at ordinary pen contrast and has UNMEASURED sensitivity below the floor.")
