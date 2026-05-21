# Command Log

Commands were run from the public release repository unless noted. Environment files were sourced locally; secrets were not printed.

```bash
git status -sb
git branch --show-current
git log --oneline -12
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
```

Read project-control and audit context:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -80 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,220p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
python - <<'PY'
import csv
from pathlib import Path
rows=list(csv.DictReader(Path('audits/common_core_mysql_local_diagnostic_v0/case_outcome_matrix.csv').open()))
print([r['case_id'] for r in rows if r['failure_bucket']=='source_execution_failed'])
PY
```

Targeted rerun:

```bash
cat >/tmp/sqlrb_mysql_failed_cases.txt <<'EOF'
PORT_0003
PORT_0005
PORT_0008
PORT_0012
EOF
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine mysql \
  --case-list /tmp/sqlrb_mysql_failed_cases.txt \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/mysql_source_failure_triage \
  --enable-db-execution \
  --enable-checker
```

New repository case inspection covered each failing case's README, manifest, source SQL, positive SQL, schema profile, checker configs, and referenced external schema assets.

Legacy read-only reference commands used `git show` and `git ls-tree` against `artifact/case-package-contract-alignment-clean` in `~/code/sql-rewrite-bench`; the legacy worktree was not checked out or modified.

Validation commands are recorded in the final validation result and were run after the audit packet/project-control writeback was created.
