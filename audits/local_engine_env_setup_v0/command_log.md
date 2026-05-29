# Command Log

Pre-edit inspection:

```bash
git status -sb
git branch --show-current
git log --oneline -12
```

Read before editing:

```bash
project_control/MIGRATION_MASTER_PLAN.md
project_control/MIGRATION_STATUS.md
project_control/DECISION_LOG.md
tail of project_control/MIGRATION_RUN_LOG.md
project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
src/sql_rewrite_bench/postgres_execution.py
src/sql_rewrite_bench/mysql_execution.py
src/sql_rewrite_bench/spark_execution.py
src/sql_rewrite_bench/engine_execution.py
README.md
docs/USER_BENCHMARK_GUIDE.md
docs/USER_ENTRY_DATA_FLOW.md
```

Validation commands:

```bash
git diff --check
bash -n scripts/env_postgres.example.sh
bash -n scripts/env_mysql.example.sh
bash -n scripts/env_spark.example.sh
bash -n scripts/env_all.example.sh
PYTHONPATH=src python -m py_compile scripts/dev/check_local_engine_env.py
python scripts/dev/check_local_engine_env.py
bash -c 'source scripts/env_all.example.sh'
git check-ignore -v runs/user/
git check-ignore -v runs/
git check-ignore -v scripts/env_mysql.local.sh
git status --short
git diff --name-only
git ls-files --others --exclude-standard
git diff --name-only -- src cases case_sets reports results benchmark_spec repository_spec .github
git ls-files --others --exclude-standard -- src cases case_sets reports results benchmark_spec repository_spec .github
git status --short runs/user
git ls-files runs/user
```

Observed validation results:

- `git diff --check`: passed.
- Shell syntax checks: passed.
- Python compile: passed.
- Local engine check helper: passed, exit code 0.
- `source scripts/env_all.example.sh`: passed and printed set/unset summaries without secrets.
- `runs/user/` ignored: yes, by `runs/.gitignore`.
- Whole `runs/` ignored: no.
- `scripts/env_mysql.local.sh` ignored: yes, by root `.gitignore`.
- Protected source/case/case_set/report/result/spec/workflow surfaces changed: no.
- No `runs/user/` output was created.

Task boundaries:

- Environment setup only.
- No DB execution backend changes.
- No metrics/timing.
- No reports/results updates.
- No case or manifest changes.
- No leaderboard.
