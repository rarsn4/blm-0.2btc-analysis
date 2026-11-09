# Is the machine itself sound? The self-test gap, found and closed

Measured 2 Nov 2026. Prompted by the question "how do we know we are right, and did we
make the same mistake for five years" — which is a question about the machine before it
is a question about the puzzle.

## 1. The gap: the live binary had never been self-tested

| artefact | timestamp | note |
|---|---|---|
| last recorded self-test | **2026-09-23 20:24** | git `961c17c`, "recovers melody and snow at index 2270828" |
| last commit of any kind | 2026-09-27 12:30 | `b72c071` |
| `solver2.cu` modified | 2026-09-28 09:26 | **uncommitted** |
| `solver_host2.cuh` modified | 2026-09-28 09:33 | **uncommitted** |
| `solver2_jac` built | **2026-09-28 09:33** | from those uncommitted sources |

**Every run from 28 Sep onward — the bulk of the campaign — used a binary built from
uncommitted source whose last planted-key self-test predated it by five days.**

The 28 Sep change was not cosmetic. It added `derive_multi3`, the three-encoding
compare path (compressed / uncompressed / hybrid), replacing a single-hash compare;
it added the `CASE` axis to `build_phrase`; and it changed the variant bit layout from
`(sp<<2)|(kd<<1)|pc` to `(cs<<4)|(sp<<3)|(kd<<2)|pc`, so `hit[1]` went from a bare path
index to `path<<2|encoding`. The diff carries the comment **"Kernel and selftest must
move together -- see §10."** They had not moved together.

This was a live hole in rule 8's spirit: the negatives were being accrued on an
unverified machine. It is recorded here rather than silently closed.

## 2. The three self-test configs are themselves correct [MEASURED]

`selftest_find.conf`, `selftest_uncomp.conf` and `selftest_hybrid.conf` (all written
2026-09-28 07:51, with no record of ever running) plant one key per encoding, sweeping
slots 3 and 11 over all 2048 words. Phrase at index 2270828 = `1108*2048 + 1644` =
word 1109 `melody`, word 1645 `snow`.

Verified by an **independent** pure-Python implementation — own secp256k1, BIP39
checksum, PBKDF2-HMAC-SHA512, BIP32 CKDpriv, and all three pubkey serialisations —
with no shared code with the solver:

| encoding | pubkey prefix | derived address | config `TARGET` |
|---|---|---|---|
| compressed | 0x02 | `1Q4BqYqf6iaSMqi2D3uPG95uA4kZ4bHUjd` | matches |
| uncompressed | 0x04 | `1AfCMrfzrL6E722GmodNqCsWxgA2k2PppQ` | matches |
| hybrid | 0x06 | `1ASVoy8JcR4fNxu84S3fDhUM5ZABmAsHG8` | matches |

BIP39 checksum on the planted phrase: valid. So a PASS on these tests means something.

## 3. The gap is now closed — all three PASS on the live binary [MEASURED]

Run 2 Nov 2026 against `solver2_jac` as built 28 Sep, through the default config path
(rule 8), concurrently with `t21_single`:

| config | encoding exercised | process exit | `^HIT index` lines | index reproduces 2270828 |
|---|---|---|---|---|
| `selftest_find` | compressed | 0 | **1** | yes |
| `selftest_uncomp` | uncompressed | 0 | **1** | yes |
| `selftest_hybrid` | hybrid | 0 | **1** | yes |

Each loaded target was independently re-derived from its address and matched the bytes
the solver printed (`fce52fee…`, `69f26bce…`, `678b948e…`). Logs were written outside
the repository so no `HIT` line enters tracked history; nothing beyond the hit **count**
and the index **equality** was read, and `show_hit` was not run.

**The machine finds a planted key on all three encodings. The negatives stand.**

## 4. Rule 8 across the whole history [MEASURED]

`grep -hoE 'target hash160 : [0-9a-f]{40}' *.log` over every log in the tree returns
**124 occurrences of exactly one value**, `ccbd031e54cde2a3189fd59bc49f731367a1779e`,
and never the void 32-bit word-swapped form `1e03bdcca3e2cd549bd59f1813739fc49e77a167`.
The host decode is big-endian correct (`h[i*4]<<24 | …`). The address itself was
re-verified independently: base58 checksum `b0bd07dc` valid, version byte 0x00,
hash160 as above.

**No run in the project's history is void for a wrong target.**

## 5. Hits: there have never been any [MEASURED]

`grep -c -E '^HIT[[:space:]]+index'` over all **83** logs in the tree: **0**. No
case-insensitive `^hit`, no `hit*`/`found*` file on disk. Against the BLM target,
nothing has ever matched. The three HIT lines of §3 are planted test keys at
*different* addresses, not the target.

## 6. What this does NOT establish

The machine is sound. That is all this file says. It says nothing about whether the
template, the word assignments or the 21-word length are right — see §2.17 for the
provenance audit (no assigned word traces to the author) and §5 for the length
argument's own stated tension.

## 7. [CLOSED 5 Nov 2026] Casing had never varied — it has now [MEASURED]

> **The claim below is superseded and kept as the record of what prompted the runs.**
> ~~`CASE` appears in **1 of 225 configs**, set to `lower`. The one run header that
> prints it reads `case : lower`. **`upper` and `title` have never been run, once.**
> … §2.12 states the limitation and it is still unclosed. `brain_t21_pool65.conf` at
> `CASE upper` is ~16.2 GPU-hours, the cheapest untested branch in the project.~~
>
> It was the cheapest untested branch, and it was taken. `brain_t21_upper` ran
> 3–4 Nov and `brain_t21_title` ran 4–5 Nov, both exhaustive at acceptance exactly 1,
> both negative, both disjoint from the `lower` twin and from each other (81 template
> words, every one with three distinct case forms, no single-letter word, no collision
> in any pair). **The brainwallet CASE axis is closed**: §2.12 now carries three
> exhaustive t21 rows and its heading says so.
>
> One correction that came out of it: this section said "the artwork is in capitals".
> It is not — three drawn strings are genuinely mixed-case, and that claim was
> retracted in `brain_t21_upper.conf`'s own header before the run. `upper` is one
> uniform capitalisation hypothesis among three, with no stronger claim on the
> artwork than the other two.
>
> Still open in §2.12, and untouched by any of this: the key-variant narrowing,
> `sha256` + space-joined only, one quarter of the space the t18 row covered.

## 8. [MEASURED 6 Nov 2026] The first same-config repeat in the campaign — bit-exact across a reboot and an Xid 31

Until today no configuration had ever been run twice, so **nothing in this project
had shown that the solver returns the same answer for the same input.** Every
negative rested on one pass. A laptop suspend forced the test by accident: the queue
had to be restarted, `run_queue_nov.sh` has no skip logic, and so `t21_nose2` ran a
second time from zero.

```
pass 1   05 Nov 02:13:58 -> 03:26:58   wall 4,380.12 s   exit=2   HIT 0
         exhausted, no match  (survivors 387425464 of 49589822592)
pass 2   06 Nov 14:35:45 -> 15:56:56   wall 4,871.97 s   exit=2   HIT 0
         exhausted, no match  (survivors 387425464 of 49589822592)
```

**Survivors identical to the digit: 387,425,464 both times**, out of 49,589,822,592
candidates, with 0 HIT lines in both passes.

What makes it stronger than a plain repeat is everything that happened between the
two. Pass 2 ran:

- after a **full reboot** (06 Nov 14:25:59) — fresh kernel, fresh NVIDIA module load,
  fresh CUDA contexts
- after an **Xid 31 MMU fault** on the same GPU (06 Nov 14:18:22, `FAULT_PDE
  ACCESS_TYPE_VIRT_READ`) — a hardware-reported memory-access fault on the card that
  produced pass 1
- after a **1 h 37 m s2idle suspend/resume cycle** on that card
- through a different thermal history: 11.32 M cand/s on pass 1 against 10.18 M on
  pass 2, a **+11.2% wall difference**, consistent with `SW Thermal Slowdown` at 88 °C
  (§4's regime: 1605 MHz under load against 1980 MHz idle)

So the result is invariant to reboot, to a GPU fault, to a suspend cycle and to an
11% swing in clock rate. The arithmetic does not depend on the machine's state.

**What this does and does not establish.** It is **one** config repeated **once**: it
shows the pipeline is deterministic for this input, not that it is correct. A
deterministic wrong answer is still wrong, and §1's defects were all of that kind.
What it does retire is a specific unstated assumption — that a single pass per config
is reproducible at all — which 94 evidenced runs had relied on without a single test.

It also did not come free: it cost 4,871.97 s of GPU time that the queue spent
redoing finished work, and it only happened because nobody had written skip logic.
The cheap way to keep the property is to repeat one short config deliberately after
any binary change, not to rerun queues by accident.
