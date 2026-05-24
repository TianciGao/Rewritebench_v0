# Protected Surface Check

Protected surfaces:

- `cases/`: unchanged.
- `case_sets/`: unchanged.
- `schemas/`: unchanged.
- `inventory/`: unchanged.
- top-level `reports/`: unchanged.
- top-level `results/`: unchanged.
- repository-level `output/`: unchanged.
- committed `runs/user/`: unchanged.
- retained evidence: unchanged.
- external Calcite runtime/source/JAR/classes/build outputs: unchanged.
- SQLSolver/VeriEQL artifacts: unchanged.
- `project_control/MIGRATION_MASTER_PLAN.md`: unchanged.
- `project_control/DECISION_LOG.md`: unchanged.

Runtime outputs were local-only under:

`/tmp/sqlrb_calcite_hep_tri_engine_readiness_and_adapter_gap_v0/`

Ignored `runs/user/<run_id>/` staging may exist locally from the user-facade
run, but it is not staged or committed.
