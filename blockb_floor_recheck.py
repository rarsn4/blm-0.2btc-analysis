"""1.14(b). The 39-level floor was computed against a background the control column
does not have. blockb_bands_sensitivity.py estimates it as sub.max() = 254; the
column's values are bimodal and the glyphs' background is the light mode.

A glyph of depth d on background B is seen by the old sweep iff B - d < 215.
"""
import numpy as np, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray

G = load_gray()
sub = G[40:1015, 1526:1557]
dark, light = sub[sub <= 128], sub[sub > 128]
mode = lambda a: int(np.bincount(a.astype(int)).argmax())
mb = mode(light)
print("BLOCK A's CONTROL COLUMN x 1526-1557, y 40-1015  (%d px)" % sub.size)
print(f"  BIMODAL: {100*(sub<=128).mean():.1f}% at or below 128, modal value {mode(dark)}")
print(f"           {100*(sub >128).mean():.1f}% above 128,        modal value {mb}")
print(f"  max {sub.max():.0f}  min {sub.min():.0f}  median {np.median(sub):.0f}  mean {sub.mean():.1f}")
print(f"\n  as-drawn contrast, published  = max - min = {sub.max()-sub.min():.0f} levels ('full pen')")
print(f"  as-drawn contrast, light mode = {mb} - {sub.min():.0f} = {mb-sub.min():.0f} levels")
print(f"\n  FLOOR = B - 215, the old sweep's deepest cut:")
for B, lab in ((float(sub.max()), "sub.max(), as published"), (float(mb), "light mode, measured")):
    print(f"    B = {B:5.0f}  ({lab:24s}) -> floor {B-215:5.0f} levels")
print(f"\n  the rifle receiver's mark is 19 levels (REPORT 6 item 6):")
print(f"    19 < 26 and 19 < 39, so the gap the floor identifies is real on either figure.")
print(f"    the correction is in the SAFE direction: the test was less blind than published.")
