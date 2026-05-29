# Protected Surface Check

Allowed release-repo modifications for this task:

- `audits/verieql_bound4_pg_noop_all_exact_attempt_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces that must remain unchanged:

- `src/`
- `tests/`
- VeriEQL source tree
- `cases/`
- `case_sets/`
- `baselines/`
- `reports/`
- `results/`
- retained evidence
- repository-level `output/`
- `runs/user/`
- `MIGRATION_MASTER_PLAN.md`
- `DECISION_LOG.md`

Runtime files:

- Written only under `/tmp/sqlrb_verieql_bound4_pg_noop_all_exact_attempt_v0/`
- Not committed.

Final protected-surface validation:

- Cached protected-surface check passed; only this audit packet and project-control status/log files were staged.
- `git diff --cached --check` passed.
- No `runs/user/` or repository-level `output/` paths were staged.
- Staged VeriEQL source tree status remained unchanged relative to preflight, except pre-existing `M constants.py`.
