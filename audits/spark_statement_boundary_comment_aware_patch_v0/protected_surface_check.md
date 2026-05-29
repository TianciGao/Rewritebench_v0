# Protected Surface Check

Allowed modified surfaces:

- `src/sql_rewrite_bench/candidate_preflight.py`
- `src/sql_rewrite_bench/spark_execution.py`
- `tests/user_entry/`
- `audits/spark_statement_boundary_comment_aware_patch_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces not modified:

- `baselines/sqlglot/`
- `cases/`
- manifests
- SQL files
- schemas
- checker configs
- validation scripts
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `runs/user/` tracked outputs

Expected changed paths:

```text
src/sql_rewrite_bench/candidate_preflight.py
src/sql_rewrite_bench/spark_execution.py
tests/user_entry/test_candidate_preflight.py
audits/spark_statement_boundary_comment_aware_patch_v0/README.md
audits/spark_statement_boundary_comment_aware_patch_v0/patch_summary.md
audits/spark_statement_boundary_comment_aware_patch_v0/regression_tests.md
audits/spark_statement_boundary_comment_aware_patch_v0/affected_rows_before_after.csv
audits/spark_statement_boundary_comment_aware_patch_v0/command_log.md
audits/spark_statement_boundary_comment_aware_patch_v0/protected_surface_check.md
audits/spark_statement_boundary_comment_aware_patch_v0/boundary_checklist.md
project_control/MIGRATION_STATUS.md
project_control/MIGRATION_RUN_LOG.md
```

`runs/user/` outputs were created for local diagnostics only and are not staged or committed.
