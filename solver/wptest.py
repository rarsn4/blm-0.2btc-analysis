#!/usr/bin/env python3
"""Test the 'key is in the whitepaper, by order' theory exhaustively.

  pip install mnemonic bip_utils
  sudo apt install poppler-utils          # for pdftotext
  wget https://bitcoin.org/bitcoin.pdf
  pdftotext -layout bitcoin.pdf bitcoin.txt
  python3 wptest.py bitcoin.txt

Tests, all against 4 derivation paths:
  1. every sliding window of 12/15/18/21/24 BIP39 words in document order
  2. same, deduplicated (first occurrence only)
  3. same, restricted to each numbered section
  4. word-position readings of the image dates (525, 1103, 52520, 11032020)
  5. image candidate words ordered by first appearance in the whitepaper
"""
import sys, re, hashlib, itertools
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1

TARGET="ccbd031e54cde2a3189fd59bc49f731367a1779e"
PATHS=["m/44'/0'/0'/0/0","m/0'/0/0","m/0/0","m/44'/0'/0'/0/1"]
PASS=["","ONLY REAL BITCOIN","only real bitcoin","REAL","real"]
wl=Mnemonic("english").wordlist; S=set(wl); IDX={w:i for i,w in enumerate(wl)}

def ck(ws):
    n=len(ws)
    if n not in (12,15,18,21,24): return False
    b=0
    for w in ws: b=(b<<11)|IDX[w]
    cb=n//3; eb=n*4//3
    return (b&((1<<cb)-1))==(hashlib.sha256((b>>cb).to_bytes(eb,'big')).digest()[0]>>(8-cb))

def check(ws):
    for pw in PASS:
        seed=Bip39SeedGenerator(" ".join(ws)).Generate(pw)
        for p in PATHS:
            n=Bip32Slip10Secp256k1.FromSeedAndPath(seed,p)
            pub=n.PublicKey().RawCompressed().ToBytes()
            if hashlib.new("ripemd160",hashlib.sha256(pub).digest()).hexdigest()==TARGET:
                return (pw,p)
    return None

def sweep(src,label):
    t=v=0; hits=[]
    for L in (12,15,18,21,24):
        for i in range(0,len(src)-L+1):
            w=src[i:i+L]; t+=1
            if ck(w):
                v+=1
                r=check(w)
                if r: hits.append((label,L,i,r," ".join(w)))
    print(f"  {label:34s} windows={t:>6,}  valid={v:>5,}  hits={len(hits)}")
    for h in hits: print("   *** HIT ***",h)
    return hits

txt=open(sys.argv[1]).read().lower()
toks=re.findall(r"[a-z]+",txt)
seq=[w for w in toks if w in S]
print(f"document: {len(toks):,} tokens, {len(seq):,} BIP39 words, "
      f"{len(set(seq)):,} unique\n")

allhits=[]
allhits+=sweep(seq,"1. in document order")
allhits+=sweep(list(dict.fromkeys(seq)),"2. deduped, first occurrence")

# 3. per section
secs=re.split(r"\n\s*(\d{1,2})\.\s+[A-Z]",open(sys.argv[1]).read())
for k in range(1,len(secs),2):
    s=[w for w in re.findall(r"[a-z]+",secs[k+1].lower()) if w in S]
    if len(s)>=12: allhits+=sweep(s,f"3. section {secs[k]} only")

# 4. date-as-word-position
print("\n  4. image dates as word positions into the BIP39 sequence:")
for pos in (525,1103,52520,11032020,5,11,2,20):
    for L in (12,24):
        if pos+L<=len(seq):
            w=seq[pos:pos+L]
            if ck(w):
                r=check(w)
                print(f"     pos {pos} len {L}: checksum VALID  {'*** HIT ***' if r else 'no match'}")
                if r: allhits.append(("date-pos",L,pos,r," ".join(w)))

# 5. image candidates ordered by first whitepaper appearance
cand=("moon tower food this subject real black world face time proof only future "
      "order find power trust need first system agree major each chain work value "
      "coin public key sign network attack past change fee input output payment").split()
cand=[c for c in cand if c in S]
order=[]
for w in seq:
    if w in cand and w not in order: order.append(w)
print(f"\n  5. image candidates present in whitepaper, by first appearance ({len(order)}):")
print("     "+" ".join(order))
if len(order)>=12: allhits+=sweep(order,"5. candidates by 1st appearance")

print("\n"+("*** SOLVED ***" if allhits else "no match in any ordering"))
for h in allhits: print(h)
