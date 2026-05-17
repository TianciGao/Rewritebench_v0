# source_positive_control_detail_adapter_v0 Report

## Purpose And Scope

This bounded adapter emits one source/positive `control_cell` detail row per source or positive row in `controls_360.csv`.
It reads only release-repo Common-core scaffolds and canonical case package metadata/evidence indexes.
The output is an audit artifact. It is not a production metrics ledger and is not paper evidence by itself.

## Inputs Read

- `case_sets/common_core_v0/cases.csv`
- `case_sets/common_core_v0/controls_360.csv`
- `inventory/case_registry.csv`
- `cases/PERF/PERF_0006/manifest.yaml`
- `cases/PERF/PERF_0006/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0006/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0006/checker/checker.yaml`
- `cases/PERF/PERF_0006/checker/normalization.yaml`
- `cases/PERF/PERF_0006/checker/compare_config.yaml`
- `cases/PERF/PERF_0006/sql/source.sql`
- `cases/PERF/PERF_0006/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0007/manifest.yaml`
- `cases/PERF/PERF_0007/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0007/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0007/checker/checker.yaml`
- `cases/PERF/PERF_0007/checker/normalization.yaml`
- `cases/PERF/PERF_0007/checker/compare_config.yaml`
- `cases/PERF/PERF_0007/sql/source.sql`
- `cases/PERF/PERF_0007/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0008/manifest.yaml`
- `cases/PERF/PERF_0008/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0008/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0008/checker/checker.yaml`
- `cases/PERF/PERF_0008/checker/normalization.yaml`
- `cases/PERF/PERF_0008/checker/compare_config.yaml`
- `cases/PERF/PERF_0008/sql/source.sql`
- `cases/PERF/PERF_0008/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0013/manifest.yaml`
- `cases/PERF/PERF_0013/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0013/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0013/checker/checker.yaml`
- `cases/PERF/PERF_0013/checker/normalization.yaml`
- `cases/PERF/PERF_0013/checker/compare_config.yaml`
- `cases/PERF/PERF_0013/sql/source.sql`
- `cases/PERF/PERF_0013/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0017/manifest.yaml`
- `cases/PERF/PERF_0017/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0017/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0017/checker/checker.yaml`
- `cases/PERF/PERF_0017/checker/normalization.yaml`
- `cases/PERF/PERF_0017/checker/compare_config.yaml`
- `cases/PERF/PERF_0017/sql/source.sql`
- `cases/PERF/PERF_0017/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0019/manifest.yaml`
- `cases/PERF/PERF_0019/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0019/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0019/checker/checker.yaml`
- `cases/PERF/PERF_0019/checker/normalization.yaml`
- `cases/PERF/PERF_0019/checker/compare_config.yaml`
- `cases/PERF/PERF_0019/sql/source.sql`
- `cases/PERF/PERF_0019/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0024/manifest.yaml`
- `cases/PERF/PERF_0024/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0024/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0024/checker/checker.yaml`
- `cases/PERF/PERF_0024/checker/normalization.yaml`
- `cases/PERF/PERF_0024/checker/compare_config.yaml`
- `cases/PERF/PERF_0024/sql/source.sql`
- `cases/PERF/PERF_0024/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0033/manifest.yaml`
- `cases/PERF/PERF_0033/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0033/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0033/checker/checker.yaml`
- `cases/PERF/PERF_0033/checker/normalization.yaml`
- `cases/PERF/PERF_0033/checker/compare_config.yaml`
- `cases/PERF/PERF_0033/sql/source.sql`
- `cases/PERF/PERF_0033/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0034/manifest.yaml`
- `cases/PERF/PERF_0034/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0034/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0034/checker/checker.yaml`
- `cases/PERF/PERF_0034/checker/normalization.yaml`
- `cases/PERF/PERF_0034/checker/compare_config.yaml`
- `cases/PERF/PERF_0034/sql/source.sql`
- `cases/PERF/PERF_0034/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0035/manifest.yaml`
- `cases/PERF/PERF_0035/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0035/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0035/checker/checker.yaml`
- `cases/PERF/PERF_0035/checker/normalization.yaml`
- `cases/PERF/PERF_0035/checker/compare_config.yaml`
- `cases/PERF/PERF_0035/sql/source.sql`
- `cases/PERF/PERF_0035/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0052/manifest.yaml`
- `cases/PERF/PERF_0052/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0052/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0052/checker/checker.yaml`
- `cases/PERF/PERF_0052/checker/normalization.yaml`
- `cases/PERF/PERF_0052/checker/compare_config.yaml`
- `cases/PERF/PERF_0052/sql/source.sql`
- `cases/PERF/PERF_0052/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0054/manifest.yaml`
- `cases/PERF/PERF_0054/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0054/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0054/checker/checker.yaml`
- `cases/PERF/PERF_0054/checker/normalization.yaml`
- `cases/PERF/PERF_0054/checker/compare_config.yaml`
- `cases/PERF/PERF_0054/sql/source.sql`
- `cases/PERF/PERF_0054/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0056/manifest.yaml`
- `cases/PERF/PERF_0056/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0056/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0056/checker/checker.yaml`
- `cases/PERF/PERF_0056/checker/normalization.yaml`
- `cases/PERF/PERF_0056/checker/compare_config.yaml`
- `cases/PERF/PERF_0056/sql/source.sql`
- `cases/PERF/PERF_0056/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0062/manifest.yaml`
- `cases/PERF/PERF_0062/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0062/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0062/checker/checker.yaml`
- `cases/PERF/PERF_0062/checker/normalization.yaml`
- `cases/PERF/PERF_0062/checker/compare_config.yaml`
- `cases/PERF/PERF_0062/sql/source.sql`
- `cases/PERF/PERF_0062/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0077/manifest.yaml`
- `cases/PERF/PERF_0077/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0077/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0077/checker/checker.yaml`
- `cases/PERF/PERF_0077/checker/normalization.yaml`
- `cases/PERF/PERF_0077/checker/compare_config.yaml`
- `cases/PERF/PERF_0077/sql/source.sql`
- `cases/PERF/PERF_0077/sql/positives/pos_01.sql`
- `cases/PERF/PERF_0082/manifest.yaml`
- `cases/PERF/PERF_0082/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0082/evidence/package_validation_summary.json`
- `cases/PERF/PERF_0082/checker/checker.yaml`
- `cases/PERF/PERF_0082/checker/normalization.yaml`
- `cases/PERF/PERF_0082/checker/compare_config.yaml`
- `cases/PERF/PERF_0082/sql/source.sql`
- `cases/PERF/PERF_0082/sql/positives/pos_01.sql`
- `cases/CONS/CONS_0005/manifest.yaml`
- `cases/CONS/CONS_0005/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0005/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0005/checker/checker.yaml`
- `cases/CONS/CONS_0005/checker/normalization.yaml`
- `cases/CONS/CONS_0005/checker/compare_config.yaml`
- `cases/CONS/CONS_0005/sql/source.sql`
- `cases/CONS/CONS_0005/sql/positives/pos_01.sql`
- `cases/CONS/CONS_0007/manifest.yaml`
- `cases/CONS/CONS_0007/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0007/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0007/checker/checker.yaml`
- `cases/CONS/CONS_0007/checker/normalization.yaml`
- `cases/CONS/CONS_0007/checker/compare_config.yaml`
- `cases/CONS/CONS_0007/sql/source.sql`
- `cases/CONS/CONS_0007/sql/positives/pos_01.sql`
- `cases/CONS/CONS_0009/manifest.yaml`
- `cases/CONS/CONS_0009/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0009/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0009/checker/checker.yaml`
- `cases/CONS/CONS_0009/checker/normalization.yaml`
- `cases/CONS/CONS_0009/checker/compare_config.yaml`
- `cases/CONS/CONS_0009/sql/source.sql`
- `cases/CONS/CONS_0009/sql/positives/pos_01.sql`
- `cases/CONS/CONS_0010/manifest.yaml`
- `cases/CONS/CONS_0010/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0010/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0010/checker/checker.yaml`
- `cases/CONS/CONS_0010/checker/normalization.yaml`
- `cases/CONS/CONS_0010/checker/compare_config.yaml`
- `cases/CONS/CONS_0010/sql/source.sql`
- `cases/CONS/CONS_0010/sql/positives/pos_01.sql`
- `cases/CONS/CONS_0011/manifest.yaml`
- `cases/CONS/CONS_0011/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0011/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0011/checker/checker.yaml`
- `cases/CONS/CONS_0011/checker/normalization.yaml`
- `cases/CONS/CONS_0011/checker/compare_config.yaml`
- `cases/CONS/CONS_0011/sql/source.sql`
- `cases/CONS/CONS_0011/sql/positives/pos_01.sql`
- `cases/CONS/CONS_0012/manifest.yaml`
- `cases/CONS/CONS_0012/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0012/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0012/checker/checker.yaml`
- `cases/CONS/CONS_0012/checker/normalization.yaml`
- `cases/CONS/CONS_0012/checker/compare_config.yaml`
- `cases/CONS/CONS_0012/sql/source.sql`
- `cases/CONS/CONS_0012/sql/positives/pos_01.sql`
- `cases/CONS/CONS_0024/manifest.yaml`
- `cases/CONS/CONS_0024/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0024/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0024/checker/checker.yaml`
- `cases/CONS/CONS_0024/checker/normalization.yaml`
- `cases/CONS/CONS_0024/checker/compare_config.yaml`
- `cases/CONS/CONS_0024/sql/source.sql`
- `cases/CONS/CONS_0024/sql/positives/pos_01.sql`
- `cases/CONS/CONS_0036/manifest.yaml`
- `cases/CONS/CONS_0036/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0036/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0036/checker/checker.yaml`
- `cases/CONS/CONS_0036/checker/normalization.yaml`
- `cases/CONS/CONS_0036/checker/compare_config.yaml`
- `cases/CONS/CONS_0036/sql/source.sql`
- `cases/CONS/CONS_0036/sql/positives/pos_01.sql`
- `cases/CONS/CONS_0037/manifest.yaml`
- `cases/CONS/CONS_0037/evidence/runs_retention.yaml`
- `cases/CONS/CONS_0037/evidence/package_validation_summary.json`
- `cases/CONS/CONS_0037/checker/checker.yaml`
- `cases/CONS/CONS_0037/checker/normalization.yaml`
- `cases/CONS/CONS_0037/checker/compare_config.yaml`
- `cases/CONS/CONS_0037/sql/source.sql`
- `cases/CONS/CONS_0037/sql/positives/pos_01.sql`
- `cases/PORT/PORT_0003/manifest.yaml`
- `cases/PORT/PORT_0003/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0003/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0003/checker/checker.yaml`
- `cases/PORT/PORT_0003/checker/normalization.yaml`
- `cases/PORT/PORT_0003/checker/compare_config.yaml`
- `cases/PORT/PORT_0003/sql/source.sql`
- `cases/PORT/PORT_0003/sql/positives/pos_01.sql`
- `cases/PORT/PORT_0004/manifest.yaml`
- `cases/PORT/PORT_0004/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0004/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0004/checker/checker.yaml`
- `cases/PORT/PORT_0004/checker/normalization.yaml`
- `cases/PORT/PORT_0004/checker/compare_config.yaml`
- `cases/PORT/PORT_0004/sql/source.sql`
- `cases/PORT/PORT_0004/sql/positives/pos_01.sql`
- `cases/PORT/PORT_0005/manifest.yaml`
- `cases/PORT/PORT_0005/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0005/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0005/checker/checker.yaml`
- `cases/PORT/PORT_0005/checker/normalization.yaml`
- `cases/PORT/PORT_0005/checker/compare_config.yaml`
- `cases/PORT/PORT_0005/sql/source.sql`
- `cases/PORT/PORT_0005/sql/positives/pos_01.sql`
- `cases/PORT/PORT_0008/manifest.yaml`
- `cases/PORT/PORT_0008/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0008/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0008/checker/checker.yaml`
- `cases/PORT/PORT_0008/checker/normalization.yaml`
- `cases/PORT/PORT_0008/checker/compare_config.yaml`
- `cases/PORT/PORT_0008/sql/source.sql`
- `cases/PORT/PORT_0008/sql/positives/pos_01.sql`
- `cases/PORT/PORT_0012/manifest.yaml`
- `cases/PORT/PORT_0012/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0012/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0012/checker/checker.yaml`
- `cases/PORT/PORT_0012/checker/normalization.yaml`
- `cases/PORT/PORT_0012/checker/compare_config.yaml`
- `cases/PORT/PORT_0012/sql/source.sql`
- `cases/PORT/PORT_0012/sql/positives/pos_01.sql`
- `cases/PORT/PORT_0013/manifest.yaml`
- `cases/PORT/PORT_0013/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0013/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0013/checker/checker.yaml`
- `cases/PORT/PORT_0013/checker/normalization.yaml`
- `cases/PORT/PORT_0013/checker/compare_config.yaml`
- `cases/PORT/PORT_0013/sql/source.sql`
- `cases/PORT/PORT_0013/sql/positives/pos_01.sql`
- `cases/PORT/PORT_0022/manifest.yaml`
- `cases/PORT/PORT_0022/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0022/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0022/checker/checker.yaml`
- `cases/PORT/PORT_0022/checker/normalization.yaml`
- `cases/PORT/PORT_0022/checker/compare_config.yaml`
- `cases/PORT/PORT_0022/sql/source.sql`
- `cases/PORT/PORT_0022/sql/positives/pos_01.sql`
- `cases/PORT/PORT_0024/manifest.yaml`
- `cases/PORT/PORT_0024/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0024/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0024/checker/checker.yaml`
- `cases/PORT/PORT_0024/checker/normalization.yaml`
- `cases/PORT/PORT_0024/checker/compare_config.yaml`
- `cases/PORT/PORT_0024/sql/source.sql`
- `cases/PORT/PORT_0024/sql/positives/pos_01.sql`
- `cases/PORT/PORT_0025/manifest.yaml`
- `cases/PORT/PORT_0025/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0025/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0025/checker/checker.yaml`
- `cases/PORT/PORT_0025/checker/normalization.yaml`
- `cases/PORT/PORT_0025/checker/compare_config.yaml`
- `cases/PORT/PORT_0025/sql/source.sql`
- `cases/PORT/PORT_0025/sql/positives/pos_01.sql`
- `cases/LONGTAIL/LONGTAIL_0011/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0011/checker/checker.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/checker/normalization.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/checker/compare_config.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/sql/source.sql`
- `cases/LONGTAIL/LONGTAIL_0011/sql/positives/pos_01.sql`
- `cases/LONGTAIL/LONGTAIL_0012/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0012/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0012/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0012/checker/checker.yaml`
- `cases/LONGTAIL/LONGTAIL_0012/checker/normalization.yaml`
- `cases/LONGTAIL/LONGTAIL_0012/checker/compare_config.yaml`
- `cases/LONGTAIL/LONGTAIL_0012/sql/source.sql`
- `cases/LONGTAIL/LONGTAIL_0012/sql/positives/pos_01.sql`
- `cases/LONGTAIL/LONGTAIL_0013/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0013/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0013/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0013/checker/checker.yaml`
- `cases/LONGTAIL/LONGTAIL_0013/checker/normalization.yaml`
- `cases/LONGTAIL/LONGTAIL_0013/checker/compare_config.yaml`
- `cases/LONGTAIL/LONGTAIL_0013/sql/source.sql`
- `cases/LONGTAIL/LONGTAIL_0013/sql/positives/pos_01.sql`
- `cases/LONGTAIL/LONGTAIL_0022/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0022/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0022/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0022/checker/checker.yaml`
- `cases/LONGTAIL/LONGTAIL_0022/checker/normalization.yaml`
- `cases/LONGTAIL/LONGTAIL_0022/checker/compare_config.yaml`
- `cases/LONGTAIL/LONGTAIL_0022/sql/source.sql`
- `cases/LONGTAIL/LONGTAIL_0022/sql/positives/pos_01.sql`
- `cases/LONGTAIL/LONGTAIL_0023/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0023/checker/checker.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/checker/normalization.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/checker/compare_config.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/sql/source.sql`
- `cases/LONGTAIL/LONGTAIL_0023/sql/positives/pos_01.sql`
- `cases/LONGTAIL/LONGTAIL_0024/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0024/evidence/runs_retention.yaml`
- `cases/LONGTAIL/LONGTAIL_0024/evidence/package_validation_summary.json`
- `cases/LONGTAIL/LONGTAIL_0024/checker/checker.yaml`
- `cases/LONGTAIL/LONGTAIL_0024/checker/normalization.yaml`
- `cases/LONGTAIL/LONGTAIL_0024/checker/compare_config.yaml`
- `cases/LONGTAIL/LONGTAIL_0024/sql/source.sql`
- `cases/LONGTAIL/LONGTAIL_0024/sql/positives/pos_01.sql`

## Rows Emitted

- Rows emitted: 240

## Source/Positive Route Counts

- `positive`: 120
- `source`: 120

## Pool Counts

- `CONS`: 54
- `LONGTAIL`: 36
- `PERF`: 96
- `PORT`: 54

## Engine Counts

- `mysql`: 80
- `postgres`: 80
- `spark`: 80

## Applicable Status Counts

- `planned_control`: 240

## Evidence-index Caveats

- `evidence_not_retained`: 61
- `indexed_not_recomputed`: 179

`indexed_not_recomputed` means an engine-specific source/positive retained artifact is indexed in the release case package, but this task did not parse or rerun it.
`evidence_not_retained` means the row is preserved from the scaffold, but no engine-specific source/positive retained artifact was indexed for that control cell.

## Explicit Non-goals

- No legacy reports/results/runs were read.
- No production retained evidence was parsed.
- No source/positive validation was rerun.
- No source/positive pass rate was computed.
- No Result Consistency Rate was computed.
- No semantic equivalence proof was created.
- No reports/results were copied or modified.
- No production ledger was created under `results/`.
- No paper tables were rendered.

## Why This Is Not Metrics Computation

Every row has `metric_input_authorized=false`, `metrics_computed=false`, `source_positive_rate_computed=false`, `result_consistency_rate_computed=false`, and execution/correctness/timing fields set to `N.A.`.

## Why This Is Not Source-positive Consistency Computation

The adapter records SQL/config paths and retained artifact pointers only. It does not inspect outputs, classify equality, or aggregate source-positive outcomes.

## Why This Is Not Legacy Retained-evidence Parsing

The adapter reads only release-repo case package metadata and indexes. It does not inspect `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean` or parse legacy reports/results/runs.

## Validation Result

PASS: all required adapter checks passed.

## Next Safe Action

Review source/positive detail row coverage and validator output before authorizing any adapter that parses real retained evidence or computes correctness metrics.
