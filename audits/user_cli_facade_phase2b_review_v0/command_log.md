# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git merge-base --is-ancestor 5344770 HEAD
test -f src/cli/__init__.py
test -f src/cli/__main__.py
test -f src/cli/main.py
test -f src/sql_rewrite_bench/user_output.py
test -d audits/user_cli_facade_phase2b_v0
rg -n "D034|D035|user_cli_facade_phase2b_v0|Pending" project_control/DECISION_LOG.md project_control/MIGRATION_RUN_LOG.md project_control/MIGRATION_STATUS.md
```

Review:

```bash
sed -n '1,260p' src/cli/main.py
sed -n '260,520p' src/cli/main.py
sed -n '1,260p' tests/user_entry/test_cli_facade.py
sed -n '1,220p' repository_spec/user_output_contract_v0_draft.md
sed -n '1,220p' src/sql_rewrite_bench/user_output.py
sed -n '1,220p' src/sql_rewrite_bench/local_metrics.py
for cmd in evaluate list-cases explain-selection show-output-schema show-boundary compute-local-metrics summarize; do
  PYTHONPATH=src python -m cli.main user "$cmd" --help
done
```

Bounded smoke:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
python scripts/dev/check_local_engine_env.py
python -c "import sqlglot; print(sqlglot.__version__)"
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root /tmp/<temp>/output \
  --run-id phase2b_review_cli_smoke_pg_<timestamp> \
  --smoke \
  --enable-db-execution \
  --enable-checker
```

Validation:

```bash
PYTHONPATH=src pytest tests/user_entry/test_cli_facade.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile src/cli/__init__.py src/cli/__main__.py src/cli/main.py
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
python - <<'PY'  # audit Markdown/CSV sanity
from pathlib import Path
for path in sorted(Path('audits/user_cli_facade_phase2b_review_v0').glob('*')):
    if path.suffix in {'.md', '.csv'}:
        assert path.read_text(encoding='utf-8').strip()
PY
git diff --check
```
