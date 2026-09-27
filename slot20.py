"""Slot 20: can the ink decide between `apple` and `second`?

Neither word is written or encoded anywhere in the image (letter census,
census_crops.py). The README derives slot 20 from two physical features only:
the 'XX' on the hooded head of the Leopold II bust (-> the number 20) and, for
the word `second`, the fact that Leopold II was the second King of the
Belgians. `apple` has no derivation in the README at all. This script
measures the two features:

1. the wreath plaque below the bust: is there an in-image 'II'?
2. the two X marks on the head, and
3. whether they are spaced like letters/numerals in the artist's own hand.

One method for every glyph, marks included: a glyph is a connected ink
component (8-connectivity; fragments under 40% of the median glyph height are
dropped -- by height, never by gap). GAP = clear pixels between the two
closest ink pixels of neighbouring glyphs, so slanted or rotated text is
measured the same way as upright text. HEIGHT = each glyph's own ink extent
across its line of text; a pair is normalised by the mean of its two heights.
A reference set is used only if (a) segmentation yields exactly the known
character count and (b) the boxes, written to slot20_segmentation.png, show
one glyph per box. Word spaces and dots are excluded by their position in
the known text, never by their size.
"""
import numpy as np
from PIL import Image, ImageDraw

from imgio import load_gray

G = load_gray()


def components(mask):
    lab = np.zeros(mask.shape, int)
    n = 0
    for sy, sx in zip(*np.where(mask)):
        if lab[sy, sx]:
            continue
        n += 1
        lab[sy, sx] = n
        stack = [(sy, sx)]
        while stack:
            cy, cx = stack.pop()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = cy + dy, cx + dx
                    if 0 <= yy < mask.shape[0] and 0 <= xx < mask.shape[1] and mask[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n
                        stack.append((yy, xx))
    return [np.argwhere(lab == k) for k in range(1, n + 1)]


def glyphs(y0, y1, x0, x1, thr, along, reverse):
    """Main glyphs = components; HEIGHT = across-extent of ALL ink within the
    glyph's span along the line, so a letter that breaks where the paint is
    lighter (the spray H does, at y948-966) is still measured at full height."""
    ink = np.argwhere(G[y0:y1, x0:x1] < thr) + [y0, x0]
    comps = [c + [y0, x0] for c in components(G[y0:y1, x0:x1] < thr) if len(c) >= 15]
    a_al, a_ac = (1, 0) if along == "x" else (0, 1)
    out = [(c, c[:, a_ac].max() - c[:, a_ac].min() + 1, c[:, a_al].mean()) for c in comps]
    med = np.median([h for _, h, _ in out])
    out = [g for g in out if g[1] >= 0.4 * med]
    full = []
    for c, _, pos in out:
        lo, hi = c[:, a_al].min(), c[:, a_al].max()
        span = ink[(ink[:, a_al] >= lo) & (ink[:, a_al] <= hi)][:, a_ac]
        full.append((c, span.max() - span.min() + 1, pos))
    full.sort(key=lambda g: g[2], reverse=reverse)
    return full


def closest(a, b):
    d = a[:, None, :].astype(float) - b[None, :, :]
    return np.sqrt((d ** 2).sum(axis=2)).min() - 1


# ---- 1. plaque -------------------------------------------------------------
print("1. WREATH PLAQUE (outer frame x1380/x1402, y692/y709-710)")
print("   column means over the panel rows y697-706 (panel light ~150-160):")
print("   " + "  ".join("x%d %.0f" % (x, G[697:707, x].mean()) for x in range(1381, 1402)))
print("   vertical extent of each stroke column (value < 135), panel rows y696-708:")
for x in (1386, 1387, 1389, 1390, 1392, 1393, 1395, 1398):
    runs, s = [], None
    for y in range(696, 709):
        on = G[y, x] < 135
        if on and s is None:
            s = y
        elif not on and s is not None:
            runs.append((s, y - 1))
            s = None
    if s is not None:
        runs.append((s, 708))
    print("     x%d  %s  min %3.0f" % (x, " ".join("y%d-%d" % r for r in runs), G[696:709, x].min()))

# ---- 2. X marks --------------------------------------------------------------
print("\n2. X MARKS ON THE HEAD (window x1345-1425 y430-490)")
bg = np.percentile(G[430:490, 1360:1420], 90)
print("   background (90th pct) %.0f; darkest hood shading between the marks %.0f -> thresholds >= ~126"
      " would bridge the marks through shadow, so the sweep stops at 120"
      % (bg, G[440:480, 1378:1392].min()))
ratios = []
for thr in (90, 100, 110, 120):
    cs = [c + [430, 1345] for c in components(G[430:490, 1345:1425] < thr) if len(c) >= 40]
    lm = max((c for c in cs if 1355 <= c[:, 1].mean() <= 1378), key=len)
    rm = max((c for c in cs if 1392 <= c[:, 1].mean() <= 1420), key=len)
    hl, hr = np.ptp(lm[:, 0]) + 1, np.ptp(rm[:, 0]) + 1
    g = closest(lm, rm)
    ratios.append(g / ((hl + hr) / 2))
    print("   ink<%d  left x%d-%d y%d-%d  right x%d-%d y%d-%d  heights %d, %d  closest-ink gap %.0f"
          "  gap/mean height %.3f" % (thr, lm[:, 1].min(), lm[:, 1].max(), lm[:, 0].min(), lm[:, 0].max(),
                                      rm[:, 1].min(), rm[:, 1].max(), rm[:, 0].min(), rm[:, 0].max(),
                                      hl, hr, g, ratios[-1]))
x_ratio = min(ratios)
print("   conservative value (smallest over the sweep): %.3f" % x_ratio)
print("   (the right mark's upper arm meets the head outline; its left side, which sets the gap, is clear)")

# ---- 3. reference: the artist's own lettering and numerals -----------------------
REFS = [  # (tag, text, region y0,y1,x0,x1, threshold, text direction, bottom-to-top?)
    ("FUCK", "FUCK", (786, 846, 1312, 1485), 80, "x", False),
    ("THIS", "THIS", (845, 903, 1302, 1480), 80, "x", False),
    ("SHIT", "SHIT", (898, 995, 1318, 1462), 80, "x", False),   # y898-900 are ink-free: THIS ends above
    ("BLACK", "BLACK", (188, 296, 1114, 1141), 90, "y", True),
    ("LIVES", "LIVES", (206, 310, 1143, 1169), 90, "y", True),
    ("MATTER", "MATTER", (198, 344, 1170, 1197), 90, "y", True),
    ("NO JUSTICE NO PEACE", "NO JUSTICE NO PEACE", (112, 425, 1199, 1226), 90, "y", True),
    ("END POLICE BRUTALITY", "END POLICE BRUTALITY", (32, 372, 1229, 1254), 90, "y", True),
    ("STOP KILLING US", "STOP KILLING US", (88, 432, 1254, 1289), 90, "y", True),
    ("NOT ONE MORE", "NOT ONE MORE", (152, 392, 1289, 1310), 90, "y", True),
    ("11.03.20", "11.03.20", (1098, 1122, 1012, 1098), 90, "x", False),
    ("05.25.20", "05.25.20", (366, 388, 988, 1072), 90, "x", False),
    (".VS.", ".VS.", (1052, 1092, 1015, 1095), 150, "x", False),
]
# Count-matching sets whose boxes, on inspection of slot20_segmentation.png,
# are NOT one glyph per box:
VISUAL_REJECT = {"NO JUSTICE NO PEACE": "the I of JUSTICE is unsegmented; the count matches only through a split elsewhere"}

print("\n3. REFERENCE: within-word gap / height in the artist's own hand")
allr, sheet = [], []
for tag, text, (y0, y1, x0, x1), thr, along, rev in REFS:
    chars = [c for c in text if c not in " ."]
    gl = glyphs(y0, y1, x0, x1, thr, along, rev)
    sub = G[y0:y1, x0:x1]
    im = Image.fromarray(np.clip(sub, 0, 255).astype(np.uint8)).resize(
        (sub.shape[1] * 3, sub.shape[0] * 3), Image.NEAREST).convert("RGB")
    d = ImageDraw.Draw(im)
    for c, _, _ in gl:
        ys, xs = c[:, 0] - y0, c[:, 1] - x0
        d.rectangle([xs.min() * 3, ys.min() * 3, (xs.max() + 1) * 3 - 1, (ys.max() + 1) * 3 - 1], outline=(255, 0, 0))
    sheet.append((tag, im.rotate(-90, expand=True) if along == "y" else im))
    if len(gl) != len(chars):
        print("   %-22s rejected: %d glyphs for %d characters" % (tag, len(gl), len(chars)))
        continue
    if tag in VISUAL_REJECT:
        print("   %-22s rejected on inspection: %s" % (tag, VISUAL_REJECT[tag]))
        continue
    pairs, k, prev = [], 0, None
    for ch in text:
        if ch == " ":
            prev = None
            continue
        if ch != "." and prev not in (None, "."):
            pairs.append((k - 1, k))
        if ch != ".":
            k += 1
        prev = ch
    rs = []
    for i, j in pairs:
        g, h = closest(gl[i][0], gl[j][0]), (gl[i][1] + gl[j][1]) / 2
        rs.append((chars[i] + chars[j], g, h, g / h))
    allr += [r[3] for r in rs]
    print("   %-22s %s" % (tag, "  ".join("%s %.0f/%.0f=%.3f" % r for r in rs)))

W = max(im.width for _, im in sheet) + 8
H = sum(im.height + 16 for _, im in sheet)
out = Image.new("RGB", (W, H), (255, 255, 255))
dd = ImageDraw.Draw(out)
y = 0
for tag, im in sheet:
    dd.text((4, y + 2), tag, fill=(0, 0, 255))
    out.paste(im, (0, y + 14))
    y += im.height + 16
out.save("slot20_segmentation.png")

allr = np.array(allr)
print("\n4. RESULT")
print("   reference pairs n=%d (%s): median %.3f, 95th pct %.3f, max %.3f"
      % (len(allr), "within-word, verified sets", np.median(allr), np.percentile(allr, 95), allr.max()))
print("   X marks %.3f = %.1fx the reference maximum, %.1fx its median"
      % (x_ratio, x_ratio / allr.max(), x_ratio / np.median(allr)))
print("   wrote slot20_segmentation.png (every reference set, with its glyph boxes)")
