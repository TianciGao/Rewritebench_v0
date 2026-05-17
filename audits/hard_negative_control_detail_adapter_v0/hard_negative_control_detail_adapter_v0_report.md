# hard_negative_control_detail_adapter_v0 Report

## Purpose And Scope

This bounded adapter emits one hard-negative `control_cell` detail row per hard-negative row in `controls_360.csv`.
It reads only release-repo Common-core scaffolds and canonical case package metadata/evidence indexes.
The output is an audit artifact. It is not a production metrics ledger and is not paper evidence by itself.

## Inputs Read

- `case_sets/common_core_v0/cases.csv`
- `case_sets/common_core_v0/controls_360.csv`
- `inventory/case_registry.csv`
- `cases/PERF/PERF_0006/manifest.yaml`
- `cases/PERF/PERF_0006/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0006/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0006/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0006/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0007/manifest.yaml`
- `cases/PERF/PERF_0007/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0007/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0007/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0007/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0008/manifest.yaml`
- `cases/PERF/PERF_0008/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0008/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0008/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0008/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0013/manifest.yaml`
- `cases/PERF/PERF_0013/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0013/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0013/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0013/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0017/manifest.yaml`
- `cases/PERF/PERF_0017/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0017/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0017/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0017/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0019/manifest.yaml`
- `cases/PERF/PERF_0019/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0019/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0019/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0019/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0024/manifest.yaml`
- `cases/PERF/PERF_0024/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0024/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0024/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0024/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0033/manifest.yaml`
- `cases/PERF/PERF_0033/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0033/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0033/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0033/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0034/manifest.yaml`
- `cases/PERF/PERF_0034/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0034/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0034/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0034/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0035/manifest.yaml`
- `cases/PERF/PERF_0035/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0035/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0035/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0035/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0052/manifest.yaml`
- `cases/PERF/PERF_0052/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0052/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0052/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0052/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0054/manifest.yaml`
- `cases/PERF/PERF_0054/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0054/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0054/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0054/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0056/manifest.yaml`
- `cases/PERF/PERF_0056/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0056/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0056/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0056/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0062/manifest.yaml`
- `cases/PERF/PERF_0062/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0062/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0062/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0062/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0077/manifest.yaml`
- `cases/PERF/PERF_0077/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0077/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0077/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0077/evidence/hard_negative/hard_negative_summary.json`
- `cases/PERF/PERF_0082/manifest.yaml`
- `cases/PERF/PERF_0082/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0082/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0082/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0082/evidence/hard_negative/hard_negative_summary.json`
- `cases/CONS/CONS_0005/manifest.yaml`
- `cases/CONS/CONS_0005/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0005/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0005/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0005/evidence/hard_negative/hard_negative_summary.json`
- `cases/CONS/CONS_0007/manifest.yaml`
- `cases/CONS/CONS_0007/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0007/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0007/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0007/evidence/hard_negative/hard_negative_summary.json`
- `cases/CONS/CONS_0009/manifest.yaml`
- `cases/CONS/CONS_0009/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0009/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0009/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0009/evidence/hard_negative/hard_negative_summary.json`
- `cases/CONS/CONS_0010/manifest.yaml`
- `cases/CONS/CONS_0010/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0010/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0010/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0010/evidence/hard_negative/hard_negative_summary.json`
- `cases/CONS/CONS_0011/manifest.yaml`
- `cases/CONS/CONS_0011/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0011/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0011/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0011/evidence/hard_negative/hard_negative_summary.json`
- `cases/CONS/CONS_0012/manifest.yaml`
- `cases/CONS/CONS_0012/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0012/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0012/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0012/evidence/hard_negative/hard_negative_summary.json`
- `cases/CONS/CONS_0024/manifest.yaml`
- `cases/CONS/CONS_0024/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0024/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0024/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0024/evidence/hard_negative/hard_negative_summary.json`
- `cases/CONS/CONS_0036/manifest.yaml`
- `cases/CONS/CONS_0036/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0036/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0036/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0036/evidence/hard_negative/hard_negative_summary.json`
- `cases/CONS/CONS_0037/manifest.yaml`
- `cases/CONS/CONS_0037/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0037/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0037/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0037/evidence/hard_negative/hard_negative_summary.json`
- `cases/PORT/PORT_0003/manifest.yaml`
- `cases/PORT/PORT_0003/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0003/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0003/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0003/evidence/hard_negative/hard_negative_summary.json`
- `cases/PORT/PORT_0004/manifest.yaml`
- `cases/PORT/PORT_0004/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0004/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0004/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0004/evidence/hard_negative/hard_negative_summary.json`
- `cases/PORT/PORT_0005/manifest.yaml`
- `cases/PORT/PORT_0005/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0005/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0005/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0005/evidence/hard_negative/hard_negative_summary.json`
- `cases/PORT/PORT_0008/manifest.yaml`
- `cases/PORT/PORT_0008/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0008/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0008/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0008/evidence/hard_negative/hard_negative_summary.json`
- `cases/PORT/PORT_0012/manifest.yaml`
- `cases/PORT/PORT_0012/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0012/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0012/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0012/evidence/hard_negative/hard_negative_summary.json`
- `cases/PORT/PORT_0013/manifest.yaml`
- `cases/PORT/PORT_0013/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0013/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0013/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0013/evidence/hard_negative/hard_negative_summary.json`
- `cases/PORT/PORT_0022/manifest.yaml`
- `cases/PORT/PORT_0022/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0022/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0022/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0022/evidence/hard_negative/hard_negative_summary.json`
- `cases/PORT/PORT_0024/manifest.yaml`
- `cases/PORT/PORT_0024/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0024/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0024/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0024/evidence/hard_negative/hard_negative_summary.json`
- `cases/PORT/PORT_0025/manifest.yaml`
- `cases/PORT/PORT_0025/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0025/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0025/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0025/evidence/hard_negative/hard_negative_summary.json`
- `cases/LONGTAIL/LONGTAIL_0011/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/checker/expected_rejections.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0011/evidence/hard_negative/hard_negative_summary.json`
- `cases/LONGTAIL/LONGTAIL_0012/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0012/checker/expected_rejections.yaml`
- `cases/LONGTAIL/LONGTAIL_0012/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0012/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0012/evidence/hard_negative/hard_negative_summary.json`
- `cases/LONGTAIL/LONGTAIL_0013/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0013/checker/expected_rejections.yaml`
- `cases/LONGTAIL/LONGTAIL_0013/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0013/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0013/evidence/hard_negative/hard_negative_summary.json`
- `cases/LONGTAIL/LONGTAIL_0022/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0022/checker/expected_rejections.yaml`
- `cases/LONGTAIL/LONGTAIL_0022/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0022/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0022/evidence/hard_negative/hard_negative_summary.json`
- `cases/LONGTAIL/LONGTAIL_0023/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/checker/expected_rejections.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0023/evidence/hard_negative/hard_negative_summary.json`
- `cases/LONGTAIL/LONGTAIL_0024/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0024/checker/expected_rejections.yaml`
- `cases/LONGTAIL/LONGTAIL_0024/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0024/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0024/evidence/hard_negative/hard_negative_summary.json`

## Rows Emitted

- Rows emitted: 120

## Pool Counts

- `CONS`: 27
- `LONGTAIL`: 18
- `PERF`: 48
- `PORT`: 27

## Engine Counts

- `mysql`: 40
- `postgres`: 40
- `spark`: 40

## Approval Status Counts

- `maintainer_approved_for_migration`: 45
- `manual_review_required`: 3
- `migration_planning_static_inference_needs_review_if_not_explicit_in_legacy`: 72

## Applicable / N.A. Counts

- `planned_control`: 120

## Evidence-index Caveats

- `evidence_not_retained`: 23
- `indexed_not_recomputed`: 97

`indexed_not_recomputed` means an engine-specific hard-negative retained artifact is indexed in the release case package, but this task did not parse or rerun it.
`evidence_not_retained` means the row is preserved from the scaffold, but no engine-specific hard-negative retained artifact was indexed for that control cell.

## Explicit Non-goals

- No legacy reports/results/runs were read.
- No production retained evidence was parsed.
- No hard-negative validation was rerun.
- No hard-negative pass/fail rate was computed.
- No false-accept rate was computed.
- No semantic equivalence proof was created.
- No reports/results were copied or modified.
- No production ledger was created under `results/`.
- No paper tables were rendered.

## Why This Is Not Metrics Computation

Every row has `metric_input_authorized=false`, `metrics_computed=false`, `hard_negative_rate_computed=false`, and execution/correctness/timing fields set to `N.A.`.

## Why This Is Not False-accept-rate Computation

The adapter records expected-rejection metadata and retained artifact pointers only. It does not inspect outputs, classify outcomes, or aggregate rejected/accepted counts.

## Why This Is Not Legacy Retained-evidence Parsing

The adapter reads only release-repo case package metadata and indexes. It does not inspect `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean` or parse legacy reports/results/runs.

## Validation Result

PASS: all required adapter checks passed.

## Next Safe Action

Review hard-negative detail row coverage and validator output before authorizing any adapter that parses real retained evidence or computes hard-negative metrics.
