# Protected Surface Check

Repository surfaces unchanged:

- `src/`
- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- top-level `reports/`
- top-level `results/`
- repository-level `output/`
- committed `runs/user/`
- retained evidence
- SQLSolver / VeriEQL artifacts
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Runtime artifacts:

- Bounded validation output was written only under
  `/tmp/sqlrb_calcite_hep_target_dialect_runtime_mode_v0/`.
- User-run internal staging under `runs/user/<run_id>/` is ignored and not
  staged.

External Calcite runtime:

- External source/classes under
  `/home/tianci_gao/.local/share/sqlrb/calcite_hep/` were changed locally to
  stage target dialect mode.
- No external runtime source, class, JAR, dependency cache, or build output is
  part of the release repository commit.
