# Command Log

Date: 2026-05-21.

## Repository State

```bash
git status -sb
```

Result: clean branch state at start.

```bash
git branch --show-current
```

Result: `feature/case-package-v2-external-schema`.

```bash
git log --oneline -12
```

Top entries observed:

```text
4707fca docs(env): add local engine setup helpers
ccc0e8e feat(user-entry): add MySQL source-reference backend
605c8ed feat(user-entry): consume PORT diagnostic metadata
6187062 docs(cases): add PORT local diagnostic role metadata
de4075d docs(audit): design PORT manifest diagnostic roles
a7f8ffe docs(project-control): plan PORT cross-dialect diagnostics
```

## Required Reads

Read before the live run:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md` tail
- `project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md`
- `audits/port_cross_dialect_mysql_backend_v0/README.md`
- `audits/port_cross_dialect_runner_metadata_consumption_v0/README.md`
- `src/sql_rewrite_bench/mysql_execution.py`
- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/user_run.py`
- the five target `manifest.yaml` files

## Environment Probe

Sandboxed probe:

```bash
bash -lc 'source scripts/env_mysql.local.sh; source scripts/env_postgres.local.sh; python scripts/dev/check_local_engine_env.py'
```

Result: sandbox local TCP restriction prevented the DB probe from being
authoritative.

Escalated local probe:

```bash
bash -lc 'source scripts/env_mysql.local.sh; source scripts/env_postgres.local.sh; python scripts/dev/check_local_engine_env.py'
```

Result:

- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark: deferred/fail-closed.

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
bash -lc 'source scripts/env_mysql.local.sh; source scripts/env_postgres.local.sh; PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_port_cross_dialect_cases.txt --adapter-command "python examples/user/noop_adapter.py" --out runs/user/port_mysql_source_reference_live --enable-db-execution --enable-checker'
```

Result:

```text
user run complete: run_id=port_mysql_source_reference_live selected_rows=5 candidate_generated_rows=5
```

## Inspection

Inspected:

- `runs/user/port_mysql_source_reference_live/ledger.csv`
- `runs/user/port_mysql_source_reference_live/failures.csv`
- `runs/user/port_mysql_source_reference_live/summary.json`
- `runs/user/port_mysql_source_reference_live/quality_summary.json`
- `runs/user/port_mysql_source_reference_live/quality_report.md`
- `runs/user/port_mysql_source_reference_live/tag_slices.csv`
- execution artifacts under `runs/user/port_mysql_source_reference_live/workspaces/`

Key inspection result:

- MySQL source-reference artifacts were written for all five selected rows.
- PostgreSQL target-candidate artifacts show target-side syntax failures on the
  no-op source-like MySQL SQL.
- Checker did not run because target-candidate execution failed.
