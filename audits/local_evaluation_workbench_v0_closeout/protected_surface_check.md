# Protected Surface Check

Allowed tracked changes:

- `audits/local_evaluation_workbench_v0_closeout/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces expected unchanged:

- `src/`
- `tests/`
- `scripts/`
- `cases/`
- `baselines/`
- `case_sets/`
- `reports/`
- `results/`
- retained evidence
- `repository_spec/`
- `benchmark_spec/`
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `runs/user/` tracked outputs

Result:

- No code, tests, scripts, cases, baselines, case sets, reports, results, retained evidence, repository spec, benchmark spec, or tracked run output was modified.
- Existing ignored `runs/user/` local outputs remain uncommitted.
