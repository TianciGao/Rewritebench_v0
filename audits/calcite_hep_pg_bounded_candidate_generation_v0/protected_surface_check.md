# Protected Surface Check

Allowed release-repo modifications for this task:

- `audits/calcite_hep_pg_bounded_candidate_generation_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces expected unchanged:

- `baselines/calcite_hep_fail_closed/adapter.py` source code
- `src/`
- `tests/`
- `cases/`
- `case_sets/`
- top-level `reports/`
- top-level `results/`
- retained evidence
- repository-level `output/`
- `runs/user/`
- SQLSolver/VeriEQL external artifacts
- Calcite source/JAR/class/build outputs
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Validation result:

- `git diff --check`: passed.
- `git status --porcelain -- runs/user output reports results`: no output.
- Tracked Calcite artifact scan found no Calcite JAR/class/build artifacts in the release repo.
- Changed release-repo paths before staging were limited to this audit packet and `project_control/MIGRATION_STATUS.md`; `project_control/MIGRATION_RUN_LOG.md` is updated by the required project-control writeback.
- Runtime outputs remain under `/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0/`.
