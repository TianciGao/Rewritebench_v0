# Command Log

## Repository Baseline

```bash
git status -sb
```

Output:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
```

```bash
git branch --show-current
```

Output:

```text
feature/case-package-v2-external-schema
```

```bash
git log --oneline -15
```

Output:

```text
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
132c2b8 docs(audit): triage MySQL same-engine source failures
7830828 docs(audit): run Common-core MySQL local diagnostic trial
6b2ffcf feat(user-entry): add MySQL same-engine backend
5cece03 docs(audit): close PORT cross-dialect diagnostic path
```

Pre-run dirty check:

```text
Tracked worktree was clean. `runs/user/` was ignored local output only. `runs/user/common_core_spark_noop_db_checker/` did not exist before the accepted run.
```

## Environment Check

Command:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
PYTHONPATH=src python scripts/dev/check_local_engine_env.py
```

Accepted result:

```text
PostgreSQL probe SELECT version(): ok
MySQL probe SELECT VERSION(): ok
Spark PYSPARK_PYTHON: set
Spark SQLRB_SPARK_MASTER: set
Spark pyspark import: available
Spark backend status: live local diagnostic backend available through PySpark
Result: diagnostic report complete
```

No passwords or DSN values were printed.

## Context Read

Read project-control context:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- tail of `project_control/MIGRATION_RUN_LOG.md`
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- `project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md`

Read recent audit context:

- `audits/spark_live_backend_v0/README.md`
- `audits/spark_live_two_case_smoke_v0/README.md`
- `audits/spark_fail_closed_skeleton_v0/README.md`
- `audits/spark_backend_design_v0/README.md`
- `audits/user_entry_engine_backend_closeout_v0/README.md`
- `audits/user_entry_pg_mysql_bounded_local_diagnostic_rerun_v0/README.md`
- `audits/port_bidirectional_cross_dialect_closeout_v0/README.md`

Read implementation context:

- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/spark_execution.py`
- `src/sql_rewrite_bench/postgres_execution.py`
- `src/sql_rewrite_bench/mysql_execution.py`
- `src/sql_rewrite_bench/local_result_checker.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `src/sql_rewrite_bench/user_quality_report.py`
- `src/sql_rewrite_bench/tag_slices.py`
- `examples/user/noop_adapter.py`

## Spark Diagnostic Run

Command:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/common_core_spark_noop_db_checker \
  --enable-db-execution \
  --enable-checker
```

Accepted run result:

```text
user run complete: run_id=common_core_spark_noop_db_checker selected_rows=40 candidate_generated_rows=40
```

Observed non-fatal Spark warnings:

- Window operations without partitioning.
- Local memory-manager row-group scaling warnings.

These warnings did not stop the local diagnostic run.

## Inspected Local Outputs

Inspected:

- `runs/user/common_core_spark_noop_db_checker/selected_cases.csv`
- `runs/user/common_core_spark_noop_db_checker/ledger.csv`
- `runs/user/common_core_spark_noop_db_checker/failures.csv`
- `runs/user/common_core_spark_noop_db_checker/summary.json`
- `runs/user/common_core_spark_noop_db_checker/report.md`
- `runs/user/common_core_spark_noop_db_checker/quality_summary.json`
- `runs/user/common_core_spark_noop_db_checker/quality_report.md`
- `runs/user/common_core_spark_noop_db_checker/tag_slices.csv`
- `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/checker/mismatch_summary.json`

Run summary:

- Selected rows: 40.
- Candidate generated rows: 40.
- Candidate preflight passed rows: 40.
- Spark source execution attempted rows: 31.
- Spark source executable rows: 31.
- Spark candidate execution attempted rows: 31.
- Spark candidate executable rows: 31.
- Checker attempted rows: 31.
- Exact rows: 30.
- Mismatch rows: 1.
- Source-like rows: 40.
- Failure buckets: `none=30`, `mismatch=1`, `unsupported_engine=9`.
- Diagnostic modes: `same_engine=31`, `unsupported=9`.
- Official metrics computed: no.
- Timing or speedup computed: no.
- Reports/results updated: no.
- Global leaderboard created: no.

Failure classification:

- `CONS_0011`: checker/normalization row-order mismatch. Source rows were `ALICE`, `BOB`; candidate rows were `BOB`, `ALICE`.
- `PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`: unsupported Spark role / explicit fail-closed PORT local diagnostic path.

## Validation

```bash
git diff --check
```

Result: passed with no output.

```bash
python -c "... parse run_summary.json and audit CSV files ..."
```

Result:

```text
csv_json_parse_ok {'funnel_counts.csv': 13, 'failure_bucket_summary.csv': 3, 'case_outcome_matrix.csv': 40, 'tag_slice_summary.csv': 3, 'artifact_inventory.csv': 22}
```

```bash
python -c "... sanity-check audit Markdown files ..."
```

Result:

```text
markdown_sanity_ok 5
```

```bash
python -c "... verify git status paths are limited to allowed surfaces ..."
```

Result:

```text
protected_surface_status_ok ['project_control/MIGRATION_RUN_LOG.md', 'project_control/MIGRATION_STATUS.md', 'audits/common_core_spark_local_diagnostic_v0/README.md', 'audits/common_core_spark_local_diagnostic_v0/artifact_inventory.csv', 'audits/common_core_spark_local_diagnostic_v0/case_outcome_matrix.csv', 'audits/common_core_spark_local_diagnostic_v0/command_log.md', 'audits/common_core_spark_local_diagnostic_v0/environment_check.md', 'audits/common_core_spark_local_diagnostic_v0/failure_bucket_summary.csv', 'audits/common_core_spark_local_diagnostic_v0/funnel_counts.csv', 'audits/common_core_spark_local_diagnostic_v0/interpretation_boundary.md', 'audits/common_core_spark_local_diagnostic_v0/protected_surface_check.md', 'audits/common_core_spark_local_diagnostic_v0/run_summary.json', 'audits/common_core_spark_local_diagnostic_v0/tag_slice_summary.csv']
```

```bash
git status -sb --ignored=matching runs/user/common_core_spark_noop_db_checker
```

Result:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
!! runs/user/
```

Interpretation: `runs/user/common_core_spark_noop_db_checker/` is ignored local diagnostic output and is not staged.
