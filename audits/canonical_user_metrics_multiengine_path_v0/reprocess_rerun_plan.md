# Reprocess / Rerun Plan

SQLGlot optimize schema-aware next canonical task:

1. Rerun through the user facade, not an audit helper:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware" \
  --output-root /tmp/sqlrb_<task>/output \
  --run-id <run_id> \
  --enable-db-execution \
  --enable-checker \
  --collect-timing
```

2. Compute canonical aggregate metrics:

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix <run_id> \
  --engines postgres,mysql,spark \
  --aggregate-run-id <run_id> \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_<task>/output
```

Calcite HEP next canonical task:

- For PostgreSQL-only local diagnostics, use the single-run `compute-local-metrics --run-id <run_id>` path after a canonical user-facade run.
- For future tri-engine Calcite diagnostics, use the aggregate path only after MySQL/Spark route blockers and runtime readiness are separately addressed.

SQLGlot noop next canonical task:

- Refresh through the user facade and use the same single-run or aggregate command depending on the selected engine scope.

Prior provisional outputs to regenerate:

- `audits/sqlglot_noop_pg_current_route_card_refresh_v0/`
- `audits/calcite_hep_pg_local_metrics_projection_v0/`
- `audits/calcite_hep_pg_post_quoting_chain_rerun_v0/`
- `audits/calcite_vs_sqlglot_noop_pg_local_comparison_v0/`
- `audits/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/`
- `audits/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/`
