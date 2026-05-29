# Protected Surface Check

Allowed changed paths:

- `audits/user_entry_common_core_pg_local_diagnostic_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected paths:

- source code
- scripts
- tests
- docs
- examples
- cases/manifests/sql/schema/checker/validation
- `case_sets/`
- inventory
- reports/results data
- benchmark_spec
- repository_spec
- raw retained evidence
- workflows
- root metadata files
- release tags/export branches

Validation result: passed.

Local run output policy:

- `runs/user/common_core_pg_noop_db_checker/` is local diagnostic output.
- The run output directory must not be staged or committed.

Observed changed paths:

- `audits/user_entry_common_core_pg_local_diagnostic_v0/README.md`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/run_summary.json`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/funnel_counts.csv`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/failure_bucket_summary.csv`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/tag_slice_summary.csv`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/environment_check.md`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/command_log.md`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/protected_surface_check.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
