# Command Log

Repository state:

```bash
git status -sb
git branch --show-current
git log --oneline -15
```

Environment:

```bash
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
```

Read/context commands included project-control files, recent audit packets, and implementation inventory with `sed` and `rg`.

PostgreSQL diagnostic command:

```bash
source scripts/env_mysql.local.sh && source scripts/env_postgres.local.sh && PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/bounded_pg_noop_db_checker_current \
  --enable-db-execution \
  --enable-checker
```

MySQL diagnostic command:

```bash
source scripts/env_mysql.local.sh && source scripts/env_postgres.local.sh && PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine mysql \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/bounded_mysql_noop_db_checker_current \
  --enable-db-execution \
  --enable-checker
```

Validation commands are recorded after execution in this file by the final validation update.

Cleanup command:

```bash
rm -rf runs/user/bounded_pg_noop_db_checker_current runs/user/bounded_mysql_noop_db_checker_current
```

Validation commands:

```bash
git diff --check
python - <<'PY'
import csv, json
from pathlib import Path
root = Path("audits/user_entry_pg_mysql_current_diagnostic_rerun_v0")
for p in sorted(root.glob("*.csv")):
    with p.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows, f"{p} has no rows"
for p in sorted(root.glob("*.json")):
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{p} root not object"
PY
python - <<'PY'
from pathlib import Path
root = Path("audits/user_entry_pg_mysql_current_diagnostic_rerun_v0")
for p in sorted(root.glob("*.md")):
    text = p.read_text(encoding="utf-8")
    assert text.strip(), f"{p} empty"
    assert text.lstrip().startswith("#"), f"{p} missing top-level heading"
PY
python - <<'PY'
import subprocess, sys
allowed = (
    "audits/user_entry_pg_mysql_current_diagnostic_rerun_v0/",
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
bad = [p for p in changed if not any(p == a or p.startswith(a) for a in allowed)]
if bad:
    print("protected surface violation:", bad)
    sys.exit(1)
PY
git status --short -- runs/user/bounded_pg_noop_db_checker_current runs/user/bounded_mysql_noop_db_checker_current
```

Validation results:

- `git diff --check`: passed.
- CSV parse checks: passed.
- JSON parse checks: passed.
- Markdown sanity checks: passed.
- Protected-surface check: passed.
- Local run outputs committed: no.
