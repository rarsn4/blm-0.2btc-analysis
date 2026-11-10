"""LL-1: verify configs/electrum_old_en.txt against the _words TUPLE in
electrum/old_mnemonic.py, by TEXT PARSING (their code is data; we do not import it).

Checks the brief's figures and the user's warning that a `words = [` regex
silently falls through to a different count.
"""
import hashlib, re, sys

SRC = ["/home/soul/.local/lib/python3.10/site-packages/electrum/old_mnemonic.py",
       "/home/soul/squashfs-root/usr/lib/python3.10/site-packages/electrum/old_mnemonic.py"]
PROJ = "/home/soul/blm-analysis/configs/electrum_old_en.txt"

def parse_tuple(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"^_words\s*=\s*\(", t, re.M)
    if not m:
        return None, "no `_words = (` found"
    # walk to the matching close paren at depth 0
    i = m.end() - 1
    depth = 0
    for j in range(i, len(t)):
        if t[j] == "(":
            depth += 1
        elif t[j] == ")":
            depth -= 1
            if depth == 0:
                body = t[i + 1:j]
                break
    else:
        return None, "unterminated tuple"
    words = re.findall(r'"([^"]*)"', body)
    return words, None

def norm_md5(ws):
    return hashlib.md5("\n".join(ws).encode()).hexdigest()

print("LL-1  OLD-ELECTRUM WORDLIST, VERIFIED INDEPENDENTLY")
print("=" * 70)

ref = None
for p in SRC:
    try:
        ws, err = parse_tuple(p)
    except FileNotFoundError:
        print(f"  ABSENT  {p}")
        continue
    if err:
        print(f"  PARSE FAIL  {p}: {err}")
        continue
    print(f"  {len(ws):5d} words  {len(set(ws)):5d} unique   {p}")
    print(f"        first five: {' '.join(ws[:5])}")
    print(f"        last five : {' '.join(ws[-5:])}")
    print(f"        md5 newline-joined, no trailing NL : {norm_md5(ws)}")
    md5_tr = hashlib.md5(("\n".join(ws) + "\n").encode()).hexdigest()
    print(f"        md5 newline-joined, trailing NL    : {md5_tr}")
    if ref is None:
        ref = ws
    else:
        print(f"        identical to first source: {ws == ref}")

# the user's warning, reproduced
t = open(SRC[0], encoding="utf-8").read()
alt = re.search(r"^words\s*=\s*\[", t, re.M)
print(f"\n  the `words = [` trap: regex matches in source? {bool(alt)}")
loose = re.findall(r'"([^"]*)"', t)
print(f"  a bare quoted-string scan over the WHOLE FILE yields: {len(loose)}"
      f"   <- the 1627 the brief warns about" if len(loose) == 1627
      else f"  a bare quoted-string scan over the WHOLE FILE yields: {len(loose)}")

# project copy
raw = open(PROJ, "rb").read()
proj = raw.decode().split("\n")
trail = proj[-1] == ""
if trail:
    proj = proj[:-1]
print("\n  PROJECT COPY  configs/electrum_old_en.txt")
print(f"        {len(proj)} words  {len(set(proj))} unique   trailing newline: {trail}")
print(f"        md5 of file as stored              : {hashlib.md5(raw).hexdigest()}")
print(f"        md5 newline-joined, no trailing NL : {norm_md5(proj)}")
print(f"        first five: {' '.join(proj[:5])}")
print(f"        last five : {' '.join(proj[-5:])}")
try:
    print(f"        breathe 1-based index: {proj.index('breathe') + 1}")
except ValueError:
    print("        breathe: ABSENT")

print("\n  COMPARISON  source tuple vs project copy")
if ref is None:
    print("        CANNOT COMPARE: source not parsed")
    sys.exit(1)
print(f"        same length        : {len(ref) == len(proj)}  ({len(ref)} vs {len(proj)})")
print(f"        same set           : {set(ref) == set(proj)}")
print(f"        IDENTICAL IN ORDER : {ref == proj}")
if ref != proj:
    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(ref, proj)) if a != b]
    print(f"        first order mismatches ({len(diffs)} total):")
    for i, a, b in diffs[:10]:
        print(f"          idx {i}: source={a!r} project={b!r}")
    only_s = set(ref) - set(proj)
    only_p = set(proj) - set(ref)
    if only_s:
        print(f"        in source only ({len(only_s)}): {sorted(only_s)[:20]}")
    if only_p:
        print(f"        in project only ({len(only_p)}): {sorted(only_p)[:20]}")

print("\n  BRIEF'S FIGURES")
for label, got, want in [
    ("count", len(ref), 1626),
    ("unique", len(set(ref)), 1626),
    ("first five", " ".join(ref[:5]), "like just love know never"),
    ("last five", " ".join(ref[-5:]), "throne total unseen weapon weary"),
    ("breathe 1-based", ref.index("breathe") + 1 if "breathe" in ref else None, 245),
    ("md5 newline-joined", norm_md5(ref), "33f89ca84f7c9b3eeec1bcc253bce673"),
]:
    print(f"        {'MATCH ' if got == want else 'DIFFER'}  {label}: {got}")
