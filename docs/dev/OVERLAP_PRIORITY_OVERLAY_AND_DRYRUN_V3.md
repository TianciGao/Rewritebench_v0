# Overlap Priority Overlay And Dry-Run V3

## Purpose

This developer note documents the audit-only `overlap_priority_overlay_v1` and `normalized_status_only_metrics_dryrun_v3` workflow.

The workflow resolves candidate-status source overlap using the maintainer-approved Option B policy, refreshes normalization for newly authorized overlap rows, and runs an audit-only normalized status dry run. It does not compute official metrics.

## Commands

Build the overlap priority overlay:

```bash
python scripts/dev/build_overlap_priority_overlay_v1.py \
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \
  --readiness-review audits/candidate_status_parser_v1_closeout/candidate_status_metric_input_readiness_review.csv \
  --denied-rows audits/metric_input_authorization_overlay_v0/metric_input_authorization_denied_rows.csv \
  --overlap-proposal audits/candidate_status_evidence_completion_round1/overlap_rows_resolution_proposal.csv \
  --out-dir audits/overlap_priority_overlay_v1
```

Refresh normalization for newly authorized overlap rows:

```bash
python scripts/dev/normalize_overlap_authorized_rows_v1.py \
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \
  --combined-authorization audits/overlap_priority_overlay_v1/combined_metric_input_authorization_overlay_v1.csv \
  --existing-normalized-overlay audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv \
  --mapping-table audits/status_field_normalization_v0/status_normalization_mapping_table.csv \
  --out-dir audits/overlap_priority_overlay_v1
```

Run the audit-only dry run:

```bash
python scripts/dev/compute_normalized_status_only_metrics_dryrun_v3.py \
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \
  --combined-authorization audits/overlap_priority_overlay_v1/combined_metric_input_authorization_overlay_v1.csv \
  --combined-normalized-overlay audits/overlap_priority_overlay_v1/combined_normalized_candidate_status_overlay_v1.csv \
  --inference-overlay audits/status_inference_overlay_v0/status_inference_overlay_v0.csv \
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --out-dir audits/normalized_status_only_metrics_dryrun_v3
```

## Option B Policy

- P001 provides generation/readiness evidence.
- P002 provides primary candidate status.
- P003 provides Repair-1 failure enrichment only.
- P003 must not override P002 primary status.
- Ambiguous rows remain unauthorized.

## Outputs

- `audits/overlap_priority_overlay_v1/overlap_priority_overlay_v1.csv`
- `audits/overlap_priority_overlay_v1/combined_metric_input_authorization_overlay_v1.csv`
- `audits/overlap_priority_overlay_v1/combined_normalized_candidate_status_overlay_v1.csv`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_metrics_dryrun_v3_table.csv`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_dryrun_v3_delta_vs_v2.csv`

## Non-Goals

- No official metrics.
- No paper tables.
- No timing or performance metrics.
- No SQLGlot parser implementation.
- No reports/results updates.
- No denominator or case membership changes.
- No parser-ledger, v0 authorization-overlay, normalization-overlay, or inference-overlay mutation.

## Warnings

The v3 dry run remains audit-only. `dry_run_value_is_official=false`, `paper_result=false`, and `audit_only=true` are required on dry-run table rows. Future official metric computation requires separate authorization.
