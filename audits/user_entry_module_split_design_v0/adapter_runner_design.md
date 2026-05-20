# Adapter Runner Design

## Purpose

`adapter_runner.py` should own user adapter invocation and candidate SQL capture. It should preserve current public smoke behavior while removing subprocess and workspace details from `user_run.py`.

The adapter runner is local diagnostic infrastructure only. It must not judge correctness, execute DB queries, run checkers, compute metrics, render paper tables, update reports/results, or create leaderboard rows.

## Environment Variables

The runner must provide the existing adapter environment:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_CASE_DIR`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

Values should be absolute paths for filesystem paths where current behavior already uses absolute paths. The canonical ledger path for captured candidate SQL should remain repository-relative.

## Invocation Contract

Design-only interface: `run_adapter_for_case(...) -> AdapterInvocationResult`.

Inputs:

- `run_id`
- `selected_row`
- `resolved_package`
- `adapter_command`
- `repo_root`
- `out_dir`
- `timeout_sec`

Invocation rules:

- Parse `adapter_command` with `shlex.split`.
- Invoke with `subprocess.run(..., shell=False)`.
- Set `cwd` to repository root.
- Capture stdout and stderr.
- Write stdout to `workspaces/{case_id}/{engine}/adapter_stdout.txt`.
- Write stderr to `workspaces/{case_id}/{engine}/adapter_stderr.txt`.
- Use `workspaces/{case_id}/{engine}/candidate.sql` as the adapter-provided candidate file path.
- Fail closed on timeout, empty command, subprocess exceptions, or non-zero exit.

## Candidate Capture Priority

Preserve current behavior:

1. If workspace `candidate.sql` exists and has non-whitespace content, copy it to `candidate_sql/{case_id}__{engine}.sql`.
2. Else if adapter stdout has non-whitespace content, write stdout to `candidate_sql/{case_id}__{engine}.sql`.
3. Else record `candidate_generated=false` and `extraction_status=no_candidate_sql`.

Workspace `candidate.sql` remains higher priority than stdout.

## Stdout/Stderr Handling

The adapter runner writes:

- `adapter_stdout.txt`
- `adapter_stderr.txt`

Stdout may be both diagnostic output and candidate SQL fallback. If workspace `candidate.sql` is present, stdout is preserved as an artifact but not used as candidate SQL.

## Workspace Layout

Per-row workspace:

```text
runs/user/{run_name}/workspaces/{case_id}/{engine}/
  candidate.sql
  adapter_stdout.txt
  adapter_stderr.txt
```

Canonical candidate capture:

```text
runs/user/{run_name}/candidate_sql/{case_id}__{engine}.sql
```

The adapter runner must not write outside `runs/user/{run_name}/`.

## Status Outputs

Design-only interface: `AdapterInvocationResult`.

Fields:

- `adapter_invoked`
- `adapter_exit_code`
- `adapter_status`
- `candidate_generated`
- `candidate_capture_mode`
- `candidate_sql_path`
- `workspace_dir`
- `adapter_stdout_path`
- `adapter_stderr_path`
- `artifact_path`
- `failure_bucket_hint`
- `notes`

Current status mapping:

- non-zero exit -> `adapter_failed`
- timeout -> `adapter_timeout`
- file capture -> `captured_from_candidate_file`
- stdout capture -> `captured_from_stdout`
- no candidate -> `no_candidate_sql`
- dry-run -> adapter runner not invoked; `user_run.py` or `user_ledger.py` creates the dry-run row.

## Non-Goals

- SQL parsing or safety checks.
- Source-like/no-op detection.
- DB execution.
- Checker execution.
- Semantic correctness.
- Performance or timing.
- Official metric computation.
- Paper/reports/results output.
