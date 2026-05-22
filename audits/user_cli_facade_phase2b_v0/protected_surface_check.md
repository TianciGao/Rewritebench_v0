# Protected Surface Check

Allowed surfaces changed:

- `src/cli/`
- `tests/user_entry/test_cli_facade.py`
- `pyproject.toml`
- `audits/user_cli_facade_phase2b_v0/`
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

Runtime-output checks:

- No `runs/user/` outputs staged or committed.
- No `output/` runtime artifacts staged or committed.

Behavior boundaries:

- No verifier integration implemented.
- No official metrics computed.
- No timing/speedup computed.
- No top-level reports/results updated.
- No retained evidence promoted.
- No leaderboard created.
