"""R10: is the artwork laid out on the clock dial?

Pre-registered inputs (r10_elements.json, sha256 checked below, fixed before any
angle was computed):
  hub (473.75, 940.0); theta12 = 162.30 deg (image y up); numeral n at theta12 - 30n;
  grid = 24 directions every 15 deg (numerals and midpoints);
  element centre = bounding-box centre.

Pre-stated decision rule, written before running:
  PRIMARY test = set A (28 whole-object elements). "Significant" = p < 0.05
  under BOTH nulls at the same tolerance (0.5 or 1.0 deg). Sets B-D and the
  pilot's five named items are reported but cannot by themselves make it significant.
  Nulls: (1) theta12 + U[0,15); (2) hub uniform inside the drawn frame, theta12 fixed.
  10,000 draws each, seeded; p = (1 + #null >= observed) / (1 + draws).
If significant: score slot = clock sum at each element's direction (at numeral n:
2n; between n and n+1: 2n+1) for elements within 1 deg, with collisions.
If not: the clock governs the hands and the seal only; stop.
"""
import hashlib
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "r10_elements.json")
PREREG_SHA256 = "3634036d4e0d785b2f2efbe5cb34c6a2ca69528f73a316c16c9d31c0e2b49b88"
raw = open(PREREG, "rb").read()
h = hashlib.sha256(raw).hexdigest()
if h != PREREG_SHA256:
    raise SystemExit("r10_elements.json has sha256 %s, expected the pre-registered %s" % (h, PREREG_SHA256))
cfg = json.loads(raw)
HX, HY = cfg["hub"]
T12 = cfg["theta12_deg"]
FX0, FY0, FX1, FY1 = cfg["frame"]
TOLS = (0.5, 1.0)
DRAWS = 10000
rng = np.random.default_rng(20260929)


def centre(b):
    return ((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0)


def angle(cx, cy, hx=HX, hy=HY):
    return math.degrees(math.atan2(-(cy - hy), cx - hx))


def offset(theta, t12=T12):
    r = (theta - t12) % 15.0
    return min(r, 15.0 - r)


def counts(cents, t12=T12, hx=HX, hy=HY):
    d = np.array([offset(angle(cx, cy, hx, hy), t12) for cx, cy in cents])
    return [int((d <= t).sum()) for t in TOLS]


def nulls(cents):
    rot = np.zeros((DRAWS, 2), int)
    hub = np.zeros((DRAWS, 2), int)
    us = rng.uniform(0, 15, DRAWS)
    hxs = rng.uniform(FX0, FX1, DRAWS)
    hys = rng.uniform(FY0, FY1, DRAWS)
    C = np.array(cents)
    for i in range(DRAWS):
        th = np.degrees(np.arctan2(-(C[:, 1] - HY), C[:, 0] - HX))
        r = (th - (T12 + us[i])) % 15.0
        d = np.minimum(r, 15.0 - r)
        rot[i] = [(d <= t).sum() for t in TOLS]
        th = np.degrees(np.arctan2(-(C[:, 1] - hys[i]), C[:, 0] - hxs[i]))
        r = (th - T12) % 15.0
        d = np.minimum(r, 15.0 - r)
        hub[i] = [(d <= t).sum() for t in TOLS]
    return rot, hub


def grid_slot(theta):
    j = int(round(((T12 - theta) % 360.0) / 15.0)) % 24      # j-th direction clockwise from 12
    if j % 2 == 0:
        n = 12 if j == 0 else j // 2
        return 2 * n, "on numeral %d" % n
    n = (j - 1) // 2
    a, b = (12, 1) if n == 0 else (n, n + 1)
    return a + b, "between %d and %d" % (a, b)


E = cfg["elements"]
FACE = cfg["face_level_substitutions"]
seal = set(cfg["seal_group"])
sets = {
    "A  whole objects, all 28": {k: v["box"] for k, v in E.items()},
    "B  whole objects, seal excluded": {k: v["box"] for k, v in E.items() if k not in seal},
    "C  face level, all 28": {k: FACE.get(k, v["box"]) for k, v in E.items()},
    "D  face level, seal excluded": {k: FACE.get(k, v["box"]) for k, v in E.items() if k not in seal},
}

print("pre-registration verified: r10_elements.json sha256 %s" % h)
print("hub (%.2f, %.2f)  theta12 %.2f deg  grid every 15 deg; chance P(offset <= t) = t / 7.5" % (HX, HY, T12))

print("\nPER-ELEMENT OFFSETS, set A (angular half-width = half the angle the box subtends at the hub)")
print("   %-4s %-52s %8s %7s %8s %9s %s" % ("id", "element", "dist", "theta", "offset", "halfwid", "nearest"))
for k, v in E.items():
    cx, cy = centre(v["box"])
    th = angle(cx, cy)
    b = v["box"]
    angs = [angle(x, y) for x in (b[0], b[2]) for y in (b[1], b[3])]
    hw = (max(angs) - min(angs)) / 2 if max(angs) - min(angs) < 180 else float("nan")
    s, where = grid_slot(th)
    print("   %-4s %-52s %8.0f %7.2f %8.2f %9.1f %s" % (k, v["name"][:52], math.hypot(cx - HX, cy - HY), th, offset(th), hw, where))

print("\nCOUNTS AGAINST BOTH NULLS")
print("   %-34s %3s   %-28s %-28s" % ("set", "N", "within 0.5 deg: obs / exp / p(rot) / p(hub)", "within 1.0 deg: same"))
verdict = {}
for name, boxes in sets.items():
    cents = [centre(b) for b in boxes.values()]
    obs = counts(cents)
    rot, hub = nulls(cents)
    cells = []
    sig = []
    for i, t in enumerate(TOLS):
        pr = (1 + (rot[:, i] >= obs[i]).sum()) / (1 + DRAWS)
        ph = (1 + (hub[:, i] >= obs[i]).sum()) / (1 + DRAWS)
        cells.append("%2d / %4.1f / %.4f / %.4f" % (obs[i], len(cents) * t / 7.5, pr, ph))
        sig.append(pr < 0.05 and ph < 0.05)
    verdict[name] = sig
    print("   %-34s %3d   %-28s   %-28s" % (name, len(cents), cells[0], cells[1]))

print("\nPILOT'S FIVE NAMED ITEMS (side check, not evidence)")
for k, b in cfg["pilot_named_items_side_check"].items():
    cx, cy = centre(b)
    th = angle(cx, cy)
    print("   %-22s centre (%.1f, %.1f)  theta %.2f  offset %.2f deg  %s" % (k, cx, cy, th, offset(th), grid_slot(th)[1]))

primary = verdict["A  whole objects, all 28"]
significant = any(primary)
print("\nDECISION (pre-stated rule, primary set A): %s" % ("SIGNIFICANT" if significant else "NOT SIGNIFICANT"))
if significant:
    print("slots for set-A elements within 1.0 deg:")
    slots = {}
    for k, v in E.items():
        cx, cy = centre(v["box"])
        th = angle(cx, cy)
        if offset(th) <= 1.0:
            s, where = grid_slot(th)
            slots.setdefault(s, []).append("%s %s (%s)" % (k, v["name"], where))
    for s in sorted(slots):
        print("   slot %2d <- %s%s" % (s, "; ".join(slots[s]), "   ** COLLISION" if len(slots[s]) > 1 else ""))
else:
    print("-> the clock governs the hands and the seal only; the non-clock half of the phrase has no")
    print("   recoverable layout rule in this image. Stop.")
