# Adapter Template

Adapters are executable commands invoked by `sqlrb user evaluate` through
`--adapter-command`. They are responsible only for candidate generation.

## Environment

The runner provides:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

## Minimal Contract

1. Read source SQL from `SQLRB_SOURCE_SQL_PATH`.
2. Write candidate SQL to `SQLRB_CANDIDATE_SQL_PATH`, or print candidate SQL to stdout.
3. Exit nonzero if the adapter cannot safely produce a candidate.
4. Do not write user outputs directly under `output/`, `runs/user/`, top-level `reports/`, or top-level `results/`; the runner manages export and internal staging.

The runner captures adapter output, writes internal transitional staging, and
exports user-facing artifacts under:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

## Layout

Route-specific baseline adapters belong under `baselines/`. General examples
belong under `examples/`. Core reusable implementation belongs under
`src/sql_rewrite_bench/`.
