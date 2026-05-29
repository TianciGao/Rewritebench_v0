# Command Log

Preflight and context commands:

```bash
git status -sb
git branch --show-current
git log --oneline -8
git merge-base --is-ancestor b3ad644 HEAD
test -d audits/timing_schema_open_questions_resolution_v0
rg -n "D032|timing_schema_open_questions_resolution_v0|Commit hash:|Push result:" project_control/DECISION_LOG.md project_control/MIGRATION_RUN_LOG.md
tail -n 90 project_control/MIGRATION_RUN_LOG.md
tail -n 50 project_control/MIGRATION_STATUS.md
sed -n '1,220p' repository_spec/timing_artifact_schema_v0_draft.md
sed -n '1,180p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
```

Implementation inspection commands included reads of:

```bash
src/sql_rewrite_bench/user_run.py
src/sql_rewrite_bench/engine_execution.py
src/sql_rewrite_bench/postgres_execution.py
src/sql_rewrite_bench/mysql_execution.py
src/sql_rewrite_bench/spark_execution.py
src/sql_rewrite_bench/local_result_checker.py
src/sql_rewrite_bench/user_ledger.py
src/sql_rewrite_bench/user_run_schema.py
tests/user_entry/
```

Environment check:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
python scripts/dev/check_local_engine_env.py
```

Result: PostgreSQL ok, MySQL ok, Spark PySpark backend available.

Bounded timing smoke commands:

```bash
cat > /tmp/sqlrb_timing_smoke_cases.txt <<'EOF'
PERF_0006
CONS_0005
EOF

PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --case-list /tmp/sqlrb_timing_smoke_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/timing_sqlglot_noop_postgres_smoke \
  --enable-db-execution \
  --enable-checker \
  --collect-timing

PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine mysql \
  --case-list /tmp/sqlrb_timing_smoke_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/timing_sqlglot_noop_mysql_smoke \
  --enable-db-execution \
  --enable-checker \
  --collect-timing

PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --case-list /tmp/sqlrb_timing_smoke_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/timing_sqlglot_noop_spark_smoke \
  --enable-db-execution \
  --enable-checker \
  --collect-timing
```

Validation commands:

```bash
PYTHONPATH=src pytest tests/user_entry/test_local_timing.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile \
  src/sql_rewrite_bench/local_timing.py \
  src/sql_rewrite_bench/user_run.py \
  src/sql_rewrite_bench/user_ledger.py \
  src/sql_rewrite_bench/user_run_schema.py
git diff --check
python -m json.tool audits/exact_gated_local_timing_diagnostic_v0/timing_status_counts.json
python - <<'PY'
import csv, json
from pathlib import Path
for path in Path("audits/exact_gated_local_timing_diagnostic_v0").glob("*.csv"):
    with path.open(newline="", encoding="utf-8") as f:
        list(csv.DictReader(f))
for path in Path("audits/exact_gated_local_timing_diagnostic_v0").glob("*.md"):
    assert path.read_text(encoding="utf-8").strip()
PY
git diff --name-only > /tmp/sqlrb_changed_files.txt
python - <<'PY'
from pathlib import Path
allowed = {
    "src/sql_rewrite_bench/local_timing.py",
    "src/sql_rewrite_bench/user_run.py",
    "src/sql_rewrite_bench/user_ledger.py",
    "src/sql_rewrite_bench/user_run_schema.py",
    "tests/user_entry/test_local_timing.py",
    "project_control/MIGRATION_STATUS.md",
    "project_control/MIGRATION_RUN_LOG.md",
}
bad = []
for line in Path("/tmp/sqlrb_changed_files.txt").read_text().splitlines():
    if line.startswith("audits/exact_gated_local_timing_diagnostic_v0/"):
        continue
    if line not in allowed:
        bad.append(line)
assert not bad, bad
PY
git status -sb
```

Results:

- Focused timing tests: passed, 7 tests.
- Full user-entry tests: passed, 153 tests, 1 skipped, 12 subtests passed.
- Python compile: passed.
- Bounded SQLGlot noop timing smoke: PostgreSQL/MySQL/Spark each selected 2 rows, exact 2 rows, timing eligible 2 rows, and timed 2 rows.
- CSV/JSON/Markdown audit sanity checks: passed.
- Protected-surface check: passed; no cases, baselines, `case_sets/`, reports, or results changed.
