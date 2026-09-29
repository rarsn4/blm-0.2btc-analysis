"""Even-slot rule hunt: apply each candidate numbering rule to the WHOLE picture.

For every rule this script reports:
  1. every slot the rule produces, with the element that produced it
  2. collisions: two elements on one slot, or a slot the clock owns
  3. calibration: how many of camera 2, mask 4, rifle 16, subject 1 it
     reproduces independently

A rule counts only if it fills each slot at most once AND reproduces at least
two calibration words. Scoring is mechanical; the only inputs are the
inventories below, each with its provenance.
"""
import numpy as np

from imgio import load_gray

CLOCK = {3: "tower", 9: "eye", 11: "pyramid", 13: "moon", 21: "(hand, no word)"}   # confirmed clock sums
# Non-clock template slots: reported as overlaps for information only. They are
# not collisions, because the template is the thing under test.
TEMPLATE = {1: "subject", 2: "camera", 4: "mask", 5: "police", 7: "liberty", 10: "black", 12: "vote",
            16: "rifle", 17: "gold", 19: "glove"}
CALIB = {"camera": 2, "mask": 4, "rifle": 16, "subject": 1}

# Pre-registered depicted-object counts (enumeration_result.py, rule committed
# before scanning). None = indeterminate. torch and pole are removed: both were
# disproven by crop. Object names are all BIP39 words.
DEPICTED = {
    'arm': None, 'book': None, 'box': None, 'brick': None, 'camera': 2, 'clock': 1, 'cloth': 1,
    'coin': 1, 'course': 12, 'eye': None, 'face': None, 'finger': 5, 'flag': 1, 'glove': 1,
    'gun': 1, 'hand': None, 'head': None, 'lens': 2, 'liberty': 1, 'man': None, 'mask': 4,
    'neck': None, 'people': None, 'pyramid': 1, 'rifle': 1, 'shadow': None, 'shoulder': None,
    'space': 1, 'spike': None, 'suit': 2, 'tower': 1, 'uniform': 1, 'weapon': 1, 'wire': None,
    'woman': 1,
}
# Sub-part counts measured in earlier passes (element -> (word, count, note)).
SUBPARTS = [
    ("Liberty's crown spikes", "liberty", 7, "5 measured, 7 inferred"),
    ("fingers of a hand", "hand", 5, "enumeration: finger 5"),
    ("brick courses of the pyramid", "pyramid", 12, "enumeration: course 12"),
    ("numerals of the clock dial", "clock", 12, "12-hour dial"),
    ("lenses per CCTV camera", "camera", 1, "one lens each"),
    ("buttons on the bust's coat", "(coat: not BIP39)", 8, "8 measured"),
]
# Numbers written in ink (letter/number census, chronology.py). No legible number
# is written on the rifle: see section 0 below.
WRITTEN = [
    ("hoodie date 05.25.20", [5, 25, 20]),
    ("date under .VS. 11.03.20", [11, 3, 20]),
    ("'1865' beside Liberty", [1865]),
    ("'202...?' beside Liberty", [202]),
    ("vial label CVD19", [19]),
    ("amendment heading 'Section 1.'", [1]),
    ("address digits 1KfZ...EV75...", [1, 7, 5]),
    ("gold-chart axis labels (1)200-(1)800", [1200, 1400, 1600, 1800]),
    ("clock dial numerals", list(range(1, 13))),
]
# Multi-line texts: (text, [lines], where each line maps to the in-template word it holds, if any)
LINES = {
    "slogans": ["BLACK", "LIVES", "MATTER", "NO JUSTICE NO PEACE", "END POLICE BRUTALITY",
                "STOP KILLING US", "NOT ONE MORE"],
    "amendment": ["Section 1.", "Neither slavery nor", "involuntary servitude,", "except as a punishment",
                  "for crime whereof the", "party shall have been", "duly convicted, shall exist",
                  "within the United States,", "or any place subject to", "their jurisdiction."],
    "title": ["WELCOME TO THE", "BRAVE", "NEW WORLD"],
    "watermark": ["FIND", "THE", "SEED", "PHRASE", "IN THE THIS PICTURE"],
    "graffiti": ["FUCK", "THIS", "SHIT"],
    "top-left runes": ["line 1", "line 2", "line 3"],
    "ghost text": ["PAY FOR THE FUTURE.", "THIS IS THE FIRST PREDICTION."],
}


def score(name, produced, calib_hits, note=""):
    """produced: {slot: [element, ...]}"""
    produced = {s: v for s, v in produced.items() if 1 <= s <= 24}
    coll = []
    for s, els in sorted(produced.items()):
        if len(els) > 1:
            coll.append("slot %d x%d (%s)" % (s, len(els), "; ".join(els)))
        if s in CLOCK:
            coll.append("slot %d is clock-owned (%s)" % (s, CLOCK[s]))
    ok = not coll and len(calib_hits) >= 2
    print("\n== %s" % name)
    for s, els in sorted(produced.items()):
        print("   slot %2d <- %s" % (s, "; ".join(els)))
    print("   collisions: %s" % ("none" if not coll else " | ".join(coll)))
    ov = ["slot %d (%s)" % (s, TEMPLATE[s]) for s in sorted(produced) if s in TEMPLATE]
    print("   overlaps with non-clock template slots (information only): %s" % (", ".join(ov) or "none"))
    print("   calibration: %d of 4 %s" % (len(calib_hits), sorted(calib_hits)))
    if note:
        print("   note: %s" % note)
    print("   VERDICT: %s" % ("PASSES" if ok else "FAILS"))
    return ok


G = load_gray()
rm = G[690:708, 808:834]
print("0. RIFLE: the only mark on the receiver, x816-825 y695-702: darkest %.0f on background %.0f "
      "(%.0f levels) -> no legible number; 'rifle 16' rests on identifying the model by shape"
      % (rm.min(), np.percentile(rm, 90), np.percentile(rm, 90) - rm.min()))
cx, cy = 470, 937
for el, (x, y) in (("cameras", (1300, 240)), ("masked faces", (470, 330)), ("subject", (1402, 900)), ("rifle", (600, 740))):
    print("   nearest point of %-12s to the clock centre: %4.0f px (dial numerals sit at ~180 px)" % (el, np.hypot(x - cx, y - cy)))

results = {}

# R1: count of a depicted object = slot
p = {}
for w, c in DEPICTED.items():
    if c:
        p.setdefault(c, []).append("%s x%d" % (w, c))
hits = [w for w, s in CALIB.items() if DEPICTED.get(w) == s]
results["R1"] = score("R1  count of a depicted object = slot (all counts)", p, hits)

# R1b: counts >= 2 only (repeated objects)
p2 = {s: v for s, v in p.items() if s >= 2}
results["R1b"] = score("R1b count of a REPEATED object (count >= 2) = slot", p2, hits,
                       "slot 2 keeps camera, lens and suit; restricting to whole objects (dropping lens) still leaves camera and suit")

# R2: any number written in ink = slot
p = {}
for el, nums in WRITTEN:
    for n in nums:
        p.setdefault(n, []).append(el)
hits = ["subject"]           # Section 1 labels the text that contains 'subject'
results["R2"] = score("R2  a number written in ink = slot of that element", p, hits,
                      "camera, mask carry no number; rifle has no legible number")

# R2b: labels on objects only (dates, dial, address and axis excluded)
p = {1: ["amendment heading 'Section 1.'"], 19: ["vial label CVD19"]}
results["R2b"] = score("R2b a number labelling an object (dates, dial, address, axis excluded)", p, ["subject"],
                       "reproduces glove 19 too, which is outside the calibration set")

# R3: dates
p = {}
for el, nums in WRITTEN[:2]:
    for n in nums:
        p.setdefault(n, []).append(el)
results["R3"] = score("R3  the parts of a written date = slots", p, [])

# R4: line number within a multi-line text = slot
p = {}
for t, ls in LINES.items():
    for i, l in enumerate(ls, 1):
        p.setdefault(i, []).append("%s line %d" % (t, i))
results["R4"] = score("R4  line number within any multi-line text = slot", p, [],
                      "'subject' is on amendment line 9, so this rule puts it at 9, not 1; police 5 is outside the calibration set")

# R4b: slogans only
p = {i: ["slogan line %d: %s" % (i, l)] for i, l in enumerate(LINES["slogans"], 1)}
p[5] = ["slogan line 5 word END", "slogan line 5 word POLICE"]      # two BIP39 words on one line
p[7] = ["slogan line 7 word ONE", "slogan line 7 word MORE"]
results["R4b"] = score("R4b line number within the slogan block only", p, [],
                       "lines 2 and 6 hold no BIP39 word; lines 5 and 7 hold two each")

# R5: mirror / reversal yields a numeral
results["R5"] = score("R5  a transformation (vertical flip) turns lettering into a numeral", {12: [".VS. flipped vertically reads 12"]}, [],
                      "the other mirror-written texts (seal ring, pyramid base, TOWER/MOON) contain no numerals")

# R6: sub-part count
p = {}
for el, w, c, note in SUBPARTS:
    p.setdefault(c, []).append("%s -> %s (%s)" % (el, w, note))
results["R6"] = score("R6  count of an object's sub-parts = slot", p, [],
                      "pyramid would hold slot 12 here and slot 11 by the clock: one word, two slots")

# R7: the single dial numeral nearest the element
results["R7"] = score("R7  the single clock numeral nearest an element (not a sum)", {}, [],
                      "reaches only slots 1-12 and only elements near the dial; every calibration element is 236-1084 px from the centre")

# R9: number words inside the decoded rune plaintexts
results["R9"] = score("R9  a number word in the rune plaintexts = slot",
                      {2: ["clock caption 'сумма ДВУХ чисел' (two)"]}, [],
                      "'номер X' gives no number (X is a hapax with no numeral reading); 'много' (many) is not a number; "
                      "the caption's 'two' describes the clock's own sums")

# R8: the disjunction R1b OR R2b
p = {s: list(v) for s, v in p2.items()}
p.setdefault(1, []).append("amendment heading 'Section 1.'")
p.setdefault(19, []).append("vial label CVD19")
results["R8"] = score("R8  R1b OR R2b (count if repeated, else a labelling number)", p, ["camera", "mask", "subject"],
                      "two rules joined after seeing the template; inherits R1b's slot-2 collision")

print("\nSUMMARY: %d of %d rules pass" % (sum(results.values()), len(results)))
