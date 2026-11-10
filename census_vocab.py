"""LL-2  The canvas's own vocabulary against both ledgers.

Pre-registered in census_vocab_plan.md, committed aa148de, blob
e962bca2b9583238717e334c41798ec5fb624eb0, BEFORE any membership was computed.
Exclusions, strata, the three nulls and the decision rule are all fixed there.

Membership by exact token, no stemming (the EE-1 defect). The census's own
bip39 column is not trusted; both ledgers are re-read from configs/.
"""
import hashlib, re, sys
from collections import Counter

OLD = "configs/electrum_old_en.txt"
BIP = "configs/bip39_en.txt"
CENSUS = "word_census.tsv"
CTRL = "/home/soul/Downloads/Brainwallet/files(6)/bitcoin.txt"
DICT = "/usr/share/dict/american-english"

LATIN = {"esse","quam","dixit","ollae","rerum","causas","mundus","pereat",
         "caccabus","justitia","cognoscere","niger"}
FRAG  = {"ral","spen","ding","tion","thority","transac","re"}
ACRO  = {"blm","cvd","sic"}
MISSP = {"introdue"}

def load(p):
    return [w.strip() for w in open(p, encoding="utf-8") if w.strip()]

old = load(OLD); bip = load(BIP)
O, B = set(old), set(bip)
print("LL-2  THE CANVAS'S OWN VOCABULARY, BOTH LEDGERS")
print("=" * 74)
print(f"  old Electrum {len(O)} words  md5(file) "
      f"{hashlib.md5(open(OLD,'rb').read()).hexdigest()}")
print(f"  BIP39        {len(B)} words  md5(file) "
      f"{hashlib.md5(open(BIP,'rb').read()).hexdigest()}")
print(f"  base rates: old-only {len(O-B)}/{len(O)} = {100*len(O-B)/len(O):.1f}%   "
      f"bip39-only {len(B-O)}/{len(B)} = {100*len(B-O)/len(B):.1f}%   both {len(O&B)}")

def klass(w):
    i, j = w in O, w in B
    return "BOTH" if i and j else "OLD_ONLY" if i else "BIP39_ONLY" if j else "NEITHER"

# ---------- read the census ----------
rows = []
for ln in open(CENSUS, encoding="utf-8"):
    if ln.startswith("#"): continue
    f = ln.rstrip("\n").split("\t")
    if len(f) < 3 or f[0] == "section" or not f[1]: continue
    rows.append((f[0], f[1], int(f[2]) if f[2].isdigit() else 1))
print(f"\n  census rows: {len(rows)}  "
      f"{dict(Counter(s for s, _, _ in rows))}")

def excl(w):
    if not w.isascii():          return "cyrillic"
    if not w.isalpha():          return "non-alpha"
    if w in LATIN:               return "latin"
    if w in FRAG:                return "fragment"
    if w in ACRO:                return "acronym"
    if w in MISSP:               return "misspelling"
    if len(w) < 3:               return "len<3 (both ledgers start at 3)"
    return None

ex = Counter()
keep = []
for sec, w, c in rows:
    r = excl(w)
    if r: ex[r] += 1
    else: keep.append((sec, w, c))
print("  excluded per the plan:")
for k, v in sorted(ex.items(), key=lambda kv: -kv[1]):
    print(f"        {v:3d}  {k}")
print(f"  eligible English words: {len(keep)}  "
      f"({sum(1 for s,_,_ in keep if s=='A_display')} A_display, "
      f"{sum(1 for s,_,_ in keep if s=='B_microtext')} B_microtext)")
noop = FRAG - {w for _, w, _ in rows}
if noop:
    print(f"  NOTE: the plan named fragment(s) absent from the census, no-op: {sorted(noop)}")

# ---------- THE FOUR COUNTS ----------
def four(sel, label):
    c = Counter(klass(w) for w in sel)
    n = len(sel)
    print(f"\n  {label}   n={n}")
    for k in ("BOTH", "OLD_ONLY", "BIP39_ONLY", "NEITHER"):
        print(f"        {k:11s} {c[k]:4d}   {100*c[k]/n if n else 0:5.1f}%")
    return c

print("\n" + "-" * 74)
print("  THE FOUR COUNTS  (exact token, types not occurrences)")
allw = [w for _, w, _ in rows]
four(allw, "ALL 151 census rows, nothing excluded")
four([w for s, w, _ in rows if s == "A_display"], "A_display, nothing excluded")
four([w for s, w, _ in rows if s == "B_microtext"], "B_microtext, nothing excluded")
elig = [w for _, w, _ in keep]
four(elig, "ELIGIBLE ENGLISH, all lengths")
prim = [w for s, w, _ in keep if s == "A_display" and 3 <= len(w) <= 8]
four(prim, "PRIMARY STRATUM: A_display, English, length 3-8")
long_ = [(s, w) for s, w, _ in keep if len(w) >= 9]
print(f"\n  length 9-12, reported separately per plan sec.3 (BOTH is impossible): "
      f"n={len(long_)}")
for s, w in sorted(long_, key=lambda t: t[1]):
    print(f"        {w:13s} {klass(w):11s} [{s}]")

print("\n  the primary stratum, word by word:")
for w in sorted(prim):
    k = klass(w)
    mark = "  <-- old-Electrum only" if k == "OLD_ONLY" else ""
    print(f"        {w:10s} len {len(w)}  {k:11s}{mark}")

# ---------- NULLS ----------
def pb(ps):
    d = [1.0]
    for p in ps:
        nd = [0.0] * (len(d) + 1)
        for k, v in enumerate(d):
            nd[k] += v * (1 - p); nd[k + 1] += v * p
        d = nd
    return d

def tail(ps, obs):
    d = pb(ps)
    return sum(d[obs:]), sum(k * p for k, p in enumerate(d))

# null 1: frequency-weighted English prose
ctrl_tok = [t.lower() for t in re.findall(r"[A-Za-z]+", open(CTRL, encoding="utf-8", errors="replace").read())]
ctrl_tok = [t for t in ctrl_tok if 3 <= len(t) <= 8 and excl(t) is None]
by_len_ctrl = {}
for L in range(3, 9):
    toks = [t for t in ctrl_tok if len(t) == L]
    by_len_ctrl[L] = (sum(1 for t in toks if klass(t) == "OLD_ONLY") / len(toks)) if toks else 0.0

# null 2: union draw
by_len_uni = {}
for L in range(3, 9):
    u = [w for w in (O | B) if len(w) == L]
    by_len_uni[L] = sum(1 for w in u if w in O and w not in B) / len(u)

# null 3: type dictionary (sensitivity only)
dwords = [w.strip().lower() for w in open(DICT, encoding="utf-8", errors="replace")
          if w.strip() and "'" not in w and w.strip().isascii() and w.strip().isalpha()]
by_len_dict = {}
for L in range(3, 9):
    dl = [w for w in dwords if len(w) == L]
    by_len_dict[L] = (sum(1 for w in dl if w in O and w not in B) / len(dl)) if dl else 0.0

obs = sum(1 for w in prim if klass(w) == "OLD_ONLY")
print("\n" + "-" * 74)
print(f"  EXACT POISSON-BINOMIAL,  observed OLD_ONLY = {obs} of {len(prim)}")
print(f"  control corpus: bitcoin.txt, {len(ctrl_tok)} eligible tokens (frequency-weighted)")
print("\n        len  n_prim | P(old-only) prose   union   dict")
cl = Counter(len(w) for w in prim)
for L in range(3, 9):
    print(f"        {L:3d}  {cl[L]:6d} | {by_len_ctrl[L]:17.4f} {by_len_uni[L]:7.4f} "
          f"{by_len_dict[L]:6.4f}")

print("\n        null                       expected   P(X >= obs)")
res = {}
for name, tbl in (("PRIMARY  prose, freq-wtd", by_len_ctrl),
                  ("SECONDARY  union draw", by_len_uni),
                  ("SENSITIVITY  dictionary", by_len_dict)):
    ps = [tbl[len(w)] for w in prim]
    t, e = tail(ps, obs)
    res[name] = (t, e)
    print(f"        {name:26s} {e:8.2f}   {t:11.4g}")

print("\n" + "-" * 74)
p_prim = res["PRIMARY  prose, freq-wtd"][0]
p_sec = res["SECONDARY  union draw"][0]
e_prim = res["PRIMARY  prose, freq-wtd"][1]
print("  DECISION, by the rule fixed in census_vocab_plan.md sec.6")
print(f"        observed {obs}, expected {e_prim:.2f} under the primary null")
if p_prim > 0.5:
    print(f"        P(X >= {obs}) = {p_prim:.4g} > 0.5  ->  H1 REFUTED")
    print("        The canvas sits at or below what ordinary English prose gives.")
elif p_prim < 0.05 and p_sec < 0.5:
    print(f"        P = {p_prim:.4g} < 0.05 and the union null agrees  ->  H1 SUPPORTED")
    print("        Carries the sec.5 confound: the old list IS a poetry frequency list.")
else:
    print(f"        P(X >= {obs}) = {p_prim:.4g}, union {p_sec:.4g}  ->  NO RESULT")
print("\n  Word consequences, per plan sec.0: NO WORD ENTERS ANY CONFIG FROM THIS,")
print("  under any outcome. LL-5's arithmetic is what governs, not this test.")
