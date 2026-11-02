#!/usr/bin/env python3
"""Reconciliation gate: the brainwallet corpus must contain every string the canvas
census measures. REFUSES, does not warn.

WHY THIS EXISTS. `caccobus` was hashed for five weeks because a transcription was
written down once and never checked back against the image. Worse, `05.25.20`,
`11.03.20`, `UBI BENE IBI PATRIA`, `BREATHE` and `CHR` were each measured and written
down elsewhere in this tree -- premise_audit.md, even_slot_rules.py, slot20.py,
seal_ring.py, three_object_measurement.md, REPORT 9 -- and none of them ever reached the
brainwallet corpus. Nothing there was unknowable. The corpus simply never heard about
it. See REPORT 1.8.

This is to the corpus what selftest_gate.sh is to the binary, and it is built the same
way: it RE-PROVES the property rather than trusting a timestamp, and it keys its cached
pass on the CONTENT of both sides, so any edit to either invalidates it automatically
with no edit to any script.

THE TWO SIDES, deliberately independent:

  census   census_crops.DRAWN -- every string this project has measured as painted on
           the image, with its box and the file the measurement lives in. Read by
           STATIC PARSE (ast), never imported: census_crops.py loads the image and
           writes crops at import, and a gate must not depend on that, nor be
           foolable by it.

  corpus   brain_image_corpus.build(MAXIMAL) -- not the source text, the strings the
           corpus ACTUALLY GENERATES, under the union of all 64 readings 2.12's
           description admits. Checking the source would only prove that two files
           contain the same characters; checking the generated set proves that the
           strings will really be hashed. The source is COMPILED AND EXECUTED, never
           imported, so the bytes that were hashed are the bytes that ran -- a cached
           .pyc is validated on (mtime, size) and a size-preserving edit inside one
           second can be served stale.

The long canvas texts are written out separately in both files on purpose. A
disagreement between them is a finding, not a merge conflict.

    python3 -I corpus_gate.py           # gate: exit 0 pass, 1 refuse
    python3 -I corpus_gate.py --verbose # list every element and its verdict
    python3 -I corpus_gate.py --force   # ignore the cached pass, re-prove from scratch

Exit codes:  0 pass   1 REFUSE (a measured element is absent or differs)   2 gate error
"""
import ast
import hashlib
import io
import os
import re
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
STAMP = os.path.join(HERE, "corpus_gate_stamp.txt")
WS = re.compile(r"\s+", re.UNICODE)


def say(msg):
    print(msg)
    sys.stdout.flush()


# ----------------------------------------------------------------- census side
def census_drawn(path):
    """Statically extract census_crops.DRAWN. No import, no pixels, no side effects."""
    src = io.open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    consts, drawn = {}, None
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        name = getattr(node.targets[0], "id", None)
        if name is None:
            continue
        if name == "DRAWN":
            drawn = node.value
            continue
        try:
            consts[name] = ast.literal_eval(node.value)
        except ValueError:
            pass
    if drawn is None:
        raise SystemExit("gate error: census_crops.py has no DRAWN list")

    def resolve(n):
        if isinstance(n, ast.Name):
            if n.id not in consts:
                raise SystemExit("gate error: DRAWN references unknown name %r" % n.id)
            return consts[n.id]
        return ast.literal_eval(n)

    out = []
    for item in drawn.elts:
        label, text, box, status, ref = item.elts
        out.append((ast.literal_eval(label), resolve(text), ast.literal_eval(box),
                    ast.literal_eval(status), ast.literal_eval(ref)))
    return out, src


# ----------------------------------------------------------------- corpus side
def corpus_strings(src, path):
    """The strings the corpus actually generates, under the maximal reading.

    The source TEXT is compiled and executed in a fresh namespace rather than imported.
    This is not fussiness. CPython validates a cached .pyc on (mtime, size), so a
    size-preserving edit made inside the same mtime second -- `caccabus` -> `caccobus`
    is exactly that -- can be served from stale bytecode. A gate that imports could then
    hash the NEW source for its key, decide the cache is invalid, and still reconcile
    against the OLD code. Executing the bytes we hashed makes the thing proved and the
    thing measured the same object, which is the whole point of a gate.
    """
    ns = {"__name__": "_corpus_under_gate", "__file__": path, "__builtins__": __builtins__}
    exec(compile(src, path, "exec"), ns)
    groups, _ = ns["build"](ns["MAXIMAL"])
    return set().union(*groups.values()) if groups else set()


# ----------------------------------------------------------------------- gate
def main(argv):
    verbose = "--verbose" in argv
    force = "--force" in argv

    census_path = os.path.join(HERE, "census_crops.py")
    corpus_path = os.path.join(HERE, "brain_image_corpus.py")
    for p in (census_path, corpus_path):
        if not os.path.exists(p):
            say("GATE ERROR: %s is missing" % p)
            return 2

    drawn, census_src = census_drawn(census_path)
    corpus_src = io.open(corpus_path, encoding="utf-8").read()

    # Key on the content of BOTH sides. A stamp can go stale silently; a hash cannot.
    key = hashlib.sha256()
    key.update(hashlib.sha256(census_src.encode("utf-8")).digest())
    key.update(hashlib.sha256(corpus_src.encode("utf-8")).digest())
    key = key.hexdigest()

    if not force and os.path.exists(STAMP):
        for line in io.open(STAMP, encoding="utf-8"):
            if line.strip() == "key " + key:
                say("GATE PASS (cached): %d measured elements, census+corpus unchanged"
                    % len(drawn))
                return 0

    keys = corpus_strings(corpus_src, corpus_path)
    if not keys:
        say("GATE REFUSE: the corpus generated no strings at all")
        return 1

    # Match the way the corpus itself stores strings: variants() collapses whitespace.
    missing, rows = [], []
    for label, text, box, status, ref in drawn:
        joined = WS.sub(" ", text).strip()
        ok = joined in keys
        rows.append((ok, label, joined, status, ref))
        if not ok:
            missing.append((label, joined, box, status, ref))

    if verbose:
        say("  %-6s %-40s %-14s %s" % ("state", "element", "status", "string"))
        for ok, label, joined, status, ref in rows:
            say("  %-6s %-40s %-14s %s"
                % ("ok" if ok else "ABSENT", label[:40], status,
                   (joined[:70] + ("..." if len(joined) > 70 else ""))))

    if missing:
        say("")
        say("GATE REFUSE: %d of %d measured canvas elements are NOT in the corpus."
            % (len(missing), len(drawn)))
        for label, joined, box, status, ref in missing:
            say("  absent: %-38s [%s]  x%d y%d w%d h%d  (%s)"
                % (label, status, box[0], box[1], box[2], box[3], ref))
        say("")
        say("A brainwallet has no checksum, so a string that is not in the corpus is")
        say("simply never hashed: the run would return a negative for text that is not")
        say("on the canvas, and the canvas string would stay untested in every casing.")
        say("Add each string to brain_image_corpus.py, or -- if the census is what is")
        say("wrong -- correct census_crops.DRAWN and say so with a dated letterform")
        say("re-read. Do NOT run the corpus past this gate. See REPORT 1.8.")
        return 1

    with io.open(STAMP, "w", encoding="utf-8") as f:
        f.write("key %s\n" % key)
        f.write("census  %s  sha256 %s\n"
                % (census_path, hashlib.sha256(census_src.encode("utf-8")).hexdigest()))
        f.write("corpus  %s  sha256 %s\n"
                % (corpus_path, hashlib.sha256(corpus_src.encode("utf-8")).hexdigest()))
        f.write("elements %d\ncorpus_strings %d\n" % (len(drawn), len(keys)))
        import datetime
        f.write("passed %s\n" % datetime.datetime.now(datetime.timezone.utc)
                .strftime("%Y-%m-%dT%H:%M:%SZ"))
    say("GATE PASS: all %d measured canvas elements are present in the corpus "
        "(%d distinct strings, maximal reading)" % (len(drawn), len(keys)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except Exception as e:
        say("GATE ERROR: %s: %s" % (type(e).__name__, e))
        sys.exit(2)
