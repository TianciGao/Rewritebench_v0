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
git log --oneline -12
```

Output:

```text
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
```

## Environment Check

Command:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
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

Sandbox note:

- A preliminary sandboxed check could not derive `PGHOST` because `ip route` was not permitted and could not create a MySQL TCP socket.
- The accepted check above was rerun with local network/socket access.

## Context Read

Read project-control context:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- tail of `project_control/MIGRATION_RUN_LOG.md`
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`

Read prior audit context:

- `audits/spark_live_backend_v0/README.md`
- `audits/spark_fail_closed_skeleton_v0/README.md`
- `audits/spark_backend_design_v0/README.md`
- `audits/user_entry_engine_backend_closeout_v0/README.md`

Read implementation context:

- `src/sql_rewrite_bench/spark_execution.py`
- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/local_result_checker.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `src/sql_rewrite_bench/user_quality_report.py`
- `src/sql_rewrite_bench/tag_slices.py`
- `examples/user/noop_adapter.py`

## Case List

Created `/tmp/sqlrb_spark_live_smoke_cases.txt` with:

```text
PERF_0006
CONS_0005
```

## Smoke Run

Command:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --case-list /tmp/sqlrb_spark_live_smoke_cases.txt \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/spark_live_smoke \
  --enable-db-execution \
  --enable-checker
```

Sandbox attempt:

- Runner completed, but both Spark rows failed to start PySpark because Py4J could not bind `/127.0.0.1:0` due `Operation not permitted`.
- The local output from that sandbox attempt was removed because it was created by this task and would have contained stale failure artifacts.

Accepted run:

```text
user run complete: run_id=spark_live_smoke selected_rows=2 candidate_generated_rows=2
```

Accepted run summary:

- Selected rows: 2.
- Candidate generated rows: 2.
- Candidate preflight passed rows: 2.
- Spark source execution attempted rows: 2.
- Spark source executable rows: 2.
- Spark candidate execution attempted rows: 2.
- Spark candidate executable rows: 2.
- Checker attempted rows: 2.
- Exact rows: 2.
- Mismatch rows: 0.
- Failure buckets: `none=2`.
- Official metrics computed: no.
- Timing or speedup computed: no.
- Reports/results updated: no.
- Global leaderboard created: no.

## Inspected Local Outputs

Inspected:

- `runs/user/spark_live_smoke/selected_cases.csv`
- `runs/user/spark_live_smoke/ledger.csv`
- `runs/user/spark_live_smoke/failures.csv`
- `runs/user/spark_live_smoke/summary.json`
- `runs/user/spark_live_smoke/quality_summary.json`
- `runs/user/spark_live_smoke/quality_report.md`
- `runs/user/spark_live_smoke/tag_slices.csv`
- per-row Spark execution metadata, source/candidate JSONL artifacts, and checker results under `runs/user/spark_live_smoke/workspaces/`

Observed:

- `PERF_0006`: Spark source/candidate executed through PySpark, source rows 2, candidate rows 2, checker exact.
- `CONS_0005`: Spark source/candidate executed through PySpark, source rows 0, candidate rows 0, checker exact.
- `failures.csv` contains only the header.

## Validation

```bash
git diff --check
```

Result: passed with no output.

```bash
python -c "... parse live_smoke_summary.json and audit CSV files ..."
```

Result:

```text
csv_json_parse_ok {'case_outcome_matrix.csv': 2, 'failure_bucket_summary.csv': 1, 'artifact_inventory.csv': 27}
```

```bash
python -c "... sanity-check audit Markdown files ..."
```

Result:

```text
markdown_sanity_ok 4
```

```bash
python -c "... verify git status paths are limited to allowed surfaces ..."
```

Result:

```text
protected_surface_status_ok ['project_control/MIGRATION_RUN_LOG.md', 'project_control/MIGRATION_STATUS.md', 'audits/spark_live_two_case_smoke_v0/README.md', 'audits/spark_live_two_case_smoke_v0/artifact_inventory.csv', 'audits/spark_live_two_case_smoke_v0/case_outcome_matrix.csv', 'audits/spark_live_two_case_smoke_v0/command_log.md', 'audits/spark_live_two_case_smoke_v0/environment_check.md', 'audits/spark_live_two_case_smoke_v0/failure_bucket_summary.csv', 'audits/spark_live_two_case_smoke_v0/live_smoke_summary.json', 'audits/spark_live_two_case_smoke_v0/protected_surface_check.md']
```

```bash
git status -sb --ignored=matching runs/user/spark_live_smoke
```

Result:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
!! runs/user/
```

Interpretation: `runs/user/spark_live_smoke/` is ignored local diagnostic output and is not staged.
