# SQLGlot Noop Alignment Review

Reviewed packet:

- `audits/sqlglot_noop_pg_current_route_card_refresh_v0/`

Findings:

- The packet contains `per_row_candidate_status.csv`, `per_row_execution_checker_status.csv`, `per_row_timing.csv`, `route_card.json`, `route_card.csv`, and `diagnostic_summary.json`.
- The route card was computed by `run_sqlglot_noop_pg_route_card.py`, not by `local_metrics.py`.
- The packet does not contain a standard source-run directory with `ledger.csv`, `config.yaml`, and canonical timing row artifacts.
- The packet does not contain canonical `metrics/local_metrics_*` outputs.

Related but distinct state:

- Older ignored local source runs under `runs/user/common_core_sqlglot_noop_postgres_snapshot`, `runs/user/common_core_sqlglot_noop_mysql_snapshot`, and `runs/user/common_core_spark_sqlglot_noop_after_statement_patch` have canonical `metrics/local_metrics_*` outputs.
- Those older canonical metrics snapshots do not include timing artifacts and are not the refreshed PostgreSQL route-card packet.

Correction plan:

1. Treat `sqlglot_noop_pg_current_route_card_refresh_v0` route-card outputs as provisional audit-helper summaries.
2. For refreshed SQLGlot noop PG timing metrics, rerun through `sqlrb user evaluate --collect-timing` or create a separately authorized canonical reprocess path from a standard source run.
3. Use `compute-local-metrics` outputs as the only route-card source.
