# R10 erratum — E24 (Leopold II bust) boxes

**A box error found after scoring. It does not change the primary result.**

`r10_elements.json` is kept exactly as pre-registered: sha256 `3634036d4e0d785b2f2efbe5cb34c6a2ca69528f73a316c16c9d31c0e2b49b88`, not edited.

## The error

The file's E24 boxes are shifted **~60–90 px right** of the bust. The cause was a misread grid line in the top-right quadrant view used for boxing. The file is also internally inconsistent: its own pilot box for "Leopold XX eyes", `[1358, 443, 1424, 476]`, is correct, but it doesn't fit inside the face box.

| box | pre-registered (wrong) | corrected, review session | corrected, Windows re-measurement |
|---|---|---|---|
| bust (whole object, set A) | `[1395, 425, 1520, 615]` | `[1305, 420, 1475, 660]` | `[1303, 426, 1475, 652]` |
| head (face level, set C) | `[1418, 425, 1484, 512]` (sits beside the head) | `[1353, 425, 1430, 525]` | `[1353, 426, 1432, 515]` |

The two independent corrections agree to within 10 px. The corrected head contains both X marks, which `slot20.py` measures at x1358–1374 and x1395–1424.

## Effect: post hoc, NOT used for the decision

This uses the same pipeline as `r10_layout.py`: same seed, same draw order, and 10,000 draws per null. The script is `r10_erratum_check.py`.

| set | within 0.5°: count, p rotation / p hub | within 1.0°: count, p rotation / p hub |
|---|---|---|
| A, primary (unchanged) | 3/28, 0.286 / 0.281 | 4/28, 0.520 / 0.511 |
| C, face level | 5/28, 0.069 / 0.032 | 8/28, 0.119 / 0.024 |
| D, face level without the seal | 4/25, 0.105 / 0.081 | 7/25, 0.121 / 0.042 |

These figures use the review session's boxes. The Windows re-measurement gives identical counts and p-values within 0.005. The review session's independent rerun reported C as 0.068 / 0.033 and 0.121 / 0.025, which agrees within Monte Carlo error.

**Set C still fails the pre-stated rule** that p must be below 0.05 under *both* nulls: the rotation null gives 0.069 and 0.119. Across 8 comparisons (4 sets × 2 tolerances) it would also need p < 0.0063.

**Verdict unchanged: NOT SIGNIFICANT.** No further R10 work.
