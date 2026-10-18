#!/usr/bin/env python3
"""CPU test: the 21 distinct BIP39 words written in the artwork, in reading orders.

usage: python3 -I artwork_orders.py BIP39_WORDLIST

Word centres are master pixels read from gridded views (approximate, +/- ~20 px), listed below.
Orders: row-major (y, then x), column-major (x, then y), and block by block (blocks by top edge, and by
left edge; words inside a block in the order they are read). Any two neighbours closer than TOL px in the
sort key may be in either order: every permutation inside such a tie cluster is tried. A word written
twice (`this`) keeps its first occurrence in each order.
Checks: BIP39 checksum (7 bits for 21 words) and the Electrum v2 "Seed version" prefix (01 or 100, as
the solver's kernel accepts). Only passing sequences are derived: BIP39 on its four campaign paths, salt
"mnemonic"; Electrum on its four paths, salt "electrum"; empty passphrase; compressed and uncompressed keys.
HIT RULE: a sequence's words are printed only after it has been derived and shown not to match. On any
match the script prints only the count and stops.
"""
import sys, os, hashlib, hmac, itertools, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_hit as V

WL = [w.strip() for w in open(sys.argv[1])]; IDX = {w: i for i, w in enumerate(WL)}
TARGET = bytes.fromhex('ccbd031e54cde2a3189fd59bc49f731367a1779e')
TOL = 25

# (word, x, y, block). Blocks: wm = FIND THE SEED PHRASE IN THE THIS PICTURE; ord = Order and stability;
# sl = BLACK LIVES MATTER ... NOT ONE MORE; wel = WELCOME TO THE BRAVE NEW WORLD; br = I can't BREATHE;
# pay = PAY FOR THE FUTURE. THIS IS THE FIRST PREDICTION.; pl = ONLY real BITCOIN
OCC = [('order', 705, 87, 'ord'), ('find', 710, 98, 'wm'), ('seed', 705, 240, 'wm'), ('phrase', 690, 325, 'wm'),
       ('this', 690, 378, 'wm'), ('picture', 790, 378, 'wm'), ('welcome', 735, 430, 'wel'), ('brave', 750, 530, 'wel'),
       ('world', 900, 650, 'wel'), ('can', 1025, 398, 'br'), ('black', 1135, 250, 'sl'), ('matter', 1182, 255, 'sl'),
       ('peace', 1215, 125, 'sl'), ('end', 1240, 395, 'sl'), ('police', 1240, 325, 'sl'), ('one', 1298, 275, 'sl'),
       ('more', 1298, 195, 'sl'), ('future', 82, 855, 'pay'), ('this', 95, 1010, 'pay'), ('first', 95, 900, 'pay'),
       ('only', 110, 1057, 'pl'), ('real', 152, 1057, 'pl')]
READ = {'wm': ['find', 'seed', 'phrase', 'this', 'picture'], 'ord': ['order'],
        'sl': ['black', 'matter', 'peace', 'end', 'police', 'one', 'more'], 'wel': ['welcome', 'brave', 'world'],
        'br': ['can'], 'pay': ['future', 'this', 'first'], 'pl': ['only', 'real']}
BLOCK_ANCHOR = {'wm': (495, 15), 'ord': (650, 70), 'sl': (1080, 85), 'wel': (420, 378), 'br': (1000, 375),
                'pay': (74, 815), 'pl': (93, 1050)}
assert len({w for w, *_ in OCC}) == 21 and all(w in IDX for w, *_ in OCC)

def tie_orders(items, key):
    """all orders of `items` sorted by key, permuting inside clusters of neighbours closer than TOL"""
    s = sorted(items, key=key); clusters, cur = [], [s[0]]
    for a, b in zip(s, s[1:]):
        if key(b)[0] - key(a)[0] < TOL: cur.append(b)
        else: clusters.append(cur); cur = [b]
    clusters.append(cur)
    for combo in itertools.product(*[itertools.permutations(c) for c in clusters]):
        yield [x for c in combo for x in c]

def first_occ(seq):
    out, seen = [], set()
    for w in seq:
        if w not in seen: seen.add(w); out.append(w)
    return tuple(out)

FAM = {}
FAM['row-major'] = {first_occ([o[0] for o in p]) for p in tie_orders(OCC, lambda o: (o[2], o[1]))}
FAM['column-major'] = {first_occ([o[0] for o in p]) for p in tie_orders(OCC, lambda o: (o[1], o[2]))}
for name, k in (('blocks by top edge', lambda b: (BLOCK_ANCHOR[b][1], BLOCK_ANCHOR[b][0])),
                ('blocks by left edge', lambda b: (BLOCK_ANCHOR[b][0], BLOCK_ANCHOR[b][1]))):
    FAM[name] = {first_occ([w for b in p for w in READ[b]]) for p in tie_orders(list(READ), lambda b: k(b))}

def bip39_ok(ws):
    bits = ''.join(f'{IDX[w]:011b}' for w in ws); ent, cs = bits[:224], bits[224:]
    return f'{hashlib.sha256(int(ent, 2).to_bytes(28, "big")).digest()[0]:08b}'[:7] == cs

def electrum_ok(ws):
    h = hmac.new(b'Seed version', ' '.join(ws).encode(), hashlib.sha512).hexdigest()
    return h.startswith('01') or h.startswith('100')

def keys_match(seed, paths):
    hits = 0
    for p in paths:
        k, _ = V.derive(seed, p); x, y = V._mul(k)
        for pub in (V.pub_compressed(k), b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')):
            hits += V.hash160(pub) == TARGET
    return hits

EL_PATHS = ["m/0'/0", "m/0'/0/0", "m/0/0", "m/44'/0'/0'/0/0"]
total = matches = 0; derived_clean = []
for fam, seqs in FAM.items():
    nb = ne = 0
    for ws in sorted(seqs):
        b, e = bip39_ok(ws), electrum_ok(ws); total += 1; nb += b; ne += e
        if b:
            m = keys_match(V.mnemonic_to_seed(' '.join(ws)), V.CAMPAIGN); matches += m
            if m == 0: derived_clean.append((fam, 'BIP39', ws))
        if e:
            seed = hashlib.pbkdf2_hmac('sha512', unicodedata.normalize('NFKD', ' '.join(ws)).encode(), b'electrum', 2048, 64)
            m = keys_match(seed, EL_PATHS); matches += m
            if m == 0: derived_clean.append((fam, 'Electrum', ws))
        if matches:
            print(f'MATCH COUNT: {matches}. Stopping. HIT rule in DO_NOT_PUSH: print nothing else, move the funds first.'); sys.exit(3)
    print(f'{fam:20s} distinct orders {len(seqs):5d}   BIP39 checksum pass {nb:3d}   Electrum seed-version pass {ne:3d}')
print(f'\ntotal distinct orders checked: {total}; derived: {len(derived_clean)}; matches against the target: {matches}')
for fam, kind, ws in derived_clean:
    print(f'  derived, no match ({kind}, {fam}): {" ".join(ws)}')
print('\nunpermuted base orders (all failed both checks unless listed above as derived):')
print('  row-major   :', ' '.join(first_occ([o[0] for o in sorted(OCC, key=lambda o: (o[2], o[1]))])))
print('  column-major:', ' '.join(first_occ([o[0] for o in sorted(OCC, key=lambda o: (o[1], o[2]))])))
print('  blocks, top :', ' '.join(first_occ([w for b in sorted(READ, key=lambda b: (BLOCK_ANCHOR[b][1], BLOCK_ANCHOR[b][0])) for w in READ[b]])))
print('  blocks, left:', ' '.join(first_occ([w for b in sorted(READ, key=lambda b: (BLOCK_ANCHOR[b][0], BLOCK_ANCHOR[b][1])) for w in READ[b]])))
