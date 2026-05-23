# Protected Surface Check

Allowed release-repo modifications:

- `audits/verieql_longtail0023_non_equivalent_triage_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces:

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

Runtime output:

- Written only under `/tmp/sqlrb_verieql_longtail0023_non_equivalent_triage_v0/`.
- Not committed.

Final protected-surface validation:

- `git diff --check` passed.
- `git status -sb` before staging showed only this audit packet and project-control status/log files changed.
- No `runs/user/` or repository-level `output/` runtime artifact paths were changed.
- Staged VeriEQL source tree status remained unchanged relative to preflight, except pre-existing `M constants.py`.
