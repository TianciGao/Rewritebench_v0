# Protected Surface Check

Allowed changed paths:

- `LICENSE`
- `CITATION.cff`
- `CONTRIBUTING.md`
- `.gitignore`
- `benchmark_spec/*.md`
- `reports/README.md`
- `results/README.md`
- `docs/README.md`
- `audits/release_surface_metadata_polish_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected paths:

- `src/`
- `scripts/`
- `tests/`
- `examples/`
- `cases/`
- `case_sets/`
- `inventory/`
- existing report/result data files beyond boundary README files
- `repository_spec/`
- raw retained evidence
- `.github/workflows/`
- root `README.md`
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- release tags/export branches

Validation result: passed.

Observed changed paths:

- `LICENSE`
- `benchmark_spec/scope.md`
- `reports/README.md`
- `results/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `audits/release_surface_metadata_polish_v0/README.md`
- `audits/release_surface_metadata_polish_v0/polished_files_inventory.csv`
- `audits/release_surface_metadata_polish_v0/readability_check.md`
- `audits/release_surface_metadata_polish_v0/license_citation_check.md`
- `audits/release_surface_metadata_polish_v0/protected_surface_check.md`
- `audits/release_surface_metadata_polish_v0/command_log.md`

Protected surfaces unchanged:

- source code
- scripts
- tests
- examples
- cases/manifests/sql/schema/checker/validation
- `case_sets/`
- inventory
- existing report/result data beyond boundary README files
- `repository_spec/`
- raw retained evidence
- `.github/workflows/`
- root `README.md`
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- release tags/export branches
