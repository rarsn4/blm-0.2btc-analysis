#!/usr/bin/env python3
"""Generate t18 configs that free ONE fixed word at a time to the 53-word
candidate list. Tests the weakest links in position_table.md directly."""
POOL=("accuse agree axis deal debate fire first food future gun hand life major "
      "maximum minimum mobile need news order paper payment phone power predict "
      "price proof punch receive security space stock there trade twin weapon "
      "welcome world").split()
ALL53=sorted(set(POOL+("apple black camera eye glove gold liberty mask moon "
                       "police pyramid rifle second subject tower vote").split()))
BASE={1:"subject",2:"camera",3:"tower",4:"mask",5:"police",7:"liberty",9:"eye",
      10:"black",11:"pyramid",12:"vote",13:"moon",16:"rifle",17:"gold"}
GAPS=[6,8,14,15,18]
TARGET="1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"
PATHS=["m/44'/0'/0'/0/0","m/0'/0/0","m/0/0","m/44'/0'/0'/0/1"]

def emit(free_slot):
    fn=f"t18_free{free_slot}.conf"
    L=[f"# t18 with slot {free_slot} ({BASE[free_slot]}) freed to all 53 candidates",
       "WORDS 18",f"TARGET {TARGET}"]+[f"PATH {p}" for p in PATHS]
    for i in range(1,19):
        if i==free_slot: v="@ALT"
        elif i in GAPS:  v="@POOL"
        else:            v=BASE[i]
        L.append(f"SLOT {i:<2} {v}")
    # @ALT is expressed as an explicit choice list
    L=[l.replace("@ALT","|".join(ALL53)) for l in L]
    for i in range(0,len(POOL),13):
        L.append("POOL "+" ".join(POOL[i:i+13]))
    open(fn,'w').write("\n".join(L)+"\n")
    return fn

print(f"candidate list: {len(ALL53)} words")
for s in sorted(BASE): print("  ",emit(s))
