#!/bin/bash
# Pre-push check (DO_NOT_PUSH). Checks everything a push of HEAD to origin/main would send: the tree and
# the message of every commit in origin/main..HEAD, plus the current tracked files. Three checks:
#   1. Pattern '^\s*HIT[[:space:]]+index|^\s*phrase[[:space:]]*:'. Allowed, by content: the planted
#      self-test pair, "HIT   index 2270828" and "phrase : tiger live melody ..." on the line directly
#      after it, in README.md and REPORT.md. Any other match blocks.
#   2. Private deny-list: if ~/blm-private/never_publish.txt exists, any case-insensitive fixed-string
#      match of one of its lines blocks. This script names only the path, never the entries.
#   3. Phrase guard: 12 or more consecutive BIP39 words block, in any format. Tokens are runs of letters
#      (digits and punctuation separate them), compared case-insensitively with configs/bip39_en.txt.
#      Runs continue across line breaks, so a wrapped phrase is still one run. Exempt, and breaking a
#      run: lines starting with POOL or SLOT in configs/*.conf, the wordlist itself, and the 2270828
#      self-test phrase line. Exempt by exact content: blobs pinned in pre_push_allow.txt (<sha> <path>),
#      reviewed once by hand; editing such a file changes its sha, so the new content is checked again.
#      A commit message is never exempt.
# If origin/main cannot be resolved: BLOCK, never a fall-back to the current tree only.
# A match's text is never printed: only commit, file, line and kind. Exit 0 PASS, 1 BLOCK.
cd "$(dirname "$0")" || exit 1
PAT='^\s*HIT[[:space:]]+index|^\s*phrase[[:space:]]*:'
NP=~/blm-private/never_publish.txt
base=$(git rev-parse --verify -q 'origin/main^{commit}') || { echo "BLOCK: origin/main cannot be resolved"; exit 1; }
commits=$(git rev-list "$base..HEAD") || { echo "BLOCK: git rev-list $base..HEAD failed"; exit 1; }
ncommits=$(printf '%s\n' $commits | grep -c .)
np=
if [ -e "$NP" ]; then
  np=$(mktemp -p "$(dirname "$NP")") || { echo "BLOCK: cannot stage the deny-list"; exit 1; }
  trap 'rm -f "$np"' EXIT
  grep -v '^[[:space:]]*$' "$NP" > "$np" || { echo "BLOCK: $NP exists but has no readable entries"; exit 1; }
fi

# every line below is <where>:<file>:<line>:<text or @kind>; a failure becomes a line that blocks
{
  git grep -n -E "$PAT" | sed 's/^/worktree:/'; [ "${PIPESTATUS[0]}" -gt 1 ] && echo "worktree:(git grep failed):0:"
  if [ -n "$np" ]; then
    git grep -n -i -F -f "$np" | cut -d: -f1-2 | sed 's/^/worktree:/; s/$/:@private/'
    [ "${PIPESTATUS[0]}" -gt 1 ] && echo "worktree:(git grep failed):0:"
  fi
  for c in $commits; do
    git grep -n -E "$PAT" "$c"; [ $? -gt 1 ] && echo "$c:(git grep failed):0:"
    git log -1 --format=%B "$c" | grep -n -E "$PAT" | sed "s/^/$c:(commit message):/"
    if [ -n "$np" ]; then
      git grep -n -i -F -f "$np" "$c" | cut -d: -f1-3 | sed 's/$/:@private/'
      [ "${PIPESTATUS[0]}" -gt 1 ] && echo "$c:(git grep failed):0:"
      git log -1 --format=%B "$c" | grep -n -i -F -f "$np" | cut -d: -f1 | sed "s/^/$c:(commit message):/; s/\$/:@private/"
    fi
  done
  python3 -I - $commits <<'PY'
import os, re, subprocess, sys
TOK = re.compile(r'[^\W\d_]+')
HIT = re.compile(r'^\s*HIT\s+index\s+2270828\s*$')
SELF = re.compile(r'^\s*phrase\s*:\s*tiger live melody ')
CONF = re.compile(r'^configs/[^/]+\.conf$')
POOLSLOT = re.compile(r'^(POOL|SLOT)\b')
ALLOW_FILE = 'pre_push_allow.txt'

def emit(where, path, line, kind): print(f'{where}:{path}:{line}:@{kind}')

def scan(where, path, data, sha=None, also=0):
    if os.path.basename(path) == 'bip39_en.txt' and data == REF: return
    if sha is not None and (path, sha) in ALLOW: SKIPPED.add((path, sha)); return
    lines = data.decode('utf-8', 'replace').split('\n')
    conf, doc = bool(CONF.match(path)), path in ('README.md', 'REPORT.md')
    run = start = last = 0
    def flag():
        more = f', and in {also} later commit(s)' if also else ''
        emit(where, path, start, f'phrase guard: {run} consecutive BIP39 words, lines {start}-{last}{more}')
    for i, ln in enumerate(lines, 1):
        if (conf and POOLSLOT.match(ln)) or (doc and i > 1 and SELF.match(ln) and HIT.match(lines[i - 2])):
            if run >= 12: flag()
            run = 0; continue
        for tok in TOK.findall(ln):
            if tok.lower() in W:
                if run == 0: start = i
                run += 1; last = i
            else:
                if run >= 12: flag()
                run = 0
    if run >= 12: flag()

try:
    REF = open('configs/bip39_en.txt', 'rb').read()
    words = REF.decode().split()
    if not (len(words) == 2048 and len(set(words)) == 2048 and words == sorted(words)
            and all(w.isalpha() and w.islower() for w in words)):
        raise ValueError('configs/bip39_en.txt is not 2048 sorted, unique, lowercase words')
    W = set(words)
    ALLOW, SKIPPED = set(), set()
    if os.path.exists(ALLOW_FILE):
        for ln in open(ALLOW_FILE):
            ln = ln.split('#')[0].split()
            if len(ln) >= 2:
                if not re.fullmatch(r'[0-9a-f]{40}', ln[0]):
                    raise ValueError(f'{ALLOW_FILE}: {ln[0][:12]}... is not a blob sha')
                ALLOW.add((ln[1], ln[0]))
    for path in subprocess.run(['git', 'ls-files', '-z'], check=True, capture_output=True).stdout.decode().split('\0'):
        if not path: continue
        if os.path.islink(path): scan('worktree', path, os.readlink(path).encode())
        elif os.path.isfile(path):
            data = open(path, 'rb').read()
            sha = subprocess.run(['git', 'hash-object', path], check=True, capture_output=True).stdout.decode().strip()
            scan('worktree', path, data, sha)
    commits = sys.argv[1:]
    seen = {}                                   # (path, blob) -> [commits containing it], oldest first
    for c in reversed(commits):
        tree = subprocess.run(['git', 'ls-tree', '-r', '-z', c], check=True, capture_output=True).stdout.decode()
        for ent in tree.split('\0'):
            if not ent: continue
            meta, path = ent.split('\t', 1); mode, typ, sha = meta.split()
            if typ == 'blob': seen.setdefault((path, sha), []).append(c)
    cat = subprocess.Popen(['git', 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for (path, sha), cs in seen.items():
        cat.stdin.write(sha.encode() + b'\n'); cat.stdin.flush()
        size = int(cat.stdout.readline().split()[2]); data = cat.stdout.read(size); cat.stdout.read(1)
        scan(cs[0], path, data, sha, len(cs) - 1)
    cat.stdin.close(); cat.wait()
    for c in commits:
        scan(c, '(commit message)', subprocess.run(['git', 'log', '-1', '--format=%B', c], check=True, capture_output=True).stdout)
    unused = sorted(ALLOW - SKIPPED)
    print(f'guard:(phrase guard):0:@done {len(ALLOW)} allow-list entr(ies), {len(SKIPPED)} matched, {len(unused)} unused')
except Exception as e:
    print(f'guard:(phrase guard failed: {type(e).__name__}):0:@error')
PY
} | awk -v base="$base" -v ncommits="$ncommits" -v np="${np:+yes}" '
  function where(c) { return (c == "worktree" || c == "guard") ? c : substr(c, 1, 7) }
  { c = $0; sub(/:.*/, "", c); r = substr($0, length(c) + 2)
    f = r; sub(/:.*/, "", f); r = substr(r, length(f) + 2)
    n = r; sub(/:.*/, "", n); t = substr(r, length(n) + 2)
    if (t ~ /^@done/) { done = 1; allowinfo = substr(t, 7); next }
    doc = (f == "README.md" || f == "REPORT.md"); prev = c ":" f ":" (n - 1)
    if (doc && t ~ /^[ \t]*HIT[ \t]+index[ \t]+2270828[ \t]*$/) { hit[c ":" f ":" n] = 1; next }
    if (doc && t ~ /^[ \t]*phrase[ \t]*:[ \t]*tiger live melody / && (prev in hit)) { ok[prev] = 1; next }
    if (t == "@private") { kind = "private deny-list entry"; npriv++ }
    else if (t ~ /^@phrase guard:/) { kind = substr(t, 2); nphr++ }
    else if (t ~ /^[ \t]*HIT/) { kind = "HIT line"; npat++ }
    else if (t ~ /^[ \t]*phrase/) { kind = "phrase line"; npat++ }
    else { kind = "error"; nerr++ }
    print "  not allowed: " where(c) "  " f ":" n "  (" kind ")" }
  END { for (k in hit) if (!(k in ok)) { split(k, a, ":"); npat++
          print "  not allowed: " where(a[1]) "  " a[2] ":" a[3] "  (HIT line, no phrase line directly after)" }
        if (!done) { nerr++; print "  not allowed: the phrase guard did not report completion" }
        bad = npat + npriv + nphr + nerr
        printf "%s: %d unpushed commit(s) after %s (trees and messages) + the current tracked files\n", (bad ? "BLOCK" : "PASS"), ncommits, substr(base, 1, 7)
        printf "  pattern %d, private deny-list %d (%s), phrase guard %d, errors %d\n", npat + 0, npriv + 0, (np ? "checked" : "no list file"), nphr + 0, nerr + 0
        printf "  allow-list:%s\n", allowinfo
        exit bad ? 1 : 0 }'
