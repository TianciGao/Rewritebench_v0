# candidate_status_adapter_v0

Developer-facing note. This is a release-summary-only, non-timing overlay for the existing rewrite candidate scaffold. It is not public runner documentation and not a production metrics ledger.

## Command

```bash
python scripts/dev/build_candidate_status_ledger.py \
  --scaffold audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv \
  --out-dir audits/candidate_status_adapter_v0
```

## Scope

The adapter reads the 600-row `rewrite_candidate_adapter_v0` scaffold and approved release-repo audit metadata files only. It emits one `rewrite_candidate_cell` row for each scaffold row.

Allowed method routes:

- `direct_llm_original`
- `direct_llm_repair_1`
- `sqlglot_optimize`
- `sqlglot_noop`
- `calcite_hep_fail_closed`

## Inputs

- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv`
- Release-repo retained-summary and retained-evidence mapping audit files
- Release-repo metrics contract and closeout metadata

Legacy paths referenced inside audit CSVs are not opened.

## Outputs

- `audits/candidate_status_adapter_v0/candidate_status_ledger_v0.csv`
- `audits/candidate_status_adapter_v0/candidate_status_adapter_v0_summary.json`
- `audits/candidate_status_adapter_v0/candidate_status_adapter_v0_report.md`
- `audits/candidate_status_adapter_v0/candidate_status_adapter_v0_checks.csv`
- `audits/candidate_status_adapter_v0/candidate_status_adapter_v0_limitations.md`
- `audits/candidate_status_adapter_v0/candidate_status_input_use_log.csv`
- `audits/candidate_status_adapter_v0/ledger_validation/*`

## Fields

The adapter may fill overlay provenance fields and notes. Candidate outcome fields remain unresolved unless exact row-grain release evidence exists.

In the current overlay, no row-level candidate status was filled. `generated`, `ready`, `executed`, `exact`, and `timed` remain `N.A.`, while `result_status=evidence_not_adapted_yet`.

## Timing Exclusion

Timing remains excluded. `timed=N.A.`, `latency_ms` is blank, `speedup_ratio` is blank, and `timing_eligible=N.A.` for every row.

## Metrics Boundary

No metrics are computed. `metric_input_authorized=false` and `metrics_computed=false` for every row.

Route-level summaries are not row-level statuses and must not be distributed across the 600 rows.

## Validation Command

```bash
python scripts/dev/validate_ledger_csv.py \
  --ledger audits/candidate_status_adapter_v0/candidate_status_ledger_v0.csv \
  --case-set case_sets/common_core_v0/cases.csv \
  --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/candidate_status_adapter_v0/ledger_validation
```

## Next Safe Action

Review unresolved rows and request separate authorization before implementing a production retained-evidence candidate adapter, filling timing fields, authorizing metric input, or computing metrics.
