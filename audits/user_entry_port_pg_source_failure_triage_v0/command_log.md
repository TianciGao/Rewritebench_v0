# Command Log

Initial repository checks:

```bash
git status -sb
git branch --show-current
git log --oneline -12
```

Context read:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md` tail
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/*`
- current user-entry execution/checker/ledger/report/tag modules
- target case READMEs, manifests, source SQL, positive SQL, and dialect-variant inventories
- target external schema profiles

PostgreSQL environment checks:

```bash
command -v psql
psql --version
psql -X -v ON_ERROR_STOP=1 -q -Atc 'select 1'
```

Environment result:

- `psql` available.
- PostgreSQL version: 16.13.
- `SQLRB_POSTGRES_DSN`: unset.
- `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, and `PGPASSWORD`: set.
- `select 1` probe: passed.

Temporary case list:

```bash
printf 'PORT_0004\nPORT_0013\nPORT_0022\nPORT_0024\nPORT_0025\n' > /tmp/sqlrb_port_pg_failure_cases.txt
```

Targeted run:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --case-list /tmp/sqlrb_port_pg_failure_cases.txt \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/port_pg_source_failure_triage \
  --enable-db-execution \
  --enable-checker
```

Targeted run result:

- Command exited 0.
- Selected rows: 5.
- Candidate generated rows: 5.
- Candidate preflight passed rows: 5.
- Failure bucket counts: `source_execution_failed=5`.

Validation:

- `git diff --check`: passed.
- CSV parse checks for `case_failure_triage.csv` and `variant_inventory.csv`: passed.
- JSON parse check for `targeted_run_summary.json`: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff/status check: passed.
- `runs/user/port_pg_source_failure_triage/` cleanup check: passed; the directory is absent and not staged.
