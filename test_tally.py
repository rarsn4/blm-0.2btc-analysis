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

# ---- parser: what it must refuse, and what it must NOT refuse ----------
import tempfile, textwrap
# Temp configs go in their own directory, never in configs/. An earlier version
# used dir=CFG and skipped the unlink on any exception other than NotBIP39, so a
# stray temp config could survive in the published tree -- exactly what a glob
# audit or `git add configs/` would then pick up.
TMP = tempfile.mkdtemp(prefix='tally_tests_')
def mkcfg(body):
    f=tempfile.NamedTemporaryFile('w',suffix='.conf',delete=False,dir=TMP)
    f.write(textwrap.dedent(body)); f.close(); return f.name

SLOTS21="\n".join("SLOT %d abandon"%i for i in range(1,22))

# 8. A non-BIP39 word with no EXTRA must be refused -- the solver exits 1 on
#    exactly this, so the ledger must not quietly shrink the pool instead.
p=mkcfg(f"""
    WORDS 21
    TARGET 1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ
    {SLOTS21.replace('SLOT 6 abandon','SLOT 6 @POOL')}
    POOL able accuse stop freedom
    """)
try:
    m.parse(p); chk("non-BIP39 pool word is REFUSED", "accepted", "raised NotBIP39")
except m.NotBIP39: chk("non-BIP39 pool word is REFUSED", "raised NotBIP39", "raised NotBIP39")

# 9. The same words ARE legal when declared EXTRA. A brainwallet phrase need not
#    be BIP39 at all; refusing these would be a hard stop on valid input, which
#    is worse than the undercount it replaced.
p=mkcfg(f"""
    SCHEME brainwallet
    WORDS 21
    TARGET 1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ
    EXTRA stop freedom
    {SLOTS21.replace('SLOT 6 abandon','SLOT 6 @POOL')}
    POOL able accuse stop freedom
    """)
try:
    b=m.parse(p)
    chk("EXTRA-declared non-BIP39 word is ACCEPTED", len(b[6]) if b else None, 4)
except m.NotBIP39 as e:
    chk("EXTRA-declared non-BIP39 word is ACCEPTED", "refused: %s"%e, 4)

# 10. EXTRA declared AFTER the line that uses it must still resolve -- configs
#     are not required to order their keys.
p=mkcfg(f"""
    SCHEME brainwallet
    WORDS 21
    TARGET 1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ
    {SLOTS21.replace('SLOT 6 abandon','SLOT 6 @POOL')}
    POOL able stop
    EXTRA stop
    """)
try:
    b=m.parse(p); chk("EXTRA declared after use still resolves", len(b[6]) if b else None, 2)
except m.NotBIP39 as e: chk("EXTRA declared after use still resolves", "refused", 2)

# 11-12. CROSS-CONFIG consistency. Every case above parses ONE config, so none
#        of them can see the bug that mattered: EXTRA indices assigned per
#        config made `stop` in one and `battery` in another the same integer,
#        and this script exists to intersect sets ACROSS configs.
def brain(extra, pool):
    return mkcfg(f"""
        SCHEME brainwallet
        WORDS 21
        TARGET 1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ
        EXTRA {extra}
        {SLOTS21.replace('SLOT 6 abandon','SLOT 6 @POOL')}
        POOL {pool}
        """)
a=m.parse(brain('stop freedom','stop'))
b=m.parse(brain('battery staple','battery'))
chk("different EXTRA words never share an index", a[6]==b[6], False)

c=m.parse(brain('freedom stop','stop'))          # same word, declared 2nd not 1st
chk("same EXTRA word maps identically across configs", c[6]==a[6], True)

import shutil; shutil.rmtree(TMP, ignore_errors=True)
print("\n{}".format("ALL PASS" if not fails else "*** {} FAILURE(S) ***".format(fails)))
sys.exit(1 if fails else 0)
