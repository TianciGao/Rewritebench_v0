# Future U2 Prompt

Task title:
U2 design user-entry resolver adapter-runner ledger split

Purpose:
Design the next module split for the user-entry local diagnostic harness after the U1 output schema audit.

Mode:
Design-only unless separately authorized. Do not implement source-code changes in this prompt without explicit writable implementation approval.

Read first:

- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- `audits/user_entry_output_schema_audit_v0/README.md`
- `audits/user_entry_output_schema_audit_v0/current_ledger_fields.csv`
- `audits/user_entry_output_schema_audit_v0/proposed_user_run_row_schema.csv`
- `audits/user_entry_output_schema_audit_v0/proposed_failure_bucket_policy.md`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/case_selection.py`
- `src/sql_rewrite_bench/user_run_schema.py`

Design scope:

- `case_package_resolver.py`
- `adapter_runner.py`
- `user_ledger.py`
- Typed row/status schema updates needed before U3 preflight
- Migration path from current `user_run.py` without changing behavior

Hard boundaries:

- Do not compute official metrics.
- Do not render paper tables.
- Do not update reports/results.
- Do not parse retained evidence.
- Do not change case_sets, denominators, paper results, case membership, or raw legacy evidence.
- Do not create a global leaderboard.

Expected output:

- A design packet or minimal patch plan that separates responsibilities while preserving current smoke behavior.
- Validation plan covering module help, wrapper help, smoke dry-run, smoke adapter-capture, user-entry tests, and protected-surface checks.
