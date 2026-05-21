# Command Log

Date: 2026-05-21.

## Repository State

```bash
git status -sb
git branch --show-current
git log --oneline -12
```

Starting branch: `feature/case-package-v2-external-schema`.

Starting HEAD:

```text
64ece0a docs(audit): run PORT MySQL live diagnostic
```

The tracked worktree was clean before changes.

## Required Reads

Read before the live run:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md` tail
- `project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md`
- recent PORT cross-dialect audit README files and MySQL live summary
- user runner, engine router, MySQL/PostgreSQL execution, checker, resolver code
- the five target PORT manifests

## Environment Probe

```bash
bash -lc '
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
'
```

Result:

- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark: deferred/fail-closed.

## Adapter Validation

```bash
PYTHONPATH=src python -m py_compile examples/user/port_postgres_target_reference_adapter.py
PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry/test_port_target_reference_adapter.py
PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry
```

Result:

- Adapter compile: passed.
- New adapter tests: 3 passed.
- Full user-entry tests: 82 passed, 2 skipped.

## Case List

```bash
cat > /tmp/sqlrb_port_cross_dialect_cases.txt <<'EOF'
PORT_0004
PORT_0013
PORT_0022
PORT_0024
PORT_0025
EOF
```

## Live Diagnostic

```bash
bash -lc '
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
PYTHONPATH=src python -m sql_rewrite_bench.user_run   --case-set common_core_v0   --engine postgres   --case-list /tmp/sqlrb_port_cross_dialect_cases.txt   --adapter-command "python examples/user/port_postgres_target_reference_adapter.py"   --out runs/user/port_pg_target_reference_controlled   --enable-db-execution   --enable-checker
'
```

Result:

```text
user run complete: run_id=port_pg_target_reference_controlled selected_rows=5 candidate_generated_rows=5
```

## Inspection

Inspected:

- `runs/user/port_pg_target_reference_controlled/ledger.csv`
- `runs/user/port_pg_target_reference_controlled/failures.csv`
- `runs/user/port_pg_target_reference_controlled/summary.json`
- `runs/user/port_pg_target_reference_controlled/quality_summary.json`
- `runs/user/port_pg_target_reference_controlled/quality_report.md`
- `runs/user/port_pg_target_reference_controlled/tag_slices.csv`
- execution artifacts under `runs/user/port_pg_target_reference_controlled/workspaces/`

Key inspection result:

- MySQL source-reference execution succeeded for all five selected rows.
- PostgreSQL target-candidate execution succeeded for all five selected rows.
- Checker ran for all five rows.
- Local checker outcome: 1 exact row and 4 mismatch rows.
