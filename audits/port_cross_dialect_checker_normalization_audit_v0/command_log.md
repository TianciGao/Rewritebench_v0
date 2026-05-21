# Command Log

Commands run or inspected for this audit:

```bash
git status -sb
git branch --show-current
git log --oneline -12
```

Result: branch `feature/case-package-v2-external-schema`; worktree was clean before audit edits.

```bash
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
```

Result: PostgreSQL probe ok; MySQL probe ok; Spark deferred/fail-closed. Passwords and connection strings are not recorded here.

Read project-control context:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
tail -n 120 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/DECISION_LOG.md
sed -n '1,260p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
```

Read recent PORT diagnostic audit packets and implementation/config context, including the prior controlled run packet, `local_result_checker.py`, engine execution modules, the controlled adapter, manifests, checker configs, and source/target SQL for the five audited cases.

Checked controlled diagnostic artifacts:

```bash
test -d runs/user/port_pg_target_reference_controlled && echo present || echo missing
sed -n '1,80p' runs/user/port_pg_target_reference_controlled/ledger.csv
python -m json.tool runs/user/port_pg_target_reference_controlled/summary.json
python -m json.tool runs/user/port_pg_target_reference_controlled/quality_summary.json
```

Result: prior controlled diagnostic artifacts were present; rerun was not required.

Inspected local source, target, normalized, and mismatch artifacts under:

```text
runs/user/port_pg_target_reference_controlled/workspaces/
```

Validation commands run after writing the audit packet:

```bash
git diff --check
python - <<'PY'
# CSV parse/header checks for audit CSV files.
PY
python - <<'PY'
# Markdown sanity checks for audit Markdown files.
PY
python - <<'PY'
# Protected-surface changed-path allowlist check.
PY
git diff --cached --name-only
git status --short --ignored runs/user/port_pg_target_reference_controlled
```

Result: validation passed. The controlled run output remained ignored and unstaged.
