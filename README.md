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

Requires [CUDACyclone](https://github.com/Dookoo2/CUDACyclone) for the secp256k1
backend — clone it alongside `solver/` as `CUDACyclone-main`. Also needs the
BIP39 English wordlist as `bip39_en.txt`:

    python3 -c "from mnemonic import Mnemonic; open('bip39_en.txt','w').write(chr(10).join(Mnemonic('english').wordlist))"

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

## Contact

Questions, corrections, or a higher-resolution source image:
**goldenwhales699@gmail.com** — or open an issue on this repo.

I can test a corrected word list or template in seconds, so if you have a
reading I don't, it costs nothing to check.

## Support

If this saved you time, or the 24-word pre-hashing warning caught a bug in your
own solver:

- **BTC:** `bc1qtuqm6xvpkhp0zdkj0pmat94lj4kl4whqjqz7p0`
- **ETH:** `0x7fB09415a4BDf6788949D524EE66b610A6A7fC0A`

Entirely optional. The findings and the solver are public either way.
