# Protected Surface Check

Protected surfaces intentionally not modified:
- `src/`
- `tests/`
- `baselines/`
- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- top-level `reports/`
- top-level `results/`
- retained evidence
- repository-level `output/`
- `runs/user/`
- external Calcite/SQLSolver/VeriEQL artifacts
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Allowed surfaces modified:
- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Runtime artifacts:
- Written under `/tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/`.
- Not staged or committed.

No official metrics, Semantic Equivalence Rate, formal Regression@20, paper results, retained-evidence promotion, leaderboard output, denominator change, or case-membership change occurred.
