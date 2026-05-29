# Command Log

## Preflight

```bash
git status -sb
git branch --show-current
git log --oneline -10
```

Result: clean worktree on `feature/case-package-v2-external-schema` before edits.

## Implementation Validation

```bash
PYTHONPATH=src python -m py_compile \
  src/sql_rewrite_bench/candidate_preflight.py \
  src/sql_rewrite_bench/user_run.py \
  src/sql_rewrite_bench/user_ledger.py \
  src/sql_rewrite_bench/user_run_schema.py
```

Result: passed.

```bash
PYTHONPATH=src pytest tests/user_entry
```

Result: passed, 52 passed and 1 skipped.

## Final Validation

```bash
git diff --check
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/candidate_preflight.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
python scripts/user/run_user_benchmark.py --help
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u3_preflight_dry_run --dry-run
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u3_preflight_dummy_adapter
PYTHONPATH=src pytest tests/user_entry
```

Result: passed.

## Cleanup

```bash
rm -rf runs/user/u3_preflight_dry_run runs/user/u3_preflight_dummy_adapter
```

Result: task-created smoke outputs removed before commit.
