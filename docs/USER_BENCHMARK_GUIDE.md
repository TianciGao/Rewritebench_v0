# SQL-RewriteBench User Benchmark Guide

This guide covers the current B-line user-entry MVP. The MVP is a non-DB adapter-capture runner: it lets a user run a SQL rewrite adapter over selected Common-core v0 case-engine rows and stores local experiment outputs under `runs/user/<run_id>/`.

The MVP does not score a full benchmark run. It does not execute SQL, run checkers, collect timing, compute official metrics, update paper results, update retained evidence, or create a leaderboard.

## Installation And Imports

For local development, use the repository root as the working directory.

With editable packaging:

```bash
python -m pip install -e .
python -m sql_rewrite_bench.user_run --help
```

Without installation:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
```

The thin wrapper is also available:

```bash
python scripts/user/run_user_benchmark.py --help
```

## Minimal Command

Create a text file containing Common-core case ids, for example:

```text
PERF_0006
PERF_0007
```

Run an adapter over those selected rows:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_run
```

Equivalent wrapper command:

```bash
python scripts/user/run_user_benchmark.py \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_run
```

## Dry-run Example

Dry-run resolves selected rows and writes the local run files without invoking the adapter:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_dry_run \
  --dry-run
```

Dry-run ledger rows use:

- `adapter_invoked=false`
- `candidate_generated=false`
- `extraction_status=skipped_dry_run`
- `execution_status=not_run_non_db_mvp`
- `checker_status=not_run_non_db_mvp`
- `exact_status=not_evaluated_non_db_mvp`
- `timed_status=not_timed_non_db_mvp`
- `failure_bucket=none`

## Dummy Adapter Example

The test fixture adapter writes deterministic candidate SQL to the path supplied by the runner:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python tests/user_entry/fixtures/dummy_adapter.py" \
  --out runs/user/demo_dummy_adapter
```

Adapters can produce candidate SQL in either of two ways:

- Write candidate SQL to the file path in `SQLRB_CANDIDATE_SQL_PATH`.
- Print candidate SQL to stdout.

If both are present, workspace `candidate.sql` takes precedence over stdout.

## Adapter Environment Variables

The runner provides these variables to each adapter invocation:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

The adapter command is invoked with `shell=False` using `shlex.split`. The subprocess working directory is the repository root.

## Output Directory Rule

The output root must be under:

```text
runs/user/<run_id>/
```

The runner rejects case-local paths, `reports/`, `results/`, absolute paths, and parent-relative paths such as `../demo`.

User-run outputs are local experiment outputs only. They are not retained paper evidence and should not be committed.

## Output Files

Each run writes:

- `config.yaml`: command arguments, selected scope, output policy flags, and no-leaderboard/no-paper boundary flags.
- `selected_cases.csv`: the selected Common-core case-engine rows after metadata resolution.
- `candidate_sql/`: captured user-generated candidate SQL, when produced.
- `workspaces/`: per-row adapter stdout/stderr diagnostics and workspace files.
- `ledger.csv`: one local diagnostic row per selected case-engine row.
- `summary.json`: local diagnostic counts and boundary flags.
- `failures.csv`: rows whose `failure_bucket` is not `none`.
- `report.md`: local report with selected scope, diagnostic funnel, failure buckets, artifact links, and warnings.

## Current Limitations

- No DB execution.
- No checker execution.
- No timing collection.
- No official benchmark metrics.
- No paper table rendering.
- No paper result updates.
- No retained evidence updates.
- No leaderboard.
- No SQLGlot, Calcite, or R-Bot baseline adapter implementation.
- No paper reproduction CLI.
- No non-Common-core selection in the MVP.

User-run outputs must not be written into `cases/`, case-local `runs/`, `case_sets/`, `inventory/`, `reports/`, or `results/`.
