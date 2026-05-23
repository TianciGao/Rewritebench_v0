# Protected Surface Check

Allowed changed paths:

- `audits/calcite_hep_pg_post_quoting_chain_rerun_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces:

- `src/`: not modified.
- `tests/`: not modified.
- `baselines/`: not modified.
- `cases/`: not modified.
- `case_sets/`: not modified.
- top-level `reports/`: not modified.
- top-level `results/`: not modified.
- repository-level `output/`: not modified.
- `runs/user/`: no committed artifacts.
- retained evidence: not modified or promoted.
- Calcite external runtime/source/JAR/classes/build outputs: not modified or committed.
- SQLSolver/VeriEQL artifacts: not modified.
- `MIGRATION_MASTER_PLAN.md`: not modified.
- `DECISION_LOG.md`: not modified.

Runtime output was confined to `/tmp/sqlrb_calcite_hep_pg_post_quoting_chain_rerun_v0/`.
