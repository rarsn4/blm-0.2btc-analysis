from itertools import permutations
from math import gcd
from fractions import Fraction as F

def ang(t):
    """hand angles (deg cw from 12) at t seconds past 12:00"""
    return (t/120.0 % 360.0, 0.1*t % 360.0, 6.0*t % 360.0)   # hour, minute, second

def dev(a, b):
    d = abs(a-b) % 360.0
    return min(d, 360.0-d)

def mid_dev(a):
    """distance to nearest numeral midpoint (angle = 15 + 30k)"""
    return abs(((a - 15.0) % 30.0) - 15.0) if False else min(((a-15.0) % 30.0), 30.0-((a-15.0)%30.0))

# ---------- 1. EXACT: can all three hands sit exactly on midpoints? ----------
# exact rational scan over the 43200 s cycle using Fractions on the 3 congruences
# second: 6t = 15 (mod 30)  -> t = 2.5 (mod 5)
# minute: t/10 = 15 (mod 30) -> t = 150 (mod 300)
# hour:   t/120 = 15 (mod 30) -> t = 1800 (mod 3600)
# hour cond => t = 1800 + 3600k, always = 0 (mod 300); minute needs 150 (mod 300).
print("EXACT congruence check")
sols = [t for t in range(0, 43200) if t % 300 == 150 and t % 3600 == 1800]
print("  minute&hour simultaneous exact solutions:", len(sols))
print("  hour cond gives t in {1800,5400,...}; all = 0 mod 300, minute needs 150 mod 300 -> none")

# ---------- 2. ANY three midpoints, 1.5 deg tolerance, 0.01 s sampling ----------
TOL = 1.5
N = 4320000            # 43200 s at 0.01 s
hits = 0
best_any = (1e9, None)
for i in range(N):
    t = i*0.01
    h, m, s = ang(t)
    dh, dm, ds = mid_dev(h), mid_dev(m), mid_dev(s)
    w = max(dh, dm, ds)
    if w < best_any[0]:
        best_any = (w, t)
    if w <= TOL:
        hits += 1
print("\nANY three numeral midpoints, tol 1.5 deg, 0.01 s sampling")
print("  matching samples :", hits, "of", N)
print("  best worst-hand deviation: %.4f deg at t=%.2f s (%02d:%02d:%05.2f)"
      % (best_any[0], best_any[1], int(best_any[1]//3600), int(best_any[1]%3600//60), best_any[1]%60))

# ---------- 3. THESE three angles, all 6 hand assignments ----------
OBS = [315.0, 45.0, 15.0]
best = (1e9, None, None)
for i in range(N):
    t = i*0.01
    a = ang(t)
    for p in permutations(OBS):
        w = max(dev(a[0], p[0]), dev(a[1], p[1]), dev(a[2], p[2]))
        if w < best[0]:
            best = (w, t, p)
print("\nTHESE three angles {315,45,15}, all 6 hand-to-angle assignments")
w, t, p = best
h, m, s = ang(t)
print("  best worst-hand deviation: %.4f deg at t=%.2f s (%02d:%02d:%06.3f)"
      % (w, t, int(t//3600), int(t%3600//60), t%60))
print("  assignment (hour,minute,second) wanted =", p)
print("  actual  hour %8.3f  wanted %6.1f   (off %6.3f)" % (h, p[0], dev(h,p[0])))
print("  actual  min  %8.3f  wanted %6.1f   (off %6.3f)" % (m, p[1], dev(m,p[1])))
print("  actual  sec  %8.3f  wanted %6.1f   (off %6.3f)" % (s, p[2], dev(s,p[2])))

# ---------- 4. canonical assignment only (hour=315, min=45, sec=15) ----------
best_c = (1e9, None)
for i in range(N):
    t = i*0.01
    h, m, s = ang(t)
    w = max(dev(h,315.0), dev(m,45.0), dev(s,15.0))
    if w < best_c[0]:
        best_c = (w, t)
print("\nCANONICAL assignment only (hour 315, minute 45, second 15)")
print("  best worst-hand deviation: %.4f deg at t=%.2f s (%02d:%02d:%06.3f)"
      % (best_c[0], best_c[1], int(best_c[1]//3600), int(best_c[1]%3600//60), best_c[1]%60))

# ---------- 5. the 10:07:30 sanity check ----------
t = 10*3600 + 7*60 + 30
h, m, s = ang(t)
print("\n10:07:30 -> hour %.2f  minute %.2f  second %.2f ; hour off from 315 = %.2f"
      % (h, m, s, dev(h,315.0)))
