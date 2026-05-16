# LONGTAIL_0012 Witness Design Notes

# Witness Design Notes

Per-title user post summary with optional vote-count enrichment; negative drops zero-vote posts.
The witness dataset is intentionally small and case-local.
It is designed so `source.sql` and `rewrite_pos_01.sql` should agree, while `rewrite_neg_01.sql` should diverge.
No engine-closure or review claim is made by package construction.
