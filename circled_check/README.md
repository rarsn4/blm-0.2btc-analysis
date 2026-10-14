# Circled-mark check: the BLM card

Source of coordinates: REPORT.md §6 item 6. Circle fit centre (263.5, 760.5),
diameter 17.5 px, interior mark 13×10 px. The mark sits on the tablet held by
the Statue of Liberty, below the word `BLM`.

## Crops (from `0.2-btc-puzzle.png`, sha256 d0b04378…4189a782)

Crop box, master pixels: **left 242, top 704, right 314, bottom 812**
(right/bottom exclusive), i.e. columns 242–313, rows 704–811, 72 × 108 px.
Circle centre in crop coordinates: (21.5, 56.5).

| file | size | sha256 |
|---|---|---|
| `blm_card.png` | 72 × 108, RGBA, pixel-exact copy of the master region | `bdeb6a0f764c341ab34a1fc9308c78c7f67de47c15817e7ea4df459d6b0bd2c4` |
| `blm_card_x4.png` | 288 × 432, nearest-neighbour ×4, exact 4×4 replication | `5fc662831709389d2d8012c1e0b1149cda539f1c8b09e1e78b4cae201c69aeb1` |

## When a source URL comes back

1. Download it into its own new, empty directory (untrusted data).
2. Run the controls first; they must print `ALL PASS`:
   `~/venvs/blm-img/bin/python -I controls.py ../0.2-btc-puzzle.png <scratch dir>`
3. Compare:
   `~/venvs/blm-img/bin/python -I ../align_diff.py ../0.2-btc-puzzle.png <source> <outdir>`
4. Output: `regions.json` (every region beyond noise, master-pixel boxes),
   `absdiff_card.png`, `ref_card.png`, `src_card_aligned.png`.

"Beyond compression noise" means: peak z above the largest z on a clean ring
(48 px) around the card, where z is |difference| over the noise expected at that
pixel's edge strength. Smallest change tested and found: one pixel ~100 grey
levels darker (z 43.7 against a ring maximum of 22.5). Fainter changes may be
missed.
