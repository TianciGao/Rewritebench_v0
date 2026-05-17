# STATUS_ONLY_METRICS_DRYRUN_V0

## Command

```bash
python scripts/dev/compute_status_only_metrics_dryrun.py \
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \
  --authorization-overlay audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv \
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --out-dir audits/status_only_metrics_dryrun_v0
```

## Inputs

- `candidate_status_parsed_ledger_v1.csv`
- `metric_input_authorization_overlay_v0.csv`
- `denominator_same_engine_120.csv`

## Outputs

Outputs are written only under `audits/status_only_metrics_dryrun_v0/`.

## Dry-Run Metric Scope

The dry run covers Generation Rate, Execution Coverage Rate, and Result Consistency Rate logic only. Outputs are audit-only and are marked as not official and not paper results.

## Denominator Handling

The planned Track A same-engine denominator remains visible. Unauthorized overlap rows and unresolved rows are preserved in denominator/accounting outputs and are not used as success evidence.

## Non-Goals

No timing metrics, performance metrics, Semantic Equivalence Rate, Attribution Coverage, Cross-Engine metrics, reports/results updates, paper rendering, denominator changes, or paper-result changes are performed.

## Warnings

This dry run does not create official benchmark metrics. Status vocabulary may require normalization before any official metric computation can be authorized.
