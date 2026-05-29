# Command Log

Preflight:
- `git status -sb`
- `git branch --show-current`
- `git status --porcelain -- runs/user output reports results`
- `git fetch origin main feature/case-package-v2-external-schema`
- `git merge-base --is-ancestor 3d6fecb3d866ced681a354c9abafb063f4e181ac HEAD`
- `git show origin/main:project_control/MIGRATION_MASTER_PLAN.md | wc -l`
- `git show origin/main:project_control/MIGRATION_STATUS.md | wc -l`
- `git show origin/main:project_control/DECISION_LOG.md | wc -l`
- `git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md | wc -l`
- `git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md | wc -l`
- `git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md | wc -l`
- `rg -n "D033|D034|D035" project_control/DECISION_LOG.md`
- `python -m cli.main user evaluate --help`
- `python -m cli.main user compute-local-metrics --help`
- `source scripts/env_postgres.local.sh && psql -v ON_ERROR_STOP=1 -c 'SELECT 1;'`
- `source scripts/env_mysql.local.sh && MYSQL_PWD="$SQLRB_MYSQL_PASSWORD" mysql -h "$SQLRB_MYSQL_HOST" -P "$SQLRB_MYSQL_PORT" -u "$SQLRB_MYSQL_USER" -e 'SELECT 1;'`
- `source scripts/env_spark.local.sh && python - <<'PY' ... SparkSession SELECT 1 ... PY`

Canonical run:
- `source scripts/env_postgres.local.sh && source scripts/env_mysql.local.sh && source scripts/env_spark.local.sh && python -m cli.main user evaluate --case-set common_core_v0 --engines postgres,mysql,spark --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --output-root /tmp/sqlrb_sqlglot_noop_track_a_120_canonical_user_rerun_v0/output --run-id sqlglot_noop_track_a_120_canonical_v0 --enable-db-execution --enable-checker --collect-timing`
- `python -m cli.main user compute-local-metrics --run-id-prefix sqlglot_noop_track_a_120_canonical_v0 --engines postgres,mysql,spark --aggregate-run-id sqlglot_noop_track_a_120_canonical_v0 --source-run-root runs/user --output-root /tmp/sqlrb_sqlglot_noop_track_a_120_canonical_user_rerun_v0/output`

Validation:
- `python - <<'PY' ... parse canonical metrics JSON/CSV ... PY`
- `python -m cli.main user compute-local-metrics --help`
- `git diff --check`
- `git status -sb`
- `git status --porcelain -- runs/user output reports results`
