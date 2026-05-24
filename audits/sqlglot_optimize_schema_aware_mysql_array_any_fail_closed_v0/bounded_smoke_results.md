# Bounded Smoke Results

Smoke helper:

- `audits/sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0/run_bounded_smoke.py`

Runtime root:

- `/tmp/sqlrb_sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0/`

Rows:

| Row | Role | Result |
| --- | --- | --- |
| `CONS_0005` / MySQL | target blocker | Fail-closed before DB execution with `sqlglot_status_failure_bucket=mysql_unsupported_array_any`; no executable candidate emitted. |
| `CONS_0005` / PostgreSQL | control | Source/candidate/checker exact. |
| `CONS_0005` / Spark | non-target blocker control | Remains checker mismatch; source/candidate execution reached. |
| `PERF_0006` / MySQL | non-ARRAY_ANY control | Source/candidate/checker exact. |

Machine-readable outputs:

- `before_after_status.csv`
- `diagnostic_summary.json`

Summary flags:

- `target_mysql_array_any_fail_closed = true`
- `postgres_cons0005_exact = true`
- `spark_cons0005_remains_mismatch = true`
- `mysql_perf0006_exact = true`

Interpretation:

- `CONS_0005` / MySQL no longer appears as a candidate execution failure in this bounded smoke because the unsupported candidate is not exposed for DB execution.
- PostgreSQL behavior is unaffected.
- Spark behavior is unaffected and remains a separate semantic mismatch.
- The non-ARRAY_ANY MySQL control row did not regress.
