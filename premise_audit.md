# Premise audit — 28 Sep 2026

Every claim below carries one of four provenance tags:

- **AUTHOR**: the posting account, or text inside the artwork itself
- **COMMUNITY**: solvers
- **MEASURED**: from the image or the chain, reproducible by `chronology.py` or another script in this bundle
- **SOURCE**: a program's own source code, at the version current in May 2020

---

## Chronology anchor

| fact | tag | evidence |
|---|---|---|
| 0.2 BTC arrived in tx `fcee21d4…d043`, block 629754, **2020-05-10 08:01:46 UTC** (an earlier note said 10:01; that was a UTC+2 display) | MEASURED | mempool.space API |
| The address has 5 funding transactions and 0 spends. Balance 20,107,284 sat. The 0.2 BTC is the first funding; four later deposits (2023–25) came from third parties. | MEASURED | mempool.space API |
| The artwork contains **05.25.20**: x992–1069 y370–388, ink median 43 on a background of 121, **78 levels of contrast** | MEASURED | `chronology.py` §1 |
| The **gold chart's series ends at about $1,970, above its own drawn 2011 peak (~$1,808)** by 20 px. Gold first exceeded its 2011 high in July 2020, so the chart's data runs to **July 2020 or later**. | MEASURED, plus an external price fact | `chronology.py` §2; [goldnews, 10 Jul 2020](https://goldnews.substack.com/p/gold-news-10-july-2020), [17 Jul 2020](https://goldnews.substack.com/p/gold-news-17-july-2020) |

So the seed and the passphrase existed by 2020-05-10, and the artwork's content was made **July 2020 or later**. It was posted on 2020-10-08.

---

## A — Versions

| version | tag | first posted (UTC) | relation to our file |
|---|---|---|---|
| Reddit `j79zvj` by u/stsh_n, "Bitcoin puzzle (2000$)", on the account's own profile, image `n1x7g8ceaur51.png` | AUTHOR | **2020-10-08 09:25** | **byte-identical** (md5 `7710323…`) |
| Reddit `jrr7mo` by u/fijiMath, r/bitcoinpuzzles | COMMUNITY | 2020-11-10 19:06 | byte-identical |
| Reddit `mbdogq` by u/DiOnline, r/CryptoPuzzlers | COMMUNITY | 2021-03-23 12:32 | pixel-identical; re-encoded with the sRGB chunk stripped |
| BitcoinTalk mention in topic 1306983 (msg 55361483) | COMMUNITY | December 2020, per dkbit98 | not opened in this pass |
| BitcoinTalk topic 5404767, opened by Minase ("Yesterday i found this puzzle") | COMMUNITY | 2022-07-01 | links the HomelessPhD repo |
| privatekeys.pw | COMMUNITY | "Start Date: 2020-05-10" is the **funding** date, not a posting date | — |
| Wayback Machine | — | earliest captures: post 2021-06-13, image 2023-06-20, profile 2025-03-27 | — |

Submission records come from PullPush (Reddit itself returns 403 to scripts).

**No version predates 2020-10-08. A.3, diffing against an earlier version, stops here: there is nothing to diff.**

---

## B — Statements by the author

- **The posting account is a single-use throwaway.** Its `dateCreated` is 2020-10-08 09:21:42 UTC, **3 min 48 s before the post** (from the schema.org record in the archived profile). The profile has 1 post, 1 post karma and 0 comment karma.
- **The post has no text and was never edited** (`edited=False`).
- **The author made 0 of the 273 archived comments in the thread.** 33 comments are deleted with no text surviving.
- Solvers report the same: "He posted and left. Seems to be keen on anonymity" (DiOnline, 2021-02-01, `glm7ize`). DiOnline says they contacted the OP, and reports no disclosure (`gpaw1ca`).
- **Wall:** the account's history beyond that snapshot could not be queried. PullPush rate-limited every author query (429). Also, 0 comment karma does not prove there are zero comments.

So the only AUTHOR statements that exist are the title **"Bitcoin puzzle (2000$)"** and the text inside the artwork. The artwork says **"FIND THE SEED PHRASE IN THE THIS PICTURE"**: a seed phrase, not a passphrase. Nothing from the author addresses word count, wallet or language.

**Every hint traces to COMMUNITY comments:**

| hint | first stated by | date | comment id |
|---|---|---|---|
| moon, tower, real, subject | u/boriserd | 2020-10-12 | `g8lip0e` |
| Tuesday | u/hmm_dimasiki | 2021-01-10 | `gipljed` |
| "24 identifiable elements" | u/DiOnline | 2021-01-20 | `gjyhtie` |
| food | u/meserit | 2021-01-31 | `glilhuv` |
| breathe; subject "underlined" | u/Accomplished_Weird36 | 2021-02-02 | `glrgy6c`, `glrg4tw` |

privatekeys.pw's hint list is word-for-word Minase's BitcoinTalk post, which is tagged "(source reddit)". Its wording is inferential ("which likely means 'Real' is a seed word").

Not pursued, because it would identify a person: the README's leads to an Instagram artist and to a Wikipedia editor.

---

## C — How the address was made (software class only)

**Sender's transaction, MEASURED:**
- version 1, locktime 0, every sequence 0xffffffff
- 4 P2SH-P2WPKH inputs, a P2SH change output, 0.2 BTC to P2PKH
- fee **3.03 sat/vB, the lowest in its block** (block median 65)

**Bitcoin Core v0.19.1** (released 2020-03-09) and **Electrum 3.3.8** (released 2019-07-11), both current in May 2020, **never emit sequence 0xffffffff**:
- Core: `wallet.cpp:3251` uses 0xfffffffd or 0xfffffffe.
- Electrum: `transaction.py:945–951` uses `0xffffffff - (2 if rbf else 1)`.

(SOURCE) This, not locktime, is what excludes them. **Both set locktime 0 when not synced**: Electrum's `wallet.py:157` says "if no network or not up to date, just set locktime to zero", and Core's `wallet.cpp:2916` has the equivalent.

**Personal or custodial.** [INFERRED, moderate confidence] **Personal self-custody.** Three of the four inputs came from batched payouts (38, 47 and 62 outputs) and were held 10–17 months. They were spent as an exact-amount payment with change, at a bottom-of-market fee. The analysis stopped at the inputs' parents; the change output was not followed.

**"The author chose legacy on purpose" is not established.** The receiving wallet is independent of the sending wallet, and legacy was the default of common tools:

| tool (May 2020) | legacy `1…` by default? | default path | default words | source |
|---|---|---|---|---|
| iancoleman BIP39 (commit `115eb45`, 2020-05-08) | **yes**: the BIP44 tab is the default | m/44'/0'/0'/0/0 | **15** (options 3–24; 21 is available but not the default) | SOURCE `src/index.html` |
| Electrum 3.3.8 "standard" | no: the seed menu lists Segwit first and Legacy second | m/0/n | 12, **Electrum format, not BIP39** | SOURCE `base_wizard.py:609–616`, `mnemonic.py:163` |
| Blockchain.com | yes: its only path | m/44'/0'/n' | not verified here | walletsrecovery.org at `80436a2b98`, 2020-05-29 |
| BRD | yes: its only path | m/0' | not verified here | same |
| Jaxx Liberty | yes: its only path | m/44'/0'/0' | not verified here | same |
| Exodus | optional | m/44' \| m/84' | not verified | same |
| Ledger Live, Trezor web wallet | optional | m/44' \| m/49' | not verified | same (the table lists supported paths, not defaults) |

---

## D — Premise ledger for the 21-slot template

**On the chronology rule.** Post-May-25 content can *encode* a word but cannot *source* it. So **no assignment is falsified by being dated POST**. The rule only kills justifications of the form "the author chose word W because of E", and passphrases containing a fact that could not be known on 2020-05-10.

**Correction to the deletion rule.** The rule should delete candidates containing a fact **unknowable** on 2020-05-10, not any post-May-10 date:

| date or fact | knowable on 2020-05-10? | verdict |
|---|---|---|
| 05.25.20 | no | delete |
| gold above $1,800 | no (July 2020) | delete |
| the June 2020 Leopold defacement | no | delete |
| 11.03.20 | yes: the election date is fixed by statute, and the Trump–Biden match-up was set in April 2020 | keep |
| "Tuesday" | yes | keep |
| "I can't breathe", "No justice no peace" | yes: slogans from 2013–14 | keep |

The project's passphrase list is not on this machine, so the rule has not been applied to it here.

**The premises.** Each word has two provenance links: where the *word* comes from and where the *slot number* comes from. Tags are in brackets.

| slot | word | word from | slot number from | element dated |
|---|---|---|---|---|
| 1 | subject | written in the amendment copy; **underlined** [MEASURED, 1 of 25 checkable words] | "Section 1" heading [COMMUNITY] | POST (Leopold pedestal scene, June 2020) |
| 2 | camera | depicted, 2 cameras [MEASURED] | count [COMMUNITY] | UNDATED |
| 3 | tower | written on a clock hand [MEASURED] | clock sum 1+2 [MEASURED geometry + AUTHOR rune "сумма двух чисел"] | UNDATED |
| 4 | mask | depicted, 4 masks [MEASURED] | count [COMMUNITY] | PRE (COVID era) |
| 5 | police | written, END POLICE BRUTALITY | "line five" [COMMUNITY; a convention used nowhere else] | POST (Floyd block) |
| 7 | liberty | named (the statue) [COMMUNITY] | 7 crown spikes [5 MEASURED, 2 inferred] | UNDATED |
| 9 | eye | depicted | "4+5" [COMMUNITY, not measured] | UNDATED |
| 10 | black | written (rune plaintext; BLACK LIVES MATTER) | "номер X": **no derivation**; X is a hapax [MEASURED] | UNDATED |
| 11 | pyramid | depicted | "5+6" [COMMUNITY, not measured] | UNDATED |
| 12 | vote | **association** from .VS. [COMMUNITY] | .VS. flipped vertically reads "·12·" [MEASURED] | PRE-knowable |
| 13 | moon | written on a clock hand [MEASURED] | clock sum 12+1 [MEASURED] | UNDATED |
| 16 | rifle | depicted, 1 [MEASURED] | "M16" model identification [COMMUNITY] | UNDATED |
| 17 | gold | **inferred** chart subject; not written, metal not depicted [COMMUNITY] | "17 years", a span checked against TradingView [COMMUNITY] | **POST (July 2020 or later) [MEASURED]** |
| 19 | glove | depicted (a hand holding the vial) [COMMUNITY] | "CVD19" label [text MEASURED] | PRE-knowable |
| 20 | — | **no README value**: the table gives `apple` with no derivation; §19 gives `second` by an excluded lookup, and its XX = 20 step conflicts with the spacing measurement (0 of 33) | — | POST scene (Leopold) |
| 6, 8, 14, 15, 18, 21 | gaps | — | slot 21's hand carries no word [MEASURED] | — |

**Word count.**
- MEASURED: slot 21 exists, so the phrase has **at least 21 words**.
- INFERRED: exactly 21. 24 fits the measurement equally well.
- The README does **not** assert 21: it lists lengths 3–24, and its table has 24 rows.

**Slot-numbering mechanism.**
- Only the clock sums are anchored by the author, through the rune "sum of two numbers".
- All other slot numbers come from heterogeneous COMMUNITY conventions: counts, labels, spans and model numbers.

### The weakest five premises

1. **Slot 20.** There is no value to be right about.
2. **gold @ 17.** Both links are inferred.
3. **black @ 10.** The slot has zero derivation. This is what free10 and the relocation run address.
4. **vote @ 12.** The word is pure association, although the slot is measured.
5. **police @ 5.** Its slot convention is unique in the table.

**Template-level flag:** exactly 21 words. If it is wrong, "a + g ≥ 2" is undefined. That deduction also holds only given the other fixed premises: path, empty passphrase, English wordlist, and one reading of slot 20.
