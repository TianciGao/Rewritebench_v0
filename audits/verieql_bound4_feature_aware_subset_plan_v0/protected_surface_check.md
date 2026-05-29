# Protected Surface Check

Allowed release-repo modifications for this task:

- `audits/verieql_bound4_feature_aware_subset_plan_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces that must remain unchanged:

- `src/`
- `tests/`
- `cases/`
- `case_sets/`
- `baselines/`
- `reports/`
- `results/`
- repository-level `output/`
- retained evidence
- `runs/user/`
- `MIGRATION_MASTER_PLAN.md`
- `DECISION_LOG.md`

Preflight status:

- Release repo working tree was clean before changes.
- Staged VeriEQL source tree had pre-existing `M constants.py`; it was not modified by this task.

Final protected-surface validation:

- `git status --short` before staging showed only `project_control/MIGRATION_STATUS.md`, `project_control/MIGRATION_RUN_LOG.md`, and this audit packet changed.
- `git diff --check` passed.
- No `runs/user/` output changes were present.
- No repository-level `output/` runtime artifact changes were present.
- Staged VeriEQL source tree status remained unchanged relative to preflight, except pre-existing `M constants.py`.
