# Official Status Metrics v0 Limited

## Command

```bash
python scripts/dev/compute_official_status_metrics_limited.py \
  --combined-candidate-ledger audits/combined_candidate_status_overlay_v2/combined_candidate_status_ledger_v2.csv \
  --combined-authorization audits/overlap_priority_overlay_v1/combined_metric_input_authorization_overlay_v1.csv \
  --combined-normalized-overlay audits/overlap_priority_overlay_v1/combined_normalized_candidate_status_overlay_v1.csv \
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --out-dir audits/official_status_metrics_v0_limited
```

## Inputs

- Combined candidate status overlay v2.
- Combined metric-input authorization overlay v1.
- Combined normalized candidate status overlay v1.
- Track A same-engine denominator scaffold.

## Outputs

- `official_status_metrics_v0_limited_table.csv`
- `official_status_metrics_denominator_audit.csv`
- `official_status_metrics_input_rows.csv`
- `official_status_metrics_blocked_generation_rate.csv`
- `official_status_metrics_v0_limited_report.md`
- `official_status_metrics_v0_limited_checks.csv`
- `official_status_metrics_v0_limited_summary.json`
- `official_status_metrics_v0_limited_limitations.md`

## Official Limited Metric Scope

This task computes only:

- Execution Coverage Rate
- Result Consistency Rate

Rows are grouped by metric, rewrite method, pool, and engine. Outputs are official limited status metrics, not paper tables.

## Blocked Generation Rate

Generation Rate is not computed. It remains blocked because inferred-generated policy has not been officialized and SQLGlot generated/ready evidence is missing.

## Denominator Handling

The planned Track A same-engine candidate denominator remains visible. Authorized input rows do not replace the denominator. Unresolved and unauthorized rows remain explicit non-success partitions.

## Non-Goals

- No official Generation Rate.
- No timing or performance metrics.
- No paper table rendering.
- No reports/results updates.
- No denominator, paper-result, case-membership, or raw-evidence changes.
- No global leaderboard.

## Warnings

SQLGlot rows are present in combined candidate status overlay v2, but they are not in the current metric-input authorization and normalization overlay used by this limited official task. They remain denominator-visible and unauthorized for this computation.
