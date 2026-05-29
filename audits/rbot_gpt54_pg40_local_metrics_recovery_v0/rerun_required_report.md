# Rerun Required Report

The requested recovery cannot proceed from the current working tree because the source run artifacts are missing.

Missing path:

```text
runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0
```

Required source artifacts would include the user-facade source run ledger, quality summary, timing artifacts, workspaces, candidate SQL files, and other run-local files consumed by `src/sql_rewrite_bench/local_metrics.py`.

No replacement data source was used. In particular:

- audit CSVs were not used as metric input
- previous summary counts were not converted into canonical metrics
- metrics were not reconstructed manually

Recovery requires one of the following separately authorized actions:

1. Restore the original source run directory from an external local backup, if available.
2. Rerun the PostgreSQL-only R-Bot adapted PG40 diagnostic under the same boundary and then run single-run `compute-local-metrics`.

Do not treat this packet as a metric recovery. It is only a fail-closed artifact-availability finding.
