# Run Scope

Task id:
- `sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0`

Route under test:
- `sqlglot_optimize_schema_aware`

Adapter:
- `baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware`

Planned rows:

| case_id | PostgreSQL | MySQL | Spark |
| --- | --- | --- | --- |
| `CONS_0005` | attempted | attempted | attempted |
| `PERF_0006` | attempted | attempted | attempted |
| `CONS_0036` | attempted | attempted | attempted |

Execution/checker policy:
- Generate candidate SQL through the schema-aware route.
- Run candidate preflight.
- Execute source and candidate on the selected same engine.
- Run the local checker when both source and candidate execution succeed.
- Do not collect timing.
- Do not run verifiers.

Runtime root:
- `/tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/`

Repository writes:
- Audit files only under `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/`.
- Project-control status/run-log update only.
