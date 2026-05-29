# Source/Positive Contract Review

The corrected `pos_01.sql` matches the source query surface for `LONGTAIL_0011`.

Observed alignment:

- Both source and corrected positive SQL define `RankedPosts`.
- Both compute `DENSE_RANK()` over `PARTITION BY p.OwnerUserId ORDER BY p.Score DESC`.
- Both name the rank as `PostRank`.
- Both define `MaxRank` grouped by `OwnerDisplayName` with `MAX(PostRank) AS MaxPostRank`.
- Both join `RankedPosts` to `MaxRank` by `OwnerDisplayName`.
- Both select rows using `rp.PostRank = mr.MaxPostRank`.
- Both preserve the projected columns and final ordering by `rp.Score DESC, rp.ViewCount DESC`.

This correction is semantic, not surface-only. The previous positive SQL selected ascending lowest-score ranks via `WorstRank = 1`, which contradicted the source and skills contract. The corrected file restores the intended descending-rank and max-rank boundary.

Common-core membership changed: no.

Denominator changed: no.
