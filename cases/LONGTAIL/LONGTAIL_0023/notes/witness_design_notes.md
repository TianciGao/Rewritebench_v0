# LONGTAIL_0023 Witness Design Notes

# Witness Design Notes

This witness focuses on graph-like relation structure rather than user ranking.
It includes:

- one post with both inbound and outbound links
- one post with outbound-only links
- one post with inbound-only links
- one isolated post that should be filtered out

`source.sql` and `rewrite_pos_01.sql` should agree.
`rewrite_neg_01.sql` collapses inbound and outbound directionality and therefore changes link counts.
No engine-closure or review claim is made by package construction.
