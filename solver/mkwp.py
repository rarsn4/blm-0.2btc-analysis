#!/usr/bin/env python3
"""Whitepaper hypothesis: the bottom-of-image fragment (end of Section 2, cut
off right after the word 'order') supplies the END of the phrase — positions
21-24, the four gaps position_table.md has no evidence for."""
SEQ="they receive need proof that time major agree first receive".split()
CONTENT=[w for w in SEQ if w not in ("they","that")]
POOL=("accuse agree axis deal debate fire first food future gun hand life major "
      "maximum minimum mobile need news order paper payment phone power predict "
      "price proof punch receive security space stock there trade twin weapon "
      "welcome world").split()
POOL40=sorted(set(POOL+["they","that","time"]))   # 3 words the repo's list missed
BASE={1:"subject",2:"camera",3:"tower",4:"mask",5:"police",7:"liberty",9:"eye",
      10:"black",11:"pyramid",12:"vote",13:"moon",16:"rifle",17:"gold",19:"glove",
      20:"apple|second"}
TARGET="1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"
PATHS=["m/44'/0'/0'/0/0","m/0'/0/0","m/0/0","m/44'/0'/0'/0/1"]

def emit(fn,words,tail,pool,note):
    L=[f"# {note}","",f"WORDS {words}",f"TARGET {TARGET}"]+[f"PATH {p}" for p in PATHS]
    sp=1
    for i in range(1,words+1):
        if i in tail:      v=tail[i]
        elif i in BASE:    v=BASE[i]
        else:              v="@POOL"
        L.append(f"SLOT {i:<2} {v}")
        if v=="@POOL": sp*=len(pool)
        elif "|" in v:  sp*=len(v.split("|"))
    for i in range(0,len(pool),13): L.append("POOL "+" ".join(pool[i:i+13]))
    open(fn,"w").write("\n".join(L)+"\n")
    return sp, sp>>(words//3)

alt10="|".join(sorted(set(SEQ)))
alt8="|".join(sorted(set(CONTENT)))
jobs=[
 ("wp_fixed.conf",24,{21:"major",22:"agree",23:"first",24:"receive"},POOL,
  "21-24 = last four sentence words IN ORDER"),
 ("wp_fixed2.conf",24,{21:"time",22:"major",23:"agree",24:"first"},POOL,
  "21-24 = shifted one earlier in the sentence"),
 ("wp_pool10.conf",24,{i:alt10 for i in (21,22,23,24)},POOL,
  "21-24 each free over the 10 sentence words"),
 ("wp_pool8.conf",24,{i:alt8 for i in (21,22,23,24)},POOL,
  "21-24 each free over the 8 content words"),
 ("t18_pool40.conf",18,{},POOL40,
  "t18 with they/that/time added to the gap pool (3 words the repo missed)"),
 ("t21_pool40.conf",21,{},POOL40,
  "t21 with the 40-word pool"),
]
R=1_800_000
print(f"{'config':18s}{'space':>20s}{'derivations':>16s}{'time':>9s}")
for fn,w,tail,pool,note in jobs:
    sp,de=emit(fn,w,tail,pool,note)
    t=de/R
    print(f"  {fn:16s}{sp:>20,}{de:>16,}{(f'{t:.0f}s' if t<600 else f'{t/60:.0f}min'):>9}")
