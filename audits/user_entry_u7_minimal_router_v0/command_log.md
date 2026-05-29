# Command Log

## Preflight

- `git status -sb`: clean worktree before edits.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -10`: reviewed latest branch history.

## Implementation Validation

- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/mysql_execution.py src/sql_rewrite_bench/spark_execution.py src/sql_rewrite_bench/user_run.py`: passed.
- `PYTHONPATH=src pytest tests/user_entry/test_engine_execution_router.py tests/user_entry/test_candidate_preflight.py -q`: passed, 18 tests.
- `PYTHONPATH=src pytest tests/user_entry -q`: passed, 70 passed and 1 skipped.

## Required Validation

- `git diff --check`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --list-cases`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --explain-selection`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u7_router_dry_run --dry-run`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u7_router_dummy_adapter`: passed.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 70 passed and 1 skipped.
- Protected-surface check: passed.
- Run-output cleanup: passed; `runs/user/u7_router_dry_run` and `runs/user/u7_router_dummy_adapter` removed before commit.
