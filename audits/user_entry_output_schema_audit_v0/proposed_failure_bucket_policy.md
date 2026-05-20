# Proposed Failure Bucket Policy

## Purpose

This is a proposed local diagnostic failure-bucket policy for future user-entry work. It is not an implementation and not an official paper metric policy.

Failure buckets explain where a local user-run row stopped in the diagnostic funnel. They must not change Common-core membership, denominator values, paper results, reports/results, retained evidence, or official metrics.

## Proposed priority

Apply the first matching bucket in this order:

1. `selection_failed`
2. `adapter_failed`
3. `candidate_missing`
4. `candidate_preflight_failed`
5. `source_execution_failed`
6. `candidate_execution_failed`
7. `checker_failed`
8. `mismatch`
9. `source_like_or_noop`
10. `none`

## Current fields available

- `selected`, `planned`, `denominator_id`, `case_id`, `pool`, and `engine` support selected-row accounting.
- `adapter_invoked`, `adapter_exit_code`, and `extraction_status` support adapter and candidate-capture failures.
- `candidate_generated` and `candidate_sql_path` support candidate-missing detection.
- `execution_enabled`, `execution_status`, `source_execution_status`, and `candidate_execution_status` support local DB execution diagnostics.
- `checker_enabled`, `checker_status`, `exact_status`, and `checker_failure_class` support local checker diagnostics.
- `failure_bucket` already stores one primary local bucket.
- `notes` and `artifact_path` provide supporting human diagnostics.

## Missing before implementation

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

## Bucket derivation notes

- `selection_failed` should represent row resolution failures before a selected row exists. It may require a run-level failure file because no normal ledger row may exist.
- `adapter_failed` should cover non-zero adapter exit and adapter timeout.
- `candidate_missing` should cover successful adapter invocation without candidate SQL.
- `candidate_preflight_failed` should cover static candidate checks before DB execution.
- `source_execution_failed` should outrank candidate execution failures because source-as-oracle execution is required for local comparison.
- `candidate_execution_failed` should cover candidate DB failures after source execution succeeds.
- `checker_failed` should cover missing checker config, normalization config, checker internal error, and checker timeout.
- `mismatch` should mean local result comparison mismatch only.
- `source_like_or_noop` should be diagnostic and lower priority than execution/checker failures.
- `none` should mean the row reached the highest enabled local diagnostic stage without failure.

## Boundary

This is local diagnostic failure accounting only. It is not official Generation Rate, Execution Coverage Rate, Result Consistency Rate, Semantic Equivalence Rate, timing, paper rendering, or leaderboard logic.
