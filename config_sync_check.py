#!/usr/bin/env python3
"""Compare the published configs with the solver's own copies, on SUBSTANCE only.

WHY. The ledger (tally2.py) parses the configs under blm-analysis/configs/. The runs
parse the copies in the solver directory. If those two sets ever disagree on a SLOT,
POOL, PATH, WORDS or TARGET line, then the ledger describes a different word box than
the one that actually ran -- and every survivor count, band and z-score computed from
it is about a box nobody searched. That is REPORT 1.8's shape (a record describing
something other than what was measured) moved down to the config level, and nothing
in either tree would notice it: both files parse, both runs complete, both report
plausible numbers.

Comment divergence is expected and harmless: the parser ignores it, and the published
copies carry the [MODEL CORRECTED] notes of 9 Nov 2026 that the solver copies do not.
So the two counts are reported separately, and only the first is a fault.

SUBSTANCE = the lines the solver acts on. Everything else -- comments, blank lines --
is stripped, and whitespace inside a kept line is normalised, because `SLOT 1  subject`
and `SLOT 1 subject` are the same instruction.
"""
import os, sys

PUB = '/home/soul/blm-analysis/configs'
SOL = '/home/soul/Downloads/Brainwallet/files(6)'
KEEP = ('SLOT', 'POOL', 'PATH', 'WORDS', 'TARGET')

def substance(path):
    out = []
    with open(path, encoding='utf-8', errors='replace') as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            if ln.split()[0] in KEEP:
                out.append(' '.join(ln.split()))
    return out

def main():
    pub = {f for f in os.listdir(PUB) if f.endswith('.conf')}
    sol = {f for f in os.listdir(SOL) if f.endswith('.conf')}
    both = sorted(pub & sol)
    same_all, comment_only, substance_diff = [], [], []
    for f in both:
        p, s = os.path.join(PUB, f), os.path.join(SOL, f)
        sp, ss = substance(p), substance(s)
        if sp != ss:
            substance_diff.append((f, sp, ss))
        elif open(p, encoding='utf-8', errors='replace').read() != \
             open(s, encoding='utf-8', errors='replace').read():
            comment_only.append(f)
        else:
            same_all.append(f)

    print(f"configs in both trees      {len(both)}")
    print(f"  byte-identical           {len(same_all)}")
    print(f"  differ in COMMENTS only  {len(comment_only)}   (expected, harmless)")
    print(f"  differ in SUBSTANCE      {len(substance_diff)}   <- any nonzero is a FAULT")
    print(f"published only             {len(pub - sol)}")
    print(f"solver only                {len(sol - pub)}")

    # A solver-only config is harmless UNLESS it ran: then a completed run exists whose
    # word box is not in the published record at all, so nothing in the repository can
    # say what was searched. That is the audit gap worth surfacing on every check, not
    # the raw solver-only count.
    ran = []
    for f in sorted(sol - pub):
        b = f[:-5]
        logs = [g for g in os.listdir(SOL)
                if g.endswith('.log') and (g == b + '.log' or g.endswith('_' + b + '.log'))]
        if logs: ran.append((b, sorted(logs)))
    if ran:
        print(f"\n  UNPUBLISHED BUT RAN ({len(ran)}) -- a log exists, the config does not:")
        for b, logs in ran:
            print(f"    {b:<24} {', '.join(logs)}")
        print("  Each is a completed run whose word box the published record cannot describe.")
    else:
        print("  every solver-only config is unrun (no log)")

    if substance_diff:
        print("\nSUBSTANCE DIVERGENCE -- the ledger and the run describe different boxes:")
        for f, sp, ss in substance_diff:
            print(f"\n  {f}")
            for a, b in zip(sp, ss):
                if a != b:
                    print(f"    published: {a[:90]}")
                    print(f"    solver   : {b[:90]}")
            if len(sp) != len(ss):
                print(f"    line counts differ: published {len(sp)}, solver {len(ss)}")
        return 1

    print("\nPASS: every config present in both trees agrees on every SLOT, POOL, PATH,")
    print("WORDS and TARGET line. The ledger describes the boxes that actually ran.")
    if comment_only:
        print(f"\n{len(comment_only)} differ in comments only:")
        for f in comment_only: print("  ", f)
    return 0

if __name__ == '__main__':
    sys.exit(main())
