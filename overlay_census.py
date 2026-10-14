#!/usr/bin/env python3
"""Brighter-pixel census across faint overlay texts, exactly as fixed in circled_check/overlay_census_plan.tsv.

usage: ~/venvs/blm-img/bin/python -I overlay_census.py MASTER PLAN.tsv [--round 1|2]

Reads the items and windows from the plan; the method and decision rule are the plan's, unchanged.
--round 1 (default) reproduces plan e915ab5; --round 2 implements overlay_census_plan_r2.tsv.
Pixels only. No reading of what any item says.
"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi

im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
L = np.round(0.299 * im[..., 0] + 0.587 * im[..., 1] + 0.114 * im[..., 2]).astype(int)
EIGHT = np.ones((3, 3), bool)
ROUND = int(sys.argv[sys.argv.index('--round') + 1]) if '--round' in sys.argv else 1

items = []
for line in open(sys.argv[2], encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    f = line.rstrip('\n').split('\t')
    items.append(dict(id=f[0], role=f[1], name=f[2], box=tuple(map(int, f[3:7]))))

rows = []
print(f"{'id':3s} {'role':15s} {'fill':>4s} {'cover':>6s} {'mask':>5s} {'depth':>5s} {'nbrs':>5s} {'brighter':>8s} {'max':>4s} {'FAR':>4s}  status   name")
for it in items:
    x0, y0, x1, y1 = it['box']
    W = L[y0:y1 + 1, x0:x1 + 1]
    if ROUND == 1:
        vals, cnts = np.unique(W, return_counts=True)
        fill = int(vals[cnts.argmax()]); cover = cnts.max() / W.size
    else:
        med = np.median(W); up = W[W > med]
        if up.size == 0: up = W[W >= med]
        vals, cnts = np.unique(up, return_counts=True)
        fill = int(vals[cnts.argmax()])
        mk = W <= fill - 4
        farm = ~ndi.binary_dilation(mk, EIGHT, iterations=2) if mk.any() else np.ones_like(mk)
        cover = float((W[farm] == fill).mean()) if farm.any() else 0.0
    r = dict(it, fill=fill, cover=cover, mask=0, depth=None, nbrs=0, bright=0, bmax=None, far=0)
    if ROUND == 2 and fill >= 250:
        r['status'] = 'EXCLUDED'
    elif ROUND == 2 and not (W <= fill - 4).any():
        r['status'] = 'NO-MARKS'
    elif cover < 0.5:
        r['status'] = 'SKIPPED'
    elif fill >= 250:
        r['status'] = 'EXCLUDED'
    else:
        mask = W <= fill - 4
        r['mask'] = int(mask.sum())
        if not mask.any():
            r['status'] = 'NO-MARKS'
        else:
            near = ndi.binary_dilation(mask, EIGHT, iterations=2)
            nb = near & ~mask
            br = nb & (W >= fill + 1)
            far = ~near & (W >= fill + 1)
            r.update(depth=fill - int(W[mask].min()), nbrs=int(nb.sum()), bright=int(br.sum()),
                     bmax=int(W[br].max()) if br.any() else None, far=int(far.sum()))
            r['status'] = ('INDETERM' if r['far'] > 0 and r['bright'] > 0 else
                           'SHOWS' if r['bright'] > 0 else 'NONE')
    rows.append(r)
    print(f"{r['id']:3s} {r['role']:15s} {r['fill']:4d} {r['cover']:6.1%} {r['mask']:5d} "
          f"{'' if r['depth'] is None else r['depth']:>5} {r['nbrs']:5d} {r['bright']:8d} "
          f"{'' if r['bmax'] is None else r['bmax']:>4} {r['far']:4d}  {r['status']:8s} {r['name']}")

subj = [r for r in rows if r['role'] == 'subject']
dec = [r for r in rows if r['role'] in ('overlay-s9', 'overlay-numeral')]
if ROUND == 2:
    INEL = ('SKIPPED', 'EXCLUDED', 'NO-MARKS')
    el = [r for r in dec if r['status'] not in INEL]
    cel = [r for r in rows if r['role'] == 'control' and r['status'] not in INEL]
    print('\nROUND 2')
    print('ineligible decision-set items (count against nothing):', ', '.join(f"{r['id']} {r['name']} [{r['status']}]" for r in dec if r['status'] in INEL) or 'none')
    print('eligible decision-set items:', ', '.join(f"{r['id']} [{r['status']}]" for r in el) or 'none')
    print('eligible controls:', ', '.join(f"{r['id']} [{r['status']}]" for r in cel) or 'none')
    s_ok = bool(subj) and all(r['status'] == 'SHOWS' for r in subj)
    print('subject:', subj[0]['status'] if subj else '-')
    if len(el) < 3:
        print('DECISION: cannot be decided at this resolution (fewer than 3 eligible overlay items)')
    elif s_ok and all(r['status'] == 'SHOWS' for r in el) and not any(r['status'] in ('SHOWS', 'INDETERM') for r in cel):
        print('DECISION: the tablet marks share the rendering signature of the faint overlay texts')
    else:
        print('DECISION: mixed')
    sys.exit(0)
ctl = [r for r in rows if r['role'] == 'control']
ctl_elig = [r for r in ctl if r['status'] not in ('SKIPPED', 'EXCLUDED')]
print('\nsubject shows:', all(r['status'] == 'SHOWS' for r in subj))
print(f"decision set: {len(dec)} items; shows {sum(r['status'] == 'SHOWS' for r in dec)}; "
      f"none {sum(r['status'] == 'NONE' for r in dec)}; skipped {sum(r['status'] == 'SKIPPED' for r in dec)}; "
      f"excluded {sum(r['status'] == 'EXCLUDED' for r in dec)}; no-marks {sum(r['status'] == 'NO-MARKS' for r in dec)}; "
      f"indeterminate {sum(r['status'] == 'INDETERM' for r in dec)}")
print(f"controls: {len(ctl)} items; eligible {len(ctl_elig)}; showing {sum(r['status'] in ('SHOWS', 'INDETERM') for r in ctl_elig)}")
ok = (all(r['status'] == 'SHOWS' for r in subj) and all(r['status'] == 'SHOWS' for r in dec)
      and not any(r['status'] in ('SHOWS', 'INDETERM') for r in ctl_elig))
print('DECISION:', 'the tablet marks share the rendering signature of the faint overlay texts' if ok else 'MIXED')
