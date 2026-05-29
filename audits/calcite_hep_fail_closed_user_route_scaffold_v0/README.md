# Calcite HEP Fail-Closed User Route Scaffold

Task: `calcite_hep_fail_closed_user_route_scaffold_v0`

Verdict: scaffold implemented and validated as a local-only fail-closed route.

The route is user-entry reachable through the existing adapter-command contract:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --adapter-command "python src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_fail_closed_user_route_scaffold_v0/d035_output \
  --run-id calcite_hep_scaffold_smoke
```

Current behavior is intentionally fail-closed because no Calcite HEP runtime or invocation contract is configured in this release repo. The adapter writes a per-row `calcite_hep_status.json` artifact and emits no candidate SQL. The user-run ledger records `candidate_generated=false`, `extraction_status=no_candidate_sql`, and `failure_bucket=no_candidate_sql`.

This is local diagnostic infrastructure only. It did not run full Common-core, compute official metrics, update paper reports/results, promote retained evidence, create leaderboard output, change denominators, change case membership, or vendor Calcite.
