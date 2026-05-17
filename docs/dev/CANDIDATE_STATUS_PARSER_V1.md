# Candidate Status Parser V1

## Command

Build the approved input manifest:

```bash
python scripts/dev/build_candidate_status_parser_v1_manifest.py \
  --out-dir audits/candidate_status_parser_v1
```

Run the bounded parser:

```bash
python scripts/dev/parse_candidate_status_v1.py \
  --scaffold audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv \
  --manifest audits/candidate_status_parser_v1/candidate_status_parser_v1_input_manifest.csv \
  --out-dir audits/candidate_status_parser_v1
```

Validate the audit ledger:

```bash
python scripts/dev/validate_ledger_csv.py \
  --ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \
  --case-set case_sets/common_core_v0/cases.csv \
  --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/candidate_status_parser_v1/ledger_validation
```

## Scope

`candidate_status_parser_v1` is a bounded non-timing parser for Track-A same-engine `rewrite_candidate_cell` rows. It starts from the 600-row scaffold created by `rewrite_candidate_adapter_v0`.

Approved proposal inputs:

- `P001`
- `P002`
- `P003`
- `P011`
- `P012`

Forbidden inputs:

- `P013`
- deferred rows `P006`, `P007`, `P008`, and `P014`
- rejected route-level, timing/performance, raw-log/debug, or reference-only rows
- any unapproved legacy file

## Approved Fields

The parser may fill only non-timing status fields:

- `generated`
- `ready`
- `executed`
- `exact`
- `result_status`
- `failure_stage`
- `failure_type`
- `parse_status`
- `checker_status`
- `retained_artifact_path`
- `evidence_source`
- `notes`

## Forbidden Fields

The parser must not fill:

- `timed`
- `latency_ms`
- `speedup_ratio`
- `timing_eligible`
- `plan_available`
- `plan_artifact_path`
- attribution fields
- metric outputs

`metric_input_authorized=false` and `metrics_computed=false` remain fixed for every row.

## Fail-closed Behavior

The parser opens only manifest-approved files. If a source row cannot map deterministically to the scaffold row grain, it is rejected or left unmatched. Route-level and aggregate counts are never distributed into row statuses.

## Outputs

Outputs are audit-only under `audits/candidate_status_parser_v1/`:

- `candidate_status_parser_v1_input_manifest.csv`
- `candidate_status_parsed_ledger_v1.csv`
- `candidate_status_parser_v1_summary.json`
- `candidate_status_parser_v1_report.md`
- `candidate_status_parser_v1_checks.csv`
- `candidate_status_parser_v1_input_rejection_log.csv`
- `candidate_status_parser_v1_source_use_log.csv`
- `candidate_status_parser_v1_limitations.md`
- `ledger_validation/`

## Warnings

This output is not a production metrics ledger and is not paper evidence by itself. Metrics are not computed. Timing remains a separate future adapter. Reports/results, denominators, paper results, and raw legacy evidence are not changed.
