# Command Log

Commands run for repository snapshot:

```bash
git status -sb
git branch --show-current
git log --oneline -15
```

Read project-control files:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -120 project_control/MIGRATION_RUN_LOG.md
sed -n '1,260p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
```

Read prior PORT audit evidence:

```bash
sed -n '1,220p' audits/user_entry_port_pg_source_failure_triage_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_diagnostic_execution_plan_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_manifest_role_design_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_manifest_metadata_patch_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_runner_metadata_consumption_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_mysql_backend_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_mysql_live_diagnostic_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_pg_target_reference_diagnostic_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_checker_normalization_audit_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_checker_normalization_v0/README.md
cat audits/port_cross_dialect_checker_normalization_v0/controlled_rerun_summary.json
```

Inventory checks:

```bash
rg -n "local_diagnostic|diagnostic_mode|source_reference|target_reference|checker.comparison|cross_dialect|positional|Decimal|source_reference_result_to_target_candidate_result" src/sql_rewrite_bench/case_package_resolver.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/mysql_execution.py src/sql_rewrite_bench/postgres_execution.py src/sql_rewrite_bench/local_result_checker.py examples/user/port_postgres_target_reference_adapter.py
rg -n "local_diagnostic|diagnostic_mode|source_reference|target_candidate|target_reference|checker|comparison|engine|query|role|use_for_checker_oracle" cases/PORT/PORT_0003/manifest.yaml cases/PORT/PORT_0004/manifest.yaml cases/PORT/PORT_0005/manifest.yaml cases/PORT/PORT_0008/manifest.yaml cases/PORT/PORT_0012/manifest.yaml cases/PORT/PORT_0013/manifest.yaml cases/PORT/PORT_0022/manifest.yaml cases/PORT/PORT_0024/manifest.yaml cases/PORT/PORT_0025/manifest.yaml
rg -n "PORT_" case_sets/common_core_v0/cases.csv
sed -n '245,380p' src/sql_rewrite_bench/case_package_resolver.py
sed -n '467,555p' src/sql_rewrite_bench/engine_execution.py
sed -n '474,490p' src/sql_rewrite_bench/user_run.py
sed -n '122,170p' src/sql_rewrite_bench/local_result_checker.py
```

Validation commands:

```bash
git diff --check
python - <<'PY'
from pathlib import Path
import csv
import json

root = Path("audits/port_cross_dialect_local_diagnostic_closeout_v0")
for path in root.glob("*.csv"):
    with path.open(newline="") as handle:
        list(csv.DictReader(handle))
for path in root.glob("*.json"):
    json.loads(path.read_text())
for path in root.glob("*.md"):
    text = path.read_text()
    assert text.strip(), path
    assert "\t" not in text, path
print("audit parse and markdown sanity checks passed")
PY
```

Protected-surface validation:

```bash
git diff --name-only
git ls-files --others --exclude-standard
git diff --cached --name-only
git status -sb
```

No `runs/user/` outputs were created by this closeout task.
