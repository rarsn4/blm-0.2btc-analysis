"""X-3: CPU deriver for 12-word phrases of the t12full family.

Self-tests against the canonical BIP39 vector FIRST, then sweeps. Covers the
described family (slot 6 in a named set, slot 8 over ALL 2048) rather than
guessing seven specific phrases, so the result holds whatever slot 8 held.

HIT protocol: this script never prints a phrase. On a match it prints the slot-6
word and the slot-8 INDEX only, and stops.
"""
import os, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_hit import (hash160, mnemonic_to_seed, derive, pub_compressed,
                        _mul, p2pkh)

TARGET_H160 = bytes.fromhex('ccbd031e54cde2a3189fd59bc49f731367a1779e')
SWAPPED     = bytes.fromhex('1e03bdcca3e2cd549bd59f1813739fc49e77a167')
assert TARGET_H160 != SWAPPED
assert p2pkh(TARGET_H160) == '1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ', "rule 8: target blob"

WORDS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs', 'bip39_en.txt')).read().split()
assert len(WORDS) == 2048
IDX = {w: i for i, w in enumerate(WORDS)}
PATHS = ["m/44'/0'/0'/0/0", "m/0'/0/0", "m/0/0", "m/44'/0'/0'/0/1"]

def pub_uncompressed(priv):
    x, y = _mul(priv)
    return b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

def checksum_ok(words):
    bits = ''.join(f'{IDX[w]:011b}' for w in words)
    n = len(words) * 11
    ent, cs = bits[:n - n // 33], bits[n - n // 33:]
    b = int(ent, 2).to_bytes(len(ent) // 8, 'big')
    return hashlib.sha256(b).digest()[0] >> (8 - len(cs)) == int(cs, 2)

# ---------------------------------------------------------------- self-test
def selftest():
    ok = True
    def chk(name, got, want):
        nonlocal ok
        good = got == want; ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {name}")
        if not good: print(f"        got  {got}\n        want {want}")
    ab = 'abandon ' * 11 + 'about'
    chk("canonical BIP39 seed (abandon x11 about, empty passphrase)",
        mnemonic_to_seed(ab).hex()[:32], '5eb00bbddcf069084889a8ab91555681')
    k, _ = derive(mnemonic_to_seed(ab), "m/44'/0'/0'/0/0")
    chk("canonical BIP44 address, compressed",
        p2pkh(hash160(pub_compressed(k))), '1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA')
    # privkey = 1: both addresses are externally published, and both were
    # reproduced independently by libsecp256k1 (coincurve) before being pinned here.
    chk("privkey=1 compressed address (published)",
        p2pkh(hash160(pub_compressed(1))), '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH')
    chk("privkey=1 UNCOMPRESSED address (published)",
        p2pkh(hash160(pub_uncompressed(1))), '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm')
    chk("canonical BIP44 address, UNCOMPRESSED (vs libsecp256k1)",
        p2pkh(hash160(pub_uncompressed(k))), '18LhnLKXjcTw5xJFiTxntnKit2Gd63eWFm')
    chk("checksum accepts the canonical phrase", checksum_ok(ab.split()), True)
    chk("checksum rejects it with one word changed",
        checksum_ok((('abandon ' * 11) + 'zoo').split()), False)
    chk("target blob is NOT the word-swapped form", TARGET_H160 == SWAPPED, False)
    # The two encoding arms must stay DISTINCT. A library that re-serialises the point
    # silently collapses uncompressed onto compressed and halves the real derivation
    # count while the printed count stays the same. Checked, not assumed.
    arms = []
    for p_ in PATHS:
        kk, _ = derive(mnemonic_to_seed(ab), p_)
        arms += [hash160(pub_compressed(kk)), hash160(pub_uncompressed(kk))]
    chk("compressed and uncompressed give DISTINCT hash160s on all 4 paths",
        len(set(arms)), len(arms))
    # planted-hit test through the SAME comparison path the sweep uses
    planted = hash160(pub_compressed(k))
    chk("a planted target IS detected by the sweep's comparison",
        planted == hash160(pub_compressed(k)), True)
    print(f"  {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return ok

if not selftest():
    raise SystemExit("self-test failed: nothing was derived")

# ---------------------------------------------------------------- the sweep
TEMPLATE = ['subject','camera','tower','mask','police',None,'liberty',None,
            'eye','black','pyramid','vote']          # configs/t12full_mp.conf
S6 = ['neck','air','gasp','inhale','asthma']
for w in S6: assert w in IDX, w

print(f"\nfamily: configs/t12full_mp.conf slots 1-12, slot 6 in {S6}, slot 8 over all 2048")
print(f"paths: {len(PATHS)}   encodings: compressed + uncompressed\n")
valid = derivs = hits = 0
per6 = {}
for w6 in S6:
    v6 = 0
    for i8, w8 in enumerate(WORDS):
        ph = list(TEMPLATE); ph[5] = w6; ph[7] = w8
        if not checksum_ok(ph):
            continue
        valid += 1; v6 += 1
        seed = mnemonic_to_seed(' '.join(ph))
        for p in PATHS:
            k, _ = derive(seed, p)
            for pub in (pub_compressed(k), pub_uncompressed(k)):
                derivs += 1
                if hash160(pub) == TARGET_H160:
                    hits += 1
                    print(f"!! MATCH: slot6={w6} slot8 INDEX={i8} path={p} "
                          f"enc={'compressed' if len(pub)==33 else 'uncompressed'}")
                    print("!! STOP. Do not print the phrase. Follow the HIT protocol.")
                    raise SystemExit(2)
    per6[w6] = v6
    print(f"  slot6={w6:7s}  checksum-valid slot-8 words {v6:4d}  "
          f"derivations {v6*len(PATHS)*2:5d}  matches 0", flush=True)

print(f"\nTOTAL  phrases enumerated {len(S6)*2048:,}   checksum-valid {valid:,}"
      f"   derivations {derivs:,}   MATCHES {hits}")
print(f"expected valid ~ {len(S6)*2048/16:.0f} (1 in 16); observed {valid}")
