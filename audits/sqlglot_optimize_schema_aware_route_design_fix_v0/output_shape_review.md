# Output Shape Review

Runtime outputs for the bounded smoke were written under:

```text
/tmp/sqlrb_sqlglot_optimize_schema_aware_route_design_fix_v0/
```

No runtime artifacts were intentionally written to:
- `runs/user/`
- repository-level `output/`
- top-level `reports/`
- top-level `results/`

The adapter remains compatible with the user-entry candidate file contract:
- reads `SQLRB_SOURCE_SQL_PATH`
- reads `SQLRB_CASE_DIR`
- writes `SQLRB_CANDIDATE_SQL_PATH`
- writes status metadata under `SQLRB_WORKSPACE_DIR`

Future user-facing reruns should use the D035 exported output shape:
- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

`runs/user/<run_id>/` remains internal transitional staging only.
