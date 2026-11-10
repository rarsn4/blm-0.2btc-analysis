#!/usr/bin/env python3
"""HH. The two external edit lists, tested exactly, on the tokens their authors
actually wrote.

WHY THIS SUPERSEDES wp_bip39_baserate.py (EE-2). That script hardcoded the
observed set as ["double","sign","absent","proof","order","trust"] and called it
"six of the ten edits". Two of those six are NOT edit tokens. The primary source
(their README.md:362-363, fetched 9 Nov 2026) lists the painted forms "abcense"
and a deleted "a trusted" -- whose whitepaper targets are ABSENCE and TRUSTED,
neither of which is a BIP39 word. `absent` and `trust` ARE BIP39 words, and they
entered our count by stemming. So our own six-of-ten was built by the very
normalisation this project refused to allow the 2021 list in external review
4.3b ("a reader who writes ABSENCE and a reader who writes absent did not
transcribe the same string"). Measured on exact targets the count is FOUR.

TWO LISTS, ONE STANDARD. Both lists are graded [EXTERNAL, UNLOCATED]: neither
has been re-derived from pixels here. The test below applies the same rule to
both -- exact token, no stemming -- and conditions on length, because BIP39
holds no word under 3 letters or over 8 and a word outside that band cannot be
BIP39 whatever the artist intended.

EXACT, NOT NORMAL-APPROXIMATE. Each token carries its own length and therefore
its own BIP39 probability, so the count is Poisson-binomial, not binomial. The
distribution is computed exactly by convolution; no SE, no normal tail.
"""
import re, hashlib, collections, os, sys

A  = "/home/soul/blm-analysis"
WL = A + "/configs/bip39_en.txt"
WP = "/home/soul/Downloads/Brainwallet/files(6)/bitcoin.txt"
TOK = re.compile(r"[A-Za-z]+")

# ---------------------------------------------------------------- primary source
# README.md:362-363 [THEIRS], verbatim:
#   "the copy carries ten edits (introdue, doudle, sing for sign, abcense,
#    participans, wich, proot, transactian, a deleted "a trusted", and "oder"
#    for "order", the only edit on a device word)"
# painted form -> the whitepaper word it alters.
L2026 = [("introdue",    "introduce"),
         ("doudle",      "double"),
         ("sing",        "sign"),
         ("abcense",     "absence"),
         ("participans", "participants"),
         ("wich",        "which"),
         ("proot",       "proof"),
         ("transactian", "transaction"),
         ("(deleted)",   "trusted"),      # a deleted "a trusted"
         ("oder",        "order")]

# glrfjsz, u/Accomplished_Weird36, 2021-02-02, verbatim:
#   "I chose these words. Here they are. SIGN, DOUBLE, FATE, AWARE, A TRUSTED,
#    ABSENCE, WHICH, MINI, and others."
# "and others" is theirs: this list is SELF-REPORTED INCOMPLETE.
L2021 = ["sign", "double", "fate", "aware", "trusted", "absence", "which", "mini"]
L2021_AS_WRITTEN = ["SIGN","DOUBLE","FATE","AWARE","A TRUSTED","ABSENCE","WHICH","MINI"]

def poisson_binomial(ps):
    d = [1.0]
    for p in ps:
        nd = [0.0] * (len(d) + 1)
        for k, v in enumerate(d):
            nd[k]     += v * (1 - p)
            nd[k + 1] += v * p
        d = nd
    return d

def main():
    raw = open(WL, "rb").read()
    W = [w.strip().lower() for w in raw.decode().split("\n") if w.strip()]
    S = set(W)
    c = collections.Counter(len(w) for w in W)

    print("=" * 78)
    print("0. THE WORDLIST, MEASURED (HH-2)")
    print("=" * 78)
    print("  file      %s" % WL)
    print("  words     %d" % len(W))
    print("  md5       %s   (file as stored here)" % hashlib.md5(raw).hexdigest())
    print("  sha256    %s" % hashlib.sha256(raw).hexdigest())
    norm = ("\n".join(W) + "\n").encode()
    print("  md5       %s   (normalised: sorted, \\n, trailing newline)"
          % hashlib.md5(norm).hexdigest())
    print("  HH-2 cites md5 f23506956964fa69c98fa3fb5c8823b5 -- %s"
          % ("MATCHES one of the above" if "f23506956964fa69c98fa3fb5c8823b5" in
             (hashlib.md5(raw).hexdigest(), hashlib.md5(norm).hexdigest())
             else "matches NEITHER form here; the distribution below is what the claim rests on"))
    print("  lengths   %s" % "  ".join("%d:%d" % (L, c[L]) for L in sorted(c)))
    print("  min %d, max %d" % (min(c), max(c)))
    print("  HH-2's distribution 3:103 4:442 5:555 6:508 7:352 8:88 -- %s"
          % ("CONFIRMED" if dict(c) == {3:103,4:442,5:555,6:508,7:352,8:88} else "DIFFERS"))
    print()
    print("  CONSEQUENCE: a word of 9 or more letters is STRUCTURALLY ineligible,")
    print("  not merely unlikely. Eligibility is a property of the word, not of")
    print("  the artist's intent, and must be conditioned on before any ratio.")
    print()

    print("=" * 78)
    print("1. THE TEN 2026 EDITS, ON EXACT TARGETS (HH-1)")
    print("=" * 78)
    print("  %-14s %-14s %4s %4s %-8s" % ("painted", "target", "len", "elig", "BIP39"))
    for painted, tgt in L2026:
        el = 3 <= len(tgt) <= 8
        print("  %-14s %-14s %4d %4s %-8s" % (painted, tgt, len(tgt),
              "yes" if el else "NO", "yes" if tgt in S else "no"))
    t26 = [t for _, t in L2026]
    el26 = [t for t in t26 if 3 <= len(t) <= 8]
    b26  = [t for t in el26 if t in S]
    inel = [t for t in t26 if not (3 <= len(t) <= 8)]
    print()
    print("  ten targets        %s" % ", ".join(t26))
    print("  structurally out   %s  (%d)" % (", ".join(inel), len(inel)))
    print("  eligible           %d" % len(el26))
    print("  BIP39, exact       %d  (%s)" % (len(b26), ", ".join(b26)))
    print("  ratio of eligible  %d/%d = %.1f%%" % (len(b26), len(el26), 100*len(b26)/len(el26)))
    print()
    stem = {"absence": "absent", "trusted": "trust"}
    print("  THE COMMITTED FIGURE WAS SIX. The two extra came from stemming:")
    for k, v in stem.items():
        print("    %-9s not BIP39  ->  counted as %-7s BIP39 %s"
              % (k, v, "yes" if v in S else "no"))
    print("  HH-2 states 6 of 7 eligible = 85.7 per cent. Measured on exact targets it is")
    print("  %d of %d = %.1f%%. HH-2's eligibility split is exactly right and names the"
          % (len(b26), len(el26), 100*len(b26)/len(el26)))
    print("  right three long words; its numerator inherits our stemming defect.")
    print()

    print("=" * 78)
    print("2. OVERLAP OF THE TWO LISTS, EXACT TARGETS (HH-1)")
    print("=" * 78)
    s26, s21 = set(t26), set(L2021)
    both = [t for t in L2021 if t in s26]
    only21 = [t for t in L2021 if t not in s26]
    only26 = [t for t in t26 if t not in s21]
    print("  2021 as written    %s" % ", ".join(L2021_AS_WRITTEN))
    print("  2021 as targets    %s" % ", ".join(L2021))
    print()
    print("  IN BOTH LISTS      %d: %s" % (len(both), ", ".join(both)))
    print("  2021 only          %d: %s" % (len(only21), ", ".join(only21)))
    print("  2026 only          %d: %s" % (len(only26), ", ".join(only26)))
    print()
    print("  `which` IS IN THE 2026 LIST (painted `wich`), so the review's row")
    print("  'we hold only the six BIP39 of their ten, so which may or may not be")
    print("  among the four we do not hold' is VOID: we hold all ten, and it is.")
    print("  Exact-token overlap is %d, not two and not three." % len(both))
    print("  The two pairs the review demoted to 'root only' -- ABSENCE/absent and")
    print("  A TRUSTED/trust -- were demoted against OUR stemmed rendering, not")
    print("  against their text. Both readers wrote the same word. The demotion was")
    print("  an artefact of our own normalisation.")
    print()

    # ------------------------------------------------------- base rate by length
    lines = open(WP, encoding="utf-8", errors="replace").read().split("\n")
    sec2 = "\n".join(lines[50:90])
    types = sorted(set(t.lower() for t in TOK.findall(sec2)))
    byL  = collections.Counter(len(t) for t in types)
    byLB = collections.Counter(len(t) for t in types if t in S)
    print("=" * 78)
    print("3. THE REFERENCE CLASS, BY LENGTH (bitcoin.txt lines 51-90, section 2)")
    print("=" * 78)
    print("  %4s %9s %7s %8s" % ("len", "distinct", "BIP39", "p"))
    for L in sorted(byL):
        print("  %4d %9d %7d %7.1f%%" % (L, byL[L], byLB.get(L, 0),
                                         100 * byLB.get(L, 0) / byL[L]))
    pL = {L: byLB.get(L, 0) / byL[L] for L in byL}
    print()
    print("  Section 2 is a PROXY: it is the whitepaper as published, not as")
    print("  painted, and we have never measured the painted text. Words absent")
    print("  from it (fate, mini) take the rate of their length class.")
    print()

    print("=" * 78)
    print("4. EXACT POISSON-BINOMIAL, SAME TEST ON BOTH LISTS (HH-2, HH-4)")
    print("=" * 78)
    def test(label, toks):
        el = [t for t in toks if 3 <= len(t) <= 8]
        ps = [pL.get(len(t), 0.0) for t in el]
        obs = sum(1 for t in el if t in S)
        d = poisson_binomial(ps)
        pv = sum(d[obs:])
        mu = sum(ps)
        print("  %s" % label)
        print("    eligible tokens %d, lengths %s" % (len(el), [len(t) for t in el]))
        print("    per-token p     %s" % ["%.3f" % p for p in ps])
        print("    expected %.2f   observed %d   P(X >= %d) = %.3f"
              % (mu, obs, obs, pv))
        return obs, mu, pv
    print()
    test("2026 list (ten edits, their README)", t26)
    print()
    test("2021 list (eight words, glrfjsz)", L2021)
    print()
    o, m, p = test("THE FIVE BOTH READERS NAMED -- the only alterations with two"
                   "\n  independent witnesses", both)
    print()
    print("  Where the two readers AGREE, the BIP39 rate is %d of %d against an"
          % (o, len(both)))
    print("  expectation of %.2f: P(X >= %d) = %.3f. The agreed set is the one with" % (m, o, p))
    print("  the best provenance in the whole question, and it shows NOTHING.")
    print()
    print("=" * 78)
    print("5. WHAT THIS DOES AND DOES NOT SETTLE")
    print("=" * 78)
    print("  The ratio is not evidence of design, on either list, on any class.")
    print("  It is also not disproof. The test is uninformative, which is the")
    print("  point: an uninformative statistic presented as support is 1.7's shape.")
    print()
    print("  The confound HH-4 names is real and is NOT measured here:")
    print("    - glrfjsz: 'Sorry, I'm using a translator.'")
    print("    - gn69cqa (same author, 11 days later): 'somvols' for symbols.")
    print("    - 'A TRUSTED' and 'ABSENCE' are a phrase and a noun form; the 2026")
    print("      list gives painted misspellings. The two are not the same kind of")
    print("      object, and transcription quality is unequal and unquantified.")
    print("    - 'and others': the 2021 list is SELF-REPORTED INCOMPLETE, and its")
    print("      author says 'I chose these words' -- a selected subset, not a")
    print("      transcription. A ratio over a self-selected subset of an unstated")
    print("      total is not a ratio over the alterations.")
    print()
    print("  HH-4 asks for the claim 'the two lists disagree enough that NEITHER")
    print("  supports a ratio'. MEASURED, THEY DO NOT DISAGREE: %d of the 2021" % len(both))
    print("  list's eight targets are in the 2026 list of ten. The ratio argument")
    print("  does not need their disagreement and must not be rested on it. It")
    print("  rests on the agreed five showing nothing, and on the 2026 list's own")
    print("  exact count being %d of %d eligible." % (len(b26), len(el26)))
    print()
    print("  RETRACTED by this script: 'A designed signal does not halve when a")
    print("  different person reads the same marks' (external review 4.3b). The")
    print("  halving it describes -- 60 per cent to 37.5 per cent -- compared a stemmed")
    print("  numerator over ten to an exact numerator over eight, across two different")
    print("  length mixes. There was no halving to explain.")

main()
