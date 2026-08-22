#!/usr/bin/env python3
"""Every fixed slot gets a small choice set, so ONE run covers 0..13 wrong
words simultaneously — instead of tiering by how many are wrong."""
POOL=("accuse agree axis deal debate fire first food future gun hand life major "
      "maximum minimum mobile need news order paper payment phone power predict "
      "price proof punch receive security space stock there trade twin weapon "
      "welcome world").split()
TARGET="1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"
PATHS=["m/44'/0'/0'/0/0","m/0'/0/0","m/0/0","m/44'/0'/0'/0/1"]
GAPS=[6,8,14,15,18]

# (table word, alternative, third) — third used only in the "wide" config
ALT={ 1:("subject","section","proof"),
      2:("camera","twin","security"),
      3:("tower","clock","hand"),
      4:("mask","face","phone"),
      5:("police","order","power"),
      7:("liberty","torch","light"),
      9:("eye","pyramid","seven"),
     10:("black","night","fire"),
     11:("pyramid","space","axis"),
     12:("vote","debate","agree"),
     13:("moon","month","first"),
     16:("rifle","gun","weapon"),
     17:("gold","price","stock") }
WEAK=[2,11,5]   # the three the table itself rates lowest / flags as conflicted

def emit(fn,nchoice,note,wide=()):
    L=[f"# {note}","","WORDS 18",f"TARGET {TARGET}"]+[f"PATH {p}" for p in PATHS]
    space=1
    for i in range(1,19):
        if i in GAPS:
            v="@POOL"; space*=len(POOL)
        else:
            n = 3 if i in wide else nchoice
            ws=ALT[i][:n]
            v="|".join(ws); space*=len(ws)
        L.append(f"SLOT {i:<2} {v}")
    for i in range(0,len(POOL),13): L.append("POOL "+" ".join(POOL[i:i+13]))
    open(fn,"w").write("\n".join(L)+"\n")
    return space, space//64

R=1_800_000
jobs=[("alt2.conf",2,(),"all 13 fixed slots: table word OR one alternative"),
      ("alt2w.conf",2,WEAK,"as alt2, but slots 2/5/11 get a third option"),
      ("alt3.conf",3,(),"all 13 fixed slots: three options each")]
print(f"{'config':14s}{'space':>20s}{'derivations':>18s}{'time':>10s}")
for fn,n,w,note in jobs:
    sp,de=emit(fn,n,note,w)
    h=de/R/3600
    print(f"  {fn:12s}{sp:>20,}{de:>18,}{h:>9.1f}h")
