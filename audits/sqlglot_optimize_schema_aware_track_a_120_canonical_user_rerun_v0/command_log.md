# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 9ceb9989acfd18323ac16f83d07fe25c70e6e91b HEAD
python -m cli.main user evaluate --help
python -m cli.main user compute-local-metrics --help
```

Environment checks:

```bash
psql -Atc 'select 1'
MYSQL_PWD="$SQLRB_MYSQL_PASSWORD" mysql -h "$SQLRB_MYSQL_HOST" -P "$SQLRB_MYSQL_PORT" -u "$SQLRB_MYSQL_USER" -N -e 'select 1'
python - <<'PY'
from sql_rewrite_bench.mysql_execution import mysql_config_available
from sql_rewrite_bench.spark_execution import inspect_spark_environment
from sql_rewrite_bench.postgres_execution import postgres_config_available
print(postgres_config_available())
print(mysql_config_available())
print(inspect_spark_environment().summary)
PY
```

Run commands:

```bash
python -m cli.main user evaluate --case-set common_core_v0 --engines postgres,mysql,spark --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware" --output-root /tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_canonical_user_rerun_v0/output --run-id sqlglot_optimize_schema_aware_track_a_120_canonical_v0 --enable-db-execution --enable-checker --collect-timing
python -m cli.main user compute-local-metrics --run-id-prefix sqlglot_optimize_schema_aware_track_a_120_canonical_v0 --engines postgres,mysql,spark --aggregate-run-id sqlglot_optimize_schema_aware_track_a_120_canonical_v0 --source-run-root runs/user --output-root /tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_canonical_user_rerun_v0/output
```

Validation:

```bash
python -m cli.main user compute-local-metrics --help
git diff --check
git status -sb
```
