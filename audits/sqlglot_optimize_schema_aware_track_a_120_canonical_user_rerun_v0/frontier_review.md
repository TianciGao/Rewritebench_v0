# Frontier Review

Source: `metrics/local_metrics_summary.json` diagnostic status counts.

Canonical exact status counts:

- exact: 66
- mismatch: 25
- not_evaluated_non_db_mvp: 15
- not_exact_due_to_execution_failure: 14

Canonical failure bucket counts:

- none: 66
- mismatch: 25
- adapter_failed: 14
- candidate_execution_failed: 9
- unsupported_engine: 5
- no_candidate_sql: 1

Canonical execution/checker status counts:

- source_execution_success: 100
- execution_not_enabled: 15
- execution_unsupported: 5
- candidate_execution_success: 91
- candidate_execution_failed: 9
- checker_success: 66
- checker_mismatch: 25
- checker_not_enabled: 14
- not_run_non_db_mvp: 15

Canonical timing status counts:

- timed: 66
- not_eligible: 54

The non-exact frontier remains denominator-visible. It was not normalized, verifier-checked, or promoted.
