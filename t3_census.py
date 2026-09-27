"""Task 3: per-word underline census over the hand-copied 13th Amendment
(Leopold pedestal, under the FUCK THIS SHIT graffiti).

Part 1 -- is the line under 'subject' a drawn underline or the soft top edge of
the spray paint below it? Column-mean profiles under 'subject' against words on
the same line that also sit directly above spray.

Part 2 -- census. Word spans were read off ruled nearest-neighbour crops.
Band = rows baseline+1 .. baseline+4 under the word.
OBSCURED if >= 40% of band pixels are spray (<80); a strict variant uses 25%.
MARKED only if the detector finds a run in the band covering >= 50% of the word
AND at least one CLEAN run >= 10 px (spray-adjacent runs alone are
inconclusive). The heading 'Section 1.' is reported separately: its line
fragments cannot be separated from the letter bottoms.
"""
import numpy as np

from t3_lines import G, scan

print("PART 1 -- column-mean value per row (paper ~140, handwriting ~90-125, spray ~55-75)")
spans = [
    ("subject 'su' + I/T gap  x1401-1413", 1401, 1414),
    ("subject 'bject' over T  x1414-1452", 1414, 1453),
    ("I/T gap only (no spray) x1410-1413", 1410, 1414),
    ("CONTROL 'place' over H  x1384-1394", 1384, 1395),
    ("CONTROL 'any'   over S  x1340-1358", 1340, 1359),
    ("CONTROL 'to' no spray   x1455-1466", 1455, 1467),
]
rows = range(896, 909)
print("%-36s" % "" + "".join("%5d" % y for y in rows))
for name, a, b in spans:
    print("%-36s" % name + "".join("%5.0f" % G[y, a:b].mean() for y in rows))

WORDS = [
    ("Section", 1350, 1415, 820), ("1.", 1420, 1436, 820),
    ("Neither", 1318, 1365, 832), ("slavery", 1368, 1412, 832), ("nor", 1420, 1462, 832),
    ("involuntary", 1318, 1395, 842), ("servitude,", 1400, 1475, 842),
    ("except", 1318, 1360, 852), ("as", 1368, 1383, 852), ("a", 1388, 1395, 852), ("punishment", 1400, 1465, 852),
    ("for", 1318, 1334, 862), ("crime", 1338, 1370, 862), ("whereof", 1375, 1432, 862), ("the", 1440, 1465, 862),
    ("party", 1318, 1342, 871), ("shall", 1350, 1378, 871), ("have", 1385, 1415, 871), ("been", 1425, 1462, 871),
    ("duly", 1318, 1342, 881), ("convicted,", 1348, 1395, 881), ("shall", 1400, 1432, 881), ("exist", 1440, 1472, 881),
    ("within", 1318, 1350, 891), ("the", 1355, 1376, 891), ("United", 1382, 1420, 891), ("States,", 1425, 1478, 891),
    ("or", 1318, 1332, 900), ("any", 1338, 1362, 900), ("place", 1368, 1398, 900), ("subject", 1402, 1453, 900), ("to", 1458, 1472, 900),
    ("their", 1318, 1346, 910), ("jurisdiction.", 1350, 1442, 910),
]

runs = scan(1296, 1496, 800, 918, "", quiet=True)
print("\nPART 2 -- census, %d tokens" % len(WORDS))
counts = {"MARKED": 0, "VISIBLE-unmarked": 0, "OBSCURED": 0, "HEADING-indet": 0}
strict = []
print("%-14s %-11s %-6s %-17s %s" % ("word", "x-span", "spray", "status", "detector runs in band"))
for w, x0, x1, bl in WORDS:
    band = G[bl + 1:bl + 5, x0:x1]
    spray = (band < 80).mean()
    cover, hit = 0, ""
    for y, s, e, kind in runs:
        if bl + 1 <= y <= bl + 4:
            ov = max(0, min(e, x1) - max(s, x0) + 1)
            if ov > 0:
                cover += ov
                hit += "y%d x%d-%d %s; " % (y, s, e, kind)
    clean = any(kind == "CLEAN" and bl + 1 <= y <= bl + 4 and min(e, x1) - max(s, x0) >= 9
                for y, s, e, kind in runs)
    if bl == 820:
        st = "HEADING-indet"
    elif spray >= 0.40:
        st = "OBSCURED"
    elif cover / (x1 - x0) >= 0.5 and clean:
        st = "MARKED"
    else:
        st = "VISIBLE-unmarked"
    counts[st] += 1
    if bl != 820 and spray < 0.25:
        strict.append((w, st))
    print("%-14s %4d-%-6d %4.0f%%  %-17s %s" % (w, x0, x1, 100 * spray, st, hit))
print("\nTOTAL %d tokens: " % len(WORDS) + ", ".join("%s %d" % kv for kv in counts.items()))
m = sum(1 for _, st in strict if st == "MARKED")
print("STRICT (band spray < 25%%): %d body words checkable, %d marked" % (len(strict), m))
