# Protected Surface Check

Allowed changed paths for this task:

- `README.md`
- `docs/USER_ENTRY_DATA_FLOW.md`
- `audits/user_entry_data_flow_doc_v0/README.md`
- `audits/user_entry_data_flow_doc_v0/smoke_results.csv`
- `audits/user_entry_data_flow_doc_v0/command_log.md`
- `audits/user_entry_data_flow_doc_v0/protected_surface_check.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces expected unchanged:

- source code under `src/`
- scripts
- tests
- examples
- cases, manifests, SQL, schemas, checker files, and validation files
- `case_sets/`
- inventory
- reports and results
- denominator scaffolds
- paper results
- raw retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Observed changed paths:

- `README.md`
- `docs/USER_ENTRY_DATA_FLOW.md`
- `audits/user_entry_data_flow_doc_v0/README.md`
- `audits/user_entry_data_flow_doc_v0/smoke_results.csv`
- `audits/user_entry_data_flow_doc_v0/command_log.md`
- `audits/user_entry_data_flow_doc_v0/protected_surface_check.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Result: passed. Only allowed documentation, audit, and project-control files changed.
