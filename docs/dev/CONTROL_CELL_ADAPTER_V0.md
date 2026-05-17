# control_cell_adapter_v0

Developer-facing note. This is not public runner documentation and not a production metrics ledger.

## Command

```bash
python scripts/dev/build_control_cell_ledger.py \
  --case-set case_sets/common_core_v0/cases.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/control_cell_adapter_v0
```

## Scope

The adapter reads only release-repo Common-core case-set scaffolds, `controls_360.csv`, `inventory/case_registry.csv` context where needed, and canonical case package metadata/evidence index files such as `manifest.yaml`, `evidence/runs_retention.yaml`, `evidence/package_validation_summary.json`, and `checker/expected_rejections.yaml`.

It emits one `control_cell` row for each planned `case_id x engine x control_route` row in `controls_360.csv`.

## Outputs

- `audits/control_cell_adapter_v0/control_cell_ledger_v0.csv`
- `audits/control_cell_adapter_v0/control_cell_adapter_v0_summary.json`
- `audits/control_cell_adapter_v0/control_cell_adapter_v0_report.md`
- `audits/control_cell_adapter_v0/control_cell_adapter_v0_checks.csv`
- `audits/control_cell_adapter_v0/ledger_validation/*`

## Non-goals

- No legacy repo reads.
- No legacy reports/results/runs parsing.
- No production retained-evidence parsing.
- No metrics computation.
- No hard-negative pass-rate computation.
- No source/positive execution inference.
- No reports/results migration.
- No production ledger under `results/retained`.
- No paper table rendering.

## Validation Command

```bash
python scripts/dev/validate_ledger_csv.py \
  --ledger audits/control_cell_adapter_v0/control_cell_ledger_v0.csv \
  --case-set case_sets/common_core_v0/cases.csv \
  --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/control_cell_adapter_v0/ledger_validation
```

## Relation To Future Metrics

These rows preserve control scaffold coverage and indexed evidence references. They are not metric inputs yet: `metric_input_authorized=false`, `metrics_computed=false`, and execution/correctness/timing fields are `N.A.`.

Any future metric consumption requires separate authorization and a validated production ledger policy.
