# Candidate Status Parser v0

Developer-facing note. This is not public runner documentation.

## Purpose

`candidate_status_parser_v0` is a manifest-first, bounded non-timing parser for Track-A same-engine `rewrite_candidate_cell` rows.

It is allowed to fill candidate status fields only when an explicit input manifest approves a row-level source with exact grain:

`case_id x engine x rewrite_method x candidate_id x denominator_id`

Current expected behavior is fail-closed: no approved row-level inputs are present, so the parser emits 600 unresolved rows.

## Build Manifest

```bash
python scripts/dev/build_candidate_status_parser_input_manifest.py \
  --out-dir audits/candidate_status_parser_v0
```

The manifest builder reads only release-repo locator and mapping metadata. It does not open legacy files and does not parse retained evidence.

## Run Parser

```bash
python scripts/dev/parse_candidate_status_from_manifest.py \
  --scaffold audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv \
  --manifest audits/candidate_status_parser_v0/candidate_status_parser_input_manifest.csv \
  --out-dir audits/candidate_status_parser_v0
```

## Approved Fields

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

- `timed`
- `latency_ms`
- `speedup_ratio`
- `timing_eligible`
- `plan_available`
- `plan_artifact_path`
- attribution fields
- `metric_input_authorized=true`
- any metric output

## Fail-closed Behavior

If no approved row-level source exists, or if a source fails row-grain validation, the parser emits unresolved rows and exits successfully because the safe no-op behavior is expected.

The parser must not distribute route-level counts into row-level statuses.

## Outputs

- `audits/candidate_status_parser_v0/candidate_status_parser_input_manifest.csv`
- `audits/candidate_status_parser_v0/candidate_status_parsed_ledger_v0.csv`
- `audits/candidate_status_parser_v0/candidate_status_parser_v0_summary.json`
- `audits/candidate_status_parser_v0/candidate_status_parser_v0_report.md`
- `audits/candidate_status_parser_v0/candidate_status_parser_v0_checks.csv`
- `audits/candidate_status_parser_v0/candidate_status_parser_input_rejection_log.csv`

These outputs are audit-only. They are not production ledger files and are not paper evidence by themselves.

## Validation

```bash
python scripts/dev/validate_ledger_csv.py \
  --ledger audits/candidate_status_parser_v0/candidate_status_parsed_ledger_v0.csv \
  --case-set case_sets/common_core_v0/cases.csv \
  --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/candidate_status_parser_v0/ledger_validation
```

## Boundaries

- Metrics are not computed.
- Timing remains separate.
- Reports/results are not updated.
- Denominators are not changed.
- Paper results are not changed.
- Production ledger promotion requires separate authorization.
