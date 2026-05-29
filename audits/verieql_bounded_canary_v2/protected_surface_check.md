# Protected Surface Check

Allowed surfaces changed:

- `src/sql_rewrite_bench/verifier_support/verieql.py`
- shared verifier-support helpers only as needed
- `tests/user_entry/test_verieql_support.py`
- `audits/verieql_bounded_canary_v2/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces unchanged:

- `baselines/`
- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- `reports/`
- `results/`
- `output/`
- `benchmarks/`
- retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Runtime artifacts:

- No `runs/user/` outputs staged or committed.
- No `output/` runtime artifacts staged or committed.
