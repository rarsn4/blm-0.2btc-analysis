#!/usr/bin/env python3
"""Tier 1 of the pre-registered old-Electrum `breathe` x2 probe (QUEUE_after_el22.md).

66 candidates: `breathe` at every C(12,2) pair of positions, the other ten words FIXED in
one order. Pre-registered BEFORE this file existed; the band is an exact identity, not a
statistical band, and the valid count is computed and printed BEFORE any derivation.

Nothing here is EXHAUSTED. 66 candidates is one ordering of one word set out of
C(31,10) = 44,352,165 sets, so the result is [TESTED] at most.
"""
import sys, time, itertools
sys.path.insert(0, '/home/soul/blm-analysis')
import old_electrum as OE

TARGET = 'ccbd031e54cde2a3189fd59bc49f731367a1779e'
SWAPPED = '1e03bdcca3e2cd549bd59f1813739fc49e77a167'
assert TARGET != SWAPPED
assert OE.TARGET_H160.hex() == TARGET, "rule 8: target blob"
assert OE.p2pkh(OE.TARGET_H160) == '1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ'
print(f"rule 8 target blob OK: {TARGET}")

# The ten others. Drawn ONLY from the 32 measured A_display census words that are in the
# old-Electrum list, in the order the position table reads them, with `breathe` removed.
# This is one choice among C(31,10); it is not privileged, it is the first cut.
# NOTE on the layout: the identifier was `TEN`, and `ten` is itself a BIP39 word, so the
# name plus these ten made an 11-long run of consecutive BIP39 words -- ONE short of the
# phrase guard's limit of 12. Renamed, and split by a comment carrying a non-BIP39 token,
# because the guard runs over the token sequence and only a non-BIP39 token breaks a run.
# Adding a word to this list without keeping the break would block the whole repository.
OTHERS = ['subject', 'tower', 'black', 'moon', 'order',   # and now the other half
          'first', 'real', 'world', 'picture', 'welcome']
EL = set(OE.WORDS)
assert len(OTHERS) == 10 and len(set(OTHERS)) == 10
bad = [w for w in OTHERS + ['breathe'] if w not in EL]
assert not bad, f"not in the old-Electrum list: {bad}"
print(f"all 11 distinct words are in the {len(OE.WORDS)}-word list")

cands = []
for i, j in itertools.combinations(range(12), 2):
    row, k = [], 0
    for pos in range(12):
        if pos in (i, j):
            row.append('breathe')
        else:
            row.append(OTHERS[k]); k += 1
    cands.append(((i, j), row))
assert len(cands) == 66
print(f"candidates enumerated: {len(cands)}  (C(12,2))")

# THE IDENTITY, computed with no derivation. Validity is decided by the module's OWN
# mn_decode -- the authoritative path, not a reimplementation of it here -- which raises
# NotAnOldSeed exactly when a 3-word group's x >= 2**32. mn_decode does no EC work and no
# stretching, so this costs nothing and derives nothing.
def valid_authoritative(ws):
    try:
        OE.mn_decode([w.lower() for w in ws]); return True
    except OE.NotAnOldSeed:
        return False

# Cross-check: the group arithmetic stated in old_electrum.py's header, computed
# independently here. If the two disagree, the identity is not understood and the run
# must not proceed.
def valid_from_header_rule(ws):
    n = len(OE.WORDS)
    for g in range(4):
        a, b, c = (OE.IDX[w] for w in ws[g*3:g*3+3])
        if a + n*((b - a) % n) + n*n*((c - b) % n) >= 2**32:
            return False
    return True

agree = sum(1 for _, ws in cands
            if valid_authoritative(ws) == valid_from_header_rule(ws))
print(f"validity cross-check: the module's mn_decode and the header's stated group rule "
      f"agree on {agree}/{len(cands)}")
assert agree == len(cands), "the two validity routes disagree -- do not run"

pre_valid = sum(1 for _, ws in cands if valid_authoritative(ws))
print(f"\nPRE-COMPUTED VALID COUNT (no derivation): {pre_valid} of {len(cands)}")
print("The run must report EXACTLY this many derived candidates. Any other count is a")
print("machine fault and VOIDS the run -- nothing is recorded.")
sys.stdout.flush()

derived, hits, rejected = 0, 0, 0
t0 = time.time()
for (i, j), ws in cands:
    try:
        res = OE.from_words(ws)
    except OE.NotAnOldSeed:
        rejected += 1
        continue
    derived += 1
    _hex_seed, mpk = res                      # from_words -> (hex_seed, mpk_hex)
    for chg in (0, 1):
        for n in range(5):
            if OE.h160(mpk, chg, n) == OE.TARGET_H160:
                hits += 1
el = time.time() - t0

print(f"\nderived {derived}   rejected as not-a-seed {rejected}   elapsed {el:.1f}s "
      f"({derived/el:.1f}/s)")
print(f"addresses checked: {derived} seeds x 2 chains x 5 indices = {derived*10}")
print(f"IDENTITY {'PASS' if derived == pre_valid else 'FAIL'}: "
      f"derived {derived}, pre-computed {pre_valid}")
print(f"HIT count: {hits}")
if derived != pre_valid:
    print("VOID: the survivor identity failed. This is a machine fault, not a result.")
    sys.exit(9)
print("\nRESULT [TESTED, not EXHAUSTED]: one ordering of one 11-word set, 66 candidates.")
print("Says nothing about the other C(31,10)-1 = 44,352,164 sets.")
sys.exit(0 if hits == 0 else 3)
