# Protected Surface Check

Allowed release-repo paths changed:

- `src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py`
- `src/sql_rewrite_bench/local_timing.py`
- `tests/user_entry/test_calcite_hep_fail_closed_route.py`
- `audits/calcite_hep_fail_closed_user_route_scaffold_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected paths not modified:

- `cases/`
- `case_sets/`
- `baselines/`
- top-level `reports/`
- top-level `results/`
- retained evidence
- repository-level `output/`
- committed `runs/user/`
- `MIGRATION_MASTER_PLAN.md`
- `DECISION_LOG.md`

Third-party artifact check:

- No Calcite source tree, JAR, native library, Gradle cache, or build output was staged.
- No SQLSolver or VeriEQL external artifact was staged.
