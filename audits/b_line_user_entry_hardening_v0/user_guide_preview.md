# SQL-RewriteBench User Runner MVP Guide Preview

This preview describes the current non-DB user-entry MVP. It is construction documentation, not final public release documentation.

## Minimal Command

Run from the repository root:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list /path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_run
```

Equivalent thin wrapper:

```bash
python scripts/user/run_user_benchmark.py \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list /path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_run
```

The output path must be under `runs/user/<run_id>/`.

## Dry-run Example

Dry-run resolves selected rows and writes local run files without invoking the adapter:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list /path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_dry_run \
  --dry-run
```

Dry-run ledger rows use `adapter_invoked=false`, `candidate_generated=false`, and `extraction_status=skipped_dry_run`.

## Dummy Adapter Example

The test fixture adapter writes deterministic candidate SQL to the path supplied by the runner:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list /path/to/case_ids.txt \
  --adapter-command "python tests/user_entry/fixtures/dummy_adapter.py" \
  --out runs/user/demo_dummy_adapter
```

Adapters may either write `candidate.sql` to `SQLRB_CANDIDATE_SQL_PATH` or print candidate SQL to stdout. Workspace `candidate.sql` takes precedence when both are present.

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

## Output Files

Each run writes under `runs/user/<run_id>/`:

- `config.yaml`
- `selected_cases.csv`
- `candidate_sql/`
- `workspaces/`
- `ledger.csv`
- `summary.json`
- `failures.csv`
- `report.md`

These are local user-run artifacts. They are ignored by git through `runs/.gitignore` and should not be staged.

## Current Limitations

- No DB execution.
- No checker execution.
- No timing collection.
- No official benchmark metrics.
- No paper table rendering.
- No paper result updates.
- No retained evidence updates.
- No leaderboard.
- No non-Common-core selection in the MVP.

User-run outputs are not retained paper evidence and must not be written into case-local `runs/`, `reports/`, `results/`, `case_sets/`, inventory, or case packages.
