# Command Log

Preflight:

```bash
git status -sb
find project_control -maxdepth 1 -type f -print | sort
git merge-base --is-ancestor a5fbd54 HEAD
test -f src/sql_rewrite_bench/user_output.py
test -d audits/user_output_writer_phase2a_v0
```

Read/inspection:

```bash
sed -n '1,260p' tests/user_entry/test_cli_facade.py
sed -n '1,320p' src/cli/main.py
sed -n '1,220p' src/sql_rewrite_bench/user_output.py
```

Environment checks:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
python scripts/dev/check_local_engine_env.py
PYTHONPATH=src python -c "import sqlglot; print(sqlglot.__version__)"
```

Validation:

```bash
PYTHONPATH=src pytest tests/user_entry/test_cli_facade.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile src/cli/__init__.py src/cli/__main__.py src/cli/main.py src/sql_rewrite_bench/user_output.py
PYTHONPATH=src python -m cli.main user show-output-schema
PYTHONPATH=src python -m cli.main user show-boundary
python - <<'PY'  # project-control readability
from pathlib import Path
for path in [
    Path('project_control/MIGRATION_MASTER_PLAN.md'),
    Path('project_control/MIGRATION_STATUS.md'),
    Path('project_control/MIGRATION_RUN_LOG.md'),
    Path('project_control/DECISION_LOG.md'),
]:
    assert path.read_text(encoding='utf-8').strip()
PY
python - <<'PY'  # audit Markdown sanity
from pathlib import Path
for path in sorted(Path('audits/user_cli_facade_phase2b_v0').glob('*.md')):
    assert path.read_text(encoding='utf-8').strip()
PY
git diff --check
```

Bounded CLI smoke:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root /tmp/<temp>/output \
  --run-id phase2b_cli_smoke_pg_<timestamp> \
  --smoke \
  --enable-db-execution \
  --enable-checker
```

The smoke runtime directories were removed after result inspection.
