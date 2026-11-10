# LL-2 pre-registration — the canvas's own vocabulary against the two ledgers

Written and committed **before** any membership was computed for the census.
Brief LL-2, 10 Nov 2026. Direction is fixed by the brief and is not ours to choose.

## 0. Word consequences, fixed first

**No word enters any config from this measurement, under any outcome.** LL-5 settles
that independently: the old-Electrum path measures 1.507 candidates/s and one fixed
12-word set over all orderings is 1,840 CPU-days, which is not authorised and is not
queued. A vocabulary result cannot change that arithmetic, so it cannot license a run.
If the test comes back positive, the only thing it licenses is a search for an **order
constraint**, pre-registered before it is applied.

## 1. Hypothesis and direction

H1: the words painted on the canvas are **enriched in OLD-ELECTRUM-ONLY words**
relative to the base rate for English words of the same lengths.

H0: they are not — the canvas's split is what any English text of that length mix gives.

## 2. What counts as a census word

From `word_census.tsv`, 151 rows: `A_display` 110, `B_microtext` 41.

**Excluded, with reasons fixed now:**

- **14 Cyrillic tokens** (`я на будут присылать биткоины зашифрованы здесь номер
  сумма чисел чёрный двух день надеюсь`) — not English; neither ledger is a Russian
  list. Recorded with their ellipses elsewhere; not completed here.
- **Latin tokens** (`esse quam dixit ollae rerum causas mundus pereat caccabus
  justitia cognoscere niger`) — not English. `niger` is Latin in context (the motto),
  not the English-looking string.
- **Line-wrap fragments** of the micro-text (`ral spen ding tion thority transac re`)
  — not words. They are halves of *several/spending/-tion/authority/transaction*
  produced by the painted line breaks.
- **Acronyms** `blm cvd sic`.
- **The misspelling** `introdue` — one of the ten whitepaper edits, not a word.
- **Length 1-2** (`a i as es et in is no or to us vs at au it of`) — **structurally
  impossible in both ledgers**: old Electrum is 3-12 letters, BIP39 is 3-8. Keeping
  them would pad NEITHER with free hits, the mirror of the HH-2 defect.

Membership is by **exact token**, no stemming. The `bip39` column of the census is
not trusted; membership is recomputed from `configs/bip39_en.txt` and
`configs/electrum_old_en.txt` (LL-1 verified the latter against the `_words` tuple:
1626 words, identical in order, md5 of the file `33f89ca84f7c9b3eeec1bcc253bce673`).

## 3. The structural asymmetry, stated before measuring

**Old Electrum has 80 words of 9-12 letters; BIP39 has none.** Per length, old-only
share of the old list: 3→50.0% 4→43.6% 5→38.9% 6→39.0% 7→50.0% 8→71.9% and
**9-12→100%**. So every census word of 9+ letters that is in the old list is
"old-Electrum-only" with **no possibility of being BOTH**.

Therefore the comparative test runs on the **length 3-8 stratum only**, where both
ledgers are populated. Words of 9-12 letters are counted and reported separately and
are **not** evidence of enrichment.

## 4. Primary test and its null

Primary stratum: **`A_display`, English, length 3-8.** `B_microtext` is excluded from
the primary test for a reason that is fatal and specific: **B is whitepaper text, and
the control corpus below is the whitepaper.** B's split estimates the whitepaper's own
vocabulary, not the canvas's choices. B is reported descriptively only. The census
header already warns B is a sample, not a census.

**No English frequency list is on this disk** — no `wordfreq`, no `nltk`, no unigram
counts. The brief's design cannot be run as specified. Substitutes, both fixed now,
primary named first:

1. **PRIMARY — frequency-weighted English prose control:** `bitcoin.txt` on disk
   (3,571 tokens), tokenised and classified by the rules in §2. Per-length
   P(old-only) is estimated from its **token** occurrences, so the null is
   frequency-weighted, which is what the brief asks for. It is an independent English
   sample of neutral theme.
2. **SECONDARY — union draw:** P(old-only | in at least one ledger), per length.
   Neutralises "is it a common word at all" and asks only whether, among wallet
   vocabulary, the canvas tilts old.
3. **SENSITIVITY ONLY — type dictionary:** `/usr/share/dict/american-english`,
   per-length. Recorded in advance as **expected to overstate**: it is a list of
   dictionary types, dense in rare and inflected forms, while the canvas's words are
   common ones. A positive here alone means nothing.

Test: **exact Poisson-binomial** by convolution over per-token, length-conditioned
probabilities — the same standard as `edit_lists_exact.py`. No normal approximation,
no comparison of a raw percentage to a range.

## 5. The confound that outranks the result

**The old-Electrum list IS a frequency list** — its own source comment reads
"list of words from http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/
Contemporary_poetry". Membership in it is therefore a proxy for *"common word in
contemporary poetry"*. BIP39 by contrast is curated to be neutral and concrete.
So any emotionally loaded English text will show old-Electrum-only enrichment, and
that is a property of the two lists, not a fact about this canvas. The census test is
the right instrument precisely because the census is **not** anyone's thematic
selection — but even a positive result carries this confound and must say so.

## 6. Decision rule, fixed before the numbers

Let X be the count of old-Electrum-only words in the primary stratum.

- **REFUTED** if P(X ≥ observed) **> 0.5** under the primary null — the canvas is at
  or below what ordinary English prose gives.
- **SUPPORTED** only if P(X ≥ observed) **< 0.05** under the primary null **and** the
  direction is the same under the secondary union null. Both, not either.
- **NO RESULT** otherwise, including whenever the three nulls disagree in direction.

Published either way, under §0. A null is not a disappointment here; it closes a path.
