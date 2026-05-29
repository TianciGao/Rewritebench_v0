# Capture Plan

The task attempted Track A 120 candidate capture for:

1. `method_id=sqlglot_noop`, `route_id=sqlglot_noop_track_a_120_candidate_capture_v0`
2. `method_id=sqlglot_optimize_schema_aware`, `route_id=sqlglot_optimize_schema_aware_track_a_120_candidate_capture_v0`
3. `method_id=calcite_hep_fail_closed`, `route_id=calcite_hep_fail_closed_track_a_120_candidate_capture_v0`

Each route planned 120 rows: 40 Common-core cases x PostgreSQL, MySQL, and Spark.

Existing baseline adapters were invoked directly through their public adapter environment contract:

- `python baselines/sqlglot/sqlglot_user_adapter.py --route noop`
- `python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware`
- `python baselines/calcite_hep_fail_closed/adapter.py`

Candidate paths were set directly to the D035-style output locations:

```text
output/results/<run_id>/candidate_sql/<method_id>/<route_id>/<engine>/<CASE_ID>__<engine>.sql
```

Adapter workspaces, stdout/stderr, and status JSON were written under:

```text
output/logs/<run_id>/workspaces/<CASE_ID>/<engine>/
```

No `python -m cli.main user evaluate` command was used because the current user runner writes transitional source runs under `runs/user/`, which this task explicitly avoided.

No DB/checker/timing/local_metrics/POCR annotation/POCR Stage B command was run.
