# SQL-RewriteBench User Benchmark Guide

This guide covers the current B-line user-entry surface. The supported public smoke/default path is a non-DB adapter-capture runner: it lets a user run a SQL rewrite adapter over selected Common-core v0 case-engine rows and stores local experiment outputs under `runs/user/<run_id>/`. Optional PostgreSQL diagnostics are described separately below.

The default public path does not score a full benchmark run. It does not execute SQL, run checkers, collect timing, compute official metrics, update paper results, update retained evidence, or create a leaderboard.

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

## Public Smoke Example

Use `--smoke` for a deterministic tiny Common-core selection. It selects `PERF_0006` and `CONS_0005` for the requested engine and does not require a case-list file.

Dry-run smoke does not invoke the adapter:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/smoke_dry_run \
  --dry-run
```

Adapter-capture smoke invokes the public no-op example adapter:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/smoke_dummy_adapter
```

The example adapter copies the source SQL to the candidate path. These smoke outputs remain local diagnostics only.

## Adapter Example

The public no-op example adapter writes deterministic candidate SQL to the path supplied by the runner:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/demo_noop_adapter
```

Adapters can produce candidate SQL in either of two ways:

- Write candidate SQL to the file path in `SQLRB_CANDIDATE_SQL_PATH`.
- Print candidate SQL to stdout.

If both are present, workspace `candidate.sql` takes precedence over stdout.

## Optional SQLGlot Adapter Examples

The repository includes optional SQLGlot user-entry adapters for candidate generation only. They do not execute SQL, run checkers, collect timing, compute official metrics, update paper results, update retained evidence, or create a leaderboard.

Dry-run does not require SQLGlot because the adapter is not invoked:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/sqlglot_noop_dry_run \
  --dry-run
```

Install optional SQLGlot support before running the real adapter routes:

```bash
python -m pip install -e ".[sqlglot]"
```

SQLGlot no-op route:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/sqlglot_noop_demo
```

SQLGlot optimize route:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize" \
  --out runs/user/sqlglot_optimize_demo
```

Both routes write candidate SQL to the per-row user-run workspace path supplied by `SQLRB_CANDIDATE_SQL_PATH`. If SQLGlot is unavailable or parsing fails, the adapter exits nonzero instead of silently falling back to raw source SQL.

## Optional Local PostgreSQL Diagnostics

The runner also exposes optional PostgreSQL DB/checker diagnostics:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/postgres_local_diagnostic \
  --enable-db-execution \
  --enable-checker
```

This mode is local diagnostic support only. It resolves PostgreSQL DDL/load files through each case manifest's `schema.external_profile` and the external schema package under `schemas/`. It fails closed if the external schema profile or PostgreSQL DDL/load paths are missing. It requires local PostgreSQL configuration through `SQLRB_POSTGRES_DSN` or standard libpq environment variables, plus the `psql` CLI.

DB/checker diagnostic outputs remain under `runs/user/<run_id>/`. They are not official metrics, retained evidence, reports, results, paper outputs, or leaderboard rows.

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

- Default public smoke and adapter-capture commands do not execute DB queries.
- Default public smoke and adapter-capture commands do not run checkers.
- No timing collection.
- No official benchmark metrics.
- No paper table rendering.
- No paper result updates.
- No retained evidence updates.
- No leaderboard.
- SQLGlot adapters are candidate-generation only and optional.
- No Calcite or R-Bot baseline adapter implementation.
- No paper reproduction CLI.
- No non-Common-core selection in the MVP.

Optional local PostgreSQL diagnostics are not full paper reproduction and do not change any official benchmark result.

User-run outputs must not be written into `cases/`, case-local `runs/`, `case_sets/`, `inventory/`, `reports/`, or `results/`.
