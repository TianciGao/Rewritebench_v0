# NORMALIZED_STATUS_ONLY_METRICS_DRYRUN_V1

## Command

```bash
python scripts/dev/compute_normalized_status_only_metrics_dryrun.py \
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \
  --authorization-overlay audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv \
  --normalized-overlay audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv \
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --out-dir audits/normalized_status_only_metrics_dryrun_v1
```

## Inputs

- `candidate_status_parsed_ledger_v1.csv`
- `metric_input_authorization_overlay_v0.csv`
- `normalized_candidate_status_overlay_v0.csv`
- `denominator_same_engine_120.csv`

## Outputs

Outputs are written only under `audits/normalized_status_only_metrics_dryrun_v1/`.

## Normalized Field Usage

The dry run uses `normalized_generated`, `normalized_executed`, and `normalized_exact` for numerator membership. Unknown, not-applicable, and manual-mapping states remain visible and are not coerced to false.

## Dry-Run Metric Scope

The audit-only dry run covers Generation Rate, Execution Coverage Rate, and Result Consistency Rate logic only. It is not official benchmark computation.

## Denominator Handling

The planned Track A same-engine denominator remains visible. Unauthorized overlap rows and unresolved rows remain in accounting and are not used as success evidence.

## Non-Goals

No timing metrics, performance metrics, Semantic Equivalence Rate, Attribution Coverage, Cross-Engine metrics, reports/results updates, paper rendering, denominator changes, or paper-result changes are performed.

## Warnings

This dry run is not a paper result and not an official benchmark result. Future official metrics require separate authorization.
