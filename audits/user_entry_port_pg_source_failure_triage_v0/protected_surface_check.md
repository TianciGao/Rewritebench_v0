# Protected Surface Check

Allowed changes for this task:

- `audits/user_entry_port_pg_source_failure_triage_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces expected unchanged:

- source code under `src/`
- scripts
- tests
- docs
- examples
- cases and manifests
- SQL files
- schemas
- checker files
- validation files
- `case_sets/`
- inventory
- reports/results data
- benchmark specs
- repository specs
- raw retained evidence
- workflows
- root metadata files
- release tags/branches

Observed local run output:

- `runs/user/port_pg_source_failure_triage/` was created as ignored local diagnostic output for triage only.
- The run output was not staged and must not be committed.
- The run output was removed before commit after audit summaries were recorded.

Validation result:

- `git diff --check`: passed.
- CSV parse checks for audit CSV files: passed.
- JSON parse check for `targeted_run_summary.json`: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface check: passed.
- `git status --short` shows only `project_control/MIGRATION_STATUS.md`, `project_control/MIGRATION_RUN_LOG.md`, and `audits/user_entry_port_pg_source_failure_triage_v0/`.
- `runs/user/port_pg_source_failure_triage/` is absent and not staged.
