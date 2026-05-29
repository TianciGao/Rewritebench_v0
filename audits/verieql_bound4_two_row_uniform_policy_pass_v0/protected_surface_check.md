# Protected Surface Check

Allowed release-repo changes:
- `audits/verieql_bound4_two_row_uniform_policy_pass_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected paths:
- `src/`: unchanged.
- `tests/`: unchanged.
- `cases/`: unchanged.
- `case_sets/`: unchanged.
- `baselines/`: unchanged.
- `reports/`: unchanged.
- `results/`: unchanged.
- repository-level `output/`: unchanged.
- `runs/user/`: unchanged.
- `MIGRATION_MASTER_PLAN.md`: unchanged.
- `DECISION_LOG.md`: unchanged.

Runtime artifacts:
- Runtime/probe files were written only under `/tmp/sqlrb_verieql_bound4_two_row_uniform_policy_pass_v0/`.
- Runtime files are not committed.

External VeriEQL source tree:
- `/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL` was not modified.
- Pre-existing `M constants.py` remains.

