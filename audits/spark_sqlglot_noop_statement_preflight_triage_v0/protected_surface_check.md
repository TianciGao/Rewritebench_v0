# Protected Surface Check

Allowed surfaces for this task:

- `audits/spark_sqlglot_noop_statement_preflight_triage_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces not modified:

- `src/`
- `tests/`
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

The audit used existing local artifacts under `runs/user/common_core_sqlglot_noop_spark_snapshot/` for diagnosis only. Those outputs are ignored/untracked local run artifacts and are not part of the commit.

Protected-surface validation command:

```bash
git diff --name-only
```

Expected changed paths:

```text
audits/spark_sqlglot_noop_statement_preflight_triage_v0/README.md
audits/spark_sqlglot_noop_statement_preflight_triage_v0/affected_rows.csv
audits/spark_sqlglot_noop_statement_preflight_triage_v0/boundary_checklist.md
audits/spark_sqlglot_noop_statement_preflight_triage_v0/candidate_statement_examples.md
audits/spark_sqlglot_noop_statement_preflight_triage_v0/command_log.md
audits/spark_sqlglot_noop_statement_preflight_triage_v0/protected_surface_check.md
audits/spark_sqlglot_noop_statement_preflight_triage_v0/recommendation.md
audits/spark_sqlglot_noop_statement_preflight_triage_v0/root_cause_matrix.csv
project_control/MIGRATION_RUN_LOG.md
project_control/MIGRATION_STATUS.md
```
