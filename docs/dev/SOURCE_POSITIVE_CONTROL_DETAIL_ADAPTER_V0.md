# source_positive_control_detail_adapter_v0

Developer-facing note. This is not public runner documentation and not a production metrics ledger.

## Command

```bash
python scripts/dev/build_source_positive_control_detail_ledger.py \
  --case-set case_sets/common_core_v0/cases.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/source_positive_control_detail_adapter_v0
```

## Scope

The adapter reads only release-repo Common-core scaffolds, `inventory/case_registry.csv`, and canonical case package metadata/evidence index files:

- `manifest.yaml`
- `evidence/runs_retention.yaml`
- `evidence/package_validation_summary.json`
- `checker/checker.yaml`
- `checker/normalization.yaml`
- `checker/compare_config.yaml`
- `sql/source.sql`
- `sql/positives/pos_01.sql`

It emits one `control_cell` row for each planned `case_id x engine x source|positive` row in `controls_360.csv`.

## Outputs

- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_ledger_v0.csv`
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_adapter_v0_summary.json`
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_adapter_v0_report.md`
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_adapter_v0_checks.csv`
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_limitations.md`
- `audits/source_positive_control_detail_adapter_v0/ledger_validation/*`

## Non-goals

- No legacy repo reads.
- No legacy reports/results/runs parsing.
- No production retained-evidence parsing.
- No method candidate adapter implementation.
- No metrics computation.
- No source-positive pass-rate computation.
- No Result Consistency Rate computation.
- No fresh DB validation.
- No reports/results migration.
- No production ledger under `results/retained`.
- No paper table rendering.

## Validation Command

```bash
python scripts/dev/validate_ledger_csv.py \
  --ledger audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_ledger_v0.csv \
  --case-set case_sets/common_core_v0/cases.csv \
  --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/source_positive_control_detail_adapter_v0/ledger_validation
```

## Relation To Future Correctness Metrics

These rows preserve source/positive control scaffold coverage, checker configuration pointers, SQL artifact paths, and release-package retained evidence pointers. They do not establish execution, exactness, source-positive consistency, or Result Consistency Rate.

Any future correctness metric or report must use separately authorized retained-evidence parsing, production ledger validation, and metric computation.
