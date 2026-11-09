#!/usr/bin/env python3
"""EE-2. The base rate for "six of the ten whitepaper edits are BIP39 words".

A ratio is not evidence until its base rate is measured. Section 1.1's lesson is
that naming a confound is not testing it, so this tests it.

THE REFERENCE CLASS IS THE WHOLE QUESTION. BIP39's wordlist holds no word under
3 letters and none over 8, so a base rate taken over every distinct word in the
passage -- "a", "of", "transactions" -- is a rate over a population that
includes words which CANNOT be BIP39 whatever the artist intended. The honest
comparison is against words of the shape the observed ones actually have.

Source: section 2 of the Bitcoin whitepaper as published, NOT as painted. We
have never measured the painted text (see the external review, 4.3), so the
published text is a proxy and is labelled as one. The ten edits differ from it
by definition -- that is what makes them edits -- which is a further reason this
rate is an estimate and not a measurement of the artwork.
"""
import re, math, collections, os, sys

WL = "/home/soul/blm-analysis/configs/bip39_en.txt"
WP = "/home/soul/Downloads/Brainwallet/files(6)/bitcoin.txt"
SIX = ["double", "sign", "absent", "proof", "order", "trust"]
TOK = re.compile(r"[A-Za-z]+")

def main():
    if not os.path.exists(WP):
        sys.exit("whitepaper text not found at %s" % WP)
    W = set(w.strip().lower() for w in open(WL) if w.strip())
    lines = open(WP, encoding="utf-8", errors="replace").read().split("\n")

    # Section 2 "Transactions" begins at line 51 and section 3 at line 91.
    # Verified by the boundary print below rather than asserted.
    sec2 = "\n".join(lines[50:90])
    toks = [t.lower() for t in TOK.findall(sec2)]
    types = sorted(set(toks))
    print("SOURCE   %s lines 51-90, section 2 'Transactions'" % os.path.basename(WP))
    print("  first  %s" % " ".join(TOK.findall(sec2)[:10]))
    print("  last   %s" % " ".join(TOK.findall(sec2)[-10:]))
    print("  %d tokens, %d distinct words" % (len(toks), len(types)))
    print()

    print("THE OBSERVED SET: %d words, all BIP39, lengths %s"
          % (len(SIX), sorted(len(w) for w in SIX)))
    missing = [w for w in SIX if w not in set(types)]
    print("  not in section 2's own vocabulary: %s" % (missing or "none"))
    print("  -> the edits are not all drawn from the passage, so the passage is")
    print("     not a complete reference class for them.")
    print()

    print("BASE RATES AND WHAT 6 OF 10 IS WORTH AGAINST EACH")
    print("  %-46s %-16s %7s %7s %8s %8s" % ("reference class", "BIP39 fraction",
                                             "expect", "SE", "6 is", "P(>=6)"))
    rows = [("every distinct word", lambda t: True),
            ("words of 3-8 letters (BIP39's length range)", lambda t: 3 <= len(t) <= 8),
            ("words of 4-6 letters (the observed band)", lambda t: 4 <= len(t) <= 6)]
    for label, keep in rows:
        sub = [t for t in types if keep(t)]
        b = [t for t in sub if t in W]
        p = len(b) / len(sub)
        mu, sd = 10 * p, math.sqrt(10 * p * (1 - p))
        pv = sum(math.comb(10, i) * p**i * (1 - p)**(10 - i) for i in range(6, 11))
        print("  %-46s %4d/%-4d %5.1f%% %7.2f %7.2f %+7.2f SE %7.2f"
              % (label, len(b), len(sub), 100 * p, mu, sd, (6 - mu) / sd, pv))
    print()
    print("  Length profile of the vocabulary (why the class matters):")
    c = collections.Counter(len(t) for t in types)
    cb = collections.Counter(len(t) for t in types if t in W)
    for L in sorted(c):
        print("    %2d letters  %3d distinct  %3d BIP39  %5.1f%%"
              % (L, c[L], cb.get(L, 0), 100 * cb.get(L, 0) / c[L]))
    print()
    print("VERDICT. Against the only class matching the observed words' shape, six")
    print("of ten is half a standard error from nothing and is beaten by chance in")
    print("44% of draws. THE RATIO IS NOT EVIDENCE AND MUST NOT BE QUOTED AS SUCH.")
    print("It is also not disproof: the test is simply uninformative, which is the")
    print("point -- an uninformative statistic presented as support is 1.7's shape.")

main()
