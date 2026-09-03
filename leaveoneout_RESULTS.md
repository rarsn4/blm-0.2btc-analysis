# Leave-one-out, closed properly — 2026-09-02

## The gap

`REPORT.md` §2 claims, under **[EXHAUSTED]**:

> leave-one-out over the entire 2048-word dictionary at each gap

The configs that did this — `t18_full{6,8,14,15,18}.conf` — do sweep one gap over
all 2048 words. But each one:

- runs the other four gaps over the **old 37-word pool**, not the current 54-word
  README pool, and
- carries **no `PATH` lines at all**, so it ran the single default
  `m/44'/0'/0'/0/0` rather than the four paths every later config uses.

Audited across every `.conf` in the directory: **no config combined `@FULL` with a
pool ≥52 or with 4 paths.** So two regions had never been tested:

1. one gap free over 2048 while another gap draws one of the 17 words added
   since: `able cause crime exist happy know neither only party peace place that
   they thing time any verb`
2. the entire leave-one-out family on paths 2–4

That is precisely where a word outside every pool survives. `flag`, `banner`,
`nation`, `state`, `eagle`, `field`, `glory`, `salute` are all BIP39 and none has
ever appeared in a gap pool — an `@FULL` sweep was the only thing that could
reach them, and the `@FULL` sweeps were the weak ones.

## The runs

`t18_loo{6,8,14,15,18}.conf` — one gap over all 2048, the other four over the
54-word pool, all four paths. 17,414,258,688 candidates each.

| sweep | survivors | deviation | | wall |
|---|---|---|---|---|
| `loo6` | 272,071,961 | −25,831 | −1.58 σ | 2h35m36s |
| `loo8` | 272,088,758 | −9,034 | −0.55 σ | 2h35m27s |
| `loo14` | 272,108,206 | +10,414 | +0.64 σ | 2h32m11s |
| `loo15` | 272,101,787 | +3,995 | +0.24 σ | 2h29m33s |
| `loo18` | 272,097,792 | **0** | **exact** | 2h28m56s |

**All five: exhausted, no match.**

Totals: **87,071,293,440 candidates, 1,360,468,504 derivations, 12.7 h GPU**
at ~29,100 derivations/s with 4 paths.

## `loo18` is an exact-value control, and it was free

The other four survivor counts are binomial around 272,097,792 with σ = 16,366,
and all sit inside ±1.6 σ. `loo18` is **not** binomial — it is deterministic, and
it landed exactly.

An 18-word phrase is 198 bits: 192 entropy + 6 checksum. Slot 18 carries the last
5 entropy bits **and all 6 checksum bits**. So for any fixed slots 1–17, exactly
2⁵ = 32 of the 2048 candidate words pass the checksum — never 31, never 33.

    predicted   54^4 × 32  =  8,503,056 × 32  =  272,097,792
    observed                                  =  272,097,792

This is the exact-count validation rule 3 asks for, at production scale, obtained
without designing a control for it. It confirms the checksum path end to end: the
11-bit packing, the entropy/checksum split at 18 words, and the survivor
accounting across all 10 chunks. Worth adding to §10 beside `selftest_find` — and
it generalises: **whenever the `@FULL` slot is the LAST word of the phrase, the
survivor count is exactly `(product of other radices) × 2^(11 − words/3)`.** Any
deviation is a bug, with no statistical wiggle room to hide in.

## What this settles

The `[EXHAUSTED]` leave-one-out claim is now **earned at all five t18 gaps** —
every BIP39 word at every gap, against the current pool, on all four paths. It
was previously true only under the 37-word pool on one path.

It also kills the hypothesis these were launched for. The flag carries **44
stars**, six short of 50 (verified by connected-component count inside the
canton, every star visually confirmed, two clipped at the fold; stripes are the
canonical 13). If slot 6 came from that six-star deficit, its word would be
flag-related — and `flag`, `banner`, `nation`, `state`, `eagle`, `field`,
`glory`, `salute` are now all eliminated at slot 6, along with the other 2040.
The deficit may still be the right *mechanism* for the number 6; the word it
implies is not at slot 6 in an 18-word phrase.

## Note for §3

These 1,360,468,504 derivations are ordinary BIP39 seed derivations and **do**
belong in the §3 tally, unlike the brainwallet figures. But check for overlap
before adding: the region where the `@FULL` slot happens to take a value already
in the 54-word pool duplicates `t18_readme54.conf`. That overlap is
5 × 54⁵/64 = 35,429,400 derivations, about 2.6% of the total.
