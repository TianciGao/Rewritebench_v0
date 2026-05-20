# Protected Surface Check

Allowed changed paths for this task:

- `audits/user_entry_output_schema_audit_v0/README.md`
- `audits/user_entry_output_schema_audit_v0/current_output_files.csv`
- `audits/user_entry_output_schema_audit_v0/current_ledger_fields.csv`
- `audits/user_entry_output_schema_audit_v0/current_summary_fields.csv`
- `audits/user_entry_output_schema_audit_v0/current_failure_fields.csv`
- `audits/user_entry_output_schema_audit_v0/status_value_inventory.csv`
- `audits/user_entry_output_schema_audit_v0/target_funnel_gap_matrix.csv`
- `audits/user_entry_output_schema_audit_v0/proposed_user_run_row_schema.csv`
- `audits/user_entry_output_schema_audit_v0/proposed_failure_bucket_policy.md`
- `audits/user_entry_output_schema_audit_v0/output_schema_gap_list.md`
- `audits/user_entry_output_schema_audit_v0/future_u2_prompt.md`
- `audits/user_entry_output_schema_audit_v0/command_log.md`
- `audits/user_entry_output_schema_audit_v0/protected_surface_check.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces expected unchanged:

- source code under `src/`
- scripts
- tests
- docs outside `project_control/`
- examples
- cases, manifests, SQL, schemas, checker files, validation files
- `case_sets/`
- inventory
- reports and results
- benchmark specs
- repository specs
- denominator scaffolds
- paper results
- raw retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`

Observed changed paths:

- `audits/user_entry_output_schema_audit_v0/README.md`
- `audits/user_entry_output_schema_audit_v0/current_output_files.csv`
- `audits/user_entry_output_schema_audit_v0/current_ledger_fields.csv`
- `audits/user_entry_output_schema_audit_v0/current_summary_fields.csv`
- `audits/user_entry_output_schema_audit_v0/current_failure_fields.csv`
- `audits/user_entry_output_schema_audit_v0/status_value_inventory.csv`
- `audits/user_entry_output_schema_audit_v0/target_funnel_gap_matrix.csv`
- `audits/user_entry_output_schema_audit_v0/proposed_user_run_row_schema.csv`
- `audits/user_entry_output_schema_audit_v0/proposed_failure_bucket_policy.md`
- `audits/user_entry_output_schema_audit_v0/output_schema_gap_list.md`
- `audits/user_entry_output_schema_audit_v0/future_u2_prompt.md`
- `audits/user_entry_output_schema_audit_v0/command_log.md`
- `audits/user_entry_output_schema_audit_v0/protected_surface_check.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Result: passed. Only the allowed audit packet and project-control writeback files changed.
