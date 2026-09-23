#!/usr/bin/env python3
"""Regression tests for tally2.py's box algebra. Run before adding rows."""
import importlib.util, sys, os
# tally2.py reads bip39_en.txt from argv[1] (default: its own directory), so the
# loader must hand it a directory that actually has one. `configs` in the
# published repo, the working directory in the solver tree.
HERE=os.path.dirname(os.path.abspath(__file__))
CFG=next((d for d in (os.path.join(HERE,'configs'), HERE)
          if os.path.exists(os.path.join(d,'bip39_en.txt'))), HERE)
spec=importlib.util.spec_from_file_location("t",os.path.join(HERE,"tally2.py"))
m=importlib.util.module_from_spec(spec)
sys.argv=['x',CFG]; spec.loader.exec_module(m)

def box(**dims):
    b={s:frozenset({0}) for s in range(1,22)}
    for k,v in dims.items(): b[int(k[1:])]=frozenset(v)
    return b

fails=0
def chk(name, got, want):
    global fails
    ok = got==want
    if not ok: fails+=1
    print("  {:<58} {}  (got {}, want {})".format(name,"PASS" if ok else "*** FAIL ***",got,want))

# 1. The dropped-volume bug: disjoint dimension AFTER a dimension that already
#    emitted a piece. Returned 1 of 2 points before the fix.
A=box(s1={0,1}, s2={0}); B=box(s1={0}, s2={9})
chk("disjoint in a LATER dim keeps earlier pieces", sum(m.vol(p) for p in m.subtract(A,B)), 2)

# 2. Disjoint in the FIRST differing dim — the path the original run set took,
#    which is why two methods agreed while the bug sat untouched.
A=box(s1={0,1}, s2={0}); B=box(s1={7}, s2={0})
chk("disjoint in the FIRST dim returns A whole", sum(m.vol(p) for p in m.subtract(A,B)), 2)

# 3. Full containment -> nothing survives.
A=box(s1={0}); B=box(s1={0,1})
chk("A inside B subtracts to nothing", sum(m.vol(p) for p in m.subtract(A,B)), 0)

# 4. Self-subtraction.
A=box(s1={0,1,2}, s3={0,1})
chk("A \\ A is empty", sum(m.vol(p) for p in m.subtract(A,A)), 0)

# 5. Partial overlap in two dimensions at once.
A=box(s1={0,1}, s2={0,1}); B=box(s1={1,2}, s2={1,2})
chk("2-dim partial overlap leaves 3 of 4 points", sum(m.vol(p) for p in m.subtract(A,B)), 3)

# 6. Pieces must be disjoint from each other, not just sum correctly.
A=box(s1={0,1,2}, s2={0,1,2}); B=box(s1={1}, s2={1})
ps=m.subtract(A,B)
pts=set()
dup=False
for p in ps:
    for a in p[1]:
        for b in p[2]:
            if (a,b) in pts: dup=True
            pts.add((a,b))
chk("remainder pieces are mutually disjoint", (not dup) and len(pts)==8, True)

# 7. Union is order-independent.
X=box(s1={0,1,2}); Y=box(s1={1,2,3}); Z=box(s1={2,3,4})
u1,_=m.union_volume([X,Y,Z]); u2,_=m.union_volume([Z,Y,X])
chk("union invariant under run order", (u1,u2), (5,5))

print("\n{}".format("ALL PASS" if not fails else "*** {} FAILURE(S) ***".format(fails)))
sys.exit(1 if fails else 0)
