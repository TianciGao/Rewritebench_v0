# Protected Surface Check

Allowed release-repo changes:

- `audits/legacy_baseline_smoke_verifier_clue_audit_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces not modified:

- `src/`
- `tests/`
- `scripts/`
- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- `baselines/`
- `reports/`
- `results/`
- `output/`
- `benchmarks/`
- retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `runs/user/`

Legacy repo modification status:

- Legacy repo `/home/tianci_gao/code/sql-rewrite-bench` had pre-existing dirty state: `1280` porcelain entries observed.
- This task used read-only commands only and did not modify legacy files.
