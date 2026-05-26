# Aggregation Formula Review

Metric-definition checkpoint:

- POCR@planned is the denominator-aware route-level headline candidate for promotion diagnostics.
- POCR@candidate is the candidate-quality diagnostic view.
- POCR@curated remains `NA` / `curated_manifest_missing`.
- Macro-average over per-row OC_i is the main formula.
- Total supported atoms divided by total expected atoms is diagnostic micro-average only.
- This task does not compute official POCR or promote a paper metric.

Implemented aggregation:

- POCR@planned uses rows where `pocr_planned_denominator_member=true`.
- POCR@candidate uses rows where `pocr_candidate_denominator_member=true`.
- Both denominator views use `oc_i_fail_closed`.
- Rows with `not_applicable_reason=not_applicable_no_expected_operation_atoms` are counted separately and excluded from numeric macro denominators.
- Fail-closed denominator rows with `oc_i_fail_closed=0` remain in the numeric denominator.
- POCR@curated is not computed and is emitted as `NA` with `pocr_curated_status=curated_manifest_missing`.
- Diagnostic micro-average is emitted under `diagnostic_micro_average_supported_over_expected`.

This aggregator computes promotion-diagnostic POCR@planned and POCR@candidate only.

Macro-average over per-row OC_i is used.

Diagnostic micro-average is not the paper formula.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
