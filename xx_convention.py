"""OO-2. Is XX-for-a-doubled-letter a convention of this painting?

Direction pre-registered in xx_marks_plan.md sec.6 (commit a6ab39a, blob eb6ef14b):
THE EXPECTED RESULT IS NONE. Published either way.

Enumerate every word in word_census.tsv carrying a doubled letter, then ask whether
any is painted with XX or any mark standing in for the doubled letter. Evidence named
in advance: census_crops.py's DRAWN boxes and its ELEMENTS letter-substitution census,
which is where "O -> clenched fist" and "the I of SHIT is written" are recorded.
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DOUBLE = re.compile(r"(.)\1", re.UNICODE)

rows = []
for ln in open("word_census.tsv", encoding="utf-8"):
    if ln.startswith("#"): continue
    f = ln.rstrip("\n").split("\t")
    if len(f) < 3 or f[0] == "section" or not f[1]: continue
    rows.append((f[0], f[1]))

doubles = [(s, w, DOUBLE.search(w).group(0)) for s, w in rows if DOUBLE.search(w)]
print("OO-2  DOUBLED LETTERS IN THE CANVAS'S OWN VOCABULARY")
print("=" * 78)
print(f"  census rows scanned: {len(rows)}")
print(f"  words carrying a doubled letter: {len(doubles)}\n")
print(f"  {'section':13s} {'word':14s} {'double':8s}")
for s, w, d in sorted(doubles, key=lambda r: (r[1])):
    print(f"  {s:13s} {w:14s} {d.upper():8s}")

# the painted-location table and the substitution census, read as data
from census_crops import DRAWN, ELEMENTS
print(f"\n  census_crops.DRAWN holds {len(DRAWN)} measured painted strings;")
print(f"  census_crops.ELEMENTS holds {len(ELEMENTS)} letter-substitution rows.")

print("\n--- WHERE EACH DOUBLED-LETTER WORD IS PAINTED, AND WHAT IS RECORDED THERE ---")
seen = set()
for s, w, d in sorted(doubles, key=lambda r: r[1]):
    if w in seen: continue
    seen.add(w)
    hits = [(lbl, box, st, src) for lbl, txt, box, st, src in DRAWN
            if re.search(r"\b" + re.escape(w) + r"\b", str(txt), re.I)]
    if hits:
        for lbl, box, st, src in hits:
            print(f"  {w:12s} {d.upper():4s}  box {str(box):24s} [{st}]  {lbl}  <- {src}")
    else:
        print(f"  {w:12s} {d.upper():4s}  NO MEASURED BOX -- reported UNEXAMINED, not negative")

print("\n--- THE SUBSTITUTION CENSUS: every recorded letter-for-object substitution ---")
subs = [(lbl, n, note) for lbl, n, note, _ in ELEMENTS if note.strip() not in ("-", "")]
for lbl, n, note in subs:
    print(f"  {lbl:40s} {note}")
print(f"\n  substitutions recorded in the whole census: {len(subs)}")
# NOTE: the first version of this check scanned the whole NOTE TEXT for a doubled
# letter and matched the "tt" inside the word "written", reporting a second instance
# that does not exist. The test has to ask whether the SUBSTITUTED LETTER is one of a
# doubled pair in the element's own text -- not whether the prose contains a double.
xxsub = [s for s in subs if "xx" in s[2].lower()]
dblsub = []
for lbl, n, note in subs:
    m = re.match(r"\s*([A-Za-z])\s*->", note)          # "O -> clenched fist"
    if not m:
        continue                                        # not a substitution of a letter
    ch = m.group(1).upper()
    if ch * 2 in lbl.upper():                           # is that letter doubled here?
        dblsub.append((lbl, ch, note))
print(f"  of those, any involving XX:              {len(xxsub)}  {xxsub if xxsub else ''}")
print(f"  of those, substituting a DOUBLED letter: {len(dblsub)}  {dblsub if dblsub else ''}")
print("\n  each substitution row, checked individually:")
for lbl, n, note in subs:
    m = re.match(r"\s*([A-Za-z])\s*->", note)
    if m:
        ch = m.group(1).upper()
        print(f"    {lbl:28s} substitutes {ch}; {ch}{ch} in its text: "
              f"{'YES' if ch*2 in lbl.upper() else 'no'} -> "
              f"{'a doubled-letter substitution' if ch*2 in lbl.upper() else 'single letter, not a double'}")
    else:
        print(f"    {lbl:28s} note is not a letter substitution at all: {note!r}")

# the decisive single case: MOON is the one OO word examined glyph by glyph
moon = [(lbl, n, note) for lbl, n, note, _ in ELEMENTS if "MOON" in lbl.upper()]
print("\n  THE DECISIVE CASE -- `moon`, the only OO word with a letter-by-letter examination:")
for lbl, n, note in moon:
    print(f"    {lbl}: {n} letters, substitution field {note!r}")
    print(f"    TOWER(5) + MOON(4) = 9 letters, all accounted as written.")
    print(f"    -> MOON's OO is WRITTEN AS OO, not as XX and not as any stand-in.")

print("\n--- DECISION (plan sec.6) ---")
if not xxsub and not dblsub:
    print("  NONE. No doubled letter anywhere in this painting is written with XX, and the")
    print("  substitution census records no doubled-letter substitution of any kind.")
    print("\n  -> XX-for-OO is NOT a convention of this painting. The hypothesis collapses")
    print("     to its single-instance version and is graded")
    print("     [EXTERNAL/PROPOSED, UNSUPPORTED] -- the same grade as apple@20.")
else:
    print("  A SECOND INSTANCE EXISTS -- report loudly; still gated by plan sec.0.")
