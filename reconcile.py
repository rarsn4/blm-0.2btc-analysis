#!/usr/bin/env python3
"""
reconcile.py — bring README.md and STATUS.md into agreement with REPORT.md.

Run from the repo root.

    python3 reconcile.py            dry run: print every line it would change
    python3 reconcile.py --apply    write the files

WHY THIS EXISTS

One repo currently states three different totals:

    README.md    25,188,563,424 derivations,   729 CPU-days
    STATUS.md    78,273,080,964 derivations, 2,265 CPU-days
    REPORT.md   190,701,305,838 derivations, 5,518 CPU-days

and STATUS.md section 8 asserts, as [MEASURED], the marked-and-withheld reading
that REPORT.md section 7.7 retracts. A reader hitting the assertion first sees the
stronger tag on the withdrawn claim.

TWO DIFFERENT TREATMENTS, DELIBERATELY

README.md is a front page. Its job is to be current, so its figures are replaced.

STATUS.md is a dated snapshot of what was believed at a point in time, and its
value is precisely that it is not current. Rewriting it to match today would
destroy the record -- and STATUS.md section 8 is the document that caused
REPORT.md section 8 to be overwritten, because three parties spent four days
discussing "section 8" while reading neither. That evidence is worth keeping.

So STATUS.md is NOT rewritten. It gets a header marking it superseded, and its
three contradicting claims are retagged in place so the withdrawal is visible
where the claim is made. The bodies stay.

Note that STATUS.md's 78,273,080,964 is not simply stale. It predates the
free-one-fixed campaign, so every t21 run it counted was a gap sweep -- the
branch where all assigned words are correct. It is the figure REPORT.md 2.13
cites as "roughly 78 billion went into the 1.8% branch", and it is correct as
that. The header says so rather than crossing it out.
"""

import sys, os, re

APPLY = '--apply' in sys.argv
CHANGES = []          # (file, lineno, before, after)


def edit(path, rules, header=None):
    if not os.path.exists(path):
        print('  SKIP {} (not present)'.format(path)); return
    lines = open(path, encoding='utf-8').read().split('\n')
    hits = {k: 0 for k, _, _ in rules}
    for i, l in enumerate(lines):
        for key, pat, repl in rules:
            if re.search(pat, l):
                new = re.sub(pat, repl, l)
                if new != l:
                    CHANGES.append((path, i + 1, l, new))
                    lines[i] = new
                    hits[key] += 1
                    l = new
    missing = [k for k, n in hits.items() if n == 0]
    if missing:
        print('  {}: NO MATCH for {} — anchors moved, nothing written for this file'
              .format(path, ', '.join(missing)))
        return
    if header:
        lines = header.split('\n') + [''] + lines
        CHANGES.append((path, 0, '(top of file)', '+{} header lines'.format(
            len(header.split('\n')))))
    if APPLY:
        open(path, 'w', encoding='utf-8').write('\n'.join(lines))
    print('  {}: {} line(s) {}'.format(
        path, sum(hits.values()), 'written' if APPLY else 'would change'))


# ---------------------------------------------------------------- README.md
edit('README.md', [
    ('total',    r'25,188,563,424', '190,701,305,838'),
    ('cpu_days', r'\b729\b(?=\s*(CPU-days|CPU days|days))', '5,518'),
])

# ---------------------------------------------------------------- STATUS.md
STATUS_HEADER = """> **SUPERSEDED SNAPSHOT — do not cite figures from this file.**
>
> This is a working status document, dated, kept as a record of what was believed
> at the time. `REPORT.md` is authoritative. Three claims below have since been
> withdrawn or overtaken, and each is retagged in place rather than rewritten,
> because what was believed when is itself part of the record:
>
> - **Section 8, "the pattern worth naming"** — retracted. Four of its five
>   entries fail a base rate; only the blank clock hand survives, and on measured
>   hand placement rather than on an absence. See `REPORT.md` §7.7. This section
>   is also the direct cause of a publishing error: it was numbered 8 here, and
>   "§8" was discussed for four days as though it were a section of `REPORT.md`,
>   whose §8 was consequently overwritten. See `REPORT.md` §10, bug 15.
> - **The bug count** — `REPORT.md` §10 now lists fifteen.
> - **The derivation total, 78,273,080,964** — not wrong, superseded. This file
>   predates the free-one-fixed campaign, so every t21 run it counted was a *gap*
>   sweep: the branch in which all assigned words are correct. It is the figure
>   `REPORT.md` §2.13 cites as "roughly 78 billion went into the 1.8% branch".
>   The current total across all branches is **190,701,305,838**.
> - **The 31× brainwallet-to-seed cost ratio** (489,000/s against 15,600/s) — both
>   figures are pre-Jacobian, and no uncontended re-measurement exists. Treat the
>   ratio as unquantified; the exclusion argument in `REPORT.md` §2.12 does not
>   depend on its value."""

edit('STATUS.md', [
    ('pattern',   r'\[MEASURED\](?=\s*The pattern worth naming)',
                  '[RETRACTED — see REPORT.md §7.7]'),
    ('bugcount',  r'\bTen bugs\b',
                  'Ten bugs *(superseded: REPORT.md §10 lists fifteen)*'),
    ('total',     r'78,273,080,964',
                  '78,273,080,964 *(the a=0 branch only; current total 190,701,305,838)*'),
], header=STATUS_HEADER)

# ---------------------------------------------------------------- report
print()
if not CHANGES:
    print('nothing to change — anchors absent or already applied.')
else:
    for path, ln, before, after in CHANGES:
        print('{}:{}'.format(path, ln))
        print('  -  {}'.format(before[:140]))
        print('  +  {}'.format(after[:140]))
    print()
    print('DRY RUN — nothing written. Re-run with --apply.' if not APPLY
          else 'WRITTEN. `git diff` and read it before committing.')
