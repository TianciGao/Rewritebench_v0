# LONGTAIL_0022 Witness Design Notes

# Witness Design Notes

This witness focuses on comment-driven interaction rather than broad user ranking.
It includes:

- one post with repeated comments from the same user
- one post with comments from multiple distinct users
- one post below the discussion threshold
- one qualifying post with a different owner and lower score

`source.sql` and `rewrite_pos_01.sql` should agree.
`rewrite_neg_01.sql` fragments aggregation by commenter and therefore changes row cardinality and counts.
No engine-closure or review claim is made by package construction.
