# 0.2 BTC "BLM" Puzzle — analysis

Target: [`1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`](https://blockchair.com/bitcoin/address/1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ) · still unsolved.

**[Full writeup → REPORT.md](REPORT.md)**

## Headlines

- **The rune cipher is solved.** It is monoalphabetic substitution over
  **Cyrillic**, not Greek. The circulating "HELLO : FROM : THEM" reading is
  internally impossible — it maps Φ to both H and M. Alphabet mapped across all
  four inscriptions; the repo's Russian decode confirmed independently by
  glyph-shape correlation (+0.63 same-letter vs +0.07 different).

  `Сумма двух чисел  =  ◇⏶ᛗᛗ△ : ⇧⧗⏶⤬ : ⊤Ψ◇⫽ᛉ`

- **12,073,043,767 seed derivations eliminated** across BIP39 *and* Electrum —
  349 CPU-days at typical solver rates. Electrum had never been tested by
  anyone; lengths 13/14/16/17 are illegal under BIP39 and were unreachable.

- **Four defects in the community candidate data**, including that `breathe`
  is not a BIP39 word.

- **A silent-failure trap that breaks custom 24-word solvers** — see §1.4.
  If you wrote your own, check it before trusting any 24-word negative.

## Layout

    REPORT.md    findings, scope of every elimination, method
    solver/      CUDA solver + config generators
    configs/     every hypothesis tested, as a config file

## Reproducing

    nvcc -O3 -arch=sm_89 -I CUDACyclone-main -Xptxas -v solver2.cu -o solver2
    ./solver2 --selftest                 # both canonical BIP39 addresses
    ./solver2 --config ../configs/t18_pool52.conf

Every stage validated against independently computed exact values. `--selftest`
reproduces the canonical 12-word and 24-word addresses through the full
pipeline — if it passes, the negatives are trustworthy.

## The open question

The right-hand inscription ends `… чёрный день номер X`. That final glyph is
complete, untruncated, carries no titlo, matches nothing in a 68-glyph corpus,
and does not match the artist's own hand-drawn digits. **If you have a
higher-resolution source where it is legible, that is the most valuable file in
this puzzle.**
