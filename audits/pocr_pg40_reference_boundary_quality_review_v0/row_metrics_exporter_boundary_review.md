# Row Metrics Exporter Boundary Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

The row-metrics exporter at `src/sql_rewrite_bench/pocr/stage_b_row_metrics.py` was reviewed.

Boundary checks:

- It writes one durable diagnostic CSV, `pocr_stage_b_row_metrics.csv`.
- It exports `expected_operation_atoms` and `stage_b_supported_operation_atoms` as separate fields.
- It exports `presence_only_operation_atoms`, `insufficient_transformation_evidence_atoms`, and `rejected_noop_equivalent_atoms` separately from supported atoms.
- It exports `semantic_guard_atoms` separately and does not place semantic guards in the operation numerator or denominator.
- It computes `oc_i` and `oc_i_fail_closed` from Stage B-supported operation atom counts and expected operation atom counts.
- It sets `diagnostic_only=true`.
- It requires `official_pocr_computed=false`, `route_level_pocr_aggregated=false`, and `paper_metric_promoted=false` through the diagnostic row schema.
- It marks malformed JSON, provider failures, timeouts, annotation missing, route mismatch, candidate mismatch, and no-candidate rows fail-closed.
- It does not inspect positive SQL, source SQL, or candidate SQL to infer new atoms during export.

Verdict: `pass`.

Boundary retained: positive SQL is reference evidence, not an atom source. skills.md is the only operation-atom source. candidate/source/positive span presence alone is not operation support.
