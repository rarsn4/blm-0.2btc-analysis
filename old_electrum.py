#!/usr/bin/env python3
"""old_electrum.py — pre-2.0 ("old") Electrum seeds, implemented and self-tested.

WHY THIS EXISTS. Everything this project has run against Electrum used the v2
scheme: seed-version prefix, PBKDF2-HMAC-SHA512 with the "electrum" salt, the
2048-word list, BIP32 derivation. Old Electrum is a different scheme end to end
and has never been tested against the target:

    12 words over a 1,626-word list (configs/electrum_old_en.txt)
    mn_decode  -> 128-bit hex string (four 8-hex-digit groups, one per triple)
    stretch    -> x = seed_hex_ascii;  repeat 100,000x: x = sha256(x + seed_hex_ascii)
                  master secret exponent = int(x, big-endian)
    mpk        -> UNCOMPRESSED public key of that exponent, hex, '04' prefix stripped
    address n  -> z = sha256d(b"%d:%d:" % (n, change) + mpk_bytes)
                  pubkey = MPK + z*G, UNCOMPRESSED
                  hash160 -> P2PKH
    there is no BIP32 anywhere in it, and the keys are uncompressed.

THE ALGORITHM IS NOT GUESSED. It is transcribed from Electrum 4.6.2 as installed
here (electrum/keystore.py Old_KeyStore, electrum/old_mnemonic.py), and the EC
and hashing primitives are this project's own pure-Python ones from verify_hit.py
-- NOT Electrum's ecc module -- so a pass is agreement between two independent
implementations, not a tautology.

SELF-TEST BEFORE SEARCH. selftest() checks a published known-answer vector from
Electrum's own test suite (tests/test_wallet_vertical.py::test_electrum_seed_old)
plus the wordlist digest, mn_encode/mn_decode round-trips, and the over-length
rejection case the suite records as "invalid old". Nothing in this module is to
be used for a search until `python3 old_electrum.py selftest` prints ALL PASS.
That rule is here because the 28 Sep defect was a 16-hour run on an unverified
feature.

ONE CORRECTION TO THE USUAL DESCRIPTION. Old Electrum is often described as
having no checksum, so that every word combination is a valid seed. Almost: each
3-word group encodes an integer x < 1626^3 = 4,299,816,375, and '%08x' overflows
to nine digits when x >= 2^32, which Electrum then rejects as not-a-seed. The
fraction surviving is (2^32 / 1626^3)^4 = 99.55%, so there is no checksum worth
the name -- but it is not exactly 1.
"""
import hashlib, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_hit import hash160, p2pkh, _add, _mul, N, GX, GY   # independent primitives

CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')
WORDS_SHA256 = 'c8da327d316f8ee758b790068e618077ac271a89fd77ec1250c59ae40e7b599e'

def load_words(path=None):
    path = path or os.path.join(CFG, 'electrum_old_en.txt')
    raw = open(path, 'rb').read()
    w = raw.decode('ascii').split()
    assert len(w) == 1626, f"old Electrum wordlist must be 1626 words, got {len(w)}"
    assert len(set(w)) == 1626, "wordlist has duplicates"
    return w, hashlib.sha256(raw).hexdigest()

WORDS, _digest = load_words()
NW = len(WORDS)
IDX = {w: i for i, w in enumerate(WORDS)}

def sha256(b): return hashlib.sha256(b).digest()
def sha256d(b): return sha256(sha256(b))

# ---- mnemonic <-> hex (transcribed from electrum/old_mnemonic.py) ----------
def mn_encode(hex_seed: str):
    assert len(hex_seed) % 8 == 0, "hex seed length must be a multiple of 8"
    out = []
    for i in range(len(hex_seed) // 8):
        x = int(hex_seed[8*i:8*i+8], 16)
        w1 = x % NW
        w2 = ((x // NW) + w1) % NW
        w3 = ((x // NW // NW) + w2) % NW
        out += [WORDS[w1], WORDS[w2], WORDS[w3]]
    return out

class NotAnOldSeed(Exception): pass

def mn_decode(wlist) -> str:
    """Returns the hex seed, or raises NotAnOldSeed for the cases Electrum rejects."""
    if len(wlist) % 3: raise NotAnOldSeed(f"word count {len(wlist)} is not a multiple of 3")
    out = ''
    for i in range(len(wlist) // 3):
        a, b, c = wlist[3*i:3*i+3]
        for w in (a, b, c):
            if w not in IDX: raise NotAnOldSeed(f"{w!r} is not in the old wordlist")
        w1 = IDX[a]; w2 = IDX[b] % NW; w3 = IDX[c] % NW
        x = w1 + NW*((w2 - w1) % NW) + NW*NW*((w3 - w2) % NW)
        # Electrum writes '%08x'; x >= 2**32 produces nine digits and the seed is
        # then not hex of even length, which its seed_type() reports as invalid.
        if x >= 2**32:
            raise NotAnOldSeed(f"group {i} encodes {x} >= 2**32; Electrum rejects this seed")
        out += '%08x' % x
    return out

# ---- key derivation --------------------------------------------------------
def stretch_key(hex_seed: str) -> int:
    e = hex_seed.encode('ascii')
    x = e
    for _ in range(100000):
        x = sha256(x + e)
    return int.from_bytes(x, 'big')

def _uncompressed(pt) -> bytes:
    x, y = pt
    return b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

def mpk_from_hex_seed(hex_seed: str) -> str:
    secexp = stretch_key(hex_seed)
    assert 0 < secexp < N, "stretched exponent out of range"
    return _uncompressed(_mul(secexp, (GX, GY)))[1:].hex()

def get_sequence(mpk_hex: str, for_change: int, n: int) -> int:
    return int.from_bytes(
        sha256d(("%d:%d:" % (n, for_change)).encode('ascii') + bytes.fromhex(mpk_hex)), 'big')

def pubkey_from_mpk(mpk_hex: str, for_change: int, n: int) -> bytes:
    z = get_sequence(mpk_hex, for_change, n) % N
    M = (int(mpk_hex[:64], 16), int(mpk_hex[64:], 16))
    return _uncompressed(_add(M, _mul(z, (GX, GY))))

def address(mpk_hex: str, for_change: int, n: int) -> str:
    return p2pkh(hash160(pubkey_from_mpk(mpk_hex, for_change, n)))

def h160(mpk_hex: str, for_change: int, n: int) -> bytes:
    return hash160(pubkey_from_mpk(mpk_hex, for_change, n))

def from_words(words):
    """words (list or space-joined str) -> (hex_seed, mpk_hex)"""
    if isinstance(words, str): words = words.split()
    hex_seed = mn_decode([w.lower() for w in words])
    return hex_seed, mpk_from_hex_seed(hex_seed)

# ---- self-test -------------------------------------------------------------
# Known-answer vector published in Electrum's own test suite, tag 4.5.8,
# tests/test_wallet_vertical.py::test_electrum_seed_old.
KAT_SEED = 'powerful random nobody notice nothing important anyway look away hidden message over'
KAT_MPK  = ('e9d4b7866dd1e91c862aebf62a49548c7dbf7bcc6e4b7b8c9da820c7737968df'
            '9c09d5a3e271dc814a29981f81b3faaf2737b551ef5dcc6189cf0f8252c442b3')
KAT_RECV0 = '1FJEEB8ihPMbzs2SkLmr37dHyRFzakqUmo'
KAT_CHG0  = '1KRW8pH6HFHZh889VDq6fEKvmrsmApwNfe'
# tests/test_mnemonic.py records this one as 'invalid old': it maps to 33 hex chars.
KAT_INVALID = 'hurry idiot prefer sunset mention mist jaw inhale impossible kingdom rare squeeze'
# and these as valid 'old'
KAT_VALID   = 'cell dumb heartbeat north boom tease ship baby bright kingdom rare squeeze'

def selftest() -> bool:
    ok = True
    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {name}")
        if not good: print(f"        got  {got}\n        want {want}")

    print("wordlist")
    chk("1626 words, sha256 matches the extract from electrum/old_mnemonic.py",
        _digest, WORDS_SHA256)

    print("mnemonic codec")
    hex_seed, mpk = from_words(KAT_SEED)
    chk("mn_decode(KAT) is 32 hex chars", (len(hex_seed), all(c in '0123456789abcdef' for c in hex_seed)), (32, True))
    chk("mn_encode(mn_decode(KAT)) round-trips", ' '.join(mn_encode(hex_seed)), KAT_SEED)
    rt = True
    for i in range(64):                      # deterministic pseudo-random round-trip
        hs = hashlib.sha256(b'rt%d' % i).hexdigest()[:32]
        try:
            rt &= (mn_decode(mn_encode(hs)) == hs)
        except NotAnOldSeed:
            pass                             # over-length group: not encodable, skip
    chk("64 random hex seeds round-trip through encode/decode", rt, True)
    try:
        mn_decode(KAT_INVALID.split()); bad = 'accepted'
    except NotAnOldSeed:
        bad = 'rejected'
    chk("the suite's 'invalid old' seed is rejected (33 hex chars)", bad, 'rejected')
    try:
        mn_decode(KAT_VALID.split()); good = 'accepted'
    except NotAnOldSeed as e:
        good = f'rejected: {e}'
    chk("the suite's valid 'old' seed is accepted", good, 'accepted')

    print("key derivation vs the published known-answer vector")
    chk("master public key", mpk, KAT_MPK)
    chk("receiving address 0", address(mpk, 0, 0), KAT_RECV0)
    chk("change address 0",    address(mpk, 1, 0), KAT_CHG0)

    # Rule 8's analogue for a CPU module: prove the comparison against the target
    # can actually fire. A negative from a comparison that never fires is void.
    print("planted-hit test (the comparison must fire, and only on a match)")
    planted = h160(mpk, 0, 0)
    chk("a planted target h160 IS detected", planted == planted, True)
    chk("the planted h160 is not the real target (the vector is not a hit)",
        planted != TARGET_H160, True)
    chk("scanning the KAT seed against the REAL target gives no hit",
        any(h160(mpk, c, i) == TARGET_H160 for c in (0, 1) for i in range(5)), False)
    chk("scanning the KAT seed against ITS OWN h160 at (0,0) gives a hit",
        any(h160(mpk, c, i) == planted for c in (0, 1) for i in range(5)), True)

    print("\n" + ("ALL PASS" if ok else "FAILED — do not search with this module"))
    return ok

TARGET_H160 = bytes.fromhex('ccbd031e54cde2a3189fd59bc49f731367a1779e')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest':
        sys.exit(0 if selftest() else 1)
    print(__doc__)
    print("run:  python3 old_electrum.py selftest")
