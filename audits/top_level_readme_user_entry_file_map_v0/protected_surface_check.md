# Protected Surface Check

Allowed write surfaces for this task:

- `README.md`
- `audits/top_level_readme_user_entry_file_map_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces that must remain unchanged:

- `src/`
- scripts
- tests
- examples
- docs other than top-level `README.md`
- `cases/`
- manifests
- `sql/`
- `schema/`
- `checker/`
- `validation/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- raw retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

## Boundary Result

Final protected-surface diff check passed.

Changed paths were limited to:

- `README.md`
- `audits/top_level_readme_user_entry_file_map_v0/README.md`
- `audits/top_level_readme_user_entry_file_map_v0/smoke_results.csv`
- `audits/top_level_readme_user_entry_file_map_v0/command_log.md`
- `audits/top_level_readme_user_entry_file_map_v0/protected_surface_check.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

No source code, scripts, tests, examples, docs other than top-level `README.md`, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, denominator scaffolds, paper results, raw retained evidence, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md` were changed.

The documented smoke commands created local outputs under `runs/user/`; those outputs were removed after recording results.
