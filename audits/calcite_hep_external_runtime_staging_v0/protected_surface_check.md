# Protected Surface Check

Allowed release-repo modifications:

- `baselines/calcite_hep_fail_closed/adapter.py`
- `baselines/calcite_hep_fail_closed/README.md`
- `tests/user_entry/test_calcite_hep_fail_closed_route.py`
- `audits/calcite_hep_external_runtime_staging_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces unchanged:

- `src/sql_rewrite_bench/`
- `cases/`
- `case_sets/`
- top-level `reports/`
- top-level `results/`
- retained evidence
- repository-level `output/`
- `runs/user/`
- SQLSolver/VeriEQL external artifacts
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Third-party artifacts:

- Calcite source/JAR/class/build outputs staged only outside the release repo.
- No Calcite binary or source artifact is staged for commit.
