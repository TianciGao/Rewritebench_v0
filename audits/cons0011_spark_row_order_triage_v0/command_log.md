# Command Log

## Repository Baseline

```bash
git status -sb
git branch --show-current
git log --oneline -12
```

Observed baseline:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
feature/case-package-v2-external-schema
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
923243d feat(user-entry): add target-engine PORT role mapping
```

## Environment Check

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
PYTHONPATH=src python scripts/dev/check_local_engine_env.py
```

Observed result:

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

Read project-control context:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- tail of `project_control/MIGRATION_RUN_LOG.md`
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`

Read Spark diagnostic audit context:

- `audits/spark_live_two_case_smoke_v0/README.md`
- `audits/common_core_spark_local_diagnostic_v0/README.md`
- `audits/common_core_spark_local_diagnostic_v0/run_summary.json`
- `audits/common_core_spark_local_diagnostic_v0/case_outcome_matrix.csv`
- `audits/common_core_spark_local_diagnostic_v0/failure_bucket_summary.csv`
- `audits/common_core_spark_local_diagnostic_v0/command_log.md`

Read `CONS_0011` package files:

- `cases/CONS/CONS_0011/README.md`
- `cases/CONS/CONS_0011/manifest.yaml`
- `cases/CONS/CONS_0011/sql/source.sql`
- `cases/CONS/CONS_0011/sql/pos_01.sql`
- `cases/CONS/CONS_0011/schema/schema_profile.yaml`
- `cases/CONS/CONS_0011/checker/checker.yaml`
- `cases/CONS/CONS_0011/checker/normalization.yaml`
- `cases/CONS/CONS_0011/checker/compare_config.yaml`

Read implementation context:

- `src/sql_rewrite_bench/local_result_checker.py`
- `src/sql_rewrite_bench/spark_execution.py`

## Local Artifact Inspection

Existing local artifacts were present, so no `CONS_0011` rerun was performed.

Inspected:

- `runs/user/common_core_spark_noop_db_checker/ledger.csv`
- `runs/user/common_core_spark_noop_db_checker/failures.csv`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/execution/source_query.sql`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/execution/candidate_query.sql`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/execution/source_result.jsonl`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/execution/candidate_result.jsonl`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/checker/normalized_source_result.jsonl`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/checker/normalized_candidate_result.jsonl`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/checker/checker_result.json`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/checker/mismatch_summary.json`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/execution/spark_execution_metadata.json`

Observed:

- Source SQL contains no `ORDER BY`.
- Positive rewrite SQL contains no `ORDER BY`.
- Workspace source and candidate SQL are identical for the no-op diagnostic row.
- Source row count: 2.
- Candidate row count: 2.
- Column labels equal: yes, `ENAME`.
- Values equal after sorting rows: yes.
- Checker status: `checker_mismatch`.
- Exact status: `mismatch`.
- Failure bucket: `mismatch`.
- Mismatch reason detail: `none`, with row-order-only preview difference.

## Triage Conclusion

`CONS_0011` should be treated as order-insensitive for this result-equivalence check unless maintainers explicitly add an order-sensitive contract. The observed Spark mismatch is a case-level order policy/configuration gap surfaced by nondeterministic row order for an unordered query, not a true semantic mismatch.

## Validation

```bash
git diff --check
```

Result: passed with no output.

```bash
python - <<'PY'
import csv, json
from pathlib import Path
base=Path('audits/cons0011_spark_row_order_triage_v0')
for name in ['cons0011_result_shape.csv','checker_config_review.csv']:
    with (base/name).open(newline='', encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    if not rows:
        raise SystemExit(f'{name}: no rows')
for path in [
    Path('runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/checker/checker_result.json'),
    Path('runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/checker/mismatch_summary.json'),
    Path('runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/execution/spark_execution_metadata.json'),
]:
    json.loads(path.read_text(encoding='utf-8'))
print('csv_json_parse_ok')
PY
```

Result:

```text
csv_json_parse_ok
```

```bash
python - <<'PY'
from pathlib import Path
base=Path('audits/cons0011_spark_row_order_triage_v0')
for path in base.glob('*.md'):
    text=path.read_text(encoding='utf-8')
    if not text.strip():
        raise SystemExit(f'{path}: empty')
    if '\t' in text:
        raise SystemExit(f'{path}: tab character')
print('markdown_sanity_ok', len(list(base.glob('*.md'))))
PY
```

Result:

```text
markdown_sanity_ok 5
```

```bash
python - <<'PY'
import subprocess
allowed_prefixes=(
    'audits/cons0011_spark_row_order_triage_v0/',
    'project_control/MIGRATION_STATUS.md',
    'project_control/MIGRATION_RUN_LOG.md',
)
status=subprocess.check_output(['git','status','--porcelain'], text=True).splitlines()
paths=[]
for line in status:
    path=line[3:] if line.startswith('?? ') else line[3:]
    paths.append(path)
    if not any(path == p or path.startswith(p) for p in allowed_prefixes):
        raise SystemExit(f'protected surface changed: {path}')
print('protected_surface_status_ok', paths)
PY
```

Result:

```text
protected_surface_status_ok ['project_control/MIGRATION_RUN_LOG.md', 'project_control/MIGRATION_STATUS.md', 'audits/cons0011_spark_row_order_triage_v0/']
```

```bash
git status -sb --ignored=matching runs/user/cons0011_spark_order_triage runs/user/common_core_spark_noop_db_checker
```

Result:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
!! runs/user/
```

Interpretation: `runs/user/common_core_spark_noop_db_checker/` remains ignored local diagnostic output, and `runs/user/cons0011_spark_order_triage/` was not created.
