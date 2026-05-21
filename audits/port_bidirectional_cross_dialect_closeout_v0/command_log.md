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
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -n 120 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
sed -n '1,220p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,200p' audits/*PORT-related*/README.md
rg -n 'local_diagnostic|engine_roles|diagnostic_mode|source_reference|target_candidate|target_reference|cross_dialect' src/sql_rewrite_bench examples/user cases/PORT
python - <<'PY'
from pathlib import Path
import yaml
for p in [Path("cases/PORT") / c / "manifest.yaml" for c in [
    "PORT_0003", "PORT_0004", "PORT_0005", "PORT_0008", "PORT_0012",
    "PORT_0013", "PORT_0022", "PORT_0024", "PORT_0025"
]]:
    m = yaml.safe_load(p.read_text())
    print(p.parent.name, m["local_diagnostic"]["schema_version"])
PY
```

Audit creation:

```bash
mkdir -p audits/port_bidirectional_cross_dialect_closeout_v0
```

Validation commands are recorded after execution in this file by the final validation update.

Validation commands:

```bash
git diff --check
python - <<'PY'
import csv, json
from pathlib import Path
root = Path("audits/port_bidirectional_cross_dialect_closeout_v0")
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
root = Path("audits/port_bidirectional_cross_dialect_closeout_v0")
for path in sorted(root.glob("*.md")):
    text = path.read_text(encoding="utf-8")
    assert text.strip(), f"{path} empty"
    assert text.lstrip().startswith("#"), f"{path} missing top-level heading"
PY
python - <<'PY'
import subprocess, sys
allowed_prefixes = (
    "audits/port_bidirectional_cross_dialect_closeout_v0/",
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
