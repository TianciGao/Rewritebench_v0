# Protected Surface Check

Allowed changes for this task:

- `project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `audits/port_cross_dialect_diagnostic_execution_plan_v0/*`

Protected surfaces expected unchanged:

- source code under `src/`
- scripts
- tests
- docs outside `project_control/`
- examples
- cases and manifests
- SQL files
- schemas
- checker files
- validation files
- `case_sets/`
- inventory
- reports/results
- benchmark specs
- repository specs
- denominator scaffolds
- paper results
- raw retained evidence
- workflows
- root metadata files
- release tags/branches

Validation result:

- `git diff --check`: passed.
- CSV parse check for `execution_subplan_summary.csv`: passed.
- Markdown sanity checks for new project-control and audit Markdown files: passed.
- Protected-surface status check: passed.
- Changed files are limited to `project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md`, `project_control/DECISION_LOG.md`, `project_control/MIGRATION_STATUS.md`, `project_control/MIGRATION_RUN_LOG.md`, and `audits/port_cross_dialect_diagnostic_execution_plan_v0/*`.
- No source code, scripts, tests, docs outside `project_control`, examples, cases, manifests, SQL files, schemas, checker files, validation files, case sets, inventory, reports/results, benchmark specs, repository specs, denominator scaffolds, paper results, raw retained evidence, workflows, root metadata files, release tags, or release branches were changed.
- No `runs/user/` output was created by this task. Existing ignored `runs/user/` local output remains untracked and was not staged.
