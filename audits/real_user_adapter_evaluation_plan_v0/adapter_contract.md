# Adapter Contract

The user-entry runner invokes one adapter command per selected case-engine row. The adapter is responsible only for producing candidate SQL; it must not execute SQL, run the checker, compute metrics, update reports/results, write retained evidence, or create leaderboard artifacts.

## Command Interface

The runner accepts an adapter command through `--adapter-command`, for example:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --case-list /tmp/sqlrb_real_adapter_smoke_pg.txt \
  --adapter-command "python path/to/user_adapter.py" \
  --out runs/user/<run_name> \
  --enable-db-execution \
  --enable-checker
```

The command is split by shell-like syntax and executed from the repository root. The runner captures stdout, stderr, exit code, timeout status, and candidate SQL artifacts.

## Environment Variables

The runner supplies:

- `SQLRB_RUN_ID`: local run identifier.
- `SQLRB_CASE_ID`: selected case id.
- `SQLRB_POOL`: case pool.
- `SQLRB_ENGINE`: selected target engine.
- `SQLRB_SOURCE_SQL_PATH`: resolved source SQL path.
- `SQLRB_CASE_DIR`: resolved case package directory.
- `SQLRB_WORKSPACE_DIR`: per-row adapter workspace under `runs/user/{run_name}/workspaces/{case_id}/{engine}/`.
- `SQLRB_CANDIDATE_SQL_PATH`: preferred candidate SQL output path inside the workspace.

Adapters may read these variables and repository files needed to generate a candidate. Adapters should write only to `SQLRB_CANDIDATE_SQL_PATH` or their workspace-local artifacts.

## Candidate SQL Output

Preferred output is a non-empty SQL file at `SQLRB_CANDIDATE_SQL_PATH`. If that file is absent or empty and the adapter exits successfully, non-empty stdout is captured as candidate SQL. The workspace candidate file takes precedence over stdout.

The runner copies the captured candidate into `runs/user/{run_name}/candidate_sql/{CASE_ID}__{engine}.sql` for the local run. Candidate SQL then proceeds to preflight, optional DB execution, and optional checker comparison.

## Stdout and Stderr

The runner records adapter stdout and stderr under the per-row workspace. Stdout is candidate SQL only when no non-empty `SQLRB_CANDIDATE_SQL_PATH` file exists and the adapter exits successfully. Stderr is diagnostic text and must not be parsed as candidate SQL.

## Failure and Timeout Behavior

- Non-zero adapter exit: `adapter_failed`; SQL is not evaluated.
- Adapter timeout: `adapter_timeout`; SQL is not evaluated.
- Successful adapter with no candidate SQL: `no_candidate_sql`; SQL is not evaluated.
- Candidate generated but preflight fails: `candidate_preflight_failed`; DB execution is not a method success.
- Candidate generated and preflight passes but source or candidate SQL execution fails: source/candidate execution failure, not adapter invocation failure.
- Checker mismatch after both sides execute: semantic/result mismatch under local checker policy, not adapter command failure.

This separation is required so adapter reliability, SQL validity, engine executability, and result equivalence remain distinguishable.
