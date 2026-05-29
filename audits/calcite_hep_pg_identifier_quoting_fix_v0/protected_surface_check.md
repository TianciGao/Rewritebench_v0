# Protected Surface Check

Allowed changed paths for this task:

- `baselines/calcite_hep_fail_closed/adapter.py`
- `baselines/calcite_hep_fail_closed/README.md`
- focused tests under `tests/user_entry/`
- `audits/calcite_hep_pg_identifier_quoting_fix_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces:

- `cases/`: not modified.
- `case_sets/`: not modified.
- top-level `reports/`: not modified.
- top-level `results/`: not modified.
- repository-level `output/`: not modified.
- `runs/user/`: no committed artifacts.
- retained evidence: not modified or promoted.
- Calcite source/JAR/classes/build outputs: not committed.
- SQLSolver/VeriEQL external artifacts: not modified.
- `MIGRATION_MASTER_PLAN.md`: not modified.
- `DECISION_LOG.md`: not modified.

Runtime artifacts were confined to `/tmp/sqlrb_calcite_hep_pg_identifier_quoting_fix_v0/`.
