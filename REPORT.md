# 0.2 BTC Puzzle — the rune cipher solved, over 278 billion derivations eliminated, and six defects in the shared data

**Target:** `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`
**HASH160:** `ccbd031e54cde2a3189fd59bc49f731367a1779e`

**Status:** the Bitcoin puzzle is **NOT solved.** The address has received
20,107,284 sats across 5 transactions and spent zero — verified on-chain,
untouched since May 2020.

What **is** solved is the **rune cipher**, except for a single glyph. Those are
different claims and this report keeps them separate throughout.

I built a GPU search pipeline covering both BIP39 and Electrum and ran
**278,996,119,787 full seed derivations** — 8,073 days of CPU at typical solver
rates — plus 7,939,492,344 brainwallet addresses counted separately (§2.12).
§2.1–2.11, §2.13 and §2.14 are exhaustively eliminated, not "tried and didn't
find". §2.12 and §2.15 are tested corpora — a weaker claim, and tagged as such
in their own headings. §2.16 and §2.17 are measurements of the template itself
rather than eliminations within it, §2.18 is a tested hypothesis about its
numbering, and §2.19 banks the leave-one-out family — a fifth of all the compute,
previously credited in one table row, and §2.17 is the one to read first if you
are deciding whether any of this is worth continuing.

Code, configs and every hypothesis tested:
https://github.com/rarsn4/blm-0.2btc-analysis

---

## 0. Epistemic status

Claims below are tagged. Do not promote a tag without new evidence.

| Tag | Meaning |
|---|---|
| **[MEASURED]** | Re-derived from the image, the wordlist, or the chain. Reproducible. |
| **[EXHAUSTED]** | A complete search space enumerated, empty. |
| **[TESTED]** | A finite corpus tried, empty. **Not** an elimination of the class. |
| **[INFERRED]** | Follows from measured facts by a stated argument. |
| **[ASSUMED]** | Load-bearing but unproven. The soft spots. |

The distinction between [EXHAUSTED] and [TESTED] is the one that matters: §2.1–2.11
are the first, §2.12 is the second, and conflating them would be the only overclaim
in this document.

---

## 1. Six defects in the shared data

### 1.1 `breathe` is not a BIP39 word

It appears in circulating word lists and is the widely-assumed passphrase. It is
**not in the BIP39 English wordlist** and cannot appear in any seed phrase.

```python
from mnemonic import Mnemonic
"breathe" in Mnemonic("english").wordlist   # False
```

`breath` is also absent. As a *passphrase* it remains possible — tested, along
with 64 others, negative (§2.4).

### 1.2 `candidates_unplaced.txt` is missing three valid words

The list appears to derive from the whitepaper fragment quoted at the bottom of
the image. That fragment yields **ten** BIP39 words in order:

```
they receive need proof that time major agree first receive
```

The published list has seven. **`they`, `that` and `time` are absent** —
presumably filtered as function words without checking membership. All three
are valid (`they` #1796, `that` #1791, `time` #1810, 1-based).

### 1.3 `any` is #82, and the repo indexes 1-based

The README's per-section BIP39 indices are **1-based** — 44 of 45 confirm it.
BIP39's own encoding is **0-based**, so `1713 → stock` follows the repo's
convention while the spec gives `stomach`. Both need testing.

The 13th-Amendment reading gives `any` as #84; it is **#82** 1-based, #81
0-based. `slave`, `duly` and `convicted` from the same text are not BIP39 at all.

### 1.4 A whole phrase is missing from the "BRAVE NEW WORLD" micro-text

Section 14 of the README documents only letter-level typos (`introdue`,
`participans`, `doudle`, `sing`, `abcense`). It misses that an entire phrase is
absent.

Inside the **E of BRAVE**, the micro-text reads:

> common solution / is to introdue / cent / ral au / thority / or mint that /
> checks every / transac / tion / for double spen / ding. After

The whitepaper reads:

> A common solution is to introduce **a trusted** central authority, or mint,
> that checks every transaction for double spending.

**"a trusted" is absent.** Note the typo `introdue` sits exactly at the splice.
Whether this is deliberate or the same carelessness that produced the other
typos is open — but `trust` (#1870) was tested at every gap and pinned at slot
21, negative (§2.7).

### 1.5 The `.VS.` ambigram flips **vertically**, not horizontally

Confirmed by direct extraction: mirrored across the **horizontal axis**,
`.VS.` renders as a clean `·12·`. It is a deliberate ambigram.

This is a **slot marker**, not a phrase length. Reading it as "the seed is 12
words" is likely the single most common wrong turn in this puzzle (§5).

### 1.6 24-word mnemonics require HMAC key pre-hashing — this silently breaks solvers

**Check this before trusting any 24-word negative you have produced.**

PBKDF2-HMAC-SHA512 uses the mnemonic as the HMAC *key*. RFC 2104 requires a key
longer than the 128-byte block be replaced by `SHA512(key)`. Measured over 2000
random 24-word phrases:

| | bytes |
|---|---|
| minimum | 135 |
| mean | 153 |
| maximum | 172 |
| **fraction exceeding 128 bytes** | **100%** |

A solver that zero-pads instead is **correct for 12 words** — it passes every
12-word test vector — and derives well-formed, plausible, **entirely wrong**
seeds for 24 words. No error, no malformed output.

```
abandon x23 + art
correct  : 408b285c123836004f4b8842c89324c1...
zero-pad : 2facfb042cc06dc665f95578b2b74c68...
```

Canonical check: `abandon` ×23 + `art` → `1KBdbBJRVYffWHWWZ1moECfdVBSEnDpLHi`
at `m/44'/0'/0'/0/0`.

---

## 2. What is exhaustively eliminated

All runs cover four derivation paths unless noted.

### 2.1 The clock overlay is dead as a word set

The twelve words `order camera more second this vote black liberty real punch
mask address` across **all 479,001,600 orderings** — every rotation, both
directions, every reflection — with 12 passphrases. 359 million derivations.

Enumerating 12! subsumes every rotation; reading directions need no separate test.

### 2.2 The 12-word template is dead over its complete space

Positions 1–12 of the position table with **both gaps swept over all 2048 BIP39
words** — not a candidate list, the entire wordlist — across 65 passphrases and
4 paths.

### 2.3 The 18-word template is dead in both directions

- **Leave-one-out:** each of the five gaps freed to **all 2048 words** with the
  others pooled. 300 M derivations.

  > **[CORRECTED 2026-09-01] This is narrower than originally stated.** The
  > configs that ran it (`t18_full{6,8,14,15,18}.conf`) drew the *other four*
  > gaps from the old **37-word** pool and carried **no `PATH` lines**, so they
  > ran the single default path. An audit of every config in the project found
  > that **none combines `@FULL` with a pool ≥52 or with 4 paths.**
  >
  > So two regions were never tested: one gap free over all 2048 while another
  > gap holds one of the 17 words added since (`able cause crime exist happy
  > know neither only party peace place that they thing time any verb`), and
  > the entire leave-one-out family on paths 2–4.
  >
  > This matters most for words outside **every** pool. `flag`, `banner`,
  > `nation`, `state`, `eagle`, `field`, `glory` and `salute` are all BIP39 and
  > none has ever been in a gap pool — they are reachable *only* through an
  > `@FULL` sweep, and the `@FULL` sweeps were the weak ones.
  >
  > **[RESOLVED 2026-09-01]** Closed by `t18_loo{6,8,14,15,18}.conf`: each slot
  > free over all 2048 words, the other four over the current 54-word pool, all
  > four paths. 87,071,293,440 candidates, 1,331,791,148 derivations after
  > removing the overlap between runs. All five negative. The claim is now
  > earned at every t18 gap under the current pool and path set.
- **Free-one-fixed:** each of the thirteen fixed words freed to all 53
  candidates. 747 M derivations. *No single wrong fixed word explains it.*
- **Paired:** `camera` + `pyramid` — the pairing the table itself flags as
  conflicted — both freed. 3.04 B derivations.

### 2.4 Also eliminated

- t15 and t21 across pools of 37, 40, 52, 61, 67, 69, 71, 75 and 80 words
- Template reversal (slot order) for t18 and t21
- Position offsets −1 and +1
- 65 passphrases from the image text, including `Сумма двух чисел`, all
  `BREATHE` casings, BLM slogans, dates, and the target address itself
- The gold-chart y-axis values as BIP39 indices — `1800 1600 1400 1200 1000 800
  600 400 200` → `thought side puzzle nominee language glue enough cradle body`
  (1-based, all nine correct), tested both as an exclusive gap pool and merged
  into the 52-word pool

### 2.5 Every derivation path in the standard gap limit

This was a live assumption underneath every other result. Now closed:

- `m/44'/0'/0'/0/0` through `/35` — well past the standard BIP44 gap limit of 20.
  Index **21** was checked specifically: the positional argument in §5 points there
  and it sat one past the original sweep
- change chain `m/44'/0'/0'/1/0`, `/1`
- accounts `m/44'/0'/1'/0/0`, `m/44'/0'/2'/0/0`
- bare BIP32 `m/0/0`, `m/0/1`, `m/0/2`, `m/0'/0/0`, `m/0'/0/1`, `m/0'/0/2`

`m/49'` and `m/84'` are excluded by the address format — they produce `3…` and
`bc1…`, and the target is legacy `1…`.

### 2.6 Electrum v2 — never tested by anyone before this

The repo README says "we should consider Electrum seed derivation and BIP39 seed
derivation." Every published attempt used BIP39 only. **A BIP39 checksum filter
actively discards valid Electrum phrases.**

| | BIP39 | Electrum v2 |
|---|---|---|
| validity | 4–8 bit checksum in the words | `HMAC-SHA512("Seed version", mnemonic)` prefix |
| prefixes | — | `01` standard, `100` segwit |
| PBKDF2 salt | `"mnemonic" + passphrase` | `"electrum" + passphrase` |
| default path | `m/44'/0'/0'/0/0` | `m/0'/0` |
| **word count** | 12/15/18/21/24 only | **any length** |

Proof it matters — Electrum's own documented seed:

```
wild father tree among universe such mobile favorite target dynamic credit identify
  HMAC-SHA512("Seed version", ...) = 1001bc7d...   -> valid Electrum (segwit)
  BIP39 checksum                                    -> INVALID
```

A valid Electrum seed that fails BIP39 and would be discarded before any address
is derived. My filter was verified to accept it before any run.

Eliminated: **12, 13, 14, 16, 17, 18 and 21 words**, four paths, plus 65
passphrases and the all-slots-vary sweep. Lengths 13/14/16/17 are illegal under
BIP39 and had never been searchable by anyone.

> **[MEASURED, 2026-10-13] Re-run with logs; six of the claimed lengths now
> evidenced.** The originals had no log anywhere on the machine, so they were
> re-run, cheapest first, into `electrum_rerun.log`, each scored against a band
> stated before it ran:
>
> | run | candidates | survivors | expected | z | result |
> |---|---|---|---|---|---|
> | `el12` | 4,900 | 16 | 20.3 | −0.96 | negative |
> | `el13` | 4,900 | 17 | 20.3 | −0.74 | negative |
> | `el14` | 343,000 | 1,379 | 1,423.6 | −1.18 | negative |
> | `el16` | 24,010,000 | 99,509 | 99,650.9 | −0.45 | negative |
> | `el17` | 24,010,000 | 99,869 | 99,650.9 | +0.69 | negative |
> | `el18` | 1,680,700,000 | 6,974,876 | 6,975,561.5 | −0.26 | negative |
>
> All in band, all on the current binary, so all three key encodings were
> checked. `el21` (235,298,000,000 candidates, band 976,578,613.3 ± 31,185) is
> running. **`el22` is held**: it is `70⁷ × 2 = 16,470,860,000,000` candidates,
> about 8.5 days at the measured Electrum rate — not the 31 hours a `54⁷`
> estimate gave, because the `el*` configs use a **70-word** pool, not the BIP39
> 54-word one.
>
> **The Electrum route was certified first.** A valid Electrum v2 *standard*
> seed (HMAC `"Seed version"` prefix `0x01`) was planted in `el21`'s own shape —
> four paths, 70-word pool, two gaps free — and chosen to be an **invalid**
> BIP39 mnemonic, so a hit could only come through the Electrum route. Both
> binaries recovered it at the predicted index on `m/0/0`; the word-swapped
> target went silently negative on both.
>
> **Every band above uses the kernel's acceptance, not the host's.** The kernel
> accepts first byte `0x01` (1/256) or `0x10` with a zero high nibble next
> (1/4096): **17/4096 = 1/240.94**. The host's printout and its rate estimate
> divide by **171**, which overstates expected survivors **1.409×**. Measured on
> `el16`'s 24,010,000 candidates: 99,509 survivors, acceptance **1/241.28** —
> −0.45σ from 17/4096 and **−109σ** from 1/171. Its third use, chunk sizing, errs
> safe: it under-fills chunks rather than overflowing them. Read against the
> printout, `el18` would have looked like a −1,013σ shortfall.

> **[SCOPE] The original Electrum runs had no surviving log, and the list did
> not include 22.** Configs exist for `el12`, `el13`, `el14`, `el16`, `el17`,
> `el18`, `el21` and `el22`. A search of this tree and of the whole machine finds
> **no log for any of them** and no line reading `scheme=ELECTRUM` anywhere. None
> is in the `EVIDENCED` ledger. So the eliminations above rest on this
> paragraph's prose alone — the same status the image-text brainwallet corpus had
> before it was rebuilt — and should be read as asserted, not evidenced.
>
> `el22.conf` exists and was never run, which is why 22 is absent from the list.
> Electrum v2 accepts any length, so a list that reads as an enumeration implies
> a completeness it does not have: **15, 19, 20, 22, 23 and 24 are open under
> Electrum.** Same disease as §2.19's heading — a true list that implies more
> than it covers. Raised by an outside reader in public issue #1.

### 2.7 The all-slots-vary sweep — both schemes

The strongest structural test in the project. All 13 fixed words varied
**simultaneously** across 8,192 combinations of {table word, alternative}, with
the gaps pooled:

```
subject|section  camera|twin  tower|clock   mask|face    police|order
liberty|torch    eye|pyramid  black|night   pyramid|space
vote|debate      moon|month   rifle|gun     gold|price
```

This covers 0, 1, 2 … 13 wrong words at once rather than one tier at a time.
Run under **BIP39** (8.88 B derivations) and **Electrum v2** (3.32 B). Both
exhausted.

Also tested: `trust` pinned at slot 21 — the blank clock hand — with pools of 52
and 69 words. Negative. The two manufactured absences (the unlabelled hand and
the deleted "a trusted") do not combine this way.

### 2.8 Two wordlists are impossible, not merely untested

- **Electrum v1** (1626-word list): seven of the fifteen fixed table words do
  not exist in it — `camera`, `police`, `liberty`, `pyramid`, `vote`, `rifle`,
  `gold`. So does `food`. No v1 seed on this table is possible regardless of
  derivation.
- **Russian BIP39**: nine of twenty core words have no Russian equivalent —
  `camera`, `mask`, `black`, `vote`, `rifle`, `gold`, `real`, `world`, `proof`.
  The table cannot be translated. (Russian is also not in the official BIP-39
  spec; it is a community addition.)

Both die at the vocabulary stage, before any algorithm needs implementing.

### 2.9 The image is closed

- **No steganography.** LSB across R/G/B: 0.498 / 0.500 / 0.505.
- **No hidden layer.** The PNG is RGBA; alpha is fully opaque, zero non-opaque
  pixels.
- **No JPEG history.** 8×8 block-edge ratio 0.985 / 0.910 — never compressed.
- **No metadata.** Chunks are `IHDR`, `sBIT`, `IDAT` only.
- **No larger source exists.** `i.redd.it/n1x7g8ceaur51.png` serves 1600×1200,
  md5 `7710323461a924987eb35c77055e59f6`, byte-identical to the circulating
  copy. `preview.redd.it` at 2048/3000/4096 returns nothing.

### 2.10 The chain is closed

- **No `OP_RETURN`** in any of the five transactions. No on-chain message.
- **Never spent.** `spent_txo_count: 0`.
- The extra 107,284 sats are three dust payments plus one deliberate 0.001 BTC
  deposit on 2024-12-13.
- **Change address `39rEPyWKE9Ej…` untouched since 2020** — funded once, never
  spent.
- The funding transaction is `version 1`, `locktime 0`, `sequence 0xffffffff` on
  all four P2SH inputs. That rules out Bitcoin Core (v2 + anti-fee-sniping
  locktime) and Electrum (v2 + RBF sequence). It is a **custodial service or
  exchange batcher** — so the funding wallet is not the puzzle wallet and
  reveals nothing about which software produced the seed.

### 2.11 The whitepaper is not the ordering key

3,564 tokens, 788 BIP39 words, 241 unique:

| test | windows | checksum-valid | hits |
|---|---|---|---|
| document order, lengths 12/15/18/21/24 | 3,855 | 93 | 0 |
| deduplicated, first occurrence | 1,120 | 25 | 0 |
| each of the 12 sections separately | 2,653 | 63 | 0 |
| image candidates by first appearance | 35 | 3 | 0 |

For anyone reasoning about section numbers: **the whitepaper has 12 sections,
not 9.** Section 11 (Calculations) exists, so `11.03.20` → Section 11 is a live
reading. Tested; negative.

**[TESTED, externally] The 24-word whitepaper-sentence family.** Four configs —
`wp_fixed`, `wp_fixed2`, `wp_pool8`, `wp_pool10` — were written into this
repository and **never run by this project**: no log, no checkpoint. An outside
researcher, hiddengogeta, ran three of them independently on an Arc B580 and
reported in public issue #1. Their figures reproduce here exactly, and all three
pass the 24-word checksum-ratio test at /256:

```
wp_pool10   37^5 x 2 x 9^4 = 909,931,403,754 candidates
            survivors 3,554,484,286 vs 3,554,419,545.9   z = +1.09
wp_fixed    survivors 541,520   vs (37^5 x 2)/256        z = -0.31
wp_fixed2   survivors 541,662   same space               z = -0.12
```

The fourth, `wp_pool8`, is covered without a run: it is a **strict subset** of
`wp_pool10` slot by slot — each of slots 21–24 frees over seven content words
that all appear among `wp_pool10`'s nine. So the whole family is closed, by an
external run whose arithmetic was checked here rather than taken on trust. It is
**not** added to this project's ledger, because its logs are not in this tree;
it is recorded as an independent result.

Their note that this family was "openable on your hardware in seconds" was wrong
by about five orders of magnitude — at this rig's 11,925,000 cand/s,
`wp_pool10` alone is 21.2 h. Irrelevant now that it is done, but their cost model
for this hardware should not be relied on.

### 2.12 [TESTED] Brainwallets — a class nobody had touched

`priv = SHA256(phrase)` directly: no BIP39 checksum, no PBKDF2, no BIP32, no path.
Common in 2020-era puzzles and never tested against this target.

**Two corpora, both negative.**

*Image text*, 22,638 keys: every text string in the image (Latin mottos, Russian
plaintexts, BLM slogans, dates, the 13th Amendment, whitepaper fragments, the target
address itself), casing / punctuation-stripped / whitespace-stripped variants, each
individual word of the Russian plaintexts, all 2048 BIP39 words singly, and pairwise
concatenations of 33 salient phrases under three joiners. Plus SHA256 and SHA256² of
the PNG file and of the concatenated IDAT payload.

*Template sequences*, 992,436,543 candidates → **7,939,492,344 addresses**: the t18
template over a 63-word pool (the 52-word pool plus the eleven image words that are
**not** BIP39 — `stop freedom hate white death kill war bleed shut money buy`, which
a brainwallet permits and a mnemonic cannot). All four key variants — SHA256 and
double-SHA256, space-joined and concatenated — each as compressed and uncompressed.

**[TESTED] The 21-word template, lowercase, 2026-09-29.** The t18 gap above is
now partly filled. `brain_t21_pool65.conf` ran the **t21** template over a
65-word pool — the template's own 54-word pool plus the eleven non-BIP39 image
words; 54 + 11 = 65, not the 63 of the t18 run, because the t21 pool is larger.

```
space        150,837,781,250 candidates   (65^6 x 2, six @POOL slots + slot 20's two words)
survivors    150,837,781,250              acceptance EXACTLY 1.0
addresses    452,513,343,750              (x3: compressed, uncompressed, hybrid)
result       exhausted, no match          exit 2
wall         16.23 h, 2,582,308 cand/s
```

**Acceptance is the load-bearing number.** A brainwallet has no checksum, so
every candidate must pass the filter by construction; survivors equalled
candidates on every checkpoint line and at the total. Anything below 1.0 would
mean work was being silently dropped, and the negative would be void.

Two narrowings, both deliberate, both stated in the config header so no reader
infers parity with the t18 figure. **Casing: lowercase only** — the artwork is
in capitals and SHA-256 is case-sensitive, so the capitalised reading is
untested here. **Key variants: `sha256` + space-joined only**, which is 3
addresses per candidate against the 12 of an `_all` run, because `BRAINPUB` is
three serialisations of one EC multiply while `BRAINHASH` and `BRAINSPACE` each
produce a different private key. So this covers **one quarter** of the
key-variant space the t18 figure covered, on the canonical variant.

Two scope limits remain on the **t18** corpus, both narrow and both stated
rather than implied. It ran at t18, not t21 — and the t21 run above does not
inherit its key-variant coverage. And it predates hybrid-key support, so it covers compressed
and uncompressed only; the kernel now hashes all three, but the 7.94 B figure
above was measured before that.

**Casing, which applies to the two corpora differently.** The *template* corpus
is **lowercase only**, verified: every `SLOT`, `POOL` and `EXTRA` word in
`brain_t18_pool63.conf` is lowercase, the BIP39 wordlist is lowercase, and the
phrase builder emitted those bytes verbatim — at the time of that run it had no
casing parameter to pass. SHA-256 is case-sensitive and the artwork is in
capitals, so **no capitalised template sequence has been tested.** The solver now
takes `CASE lower | upper | title | all`, defaulting to `lower` and printing the
setting in the run header, so no future run can be silently lowercase.

The *image-text* corpus had no surviving generator, key list or log, so its
22,638 was reproducible from nothing but the sentence describing it. It now has
one: `brain_image_corpus.py` rebuilds it from the sources that do survive —
`slogan_lines.py`'s transcription, §7's decoded Russian, §1.4's micro-text, the
Latin from `census_crops.py` and the seal ring, the dates, the target address,
the BIP39 wordlist, and the PNG and IDAT digests — and derives the whole corpus
in seconds.

**The corpus that was actually run is the maximal reading: 29,408 distinct key
strings, 176,448 addresses, no match, 3.4 seconds.** Every flag below is
monotone — setting one only ever adds strings — so the all-True reading is the
*union* of all 64 readings the description admits. That matters for what the
negative covers: not one defensible interpretation of §2.12's sentence with the
rest bounded, but every corpus that sentence could denote. The committed key
list makes it auditable string by string. (The narrower best-justified reading
gives 9,974 strings and 59,844 addresses, also no match.)

**The description underdetermines its own corpus, and by how much is now
measured.** §2.12's sentence leaves at least six binary choices open — whether
punctuation-stripped and whitespace-stripped forms are both included, whether
Title case counts as a casing, whether the pairwise concatenations themselves
get the variant treatment, whether the 2048 BIP39 words get casing, whether the
whole-document concatenations are in. Enumerating all 64 readings gives totals
from **5,589 to 29,408**, a 5.3× spread. 22,638 sits inside that band. No
reading reproduces it exactly; the nearest is 21,646, off by −992.

A second discrepancy is left standing rather than resolved. §2.12 says **33**
salient phrases; the natural list from the surviving sources is **34**. An
earlier version of this script sliced the list to `[:33]`, which enforced the
reported figure — and then the resulting `33 × 32 × 3 = 3,168` was briefly
written up as *agreement* with §2.12. It was an artefact of the slice. The slice
is gone, the count is 34, and the one-item gap is informative in a way the
truncation destroyed: it points either at which phrase the original excluded or
at a different counting convention.

That is the claim this section carries: the sentence is underdetermined, **not**
that the figure is doubtful. The distinction matters and the evidence supports
only the first.

**Why the search stopped at six flags.** Not gap density — each reading is a
specific integer and even 512 of them would not reliably land on 22,638 exactly.
The reason is simpler and harder to argue with: **six binary flags are 64
predictions for one observation.** A model that over-parameterised cannot be
confirmed by matching that observation at all, whatever the spacing works out
to. What more flags would actually buy is a *near* miss close enough to round
into agreement, which is worse than a clean gap because it reads as a result.
The band is reported instead.

One correction worth recording, because the first attempt got it wrong. The
Latin was initially reported as having no surviving source, on a grep for
`novus|ordo|seclorum|annuit|coeptis`. The artwork's Latin is not the Great Seal
mottos: it is `Esse quam niger es, sic dixit caccobus ollae` in the element
census, `FIAT JUSTITIA ET PEREAT MUNDUS` on the pyramid base, and
`RERUM · COGNOSCERE · CAUSAS` mirror-written on the seal ring. A pattern built
from the expected answer found nothing and was briefly taken as evidence of
absence.

> **This is [TESTED], not [EXHAUSTED].** The brainwallet class is every possible
> string and is unbounded. The honest claim is "the phrases present in the image, plus
> the template sequences over a 63-word pool". It is **not** filed with the GPU sweeps
> in §3 for the same reason: a brainwallet address is ~31× cheaper than a seed
> derivation (489,000/s against 15,600/s measured), so folding 7.9 billion of them
> into a total headed "full seed derivations" would inflate the figure with work that
> is not the same work.

Neither corpus touches orderings outside the template. For a brainwallet, order matters
exactly as much as for BIP39 — the same wall, and the position machinery is still what
you would need.

**Control, mandatory here.** A brainwallet has no checksum: every candidate passes the
filter by construction, so a wrong SHA-256 produces a full run of plausible garbage and
reports "exhausted, no match" exactly like a correct run. Nothing else in the pipeline
would notice. 26/26 vectors pass — `correct horse battery staple` under both hashes,
both joins and all three pubkey encodings, plus UPPER and Title casing in spaced and
concatenated form, plus three multi-block phrases at 124 bytes (`len%64=60`, forcing
the extra pad block), 128 bytes (`len%64=0`) and 157 bytes. The canonical vector is 28
bytes, a single block, and cannot reach the multi-block path an 18- or 24-word phrase
needs. Every expected address was computed by an independent Python implementation
before being used, so a shared bug could not make the two agree.

Note `battery` and `staple` are not BIP39 words, so the control cannot be assembled
without an arbitrary-word table. That made the table mandatory, not optional.

**Self-validation:** acceptance came out exactly 1.0 — survivors == candidates in both
runs. With no checksum, anything less would mean the filter was silently dropping
candidates, and this is only visible because of the cumulative survivor counter added
during the seam work (§10).

---

### 2.13 [EXHAUSTED, compressed key; 13 of 15 slots path 1 only] Free-one-fixed at 21 words: the branch that was never run

Every t21 sweep before September freed a **gap** — slots 6, 8, 14, 15, 18, 21.
Not one freed an **assigned** slot. An audit of all twenty t21 configs confirmed
it: the only assigned slot ever varied was 20, and only as a two-way
`apple|second` list. Free-one-fixed existed at 18 words and nowhere else.

So "a fixed word is wrong" was not an infeasible branch. It was an untested
one. You do not need to know *which* word is wrong; you iterate over which.

**This matters more than the count suggests.** At p ≈ 0.75 per assigned word:

| assigned words wrong | probability mass |
|---|---|
| 0 | **1.8%** |
| 1 | 8.3% |
| 2 | 18% |
| 3–4 | 46% |

**The spend by branch, computed from the ledger rather than estimated:**

| branch | probability | derivations | per point of probability |
|---|---|---|---|
| a = 0, gap sweeps only (7 rows) | 1.8% | **50,457,931,465** | 28.0 B |
| a = 1, free-one-fixed (13 rows) | 8.3% | **136,372,012,128** | 16.4 B |

So the least likely branch received **1.71× more compute per point of
probability** than the next one. That is real, and it is much milder than it
looked while an uncomputed "roughly 78 billion" was attached to the 1.8% branch —
that figure was 1.55× too large *and* the wrong quantity, being the whole
project's total as of 11 September across every template length, Electrum,
passphrases and t18 free-one-fixed work. It was borrowed from a status snapshot
and relabelled as a branch figure without being computed.

None of this is a criticism of the work — the branch had to be closed, and
closing it is what turns a conjecture into a deduction. But stating it from the
ledger rather than from a recollection is what makes the next decision legible.

**[EXHAUSTED] The deduction, stated at full strength.** Let *a* be the number of
assigned words that are wrong and *g* the number of gap words outside the
54-word pool. The completed runs exclude:

```
a = 0, g = 0                          t21_readme54
a = 0, g = 1                          t21_loo_k, six ways
a = 1, g = 0  (13 slots, 55 cands)    free-one-fixed
```

So **a + g ≥ 2** — the answer departs from the README's reading in at least two
places. One hole remains: `a = 1` at slot 3 (`tower`) or 13 (`moon`), which were
deliberately never freed, or a replacement outside the 55.

**[EXHAUSTED] The hole's first half is now closed.** The two assigned slots
free-one-fixed never freed have been swept, each over the 54-word pool plus its
own table word, with `SLOT 20 apple|second` and all four campaign paths:

| run | survivors | vs 21,308,126,895 ± 145,402 | wall | result |
|---|---|---|---|---|
| `t21_free3` (`tower`) | 21,308,015,749 | **−0.764 σ** | 68.7 h | exhausted, no match |
| `t21_free13` (`moon`) | 21,308,200,613 | **+0.507 σ** | 67.4 h | exhausted, no match |

Both bands were published before either run started and both landed well
inside, so these are clean negatives rather than broken runs. Together they add
**41,841,412,812** derivations to the ledger — not the 42,616,253,790 the two
box volumes sum to, because each overlaps `t21_readme54` by exactly
**387,420,489**, one 55th of its own box: the single combination in which the
freed slot takes back its own table word, at which point the box *is* the
README reading.

So `a + g ≥ 2` is no longer conditional on slots 3 and 13 being untested. It is
conditional only on the universe, which is the next paragraph.

> **This deduction is conditional on the phrase being 21 words, and that is not
> established.** Every run in the table above is a 21-word template, so *a* and
> *g* are defined only over that template. §5 narrows the length to **21 or 24**
> and does not settle between them — the clock's hour hand proves slot 21
> *exists*, which makes 21 a lower bound, not the value. The README's own table
> runs to 24 rows with 21 through 24 blank, so it does not commit to 21 either.
>
> If the phrase is 24 words, `a + g ≥ 2` says nothing, because the quantities it
> counts are not defined over that template. And the 24-word branch is
> effectively untested: the tails carried in §3 come to 3,618,580,262 candidates,
> 14,135,079 derivations, against a space of 2048²⁴. That is not a search, it is
> a rounding error.
>
> **[UNCOSTED] and the floor is worth stating, because figures for this branch
> have been circulating in prose without ever entering the record.** A grep of
> this repository for them returns nothing: they have no home here and never
> did, which is the §10 failure exactly — a number crossing an agent boundary in
> conversation and acquiring authority by repetition. So, computed here and
> pinned: the *cheapest* 24-word variant of the current template adds slots 22,
> 23 and 24 as gaps over the same 54-word pool, giving nine gaps rather than
> six, and keeps slot 20's two readings:
>
> ```
> candidates   54⁹ × 2       = 7,808,611,824,626,688
> derivations  ÷ 256         =    30,502,389,939,948
> wall time    ÷ 11,925,000 cand/s = 7,579 days = 20.7 years
> ```
>
> **The wall time is costed from the CANDIDATE count, not the derivation
> count, and the distinction is a factor of two.** Every rate elsewhere in this
> report is a 21-word rate, where 128 candidates yield one derivation; a
> 24-word template yields one per 256. Taking 30,502,389,939,948 derivations
> and dividing by a derivations-per-day figure from §3 applies a /128 rate to a
> /256 count and halves the answer. The solver enumerates candidates and the
> clock runs on candidates, so candidates are what the hours are computed from.
>
> **That floor is 159× the entire 21-word campaign to date.** The assumption it
> rests on is named rather than buried: it presumes slot 24's word is *in the
> pool*. Anything outside the pool at any of the three new slots multiplies it
> again, and the clock cannot reach 22 or 24 at all (§5), so there is no
> mechanism proposing words for them. The figure is a floor and a loose one.
>
> Read it as: **if the phrase is 21 words, the answer departs from the README in
> at least two places.** The conditional was missing from every earlier statement
> of it, including §4's.
>
> **And a second conditional, which is easy to drop and changes what is left to
> do.** Closing slots 3 and 13 does not make `a + g ≥ 2` unconditional. It makes
> it unconditional **only inside the 55-candidate universe** — the 54-word README
> pool plus each slot's own table word. Outside that universe `a = 1` stays open
> at *every* assigned slot, not merely at 3 and 13, because no free-one-fixed run
> ever offered a slot a word from outside the pool.
>
> That is not a remote possibility. All **34** distinctive words of the Tarot
> word-source hypothesis are BIP39 **and all 34 are outside the 54-word pool** —
> `wheel fortune clock cycle judge trumpet balance scale law legal equal flip
> mirror neck man hope flag gold coin two woman stable uniform hood isolate fall
> crash destroy brave choice face one more real`. Zero overlap, verified against
> the pool. Not one has ever been tested at a filled slot. (`hand` *is* in the
> pool and is excluded from that list; `brave` and `gold` are not.)
>
> So free3 and free13 close the hole's **first** half — wrong word, replacement
> inside the pool. The Tarot configs attack its **second** — wrong word,
> replacement outside the pool. They are complements, not duplicates, and a
> reader who takes the stronger claim will stop looking one branch early.

This is stronger than the earlier statement that "at least one gap word is
outside the pool," which was true but understated: the six leave-one-out runs
already swept each gap across the entire dictionary, so the single-surprise case
was closed six ways over.

**Method.** Each run frees one assigned slot to the 54-word README pool plus
that slot's own table word (55 candidates; 56 at slot 20, which carries both
`apple` and `second`), with the six gaps over the full pool, `second` pinned at
slot 20, on the primary path `m/44'/0'/0'/0/0`.

> **[SCOPE] Thirteen of these runs covered ONE path, and the ledger cannot see
> that.** `tally2.py` never reads `PATH` — it unions word-boxes, so a one-path
> run and a four-path run over the same words are credited identically. Of the
> 33 evidenced runs, **13 ran one path and 20 ran four**, and the 13 are exactly
> the `free*_p1` free-one-fixed set:
>
> ```
> one path  : free1 free2 free4 free5 free7 free9 free10 free11
>             free12 free16 free17 free19 free20
> four paths: readme54, the six loo, swap114, written, pool75, the six black,
>             free3, free13, tarot_j10x20, tarot_j17x19
> ```
>
> **This is a condition on the deduction, not a footnote to it.** The deduction
> below has three legs. `t21_readme54` and the six leave-one-out runs ran **four
> paths**. The third leg — `a = 1, g = 0 (13 slots, 55 cands) free-one-fixed` —
> **is the one-path set.** So:
>
> **On paths 2–4, a single wrong word is still open at thirteen of the fifteen
> assigned slots.** Slots 3 and 13 are the only assigned slots closed on all four
> paths, and only since October 2026.
>
> Every joint `a = 2` config in §2.18 — `j10x20`, `j17x19`, `ink10x20` — was
> chosen on the understanding that `a = 1` was closed. It is closed **on path 1**.
> The report flagged the risk when it adopted staging (break-even `q > 63.4%`,
> "should not be described as comfortable") and then the qualifier did not reach
> the conclusion. If `q` is 80%, a fifth of the probability mass sits on paths
> never searched at those thirteen slots.
>
> **The remaining cost, re-derived rather than carried forward.** The 89 h figure
> in §2.13 below is for **three slots**, not thirteen — the `3 ×` in
> `3 × (P+3X) × 10,654,063,447` is a slot count, and the text declining it says
> "paths 2–4 on three slots". Per slot at `P+3X = 9.794 µs` over 10,654,063,447
> derivations is **29.0 h**, so all thirteen is **377 h ≈ 15.7 days**; at the
> 11,080,699 cand/s measured on `j17x19`, scaled to three paths, **396 h ≈ 16.5
> days**. Closing the `a = 1` branch across all four paths is a two-week job, not
> an 89-hour one.
>
> The ledger's figures are unaffected, because its unit is the checksum-valid
> candidate rather than the derivation performed, and that convention is applied
> uniformly. What is affected is the word *exhausted*: a one-path run does not
> exhaust its box over the path set, and §2.17's slot-11 row saying "freeing slot
> 11 found no candidate fits at all" is a path-1 result.

Staging by path rather than running all four costs **1.565× overhead** against a
break-even at **q > 63.4%**, where *q* is the chance the answer sits on path 1.
Those figures are from production — `P = 6.209 µs` shared, `X = 1.195 µs` per
path, derived from `T4/T1 = 1.484` (see §10) — and they **supersede an earlier
1.18× and 22.8% taken from a microbenchmark.** The decision still goes the same
way for a legacy address under BIP44, where `m/44'/0'/0'/0/0` is the dominant
convention, but it is a much closer call than the original figures implied and
should not be described as comfortable.

The 89 h quoted below for stage 2 reconciles with these numbers to 2%
(`3 × (P+3X) × 10,654,063,447 = 87.0 h`), which is what confirms it as a real
figure rather than a projection.

**Results — thirteen slots freed, all negative.** Each run **21.910 h ± 0.32%**
(six back-to-back runs, measured from checkpoint mtimes), **284.8 h / 11.9 days**
for the campaign. Every survivor count is within 1.1σ of its exact binomial
expectation of **10,654,063,447** (σ = 102,815).

The last four to land were the self-naming slots, run together:

| run | freed | survivors | deviation |
|---|---|---|---|
| `free4` | `mask`@4 | 10,654,138,418 | +0.73σ |
| `free16` | `rifle`@16 | 10,653,972,836 | −0.88σ |
| `free12` | `vote`@12 | 10,654,012,263 | −0.50σ |
| `free19` | `glove`@19 | 10,654,167,169 | +1.01σ |

**[MEASURED] What these four do not establish.** Each asks *"is this word wrong,
and is its replacement among the 55?"* A negative is equally consistent with the
word being **right** and with it being **wrong while the right word sits outside
those 55**. The two do not separate, so four negatives return the status quo and
say nothing about whether the self-naming mechanism is reliable. Only a hit would
have been informative — and a hit would have solved the puzzle outright.

| slot | word | why it was weak |
|---|---|---|
| 10 | `black` | **zero derivation** — rests entirely on the unreadable glyph |
| 20 | `apple`/`second` | freed across all 56, superseding the provenance question |
| 11 | `pyramid` | the contested pyramid / Space Needle slot |
| 1 | `subject` | the README hedges it in writing |
| 7 | `liberty` | canon-assumed; 5 spikes measured directly, 2 inferred |
| 5 | `police` | "line five" needs a convention nothing else in the table uses |
| 17 | `gold` | "17 years" is a chart-span reading, not a count |
| 9 | `eye` | occluded clock position, inferred from the fit |
| 2 | `camera` | the README's own `twin` hedge |
| 4 | `mask` | self-naming — four masked faces |
| 16 | `rifle` | self-naming — M16 |
| 12 | `vote` | self-naming — the `.VS.` ambigram |
| 19 | `glove` | self-naming — the CVD19 vial |

**Two of these settled standing questions rather than merely eliminating
words.** Freeing slot 20 across all 56 candidates **supersedes** the
`apple`-versus-`second` provenance argument — neither works, so the argument is
retired rather than resolved. And `black`@10, load-bearing since 2020 on nothing
but a glyph nobody can read, is now tested rather than assumed.

**Scope, stated exactly.** What is eliminated is "the assigned word at slot *n*
is wrong **and** its replacement is one of the 55 README-derived candidates."
Not "the assigned word at slot *n* is wrong." Freeing to the whole dictionary is
1,216 h per run and was not done.

**Two slots were deliberately not freed.** `tower`@3 and `moon`@13 are **written
on the clock hands themselves**. Freeing them would not test an inference — it
would test whether the puzzle's own labels are wrong, and if they are, no
ordering of sweeps recovers from it. Excluded by choice, not oversight.

**Stage 2 was declined.** Paths 2–4 on three slots costs 89 h and covers 0.33%
of total probability, against 1.4% for the six remaining slots at path 1 — four
times worse per hour, and the lowest-value run on the board. The argument that
justified staging by path is the same one that rules out revisiting those paths.

### 2.14 [EXHAUSTED, compressed key] Two hypotheses the source document itself named

The README hedges exactly twice, and both hedges have now been tested.

**Row 1:** *"Appear in the section 1 (13th) or it could be 14?"* Tested as
`t21_swap114` — `subject` moved from slot 1 to slot 14, slot 1 opened to the
pool, all four paths. 49,589,822,592 candidates, +0.27σ, negative.

This one mattered because slot 14 had already been closed on the image side by
both routes the author used elsewhere: a clustering sweep with a passing control
(45 blobs against a known 44 stars) found no countable object set of size 14,
and a region-by-region review found no written numeral. The README's own
question mark was the only documentary candidate left.

**Row 2:** *"Two cameras. Maybe could be 'twin' word?"* Tested by freeing
slot 2 to 55 candidates including `twin`. Negative.

### 2.15 [TESTED] Letter substitution: one in 331

Does the artwork encode words by drawing objects in place of letters? If it did
at any rate, the substituted letters would be a channel — and the channel would
have to be read before the template could be trusted.

**331 letters were examined glyph by glyph** at ×2–×8 nearest-neighbour, across
every element large enough for a letter-sized object to be identifiable: the
title words, the `FIND THE SEED PHRASE` watermark, the five slogans, the hoodie
text, the BLM card, `FUCK THIS SHIT`, `.VS.`, the seal ring and scroll, the
clock-hand words, the address, the plinth, the ghost text beside the address,
and the Latin line at bottom right. Text of ~5–8 px was screened as blocks only:
the bottom caption, the amendment copy, the pyramid base, the vial label and the
micrography. A letter counts only if a depicted object occupies its place in the
word — outlined, textured, micrography-filled and mirror-written letterforms all
count as written.

**Result: exactly one.** The O of `STOP` is a clenched fist. `SHIT` is fully
lettered — the I is written, not an object — and all ten of the artist's digits
are written.

**One substitution in 331 letters is a one-off, not a system**, and the single
instance is inert besides: neither `stop` nor `fist` is a BIP39 word, so even
reading it yields nothing placeable.

**Why this is `[TESTED]` and not `[EXHAUSTED]`.** The 331 letters examined at
letter level are roughly **half** the artwork's text. The screened regions —
~115 letters of bottom caption, ~179 of amendment copy, 26 on the pyramid base,
3 on the vial, plus the `BRAVE` micrography — come to at least 323 more, so this
census covers 331 of ≥654, about **51%**, at best. Half the letters were never
examined at letter level, which is a finite corpus tried and empty: §0's
definition of `[TESTED]`, not of `[EXHAUSTED]`.

The screening rationale is sound on its own terms — at 5–8 px an object standing
in for a letter could not be identified as an object, so it could not function as
a readable channel for anyone, including the intended reader. That is why the
unexamined residue is unlikely to hold anything. But it is an argument about
**detectability**, not about the hypothesis being false there, and it cannot
carry the tag. An earlier version of this section was filed `[EXHAUSTED]` on the
ground that the census is complete over its stated scope — a justification that
would promote every `[TESTED]` result in this document, since each is complete
over whatever scope it states.

The conclusion survives the weaker tag unchanged: one in 331 is a one-off rather
than a system, and `stop` and `fist` being absent from BIP39 closes the reading
at the other end regardless of how much of the artwork the census reached.

The judgment is visual and cannot be computed. `census_crops.py` regenerates
every view it was made from and prints the table, so it can be re-judged rather
than taken on trust.

---

### 2.16 [MEASURED] Slot 20: the ink cannot decide between `apple` and `second`

**Neither word is in the image.** The letter census (§2.15) found no `apple`,
`second`, `2nd` or `II` in any display lettering. Slot 20 has no glyph group, so
there is nothing to resolve in the ink. It is an *assigned* slot carrying a
two-way list, not one of the six gaps.

**The README disagrees with itself.** Table row 20 gives `apple` with an **empty
description** and no derivation anywhere in the document. §19 instead derives
`second`, in two steps: the number from the `XX` on Leopold's head read as 20,
and the word from the external fact that Leopold II was the second King of the
Belgians — a lookup the enumeration rule excludes.

**[MEASURED] The spacing test.** How widely does the artist space adjacent
characters *within* a word? A glyph is a connected ink component; fragments under
40% of median height are dropped, judged by height and never by gap; gap is the
clear pixels between the closest ink of two neighbours, which measures rotated
text the same way as upright. A set is used only where segmentation yields
exactly the known character count **and** one glyph per box on inspection — both
checks proved necessary, since FUCK and THIS matched their counts by coincidence
(a merged pair plus a sliver of pedestal edge).

Seven sets qualified — SHIT, LIVES, MATTER, STOP KILLING US, NOT ONE MORE,
11.03.20, .VS. — giving **33 within-word pairs**:

| reference | widest gap ÷ height | X marks (0.597, conservative) as a multiple |
|---|---|---|
| SHIT at measured cap heights 70–72 px | 0.128 | 4.7× |
| the artist's own numerals, 11.03.20 | 0.194 | 3.1× |
| all 33 pairs, median 0.182 | — | 3.3× |
| all 33 pairs, widest: IN of KILLING | 0.291 | **2.1×** |

**No letter or numeral pair in the artist's hand is spaced as widely as the X
marks — 0 of 33.** Reading `XX` as the numeral 20 therefore requires a spacing
used nowhere else in the artwork, while the crossed-out-eyes reading is supported
by complete separation. The margin is 2.1× over the single widest pair in the
whole corpus, 3.1× over the artist's own numerals.

**Verdict, stated no more strongly than the measurement supports.** The ambiguity
is in the reading and the provenance, not in the ink: the ink is clear and
contains neither candidate, so it cannot collapse slot 20 to one word. What the
spacing does is *weaken* §19's step from `XX` to the number 20. It does not
formally refute it and this section does not claim to — the distinction matters,
because a refutation would close slot 20 and a weakening only reopens it.

**Consequence for §2.13.** The README table and §19 disagree, and §19's
derivation rests on an excluded lookup. So there is **no README value at slot 20**
to be right or wrong about, *a* is undefined there, and every §2.13 branch claim
must be stated per reading: slot 20 = `second`, and slot 20 = `apple`.

An earlier figure of 6.8× divided by the 87-px search band rather than measured
cap heights, and used SHIT alone as the reference. It is superseded by the table
above. Script: `slot20.py`.

---

### 2.17 [MEASURED] What holds the template up, word by word

Fifteen slots are assigned. They are not assigned equally well, and the
difference has never been tabulated.

| slot | word | what supports the WORD | what supports the SLOT |
|---|---|---|---|
| 1 | `subject` | **written** in the Amendment copy, and carries the census's one underline (§9) | Section 1 numbering |
| 3 | `tower` | **written** on the minute hand | clock 1+2, under a caption that says to add two numbers |
| 13 | `moon` | **written** on the second hand | clock 12+1, same caption |
| 2 | `camera` | depicted | a count of cameras |
| 4 | `mask` | depicted | a count of masked faces |
| 7 | `liberty` | depicted | a count of crown points |
| 9 | `eye` | depicted | pyramid 4+5 |
| 16 | `rifle` | depicted | the 16 of M16 |
| 19 | `glove` | depicted | the 19 of CVD19 |
| 5 | `police` | depicted | "line five" — a convention used nowhere else in the table |
| 12 | `vote` | association only | the `.VS.` ambigram |
| 17 | `gold` | inferred from the chart | inferred from the chart |
| 11 | `pyramid` | depicted | **worse than contested.** The stated conflict is pyramid 5+6 against the Space Needle, but freeing slot 11 found **no candidate fits at all** — *on path 1 only*, over 55 candidates that include `space` but **not** `eye` or `tower`, with slot 20 pinned to `second` (§2.13's path-coverage note). So the problem is not choosing between two words; it is that neither of the two tested is right, and the object's other BIP39 names were never tried |
| 10 | `black` | the rune line `чёрный день номер X`, written as running prose with **no mark of any kind** — unlike `subject`, `tower` and `moon`, the three other ink-supported words, each of which carries a positional marker (n=3, suggestive not conclusive) | the same line, via `номер X` — a glyph §7.4 shows is unreadable |
| 20 | `apple` | README table row, **empty description** | none: §2.16 finds no README value to be right about, and weakens `XX` → 20 |

**Three of fifteen are written in the artwork.** Six rest on counting things.
Three on association or inference. One — slot 11 — is not merely contested
between two readings but has been tested and fits neither. Two rest on nothing
that survives inspection: slot 20 by §2.16 above, and slot 10 on a glyph that
§7.4 establishes cannot be read by anyone, which §2.13 already called
"load-bearing since 2020 on nothing but a glyph nobody can read" — and which
the ink measurement below now detaches at the other end too.

**[MEASURED] Who first claimed each word — no assigned word traces to the
author.** The table above asks what holds a word up in the artwork. This one
asks who first said it. Together they close the loop.

| hint | first posted by | date |
|---|---|---|
| `moon`, `tower`, `real`, `subject` | u/boriserd | 2020-10-12 |
| `Tuesday` | u/hmm_dimasiki | 2021-01-10 |
| `food` | u/meserit | 2021-01-31 |
| `breathe`; `subject` "underlined" | u/Accomplished_Weird36 | 2021-02-02 |

privatekeys.pw copies Minase's list, which is itself tagged "(source reddit)".

**The post, so an outsider can check this rather than take it.** Reddit
submission [`j79zvj`](https://www.reddit.com/comments/j79zvj), titled "Bitcoin
puzzle (2000$)", posted by **u/stsh_n** on **2020-10-08 09:25 UTC** to the
account's own profile, carrying the image
[`i.redd.it/n1x7g8ceaur51.png`](https://i.redd.it/n1x7g8ceaur51.png) — which is
byte-identical to this project's working file, md5
`7710323461a924987eb35c77055e59f6`. The account was created **3 min 48 s**
before the post, carries that one post, has no text body, was never edited, and
wrote **none** of the 273 archived thread comments. Claims about what the author
did and did not say are checkable against those two identifiers; without them
the claim is unfalsifiable, which is what it was until now. The only author text in existence is the title "Bitcoin puzzle
(2000$)" and the artwork, which says **SEED PHRASE**, not passphrase. Nothing
from the author covers word count, wallet or language.

**Community attribution is not community invention, and the two tables are the
only place in this report where both facts about a word sit together.**
`subject` was *claimed* by a Reddit user in October 2020 **and** is
*independently underlined in the ink* (§9) — those are different kinds of fact
and the underline does not become weaker for having been noticed by a
commenter. What the pairing does establish is that every assigned word entered
circulation through a reader, not a source: there is no authorial statement
behind any of the fifteen, and the ink independently supports only three of
them.

**[MEASURED] Being written in the artwork has never once supplied a slot
number.** The artwork's text contains **21 BIP39 words** — `black brave can end
find first future matter more one only order peace phrase picture police real
seed this welcome world`, from the transcription of record in
`slogan_lines.py`. The template assigns exactly **two** of them, `black` and
`police`, and neither draws its *slot* from being written: `black`@10 comes from
the rune line and `police`@5 from "line five". The other nineteen hold no slot
at all.

Conversely the three words that *are* positional labels — `subject` in the
Amendment copy, `tower` and `moon` on the clock hands — get their slots from
Section-1 numbering and clock sums, not from the writing either. **In both
directions the ink supplies words and the mechanism supplies numbers, and the
two have never met.** `food` is worth naming for the same reason: it is a BIP39
word, it is in the 54-word gap pool, and it is not a template slot word at all —
a community hint (§above) rather than an assignment.

**The parity split is not a coincidence, and it has not been written down.** §5
proves the clock — the one mechanism the artwork captions — yields odd slots and
nothing else. §5 already draws the consequence for the *open* even slots: they
need a count or a written number, and the source document supplies neither. The
same holds for the **filled** even slots:

```
odd  slots  1 3 5 7 9 11 13 17 19    ink-supported: subject, tower, moon
even slots  2 4 10 12 16 20          ink-supported: NONE
```

Slots 2, 4, 10, 12, 16 and 20 are assigned entirely on counts that someone
noticed and nobody validated. **No word at an even slot is written in the
artwork.**

**And that half is the half that cannot be afforded.** Free-one-fixed covered 13
of 15 slots over 55 candidates each — 55/2048, **2.7% of the dictionary**.
Testing one assigned slot against the whole dictionary means 2048 × 54⁶ × 2
candidates, because freeing an assigned slot leaves six gaps pooled rather than
five:

| | derivations | wall time |
|---|---|---|
| one slot, 55 candidates (what was done) | 21,308,126,895 | 2.6 days |
| one slot, full dictionary (what would settle it) | 793,437,161,472 | **98.6 days** |
| all six even slots, full dictionary | — | **1.6 years** |

Wall times at **11,925,000 candidates/s**, the mean of the five hot-started
black runs of 27–28 September (§3); they scale inversely with any future rate.

So the project's boundary is not compute in general. It is this: **the half of
the template resting on an unstated mechanism is the half that would take a year
and a half to check**, and the branch that would matter most — slot 10, whose
support is a glyph nobody can read — is ninety-nine days on its own.

**[MEASURED] The ink treats `на чёрный день` as ordinary running prose.**
`idiom_ink.py` segments the right-edge column and measures whether `чёрный день`
is set apart from its neighbours in any way the ink can express:

- **Not by size or weight.** Across glyph height, glyph width, ink pixels per
  glyph and ink darkness, every z-score for `чёрный` and `день` is within
  **±0.76** of the column mean.
- **Not by separation.** The column has **seven** separators, all the same
  three-dot glyph at x ≈ 1534 / 1542 / 1551, sitting at *every* adjacent word
  boundary — `чёрный | день` included, treated exactly like every other pair.
  The clear rows flanking them (6/4 and 6/2) sit inside the column's own 2–9
  range. No punctuation marks the comma the plaintext would need.
- **Not by annotation.** There is no ink beside any word in the column. The one
  non-zero reading, 80 px beside `номер`, is the CCTV camera's body.

The only word that *is* distinguished is `номер X`, and in the opposite
direction: three of its four comparable letters are 21–36% shorter than the same
letters elsewhere in the column (`н` 15 against 19–22, `о` 12 against 16–18, `р`
14 against 20–22, while `е` at 17 is one row *taller*), its letter gaps are 1–2
rows against a column median of 3.5, and the separator before `X` has the
tightest dot spread in the column at 12.7 px against 15.0–18.4. These are the
last words before the frame, so this is the signature of **running out of room**,
not of emphasis.

The other two inscriptions use the same system: five separators for five
within-line word boundaries top-left, two for two on the clock, all three-dot,
none grouping words. Per-word size there varies by *line*, not by word.

> **The limit, which the measurement states itself.** The ink encodes words and
> nothing above them, so it would look identical if `чёрный` *were* being named.
> This cannot supply positive support for the idiom reading. What it establishes
> is that **nothing in the ink supports the naming reading** — and under §9's
> simplicity criterion, running prose makes the idiom the simpler reading.
>
> Under it the rune supplies neither half of slot 10's row: `чёрный` is part of
> a fixed phrase naming nothing, and `номер X` is an identifier. `black` is
> still written in BLACK LIVES MATTER, but that assigns it no slot.

Verified independently before being entered: bundle sha256 `dc4da37f…7b05a`,
31 of 31 manifest entries OK, and a local re-run of `idiom_ink.py` is
byte-identical to the bundled `expected_output/idiom_ink.txt`.

---

### 2.18 [TESTED] Tarot word-source: the two Roman-numeral slots, jointly

Read each Major Arcana number as a slot: card **X** (Wheel of Fortune) at slot
10, card **XX** (Judgement) at slot 20. Those are the artwork's only two
Roman-numeral marks, and §2.17 ranks them the two weakest rows in the table —
slot 10 with no slot derivation at all, slot 20 with no README value to be right
about (§2.16).

`t21_tarot_j10x20` ran both jointly, which matters: the single-slot configs can
only hit under `a = 1`, and §2.13's deduction says the answer must have at least
two faults. **This is the first config in the project able to hit under
`a = 2`.**

```
slot 10   black | wheel | fortune | time | clock | cycle
slot 20   second | apple | judge | trumpet
space     595,077,871,104 candidates   (24 combinations x 54^6)
survivors 4,649,028,117   vs 4,649,045,868 +/- 67,917   =  -0.261 sigma
wall      14.28 h   11,572,212 cand/s   (0.970x the black-run mean)
result    exhausted, no match
```

Band published before the run; the count landed at −0.26 σ and acceptance at
1/128.0005. A clean negative.

**What it does and does not close.** It adds **4,067,915,134** derivations to the
ledger, not its full 4,649,045,868: the box overlaps earlier work by
**581,130,734**, exactly one eighth, three of its twenty-four slot combinations
having been reached before. One cause is visible in the config and worth
recording — `time` is a **54-word pool word**, the only one of these ten, so
slot 10 = `time` was already reachable by any run that swept that slot. The
brief's claim that all 34 distinctive Tarot words lie outside the pool holds for
its own 34-word list; this config's slot-10 list is not a subset of it.

**The second joint config, and the only link with authorial text behind it.**
`t21_tarot_j17x19` tested Star (XVII) × Sun (XIX): `hope` at 17 against the
author's own runes reading `Я надеюсь` — *I hope* — with `gold` free to move to
19, since the Sun is gold in alchemy. Every other card-to-word link in the
hypothesis is a reader's construction; this one is not.

```
slot 17   gold | hope | flag        slot 19   glove | gold
space     148,769,467,776 candidates   (6 combinations x 54^6)
survivors 1,162,271,630   vs 1,162,261,467 +/- 33,959   =  +0.299 sigma
wall      3.73 h   11,080,699 cand/s
result    exhausted, no match
```

It adds **968,551,222** derivations, not its full 1,162,261,467: one of the six
combinations is slot 17 `gold` × slot 19 `glove`, which **is** the README
reading, so a sixth of the box sits inside `t21_readme54`. Predicted from the
config before the run and confirmed at exactly 1/6 by the ledger. This is a
different overlap mechanism from `j10x20`'s — that one came from a pool word in
the candidate list, this one from the config necessarily containing the template
reading it varies around.

Two limits this config does **not** cover, since the brief pinned them. `SLOT 20`
is fixed to `second`, so if slot 20 is `apple` *and* 17 or 19 is wrong, the run
misses — §2.16 having established there is no README value at slot 20 to be
right about, that is a real gap, and the free-one-fixed runs used `apple|second`
precisely to avoid it.

**Why these two negatives are worth more than their size.** The branch was tested
at its **strongest point first**. Slots 10 and 20 are the two weakest rows in
§2.17 — one with no slot derivation at all, one with no README value — and they
carry the artwork's only two Roman-numeral marks, which is the whole mechanism
the hypothesis proposes. `j10x20` was also the first config in this project able
to find a **two-word** fault, which is what §2.13's deduction requires. It
returned −0.26 σ and empty. `j17x19`, the one link with the author's own writing
behind it, returned +0.30 σ and empty.

What remains of the branch is weaker cases at higher cost: `j12x16` is ~24 h, and
the eleven single-slot configs total ~30 h and can only find a one-word fault
outside the 55-candidate universe. A hypothesis that fails at its strongest
configuration is not refuted, but the order in which it was tested is what makes
these two negatives informative rather than merely two more rows.

**[TESTED] The author's own ink at the two worst slots.** §2.17 measures that 21
BIP39 words are written in the artwork, that the template assigns two of them,
and that neither draws its slot *number* from being written. Seven of the
nineteen written-but-unslotted words are 54-pool words and so were already
reachable at gap slots. The remaining **twelve** had never been testable at a
filled slot: `brave can end find matter more one phrase picture real seed this`.

```
t21_ink10x20   slot 10  black + the twelve      slot 20  apple|second
               644,667,693,696 candidates
               survivors 5,036,361,073  vs 5,036,466,357 +/- 70,690  =  -1.489 sigma
               15.66 h, exhausted, no match
```

This is the author's ink rather than a reader's construction, and it is the
experiment §2.17's own measurement points at — the ink supplies words, the
mechanism supplies numbers, and this asked whether the ink supplies the word at
a slot whose number comes from elsewhere. It does not.

**[TESTED] Slot 11 under the Space Needle's own names.** Slot 11 is the one slot
§2.17 reports as fitting *nothing*. The Space Needle's original 1962 revolving
restaurant was "the Eye of the Needle"; `eye` is BIP39, `needle` is not. The run
that produced "no candidate fits at all" offered 55 words containing `space` but
**not** `eye` or `tower`, with slot 20 pinned and on **path 1 only** — so the
object's two other BIP39 names had never been tried there.

```
t21_needle11   slot 11  pyramid|eye|tower       slot 20  apple|second
               148,769,467,776 candidates, four paths
               survivors 1,162,265,233  vs 1,162,261,467 +/- 33,959  =  +0.111 sigma
               3.71 h, exhausted, no match
```

The supporting claim that the 1962 restaurant rotated once per hour, matching the
minute hand that carries `TOWER`, is **unresolved** — sources disagree and the
1962 figure could not be reached — and was not offered as evidence. The lead
stood on the restaurant's name alone. One limit remains: `eye` is assigned at
slot 9, so a true *eye-moves-to-11* hypothesis is `a = 2` and this did not cover
it.

**[TESTED] Two cells no previous run had entered.** Both cheap, both closing
holes left by earlier configs' pinned slots rather than proposing new readings.

```
t21_amend1415    slots 14+15 = the 19 BIP39 words of the 14th/15th Amendments
                 6,139,206,432 candidates, slot 20 apple|second, four paths
                 survivors 47,972,096  vs 47,962,550 +/- 6,898  =  +1.384 sigma
                 9.03 min, exhausted, no match

t21_flag6_apple  slot 6 = flag|banner|nation|state|eagle|field|glory|salute
                 3,673,320,192 candidates, slot 20 apple, four paths
                 survivors 28,697,967  vs 28,697,814 +/- 5,336  =  +0.029 sigma
                 5.67 min, exhausted, no match
```

`flag6_apple` has **zero** overlap with anything already run, and the reason is
instructive: `t21_loo6` swept slot 6 over all 2048 words but **pinned slot 20 to
`second`**, so flag-words at 6 crossed with `apple` at 20 was unreachable. The
pinned slot that §2.16 argues against left a real hole, and this is it closed.

`amend1415` enters a cell neither `loo14` nor `loo15` could: each swept its own
slot with the other in the pool, so non-pool words at **both simultaneously** had
never been placed. Its overlap was predicted before launch at 76/722 = 10.53% and
measured at exactly **76.00/722**. Two of the nineteen amendment words — `life`
and `power` — are 54-pool words, which is why the figure is 76/722 and not
72/722.

**The boundary as it stood when this section was written.** Thirty-seven runs,
243,641,342,961 derivations, about 7,050 CPU-days, and no anomaly anywhere —
every survivor count inside 1.5σ of its band, most inside 1.0, with §3's
correlation caveat against reading that as 37 independent confirmations. §2.19's
mirror campaign has since taken the ledger past it; this paragraph records the
state at which the *compute-branch* argument was made, not the current total.

- The Tarot branch was tested at its two strongest points: the only two
  Roman-numeral slots jointly, and the only card-to-word link with authorial
  text behind it. Both empty.
- The author's own ink at the two worst-supported slots. Empty.
- Slot 11 under the names of the object it supposedly depicts. Empty.
- **Every remaining compute branch costs more per unit of probability than
  anything already run.** Stage 2 across thirteen slots is 377 h for ~1.4% —
  about 264 hours per percentage point. `j12x16` is ~26 h for a case weaker than
  two that already returned empty. The eleven single-slot configs can only find a
  one-word fault inside a universe already swept on path 1.

What is left is not a compute problem, and the evidence has pointed this way for
a week:

| open question | status |
|---|---|
| glyph **X** | measured; Cyrillic, Arabic, Church Slavonic **and Elder Futhark** all eliminated. Still unread. A key is missing, not pixels (§7.4). |
| **slot 11** | fits nothing. Not contested between two readings — nothing tested fits. |
| **slot 21** | the hour hand names a slot and leaves it empty (§5). |
| **even slots** | 0 of 12 ink-supported, pre-registered and measured (§2.17). |

`[TESTED]`, not `[EXHAUSTED]`. These are constructed hypotheses about the
artwork's numbering and word sources, not statements the author made.

---

### 2.19 [EXHAUSTED, both slot-20 readings; `second` on compressed key only] One gap slot over the whole dictionary, every gap in turn

The largest single block of work in this project had one line of credit in §2.13
and no section of its own. Read across the six configs, `@FULL` rotates through
the gap set — **slots 6, 8, 14, 15, 18, 21, one per run, each exactly once** —
with the other five gaps on the 54-word pool. That is not six scattered runs. It
is a complete single-free-slot sweep of the gap set, and it closes
**`a = 0, g = 1` for every gap**: no assignment wrong, exactly one gap word
outside the pool, at any of the six positions, over the entire 2048-word list.

| run | `@FULL` at | candidates | derivations | paths |
|---|---|---|---|---|
| `t21_loo6` | slot 6 | 940,369,969,152 | 7,346,640,384 | 4 |
| `t21_loo8` | slot 8 | 940,369,969,152 | 7,346,640,384 | 4 |
| `t21_loo14` | slot 14 | 940,369,969,152 | 7,346,640,384 | 4 |
| `t21_loo15` | slot 15 | 940,369,969,152 | 7,346,640,384 | 4 |
| `t21_loo18` | slot 18 | 940,369,969,152 | 7,346,640,384 | 4 |
| `t21_loo21` | slot 21 | 1,880,739,938,304 | 14,693,280,768 | 4 |
| **sum** | | **6,582,589,784,064** | **51,426,482,688** | |
| **union** | | 6,458,615,227,584 | **50,457,931,465** | |

**The union has a closed form, so it is checkable by hand rather than on trust.**
Every intersection of two or more of the six boxes is the *same* set: all six gaps
in-pool with slot 20 = `second`, which is `54⁶ = 24,794,911,296`. A point outside
that set lies in at most one box. So the inclusion–exclusion collapses to

```
union = sum - 5 x 54^6
      = 6,582,589,784,064 - 123,974,556,480
      = 6,458,615,227,584      <- matches tally2.py to the candidate
```

and the difference is exactly `5.0 × 54⁶`. This is the sharper form of "every
pair shares a sub-box": it is not only pairs, it is every higher intersection
too, all collapsing to one set.

**Marginal contribution to the campaign: 49,258,867,709 derivations.** That
figure is stable and is the one to quote: the `apple` mirrors take `SLOT 20
apple` and are therefore disjoint from these six boxes, so nothing the mirror
campaign adds can erode it. What does move is the *fraction*, because the mirrors
grow the denominator — 20.2% of the 243,641,342,961 headline when this section
was written, 18.6% of the 264,843,181,656 it stands at now, and lower again when
the last two mirrors land. Either way it is close to a fifth of everything this
project has computed, recorded until now as a single table row.

**The conditionals, stated the way §2.13 states its own.** This is `[EXHAUSTED]`
over its box and the box has four walls:

1. **Slot 20 is pinned, and this is in the heading because it halves the claim.**
   Five of the six take `SLOT 20 second`; only `t21_loo21` carries
   `apple|second`. So:

   | slot 20 reading | `a = 0, g = 1` closed at |
   |---|---|
   | `second` | slots 6, 8, 14, 15, 18, 21 — **all six** |
   | `apple` | **slot 21 only** |

   §2.16 established there is no README value at slot 20 to be right about, so the
   two readings are **equally live**. The strongest structural claim in the
   campaign therefore covered half the space its original heading implied.
   `t21_flag6_apple` nibbled one cell at slot 6 — eight words, not 2048 — and the
   rest was open.

   **This is how the family went unbanked for two months**: a true statement filed
   under a heading that implied more. The tag now names the reading.
2. **The other five gaps are assumed in-pool.** Each run frees one gap to 2048
   and leaves the rest on the 54-word pool. Two gap words outside the pool
   simultaneously is `g = 2` and is not covered here.
3. **All assignments are assumed correct.** `a = 0` is the premise, not a result.
   The `a ≥ 1` branches are §2.13's.
4. **Path coverage is uniform and complete.** All six ran **four paths**
   (`m/44'/0'/0'/0/0`, `m/0'/0/0`, `m/0/0`, `m/44'/0'/0'/0/1`) — unlike the
   thirteen `free*_p1` runs, which ran one. So unlike §2.13's third leg, this one
   carries no path caveat: there is no staging unevenness across the six.

**[EXHAUSTED] The mirror campaign is complete. All five negative.** Band for
every one: 7,346,640,384 ± 83,971, stratified because slot 21 is `@POOL`.

| run | survivors | Δ | σ | wall | rate |
|---|---|---|---|---|---|
| `t21_loo6_apple` | 7,346,697,647 | +57,263 | **+0.682** | 23.17 h | 11,275,419 |
| `t21_loo8_apple` | 7,346,560,690 | −79,694 | **−0.949** | 22.52 h | 11,598,194 |
| `t21_loo14_apple` | 7,346,605,249 | −35,135 | **−0.418** | 23.38 h | 11,172,403 |
| `t21_loo15_apple` | 7,346,589,918 | −50,466 | **−0.601** | 23.38 h | 11,174,261 |
| `t21_loo18_apple` | 7,346,544,828 | −95,556 | **−1.138** | 23.38 h | 11,170,545 |

Mean z **−0.485**, Var(z) 0.505 over five draws — which tests nothing, for the
reason §3 gives about six. Each was admitted to `EVIDENCED` on completion and on
landing inside its band, which is §10's rule, not when its file appeared.

**`a = 0, g = 1` is now closed for *both* slot-20 readings at every one of the
six gap slots: 6, 8, 14, 15, 18 and 21.** Slot 21 came with `t21_loo21`, which
carried `apple|second` from the start; the other five are these mirrors. The hole
this section's heading correction exposed on 8 October — an `[EXHAUSTED]` tag
covering half the space it implied — is closed end to end.

**What that costs and what it buys.** 110 hours of wall clock across 8–13
October, for 7,077,598,377 derivations at the largest marginal and ~7.05 billion
at the smallest. The claim it upgrades is the strongest structural statement in
the campaign: **no assignment wrong and exactly one gap word outside the pool is
eliminated at every gap, over the whole 2048-word list, on all four paths, under
both readings of slot 20.** No conditional on slot 20 remains.

**[SCOPE] How the campaign was costed and launched.** Five mirror runs —
`t21_loo6/8/14/15/18_apple`, exact copies of their parents with `SLOT 20 apple`
and nothing else changed (verified by diff: one line, line 50, in each) — started
2026-10-08.

```
7,346,640,384 derivations each, 36,733,201,920 gross
marginal to the campaign union  35,354,776,826   = 14.5% of the headline
21.9 h per run at 11,925,000 cand/s   109.5 h for five   ~7.6 h per point
24.2 h per run at 10,800,000 cand/s   120.9 h for five   ~8.3 h per point
```

**The 14.5% is attributable, not asserted — and the attribution is tested in
candidates, where the box algebra is exact.** Derivation counts are
`candidates / 128` and they floor, so two correct quantities can differ by one
and an identity can appear to hold when it has only been checked to a rounding
step. Nothing below is divided until the last line.

```
closed form, 5B - 5 x 54^6      4,577,875,289,280 candidates
marginal m0, full EVIDENCED      4,525,411,433,760
gap to explain                      52,463,855,520
```

Resolved by leave-one-out — dropping each evidenced run in turn and seeing which
move the marginal — rather than by argument:

| dropped run | moves the marginal by (candidates) |
|---|---|
| `t21_pool75` | **48,212,327,520** |
| `t21_flag6_apple` | 3,673,320,192 |
| `t21_amend1415` | 578,207,808 |
| **sum** | **52,463,855,520 — the gap, exactly** |

`t21_pool75`'s term has an independent closed form that matches to the
candidate: `5 × (75 × 54⁵) − 5 × 54⁶ = 48,212,327,520`. `t21_flag6_apple`'s move
is its **entire** 3,673,320,192 candidates, because it is a strict subset of
`t21_loo6_apple`.

Only three runs move it. In derivations the gap is `52,463,855,520 / 128 =
409,873,871.25`, and that fractional quarter is what made an earlier draft of
this section quote the `pool75` term as both 376,658,808 and 376,658,809 in the
same page — two floors of one number, asserted to be equal.

**The table is provably complete, which is why three numbers adding up can be
taken at face value here.** A sum of individual leave-one-out moves is *not* in
general the joint move — if the three overlaps touched each other, each run's
unique contribution would be smaller than its share of the union, so
`Σ unique < |union|` and `m₀ + Σ` would **undershoot** the closed form. In
candidates it lands on it exactly:

```
m0 + sum of moves = 4,525,411,433,760 + 52,463,855,520 = 4,577,875,289,280
closed form, 5B - 5 x 54^6                             = 4,577,875,289,280
```

**An exact identity on integers, with no tolerance.** That proves two things at
once: the three overlaps are **pairwise disjoint**, and **no fourth run touches
the mirror space at all** — a run whose overlap sat inside `pool75`'s would have
shrunk `pool75`'s unique part and broken the identity.

An earlier draft ran this test in derivations, where it read 35,764,650,697
against 35,764,650,697.5 and was described as landing "exactly." That was a match
of **floors**, and it proved only "no overlap larger than about 128 candidates"
rather than no overlap. The conclusion survived — the smallest structurally
possible overlap here is vastly larger than 128 candidates — but the claim of
exactness did not. In candidates it is now what it was said to be.

`t21_pool75` is the main term: a 75-word pool at the gaps intersects each mirror
in `75 × 54⁵` rather than `54⁶`. `t21_flag6_apple`'s move is its **entire
volume**, because it is a strict subset of `t21_loo6_apple` — identical in every
slot but 6, where its eight flag words sit inside the mirror's full 2048. So that
run is wholly re-covered by this one.

Two errors were made in explaining this gap, and both are the same error.

An earlier draft attributed it to the five mirrors overlapping *each other*. That
cannot be right: the inter-box term appears in **both** the estimate and the
measurement, so it cannot be their difference. And a closed form offered for the
`pool75` term was short by exactly that same term:

```
in candidates:   5p - 5 x 54^6 =  48,212,327,520   <- correct, matches exactly
                 5p - 1 x 54^6 = 147,391,972,704   <- what was computed
                 difference        99,179,645,184   = 4 x 54^6
```

The missing piece is `4 × 54⁶`, the inter-box term — dropped from a formula
within the hour of being dropped from the prose, in a correction of that same
prose. §10 files both under one rule rather than as two anecdotes.

For comparison, stage 2 — rejected as the worst value on the table — is **264
hours per point**. This is roughly **35× better**, and it is the lowest-risk
branch available because it is not a new hypothesis: it is the exact mirror of
work already paid for, so it inherits that work's prior rather than needing one
argued for it. **The slot-20 ambiguity is in the template, not something we
invented.**

**Why this is worth more than it was credited.** A coverage statement says what
is ruled out. `a = 0, g = 1` being closed at every gap on all four paths is the
strongest single structural claim in the campaign, and it is what makes the
`a ≥ 1` work in §2.13 and the joint `a = 2` configs in §2.18 the right next
places to look rather than arbitrary ones.

---

**[INFERRED] From this point, every remaining hypothesis is one we construct,
not one the document offers.** That is a different epistemic footing from
everything preceding it, and the distinction is worth preserving: earlier
negatives eliminated readings someone could point at; later ones eliminate
readings we invented.

## 3. Tally

**The tally is computed, not maintained.**

It had been kept as a running sum with per-change patches, and it drifted. Two
independent reconstructions on 23 September differed by 331 M, and tracing the
gap showed **both** were wrong: one used the solver's *reported* per-run
expected value instead of exact `space/128` (+194 M), the other omitted ~1.14 B
of runs. Neither was reproducible from its own inputs.

The deeper defect was double-counting. Every run on the same template shares
the all-pool core, so summing counts that core once per run — **3.72%** of the
naive total across the t21 campaign. Of the twelve older t21 runs, **37% was
already covered** by newer sweeps.

`tally2.py` replaces the sum. It parses the run configs directly — so a row
cannot drift from the config it claims to describe — and computes the union by
box disjointification with real set intersections. Run it as
`python3 tally2.py configs`.

```
t21 campaign, 42 evidenced runs     278,996,119,787 derivations
+ the twelve older asserted runs    282,171,117,443
    marginal of the twelve          3,608,896,368
    at 400 derivations/s            8,165 CPU-days
```

**The seven runs added on 27–28 September are why the union matters.** Six were
the black-relocation sweep and one a pool expansion. Added as boxes they
contribute **4,190,694,419** derivations; added as a sum they would contribute
5,105,437,240. The 914,742,821 difference is entirely `t21_pool75`; the six black
runs overlap nothing and contribute their full 387,420,489 each. An addition would
have overstated the total by 0.48% and there would have been nothing in the
arithmetic to reveal it.

**Where pool-75's overlap actually comes from.** Containment of the earlier
pool-54 box is the obvious mechanism and it is not the main one. Marginal
coverage of pool-75's 2,780,914,306, taken from the box definitions:

```
t21_readme54     387,420,489   cumulative   387,420,489   13.93%
t21_loo21        150,663,523                538,084,012   19.35%
t21_loo6          75,331,761                613,415,774
t21_loo8          75,331,761                688,747,536
t21_loo14         75,331,761                764,079,297
t21_loo15         75,331,761                839,411,059
t21_loo18         75,331,761                914,742,821   32.89%
```

`t21_readme54` — the pool-54 run pool-75 strictly contains — accounts for
387,420,489, or 13.93%. The remaining **527,322,332 (18.96%)** is the six
leave-one-out runs, which each swept a gap over all 2048 words and so reach
into pool-75 wherever the rest of the template agrees. The fourteen
free-one-fixed boxes, `t21_swap114` and `t21_written` add **nothing** beyond
what the leave-one-out family already covers.

`t21_loo21` contributes exactly twice the marginal of each of the other five,
and the reason is in the configs, not in any symmetry: `t21_loo21`, `t21_readme54`
and `t21_pool75` all take `SLOT 20 apple|second`, while `t21_loo6/8/14/15/18`
pin `SLOT 20 second`. Two words against one, at one slot, is a factor of two in
the intersection. A uniformity assumption across the six would have been wrong
by that factor — which is why these are computed from the box definitions.

**All three public-key encodings are hashed, so the address-representation
question is closed.** Every derived key is serialised three ways and each is
hashed and compared: compressed (33 B, `0x02`/`0x03`), uncompressed (65 B,
`0x04`) and hybrid (65 B, `0x06`/`0x07`, SEC1 2.3.3). One EC multiply feeds all
three — y is already in hand for the parity byte — so the cost is two extra
SHA-256 + RIPEMD-160 per key. `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ` carries
version byte `0x00`, so it is P2PKH: neither P2SH-wrapped segwit nor bech32 can
be the target. With all three encodings covered, this is **exhausted without
qualification** — not "over the encodings wallets happen to produce".

Three permanent regression configs pin it: `selftest_find.conf`,
`selftest_uncomp.conf` and `selftest_hybrid.conf` are the same phrase at the
same path with the same private key, differing only in serialisation, so any
future miss isolates exactly one code path. All three recover index 2270828.

**The runs before this change were compressed-only, and are not being re-run.**
Measured, not assumed: the pre-patch binary was kept and run against the
uncompressed address of a known phrase, and it exhausted without finding it. So
the 191.3 B carries one scope line — *compressed-pubkey P2PKH* — and that is
sufficient, because BIP32 wallets emit compressed leaf keys at every path
including `m/0/0` and `m/0'/0/0`, while the 2013-era software that produced
uncompressed keys (Electrum v1 old seeds, brainwallets, pre-0.6 Core) never used
BIP32 paths at all. The two populations do not intersect. Everything from here
covers all three regardless, because conditioning the check on that argument
would let the next kernel variant drop back to compressed-only in silence.

**[MEASURED] One run is checkable by an exact identity, not a band — and it
holds.** `t21_loo21` sweeps slot 21 over all 2048 words. A 21-word phrase carries
seven checksum bits, so for any fixed 20-word prefix exactly **16** of the 2048
last words are valid, and they sit **one per 128-block**: word 21's four entropy
bits are the *high* bits of its index. Survivors must therefore equal
`candidates / 128` **exactly, with remainder zero**. There is no band, and any
nonzero delta would be a counting or checksum defect rather than a fluctuation.

```
space               1,880,739,938,304        /128 = 14,693,280,768  remainder 0
counted segment     1,489,897,914,368        /128 = 11,639,827,456  remainder 0
logged survivors                                    11,639,827,456
delta                                                            0
```

**Exact.** This is a stronger validation of the pipeline than any band has given:
an exact structural identity confirmed on a production run, not a tolerance.

**But it covers 79.2% of the run, not all of it, and the reason is worth
recording.** `t21_loo21` was started on the affine binary on 3 September, killed
at 20:25:57 on the 4th, and **resumed on the Jacobian binary** ten seconds later
from its checkpoint. The cumulative survivor counter restarts on resume, so the
logged 11,639,827,456 is the count from the resume point onward. The affine
segment's own total was never printed — that log ends mid-run. The resume index
recovers exactly: `1,880,739,938,304 − 11,639,827,456 × 128 = 390,842,023,936`,
which is **exactly 104 chunks** of 3,758,096,384. So the identity is confirmed on
every candidate the Jacobian binary counted and is simply unrecorded for the
first 104 chunks. Not wrong — uncounted.

**[MEASURED] Bands on slot-21 pool sweeps are 1.67% too wide (σ 1.65%
narrower), and the structure is known rather than assumed.** The binomial band treats each pool word as
independently valid with `p = 1/128`. It is not independent: exactly one word per
128-block is valid, so the count is a sum of **16 independent Bernoullis**, block
*j* contributing `k_j/128` where `k_j` is how many of the 54 pool words fall in
block *j*. Measured from the wordlist:

```
k = [4, 1, 1, 3, 1, 4, 3, 1, 5, 6, 10, 1, 1, 3, 6, 4]     sum 54

variance   binomial 0.418579   hypergeometric 0.407741   stratified 0.404907
sigma      ratio to binomial:  0.986962                  0.983533
```

**Both 1.65% and 1.67% are correct, and they are the same quantity read from
opposite ends** — stated here so nobody "corrects" one into the other later. With
`r = σ_strat/σ_binom = 0.983533`:

```
sigma is NARROWER by   1 - r     = 1.65%
bands are TOO WIDE by  1/r - 1   = 1.67%
```

A z-score computed with the binomial σ is 1.67% smaller than it should be; the σ
itself is 1.65% larger than it should be. Not a disagreement, a direction.

The hypergeometric form knows the valid set has fixed size 16; the stratified
form knows **where** they are, and is the correct one. Rescaled, the project's
widest deviation of 1.489σ becomes **1.514σ**, and `P(all 37 inside)` falls from
0.0044 to 0.0058 — which does not change the conclusion below.

**The correction applies only to runs that sweep slot 21 over a pool.** A run
with slot 21 **pinned** gets none, and a run with slot 21 `@FULL` gets the exact
identity instead. Of the six black runs, five sweep slot 21 over the pool and
`t21_black21` pins `black` there, so it keeps the binomial band.

Applying it to the six, which is the only place in this project with repeated
draws from one box shape:

```
black6  -0.819   black8  +1.053   black14 -0.009
black15 -1.188   black18 +0.509   black21 -1.035  (uncorrected)

mean z -0.2484    Var(z) 0.8305    95% CI from 5 df  [0.324, 4.996]
```

`Var(z) = 0.83` against an expected 1.0, and **1.0 sits inside the interval** —
but the interval spans a factor of fifteen, because six draws carry almost no
power to test a variance. The runs are not suspiciously tight; the sample is too
small to say they are anything.

**[RETRACTED] The underdispersion result.** This section previously stated that
the widest deviation across all 37 runs is 1.489 σ, that
`P(all 37 inside) = 0.0058` after rescaling, and that about five runs should
have fallen outside with zero observed. **That is withdrawn, not corrected.**

It was never a measurement. It was a claim about 37 runs supported by a subset of
them: no complete 37-row table of z-scores exists anywhere in this document, and
the `loo` runs' survivor counts appear in it nowhere at all. A statistic computed
over a population that was never fully measured is the same class of error as the
192,196,843,171 headline — an addition presented as a union.

**The run that exposed it.** `t21_loo6` was resumed mid-space, and the harness
restarts the cumulative survivor counter on resume, so its logged count covers
only the final segment while its expectation was computed over the whole box.
Scored against the full box it is −12,034 σ; scored against the segment it
actually counted it is **+1.802 σ** — larger than the 1.489 the retracted claim
rested on. It did not hide inside a band. **It was never scored**, which is a
hiding place the audit had not considered.

```
t21_loo_rest.log:3   "t21_loo6  (resume from 131533373440)"
resume index         131,533,373,440 = 35.000 chunks of 3,758,096,384   WHOLE
counted segment      808,836,595,712   expectation 6,319,035,904
logged survivors                                   6,319,176,204
z vs segment                                              +1.802
```

**The segment boundary is confirmed by the z, not assumed by it.** One chunk of
boundary error shifts the expected survivor count by `3,758,096,384 / 128 =
29,360,128`, against a σ of 77,883 at this run's scale — **377 σ per chunk**. At
±1 chunk the z would be −375.2 or +378.8. One *candidate* of error moves it by
0.00002. So an ordinary z is only possible at exactly the right boundary: the
same logic as `t21_loo21`'s 104-chunk alignment, where an arbitrary kill point
would not land on a chunk and an arbitrary boundary would not yield a sane z.
This is self-verification, not a caveat.

The five `loo` runs scored for the first time, with the box at 940,369,969,152
candidates (2048 × 54⁵, slot 20 pinned to `second`):

| run | resume | segment expectation | survivors | z |
|---|---|---|---|---|
| `t21_loo6` | 35.000 chunks | 6,319,035,904 | 6,319,176,204 | **+1.802** |
| `t21_loo8` | — | 7,346,640,384 | 7,346,621,056 | −0.230 |
| `t21_loo14` | — | 7,346,640,384 | 7,346,616,393 | −0.286 |
| `t21_loo15` | — | 7,346,640,384 | 7,346,676,192 | +0.426 |
| `t21_loo18` | — | 7,346,640,384 | 7,346,552,717 | −1.044 |

**[MEASURED] The dispersion statement, computed once, from every run.**
`zscore_table.py` scores all 42 evidenced runs from their configs and logs. Each
run's σ comes from **its own** slot-21 word set — per-prefix variance
`Σ (k_j/128)(1 − k_j/128)` over the 16 blocks — so one formula covers all three
models: `@FULL` gives zero variance, a pinned slot gives the binomial, a pool
gives the stratified value for *that* pool. That matters for `t21_pool75`, whose
slot 21 sweeps 75 words, not 54. Survivor lines are matched to runs by name
**and** by the `of <space>` figure, which must equal the box volume. Resumed runs
are scored on the segment they counted.

```
runs 42 = 41 scored with a z + 1 exact identity (t21_loo21)
mean z -0.0587    sample Var 0.6948    sd 0.8335    max |z| 1.802 (t21_loo6)
95% CI on Var, if independent      [0.468, 1.138]   -- contains 1.0
|z| < 1   30   (expect 28.0)
1 - 2     11   (expect 11.1)
>= 2       0   (expect  1.9)
```

**The honest reading is mild, borderline underdispersion — much weaker than the
retracted figure, and not nothing.** Three statistics, side by side, because
which one is quoted changes the impression:

```
IF independent:
P(all 41 inside 1.802)        0.048   <- the SAME statistic as the retracted 0.0058
P(sample Var <= 0.695)        0.072
P(none of 41 beyond 2 sigma)  0.148
```

So p ≈ 0.05–0.15 depending on the statistic. An earlier draft of this paragraph
computed the 0.048 and then wrote "there is no significant underdispersion"
without printing it — leaving out the one number that sat near 5%, which is the
same motivated reasoning §10 records when the option that preserved the stronger
claim was preferred for that reason.

**Overlap pushes the variance down, and was measured rather than argued.** That
same draft said the overlap made underdispersion "harder to establish". It points
the other way. For standardised scores with mean pairwise correlation ρ̄,
`E[s²] = 1 − ρ̄`, so positively correlated runs produce a sample variance *below*
1 and overlap is a candidate **explanation**. `rho_bar.py` computes it from the
box intersections: survivor counts co-vary only through their shared sub-box, so
`Cov(N_A, N_B) = Var(N_{A∩B})`, each variance from that box's own slot-21 set.

```
41 runs, 820 pairs, 434 with any overlap
mean pairwise rho          0.0223
E[s^2] = 1 - rho_bar        0.978
P(s^2 <= 0.695), adjusted   0.086
largest pair                0.5774  readme54 x needle11
```

The largest pair is a closed-form check: `readme54` sits inside `needle11` with the
same slot-21 set and a third of the prefixes, so ρ must be `1/√3 = 0.5774` — and
is. **Overlap accounts for about 7% of the shortfall from 1.0.** It does not
explain the 0.695. The rest is unexplained, at a level that a 41-run sample makes
borderline rather than established.

**What this does and does not touch.** Dispersion tests the σ *models* — whether
the stratified variance correctly describes how survivor counts scatter. It
cannot hide a hit, because the survivor counter is not the hit path: a hit is a
`hash160` comparison inside the kernel and never passes through it.

`t21_loo21` is the one run with no z. It is an exact identity on its counted
segment, but its resume index was never recorded, because the run moved between
binaries. The index is therefore **inferred** from the survivor count — which
makes the residual zero by construction, so the residual is not evidence. The
evidence is that the inferred index lands on **exactly 104.000 chunks**. An
arbitrary survivor count would not.

Building this table found two defects in the tooling that built it, both caught
before any figure reached the page: banner-less single-run logs were being
skipped, which hid `readme54`, `swap114` and `written`; and the first pass at the
statistics counted the table's own summary line as a 42nd data point.

**[SCOPE] What survives of the original point.** The boxes do overlap by design,
so whatever the completed table shows, the counts are positively correlated and
the effective number of independent draws is far below 37. That part did not
depend on the retracted arithmetic.

The explanation is almost certainly not that the pipeline is unusually accurate.
It is that **the boxes overlap by design** — this section's whole purpose is
computing a union because they do — so the survivor counts are positively
correlated and the effective number of independent draws is far below 35. A
candidate counted in `readme54` and again in a `loo` run is not two samples of
anything.

What the bands still do, and it is the thing they were built for: a broken run
blows past 3 σ regardless of correlation, and that is how the `_ModInv`
limb-count bug and the 24-word HMAC omission were caught. Each individual run's
band remains a valid check on that run. What does **not** follow is treating 37
in-band results as 37 independent confirmations of the template — the collective
evidence is weaker than the row count implies, and a reader should not read the
tidiness as significance.

**What "derivations" means here, exactly.** A 21-word mnemonic carries seven
checksum bits, so one sequence in 128 is valid and the ledger reports
`⌊candidates / 128⌋`. **That is a convention, not a count.** The true number of
checksum-valid mnemonics inside a given template is a determinate integer that
nobody has enumerated, and per-run survivor counts scatter binomially around
`N/128` — which is why every run is z-tested against that expectation rather
than required to equal it.

The convention has a rounding choice inside it. `⌊(A−B)/128⌋` and
`⌊A/128⌋ − ⌊B/128⌋` can differ by one, and on an earlier set of figures they did.
They agree on the current ones, for a reason worth recording: the 24-word tails
are now converted at their own checksum width and added *after* flooring,
identically to both totals, so they cancel out of the difference. The rule holds
whether or not it bites — the ledger prints the two totals, so the marginal it
quotes **must** be the difference of the two printed figures or the three numbers
on the page do not reconcile. Floor once, at the point of reporting, and derive
every difference from the reported values.

**The two templates cannot share a divisor.** A 21-word phrase carries seven
checksum bits and converts at 1/128; a 24-word phrase carries eight and converts
at 1/256. An earlier `tally2.py` added the 24-word candidate tails into the
21-word candidate union and divided the whole sum by 128, crediting that work at
**double** its true derivation count: 28,270,158 where 14,135,079 is correct. The
headline was overstated by 14,135,079 derivations, 0.0074%. Numerically trivial,
and structurally the same error as any other — a conversion applied to a
population it does not describe. Each template now converts at its own width
before the totals are added.

**No single grand total is quoted, and that is deliberate.** The previously
published figure (26,513,178,774) was a running sum that already included the
twelve older t21 runs, and whether it counted them at naive size or with overlap
removed is unrecorded. Subtracting them to isolate a pre-t21 residual therefore
rests on an assumption nobody can check — the residual is somewhere between
roughly zero and the whole 26.5 billion.

The t21 figure above **is** computed, and every digit reproduces from
`tally2.py configs`. Adding an unverifiable constant to it would make the sum
less trustworthy than either part. Where one number is needed, **"over 278
billion derivations eliminated"** is a floor that is computed, in preference to
an estimate that is not.

**The headline quotes the evidenced figure, not the combined one.** 278,996,119,787
is the union of the 42 runs whose logs are in this tree; 282,171,117,443 adds the
twelve older runs carried on report alone. The larger number is not wrong, but it
inherits the weaker warrant of its weakest component, and a headline that needs a
footnote about which runs have logs is worse than a smaller headline that needs
none. The previous headline had the same dependency and did not disclose it.

**EVIDENCED versus ASSERTED is deliberate.** Runs with logs present in the
working tree are separated from runs included on report alone. A config is not
evidence that a run happened, and a ledger that reads configs cannot tell the
difference.

An earlier size-based inclusion-exclusion (`tally.py`) is retained. It agrees
with `tally2.py` to the candidate on the declared runs but is **exact only
where the per-dimension sets nest**, which the older runs do not: `readme54`(54)
is not inside `trust21`(69), and `trustonly`'s pool is disjoint from every
other. Taking `min()` there would overstate intersections and so understate the
union — wrong in the flattering direction.

**This supersedes the hand-derived `5·L − 4·R` subsumption note** previously
carried in this section for the t18 leave-one-out family. That formula was
correct for that one family and does not generalise; `tally2.py` computes the
same quantity for every family without a closed form. One method, stated once.

**One tranche is knowingly excluded.** Three runs on 14 August used an earlier
CPU solver (`template_solve.py`, 16 workers) in `~/Downloads/puz2/files/` with
**no config file at all** — the template lived in the Python. All three
completed and exhausted without a match — **138,707,999 derivations**, 0.096% of
the ledger. They are not rows and cannot be: the logs print `37 candidates` per slot
but not *which* 37, and the pool file they were given no longer exists. Without
the pool there is no set, and hand-entering a guessed one would be exactly the
maintained-tally failure this section exists to end. **A run with no config is a
run with no provenance, whatever its log says** — so it is stated here and
counted nowhere.

Those three were invisible to a config-based audit by construction. They were
found by inventorying *logs* instead, which is the dual check and the only one
that can see a run whose config never existed.
## 4. Why more compute will not solve this

The position table has 13 fixed words for t18. Using its own confidence ratings
(high ≈ 0.9, medium ≈ 0.65):

**P(all 13 correct) ≈ 1%. Expected number wrong ≈ 4.**

The all-slots-vary sweep (§2.7) covers every combination of {table word, *my*
alternative} — 8,192 of them, in both schemes. It cannot help if the correct
word at any slot is neither.

And there is a harder structural limit. With ~5 candidates across 24 slots the
space is 5²⁴ ≈ 6 × 10¹⁶, and **being right about 23 words out of 24 pays exactly
nothing** — there is no way to test a partial answer. Candidate lists cannot
converge. Every slot must be pinned to one word by reasoning.

Scale, for contrast:

- 12-word free permutation over 16 candidates: P(16,12) ≈ 8.7 × 10¹¹ — 8 hours
- over 53 candidates: 8 × 10¹⁸ — unreachable
- 24-word, exact words known, order unknown: 24! ≈ 6.2 × 10²³ — **43 million
  years**

**Position information is not an optimization for long phrases; it is the only
thing that makes them solvable.** Which means every 24-word attack inherits
whatever errors its position table contains.

---

## 5. The length argument

The clock is a position machine. Measured rather than eyeballed: all three hands
sit midway between two adjacent numerals, within ~1.5°.

| hand | between | sum | label |
|---|---|---|---|
| seconds | 12 and 1 | **13** | `moon` |
| minutes | 1 and 2 | **3** | `tower` |
| hours | 10 and 11 | **21** | *(blank)* |

The runes beneath decode to `Сумма двух чисел` — "sum of two numbers" — stating
the mechanic outright.

**[MEASURED] The clock can only produce ODD slots.** Consecutive integers *n* and
*n+1* sum to 2*n*+1, always odd; the wrap pair 12+1 = 13 is odd too. So the twelve
adjacent pairs yield exactly {3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23} and nothing
even, ever.

This is consistent with every filled entry in the table: the clock slots (3, 13, 21)
are odd, and every **even** slot comes from a count or a written number instead —
`camera` at 2 (two cameras), `mask` at 4 (four masked faces), `black` at 10 ("black
day number X"), `vote` at 12 (the mirrored `.VS.`), `rifle` at 16 (M16), `apple` at
20 (the XX on Leopold's head — but see §2.16, which measures that XX and finds
it spaced more widely than any letter or numeral pair in the artist's hand).

**Consequence for the unfilled slots.** Of 6, 8, 14, 15, 18, 21, 22, 23, 24:

| | slots | mechanism |
|---|---|---|
| odd | 15, 21, 23 | clock-reachable, but only three hands exist and they are spent |
| even | 6, 8, 14, 18, 22, 24 | **cannot** come from the clock — need a count or a number written in the artwork |

That is a real narrowing: six of the nine open slots are provably outside the one
mechanism the puzzle states outright, and the README's twenty-one sections supply no
count or number that produces any of them. The `.VS.` ambigram adds a fourth: slot **12** → `vote`.

**The clock is not mirrored.** Reading the numerals clockwise gives 8→9→10→11→
12→1→2→3, i.e. increasing. A mirrored face would decrease. The digits merely
look odd because they are hand-drawn along the rim. (This refutes a mirroring
correction I proposed earlier, which would have moved the unknown to slot 3.)

Slot 21 therefore exists, and valid BIP39 lengths are 12/15/18/21/24 — so the
phrase is **21 or 24 words**.

There is a second, independent reason it cannot be 12. At 12 words, order is
brute-forceable: 12! = 479,001,600 arrangements, ~29.9 M after the 4-bit
checksum, which is minutes of compute. **If you had the right twelve words you
would not need the clock at all.** An author who built an elaborate
position-marking system did so because order cannot be searched — which is only
true at 21 or 24.

**[MEASURED] What the wallets of May 2020 emitted by default.** Of the 13
wallets in the [walletsrecovery.org snapshot of
2020-05-29](https://github.com/nvk/walletsrecovery.org/blob/80436a2b98/README.md)
whose *only* Bitcoin path is legacy, 11 could be determined — 9 from source at
the last commit on or before 2020-05-10, 2 from vendor documentation. **All 11
default to 12 words. None defaults to 15, 18, 21 or 24.** Two were not
determinable: KeepKey Client has no pre-May-2020 repository, and Luxstack could
not be found. Every figure is pinned to a file and line in `wallet_defaults.md`.

> **[SCOPE] This supports no prior over phrase length, and the point is worth
> being blunt about.** The population is defined by being legacy-**only**, which
> excludes every multi-path wallet — that is, every 24-word hardware wallet, and
> iancoleman's tool, which defaulted to legacy and **15** words while offering 21
> and 24, and which is not among the 13. "Zero of these produce 21 or 24 by
> default" is true *because the population was built by removing the wallets that
> do.* The snapshot lists supported paths only, with no defaults column, so the
> multi-path wallets could not be read from it at all.
>
> What the measurement supports is one conditional on a branch nobody has
> established: **if the seed came from a legacy-only wallet at its defaults, it
> is 12 words.**

**And the 12-word branch is a package, not a footnote.** If the clock is a
position machine, the phrase is ≥ 21 and the author made a non-default choice —
a longer length than the tool offered by default, or a legacy account on a wallet
whose default is something else. If the clock is *not* a position machine, then
the mechanism, the slot numbers, the template and all 191 billion derivations in
§3 were aimed at a structure that does not exist. **The template and the 12-word
prior cannot both be kept.** Anyone reaching for 12 on the strength of the
wallet defaults is discarding §5, §2.13 and §3 in the same motion, and should say
so.

---

## 6. What would actually help

1. **A key to the glyphs the author invented beyond the Gravity Falls 26** —
   which is also the shortest path to slot 10, and the two are the same request.
   This was previously filed as two separate asks and it is one.

   §2.17 records that `black`@10 is the only assigned slot with **zero
   derivation**: it rests entirely on `номер X`, and §7.4 establishes that X has
   no key entry, occurs exactly once, and is therefore unassignable in principle
   from this corpus — a better scan renders the same two strokes. Meanwhile §9's
   ink measurement finds the column distinguishes **`номер X`** — compressed
   letters, 1–2 row gaps, the tightest separator in the column — and does **not**
   distinguish `чёрный день`, which it treats as ordinary running prose.

   So the one word with no slot derivation depends on the one glyph with no
   reading, and the ink points at the *number* rather than the colour. Resolving
   X does not merely read a glyph; it settles or kills slot 10. Nothing else on
   this list has that property.

2. **A word for slot 21.** The hour hand is produced by the same labelled
   mechanism that gave `moon` (12+1) and `tower` (1+2) at high confidence, and
   it is the only hand with no word on it. Checked at four contrast settings —
   it is a plain wedge, not faint writing.
3. **Anything placing 22, 23, 24.** These have no evidence at all.
4. **Resolving slot 11.** `pyramid` (5+6 in the pyramid) versus the Space Needle
   "marks the 11". Freeing slot 11 found no candidate fits, which suggests the
   conflict runs deeper than a two-way choice. Note also that the CCTV junction
   box bears a pyramid symbol, visually linking `camera` and `pyramid`.
5. **A count or a written number producing slot 6, 8, 14, 18, 22 or 24.** Per §5
   these cannot come from the clock, and the README's twenty-one sections supply no
   mechanism for any of them. This is where the mechanism inventory is actually
   incomplete.

   **[MEASURED] The flag carries 44 stars and 13 stripes.** Star count by
   connected-component analysis inside the canton — every star located, two
   clipped at the fold, visually verified against the detection. Stripe pattern
   `KRTKRTKRTKRTK`: 13, canonical. The flag's only anomaly is the star deficit.

   **50 − 44 = 6**, and 6 is an open even slot. That is a deficit in a
   deliberately-drawn flag, the same kind of count as "four masked faces", and it
   needs no invented operation. (Digit-summing 44 → 8 was proposed and is
   withdrawn: the artwork nowhere identifies digit-summing as an operation, which
   acceptance criterion 5 forbids.)

   **[TESTED] The flag reading is negative.** `flag`, `banner`, `nation`, `state`,
   `eagle`, `field`, `glory` and `salute` are all BIP39 and none has ever been in a
   gap pool, so only an `@FULL` sweep could reach them — and until 2026-09-01 the
   `@FULL` sweep at slot 6 was the weak one (§2.3). `t18_loo6.conf` swept slot 6
   over all 2048 words with the current pool and all four paths. Empty. The chain
   was coherent and it is closed.

6. **[MEASURED] A larger source image, for one specific reading: the circled
   mark on the BLM card.** This is the only place in the artwork where the file's
   resolution genuinely blocks a reading, and the claim is measured rather than
   asserted.

   The circle was fitted as the ring darker than both its inner and outer
   neighbours: centre (263.5, 760.5), **diameter 17.5 px**, interior mark 13×10 px.
   A stroke narrower than one pixel never reaches the pen's full darkness, so
   (background − darkest) ÷ (background − pen) estimates the widest stroke. With
   background 222 and pen 29, both taken from the BLM capitals on the same card:

   | feature | darkest pixel | peak stroke coverage | px past half-pen |
   |---|---|---|---|
   | interior mark | 76 | **0.76 px** | 17 |
   | ring | 118 | **0.54 px** | 2 |
   | BLM capitals, same card (legible control) | 29 | full | 135 |
   | rune glyph (resolved control) | 0 | full | — |

   Both strokes are **sub-pixel**. Strokes that narrow merge, so a junction and a
   near-miss render identically and the mark's topology cannot be recovered from
   this file at all.

   **It is not the STOP fist drawn small.** That emblem box-averaged down to 18 px
   keeps **74** pixels below 90; the card mark has **4**. At this size a
   line-drawn fist, a circled A and similar shapes are indistinguishable.

   Sub-pixel strokes are what a larger working file produces when downsampled, so
   such an original probably exists — which is the reason to want one.

**Deprioritised, with reasons:**

- **A larger source image, for the rune glyph.** The glyph is not pixel-blocked:
  §7.4 measures it at 13×20 px, 96 ink pixels, strokes 3–4 px wide, 248 levels
  of contrast, 4 clear rows to the border above it and 5 to the separator below,
  and no ink in the titlo band — complete, untruncated, carrying no numeral mark. Its shape is
  fully resolved and a better scan renders the same two strokes. What is missing
  is a **key** — the author invented glyphs beyond the 26 Gravity Falls supplies,
  and X occurs once, so there is no second instance to triangulate from. Per §2.9
  no larger source is served anyway: `i.redd.it` returns the same 1600×1200 file,
  md5-identical. The circled mark above is a separate case and the only real one:
  **a higher-resolution source can unblock one reading, not two.**
- **More compute against the current template.** It is exhausted. A corrected
  template can be tested in seconds; an uncorrected one cannot be rescued by scale.

---

## 7. The rune cipher is solved — it is Cyrillic, not Greek

### 7.1 Both circulating decodes are wrong at the premise

- **"HELLO : FROM : THEM"** is **internally impossible**: it reads Φ as **H** in
  "HELLO" and as **M** in "THEM". A substitution is a function; one glyph cannot
  have two values. It also carries no word, index or position.
- **Greek QWERTY** yields `FLNND : 4ZDX : 7CUF` — a real mechanism, but the
  output is not English, not BIP39, not numeric.

Both fail because the glyphs are **not Greek**.

### 7.2 The cipher is monoalphabetic — measured

Glyphs segmented and correlated after normalising to a common bounding box:

| | correlation |
|---|---|
| same-letter, within one line | **+0.63** |
| same-letter, across two images | **+0.54 to +0.61** |
| different-letter | **+0.05 to +0.07** |

The double `м` in `Сумма` uses the **identical glyph twice**; so does `с` in
`Сумма`/`чисел`. This also **independently confirms** the repo's Russian decode:
the glyph group sizes on the right-hand line match `здесь(5) зашифрованы(11)
биткоины(8) на(2) чёрный(6) день(4) номер(5) X(1)` exactly.

### 7.3 The alphabet

```
Сумма двух чисел  =  ◇⏶ᛗᛗ△ : ⇧⧗⏶⤬ : ⊤Ψ◇⫻ᛉ

С=◇  у=⏶  м=ᛗ  а=△     д=⇧  в=⧗  х=⤬     ч=⊤  и=Ψ  е=⫻  л=ᛉ

(`е` is drawn with **three** parallel strokes, not two. An earlier version of
this table had `⫽`; the glyph is `⫻`, measured across all four occurrences.)
```

Extended from the top-left lines (`Я надеюсь …`, `… будут присылать …`):

```
я=木  н=⊥  ь=⊤  ю=⧓  б=ᐭ  т=⊔    plus  п р и с ы
```

Cross-line agreement on `а д е с у и н р т ь ы б ч` — each verified in at least
two independent inscriptions.

**Reading geometry.** The right-edge inscription runs **bottom-to-top** on the master
(x 1529–1554, y 29–1014); the same text reads left-to-right in
[`pictures/20_1.png`](https://github.com/HomelessPhD/BLM_0.2BTC/blob/master/pictures/20_1.png)
— **a file in HomelessPhD's repository, not this one** — a 797×45 de-rotated
render (md5 `24640d4a4020a1ac86d4d690a54b8e0f`) far more legible than anything
extractable from the 1600×1200 master. It is cited rather than copied here
because it is someone else's artefact; the md5 lets you confirm you have the
same file. Use it for glyph work. The clock line reads
left-to-right, and its ink sits at luminance ~160–200 against a light background — a
hard threshold near 120 finds nothing, so use a levels stretch rather than a contrast
multiply.

Note also that the two ciphers share some shapes with **different values**: `◇` is
`W` in the Gravity Falls Latin cipher and `с` in the Cyrillic one. Do not
cross-apply them.

### 7.4 The falsification chain for X

The right-hand line ends `… чёрный день номер X`. Ten tests, ten negatives:

| test | result |
|---|---|
| truncated at the image edge? | no — cols 785–795 of 797, whitespace after |
| matches any of 68 corpus glyphs? | no — best +0.491 vs +0.55–0.63 baseline |
| matches the artist's own hand-drawn digits? | no — all at the +0.05 noise floor |
| carries a titlo (numeral marker)? | no — rows 0–10 above are empty |
| is it `л` = 30? | no — +0.377 vs +0.55 baseline |
| any Church-Slavonic numeral that is a mapped letter? | excluded — 18 of 27 are letters X does not match |
| the archaic numerals `ѕ ѳ і ѯ ѱ ѡ`? | no shape match established |
| a rare modern letter `ж ц щ ъ э`? | possible, but only `ц` carries a numeral value |
| does `1865-202…?` share the glyph? | no — that is Arabic numerals and a literal `?` |
| is it `ж`? | **refuted on arm count: 4 against 6** |

**A withdrawn test.** An earlier version of this table reported "X vs `х` = +0.056,
noise" as evidence against `ж`. That test does not discriminate and is withdrawn:
if `ж` were drawn as `х` plus an added stroke, the extra stroke changes the
bounding-box normalisation and the overlap, so a low correlation against bare `х` is
expected whether or not the hypothesis holds. Correlation is the wrong instrument for
a compositional hypothesis.

The valid test is structural. X has **four** arms from its crossing point; `ж` has
**six**. That refutes it on shape, which correlation could not do.

Its geometry is a vertical stroke crossed by a single diagonal, one arm up-right and
one down-left — verified identically in the master and in `20_1.png` (§7.3).

**[MEASURED] Elder Futhark, tested and also failing.** §7.4 previously tested X
only against Cyrillic, the artist's Arabic digits and Church Slavonic numerals.
Measured on the master at x1530–1560, y38–55 (ink < 110, 92-px component,
rotated to the reading frame, skeletonized): **2 strokes, 4 endpoints, one
crossing; stave 18 px; crossing at 56% of stave height; arms up 9.5 / down 7.5 /
upper-right 4.7 / lower-left 6.1; the diagonal rises to the RIGHT (`/`), 56° from
the stave.**

That is structurally **naudiz-like** — ᚾ is two strokes, four arms, a
near-central crossing — **but mirrored**: standard ᚾ falls to the right.

**The mirroring is not house style, and the discriminator settles it.** The
obvious defence was that this author mirrors glyphs anyway, citing the seal
ring's mirror-written Latin. That defence fails. The cipher's only asymmetric
glyph, `е`, was measured in **all four** of its occurrences:

| word | stroke angles |
|---|---|
| `надеюсь` | 50 / 50 / 49 |
| `чисел` | 43 / 45 |
| `номер` | 75 |
| `день` | 51 / 43 / 45 |

**All `/`.** One orientation everywhere — across the horizontal top-left lines
*and* the rotated right-edge column. Inside the cipher this author does **not**
mirror glyphs; the seal ring is a whole Latin inscription mirrored, which is a
different practice. So a mirrored ᚾ is an anomaly *within* the cipher, not a
habit of it.

That measurement carries a bonus: `е` matching across both frames **confirms the
rotation** applied to X, so the `/` direction of its diagonal is real and not a
rotation artefact.

**[TESTED, externally] A correlation null, and it is cleaner than it looks.**
hiddengogeta's independent template-matching of X against 104 reference
components reported a best match of **+0.399** against a 95th percentile of
+0.342, and read that as "low". It is stronger than that: with 104 independent
components, `0.95¹⁰⁴ = 0.0048`, so the maximum is expected to exceed the 95th
percentile **99.5% of the time** under pure noise. +0.399 is exactly what noise
produces. That makes it a clean null rather than a marginal one, and it agrees
with the structural result above.

> **Recorded as NOT READ.** Structurally naudiz-like (2 strokes, 4 arms,
> near-central crossing) but in mirrored orientation, which the cipher's own
> asymmetric glyph shows the author does not otherwise use. Shape-ambiguous with
> Latin `ł`, which has no semantic candidate at the end of a Russian
> `номер ___`. **NOT READ.**

**X matches neither the mapped alphabet, nor the artist's Arabic numerals, nor
the remaining plausible Church-Slavonic numerals, and carries no titlo. It is a
hapax — shape fully resolved, meaning unassigned.** The distinction matters and
the earlier wording blurred it: the geometry is *not* in doubt. It is a vertical
stroke crossed by a single diagonal, four arms from the crossing point, verified
identically in the master and in `20_1.png` (§7.3). What is unassigned is which
character that shape denotes. It occurs exactly once in 68 glyphs, which is
*why* it has never been read.

### 7.6 [MEASURED] Linguistic exhaustion — an independent route to the same wall

Reached by letter inventory rather than shape correlation, so it does not inherit
§7.4's method.

Across the three decoded plaintexts, **28 of the 33 Cyrillic letters appear**. The
five that never do:

```
ж   ц   щ   ъ   э
```

X must be one of those — and because none of them occurs anywhere else in the corpus,
**there is no second instance to triangulate from**. Of the five, only `ц` carries a
Church Slavonic numeral value (900); `ж`, `щ`, `ъ` and `э` have none. So `номер X`
resolves to a number only if the glyph is `ц`, and its shape does not support that —
`ц` is a U with a descender.

**[MEASURED]** The glyph is also **not in the Gravity Falls key at all**, checked
against both the pyramid layout and the Wheel of Intrigue. That is expected: Russian
needs 33 letters and the GF set supplies 26, so the author invented extras. This is
one of them.

> **Dependency.** This argument inherits the published plaintexts. The group sizes
> were confirmed independently by ink-profile segmentation (5/11/8/2/6/4/5/1 on the
> edge, 5/4/5 on the clock), and `е`, `с` and the doubled `м` were verified
> glyph-by-glyph — but not all 68 glyphs were re-derived. If any word in the
> plaintexts is wrong, the letter inventory shifts and the absent-five set with it.

**[INFERRED] X is unassignable from this corpus in principle.** No key entry, one
occurrence, and every candidate letter equally unattested. A higher-resolution scan
renders the shape more crisply and still cannot say which letter it is. The missing
thing is a key, not pixels.

### 7.5 `Сумма двух чисел` is the clock's caption

The bottom rune sits **inside the clock face**, among the numerals. The
mechanism it describes is fully consumed by the three hands. Proposing a second
application requires positive evidence.

For the record, a pair-sum search over the twenty explicit numbers in the image
has almost no discriminating power: **158 of 190 pairs land inside BIP39's
0–2047 range.** Only five pairs sum to another number present in the artwork,
and the one clearly designed relationship is `17 + 2003 = 2020` — the gold
chart's span, which the README already explains.

---


### 7.7 [RETRACTED] The "marked and withheld" reading

Five observations in this document were at one point read together as a
deliberate pattern — the author marks a thing and then withholds it — and an
inference was drawn from that pattern: that the seed words come from outside the
image and the artwork supplies only the ordering.

| where | observation |
|---|---|
| §1.4 | the phrase **"a trusted"** deleted from the whitepaper micro-text |
| §2.7, §5 | the **blank clock hand** at the 21st position |
| §6 | the flag's **star deficit**, 50 − 44 = 6 |
| §7.3 | the **unreadable final glyph** |
| §7.4 | **"1865 − 202…?"** |

Four of the five do not survive a base rate, and the rule that removes them is
now §10's:

| entry | why it fails |
|---|---|
| the deleted *"a trusted"* | the artwork has five letter-level typos in ~250 words. One dropped word-pair is unremarkable at that rate, and the phrase surviving twice elsewhere is exactly what a single accidental omission looks like — not evidence against accident. |
| the unreadable glyph | not the author's absence, ours. Russian needs 33 letters; the Gravity Falls key supplies 26; the author invented the rest and we lack the key. Filing it as withholding assumes an intent nothing supports. |
| *"1865 − 202…?"* | reads naturally as an open-ended range — abolition to the present and counting. §9 criterion 4 forbids assigning a cryptographic function to punctuation that already has a plain meaning. |
| the star and course deficits | two deviations across five resolved canonical-count checks is the ordinary yield of hand-drawing. They also **disagree**: 50 − 44 = 6 lands on an open slot, but 13 − 12 = 1 lands on `subject`, which is assigned, freed and eliminated. A real mechanism works twice. |

**[MEASURED] One entry survives: the third clock hand.**

It survives on the **placement** of the hands, not on the absence of a word —
and that distinction is what makes it testable. A decorative clock needs no
deliberate placement, because a clock showing a time has three hands determined
by *one* parameter. So the null hypothesis is: the clock simply shows a time.

It does not. All three hands sit at numeral midpoints (angles ≡ 15 mod 30°),
and that is impossible on a real clock. With *t* in seconds past twelve:

```
second : 6t    ≡ 15 (mod 30)  →  t ≡ 2.5  (mod 5)
minute : t/10  ≡ 15 (mod 30)  →  t ≡ 150  (mod 300)
hour   : t/120 ≡ 15 (mod 30)  →  t ≡ 1800 (mod 3600)
```

Every *t* ≡ 1800 (mod 3600) is a multiple of 1800, and 1800 and 3600 are both
≡ 0 (mod 300) — so the hour condition forces *t* ≡ 0 (mod 300), which can never
be 150. **Hour and minute are incompatible.** Sanity check: at 10:07:30 the hour
hand sits at 303.75°, 11.25° from the observed 315°.

Exactness is the weak claim, though, and it is not the one that matters.
*Approximate* triples of midpoints are common — 7,344 of 4,320,000 samples
across the 12-hour cycle fall within 1.5° on all three hands, the best being
1.186° at 9:27:37.69. **The question was never whether a clock can show three
midpoints. It is whether it can show *these* three: 12&1, 1&2, 10&11.**

Searching every time in the cycle at 0.01 s resolution, against all six
hand-to-angle assignments:

```
best achievable error : 10.465 deg   at 10:09:04.24
   hour   304.535   wanted 315.0   (off 10.465)
   minute  54.424   wanted  45.0   (off  9.424)
   second  25.440   wanted  15.0   (off 10.440)
```

10.5°, against a measurement precision of ~1.5° — **seven times the fit
tolerance**, and the canonical assignment is itself the best of the six. No time
produces this configuration. The three angles are therefore three independent
choices, not one.

**The prior, since §10's rule applies here too.** Under a null of free
placement, each hand lands within 1.5° of a midpoint with probability 3/30 = 10%
— or 3/24 = 12.5% granting an illustrator who keeps hands off the numerals for
legibility. Three hands: **0.195%, about 1 in 512.**

That figure must then be corrected for look-elsewhere, because midpoints are not
the only configuration an observer would have flagged: all three on numerals,
all three coincident, two coincident, all three 120° apart, symmetric about an
axis. Dividing across four such alternatives gives ~1 in 130, and four is
conservative. **State it as order 10⁻², not 10⁻³.** That is still the strongest
number in the section, and it no longer overstates.

**The same discipline applied to a coincidence in the survivor counts.** In the
six-run black sweep of 27–28 September, `t21_black8` came in at exactly
**+20,301** survivors against the `N/128` expectation and `t21_black21` at
exactly **−20,301** — the same magnitude, opposite signs. Across the 15 pairs
available from six runs, an exact magnitude match is of order 1 in 4,600. That
is noticeable and it is not evidence: no mechanism connects the two runs, they
differ only in where `black` sits, and 1 in 4,600 is the *unconditional* figure
before any correction for the many other coincidences that would equally have
been flagged. Noted and dismissed. It is recorded here rather than omitted
because a reader checking the six counts will find it, and should find it
already accounted for.

**[RETRACTED] The inference the pattern carried.** That the seed words come from
outside the image and the artwork supplies only the ordering. With one entry
left, it has no basis and is dropped rather than downgraded. It was the most
defeatist claim in the document and the least supported — it told every reader
the answer is not findable in the artwork, on the strength of four observations
that turned out to be base rate.

**The four retracted entries remain in place where they were made.** Each is a
correct observation about the artwork; what is withdrawn is reading them as a
system. §1.4's deleted phrase is still a real deletion and `trust`@21 was still
tested on the strength of it. This subsection retracts the pattern, not the
facts.

**A note on how this error was found and on one it concealed.** The pattern was
assembled in a working document, not here, and for four days it was discussed as
though it were a section of this report — "§8" — by three parties, none of whom
looked at what §8 actually contains. The first patch written from that belief
replaced §8's real content with this retraction, keeping §8's heading, and an
anchor-checked script applied it faithfully because the line numbers were right
and the identity behind them was assumed. **A hash verifies which file; an anchor
verifies what text you are editing; neither verifies that the section is the one
you think it is.**

## 8. Do not use AI upscaling on this image

Generative upscalers invent detail; they do not recover it.

The artist's signature in the bottom-right reads `-yi-` under plain LANCZOS
interpolation. Run through VanceAI at 8×, the same region renders as a boxed
`ER`. The model **replaced** characters it could not read with letterforms it
found more plausible — cleanly, confidently, and wrongly.

Across the rune region, 6.5% of pixels differ by more than 30 levels from a
plain interpolation, with strokes reshaped and terminals sharpened.

**Any reading of X taken from an upscaled image is a reading of the upscaler's
guess.**

---

## 9. Acceptance criteria

So that "solved" means the same thing to everyone:

1. **Consistency.** A candidate plaintext must map every occurrence of each
   glyph to the same letter. One glyph, one value.
2. **X must be independently justified** — not inferred from the answer it
   produces.
3. **It must derive the address.** HASH160
   `ccbd031e54cde2a3189fd59bc49f731367a1779e` under a stated path.
4. **No post-hoc transformations** unless the image independently indicates
   them. "Reduce modulo 2048 because the result was too large" is not a
   mechanism the artwork specifies.
5. **A numerical coincidence is not evidence** unless the image identifies both
   the operands and the operation (§7.5).
6. **Check every candidate word against the wordlist before building on it.**
   Widely-circulated candidate lists contain `breathe`, `stop`, `freedom`,
   `hate`, `white`, `death`, `kill`, `war`, `money`, `buy` and `trusted` — none
   of which are BIP39 words.

---


7. **An observation needs its control before it is recorded, not after — and
   the control needs checking too.** A finding that survives only a qualitative
   caveat has not been tested. Worked example, in three stages, because the first
   two were both wrong.

   **Stage 1 — the finding.** The protest-slogan block has seven lines; line six
   was reported as the only one containing no BIP39 word, and slot 6 is an open
   gap. Striking, and recorded before any control was run.

   **Stage 2 — the bad control.** Two reviewers independently computed the base
   rate and both **stemmed** before matching (`LIVES`→`live`, `KILLING`→`kill`),
   giving p ≈ 0.50 and an expectation of **1.94** wordless lines against one
   observed. Fewer empties than chance: no evidence either way. Right verdict.

   **Stage 3 — the control, checked.** BIP39 matching is exact. `lives` is not
   `live`; `stop`, `kill`, `killing`, `not` and `us` are not in the wordlist at
   all. Matching exactly, the block reads:

   | # | colour | words | exact BIP39 hits | n |
   |---|---|---|---|---|
   | 1 | black | BLACK | `black`#184 | 1 |
   | 2 | black | LIVES | — none — | 1 |
   | 3 | black | MATTER | `matter`#1099 | 1 |
   | 4 | blue | NO JUSTICE NO PEACE | `peace`#1295 | 4 |
   | 5 | red | END POLICE BRUTALITY | `end`#589, `police`#1342 | 3 |
   | 6 | green | STOP KILLING US | — none — | 3 |
   | 7 | black | NOT ONE MORE | `one`#1238, `more`#1151 | 3 |

   **Two wordless lines, not one** — and line 2 is one of them. The original
   observation was not merely uncontrolled, it was miscounted.

   **The base rate depends on which text you take as the corpus**, which is a
   transcription judgement, so it is reported across five choices rather than one:

   | corpus | words | BIP39 | p | E[wordless] | observed |
   |---|---|---|---|---|---|
   | headline only | 59 | 23 | 0.390 | 2.65 | 2 |
   | headline + amendment | 92 | 32 | 0.348 | 2.97 | 2 |
   | headline + amendment + whitepaper | 118 | 37 | 0.314 | 3.25 | 2 |
   | slogan block alone | 16 | 7 | 0.438 | 2.32 | 2 |
   | amendment + whitepaper only *(out-of-sample)* | 59 | 14 | 0.237 | 3.96 | 2 |

   Expectation exceeds the observed 2 under **every** corpus, so the verdict does
   not depend on the transcription. The first four rows include the slogan block
   inside the corpus that scores it; that inflates p and so *lowers* E, biasing
   the test **toward** declaring signal — and it still does not. The last row is
   the clean out-of-sample estimate and is the least favourable of all.

   The expectation alone understates the case. Taking the seven lines as
   independent, the exact distribution of the wordless-line count gives a
   one-sided probability for the observed 2 under each corpus:

   ```
   corpus                                 p      E     P(=2)   P(<=2)
   slogan block alone                  0.438   2.32    0.340    0.576
   headline only                       0.390   2.65    0.298    0.457
   headline + amendment                0.348   2.97    0.247    0.351
   headline + amendment + whitepaper   0.314   3.25    0.199    0.269
   amendment + whitepaper only         0.237   3.96    0.094    0.115   <- clean
   ```

   **Quote the range, not a row: p = 0.12 to 0.58 one-sided.** Under the corpus
   most often cited (0.314) three is the modal outcome and two the second most
   likely, so the observation is an ordinary draw at p = 0.27.

   Note which way the out-of-sample row cuts. It has the **highest** expectation,
   so 2 sits furthest below it and `P(≤2)` falls to **0.115** — leading with the
   clean estimate makes the observation look *more* notable, not less.

   **And note which tail that is.** `P(≤2) = 0.115` is a **lower**-tail result:
   `P(≥2) = 0.979`, and the mode is **4**. The original claim was that a wordless
   line is notable, which requires wordlessness in *excess*. The artwork contains
   **fewer** wordless lines than chance, not more — so 0.115 cannot support the
   claim it was raised against, in any corpus, and a reader who sees "1 in 9"
   without the direction could conclude the opposite.

   That makes the conservative corpus choice unambiguously right rather than
   merely cautious: it is the row least favourable to the null, the null survives
   it anyway, and the residual deviation points away from the finding. **There is
   nothing here in either direction.**

   **What the example is for.** Two reviewers ran the same control independently
   and both reached the right verdict from a wrong premise. It surfaced only when
   the expected values were placed side by side — 1.94 against 3.25 — rather than
   the conclusions. **A control that reaches the right answer from a bad premise
   is still a control nobody checked.** Bending a written word to reach a wordlist
   entry is precisely how `breathe`, `trusted`, `stop` and the other eleven
   entered circulation, and both reviewers did it inside the section documenting
   it. That costs nothing to do and nothing prompts you to check it, which is why
   it is a better worked example than any of the thirteen bugs.

   Reproduce with `slogan_lines.py` in the project root (needs `mnemonic` only).
**[MEASURED] The chronology anchor, which the rule below is keyed to.** A rule
about what was knowable on 2020-05-10 is unusable without saying what that date
is, and the report has not said.

- **The address was funded 2020-05-10 08:01:46 UTC, in block 629754**, by tx
  `fcee21d4…d043`. It has five incoming transactions and no spends; the 0.2 BTC
  is the first, and the four later deposits (2023–25) came from third parties.
  *(From the mempool.space API via `chronology.py`; this is the one figure here
  not re-derived offline in this tree.)*
- **The artwork's gold chart postdates the funding by at least two months.** Its
  drawn 2011 peak sits at x240 y248 and its final peak at x454 y228 — **20 px
  higher**, or 0.8 gridline steps. With the chart's own $1,800 line at y249 and
  $200 per step, that reads as a 2011 peak of **~$1,808** and a series ending at
  **~$1,971**. Gold first exceeded its 2011 high in **July 2020**, so the
  artwork's content dates to July 2020 or later.
- **The `05.25.20` in the artwork is unambiguous**, not a reading: x992–1069,
  y370–388, ink median 43 against a background of 121, **78 levels of
  contrast**, with column runs separating every digit.
- **First posted 2020-10-08 09:25 UTC**, and our working file is byte-identical
  to that original (md5 `7710323…`). No version predates it.

**Consequence, and this is the premise the deletion table runs on.** The words,
the order, the passphrase and the scheme were all fixed **five months before the
artwork was posted** and at least two months before it could have been drawn.
Later content can **encode** the secret; it cannot **source** it.

Image measurements reproduce from `chronology.py`, whose output is
byte-identical to `expected_output/chronology.txt` on a local re-run.

**The chronology rule deletes what was unknowable, not what is late.** Content
that postdates the funding transaction can still *encode* a word — a later
drawing can depict something the author already had in mind — so **no assignment
is falsified merely by being dated after 2020-05-10**. What the rule kills is
narrower and sharper: justifications of the form "the author chose W *because of*
E" where E postdates the seed, and any candidate passphrase containing a fact
nobody could have known on the funding date.

| date or fact | knowable on 2020-05-10? | verdict |
|---|---|---|
| `05.25.20` | no | delete |
| gold above $1,800 | no — first exceeded in July 2020 | delete |
| the June 2020 Leopold defacement | no | delete |
| `11.03.20` | **yes** — the election date is fixed by statute, and the Trump–Biden match-up was set in April 2020 | keep |
| "Tuesday" | yes | keep |
| "I can't breathe", "No justice no peace" | **yes** — slogans from 2013–14 | keep |

An earlier form of this rule deleted every post-May-10 date, which over-deletes:
it would have discarded `11.03.20` and both slogans, none of which required
foreknowledge of anything. The corrected rule has not been applied to the
project's passphrase list, which is not in this tree.

**[MEASURED] One underline in 25 checkable words, and it lands on an assigned
word.** The hand-copied 13th Amendment was censused across 34 tokens — 32 body
words plus the heading `Section 1.` A word counts as *marked* only if the
thin-line detector finds a run covering ≥50% of it with at least one clean run;
*obscured* if spray paint covers ≥40% of its underline band.

| status | count |
|---|---|
| underlined | **1** (`subject`) |
| visible, unmarked | 24 (12 under a strict 25% spray rule) |
| obscured, uncheckable | 7 |
| heading `Section 1.` | indeterminate |

`subject` is BIP39 **#1728** and the template's **assigned** word for slot 1. It
is in no pool, so the underline proposes no new candidate — **it is the first
physical, in-image corroboration of any template assignment in this project.**
Every other assignment rests on the README alone.

**State the base rate in the same breath.** Of the amendment's 32 body words,
exactly **one** is an assigned template word (`subject`) and six more are gap-pool
words — nowhere near the half a first guess suggests. But the denominator here is
the 25 *checkable* words, and one of those six (`any`) is in the obscured seven,
so among the checkable words there are **six** template-relevant words, not
seven: `subject`, `crime`, `exist`, `neither`, `party`, `place`. A single mark
placed at random among the 25 hits *the assigned word* with probability
**1/25 = 4.0%**, and hits *any* template-relevant word with probability
**6/25 = 24%**.

4% is low enough to be worth recording and nowhere near low enough to lean on.
This is corroboration, not proof, and §9 criterion 5 applies to it as much as to
anything else — the more so because the underline was one of nine first reads in
this pass and the only one that survived, which is exactly the position from
which a surviving observation looks more significant than it is.

The mark is a drawn line, not spray halo: it has a paper-level row directly
beneath it and runs on across a letter gap with no spray underneath, where the
two control words on the same line darken steadily into the spray with no
separate line. Detector positive control passes on the `subject` line itself;
the known false-positive mode — a flat baseline where rounded letter bottoms
touch, as at y842 under `servitude` — is distinguished by the absence of a
lighter row between line and letters. Scripts: `t3_lines.py`, `t3_census.py`.

**Calibration: of 9 first reads in the image pass, 1 survived.**

| first read | outcome |
|---|---|
| `-IGHT` on the BLM card | not text: flat row profile, 35 levels of contrast against 193 for the BLM capitals |
| `SHT`, missing its I | `SHIT` is complete |
| `except` underlined | spray edge; the word is uncheckable |
| `DAY FOR THE FUTURE` | it reads `PAY`, so `day` stays translation-only |
| `wich` for "which" | indeterminate: the ascender band lies under the frame stripe |
| `Section 1.` underlined | indeterminate |
| `FELIX` on the seal ring | it is `RERUM` |
| SHIT letter spacing, first measurement | the T was cropped below its crossbar and measured as an 8-px stem; with full letters every letter gap is narrower than the X gap |
| `subject` underlined | **survived** |

**An 8-in-9 withdrawal rate is the number to keep in view when reading any
single image observation in this report, including the one that survived.** The
rule it produced: nothing enters the record from an upscaled view until it has
survived a native-pixel re-measurement, with a control.

---

## 10. Method

Custom CUDA pipeline, RTX 4070 Laptop (sm_89):

| stage | rate | verified against |
|---|---|---|
| unrank + checksum filter | 216 M/s | exact count 1263 over ranks 0–19999 |
| SHA-512 (paired uint32) | — | 7 vectors, all padding boundaries |
| PBKDF2-HMAC-SHA512, 2048 iters | 209 k/s | 5 vectors incl. canonical BIP39 |
| SHA-256(33B) + RIPEMD-160 | — | 3 vectors incl. hash160(G) |
| BIP32 + secp256k1 | 925 k/s | 6 vectors incl. k = n−1 |
| Electrum HMAC filter | 7 M seq/s | Electrum's documented segwit test seed |
| **combined** | **125 k/s** | canonical 12- and 24-word addresses |

Two-kernel structure: checksum filter with warp-aggregated stream compaction,
then derivation over the survivors. Fusing them runs the 4096-compression path
in ~87% of warps with ~2 live lanes each (~6% utilization); splitting recovers
~16×.

**The rate table above predates this rewrite.** Every figure in it was measured
on the affine pipeline; the combined 125 k/s is now roughly 3× that. The table
is retained as measured rather than re-scaled, because a scaled number is not a
measured one — it will be replaced when the suite is re-run end to end.

The pipeline is **~3× faster** since replacing affine double-and-add with
**Jacobian coordinates**: ~384 modular inversions per scalar multiplication
down to one, at the final conversion back to affine. **Measured 2.956×
end-to-end** on a 4-path config (10.08 s → 3.41 s).

**Every rate below is stated with the conditions that produced it**, because
this project lost an evening to figures whose unit, path count and thermal state
were unrecorded:

| quantity | value | conditions |
|---|---|---|
| pipeline throughput | **135,074 derivations/s** | 22 production runs, sd 0.32%, 1 path |
| 4-path / 1-path cost | **T4/T1 = 1.484** | `loo` (4-path) against `free` (1-path), both post-Jacobian |
| shared / per-path split | P = 6.209 µs, X = 1.195 µs | per derivation, from the above |
| `BIP32 + secp256k1` row | 925 k/s | **per derivation, single path** — not per scalar multiplication |
| scalar-mult speedup | **5.50× production** | 6.5× is the isolated-kernel figure; production wins |
| EC share, 4 paths | **43.5% [MEASURED]** post-Jacobian | from P and X directly |
| EC share, 4 paths | ~81% **[INFERRED]** pre-Jacobian | from a contended A/B, assuming both arms were slowed equally |
| hardware state | 1605 MHz SM — **51.7% of the card's 3105 MHz max** | 88 °C sustained, 59.7 W of 80 W, `SW Thermal Slowdown` active |

The last row is the reproducibility item. **An unthrottled card should be roughly
twice as fast**; without that line a reader benchmarking their own solver
concludes ours is broken.

The two EC-share figures describe **different binaries**, and pairing the
post-Jacobian cost ratio with the pre-Jacobian share produces an Amdahl
impossibility. That mistake was made and caught here; the labels exist to stop
it recurring.

All three scalar multiplications in the derivation are **fixed-base** — the
hardened BIP32 steps need no public key, and the rest multiply the generator —
so a comb table was considered and rejected: it adds ~2% against a 5.5× Amdahl
ceiling that Jacobian alone reaches 87% of. Extra risk surface for nothing.

Verified bit-identical to the affine routine over **122,880 random scalars plus
k = 1, 2, 3 and n−1**, with the affine implementation retained as the oracle
rather than replaced. The swap happened mid-sweep, at a chunk boundary; the
survivor count of the completed run reconciled **exactly** across the two
segments, proving the swap introduced no gap and no overlap.

Two estimates were wrong in opposite directions and the decision survived both:
a predicted 30× on the multiply (inversion priced at ~100 multiplies; Cyclone's
`_ModInv` is divstep and far cheaper) and a recommendation to build the comb
table first. The robustness table is the only reason — the case never depended
on hitting the multiplier.

**Seam validation.** Chunking is where an exhaustive claim can quietly fail: an
off-by-one dropping one candidate per join loses N−1 of 25 billion — numerically
irrelevant, fatal to the word "exhaustive". Three instruments, all green:

1. **Count invariance.** The survivor total is a pure function of the config, so
   chunking cannot change it. `seam_count.conf` reports an identical 262,250 at seven
   chunk sizes down to `--chunk 7` — 599,187 chunks over 4.2 M candidates. A single
   candidate lost per join would show as a shortfall of 599,186.
2. **Cross-binary match at production scale.** `t18_pool52` reports **5,941,047**
   survivors at four chunkings — the same value logged by three full runs of the
   *previous* binary. That is not self-consistency: it validates the historical runs
   and proves the refactor did not move filter semantics.
3. **The answer planted on a seam.** `--seam N` truncates the chunk containing N−1 to
   end exactly at N. The known answer HITs when placed first-of-chunk and
   last-of-chunk, at both small indices and past 2³².

A note on a broken test: the obvious form — set `--chunk` equal to the hit index —
cannot run. At 4,650,657,157 candidates and 1/16 acceptance that is 290 M survivors
against a 33,554,432 buffer, and the run aborts on `survivor overflow` before
reaching the seam. Chunk *size* and boundary *position* are different parameters.
The abort is itself a validation: the guard fired rather than truncating silently.

**Positive control.** Reproducing a known mnemonic proves little; the solver
must *find* an unknown one. A config blanks two slots of a known phrase to all
2048 words and requires recovery:

```
./solver2 --config selftest_find.conf
HIT   index 2270828
phrase : tiger live melody inject guitar nose route obtain ball diesel snow radar
```

262,144 derivations, `melody` and `snow` recovered.

That control is single-chunk. A second, `selftest_multichunk.conf`, blanks three
slots — 8,589,934,592 sequences, 536,870,912 derivations — and recovers the answer at
index 4,650,657,157, which sits in chunk 10 at offset 422,798,725 with a chunk size of
469,762,048. Nine boundaries crossed. Together with the seam instruments above, this
is what licenses the negative results.

**Fifteen bugs were caught by exact-value validation**, each producing plausible
output with zero register spills and no warnings:

- a SHA-256 message-schedule error yielding a 6.39% checksum rate against a true
  6.25% — invisible to any tolerance-based check
- the 24-word HMAC key pre-hashing omission (§1.6)
- a benchmark timing 20-bit scalars instead of 256-bit, overstating secp256k1
  throughput 12×
- a single-block `hmac_sha512` valid only to 119 bytes — harmless for the
  37-byte BIP32 data it was written for, fatal for Electrum, since 16% of
  18-word and 100% of 21/24-word mnemonics are longer
- a chunk-sizing assumption that survivor counts are exact rather than binomial
- an incorrect canonical 24-word address recalled rather than computed
- a widened bit field in the hit record that eight of twelve control cases were
  structurally unable to see (below)
- `BigInteger.Parse(hex, NumberStyles.HexNumber)` misparsing an **odd-length**
  string. A curve constant written as `"0" + 64 hex chars` comes back 4 bits shifted;
  PBKDF2 and BIP32 master stay byte-perfect against test vectors while every derived
  address is wrong. Build curve constants from byte arrays.
- **`show_hit` reporting the wrong derivation path.** It printed
  `m/44'/0'/0'/0/0` unconditionally, so any config with multiple `PATH` lines —
  `t18_pool52` has four, `t18_pathc` has eight — would have misreported which path
  produced a hit. **This is the only member of the family that corrupts a success
  rather than a negative:** the other seven produce a wrong "no match", this one
  produces a wrong answer to "which path found it", on the single run that would ever
  have mattered. It fires only on success, so nothing but a hit could have exposed
  it. `k_derive` now records the path index alongside the hit.

9. **The global checkpoint path.** `progress2.txt` was a fixed filename shared
   by every invocation, so any second run — a benchmark, a selftest, a config
   check — destroyed a multi-day sweep's resume point. A crash afterwards would
   resume from the wrong index and skip candidates silently, voiding the
   exhaustiveness the project rests on. Audited backward: no completed sweep was
   affected. Its fix has since prevented two concrete losses.
10. **A `uint64_t[4]` passed to a 5-limb `_ModInv`.** Compiles, runs, returns
   plausible garbage. The affine code never hits it because it routes through a
   `fieldInv` wrapper. Caught by the differential oracle on first execution.
11. **`subtract()` in the ledger discarded already-emitted pieces** on its
   disjoint-dimension early return, losing real volume. It never fired on the
   declared runs because in every pair the disjoint dimension is the *first* one
   where the runs differ, so the discarded list was always still empty. Fixing
   it left the evidenced figure unchanged and moved the combined figure by
   68,300,324 derivations.
12. **The ledger and the solver disagreed about what a config means.** The
   solver refuses a pool or slot word that is not in the wordlist and exits 1,
   in all three positions (`POOL`, a bare `SLOT`, a `SLOT` list) — verified by
   injection. The ledger's parser filtered the same words with `if w in IDX`,
   silently shrinking a declared pool. No run could have used such a config, so
   nothing was miscounted, but the error direction was to **understate coverage
   with no symptom** — the one direction that never announces itself. A ledger
   that reads configs must fail on whatever the solver would refuse.

   The first fix was scheme-blind: it checked the BIP39 map alone, so a
   brainwallet config legally declaring `EXTRA stop freedom` would have made the
   ledger abort on valid input — a hard stop traded for a silent undercount,
   which is the worse of the two. It never fired only because the ledger walks an
   explicit list of declared runs rather than a glob. Containment, not a fix.

   The audit that cleared it was also too narrow: it covered 239 configs in two
   directories. A correct enumeration of the home directory finds **767 `.conf`
   files, 735 of them puzzle configs**. Re-run across all 735 — no pool or slot
   word is neither BIP39 nor `EXTRA`, and all eight `EXTRA`-declaring configs are
   `scheme=brainwallet`. The conclusion survived; the evidence for it had been a
   third of what it should have been.

   The *widened* audit was itself wrong first, in the same family. It reported
   837 files and 667 puzzle configs, because it split `find` output on bare
   whitespace rather than newlines — shredding every path containing a space into
   fragments that failed to open and were swallowed by a bare `except: continue`.
   That **inflated** the file count while **dropping 70 real configs**, all of
   them under `~/Downloads/real (copy)/`. The discrepancy only surfaced because a
   later run with a *narrower* content filter returned *more* configs, which is
   impossible. Two audits of the same tree, and the one that agreed with
   expectations went unchecked.
13. **The fix for bug 12 introduced a collision, by relying on the containment
   it had just rejected.** Exempting `EXTRA` words meant giving them indices
   above the wordlist, and the first version enumerated each config's *own* list:

   ```
   brain_find.conf      EXTRA stop freedom    ->  stop    = 2048
   brain_selftest.conf  EXTRA battery staple  ->  battery = 2048
   ```

   `stop` and `battery` became the same element. The ledger's whole purpose is
   computing unions by real set intersection **across** configs, so a union over
   two `EXTRA`-declaring rows would have been arithmetic on words with nothing in
   common. Demonstrated before fixing: two configs sharing no pool word produced
   identical slot sets.

   It could not fire while no brainwallet config was a declared row — which is
   the same accidental containment rejected one bug earlier, reintroduced by the
   fix that makes such rows possible. **A fix inherits the standard applied to
   the bug.** Now one module-level registry: same word, same integer, every
   config, matching the solver.

   The related hazard was checked and does not apply — this script's index map is
   0-based (`zoo` = 2047), so basing at 2048 cannot alias it. Had it followed the
   report's 1-based convention, the first `EXTRA` word in every config would
   silently have become `zoo`.

   All three tests written for bug 12 parse a **single** config and so could not
   see this. Two cross-config cases were added and mutation-tested.
14. **The log filter destroyed the record of work that did happen.** The queue
   script piped solver stdout through `grep -vE "^ +[0-9]+\.[0-9]{2}%"` to keep
   logs readable, which strips every per-chunk progress line. `t21_free4.log` is
   108 bytes of header. When a question arose about how much a set of benchmarks
   had cost a running sweep, the data that would have answered it retrospectively
   — for free, exactly — had been discarded by design.

   Not a solver defect. The same family as bug 9 and `show_hit`: **tooling that
   loses the evidence rather than the work.** It cost nothing only because
   checkpoint mtimes survived independently, which was luck. Replaced by an
   external poller recording `(epoch, value)` on every checkpoint change — and
   that poller's first output turned out to contain the whole campaign's run
   durations, which is where the 21.910 h ± 0.32% figure came from.
15. **Two commits claimed work they did not contain.** Publishing this report
   took four commits to land three changes. `d30d8d3` applied the additions but
   substituted the wrong section (see §7.7). `9e7ef0d` and `d534547` each carried
   a message describing the section-8 restoration and **one line of
   `.gitignore`** — because they were staged with `git add -u <pathspec>`, which
   git reads as *"update only that pathspec"* rather than *"update everything,
   and also this"*. `1aad6fe` finally carried the content.

   Same family as bug 9, bug 14 and `show_hit`: **the record said the work
   happened and the artifact did not change.** Both bad commits reported
   `1 file changed, 1 insertion(+)` and neither was read. The check that catches
   it is three lines and confirms the artifact rather than the message:

   ```
   git show HEAD:REPORT.md | wc -l
   git show HEAD:REPORT.md | grep -c '\[FIGURE\]'
   git show --stat HEAD | tail -3
   ```

**Test an identity in the unit where it is exact. Divide last.** Derivation
counts are `candidates / 128` and they floor, so two correct quantities can
differ by one, and a true identity can appear to hold when it has only been
checked to a rounding step. The box algebra is exact in candidates; the campaign
is *measured* in derivations. Use derivations for cost and coverage, and
candidates for any identity.

This is the fifth instance of the rule below and it occurred inside the
correction of the fourth: the `pool75` term was quoted as 376,658,808 in one
paragraph and 376,658,809 four paragraphs above, with the text asserting they
were the same figure. Both are floors of 376,658,808.75. The disjointness proof
built on them compared 35,764,650,697 with 35,764,650,697.5 and called it exact.
Restated in candidates, both are integers and the identity is real.

Same failure shape as the four below — a figure arrived at correctly and then
compared against something that had been transformed.

**Whenever two or more boxes are combined, the inter-box term is part of the
answer.** This project has one recurring error, not four, and `tally2.py` exists
because it produced the headline figure. A figure derived from box volumes is not
finished until the overlap term appears in it **explicitly — in the formula, not
in the reasoning around it.**

| instance | what was omitted |
|---|---|
| the **192,196,843,171** headline | summed the boxes instead of unioning them. This is why `tally2.py` exists. |
| the amendment overlap at **14.96%** | summed 76 + 32 when 16 of the 32 rows were already inside the 76 |
| "the five mirrors **overlap each other**" | cited a term present in *both* numbers, so it could not be their difference |
| the `pool75` **closed form** | dropped `4 × 54⁶`, the inter-box term — inside a correction of the instance above it |

Four instances, two from each side of the review, and the fourth occurred inside
the explanation of the third within the same hour. The pattern is more useful
than any of the four stories: a reader who has seen it once will catch the fifth,
and a reader given four unrelated anecdotes will not.

**A figure taken from the record carries its factors with it, and they must be
re-derived before it is used.** Twice now a number already in this document has
been applied to a question it did not answer, and both times the error was in
what its factors *meant* rather than in its arithmetic:

- The 24-word floor. `30,502,389,939,948` is a **derivation** count at a /256
  checksum; it was divided by a **candidates**-per-second rate taken from
  21-word runs at /128. Out by exactly **2×** — 3,789 days reported against
  7,579.
- Stage 2. `3 × (P+3X) × 10,654,063,447 = 87.0 h` was read as *three paths*
  when the `3 ×` is a **slot count** — the declining text says "paths 2–4 on
  three slots". Out by **4.3×**: the thirteen-slot figure is 377 h, not 89. That
  turned the cheapest-looking remaining branch into the most expensive, from
  about 264 hours per percentage point of probability against the 89/0.33
  the three-slot figure implies.

Both were caught the same way: by recomputing from the box definitions instead
of adopting the number. Neither would have been caught by checking the
arithmetic, because the arithmetic was right in both cases.

**That is the argument for keeping the formula visible beside the figure.**
`3 × (P+3X) × 10,654,063,447` is re-derivable and was re-derived; `89 h` alone
would have been believed. Where this document states a cost, it states the
expression that produces it, and that is not decoration — it is the only thing
that makes a misreading recoverable by a later reader who was not there when
the number was computed.

**A config enters `EVIDENCED` when its run completes and its survivor count
lands inside its band — not when its file exists.** The five `*_apple` mirrors
were written into `configs/` and started on 2026-10-08, and their boxes were
passed to `union_volume` to compute a marginal while they were still running. Had
they been added to the `EVIDENCED` literal instead — by a glob, or by someone
computing that marginal and not reverting — the headline would have silently
gained 35 billion derivations that had not been computed.

It did not happen: `tally2.py` has no directory scan, `EVIDENCED` and `ASSERTED`
are explicit literal lists, and the only `apple` entry is `t21_flag6_apple`,
whose run finished. But the hazard is structural rather than hypothetical, and it
is the same class as the two errors above — a true-looking thing admitted on the
strength of its appearance rather than its verification. The admission test is
the band: 7,346,640,384 ± 83,971 for a mirror, checked after the run, never
before.

**When a model depends on which slot holds a property, read the config line,
never the volume.** A distinct failure mode from the four numerical errors above,
and it cost more: not a wrong calculation of the right object, but a **right
calculation whose object was never opened.**

The leave-one-out boxes factor as `2048 × 54⁵`. From that factorisation it was
concluded that the 2048 sat at slot 21 — the one slot where the checksum makes
the survivor count deterministic — and an exact-identity test was built on it,
complete with a prefix table, a residual column, five "failing" runs and a
GPU instruction to re-run three of them against a 16.8M-candidate coverage gap.
Every number in it was arithmetically correct. The box did not exist: `@FULL`
sits at slot 6 in `t21_loo6`, at slot 8 in `t21_loo8`, and so on, with slot 21
on the 54-word pool in all five. The run *name* says which slot is free.

Nothing in the volume could have revealed it, because `2048 × 54⁵` is identical
whichever slot holds the 2048. Checking the arithmetic — which was done, and
passed — could not catch it either. What caught it was `grep '^SLOT' config`.

**A negative control that passes under any target certifies nothing.** An
outside researcher's void run, disclosed in public issue #1, made this concrete:
their target was byte-swapped, their self-test planted its own target in a
separate buffer, and every gate they had passed regardless. Checked here, the
same corruption produces a clean `exhausted, no match` with a normal survivor
count and exit 2 — **indistinguishable from a real negative by anything the run
reports about itself.** The only test that distinguishes them is a planted
*positive* through the production code path, and the only place it can be
trusted is the one write to `d_target`. A control is worth exactly as much as the
path it shares with the thing it controls.

**Read the code, not its printout.** The host computes Electrum's expected
survivor count as `total/171`, a constant that entered with the original Electrum
patch: `electrum_patch.md` line 12 reads *"~1/256 per prefix, ~1/171 for both."*
That rationale is inconsistent with its own number — two prefixes at 1/256 each
would give 1/128, not 1/171. The kernel's `electrum_ok` accepts first byte
`0x01` or `0x10` with a zero high nibble next — **17/4096 = 1/240.94**. The two
differ by 1.409×. Measured on 24,010,000 candidates, acceptance was 1/241.28:
−0.45σ from the kernel's figure, −109σ from the printout's. A band built from the
printout would have reported every honest Electrum run as a catastrophic
shortfall, and the natural "fix" would have been to distrust the solver rather
than the constant. The printout is a second, unchecked implementation of the
thing it describes; the kernel is the thing.

**A verified list is only verified over the words actually in it.** A 34-word
Tarot candidate list was checked against the 54-word pool and found disjoint —
correctly, for those 34 words. The claim was then carried as coverage of the
*configs*, and the configs were built from a different list: `t21_tarot_j10x20`
includes `time` at slot 10, `time` is a pool word, and an eighth of that box was
consequently already searched. The verification and the artefact it was claimed
about were not the same object.

The same list had earlier omitted `gold`. Two omissions, but only the second cost
coverage, and the difference is instructive: a word missing from an enumeration
is a gap in a list, while a word missing from a list used to assert something
about a *config* is a false claim about work. Check the artefact that will run,
not the list that informed it.

**Tight intervals inside one window say nothing about where the window sits.**
Five consecutive chunk-boundary intervals of `t21_free3` gave 10,119,149 cand/s
with only 4.4% internal spread — read as a warmed, representative rate and
reported as a 15% shortfall needing a mechanism. The finished run came in at
11,030,969 end-to-end, 0.925× budget. The window had understated it by 9% by
sitting in a slow stretch, and its internal tightness was evidence of nothing
except that the stretch was uniformly slow.

This is the **inverse** of the lagged-checkpoint error two entries down: that
one divided a lagged count by unlagged time and understated; this one read
internal consistency as representativeness. Same family, opposite direction.
Both are cured the same way — by the finished number, which is why a projection
should be labelled as a floor or a bound and never as the figure.

**A summary is not a measurement, and the number to quote is the one in the
table.** Three times this week a prose sentence has drifted from figures sitting
directly above it in the same document: a glyph's "clean 4-px margin on every
side" where the measurement was 4 clear rows above and 5 below; "номер's letters
are 25–35% shorter" where three of four are and the fourth is a row taller; and
a dot-spread range given as 15.9–18.4 where the measured minimum is 15.0. None
changed a conclusion, which is exactly why the pattern is worth naming — each
survived because it was *roughly* right, and roughly right is how a table's
authority gets transferred to a sentence that has not earned it. When writing
prose over a table, re-read the table.

**The same rule one level up: a decision is only as durable as the message that
changes it is prominent.** The note above is about a sentence drifting from its
table. The identical failure happens to decisions.

The failure in this project was **not** a sign-off restating a stale decision.
It was a **reversal issued as an aside** inside a message about something else,
while the original instruction had been given with a cost table and an argument.
The party carrying the older instruction was reading the record correctly. A
decision overturned in passing, three sections into a message whose headline is
a different topic, is exactly as un-re-readable as a closing line — and it is
worse, because the person who carried the superseded course did nothing wrong
and can be told they drifted.

Neither party could produce the other's message, because they communicate only
through a relay and neither holds the other's transcript. That is the structural
fact, and it is why the fix is not care in wording: **a decision governing
machine time must exist as a config, a script, or a line in this document, where
it can be diffed by both.** In this case it became
[`STOP_AFTER_LOWERCASE`](STOP_AFTER_LOWERCASE), which is the only part of the
episode that will still be working in a month.

**A partial pass is not a pass.** Adding hybrid public keys widened the pubkey
index in `hit[1]` from one bit to two, which moved the `sp` and `kd` fields up by
one. The kernel was updated; the selftest's expected-value computation was not.
Twelve cases ran and **eight passed** — every case with `sp = 0` and `kd = 0`,
because at zero the two bit layouts are numerically identical. The suite looked
two-thirds healthy while the field it was checking had moved underneath it, and
the four failures were exactly the cases where the layouts disagree.

Two things made it recoverable. The pre-patch binary had been kept, so
`--selftest-brain` on it returned 12/12 and localised the change to the patch
rather than the hardware or the vectors. And the failure pattern was itself
diagnostic: a fault that spares every case sharing a particular parameter value
is pointing at that parameter. What would *not* have worked is reading "8/12" as
mostly-working. A control suite reports on the code as it was when the suite was
written; when the two drift, the suite's silence is not evidence.

**If you run your own solver: validate against exact expected counts, not
plausible-looking ones.** A 1.2% deviation is invisible to a sanity check and
fatal to correctness.

**Five rules, each learned by getting it wrong first:**

- **A number that lands where you expected is the one to check twice.** **Five**
  instances in a single day, each a figure that agreed with its author and so was
  never re-run:

  - `$?` after a pipeline or command substitution belongs to the last thing that
    ran, not the thing under test. It twice reported success where there was
    failure — a solver that had correctly refused a poisoned config, and a test
    suite carrying two failures.
  - An audit split `find` output on bare whitespace instead of newlines,
    inflating the file count while silently dropping 70 configs. It surfaced only
    because a later run with a *narrower* filter returned *more*.
  - A test proposed to prove a run never happened — `grep -c 'chunks'` — counts
    **lines**, and the progress writer emits `\r`. It returned 1, which would
    have confirmed the hypothesis it was designed to test. The run had in fact
    completed all 37 chunks. Counting records instead of lines reversed the
    conclusion and moved the excluded tranche from 98.6 M to 138.7 M.
  - Three consecutive progress reports of `~40%`, `~41%`, `~44%` on a run that
    elapsed time placed at **70–72%**. They incremented smoothly, which is what a
    number carried forward and nudged looks like, and the ETA riding on them was
    six hours out. The next measured reading was 71.1%.

  The common shape is not carelessness; it is that **nobody re-runs a check that
  agrees with them.** A passing check is where a broken harness hides. Every
  verdict in this project that arrived pre-agreed — the stemmed base rate, the
  two agreeing tallies, the zero exit codes, the shredded audit — was wrong or
  unfounded.

- **A single source of truth kept in two places is a running sum by another
  name.** The ledger existed as two copies — the published tree and the working
  tree — and they silently diverged: a patch went into one only, so the other
  kept an older parser. This is the same failure the maintained tally had, one
  level up. Whatever computes a figure must exist once, and the copy that gets
  run must be the copy that gets published.

- **A pattern match against §8 needs a base rate before it counts.** The artwork
  is full of numbered sequences, absences and near-misses. "This looks like the
  author's signature" is a hypothesis with a prior, and the prior is usually high
  enough to explain the observation on its own. Four of §8's five entries were
  retired by asking, once, how often the artwork produces that shape by accident.
  The one that survived did so because it had an independent measurement behind
  it, not because it looked more like a signature.

- **A reported elapsed time is a measurement, not a recollection.** **Seven** of
  this project's wrong numbers have been timings or rates:

  ```
  a cold chunk reported as a sustained rate
  a model quoted where a measurement was available
  an elapsed time never taken
  a fabricated progress reading (40.8%, invented, with a future timestamp)
  three consecutive status lines ~30 points below what elapsed time allowed
  an ETA carried forward for six hours without recomputation
  microbenchmark staging figures (1.18x, q > 22.8%) quoted as measured
  ```

  Survivor counts are z-tested against an exact expectation on every run;
  timings get quoted from memory. Same project, two standards — and it is the
  unexamined one that keeps failing. **A figure passed between collaborators
  carries the command that produced it, or it is not reported.** Stated as a
  producer's duty it failed repeatedly; it holds only when the consumer refuses
  to compute on a number that arrives as prose.
- **Agreement between two methods validates only the paths both take — so when
  two checks agree, compare the intermediate values, not just the verdicts.**
  Two independent tally implementations agreed to the candidate while sitting on
  a defect in a branch neither exercised. Separately, two reviewers independently
  stemmed the same word list and both reached "fewer empty lines than chance";
  the error surfaced only when the expected counts were placed side by side
  (1.94 against 3.25). A failed control announces itself. A control that agrees
  with you is invisible, and agreement on the conclusion is the weakest evidence
  the two methods can produce.

---

*Published so these paths are not re-walked. If you have a word for slot 21,
evidence placing 22–24, a resolution of slot 11, a **key** to the glyphs the
author invented beyond the Gravity Falls 26, or a genuinely larger source image
— that is worth more than any amount of GPU. A corrected template can be tested
in seconds.*

*Note what is no longer asked for: a legible view of the final rune glyph. It is
already legible. §7.4 resolves its shape completely and §6 explains why pixels
were never the obstacle there — the circled mark on the BLM card is the one
reading in the artwork that a larger file would actually unblock.*
