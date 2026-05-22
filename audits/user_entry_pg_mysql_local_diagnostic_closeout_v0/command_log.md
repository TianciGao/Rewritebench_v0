# Command Log

Repository state commands:

```bash
git status -sb
git branch --show-current
git log --oneline -15
```

Read commands:

```bash
sed -n '1,180p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,140p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -n 140 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,220p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
sed -n '1,220p' audits/user_entry_local_evaluation_phase_closeout_v0/README.md
sed -n '1,220p' audits/user_entry_common_core_pg_local_diagnostic_v0/README.md
sed -n '1,220p' audits/mysql_same_engine_backend_v0/README.md
sed -n '1,220p' audits/common_core_mysql_local_diagnostic_v0/README.md
sed -n '1,220p' audits/mysql_same_engine_source_failure_triage_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_local_diagnostic_closeout_v0/README.md
sed -n '1,220p' audits/port_target_engine_role_mapping_v0/README.md
sed -n '1,220p' audits/port_bidirectional_cross_dialect_closeout_v0/README.md
rg -n 'diagnostic|execute_|cross_dialect|mysql|postgres|spark|official|timing|leaderboard' src/sql_rewrite_bench
```

Audit creation:

```bash
mkdir -p audits/user_entry_pg_mysql_local_diagnostic_closeout_v0
```

Validation commands are recorded after execution in this file by the final validation update.

Validation commands:

```bash
git diff --check
python - <<'PY'
import csv, json
from pathlib import Path
root = Path("audits/user_entry_pg_mysql_local_diagnostic_closeout_v0")
for path in sorted(root.glob("*.csv")):
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows, f"{path} has no rows"
for path in sorted(root.glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{path} root not object"
PY
python - <<'PY'
from pathlib import Path
root = Path("audits/user_entry_pg_mysql_local_diagnostic_closeout_v0")
for path in sorted(root.glob("*.md")):
    text = path.read_text(encoding="utf-8")
    assert text.strip(), f"{path} empty"
    assert text.lstrip().startswith("#"), f"{path} missing top-level heading"
PY
python - <<'PY'
import subprocess, sys
allowed_prefixes = (
    "audits/user_entry_pg_mysql_local_diagnostic_closeout_v0/",
    "project_control/MIGRATION_STATUS.md",
    "project_control/MIGRATION_RUN_LOG.md",
)
result = subprocess.run(["git", "status", "--porcelain"], text=True, capture_output=True, check=True)
changed = []
for line in result.stdout.splitlines():
    if not line:
        continue
    path = line[3:] if line.startswith("?? ") else line[3:]
    changed.append(path)
bad = [p for p in changed if not any(p == a or p.startswith(a) for a in allowed_prefixes)]
if bad:
    print("protected surface violation:", bad)
    sys.exit(1)
PY
git status --short -- runs/user
```

Validation results:

- `git diff --check`: passed.
- CSV parse checks: passed.
- JSON parse checks: passed.
- Markdown sanity checks: passed.
- Protected-surface check: passed.
- `runs/user/` outputs committed: no.
