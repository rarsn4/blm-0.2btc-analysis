#!/usr/bin/env python3
"""Known-answer + planted-hit self-test for the image-text brainwallet derivation.

A negative is only worth as much as the machine that produced it. REPORT 1.7 was the
binary running unverified for five weeks; this is the same discipline applied to the
Python derivation path, and it runs before the corpus does.

  1  the canonical public brainwallet example derives to its PUBLISHED addresses,
     compressed and uncompressed -- an external oracle, not a self-consistency check
  2  the hybrid encoding is a well-formed 0x06/0x07 form of the same point
  3  a PLANTED string is found through the same comparison the real run uses

    python3 -I brain_corpus_selftest.py     # exit 0 pass, 1 fail
"""
import hashlib
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_hit as V

# The canonical example and its published addresses. Public, well-known, and not this
# project's own output -- which is what makes it an oracle.
VECTOR = ("correct horse battery staple",
          "c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a",
          "1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T",     # uncompressed
          "1C7zdTfnkzmr13HfA2vNm5SJYRK6nEKyq8")     # compressed


def pubkeys(kd):
    x, y = V._mul(int.from_bytes(kd, "big"))
    xb, yb = x.to_bytes(32, "big"), y.to_bytes(32, "big")
    u = b"\x04" + xb + yb
    return ((b"\x03" if y & 1 else b"\x02") + xb, u,
            bytes([0x06 | (y & 1)]) + xb + yb)


def h160(b):
    return hashlib.new("ripemd160", hashlib.sha256(b).digest()).digest()


def main():
    ok = []
    s, want_priv, want_u, want_c = VECTOR
    kd = hashlib.sha256(s.encode("utf-8")).digest()
    ok.append(("sha256 of the canonical example", kd.hex() == want_priv))
    c, u, hy = pubkeys(kd)
    ok.append(("uncompressed address matches the published value",
               V.p2pkh(h160(u)) == want_u))
    ok.append(("compressed address matches the published value",
               V.p2pkh(h160(c)) == want_c))
    ok.append(("hybrid encoding is a well-formed 0x06/0x07 of the same point",
               hy[0] in (6, 7) and len(hy) == 65 and hy[1:] == u[1:]))

    plant = "blm-corpus-planted-selftest"
    target = h160(pubkeys(hashlib.sha256(plant.encode("utf-8")).digest())[0])
    found = False
    for st in ("not it", plant, "nor this"):
        d = hashlib.sha256(st.encode("utf-8")).digest()
        for k in (d, hashlib.sha256(d).digest()):
            for pub in pubkeys(k):
                if h160(pub) == target:
                    found = True
    ok.append(("a planted hit is found through the real comparison", found))

    for name, good in ok:
        print("  %s  %s" % ("PASS" if good else "FAIL", name))
    bad = [n for n, g in ok if not g]
    if bad:
        print("\n  *** %d FAILURE(S) -- do not run the corpus ***" % len(bad))
        return 1
    print("\n  ALL PASS -- the derivation path is verified against an external oracle.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
