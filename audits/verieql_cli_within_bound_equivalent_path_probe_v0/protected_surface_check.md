# Protected Surface Check

## Allowed Release Repo Changes

Allowed and changed:

- `audits/verieql_cli_within_bound_equivalent_path_probe_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Protected Release Repo Surfaces

No changes were made to:

- `src/`
- `tests/`
- `cases/`
- `case_sets/`
- `baselines/`
- `reports/`
- `results/`
- repository-level `output/`
- retained evidence
- `runs/user/`
- `MIGRATION_MASTER_PLAN.md`
- `DECISION_LOG.md`

## External VeriEQL Tree

The staged VeriEQL source tree was not modified. Preflight and final status both showed only the pre-existing `M constants.py`.

## Runtime Artifacts

Probe runtime files were written only under:

`/tmp/sqlrb_verieql_cli_within_bound_equivalent_path_probe_v0/`

Those runtime artifacts were not committed.
