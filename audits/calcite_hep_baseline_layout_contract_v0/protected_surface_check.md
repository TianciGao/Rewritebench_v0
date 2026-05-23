# Protected Surface Check

Allowed paths changed:

- `baselines/calcite_hep_fail_closed/`
- `src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py` removed.
- `src/sql_rewrite_bench/local_timing.py`
- `tests/user_entry/test_calcite_hep_fail_closed_route.py`
- `audits/calcite_hep_baseline_layout_contract_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected paths not modified:

- `cases/`
- `case_sets/`
- top-level `reports/`
- top-level `results/`
- retained evidence
- repository-level `output/`
- committed `runs/user/`
- `MIGRATION_MASTER_PLAN.md`
- `DECISION_LOG.md`
- SQLSolver/VeriEQL external artifacts

Third-party artifact check:

- No Calcite binaries, JARs, native libraries, source tree, Gradle cache, or build outputs were staged.
