# Protected Surface Check

Changed surfaces:

- `src/cli/main.py`
- `tests/user_entry/test_cli_facade.py`
- `audits/user_cli_facade_phase2b_review_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces unchanged:

- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- `baselines/`
- `reports/`
- `results/`
- `benchmarks/`
- retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Runtime artifacts:

- No `runs/user/` outputs staged or committed.
- No `output/` runtime artifacts staged or committed.

Boundary:

- No VeriEQL or SQLSolver implementation.
- No full Common-core run.
- No SQLGlot optimize run.
- No timing collection.
- No official metrics.
- No top-level reports/results update.
- No retained-evidence promotion.
- No leaderboard output.
