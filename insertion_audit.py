#!/usr/bin/env python3
"""REPORT 1.18. Did an insertion land inside an entry instead of between entries?

Diffs REPORT.md (working copy) against a published version -- default origin/main --
and, for every inserted or replaced block of 3+ lines, prints the first non-blank line
that FOLLOWS it. A block followed by a heading, a top-level bullet, a tagged paragraph
or a tagged quote ends cleanly. A block followed by anything else may have split the
entry it was inserted into, and is listed for reading by hand.

Found five splits written on 10 Nov 2026, three of them only by this audit.
Usage: python3 insertion_audit.py [base] [--target REF]
  base     the published version to diff against (default origin/main)
  --target audit REF:REPORT.md instead of the working copy -- the positive control is
           to point this at a version known to contain splits and see them listed.
Exit 0 clean, 1 if anything is listed.

What is NOT listed, because it is not a split: a 1-2 line in-place word edit; a
replacement that adds fewer than 3 lines net (an edit inside a paragraph); and a
block whose last line is a heading (what follows a heading is that heading's body).
"""
import difflib, re, subprocess, sys

args = sys.argv[1:]
target = None
if "--target" in args:
    i = args.index("--target"); target = args[i + 1]; del args[i:i + 2]
ref = args[0] if args else "origin/main"
old = subprocess.run(["git", "show", f"{ref}:REPORT.md"], capture_output=True, text=True)
if old.returncode:
    sys.exit(f"cannot read {ref}:REPORT.md")
old = old.stdout.split("\n")
if target:
    tgt = subprocess.run(["git", "show", f"{target}:REPORT.md"], capture_output=True, text=True)
    if tgt.returncode:
        sys.exit(f"cannot read {target}:REPORT.md")
    new = tgt.stdout.split("\n")
else:
    new = open("REPORT.md", encoding="utf-8").read().split("\n")

CLEAN = re.compile(r"^(#{1,6} |- \*\*|(> )+\*\*\[|\*\*\[|\*\*\"|---\s*$)")
def blank(s): return not s.strip() or s.strip() == ">"

listed, n = [], 0
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
    if op == "insert":
        pass
    elif op == "replace" and (j2 - j1) - (i2 - i1) >= 3:
        pass                          # an insertion merged with a nearby edit
    else:
        continue                      # in-place edits inside a paragraph are not splits
    n += 1
    k = j2
    while k < len(new) and blank(new[k]): k += 1
    nxt = new[k] if k < len(new) else "<EOF>"
    last = next((x for x in reversed(new[j1:j2]) if not blank(x)), "")
    if nxt == "<EOF>" or CLEAN.match(nxt) or re.match(r"^#{1,6} ", last):
        continue
    first = next((x for x in new[j1:j2] if not blank(x)), "")
    listed.append((j1 + 1, j2, first, nxt))

what = f"{target}:REPORT.md" if target else "REPORT.md (working copy)"
print(f"insertion audit, {what} against {ref}: {n} insertion(s) examined")
for a, b, first, nxt in listed:
    print(f"\n  lines {a}-{b}\n    starts  {first[:96]}\n    next    {nxt[:96]}   <-- read by hand")
print(f"\n{'CLEAN' if not listed else str(len(listed)) + ' to read by hand'}")
sys.exit(1 if listed else 0)
