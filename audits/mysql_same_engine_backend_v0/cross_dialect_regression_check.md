# Cross-Dialect Regression Check

Command shape:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --case-list /tmp/sqlrb_port_cross_dialect_cases.txt \
  --adapter-command "python examples/user/port_postgres_target_reference_adapter.py" \
  --out runs/user/port_pg_target_reference_normalized_regression \
  --enable-db-execution \
  --enable-checker
```

Result:

- Selected rows: 5.
- MySQL source-reference executable rows: 5.
- PostgreSQL target-candidate executable rows: 5.
- Checker attempted rows: 5.
- Exact rows: 5.
- Mismatch rows: 0.
- Failure buckets: `none=5`.

This confirms the existing PORT cross-dialect MySQL source-reference path remains distinguishable from the new same-engine MySQL path. Cross-dialect artifacts remain under `execution/mysql_source/`, while same-engine MySQL artifacts are written under `execution/mysql_same_engine/`.

The regression run is local diagnostic only and was not used for official metrics, timing, reports/results, paper results, retained evidence, or leaderboard output.
