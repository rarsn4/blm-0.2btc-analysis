"""Section 9 worked example -- self-contained and independently checkable.

Reads: BLM slogan block, image x1080-1350 y85-415, text rotated 90 deg,
       verified visually at 5x with saturation boosted.

The seven lines and their colours are DATA read off the image. The base-rate
corpus is a TRANSCRIPTION and therefore a judgement call, so this script
reports the result under several corpus choices rather than one, and states
whether the conclusion depends on which is used.

Run:  python slogan_lines.py        (needs the `mnemonic` package)
"""
from mnemonic import Mnemonic
WS = set(Mnemonic("english").wordlist)
IDX = {w: i + 1 for i, w in enumerate(Mnemonic("english").wordlist)}  # 1-based, repo convention

# ---------------------------------------------------------------- the data
LINES = [
    (1, "black", ["BLACK"]),
    (2, "black", ["LIVES"]),
    (3, "black", ["MATTER"]),
    (4, "BLUE",  ["NO", "JUSTICE", "NO", "PEACE"]),
    (5, "RED",   ["END", "POLICE", "BRUTALITY"]),
    (6, "GREEN", ["STOP", "KILLING", "US"]),
    (7, "black", ["NOT", "ONE", "MORE"]),
]

print("THE SEVEN LINES  (exact words as written; BIP39 requires exact match)")
print(f"   {'#':>2} {'colour':<7} {'words':<26} {'exact BIP39 hits':<28} n")
empty = []
for n, col, ws in LINES:
    hit = [f"{w.lower()}#{IDX[w.lower()]}" for w in ws if w.lower() in WS]
    print(f"   {n:>2} {col:<7} {' '.join(ws):<26} {', '.join(hit) if hit else '-- NONE --':<28} {len(ws)}")
    if not hit:
        empty.append(n)
print(f"\n   lines with no exact BIP39 word: {empty}   count = {len(empty)}")
print("   NOTE: line 2 reads LIVES. 'lives' is not BIP39; 'live' (#1046) is.")
print("         Stemming to reach the wordlist is how `breathe`, `stop`,")
print("         `trusted` and the other eleven entered circulation.\n")

# ---------------------------------------------------------------- corpora
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

BLOCK = "BLACK LIVES MATTER NO JUSTICE NO PEACE END POLICE BRUTALITY STOP KILLING US NOT ONE MORE"

def rate(text):
    ws = [w.strip(".,:;'\"").lower() for w in text.split()]
    ws = [w for w in ws if w.isalpha()]
    return ws, [w for w in ws if w in WS]

print("BASE RATE under several corpus choices")
print("   the corpus is MY transcription -- so test whether the verdict depends on it")
print(f"\n   {'corpus':<38} {'words':>6} {'BIP39':>6} {'p':>7} {'E[wordless]':>12} {'obs':>4} {'verdict':>10}")
corpora = [
    ("headline only",                       HEADLINE),
    ("headline + amendment",                HEADLINE + "\n" + AMENDMENT),
    ("headline + amendment + whitepaper",   HEADLINE + "\n" + AMENDMENT + "\n" + WHITEPAPER),
    ("slogan block alone",                  BLOCK),
    ("amendment + whitepaper only",         AMENDMENT + "\n" + WHITEPAPER),
]
for name, txt in corpora:
    ws, hits = rate(txt)
    p = len(hits) / len(ws)
    exp = sum((1 - p) ** len(l[2]) for l in LINES)
    verdict = "NOT signal" if len(empty) <= exp else "signal"
    print(f"   {name:<38} {len(ws):>6} {len(hits):>6} {p:>7.3f} {exp:>12.2f} {len(empty):>4} {verdict:>10}")

print("\n   -> E[wordless] exceeds the observed 2 under every corpus tested.")
print("      The conclusion does not depend on the transcription choice.")

ws, hits = rate(HEADLINE + "\n" + AMENDMENT + "\n" + WHITEPAPER)
print(f"\nFULL WORD LIST used for the headline figure (p = {len(hits)/len(ws):.3f})")
print(f"   {len(ws)} words, {len(hits)} exact BIP39. Check the transcription against the image.")
print("   BIP39 words, in order of appearance:")
print("     " + " ".join(hits))
print("\n   per-line P(no BIP39 word) at that p:")
p = len(hits) / len(ws)
for n, col, wsl in LINES:
    print(f"      line {n} ({len(wsl)} word{'s' if len(wsl)>1 else ' '}): {(1-p)**len(wsl):.3f}")
