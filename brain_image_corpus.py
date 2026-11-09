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

[DEFECT, found and closed 2026-11-02] THIS CORPUS ONCE HASHED STRINGS THAT ARE NOT ON
THE CANVAS. A letterform re-read of every element against the master image
(`letterform_audit.md`) found six of the 22 Latin-letterform elements differing from
what this file held, and five drawn strings it did not contain at all. All six are now
corrected above and all five are added; two readings that did NOT clear REPORT 9's
native-pixel rule are carried as EXTRA strings in INDETERMINATE rather than substituted,
and every superseded form is kept in SUPERSEDED so the 28 Sep negative stays
reproducible. See REPORT 1.8.

THE RULE THIS PRODUCED, AND WHAT ENFORCES IT. No transcription enters this corpus
without a dated letterform re-read against the master image, and no element the project
measures anywhere may stay out of this corpus silently. `corpus_gate.py` enforces the
second half: it reconciles `census_crops.DRAWN` -- the canvas census, with coordinates
and provenance -- against the strings this file actually generates, and REFUSES, not
warns, if any measured element is absent or differs. It is keyed on the content of both
sides, so it re-proves itself on any edit rather than trusting a timestamp. The
brainwallet queue calls it first. Do not run this corpus by hand past a gate failure.

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
COVID 19 IS A HOAX 5G IS THE KILLER
I CAN NOT BREATHE
BLACK LIVES MATTER NO JUSTICE NO PEACE END POLICE BRUTALITY
STOP KILLING US NOT ONE MORE
WELCOME TO THE BRAVE NEW WORLD
ONLY REAL BITCOIN PAY FOR THE FUTURE THIS IS THE FIRST PREDICTION
FUCK THIS SHIT"""

# [CORRECTED 2026-11-02, letterform_audit.md 1.3] The heading carries an underlined
# numeral -- `Section 1.` -- which the first transcription dropped, and the body is
# drawn WITH punctuation. The old unpunctuated form is kept in SUPERSEDED below.
AMENDMENT = """Section 1.
Neither slavery nor involuntary servitude, except as a punishment
for crime whereof the party shall have been duly convicted shall exist
within the United States, or any place subject to their jurisdiction."""

# [CORRECTED 2026-11-02, letterform_audit.md 1.5] `received.` takes a full stop and
# `transaction,` a comma. `which` is LEFT as `which`: `wich` stays [INDETERMINATE]
# because the ascender band lies under the frame stripe (rows y1154-1160 are the
# stripe, 61 of 67 px below grey 110). The `wich` reading is carried as an EXTRA in
# INDETERMINATE below rather than substituted here.
WHITEPAPER = """in which they were received. The payee needs proof that at the time of each
transaction, the majority of nodes agreed it was the first received"""

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
#
# [CORRECTED 2026-11-02, letterform_audit.md 1.4] Measured at NATIVE pixels: the block's
# lines run 19 px / 19 px / 15 px against 4.4 px per character, calibrated on
# `common solution` (66 px / 15 ch). The old split `transac` (7 ch = 31 px) + `tion`
# would need a 31 px line and there is none. The drawn word is `transactions.` --
# plural and stopped -- broken as `tran` / `sacti` / `ons.`, and the next line opens
# with a capital `For`. `thority,` takes a comma.
#
# The mint-word is drawn `m-i-n-i` or `m-i-n-t` with a stop before `that`; at 6 px that
# is [INDETERMINATE], so BOTH are carried rather than one being chosen.
MICROTEXT = ("common solution is to introdue cent ral au thority, or mini.that "
             "checks every tran sacti ons. For double spen ding. After")
MICROTEXT_ALT = ("common solution is to introdue cent ral au thority, or mint.that "
                 "checks every tran sacti ons. For double spen ding. After")
MICRO_FRAGS = ["common solution", "is to introdue", "cent", "ral au", "thority,",
               "or mini.that", "or mint.that", "checks every", "tran", "sacti",
               "ons.", "For double spen", "ding. After"]
WP_TRUE = ("A common solution is to introduce a trusted central authority, or "
           "mint, that checks every transaction for double spending.")

# §7.4. The final character is a literal drawn `?`, not a digit, so the string is
# carried as written rather than expanded over the ten readings it might stand for.
# [CORRECTED 2026-11-02, letterform_audit.md 1.6] Measured at NATIVE pixels: between the
# final `2` and the red `?` there are THREE ink blobs -- 14/13/13 px, evenly stepped at
# x318-321, x323-326, x328-331 y707-719 -- distinct from the `?`'s own dot at x334-337.
# The ellipsis forms are added; the earlier forms are kept, since they were tested.
DATES = ["1865", "2020", "1865-202?", "1865 - 202?", "1865\u2013202?", "1865-2020",
         "1865-202...?", "1865 - 202...?", "1865\u2013202...?", "1865-202\u2026?"]

# §2.12's "Latin mottos". These are NOT the Great Seal mottos -- searching for
# novus/ordo/seclorum/annuit/coeptis finds nothing because the artwork's Latin is
# different text entirely, and it lives in census_crops.py's ELEMENTS and SCREENED
# lists and in the seal-ring measurement, not in the prose.
#
#   census_crops.py:46          Esse quam niger es, sic dixit caccabus ollae  (36)
#   census_crops.py SCREENED    pyramid base FIAT JUSTITIA ET PEREAT MUNDUS   (26)
#   seal_ring.py / report_additions_image_pass.md
#                               ring reads RERUM COGNOSCERE CAUSAS, mirror-written
#
# Both readings of the ring are carried: the three words as drawn, and the full
# Virgil line they are the tail of. The canonical `esse quam videri` that the
# niger line plays on is carried too, since it is the phrase a solver would try.
LATIN_MOTTOS = [
    "Esse quam niger es, sic dixit caccabus ollae",
    "Esse quam videri",
    "RERUM COGNOSCERE CAUSAS",
    "Felix qui potuit rerum cognoscere causas",
    "FIAT JUSTITIA ET PEREAT MUNDUS",
    # [ADDED 2026-11-02] Mirror-written on the seal's lower scroll. Measured since
    # `seal_ring.py:13`, where it is the glyph-count control, and never carried here.
    "UBI BENE IBI PATRIA",
]

# Other text elements the census records that the first pass missed. Note the
# apostrophe form: census_crops has "I can't BREATHE" where slogan_lines.py's
# transcription has "I CAN NOT BREATHE". Both are carried -- which one is on the
# canvas is a transcription judgement and SHA-256 does not forgive either way.
CENSUS_MISC = ["I can't BREATHE", "BLM", ".VS.", "CVD19", "TOWER", "MOON",
               "ONLY real BITCOIN", "PAY FOR THE FUTURE.",
               "THIS IS THE FIRST PREDICTION.",
               # [ADDED 2026-11-02] Drawn, measured elsewhere in this project for
               # months, and never carried here. See letterform_audit.md 3.
               "05.25.20",             # hoodie,      x992-1069  y370-388
               "11.03.20",             # under .VS.,  x1012-1098 y1098-1122
               "BREATHE",              # neck band,   x1355-1430 y528-545
               "CHR",                  # monogram,    x1520-1590 y1125-1165
               ]

# [ADDED 2026-11-02] Readings that did NOT clear REPORT 9's rule -- nothing enters the
# record from an upscaled view until it survives a native-pixel re-measurement with a
# control. They are carried as EXTRA strings, never as replacements, because each is a
# canvas reading that may be right and hashing one more string costs nothing.
#
#   PAY FOR THE FVTURE.  pointed V in position 2 against a flat-bottomed U in position 4
#                        of the same word; at native resolution the word is one merged
#                        blob with no inter-letter gaps.
#   \u00b7VS\u00b7              the two dots sit 9 px and 23 px above a baseline of 33 px cap
#                        height, diagonally opposed as a 180\u00b0 ambigram requires -- not
#                        baseline full stops. Whether that makes the string U+00B7 is a
#                        transcription convention, not a measurement.
#   wich                 favours `wich` at 34x, but the ascender band lies under the
#                        frame stripe. Carried for the same reason as the other two.
INDETERMINATE = [
    "PAY FOR THE FVTURE.",
    "\u00b7VS\u00b7",
    ("in which they were received. The payee needs proof that at the time of each "
     "transaction, the majority of nodes agreed it was the first received"
     ).replace("in which", "in wich"),
]

# Strings this corpus hashed BEFORE the 2 Nov letterform re-read and that the re-read
# showed are NOT on the canvas. They are kept, not deleted: they were tested, and
# removing them would make the 28 Sep negative unreproducible for no gain. Keeping a
# superseded string costs six addresses; deleting it costs the audit trail.
SUPERSEDED = [
    "COVID IS A HOAX IS THE KILLER",
    "Esse quam niger es, sic dixit caccobus ollae",
    ("Section Neither slavery nor involuntary servitude except as a punishment "
     "for crime whereof the party shall have been duly convicted shall exist "
     "within the United States or any place subject to their jurisdiction"),
    ("in which they were received The payee needs proof that at the time of each "
     "transaction the majority of nodes agreed it was the first received"),
    ("common solution is to introdue cent ral au thority or mint that "
     "checks every transac tion for double spen ding. After"),
    "thority", "or mint that", "transac", "tion", "for double spen",
]

def bip39_words():
    for d in (os.path.dirname(os.path.abspath(__file__)),
              os.path.expanduser("~/Downloads/Brainwallet/files(6)")):
        p = os.path.join(d, "bip39_en.txt")
        if os.path.exists(p):
            return [w.strip() for w in open(p) if w.strip()]
    raise SystemExit("bip39_en.txt not found")

MASTER_SHA256 = "d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782"

def png_bytes():
    """The master only. A copy with any other sha256 (re-encoded, overlaid) is refused, never hashed."""
    for p in (os.path.expanduser("~/Downloads/Brainwallet/files(6)/imges/0.2-btc-puzzle.png"),
              os.path.join(os.path.dirname(os.path.abspath(__file__)), "0.2-btc-puzzle.png")):
        if os.path.exists(p):
            raw = open(p, "rb").read()
            if hashlib.sha256(raw).hexdigest() != MASTER_SHA256:
                raise SystemExit("%s is not the master (sha256 %s): refused" % (p, hashlib.sha256(raw).hexdigest()))
            return p, raw
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
    add("micro-text",       MICRO_FRAGS + ([MICROTEXT, MICROTEXT_ALT] if F["whole_text"] else []))
    add("whitepaper true",  [WP_TRUE])
    add("dates",            DATES)
    add("latin mottos",     LATIN_MOTTOS)
    add("census misc",      CENSUS_MISC)
    # [ADDED 2026-11-02] See the constants for what each group is and why it exists.
    add("indeterminate",    INDETERMINATE)
    add("superseded",       SUPERSEDED)
    add("target address",   [TARGET_ADDR])
    add("bip39 words",      bip39_words(), use_variants=F["bip39_casing"])

    # §2.12: "pairwise concatenations of 33 salient phrases under three joiners"
    # §2.12 says 33 salient phrases. The natural list from the surviving sources
    # was 34, and is 39 after the 2 Nov corrections (DATES +4 ellipsis forms,
    # LATIN_MOTTOS +1 scroll). An earlier version of this script sliced it to [:33],
    # which enforced the reported figure and then let it be read back as agreement --
    # the count was an artefact of the slice, not a measurement. The slice is gone and
    # the natural count is printed, so the discrepancy stays visible: it points either
    # at which phrases the original excluded or at a different counting convention.
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

    # --selftest-plant is the POSITIVE CONTROL for the shape arm of the log-reading rule.
    # The rule's detection has two arms: a wording arm (hit|hits|commit=|phrase:) and a
    # shape arm (hex64 | hex40 | WIF | xprv/xpub). The wording arm has a control -- the
    # three planted solver self-tests. The shape arm had NONE: measured 2026-11-09, no log
    # in either tree contained a single hex64, WIF or extended key, so three of its five
    # alternatives had never fired on anything and could not be shown to fire at all.
    # This mode manufactures the artifact deliberately: it replaces the target with the
    # planted string's OWN hash160, so the hit branch below runs for real and emits a real
    # commit=<sha256> line -- the first hex64 ever written to a log in this project.
    # It is a sha256 commitment to the literal string named here and discloses nothing
    # about the puzzle. It must be captured to a *.log path, which both repositories
    # ignore; never to .txt, .out or .md, none of which are ignored.
    PLANT = "blm-corpus-planted-selftest"

    # --run derives the MAXIMAL reading: the union of all 64, so the negative
    # covers the whole space of readings rather than one choice among them.
    F = MAXIMAL if mode == "--run" else DEFAULTS
    groups, png = build(F)
    if mode == "--selftest-plant":
        groups = {"planted-selftest": {PLANT}}
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
    if mode == "--selftest-plant":
        print("  key list NOT written: --selftest-plant must not touch brain_image_keys.txt,"
              "\n  which is tracked and pinned by blob sha in pre_push_allow.txt.")
    else:
        with open(out, "w") as f:
            for s in sorted(seen): f.write(s.replace("\n", "\\n") + "\n")
        print(f"  key list written: {out}")

    if mode == "--count-only":
        print("\n  --count-only: no derivation performed.")
        sys.exit(0)

    # EC backend. coincurve is not installed here, and installing a package to run a
    # verification is the wrong direction: verify_hit.py already carries this project's
    # INDEPENDENT pure-Python secp256k1 -- plain double-and-add, no Jacobian
    # optimisation shared with the solver -- and it self-tests against known-answer
    # vectors including 1*G, 2*G and (N-1)*G + G == infinity. Use that.
    try:
        from coincurve import PrivateKey
        def pubkeys(kd):
            pk = PrivateKey(kd).public_key
            u = pk.format(compressed=False)
            return (pk.format(compressed=True), u, bytes([0x06 | (u[64] & 1)]) + u[1:])
        backend = "coincurve"
    except ImportError:
        import verify_hit as V
        def pubkeys(kd):
            x, y = V._mul(int.from_bytes(kd, "big"))
            xb, yb = x.to_bytes(32, "big"), y.to_bytes(32, "big")
            u = b"\x04" + xb + yb
            return ((b"\x03" if y & 1 else b"\x02") + xb, u,
                    bytes([0x06 | (y & 1)]) + xb + yb)
        backend = "verify_hit (independent pure-Python secp256k1)"

    def h160(b):
        return hashlib.new("ripemd160", hashlib.sha256(b).digest()).digest()

    # Which group each string came from, so a HIT can be reported without quoting it.
    origin = {}
    for gname, acc in groups.items():
        for st in acc: origin.setdefault(st, gname)

    tgt = bytes.fromhex(TARGET_H160)
    if mode == "--selftest-plant":
        tgt = h160(pubkeys(hashlib.sha256(PLANT.encode("utf-8")).digest())[0])
        print("\n  --selftest-plant: target REPLACED by the planted string's own hash160,")
        print(f"  derived from {PLANT!r} by the same two functions the real run uses.")
        print("  The commit= line below is a commitment to THAT string and to nothing else.")
    hits, n, skipped = [], 0, 0
    t0 = __import__("time").time()
    print(f"\n  EC backend: {backend}")
    print(f"  deriving {len(seen):,} strings x 2 hashes x 3 encodings "
          f"= {len(seen)*6:,} addresses expected")
    for i, st in enumerate(sorted(seen), 1):
        d = hashlib.sha256(st.encode("utf-8")).digest()
        for kdi, kd in enumerate((d, hashlib.sha256(d).digest())):
            if not (1 <= int.from_bytes(kd, "big") < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141):
                skipped += 3
                continue
            for pci, pub in enumerate(pubkeys(kd)):
                n += 1
                if h160(pub) == tgt:
                    # HIT RULE. Never print the phrase, the private key or the pubkey.
                    # A sha256 commitment plus the group is enough for the owner to
                    # re-find it offline; nothing here discloses it.
                    hits.append((hashlib.sha256(st.encode("utf-8")).hexdigest(),
                                 origin.get(st, "?"), kdi, pci))
        if i % 2000 == 0:
            el = __import__("time").time() - t0
            print(f"    {i:,}/{len(seen):,} strings  {n:,} addresses  {el:,.0f}s", flush=True)

    el = __import__("time").time() - t0
    expected = len(seen) * 6
    print(f"\n  derived {n:,} addresses in {el:,.1f}s")
    print(f"  expected {expected:,}   skipped (key out of range) {skipped}")

    # ACCEPTANCE AS AN IDENTITY. A brainwallet has no checksum, so every candidate must
    # be derived by construction. Anything below 1.0 means work was silently dropped and
    # the negative is VOID -- a machine fault, not a result.
    if n != expected:
        print(f"  acceptance {n/expected:.6f}  *** NOT 1.0 ***")
        print("  VOID: a brainwallet has no checksum, so acceptance below 1.0 means work")
        print("  was silently DROPPED. This is a MACHINE fault and the negative does not")
        print("  stand. Nothing is recorded.")
        sys.exit(9)
    print(f"  acceptance {n}/{expected} = EXACTLY 1.0")

    if hits:
        print(f"\n  *** {len(hits)} HIT ***")
        print("  HIT RULE: the phrase is NOT printed. Each line is a sha256 commitment")
        print("  to the matching string, which the owner can re-find offline.")
        for c, g, kdi, pci in hits:
            print("    commit=%s  group=%s  kd=%s  enc=%s"
                  % (c, g, ("sha256", "double-sha256")[kdi],
                     ("compressed", "uncompressed", "hybrid")[pci]))
        print("  Move the funds first. Then verify on the affine binary and on an")
        print("  independent BIP32 implementation before anything else.")
    else:
        print("  NO MATCH")

    if mode == "--selftest-plant":
        ok = len(hits) == 1
        print(f"\n  SELFTEST-PLANT {'PASS' if ok else 'FAIL'}: "
              f"expected exactly 1 hit, got {len(hits)}")
        print("  A FAIL here means the hit branch is unreachable and every 'NO MATCH' this")
        print("  script has ever printed is uncontrolled.")
        sys.exit(0 if ok else 1)
    sys.exit(0 if not hits else 3)
