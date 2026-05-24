# SQL-RewriteBench User Benchmark Guide

This guide covers the current B-line user-facing local workbench. The public
facade is `src/cli/`, exposed as `sqlrb user ...` after installation or as
`PYTHONPATH=src python -m cli.main user ...` from a checkout.

User-facing local diagnostic output is exported to the D035 shape:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

The current implementation also creates internal transitional staging under
`runs/user/<run_id>/` before export. That staging path is not the public output
contract and should not be committed.

These commands do not compute official metrics, update paper results, promote
retained evidence, or create leaderboard output.

## Install And Import

From the repository root:

```bash
python -m pip install -e .
sqlrb user show-output-schema
```

Without installation:

```bash
PYTHONPATH=src python -m cli.main user show-output-schema
```

## Minimal Adapter Run

Create a text file containing Common-core case ids:

```text
PERF_0006
PERF_0007
```

Run an adapter over the selected PostgreSQL rows and export D035 local output:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --pool PERF \
  --engines postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --output-root output \
  --run-id demo_run
```

The same command works as `sqlrb user evaluate ...` after editable install.

## Dry Run

Dry-run parses the selected rows and writes local diagnostic output, but does
not invoke the adapter:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --pool PERF \
  --engines postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --output-root output \
  --run-id demo_dry_run \
  --dry-run
```

Dry-run ledger rows keep candidate generation and execution statuses visibly
skipped. They are not official metric inputs.

## Public Smoke

`--smoke` selects the deterministic tiny subset `PERF_0006` and `CONS_0005`
for the requested engine.

Dry-run smoke:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_dry_run \
  --dry-run
```

Adapter-capture smoke:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_dummy_adapter
```

The example adapter copies source SQL to the candidate path. The smoke output
is still local diagnostic output only.

## Readability Commands

These commands do not call adapters, execute databases, run checkers, compute
official metrics, update top-level `reports/` or `results/`, or create
leaderboard output.

List Common-core cases:

```bash
PYTHONPATH=src python -m cli.main user list-cases \
  --case-set common_core_v0 \
  --engines postgres
```

Explain the smoke selection:

```bash
PYTHONPATH=src python -m cli.main user explain-selection \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke
```

Show the output schema:

```bash
PYTHONPATH=src python -m cli.main user show-output-schema
```

Show the local-only boundary:

```bash
PYTHONPATH=src python -m cli.main user show-boundary \
  --output-root output \
  --run-id smoke_dummy_adapter
```

## Adapter Contract

The runner provides these environment variables to each adapter invocation:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

Adapters should read source SQL from `SQLRB_SOURCE_SQL_PATH` and write candidate
SQL to `SQLRB_CANDIDATE_SQL_PATH`. Candidate SQL printed to stdout is also
captured, but a workspace `candidate.sql` file takes precedence.

Route-specific baseline adapters belong under `baselines/`. Public examples
belong under `examples/`. Core reusable implementation remains under
`src/sql_rewrite_bench/`.

## SQLGlot Adapter Example

SQLGlot adapters are optional candidate-generation routes. They do not execute
SQL, run checkers, collect timing, compute official metrics, update retained
evidence, or create leaderboard output.

Install optional SQLGlot support:

```bash
python -m pip install -e ".[sqlglot]"
```

SQLGlot no-op route:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --pool PERF \
  --engines postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root output \
  --run-id sqlglot_noop_demo
```

SQLGlot optimize route:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --pool PERF \
  --engines postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize" \
  --output-root output \
  --run-id sqlglot_optimize_demo
```

If SQLGlot is unavailable or parsing fails, the adapter exits nonzero rather
than silently falling back to raw source SQL.

## Optional PostgreSQL Diagnostics

PostgreSQL DB/checker diagnostics are opt-in:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id postgres_local_diagnostic \
  --enable-db-execution \
  --enable-checker
```

This path resolves PostgreSQL DDL/load files through each case manifest's
`schema.external_profile` and the current `schemas/` directory. Missing schema
metadata fails closed. Configure PostgreSQL with `SQLRB_POSTGRES_DSN` or
standard libpq environment variables.

DB/checker diagnostics are local-only. They do not update top-level
`reports/`, top-level `results/`, retained evidence, paper outputs, or
leaderboard rows.

## Output Directories

The public output contract is:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

The current runner uses `runs/user/<run_id>/` as internal transitional staging
before export. That staging path may contain source-run ledgers, candidate SQL,
workspaces, and summaries. It is not the public output root.

Top-level `reports/` and top-level `results/` are official/paper surfaces and
must not be updated by ordinary user-run tasks.

## Current Physical Layout Boundary

The final D035 public layout targets `benchmarks/` for benchmark data, but the
physical migration is not complete. Current working paths remain valid until a
separate migration task:

- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`

Do not move those directories as part of normal user-run work.

## Current Limits

- Default adapter-capture runs do not execute database queries.
- DB/checker diagnostics are opt-in local diagnostics.
- Timing is opt-in and exact-gated.
- There are no official benchmark metrics in this path.
- Semantic Equivalence Rate is not computed by user adapter runs.
- No paper tables are rendered.
- No retained evidence is updated or promoted.
- No global leaderboard is created.
