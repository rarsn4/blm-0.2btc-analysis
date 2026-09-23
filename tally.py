#!/usr/bin/env python3
"""
tally.py — the project's single source of truth for the derivation count.

WHY THIS EXISTS. The headline tally has been maintained as a running sum with
per-change patches, and it drifted. Two independent reconstructions on
2026-09-23 differed by 331 M, and tracing the gap showed BOTH were wrong:
one used the solver's *reported* per-run expected value instead of exact
space/128 (+194 M), the other omitted ~1.14 B of runs. Neither was reproducible
from its own inputs.

Worse, the naive sum double-counts. Every run on the same template shares the
all-pool core, so summing them counts that core once per run. For the 17 runs
of the t21 campaign that is 482 billion candidates, 2.53% of the naive total.

So: no more running sums. Every run is declared here as a product set, the
union is computed by exact inclusion-exclusion, and the tally is whatever this
script prints. Add a run by adding a row, never by adding to a number.

HOW A RUN IS DECLARED. A run is a dict of dimension -> how many values that
dimension takes. All sets within a dimension are nested (the 54-word pool sits
inside the 67-word pool sits inside the 2048-word dictionary; {second} inside
{apple,second} inside pool+both; a fixed word inside pool+that word), so an
intersection's size in any dimension is simply the minimum. That is what makes
the inclusion-exclusion exact rather than approximate.

STILL OUTSTANDING. Only the t21 campaign is declared below. The pre-t21 figure
(26,513,178,774) is carried as an opaque constant and is NOT included in the
total, because it contains eight older t21 runs on this same template
(pool52, idx, pathd, pathe, trust21, bnw18, pool52_rev, pool40, trustonly)
which overlap what is declared here. Those need declaring as rows before a
single grand total can be quoted honestly. Until then this script reports the
t21 campaign exactly and the rest is stated separately.
"""
from itertools import combinations

GAPS     = ['g6','g8','g14','g15','g18','g21']
ASSIGNED = ['s1','s2','s5','s7','s9','s10','s11','s17']
DIMS     = GAPS + ['s20'] + ASSIGNED

POOL, POOL67, DICT = 54, 67, 2048
SECOND, APPLE_SECOND, POOL_PLUS_BOTH = 1, 2, 56
FIXED, POOL_PLUS_WORD = 1, 55

def tpl(gaps=POOL, g21=None, s20=SECOND, freed=None):
    d = {k: gaps for k in GAPS}
    if g21 is not None: d['g21'] = g21
    d['s20'] = s20
    for k in ASSIGNED: d[k] = FIXED
    if freed: d[freed] = POOL_PLUS_WORD
    return d

# ---- the t21 campaign, standard template ---------------------------------
RUNS = {
    'readme54' : tpl(s20=APPLE_SECOND),
    'loo21'    : tpl(g21=DICT, s20=APPLE_SECOND),
    **{f'loo{n}': {**tpl(), f'g{n}': DICT} for n in (6,8,14,15,18)},
    'written'  : tpl(gaps=POOL67),
    **{f'free{m}': tpl(freed=f's{m}') for m in (1,2,5,7,9,10,11,17)},
    'free20'   : tpl(s20=POOL_PLUS_BOTH),
    # when the four self-naming sweeps land, add:
    #   'free4','free16','free12','free19' : tpl(freed='s4') etc.
    #   (ASSIGNED must gain 's4','s16','s12','s19' first)
}

# Disjoint templates — counted separately, never unioned with the above.
# swap114 moves `subject` to slot 14 and pools slot 1; `subject` is not in the
# 54-word pool, so no phrase can satisfy both templates.
DISJOINT = {'swap114': 49_589_822_592, 't24_tail54': 918_330_048,
            't24_tail67': 2_700_250_214}

CHECKSUM = 128          # 21-word phrases: 7 checksum bits
PRE_T21  = 26_513_178_774   # opaque; see STILL OUTSTANDING above

def size(run):
    s = 1
    for d in DIMS: s *= run[d]
    return s

def union(runs):
    names, tot = list(runs), 0
    for r in range(1, len(names)+1):
        for c in combinations(names, r):
            s = 1
            for d in DIMS: s *= min(runs[n][d] for n in c)
            tot += s if r % 2 else -s
    return tot

if __name__ == '__main__':
    u = union(RUNS)
    naive = sum(size(r) for r in RUNS.values())
    dis = sum(DISJOINT.values())
    print(f"t21 campaign, {len(RUNS)} runs, {2**len(RUNS):,} i-e terms")
    print(f"  naive sum       {naive:>20,} candidates")
    print(f"  union           {u:>20,}")
    print(f"  double-counted  {naive-u:>20,}  ({(naive-u)/naive:.2%})")
    print(f"\ndisjoint templates {dis:>18,} candidates")
    for k, v in DISJOINT.items(): print(f"    {k:<12} {v:>18,}")
    print(f"\nTOTAL             {u+dis:>20,} candidates")
    print(f"                  {(u+dis)//CHECKSUM:>20,} derivations")
    print(f"                  {(u+dis)//CHECKSUM/400/86400:>20,.0f} CPU-days at 400/s")
    print(f"\npre-t21, carried separately (see docstring):")
    print(f"                  {PRE_T21:>20,} derivations")
    print(f"\nDo not add these two. Declare the eight older t21 runs as rows first.")
