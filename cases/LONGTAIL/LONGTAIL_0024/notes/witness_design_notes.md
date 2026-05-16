# LONGTAIL_0024 Witness Design Notes

# Witness Design Notes

This witness focuses on edit-history intensity rather than user reputation or badge counts.
It includes:

- one post with repeated edits by the same user
- one post edited by multiple users
- one post with exactly one history row that should be filtered out
- one post with more revisions but older last-edit timestamp

`source.sql` and `rewrite_pos_01.sql` should agree.
`rewrite_neg_01.sql` groups by editor too early and fragments revision counts.
No engine-closure or review claim is made by package construction.
