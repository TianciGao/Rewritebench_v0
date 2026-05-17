# hard_negative_control_detail_adapter_v0

Developer-facing note. This is not public runner documentation and not a production metrics ledger.

## Command

```bash
python scripts/dev/build_hard_negative_control_detail_ledger.py \
  --case-set case_sets/common_core_v0/cases.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/hard_negative_control_detail_adapter_v0
```

## Scope

The adapter reads only release-repo Common-core scaffolds, `inventory/case_registry.csv`, and canonical case package metadata/evidence index files:

- `manifest.yaml`
- `checker/expected_rejections.yaml`
- `evidence/runs_retention.yaml`
- `evidence/package_validation_summary.json`
- `evidence/hard_negative/`

It emits one `control_cell` row for each planned `case_id x engine x hard_negative` row in `controls_360.csv`.

## Outputs

- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_ledger_v0.csv`
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_adapter_v0_summary.json`
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_adapter_v0_report.md`
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_adapter_v0_checks.csv`
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_limitations.md`
- `audits/hard_negative_control_detail_adapter_v0/ledger_validation/*`

## Non-goals

- No legacy repo reads.
- No legacy reports/results/runs parsing.
- No production retained-evidence parsing.
- No method candidate adapter implementation.
- No metrics computation.
- No hard-negative rejection-rate computation.
- No false-accept-rate computation.
- No fresh DB validation.
- No reports/results migration.
- No production ledger under `results/retained`.
- No paper table rendering.

## Validation Command

```bash
python scripts/dev/validate_ledger_csv.py \
  --ledger audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_ledger_v0.csv \
  --case-set case_sets/common_core_v0/cases.csv \
  --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/hard_negative_control_detail_adapter_v0/ledger_validation
```

## Relation To Future Hard-negative Metrics

These rows preserve hard-negative control scaffold coverage, expected-rejection metadata, approval status, semantic-risk labels, and release-package evidence pointers. They do not establish hard-negative rejection outcomes and do not compute false-accept rates.

Any future hard-negative metric or report must use separately authorized retained-evidence parsing, production ledger validation, and metric computation.
