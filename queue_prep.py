#!/usr/bin/env python3
"""Bands, overlaps and wall times for the after-el22 queue. Computes from the config files only.

usage: python3 -I queue_prep.py SOLVER_DIR

For each queued config: candidates; expected survivors and sigma (BIP39: stratified on its own
slot-21 set, per-prefix variance sum_j (k_j/128)(1 - k_j/128); Electrum: binomial at 17/4096);
new candidates against the 42-run EVIDENCED union (tally2's word-set boxes, paths not modelled);
named overlaps slot by slot, with the PATH sets intersected separately; wall time at measured rates.
"""
import sys, os, math
SOLVER = sys.argv[1]
sys.argv = [sys.argv[0], SOLVER]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tally2 as T                                    # reads SOLVER/bip39_en.txt at import

RATE = {'bip39': (11.0e6, 11.6e6), 'electrum': (18.06e6, 18.53e6)}   # measured, free313_boundaries.tsv

def conf(name):
    p = os.path.join(SOLVER, name + '.conf'); d = dict(paths=[], pool=[], slots={}, scheme='bip39')
    for line in open(p):
        t = line.split()
        if not t or t[0].startswith('#'): continue
        if t[0] == 'PATH': d['paths'].append(t[1])
        elif t[0] == 'POOL': d['pool'] += t[1:]
        elif t[0] == 'SLOT': d['slots'][int(t[1])] = t[2]
        elif t[0] == 'WORDS': d['words'] = int(t[1])
        elif t[0] == 'SCHEME': d['scheme'] = t[1]
    P = frozenset(T.IDX[w] for w in d['pool'])
    d['box'] = {s: (P if v == '@POOL' else T.ALL if v == '@FULL' else frozenset(T.IDX[w] for w in v.split('|')))
                for s, v in d['slots'].items()}
    d['n'] = math.prod(len(d['box'][s]) for s in range(1, d['words'] + 1))
    return d

def band(d):
    N = d['n']
    if d['scheme'] == 'electrum':
        p = 17 / 4096; mu = N * p; return mu, math.sqrt(mu * (1 - p)), math.sqrt(mu * (1 - p))
    s21 = d['box'][21]
    k = [sum(1 for i in s21 if i // 128 == j) for j in range(16)]
    v = sum(kj / 128 * (1 - kj / 128) for kj in k)
    prefixes = N // len(s21)
    return N / 128, math.sqrt(prefixes * v), math.sqrt(N / 128 * (1 - 1 / 128))

def overlap(a, b):
    w = math.prod(len(a['box'][s] & b['box'][s]) for s in range(1, a['words'] + 1)) if a['words'] == b['words'] else 0
    return w, sorted(set(a['paths']) & set(b['paths']))

E = T.load(T.EVIDENCED); U0, _ = T.union_volume(list(E.values()))
def new_vs_union(name):
    b = T.parse(os.path.join(SOLVER, name + '.conf'))
    if not b: return None
    U1, _ = T.union_volume(list(E.values()) + [b]); return U1 - U0

check = conf('t21_readme54'); mu, s, sb = band(check)
print(f'check, t21_readme54: stratified sigma / binomial = {s / sb:.6f} (REPORT: 0.983533)\n')

QUEUE = [('t21_slot1_line', ['t21_free1_p1', 't21_readme54']), ('t21_rev54', ['t21_pool52_rev']),
         ('el21_rev', ['el21']), ('t21_pool58', ['t21_readme54']), ('t21_alt3', ['t21_readme54'])]
tot_lo = tot_hi = 0
for name, refs in QUEUE:
    d = conf(name); mu, s, sb = band(d); lo, hi = RATE[d['scheme']]
    tot_lo += d['n'] / hi; tot_hi += d['n'] / lo
    print(f"{name}  [{d['scheme']}, {d['words']} words, {len(d['paths'])} paths]")
    print(f"  candidates   {d['n']:,}")
    print(f"  band         {mu:,.1f} +/- {s:,.1f}  ({'binomial' if d['scheme'] == 'electrum' else f'stratified, {s / sb:.6f} x binomial'})")
    print(f"  wall time    {d['n'] / hi / 3600:.2f} - {d['n'] / lo / 3600:.2f} h at {lo / 1e6:.1f}-{hi / 1e6:.1f}M cand/s")
    if d['scheme'] == 'bip39' and d['words'] == 21:
        nv = new_vs_union(name); print(f"  new vs the 42-run union (paths not modelled): {nv:,} = {nv / d['n']:.2%}")
    for r in refs:
        w, ps = overlap(d, conf(r))
        print(f"  overlap with {r}: {w:,} candidates = {w / d['n']:.2%}, on {len(ps)} shared path(s) {ps}")
    print()
print(f'queue total: {tot_lo / 3600:.1f} - {tot_hi / 3600:.1f} h of GPU time')
