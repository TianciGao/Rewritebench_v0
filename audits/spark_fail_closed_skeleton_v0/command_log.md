# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git log --oneline -15
```

Implementation and validation:

```bash
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/spark_execution.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py scripts/dev/check_local_engine_env.py
python scripts/dev/check_local_engine_env.py
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
python scripts/user/run_user_benchmark.py --help
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --smoke --explain-selection
PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema
PYTHONPATH=src pytest tests/user_entry/test_engine_execution_router.py
PYTHONPATH=src python -m unittest tests.user_entry.test_engine_execution_router
PYTHONPATH=src python -m unittest discover -s tests/user_entry
PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py
PYTHONPATH=src python -m unittest discover -s tests/case_package_v2
```

Spark fail-closed smoke:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/spark_fail_closed_smoke \
  --enable-db-execution \
  --enable-checker
```

PostgreSQL/MySQL preservation smokes:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/spark_skeleton_pg_smoke \
  --enable-db-execution \
  --enable-checker

PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine mysql \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/spark_skeleton_mysql_smoke \
  --enable-db-execution \
  --enable-checker
```

Notes:

- `pytest` was unavailable (`command not found`), so the equivalent unittest suite was run and passed.
- A parallel validation attempt was discarded after concurrent test processes raced on temporary `runs/user` directories; serial reruns passed.
- All local run outputs are local diagnostics only and are not committed.
