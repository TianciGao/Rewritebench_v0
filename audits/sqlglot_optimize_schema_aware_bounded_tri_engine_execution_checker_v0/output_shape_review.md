# Output Shape Review

Runtime artifacts were written under:

```text
/tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/
```

The audit helper used existing adapter, execution, and checker functions directly so runtime files stayed outside the repository.

No runtime artifacts were intentionally written or staged under:
- `runs/user/`
- repository-level `output/`
- top-level `reports/`
- top-level `results/`

Committed audit outputs:
- `per_row_execution_checker_status.csv`
- `diagnostic_summary.json`
- Markdown review files
- audit-scoped helper script

Future user-facing reruns should use the D035 exported output shape:
- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

This audit does not promote the runtime artifacts to retained evidence or paper surfaces.
