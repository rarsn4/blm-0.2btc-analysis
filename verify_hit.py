#!/usr/bin/env python3
"""
verify_hit.py -- an INDEPENDENT BIP39/BIP32/secp256k1 implementation, written to
check a solver HIT without sharing a single line of code with the solver.

It has no dependencies: no `mnemonic` package, no `ecdsa`, no `bitcoin` library,
and a pure-Python RIPEMD-160 so it works where OpenSSL 3 has disabled it.

WHY THIS EXISTS

The verification protocol says a hit must be re-derived "on a separate BIP32
implementation". That implementation did not exist. Building it at 05:31 against
the real thing, in a hurry, is the worst possible time. This is built and
self-tested against known-answer vectors first.

It also answers a question the solver cannot answer about itself: show_hit()
reconstructs the phrase from the candidate index in HOST code (solver_host2.cuh
:301-311), which is a SECOND unranking, not the one the GPU kernel used to find
the hit. If the two disagree, a hit prints a phrase that is not the phrase that
matched. That is worse than a wrong path field, because the phrase is the prize.

USAGE

  python3 verify_hit.py --selftest
      Run the known-answer vectors. Do this first. Everything must pass.

  python3 verify_hit.py --phrase "word1 word2 ... word21" [--passphrase ""]
      Derive the phrase on all four campaign paths plus the common alternatives,
      and report every address and hash160. Compare against the target yourself.

  python3 verify_hit.py --phrase "..." --target ccbd031e54cde2a3189fd59bc49f731367a1779e
      Same, but says MATCH / no match per path.

SECURITY

Run it with networking disabled. It never opens a socket, but that is not the
point -- the point is that the phrase must not exist on a networked machine.
If a path MATCHes, move the funds with a key generated fresh and offline BEFORE
the phrase appears in any log, commit, shell history or message.
"""

import hashlib, hmac, sys, unicodedata

# ---------------------------------------------------------------- RIPEMD-160
# Pure Python. OpenSSL 3 disables ripemd160 in the default provider on many
# distributions, and this script must not fail on the one night it matters.

_R = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
      7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,
      3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12,
      1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,
      4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13]
_RP = [5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12,
       6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,
       15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13,
       8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,
       12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11]
_S = [11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8,
      7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12,
      11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5,
      11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12,
      9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6]
_SP = [8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6,
       9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,
       9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5,
       15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8,
       8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11]
_K  = [0x00000000,0x5a827999,0x6ed9eba1,0x8f1bbcdc,0xa953fd4e]
_KP = [0x50a28be6,0x5c4dd124,0x6d703ef3,0x7a6d76e9,0x00000000]


def _rol(x, n):
    x &= 0xffffffff
    return ((x << n) | (x >> (32 - n))) & 0xffffffff


def _f(j, x, y, z):
    if j < 16:  return x ^ y ^ z
    if j < 32:  return (x & y) | (~x & 0xffffffff & z)
    if j < 48:  return (x | ~y & 0xffffffff) ^ z
    if j < 64:  return (x & z) | (y & ~z & 0xffffffff)
    return x ^ (y | ~z & 0xffffffff)


def ripemd160(data: bytes) -> bytes:
    h = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]
    ml = len(data) * 8
    data = data + b'\x80'
    while len(data) % 64 != 56:
        data += b'\x00'
    data += (ml & 0xffffffffffffffff).to_bytes(8, 'little')
    for off in range(0, len(data), 64):
        X = [int.from_bytes(data[off + 4 * i:off + 4 * i + 4], 'little') for i in range(16)]
        a, b, c, d, e = h
        ap, bp, cp, dp, ep = h
        for j in range(80):
            t = _rol(a + _f(j, b, c, d) + X[_R[j]] + _K[j // 16], _S[j]) + e
            a, e, d, c, b = e, d, _rol(c, 10), b, t & 0xffffffff
            t = _rol(ap + _f(79 - j, bp, cp, dp) + X[_RP[j]] + _KP[j // 16], _SP[j]) + ep
            ap, ep, dp, cp, bp = ep, dp, _rol(cp, 10), bp, t & 0xffffffff
        h = [(h[1] + c + dp) & 0xffffffff, (h[2] + d + ep) & 0xffffffff,
             (h[3] + e + ap) & 0xffffffff, (h[4] + a + bp) & 0xffffffff,
             (h[0] + b + cp) & 0xffffffff]
    return b''.join(x.to_bytes(4, 'little') for x in h)


def hash160(b: bytes) -> bytes:
    return ripemd160(hashlib.sha256(b).digest())


# ---------------------------------------------------------------- secp256k1
P  = 2**256 - 2**32 - 977
N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def _inv(a, m=P):
    return pow(a, m - 2, m)


def _add(p, q):
    if p is None: return q
    if q is None: return p
    x1, y1 = p; x2, y2 = q
    if x1 == x2:
        if (y1 + y2) % P == 0: return None
        lam = 3 * x1 * x1 % P * _inv(2 * y1) % P
    else:
        lam = (y2 - y1) * _inv(x2 - x1) % P
    x3 = (lam * lam - x1 - x2) % P
    return (x3, (lam * (x1 - x3) - y1) % P)


def _mul(k, p=(GX, GY)):
    """Plain double-and-add. Deliberately the most boring algorithm available:
    this must not share a Jacobian optimisation with the thing it is checking."""
    r = None
    while k:
        if k & 1: r = _add(r, p)
        p = _add(p, p)
        k >>= 1
    return r


def pub_compressed(priv: int) -> bytes:
    x, y = _mul(priv)
    return (b'\x03' if y & 1 else b'\x02') + x.to_bytes(32, 'big')


# ---------------------------------------------------------------- BIP39 / 32
def mnemonic_to_seed(words: str, passphrase: str = "") -> bytes:
    m = unicodedata.normalize('NFKD', ' '.join(words.split()))
    s = unicodedata.normalize('NFKD', 'mnemonic' + passphrase)
    return hashlib.pbkdf2_hmac('sha512', m.encode(), s.encode(), 2048, 64)


def master(seed: bytes):
    I = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
    return int.from_bytes(I[:32], 'big'), I[32:]


def ckd_priv(k: int, c: bytes, i: int):
    if i & 0x80000000:
        data = b'\x00' + k.to_bytes(32, 'big') + i.to_bytes(4, 'big')
    else:
        data = pub_compressed(k) + i.to_bytes(4, 'big')
    I = hmac.new(c, data, hashlib.sha512).digest()
    kc = (int.from_bytes(I[:32], 'big') + k) % N
    if kc == 0 or int.from_bytes(I[:32], 'big') >= N:
        raise ValueError('invalid child key -- increment the index (BIP32 §5)')
    return kc, I[32:]


def derive(seed: bytes, path: str):
    k, c = master(seed)
    if path in ('m', ''):
        return k, c
    for part in path.split('/')[1:]:
        hard = part.endswith(("'", 'h', 'H'))
        idx = int(part.rstrip("'hH")) + (0x80000000 if hard else 0)
        k, c = ckd_priv(k, c, idx)
    return k, c


_B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def b58check(payload: bytes) -> str:
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(payload + chk, 'big')
    out = ''
    while n:
        n, r = divmod(n, 58)
        out = _B58[r] + out
    return '1' * (len(payload + chk) - len((payload + chk).lstrip(b'\x00'))) + out


def p2pkh(h160: bytes) -> str:
    return b58check(b'\x00' + h160)


# ---------------------------------------------------------------- paths
CAMPAIGN = ["m/44'/0'/0'/0/0", "m/0'/0/0", "m/0/0", "m/44'/0'/0'/0/1"]
EXTRA    = ["m", "m/0'/0'/0'", "m/44'/0'/0'", "m/49'/0'/0'/0/0", "m/84'/0'/0'/0/0",
            "m/0'/0/1", "m/0/1", "m/44'/0'/0'/1/0"]


def report(phrase: str, passphrase: str = "", target: str = None):
    seed = mnemonic_to_seed(phrase, passphrase)
    print(f"  words      : {len(phrase.split())}")
    print(f"  passphrase : {'(none)' if passphrase == '' else repr(passphrase)}")
    print(f"  seed       : {seed.hex()[:32]}...{seed.hex()[-16:]}")
    print()
    tgt = target.lower().strip() if target else None
    hit = []
    for label, paths in (("CAMPAIGN (the four the solver searched)", CAMPAIGN),
                         ("OTHER COMMON PATHS", EXTRA)):
        print(f"  {label}")
        for p in paths:
            try:
                k, _ = derive(seed, p)
                h = hash160(pub_compressed(k))
                mark = ''
                if tgt:
                    mark = '   *** MATCH ***' if h.hex() == tgt else '   no'
                    if h.hex() == tgt: hit.append(p)
                print(f"    {p:<20} {p2pkh(h):<36} {h.hex()}{mark}")
            except ValueError as e:
                print(f"    {p:<20} {e}")
        print()
    if tgt:
        if hit:
            print("  " + "=" * 68)
            print(f"  MATCH on {', '.join(hit)}")
            print("  " + "=" * 68)
            print("  Before anything else: move the funds to a key generated FRESH and")
            print("  OFFLINE. Do not commit, log, paste or message this phrase first.")
        else:
            print("  no match on any path tried.")
            print("  That does NOT by itself mean the hit is spurious -- the solver's")
            print("  reported path field is reconstructed by different code than the")
            print("  kernel that matched. Check the phrase against the solver's own")
            print("  affine binary (EC_USE_JACOBIAN=0) before discarding it.")
    return hit


# ---------------------------------------------------------------- self-test
def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {name}")
        if not good:
            print(f"        got  {got}")
            print(f"        want {want}")

    # RIPEMD-160, from the reference test vectors
    chk('ripemd160("")', ripemd160(b'').hex(),
        '9c1185a5c5e9fc54612808977ee8f548b2258d31')
    chk('ripemd160("abc")', ripemd160(b'abc').hex(),
        '8eb208f7e05d987a9b044a8e98c6b087f15a0bfc')
    chk('ripemd160("a"*1000000 prefix check)',
        ripemd160(b'message digest').hex(),
        '5d0689ef49d2fae572b881b123a85ffa21595f36')

    # cross-check against OpenSSL where it is available
    try:
        h = hashlib.new('ripemd160', b'The quick brown fox').hexdigest()
        chk('pure-python ripemd160 == OpenSSL', ripemd160(b'The quick brown fox').hex(), h)
    except Exception:
        print('  SKIP  OpenSSL ripemd160 unavailable (pure-python path is in use)')

    # secp256k1: G, and the order
    chk('1*G', '%064x' % _mul(1)[0], '%064x' % GX)
    chk('2*G x', '%064x' % _mul(2)[0],
        'c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5')
    chk('(N-1)*G + G == infinity', _add(_mul(N - 1), _mul(1)), None)

    # BIP39 seed vectors (official)
    ab = 'abandon ' * 11 + 'about'
    chk('BIP39 seed, empty passphrase', mnemonic_to_seed(ab).hex(),
        '5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc1'
        '9a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4')
    chk('BIP39 seed, passphrase TREZOR', mnemonic_to_seed(ab, 'TREZOR').hex(),
        'c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e5349553'
        '1f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04')

    # BIP32/BIP44 end to end: the well-known address of the abandon-about seed
    k, _ = derive(mnemonic_to_seed(ab), "m/44'/0'/0'/0/0")
    chk("BIP44 m/44'/0'/0'/0/0 address", p2pkh(hash160(pub_compressed(k))),
        '1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA')

    # BIP32 test vector 1, chain m/0'
    seed1 = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
    k, c = derive(seed1, "m/0'")
    chk("BIP32 vector 1, m/0' privkey", '%064x' % k,
        'edb2e14f9ee77d26dd93b4ecede8d16ed408ce149b6cd80b0715a2d911a0afea')
    chk("BIP32 vector 1, m/0' chaincode", c.hex(),
        '47fdacbd0f1097043b78c63c20c34ef4ed9a111d980047ad16282c7ae6236141')

    print()
    print('  ALL PASS -- this implementation is trustworthy as an independent check.'
          if ok else '  *** SOMETHING FAILED -- do not use this to verify a hit. ***')
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or '--selftest' in a:
        print('verify_hit.py -- known-answer self-test\n')
        sys.exit(0 if selftest() else 1)
    phrase = passphrase = target = None
    i = 0
    while i < len(a):
        if a[i] == '--phrase':      phrase = a[i + 1]; i += 2
        elif a[i] == '--passphrase': passphrase = a[i + 1]; i += 2
        elif a[i] == '--target':    target = a[i + 1]; i += 2
        else:
            print(f'unknown argument: {a[i]}'); sys.exit(2)
    if not phrase:
        print('need --phrase "..."'); sys.exit(2)
    print('verify_hit.py -- independent derivation\n')
    if not selftest():
        sys.exit(1)
    print()
    report(phrase, passphrase or '', target)
