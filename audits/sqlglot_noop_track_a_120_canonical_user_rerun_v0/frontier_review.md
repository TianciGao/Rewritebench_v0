# Frontier Review

Source: `runs/user/sqlglot_noop_track_a_120_canonical_v0/metrics/local_metrics_summary.json`

Canonical non-exact frontier from `diagnostic_status_counts`:

| Status family | Counts copied from canonical output |
| --- | --- |
| exact_status | `exact=97`, `mismatch=10`, `not_evaluated_non_db_mvp=5`, `not_exact_due_to_execution_failure=8` |
| failure_bucket | `none=97`, `mismatch=10`, `adapter_failed=5`, `candidate_execution_failed=3`, `unsupported_engine=5` |
| source_execution_status | `source_execution_success=110`, `execution_not_enabled=5`, `execution_unsupported=5` |
| candidate_execution_status | `candidate_execution_success=107`, `candidate_execution_failed=3`, `execution_not_enabled=5`, `execution_unsupported=5` |
| checker_status | `checker_success=97`, `checker_mismatch=10`, `checker_not_enabled=8`, `not_run_non_db_mvp=5` |
| timing_status | `timed=97`, `not_eligible=23` |

Interpretation boundary:
- The 23 non-timed rows remain denominator-visible.
- The 10 mismatches are not treated as exact.
- The 5 label-only mismatches are reported separately by canonical metrics but are not normalized in this task.
- The 5 unsupported fail-closed rows and 5 `unsupported_engine` failure-bucket rows remain visible.
- No verifier evidence was produced, so Semantic Equivalence Rate remains N.A.
