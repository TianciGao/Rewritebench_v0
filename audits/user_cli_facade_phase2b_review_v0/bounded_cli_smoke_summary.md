# Bounded CLI Smoke Summary

Command shape:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root /tmp/<temp>/output \
  --run-id phase2b_review_cli_smoke_pg_<timestamp> \
  --smoke \
  --enable-db-execution \
  --enable-checker
```

Environment:

- PostgreSQL/MySQL/Spark readiness check completed.
- SQLGlot version: 30.2.1.

Result:

| field | value |
| --- | ---: |
| selected_rows | 2 |
| adapter_invoked_rows | 2 |
| candidate_generated_rows | 2 |
| candidate_preflight_failed_rows | 0 |
| source_execution_success_rows | 2 |
| candidate_execution_success_rows | 2 |
| checker_success_rows | 2 |
| exact_rows_local | 2 |
| mismatch_rows_local | 0 |
| timed_rows | 0 |

Manifest boundary flags:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

Runtime outputs were removed after inspection. No `runs/user/` or `output/` runtime artifacts were staged or committed.
