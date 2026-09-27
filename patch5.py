#!/usr/bin/env python3
"""
patch5.py — apply the 23 Sep additions to REPORT.md.

Run from the repo root (~/blm-analysis), where REPORT.md and
report_additions.md both live.

    python3 patch5.py --inspect     print the §10 sub-structure (do this first)
    python3 patch5.py --dry-run     show the unified diff, write nothing
    python3 patch5.py --apply       write REPORT.md (backup at REPORT.md.bak)

DESIGN NOTES

1. The content is NOT duplicated here. Every inserted block is read out of
   report_additions.md at run time and the leading "> " quote marker stripped.
   That file is the single copy; editing it changes what this script applies.
   A patch script carrying its own copy of the text would be a second source of
   truth, which is the failure this project has now hit three times.

2. The file is pinned by md5 AND line count before anything is touched. An
   anchor-checked patch can still apply cleanly to the WRONG file if the anchors
   happen to exist in both — and there is a 546-line REPORT.md in ~/Downloads
   that is 298 lines stale. Anchors verify what you are editing; a hash verifies
   WHICH FILE you are editing. Both are needed.

3. Line-range splices are applied bottom-up so earlier indices stay valid.

4. It refuses to apply while any Sunday figure is still None.
"""

import sys, os, re, hashlib, difflib

HERE   = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, 'REPORT.md')
DRAFT  = os.path.join(HERE, 'report_additions.md')

# ---------------------------------------------------------------- identity
EXPECT_MD5   = 'c901b4ffef659d12c3b4d463b48c7605'
EXPECT_LINES = 800
EXPECT_COMMIT = '5fee94d'

# ---------------------------------------------------------------- line map
# 1-based, inclusive. From the structure dump of 5fee94d.
SEC = {
    'insert_after_2_12': 364,   # §2.13 and §2.14 go in here, before §3 at 365
    'sec3':  (365, 399),        # replaced entirely
    'sec8':  (667, 683),        # replaced entirely
    'sec9':  (684, 705),        # criterion 7 appended at the end
}

# §10 spans 706-800. Filled from --inspect against 5fee94d.
#   706  ## 10. Method
#   710-718  rate table (PRE-rewrite; the EC block says so)
#   720-723  two-kernel paragraph        <- EC rewrite goes after this
#   725-745  seam validation
#   747-763  positive controls
#   765      "**Eight bugs were caught..."
#   768-789  the eight bullets           <- bugs 9-13 go after 789
#   791-793  closing advice              <- the rules subsection goes after 793
#   795      ---
#   797-800  envoi
SEC10 = {
    'bug_count_line':     765,
    'bug_list_end':       789,
    'rules_insert_after': 793,
    'ec_insert_after':    723,
}
RULES_HEADING = '**Five rules, each learned by getting it wrong first:**'

# ---------------------------------------------------------------- figures
# Fill from `python3 tally2.py configs` once free4/16/12/19 land.
FIGS = {
    'evidenced': '187,091,405,931',   # 22 evidenced runs
    'combined':  '190,701,305,838',   # + the twelve asserted
    'marginal':    '3,609,899,907',   # difference of the two printed figures
    'cpu_days':            '5,518',   # at 400 derivations/s
    'headline':  'over 190 billion',  # replaces "26.5 billion" on line 1
}


def die(msg):
    print('patch5: ' + msg, file=sys.stderr)
    sys.exit(1)


def read_report():
    if not os.path.exists(REPORT):
        die('REPORT.md not found beside this script. Run from ~/blm-analysis.')
    raw = open(REPORT, 'rb').read()
    md5 = hashlib.md5(raw).hexdigest()
    lines = raw.decode('utf-8').split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    if md5 != EXPECT_MD5 or len(lines) != EXPECT_LINES:
        die('IDENTITY MISMATCH — refusing to touch this file.\n'
            '  expected  md5 {}  lines {}  (commit {})\n'
            '  found     md5 {}  lines {}\n'
            'This is either the stale 546-line copy from ~/Downloads, or\n'
            'REPORT.md moved since the structure dump. Re-dump and update the\n'
            'constants at the top of this script; do not edit the hash to match.'
            .format(EXPECT_MD5, EXPECT_LINES, EXPECT_COMMIT, md5, len(lines)))
    return lines


def load_blocks():
    """Pull the quoted content out of report_additions.md, by section."""
    if not os.path.exists(DRAFT):
        die('report_additions.md not found beside this script.')
    txt = open(DRAFT, encoding='utf-8').read().split('\n')
    blocks, key, sub, buf = {}, None, None, []

    def flush():
        if key and buf:
            name = key if sub is None else '{}/{}'.format(key, sub)
            body = [re.sub(r'^> ?', '', l) for l in buf]
            while body and not body[-1].strip():
                body.pop()
            blocks[name] = body

    for l in txt:
        m2 = re.match(r'^## §([0-9.]+)', l)
        m3 = re.match(r'^### (.+)', l)
        if m2:
            flush(); buf = []; key = m2.group(1); sub = None; continue
        if m3 and key:
            flush(); buf = []; sub = m3.group(1).strip(); continue
        if l.startswith('>'):
            buf.append(l)
        elif buf and not l.strip():
            buf.append('')
    flush()
    return blocks


def inspect(lines):
    print('=== §10 sub-structure: lines 706-800 ===')
    print('Paste this back so the SEC10 constants can be filled.\n')
    for i in range(705, min(800, len(lines))):
        print('{:>4}  {}'.format(i + 1, lines[i]))
    print('\n=== anchor lines referenced by this script ===')
    for n in (1, 14, SEC10['bug_count_line']):
        if n and n <= len(lines):
            print('{:>4}  {}'.format(n, lines[n - 1]))


def build(lines, blocks):
    out = list(lines)
    edits = []          # (start1, end1, replacement_lines) — 1-based inclusive

    # --- §9: append acceptance criterion 7 -----------------------------
    body = blocks.get('9')
    if not body:
        die('could not find the §9 block in report_additions.md')
    edits.append((SEC['sec9'][1] + 1, SEC['sec9'][1], [''] + body))

    # --- §8: replace entirely ------------------------------------------
    body = blocks.get('8')
    if not body:
        die('could not find the §8 block in report_additions.md')
    hdr = lines[SEC['sec8'][0] - 1]
    edits.append((SEC['sec8'][0], SEC['sec8'][1], [hdr, ''] + body))

    # --- §3: replace entirely ------------------------------------------
    body = blocks.get('3')
    if not body:
        die('could not find the §3 block in report_additions.md')
    body = fill_figures(body)
    hdr = lines[SEC['sec3'][0] - 1]
    edits.append((SEC['sec3'][0], SEC['sec3'][1], [hdr, ''] + body))

    # --- line 1 and line 14: the headline figure --------------------------
    if '26.5 billion' not in lines[0]:
        die('line 1 no longer contains "26.5 billion" — headline anchor moved.\n'
            '  found: {!r}'.format(lines[0]))
    edits.append((1, 1, [lines[0].replace('26.5 billion', FIGS['headline'])]))
    if '26,513,178,774' not in lines[13]:
        die('line 14 no longer contains "26,513,178,774" — anchor moved.\n'
            '  found: {!r}'.format(lines[13]))
    l14 = lines[13].replace('26,513,178,774', FIGS['combined'])
    if '767 days of CPU' in l14:
        l14 = l14.replace('767 days of CPU', FIGS['cpu_days'] + ' days of CPU')
    edits.append((14, 14, [l14]))

    # --- §2.13 and §2.14: insert before §3 ------------------------------
    ins = []
    for k, title in (('2.13', '### §2.13 — [EXHAUSTED] Free-one-fixed at 21 words: '
                              'the branch that was never run'),
                     ('2.14', '### §2.14 — [EXHAUSTED] Two hypotheses the source '
                              'document itself named')):
        b = blocks.get(k)
        if not b:
            die('could not find the §{} block in report_additions.md'.format(k))
        ins += [title, ''] + b + ['']
    edits.append((SEC['insert_after_2_12'] + 1, SEC['insert_after_2_12'], ins))

    # --- §10 -------------------------------------------------------------
    missing = [k for k, v in SEC10.items() if v is None]
    if missing:
        print('patch5: §10 NOT patched — unknown line numbers: {}\n'
              '        run `python3 patch5.py --inspect`, paste the output,\n'
              '        fill the SEC10 constants, and re-run.'
              .format(', '.join(sorted(missing))), file=sys.stderr)
    else:
        n = SEC10['bug_count_line']
        if 'Eight' not in lines[n - 1]:
            die('line {} does not contain "Eight" — the bug-count anchor moved.\n'
                '  found: {!r}'.format(n, lines[n - 1]))
        edits.append((n, n, [lines[n - 1].replace('Eight', 'Thirteen')]))
        # §10 has no existing rules list, so the rules arrive with a heading.
        for key, sub, head in (
                ('rules_insert_after', 'Five rules',          [RULES_HEADING, '']),
                ('bug_list_end',       'Bugs 9 through 13',   []),
                ('ec_insert_after',    'The EC rewrite',      [])):
            b = blocks.get('10/' + sub)
            if not b:
                die('could not find the "{}" sub-block in the draft'.format(sub))
            at = SEC10[key]
            edits.append((at + 1, at, [''] + head + b))

    # bottom-up so earlier indices stay valid
    for start, end, repl in sorted(edits, key=lambda e: -e[0]):
        out[start - 1:end] = repl
    return out


def fill_figures(body):
    missing = [k for k, v in FIGS.items() if v is None]
    if missing:
        die('Sunday figures not filled: {}\n'
            'Run `python3 tally2.py configs` once free4/16/12/19 have landed and\n'
            'set FIGS at the top of this script. Refusing to write placeholders.'
            .format(', '.join(sorted(missing))))
    order = ['evidenced', 'combined', 'marginal', 'cpu_days']
    it = iter(order)
    outl = []
    for l in body:
        while '[FIGURE]' in l:
            l = l.replace('[FIGURE]', str(FIGS[next(it)]), 1)
        outl.append(l)
    return outl


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else '--dry-run'
    lines = read_report()
    print('patch5: identity OK — md5 {} ... {} lines, commit {}'
          .format(EXPECT_MD5[:8], EXPECT_LINES, EXPECT_COMMIT), file=sys.stderr)

    if mode == '--inspect':
        inspect(lines); return

    blocks = load_blocks()
    print('patch5: draft blocks found: {}'
          .format(', '.join(sorted(blocks))), file=sys.stderr)

    new = build(lines, blocks)
    diff = list(difflib.unified_diff(lines, new, 'REPORT.md', 'REPORT.md (patched)',
                                     lineterm='', n=2))
    print('patch5: {} -> {} lines, {} diff lines'
          .format(len(lines), len(new), len(diff)), file=sys.stderr)

    if mode == '--dry-run':
        print('\n'.join(diff))
        print('\npatch5: DRY RUN — nothing written. Re-run with --apply.',
              file=sys.stderr)
        return

    if mode != '--apply':
        die('unknown mode {!r} — use --inspect, --dry-run or --apply'.format(mode))

    open(REPORT + '.bak', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    open(REPORT, 'w', encoding='utf-8').write('\n'.join(new) + '\n')
    print('patch5: written. backup at REPORT.md.bak', file=sys.stderr)
    print('patch5: now `git diff REPORT.md` and read it before committing.',
          file=sys.stderr)


if __name__ == '__main__':
    main()
