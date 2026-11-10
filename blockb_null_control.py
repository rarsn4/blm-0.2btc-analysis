"""Did the OLD bands sweep's criterion ever discriminate? Its plan ran a POSITIVE
control (block A's column, 42 glyphs known present) and no NEGATIVE control.
Run the OLD detector, unchanged, over the four null strips declared in
blockb_contrast_plan.md sec.5."""
import os, sys
import numpy as np
from scipy import ndimage
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgio import load_gray
G = load_gray(); H, W = G.shape
CUTS = (90, 110, 130, 150, 170, 190, 215)
def box(x0,y0,x1,y1):
    m=np.zeros((H,W),bool); m[y0:y1,x0:x1]=True; return m
def glyph_count(mask, cut):                     # verbatim from blockb_bands_check.py
    lab,k = ndimage.label((G < cut) & mask)
    if not k: return 0
    n=0
    for sl,i in zip(ndimage.find_objects(lab), range(1,k+1)):
        h=sl[0].stop-sl[0].start; w=sl[1].stop-sl[1].start
        if 6<=w<=33 and 10<=h<=40 and 40<=int((lab[sl]==i).sum())<=600: n+=1
    return n
NULLS=[("null y 160-198",box(0,160,1600,198)),("null y 420-458",box(0,420,1600,458)),
       ("null y 600-638",box(0,600,1600,638)),("null y 980-1018",box(0,980,1600,1018))]
print("THE OLD DETECTOR, UNCHANGED, ON NULL STRIPS IT NEVER RAN ON")
print(f"{'region':30s} " + "".join(f"{('<%d'%c):>7s}" for c in CUTS))
mx=[0]*len(CUTS)
for name,m in NULLS:
    row=[glyph_count(m,c) for c in CUTS]
    mx=[max(a,b) for a,b in zip(mx,row)]
    print(f"{name:30s} " + "".join(f"{v:7d}" for v in row))
print(f"{'MAX over the four nulls':30s} " + "".join(f"{v:7d}" for v in mx))
print(f"\n{'R1 as published (negative)':30s} " + "".join(f"{v:7d}" for v in [8,8,7,7,13,11,5]))
print(f"\n  the published criterion: >= 14 at two or more CONSECUTIVE cuts")
print(f"  cuts where a NULL strip alone reaches 14: "
      f"{[c for c,v in zip(CUTS,mx) if v>=14] or 'none'}")
run=best=0
for v in mx:
    best = best+1 if v>=14 else 0; run=max(run,best)
print(f"  longest consecutive run of >=14 in the nulls: {run}")
print(f"  -> the nulls would themselves score {'POSITIVE' if run>=2 else 'negative'} "
      f"under the published rule")
