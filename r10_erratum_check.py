"""R10 erratum, POST HOC: re-score with the corrected E24 (Leopold II bust) boxes.

r10_elements.json is left exactly as pre-registered (its sha256 is checked).
The corrected boxes are substituted in memory only. The pipeline is identical
to r10_layout.py: same seed, same draw order, sets scored in the same A-D
order. The result is NOT used for the decision.
"""
import hashlib
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(HERE, "r10_elements.json"), "rb").read()
assert hashlib.sha256(raw).hexdigest() == "3634036d4e0d785b2f2efbe5cb34c6a2ca69528f73a316c16c9d31c0e2b49b88"
cfg = json.loads(raw)
HX, HY = cfg["hub"]
T12 = cfg["theta12_deg"]
FX0, FY0, FX1, FY1 = cfg["frame"]
TOLS, DRAWS = (0.5, 1.0), 10000

CORRECTIONS = {
    "review session's boxes": {"bust": [1305, 420, 1475, 660], "head": [1353, 425, 1430, 525]},
    "Windows re-measurement": {"bust": [1303, 426, 1475, 652], "head": [1353, 426, 1432, 515]},
}


def centre(b):
    return ((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0)


def run(bust, head):
    rng = np.random.default_rng(20260929)
    E = {k: dict(v) for k, v in cfg["elements"].items()}
    E["E24"]["box"] = bust
    face = dict(cfg["face_level_substitutions"])
    face["E24"] = head
    seal = set(cfg["seal_group"])
    sets = [
        ("A", {k: v["box"] for k, v in E.items()}),
        ("B", {k: v["box"] for k, v in E.items() if k not in seal}),
        ("C", {k: face.get(k, v["box"]) for k, v in E.items()}),
        ("D", {k: face.get(k, v["box"]) for k, v in E.items() if k not in seal}),
    ]
    out = []
    for name, boxes in sets:
        C = np.array([centre(b) for b in boxes.values()])
        th = np.degrees(np.arctan2(-(C[:, 1] - HY), C[:, 0] - HX))
        r = (th - T12) % 15.0
        d = np.minimum(r, 15.0 - r)
        obs = [int((d <= t).sum()) for t in TOLS]
        us = rng.uniform(0, 15, DRAWS)
        hxs = rng.uniform(FX0, FX1, DRAWS)
        hys = rng.uniform(FY0, FY1, DRAWS)
        rot = np.zeros((DRAWS, 2), int)
        hub = np.zeros((DRAWS, 2), int)
        for i in range(DRAWS):
            rr = (th - (T12 + us[i])) % 15.0
            dd = np.minimum(rr, 15.0 - rr)
            rot[i] = [(dd <= t).sum() for t in TOLS]
            t2 = np.degrees(np.arctan2(-(C[:, 1] - hys[i]), C[:, 0] - hxs[i]))
            rr = (t2 - T12) % 15.0
            dd = np.minimum(rr, 15.0 - rr)
            hub[i] = [(dd <= t).sum() for t in TOLS]
        cells = []
        for i, t in enumerate(TOLS):
            pr = (1 + (rot[:, i] >= obs[i]).sum()) / (1 + DRAWS)
            ph = (1 + (hub[:, i] >= obs[i]).sum()) / (1 + DRAWS)
            cells.append("%d/%d @%.1f: p %.3f / %.3f" % (obs[i], len(C), t, pr, ph))
        out.append("   %s  %s   %s" % (name, cells[0], cells[1]))
    return out


print("r10_elements.json unchanged (sha256 3634036d...); E24 substituted in memory only")
for label, c in CORRECTIONS.items():
    cx, cy = centre(c["head"])
    th = math.degrees(math.atan2(-(cy - HY), cx - HX))
    r = (th - T12) % 15.0
    print("\n%s: bust %s, head %s (head offset %.2f deg)" % (label, c["bust"], c["head"], min(r, 15 - r)))
    for line in run(c["bust"], c["head"]):
        print(line)
print("\nBonferroni over 8 comparisons (4 sets x 2 tolerances): p < %.4f needed" % (0.05 / 8))
