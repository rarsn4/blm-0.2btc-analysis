# 0.2 BTC Puzzle — the rune alphabet solved and block A measured, over 316 billion derivations eliminated, and six defects in the shared data

**Target:** `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`
**HASH160:** `ccbd031e54cde2a3189fd59bc49f731367a1779e`

**Status:** the Bitcoin puzzle is **NOT solved.** The address has received
20,107,284 sats across 5 transactions and spent zero — verified on-chain,
untouched since May 2020.

What **is** solved is the **rune cipher**, except for a single glyph. Those are
different claims and this report keeps them separate throughout.

I built a GPU search pipeline covering both BIP39 and Electrum and ran
**316,456,008,920 full seed derivations** — 9,157 days of CPU at typical solver
rates *[4 Nov 2026: this read 305,201,540,079 and 8,831 days until today, when the
31 completed t21 runs of 26–31 Oct were admitted to `tally2.py`. Ledger and the
admission entry are in §3; the scored table is at the end of §2.]* — plus
**1,365,479,729,718 brainwallet addresses** counted separately
(§2.12): three exhaustive t21 template sweeps at acceptance exactly 1, the t18
template corpus, and the image-text corpus. *[5 Nov 2026: this read 912,966,385,968
and "two … sweeps" until today, when `brain_t21_title` closed the case axis — lower,
upper and title, all three exhaustive, all three disjoint, all three negative. The
label and the figure moved in the same commit as the row.]* *[Corrected 4 Nov 2026. This line read
"7,939,492,344 brainwallet addresses" from 1 Sep 2026 (`94516a7`) to today. That is
the **t18 template row alone**. It was complete when written, but `brain_t21_pool65`
entered §2.12 on 29 Sep 2026 (`7fb9d22`) and the line was not updated with it, so for
**36 days** it omitted that run's 452,513,343,750 addresses; it also omitted the
image-text corpus, in the tree since 28 Sep (`78687ec`), and as of today
`brain_t21_upper`'s 452,513,343,750. The understatement reached about **115×**. The
old figure is not wrong about what it counts — it is the wrong scope for a line that
says "brainwallet addresses", and it is recorded here rather than swapped out,
because the marginal line in §3 drifted the same way for two weeks and the rule that
came out of it applies to every total on the page.]* The two t21 sweeps are
exhaustive over their **declared** space, which is `sha256` + space-joined only — one
quarter of the key-variant space the t18 row covered, stated in §2.12 and not closed.
§2.1–2.11, §2.13 and §2.14 are exhaustively eliminated, not "tried and didn't
find". **§2.12 is mixed and its heading now says so**: the two t21 template sweeps
are *exhaustive over their declared space*, acceptance exactly 1 with survivors equal
to candidates, while the t18 template corpus and the image-text corpus are *tested*
— the weaker claim. The declared space is the narrowing to watch: `sha256` +
space-joined only, one quarter of the key-variant space. §2.15 is a tested corpus,
unchanged. §2.16 and §2.17 are measurements of the template itself
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
| **[COMMUNITY]** | A reading or convention taken from the shared solver corpus, not derived here. Weaker than [INFERRED]: no argument from this project's measurements backs it. `premise_audit.md`'s vocabulary, used in §5 from 9 Nov 2026. |
| **[DEFECT]** | A fault in this project's own method or machine, found and dated. §1.7, §1.8, §1.9, §1.10, §1.12, §1.13. §1.11 is the same register for a fault in material **sent to** this project, kept separate because it is not ours. |

The distinction between [EXHAUSTED] and [TESTED] is the one that matters: §2.1–2.11
are the first, §2.12 is the second, and conflating them would be the only overclaim
in this document.

---

## 1. Six defects in the shared data, six in ours — and three in briefs sent here

§1.1–1.6 are faults in the data the community shares. **§1.7–§1.10, §1.12 and §1.13 are
faults of this project's own**, and they are the more serious kind, so they are not buried: for
five weeks this project accrued negatives on a solver binary that had never passed a
self-test (§1.7), and for five weeks it hashed a transcription that was never checked
back against the image (§1.8). They have the same shape — something written down once,
trusted thereafter, never re-measured.

**§1.11 is a third kind**, and it records **three** claims, all of which arrived in briefs
addressed to this project. Two were attributed to this project's own files and are not in
them. The third is different and worth distinguishing: its stated facts were **correct**, and
its conclusion was wrong anyway, because the facts were checked against one ledger and the
conclusion was drawn about words in general. It is recorded in the same register as the other
twelve because the failure mode is identical — something stated once and trusted thereafter —
and because a defect in an instruction is the one class a reader of this report cannot
otherwise see.

### 1.1 `breathe` is not a BIP39 word — but it *is* an Electrum word, and this section said otherwise

It appears in circulating word lists and is the widely-assumed passphrase. It is
**not in the BIP39 English wordlist**.

```python
from mnemonic import Mnemonic
"breathe" in Mnemonic("english").wordlist   # False
```

`breath` is also absent. As a *passphrase* it remains possible — tested, along
with 64 others, negative (§2.4).

> **[RETRACTED in part, 4 Nov 2026.]** This section read "…and ~~cannot appear in
> any seed phrase~~". The BIP39 fact stands; the universal claim does not.
> `breathe` is word **245** (1-based; index 244 0-based) of the **1,626-word
> pre-2.0 Electrum wordlist**
> (`electrum/old_mnemonic.py`, mirrored at `configs/electrum_old_en.txt`,
> sha256 `c8da327d…`), so it can appear in an old-Electrum seed, and an
> old-Electrum seed derives P2PKH addresses — the kind this target is. The error
> was writing "seed phrase" where the evidence supported "BIP39 seed phrase",
> inside a section whose title is "defects in the shared data". Six years of
> solvers putting `breathe` on a candidate list were not necessarily making a
> mistake; they may have been reading a different wordlist, and this report filed
> that possibility as somebody else's error.

**[MEASURED 4 Nov 2026] All twelve of the non-BIP39 words this project has
collected from the canvas are in the old Electrum list.** `breathe`, `stop`,
`freedom`, `hate`, `white`, `death`, `kill`, `war`, `money`, `buy`, `bleed`,
`shut` — 0 of 12 in BIP39, **12 of 12** in the 1,626-word list. The two lists
share 861 words, so 765 of the old list is outside BIP39.

**And the base rate does not support reading that as a signal about the creator.
This is the measurement that matters, and it goes against the hypothesis.** Two
controls, both computed here:

| control | n | in the old list | rate | P(all 12) |
|---|---|---|---|---|
| top-2,000 English words by frequency, not in BIP39 | 1,289 | 191 | **14.8%** | 1 in 8.9 billion |
| top-3,000, not in BIP39 | 2,086 | 264 | 12.7% | 1 in 59 billion |
| whole dictionary (104k), not in BIP39 | 71,557 | 764 | 1.07% | — |
| **common emotive/violent words, not in BIP39, excluding the twelve** | **31** | **21** | **67.7%** | **1 in 107** |

The frequency-matched rate of about 14–15% is what makes 12-for-12 look like
1-in-billions. The emotive control destroys that, and there is a structural
reason rather than a lucky one: `old_mnemonic.py`'s own header says the list came
from *"Wiktionary:Frequency_lists/Contemporary_poetry"*. A contemporary-poetry
frequency list over-represents exactly the body, emotion and violence vocabulary
that BIP39's curation removes — `breath`, `throat`, `lung`, `wound`, `terror`,
`sorrow`, `murder` are all in it. So "non-BIP39 protest-slogan word" and "in the
old Electrum list" are both largely consequences of how the two lists were built,
and the coincidence is **1 in 107, not 1 in 24 billion — about eight orders of
magnitude weaker**. Under §9's rule, that is a numerical coincidence and not
evidence.

*The emotive control is 31 hand-listed words and therefore a judgement call,
stated as one in the manner of `slogan_lines.py`. It was written down before
membership was checked, and excludes the twelve themselves. A reader who rejects
it is left with the 14.8% figure; a reader who accepts it is left with 1 in 107.
Neither reading licenses a search, and the first does not survive the second.*

**What does not depend on the statistics at all**, and is the part worth acting
on: pre-2.0 Electrum is a scheme that **has never been tested against this
target**, by this project or anyone, and `breathe` being in its wordlist is
enough to make it worth implementing. That is done and self-tested — §2.6.

**The asymmetry is the one piece of the signal that survives, and it is weak.**
Measured over the three word groups this project uses:

| group | in the old list |
|---|---|
| the 11 non-BIP39 words the brainwallet templates paint as slogans | 11 of 11 — 100% |
| the 54-word gap pool (all BIP39) | 36 of 54 — 67% |
| the 16 assigned object-words (all BIP39) | 9 of 16 — 56% |

The words *painted* on the canvas are 11 for 11; the words the community
*inferred from objects* — `camera`, `gold`, `liberty`, `police`, `pyramid`,
`rifle`, `vote` — are the ones absent. But 42% of BIP39 is in the old list
anyway, so 67% and 56% are mild enrichments, and 11 of 11 at the emotive base
rate is 1 in 73. Recorded because it is the right shape of test, not because it
clears the bar.

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

### 1.7 [DEFECT, found and closed 2026-11-02] The solver ran unverified for five weeks

**This is the most serious defect found in this project, and it is ours, not the
community's.** It is recorded here rather than only in a commit message because it bears
on the trustworthiness of every negative in §2 and §3.

#### What happened

| artefact | timestamp |
|---|---|
| last recorded self-test | **2026-09-23 20:24** — git `961c17c`, "recovers melody and snow at index 2270828" |
| last commit of any kind | 2026-09-27 12:30 — `b72c071` |
| `solver2.cu` modified | 2026-09-28 09:26 — **uncommitted** |
| `solver_host2.cuh` modified | 2026-09-28 09:33 — **uncommitted** |
| `solver2_jac` built | **2026-09-28 09:33**, from those uncommitted sources |
| defect found | 2026-11-02 |

**Every run from 28 September to 1 November — the bulk of the whole campaign — used a
binary built from uncommitted source whose last passing self-test predated it by five
days.**

The 28 September change was not cosmetic. It replaced the single-hash compare with
`derive_multi3`, which produces three hash160s per key (compressed, uncompressed,
hybrid); it added the `CASE` axis to `build_phrase`; and it changed the variant bit
layout from `(sp<<2)|(kd<<1)|pc` to `(cs<<4)|(sp<<3)|(kd<<2)|pc`, so `hit[1]` went from
a bare path index to `path<<2|encoding`. That is the comparison path, the phrase builder
and the hit-reporting format, all in one unverified rebuild.

The diff carries its own warning, which went unheeded:
`// Kernel and selftest must move together -- see §10.`

#### How it was closed

Three planted-key configs — `selftest_find`, `selftest_uncomp`, `selftest_hybrid`, one
per pubkey encoding, written 2026-09-28 07:51 with no record of ever running — were run
on the live binary through the **default config path**, as rule 8 requires.

**The tests were validated before being trusted.** An independent pure-Python
implementation — its own secp256k1, BIP39 checksum, PBKDF2-HMAC-SHA512, BIP32 CKDpriv
and all three pubkey serialisations, sharing no code with the solver — re-derived all
three planted addresses from the phrase at index 2270828 (`1108×2048 + 1644` → word 1109
`melody`, word 1645 `snow`) and matched each config's `TARGET` exactly.

| config | encoding | exit | `^HIT index` lines | index = 2270828 |
|---|---|---|---|---|
| `selftest_find` | compressed | 0 | **1** | yes |
| `selftest_uncomp` | uncompressed | 0 | **1** | yes |
| `selftest_hybrid` | hybrid | 0 | **1** | yes |

The binary's own known-answer suites were run too: `--selftest` passes the canonical
BIP39 12- and 24-word spec vectors, and `--selftest-brain` passes all **26** brainwallet
vectors, including 16–23 covering `upper` and `title` casing.

#### Two further checks, both clean

- **Rule 8 across all history.** Every log in the tree yields **124 target loads, all of
  exactly one value**, `ccbd031e54cde2a3189fd59bc49f731367a1779e`, and never the void
  32-bit word-swapped form `1e03bdcca3e2cd549bd59f1813739fc49e77a167`. The host decode is
  big-endian correct. **No run is void for a wrong target.**
- **Hits.** [WIDENED 2026-11-09 — the original check read one producer's format; see §10]
  The format-agnostic detection grep `grep -c -i -w -E 'hit|hits|commit=|phrase[[:space:]]*:'`
  over **every log in both trees — 101 of them when this was measured, 2026-11-09 16:00 UTC**
  — returns **0** on every log except the three planted
  self-tests `st_selftest_find.log`, `st_selftest_uncomp.log` and `st_selftest_hybrid.log`,
  which return **2** each and are required to. The superseded form,
  `grep -c -E '^HIT[[:space:]]+index'` over 83 logs, also returned 0, but only
  `solver2_jac` ever prints that string, so it could not have reported a hit from the
  other three producers. **Against this target nothing has ever matched, and that now
  rests on a check with a positive control.** The log count is a live figure, not a
  constant: runs are still finishing, and it went 100 → 101 → 102 during the session that
  measured it. It is pinned to an instant above rather than quoted as a total, and the
  check is defined over *every* log rather than over a count.

  Both arms of that check now have controls, and the shape arm's was built on 2026-11-09 —
  see **§1.10**, which is the defect the control found on its first run.

#### Therefore the negatives stand

The machine finds a planted key on all three encodings and loads the right target. No
result in §2 or §3 is withdrawn. **But this was unverified for five weeks, and the
verification was prompted by a question from the owner, not by the project's own
discipline.** That is the defect, and a passing test afterwards does not undo it.

#### The standing rule it produced

> **No run starts on a binary whose build time is newer than its last passing
> self-test.**

Enforced by `selftest_gate.sh`, which every queue script now calls first. It proves the
rule fresh rather than comparing timestamps — strictly stronger, since a stamp can go
stale silently but a passing test cannot. The stamp is keyed on the binary's **sha256**,
so a rebuild invalidates it automatically with no edit to any script; a cached pass costs
0.02 s and a cold one about 15 s. Also recorded in `DO_NOT_PUSH` and
`machine_verification.md`.

### 1.8 [DEFECT, found 2026-11-02, five of six still open] A one-letter transcription error invalidated part of the brainwallet negative, and survived five weeks because the transcription was never checked against the image again

**This is the second defect of this project's own**, and it has the same shape as §1.7:
something was written down once, trusted thereafter, and never re-measured.

#### What happened

The §2.12 image-text brainwallet corpus hashes transcriptions of the strings painted on
the canvas. The bottom Latin line was transcribed **`caccobus`**. The canvas reads
**`caccabus`** — the 5th glyph is a single-storey `a`, flat-topped with a straight right
stem, against the closed round `o` of `ollae` two words later as the control. *caccabus*
is also the correct Latin, and it matches §7's own gloss.

**SHA-256 does not forgive one letter.** Every key derived from that line, in every
casing and every stripping variant — 206 strings in the generated key list — hashed a
string that **is not on the canvas**, and the string that **is** on the canvas was never
tested, in any casing. Those keys are not a negative for the drawn line. They are a
negative for a word nobody wrote.

The error entered in the first transcription pass and was copied into
`census_crops.py`, `word_census.py`, `brain_image_corpus.py`, `expected_output/`,
`word_census.tsv`, `brain_image_keys.txt` and twice into this report. It was found on
2 Nov 2026 only because the owner asked an unrelated question about casing, which forced
the line to be read off the pixels again — **the first time anyone had looked at it since
the transcription was made.**

#### What the re-read then found

Being wrong once is a mistake; being wrong without a check is the defect. So every
element was re-read against the drawn letterforms, from the image, not from any
transcription file. Method, coordinates and per-element evidence: `letterform_audit.md`.

Of the 26 audit units (`word_census.py`'s own element list), 4 are rune decodes and out
of scope for a letterform read. **Of the remaining 22, six differ from the corpus:**

| element | corpus holds | canvas reads | kind |
|---|---|---|---|
| COVID sign | `COVID IS A HOAX IS THE KILLER` | `COVID 19 IS A HOAX 5G IS THE KILLER` | two whole tokens missing |
| bottom Latin line | `…caccobus ollae` | `…caccabus ollae` | spelling — **fixed 2 Nov** |
| 13th Amendment copy | `Section Neither slavery…` | `Section 1.` heading; `servitude,` `States,` `jurisdiction.` | content + punctuation |
| E-of-BRAVE micro-text | `…every transac tion for double spen ding. After` | `…every / tran / sacti / ons. / For double spen / ding. After` | spelling, split, punctuation, casing |
| bottom whitepaper caption | `…received The payee…transaction the majority…` | `…received. The payee…transaction, the majority…` | punctuation |
| dates | `1865-202?` | `1865-202...?` | punctuation |

Two of the six are measured at **native pixels**, not from an upscale, per §9's rule:

- the ellipsis is three ink blobs, 14/13/13 px, evenly stepped at x318–321, x323–326,
  x328–331 y707–719, separate from the red `?`'s own dot at x334–337;
- the micro-text lines run **19 px / 19 px / 15 px** against 4.4 px per character
  calibrated on `common solution` (66 px / 15 ch). The corpus's `transac` would be 31 px
  and **there is no 31 px line**. The canvas word is `transactions.`, plural and stopped.

**And five drawn strings are in no corpus string at all** — tested against
`build(MAXIMAL)`, the union of all 64 readings §2.12 admits, 29,408 distinct strings:
`05.25.20`, `11.03.20`, `UBI BENE IBI PATRIA`, `BREATHE` (the neck band), `CHR` (the
monogram). **Every one of them was already measured and written down elsewhere in this
project** — in `premise_audit.md`, `even_slot_rules.py`, `seal_ring.py`,
`three_object_measurement.md`, and §9 of this report — and none reached the corpus. The
corpus was built once from two transcription files and never reconciled against the
element census the project kept building afterwards.

#### Two readings deliberately *not* counted

Both fail §9's rule — *nothing enters the record from an upscaled view until it has
survived a native-pixel re-measurement, with a control*:

- `PAY FOR THE FUTURE.` reads **`FVTURE`** under LANCZOS, with a flat-bottomed `U` in the
  same word as the control. At native resolution the whole word is one merged blob with
  no inter-letter gaps. **[INDETERMINATE]** If it is a V, that is a seventh untested
  string.
- `.VS.`'s two dots sit 9 px and 23 px above a baseline with a 33 px cap height,
  diagonally opposed as a 180° ambigram requires — **not baseline full stops**. Whether
  that makes the string `·VS·` is a transcription convention, not a measurement.

`wich` for `which` was re-read at 34× and again favours `wich`. It **stays
[INDETERMINATE]** for the reason §9 already gave, now measured: rows y1154–1160 are the
dark frame stripe, 61 of 67 px below grey 110, and that is precisely the ascender band.

#### The defect is BOUNDED to the brainwallet scheme — stated so no reader has to infer it

**A transcription error cannot have corrupted any BIP39 or Electrum negative, and the
headline 316,456,008,920 derivations are unaffected.** The reason is structural, not
lucky: those two schemes encode words as indices into the fixed 2048-word list, and the
solver resolves every config word through `widx()` before any GPU work begins. For a
non-brainwallet config `allow_extra` is false, so a word outside the list returns −1 and
the config parse **fails**:

```
solver_host2.cuh:181   if(i<0){ fprintf(stderr,"'%s' not %s\n", w,
                           cf.brain ? "a known word (add it with EXTRA)" : "BIP39");
                       return false; }
```

Verified empirically, 2 Nov 2026, not merely read: a copy of `t21_single.conf` with
slot 1 set to `caccabus` instead of `subject` prints

```
'caccabus' not BIP39
exit=1
```

and **the run does not start.** No kernel launches, no checkpoint advances, no negative
is recorded. A mistranscribed word in a BIP39 or Electrum config therefore **halts**,
loudly, on the first parse — it cannot be silently searched.

The brainwallet is the one scheme with no such guard, and that is inherent to it rather
than a solver choice: `priv = SHA256(phrase)` accepts any byte string, so there is
nothing to validate against. A wrong letter does not fail — it quietly hashes a
different key. That asymmetry is exactly why this defect could live for five weeks here
and could not live at all in §2.1–2.11.

| scheme | word validated against the 2048-word list? | a mistranscribed word |
|---|---|---|
| BIP39 (§2.1–2.5, §2.7–2.11) | yes, `widx()` before launch | **run refuses to start** |
| Electrum v2 (§2.6) | yes, same path | **run refuses to start** |
| brainwallet image text (§2.12) | no — `SHA256` accepts anything | **silently hashes the wrong string** |

So the scope of §1.8 is the §2.12 *image-text* corpus and nothing else. The §2.12
*template-sequence* corpus is also outside it, for a different reason: it builds phrases
from the word pool in template slot order, never from a transcription.

#### How it was closed

**All six differences are corrected and all five absent strings are added.** The corpus
grew from 29,408 distinct key strings to 34,354 under the maximal reading.

Three decisions, each deliberate:

- **Add, never remove.** Every superseded form — `caccobus`, the un-numbered
  `Section`, the unpunctuated caption, `transac`/`tion`, the old COVID line — is kept in
  a `SUPERSEDED` group. They were tested, and deleting them would make the 28 September
  negative unreproducible for no gain. A superseded string costs six addresses; deleting
  it costs the audit trail.
- **Indeterminate readings are carried as extras, never as substitutions.**
  `PAY FOR THE FVTURE.`, `·VS·` and the `wich` form of the caption are each in the
  corpus *alongside* the reading they might replace. None of them cleared §9's
  native-pixel rule, so none of them may displace anything; hashing one more string
  costs nothing and closes the hole either way.
- **The two sides are written out independently.** The four long canvas texts appear in
  both `census_crops.py` and `brain_image_corpus.py`, separately. That duplication is
  the point: a disagreement between them is a finding, not a merge conflict.

#### The standing rule it produced, and the gate that enforces it

> **No transcription enters the corpus without a dated letterform re-read against the
> master image, and no element the project measures anywhere may stay out of the corpus
> silently.**

The first half is what §1.7's self-test gate is to the binary. The second half is the
part that actually bit: nothing here was unknowable — `05.25.20`, `11.03.20`,
`UBI BENE IBI PATRIA`, `BREATHE` and `CHR` were all measured and written down elsewhere
in this tree, and the corpus simply never heard about them.

`corpus_gate.py` enforces it, and is built like the self-test gate — it **re-proves** the
property instead of trusting a timestamp:

- **The census side** is `census_crops.DRAWN`, new: every string this project has
  measured as painted on the image, with its box, a status
  (`measured` / `magnified` / `indeterminate` / `inferred` / `cipher`) and the file the
  measurement lives in. It is read by **static parse**, never imported — `census_crops.py`
  loads the image and writes crops at import, and a gate must not depend on that.
- **The corpus side** is the strings `build(MAXIMAL)` **actually generates**, not the
  source text. Comparing sources would only prove two files contain the same characters.
- **It refuses, it does not warn.** Exit 1, naming each absent element with its
  coordinates and provenance.
- **It is keyed on the content of both sides**, so any edit to either invalidates the
  cached pass automatically with no edit to any script. A cached pass costs 0.03 s, a
  cold one 0.33 s.
- **The brainwallet queue calls it first**, before the self-test gate.

It was tested against four failure modes, including the original defect itself — a
one-letter revert to `caccobus` — and refuses on each; ten rapid rounds alternating
wrong-letter and restored gave REFUSE and PASS correctly every time.

**One hole found and closed in the gate itself while testing it.** The first version
*imported* the corpus module. CPython validates a cached `.pyc` on `(mtime, size)`, and
`caccabus → caccobus` is a size-preserving edit — so a gate run in the same mtime second
could hash the new source, correctly decide its cache was stale, and then still
reconcile against the **old bytecode**. It now compiles and executes the bytes it
hashed, in a fresh namespace, with `sys.dont_write_bytecode` set. The thing proved and
the thing measured are the same object, which is the whole point of a gate.

#### §2.12's status

Unchanged in kind — it was already [TESTED], never [EXHAUSTED]. Its *coverage* is now
wider than before and, for the first time, **provably equal to the canvas census**.

---

### 1.9 [DEFECT, found and closed 2026-11-09] A derivation check reported two encodings and ran one: the uncompressed arm collapsed onto the compressed one

**Reported by the owner against the owner's own check**, the same day §2.2's third-party
phrase entry was written, and logged here because it is the same shape as §1.7 and
§1.8: something that printed a number nobody made it earn.

#### What happened

The check of seven third-party 12-word phrases was run over four derivation paths and
reported **"compressed and uncompressed"**, printing **56 derivations** = 7 × 4 × 2.
The uncompressed arm did not exist. The library **re-serialised the point** rather than
emitting the 65-byte `0x04` form, so both arms produced the same compressed bytes and
the same hash160. **28 real derivations were counted as 56**, and the printed total was
indistinguishable from a correct run.

#### How it was closed

Rebuilt on **raw-bytes hash160** rather than on a library's serialisation, and
self-tested against **both published privkey = 1 addresses** —
`1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH` compressed and
`1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm` uncompressed. A collapsed arm fails the second of
those outright. The rebuilt run produces **56 DISTINCT hash160s** and **zero matches**.

**The conclusion is unchanged; the method is retracted.** The phrases were negative
before and are negative now. What was wrong was the warrant, and a factor-of-two
overstatement of work done is exactly the error class §10's rules exist for.

#### The standing rule it produced

**An encoding axis must prove it is an axis.** Any run claiming *n* encodings has to
show *n* distinct hash160s for one key before the count is believed — asserting the
axis in a config or a log line is not evidence that the code took it.

#### Two things worth saying plainly

**This project's own check of the same family had the catch built in and the owner's did
not.** `t12_family_check.py` self-tests both privkey = 1 addresses before deriving
anything, which is the test that fails on a collapsed arm; the owner's check had no
self-test at all. That is not a point in anyone's favour — it is §1.7's rule working in
one place and absent in the other, which is the whole argument for the rule.

**And it was checked here rather than assumed.** After this report arrived,
`t12_family_check.py`'s four paths were measured for the same collapse: **8 hash160s
from 4 paths × 2 encodings, 8 distinct, no collapse**, so its 4,928 figure is 4,928
distinct derivations. The check is now part of that script's self-test permanently,
rather than a thing verified once in conversation.

---


---

---

### 1.10 [DEFECT, found and closed 2026-11-09] The publication gate's leak pattern read one producer's format, and passed a tracked file containing a real hit

**Found by the control built to close the gap in §10's log-reading rule** — on that
control's first run, which is the only reason it is in this report rather than in the
repository's future.

#### What happened

Earlier the same day, the *reading* rule was widened from `solver2_jac`'s two patterns to a
format-agnostic pair, because a detection grep keyed to one producer's wording returns 0
for every other producer including on a real hit (§10). The *publication* gate,
`pre_push_check.sh`, still carried the narrow form:

```
PAT='^\s*HIT[[:space:]]+index|^\s*phrase[[:space:]]*:'
```

`brain_image_corpus.py` reports a hit as a banner line and a `commit=<sha256>` commitment,
neither of which matches that pattern. Measured: a log containing a **genuine** hit — the
planted-control hit, a real `commit=` line with a real 64-hex digest — was `git add -f`'d
into the index, and the gate returned **PASS, exit 0**. The guard that exists to stop hit
material reaching a public remote did not see it.

**Fixing the procedure had not fixed the machine.** The same single-producer blindness was
corrected in the human rule and left in the automated check, four hours apart, by the same
person on the same day. That is the shape worth recording: a correction applied to the
document and not to the code that enforces it.

A second fault surfaced in the same test. Once the pattern was widened and the gate did
block, its classifier reported the two matches as **`(error)`** rather than `pattern`,
because the `awk` branch chain tested only for text beginning `HIT` or `phrase`. A correct
block was being described as a script malfunction — which is how a real block gets
dismissed as a broken grep.

#### What was not wrong

**Nothing was ever disclosed.** The widened pattern run over all 47 unpushed commits, their
messages, and the current tracked tree returns **0**. No log containing a hit in any
producer's format has ever been committed, and the four `.log` files that were tracked
measure clean. This is a defect in the guard, found by a test, before it was ever needed.

#### The fix, and what each part is worth

| part | what it does |
|---|---|
| six-alternative `PAT` | one shape per producer plus WIF and extended keys; **each alternative measured over all tracked files before being added**, and each matches 0 of them except the two that match only the allowed self-test pair |
| classifier branches | a non-empty match is now a pattern match with a named kind; only an *empty* match text counts as a script error |
| `shape_arm_control.sh` | five assertions, run end to end |
| `brain_image_corpus.py --selftest-plant` | replaces the target with the planted string's own hash160 so the real hit branch runs, writing the **first `hex64` ever present in a log in this project** |

The control's fifth assertion is the one that matters, and it is the one §10's own rule
demands: assertion 4 checks that the gate still PASSes with the hit log on disk, which it
does — **but it passes because the gate never looks at gitignored files, so it would pass
just as happily with a blind pattern.** Assertion 5 forces the same file into the index and
**requires a BLOCK**. Without it the control is exactly what §10 warns against, a check
that passes either way. Assertion 4 alone would have certified the broken gate.

**[SCOPE] One gap is left open deliberately.** A **bare** `hex64` — a raw private key or
seed with no surrounding wording — is not in the gate's pattern, because **26 tracked files
legitimately contain one** (sha256 stamps, spec test vectors, commitments). A blanket rule
would block the repository outright. That case is covered only by the shape arm of the
reading rule in `DO_NOT_PUSH`, which is a human procedure, not an automated gate. Closing
it needs a by-file allow-list and is on §6's list.

### 1.12 [DEFECT, found and closed 2026-11-10] A pre-registered test was circular, and the box it ran in was half background

**Found by running the tests and reading their inputs**, not by the tests failing — both
returned clean-looking verdicts, and both verdicts were empty.

`collar_form_plan.md` fixed three tests on the Leopold bust's collar form before they ran,
which is the right discipline and is why the defects are visible at all. Two of the three
were broken by their own definitions:

- **The hue test was circular.** Its rule was *"if the form's saturation lies below the
  shadowed bandana distribution, it is not bandana cloth under any lighting"* — but the
  bandana mask was **defined** as `S ≥ 0.35`. Its 5th percentile came back 0.358, the mask's
  own floor. **Every desaturated pixel in the image passes that test**, so it separates
  nothing. It printed a confident verdict, which is the dangerous part.
- **The form box was 51% background sky.** The box was drawn around a shape sitting on the
  bust's outline, so half of it is the sky behind the statue. The sky set the 90th-percentile
  brightness threshold to 0.847 and **erased a real feature**: the glint the test was looking
  for is there, 4 px at +61.9 levels, and appears as soon as the sky pixels are excluded.

**The general lesson, which is not the same as §10's:** a pre-registration fixes what you
will do, and it cannot tell you that what you fixed was empty. **A mask defined by a
threshold cannot be used as the reference class for that same threshold**, and **a box drawn
around a silhouette contains whatever the silhouette sits on**. Both are checkable before
running — the first by asking what the comparison's floor is, the second by printing the
mask's composition — and neither was checked. A third test in the same plan, the symmetry
control, was sound and returned a firm negative, which is the only reason the entry it feeds
says anything at all.

### 1.13 [DEFECT, found and closed 2026-11-10] Twelve allow-list pin notes state a verification that cannot be reproduced by the method they name

**Found by trying to reproduce one.** Every pin of `REPORT.md` in `pre_push_allow.txt` is
required to carry a note verifying the pin **by run text** — that the set of 12-or-more
consecutive BIP39 word runs is unchanged, *"compared by run TEXT because the line numbers
shift"*. Twelve consecutive notes, from blob `ef48a1df` (9 Nov) to `cdba0b34` (10 Nov),
state **"the same TEN runs … lengths [13,13,13,14,14,18,21,21,27,37]"**.

**Re-running the gate's own guard over those blobs returns NINE runs,
`[13,13,13,14,18,21,21,27,37]`.** One 14 is absent. [MEASURED]

| | |
|---|---|
| what the notes claim | 10 runs, two of length 14 |
| what the current gate reports, on **every one of the 30 pinned blobs** | 9 runs, one of length 14 |
| the difference | the guard's **self-test exemption**: a `phrase:` line in `README.md` or `REPORT.md` preceded two lines earlier by the planted `HIT index` line is skipped (`pre_push_check.sh`, the `doc` clause) |
| the suppressed run | the `HIT index` / `phrase:` pair of the **planted** `selftest_find.conf` control output — `REPORT.md:6545-6546` in this revision, a line number that shifts, which is why run text and not location is the comparison — 14 words, published on purpose |
| with the exemption disabled | **10 runs, `[13,13,13,14,14,18,21,21,27,37]`** — the notes' figures exactly |

**Nothing leaked and nothing was lost.** The real phrase material is identical across all
30 pins: 0 new and 0 removed at every step, verified by run text. The tenth run was never
a secret — it is the self-test's own planted phrase, and the exemption exists precisely
because the guard should not flag a control this report publishes deliberately.

**The defect is in the note, not the file.** The figures were measured against the guard
*before* the exemption was added, and then carried forward through twelve revisions without
being re-derived — the §1.8 shape again, something written down once and trusted thereafter,
this time in the machinery whose whole purpose is to be re-checkable. A reader auditing the
most recent pin today measures nine runs against a note claiming ten and concludes **a run
was removed**, which is the opposite of what happened. *That is exactly the inference this
author drew before measuring it.* A self-verifying note whose numbers do not reproduce is
worse than no note, because it invites a false positive about the one thing the gate guards.

**Fixed going forward:** every pin note now states the count **both ways** — as the gate
reports it and with the self-test exemption disabled — so it can be reproduced whichever
way the reader runs the guard. Earlier notes are left standing as the audit trail of what
was actually published, per the retract-by-marking rule; this entry is the marking.

### 1.11 [DEFECT in material sent to this project, found 2026-11-10] Two measurements attributed to this repository do not exist in it, and a third claim was scoped to the wrong ledger

**Found by looking for them before citing them**, which is the only reason this entry is
here rather than in §2.16's text as a borrowed authority.

*One limit on this whole section, stated because it applies to §1.11 and not to §1.1–§1.10:
the briefs are working correspondence, not public documents, so a reader cannot check these
quotations the way they can check a config or a wordlist. They are therefore quoted verbatim
and dated rather than summarised, and every claim graded against them is a claim about
**this repository's own contents**, which is checkable. Nothing here grades the briefs'
reasoning, which was sound in all three cases and is noted as such below.*

A brief of 10 Nov 2026 instructed this project to distinguish a new result from an
existing one, in these words: *"We measured the Bill Cipher wheel as the CLOCK DIAL and
rejected it on geometry, 36 degrees against 30."* The same brief placed a piece of work
*"inside today's block-B sweep"*, with the instruction *"same passes, same contrast
levels"*.

**Neither exists.** [MEASURED]

| attributed | what is actually here |
|---|---|
| a 36°-against-30° rejection of the zodiac wheel as the clock dial | **no `36°` figure appears in any file of this repository.** The dial test is R10 (`r10_layout.py`, `STOP_R10_SET_C.md`): the **clock** dial, hub (473.75, 940.0), twelve numerals 30° apart, a 24-direction 15° grid, a pre-registered element list and two nulls. A ten-symbol wheel appears nowhere in it |
| "today's block-B sweep" | **no block-B sweep was scheduled or ran on 10 Nov.** The block-B work is `blockb_bands_plan.md` and `blockb_bands_check.py`, from an earlier date. There were no "same passes" to join |

**Why this is recorded rather than quietly worked around.** The instruction built on each
claim was *correct* — a dial measurement would not bear on symbols used as locators, and
reusing an existing sweep's levels is the right way to make results comparable. Acting on
good instructions while silently dropping their false premises would have left this report
citing a measurement that was never made, and the next reader could not have told the
difference. **A provenance that cannot be found is not a weaker citation; it is not a
citation.**

What was done instead: the distinction was recorded on its own merits in §2.16 and
attributed to the brief, not to this repository; and the sweep was run standalone, reusing
block B's seven cuts and its control discipline explicitly and by name, so the comparison
the brief wanted is real and traceable. *The author of the brief withdrew both claims on
being shown this, which is why they are recorded as a defect in the material rather than
as a disagreement.*

#### The third claim — true premises, wrong ledger [MEASURED 2026-11-10]

A separate brief of 10 Nov 2026 stated that `devil`, `demon`, `satan`, `hell`, `dark` and
`horns` are *"NONE of them BIP39, so the goat→devil reading terminates in a non-word and
cannot produce a seed candidate."*

**The BIP39 half is exactly right. The conclusion does not follow, because it was never
scoped.** Measured against both ledgers this project holds:

| word | BIP39 | old Electrum |
|---|---|---|
| `devil` | no | **#854** |
| `demon` | no | **#773** |
| `dark` | no | **#130** |
| `satan` | no | no |
| `hell` | no | no |
| `horns` | no | no |

**Three of the six are old-Electrum words.** "Terminates in a non-word" is true only of
BIP39; the old 1,626-word list is a ledger this project has implemented, self-tested and
run a subset of (§2.6). A reading that terminates outside BIP39 has not terminated.

Two further exact-token facts, since the same brief's list mixed forms: **`horn` *is*
BIP39** and `horns` is not, and **`goat` *is* BIP39**. So the source end of that reading is
BIP39-reachable and the destination end is not — which is a sharper statement than the one
offered, and it is the EE-1 discipline again: inflections are different tokens.

**What does not change.** The goat→devil chain still has **zero measured links**, and **no
word enters any config from it** — not on the BIP39 path, where `devil` cannot be encoded,
and not on the old-Electrum path, where §2.6's arithmetic rules out the search regardless
of how well the vocabulary fits. Being reachable in principle and being searchable are
different claims, and this entry asserts only the first.


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

> **[SCOPE, 9 Nov 2026 — CLOSED the same day by the run below. Struck, not deleted.]**
> ~~**This claim has no log and is not in the ledger.** Seven
> configs exist — `t12full.conf`, `t12full_mp.conf`, `t12_p40`, `t12_p52`, `t12_p71`,
> `t12_p75`, `t12_p80` — but a search of this tree and of the working directory finds
> **no log mentioning `t12` at all**, and `t12` appears **0 times in `tally2.py`**, so
> no 12-word work is in the `EVIDENCED` union or in any headline figure. Under §0 this
> heading reads as [EXHAUSTED]; in fact it rests on this paragraph's prose, the same
> status §2.6 records for the 65-passphrase Electrum list, and it should be read the
> same way: **asserted, not evidenced.** Nothing above is retracted. The space is also
> trivially small — 2048² = 4,194,304 candidates, 262,144 after the checksum, seconds
> of compute — so re-running it with a log would settle this for almost nothing.~~
> **It was re-run. See the admission immediately below.**

> **[EXHAUSTED, EVIDENCED 9 Nov 2026] Re-run with logs, scored against a band committed
> before launch, and admitted to the ledger.** §2.2 was the report's weakest
> [EXHAUSTED] claim — asserted since the beginning, no log, absent from `tally2.py`.
> It now has all three. Bands committed first in `QUEUE_after_el22.md` (`3ebf594`),
> self-test gate PASS (cached) on `solver2_jac` sha256 `2cace98f30d1`, the same bytes as
> the 2026-11-02 stamp.
>
> **The band model, fixed before the run.** `t12full_mp.conf` pins slot 12 to `vote`
> with slots 6 and 8 `@FULL` over all 2048, so the 4-bit checksum is a **filter, not an
> identity** — rule 4's third case, binomial at p = 1/16. Not stratified: stratification
> needs a restricted pool on the checksum-bearing slot, and here the entropy bits vary
> fully. μ = 4,194,304 / 16 = **262,144**, σ = √(4,194,304 × 1/16 × 15/16) =
> **495.74**, band **262,144 ± 496**.
>
> | run | candidates | survivors | band | z | HIT | result |
> |---|---|---|---|---|---|---|
> | `t12full_mp`, empty passphrase | 4,194,304 | **261,335** | 262,144 ± 496 | **−1.632** | 0 | negative, in band |
> | `t12full_mp` + `pw2.txt`, 65 passphrases | 4,194,304 × 65 | **261,335 on every one of the 65** | exact equality | — | 0 | negative |
>
> **The second row's check was exact, not statistical, and it was fixed before launch.**
> A passphrase cannot change BIP39 checksum validity, only seed derivation, so every
> pass had to return *identically* 261,335 or the passphrase loop was not doing what the
> config said — the §1.9 failure mode. All 65 passes returned 261,335; the log holds 65
> progress lines and 65 exhausted lines, and `sort -u` over them yields **one** distinct
> value. `pw2.txt` sha256 `a60f9ef3…`, 65 lines, **line 1 empty**, so the first row is a
> strict subset of the second.
>
> **Keys actually derived**: 261,335 survivors × 4 paths × 3 encodings
> (`derive_multi3`) = **3,136,020** on the empty passphrase, **203,841,300** across the
> 65. The ledger's `derivations` column is candidates/16 and multiplies by neither, which
> is the convention every other row uses.
>
> **In the ledger**, carried as a constant `T12 = 4,194,304` at `CHECKSUM_12 = 16`,
> disjoint from every 21-word box and from the 24-word tail by construction — three
> templates, three checksum widths, three divisors, each floored separately. Exactly how
> `T24` is already carried, and for the same reason.
>
> **What it moved, from one capture of `tally2.py`:** evidenced union
> 40,508,144,877,493 → **40,508,149,071,797** candidates (+4,194,304) and
> 316,455,746,776 → **316,456,008,920** derivations (+262,144). The run count stays
> **82** because this is a carried tail and not a box, the same as `T24`.
>
> **One figure moved that is worth naming rather than leaving to be noticed.** The
> printed `double-counted` fell from 3,712,867,368,033 to **3,712,863,173,729**, which
> is −4,194,304 — the whole of `T12`. *[Both figures are superseded: the two twin
> admissions of 9 Nov took the total to 6,440,303,416,289, and §3 now splits it into
> accidental and path-twin components. The −4,194,304 step this paragraph is about is
> unaffected — it is a property of how `naive` treats a carried tail, not of either
> component, and it still holds.]* The cause is pre-existing and not this run's:
> `naive` sums the 21-word boxes only, while the union it is differenced against
> includes the carried tails, so each tail subtracts itself from the reported
> double-count. `T24` has been doing this since it was added. **[SCOPE]** The effect is
> 0.0001% and it is left alone deliberately — fixing it inside an admission would change
> a published figure for an unrelated reason. Flagged for its own correction.
>
> **What this does and does not settle.** It makes §2.2 evidenced at the **empty
> passphrase and the 65**, on the current binary with all three encodings, which is
> strictly more than the original prose claimed. It closes the branch outsiders most
> often reach for — §1.5 calls reading `·12·` as a phrase length *"the single most
> common wrong turn in this puzzle"*, and the 12-word template is now dead with a log
> rather than dead by assertion.
>
> *Not used for anything: the run reported 86,446,629 and 85,533,454 candidates/s, about
> 8× the 11 M/s the 69-day estimate uses. Rule 6 takes rates only from checkpoint-time
> deltas, and this is a self-reported in-kernel rate on a 4-million-candidate space
> sharing a GPU with `t21_free2`. It is recorded as an anomaly to measure, and the
> 69-day figure is unchanged.*

> **[TESTED, 9 Nov 2026] Seven 12-word phrases circulated by a third-party AI —
> covered by deriving the family that contains them.** The phrases varied **slot 6**
> over `neck`, `air`, `gasp`, `inhale` and `asthma`. **The phrases themselves are not
> in this tree and were not reproduced here**, so the figure that arrived with them —
> 7 phrases × 4 paths × 2 encodings = 56 derivations, zero matches — is
> **owner-supplied and is not independently verified by this entry**. Guessing the
> other eleven words in order to "check" them would have manufactured a negative,
> which is the failure mode §1.8 exists to prevent.
>
> **[CORRECTED 9 Nov 2026] That owner-supplied figure was itself wrong, and it is now
> §1.9.** The original check reported "compressed and uncompressed" but its uncompressed
> arm collapsed onto the compressed one — the library re-serialised the point — so
> **28 real derivations were printed as 56**. Rebuilt on raw-bytes hash160 and
> self-tested against both published privkey = 1 addresses, it gives **56 distinct
> hash160s and zero matches**: the conclusion did not move, the method was retracted.
> The run recorded below was then measured for the same collapse and does not have it.
>
> What was run instead covers them whatever their remaining words were, so long as
> they are of the `t12full` template: **slot 6 over the five named words and slot 8
> over all 2048**, on `configs/t12full_mp.conf`'s four paths, compressed **and**
> uncompressed, empty passphrase.
>
> | | |
> |---|---|
> | phrases enumerated | 10,240 = 5 × 2048 |
> | BIP39-checksum-valid | **616** against 640 expected at 1 in 16, σ 24.49, **z −0.98** |
> | derivations | **4,928** = 616 × 4 paths × 2 encodings |
> | matches | **0** |
>
> That is **88× the owner-supplied 56**, and it contains those 56 as a subset if the
> phrases are of that template.
>
> **[TESTED] and not [EXHAUSTED], deliberately.** Slot 8 is exhausted over the whole
> dictionary, and so are the four paths and both encodings. **Slot 6 is a corpus of
> five words, not the dictionary**, so this eliminates one named corner and not the
> class — the §0 distinction, applied to this run rather than assumed away.
>
> **It is also not purely redundant with the paragraph above, for two measured
> reasons.** The 65 passphrases are described in §2.4 as *"from the image text …
> including `Сумма двух чисел`, all `BREATHE` casings, BLM slogans, dates, and the
> target address itself"*, and that description names no empty passphrase.
> *[CORRECTED 9 Nov 2026: the list is `pw2.txt`, sha256 `a60f9ef3…`, 65 lines, and
> **line 1 is empty** — so the empty passphrase IS one of the 65 and §2.4's description
> simply did not mention it. Found by looking at the file rather than at the prose about
> it.]* And §2.2 predates the **28 September** change that
> introduced `derive_multi3` and the three pubkey encodings (§1.7), so whatever §2.2
> ran was **compressed only**. This run adds the uncompressed encoding and the empty
> passphrase over its corner, and it is the only logged, self-tested 12-word evidence
> in the tree.
>
> **Self-tested first; nine checks; nothing was derived until they passed.** The
> canonical BIP39 vector (`abandon`×11 `about`) seed and its BIP44 compressed address
> `1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA`; the published privkey-1 pair,
> `1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH` compressed and
> `1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm` uncompressed; that key's uncompressed BIP44
> address `18LhnLKXjcTw5xJFiTxntnKit2Gd63eWFm`, cross-checked against **libsecp256k1**
> (`coincurve`), an implementation sharing no code with this project; checksum accept
> and checksum reject; **rule 8 — the target blob is the hash160 and not the 32-bit
> word-swapped form**; and a planted target detected through the same comparison the
> sweep itself uses.
>
> *The first run of that self-test **failed**: a wrongly-recalled constant had been
> pinned as the canonical uncompressed address. Nothing was derived until it was
> replaced by the value three implementations agree on. That is §1.7's rule working,
> not a new defect.*
>
> **No GPU, no new config, and the phrases are deliberately not written down here** —
> a 12-word phrase *is* a 12-word consecutive BIP39 run, which is exactly what
> `pre_push_check.sh`'s guard exists to stop, and the same reason `boriserd`'s
> `g8lip0e` is cited and not quoted in §1.1. Derived on the project's own
> `verify_hit.py`.

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
- **[TESTED, 18 Oct] The 21 distinct BIP39 words written in the artwork, in
  reading order.** The words are `black brave can end find first future matter
  more one only order peace phrase picture police real seed this welcome world`,
  at word centres read from gridded views. That gives 9,222 distinct orders:
  row-major and column-major with every near-tie (< 25 px) permuted, and block by
  block with blocks taken by top edge and by left edge. 80 pass the BIP39
  checksum and 43 the Electrum seed-version check (chance predicts 72 and 38).
  All 123 were derived on their four paths, compressed and uncompressed, with an
  empty passphrase: **no match.** Script: `artwork_orders.py`, which uses
  `verify_hit.py`.
  *[New material, published 30 Oct 2026.] This entry and its output file
  `artwork_orders.out` appear here for the first time. Both postdate the previous
  public commit `073834d` (14 Oct) — the entry was written on 18 Oct — so the
  21-word list above and the 123 candidates in `artwork_orders.out` are new,
  not a re-publication of anything released earlier. The 123 are the orders that
  pass a checksum, each one derived and tested as stated above; every one is a
  recorded negative, and the words themselves are read off the public artwork.
  `passphrase_cpu_el18n.ckpt` (§2.6) is new in the same sense.*
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

> **[SCOPE, 4 Nov 2026] This whole section is Electrum *v2*. Pre-2.0 "old"
> Electrum is a different scheme and is NOT covered by anything below, nor by any
> run in §3's ledger.** Every `el*` run used the v2 derivation. The heading has
> always said v2; the README said "Electrum had never been tested by anyone"
> without the qualifier until today, and that is now corrected. See the end of
> this section for what old Electrum is and what testing it would cost.

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

> **[MEASURED, 2026-10-13] Re-run with logs; all seven claimed lengths now
> evidenced, on the empty passphrase only.** The originals had no log anywhere on the machine, so they were
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
> | `el21` | 235,298,000,000 | 976,558,172 | 976,578,613.3 | −0.66 | negative |
> | `el21_rev` (slot order reversed, 20 Oct) | 235,298,000,000 | 976,591,446 | 976,578,613.3 | +0.41 | negative |
>
> All in band, all on the current binary, so all three key encodings were
> checked. `el21` was scored against a band stated before it finished,
> 976,578,613.3 ± 31,185. It completed on 13 October at 22:12:30 UTC after
> 12,994 s in one segment from index 0, never resumed, with 976,558,172
> survivors: 20,441 short, **z −0.66**.
>
> **The re-runs used the empty passphrase only.** No `el*` config carries a
> passphrase line, and all seven logs print `passphrases=1`. The original list's
> "65 passphrases and the all-slots-vary sweep" therefore still have no log.
>
> **[MEASURED, 19 Oct] No logged Electrum passphrase run exists.** All eight
> logged Electrum runs (el12–el18, el21, el22) print `passphrases=1`. The only
> trace of one is a shell-history command, `./solver2 --config el18.conf
> --passphrases pw2.txt   # ~38 min`, on the old `solver2` binary, with no output
> log; its "~38 min" does not fit today's el18. A further gap: real Electrum
> normalizes the passphrase before PBKDF2 (`normalize_text`: NFKD, lowercase,
> accents removed, whitespace collapsed), and the solver uses it as written. Under
> that normalization `pw2.txt`'s 65 entries **collapse to 52 forms**, and **31
> entries, uppercase-only, were never tried lowercase**, which is how real
> Electrum would use them. el12 has been run with all 52 forms (inside the planted
> control, 0 matches); el13, el14, el16, el17 and el18 are now being run on the
> CPU (`passphrase_cpu.py`; el18 with the 52 plus `memo`, `charly`, `jr`).
> **el21 with these forms is open:** about 7.7 days of GPU for all 52.
>
> *[25 Oct] The CPU passphrase runs are complete, with **0 real-target matches** in
> every run. Each run's survivor count equals the GPU solver's own count for that
> config:*
> - *The 8 new passphrases (`memo`, `Memo`, `MEMO`, `CHaRLy`, `Charly`, `charly`,
>   `CHARLY`, `JR`) on `t12full_mp` (BIP39, 2,090,680 derivations), and as 9 (the
>   8 plus `jr`) on el12–el17.*
> - *The 52 normalized forms on el12–el17.*
> - *el18 with 55 forms (the 52 plus `memo`, `charly`, `jr`): 383,618,180
>   derivations over 6,974,876 survivors, every one of 4,900 tasks exactly once.*
>
> *There were three planted controls through the same code (BIP39 `Charly`,
> Electrum `JR`, and the normalized non-ASCII form), each found exactly once.
> Scripts: `passphrase_cpu.py`, `cpu_manager_oct19.sh`; outputs
> `passphrase_cpu_*.out`. el21 with these forms remains open.*
>
> **`el22` is held**: it is `70⁷ × 2 = 16,470,860,000,000` candidates. At
> `el21`'s whole-run rate, 235,298,000,000 over 12,994 s = 18.1M cand/s, that is
> **10.5 days**. At the 17.3M of `el21`'s last 100 minutes, after the GPU began
> throttling at 85 °C, it is 11.0 days. It is not the 31 hours a `54⁷` estimate
> gave, because the `el*` configs use a **70-word** pool, not the BIP39 54-word
> one. Earlier versions of this note said 8.5 days, from `el18`'s 22.5M, a run
> under one chunk with no boundary deltas; and then 10 days, from `el21`'s
> first-hour deltas of 19.0M, measured before the throttling. 22-word phrases are
> longer HMAC-SHA512 inputs again, so both figures are floors.
>
> *[14 Oct 2026] `el22` released by the owner and started. Band stated before
> launch, from the config: 16,470,860,000,000 candidates × 17/4096 =
> **68,360,502,929.7 ± 260,915** survivors. It is scored only after it completes,
> and admitted only if it lands in band. If it is interrupted, the survivor counter
> restarts on resume, so each segment is scored against its own expectation from a
> chunk-aligned resume index. A HIT here falls under the HIT rule in
> `DO_NOT_PUSH`.]*
>
> *[20 Oct 2026] `el22` was stopped by the owner on 18 Oct at checkpoint
> 6,531,571,515,392, which is 1,738 whole chunks (39.66%), while a queue of six
> runs used the GPU. It resumed on 20 Oct at 10:45:17 UTC from that index. Band for
> the resumed segment, stated before it completes: 9,939,288,484,608 candidates ×
> 17/4096 = **41,251,929,745.7 ± 202,684**. The first segment's survivor count is
> in the log, which the HIT rule restricts to two count-only reads, so it is not
> scored. That costs no coverage.]*
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
> not include 22.** *[Partly superseded 13 October: the seven lengths are now
> evidenced by the re-runs above, on the empty passphrase only. The 65
> passphrases and the all-slots-vary sweep still rest on prose.]* Configs exist for `el12`, `el13`, `el14`, `el16`, `el17`,
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
>
> *[13 Oct 2026] Mohammed posted a short reply on public issue #1 (21:08 UTC):
> thanks for the void-run disclosure; their `wp_*` figures reproduce; `el22`
> never run; Electrum lengths re-run with logs. The reply also said the
> target-byte check and the production-path planted test had passed, and that the
> re-run lengths were "all negative". That went out 64 minutes before `el21`
> finished (22:12:30 UTC); `el21` then landed negative and in band, z −0.66. Those
> results are all it disclosed: no report text, configs, ledger figures or
> planned runs.]*

#### Pre-2.0 "old" Electrum — implemented, self-tested, the full space not searchable, and until 9 Nov 2026 **no subset had ever been tried**

**[TESTED, 4 Nov 2026; first subset run 9 Nov 2026] The scheme is built and
verified; the full search is not affordable; and that is a separate claim from
whether anything was attempted.** `old_electrum.py` implements it;
`python3 old_electrum.py selftest` prints ALL PASS.

**Two claims, and until 9 Nov 2026 only the first was written down here.**

1. *The full space is unaffordable* — the arithmetic below, and it holds.
2. *No subset of it had ever been run.* From 4 Nov to 9 Nov 2026 this section's
   heading said "not searchable", which a reader takes as **"we looked and the space
   is too big."** The measured truth was stronger and worse: **nothing had been
   derived at all** beyond the self-test vectors, no candidate list had ever been
   built, and there was no log of any run in either tree. An unaffordable space and
   an untried one are different statements, and conflating them let the second hide
   inside the first.

**As of 9 Nov 2026 the first subset has been run.** Pre-registered in
`QUEUE_after_el22.md` before the candidate list was built: `breathe` at two
positions — legal here and **impossible in BIP39, where `breathe` is not a word** —
with ten others drawn from the 32 measured `A_display` census words that are in the
1,626-word list. Tier 1 is 66 candidates, `C(12,2)` placements with the ten others
fixed in one order.

```
rule 8 target blob OK            ccbd031e54cde2a3189fd59bc49f731367a1779e
validity cross-check             mn_decode and the header's group rule agree 66/66
PRE-COMPUTED valid count          66 of 66   (computed with NO derivation)
derived                           66         rejected as not-a-seed 0
IDENTITY                          PASS       derived 66 = pre-computed 66
addresses checked                 660        66 seeds x 2 chains x 5 indices
HIT count                         0
elapsed                           43.8 s
```

**The band was an identity, not a band, and a stronger one than "no checksum"
implies.** Old Electrum is usually called checksumless; `old_electrum.py`'s own
header records that it is not exactly so — each 3-word group encodes
`x < 1626^3`, and `'%08x'` overflows at `x >= 2^32`, which Electrum rejects, so
**99.631%** of random seeds survive — `1626³ = 4,298,942,376` against
`2³² = 4,294,967,296`, so `(4,294,967,296 / 4,298,942,376)⁴ = 0.99630647`.
*(This read `99.55%` when written on 9 Nov 2026, carried from a cube that was
873,999 too large; corrected the same day. No verdict moves — see §10.)*
Validity is therefore deterministic per
candidate and **computable in advance with no derivation**, so the exact valid count
was written down before the run and the run had to report exactly it. No sigma and
no z — the `t21_top6_loo21` shape (rule 4). Any other count would have been a
machine fault voiding the run, the role §2.12's acceptance identity plays for
brainwallets.

**Graded [TESTED], not [EXHAUSTED], and the reason is the scale of what is left.**
66 candidates is one ordering of one eleven-word set out of
`C(31,10) = 44,352,165` sets. Measured end-to-end cost is **1.507 candidates/s**
(the 100,000-round SHA-256 stretch plus ten EC address derivations per seed), so
every ordering of one fixed set — `12!/2! = 239,500,800` — is **1,840 CPU-days**,
and the hypothesis in full is about `1.06e16` candidates.

> **[CORRECTED 2026-11-10] The 1,840-day figure belongs to the repeated-word set and must
> not be quoted as the cost of a general 12-word set.** The `2!` is load-bearing: it is
> there because `breathe` appears **twice**, which collapses the orderings by half. A set of
> **twelve distinct** words has `12! = 479,001,600` orderings, which at the measured
> 1.507 candidates/s is **3,678.8 CPU-days** — exactly twice as expensive. A brief of
> 10 Nov 2026 cited the figure correctly but described it as *"one fixed 12-word set, all
> orderings"*, which drops the `2!` and understates the general case **2×**. Recorded
> because it errs toward affordability, which is the direction that gets a run queued.
> The per-candidate ratio in the same brief verifies: `125,000 / 1.507 = 82,946×`, stated
> as ~83,000×. **The probe answers the
question "has anyone required `breathe` at two positions?" with "now someone has,
for one set, and it is not the answer."** It does not touch the rest.

##### The ledger itself, verified against its source [MEASURED 2026-11-10]

Everything above rests on `configs/electrum_old_en.txt`, including the Tier-1 probe's
candidate list. It had never been checked back against upstream — the §1.8 shape exactly.
It has now been, by text-parsing the `_words` **tuple** in `electrum/old_mnemonic.py`
(the package is data here; it is parsed, not imported):

| | |
|---|---|
| words / unique | **1626 / 1626** |
| identical to the source tuple **in order** | **yes** — element by element, zero mismatches |
| two installed copies agree | yes (`~/.local/lib` and `squashfs-root`) |
| first five | `like just love know never` |
| last five | `throne total unseen weapon weary` |
| `breathe` | **1-based #245** |
| md5, file as stored | `33f89ca84f7c9b3eeec1bcc253bce673` |

**No defect.** The project's copy is upstream's list in upstream's order, so the probe's
candidate derivation stands.

Two notes on the brief that requested this check, both small and neither affecting the
list. Its digest `33f89ca8…` is described as *"md5 of newline-joined, in file order"*;
strictly newline-**joined** with no trailing newline is `1f6cbdf9eb28fbeed6f834a138a29fb5`.
The quoted value is the file **as stored**, i.e. newline-**terminated**. And its warning
that a `words = [` regex *"silently falls through and yields 1627"* does not reproduce on
these copies: `words\s*=\s*\[` matches **zero** times, and a whole-file quoted-string scan
yields **1630**, the four extras being `Software`, `AS IS`, a single space, and an
f-string error message. The warning's instruction was right regardless — parse the tuple —
and following it is why the order check above exists.

##### The canvas's own vocabulary against both ledgers — H1 refuted [MEASURED 2026-11-10]

Pre-registered in `census_vocab_plan.md` (commit `aa148de`, blob `e962bca2`) **before any
membership was computed**, because the reference class decides this result and choosing it
afterwards would decide it to taste. Script `census_vocab.py`, output `census_vocab.out`.
Membership by **exact token**, no stemming; the census's own `bip39` column is not trusted
and both ledgers are re-read from `configs/`.

**The four counts.** Of all 151 census rows: **BOTH 28, OLD-ELECTRUM-ONLY 10, BIP39-ONLY
12, NEITHER 101.** Excluded for the primary test, by rules fixed in advance: 20 tokens of
1–2 letters (**structurally impossible in both ledgers** — old Electrum is 3–12, BIP39 is
3–8), 14 Cyrillic, 12 Latin, 6 line-wrap fragments of the micro-text, 3 acronyms, and
`introdue`, which is a misspelling and not a word. 95 English words remain.

Primary stratum — `A_display`, English, 3–8 letters, **n = 61**:

| | count | share |
|---|---:|---:|
| in **both** ledgers | 24 | 39.3% |
| **old-Electrum only** | 8 | 13.1% |
| **BIP39 only** | 8 | 13.1% |
| in **neither** | 21 | 34.4% |

The eight old-Electrum-only words are `been`, `except`, `new`, `pay`, `shall`, `stop`,
`within` and `breathe`.

**`B_microtext` is excluded from the test, for a reason that is fatal rather than
cautious: B is whitepaper text, and the frequency control below is the whitepaper.** B
would have been scored against itself. The census header already warns B is a sample, not
a census.

**The base rate, without which the split means nothing.** 47.0% of the old list is absent
from BIP39 and 58.0% of BIP39 is absent from the old list (both verified: 765/1626 and
1187/2048), so *old-Electrum-only is the common case*. **No English frequency list is on
this disk** — no `wordfreq`, no `nltk`, no unigram counts — so the requested design could
not run as specified. Three substitutes were named in advance, primary first, and tested by
**exact Poisson-binomial** over per-token length-conditioned probabilities, the
`edit_lists_exact.py` standard:

| null | expected | P(X ≥ 8) | |
|---|---:|---:|---|
| **primary** — frequency-weighted English prose (`bitcoin.txt`, 2,299 eligible tokens) | **8.13** | **0.580** | at base rate |
| secondary — union draw, P(old-only \| in some ledger) | 15.63 | 0.995 | **below** base rate |
| sensitivity — type dictionary (`/usr/share/dict/american-english`) | 2.10 | 0.00104 | the pre-labelled trap |

**Observed 8. Expected 8.13. H1 is REFUTED by the rule fixed in §6 of the plan**
(P > 0.5): the canvas's vocabulary is exactly what ordinary English prose of the same
length mix gives, and against wallet vocabulary it is *depleted* in old-Electrum-only
words, not enriched.

**The sensitivity null is the finding's twin and is why the plan named it in advance.** A
dictionary draw returns **P = 0.001** — a publishable-looking result — from the same 8
observations. It is wrong because a dictionary is a list of *types*, dense in rare and
inflected forms, while painted words are *common* ones. Had the reference class been picked
after seeing the count, this section could have said either thing.

**Two structural facts, both recorded before measuring.** Old Electrum holds 80 words of
9–12 letters and **BIP39 holds none**, so in that band "old-only" is free and BOTH is
impossible — which is why the test runs on 3–8. The band is reported separately and it is
emphatic: of the **9** census words of 9+ letters, **zero** are in either ledger, in the
one place where the old list has a monopoly.

**The confound that outranks the result, and would have outranked a positive one.** The old
list **is a frequency list** — its own source comment reads *"list of words from
…/Wiktionary:Frequency_lists/Contemporary_poetry"*. Membership in it is a proxy for *"common
word in contemporary poetry"*, while BIP39 is curated toward the neutral and concrete. Any
emotionally loaded English text will show old-Electrum enrichment, and that is a fact about
the two lists. **This is precisely why the census is the right instrument: it is the
canvas's own vocabulary and not anyone's thematic selection.**

*Cross-check, unplanned and reassuring:* 24 + 8 = **32** `A_display` words are in the old
list, which independently reproduces the figure the Tier-1 probe was built on — the 32 that
give `breathe` plus 31 others, hence `C(31,10)`.

##### Membership query on both ledgers, NAMED and ADMITTED [MEASURED 2026-11-10]

`config_word_membership.py`, extended to carry both ledgers, over **227 configs** (192
published, 35 solver-only). The two questions stay separate because conflating them
inflates coverage: **NAMED** means a POOL or SLOT line chose the word; **ADMITTED** means
some slot would accept it. `@FULL` is the 2048-word BIP39 list **and nothing else**, so an
old-Electrum-only word can never be admitted by an `@FULL` slot — only by being named.

**`choke` has never been named, and it has never been admitted.** Old Electrum **#621**,
not BIP39. **0 NAMED and 0 ADMITTED in all 227 configs**, and the string occurs in no
`.md`, `.py`, `.tsv` or `.conf` in either tree. Said as plainly as it can be said: *this
project has never entertained it.* That is worth stating because a chokehold and
"I can't breathe" are the painting's reference, `breathe` is the leading passphrase
candidate, and the Floyd portrait is element E19.

| word | BIP39 | old Electrum | NAMED | ADMITTED |
|---|---|---|---:|---:|
| `choke` | no | #621 | **0** | **0** |
| `hit` | no | #185 | 0 | 0 |
| `devil` | no | #854 | 0 | 0 |
| `murder` | no | #1196 | 0 | 0 |
| `silence` | no | #290 | 0 | 0 |
| `breathe` | no | #245 | 0 | 0 |
| `death` | no | #170 | 6 | 6 |
| `freedom` | no | #775 | 6 | 6 |

**`death` and `freedom` are the only two named, and every row is a brainwallet POOL line**
(`brain_find`, `brain_t18_pool63`, `brain_t18_pool63_all`, `brain_t21_pool65`, and
solver-only `brain_t21_title`, `brain_t21_upper`). That is legitimate rather than a defect:
`brain_t21_pool65.conf`'s own header says these words are *"not BIP39, so unencodable as a
mnemonic and unchecksummable — and perfectly valid brainwallet input, because SHA-256 does
not care what the string is."* The mnemonic path never admitted them; the brainwallet path
is not ledger-constrained.

**And there the gap is.** That brainwallet pool's eleven non-BIP39 image words are
`stop`, `freedom`, `hate`, `white`, `death`, `kill`, `war`, `bleed`, `shut`, `money`,
`buy` — and **11 of 11 are old-Electrum words** (#76, #775, #93, #149, #170, #198, #307,
#419, #568, #616, #852). The pool was built from the painting with no reference to that
ledger and landed inside it completely. *This figure carries the selection confound in
full* — the pool is a thematic choice, which is exactly what the census test above was
built to avoid — so it is recorded as a description of our own pool, **not** as evidence
about the canvas. What it does show is that `choke`, `hit`, `devil`, `murder` and `silence`
were never in even that pool, and `breathe` entered only as a passphrase, where no ledger
applies.

**"The 22" could not be located [EXTERNAL, UNLOCATED].** The brief requesting this query
named *"the 22"*; no set of 22 candidate words exists in this repository. The only `22` in
the record is a phrase **length** (`Electrum, 22 words`, `QUEUE_after_el22.md:177`). The
query was therefore run over a roster this project can define and defend — the 34 words
made of the nine confirmed, the fifteen previously queried, the eight above, `black` and
`brave` — which is a superset of any 22 that was meant. Noted rather than guessed at, the
§1.11 discipline.

> **[EXTERNAL, UNLOCATED — 9 Nov 2026] The repeated-word hypothesis has a dated, named source, and
> it is the only one besides block B's caption.** Everything else in the instruction layer — the
> rules a solver is supposed to apply, as opposed to the words themselves — is either our own
> inference or an undated community assertion. Two are not:
>
> - block B's caption, transcribed by `u/Amadeus407` 2021-03-06, which states the sum-of-two-numbers
>   mechanism and whose 14 glyphs have **no measured location** (§2.17);
> - and this one: **u/Accomplished_Weird36, comment `glrfjsz`, 2021-02-02, score 1** — *"That is, we
>   are looking for words that are repeated, and this will be our seed phrase."*
>
> **This does not make the probe above right. It makes it the one hypothesis in this layer with a
> source.** The distinction matters because the probe was pre-registered on structural grounds —
> `breathe` appears twice in the artwork and repeats are legal in a checksumless scheme — and those
> grounds are ours. The 2021 comment is independent of them, predates them by five years, and says
> the same structural thing: *repetition is the mechanism*. It is still **one reader's assertion with
> no method attached**, it has never been measured here, and it cannot raise the probe's grade above
> `[TESTED]`.
>
> The same comment is the source of the 2021 edit list (external review §4.3b), and the same author
> wrote the `apple@20` chain of 2021-02-13 (§2.16). One person is therefore behind three of the
> external claims this report now records. That is a **correlation, not a confirmation**: three
> claims from one reader are one reader's claims, and nothing here treats them as independent.

Old Electrum shares nothing with v2 but the name:

| | Electrum v2 (§2.6 above) | pre-2.0 "old" |
|---|---|---|
| wordlist | 2,048 words | **1,626** (`configs/electrum_old_en.txt`) |
| words | 12 / 13 / … | 12 |
| validity | `HMAC-SHA512("Seed version", …)` prefix | **none worth the name** — see below |
| stretching | PBKDF2-HMAC-SHA512, 2048 rounds, salt `"electrum"` | `x = sha256(x + seed_hex)` **×100,000** over the ASCII hex |
| child keys | BIP32 | `MPK + sha256d(b"n:change:" + mpk)·G` |
| key form | compressed | **uncompressed** |
| address | per path | P2PKH — *which is what this target is* |

**It has no checksum, but not exactly none.** Each 3-word group encodes an
integer below `1626³ = 4,298,942,376`; Electrum formats it with `'%08x'`, so a
group at or above `2³²` yields nine hex digits and the seed is rejected — the
behaviour its own test suite records as "invalid old". The surviving fraction is
`(2³² / 1626³)⁴ = 99.631%`. So nothing prunes: there is no 1-in-128 filter to
lean on, and every retained combination is a live candidate.

> **[CORRECTED 9 Nov 2026]** The cube above read `4,299,816,375` from 4 Nov to
> 9 Nov 2026, while the fraction beside it read `99.631%` — **the two were
> inconsistent with each other in the same paragraph, in the same commit
> (`87b5c37`), three lines apart.** The fraction was right and the cube was
> wrong by 873,999: `1626² = 2,643,876`, and `2,643,876 × 1626 =
> 4,298,942,376`. Only the cube moved here. §10 records why this one mattered.

**Self-test, run before anything else.** The known-answer vector is published in
Electrum's own suite (`tests/test_wallet_vertical.py::test_electrum_seed_old`,
tag 4.5.8), and the implementation under test uses **this project's** pure-Python
secp256k1 and RIPEMD-160 from `verify_hit.py`, not Electrum's `ecc` module, so a
pass is agreement between two independent implementations:

```
wordlist         1,626 words, sha256 c8da327d...  matches old_mnemonic.py   PASS
mnemonic codec   encode/decode round-trip, 64 random seeds                  PASS
                 the suite's "invalid old" seed rejected (33 hex chars)      PASS
key derivation   master public key e9d4b786...2c442b3                       PASS
                 receiving address 0  1FJEEB8ihPMbzs2SkLmr37dHyRFzakqUmo    PASS
                 change address 0     1KRW8pH6HFHZh889VDq6fEKvmrsmApwNfe    PASS
planted hit      comparison fires on a planted h160, not on the real target PASS
```

The planted-hit check is rule 8's analogue for a CPU module: a negative from a
comparison that never fires is void, so the comparison is made to fire.

**The pool, measured from the canvas and not from a conversation.** Intersecting
the 1,626-word list with every alphabetic token on the 26 **measured** elements
of `census_crops.DRAWN` — 111 tokens, 96 distinct words — gives **24** words:

```
after  black  brave  breathe  common  double  end      find
first  future matter moon     more    new     only     order
pay    peace  picture real    stop    tower   welcome  world
```

27 of the 96 are in BIP39, 19 in both lists, 5 in the old list only, and 64 in
neither (Latin, the address string, fragments). A 63-word figure circulating in
discussion was built from words quoted in conversation rather than read off the
image; the measured number is 24.

**At 24 words it is not searchable, by three orders of magnitude more than the
card can close.**

```
ordered, no repeats   P(24,12)  = 1,295,295,050,649,600        = 1.3e15
with repeats          24^12     = 36,520,347,436,056,576       = 3.7e16
x 100,000 SHA-256 compressions each                            = 1.3e20
at a hypothetical 1e12 compressions/s                          = 4.1 YEARS
```

**The one tractable case, stated so it is not rediscovered.** If the twelve words
were *pinned* and only their order unknown, it is `12! × 100,000 = 4.8e13`
compressions — hours, not years. Nothing currently pins twelve: choosing 12 of
the 24 is `C(24,12) = 2,704,156` sets before any ordering. So the tractability
turns entirely on an argument that fixes the twelve words, and no such argument
exists yet. **No GPU time has been spent on this and none is planned.**

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
- **No metadata.** Chunks are `IHDR`, `sRGB`, `sBIT`, 291 × `IDAT`, `IEND`: no
  text, time, EXIF or physical-size chunk. *[Corrected 2026-10-14: this line
  listed `IHDR`, `sBIT`, `IDAT` only and omitted `sRGB`, a one-byte colour-space
  flag (rendering intent 0, perceptual) that carries no metadata. Measured with
  `pngcheck` 3.0.2 and an independent Python chunk parser, which agree: every
  CRC valid, zero bytes after `IEND`.]*
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

### 2.12 [EXHAUSTED over three declared t21 spaces, `sha256` + space-joined only; TESTED corpora otherwise] Brainwallets — a class nobody had touched

`priv = SHA256(phrase)` directly: no BIP39 checksum, no PBKDF2, no BIP32, no path.
Common in 2020-era puzzles and never tested against this target.

> **[Heading and §0 classification corrected 4 Nov 2026.]** This heading read
> `[TESTED]` alone, and §0 said "§2.12 and §2.15 are tested corpora — a weaker claim,
> and tagged as such in their own headings", until today. **§2.12 stopped being a
> single-strength section on 29 Sep 2026** (`7fb9d22`), when `brain_t21_pool65` landed
> as an exhaustive sweep at acceptance exactly 1 alongside the two tested corpora.
> Neither the heading nor the §0 sentence was re-derived when that run was added, so
> for **36 days** the section's strongest result was published under its weakest
> label, and a reader who trusted the heading would have under-read two exhaustive
> sweeps as corpus tests. *(Two is right for that window and is left alone: the
> third, `CASE title`, did not exist until 5 Nov. A sweep for stale "two" labels on
> 5 Nov must leave this one standing, or the record of the failure stops being a
> record of what actually happened.)*
>
> **This is the third instance of the same failure, and it is worth naming as a
> pattern rather than three accidents.** A figure or label is written, a component
> changes underneath it, and the thing above is not re-derived:
>
> | | what went stale | for how long |
> |---|---|---|
> | §3 marginal line | 3,608,896,368 while both totals above it moved | 2 weeks (28 Sep – 13 Oct) |
> | §0 brainwallet figure | 7,939,492,344, the t18 row alone | 36 days (29 Sep – 4 Nov) |
> | **this heading + §0 classification** | `[TESTED]`, after an exhaustive run was added | 36 days (29 Sep – 4 Nov) |
>
> All three were caught by someone reading the page against the ledger, not by any
> check in the tree. `pre_push_check.sh` guards phrases and private strings; nothing
> guards a summary against the section it summarises. The rule §3 states for the
> marginal — a total must be re-derived whenever any component of it changes — applies
> to **labels** as well as numbers, which is the part the first two instances did not
> make explicit.
>
> **[4 Nov 2026: the rule applied prospectively, for the first time.]** The §2 note
> that listed 31 unadmitted runs by name was a fourth instance waiting to happen — it
> became false the moment those runs entered `tally2.py`. It was closed, dated and
> struck **in the same commit as the admission**, and the only remaining unadmitted
> run (`el21_rev`) is named there, so the count on the page is correct as of the
> commit that changed it. That is what the three rows above would each have needed:
> not a better reader, but the summary edited in the same change as the thing it
> summarises.

**Two corpora, both negative** — and, since 29 Sep, **three** exhaustive template
sweeps besides, the whole case axis; the heading carries both strengths.

*Image text*, 22,638 keys: every text string in the image (Latin mottos, Russian
plaintexts, BLM slogans, dates, the 13th Amendment, whitepaper fragments, the target
address itself), casing / punctuation-stripped / whitespace-stripped variants, each
individual word of the Russian plaintexts, all 2048 BIP39 words singly, and pairwise
concatenations of 33 salient phrases under three joiners. Plus SHA256 and SHA256² of
the PNG file and of the concatenated IDAT payload.

> **[DEFECT, 2026-11-02 — this corpus hashes strings that are not on the canvas.]**
> A letterform re-read of every element against the master image (§1.8,
> `letterform_audit.md`) found **six of the 22 Latin-letterform elements differing** from
> the transcriptions this corpus is built on, and **five drawn strings absent from it
> entirely** (`05.25.20`, `11.03.20`, `UBI BENE IBI PATRIA`, `BREATHE`, `CHR`). One of
> the six — `caccobus` for `caccabus` — was fixed first; **all six were corrected and all
> five added the same day**, and `corpus_gate.py` now refuses to let any brainwallet work
> start while the canvas census and this corpus disagree. The *template sequence* corpus
> below was never affected: it builds phrases from the word pool, not from transcriptions.

**[TESTED, re-run 2026-11-02 after the corrections.] 34,354 strings → 206,124 addresses,
acceptance exactly 1.0, no match.**

```
corpus       34,354 distinct key strings   (was 29,408; the maximal reading, i.e. the
                                            union of all 64 readings this section's own
                                            description admits)
addresses    206,124                        = 34,354 x 2 hashes x 3 encodings
derived      206,124                        skipped (key out of range) 0
acceptance   206,124 / 206,124 = EXACTLY 1.0
result       NO MATCH                       exit 0
wall         3,105.6 s (51.8 min), CPU only, niced 19 alongside the GPU queue
backend      verify_hit.py -- this project's INDEPENDENT pure-Python secp256k1
```

**Acceptance is the load-bearing number here, exactly as it is for the template twin.** A
brainwallet has no checksum, so every string must derive by construction; the run enforces
`derived == 6 x strings` as an identity and exits 9 as VOID rather than reporting a
negative if it misses. It did not miss, and nothing was skipped.

**The derivation path was verified against an external oracle before it was trusted**
(`brain_corpus_selftest.py`): the canonical public brainwallet example derives to its
*published* addresses on both the compressed and uncompressed encodings, the hybrid form
is a well-formed 0x06/0x07 of the same point, and a planted hit is found through the same
comparison the real run uses. That check is not this project's own output, which is what
makes it an oracle. `coincurve` is not installed here and was deliberately not installed:
`verify_hit.py` already carries an independent implementation, self-tested against
known-answer vectors including 1·G, 2·G and (N−1)·G + G = ∞.

This figure supersedes the 22,638 of the original pass, which no surviving script, key
list or log reproduces (that is why `brain_image_corpus.py` exists). The ratio is 1.52×,
and the earlier number is retained above as what the first pass reported rather than
quietly replaced.

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

> **[MEASURED, 2 Nov 2026] The case axis had never actually been run, and is now
> queued.** `CASE` appears in **1 of 225 configs** in this project, set to `lower`;
> the only run header that prints it reads `case : lower`. `upper` and `title` had
> **never been run once.** Having the flag is not the same as having used it, and the
> paragraph above reads as though the gap were closed by adding the parameter.
>
> **[RETRACTED, same day] ~~As-written is `upper`, measured.~~** That claim was wrong
> and is withdrawn. It was reached from `slogan_lines.py`, which **normalises casing** —
> it renders the plinth band as `ONLY REAL BITCOIN` where the pixels read
> `ONLY real BITCOIN`. Measured from the image (`casing_measurement.md`), **three strings
> are genuinely mixed-case as drawn**: `ONLY real BITCOIN` (plinth), `I can't BREATHE`
> (hoodie), and the bottom Latin line `Esse quam niger es, sic dixit caccabus ollae`,
> which carries **one capital and is otherwise entirely lowercase**. The artwork is not
> "in capitals"; one all-capitals block was generalised to the canvas.
>
> **`CASE upper` is therefore one uniform capitalisation hypothesis among three, not the
> as-written reading.** The run is unchanged and so is its cost — because "as-written" is
> *undefined* for this corpus. `brain_t21_*` derives no string from the artwork: it builds
> phrases from the 65-word pool in template slot order, a sequence nobody ever wrote, so
> there is no drawn casing to reproduce and a fourth mode would have nothing to encode.
> The mixed-case strings that *are* drawn belong to the image-text corpus, which already
> tests them verbatim (`brain_image_corpus.py:172` includes the as-drawn `base`).
>
> `brain_t21_upper.conf` and `brain_t21_title.conf` are banded and queued ahead of the
> 12-config paths-2-4 closure (`QUEUE_after_el22.md`): 150,837,781,250 candidates each,
> survivors required to equal that **exactly** since a brainwallet has no checksum,
> 16.2 GPU-h each, 32.5 h for both. The casing machinery was verified before use —
> `--selftest-brain` vectors 16–23 cover `upper` and `title` explicitly.
>
> Still **not** closed by those two runs: the key-variant narrowing. Both inherit
> `sha256` + space-joined only, one quarter of the space the t18 figure covered.

**[TESTED, 4 Nov 2026] `CASE upper` has now run: `brain_t21_upper`, exhausted, no
match.** Its own row in the brainwallet count, **not** added into the 7,939,492,344
above, which is a different template on a different pool.

```
candidates   150,837,781,250              (65^6 x 2, six @POOL slots + slot 20's two words)
survivors    150,837,781,250              acceptance EXACTLY 1
addresses    452,513,343,750              (x3: compressed, uncompressed, hybrid)
identity     EXACT                        survivors == candidates == 2 x 65^6
result       exhausted, no match          exit 2,  HIT lines 0
wall         56,391.96 s = 15.66 h        2.672 M cand/s, 0 thermal pauses
```

**Acceptance is quoted as an exact rational, not a float.** `Fraction(150837781250,
150837781250)` is **1**, not a quotient that rounds to `1.000000000` at nine places,
and the distinction is the whole control: a brainwallet has no checksum, so every
candidate must derive and **there is no z-score to quote** — nothing scatters around
an expectation. Anything below 1 would mean work was silently dropped and the
negative would be void. The rate is from checkpoint-mtime boundary deltas over **66
intervals** (67 boundaries, 21:08:35Z to 10:29:44Z, 128,423,420,674 candidates in
48,069 s), not from the progress file, which is chunk-quantised.

**Overlap with the image-text corpus: 0 of 34,354 strings.** Measured, not assumed.
Of the corpus's 34,354 strings, **592** have 21 space-separated tokens and so could
in principle be a phrase of this template; **all 592 fail at slot 1**, which this
config pins to `subject`. No painted or decoded line in the artwork begins with that
word — it is a template assignment, not a drawn word. The test was controlled in both
directions: three phrases built from the template itself are recognised as members
(including both `apple` and `second` at slot 20, and different pool picks), and two
deliberate near-misses are rejected. The same test run against
`brain_t21_pool65.conf`, `brain_t18_pool63.conf` and `brain_t18_pool52.conf` also
returns 0, so no brainwallet template run duplicates any corpus string.

**This run and its lowercase twin are disjoint, and the reason is checkable.**
`brain_t21_upper.conf` and `brain_t21_pool65.conf` differ in **exactly one
directive** — `CASE upper` against `CASE lower`; `diff` over their `SCHEME`, `WORDS`,
`SLOT`, `POOL`, `EXTRA`, `BRAINHASH`, `BRAINSPACE` and `BRAINPUB` lines is otherwise
empty. Of the 81 distinct template words, **none is case-invariant**, so every
upper-case phrase differs from its lower-case counterpart in at least one byte, and
SHA-256 is case-sensitive. Two rows of the same size are therefore two bodies of
work, not one counted twice.

**[TESTED, 5 Nov 2026] `CASE title` has now run: `brain_t21_title`, exhausted, no
match — and with it the brainwallet case axis is closed.** Its own row, on the same
footing as the two above.

```
candidates   150,837,781,250              (65^6 x 2, six @POOL slots + slot 20's two words)
survivors    150,837,781,250              acceptance EXACTLY 1
addresses    452,513,343,750              (x3: compressed, uncompressed, hybrid)
identity     EXACT                        survivors == candidates == 2 x 65^6
result       exhausted, no match          exit 2,  HIT lines 0,  QUEUE DONE
wall         56,585.52 s = 15.72 h        2,665,660 cand/s, 0 thermal pauses
```

**Acceptance as an exact rational, as for the twin.** `Fraction(150837781250,
150837781250)` is **1** — not a quotient that prints as `1.000000000` — and the
deficit is **0**. No z-score is quoted and none exists: a brainwallet has no
checksum, so nothing scatters around an expectation and the identity *is* the test.

**The rate here is an exact average, and that is a different claim from the twin's.**
`150,837,781,250 / 56,585.52 s = 2,665,660 cand/s`. Both endpoints of an exhausted
run are known exactly, so this is not a progress-file reading and §10 rule 6's
chunk-quantisation caveat does not apply — but wall time includes startup and
teardown, so it is a **lower bound** on kernel rate. The `CASE upper` figure above
(2.672 M/s) is a rule-6 rate from 66 checkpoint-mtime intervals and is the stronger
measurement of the two; they agree to 0.2%. Wall differs from the twin by **+193.56
s, +0.34%**, which is what two runs of identical shape should look like. **0 thermal
pauses with the guard live**: `run_queue_brain.sh` invokes `./thermal_guard_queue`
(and `./selftest_gate`), there are 0 pause lines in either log, and `thermal.log` is
unmodified since 27 Sep — so this is an active-guard zero, not an absence of
records.

**One directive separates it from each twin.** With comments and blank lines
stripped, `diff` against `brain_t21_pool65.conf` and against `brain_t21_upper.conf`
returns **exactly one changed line each** — `CASE lower` and `CASE upper`
respectively, against `CASE title`. Same `SCHEME`, `WORDS`, 21 `SLOT` lines, `POOL`,
`EXTRA`, `BRAINHASH sha256`, `BRAINSPACE yes`, `BRAINPUB all`.

**Overlap with the image-text corpus: 0 of 34,354 strings**, measured. 592 strings
carry 21 space-separated tokens and could in principle be a phrase of this template;
**all 592 fail at slot 1**, which this config pins to `Subject`. Controlled in both
directions *before* the measurement: three phrases built from the template itself are
recognised as members, two deliberate near-misses are rejected. And the control that
matters for a casing run — **0 matches with case ignored as well**, so the result is
not an artefact of comparing `Subject` against `subject`.

**[MEASURED] The three cases are provably disjoint, and the check is the one that
could have failed.** Of the 81 distinct template words, **every one has three
distinct forms** under lower, upper and title; **no word is a single letter**, which
is the case where title would equal upper; and the three resulting word sets have
**no collision in any pair**. SHA-256 is case-sensitive, so every title phrase
differs from its lower and upper counterparts in at least one byte. Three rows of
equal size are three bodies of work.

**[EXHAUSTED] This closes the brainwallet CASE axis.** `lower` (29 Sep), `upper`
(4 Nov) and `title` (5 Nov), over the 21-word template on the 65-element pool: all
three exhaustive, all three at acceptance exactly 1 with survivors equal to
candidates, all three pairwise disjoint by the measurement above, all three negative.
There is no fourth uniform casing, and `brain_t21_upper.conf`'s header already
records why an "as-written" mode would have nothing to encode for a constructed
phrase — the drawn mixed-case strings are tested verbatim by the image-text corpus
instead.

**What is still open in this section, unchanged by this run: the key-variant
narrowing.** All three case runs inherit `sha256` + space-joined only — 3 addresses
per candidate, one scalar multiplication — against the **12** per candidate
(`BRAINHASH sha256 dsha256` x `BRAINSPACE yes no` x 3 encodings, 4 scalar
multiplications) that produced the t18 row's figure. So the t21 template is covered
over **one quarter** of the key-variant space the t18 result covered. Closing it is
an `_all` run and it does not exist. The case axis being closed does not narrow that
gap by one candidate.

**Combined brainwallet total, in addresses.** Quoted only because every pairwise
overlap above is 0; the five are disjoint by token count, by case, or by the measured
slot-1 test. `7,939,492,344 + 3 x 452,513,343,750 + 206,124 = 1,365,479,729,718`, and
the row count in this table is the only place the total comes from.

| brainwallet run | candidates / strings | addresses |
|---|---|---|
| t18 template over the 63-word pool, lower, 8 key variants | 992,436,543 | 7,939,492,344 |
| t21 template, 65-word pool, `CASE lower` (`brain_t21_pool65`) | 150,837,781,250 | 452,513,343,750 |
| image-text corpus, re-run 2 Nov | 34,354 strings | 206,124 |
| t21 template, 65-word pool, `CASE upper` (`brain_t21_upper`) | 150,837,781,250 | 452,513,343,750 |
| t21 template, 65-word pool, `CASE title` (`brain_t21_title`) | 150,837,781,250 | 452,513,343,750 |
| **union** | | **1,365,479,729,718** |

**[ASSUMED] What this union rests on:** the overlap tests above compared **strings**,
while the table's unit is **addresses**, and disjoint strings yield disjoint addresses
only because the maps between them are collision-free — SHA-256 from string to private
key, and HASH160 from public key to address (the scalar→point step is injective on
`[1, n−1]`). No collision is known for either, so the union holds; it is an
assumption rather than a measurement, and it is the only one in this table.

**That total is addresses, and it is never added to the BIP39 or Electrum
derivations.** The two counts answer different questions — a derivation is a seed
phrase resolved to a key, an address is one serialisation hashed — and a brainwallet
has no checksum, so the 1-in-128 convention that defines a derivation does not apply
to any row in this table. The §3 headline and this figure are reported separately for
that reason and must not be summed.

> **[SCOPE — CLOSED the same day]** ~~The §0 headline understates this count, and is
> left alone here.~~ The summary line read "plus 7,939,492,344 brainwallet addresses
> counted separately", which is the t18 row only — it omitted the 452,513,343,750 of
> the `CASE lower` t21 run from 29 Sep, and omitted this one too. The understatement
> was a factor of about 115 against the union above. **Corrected on the owner's
> instruction later on 4 Nov**: §0 quotes the union, which became
> 1,365,479,729,718 when `CASE title` landed on 5 Nov, with the
> strength distinction and a dated note of what the old figure omitted and for how
> long. The "left alone" sentence is struck rather than deleted, because it was true
> for the few hours it stood and the gap between noticing a defect and being
> authorised to fix it is itself part of the record.

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
mottos: it is `Esse quam niger es, sic dixit caccabus ollae` in the element
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

### 2.13 [EXHAUSTED; 90.6% of its space compressed-key only; 10 of 15 slots path 1 only] Free-one-fixed at 21 words: the branch that was never run

*[Heading updated 26 Oct: it read "99.6% … 13 of 15" until the runs admitted that
day, `t21_free20` above all, re-covered part of this space with all three key
encodings and put slot 20 on four paths. Computation in §3.]*

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
> *[9 Nov 2026: twelve, not thirteen — `t21_free20` closed slot 20 on 24–25 Oct, and
> `t21_free2` closed slot 2, admitted 9 Nov on an EXACT reproduction of
> `t21_free2_p1`'s logged 10,653,915,344. Eleven remain: slots 1, 4, 5, 7, 9, 10, 11,
> 12, 16, 17, 19 — and `t21_free11` closed slot 11, admitted the same day on an EXACT
> reproduction of the identity committed for it before launch, 10,654,060,452. **Ten
> remain: slots 1, 4, 5, 7, 9, 10, 12, 16, 17, 19.**]*
>
> **On paths 2–4, a single wrong word is still open at thirteen of the fifteen
> assigned slots.** Slots 3 and 13 are the only assigned slots closed on all four
> paths, and only since October 2026.
> *[26 Oct: slot 20 joins them. `t21_free20` ran the same 56-word box as
> `t21_free20_p1` on all four paths, so twelve of the fifteen remain open on paths
> 2–4. `t21_food11` and `t21_slot1_line` add particular words at slots 11 and 1 on
> four paths, not those slots' 55-word sets.]*
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

### 2.14 [EXHAUSTED; 98.3% of its space compressed-key only] Two hypotheses the source document itself named

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

**[MEASURED, external sources] The hooded bust is not Leopold II. It is the Charles
Didier Dreux monument,** S. Jefferson Davis Pkwy at Canal St, New Orleans. The
reviewing collaborator identified it from a press photo of its vandalism. Checked
here against the reports: the bust was found on Tuesday **1 May 2018** wearing a
white hood with red X's over the eyes, with "F— this sh—" spray-painted on the base
([The Advocate](https://www.theadvocate.com/new_orleans/news/report-new-orleans-confederate-monument-again-vandalized-covered-with-white-hood/article_d1e27e62-4d6f-11e8-9bdb-d75a49fd49b8.html),
whose article id is a version-1 UUID decoding to 2018-05-01 18:45 UTC;
[WBRZ](https://www.wbrz.com/news/monument-to-confederate-officer-defaced-in-new-orleans);
[WWL-TV](https://wwltv.com/article/news/crime/monument-to-confederate-officer-defaced-in-mid-city/289-547667411)).
The hood, the red X's and the base slogan match the drawing. The press photo itself
has not been compared with the drawing pixel by pixel here.

- **[INFERRED]** The X marks were painted by the vandals and copied by the artist.
  So README §19's step (Leopold II, `XX` = 20 → `second`) loses its basis twice:
  the bust is not Leopold, and the `XX` is a vandal's mark, not the artist's
  numeral. **Slot 20 has no supported word.** It has been tested over the 54-pool
  plus `apple` and `second` on **one path only**, `m/44'/0'/0'/0/0`
  (`t21_free20_p1`, in the ledger). The four-path config `t21_free20` exists but
  has never run. It has never been tested over all 2048 words. With the six gaps
  open on the 54-pool, that would be 50,779,978,334,208 candidates, about 51–53
  days at the measured 11.0–11.6M cand/s (about 49 at 12M). **Run it only with a
  defended fixed prefix.** *[Corrected 18 Oct: an earlier version of this line
  said four paths, taken from the config's name; the run log shows path 1 only.]*
  *[26 Oct: `t21_free20` has now run, on all four paths and all three key
  encodings: 10,847,704,031 survivors, equal to `t21_free20_p1`'s as the identity
  requires. Slot 20 over its 56 words is no longer path 1 only; it is still
  untested over all 2048 words.]*
- *Reported from the press photo, not re-measured here:* the artist left the name
  panel blank, replaced the inscription with the 13th Amendment §1 (with `subject`
  underlined, §9), and added the `BREATHE` neck band. The wreath plaque is blank
  in the photo, so its strokes are the artist's own: shading or an added `II`.

**[MEASURED] The plaque strokes have no counterpart on the monument's other flat
stone.** One detector for thin vertical dark segments (median width ≤ 3 px, ≥ 6 px
tall, ≥ 12 levels darker than the stone beside them) was run over the plinth cap to
the base step, x 1262–1494, y 640–1044, excluding the spray, the inscription and
the wreath. It finds 13 segments: 10 are outlines of the cap, plinth and base, 1 is
a wreath leaf, and 2 are letters at the inscription's edge. **None is a short
isolated stroke on open stone.** On the plaque, x 1376–1405, y 690–713, the same
detector finds the plaque's frame edges and 2–3 interior strokes at x 1383–1395,
y 697–709: 7–13 px long, 1–2 px wide, 33–58 levels of contrast. Script:
`circled_check/oct18_measurements.py`, section B.

**[INFERRED, 24 Oct] Where `apple` probably came from.** The clock's first rune word
◇⏶ᛗᛗ△ is `Сумма` (§7.3): five glyphs with the 3rd equal to the 4th. Read as five
Latin letters, it has the same pattern as `ELPPA`, which is `APPLE` backwards
(E-L-P-P-A, 3rd = 4th). README row 20 gives `apple` with an empty description, and
this pattern match is its most likely source. Only the letter pattern matches; no
key maps these glyphs to E, L, P and A (◇ is W in the Gravity Falls Latin key,
§7.3). The cipher is solved as Russian (§7), so `apple` has no basis, just as
`second` has none (the Dreux finding above). **Word 20 is unsupported under both
readings.** It is now being run over the 54-pool plus both words on all four paths
(`t21_free20`), which until now had run on path 1 only (`t21_free20_p1`).
*[26 Oct: completed, negative, in band; see the queues of 24–26 Oct at the end of §2.]*

> **[EXTERNAL, UNLOCATED — 9 Nov 2026] `apple@20` has a documented source, and it is not the
> inference above.** The paragraph above is *our* guess at where `apple` came from, reached from the
> clock's Russian rune word. The actual provenance is a named comment five years older, which reaches
> `ELPPA` by a completely different route. Recorded here with the grade blocks B and C carry, because
> **not one link in its chain has been measured in this project.**
>
> Source: **u/Accomplished_Weird36, comment `gn69cqa`, 2021-02-13 09:36 UTC, score 2.** Quoted in full
> rather than paraphrased, because the chain is the claim:
>
> > *"The Statue of Liberty book doesn't say SHT. The first character is a character from the author's
> > circular cipher from Gravity Falls. and the two letters TH are located in the fourth sector. If we
> > combine the second hand on these somvols, the hour and minute hands will show on the FR UI. And
> > you get FRUITH. So the first word next to the watch will be ELPPA, that is, APPLE. Also, the apple
> > is green where Trump and Biden are, and the question mark is the tail of the apple. If you can
> > further unravel the runes, then I am waiting for your thoughts. I didn't share this secret for a
> > long time."*
>
> The chain, link by link, with what we have measured at each:
>
> | # | link | measured here? |
> |---|---|---|
> | 1 | the tablet marks are characters at all | **no** — see the faint-group work below; the method is shown to have no power |
> | 2 | the first is from "the author's circular cipher from Gravity Falls" | **MEASURED, AND NEGATIVE** — §7.3 applies that very key to these glyphs: `◇` is **`W`** in the Gravity Falls Latin cipher (and `с` in the Cyrillic one). The identification was attempted and returned a letter the chain cannot use |
> | 3 | `TH` lies in "the fourth sector" | **no** — and no sector origin or direction is defined anywhere |
> | 4 | combining the second hand with those symbols yields `FR` and `UI` | **no** |
> | 5 | `FR` + `UI` + `TH` = `FRUITH` | **no** — this is the step that supplies the letters |
> | 6 | therefore the word by the watch is `ELPPA` | **MEASURED, AND NEGATIVE** — `ELPPA` requires `◇` = `E`; the only two keys we hold give `W` and `с` (§7.3). It also does not follow from 5 by any stated rule |
> | 7 | `ELPPA` reversed is `APPLE` | yes, trivially, and it is the only link that holds |
>
> **Seven links: four unmeasured, two measured and negative, one trivially true.** [CORRECTED
> 10 Nov 2026] Links 2 and 6 were first published here as "no — not attempted", which was wrong
> against this report's own §7.3 and against the paragraph immediately above this block, both of
> which state that `◇` is `W` in the Gravity Falls Latin key. **That identification was attempted
> and it came back `W`.** Recording it as unmeasured understated the result: an untested link
> invites a test, while a tested link that failed is already an answer. **This is a worse outcome
> for the chain than the version first committed, and it was available in the file at the time.**
>
> **This changes what §2.16 claims.** Saying `apple` has "no independent support" reads as a gap in
> the record — as though nobody had looked. The measured truth is worse and more specific: `apple@20`
> rests on an **unreproduced external method**, a seven-link chain of which we have tested one link,
> the trivial one. A gap invites someone to fill it; an unreproduced method invites someone to
> reproduce it, and those call for different work.
>
> **The same comment disputes the `SHT` reading** that §6 and `three_object_measurement.md` treat as
> open: *"The Statue of Liberty book doesn't say SHT."* It is one reader's assertion, dated and named,
> with no method attached, and it is recorded here as such — it neither closes the reading nor is it
> ignorable, since it is the earliest dated opinion on that group we hold.
>
> *A reference image of the Gravity Falls zodiac wheel was supplied on 9 Nov 2026. It carries **ten
> pictograms and no letters** — glasses, question mark, ice bag, crescent, pine tree, pentagram, hand,
> llama, shooting star, stitched heart. **This is the wrong artifact for this claim, by
> construction:** the chain needs letters — `TH`, `FR`, `UI` — and a wheel of pictograms has none to
> give, so no reading of it could bear on link 3 either way. [CORRECTED 10 Nov 2026: this note first
> said link 3 "cannot be evaluated", which pointed the reader at a missing measurement. The
> measurement is not missing; the artifact is simply not of the thing the claim is about.] The
> artifact that **does** bear on the chain is the letter-substitution alphabet, and §7.3 already
> holds it — that is where links 2 and 6 were tested, and failed. Holding an image is not the same
> as being able to test a claim, and this image is not evidence about the artwork.*

> **[MEASURED, 10 Nov 2026] The ten zodiac symbols, tested three ways: as words — closed; as
> locators — untested; as objects in the painting — swept.** The wheel came into this report on
> 9 Nov only as the wrong artifact for one link. It raises a hypothesis of its own, and that
> hypothesis has three separable forms. They are graded separately because they fail separately.
>
> **1. The symbols as the words — CLOSED, on the wordlist alone.** The rule applied, stated before
> the count: *a token must name the symbol, not a category containing it.* A hypernym admits
> anything.
>
> | symbol | BIP39 token naming it | |
> |---|---|---|
> | glasses | `glass` | also `eye`, `lens` |
> | question mark | `question` | also `ask`; `mark` is not BIP39 |
> | ice bag | `ice`, `bag` | both |
> | crescent moon | `moon` | `crescent` is not BIP39 |
> | pine tree | `tree` | **`pine` is not BIP39** |
> | hand | `hand` | also `palm`, `finger` |
> | shooting star | `shoot` | **and nothing else — `star` is not BIP39** |
> | stitched heart | `heart` | `stitch` is not BIP39 |
> | **llama** | **none** | `llama`, `alpaca`, `camel` are all absent from the list |
> | **pentagram** | **none** | `pentagram`, `pentacle`, `star`, `five` all absent |
>
> Eight of ten have a naming token; **two have none**. A construction that maps ten symbols to ten
> seed words cannot be built from a list that holds no word for two of them, so *"the ten symbols
> are the ten words"* **is closed**. Were hypernyms allowed, `animal` would admit the llama — which
> is exactly why the rule is stated rather than left to taste. Wordlist: 2048 words, `md5
> f23506956964fa69c98fa3fb5c8823b5` normalised, lengths 3-8. **Checked separately and independently:
> all nine confirmed words — `subject`, `tower`, `moon`, `camera`, `mask`, `liberty`, `eye`, `rifle`,
> `glove` — are BIP39. No defect there.**
>
> **2. The symbols as locators, or as an order — `[TESTED, NEGATIVE for 2 of 10]`.**
> *(Graded `[UNTESTED]` when this block was first written on 10 Nov 2026; regraded the same
> day, after the sweep in part 4 returned a result.)* The wordlist table in part 1 does
> **not** bear on this form and must not be cited as though it did. The sweep does.
>
> **A symbol that is not drawn cannot locate anything.** Two of the ten — **pentagram** and
> **pine tree** — are now measured absent from the whole image at every contrast level
> swept, each with its planted control recovered at every one of those levels. That is
> evidence against the whole set being present, and it is **independent of the llama's
> no-power result**: a pine tree and a five-pointed line star are easier to draw and far
> easier to detect than a quadruped, so they are the two the sweep was most likely to find
> if the set were there, and they are not there.
>
> **Two of ten is not ten of ten.** Eight symbols remain unswept or unresolved, the sweep
> cannot see a symbol rendered small, faint or stylised beyond its criteria, and nothing
> here touches an ordering that uses the wheel without drawing it. The grade is therefore
> negative *for the two tested*, and the form as a whole is weakened rather than closed.
>
> **3. This is not the dial finding, and the dial finding must not be cited here.** R10
> (`r10_layout.py`, `STOP_R10_SET_C.md`) asks whether the artwork's elements are laid out on the
> **clock** dial: hub (473.75, 940.0), twelve numerals 30° apart, a 24-direction grid every 15°,
> pre-registered element list, two nulls. That negative governs the clock. **It says nothing about
> symbols scattered through a painting as locators**, and citing it against this form would be
> borrowing a measurement's authority for a question it never asked. *Dated note: the brief that
> prompted this entry attributed to us a measurement of "the Bill Cipher wheel as the clock dial,
> rejected on geometry, 36° against 30°". **No such measurement exists in this repository** — no
> `36°` figure appears in any file of it, and R10's wheel is the twelve-numeral clock, not a
> ten-symbol zodiac. The distinction the brief asks for is correct and is recorded here; the
> measurement it credits us with is not ours, and this report does not adopt it.*
>
> **4. The symbols as objects in the painting — swept, whole image.** Pre-registered in
> `zodiac_sweep_plan.md` (commit `6f1c1cd`, blob `39fc08a9…`) **before the sweep ran**; executed by
> `zodiac_sweep.py` → `zodiac_sweep.out`. Four targets only — **llama, pine tree, ice bag,
> pentagram**. Star, heart, hand, moon, glasses and question mark were **deliberately excluded**:
> they are free in any crowded painting, this one already contains a question mark, hands, stars on
> a flag and a figure in glasses (`E01`), and reporting them as hits would be §1.7's shape. Block
> B's seven cuts (`90, 110, 130, 150, 170, 190, 215`), whole image, 2,167 components in the size
> band across the seven passes, planted controls at 20/40/80/160 px.
>
> | target | control recovered | candidates | what they are |
> |---|---|---:|---|
> | **pentagram** | 40-160 px, cuts 90-190 | **1** (0.05%) | a **letterform** in the slogan block, x 1170-1196 y 250-296 — inspected and refuted |
> | **pine tree** | all sizes, all cuts | **34** (1.6%) | **all letterforms, the Great Seal pyramid and one portrait blob** — the best fit in the whole painting (r² 0.94, x 619-679 y 803-871) is the **pyramid** (`E13`), and the 269×281 one is the George Floyd portrait (`E19`). No conifer |
> | **ice bag** | all sizes, all cuts | **1,466** (**67.7%**) | **the criterion is void** — it admits two thirds of everything in the painting |
> | **llama** | **none, at any size** | — | **no power; no absence claim is made** |
>
> **Result: pentagram and pine tree are absent at all levels swept** — every candidate was inspected
> and every one is lettering, the pyramid, or a portrait. **The ice-bag test measured nothing**: a
> criterion that passes 67.7% of all components is not a detector, and reporting its 1,466 hits as
> candidates would have been the same error §1.7 names. **The llama — the highest-value target,
> because nothing else in a BLM scene looks like one — was not tested at all**: the detector could
> not recover its own planted control at any of the four sizes, and a method that cannot find a
> shape it was handed cannot be cited as evidence the shape is missing. Two of four targets
> therefore return **no result**, and that is the honest reading of this sweep.
>
> **The llama, looked at rather than computed** [10 Nov 2026]. The detector was **not**
> retuned: `STOP_R10_SET_C.md` is right that adjusting criteria after seeing the result is
> how a false positive arrives, and a retuned llama test would need a fresh
> pre-registration. Instead the image was inspected by eye, which makes no statistical
> claim and needs none. **25 overlapping tiles at 4×**, each 400 × 300 px of the master
> with 100 px horizontal and 75 px vertical overlap, in a 5 × 5 grid covering every pixel
> of the 1600 × 1200 image at least once. Every tile was looked at.
>
> **Nothing resembling an animal is depicted anywhere in the painting.** No quadruped, no
> bird, no llama. The only living figures are the eight humans already inventoried — the
> four masked protesters, the Floyd portrait, Trump, Biden and the Statue of Liberty — and
> every other object resolves to one already in the record: the flag, the fist emblem, the
> vial and glove, the two cameras, the rifle, the Space Needle, the Great Seal disc and its
> pyramid, the Leopold bust and plinth, the book stack, the slogan block, the micro-text
> letters, the clock, the faint Washington state outline and the artist's `-CHR-`
> monogram.
>
> Two forms were ambiguous at tile scale and were re-cropped at 8×:
>
> - **The ornament above the Great Seal's ribbon** (x 450-560, y 895-985) is a **scroll
>   with a flame or sprout above it**, part of the seal device. Not a bird.
> - **A grey form at the Leopold bust's collar, now measured** — see the block below. The
>   description first written here on 10 Nov ("almost certainly the knotted end of the red
>   bandana", on a symmetry argument, at x ≈ 1330-1375, y ≈ 505-545) is **retracted in both
>   its coordinates and its reasoning**. The form is at **x 1349-1373, y 509-541**.
>
> **5. `hat`.** `hat` **is** BIP39 and is **not** among the nine confirmed, so a depicted hat would
> be a genuinely new candidate word. **Measured: none is depicted.** The pre-registered 28-element
> inventory (`r10_elements.json`) contains no hat, and all eight human figures were inspected
> directly — the four masked protesters (`E01`-`E04`), the Floyd portrait (`E19`), Trump (`E26`),
> Biden (`E27`) and the Statue of Liberty (`E08`): **every one is bare-headed.** Liberty wears her
> spiked **crown**, which this report already counts for `liberty`@7 and which is not a hat. So
> `hat` gains nothing and joins no slot. *Kept separate, as it must be: a reference image of Bill
> Cipher in a black hat **is not this painting**, and `black` is already supported by two other
> routes (§2.13's rune line and the slogan block) and gains nothing whatever from a hat.*

> **[MEASURED, 10 Nov 2026] The collar form: three pre-registered tests, three defects
> found in them, and one firm negative.** Method, boxes, controls, decision rules **and the
> word consequences** were fixed in `collar_form_plan.md`, committed in `4cd5eab`
> (blob `ffda5dd6…`) **before** `collar_form.py` ran. Output `collar_form.out`; the
> post-hoc diagnostic that follows is in `collar_form_diag.out` and is labelled as post-hoc
> wherever it is used.
>
> **The 10 Nov reading is retracted.** It said the form was "almost certainly the knotted
> end of the red bandana" and rested that on a symmetry argument. **The symmetry is not
> there**, and the box it was measured in was wrong.
>
> | test | result |
> |---|---|
> | **(a) symmetry, with a garment control** | Mirroring the form about every axis from x 1374 to 1410 in 0.5 px steps, the **best** correlation is **r = +0.310** (axis x 1387, partner box x 1401-1425). Against 252 same-size garment patches mirrored the same way: mean −0.003, sd 0.268, **max +0.447**, 95th percentile +0.329. The partner sits at the **92nd percentile, z = +1.17 — inside the control distribution.** **SYMMETRY IS NOT ESTABLISHED.** The only support the 10 Nov entry offered is gone |
> | **(b) hue** | **Void as pre-registered — the test was circular.** The decision rule compared the form's saturation to the bandana's, but the bandana mask was *defined* as `S ≥ 0.35`, so its 5th percentile is 0.358, the mask's own floor. Any desaturated pixel was guaranteed to pass. The verdict it printed — "not bandana under any lighting" — **means nothing and is withdrawn** |
> | **(c) the glint** | **Artifact as pre-registered.** It reported *no* bright cluster beside the dark one. **51% of the pre-registered form box is background sky**, which set the 90th-percentile bright threshold at 0.847. On the form's own pixels the threshold is 0.468 and **the glint is real: 4 px at x 1357.5 y 518.5, +61.9 levels over its local surround** |
>
> **What replaces (b), measured on the form's own 378 pixels** [post-hoc, and a conclusion
> resting on it needs a fresh pre-registration]: **65% of them lie in the red hue band**,
> median hue ≈ 0.95. The form is **red** — dark and desaturated, but red — which is what a
> **shaded or anti-aliased edge of the red bandana** looks like. So the cloth reading
> survives, **on evidence I did not offer for it**, while the evidence I did offer failed.
>
> **The glint's control was the wrong garment.** Its contrast (+61.9 levels) exceeds every
> comparable bright cluster on the **coat** (15 found, median +1.1, max +9.5), and the
> dark-plus-bright pair is common there (7 of 8 comparable dark clusters have one). But the
> form is bandana-coloured, and no highlight control was drawn **from the bandana**, which
> is the comparison that would settle it. The plan did not ask for one. **That is the test
> still missing.**
>
> **Status: cloth is supported by hue, symmetry is refuted, and the object is not
> identified.** Under the plan's §2, fixed before any of this ran: **no word follows, under
> any outcome.** The form is recorded as **an unidentified form at x 1349-1373, y 509-541**,
> and the next step, if anyone takes it, is identifying it *from the pixels* with a fresh
> pre-registration — a clean box excluding sky, a non-circular cloth comparison, and a
> highlight control drawn from the bandana.
>
> *The `leopard`/Leopold pun is recorded here and was **excluded from the identification**
> by the plan, in writing, before the measurement: the bust is of Leopold II and `leopard`
> is a BIP39 word, and that is a reason for a stricter test, never a candidate. Nothing in
> these measurements shows spots or a feline skull, and nothing proposes a word.* **This is
> not the zodiac llama under any outcome** — that is a full-body pictogram, a head alone is
> a different object, and §2.16's locator grade stays `[TESTED, NEGATIVE for 2 of 10]`.

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
| 3 | `tower` | **written** on the minute hand | clock 1+2, under a caption that says to add two numbers — **the caption is unlocated, see below** |
| 13 | `moon` | **written** on the second hand | clock 12+1, same caption, same caveat |
| 2 | `camera` | depicted | a count of cameras |
| 4 | `mask` | depicted | a count of masked faces |
| 7 | `liberty` | depicted | a count of crown points |
| 9 | `eye` | depicted | pyramid 4+5 |
| 16 | `rifle` | depicted | the 16 of M16 |
| 19 | `glove` | depicted | the 19 of CVD19 |
| 5 | `police` | depicted — and **written** on the canvas, in `END POLICE BRUTALITY` of the slogan block (word_census.tsv, 31 Oct). Like `black` at 10 this is running prose with no positional mark, so it is **not** a support upgrade: it says where the word came from, not where it goes | "line five" — a convention used nowhere else in the table |
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

> **[MEASURED, 9 Nov 2026] Two of the slot *numbers* in this table are sub-pixel in
> this file, so neither can be checked against the image.** The `16` of M16 (rifle
> receiver, x 816–825 y 695–702: 19 levels, peak stroke **0.09 px**) and the `19` of
> `CVD19` (vial label, (130, 230, 50, 60): 110 levels, peak stroke **0.63 px**) are both
> below one pixel of stroke coverage, against **full pen for every legible control** —
> measured on §6 item 6's own model, and tabulated there. Slot 16's number is not read
> from the picture at all but inferred from the weapon's shape, and **no count of 16
> exists anywhere in the image** (`even_slot_rules.py`). This changes no row above. It
> says that two rows' slot arguments cannot be verified from pixels — and that §5's
> second leg, which derives the phrase *length* from slots 16 and 19 without the clock,
> inherits exactly that status. (§5 also considered slot 17 and struck it: the `17` is
> read off a chart whose content postdates the funding transaction, so §10's chronology
> rule kills the slot justification. The row stays; the rung goes.)

> **[SCOPE, 9 Nov 2026] Slots 3, 13 and 21 rest on a caption this project has never
> located.** The clock rows above derive their slot numbers by *adding* the two
> numerals each hand falls between — 1+2 = 3, 12+1 = 13, 10+11 = 21. The only thing
> in the artwork that licenses that addition is the rune caption `Сумма двух чисел`,
> "sum of two numbers". Its 14 glyphs have **no measured location**: a defined search
> around the dial (centre (470,937), radius ~182, ink < 130/180/215) returns zero
> glyph-sized components — **and that disc is only 15.1% of the bottom third by area,
> so 84.9% of the region the transcriber's own wording names has never been searched
> (§7's provenance note, 9 Nov)** — and its transcription is `u/Amadeus407`'s of 2021-03-06,
> adopted into this report in `77f2c52` and never re-derived from pixels (§7's
> provenance note).
>
> **Nothing here is retracted and the hand measurements are untouched.** The hands
> themselves are measured — 332.38°, 302.62°, 238.49°, all three landing between the
> numerals the table names, two of them within 1.4° of a midpoint — and §7.5 places
> the caption among the numerals, which is exactly where small glyphs are hardest to
> isolate from dial marks. The mechanism may be perfectly real. But a reader weighing
> slots 3, 13 and 21 should see that the *sum* step, as opposed to the *direction*
> step, rests on one solver's 2021 reading of a block that has never been found, and
> that slot 21's hand is additionally four times further off its midpoint than the
> other two.

> **[SCOPE, 9 Nov 2026] The same caption would license two more slots, and the standing
> instruction was narrower than the mechanism.** The note above names slots 3, 13 and
> 21 — the three hands. But the operation it licenses is *"sum the two numerals a thing
> lies between"*, and **two other assigned slots are built by exactly that operation on
> the same dial**, measured in `clock_overlap_measurement.md`:
>
> | slot | word | object | angular span | numerals spanned | sum |
> |---|---|---|---|---|---|
> | 9 | `eye` | eye triangle + radiating rays | 38.9° – 78.9° | 4 and 5 | **9** |
> | 11 | `pyramid` | pyramid brick body | 74.0° – 136.6° | 5 and 6 | **11** |
>
> **So one of two things is true, and this report does not choose between them.**
>
> **Branch A — the caption licenses the operation.** Then it licenses **five** slots,
> not three: 3, 13 and 21 from the hands, 9 and 11 from the objects. Four of the fifteen
> assigned slots, plus the slot-21 gap, rest on one block with no measured location, and
> every place this report says so for 3, 13 and 21 should say it for 9 and 11 as well.
> §5's "the clock can only produce ODD slots" is untouched either way — 4+5 = 9 and
> 5+6 = 11 are both odd, as the argument requires.
>
> **Branch B — the caption is specific to the hands.** Then slots 9 and 11 **never had
> a licence at all**, which puts them *below* 3, 13 and 21 rather than beside them:
> those three rest on an unlocated licence, these two on none. And it has a consequence
> that is already settled — if the sum reading of the objects is unlicensed, the
> motivated alternative is the **single** numeral each object sits on, `eye`@4 and
> `pyramid`@6, which is precisely what `t21_single` ran over 54⁷ × 2 and returned
> negative and in band. So under branch B the better-motivated reading of 9 and 11 is
> **closed**, and the reading the template actually uses is **unlicensed**.
>
> **Evidence bearing on the branches, reported without adjudicating.** It is
> asymmetric, and both halves are already in the tree. Against branch A:
> `report_additions_image_pass.md` §I pre-registered a test of whether the artwork is
> laid out on the dial at all — 28 whole-object elements, two nulls, decision rule fixed
> in code — and found **3 of 28 within 0.5° against 1.9 expected, p 0.28 / 0.28, NOT
> SIGNIFICANT**, concluding that *"the clock governs the hands and the seal only."*
> For branch A: `clock_overlap_measurement.md` measures these two spans directly and
> grades `pyramid`@11 measured and `eye`@9 suggestive. And its own recorded caveat cuts
> against itself — **an object that size covers two numerals automatically**, the
> pyramid spanning 62.6° where a sector is 30°. The two are different tests, one of
> global layout and one of two specific spans, and nothing here picks the winner.

> **[OPEN, UNTESTED — and narrower than it first looks] What the caption dependency
> does and does not reopen.** It does **not** reopen "some other word sits at slot 3"
> or "at slot 13". `t21_free3` and `t21_free13` are both in the evidenced ledger and
> both swept their slot over **55 words** — the 54-word pool *plus* the pinned word
> itself, since neither `tower` nor `moon` is in the pool — and both came back
> negative. Those two questions are closed and the caption does not revive them.
>
> **What it opens is the converse, and no run has ever entered it: `tower` and `moon`
> at slots other than 3 and 13.** If the addition is wrong, the natural alternative is
> the *single-numeral* reading of each hand — the numeral it is nearest rather than the
> sum of the two it lies between. Measured across all 94 configs in the ledger,
> evidenced and asserted, by which slots ever admit each word:
>
> | word | slots that have NEVER admitted it, anywhere in the ledger |
> |---|---|
> | `tower` | **1, 2**, 4, 5, **12**, 16, 20 |
> | `moon` | **1, 2**, 3, 4, 10, **12**, 16, 20 |
>
> The minute hand lies between numerals 1 and 2, so its single-numeral readings are
> `tower@1` and `tower@2` — **both in that never-tested column**. The second hand lies
> between 12 and 1, so its readings are `moon@12` and `moon@1` — **also both
> untested**. The clock-rotation family (`t21_clk2`–`clk9`) moved these words around a
> good deal — `tower` has been tested at slots 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18,
> 19 and 21 — but never to slot 1, 2 or 12, because those slots stay pinned to
> `subject`, `camera` and `vote` in every config built so far.
>
> **This is a specific swap family, not an `a ≥ 2` sweep — and it is not cheap. An
> earlier version of this note priced it wrongly, by a factor of 54.** Four placements:
> `tower@1`, `tower@2`, `moon@12`, `moon@1`, each displacing one pinned word
> (`subject`, `camera`, `vote`, `subject` respectively).
>
> > ~~Each keeps the template's shape, so each is one `t21_readme54`-sized run —
> > 49,589,822,592 candidates, about 1.25 GPU-h at 11 M cand/s, roughly 5 GPU-h for all
> > four. That is the same shape and the same cost class as `t21_single`, which tested
> > the single-numeral reading of the clock overlap for `eye` and came back
> > negative.~~ **[RETRACTED, 9 Nov 2026 — wrong by 54×. It reached for the right
> > precedent and then quoted the wrong price: `t21_single` is 54⁷ × 2, not
> > 54⁶ × 2.]**
>
> The single-numeral reading says where `tower` goes. **It says nothing about where
> `subject` goes**, and this project's own precedent is to drop the displaced word
> rather than hand it the vacated slot: `t21_single` moved `eye` to slot 4 and
> `pyramid` to slot 6, **dropped `mask` entirely**, and vacated slots 9 and 11 to the
> pool. On that shape the vacated slot is not filled, it is **freed**, which is a net
> gain of one gap:
>
> | | shape | candidates | band (survivors) | GPU-h each |
> |---|---|---|---|---|
> | **as priced** | pin the word, **free** the vacated slot — 7 gaps | **54⁷ × 2 = 2,677,850,419,968** | 20,920,706,406.0 ± 141,701 | **67.6** |
> | pure-swap probe | hand the vacated slot the displaced word — 6 gaps | 54⁶ × 2 = 49,589,822,592 | 387,420,489.0 ± 19,283 | 1.25 |
>
> The upper row is **exactly `t21_single`'s space and exactly its band** — 54⁷ × 2,
> σ 141,701, stratified at 0.983533 on this same 54-word pool, recomputed here from the
> pool's own 16 block counts rather than copied. `QUEUE_after_el22.md` states the rule
> in capitals for that run: *"Filling slot 6 while vacating 9 and 11 is a NET GAIN of
> one gap, so the space is 54^7 x 2, fifty-four times t21_readme54."* The same
> arithmetic applies to all four placements. **Four members: 10,711,401,679,872
> candidates, 83,682,825,624 derivations, 270.5 GPU-h = 11.3 days** — **16% of the
> 69-day queue, not the 0.3% the retracted figure implied.**
>
> **The pure-swap probe is kept, and labelled: there is no mechanism behind it.**
> Nothing in the artwork says a displaced word moves to the slot its replacement
> vacated. Here the displaced word's own support actively contradicts the move:
> `subject`@1 rests on "Section 1 numbering" (the table above), so `tower@1`
> **overrides** that support rather than relocating it, and a word whose only slot
> argument has just been overridden has no claim on slot 3 or on any other slot. The
> probe is worth 1.25 GPU-h as a lottery ticket. It is **not** a down-payment on the
> full run.
>
> **[MEASURED, 9 Nov 2026] And the probe is not contained in the full run — the two
> boxes are disjoint, not nested.** `subject`, `camera` and `vote` are **none of them in
> the 54-word README pool** (measured against `configs/t21_readme54.conf`), so freeing
> slot 3 over that pool never reaches `subject`@3: the pure-swap point lies **outside**
> the 54⁷ box, not inside it. Unioning the two means freeing the vacated slot over
> **55** words — the pool plus the *displaced* word — for 54⁶ × 55 × 2 =
> 2,727,440,242,560 candidates, **+1.85% over 54⁷ × 2**, 68.9 GPU-h. Recorded because
> that is a *different* 55 from §2.13's (which is the pool plus the slot's **own** table
> word, `tower`), and because at +1.85% it would make the separate 1.25 GPU-h probe
> redundant.
>
> **Not built, not queued, not started.** The 69-day path-closure queue decision is
> open and unanswered, and nothing enters the GPU before it is settled. Recorded here
> so the family is named and sized rather than rediscovered: the hour hand needs no
> entry, because the slot its sum names (21) carries no word to relocate.

**[MEASURED] Who first claimed each word — no assigned word traces to the
author.** The table above asks what holds a word up in the artwork. This one
asks who first said it. Together they close the loop.

| hint | first posted by | date |
|---|---|---|
| `moon`, `tower`, `real`, `subject` | u/boriserd | 2020-10-12 |
| `Tuesday` | u/hmm_dimasiki | 2021-01-10 |
| `food` | u/meserit | 2021-01-31 |
| `breathe`; `subject` "underlined" | u/Accomplished_Weird36 | 2021-02-02 |

> **[MEASURED 4 Nov 2026, from Reddit's own JSON for the post] The old-Electrum
> wordlist was proposed on 2021-03-01, five years before this project, and the
> credit is not ours.** `u/DiOnline`, comment `gpaw1ca`, **2021-03-01 14:35:28
> UTC**, verbatim:
>
> > *"The author is unlikely to reveal himself, I did contact the OP and other
> > individuals I thought could have produced the image above. However, as a tip,
> > don't just consider BIP39 words, try the Electrum Old Word list too since words
> > like Breathe aren't in BIP39, but are in Electrum."*
>
> Also from the same JSON: the submission's `selftext` is **length 0** and its
> `selftext_html` is `null`, and **`u/stsh_n` appears as the author of 0 of the
> comments present**. The post is `j79zvj`, posted **2020-10-08 09:25:30 UTC**,
> titled *"Bitcoin puzzle (2000$)"*.
>
> *Provenance, because this note previously said the opposite.* It read
> `[UNVERIFIED — owner-supplied]` and then `[OWNER-VERIFIED … not reproduced
> here]`, because `reddit.com` is unreachable from the environment these
> measurements are made in — `curl` gets HTTP 403, the sanctioned fetch tool
> refuses the domain, and the `pullpush.io` mirror answers 521. The owner then
> supplied the fetched JSON itself (sha256
> `39d61b72865029205f0a2fce600a895a2599f8c1b4a4091ead9aa13912cab7c7`, 394,935
> bytes, two byte-identical copies), and every figure in these notes is now parsed
> from that file rather than quoted from anyone. **It is not committed to this
> tree, and the reason is a real one — see the note on the phrase guard below.**
>
> **One narrowing kept from the earlier version, because the claim as offered was
> broader than the source can carry.** "The author has never written a word
> anywhere" is not a fact one thread's JSON can establish. What it establishes is
> the two things stated above: the body is empty, and the author wrote none of the
> comments present. DiOnline's *"I did contact the OP"* is DiOnline's account of
> his own action, not evidence about the author's silence, and is quoted as such.
>
> **[MEASURED] But DiOnline is not the first mention of the Electrum wordlist, and
> this report would have got the priority wrong too.** `u/RaTMaTaT`, comment
> `gmlbct5`, **2021-02-08 15:55:08 UTC** — three weeks earlier — wrote *"TRADE is
> also the Electrum world list."* Those are the only two Electrum mentions in the
> 168 comments present, besides a 2026 post about this project's own repository.
> The distinction that matters, and it favours DiOnline: `trade` is in **both**
> wordlists, so RaTMaTaT's observation does not discriminate between them, while
> DiOnline's turns on `breathe` being in the old list and **not** in BIP39 — which
> §1.1 measures and confirms. So **RaTMaTaT raised the Electrum wordlist first
> (2021-02-08); DiOnline made the first argument that picks out the *old* list
> (2021-03-01)**. Neither is us.
>
> What this project can still say for itself is narrower and holds: we were first
> to **run** Electrum v2, and nobody including us has run old Electrum.

> **[MEASURED, 4 Nov 2026] The absence is real but it is an absence over two
> thirds of the thread, and the reconciliation is published rather than rounded.**
> Parsing the JSON's comment tree:
>
> ```
> num_comments field                  254
> comment objects present             168   (10 of them [deleted]/[removed])
> "more" stubs                         27,  hiding 80
> present + hidden                    248
> unaccounted for                       6
> ```
>
> Over those 168, the hit count for `polyline`, `yellow`, `identify`, `bracket`,
> `loop`, `focus` and `dance` is **0 for every one of them** — which is what showed
> the AI archive's "yellow polyline" section to be fabricated. But the words
> *"confirmed absent from the thread"* **overstate what was searched**: 86 comments
> were never read, and `168 + 80 = 248` leaves six unaccounted against the stated
> 254. Both are recorded so the next reader does not mistake a two-thirds search
> for an exhaustive one.
>
> **The fabrication is nonetheless worse than "attributed to an unreachable
> user".** `Desalzes_` is a **real participant** with comments present in this
> JSON, and the string `desalzes` occurs exactly once in the 168 bodies — in
> `u/mrvclr`'s 2026 round-up, tagging him to compare notes. So the archive took a
> genuine username from the thread and attached to it pixel findings that nobody
> in the thread ever wrote. That is a sharper failure mode than inventing a person,
> because the name checks out.
>
> **[NOT COMMITTED, and why.]** The obvious close for all of this is to commit the
> JSON so every claim becomes a permanent `grep`. It is **not** committed, because
> `pre_push_check.sh`'s phrase guard would block it for a correct reason:
> `boriserd`'s comment `g8lip0e` contains a **19-word run of consecutive BIP39
> words**, which is exactly the shape of thing the guard exists to stop leaving
> this tree. Committing it would mean pinning a file that genuinely does add
> candidate phrase material, and that is the owner's call and not a mechanical one.
> The file's sha256 is recorded above so anyone holding the same bytes can re-run
> every figure in these notes. For the same reason the comment is **cited by id and
> date below rather than quoted**.
>
> **[MEASURED against the same JSON, 4 Nov 2026] Three further items, recorded
> where they bear on something this report says.**
>
> - **`boriserd`, comment `g8lip0e`, 2020-10-12 15:16:14 UTC** — the earliest word
>   list, **4.24 days** after the post. The attribution table above already credits
>   `moon`, `tower`, `real` and `subject` to that user on that date, and the primary
>   source agrees with it exactly. This is the one item of the four where the report
>   was already right, and confirming a table rather than correcting it is worth
>   recording as such. The comment is **cited and not quoted**: its word list is a
>   19-word run of consecutive BIP39 words, and reproducing it here would put
>   candidate phrase material into this file for no gain, since every word in it is
>   already credited individually in the table.
> - **`Solid-Battle-9198`, comment `gldqys9`, 2021-01-30 16:44:20 UTC** — *"For now
>   I put future as the first word. Much like I put subject as number 13."* This
>   report credits **words** to the community and never credited **positions** to
>   anyone; slot hypotheses appear here as this project's own enumeration. Nothing
>   is retracted, because no competing priority was ever claimed, but the earliest
>   proposal of a *slot map* is this comment and not us.
> - **`hmm_dimasiki`, comment `gkezuop`, 2021-01-23 17:54:05 UTC** — *"It turned out
>   **28 unique characters**, not counting the vertical three-dot sign … this is
>   WITHOUT the word 'Tuesday' from Gravity Falls. The Latin and English alphabets
>   contain 26 letters each."* That is a cross-check on the premise behind §7.4 and
>   the open ask at the end of this report: 28 distinct glyphs against the Gravity
>   Falls cipher's **26** means the author invented **two**, which is what "the
>   author invented glyphs beyond the 26" has asserted without ever putting a number
>   on it. **This project has not independently counted the glyph inventory.** The
>   figure is recorded as a target for that count, not as the count — and the
>   comment's own closing alternative, *"or it is a transcription of another
>   language"*, is what §5 went on to establish for the Cyrillic runes.
>
> **[OPEN, CHECKABLE] `DiOnline`, comment `gr081s3`, 2021-03-15 12:33:08 UTC**:
> *"There are hidden sentences with runes, numbers and words hidden across the
> puzzle, but they are extremely difficult to find, at least with Photoshop and
> Forensically. One such phrase is 'TO TEST USE WORDS' accompanied by 'FIRST THE
> AT'."* The **comment** is verified here from the JSON; the **text it claims** is
> unverified by anyone, and it is the rare claim in this thread that is
> **testable against the artwork we already hold**, with the §9 pixel method and
> the detector-plus-control discipline `yellow_polyline.md` uses. It is listed
> here rather than acted on because it would be a new pixel pass, and because a
> 2021 forensic read of a JPEG-recompressed copy is a common way to see text that
> is not there. Recorded so that it is either tested or declined deliberately,
> not forgotten.

> **[MEASURED] Three things in the same JSON that nobody asked about and that bear
> on this report directly.**
>
> - **This project's own figures are in that thread, and they are stale by 26×.**
>   `u/mohamedabb`, comment `p5auds6`, **2026-08-22 22:09:22 UTC**, posts a link to
>   `github.com/rarsn4/blm-0.2btc-analysis` and tells the thread *"I've also
>   eliminated 12 billion seed derivations (BIP39/Electrum)"* and *"there are 4
>   errors in it"*. §3's evidenced figure is **316,456,008,920**, and §1 now counts
>   six defects in the shared data plus two of this project's own. The post is not
>   ours and we cannot edit it, but a reader arriving from that comment will be
>   **26× low** on the headline and short two defects, so the discrepancy is
>   recorded here rather than left for them to discover. It also means the Electrum
>   work was publicly claimed in the thread in August 2026 — after DiOnline's 2021
>   tip, and still only for v2.
> - **The `CHR` stamp has independent corroboration.** `u/Purple-Pressure-994`,
>   comment `19rhs25whqyap`, **2026-10-22 17:18:33 UTC**: *"at the bottom right of
>   the bust is a stamp in the form of the inscription CHR"*. §1.8 admitted `CHR`
>   to the canvas census on 2 Nov 2026 from this project's own pixel reading, ten
>   days later and without knowledge of this comment. Two independent readings of
>   the same mark agreeing is worth more than either alone, and it is the only
>   element of the five admitted on 2 Nov that a third party has stated out loud.
> - **An open lead on the one thing §7.4 says it still needs.**
>   `u/Great_Bottle_5486`, comment `19rn3upe96bkx`, **2026-10-25 16:58:35 UTC**: *"I
>   have a lastglyph.png I was wondering if you maby can check it out"*. The ask at
>   the end of this report is a **key** for the invented glyphs, not a better scan;
>   a third party's crop of the final glyph is not that key, and §2.9 plus the
>   byte-identity measurement above establish there is no higher-resolution source
>   to be had. Recorded as a lead, with the warning attached: a file named
>   `lastglyph.png` from an unverified source is somebody's *interpretation* of the
>   glyph unless its provenance is established, and this project reads pixels from
>   one file at one pinned sha256 for exactly that reason.

> **This does not touch `yellow_polyline.md`, and the reason matters.** That
> document and `yellow_polyline.py` are **this project's own pixel measurement**,
> dated 3 Nov 2026 on the master image at its pinned sha256, with a stated
> detector (`Y = min(R,G) − B`), a stated threshold justified by a gap in the
> histogram, and a closure argument. They cite no thread, no Bitcointalk and no
> archive; the string `desalzes` appears nowhere in this tree. What the archive
> fabricated was an *attribution* of polyline findings to a forum user, and that
> attribution was never in this report. **Nothing there needs marking** — recorded
> because a reader who saw both documents might otherwise assume the measurement
> came from the thread, and the independence is what protects it.

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

> **[MEASURED 4 Nov 2026] The circulating file is the upstream file, bit for bit,
> and the resolution ceiling is now a measurement rather than an assumption.**
> `https://i.redd.it/n1x7g8ceaur51.png` was re-fetched on 4 Nov 2026 — HTTP 200,
> `2,383,395` bytes, sha256
> `d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782`,
> **1600 × 1200** RGBA PNG — and `cmp` reports it **byte-identical** to
> `0.2-btc-puzzle.png`, the file `imgio.py` has pinned to that same sha256 since
> the beginning. The md5 above is kept; sha256 and the pixel dimensions are added
> because the md5 alone states identity without stating what was identical.
>
> This retires an assumption the project has carried. Every pixel claim in §9 and
> in `yellow_polyline.md` rests on there being no higher-resolution original to go
> back to, and that has until now been supported by a solver's remark
> (HomelessPhD's "only picture I've seen") rather than by measurement. Reddit's own
> upload record, read here from the post JSON, offers previews at widths
> 108/216/320/640/960/1080 over a **source of 1600 × 1200** — so the largest thing
> Reddit ever held is the thing we have. **1600 × 1200 is the ceiling**, the
> magnified renders in §9 are interpolation and nothing more, and a future reader
> asking "was there a better scan?" has an answer instead of an inference.
>
> *One figure does not reconcile and is left visible rather than smoothed.* This
> paragraph says **273** archived thread comments; the JSON's `num_comments` field
> reads **254** as of 4 Nov 2026, with 168 comment objects present. Both cannot be
> the live number. The sentence above — "wrote none of the 273" — is therefore a
> claim about the archive it was taken from, and what the primary source supports
> is the narrower statement now made in §1.1: **`u/stsh_n` is the author of 0 of
> the 168 comments present, and the submission's `selftext` is length 0.** The
> thread is also still live — the most recent comment in the fetch is dated
> **2026-11-04 20:02:34 UTC**, the same day — so any count of it is a snapshot and
> should be dated, which is why both of these now are.

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

### 2.19 [EXHAUSTED, both slot-20 readings; 97.6% of its space compressed-key only] One gap slot over the whole dictionary, every gap in turn

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

**[EXHAUSTED, conditional on the template's other words] Ideas already covered by
completed runs.** Each is covered only with the run's other slots as they were:
the fixed words fixed, and the gaps on the 54-pool. "Pre-patch" means compressed
key only (§3).

| idea | slot | covered by (evidenced) | words at that slot | paths | slot-20 reading | key formats |
|---|---|---|---|---|---|---|
| `food` | 11 | `t21_free11_p1` | 54-pool + `pyramid` (55) | **path 1 only** | `second` only | compressed (pre-patch) |
| `absent`, `air`, `airport` | 6 | `t21_loo6`; `t21_loo6_apple` | all 2048 | 4 | `second`; `apple` | compressed; all three |
| `alarm`, `album` | 21 | `t21_loo21` | all 2048, so all 16 checksum-valid finals per prefix | 4 | both | compressed (pre-patch) |
| `black` | 10 | the template itself (`t21_readme54` and every run that keeps it) | `black` | 4 | both | all three, via the post-patch runs |
| `black` | 21 | `t21_black21` | `black` | 4 | both | compressed (pre-patch) |

The `food@11` row was first proposed as `t21_free11` on four paths. The evidenced
run is `t21_free11_p1`, path 1 only; the four-path config has never run, so
`food@11` is open on paths 2–4 and under `apple`. *[26 Oct: `food@11` is now
covered on all four paths under both readings and all three key formats by
`t21_food11` (20 Oct, admitted 26 Oct; below). The four-path `t21_free11`, the
whole 55-word slot, has still not run.]*

**[ASSUMED] Speculative date arithmetic: untested, no position evidence, not
queued.**
- `battle` / `beach` from 2020 − 1865 = 155, word #155 counted 1-based / 0-based.
- `dose` / `double` from `05.25` = 525, the same two ways.

Neither has any evidence placing it at a slot.

**[MEASURED] The queue of 19–20 Oct 2026, run while `el22` was paused.** Six runs,
each with its band committed before the queue started (`QUEUE_after_el22.md`).
Each run's survivors were taken automatically from its own log, and only after
`exit=2`. There are 0 HIT lines across all six logs, and 0 GPU thermal pauses over
the whole queue (peak 89 °C).

| run | candidates | survivors | band | z |
|---|---|---|---|---|
| `t21_rev54` | 49,589,822,592 | 387,420,823 | 387,420,489.0 ± 19,606 | +0.017 |
| `t21_pool58` | 76,137,385,088 | 594,824,477 | 594,823,321.0 ± 23,874 | +0.048 |
| `t21_food11` | 148,769,467,776 | 1,162,260,604 | 1,162,261,467.0 ± 33,399 | −0.026 |
| `el21_rev` (Electrum, §2.6) | 235,298,000,000 | 976,591,446 | 976,578,613.3 ± 31,185 | +0.411 |
| `t21_slot1_line` | 247,949,112,960 | 1,936,982,003 | 1,937,102,445.0 ± 43,118 | **−2.793** |
| `t21_alt3` | 396,718,580,736 | 3,099,279,830 | 3,099,363,912.0 ± 54,541 | −1.542 |

All six are negative and in band. `t21_slot1_line`'s −2.79 is the largest deviation in
the campaign (the previous largest was +1.802, `t21_loo6`):
- **It is not a coverage gap.** The log confirms the full space was processed, and
  one skipped chunk would cost about 29 million survivors, roughly 680σ; the
  shortfall is 120,442.
- **As chance it is unremarkable across the campaign.** Its two-sided p is about
  0.005, and across about 48 scored runs the chance of at least one this far out
  is about 22%.

`food@11`, `space@11`, the reversed template on the 54-pool, and the alternates
`person`, `real` and `rain` are now covered on four paths under both slot-20
readings. *[26 Oct: all five were admitted to `tally2.py`'s EVIDENCED list on the
owner's instruction, together with the three BIP39 runs of 24–26 Oct below; ledger
in §3. The note that stood here — "**Not yet admitted** … admitting the five BIP39
runs would move the headline from 278,996,119,787 to 283,874,091,848 evidenced
derivations (combined 286,738,325,903), and waits on the owner" — described a state
that ended that day. It is kept, dated, as the record of it, not as a live claim.]*

**[SCOPE — CLOSED 4 Nov 2026]** All 31 were admitted to `tally2.py`'s EVIDENCED
list on 4 Nov 2026, each on completion and in the band committed before launch; the
evidenced set went 51 → 82 runs and the headline 305,201,540,079 → 316,456,008,920
derivations (§3). The note that stood here is struck, not deleted, because it was
true when written and this report retracts by marking:

> ~~**[SCOPE] What is still unadmitted, as of 3 Nov 2026: 31 completed t21 runs.**
> Each exited 2 with its log in the tree; none is in `tally2.py`'s EVIDENCED list, so
> none is in the headline, and the headline is a floor by that much. By name —
> `t21_idx2`, `t21_pool60`, `t21_slot1`, `t21_food7` (26 Oct); `t21_pool57v` (30
> Oct); `t21_pool60c` (30 Oct); `t21_top20`, `t21_top6_loo8`, `t21_top6_loo14`,
> `t21_top6_loo15`, `t21_top6_loo18`, `t21_top6_loo21`, `t21_top_at_7`,
> `t21_top_at_9`, `t21_top_at_11`, `t21_top_at_17` (30 Oct); `t21_clk2`, `t21_clk3`,
> `t21_clk4`, `t21_clk5`, `t21_clk6`, `t21_clk7`, `t21_clk8`, `t21_clk9`,
> `t21_blackd2`, `t21_blackd3`, `t21_blackd4`, `t21_blackd5`, `t21_blackd7`,
> `t21_blackd9`, `t21_this3` (31 Oct). Admission waits on the owner, run by run,
> under the rule in §10: on completion and in band, never when the file appears.~~

**[SCOPE] What remains unadmitted, as of 4 Nov 2026: one run — Electrum `el21_rev`**
(§2.6, 20 Oct; survivors 976,591,446 against 976,578,613.3 ± 31,185, z +0.411). It is
outside `tally2.py` altogether, which models only the 21-word BIP39 template, so it
cannot be admitted by adding a row and the headline stays a floor by that much. This
note carries a date because a note that counts unadmitted runs is false the moment one
is admitted — the stale-summary failure catalogued under §2.12's heading, which had
by then happened three times. Closing this one in the same commit as the admission is
the rule being followed rather than restated.

**[MEASURED] The 31 runs, scored against the bands committed before launch.** Bands
are quoted from `QUEUE_after_el22.md` exactly as committed, not recomputed here;
survivors come from each run's own log after `exit=2`; there are 0 HIT lines in all
31. `t21_top6_loo21` has `SLOT 21 @FULL`, so it is an exact identity with no σ and no
z, and `t21_clk9` pins `tower` at slot 21, so slot 21 is not a pool and its σ is
binomial — both read off the config line, never inferred from the volume.

| run | candidates | survivors | band committed before launch | z | |
|---|---|---|---|---|---|
| `t21_idx2` (26 Oct) | 137,438,953,472 | 1,073,739,482 | 1,073,741,824.0 ± 31,839 | −0.074 | in band |
| `t21_pool60` (26 Oct) | 93,312,000,000 | 729,015,479 | 729,000,000.0 ± 26,428 | +0.586 | in band |
| `t21_slot1` (26 Oct) | 297,538,935,552 | 2,324,505,174 | 2,324,522,934.0 ± 47,234 | −0.376 | in band |
| `t21_food7` (26 Oct) | 49,589,822,592 | 387,432,088 | 387,420,489.0 ± 19,283 | +0.602 | in band |
| `t21_pool57v` (30 Oct) | 68,592,894,498 | 535,893,025 | 535,881,988.3 ± 22,660 | +0.487 | in band |
| `t21_top20` (30 Oct) | 24,794,911,296 | 193,728,375 | 193,710,244.5 ± 13,635 | +1.330 | in band |
| `t21_top6_loo8` (30 Oct) | 34,828,517,376 | 272,117,975 | 272,097,792.0 ± 16,160 | +1.249 | in band |
| `t21_top6_loo14` (30 Oct) | 34,828,517,376 | 272,096,716 | 272,097,792.0 ± 16,160 | −0.067 | in band |
| `t21_top6_loo15` (30 Oct) | 34,828,517,376 | 272,097,569 | 272,097,792.0 ± 16,160 | −0.014 | in band |
| `t21_top6_loo18` (30 Oct) | 34,828,517,376 | 272,109,740 | 272,097,792.0 ± 16,160 | +0.739 | in band |
| `t21_top6_loo21` (30 Oct) | 34,828,517,376 | 272,097,792 | must equal 272,097,792 exactly | — | **identity exact** |
| `t21_top_at_7` (30 Oct) | 49,589,822,592 | 387,413,240 | 387,420,489.0 ± 19,283 | −0.376 | in band |
| `t21_top_at_9` (30 Oct) | 49,589,822,592 | 387,435,144 | 387,420,489.0 ± 19,283 | +0.760 | in band |
| `t21_top_at_11` (30 Oct) | 49,589,822,592 | 387,423,207 | 387,420,489.0 ± 19,283 | +0.141 | in band |
| `t21_top_at_17` (30 Oct) | 49,589,822,592 | 387,446,324 | 387,420,489.0 ± 19,283 | +1.340 | in band |
| `t21_pool60c` (30 Oct) | 93,312,000,000 | 728,994,018 | 729,000,000.0 ± 26,442 | −0.226 | in band |
| `t21_clk2` (31 Oct) | 49,589,822,592 | 387,435,659 | 387,420,489.0 ± 19,283 | +0.787 | in band |
| `t21_clk3` (31 Oct) | 49,589,822,592 | 387,409,390 | 387,420,489.0 ± 19,283 | −0.576 | in band |
| `t21_clk4` (31 Oct) | 49,589,822,592 | 387,404,733 | 387,420,489.0 ± 19,283 | −0.817 | in band |
| `t21_clk5` (31 Oct) | 49,589,822,592 | 387,394,976 | 387,420,489.0 ± 19,283 | −1.323 | in band |
| `t21_clk6` (31 Oct) | 49,589,822,592 | 387,398,953 | 387,420,489.0 ± 19,283 | −1.117 | in band |
| `t21_clk7` (31 Oct) | 49,589,822,592 | 387,443,994 | 387,420,489.0 ± 19,283 | +1.219 | in band |
| `t21_clk8` (31 Oct) | 49,589,822,592 | 387,409,925 | 387,420,489.0 ± 19,283 | −0.548 | in band |
| `t21_clk9` (31 Oct) (binomial) | 49,589,822,592 | 387,439,044 | 387,420,489.0 ± 19,606 | +0.946 | in band |
| `t21_blackd2` (31 Oct) | 49,589,822,592 | 387,423,893 | 387,420,489.0 ± 19,283 | +0.177 | in band |
| `t21_blackd3` (31 Oct) | 49,589,822,592 | 387,432,290 | 387,420,489.0 ± 19,283 | +0.612 | in band |
| `t21_blackd4` (31 Oct) | 49,589,822,592 | 387,415,524 | 387,420,489.0 ± 19,283 | −0.257 | in band |
| `t21_blackd5` (31 Oct) | 49,589,822,592 | 387,403,170 | 387,420,489.0 ± 19,283 | −0.898 | in band |
| `t21_blackd7` (31 Oct) | 49,589,822,592 | 387,402,205 | 387,420,489.0 ± 19,283 | −0.948 | in band |
| `t21_blackd9` (31 Oct) | 49,589,822,592 | 387,409,169 | 387,420,489.0 ± 19,283 | −0.587 | in band |
| `t21_this3` (31 Oct) | 49,589,822,592 | 387,434,905 | 387,420,489.0 ± 19,283 | +0.748 | in band |

**All 31 in band, 0 out, no |z| > 3 and none even past 2.** The spread runs from
−1.323 to +1.340. Two independent cross-checks come with that: `tally2.py`'s
`vol(box)` equals the `space` column of every one of the 31 scores rows, so each run
covered the space the ledger credits it; and the overlap figures committed before
launch reproduce exactly. `QUEUE_after_el22.md` predicted, against the 50-run
EVIDENCED union of the time, that each `t21_top6_loo*` would add 33,910,187,328 — an
overlap of 918,330,048 — and that `t21_top20`, the four `t21_top_at_*` and all 15 of
the 31 Oct batch would add 100%. Measured now against the **51**-run union (the same
50 plus `t21_single`), the overlaps are 918,330,048 each and 0 each: the predictions
hold, and `t21_single` adds no overlap to any of them — a second independent check of its
zero-overlap result, after the unchanged `double-counted` figure recorded in §3. What the bands do **not** support is reading 31
in-band results as 31 confirmations; §3 measures that and says why.

**[MEASURED] The queues of 24–26 Oct 2026, run while `el22` was held.** Each band was
committed before launch (`QUEUE_after_el22.md`), and survivors were taken from each
run's own log after `exit=2`. There are 0 HIT lines in every log and 0 GPU thermal
pauses from 24 Oct 08:11 to the end.

| run | candidates | survivors | band | z |
|---|---|---|---|---|
| `t21_free20` (slot 20 over its 56 words, 4 paths) | 1,388,515,032,576 | 10,847,704,031 | 10,847,773,692.0 ± 102,037 | −0.683 |
| `t21_pool57` (`t21_readme54` + `black`, `air`, `silent` in the gap pool) | 68,592,894,498 | 535,897,636 | 535,881,988.3 ± 22,680 | +0.690 |
| `t21_silent4` (`t21_readme54` with slot 4 `silent`) | 49,589,822,592 | 387,414,920 | 387,420,489.0 ± 19,283 | −0.289 |

- **`t21_free20` is an identity, and it holds.** It reports 10,847,704,031 survivors,
  exactly `t21_free20_p1`'s. That is required: the word box is the same, and survivors
  do not depend on the path. Its z is therefore the same draw as `t21_free20_p1`'s,
  not a new one.
- **18 passphrase passes on `t21_readme54`, every one exact.** There were 8 BREATHE-type
  entries from `pw2.txt` (`breathe_pw.txt`: BREATHE, breathe, Breathe, I CANT BREATHE,
  I CAN'T BREATHE, ICANTBREATHE, icantbreathe, I CANT BREATHE 05.25.20). There were also
  10 entries in `black_pw.txt`: black, Black, BLACK, the three casings of "black lives
  matter", blacklivesmatter, BLM, blm, silent. The BIP39 checksum does not see the
  passphrase, and the solver resets its counter on every pass, so each pass must equal
  `t21_readme54`'s logged 387,425,296. All 18 do. They are recorded here and not in
  `tally2.py`, which does not model the passphrase.
- `silent` is a private lead, **[ASSUMED]**, with no position evidence.

## 3. Tally

**The tally is computed, not maintained.**

It had been kept as a running sum with per-change patches, and it drifted. Two
independent reconstructions on 23 September differed by 331 M, and tracing the
gap showed **both** were wrong: one used the solver's *reported* per-run
expected value instead of exact `space/128` (+194 M), the other omitted ~1.14 B
of runs. Neither was reproducible from its own inputs.

The deeper defect was double-counting. Every run on the same template shares
the all-pool core, so summing counts that core once per run — ~~**3.72%** of the
naive total across the t21 campaign. Of the twelve older t21 runs, **37% was
already covered** by newer sweeps.~~

> **[RETRACTED 4 Nov 2026] Both percentages in the sentence above are withdrawn as
> unreconstructable.** They were introduced in `d30d8d3` (27 Sep 2026) and never
> edited, and neither reproduces from the ledger state of that date. The check:
> `git show d30d8d3:tally2.py` has a 22-run `EVIDENCED` list, and running *that*
> script against the configs of *that* commit prints **3.31%**, not 3.72% —
> `double-counted 835,890,993,303 / naive sum 25,245,658,140,567`. Running the same
> script against today's configs prints 3.31%, and running today's `tally2.py` with
> `EVIDENCED` cut back to those 22 runs also prints 3.31%, so the gap is not config
> drift and not a change in the script. Eight other readings of "double-counted as a
> share" were tried against that state — with and without the `T24` tail, in
> candidates and in derivations, over the evidenced naive sum and over each union —
> and they span 2.355%–3.424%. **None is 3.72%.**
>
> **`tally.py`, the script that preceded it, was tested too, so the negative claim is
> complete.** That is the size-based `min()` model the sentence's own paragraph is
> about, and it was the obvious remaining candidate. `git show d30d8d3:tally.py` run
> as it stands prints, in full:
>
> ```
> t21 campaign, 17 runs, 131,072 i-e terms
>   naive sum         19,020,913,991,641 candidates
>   union             18,538,790,716,441
>   double-counted       482,123,275,200  (2.53%)
> disjoint templates     53,208,402,854 candidates
> TOTAL               18,591,999,119,295 candidates
>                        145,249,993,119 derivations
>                                  4,203 CPU-days at 400/s
> ```
>
> **2.53%, and no 37% anywhere in its output.** `(naive − union) / naive` on *its*
> union gives 2.535%; adding the disjoint templates to both sides gives 2.528%; over
> its union 2.601%; over its TOTAL 2.593%. Its own docstring independently states
> "for the 17 runs of the t21 campaign that is 482 billion candidates, **2.53%** of
> the naive total", so the script and its documentation agree with each other and
> disagree with the report. `tally.py` cannot be extended to 22 runs for comparison:
> its rows are hard-coded dimension *sizes*, not configs, which is the defect
> `tally2.py` was written to fix. Every ratio of its printed quantities was also
> checked; the only one near either target is `disjoint/derivations = 36.6%`, which
> divides candidates by derivations and is not a quantity.
>
> **`test_tally.py` was in the tree at `d30d8d3` too, and it prints no percentage at
> all** — 12 unit tests of the box algebra and the line `ALL PASS`, no figures — so
> the negative claim covers all three scripts that commit carried, not two.
>
> **The companion claim fails the same way.** The twelve asserted runs' own union is
> 580,237,381,114 candidates against a marginal of 462,067,188,033, so **20.37%** was
> already covered, not 37%. Read as a *sum* rather than a union it is **35.85%**,
> which is the closest any reading comes and still is not 37%; over the nine runs
> `tally.py`'s docstring names instead of twelve it is 34.97%.
>
> **One near-match, reported and dismissed on its base rate.** Searching all 8,166
> subset readings of the twelve finds 37.09% for `{t21_trust21, t21_bnw18}` and for
> supersets that add nothing to it. It is not the claim — the sentence says *the
> twelve* — and **90 of those 8,166 readings fall in the same 36.5–37.5% window,
> 1.10%**, which is what chance predicts for a one-point window. **Those 8,166 readings
> are not independent**: a superset that adds nothing repeats its subset's value, which
> is why 37.09% turns up at r=2, 3 and 4 and appears 10 times in all, so 1.10% is a
> rate per *reading*, not per *distinct value*. Collapsing to the 2,099 distinct values
> gives **83 in the window, 3.95%** — the dismissal survives, but by a *larger* margin
> rather than the same one, because the collapse is uneven (3.89× overall against
> 1.08× inside the window), so a 37%-ish value is commoner among distinct values than
> among readings. Stated because a base rate quoted in the wrong unit inside a note
> about figures that were never checked would be the same error one level up. By §9's own rule a
> numerical coincidence is not evidence unless the source identifies the operands,
> and nothing here identifies that pair. Recorded so the next reader does not have to
> rediscover it and mistake it for the origin.
>
> Both percentages entered in the same commit: `git log -S'37% was' -- REPORT.md`
> returns `d30d8d3` alone, so they were not written at different times under
> different models.
>
> No replacement is asserted, because the figure cannot be traced to a computation.
> For the quantity the sentence was describing, the two measured values are
> **3.31%** at the 22-run ledger of 27 Sep and, as the same quantity,
> **5.38%** at 84 evidenced runs.
>
> *[UNITS CORRECTED 9 Nov 2026. The series above was not comparable, and the mixing
> started at the 24 Oct admission of `t21_free20`. `tally2.py` now splits the
> double-count into the two quantities it had been adding together:*
>
> | | 84 evidenced + 12 asserted |
> |---|---|
> | **accidental overlap** — boxes that share candidates because they are variations on one template | **2,324,348,141,153** (**5.38%** of non-twin naive 43,199,107,704,973) |
> | **path-twin overlap** — declared duplicates, each 100% inside its own `_p1` counterpart | **4,115,955,275,136** (`t21_free11`, `t21_free2`, `t21_free20`) |
> | total, as printed before | **6,440,303,416,289** (13.61% of naive 47,315,062,980,109) |
>
> *Which quantity did the published figures measure? **3.31%** at 22 runs was pure
> accidental overlap — it predates every twin. **8.33%** at 82 runs was **mixed**:
> accidental plus `t21_free20`'s whole box. So the step from 3.31% to 8.33% was never
> a 2.5× rise in re-covered ground; most of it was one deliberate duplicate entering
> a figure that did not distinguish them. The accidental component has been
> **2,324,348,141,153 throughout** — it did not move when `t21_free2` was admitted and
> did not move when `t21_free11` was, which is the test that the split is the right
> one: the denominator drops the twin boxes too, so the ratio is invariant to any
> twin admission.*
>
> *The two kinds mean different things. Accidental overlap says how much of the
> campaign re-covered ground it had already covered — it is the number worth watching.
> Path-twin overlap is a cost knowingly paid: a twin buys the word "exhausted" over a
> path set and is expected to contribute its entire volume. Reporting their sum as one
> percentage made a deliberate purchase look like waste.]* Both are
> reproducible from `tally2.py`; the retracted pair is not. This is the §10 rule
> applied to the report's own prose: a number that cannot be recomputed does not
> stay on the page because it once looked right.

`tally2.py` replaces the sum. It parses the run configs directly — so a row
cannot drift from the config it claims to describe — and computes the union by
box disjointification with real set intersections. Run it as
`python3 tally2.py configs`.

```
t21 campaign, 84 evidenced runs     316,456,008,920 derivations
  (= 84 t21 boxes + 2 carried tails: 24-word at /256, 12-word at /16)
+ the twelve older asserted runs    319,320,153,389
    marginal of the twelve          2,864,144,469
    at 400 derivations/s            9,157 CPU-days evidenced, 9,240 combined
```

*[26 Oct: eight runs admitted.]* The runs are `t21_rev54`, `t21_pool58`, `t21_food11`,
`t21_slot1_line` and `t21_alt3` (19–20 Oct), and `t21_free20`, `t21_pool57` and
`t21_silent4` (24–26 Oct). Each was admitted on completion and in its band (end of
§2). The block read 42 runs, 278,996,119,787, 282,171,117,443, 3,174,997,656 and
8,165 CPU-days before this. Added as boxes, the eight contribute **676,443,377,378**
candidates. Their naive sum is 2,425,862,118,818, so the inter-box term is
**1,749,418,741,440**. That term is the overlap with the 42 and among the eight.
`t21_free20` alone contributes 0: it is `t21_free20_p1`'s word box, and the ledger
does not see paths.

In derivations, that admission moved the headline `278,996,119,787 → 284,280,833,673`,
a change of 5,284,713,886. (Both figures are the ledger as it stood on 26 Oct; the
block above now prints 316,456,008,920 after the admissions of 3 and 4 Nov.)
Each total is floored separately, so this is one more than 676,443,377,378 / 128 =
5,284,713,885.77 rounded down. Electrum `el21_rev` (§2.6) and the passphrase passes
are not in this block.

*[3 Nov: `t21_single` admitted, the 51st evidenced run.]* The single-numeral reading
of the clock overlap — the run whose own config records three objections to it.
`exit=2`, exhausted with no match, 0 HIT lines, survivors **20,920,507,774** against
the band committed before launch in `QUEUE_after_el22.md` (20,920,706,406.0 ±
141,701, stratified, slot 21 `@POOL`), **z = −1.402**. Added as a box it contributes
**2,677,850,419,968** candidates and the union rises by exactly that: the overlap
with the existing 50 boxes is **0**, which `tally2.py` computed — it was not asserted
in advance. **Slot 4 is what separates it.** `t21_single` moves `eye` to slot 4 and no
evidenced config admits `eye` there: 46 pin `mask`, two use pools that do not contain
it, one pins `silent`, one allows `mask|person`. Slot 6 separates 48 of the 50 as
well; `t21_loo6` and `t21_loo6_apple` free slot 6 so `pyramid` is reachable there, but
slot 4 still blocks both, and `t21_swap114`, `t21_rev54` and `t21_slot1_line` part at
slot 1 first. `double-counted` is unchanged at 3,272,477,091,681, which is the
independent check that nothing was added twice.

**The ledger credits this run 20,920,706,406 derivations, not the 20,920,507,774
survivors it actually counted.** The credited figure is `⌊candidates / 128⌋` — the
**modelled** count, exact here with remainder 0 — and the observed survivors fall
198,632 short of it, which is 198,632 / 141,701 = 1.402σ and is the same number as
the z-score above, reached from the other side. This is the convention this section
already states under *"What ‘derivations’ means here, exactly"*: the ledger reports
`⌊candidates / 128⌋`, **that is a convention, not a count**, and every run is
z-tested against `N/128` rather than required to equal it. The convention applies to
**all 84 evidenced rows**, not to this one specially; the residuals are signed and
centred on zero, so the error is self-cancelling in aggregate and no total above
needs adjusting. Recorded as a precision note, not a correction.

*[4 Nov: the 31 completed t21 runs of 26–31 Oct admitted, taking the evidenced set
from 51 to 82.]* Six queues feed it — `queue_oct26` (4 runs), `queue_oct30` (1),
`queue_oct30b` (10), `queue_oct30c` (1), `queue_oct31` (15). Every one reached
`exit=2` with its log in the tree and 0 HIT lines, and every one landed inside the
band committed **before** launch in `QUEUE_after_el22.md`; the scored table is at the
end of §2. What they do to this ledger:

```
                              candidates            derivations
union before, 51 evidenced    39,067,606,420,307    305,201,540,079
union after,  82 evidenced    40,508,149,071,797    316,456,008,920
contributed                    1,440,538,457,186     11,254,206,697
  (the "after" row also carries the 12-word tail admitted 9 Nov:
   +4,194,304 candidates, +262,144 derivations -- see 2.2)
disjoint boxes                       164 -> 295
CPU-days at 400/s                  8,831 -> 9,157
```

*[9 Nov 2026: the evidenced count is now **84**, not the 82 this block records, after
`t21_free2` and `t21_free11` were admitted. Every figure in the block above is unchanged by that
admission — union, derivations, disjoint boxes and CPU-days all hold, because
both are four-path twins of boxes already in the list and contribute **0** new
candidates. Only the run count and the naive/double-counted pair moved — and of the
double-count, only the path-twin component. The block is
kept as the record of the 4 Nov admission, which is what it describes.]*

Added as boxes the 31 have a union of **1,727,057,432,162** candidates of their own,
against a naive sum of **1,880,928,733,538** — so **153,871,301,376** of that is
overlap among themselves, a further **286,518,974,976** overlaps the existing 51, and
what is left is the 1,440,538,457,186 credited above. The identity closes exactly:
`1,727,057,432,162 − 286,518,974,976 = 1,440,538,457,186`.

**Twenty of the 31 overlap the evidenced 51 by exactly 0** — `t21_top20`, the four
`t21_top_at_*`, the eight `t21_clk*`, the six `t21_blackd*` and `t21_this3`, each
pinning a different word at a different slot. The overlap sits in the other eleven:
`t21_idx2` 104,689,625,472 of its own 137,438,953,472; `t21_pool60` and
`t21_pool60c` 82,649,704,320 each; `t21_slot1` 74,384,733,888; `t21_pool57v`
66,119,763,456; `t21_food7` 24,794,911,296; and each of the five `t21_top6_loo*`
918,330,048. **Those eleven figures must not be added.** Each is measured against the
51 *alone*, so wherever two of the eleven overlap the same part of the 51 — and they
do, being variations on one template — that part is counted once per run. Their sum
is 439,880,092,992, which overstates the 286,518,974,976 the union actually removes
by 153,361,118,016. The union is not the sum even of correctly measured overlaps — this
is the error of §3's opening paragraph reappearing one level down, in the per-run
presentation rather than in the totals.

**The marginal of the twelve asserted runs did not move again**: 2,864,144,469 before
and after, because none of the 31 lands inside an asserted box either. Both printed
totals rose by the same 11,254,206,697. That is twice in two days that the marginal
held while the headline moved — the reason it is derived from the two printed totals
at the moment of printing, rather than carried forward and patched.

*[Corrected 13 October.]* The marginal line read 3,608,896,368 from 28 September,
when the ledger held 29 runs, until 13 October. The two totals above it were
updated at every admission and it was not, so for two weeks the block broke the
rule stated later in this section: the marginal must equal the difference of the
two printed totals. It is now `319,320,153,389 − 316,456,008,920 = 2,864,144,469`,
which is also what `tally2.py` prints. *(It read `282,171,117,443 −
278,996,119,787 = 3,174,997,656` until the admissions of 26 Oct,
`287,144,978,142 − 284,280,833,673 = 2,864,144,469` from then until the admission of
3 Nov, and `308,065,684,548 − 305,201,540,079 = 2,864,144,469` from then until the 31
admitted on 4 Nov.)* It shrinks as newer evidenced runs re-cover the twelve asserted
ones —
**but it did not shrink on 3 Nov, and that is the point of recomputing it rather
than swapping the headline under it.** `t21_single` added 2,677,850,419,968
candidates and re-covered none of the twelve asserted boxes, so both printed totals
rose by the same amount and the marginal is unchanged to the derivation:
2,864,144,469 before and after. The gap narrows only when a new evidenced run lands
*inside* the asserted boxes. This one does not touch them — the same slot-4
disjointness that gave it zero overlap with the evidenced 50 also keeps it clear of
the asserted twelve.

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

**[MEASURED 4 Nov 2026] `0.983533` is the 54-word pool's factor, not the model's.**
The ratio depends on *where* the pool's words fall among the 16 blocks, so every
pool has its own, and the paragraphs above do not say so. That omission is a live
trap: scoring a 64-word pool with the 54-word factor is a silent 0.8% error in σ.
The five pools this campaign has actually swept at slot 21, recomputed from the
configs:

| pool | k_j by block | Σk_j² | per-prefix variance | σ_strat/σ_binom | runs |
|---|---|---|---|---|---|
| 54 | `4 1 1 3 1 4 3 1 5 6 10 1 1 3 6 4` | 278 | 0.404907 | **0.983533** | most of the campaign |
| 57 | `4 1 1 3 1 4 4 1 6 6 10 1 1 3 6 5` | 305 | 0.426697 | **0.982721** | `t21_pool57v` |
| 60 | `4 2 1 3 2 4 5 1 5 6 10 1 1 3 7 5` | 322 | 0.449097 | **0.982658** | `t21_pool60` |
| 60 | `4 1 3 3 2 4 5 1 5 6 10 1 1 3 6 5` | 314 | 0.449585 | **0.983192** | `t21_pool60c` |
| 64 | `14 1 1 3 1 4 3 1 5 6 10 1 1 3 6 4` | 458 | 0.472046 | **0.975462** | `t21_idx2` |

σ is then `sqrt(prefixes × V_p)` with `prefixes = candidates / |pool|`. Every figure
in the table is exactly what `QUEUE_after_el22.md` committed before the run launched;
recomputed from the configs on 4 Nov they reproduce to the digit.

**Two things in that table are worth reading twice.** The two 60-word pools have
**different factors** — 0.982658 and 0.983192 — because `t21_pool60` and
`t21_pool60c` add different words: *size does not determine the band*, which is §10
rule 4 one level down from where it is usually applied. And `t21_idx2` is the
outlier at 0.975462 because its ten extra words are **consecutive** — `abandon`
through `accident`, indices 0–9 — so block 0 alone holds 14 of the 64 and `Σk_j²`
jumps to 458. The more unevenly a pool is spread across the blocks, the further the
stratified σ falls below the binomial one.

> **[Recorded as an error of mine, not of the bands.]** Scoring the 31 runs on
> 4 Nov I first applied 0.983533 to all of them and reported σ of 32,102, 26,451,
> 26,451 and 22,679 for `t21_idx2`, `t21_pool60`, `t21_pool60c` and `t21_pool57v`,
> against the committed 31,839, 26,428, 26,442 and 22,660. **The committed figures
> are the correct ones** — the formula above reproduces all four exactly. The cause
> was **the wrong constant**: one pool's factor used for four other pools. Not a
> different residue distribution, not a different formula, and not an arithmetic
> slip. The published z were computed from the committed σ throughout, so no run was
> rescored and no figure on this page moved. It is recorded because the mistake is
> precisely the one the table above now exists to prevent, and because the §10 rule
> that a committed band is never altered after the fact is what made the gap visible
> rather than absorbing it.

**[MEASURED] The block model is confirmed directly, and the plausible alternative
is excluded.** The 16 Bernoullis are independent for a reason worth stating: the
4-bit nibble of word 21 is itself part of the 224-bit entropy that gets hashed, so
each nibble `j` produces its *own* checksum `c_j`, and the sixteen valid words are
`{j·128 + c_j}` — sixteen independent draws. Had one checksum served the whole
prefix, the valid set would be a single residue class `{c, c+128, …, c+15·128}`, the
per-prefix count would be `m_c` rather than a sum, and the variance would be
`Σ_c m_c²/128 − (k/128)²` = **0.384521** for the 54-pool — 2.6% narrower in σ than
the committed convention, in the direction that would make every z *larger*. The
two are distinguished by measurement, over 2,000,000 random 20-word prefixes with
the checksum taken from SHA-256 and pool membership looked up:

```
observed per-prefix variance   0.405172      (standard error 0.000405)
  block model      0.404907     0.7 SE   <- the committed convention
  one-residue      0.384521    51.0 SE
  plain binomial   0.418579    33.1 SE

observed per-prefix mean       0.421513      (54/128 = 0.421875)
```

The convention is confirmed at 0.7 standard errors and both alternatives are
excluded. The survivor count per prefix is 0 for 65.0% of prefixes, 1 for 28.6%,
2 for 5.7%, and reached 7 once in two million.

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
`zscore_table.py` scores every evidenced run from its config and log (42 when this
statement and the simulation below were computed; 50 since 26 Oct, see the note
after the block). Each
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

*[26 Oct, after the eight admissions.]* `zscore_table.py` now scores 50 runs: 49
with a z and 1 exact identity. **48 of the 49 are distinct draws.** `t21_free20`
repeats `t21_free20_p1`'s box and count, so its z is the same draw and is counted
once. Over the 48:

```
mean z -0.1312    sample Var 0.8053    sd 0.8974    max |z| 2.793 (t21_slot1_line)
95% CI on Var, if independent      [0.558, 1.263]   -- contains 1.0
|z| < 1   35   (expect 32.8)
1 - 2     12   (expect 13.0)
>= 2       1   (expect  2.2)
```

The mild underdispersion read below is weaker on 48 runs than on 41. The correlated
simulation and `rho_bar.py` figures below are for the 41 and have not been re-run.
`zscore_table.py` was changed for this: it now takes the run name from the
`queue*_<run>.log` filenames, and it prefers a run's own log over its `_p1` base
name. The 42 rows it printed before are unchanged.

**The honest reading: mild underdispersion that does not survive having looked
three ways.** Three statistics, side by side, because which one is quoted changes
the impression. The first is the like-for-like replacement for the retracted
`0.0058`. All three were computed **from one correlated simulation** —
`dispersion_mc.py`, 10⁵ draws from the 41×41 correlation matrix built from box
intersections — so they sit on the same footing rather than mixing an
independence assumption with a rescaled χ²:

```
                                 correlated sim     (independent, for reference)
P(all 41 inside 1.802)           0.052 +/- 0.001    0.048
P(sample Var <= 0.695)           0.089 +/- 0.001    0.072
P(none of 41 beyond 2 sigma)     0.155 +/- 0.001    0.148
P(at least one of the three)     0.191 +/- 0.001    <- familywise
```

The simulation checks itself: its mean sample variance is 0.9780, against the
analytic `1 − ρ̄ = 0.9777`.

**Three statistics were examined, so the smallest p is not the headline.** Looked
at three ways, the chance that at least one is this extreme under the stated σ
models is about **0.19**. That is not significant. The 0.052 is what one of three
looks produced, and quoting it alone would be selecting the most striking of
several tests after seeing them. An earlier draft of this paragraph
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
explain the 0.695 — but once three looks are accounted for, there is little left
that needs explaining.

**[MEASURED] Effective number of independent runs.** The same ρ̄ sizes a claim
made later in this section ("What survives of the original point") without
measuring it. For the mean of 41 standardised scores, `Var(z̄) = (1 + 40ρ̄)/41`
exactly — the off-diagonal sum is `41 × 40 × ρ̄` whatever the individual pairs —
so the runs are worth

```
n_eff = 41 / (1 + 40 x 0.0223) = 21.7      independent runs, for a mean
```

41 in-band results are about 22 independent confirmations of the template, not
41. For the **variance** the same overlap costs far less: `E[s²] = 1 − ρ̄ =
0.978`, which is why it accounts for only `(1 − 0.978)/(1 − 0.695) = 7.3%` of the
shortfall. Overlap matters for how much the run count proves, and hardly at all
for how tight the runs look.

**This thread is closed.** The result is not significant, and dispersion could
not have mattered to the search either way.

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

**[MEASURED] The solver compares against the right bytes, and the control that
proves it goes through the production path.** Every negative in this document
rests on the kernel comparing each candidate's `hash160` against
`ccbd031e54cde2a3189fd59bc49f731367a1779e`. An independent researcher disclosed
in public issue #1 that their own first exhaustive pass returned zero hits and
was **void**: the target had each 4-byte word byte-swapped, and no gate caught it,
because their self-test planted its target in a separate buffer and their
negative controls pass under any target. That failure mode was checked here
before anything else, in three steps, bytes before interpretation.

*The target.* The solver holds no target file. It base58-decodes `TARGET` from
the config at runtime and packs it big-endian into five words. Line 296 of
`solver_host2.cuh` prints **the uploaded words themselves**, `tg[0..4]` with
`%08x`, not a re-rendering of the config. All 70 production log headers print
`ccbd031e54cde2a3189fd59bc49f731367a1779e`, which matches an independent Python
decode of the address byte for byte; the version byte is `0x00` and the base58
checksum is valid. The byte-swapped form would be
`1e03bdcca3e2cd549bd59f1813739fc49e77a167` and appears nowhere.

*The path.* There is **exactly one write to `d_target`** in the codebase — line
295, inside `upload_cfg`. Every route sets `cf.target` from an address and calls
that same function: production sweeps, `--selftest`, `--selftest-brain`, and the
`selftest_*.conf` controls. There is no separate test buffer to bypass it.

*The control, run rather than argued.* A checksum-valid 21-word phrase was built
in the campaign's **own shape** — the real template, all four paths, slot 20
`second` — with slots 18 and 21 left free, targeted at its address on path index
2 (`m/0/0`) so the multi-path loop is exercised too. No test flags:

```
production (Jacobian)   HIT index 2565   time@18 order@21   path m/0/0
affine, EC_USE_JACOBIAN=0  HIT index 2565   same phrase       path m/0/0
target, same phrase space, WORD-SWAPPED
                        exhausted, no match   survivors 24 of 2916   exit 2
```

**The third line is the important one.** A byte-swapped target produces a
completely ordinary negative: clean exit, survivor count normal (24 against an
expected 22.8), nothing flagged. That is the failure mode reproduced inside this
harness — and it is silent here too. The campaign's target is not in that state,
and a control exists that would have caught it if it were.

Credit where it is due: this check exists because hiddengogeta disclosed a
failure of their own that nobody had asked about.

**[MEASURED] All three key encodings, controlled — and which runs used them.**
That control hit on the compressed key only, and by §10's own rule a control
certifies only the path it shares. So the same planted phrase was run once per
encoding through the production path, verified by `HIT index` against an
independently predicted index of 2,565, with the phrase line never printed:

```
binary   format         index  path   pubkey        verdict
jac      compressed     2565   m/0/0  compressed    PASS
jac      uncompressed   2565   m/0/0  uncompressed  PASS
jac      hybrid         2565   m/0/0  hybrid        PASS
affine   compressed     2565   m/0/0  compressed    PASS
affine   uncompressed   2565   m/0/0  uncompressed  PASS
affine   hybrid         2565   m/0/0  hybrid        PASS
```

The current kernel hashes all three for every derived key. **But 29 of the 42
evidenced runs predate it.** *[Still 29 as of 4 Nov 2026 — the pre-patch set is
closed and cannot grow; the post-patch set has gone 13 → 21 → 22 → 53, so the
ledger now stands at 29 pre-patch of 82.]* The three-encoding binary was built
2026-09-28 07:51; every run whose log closed before then checked the **compressed
key only**:

| key checked | runs |
|---|---|
| compressed only (29) | `readme54`, `swap114`, `written`, `pool75`, the six `loo`, the thirteen `free*_p1`, the six `black` |
| all three (13) | `free3`, `free13`, `tarot_j10x20`, `tarot_j17x19`, `ink10x20`, `needle11`, `amend1415`, `flag6_apple`, the five `*_apple` mirrors |

This section has argued since 28 September that compressed-only is the right
model for a BIP39 seed — BIP32 wallets emit compressed leaf keys at every path —
and that argument stands. But it is an argument, and every negative from the 29
depends on it, so the affected headings carry a **number** rather than a blanket
caveat. Some of the 29's space has since been re-covered by the 13 — `readme54`,
for one, sits entirely inside `needle11` — so the caveat applies only to what the
13 did not reach. In candidates, compressed-only = `|U(S) \ U₁₃| = |U(S ∪ U₁₃)| −
|U₁₃|`:

| scope | its union | checked compressed-key only | share |
|---|---|---|---|
| all 29 pre-patch runs | 24,480,490,264,651 | 24,357,314,995,435 | 99.50% |
| §2.13, the 13 `free*_p1` | 17,455,617,552,384 | 17,381,232,818,496 | 99.57% |
| §2.14, `swap114` + `free2_p1` | 1,413,309,943,872 | 1,388,515,032,576 | 98.25% |
| §2.19, the six `loo` (`second` at slots 6–18, both readings at 21) | 6,458,615,227,584 | 6,408,447,197,184 | 99.22% |

*[26 Oct: the same computation over 50 runs.]* The eight runs admitted on 26 Oct
all used the three-encoding kernel, so the post-patch set is now 21 runs. Same
formula, `|U(S ∪ U₂₁)| − |U₂₁|`:

| scope | its union | checked compressed-key only | share |
|---|---|---|---|
| all 29 pre-patch runs | 24,480,490,264,651 | 22,871,916,142,795 | 93.43% |
| §2.13, the 13 `free*_p1` | 17,455,617,552,384 | 15,918,333,052,032 | 91.19% |
| §2.14, `swap114` + `free2_p1` | 1,413,309,943,872 | 1,388,515,032,576 | 98.25% |
| §2.19, the six `loo` | 6,458,615,227,584 | 6,385,948,111,008 | 98.87% |

Over the 50-run union as it stood on 26 Oct, 22,871,916,142,795 of
36,386,137,420,077 candidates (**62.86%**) were compressed-key only. This
cross-checks exactly against `|U₅₀| − |U₂₁|`. Most of the drop from 68.21% is
`t21_free20`, which re-covers `t21_free20_p1`'s box with all three encodings.

*[Recomputed 4 Nov 2026 over 82 runs. Both of the figures above are superseded:
68.21% was the 42-run state and 62.86% the 50-run state, and each is kept as the
record of its own ledger.]* `t21_single` and all 31 runs admitted on 4 Nov used the
three-encoding kernel: `solver2_jac` was built 2026-09-28 09:33, after the
three-encoding binary of 07:51, and all five queue scripts of the 31
(`run_queue_oct26.sh`, `run_queue_oct30.sh`, `run_queue_oct30b.sh`,
`run_queue_oct30c.sh`, `run_queue_oct31.sh`) invoke it. The post-patch set is
therefore **53 runs**, and the same formula `|U(S ∪ U₅₃)| − |U₅₃|` gives:

| scope | its union | checked compressed-key only | share | was (U₂₁) |
|---|---|---|---|---|
| all 29 pre-patch runs | 24,480,490,264,651 | 22,692,382,618,411 | **92.70%** | 93.43% |
| §2.13, the 13 `free*_p1` | 17,455,617,552,384 | 15,819,153,406,848 | **90.62%** | 91.19% |
| §2.14, `swap114` + `free2_p1` | 1,413,309,943,872 | 1,388,515,032,576 | **98.25%** | 98.25% |
| §2.19, the six `loo` | 6,458,615,227,584 | 6,305,594,231,808 | **97.63%** | 98.87% |
| **the whole 82-run union** | 40,504,526,297,231 | 22,692,382,618,411 | **56.02%** | 62.86% |

**Both ends moved, which is why this could not be read off `tally2.py`.** Since
the 50-run state the denominator has risen by **4,118,388,877,154** —
`t21_single`'s 2,677,850,419,968 plus the 1,440,538,457,186 the 31 contribute — and
the numerator has *fallen* by **179,533,524,384**, all of it on the 31, because 11
of them re-cover pre-patch space with all three encodings. The naive shortcut that worked for `t21_single` — numerator
unchanged, denominator up — does not apply here: `t21_single` overlapped nothing,
and these eleven overlap a great deal.

**Which runs re-covered pre-patch space**, measured per run against `U₂₉`:
`t21_idx2` 81,731,374,272; `t21_slot1` 74,384,733,888; `t21_pool60` and
`t21_pool60c` 68,874,753,600 each; `t21_pool57v` 59,232,288,096; `t21_food7`
24,794,911,296; and each of the five `t21_top6_loo*` 459,165,024. The other 20 of
the 31 touch no pre-patch space at all. Their per-run figures sum to
380,188,639,872 but their **union** against `U₂₉` is **229,123,346,976** — these are
overlapping boxes and the sum is not the answer, the same caution as in §3.

Of that 229,123,346,976, exactly **49,589,822,592 was already three-encoding
covered** and only the remaining 179,533,524,384 is new. That already-covered
figure is exactly `t21_readme54`'s own box, and the measurement confirms why:
`t21_readme54` lies entirely inside `U₂₂` (its overlap equals its full volume),
because it sits inside `t21_needle11`. So the four gap-pool expansions re-cover
`readme54`'s core for a second time and gain nothing there; what they do gain is
the pool words `readme54` never had, reached through the `loo` runs' freed slots.

**§2.19 moved the most in relative terms, 98.87% → 97.63%, and its heading changed
shape.** It read *"compressed-key only except apple at slots 6/8/14/15/18"*, a
conditional that was complete when the only three-encoding cover of that space was
the five `*_apple` mirrors. It no longer is: `t21_top6_loo8/14/15/18/21` each
re-cover 459,165,024 of it through `t21_loo6` — slot 6 is `@FULL` there, so `top`
is reachable at slot 6 — and the four gap-pool expansions re-cover between 59 and 82
billion of it each (`t21_pool57v` 59,232,288,096, `t21_pool60` and `t21_pool60c`
68,874,753,600, `t21_idx2` 81,731,374,272) through `t21_loo21` and the five other
`loo` runs, whose freed slots admit their new pool words. Rather than extend the conditional into a list nobody can
check, the heading now carries the number, as §2.13 and §2.14 already do and as
this section's own argument prefers. **§2.14 did not move**: 98.25% before and
after, because nothing among the 31 touches `swap114` or `free2_p1`.

**These figures exclude the 24-word tails**, as the two tables above it do — the
denominators are 21-word box unions only, which is why 40,504,526,297,231 here is
`T24` = 3,618,580,262 smaller than the 40,508,149,071,797 §3 quotes. The two
templates have different checksum widths and are not mixed in one union.

**56.02% of the whole 82-run union has been checked with the compressed key only.**
The figure cross-checks exactly against `|U₈₂| − |U₅₃|`. Closing the caveat would
cost about **23 GPU-days** (22.8 at 11.5M cand/s, 23.9 at 11.0M), for a key format
BIP32 wallets do not produce, and is not planned. *[This paragraph read "68.21% of
the whole 42-run union" and "about 25 GPU-days" from 28 Sep to 4 Nov. Both were
correct for the 42-run ledger; neither was re-derived when the ledger grew to 50,
then 51, then 82. The share has fallen every time and the cost has barely moved,
because the numerator shrinks only when new runs land on old space.]*

The first pass at this table grouped `swap114` with `written` for §2.14, from the
run list rather than the section text. §2.14's second row is in fact *"freeing
slot 2 to 55 candidates including `twin`"* — `t21_free2_p1`. The wrong grouping
gave 115,253,293,465, about twelve times too small: the object was inferred
instead of read.

**A miscount cannot have swallowed a hit.** The survivor counter is a progress
statistic: it records how many candidates passed the checksum filter. A HIT is a
`hash160` comparison inside the kernel, and it never passes through that counter.
So every defect discussed above — the resume reset, the unscored runs, the
retracted dispersion figure — is a bookkeeping fault and not a search fault. What
a counting error *can* hide is a coverage gap, which is why the chunk-alignment
checks matter and the arithmetic does not.

**[SUPERSEDED] What survives of the original point — now measured; see
"Effective number of independent runs" under the dispersion statement above.**
This paragraph read: *"The boxes do overlap by design, so whatever the completed
table shows, the counts are positively correlated and the effective number of
independent draws is far below 37. That part did not depend on the retracted
arithmetic."* The direction was right; the size was asserted. Measured from the
box intersections by `rho_bar.py`: mean pairwise ρ̄ = 0.0223, effective number of
independent runs for a mean `41 / (1 + 40ρ̄) = 21.7`, and overlap accounts for
7.3% of the variance shortfall — not for the shortfall. The two paragraphs below
make the same unmeasured claim at 35 and 37 runs. They are kept as written and
marked where the measurement contradicts them.

*[SUPERSEDED — measured: overlap accounts for 7.3% of the shortfall, see the
dispersion statement above.]* The explanation is almost certainly not that the
pipeline is unusually accurate. It is that **the boxes overlap by design** — this section's whole purpose is
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
tidiness as significance. *[Measured since: 41 scored runs are worth about 21.7
independent ones for a mean.]*

*[Extended 4 Nov 2026, measured on the 31 runs admitted that day.]* Those 31 are the
cleanest test of this available, because every band was fixed before launch and 30 of
them carry a z (`t21_top6_loo21` is an exact identity and has none). Over the 30:
**mean z +0.117** (0.64 σ from zero), **sd 0.777** against the model's 1.0, min
−1.323, max +1.340. The dispersion is `χ² = 29 × 0.777² = 17.52` on 29 df, the
**4.65th percentile**, and **0** runs fall beyond |z| > 2 where **1.4** were
expected. Those are the measurements, and they stand.

> **[RETRACTED 4 Nov 2026, the same day it was published.]** What stood here read
> the sd of 0.777 as an estimate of the *true* σ scale, and concluded: ~~"the
> modelled σ is therefore about **29% larger** than the spread actually seen …
> a band drawn at ±3 σ(model) is ±`3/0.777` = **±3.86 σ(true)**, whose two-sided
> tail is **p = 0.00011** instead of the nominal 0.0027. **The band is permissive**
> — it is a 1-in-9,000 test being reported as a 1-in-370 one."~~ It also ranked the
> band **the weakest** of the four grounds for admitting those runs, on that basis,
> and offered the looseness as one of three stacked reasons the in-band results were
> not independent confirmations. **All of that is withdrawn.**
>
> It is wrong because the σ model is not inferred, it is **measured**, and the
> measurement is in this report on the same date: the per-prefix variance `V_p` is
> confirmed to **0.7 standard errors** over 2,000,000 prefixes in §2 (0.405172
> observed against 0.404907 modelled, SE 0.000405). That measurement pins σ to
> about **0.05%** in scale. For `sd(z) = 0.777` to be the true scale, `V_p` would
> have to be `0.777² × 0.404907` = **0.2444**; the measurement puts it **397
> standard errors** from there. A sample sd from 30 runs cannot outweigh a direct
> measurement of the quantity it was being used to estimate, and I should not have
> treated it as a rival estimate of σ at all.
>
> **This came from the owner's instruction and I followed it without checking it
> against the measurement one commit earlier.** That is the failure worth recording:
> not that an instruction was wrong, but that §10's first rule — recompute it, never
> adopt a figure because another party stated it — applies to instructions as much as
> to figures from other agents, and the contradicting measurement was already in the
> tree when I wrote the claim.

**[MEASURED] The band is correctly calibrated, so "in band" means what it says.**
`V_p` verified to 0.7 SE over 2,000,000 prefixes (§2), so a ±3 σ band *is* a ±3 σ
band and its two-sided tail is the nominal 0.0027. The `sd 0.777` is then what it
looks like when the model is right: a 30-sample fluctuation. `χ² = 17.52` on 29 df
sits at the **4.65th percentile** — low, and inside the range. It is one statistic
looked at once, a 1-in-22 draw, and the central 90% interval for 29 df runs from
17.71 to 42.56, so 17.52 falls just outside it on the low side.

**And it is not correlation between the runs.** That was worth checking, because
positive correlation does push the sample variance down — `E[s²] = 1 − ρ̄` — and it
is the explanation this section reaches for elsewhere. It does not work here.
Measured over the 435 pairs by the method of `rho_bar.py`
(`Cov(N_A,N_B) = Var(N_{A∩B})`):

```
pairs                                   435
pairs with any box overlap               16
mean pairwise rho                  0.007822
E[s^2] = 1 - rho_bar                0.99218      E[sd] about 0.9961
observed s^2                        0.60411
share of the shortfall in s^2 that
  correlation can account for           2.0%
```

The structural reason is cleaner than the number: **419 of the 435 pairs have
disjoint 20-word prefix sets**, differing at some slot among 1–20 and not merely at
slot 21, and **no pair is disjoint only at slot 21**. Disjoint prefixes draw their
own entropy, hence their own checksums, so the survivor counts are independent
draws. The 16 overlapping pairs are exactly the six among the four gap-pool
expansions (`t21_idx2`, `t21_pool60`, `t21_pool60c`, `t21_pool57v`, where ρ reaches
0.62) and the ten among the five `t21_top6_loo*`; every other pair is ρ = 0. There
is no correlation here to find, and no cause to look for — the low χ² is a
fluctuation, and the honest thing to say about it is that it is low.

**What survives, and it is the part that was never about σ.** "31 of 31 in band" is
still **not 31 independent confirmations of the template**. Two reasons, both intact:
the boxes overlap by construction across the whole campaign, as the paragraphs above
measure; and **20 of the 31 are not separate settings at all** — they occupy the same
49,589,822,592-candidate space with the same µ = 387,420,489.0, being permutations
and transpositions of one slot map over one pool, and 19 of those 20 share
σ = 19,283 as well (`t21_clk9` differs only in σ, because pinning `tower` at slot 21
makes its model binomial). One space, one band, 20 readings. That is a point about
what a negative tells you, not about whether σ is right.

**What the admission of those 31 rests on: four grounds, each checking something
different.** No ranking is offered, because the retracted inference was what
supplied one.

1. **`exit=2` with the run's own log in the tree.** This is what makes a run a
   negative at all; without it there is nothing to admit.
2. **The volume cross-check.** `tally2.py`'s `vol(box)`, computed from the config,
   equals the `space` column of that run's `queue_*_scores.tsv` row for all 31 — so
   the run covered the space the ledger credits it, independently of any statistics.
3. **The coverage margin.** One skipped chunk is 3,758,096,384 candidates, which is
   29,360,128 survivors: between **622 σ and 2,153 σ** across the nine committed σ,
   and **1,136×** the largest deviation any of the 31 actually showed (25,835
   survivors, `t21_top_at_17`). A dropped chunk cannot hide inside this scatter.
4. **The band**, which the Monte Carlo above confirms is correctly calibrated, and
   which is the check that caught the `_ModInv` limb-count bug and the 24-word HMAC
   omission. What it does *not* do is multiply: thirty valid checks of thirty runs
   are not one strong check of the template.

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
less trustworthy than either part. Where one number is needed, **"over 316
billion derivations eliminated"** is a floor that is computed, in preference to
an estimate that is not.

**The headline quotes the evidenced figure, not the combined one.** 316,456,008,920
is the union of the 82 runs whose logs are in this tree; 319,320,153,389 adds the
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

**The `between` column is measured; the `sum` column is not.** Adding the two
numerals is licensed only by block B's caption, which has no measured location — see
the scope note below and §7's provenance note. This table states both steps in one
voice and the two have different warrants.

> **[MEASURED, 31 Oct 2026] The "within ~1.5°" above is true of two hands, not of
> three.** Re-measured from the pixels, as the weighted centre of each hand's dark
> radial run out of the hub, against a numeral grid whose 18.75° offset is fixed by
> the same measurement (`clock_overlap_measurement.md`):
>
> | hand | direction | between | fraction of the interval | off the midpoint | sum |
> |---|---|---|---|---|---|
> | minute | 332.38° | 1 and 2 | 0.45 | **1.37°** | 3 (`tower`) |
> | second | 302.62° | 12 and 1 | 0.46 | **1.13°** | 13 (`moon`) |
> | hour | 238.49° | 10 and 11 | 0.32 | **5.26°** | 21 *(blank)* |
>
> **Slot 21 stands, and it is the loosest of the three clock slots.** The hour hand
> lies unambiguously between numerals 10 and 11 — a fraction of 0.32 is well inside
> the interval and no other pair is reachable — so the sum 21 is not in doubt. But
> it sits **5.26° off the midpoint, about four times the error of the other two**.
> The minute and second hands sit essentially *on* their midpoints, which is what a
> "sum of two numbers" mechanism requires; the hour hand does not, and the sentence
> above did not distinguish them. Slot 21 already carries no word (§5); this says the
> hand that names it is placed less precisely than the two that carry words.
>
> *An earlier draft of this note reported the hour hand as absent. That was a
> threshold fault — ink < 205 over radius 40–150 misses it — not a finding. At
> ink < 215 over radius 30–120 it is a continuous dark run from 5 to 117 px out of
> the hub, 3.5° wide.*

The runes beneath decode to `Сумма двух чисел` — "sum of two numbers" — stating
the mechanic outright.

> **[SCOPE, 9 Nov 2026] The sum-of-two-numbers mechanism rests on block B, and block
> B is unlocated.** That caption is the only thing in the artwork that states the
> mechanism; without it the three hands are three directions and nothing tells a
> reader to add the numerals they fall between. Its 14 glyphs have **no measured
> location** — a defined search around the dial returned zero glyph-sized components —
> and its transcription is `u/Amadeus407`'s of 2021-03-06, adopted here and never
> re-derived from pixels. **The mechanism is not retracted**: the caption may well be
> there, §7.5 places it among the numerals where small glyphs are hardest to isolate,
> and the hands do land between numerals as it predicts. But a reader deciding whether
> to trust slots 3, 13 and 21 should know that the sentence licensing the arithmetic
> is one solver's reading of a block this project has never found. See the scope and
> provenance notes in §7.

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

**[COMMUNITY, added 9 Nov 2026] A second leg, which this section never used: the
template's own high-numbered slots reach the same answer without the clock.**
Everything above is **one** support cited in six places — the hour hand, whose
*direction* is measured (238.49°, between numerals 10 and 11) and whose *addition* is
licensed only by a caption with no measured location (§2.17's scope note, §7's
provenance note). But §2.17 assigns words at slots **16** and **19**, and a word at
slot *n* means the phrase has at least *n* words. Against the valid BIP39 lengths
12/15/18/21/24:

| slot | word | what supports the slot NUMBER | grade | lengths left |
|---|---|---|---|---|
| **19** | `glove` | the `19` of the vial label `CVD19` — produced by the **one collision-free** numbering rule of the twelve tested (`even_slot_rules.py`) | **[COMMUNITY]** | **21, 24** |
| 16 | `rifle` | the `16` of M16, identified from the weapon's **shape**; no count of 16 exists in the picture | **[COMMUNITY]** | 18, 21, 24 |
| ~~17~~ | ~~`gold`~~ | ~~"17 years", a chart span checked against TradingView~~ | **STRUCK, see below** | — |

**Slot 19 suffices alone**: at least 19 words leaves 21 and 24 by arithmetic, with no
clock involved. **Slot 16 suffices with §2.3**, which exhausted the 18-word template in
both directions — and it is the *same* template, since slot 16 is inside it (t18's
thirteen fixed slots are 1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 13, 16, 17). The conditional
therefore closes on itself: accept the assignment that gives the bound and you have
accepted the template §2.3 emptied at 18.

> **[STRUCK 9 Nov 2026] `gold`@17 cannot serve as a rung, and this report's own
> chronology rule is what removes it.** The address was funded **2020-05-10 08:01:46
> UTC**, block 629754. §10's chronology table already grades the gold chart's content
> *"gold above $1,800 — no, first exceeded in July 2020 — **delete**"*, and
> `premise_audit.md` dates the element **POST (July 2020 or later) [MEASURED]**. The
> `17` is read *off that chart*, so its justification is exactly the form the rule
> kills: "the author chose W **because of** E" where E postdates the seed.
>
> **Stated precisely, because the rule is narrower than it first looks.** §10 says in
> terms that **no assignment is falsified merely by being dated after 2020-05-10** — a
> later drawing can depict a word the author already had in mind. So `gold` may still
> sit at slot 17 and the row is not retracted. What dies is the *reason to believe the
> slot number is 17*, and a lower bound on the phrase length is made of nothing but
> slot numbers. **The rung goes; the row stays.**
>
> **Two filters, applied for unrelated reasons, converge on this row.**
> `premise_audit.md`'s weakest-premise ranking puts **slot 20 first and `gold`@17
> second**, on the ground that `gold` is the only row in §2.17 where *both* links are
> inference — the word is not written and the metal is not depicted, and the slot comes
> from a span. The chronology filter, which knows nothing about that ranking, deletes
> the same row's justification independently.
>
> **One correction to how that convergence is sometimes stated:** chronology does
> **not** also delete `apple`@20. That row's date objection — the June 2020 Leopold
> defacement — was **withdrawn on 18 October**: the bust is the Dreux monument and the
> depicted vandalism is of 1 May 2018, knowable on the funding date, so §10 grades it
> **keep**. Slot 20 is killed by §2.16's spacing measurement, not by the calendar. The
> two filters agree on **one** row; the ranking supplies the second.

**Why this is a leg and not a proof, stated plainly.** Both remaining grades are
[COMMUNITY], and **both numerals are measured illegible in this file** —
peak stroke 0.09 px at slot 16 and 0.63 px at slot 19, against full pen for every
legible control (§6 item 6). The clock leg has one measured step and one unlocated
step; this leg has no unlocated step and no measured one either. What matters is that
they fail *independently*: the length does not rest on a single point of failure, but
it does not yet rest on a measurement either. Resolving either numeral in a better scan
is what would make it two-legged **on measurement** rather than on convention — §6.

There is a further reason it cannot be 12. At 12 words, order is
brute-forceable: 12! = 479,001,600 arrangements, ~29.9 M after the 4-bit
checksum, which is minutes of compute. **If you had the right twelve words you
would not need the clock at all.** An author who built an elaborate
position-marking system did so because order cannot be searched.

> **[CORRECTED 9 Nov 2026] Two faults in how that was stated.** The retracted words:
> ~~"a second, *independent* reason"~~, which it is not, and ~~"which is only true at
> 21 or 24"~~, which is false at 15.
>
> **It is not independent.** Its premise is that the author built a position-marking
> system, and the position-marking system *is* the clock-sum mechanism. If the addition
> fails there is no position machine and this argument has no premise left. It is the
> clock support in different clothing, not a second support. (The second support is the
> slot-16/17/19 leg above, which does not depend on the clock at all.)
>
> **And "only true at 21 or 24" is false at 15.** On this paragraph's own model —
> *n*! over 2^checksum, which is how it gets 29.9 M at 12 words:
>
> | words | checksum-valid orderings | at 11 M cand/s |
> |---|---|---|
> | 12 | 29,937,600 | 2.7 s |
> | **15** | **40,864,824,000** | **1.03 GPU-h** |
> | 18 | 100,037,089,152,000 | 105 days |
>
> **15-word order is one GPU-hour** — less than the pure-swap probe priced in §2.17.
> Corrected, the argument excludes 12 **and 15** and leaves {18, 21, 24}; §2.3 then
> closes 18, leaving {21, 24}. So it arrives where §5 arrives — but with §2.3 doing the
> last step, and **it never reached 21 on its own.**

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
whose default is something else.

> **[CORRECTED 9 Nov 2026] ~~If the clock is *not* a position machine, then the
> mechanism, the slot numbers, the template and all 279 billion derivations in §3
> (191 billion when this paragraph was written) were aimed at a structure that does
> not exist.~~** Too strong, and the second leg above is what corrects it. If the
> addition fails, slots 3, 13 and 21 go, and §2.13's `a + g ≥ 2` goes with them.
> **The length does not go.** `glove`@19 alone still leaves {21, 24}, and the slots
> that come from counts and written labels are untouched by the clock's failure. So
> the 316,456,008,920 derivations in §3 were aimed at a 21-word template that
> survives the clock — on a [COMMUNITY]-grade leg, which is weaker than a measurement
> and stronger than nothing.

**The template and the 12-word prior still cannot both be kept.** Anyone reaching
for 12 on the strength of the wallet defaults is discarding §5, §2.13 and §3 in the
same motion, and should say so.

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
   mechanism that gave `moon` (12+1) and `tower` (1+2) — at high confidence in the
   hand *directions*, and on an unlocated caption for the *addition* (§7 scope note) — and
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

6. **[MEASURED] A larger source image — for THREE readings, and two of them carry
   the length argument.**

   > **[CORRECTED 9 Nov 2026] ~~A larger source image, for one specific reading: the
   > circled mark on the BLM card. This is the only place in the artwork where the
   > file's resolution genuinely blocks a reading.~~** It is not the only place, and
   > the two others matter more, because §5's second leg derives the phrase *length*
   > from them. Measured on this item's own published model — peak stroke coverage =
   > (background − darkest) ÷ (background − pen), pen 29 from the BLM capitals:
   >
   > | reading | element, box | background | darkest | levels | peak stroke |
   > |---|---|---|---|---|---|
   > | the `16` of M16 → **slot 16** | rifle receiver, x 816–825 y 695–702 | 248 | 229 | 19 | **0.09 px** |
   > | the `19` of `CVD19` → **slot 19** | vial label, (130, 230, 50, 60) | 204 | 94 | 110 | **0.63 px** |
   > | the circled mark, interior | BLM card | 222 | 76 | 146 | 0.76 px |
   > | the circled mark, ring | BLM card | 222 | 118 | — | 0.54 px |
   > | ambigram date `11.03.20` *(control)* | (1012, 1098, 86, 24) | 203 | 0 | 203 | **full** |
   > | bust band `BREATHE` *(control)* | (1355, 528, 75, 17) | 226 | 18 | 208 | **full** |
   > | rune column *(control)* | (1526, 40, 31, 975) | 254 | 0 | 254 | **full** |
   >
   > **All three are sub-pixel; every legible control reaches full pen.** The
   > deprioritisation note at the end of this section said "a higher-resolution source
   > can unblock one reading, not two" — wrong by two, and corrected there as well.
   >
   > **Why the other two are worth more than the card mark.** §5's second leg reaches
   > {21, 24} from slots 16 and 19 with no clock, and both of its grades are [COMMUNITY]
   > — slot 17 was struck there on chronology grounds, which leaves these two numerals
   > carrying the length between them. Resolving **either the 16 or the 19** converts the
   > rung that needs no
   > further argument — slot 19 alone leaves {21, 24} — from convention into
   > measurement, and makes the phrase length two-legged *on measurement* for the first
   > time. The card mark settles slot 10 only if the mark turns out to be X.
   >
   > **A non-reproduction, logged rather than reconciled.**
   > `report_additions_image_pass.md` §H reports the rifle mark as "darkest 220 on a
   > background of 246 (26 levels)". From the coordinates it names, this measurement
   > gets **darkest 229, max 248, 19 levels**, identical in R, G and B, and the window
   > holds no structure at all — flat texture between 229 and 248. §H's verdict
   > (illegible; `rifle`@16 rests on identifying the model by shape) is unaffected and
   > is strengthened. The nine-level gap is not reconciled here.

   The claim below is measured rather than asserted.

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

   **[TESTED] Against glyph X: cannot be compared at this resolution.** X was
   re-measured first, as the control, exactly as §7.4 measures it (ink < 110, main
   component, skeletonized): 92 px, 4 endpoints, one 4-way crossing, 2 strokes at
   56°, arms 9.5 / 7.6 / 6.0 / 4.8 against §7.4's 9.5 / 7.5 / 6.1 / 4.7. It keeps
   that structure at every cutoff from 90 to 185. The circle's interior (disc of
   radius 6.55 px about the centre, darkest pixel 76, 7 px below 110), by the same
   method:

   ```
   ink cutoff       90   110   125   140   155   170   185
   main component    2     4    10    17    45    52    63   px
   endpoints         2     2     2     3     3     4     3
   junctions         0     0     0     1     2     2     1
   ```

   At X's own cutoff the interior is a 4-px blob with no crossing, and its
   structure changes at every cutoff. That is not evidence that it differs from X.
   X is drawn at full pen darkness; the interior is sub-pixel, so its skeleton
   follows the cutoff rather than the drawing. **The test can neither confirm nor
   exclude that the circle contains X.** Verified independently on a separate copy
   of the master with the same SHA-256: X 92 px, darkest 0; interior darkest 76,
   7 px below 110.

   **[MEASURED] The faint marks below the circle.** The tablet face is a flat fill.
   Below the circle, all 78 face pixels that are at least 3 px from the tablet's
   edge and not next to a mark are exactly 222. Against that fill:

   - **Extent and depth.** Pixels at least 4 levels below the fill span x 256–268,
     y 773–799. The darkest is 211, so they are **at most 11 levels** below the
     fill (R/G/B 10 / 11 / 11). The BLM capitals on the same card reach 221.
   - **Components after a levels stretch** (211 → 0, 222 → 255) depend on the cut:
     4 / 3 / 3 / 5 / 5 / 0 at depth ≥ 2 / 4 / 6 / 8 / 10 / 12 levels. At ≥ 4 there
     are three, of 49, 12 and 1 px; the two larger lie along 61° and 76°. **The 61°
     axis is parallel to the hand's edge (60°).**
   - **Not the tablet's shading.** 48 of the 62 mark pixels are darker than a
     pixel on both sides of them. The only shading on the face, a ramp 6 px wide
     along the tablet's left edge and joined to it, has 0 of 158 such pixels.

   **[MEASURED] They are the only feature on the tablet that comes out brighter
   than the fill beside it.** Pixels within 2 px of a dark feature that exceed 222:

   | feature | dark px | px within 2 px | brighter than 222 |
   |---|---|---|---|
   | BLM capitals and underline | 559 | 538 | **0** |
   | circle, ring and interior | 215 | 115 | **0** |
   | statue robe line art, x 116–239 y 640–759 | 7,313 | 3,716 | **0** |
   | statue robe line art, x 116–239 y 760–899 | 5,637 | 3,224 | **0** |
   | faint marks | 63 | 193 | **18**, max 226 |

   All 18 pixels above 222 in the tablet window lie within 2 px of a faint mark;
   the two robe windows contain none at all. An independent count on a separate
   copy, with different masks, gave 0/143, 0/114, 0/1,423, 0/448 and 6/92: the
   same pattern. **[INFERRED]** Overshoot beside an edge is what resampling with a
   ringing kernel leaves, so the faint marks went through a step that the drawing
   they sit on did not: they were produced differently from it.

   Nothing here reads them. §9's calibration table records this element's first
   read, `-IGHT`, at 35 levels of contrast; the depth measured here is at most 11,
   in luminance and in every channel. §9 recorded no coordinates, so whether it
   measured these pixels cannot be checked. Script: `tablet_measure.py`, output in
   `circled_check/tablet_measure.out`.

   **[MEASURED] Whether the faint marks share a rendering signature with the
   image's faint overlay texts: cannot be decided at this resolution.** The census
   was registered before it ran (`circled_check/overlay_census_plan_r2.tsv`,
   commit 2838769). It covered every faint overlay text that §9's census lists,
   four faint clock numerals, and six controls of ink on a flat fill, all by one
   method:

   - background: the mode of the pixels above the window's median;
   - marks: pixels at least 4 levels below the background;
   - eligible: only if the background value covers at least 50% of the pixels
     more than 2 px from any mark. Eligibility was fixed by flatness alone,
     before any brighter-pixel count.

   The claim needed three things: the faint marks showing brighter neighbours,
   at least three eligible overlay items all showing them, and no eligible
   control showing them.

   | item | role | background | flat share | result |
   |---|---|---|---|---|
   | tablet faint marks | subject | 222 | 94.3% | brighter 18 of 128, max 226 |
   | `ONLY real BITCOIN` | overlay | 222 | 100.0% | brighter 1 of 301, max 223 (see below) |
   | `PAY FOR THE FUTURE.` / `THIS IS THE FIRST PREDICTION.` | overlay | 198 | 4.6% | not eligible |
   | clock-hand word `TOWER` | overlay | 217 | 19.2% | not eligible |
   | clock-hand word `MOON` | overlay | 218 | 16.7% | not eligible |
   | `FIND THE SEED PHRASE` watermark | overlay | 223 | 7.1% | not eligible |
   | `IN THE THIS PICTURE` | overlay | 239 | 23.8% | not eligible |
   | Latin line | overlay | 241 | 17.3% | not eligible |
   | four faint clock numerals | overlay | 203–225 | 18.3–28.1% | not eligible |
   | rune lines (5), `Order and stability`, Amendment copy, bottom caption | outside the rule | 142–238 | 2.5–33.2% | not eligible |
   | BLM capitals and underline | control | 222 | 99.2% | brighter 0 of 324 |
   | circle, ring and interior | control | 222 | 100.0% | brighter 1 of 234, max 223 (see below) |
   | statue robe line art, three windows | control | 222 | 91.8–100% | brighter 0 of 164, 190, 187 |
   | plinth band top-edge line | control | 222 | 100.0% | brighter 0 of 211 |

   **One overlay item was eligible, against the three required.** The other ten
   fail on flatness alone. The clock face, the watermark and the ghost text beside
   the address all sit on textured backgrounds, so there is no flat fill against
   which to call a pixel "brighter". **This thread is closed.** The faint marks
   stay as recorded above: measured, and unread.

   **Two eligible rows do not measure what their names say,** and they should not
   be read as evidence either way:
   - `ONLY real BITCOIN` qualified only through a 74-px strip at 222 along the
     window's top row. The band itself is 209, so the band and its text were
     counted as marks together.
   - The circle control's one brighter pixel, (269, 773), sits on the window's
     bottom edge beside two faint-mark pixels. It is one of the 18 above; the
     circle contributes none.

   The rule set no minimum size for the area away from the marks, and the circle
   window qualified on 9 px of it.

   A first round, plan e915ab5, skipped all 27 items. Its flatness rule measured
   how much of each window was text. It was replaced, not tuned: round 1 computed
   no brighter-pixel count for any item. Scripts: `overlay_census.py --round 2`,
   with the post-hoc check in `circled_check/overlay_census_r2_diag.py`.

   **[MEASURED] Where the faint marks sit on the tablet.** The tablet's dark
   outline was traced, taking the darkest pixel per column or row in guided bands.
   Its edges are straight lines with 0.8–2.7 px rms residual:

   | line | direction (0° = horizontal, 90° = vertical, y up) |
   |---|---|
   | tablet long axis (left outline; right outline) | **83.4°**; 80.0° |
   | tablet short axis (top outline) | **162.9°** |
   | BLM underline | **157.5°**, within 5° of the short axis |
   | faint marks (per component; all pixels) | 61° / 76°; **65.9°** |
   | hand edge | 60° |

   In tablet coordinates (along the long axis from the top, across from the left
   edge; the bottom edge is hidden under the sleeve, so "along" is approximate):
   BLM at 0.19 along / 0.33 across, the circle at 0.47 / 0.25, the faint marks from
   0.58 to 0.81 along at 0.22–0.27 across. **The faint marks are not a third line
   parallel to BLM:** they run about 90° from BLM's direction. They lie 1–16° from
   the hand edge and 6–21° from the tablet's long axis. They are not the hand's
   shadow either: they are separate dips in a flat fill, and none touches an edge
   pixel (above).

   **[MEASURED] Their structure along that line.** Ink is taken in the G channel
   (fill 235, ink ≤ 231, face core only), with the text line at 62.1°. That gives
   63 px over 28 × 8 px, in **two groups split by an empty 2-px gap**: 20 px long and
   9 px tall at x 256–266, y 780–799, then 7 px long and 4 px tall at x 265–268,
   y 773–778. The ink profile along the line reads
   `2 1 1 1 1 2 1 5 3 3 4 4 5 2 4 1 2 2 4 2 0 0 1 3 3 3 1 1 1`. The first group has
   internal dips at steps 6 and 15, consistent with two or three glyphs, but
   nothing separates them cleanly. The same pipeline on blank tablet face
   (x 272–295, y 731–743) finds 0 ink. Three questions stay **undetermined at this
   resolution**:
   - **The glyph count.** Two groups are certain; three glyphs is not shown.
   - **An I between H and T.** The 2-px gap holds no ink, but an I merged into the
     group before it cannot be excluded.
   - **A letter before the first.** The 6 px between the first glyph and the
     tablet's left outline are the edge's shading ramp, which this test cannot
     tell from a mark.

   **S or G cannot be decided at this resolution.** The first glyph, sampled on
   the line's own axes as a 9 × 7 ink map, was correlated with the artist's own
   letters at the same size: S from STOP, SHIT (spray) and LIVES, G from KILLING
   (none of SHIT, STOP, LIVES or BLACK has a G), and T from STOP as a non-candidate.
   The scores are S −0.087 / +0.043 / −0.094, G −0.200 and T −0.101. **The
   yardstick shows the method has no power here:** the artist's three S's correlate
   with each other at −0.030 to +0.156, and with G at −0.037 to +0.143. Shifting
   the faint glyph's box by one pixel moves its G score from −0.333 to +0.206.
   Script: `sht_compare.py`; segmentation in `circled_check/oct18_measurements.py`,
   section E.

   **[INFERRED] Hypothesis, no run: "шт".** If the faint group reads `SHT`, it may
   be Russian `шт` ("pieces"); with the README's `XX` it would read "20 pieces".
   It is a reading, not a template: not a 20-word Electrum template, and nothing is
   queued on it.

   **Separately, arithmetic:** if the image holds 20 words, a 21st word completes
   the phrase, and for any 20-word prefix exactly **16** of the 2048 words are
   checksum-valid finals, one in each block of 128. `t21_loo21` swept slot 21 over
   all 2048 words under both slot-20 readings, with the other gaps on the 54-pool,
   so all 16 are covered for those prefixes (compressed key only, §3).
   *[Reworded 18 Oct: the first version joined the hypothesis, the blank clock
   hand and this arithmetic in one sentence.]*

   **[MEASURED] A possible wristwatch on the third masked person** (bag strap),
   window x 336–365, y 238–269. A closed loop appears only at loose cutoffs
   (ink < 160–170), outlined by ink at x 341–351, y 245–258, about 10–11 × 11–14 px.
   Its interior is 15–28 px at background level (173–179 against a window median
   of 173), with nothing dark inside: no hands. At ink < 150 or darker the loop is
   open, and the enclosed regions move between cutoffs. It may equally be a strap
   ring. No time can be read, and no larger copy of the image has been found
   (§7.3). If it hints at "time", that word is already in the 54-word gap pool.
   Script: `circled_check/oct18_measurements.py`, section A.

   **[INFERRED] A larger original may exist.** Sub-pixel strokes are what a larger
   working file produces when downsampled, which is the reason to want one.
   *[Tagged 14 October. This read "such an original probably exists", untagged.]*
   There is an alternative this file cannot exclude: a thin anti-aliased pen drawn
   directly at 1600×1200 gives sub-pixel strokes too. The circle shows no
   overshoot, the same as the statue's line art. That fits drawing at this size,
   and it equally fits a larger original downsampled with a filter that does not
   ring, so it does not decide between them. The hope stands; it is not a finding.

**Deprioritised, with reasons:**

- **A larger source image, for the rune glyph.** The glyph is not pixel-blocked:
  §7.4 measures it at 13×20 px, 96 ink pixels, strokes 3–4 px wide, 248 levels
  of contrast, 4 clear rows to the border above it and 5 to the separator below,
  and no ink in the titlo band — complete, untruncated, carrying no numeral mark. Its shape is
  fully resolved and a better scan renders the same two strokes. What is missing
  is a **key** — the author invented glyphs beyond the 26 Gravity Falls supplies,
  and X occurs once, so there is no second instance to triangulate from. Per §2.9
  no larger source is served anyway: `i.redd.it` returns the same 1600×1200 file,
  md5-identical. The circled mark above is a separate case. ~~and the only real one:
  **a higher-resolution source can unblock one reading, not two.**~~ **[CORRECTED
  9 Nov 2026]** Three readings in this image are sub-pixel, not one — the card mark,
  the vial's `19` and the rifle's `16` — and item 6 measures all three on one scale.
  Two of the three carry §5's second leg on the phrase length, which is what makes a
  larger source worth more than this note allowed. The rune glyph is still not among
  them.
- **More compute against the current template.** It is exhausted. A corrected
  template can be tested in seconds; an uncorrected one cannot be rescued by scale.
- **[SCOPE, opened 2026-11-09 by §1.10] A by-file allow-list for bare `hex64`, so the
  publication gate can block a raw private key or seed.** The gate's pattern deliberately
  omits a bare 64-hex token, because **26 tracked files legitimately contain one** — sha256
  stamps, spec test vectors, commitments — and a blanket rule would block the repository
  outright. Until those 26 are enumerated and pinned, that case rests on the shape arm of
  the reading rule in `DO_NOT_PUSH`, which is a human procedure. This is the only leak
  shape the automated gate does not cover.
- **[SCOPE, opened 2026-11-10] A sub-element inventory. `r10_elements.json` lists 28 whole
  objects, and nothing inside any of them.** The collar form at the Leopold bust (§2.16) is
  a feature of roughly **24 × 32 px sitting inside `E24`**, which is one box for the entire
  bust. It went unexamined for six weeks **while that box was being used in a layout test**,
  and it was found by looking at the painting in tiles rather than by any measurement this
  project had. **This gap is worth recording whatever the form turns out to be**, and it is
  recorded on that basis alone: the inventory's unit is the object, so a mark *on* an object
  is invisible to every script that reads the inventory. How many other sub-element features
  exist is unmeasured — the 25-tile contact sheet of 10 Nov is the only pass ever made at
  that scale, and it was made looking for one specific thing.

---

## 7. [MEASURED for the alphabet and block A; EXTERNAL for blocks B and C] The rune alphabet is solved — it is Cyrillic, not Greek

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

> **[MEASURED 9 Nov 2026] Re-measured on all 42 glyphs. Every earlier glyph figure in
> this section covered 37 of them and excluded `здесь` entirely.** `runelib.cells()`
> sliced `groups()[:7]` against a 7-word list, and `groups()` stopped at y=1000, which
> cut `здесь` from five glyphs to three. **The slice is what hid the truncation**: the
> length assert never saw the short group. Both are now fixed (`y1=1020`, `здесь`
> added, slice dropped), and the column yields 42 glyphs in 8 groups — sizes
> 1, 5, 4, 6, 2, 8, 11, 5 — exact against all eight words. The sentence above claims
> that exact match including `здесь(5)`; it was **true but not reproducible from the
> shipped tool**, which is its own small instance of the §10 rule.
>
> | | 37 glyphs (as shipped) | **42 glyphs** |
> |---|---|---|
> | same-letter | +0.588 (n=31) | **+0.586** (n=36) |
> | different-letter | +0.069 (n=635) | **+0.070** (n=825) |
> | separation | +0.519 | **+0.515** |
>
> **Adding a whole word moved the aggregate by 0.002, and that is the result.** The
> monoalphabetic claim is unchanged by five new glyphs.
>
> **The claim holds at 32 of 36 same-letter pairs, mean +0.622. Four fall below the
> different-letter 95th percentile of +0.390** — and this is a correction to how this
> section presented itself, not a finding against `здесь`:
>
> ```
> р  номер    x  р  чёрный        +0.224
> е  номер    x  е  здесь         +0.239
> е  день     x  е  здесь         +0.349
> р  чёрный   x  р  зашифрованы   +0.361
> ```
>
> **Two of the four are `р`, and all three `р` instances sit inside the already
> published 37.** The weakness therefore predates `здесь` by every measurement in this
> file and was never disclosed: the 37-glyph set already had 2 of 31 pairs below its
> own threshold. `р` in `чёрный` is weak against *both* its counterparts, which is the
> same pattern as the `здесь` `е`, in a word this report has treated as confirmed
> throughout.
>
> **Every weak glyph is still rank 1 for its own label**, which is what makes these
> hand-drawing variation rather than counter-evidence. The `здесь` `е` scores +0.349
> against its own label and **+0.310 against second-place `д`** — nothing in the
> inscription matches that cell better than `е` does. It is also not a segmentation
> artefact: h 17, ink 140 px, w 22, against the other two `е` cells at h 17/16, ink
> 152/130, w 22/21.
>
> **`здесь` is confirmed on 4 of 5 glyphs, not 5.** Its `с` has **only one instance in
> this column**, so there is no pair to test and it is counted as untestable, not as a
> pass. `ь` +0.691, `д` +0.756, `з` +0.836 all clear the bar; `е` is the weak one.
>
> **[NON-REPRODUCTION, logged not reconciled]** This section publishes **+0.63** for
> same-letter "within one line". The harness of `glyphX_measurement.md` §2 — ink bbox
> to 32×32, z-scored, Pearson, as `rune_x_check.py` implements it — gives **+0.588** on
> that same line. A **0.04** gap whose cause is unidentified. It is recorded rather
> than reconciled, because the way to close it would be to pick the cell set that
> reproduces +0.63, and choosing inputs to match a published output is the error this
> report exists to avoid.
>
> **[MEASURED] Shape clustering, for completeness: 24 clusters against the decode's 22,
> and the gap decomposes exactly.** At IoU ≥ 0.60 over the 42 masks, **five splits**
> and **three false merges**: `р` splits 1+2 (номер apart from чёрный/зашифрованы),
> `е` splits 2+1 (номер/день apart from здесь), `о` splits into **three** (номер,
> биткоины, зашифрованы all separate), `ь` splits 1+1 (день apart from здесь); and
> three clusters each hold two labels — **`е`/`ё`, `д`/`о`, `и`/`й`**. `22 + 5 − 3 =
> 24`. The false merges are exactly the diacritic pairs — `ё` is `е` with a diaeresis,
> `й` is `и` with a breve — which bounding-box normalisation at 34×34 washes out. The
> splits are hand-drawing variation; the correlation harness above, not IoU, is the
> measurement this section rests on.

#### Two dead ends on this inscription, recorded with their numbers so they are not re-asked

**[NEGATIVE] The dot-stacks carry no digit.** Detected globally — every ink component
in the image, filtered to dot-sized (3–14 px, bbox ≤ 5×5) and grouped into collinear
triples — the rune column holds **exactly 7 dot groups and every one has exactly 3
dots** (15–28 ink px, h 3–5). Eight words, seven separators, and **no 2-dot or 4-dot
stack anywhere in the column**. The count never varies, so it encodes nothing. In
particular **there is no dot-stack at the `номер X` position**: that cell is **one
connected component**, 96 ink px, 13 × 20, matching §7.4 exactly, and the nearest
dot-stack is 6 px below it serving as the ordinary separator between `X` and `номер`.

**[NEGATIVE] The glyphs are not Unicode Runic.** All 41 Runic codepoints that FreeMono
renders — Elder Futhark, Younger Futhark and Anglo-Saxon Futhorc — scored against a
representative of each of the 22 labels: best match **IoU 0.456** (`з` → `ᛋ`), mean
**0.376**, and **0 of 22 clear 0.60**. Every best match falls *below* the +0.587
same-letter IoU baseline measured on this very column and barely above the +0.328
different-letter baseline. So `X` cannot be read off a Futhark chart. **What this does
not close:** a decorative font can map Basic Latin codepoints to shapes that are not
the Unicode Runic characters, and the specific *AngloSaxon Runes* TrueType font is not
installed here, so the font-substitution hypothesis is narrowed, not eliminated.

#### [SCOPE, 9 Nov 2026] 99 rune letters are published here. 42 have a measured location; 57 do not

Three rune blocks are decoded in this section. Only one of them has ever been located
on the canvas by this project:

| block | published decode | letters | location |
|---|---|---|---|
| **A** right-edge column | `здесь зашифрованы биткоины на чёрный день номер X` | **42** (41 Cyrillic + `X`) | **MEASURED**: x 1526–1557, y 40–1015; 42 glyphs in 8 groups, sizes 1,5,4,6,2,8,11,5, 7 three-dot separators, pitch 19.9 px/run |
| **B** clock caption | `Сумма двух чисел` | **14** | **NOT LOCATED** |
| **C** top block | `Я надеюсь что сюда будут присылать много биткоинов` | **43** | **NOT LOCATED** |
| | | **99 / 57 unlocated** | |

**This is a larger gap than anything else this report states.** §7.2's correlation
figures, §7.4's glyph-X measurement and the monoalphabetic claim all rest on block A
and only on block A. Nothing in the tree has ever measured a pixel of B or C.

**What "not located" means here, precisely.** For B, three boxes around the dial
(centre (470,937), radius ~182) at ink < 130/180/215 return **zero** glyph-sized
components and no line of ~14 similar marks. For C, a sweep of every 31-px band on the
canvas, scored by block A's own signature — paper fraction above 40% and a run count
stable across three thresholds — finds **block A and nothing else**; the two best
horizontal candidates each span x 36–1565 with seven gaps wider than 60 px, so they
are slices through separate objects, not lines of letters. **It does not mean the
blocks are absent.** §7.5 places B *"inside the clock face, among the numerals"*,
which is exactly where small glyphs would be hardest to isolate from dial marks — and
the scattered small components found there, over x 295–692 and y 760–1123, are
consistent with either reading. The claim is that a defined search did not find them,
not that they are not there.

#### [PROVENANCE, 9 Nov 2026] B and C trace to a 2021 Reddit comment, not to a measurement

Traced with `git log -S`. Both unlocated transcriptions, and block A's as well, enter
the report in **one commit**:

```
77f2c52  2026-08-22  "Add rune cipher analysis (section 7), Electrum results, corrected tally"
         REPORT.md | 256 ++++++-------      1 file changed, 214 insertions(+), 42 deletions(-)
```

**One file, no script, no stated source.** The pixel tooling that could have measured
them arrived five weeks later: `imgio.py`, `census_crops.py` and `runelib.py` in
`c8d9f39` (2026-09-27), `rune_x_check.py` in `f3c43c5` (2026-10-24). `runelib.py`
reads x 1526–1557 only — block A. The other files that contain these strings
(`word_census.py`, `brain_image_corpus.py`, `idiom_ink.py`) are aggregators;
`word_census.py`'s own docstring says it *"reads NO pixels"* and *"adds no new reading
of the image and no new word"*. **No file in this tree has ever measured B or C.**

So of the three outcomes this trace was set up to distinguish, it is not (a) and not
(c). It is **(b)**: the source is external, and it is identifiable. `u/Amadeus407`,
comment `gpzromb`, **2021-03-06 18:27:47 UTC**, headed *"Verbatim spelling. It might
make a difference."*, carries all three decodes character for character as this report
publishes them:

> *1. runes from above "Я надеюсь что сюда будут присылать много биткоинов." 2. runes
> at the bottom "Сумма двух чисел". 3. Runes on the right "Здесь зашифрованы биткоины
> на чёрный день номер X."*

Verified against the raw Reddit JSON (sha256 `39d61b72…`), the same primary source
§1.1's provenance note uses.

**The three blocks therefore have different warrants, and the section did not
distinguish them:**

- **Block A — [EXTERNAL, independently confirmed].** It came from this comment too,
  but this project has since re-measured it: 42 glyphs, group sizes exact against all
  eight words, same-letter correlation +0.586 against +0.070 for different letters.
  The decode was adopted; the confirmation is ours.
- **Blocks B and C — [EXTERNAL, not independently measured].** Adopted from the same
  comment and never checked against a pixel. They are **not** unreconstructable in the
  way §3's retracted 3.72% was — the source is known, dated and quotable — but they
  are one solver's reading of 2021, carried for five years and never re-derived.

Nothing here is retracted. The decodes may be entirely right; `Сумма двух чисел`
reproduces as the clock's caption in meaning, and §7.2's measured confirmation of
block A raises the prior on the same hand having read the others correctly. What
changes is the label: two of the three blocks are **somebody else's measurement**, and
this section presented all three in one voice.

##### [MEASURED from the JSON, 9 Nov 2026] The transcriber said the Russian→BIP39 mapping was ambiguous — five days BEFORE posting the decodes

`u/Amadeus407`, comment **`gpasv2d`**, **2021-03-01 14:06:58 UTC**, top-level on the
submission, verbatim:

> *"Unfortunately, I do not know English. In translation from Russian, words have
> different meanings based on the context. And often there is more than one word in the
> bip39 dictionary. I would like to talk to the author, so that he gave the right words
> (if I correctly guess the meaning of a particular riddle)."*

**It predates `gpzromb` (2021-03-06 18:27:47 UTC) by 5 days** — 5 d 4 h 20 m 49 s, from
the `created_utc` fields 1614607618 and 1615055267. So the person this report takes its
three decodes from had already stated, in public and before posting them, that **he did
not read English, that his Russian readings were context-dependent, and that a Russian
word often maps to more than one BIP39 word**. He asked the author for the right words
and, on the evidence of the thread, never got them.

This is a statement about the **word** links, not the slot links, and it does not touch
the Cyrillic: §7.2 re-measured block A's glyphs and confirmed the Cyrillic reading from
pixels. What it qualifies is the step after that — Cyrillic to English to BIP39 — which
no measurement in this tree covers for any block.

**All four of this author's comments in the fetched thread, for the record:**

| id | UTC | what it is |
|---|---|---|
| `gp3hv35` | 2021-02-27 23:23:56 | reply to the submission |
| **`gpasv2d`** | **2021-03-01 14:06:58** | **the ambiguity statement above** |
| `gpzlri7` | 2021-03-06 17:42:03 | the three decodes in **English** translation, "All phrases are in Russian" |
| `gpzromb` | 2021-03-06 18:27:47 | self-reply, "Verbatim spelling", the **Cyrillic** this report adopted |

**[MEASURED] The transcriber puts block B at the BOTTOM — and the bottom is now closed
too.** Both `gpzlri7` and `gpzromb` locate the three blocks in the same words — *"runes
from above"* (C), ***"runes at the bottom"*** (B), *"Runes on the right"* (A). Block A's
"on the right" is exactly where this project measured it, x 1526–1557: the one check
available on his location wording, and it passes.

> **[CORRECTED 9 Nov 2026] ~~The bottom strip has not been searched for block B …
> recorded as the next place to look.~~** Mis-worded, then over-corrected in a first
> retraction, and now settled by a **pre-registered** test. The prior and the decision
> rule were committed before any pixel in the regions was counted:
> `blockb_bands_plan.md`, commit `ed862df`, plan blob `ee814f19`.
>
> **Two facts that bound what the test could mean, recorded in the plan ahead of it.**
> First, **"at the bottom" does not exclude the region already searched** — the dial
> disc spans x 288–652, y 755–1119, which lies inside the bottom third, so the
> transcriber's wording and the search region were never in conflict and the retracted
> note was wrong to imply they were. What the disc missed is *area*: 96,762 px of the
> bottom third's 640,000, **15.1%**, touching 320 of 400 rows but only **365 of 1600
> columns**. Second, **the bottom edge has no room**: the whitepaper caption
> (25, 1138, 1040, 28) and the Latin line (1025, 1140, 530, 50) span x 25–1555, leaving
> **25 px** and **45 px** against the **279 px** that 14 glyphs need at block A's
> measured 19.9 px pitch.
>
> **The prior was stated as LOW before measuring, with the arithmetic that makes it
> low.** Of the four regions fixed in the plan, three are too small to hold 14 glyphs
> of block A's 13 × 20 px in either orientation — R2 is 10 px tall against a 20 px
> glyph; R3a and R3b are 25 and 45 px wide against 279, and 52 px tall against it the
> other way. **One region of four was geometrically capable**, R1 at 38 × 1600.
>
> **Result: negative in all four, and the control passes.** Glyph-sized components
> (bbox 6–33 × 10–40 px, 40–600 ink px) over the pre-registered sweep:
>
> | region | px | <90 | <110 | <130 | <150 | <170 | <190 | <215 | verdict |
> |---|---|---|---|---|---|---|---|---|---|
> | R1 y 1100–1138, full width | 60,800 | 8 | 8 | 7 | 7 | 13 | 11 | 5 | negative |
> | R1′ same, minus the disc | 58,656 | 8 | 8 | 7 | 7 | 13 | 11 | 6 | negative |
> | R2 y 1190–1200, full width | 16,000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | negative |
> | R3a x 0–25, y 1138–1190 | 1,300 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | negative |
> | R3b x 1555–1600, y 1138–1190 | 2,340 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | negative |
> | **CONTROL block A, x 1526–1557** | 30,225 | **47** | **47** | **47** | **47** | **46** | **40** | **23** | **POSITIVE, 7 of 7 cuts** |
>
> The control clears the ≥14 bar at **all seven cuts**, so the nulls are informative —
> which is what last round's pitch-run attempt could not say for itself. R1 came closest
> at **13 components at a single cut**, falling to 11 and 5 on either side: it fails both
> arms of the pre-registered rule, the threshold and the stability. R2 and R3a are
> **empty at every cut**.
>
> **What the plan said a negative would mean, and so it means it.** This tested **the
> transcriber's own words** rather than our guess about the dial, which is why it closes
> more than the dial negative did: *"runes at the bottom"* now has no region that both
> fits 14 glyphs and is unexamined. **Block B stays unlocated, and §2.17's three
> scope-marked slots stay scope-marked.** Nothing here touches what block B *says* —
> only where it is. Script `blockb_bands_check.py`, output `blockb_bands_check.out`.
>
> *A counter in the first execution of that script mis-reported the control's
> consecutive-cut figure as 2 where it is 7. The component counts were unaffected; the
> bug was fixed and the script re-run before its output was committed.*
>
> **[MEASURED] What R1's 13 components ARE, which matters more than that 13 < 14.**
> Counting them invited a near-miss reading. Identifying them removes it — all 13
> centroids at ink < 170 fall in catalogued places:
>
> | where | count | box |
> |---|---|---|
> | the **ambigram date** | **6** | x 1012–1098, y 1098–1122 |
> | the **seal scroll**, mirror text | **6** | x 470–860, y 1040–1135 |
> | **neither** | **1** | centroid (40, 1119), 9 × 38 px — the left frame line, measured at x 40–43 when the left-edge column was disproved (§10, sixth rule) |
>
> So **R1's peak is a catalogued date plus mirror-text fragments**, with one frame-line
> sliver. It is not 13 unexplained glyphs one short of a bar. Nothing in R1 is
> unaccounted for.
>
> **[MEASURED] And the negative is scoped to CONTRAST, because the control is block A at
> 254 levels and full pen.** A faint block B is a different question from a missing one,
> so it was measured rather than argued: block A's **own column** was attenuated in ink
> depth only — 42 glyphs still present, same mask, same method, same cuts — and
> re-counted.
>
> | contrast of the attenuated copy | <90 | <110 | <130 | <150 | <170 | <190 | <215 | |
> |---|---|---|---|---|---|---|---|---|
> | as drawn, **254 levels** (block A) | 47 | 47 | 47 | 47 | 46 | 40 | 23 | seen |
> | **146 levels** (the circled mark, §6 item 6) | 0 | 37 | 45 | 47 | 47 | 47 | 47 | seen |
> | **110 levels** (the vial `19`, §6 item 6) | 0 | 0 | 0 | 39 | 46 | 47 | 46 | seen |
> | 80 levels | 0 | 0 | 0 | 0 | 0 | 46 | 47 | seen |
> | 60 levels | 0 | 0 | 0 | 0 | 0 | 0 | 47 | seen |
> | **45 levels** | 0 | 0 | 0 | 0 | 0 | 0 | 44 | **seen — the floor** |
> | 35 levels | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **BLIND** |
> | **19 levels** (the rifle `16`, §6 item 6) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **BLIND** |
>
> **The floor is 39 levels, and it has an exact cause rather than an empirical one.**
> The sweep's top cut is < 215 and this column's background is 254, so the test can see
> only ink reaching **254 − 215 = 39 levels** deep: at 45 levels the darkest pixel is
> 209 and is counted, at 35 levels it is 219 and is not.
>
> **So, stated plainly and more narrowly than "it cannot see a faint one":**
> - The negative **does** exclude a block B drawn anywhere from block A's 254 levels
>   down to ~39 — which covers the circled mark's 146 and the vial `19`'s 110. At those
>   contrasts the attenuated control still returns 39–47 components where R1 returns at
>   most 13, so such a block would have been seen and was not.
> - The negative does **not** exclude a block B drawn below ~39 levels. The rifle
>   receiver's `16` in this same image is **19 levels** (§6 item 6), so that is a real
>   contrast in this artwork and not a hypothetical.
>
> **That is the honest boundary of the Y-1 result**, and it narrows what the test can
> claim without weakening it much: the blind band is the bottom 15% of the contrast
> range, not "anything faint". Script `blockb_bands_sensitivity.py`, output
> `blockb_bands_sensitivity.out`. All three reference contrasts come from §6 item 6,
> which measured them on one scale.

**[MEASURED] What the ambiguity warning leaves untested, bounded.** The one word in the
template that comes from a rune plaintext is `black`@10, from `чёрный день`. Across
all 21-word configs in the tree, slot 10 has been occupied by **79 distinct words** and
**never by `@FULL`** — so the dictionary has never been swept there. `dark` is not a
BIP39 word, so that particular ambiguity does not arise; but the transcriber's warning
is general, and at slot 10 it has been explored over 79 of 2048.

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

**[MEASURED, 2026-10-14] The master is the file attached to the author's post.**
Re-downloaded from [`i.redd.it/n1x7g8ceaur51.png`](https://i.redd.it/n1x7g8ceaur51.png),
the image on submission `j79zvj` (§2.17), and compared with this project's
`0.2-btc-puzzle.png` by full sha256 and a byte comparison, not by md5 alone:

```
sha256 (both)         d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782
md5 (both)            7710323461a924987eb35c77055e59f6
bytes (both)          2,383,395
pixels (both)         1600 x 1200, RGBA
cmp                   no differing byte
HTTP Last-Modified    Thu, 08 Oct 2020 09:25:31 GMT   (post: 2020-10-08 09:25 UTC)
HTTP ETag             "7710323461a924987eb35c77055e59f6"   = the file's md5
```

Every pixel measured in this section therefore comes from the file Reddit has
served since the minute of posting, with no re-encoding anywhere between Reddit
and this project.

**[SCOPE] It does not show two further things.** First, that Reddit stored the
bytes exactly as the author uploaded them: nothing outside Reddit can measure
that. Second, that no larger copy exists anywhere in public. The only evidence on
size is §2.9's, which is narrower: Reddit serves nothing larger
(`preview.redd.it` at 2048/3000/4096 returned nothing). Reddit's post metadata,
which would record the source dimensions, refused the request (HTTP 403) and was
not read. Per §7.6, a larger copy would not resolve X anyway.

**[TESTED] Reverse image search, Yandex Images, 16 Oct 2026, run by Mohammed.**
`statue_native.png` returned no copy of the puzzle and no exact source, only
general Statue of Liberty clip art. The closest was ru.ac-illust.com "Free Vectors
statue of liberty", 453 × 750, not yet compared. `card_x6_nearest.png` returned no
matches, only unrelated cartoons. Google Lens, TinEye, Bing and Shutterstock
94143832 are still to do.

**[TESTED] File forensics on the master** (sha256 `d0b04378…a782`), 25 Oct 2026,
re-run here:

| check | result |
|---|---|
| exiftool | no EXIF, comments or text chunks; no tags beyond the PNG header fields |
| chunks | `IHDR`, `sRGB`, `sBIT`, 291 × `IDAT`, `IEND`; pngcheck OK; **0 bytes after `IEND`** |
| binwalk | two hits: the PNG header itself, and the image's own compressed stream at the start of the IDAT data. Nothing else; neither is hidden data. |
| IDAT | one zlib stream of 2,379,829 bytes, decompressing to exactly 1200 × (1600 × 4 + 1) = **7,681,200** bytes, with **0** bytes left over |
| alpha | 255 everywhere |
| zsteg `-a` | 135 lines name a file type and 40 printable runs of 24+ characters occur. The types are libmagic's usual false matches on random bits (OpenPGP keys, ADCP, cpio, MPEG ADTS, compacted data). The runs are not text: 6–64 distinct characters each, no 4-letter-or-longer BIP39 word in any. An unrelated control PNG gives the same kind of matches (22 in 57 lines). Output: `circled_check/zsteg_master_all.txt`. |
| steghide / stegseek | do not apply to PNG |

**No file-level steganography was found.**

**[MEASURED] A circulating copy, sha256 `c167c072…a5bd` (2,397,988 bytes), is a
machine image-translation overlay** (Google Lens / Translate style), **not the
original and not a plain re-encode.** *[Corrected 26 Oct: first recorded here as a
hand-annotated working copy.]* One is in
this tree's download folder. Compared with the master:
- **28,830 pixels differ, all in text areas, in 10 regions:** the top-left rune
  lines, "Order and stability", the "PAY FOR … PREDICTION" ghost text, the seal
  and pyramid lettering, the Latin line, and the bottom-right signature box.
- **In each region the artwork's text is replaced by machine-translated text,**
  checked region by region against the master:

  | region | master | overlay prints |
  |---|---|---|
  | Latin line | *Esse quam niger es, sic dixit caccabus ollae* | "To be as black as you are, that's what the shit pot said." |
  | pyramid-base motto (mirrored) | *FIAT JUSTITIA ET PEREAT MUNDUS* | "LIVL WELLY EL DENEYL SHPIROG" |
  | seal ribbon | UBI BENE IBI PATRIA | "BULBI" |
  | seal-ring motto | mirrored arc lettering | "COGMO2SELF SLG J2" |
  | yellow script | "…stabili…" | "poles" |
  | clock numeral 9 | the numeral | "of" |
  | top-left rune line | runes | "0\|Chatro yen" |
  | bottom-right box | two framed glyphs | "-yi-" |
  | ghost text | faint "…PREDICTION" | a typed "PREDICTION" (the word is faintly present in the master, so that reading stands) |

  These strings are the overlay's output, not text in the artwork, and none was
  used as a candidate anywhere in this report.
- **Its chunks are `IHDR`, `sBIT`, 293 × `IDAT`, `IEND`, with no `sRGB`:** the list
  §2.9 first recorded. That early line was probably read from this copy.
- **The areas this report measures are pixel-identical in both copies:** the
  tablet, the circle, the faint marks, glyph X, the right-edge rune column, the
  clock caption and the top-left signature.
- **This report's scripts read the master.**

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
habit of it. *[Superseded 24 Oct: the `/` form is the Younger Futhark rune ᛅ, a
different rune, not a mirrored ᚾ. See the end of this section.]*

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
> *[24 Oct: shape now matched to the Younger Futhark rune ᛅ, and read as 10,
> [INFERRED]. See below.]*

**[MEASURED, 24 Oct] X has the shape of the Younger Futhark rune ᛅ** (U+16C5,
long-branch *ár*). ᛅ is one vertical stave crossed by one diagonal rising to the
right (`/`), which is exactly the measurement above: 2 strokes, 4 arms, one
crossing, diagonal `/`. ᚾ (naudiz, *nauðr*) is the same with `\`. The Elder Futhark
test above could not find it, because the Elder Futhark has no ᛅ. So the "mirrored
naudiz" is a different rune, not an anomaly. Checked here with
`rune_x_check.py`:
- **Structure,** by the same skeleton method on X and on runes rendered in FreeMono:
  X has 4 endpoints and a `/` diagonal; ᛅ has 4 endpoints and `/`; ᚾ has 4 endpoints
  and `\`.
- **The correlation harness** of `glyphX_measurement.md` §2 (ink box stretched to
  32 × 32, z-scored), recalibrated on the right-edge column's own letters: same
  letter +0.588, different +0.069, 95th percentile +0.377. Against all 31 distinct
  Younger and Elder Futhark runes, X ranks **ᛅ first at +0.611**, then ᚼ at
  +0.508 and ᚾ at +0.359. Font glyphs are not hand-drawn, so the rank carries more
  weight than the score.

**[INFERRED] The reading.** ᛅ is rune 10 of the 16-rune Younger Futhark,
ᚠᚢᚦᚬᚱᚴ ᚼᚾᛁᛅᛋ ᛏᛒᛘᛚᛦ. The right-hand line `здесь зашифрованы биткоины на чёрный
день номер X` would then read "here are encrypted bitcoins for a black (rainy) day,
number 10". That gives word 10 a position from the author's own text, where §2.17
found none: `black` (чёрный) or `rain` (the idiom's rainy day). It reads one glyph
through a second alphabet's order, and that step is the inference. No new run is
needed: `black`@10 is in every template, and `rain`@10 ran in `t21_alt3` (§2, the
queue of 19–20 Oct, negative). Credit: suggested by Gemini, checked here.

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
interpolation. *[26 Oct: the c167c072 translation overlay (§7.3) prints "-yi-" over this
box, so this reading was probably taken from that copy. On the master the box
holds two framed glyphs that are not resolved; see the artist marks below.]* Run through VanceAI at 8×, the same region renders as a boxed
`ER`. The model **replaced** characters it could not read with letterforms it
found more plausible — cleanly, confidently, and wrongly.

**[MEASURED] Two artist marks, recorded as leads for finding a larger copy.**
- **Top-left border, inside the black frame:** a faint glyph group at x 50–65,
  y 40–78, at most 23 levels below its background (188). Rotated 90° clockwise it
  shows six glyphs over an underline, consistent with the reading `CHaRLy`.
- **Bottom-right box:** two glyphs inside a small frame, flanked by dashes, at
  about x 1532–1556, y 1136–1151. The glyph pixels are 72–91 against a panel of
  93–113. Read `-yi-` above under LANCZOS, and like `-JR-` by the reviewer; at
  native pixels the first glyph is not resolved between J, H and I.

Neither name is in the 65-passphrase list (`pw2.txt`): `CHaRLy`, `Charly`,
`charly`, `CHARLY` and `JR` all count 0. Script:
`circled_check/oct18_measurements.py`, section D.

**[INFERRED, 26 Oct] The bottom-right box is probably a boxed "CHR" monogram.** On the
master, at 10× LANCZOS and equally at native pixels, it reads as C joined to H, then
R, between two horizontal bars and flanked by dashes; not "-yi-", which came from
the translation overlay (§7.3). C, H and R are the capitals of the top-left
`CHaRLy`, so the two marks may be one signature. As a passphrase, `CHR` is tested
on the CPU with the other name forms.

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
| the June 2020 Leopold defacement | no | delete *[superseded 18 Oct: the bust is the Dreux monument and the depicted vandalism is of 1 May 2018 (§2.16), knowable on 2020-05-10, so: **keep**]* |
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
| `-IGHT` on the BLM card | not text: flat row profile, 35 levels of contrast against 193 for the BLM capitals. *[14 October: re-measured at most 11 levels below the fill, in luminance and every channel; no coordinates were recorded here, so the 35 cannot be checked. See §6 item 6.]* *[18 Oct: "not text" withdrawn. The marks are structured dips in two groups along a 62° line (§6 item 6); whether they are text is undetermined at this resolution.]* |
| `SHT`, missing its I | `SHIT` is complete *[this row is the pedestal's spray-painted SHIT, not the faint tablet marks, and says nothing about them]* |
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

**A wrong figure in this project's own file propagates faster than the
correction chasing it, because our own files read as authoritative.** The
old-Electrum survival fraction was written `99.55%` on 4 Nov 2026 and was
correct at `99.631%` in the same session's record. On 9 Nov it was copied into
four more places — a pre-registration, §2.6, an allow-list pin and an external
review — the last of them *after* the correct value had been recomputed and
reported. Rule 10's first rule says recompute, never adopt; the hardest case is
adopting from yourself.

Three things measured when it was finally caught, each worse than the headline:

- **The visible formula did not save it.** The rule immediately above says to
  keep the expression beside the figure, and it *was* beside it the whole time:
  `(2^32 / 1626^3)^4 = 99.55%`. The expression was correct and the evaluation
  was wrong, so every reader who checked the formula saw a correct formula.
  Showing the work only helps if someone runs it.
- **The root was the cube, not the fraction.** `1626^3` was written
  `4,299,816,375`; it is `4,298,942,376`, high by `873,999`. `99.55%` is what
  that wrong cube actually yields (`99.5497%`), so the fraction was faithful to
  a bad input rather than independently miscomputed. Correcting only the
  fraction would have left the two inconsistent again.
- **One file disagreed with itself for five days.** Commit `87b5c37` wrote the
  wrong cube at §2.6 and the right fraction three lines below it. The
  contradiction sat inside a single paragraph and was read past repeatedly —
  including on 9 Nov, when the wrong value was copied into the same file 32
  lines above the correct one.

No verdict changes: the Tier-1 identity passed 66 of 66 and the figure is
descriptive, not load-bearing. A run's valid count is computed per candidate by
`mn_decode`, never from this fraction. That is the only reason this was cheap,
and it is luck rather than method — the same propagation through a load-bearing
figure is the 192,196,843,171 headline all over again.

**A standard enforced on an outside reader and suspended for ourselves is not
a standard — and it is the failure that survives every check that only looks
outward.** This is a worse shape than the wrong figure above, and it happened
in the same file, in the same session, four paragraphs apart.

On 9 Nov 2026 the external review recorded that two readers of the painted
whitepaper had named the same alterations, and refused to count two of the
agreements because the strings differed: *"a reader who writes `ABSENCE` and a
reader who writes `absent` did not transcribe the same string, even if they are
pointing at the same mark."* That is the right rule. It was applied to the 2021
reader and to nobody else.

**Four paragraphs earlier, the same file's own numerator was built by exactly
that stemming.** "Six of the ten edits are BIP39 words" was published
`[MEASURED]`. The primary source lists the painted form `abcense`, whose target
is **absence**, and a deleted **"a trusted"**, whose target is **trusted**.
Neither is a BIP39 word. `absent` and `trust` are — and they are what
`wp_bip39_baserate.py` hardcoded, in a script whose docstring called the six
"the ten whitepaper edits". Measured on exact targets the count is **four**, and
the agreement the outside reader was refused was **five of eight, exact**.

Three things make this worse than §10's other cases, and they are the reason it
is written down:

- **The rule was not forgotten. It was stated, in writing, in the same file, by
  the same hand, on the same day.** Nothing here failed from ignorance of the
  standard. The standard was being enforced outward at the moment it was being
  broken inward, which is why no review that reads only the outward-facing
  claims can catch it.
- **The primary source was on disk, and the section that said we did not have it
  cited that very file twice.** `README.md:362-363` holds all ten edits in one
  sentence. §4.3 quoted the same file at `:560` and at `:390` while stating *"We
  do not hold the other four edits"* and reasoning from their absence. Not
  having a source and not having read the source you are quoting are different
  failures, and only the second one was ours.
- **It survived two rounds of correction that were looking straight at it.** The
  figure was re-examined on 9 Nov for its base rate, and again for a second
  reader's list, and both times the numerator was carried forward untouched
  because the question being asked was always *"is six of ten significant?"* and
  never *"is it six?"* A correction that inherits the thing it is correcting is
  not a check.

The general rule, and it is harder than "recompute, never adopt": **every
standard this report applies to an outside source must be run against this
report's own numbers in the same pass.** Where a claim is refused for a reason,
that reason is a test, and the test is owed to our own figures first.

> **[WITHDRAWN 10 Nov 2026 — recorded so it is not revived from a transcript]**
> Three instructions issued to this project as **FF-1, FF-2 and FF-3**, and one
> as **CC-1(c)**, are withdrawn by their author and **must not be restated,
> reconstructed or applied**. FF was an exact test computed over the stemmed six
> with `observed = 6`; observed is **4**. Applying it would have reintroduced the
> defect this case is about, with the authority of a more precise method.
> `edit_lists_exact.py` supersedes `wp_bip39_baserate.py` in full. CC-1(c) was
> never located in any transcript and is withdrawn unexecuted. **No text of
> either is reproduced here, deliberately**: a withdrawn instruction quoted in
> full is an instruction that can be acted on by someone who reads only the
> quotation.

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

**A detection grep keyed to one producer's wording returns 0 for every other producer,
including on a real hit.** [MEASURED 2026-11-09] The standing rule for reading a solver
log was two patterns: `grep -c -E '^HIT[[:space:]]+index'` for detection and
`grep -E '^exit='` for completion. Both are `solver2_jac`'s output format and nothing
else's. Four producers in this project write logs, and three of them print something
else: `brain_image_corpus.py:471-475` emits `*** n HIT ***` and `commit=<sha256>`;
`old_electrum.py` and `t12_family_check.py` have formats of their own; and
`brain_image_corpus.py` run directly prints no `exit=` line at all, because `exit=` comes
from the `run_queue_*.sh` wrappers. So the detection grep returned a clean **0** on
`image_corpus_run.log` — and would have returned the same 0 with a hit sitting in it. This
is §1.7, §1.8 and §1.9's class in its worst form: **a check that printed a number nobody
made it earn**, and the number was the one the hit protocol depends on. The rule is now
format-agnostic — `grep -c -i -w -E 'hit|hits|commit=|phrase[[:space:]]*:'` for detection,
`grep -E '^exit=|acceptance|NO MATCH|VOID'` for completion — and the word anchors are
themselves measured: unanchored, `HIT` is a substring of `SHIT` and `whitepaper`, which
fires on 5 lines across two logs that contain no hit, while anchored it fires on nothing
except the three planted self-test logs, where it fires twice each. **A rule that cries
wolf on the word "whitepaper" gets ignored, which is the same failure in the opposite
direction.** A control must be quiet where it should be *and* loud where it should be;
quiet alone is what a producer-specific grep gives you for free.

**Never edit by slicing between two distant anchors.** On 2026-10-13 one
paragraph of §3 was replaced with `s[:i] + new + s[j:]`, where `i` and `j` were
two headings 92 lines apart. The intent was to replace the paragraph at `i`.
Everything between them went with it: the **target-bytes verification** — the
check an outside researcher's disclosure prompted, and the strongest statement
in this document — its swapped-target control, the key-format controls with
their 29-against-13 table, and the line establishing that a miscount cannot
swallow a hit. The commit message described only the paragraph it meant to
replace.

The loss went unnoticed for three further commits. It surfaced only because a
later edit anchored on a sentence inside the deleted region and failed to find
it — the edit's own assertion caught what review had not. Restored verbatim from
`1cfc3a3`, after confirming that none of the four headings already existed, so
nothing was duplicated, and that the one paragraph that *was* meant to go stayed
gone.

Two rules came out of it. Replace exact text, never a span between anchors,
because an exact-match replacement fails loudly when the target is not where it
is expected, while a slice succeeds silently on whatever lies in the gap. And
diff the set of section headings across every commit, which is cheap and found
this immediately once it was run: a heading that vanishes without being
replaced is a deletion nobody intended.

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

**Six rules, each learned by getting it wrong first:**

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

- **A glyph-sized-component scan is not evidence of text until the run count holds
  across a threshold sweep.** Filtering an image for components the size of a letter
  returns letter-sized components from any textured region, and a list of them looks
  exactly like a transcription waiting to happen. On 9 Nov a left-edge band was
  reported as "a second rune column, 29 glyph-sized runs" and written into
  `census_crops.DRAWN` on that basis. It is not text: sweep the threshold and the run
  count goes 48, 44, 24, 2, 1 at ink < 130/150/180/200/215, pitch 23.7 px/run to 1,200,
  while the real column next to it holds 49, 50, 49, 38, 25 at pitch 19.9 to 39.2.
  Real text on paper survives a 50-level sweep; gaps in artwork do not. The cheap
  discriminators, in order: does the band have **paper** (10.2% of pixels above 200
  there, 57.2% in the real column), does it have a **margin** (none; the real column
  has 32 blank columns beside it), and does the **run count hold**. The wrong entry
  stood for one commit. The scan that produced it was mine, and it agreed with what
  the census said should be there — which is rule one.

  **The same rule applied one level up, and the result is worse.** The question
  "where is this block?" was never asked of two of the three rune blocks until
  9 Nov 2026 — and the arithmetic that places **three slots of the template** rests on
  one of them. Slots **3** (`tower`), **13** (`moon`) and **21** (blank) are produced
  by *adding* the numerals each clock hand falls between, and the only thing licensing
  that addition is block B's caption `Сумма двух чисел`, whose 14 glyphs have no
  measured location. The hand directions are measured; the addition is adopted from
  `u/Amadeus407`'s 2021 reading of a block this project has never found. **The report
  must say so wherever 3, 13 and 21 appear**, and now does: §2.17's clock rows and its
  scope note, §7's hand table, §7's clock paragraph, and the open-question list. The
  general form of the rule: a transcription with no measured location is somebody
  else's measurement, and anything derived from it inherits that status no matter how
  many of this project's own measurements sit downstream of it.

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
