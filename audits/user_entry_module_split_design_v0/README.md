# User-Entry Module Split Design v0

## Purpose

This U2 design packet defines a behavior-preserving split of the current user-entry runner into three focused modules:

- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/adapter_runner.py`
- `src/sql_rewrite_bench/user_ledger.py`

The design follows `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md` and the U1 output schema audit under `audits/user_entry_output_schema_audit_v0/`.

## Verdict

Verdict: `ready_for_minimal_split`.

The current user-entry schema and tests are sufficient for a narrow extraction of resolver, adapter runner, and ledger writer responsibilities. The split should preserve module help, wrapper help, public `--smoke --dry-run`, public `--smoke` adapter-capture, output-root restrictions, and current local diagnostic output files.

The split must not add candidate preflight, quality reports, tag slicing, timing diagnostics, official metrics, paper rendering, reports/results updates, retained-evidence promotion, or leaderboard output.

## Design Summary

- `case_package_resolver.py` resolves case package assets from selected rows and manifests, including source SQL, reference SQL paths, schema profile, external schema profile, checker config paths, and future taxonomy/tag references.
- `adapter_runner.py` owns adapter environment construction, `shell=False` invocation, stdout/stderr capture, workspace layout, and candidate SQL capture priority.
- `user_ledger.py` owns typed row assembly, failure-bucket priority application, `ledger.csv`, `failures.csv`, and local-only boundary flags.
- `user_run.py` remains the CLI/orchestrator and should delegate to the new modules instead of becoming a metrics or paper-reproduction runner.

## Local Diagnostic Boundary

This packet is design-only. It does not modify source code and does not execute DB/checker diagnostics. User-run outputs remain local diagnostics under `runs/user/{run_name}/`; they are not official metrics, paper tables, retained evidence, reports/results updates, or leaderboard rows.

## Next Safe Action

Authorize a minimal implementation task that extracts only resolver, adapter-runner, and ledger-writer modules while preserving current behavior and running the validation gates in `validation_plan.md`.
