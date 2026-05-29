# Protected Surface Check

Allowed changed paths:

- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/adapter_runner.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `src/sql_rewrite_bench/user_run.py`
- `tests/user_entry/test_u2_module_split.py`
- `audits/user_entry_u2_minimal_split_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces expected unchanged:

- scripts
- docs
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

- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/adapter_runner.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `src/sql_rewrite_bench/user_run.py`
- `tests/user_entry/test_u2_module_split.py`
- `audits/user_entry_u2_minimal_split_v0/README.md`
- `audits/user_entry_u2_minimal_split_v0/module_split_summary.csv`
- `audits/user_entry_u2_minimal_split_v0/behavior_preservation_results.csv`
- `audits/user_entry_u2_minimal_split_v0/test_results.md`
- `audits/user_entry_u2_minimal_split_v0/protected_surface_check.md`
- `audits/user_entry_u2_minimal_split_v0/command_log.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Result: passed. No protected benchmark, case, case-set, report/result, denominator, paper-result, repository-spec, or raw retained-evidence surfaces changed.
