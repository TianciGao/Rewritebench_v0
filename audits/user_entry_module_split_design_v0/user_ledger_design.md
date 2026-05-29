# User Ledger Design

## Purpose

`user_ledger.py` should own local diagnostic row consolidation and CSV writing. It should convert selection, resolver, adapter, execution, checker, and future preflight/timing results into typed local rows.

It must not execute DB queries, run checkers, invoke adapters, compute official metrics, render paper tables, update reports/results, or create leaderboard rows.

## Row Construction Model

Design-only interface: `UserLedgerRow`.

Row construction should be staged:

1. Start from selected row metadata.
2. Add resolver status and package paths.
3. Add adapter invocation and candidate capture result.
4. Add optional future preflight result.
5. Add optional DB execution result.
6. Add optional checker result.
7. Add optional future timing status.
8. Apply failure-bucket priority.
9. Enforce local-only boundary flags.
10. Write `ledger.csv` and `failures.csv`.

Dry-run rows should be assembled without invoking `adapter_runner.py`.

## Current Fields From U1

Current `ledger.csv` fields already cover:

- selection identity: `run_id`, `case_id`, `pool`, `engine`, `denominator_id`, `planned`, `selected`
- adapter/candidate capture: `adapter_invoked`, `adapter_exit_code`, `candidate_generated`, `candidate_sql_path`, `extraction_status`
- local execution/checker statuses: `execution_status`, `checker_status`, `exact_status`, `timed_status`
- failure accounting: `failure_bucket`, `execution_failure_class`, `checker_failure_class`
- artifacts: `artifact_path`, `source_result_path`, `candidate_result_path`, `mismatch_artifact_path`, `db_artifact_dir`
- checker paths: `checker_config_path`, `normalization_config_path`, `compare_config_path`
- boundaries: `local_execution_only`, `official_metric_input`, `retained_evidence_input`

Current `failures.csv` fields cover:

- `run_id`
- `case_id`
- `pool`
- `engine`
- `denominator_id`
- `failure_bucket`
- `artifact_path`
- `notes`

## Proposed Row Fields From U1

Fields needed later but not required for the minimal split include:

- `resolver_status`
- `resolver_failure_class`
- `candidate_preflight_attempted`
- `candidate_preflight_passed`
- `candidate_preflight_status`
- `preflight_failure_class`
- `source_like_status`
- `nontrivial_candidate`
- `db_execution_attempted`
- `source_executable`
- `candidate_executable`
- `checker_attempted`
- `failure_priority_rank`
- `tag_axes`
- `tag_values`
- `timing_attempted`
- `raw_timing_artifact_path`

The minimal split should avoid schema churn unless tests explicitly cover it. New fields can be introduced in later phases.

## Failure Bucket Priority

Future policy priority:

1. `selection_failed`
2. `resolver_failed`
3. `adapter_failed`
4. `candidate_missing`
5. `candidate_preflight_failed`
6. `source_execution_failed`
7. `candidate_execution_failed`
8. `checker_failed`
9. `mismatch`
10. `source_like_or_noop`
11. `none`

For minimal extraction, `user_ledger.py` may preserve current bucket values while centralizing the decision logic. Adding `resolver_failed`, `candidate_preflight_failed`, and `source_like_or_noop` should wait until the owning phases exist.

## Output Files

Current outputs to preserve:

- `ledger.csv`
- `failures.csv`
- `summary.json`
- `report.md`

The minimal split should move only ledger/failure row writing first. Summary/report generation can remain in `user_run.py` until `user_quality_report.py` is authorized.

## Local-Only Boundary Flags

Every user-run ledger row must preserve:

- `local_execution_only=true`
- `official_metric_input=false`
- `retained_evidence_input=false`

Run summary/config must preserve:

- `official_metrics_computed=false`
- `paper_results_updated=false`
- `retained_evidence_updated=false`
- `no_global_leaderboard=true`

## Non-Goals

- Official metric computation.
- Paper table rendering.
- Report/result migration.
- Retained evidence promotion.
- DB/checker execution.
- Candidate preflight.
- Tag slicing.
- Timing diagnostics.
- Global leaderboard.
