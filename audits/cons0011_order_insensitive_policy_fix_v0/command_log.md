# Command Log

## Baseline

```bash
git status -sb
git branch --show-current
git log --oneline -12
```

Observed:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
feature/case-package-v2-external-schema
5a49cde docs(audit): triage CONS_0011 Spark row order
55ace58 docs(audit): run Common-core Spark local diagnostic trial
8434f9f docs(audit): run Spark two-case live smoke
53ed24a feat(user-entry): add Spark live backend
9fc8a6e docs(audit): close user-entry engine backend phase
53fd736 feat(user-entry): add Spark fail-closed skeleton
e1b1814 docs(audit): design Spark local diagnostic backend
a672cc6 docs(audit): rerun bounded PostgreSQL MySQL diagnostics
79555bc docs(audit): rerun PostgreSQL MySQL local diagnostics
017e35e docs(audit): close PostgreSQL MySQL local diagnostics
e4c2ec2 docs(audit): close bidirectional PORT diagnostic path
396d98f docs(audit): validate reverse PORT cross-dialect path
```

The tracked worktree was clean before the case-local edit.

## Environment Check

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
PYTHONPATH=src python scripts/dev/check_local_engine_env.py
```

Observed:

```text
PostgreSQL probe SELECT version(): ok
MySQL probe SELECT VERSION(): ok
Spark PYSPARK_PYTHON: set
Spark SQLRB_SPARK_MASTER: set
Spark pyspark import: available
Spark backend status: live local diagnostic backend available through PySpark
Result: diagnostic report complete
```

No secrets were printed.

## Context Read

Read project-control files:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- tail of `project_control/MIGRATION_RUN_LOG.md`

Read triage packet:

- `audits/cons0011_spark_row_order_triage_v0/README.md`
- `audits/cons0011_spark_row_order_triage_v0/row_order_analysis.md`
- `audits/cons0011_spark_row_order_triage_v0/checker_config_review.csv`
- `audits/cons0011_spark_row_order_triage_v0/future_fix_prompt.md`

Read case/checker files:

- `cases/CONS/CONS_0011/checker/normalization.yaml`
- `cases/CONS/CONS_0011/checker/compare_config.yaml`
- `cases/CONS/CONS_0011/checker/checker.yaml`
- `src/sql_rewrite_bench/local_result_checker.py`

## Implementation

Changed only `cases/CONS/CONS_0011/checker/normalization.yaml`:

```yaml
sort_rows: true
```

The setting was added at top level. Existing normalization rules were preserved. No SQL files, manifests, source code, global checker behavior, or other checker configs were changed.

## Spark Validation Runs

Targeted `CONS_0011` rerun:

```bash
printf 'CONS_0011\n' > /tmp/sqlrb_cons0011_spark.txt
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --case-list /tmp/sqlrb_cons0011_spark.txt \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/cons0011_spark_order_fix \
  --enable-db-execution \
  --enable-checker
```

Result:

```text
selected=1; source_executable=1; candidate_executable=1; checker_attempted=1; exact=1; mismatch=0; failure_buckets=none=1
```

Prior two-case Spark regression:

```bash
printf 'PERF_0006\nCONS_0005\n' > /tmp/sqlrb_spark_two_case.txt
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --case-list /tmp/sqlrb_spark_two_case.txt \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/spark_two_case_regression_after_cons0011_fix \
  --enable-db-execution \
  --enable-checker
```

Result:

```text
selected=2; source_executable=2; candidate_executable=2; checker_attempted=2; exact=2; mismatch=0; failure_buckets=none=2
```

Common-core Spark regression:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/common_core_spark_after_cons0011_order_fix \
  --enable-db-execution \
  --enable-checker
```

Result:

```text
selected=40; source_executable=31; candidate_executable=31; checker_attempted=31; exact=31; mismatch=0; failure_buckets=none=31, unsupported_engine=9
```

PORT Spark rows remained explicit unsupported/fail-closed.

## Additional Validation

```bash
git diff --check
```

Result: passed with no output.

```bash
python - <<'PY'
from pathlib import Path
import yaml
path = Path('cases/CONS/CONS_0011/checker/normalization.yaml')
data = yaml.safe_load(path.read_text(encoding='utf-8'))
assert data['case_id'] == 'CONS_0011'
assert data['sort_rows'] is True
assert data['rules']['ignore_whitespace'] is True
assert data['rules']['ignore_case_for_keywords'] is True
assert data['rules']['normalize_numeric_literals'] is False
assert data['rules']['preserve_semantic_operators'] is True
print('yaml_parse_ok sort_rows=true rules_preserved')
PY
```

Result:

```text
yaml_parse_ok sort_rows=true rules_preserved
```

```bash
PYTHONPATH=src python - <<'PY'
import csv
import subprocess
from pathlib import Path
cases = []
with Path('case_sets/common_core_v0/cases.csv').open(newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row.get('common_core_v0_member') == 'true':
            cases.append(row['case_path'])
failed = []
for case_path in cases:
    completed = subprocess.run(
        ['python', 'scripts/dev/validate_case_package_v2_refs.py', '--case', case_path],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        failed.append((case_path, completed.stdout.strip()))
if failed:
    raise SystemExit(1)
print(f'case_package_v2_refs_passed {len(cases)}/{len(cases)}')
PY
```

Result:

```text
case_package_v2_refs_passed 40/40
```

```bash
PYTHONPATH=src pytest tests/user_entry
```

Result:

```text
118 passed, 1 skipped
```

Final audit CSV/Markdown/protected-surface validation is recorded in `protected_surface_check.md`.
