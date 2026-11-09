#!/usr/bin/env python3
"""EE-1. Which of our configs admit a given word, and at which slots.

Read-only membership query over every config in the published ledger, plus the
solver-only configs that ran but were never published. No runs, no derivations.

TWO DIFFERENT QUESTIONS, REPORTED SEPARATELY, because conflating them inflates
coverage:

  NAMED     the word appears in a POOL or SLOT line -- somebody chose it.
  ADMITTED  some slot of the config would accept it, which includes every
            config carrying an @FULL slot. @FULL admits all 2048 words, so a
            word can be "admitted" by configs that have never heard of it.

Only NAMED is evidence that a hypothesis was ever entertained. A report that
quoted ADMITTED alone would say every BIP39 word is covered 33 times over.

The parser mirrors tally2.py's, minus its 21-word filter, so that 12-, 18- and
24-word configs are included rather than silently skipped.
"""
import glob, os, sys, collections

A = "/home/soul/blm-analysis/configs"
S = "/home/soul/Downloads/Brainwallet/files(6)"
WORDS = sys.argv[1:] or ["double", "sign", "absent", "proof", "order", "trust"]

def parse(path):
    pool, slots = [], {}
    for line in open(path, encoding="utf-8", errors="replace"):
        t = line.split()
        if not t or t[0].startswith("#"): continue
        if t[0] == "POOL": pool += t[1:]
        elif t[0] == "SLOT":
            v = t[2]
            slots[int(t[1])] = v if v in ("@FULL", "@POOL") else set(v.split("|"))
    return {w.lower() for w in pool}, slots

def scan(files, label):
    named = collections.defaultdict(list)
    admit = collections.defaultdict(set)
    how = collections.defaultdict(collections.Counter)
    for f in sorted(files):
        c = os.path.basename(f)
        pool, slots = parse(f)
        for w in WORDS:
            pins = [s for s, v in slots.items() if isinstance(v, set) and w in {x.lower() for x in v}]
            poolslots = [s for s, v in slots.items() if v == "@POOL"] if w in pool else []
            full = [s for s, v in slots.items() if v == "@FULL"]
            if pins: named[w].append((c, "SLOT " + ",".join(map(str, sorted(pins)))))
            if w in pool:
                named[w].append((c, "POOL -> @POOL slots " + ",".join(map(str, sorted(poolslots)))
                                 if poolslots else "POOL (config has no @POOL slot)"))
            if pins or poolslots or full:
                admit[w].add(c)
                how[w]["slot pin" if pins else ("pool" if poolslots else "@FULL only")] += 1
    print("=" * 78)
    print("%s -- %d configs" % (label, len(files)))
    print("  %-10s %7s %10s   %s" % ("word", "NAMED", "ADMITTED", "how admitted"))
    for w in WORDS:
        print("  %-10s %7d %6d/%-3d   %s" % (w, len(named[w]), len(admit[w]), len(files),
                                             dict(how[w]) or "-"))
    print("  NEVER NAMED anywhere:    %s" % ([w for w in WORDS if not named[w]] or "none"))
    print("  NEVER ADMITTED anywhere: %s" % ([w for w in WORDS if not admit[w]] or "none"))
    for w in WORDS:
        if not named[w]: continue
        print("\n  %s is named in %d row(s):" % (w, len(named[w])))
        for c, where in named[w][:60]:
            print("      %-36s %s" % (c, where))
        if len(named[w]) > 60: print("      ... and %d more" % (len(named[w]) - 60))
    print()

pub = sorted(glob.glob(A + "/*.conf"))
scan(pub, "PUBLISHED LEDGER  configs/")
scan([f for f in sorted(glob.glob(S + "/*.conf"))
      if not os.path.exists(os.path.join(A, os.path.basename(f)))],
     "SOLVER-ONLY (ran, never published)")
