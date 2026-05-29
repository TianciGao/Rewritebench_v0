# Tag-Slice Diagnostic Boundary

Failure buckets and tag slices are diagnostic/support only.

They must not be used as:

- ranking metrics
- leaderboard inputs
- primary metric replacements
- official paper result inputs
- substitutes for Generation Rate, Execution Coverage Rate, Result Consistency Rate, Semantic Equivalence Rate, GM Speedup, Speedup Percentiles, POCR, or cross-engine metrics

Current implementation facts:

- `src/sql_rewrite_bench/tag_slices.py` emits `local_diagnostic_only=true`, `official_metric=false`, `leaderboard_input=false`, and a claim boundary stating that tag slices are not scores, official metrics, paper evidence, or leaderboard input.
- Tag-slice rows contain counts such as selected, generated, executed, exact, mismatch, execution failed, checker failed, source-like, and timed rows by retained manifest taxonomy tag.
- These counts are useful for frontier review and debugging but do not define a primary denominator or route score.

Repair-1 implication:

- Repair-1 may use failure buckets and tag slices to choose diagnostic review slices, but any Repair-1 result must still report primary metrics through the approved local or official metric path.
