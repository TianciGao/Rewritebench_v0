# Protected Surface Check

## Intended Modified Paths

- `audits/port_cross_dialect_checker_normalization_audit_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Protected Surfaces

This audit must not modify:

- source code under `src/`
- scripts
- tests
- docs
- examples
- cases, manifests, SQL, schemas, checker configs, or validation files
- `case_sets/`
- `reports/` or `results/`
- `benchmark_spec/` or `repository_spec/`
- raw retained evidence
- release tags or branches

## Validation Result

- `git diff --check`: passed.
- CSV parse checks for audit CSV files: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff check: passed.
- Staged-file check before commit: passed; no run outputs were staged.
- `runs/user/port_pg_target_reference_controlled/`: ignored local output only, not staged.

Changed-path allowlist confirmed only:

- `audits/port_cross_dialect_checker_normalization_audit_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
