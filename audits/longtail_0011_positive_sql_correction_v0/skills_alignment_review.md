# Skills Alignment Review

The corrected `pos_01.sql` aligns with `cases/LONGTAIL/LONGTAIL_0011/skills.md`.

Atom alignment:

- A1 `dense_rank_postrank_preservation`: satisfied by `DENSE_RANK() OVER (PARTITION BY p.OwnerUserId ORDER BY p.Score DESC) AS PostRank`.
- A2 `maxrank_join_boundary_preservation`: satisfied by `MaxRank`, `MAX(PostRank) AS MaxPostRank`, the `OwnerDisplayName` grouping boundary, and the join back to `RankedPosts`.
- A3 `dense_rank_tie_preservation`: satisfied by preserving `DENSE_RANK` and removing the ascending `WorstRank` shortcut.
- A4 `owner_partition_and_displayname_boundary_preservation`: satisfied by preserving owner partitioning, display-name grouping, post filters, output columns, and final ordering.

The previous `pos_01.sql` violated the guard against an ascending worst-rank shortcut because it used `ORDER BY p.Score ASC AS WorstRank` and `WHERE rp.WorstRank = 1`.

`skills.md` needs modification: no. The skills contract already described the correct descending `PostRank` / `MaxRank` structure and the hard-negative boundary.
