# Command Log

Initial repository state:

```bash
git status -sb
git branch --show-current
git log --oneline -12
```

Environment:

```bash
set -a
[ -f scripts/env_mysql.local.sh ] && source scripts/env_mysql.local.sh
[ -f scripts/env_postgres.local.sh ] && source scripts/env_postgres.local.sh
set +a
python scripts/dev/check_local_engine_env.py
```

Required context was read from project-control documents, recent MySQL/PORT audit packets, and current user-entry implementation files.

Run command:

```bash
rm -rf runs/user/common_core_mysql_noop_db_checker
set -a; [ -f scripts/env_mysql.local.sh ] && source scripts/env_mysql.local.sh; [ -f scripts/env_postgres.local.sh ] && source scripts/env_postgres.local.sh; set +a; PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine mysql \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/common_core_mysql_noop_db_checker \
  --enable-db-execution \
  --enable-checker
```

Inspection covered:

```bash
runs/user/common_core_mysql_noop_db_checker/selected_cases.csv
runs/user/common_core_mysql_noop_db_checker/ledger.csv
runs/user/common_core_mysql_noop_db_checker/failures.csv
runs/user/common_core_mysql_noop_db_checker/summary.json
runs/user/common_core_mysql_noop_db_checker/report.md
runs/user/common_core_mysql_noop_db_checker/quality_summary.json
runs/user/common_core_mysql_noop_db_checker/quality_report.md
runs/user/common_core_mysql_noop_db_checker/tag_slices.csv
```

Validation:

```bash
git diff --check
python - <<'PY'
import csv, json
from pathlib import Path
root = Path('audits/common_core_mysql_local_diagnostic_v0')
for path in root.glob('*.json'):
    json.loads(path.read_text(encoding='utf-8'))
for path in root.glob('*.csv'):
    with path.open(newline='', encoding='utf-8') as f:
        list(csv.DictReader(f))
for path in root.glob('*.md'):
    assert path.read_text(encoding='utf-8').strip()
print('audit sanity ok')
PY
```

The local run output directory was not staged or committed.
