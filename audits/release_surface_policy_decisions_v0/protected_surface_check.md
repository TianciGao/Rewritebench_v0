# Protected Surface Check

Allowed changed paths for this task:

- `project_control/RELEASE_SURFACE_POLICY_DECISIONS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `audits/release_surface_policy_decisions_v0/*`

Protected paths that must remain unchanged:

- `src/`
- `scripts/`
- `tests/`
- `docs/`
- `examples/`
- `cases/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- `.github/workflows/`
- `README.md`
- `LICENSE`
- `CITATION.cff`
- `CONTRIBUTING.md`
- `pyproject.toml`
- `.gitignore`
- raw retained evidence

Validation result: passed.

Observed changed paths:

- `project_control/RELEASE_SURFACE_POLICY_DECISIONS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `audits/release_surface_policy_decisions_v0/README.md`
- `audits/release_surface_policy_decisions_v0/decision_summary.csv`
- `audits/release_surface_policy_decisions_v0/implementation_next_steps.md`
- `audits/release_surface_policy_decisions_v0/protected_surface_check.md`
- `audits/release_surface_policy_decisions_v0/command_log.md`

Protected surfaces unchanged:

- source code
- scripts
- tests
- docs outside `project_control`
- examples
- cases/manifests/sql/schema/checker/validation
- `case_sets/`
- inventory
- reports/results
- `benchmark_spec/`
- `repository_spec/`
- raw retained evidence
- top-level `README.md`
- `LICENSE`
- `CITATION.cff`
- `CONTRIBUTING.md`
- release tags/export branches
