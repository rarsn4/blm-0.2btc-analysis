# Image-measurement scripts: transfer bundle

The bundle is self-contained: the puzzle image ships inside it. Every reference output in `expected_output/` can be regenerated from a fresh extraction, with no other files and no environment variables.

To verify, then apply to a git checkout:

```
cd repo_transfer
sha256sum -c MANIFEST.sha256
bash apply_bundle.sh /path/to/repo            # dry run: checks conflicts, copies, stages
bash apply_bundle.sh /path/to/repo --commit   # the same, then commits; it never pushes
```

`apply_bundle.sh` stops without copying anything if a file of the same name already exists in the repo with different content.

## Setup

**The image is included as `0.2-btc-puzzle.png`.**
- 2,383,395 bytes, md5 `7710323461a924987eb35c77055e59f6`, sha256 `d0b04378f75d63997b8034ec2ef1bdd108178e4546de78237bd35abf4189a782`.
- It is **byte-identical** to the original poster's upload, `https://i.redd.it/n1x7g8ceaur51.png`: Reddit post `j79zvj` by u/stsh_n, 2020-10-08 (compared 2026-09-28).
- An outside re-run can download that URL and check the hash, rather than trusting this copy.
- `imgio.py` finds the image next to the scripts. Set `BLM_IMAGE` to use a copy elsewhere. Any file whose md5 differs is refused.

The scripts need numpy and Pillow. `slogan_lines.py` also needs `mnemonic`. Run everything with `PYTHONDONTWRITEBYTECODE=1`.

## Files

| file | backs | run | notes |
|---|---|---|---|
| `0.2-btc-puzzle.png` | all | — | The puzzle image, byte-identical to the OP's upload (see Setup). |
| `imgio.py` | — | — | Shared loader. It finds the image and enforces the md5 check. |
| `runelib.py` | §A | — | Rune-column segmentation and mask IoU. It is imported by `t4_ctrl.py`. |
| `t4_ctrl.py` | §A | `python t4_ctrl.py` | Terminal glyph: segmentation, native size and contrast, template tails, and the wrong-direction control. |
| `t2_cov.py` | §B | `python t2_cov.py` | Circled mark on the BLM card: circle fit, peak stroke coverage, and the STOP-emblem comparison. |
| `t3_lines.py` | §C | `python t3_lines.py` | Thin-line detector over the amendment block. |
| `t3_census.py` | §C | `python t3_census.py` | The `subject` profile against its controls, and the per-word census. |
| `census_crops.py` | §D | `python census_crops.py` | Regenerates the 26 views the letter-substitution census was judged from, into `./census_crops/`. |
| `seal_ring.py` | §E | `python seal_ring.py` | Seal ring fit, unwrap, word blocks and both failed instruments. It writes `seal_ring_strip.png`. |
| `slot20.py` | §G | `python slot20.py` | Wreath plaque strokes; X-mark geometry swept over thresholds; spacing against 7 verified sets of the artist's lettering and numerals. It writes `slot20_segmentation.png`. |
| `even_slot_rules.py` | §H | `python even_slot_rules.py` | 12 candidate numbering rules applied to the whole picture, 0 of which pass. Also measures the rifle's illegible receiver mark. |
| `r10_layout.py` + `r10_elements.json` | §I | `python r10_layout.py` | The pre-registered dial-layout test. It refuses to run if `r10_elements.json` differs from its pre-registered sha256 (`3634036d…`). |
| `r10_erratum.md` + `r10_erratum_check.py` | §I | `python r10_erratum_check.py` | The E24 box error found after scoring, and the post-hoc re-score. Does not change the primary result. |
| `STOP_R10_SET_C.md` | §I | — | Stop rule: R10 set C is closed, and any future dial-layout test needs a fresh pre-registration. |
| `chronology.py` | premise audit | `python chronology.py` (add `--onchain` to re-fetch the funding tx) | The hoodie date's contrast; the gold chart's gridlines, its 2011 peak and its endpoint. |
| `idiom_ink.py` | idiom question | `python idiom_ink.py` | Whether `чёрный день` is set apart in the ink, across all three inscriptions. |
| `wallet_defaults.md` | prior on length | — | Default mnemonic length of every legacy-by-default wallet in the 2020-05-29 walletsrecovery snapshot, each pinned to a source line. |
| `premise_audit.md` | — | — | Premise audit, tasks A–D, with a provenance tag on every claim. |
| `slogan_lines.py` | §9 | `python slogan_lines.py` | Unchanged; sha256 `9d4f903b…99ee1e`, as previously recorded. |
| `report_additions_image_pass.md` | — | — | Text for REPORT.md, sections A–I. §A amends §6 item 5 and §H amends §2.17. |
| `apply_bundle.sh` | — | see top | Verifies the bundle, checks for conflicts, copies and stages. Commits only with `--commit`, and never pushes. |
| `expected_output/` | — | — | Reference stdout for each script, plus `seal_ring_strip.png` and `slot20_segmentation.png`. |

## Verification

The bundle ships no bytecode: `__pycache__/` and `*.pyc` are excluded at build time, because they are timestamp-based and could never verify on another machine.

To regenerate every reference output from a fresh extraction:

```
export PYTHONDONTWRITEBYTECODE=1
for s in t4_ctrl t2_cov t3_lines t3_census seal_ring slot20 chronology idiom_ink even_slot_rules r10_layout r10_erratum_check slogan_lines census_crops; do
  python $s.py | diff - expected_output/$s.txt && echo "$s OK"
done
```

A difference in the last digit of a percentile is worth reporting, not ignoring.

The reference `.txt` files use LF line endings. Compare the PNGs by their pixels, not their bytes: PNG compression can differ between zlib and Pillow builds even when the pixels are identical.

This was verified on Windows from a fresh extraction of the zip, with no `BLM_IMAGE` set, on Python 3.12.10, numpy 2.5.3 and Pillow 12.3.0. All 13 reproduced exactly.

## Provenance

Most of these scripts consolidate code that existed only in a scratchpad on the Windows machine. A few numbers in the 27 Sep reply were produced by one-off inline code and are now reproduced here. Two of them changed when re-measured properly:

- The BLM-card circle is **17.5 px** across (fitted), not "about 20".
- The STOP emblem at that size keeps **74** dark pixels, not "about 100".

Neither change affects a conclusion.
