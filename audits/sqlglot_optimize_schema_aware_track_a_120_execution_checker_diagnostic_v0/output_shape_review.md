# Output Shape Review

## Committed Audit Outputs

- `per_row_execution_checker_status.csv`
- `diagnostic_summary.json`
- `route_card.csv`
- `route_card.json`
- audit Markdown files in this packet
- audit-scoped helper `run_track_a_120_checker.py`

## Runtime Outputs

Runtime outputs stayed under:

`/tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/`

The helper wrote D035-shaped local output under:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

## Protected Surfaces

No runtime artifacts were committed from:

- `runs/user/`
- repository-level `output/`
- top-level `reports/`
- top-level `results/`

The route card in this audit is local diagnostic evidence only.
