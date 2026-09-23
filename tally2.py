#!/usr/bin/env python3
"""
tally2.py — exact derivation tally, computed from the config files themselves.

WHY THIS REPLACES tally.py's APPROACH (not its principle -- the principle was
right: declare runs, compute the union, never maintain a sum).

Two defects blocked declaring the older t21 runs:

1. min() IS NOT THE INTERSECTION. tally.py models each dimension by a SIZE and
   takes min() across runs, which is exact only if the sets nest. The declared
   runs happen to nest (54 <= 67 <= 2048), so its 145,249,993,119 stands. The
   older runs do not:
       readme54(54) !<= trust21(69)   true intersection 52, min says 54
       written(67)  !<= trust21(69)   true intersection 52, min says 67
       trust21(69)  !<= idx(80)       true intersection 53, min says 69
       trustonly({trust}) is disjoint from every other pool
   Overstating intersections UNDERSTATES the union -- wrong in the direction
   that looks conservative, which is the hardest kind to notice.

2. 2^N TERMS. 17 runs is 131,072 terms; adding nine more is 67 million, each
   needing a set intersection per dimension. Inclusion-exclusion does not scale
   here.

THE FIX. Parse the configs directly -- the ledger should READ the runs, not
restate them, so a row cannot drift from the config it claims to describe. Model
each run as a box (slot -> frozenset of allowed word indices) and compute the
union by disjointification: subtract each already-accumulated box from the new
one, keeping the remainder as disjoint pieces. Exact for arbitrary sets, and
linear-ish in the number of runs.

WHAT THIS SCRIPT CANNOT KNOW. A config is not evidence that a run happened.
Runs listed under EVIDENCED have logs in this directory; those under ASSERTED
were reported complete before this ledger existed and are included on that word
alone. They are reported separately for exactly that reason.
"""
import re, sys, os
from itertools import product

# Directory holding the .conf files and bip39_en.txt. Defaults to the
# script's own directory so the published copy runs standalone; override
# with argv[1] to point at another config set.
DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

WL = [w.strip() for w in open(os.path.join(DIR, 'bip39_en.txt'))]
IDX = {w: i for i, w in enumerate(WL)}
# INDEX CONVENTION. This script is 0-based: IDX maps abandon->0 ... zoo->2047.
# The repo README and slogan_lines.py are 1-based (black#184, matter#1099).
# Nothing crosses between them today -- the ledger emits only set sizes, never
# an index -- but the mismatch is one refactor from being a live bug, and it is
# the same class as the 1-based/0-based error already in the bug list. The
# assertion below is what makes EXTRA's base safe: if IDX were 1-based, the
# first EXTRA word would take index 2048, which IS zoo, and would silently
# alias it in every set operation.
assert min(IDX.values()) == 0 and max(IDX.values()) == len(IDX) - 1, \
    "IDX must be 0-based and dense; EXTRA indexing is based on len(IDX)"

ALL = frozenset(range(2048))

# One registry for every non-BIP39 EXTRA word seen in any config, assigned above
# the wordlist in deterministic sorted order. Same word -> same integer in every
# config that declares it, which is what the solver does.
EXTRA_IDX = {}
def extra_index(w):
    if w in IDX or w in EXTRA_IDX: return EXTRA_IDX.get(w, IDX.get(w))
    EXTRA_IDX[w] = len(IDX) + len(EXTRA_IDX)
    return EXTRA_IDX[w]

# Deliberately NOT re-based into sorted order. Indices are assigned first-seen,
# so the integers depend on parse order -- which is harmless, because every
# figure this script reports is a set SIZE, and sizes are invariant under
# relabeling. A rebase function existed here briefly and was dead code that
# lied: its docstring promised sorted order nothing applied, and calling it
# after any parse would have corrupted results, since frozensets already built
# keep the old integers while the registry hands out new ones.
NSLOT = 21

class NotBIP39(Exception):
    """A pool or slot word that is neither in the wordlist nor declared EXTRA.

    The solver refuses such a config outright and exits 1, so no run can have
    used one. This parser used to drop the word silently, which would make a
    pool look SMALLER than its config declares and understate the ledger with no
    symptom. A ledger that reads configs must fail on whatever the solver would
    refuse, or the two disagree about what a run actually covered.
    """

def parse(path):
    """config -> {slot: frozenset(word indices)}; None if not a 21-word config."""
    words, pool, extra = {}, [], []
    for line in open(path):
        t = line.split()
        if not t or t[0].startswith('#'): continue
        if t[0] == 'WORDS' and int(t[1]) != NSLOT: return None
        if t[0] == 'POOL': pool += t[1:]
        elif t[0] == 'EXTRA': extra += t[1:]
        elif t[0] == 'SLOT': words[int(t[1])] = t[2]
    # EXTRA declares non-BIP39 words a brainwallet config may legally use --
    # SHA-256 does not care what the string is. The solver gives them indices
    # past the wordlist; mirror that so the ledger accepts what the solver
    # accepts. Refusing them would trade a silent undercount for a hard stop on
    # valid input, the worse of the two.
    #
    # The index MUST be global, not per-config. An earlier version enumerated
    # each config's own EXTRA list, so `stop` in one config and `battery` in
    # another both became 2048 -- and this script exists to intersect sets
    # ACROSS configs, so a union over two EXTRA-declaring rows was arithmetic on
    # words with nothing in common. It could not fire while no brainwallet
    # config was a declared row, but that is the same accidental containment
    # already rejected once, introduced by the very fix that enables such rows.
    for w in extra: extra_index(w)
    LOC = {**IDX, **EXTRA_IDX}
    unk = sorted({w for w in pool if w not in LOC})
    if unk: raise NotBIP39(f"{path}: POOL words neither BIP39 nor EXTRA: {' '.join(unk)}")
    P = frozenset(LOC[w] for w in pool)
    box = {}
    for s in range(1, NSLOT + 1):
        v = words.get(s)
        if v is None: return None
        if v == '@POOL':   box[s] = P
        elif v == '@FULL': box[s] = ALL
        else:
            vs=v.split('|'); u=sorted({w for w in vs if w not in LOC})
            if u: raise NotBIP39(f"{path}: SLOT {s} words neither BIP39 nor EXTRA: {' '.join(u)}")
            box[s] = frozenset(LOC[w] for w in vs)
        if not box[s]: return None
    return box

def vol(b):
    n = 1
    for s in range(1, NSLOT + 1): n *= len(b[s])
    return n

def subtract(a, b):
    """a \\ b as a list of disjoint boxes (<= NSLOT of them)."""
    out, cur = [], dict(a)
    for s in range(1, NSLOT + 1):
        inter = cur[s] & b[s]
        if not inter:
            # Disjoint in this dimension, so everything still in `cur` survives --
            # but so do the pieces ALREADY emitted from earlier dimensions. The
            # first version returned only `cur` and discarded `out`, dropping
            # real volume. It never fired in the original run set because in
            # every pair the disjoint dimension was the FIRST one where the runs
            # differ (slot 1 for swap114, slot 6 for trustonly), so `out` was
            # always still empty. Two methods agreeing validated only the paths
            # both took; this path neither took.
            return out + [dict(cur)]
        rest = cur[s] - b[s]
        if rest:
            nb = dict(cur); nb[s] = rest
            out.append(nb)
        cur[s] = inter
    return out                              # `cur` is a & b, dropped

def union_volume(boxes):
    disjoint = []
    for nb in boxes:
        pend = [nb]
        for d in disjoint:
            nxt = []
            for p in pend: nxt += subtract(p, d)
            pend = nxt
            if not pend: break
        disjoint += pend
    return sum(vol(d) for d in disjoint), len(disjoint)

EVIDENCED = ['t21_readme54','t21_loo21','t21_loo6','t21_loo8','t21_loo14','t21_loo15',
             't21_loo18','t21_free1_p1','t21_free2_p1','t21_free5_p1','t21_free7_p1',
             't21_free9_p1','t21_free10_p1','t21_free11_p1','t21_free17_p1','t21_free20_p1',
             't21_swap114','t21_written']
ASSERTED  = ['t21_pool52','t21_pool52_rev','t21_pool40','t21_idx','t21_pathd','t21_pathe',
             't21_trust21','t21_trust21b','t21_bnw18','t21_bnw18b','t21_trustonly','t21']
CHECKSUM = 128
# 24-word tails: a different template entirely (24 slots, 8 checksum bits),
# so they cannot intersect any 21-word box. Carried as a constant.
T24 = 918_330_048 + 2_700_250_214

def load(names):
    got = {}
    for n in names:
        try:
            b = parse(os.path.join(DIR, n + '.conf'))
        except NotBIP39 as e:
            print(f"  REFUSED: {e}\n  The solver would refuse this too (exit 1); no run used it.",
                  file=sys.stderr); sys.exit(2)
        if b: got[n] = b
        else: print(f"  (skipped {n}: not a parseable 21-word config)", file=sys.stderr)
    return got

if __name__ == '__main__':
    E = load(EVIDENCED)
    A = load(ASSERTED)
    ue, ne = union_volume(list(E.values()))
    ue += T24
    ua, na = union_volume(list(E.values()) + list(A.values()))
    ua += T24
    naive = sum(vol(b) for b in list(E.values()) + list(A.values()))
    print(f"\nEVIDENCED runs ({len(E)}) — logs present in this directory")
    print(f"  union {ue:>22,} candidates   {ue//CHECKSUM:>18,} derivations")
    print(f"\n+ ASSERTED runs ({len(A)}) — reported complete, no log here")
    print(f"  union {ua:>22,} candidates   {ua//CHECKSUM:>18,} derivations")
    print(f"  marginal contribution of the asserted runs: {(ua-ue)//CHECKSUM:,} derivations")
    print(f"\n  naive sum {naive:>18,} candidates")
    print(f"  double-counted {naive-ua:>14,}  ({(naive-ua)/naive:.2%})")
    print(f"  disjoint boxes: {ne} evidenced, {na} combined")
    print(f"\n  CPU-days at 400/s: {ue//CHECKSUM/400/86400:,.0f} evidenced, "
          f"{ua//CHECKSUM/400/86400:,.0f} combined")
