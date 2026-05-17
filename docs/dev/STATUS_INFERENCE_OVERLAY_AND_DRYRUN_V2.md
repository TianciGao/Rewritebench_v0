# STATUS_INFERENCE_OVERLAY_AND_DRYRUN_V2

## Commands

```bash
python scripts/dev/build_status_inference_overlay.py \
  --preview audits/status_inference_policy_v0/inferred_status_candidate_overlay_preview.csv \
  --normalized-overlay audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv \
  --out-dir audits/status_inference_overlay_v0

python scripts/dev/compute_normalized_status_only_metrics_dryrun_v2.py \
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \
  --authorization-overlay audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv \
  --normalized-overlay audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv \
  --inference-overlay audits/status_inference_overlay_v0/status_inference_overlay_v0.csv \
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --out-dir audits/normalized_status_only_metrics_dryrun_v2
```

## Inputs

The workflow reads parser-v1 audit rows, the metric-input authorization overlay, the normalized status overlay, the R1 inference preview/overlay, and the Track A same-engine denominator scaffold.

## Outputs

Outputs are written only under `audits/status_inference_overlay_v0/` and `audits/normalized_status_only_metrics_dryrun_v2/`.

## Inference Rule Used

Only R1 is used: `normalized_ready=true` may support `inferred_generated=true` in an audit-only overlay. Observed `normalized_generated` remains unchanged.

## Observed Vs Inferred Distinction

V2 reports observed and inferred numerator counts separately. Inferred generated rows are not source-observed generated rows.

## Non-goals

No official metrics, paper tables, reports/results updates, denominator changes, timing metrics, performance metrics, reproduction CLI, public runner, or raw legacy evidence changes are performed.

## Warnings

This is an audit-only dry-run. Future official metrics require separate authorization and validation.
