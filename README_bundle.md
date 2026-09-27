# Image-measurement scripts: transfer bundle

Copy these files into the project root and commit them. Then check them on the Linux side with:

```
sha256sum -c MANIFEST.sha256
```

## Setup

The scripts need the puzzle image. Either put `0.2-btc-puzzle.png` in the project root, or set `BLM_IMAGE`.

The image's md5 is checked, and any other file is refused: `7710323461a924987eb35c77055e59f6`.

They need numpy and Pillow. `slogan_lines.py` also needs `mnemonic`.

## Files

| file | backs | run | notes |
|---|---|---|---|
| `imgio.py` | — | — | Shared loader. It finds the image and enforces the md5 check. |
| `runelib.py` | §A | — | Rune-column segmentation and mask IoU. It is imported by `t4_ctrl.py`. |
| `t4_ctrl.py` | §A | `python t4_ctrl.py` | Terminal glyph: segmentation, native size and contrast, template tails, and the wrong-direction control. |
| `t2_cov.py` | §B | `python t2_cov.py` | Circled mark on the BLM card: circle fit, peak stroke coverage, and the STOP-emblem comparison. |
| `t3_lines.py` | §C | `python t3_lines.py` | Thin-line detector over the amendment block. |
| `t3_census.py` | §C | `python t3_census.py` | The `subject` profile against its controls, and the per-word census. |
| `census_crops.py` | §D | `python census_crops.py` | Regenerates the 26 views the letter-substitution census was judged from, into `./census_crops/`. |
| `seal_ring.py` | §E | `python seal_ring.py` | Seal ring fit, unwrap, word blocks and both failed instruments. It writes `seal_ring_strip.png`. |
| `slogan_lines.py` | §9 | `python slogan_lines.py` | Unchanged; sha256 `9d4f903b…99ee1e`, as previously recorded. |
| `report_additions_image_pass.md` | — | — | Text for REPORT.md, sections A–F. |
| `expected_output/` | — | — | Reference stdout for each script, plus `seal_ring_strip.png`. |

## Verification

Every script was run on Windows from a directory containing only these files, with `BLM_IMAGE` set:

- Python 3.12.10, numpy 2.5.3, Pillow 12.3.0
- all exit 0 with empty stderr
- each finishes in under 3 s

To compare on Linux:

```
for s in t4_ctrl t2_cov t3_lines t3_census seal_ring slogan_lines census_crops; do
  python $s.py | diff - expected_output/$s.txt && echo "$s OK"
done
```

A difference in the last digit of a percentile is worth reporting, not ignoring.

The reference `.txt` files use LF line endings. Compare `seal_ring_strip.png` by its pixels, not its bytes: PNG compression can differ between zlib and Pillow builds even when the pixels are identical.

## Provenance

Seven of the scripts consolidate code that existed only in a scratchpad on the Windows machine. A few numbers in the 27 Sep reply were produced by one-off inline code and are now reproduced here. Two of them changed when re-measured properly:

- The BLM-card circle is **17.5 px** across (fitted), not "about 20".
- The STOP emblem at that size keeps **74** dark pixels, not "about 100".

Neither change affects a conclusion.
