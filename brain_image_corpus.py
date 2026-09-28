#!/usr/bin/env python3
"""Rebuild the §2.12 image-text brainwallet corpus from sources that survive.

WHY THIS EXISTS. §2.12 reports 22,638 keys for the image-text corpus. No
generator script, no key list and no log for that run survives in this tree, so
the figure rests on the report's own prose and cannot be reproduced. This script
rebuilds the corpus from what IS still here and prints a count that can be
compared against 22,638. It does not assume the old number was right, and a
mismatch is a result, not a bug.

SOURCES, all of them still in the repo:
  - slogan_lines.py    HEADLINE / AMENDMENT / WHITEPAPER / BLOCK and the seven
                       coloured lines. This is the transcription of record.
  - REPORT.md §7       the decoded Russian plaintexts
  - REPORT.md §1.4     the micro-text inside the E of BRAVE, and the true
                       whitepaper sentence it was spliced from
  - REPORT.md §2.12    its own description of the corpus, used as a checklist
  - the target address itself
  - the PNG file and its IDAT payload

VARIANTS. §2.12 claims "casing / punctuation-stripped / whitespace-stripped
variants". Those are generated here as a cross product and then deduplicated,
which is where most of the count goes: for a single lowercase BIP39 word,
stripping is a no-op and only the casings differ.

KEY VARIANTS. Two hashes (SHA256, double-SHA256) x three pubkey encodings
(compressed, uncompressed, hybrid) = 6 addresses per distinct key string.
BRAINSPACE is NOT a separate axis here: for free text, "space-joined vs
concatenated" IS the whitespace-stripped string variant, and counting it twice
would inflate the total. That is why this is 6 per key and the template corpus
is 12.

    python3 brain_image_corpus.py --count-only    # enumerate, count, write list
    python3 brain_image_corpus.py --run           # derive and compare
"""
import sys, os, re, hashlib, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
TARGET_ADDR = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"
TARGET_H160 = "ccbd031e54cde2a3189fd59bc49f731367a1779e"

# ------------------------------------------------------------------ sources
HEADLINE = """FIND THE SEED PHRASE IN THE THIS PICTURE
Order and stability
COVID IS A HOAX IS THE KILLER
I CAN NOT BREATHE
BLACK LIVES MATTER NO JUSTICE NO PEACE END POLICE BRUTALITY
STOP KILLING US NOT ONE MORE
WELCOME TO THE BRAVE NEW WORLD
ONLY REAL BITCOIN PAY FOR THE FUTURE THIS IS THE FIRST PREDICTION
FUCK THIS SHIT"""

AMENDMENT = """Section Neither slavery nor involuntary servitude except as a punishment
for crime whereof the party shall have been duly convicted shall exist
within the United States or any place subject to their jurisdiction"""

WHITEPAPER = """in which they were received The payee needs proof that at the time of each
transaction the majority of nodes agreed it was the first received"""

BLOCK = ("BLACK LIVES MATTER NO JUSTICE NO PEACE END POLICE BRUTALITY "
         "STOP KILLING US NOT ONE MORE")

LINES = ["BLACK", "LIVES", "MATTER", "NO JUSTICE NO PEACE",
         "END POLICE BRUTALITY", "STOP KILLING US", "NOT ONE MORE"]

# §7. The right-edge line ends in the unresolved glyph X, so it is carried both
# without a final token and truncated before `номер` -- the corpus cannot
# contain a string nobody can read.
RUSSIAN = [
    "Сумма двух чисел",
    "здесь зашифрованы биткоины на чёрный день номер",
    "здесь зашифрованы биткоины на чёрный день",
    "здесь зашифрованы биткоины",
    "Я надеюсь",
    "будут присылать",
]

# §1.4, as transcribed, including the typo `introdue` at the splice.
MICROTEXT = ("common solution is to introdue cent ral au thority or mint that "
             "checks every transac tion for double spen ding. After")
MICRO_FRAGS = ["common solution", "is to introdue", "cent", "ral au", "thority",
               "or mint that", "checks every", "transac", "tion",
               "for double spen", "ding. After"]
WP_TRUE = ("A common solution is to introduce a trusted central authority, or "
           "mint, that checks every transaction for double spending.")

# §7.4. The final character is a literal drawn `?`, not a digit, so the string is
# carried as written rather than expanded over the ten readings it might stand for.
DATES = ["1865", "2020", "1865-202?", "1865 - 202?", "1865\u2013202?", "1865-2020"]

# §2.12's "Latin mottos". These are NOT the Great Seal mottos -- searching for
# novus/ordo/seclorum/annuit/coeptis finds nothing because the artwork's Latin is
# different text entirely, and it lives in census_crops.py's ELEMENTS and SCREENED
# lists and in the seal-ring measurement, not in the prose.
#
#   census_crops.py:46          Esse quam niger es, sic dixit caccobus ollae  (36)
#   census_crops.py SCREENED    pyramid base FIAT JUSTITIA ET PEREAT MUNDUS   (26)
#   seal_ring.py / report_additions_image_pass.md
#                               ring reads RERUM COGNOSCERE CAUSAS, mirror-written
#
# Both readings of the ring are carried: the three words as drawn, and the full
# Virgil line they are the tail of. The canonical `esse quam videri` that the
# niger line plays on is carried too, since it is the phrase a solver would try.
LATIN_MOTTOS = [
    "Esse quam niger es, sic dixit caccobus ollae",
    "Esse quam videri",
    "RERUM COGNOSCERE CAUSAS",
    "Felix qui potuit rerum cognoscere causas",
    "FIAT JUSTITIA ET PEREAT MUNDUS",
]

# Other text elements the census records that the first pass missed. Note the
# apostrophe form: census_crops has "I can't BREATHE" where slogan_lines.py's
# transcription has "I CAN NOT BREATHE". Both are carried -- which one is on the
# canvas is a transcription judgement and SHA-256 does not forgive either way.
CENSUS_MISC = ["I can't BREATHE", "BLM", ".VS.", "CVD19", "TOWER", "MOON",
               "ONLY real BITCOIN", "PAY FOR THE FUTURE.",
               "THIS IS THE FIRST PREDICTION."]

def bip39_words():
    for d in (os.path.dirname(os.path.abspath(__file__)),
              os.path.expanduser("~/Downloads/Brainwallet/files(6)")):
        p = os.path.join(d, "bip39_en.txt")
        if os.path.exists(p):
            return [w.strip() for w in open(p) if w.strip()]
    raise SystemExit("bip39_en.txt not found")

def png_bytes():
    for p in (os.path.expanduser("~/Downloads/Brainwallet/files(6)/imges/0.2-btc-puzzle.png"),
              os.path.expanduser("~/Downloads/0.2-btc-puzzle.png")):
        if os.path.exists(p):
            return p, open(p, "rb").read()
    return None, None

def idat_payload(raw):
    """Concatenated IDAT chunk data, no headers, no CRCs."""
    out, i = b"", 8
    while i + 8 <= len(raw):
        ln = int.from_bytes(raw[i:i+4], "big"); typ = raw[i+4:i+8]
        if typ == b"IDAT": out += raw[i+8:i+8+ln]
        i += 12 + ln
        if typ == b"IEND": break
    return out

# ----------------------------------------------------------------- variants
PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
WS    = re.compile(r"\s+", re.UNICODE)

# The description's degrees of freedom, as flags. §2.12's sentence does not fix
# any of these, which is what "underdetermined" means concretely.
DEFAULTS = dict(punct=True, ws=True, title=True,
                pairwise_variants=False, bip39_casing=True, whole_text=True)

# Every flag is MONOTONE -- setting one True only ever adds strings, never
# removes or replaces them -- so the all-True reading is the union of all 64
# readings the description admits. Deriving it means a miss covers every corpus
# §2.12's sentence could denote, not merely the one reading picked here.
MAXIMAL = dict.fromkeys(DEFAULTS, True)

def variants(s, F=None):
    """casing x {as-is, punctuation-stripped} x {spaced, whitespace-stripped}."""
    F = DEFAULTS if F is None else F
    out = set()
    bases = [s] + ([PUNCT.sub("", s)] if F["punct"] else [])
    for base in bases:
        forms = [base, base.lower(), base.upper()]
        if F["title"]: forms.append(base.title())
        for form in forms:
            out.add(WS.sub(" ", form).strip())
            if F["ws"]: out.add(WS.sub("", form))
    return {v for v in out if v}

# -------------------------------------------------------------------- build
def build(F=None):
    F = DEFAULTS if F is None else F
    groups = {}
    def add(name, strings, use_variants=True):
        acc = set()
        for s in strings:
            acc |= variants(s, F) if use_variants else {s}
        groups[name] = acc

    add("headline lines",   HEADLINE.split("\n"))
    if F["whole_text"]: add("headline whole", [HEADLINE])
    add("amendment",        AMENDMENT.split("\n") + ([AMENDMENT] if F["whole_text"] else []))
    add("whitepaper strip", WHITEPAPER.split("\n") + ([WHITEPAPER] if F["whole_text"] else []))
    add("slogan block",     [BLOCK])
    add("slogan lines",     LINES)
    add("slogan words",     sorted({w for l in LINES for w in l.split()}))
    add("russian",          RUSSIAN)
    add("russian words",    sorted({w for r in RUSSIAN for w in r.split()}))
    add("micro-text",       MICRO_FRAGS + ([MICROTEXT] if F["whole_text"] else []))
    add("whitepaper true",  [WP_TRUE])
    add("dates",            DATES)
    add("latin mottos",     LATIN_MOTTOS)
    add("census misc",      CENSUS_MISC)
    add("target address",   [TARGET_ADDR])
    add("bip39 words",      bip39_words(), use_variants=F["bip39_casing"])

    # §2.12: "pairwise concatenations of 33 salient phrases under three joiners"
    # §2.12 says 33 salient phrases. The natural list from the surviving sources
    # is 34. An earlier version of this script sliced it to [:33], which enforced
    # the reported figure and then let it be read back as agreement -- the count
    # was an artefact of the slice, not a measurement. The slice is gone; the
    # natural count is printed, and the one-item discrepancy is left visible
    # because it is informative: it points either at which phrase the original
    # excluded or at a different counting convention.
    salient = (HEADLINE.split("\n") + LINES + RUSSIAN[:3] + DATES + LATIN_MOTTOS +
               [BLOCK, WP_TRUE, MICROTEXT, TARGET_ADDR])
    pairs = set()
    for a in salient:
        for b in salient:
            if a is b: continue
            for j in ("", " ", "-"):
                pairs.add(j.join((a, b)))
    if F["pairwise_variants"]:
        pv = set()
        for p in pairs: pv |= variants(p, F)
        pairs = pv
    groups[f"pairwise ({len(salient)} phrases, 3 joiners)"] = pairs

    p, raw = png_bytes()
    filehash = set()
    if raw:
        d1 = hashlib.sha256(raw).digest()
        i1 = hashlib.sha256(idat_payload(raw)).digest()
        filehash = {d1.hex(), hashlib.sha256(d1).hexdigest(),
                    i1.hex(), hashlib.sha256(i1).hexdigest()}
    groups["png / IDAT digests"] = filehash
    return groups, p

# --------------------------------------------------------------------- main
def sweep(target=22638):
    """Enumerate the description's binary readings and print each total.

    §2.12 does not say whether the pairwise concatenations get the casing and
    stripping treatment, whether the 2048 BIP39 words get casing, or whether the
    whole-document concatenations are in. Each is a coin flip the sentence leaves
    open, so enumerate them rather than pick one and call the rest a gap."""
    from itertools import product
    keys = ["punct", "ws", "title", "pairwise_variants", "bip39_casing", "whole_text"]
    rows, exact = [], []
    for combo in product([False, True], repeat=len(keys)):
        F = dict(zip(keys, combo))
        g, _ = build(F)
        tot = len(set().union(*g.values())) if g else 0
        rows.append((tot, F))
        if tot == target: exact.append(F)
    rows.sort(key=lambda r: r[0])
    print(f"  {'total':>9}  " + "  ".join(f"{k[:9]:>9}" for k in keys))
    for tot, F in rows:
        mark = "  <== MATCHES 22,638" if tot == target else ""
        print(f"  {tot:>9,}  " + "  ".join(f"{str(F[k]):>9}" for k in keys) + mark)
    lo, hi = rows[0][0], rows[-1][0]
    print(f"\n  band across all {len(rows)} readings: {lo:,} to {hi:,}")
    print(f"  22,638 is {'INSIDE' if lo <= target <= hi else 'OUTSIDE'} the band")
    if exact:
        print(f"\n  *** {len(exact)} reading(s) reproduce 22,638 EXACTLY -- corpus RECOVERED ***")
        for F in exact: print("    " + ", ".join(f"{k}={F[k]}" for k in keys))
    else:
        near = min(rows, key=lambda r: abs(r[0] - target))
        print(f"\n  no exact reading. nearest {near[0]:,} "
              f"(off by {near[0]-target:+,}): "
              + ", ".join(f"{k}={near[1][k]}" for k in keys))
    return exact

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--count-only"
    if mode == "--sweep":
        sys.exit(0 if sweep() else 0)
    # --run derives the MAXIMAL reading: the union of all 64, so the negative
    # covers the whole space of readings rather than one choice among them.
    F = MAXIMAL if mode == "--run" else DEFAULTS
    groups, png = build(F)
    seen, rows = set(), []
    for name, acc in groups.items():
        new = acc - seen
        rows.append((name, len(acc), len(new)))
        seen |= acc
    print(f"  image file: {png or '(not found -- digest group empty)'}\n")
    print(f"  {'source group':<38} {'strings':>9} {'new':>9}")
    for n, t, d in rows: print(f"  {n:<38} {t:>9,} {d:>9,}")
    print(f"  {'':<38} {'':>9} {'-'*9}")
    print(f"  {'DISTINCT KEY STRINGS':<38} {'':>9} {len(seen):>9,}")
    print(f"\n  reading: {'MAXIMAL (union of all 64)' if F is MAXIMAL else 'best-justified'}")
    print(f"  addresses = {len(seen):,} x 2 hashes x 3 encodings = {len(seen)*6:,}")
    print(f"  §2.12 reports 22,638 keys.  ratio = {len(seen)/22638:.2f}x")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brain_image_keys.txt")
    with open(out, "w") as f:
        for s in sorted(seen): f.write(s.replace("\n", "\\n") + "\n")
    print(f"  key list written: {out}")

    if mode == "--count-only":
        print("\n  --count-only: no derivation performed.")
        sys.exit(0)

    from coincurve import PrivateKey
    def h160(b):
        return hashlib.new("ripemd160", hashlib.sha256(b).digest()).digest()
    tgt, hits, n = bytes.fromhex(TARGET_H160), [], 0
    for s in seen:
        msg = s.encode("utf-8")
        d = hashlib.sha256(msg).digest()
        for kd in (d, hashlib.sha256(d).digest()):
            if not (1 <= int.from_bytes(kd, "big") < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141):
                continue
            pk = PrivateKey(kd).public_key
            u = pk.format(compressed=False)           # 0x04 || X || Y
            for pub in (pk.format(compressed=True), u,
                        bytes([0x06 | (u[64] & 1)]) + u[1:]):
                n += 1
                if h160(pub) == tgt: hits.append((s, kd.hex(), pub.hex()))
    print(f"\n  derived {n:,} addresses")
    print("  " + ("NO MATCH" if not hits else f"*** {len(hits)} HIT ***"))
    for s, k, p in hits: print(f"    phrase={s!r}\n    priv={k}\n    pub={p}")
    sys.exit(0 if not hits else 3)
