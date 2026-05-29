# Protected Surface Check

Allowed modifications:

- `src/sql_rewrite_bench/user_output.py`
- `tests/user_entry/test_user_output.py`
- `audits/user_output_writer_phase2a_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces expected unchanged:

- `src/cli/`
- `scripts/`
- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- `baselines/`
- `reports/`
- `results/`
- repository-level `output/` runtime artifacts
- `benchmarks/`
- retained evidence
- `repository_spec/`
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `runs/user/`

Validation uses `git diff --name-only`, `git status --short`, and a protected-surface path allowlist before commit.
