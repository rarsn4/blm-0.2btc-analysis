#!/usr/bin/env python3
"""Generate solver2 configs from the position table. Usage: python3 mkconf.py"""
POOL=("accuse agree axis deal debate fire first food future gun hand life major "
      "maximum minimum mobile need news order paper payment phone power predict "
      "price proof punch receive security space stock there trade twin weapon "
      "welcome world").split()
BASE={1:"subject",2:"camera",3:"tower",4:"mask",5:"police",7:"liberty",9:"eye",
      10:"black",11:"pyramid",12:"vote",13:"moon",16:"rifle",17:"gold",19:"glove",
      20:"apple|second"}
TARGET="1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

def emit(fn,words,full=(),note=""):
    L=[f"# {note}",f"WORDS {words}",f"TARGET {TARGET}"]
    space=1
    for i in range(1,words+1):
        if i in full:      v="@FULL"; space*=2048
        elif i in BASE:
            v=BASE[i]
            if '|' in v: space*=len(v.split('|'))
        else:              v="@POOL"; space*=len(POOL)
        L.append(f"SLOT {i:<2} {v}")
    for i in range(0,len(POOL),13):
        L.append("POOL "+" ".join(POOL[i:i+13]))
    open(fn,'w').write("\n".join(L)+"\n")
    der=space>>(words//3)
    return space,der

import sys
R=125_000
def t(d):
    s=d/R
    return "instant" if s<1 else (f"{s:.0f} s" if s<90 else (f"{s/60:.1f} min" if s<5400 else f"{s/3600:.1f} h"))

jobs=[("t15.conf",15,(),"15-word, gaps 6/8/14/15 from pool"),
      ("t21.conf",21,(),"21-word, gaps 6/8/14/15/18/21 from pool + slot20 apple|second"),
      ("t24.conf",24,(),"24-word, 9 gaps from pool — INFEASIBLE, for reference only")]
# leave-one-out on t18: each gap in turn gets the full wordlist
for g in (6,8,14,15,18):
    jobs.append((f"t18_full{g}.conf",18,(g,),f"18-word, slot {g} unconstrained over all 2048"))

print(f"{'config':20s}{'space':>20s}{'derivations':>18s}{'time':>10s}")
for fn,w,full,note in jobs:
    sp,de=emit(fn,w,full,note)
    print(f"  {fn:18s}{sp:>20,}{de:>18,}{t(de):>10s}")
