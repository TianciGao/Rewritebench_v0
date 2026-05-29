# Test Results

## Commands Run

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
python scripts/user/run_user_benchmark.py --help
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u2_split_dry_run --dry-run
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u2_split_dummy_adapter
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest tests/user_entry -q
```

## Results

- Module help: passed.
- Wrapper help: passed.
- Public smoke dry-run: passed with `selected_rows=2` and `candidate_generated_rows=0`.
- Public smoke adapter-capture: passed with `selected_rows=2` and `candidate_generated_rows=2`.
- User-entry tests: passed with 39 passed and 1 skipped.

## Added Coverage

- Resolver resolves smoke cases `PERF_0006` and `CONS_0005`.
- Resolver fails closed on missing required package assets.
- Adapter runner exposes required environment variables.
- Adapter runner preserves workspace `candidate.sql` before stdout.
- Adapter runner handles non-zero exit and timeout status.
- Ledger writer preserves current `ledger.csv` and `failures.csv` columns.
- Public smoke dry-run behavior remains unchanged.
- Output-root and public smoke adapter-capture behavior remain covered by existing tests.

## Cleanup

Removed required smoke output directories:

- `runs/user/u2_split_dry_run`
- `runs/user/u2_split_dummy_adapter`
