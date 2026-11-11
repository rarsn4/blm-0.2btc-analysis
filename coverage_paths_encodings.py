"""UU-1. Which paths and which public-key encodings each admitted run covers, and how
much of the admitted space is checked on fewer than all of them. Box algebra only:
no derivation, no run.

Paths come from each config's own PATH lines. Encodings are not a config directive
(no admitted config has one); they are a property of the binary that ran it. Per
REPORT 3, the three-encoding binary was built 2026-09-28 07:51 and every run whose
log closed before then checked the COMPRESSED key only.

Candidates are converted to derivations at 1/128 (21 words), divided last.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["tally2", os.path.join(HERE, "configs")]
sys.path.insert(0, HERE)
import tally2 as T

FOUR = ["m/44'/0'/0'/0/0", "m/0'/0/0", "m/0/0", "m/44'/0'/0'/0/1"]
E = list(dict.fromkeys(T.EVIDENCED))
PRE = set(["t21_readme54", "t21_swap114", "t21_written", "t21_pool75",
           "t21_loo21", "t21_loo6", "t21_loo8", "t21_loo14", "t21_loo15", "t21_loo18",
           "t21_black6", "t21_black8", "t21_black14", "t21_black15", "t21_black18", "t21_black21"]
          + [n for n in E if n.endswith("_p1")])

def paths(n):
    return [l.split()[1] for l in open(os.path.join(T.DIR, n + ".conf"))
            if l.split()[:1] == ["PATH"]]

G1 = [n for n in E if n not in PRE and paths(n) == FOUR]          # post-patch, 4 paths, 3 enc
G2 = [n for n in E if n in PRE and paths(n) == FOUR]              # pre-patch,  4 paths, comp
G3 = [n for n in E if n in PRE and paths(n) == FOUR[:1]]          # pre-patch,  path 1,  comp
odd = [n for n in E if n not in G1 + G2 + G3]
assert not odd, odd
# Derived, never hardcoded: the ledger grows. The assertion that matters is that the
# three groups PARTITION it -- a config with some other path set would land in `odd`
# and stop this script rather than be silently dropped from a coverage figure.
assert len(G1) + len(G2) + len(G3) == len(E), (len(G1), len(G2), len(G3), len(E))
NRUN = len(E)

box = {n: T.parse(os.path.join(T.DIR, n + ".conf")) for n in E}
def U(names): return T.union_volume([box[n] for n in names])[0]

print(f"UU-1  PATHS x ENCODINGS OVER THE ADMITTED LEDGER ({NRUN} 21-word runs + T12 + T24)")
print("=" * 88)
print(f"  G1  post-patch, 4 paths, compressed+uncompressed+hybrid : {len(G1):2d} runs")
print(f"  G2  pre-patch,  4 paths, COMPRESSED ONLY                : {len(G2):2d} runs  {' '.join(G2)}")
print(f"  G3  pre-patch,  PATH 1 ONLY, COMPRESSED ONLY            : {len(G3):2d} runs  {' '.join(G3)}")

u_all, u1, u12 = U(E), U(G1), U(G1 + G2)
print(f"\n  union, all {NRUN}          : {u_all:>20,} candidates  = {u_all // 128:>17,} derivations")
print(f"  union, G1              : {u1:>20,}")
print(f"  union, G1 + G2         : {u12:>20,}")

cells = [
  ("path 1 (m/44'/0'/0'/0/0)", "compressed",           u_all, "G1 G2 G3, T12, T24"),
  ("path 1 (m/44'/0'/0'/0/0)", "uncompressed / hybrid", u1,   "G1, T12"),
  ("paths 2-4",                "compressed",           u12,   "G1 G2, T12, T24"),
  ("paths 2-4",                "uncompressed / hybrid", u1,   "G1, T12"),
]
print(f"\n  COVERAGE TABLE, 21-word union by cell (T12, T24 listed; disjoint from every 21-word box)")
print(f"  {'path':26s} {'encoding':22s} {'21-word candidates':>20s} {'share':>7s}   covered by")
for p, e, v, who in cells:
    print(f"  {p:26s} {e:22s} {v:>20,} {100*v/u_all:6.2f}%   {who}")

print("\n  EXPOSURE -- admitted candidates checked on FEWER than all 12 path x encoding cells")
a = u_all - u1
b = u_all - u12
print(f"  never checked uncompressed or hybrid, on ANY path : {a:>20,} = {100*a/u_all:5.2f}%  ({a // 128:,} derivations)")
print(f"  never checked on paths 2-4, at ANY encoding       : {b:>20,} = {100*b/u_all:5.2f}%  ({b // 128:,} derivations)")
print(f"  checked on all 12 cells                           : {u1:>20,} = {100*u1/u_all:5.2f}%")

print("\n  CONSTANTS, not boxes (they intersect no 21-word box):")
print(f"  T12 = t12full_mp  {T.T12:>15,} cand.  4 paths, 3 encodings  (exit=2 9 Nov 12:14:50 UTC)")
print(f"  T24 = t24_tail54 + t24_tail67  {T.T24:>15,} cand.  4 paths, COMPRESSED ONLY [INFERRED]:")
print( "        in the ledger by 2026-09-23 13:39 (713cc0f), before the 2026-09-28 07:51 build;")
print( "        no exit= line for either in any log, so the date comes from git, not from a log.")

# ---------------------------------------------------------------- what the queue closes
# Each t21_freeN 4-path twin is the SAME word box as its _p1 run (the queue's identity
# test), run on the current binary: 4 paths x 3 encodings. So a twin converts its _p1
# box from "path 1, compressed" to "all 12 cells". Not admitted until each completes
# in band; this is a projection of coverage, not a ledger change.
print("\n  WHAT THE RUNNING QUEUE CLOSES (projection; twins are admitted only on completion)")
done_twins = [n for n in G3 if n[:-3] in E]                       # free2, free11, free20
pend = [n for n in G3 if n[:-3] not in E]
free4 = [n for n in pend if n == "t21_free4_p1"]
# t21_free4 was admitted 11 Nov, so it is in the ledger row now and its own row would
# duplicate it. The projection runs over the twins that have NOT yet been admitted.
rows_proj = [("now (admitted ledger)", [])]
if free4:
    rows_proj.append(("+ t21_free4 (not yet admitted)", free4))
rows_proj.append((f"+ the remaining {len(pend)} twins (queue complete, ~25 Nov)", pend))
for label, extra in rows_proj:
    full = U(G1 + done_twins + extra)                              # all 12 cells
    p24  = U(G1 + G2 + done_twins + extra)                         # paths 2-4, any enc
    print(f"  {label:46s} all-12-cells {100*full/u_all:6.2f}%   "
          f"never-unc/hyb {100*(u_all-full)/u_all:6.2f}%   never-paths-2-4 {100*(u_all-p24)/u_all:6.2f}%")
print("\n  After the queue, what remains short of all 12 cells is the G2 space not re-covered")
print("  by any post-patch run: 4 paths, compressed only. The queue does not touch it.")

# ---------------------------------------------------------------- against the published figure
# REPORT section 3 publishes the compressed-only share at the 82-run state as 56.02%
# (22,692,382,618,411 of 40,504,526,297,231), by |U(S u U_post)| - |U_post|. The ledger
# has since gone to 84: t21_free2 and t21_free11 were admitted 9 Nov, both post-patch
# 4-path twins of pre-patch _p1 boxes. Reproduce the 82-run figure, then this one.
print("\n  AGAINST THE PUBLISHED FIGURE (rule 1: recompute, never adopt)")
SINCE82 = ("t21_free2", "t21_free11", "t21_free4")   # twins admitted after that state
E82 = [n for n in E if n not in SINCE82]
G1_82 = [n for n in G1 if n not in SINCE82]
u82, u1_82 = U(E82), U(G1_82)
c82 = u82 - u1_82
print(f"  82-run union            {u82:>20,}   (published 40,504,526,297,231)")
print(f"  82-run compressed-only  {c82:>20,} = {100*c82/u82:5.2f}%   (published 22,692,382,618,411 = 56.02%)")
print(f"  reproduced: union {'YES' if u82 == 40_504_526_297_231 else 'NO'}, "
      f"compressed-only {'YES' if c82 == 22_692_382_618_411 else 'NO'}")
print(f"\n  {NRUN}-run compressed-only  {u_all-u1:>20,} = {100*(u_all-u1)/u_all:5.2f}%")
d = c82 - (u_all - u1)
print(f"  the admissions since re-covered {d:,} candidates with all three encodings,")
print(f"  so the published 56.02% is STALE and the current figure is {100*(u_all-u1)/u_all:.2f}%.")
print(f"  The union is unchanged at {u_all:,}: both twins are same-word-box runs and add 0 volume.")

# ---------------------------------------------------------------- every row of that table
# The 9 Nov twins sit inside several of the scopes the table rows name, so updating the
# total alone would leave its own siblings stale. All five rows, at 84 runs.
PRE29 = [n for n in E if n in PRE]
P13   = [n for n in E if n.endswith("_p1")]
P214  = ["t21_swap114", "t21_free2_p1"]
LOO   = ["t21_loo6", "t21_loo8", "t21_loo14", "t21_loo15", "t21_loo18", "t21_loo21"]
assert len(PRE29) == 29 and len(P13) == 13
print(f"\n  EVERY ROW OF SECTION 3's TABLE, RECOMPUTED AT {NRUN} RUNS")
print(f"  {'scope':34s} {'its union':>20s} {'compressed-only':>20s} {'now':>7s} {'was(82)':>8s}")
was = {"all 29 pre-patch runs": "56.02%", }
rows = [("all 29 pre-patch runs", PRE29, 22_692_382_618_411, 24_480_490_264_651),
        ("sec 2.13, the 13 free*_p1", P13, 15_819_153_406_848, 17_455_617_552_384),
        ("sec 2.14, swap114 + free2_p1", P214, None, 1_413_309_943_872),
        ("sec 2.19, the six loo", LOO, 6_305_594_231_808, 6_458_615_227_584),
        ("the whole union", E, 22_692_382_618_411, 40_504_526_297_231)]
for lab, S, old_num, pub_union in rows:
    us = U(S)
    co = U(G1 + S) - u1            # |U(S u U_post)| - |U_post|
    o = f"{100*old_num/pub_union:5.2f}%" if old_num else "   --  "
    print(f"  {lab:34s} {us:>20,} {co:>20,} {100*co/us:6.2f}% {o:>8s}")
print("\n  (sec 2.14's 82-run numerator is not in the table as a separate figure, so its")
print("   'was' column is left blank rather than guessed.)")
