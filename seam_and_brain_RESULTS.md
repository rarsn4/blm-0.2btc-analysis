# Results: seam validation and brainwallet mode

Both patches applied to `solver2.cu` / `solver_cores2.cuh` / `solver_host2.cuh`
/ `cyclone_adapter.cuh`. Every control below was run on this machine
(RTX 4070 Laptop, CUDA 12.6). Backups of the pre-patch sources are in `.bak_preseam/`.

---

## PART A — seam validation

### A3 Test 1 — exact count invariance  ✅

The survivor total is a pure function of the config, so any two chunkings must
agree exactly. `--chunk N` sets the chunk size; `--count-only` runs the filter
stage alone, which is where the base/count arithmetic under test lives.

`seam_count.conf` — 4,194,304 candidates, 12 words, slot 12 pinned wrong so it
always exhausts:

| `--chunk` | chunks | survivors | time |
|---|---|---|---|
| default | 1 | **262,250** | 0.21 s |
| 1,000,003 | 5 | **262,250** | 0.22 s |
| 65,537 | 64 | **262,250** | 0.34 s |
| 4,096 | 1,024 | **262,250** | 2.22 s |
| 1,021 | 4,108 | **262,250** | 8.17 s |
| 101 | 41,528 | **262,250** | 65.84 s |
| **7** | **599,187** | **262,250** | 206.96 s |

Prime sizes are deliberate: boundaries land at awkward offsets, not round ones.
At `--chunk 7` there are 599,186 joins. A bug dropping one candidate per join
would lose ~37,400 survivors, a 14% shortfall. It lost **zero**.

### Production scale, against a pre-existing reference  ✅

`t18_pool52.conf` is the real 380,204,032-candidate config. Three full runs made
with the **previous** binary (`t18_patha/b/c`, logged in `complet.txt`) each
reported **5,941,047** survivors. The rebuilt binary reproduces that number
exactly, at four chunkings:

| `--chunk` | chunks | survivors |
|---|---|---|
| default | 1 | **5,941,047** |
| 1,000,003 | 381 | **5,941,047** |
| 65,537 | 5,802 | **5,941,047** |
| 1,021 | 372,384 | **5,941,047** |

This is the stronger of the two count results: it is not merely self-consistent,
it matches production data generated before any of these changes existed. It
confirms both that no candidate is lost at a seam and that the refactor did not
alter filter semantics.

### A3 Test 2 — the answer planted ON a seam  ✅

The spec's `--chunk 4650657157` form **does not run**: at 12 words that chunk
yields ~290 M survivors against a 2^25 buffer, and the run aborts on
`survivor overflow` before reaching the seam. Chunk size and boundary position
were conflated.

`--seam N` separates them — it truncates the chunk containing N-1 so that it
ends exactly at N, leaving the chunk size otherwise alone.

`seam_hit.conf` — the known mnemonic with slots 11/12 blanked, answer at index
**3,368,325** (snow=1644, radar=1413), run at `--chunk 1000003`:

| placement | flag | result |
|---|---|---|
| mid-chunk (control) | *(none)* | HIT 3368325 |
| answer FIRST of its chunk | `--seam 3368325` | HIT 3368325 |
| answer LAST of its chunk | `--seam 3368326` | HIT 3368325 |
| answer SECOND of its chunk | `--seam 3368324` | HIT 3368325 |

And the same test on the real `selftest_multichunk.conf` at its actual
**4,650,657,157** — above 2^32, using `--resume 4650000000` to reach the region
cheaply:

| placement | result |
|---|---|
| mid-chunk (control) | HIT 4650657157 |
| answer FIRST of its chunk | HIT 4650657157 |
| answer LAST of its chunk | HIT 4650657157 |

That closes the hole. The original multi-chunk control proved chunk 2's base
offset was applied correctly; these prove nothing is dropped or duplicated at
the join itself, at both small and >2^32 indices.

### Also changed

- **Cumulative survivor count** (A1). The progress line and the exhaustion line
  now report the running total, not the last chunk's count. This is the
  instrument the whole count test depends on.
- **Progress throttled to ~1 Hz.** The per-chunk `fopen`+`fflush` cost more than
  the GPU work at small chunk sizes and made `--chunk 7` a 19-hour run. At
  production chunk sizes a chunk takes seconds, so nothing changes there. Worst
  case on a crash is losing under a second of progress.
- **`--count-only`** stops after the filter. The count test does not need the
  derive stage, and at tiny chunk sizes derive gets a handful of candidates per
  launch and starves the GPU. This is what made `--chunk 7` finish in 207 s.

### One latent bug found and fixed

`show_hit` printed `path : m/44'/0'/0'/0/0` unconditionally. Every config with
more than one `PATH` line — `t18_pool52.conf` has four, `t18_pathc.conf` has
eight — would have **misreported which path produced the hit**. It only ever
fires on success, so nothing could have caught it except a hit. `k_derive` now
records the matching path index in `hit[1]` and `show_hit` prints the real one.

---

## PART B — brainwallet mode

`priv = SHA256(phrase)` directly: no checksum, no PBKDF2, no BIP32, no path.

### B5 — the mandatory control  ✅ 12/12

A brainwallet has no checksum, so every candidate passes the filter by
construction. A wrong SHA-256 would report "exhausted, no match" exactly like a
correct run, with no symptom anywhere. Nothing else in the pipeline would notice.

`./solver2 --selftest-brain` — all 12 PASS:

| # | case | address |
|---|---|---|
| 1 | canonical, compressed | 1C7zdTfnkzmr13HfA2vNm5SJYRK6nEKyq8 |
| 2 | canonical, uncompressed | 1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T |
| 3 | double-SHA256, compressed | 1A95ZB1auLEAXVYorh9wrtzzHpduBUC3oC |
| 4 | double-SHA256, uncompressed | 1MBJcCMAGTjir6xQi3cFYxySCAdAaxUQsU |
| 5 | no spaces, compressed | 1aZamxMGppDGiZahCUoBqUGVRU94JBehf |
| 6 | no spaces, uncompressed | 1KqAv2r2iebeEhkoKonksJwwPczwBjLMXC |
| 7–8 | 124 B phrase, len%64 = 60 | 1H3JMSyEq2woEYLn9u1kG32HJjkQbVNwSw / 1Lc5bPdxAZzR5mm5S3swMmcxB83FtKgvLi |
| 9–10 | 128 B phrase, len%64 = 0 | 1DzFSoymTdd2eP5FFCeRG7y69nbbh18ZjW / 1BTCdnvSFPL48HaTKqaev6Z2FSANo9Keq8 |
| 11–12 | 157 B, 24 words, 3 blocks | 1HVQmcDk3u9RdwbrjNvLRgftYzwAh2fzX9 / 1863f84WJ7fDDWB4XgNWuZqg7uHCNgaSzw |

**Cases 7–12 exist because the canonical vector is not sufficient.** "correct
horse battery staple" is 28 bytes — a *single* SHA-256 block. It cannot detect a
broken multi-block path, which is precisely the trap the spec warns about and
precisely what an 18-word (~114 B) or 24-word (~153 B) phrase needs. The three
lengths were chosen to hit `len%64 = 60` (forces the extra padding block),
`len%64 = 0` (message consumed entirely by the block loop) and three full
blocks. Getting only the canonical vector green would have proved almost nothing
about the mode as actually used.

### Correction to `brainwallet_patch.md` §4

The two addresses were labelled the wrong way round. **1JwSSub… is
UNCOMPRESSED**, 1C7zd… is compressed. Verified against `coincurve` on the host
and independently by the device, which reports the matching variant:
`brain_selftest.conf` targets 1JwSSub… and the solver reports
`pubkey : uncompressed`.

### B6 — the arbitrary-word table was not optional

`battery` and `staple` are **not BIP39 words**. Neither are the eleven image
words the whole idea rests on: `stop freedom hate white death kill war bleed
shut money buy`. So the choice was never "mode flag now, word table later" — it
was "word table, or a brainwallet mode whose mandatory control cannot even be
assembled".

Implemented as an `EXTRA` config key. Wordlist tables now hold 4096 entries:
BIP39 at 0..2047, EXTRA appended after. `widx()` refuses an index past 2047
unless the config is brainwallet, so the checksum path can never receive a word
it cannot encode in 11 bits, and an `EXTRA` line in a BIP39 config is a parse
error rather than silent corruption. Worst-case phrase length is checked at
parse time, since EXTRA words have no 8-character BIP39 bound.

### Planted-hit control at scale  ✅

`brain_find.conf` — 63^5 = 992,436,543 candidates, answer planted at index
**214,072**. Three of its five gap words are non-BIP39 (`freedom`, `war`,
`money`), so the config is unrepresentable in BIP39 mode by construction.

| placement | result |
|---|---|
| mid-chunk (`--chunk 50000`) | HIT 214072 |
| answer FIRST of its chunk (`--seam 214072`) | HIT 214072 |
| answer LAST of its chunk (`--seam 214073`) | HIT 214072 |

This covers what the 1-candidate selftest cannot: `decode_template`,
`k_filter`'s accept-all branch, the `CHUNK = CAP` sizing and the chunk loop —
and it confirms the seam behaviour holds in brainwallet mode too.

### Config surface

```
SCHEME brainwallet
TARGET <address>
WORDS 18
BRAINHASH  sha256 dsha256           # key = SHA256 or double-SHA256
BRAINSPACE yes no                   # phrase joined with spaces or without
BRAINPUB   compressed uncompressed  # or "both"
EXTRA stop freedom hate white ...   # non-BIP39 words, brainwallet only
```

No `PATH` (warned and ignored). `--passphrases` is warned and ignored: a
brainwallet takes no passphrase.

### Measured cost — `brainwallet_patch.md` §5 is ~2x optimistic

Two effects it missed pull opposite ways. Against: no checksum, so **every**
candidate derives — 380,204,032 rather than 5,941,047 for t18/52, 64x the EC
work. For: each derivation is far cheaper — no PBKDF2, one scalar mult instead
of BIP32's chain. Measured **489,000 derivations/s** against **15,600/s** for
the BIP39 path.

| config | candidates | measured | §5 claimed |
|---|---|---|---|
| t18, 52-word pool | 380,204,032 | ~13 min | ~7 min |
| t18, 63-word pool (+EXTRA) | 992,436,543 | ~34 min | — |
| t18, 80-word pool | 3,276,800,000 | ~1.9 h | ~59 min |
| t21, 52-word pool | 19,770,609,664 | ~11 h | ~6 h |

Multiply by BRAINHASH × BRAINSPACE combinations — those are distinct private
keys, each costing its own scalar multiplication. **BRAINPUB multiplies
nothing**: compressed and uncompressed are two serialisations of the same curve
point and share one scalar mult. Measured `pub=both` 493,438/s against
`pub=compressed` 439,178/s — free within noise.

---

## Production sweeps — all negative

Run 2026-09-01, after every control above was green.

| config | candidates | keys/cand | addresses | rate | wall | result |
|---|---|---|---|---|---|---|
| `brain_t18_pool52_all` | 380,204,032 | 4 | 3,041,632,256 | 109,177/s | 58m09s | no match |
| `brain_t18_pool63` | 992,436,543 | 1 | 1,984,873,086 | 441,714/s | 37m38s | no match |
| `brain_t18_pool63_all` | 992,436,543 | 4 | **7,939,492,344** | 107,398/s | 2h33m59s | **no match** |

### These three runs are NESTED. Do not add them.

`brain_t18_pool63_all` **subsumes both earlier runs**, verified from the configs
rather than assumed:

- identical SLOT structure (same 13 pinned words, same 5 pool gaps)
- identical variant settings (SHA-256 + double-SHA-256, space-joined +
  concatenated, compressed + uncompressed)
- the 52-word pool is a strict subset of the 63-word pool — the 11 extras are
  exactly `bleed buy death freedom hate kill money shut stop war white`

So 52^5 ⊂ 63^5 over the same slots and the same derivations. Summing the three
rows double-counts 380,204,032 candidates twice over.

**Distinct brainwallet coverage is one number: 992,436,543 candidates =
7,939,492,344 addresses.**

*(An earlier note in this session reported 5,026,505,342 addresses for the first
two runs. That was itself an overcount: their overlap — 380,204,032 candidates
under SHA-256/space-joined, both compressions — was counted twice, so the
distinct figure at that point was 4,266,097,278. Superseded either way.)*

### Two internal checks these runs passed

**Acceptance is exactly 1.0.** All three report `survivors == total` to the
candidate. In brainwallet mode there is no checksum, so anything less would mean
`k_filter` was silently discarding candidates. The cumulative survivor counter
from Part A1 is what makes this visible; the old per-chunk display could not
have shown it.

**Variant cost multiplies as designed.** 441,714/s at one key variant against
109,177/s and 107,398/s at four — ratios of 4.05 and 4.11 against a predicted
4.00. The scalar multiplication dominates, `BRAINHASH` × `BRAINSPACE` each
multiply it, `BRAINPUB` does not. Predicted 2.53 h for the final run against
2.57 h actual.

### Coverage, stated exactly

All five template gaps over a 63-word pool — the 52 BIP39 candidates plus the
eleven image words that BIP39 cannot represent — under every combination of
SHA-256 / double-SHA-256 and space-joined / concatenated, each checked as both
compressed and uncompressed. The eleven non-BIP39 words are now covered in all
four key variants, not one.

Not covered: word orderings outside the template. For a brainwallet, order
matters exactly as much as it does for BIP39, and the position machinery is
still what would be needed.

### Keep this out of the §3 tally

The §3 total (24,767,853,989 BIP39 + Electrum derivations) must not absorb these
7.94 billion. A brainwallet address costs one scalar multiplication; a BIP39
derivation costs PBKDF2's 4,096 SHA-512 compressions plus a BIP32 chain —
measured 489,000/s against 15,600/s, a factor of 31. Adding them would inflate
the headline by a third with work that is an order of magnitude cheaper per
unit, turning a number that means something into one that merely sounds large.
Separate column, separate section, and say why.

---

## Scope note for the report

Nothing here licenses a claim about brainwallets as a *class*. The class is
every possible string and it is unbounded. What these configs sweep is the
**template word sequences** — the same slot structure the BIP39 runs used, now
under SHA-256 — plus, for the first time, the eleven image words that BIP39
could not represent. That is a real and previously uncovered derivation class,
and it belongs in a "tested, negative" section, not alongside anything titled
"exhaustively eliminated".
