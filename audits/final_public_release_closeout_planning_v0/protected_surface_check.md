# Protected Surface Check

This planning audit is allowed to write only:

- `audits/final_public_release_closeout_planning_v0/*`
- `project_control/MIGRATION_RUN_LOG.md`
- `project_control/MIGRATION_STATUS.md`

Protected surfaces that must remain unchanged:

- `cases/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- `scripts/`
- `tests/`
- `src/`
- manifests, schemas, checker files, validation files, SQL files, and raw retained evidence

## Planned Validation

- `git diff --check`
- JSON parse check for `release_readiness_summary.json`
- CSV parse check for `release_readiness_matrix.csv`
- Protected-path diff check confirming only the allowed audit packet and project-control files changed
- Static Common-core case-package validators only; no DB/checker execution, metrics computation, paper rendering, retained-evidence parsing, or leaderboard generation

## Boundary Result

Passed.

- `git status --porcelain` showed only this audit packet plus `project_control/MIGRATION_STATUS.md` and `project_control/MIGRATION_RUN_LOG.md`.
- No case files changed.
- No schemas changed.
- No `case_sets/` files changed.
- No inventory files changed.
- No reports/results files changed.
- No denominator scaffolds changed.
- No paper results changed.
- No official metrics were computed.
- No DB/checker execution was run.
- No global leaderboard was created.
- No release tag or export branch was created.
