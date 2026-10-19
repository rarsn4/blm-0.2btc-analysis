#!/usr/bin/env python3
"""CPU passphrase sweep over existing configs, while the GPU runs the queue.

usage: nice python3 -I passphrase_cpu.py SOLVER_DIR small|el18|control [workers]

  small   : t12full_mp (BIP39, 8 passphrases) and el12 el13 el14 el16 el17 (Electrum, 9 passphrases)
  el18    : el18 (Electrum, 9 passphrases)
  control : planted positive controls through this same code path (targets computed by verify_hit.py)

Passphrases. BIP39 is case-sensitive: memo Memo MEMO CHaRLy Charly charly CHARLY JR (8). Real Electrum
lowercases the passphrase (normalize_text) while the solver does not, so Electrum gets those 8 as written
plus `jr` (9), which covers both behaviours.
Checks: BIP39 checksum / Electrum "Seed version" prefix 01 or 100 (the solver kernel's rule). Derivation
on the config's PATH lines; compressed, uncompressed and hybrid public keys, as the solver checks.
HIT RULE: prints counts only. On a match against the real target it prints the count and stops; no
phrase, index or passphrase is ever printed for the real target.
"""
import sys, os, hashlib, hmac, itertools, unicodedata, time
from multiprocessing import Pool
from cryptography.hazmat.primitives.asymmetric import ec

SOLVER = sys.argv[1]; MODE = sys.argv[2]; NW = int(sys.argv[3]) if len(sys.argv) > 3 else 12
WL = [w.strip() for w in open(os.path.join(SOLVER, 'bip39_en.txt'))]; IDX = {w: i for i, w in enumerate(WL)}
REAL = bytes.fromhex('ccbd031e54cde2a3189fd59bc49f731367a1779e')
PP_BIP39 = ['memo', 'Memo', 'MEMO', 'CHaRLy', 'Charly', 'charly', 'CHARLY', 'JR']
PP_EL = PP_BIP39 + ['jr']
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
CURVE = ec.SECP256K1()
SV = hmac.new(b'Seed version', digestmod=hashlib.sha512)

def conf(name):
    d = dict(paths=[], pool=[], slots={}, scheme='bip39')
    for line in open(os.path.join(SOLVER, name + '.conf')):
        t = line.split()
        if not t or t[0].startswith('#'): continue
        if t[0] == 'PATH': d['paths'].append(t[1])
        elif t[0] == 'POOL': d['pool'] += t[1:]
        elif t[0] == 'SLOT': d['slots'][int(t[1])] = t[2]
        elif t[0] == 'WORDS': d['words'] = int(t[1])
        elif t[0] == 'SCHEME': d['scheme'] = t[1]
    d['sets'] = [d['pool'] if v == '@POOL' else WL if v == '@FULL' else v.split('|')
                 for v in (d['slots'][i] for i in range(1, d['words'] + 1))]
    return d

def pubxy(k):
    n = ec.derive_private_key(k, CURVE).public_key().public_numbers(); return n.x, n.y

def ser(k):
    x, y = pubxy(k); return (b'\x03' if y & 1 else b'\x02') + x.to_bytes(32, 'big'), x, y

def h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()

def derive_all(seed, paths):
    """hash160s of the three encodings for every path, with shared-prefix caching"""
    I = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest(); cache = {'m': (int.from_bytes(I[:32], 'big'), I[32:])}
    pubs = {}
    def pub(key):
        if key not in pubs: pubs[key] = ser(cache[key][0])
        return pubs[key]
    out = []
    for p in paths:
        parts = p.split('/')[1:]; key = 'm'
        for part in parts:
            nk = key + '/' + part
            if nk not in cache:
                k, c = cache[key]; hard = part.endswith("'"); i = int(part.rstrip("'")) + (0x80000000 if hard else 0)
                data = (b'\x00' + k.to_bytes(32, 'big') if hard else pub(key)[0]) + i.to_bytes(4, 'big')
                J = hmac.new(c, data, hashlib.sha512).digest()
                cache[nk] = ((int.from_bytes(J[:32], 'big') + k) % N, J[32:])
            key = nk
        comp, x, y = pub(key)
        xy = x.to_bytes(32, 'big') + y.to_bytes(32, 'big')
        out += [h160(comp), h160(b'\x04' + xy), h160((b'\x07' if y & 1 else b'\x06') + xy)]
    return out

def bip39_ok(ws):
    nb = len(ws) * 11; cs = nb // 33; ent = nb - cs
    v = 0
    for w in ws: v = (v << 11) | IDX[w]
    e = (v >> cs).to_bytes(ent // 8, 'big')
    return hashlib.sha256(e).digest()[0] >> (8 - cs) == v & ((1 << cs) - 1)

def el_ok(m):
    h = SV.copy(); h.update(m.encode()); d = h.digest(); return d[0] == 0x01 or (d[0] == 0x10 and d[1] >> 4 == 0)

def task(args):
    """one slice: first open slot fixed to one value. Returns (candidates, survivors, derivations, real matches, planted hits)"""
    name, first_val, target = args
    d = conf(name); sets = list(d['sets']); open_i = [i for i, s in enumerate(sets) if len(s) > 1]
    sets[open_i[0]] = [first_val]
    elec = d['scheme'] == 'electrum'; pps = PP_EL if elec else PP_BIP39
    cand = surv = der = real = planted = 0
    for ws in itertools.product(*sets):
        cand += 1; m = ' '.join(ws)
        if not (el_ok(m) if elec else bip39_ok(ws)): continue
        surv += 1
        for pp in pps:
            salt = ('electrum' if elec else 'mnemonic') + pp
            seed = hashlib.pbkdf2_hmac('sha512', unicodedata.normalize('NFKD', m).encode(), unicodedata.normalize('NFKD', salt).encode(), 2048, 64)
            hs = derive_all(seed, d['paths']); der += 1
            real += sum(h == REAL for h in hs)
            if target is not None: planted += sum(h == target for h in hs)
    return cand, surv, der, real, planted

def run(name, target=None, only=None):
    d = conf(name); open_i = [i for i, s in enumerate(d['sets']) if len(s) > 1]
    firsts = d['sets'][open_i[0]] if only is None else only
    t0 = time.time(); tot = [0, 0, 0, 0, 0]
    with Pool(NW) as pool:
        for r in pool.imap_unordered(task, [(name, v, target) for v in firsts]):
            tot = [a + b for a, b in zip(tot, r)]
            if tot[3]:
                pool.terminate()
                print(f'{name}: MATCH COUNT AGAINST THE REAL TARGET: {tot[3]}. Stopping. HIT rule: nothing else is printed.'); sys.exit(3)
    print(f'{name:11s} [{d["scheme"]}] candidates {tot[0]:,}  survivors {tot[1]:,}  derivations {tot[2]:,}  '
          f'real-target matches {tot[3]}' + (f'  planted hits {tot[4]}' if target is not None else '') + f'  ({time.time() - t0:.0f} s)')
    return tot

if MODE == 'control':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import verify_hit as V
    # BIP39 control: a checksum-valid t12full_mp sequence in the slice slot6 = 'abandon', passphrase Charly, path m/0/0
    d = conf('t12full_mp'); sets = list(d['sets']); o = [i for i, s in enumerate(sets) if len(s) > 1]; sets[o[0]] = ['abandon']
    ws = next(w for k, w in enumerate(itertools.product(*sets)) if bip39_ok(w) and k > 900)
    k, _ = V.derive(V.mnemonic_to_seed(' '.join(ws), 'Charly'), 'm/0/0'); tgt = V.hash160(V.pub_compressed(k))
    print('control 1 (BIP39, planted with passphrase Charly on m/0/0, target from verify_hit.py):')
    r = run('t12full_mp', target=tgt, only=['abandon']); print('  PASS' if r[4] == 1 else '  FAIL')
    # Electrum control: an el12 sequence passing Seed version, passphrase JR, path m/0'/0/0
    d = conf('el12'); ws = next(w for w in itertools.product(*d['sets']) if el_ok(' '.join(w)))
    seed = hashlib.pbkdf2_hmac('sha512', ' '.join(ws).encode(), b'electrumJR', 2048, 64)
    k, _ = V.derive(seed, "m/0'/0/0"); tgt = V.hash160(V.pub_compressed(k))
    print('control 2 (Electrum, planted with passphrase JR on m/0\'/0/0, target from verify_hit.py):')
    r = run('el12', target=tgt); print('  PASS' if r[4] == 1 else '  FAIL')
elif MODE == 'small':
    for n in ('t12full_mp', 'el12', 'el13', 'el14', 'el16', 'el17'): run(n)
elif MODE == 'el18':
    run('el18')
