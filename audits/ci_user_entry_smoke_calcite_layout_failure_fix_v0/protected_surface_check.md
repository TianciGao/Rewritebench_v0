# Protected Surface Check

Allowed paths changed:

- `tests/user_entry/test_calcite_hep_fail_closed_route.py`
- `audits/ci_user_entry_smoke_calcite_layout_failure_fix_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paths intentionally not changed:

- `.github/workflows/user_entry_smoke.yml`
- `scripts/dev/run_user_entry_ci_smoke.py`
- `baselines/calcite_hep_fail_closed/adapter.py`
- `cases/`
- `case_sets/`
- `reports/`
- `results/`
- retained evidence
- repository-level `output/`
- committed `runs/user/`
- `MIGRATION_MASTER_PLAN.md`
- `DECISION_LOG.md`

Calcite layout:

- Adapter remains at `baselines/calcite_hep_fail_closed/adapter.py`.
- No Calcite binaries, JARs, build outputs, source trees, or dependency caches were staged.
