# Protected Surface Check

Allowed changed surfaces:

- `src/sql_rewrite_bench/verifier_support/verieql.py`
- `tests/user_entry/test_verieql_support.py`
- `audits/verieql_adapter_jsonl_compatibility_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces not modified:

- VeriEQL source tree
- legacy repo files
- `cases/`
- `case_sets/`
- `baselines/`
- top-level `reports/`
- top-level `results/`
- committed `output/` runtime artifacts
- `benchmarks/`
- retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `runs/user/`

Legacy repo status:

- Legacy repo had pre-existing dirty state with `1280` porcelain entries.
- This task did not modify legacy repo files or the staged VeriEQL source tree.
