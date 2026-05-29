# User Command

The public D035 facade still stages user runs through repository-local `runs/user/<run_id>` before export. To keep this diagnostic's runtime artifacts entirely under `/tmp`, the pass used an audit-scoped helper that calls the same user-entry adapter, preflight, DB execution, and checker internals.

Equivalent route command embedded in the helper:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware
```

Audit helper command:

```bash
PYTHONPATH=src python audits/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/run_track_a_120_checker.py
```

D035-shaped runtime roots:

- `/tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/output/results/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/`
- `/tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/output/logs/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/`
- `/tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/output/reports/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/`
