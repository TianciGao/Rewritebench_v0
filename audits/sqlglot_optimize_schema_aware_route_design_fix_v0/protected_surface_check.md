# Protected Surface Check

Protected surfaces intentionally not modified:
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

Allowed code/test surfaces modified:
- `baselines/sqlglot/`
- `tests/user_entry/`

Runtime artifacts:
- Smoke runtime artifacts were written only under `/tmp/sqlrb_sqlglot_optimize_schema_aware_route_design_fix_v0/`.
- Only audit summaries were committed.

No official metrics, Semantic Equivalence Rate, formal Regression@20, paper reports/results, retained-evidence promotion, leaderboard output, denominator change, or case membership change occurred.
