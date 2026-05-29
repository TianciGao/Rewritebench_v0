# Protected Surface Check

## Changed Surfaces

Allowed release-repo changes:

- `audits/local_verieql_raw_directory_probe_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Unchanged Protected Surfaces

No intended changes to:

- `src/`
- `tests/`
- `scripts/`
- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- `baselines/`
- `reports/`
- `results/`
- `output/`
- retained evidence
- `runs/user/`
- `/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql`

## Raw VeriEQL Directory Status

The staged VeriEQL checkout reported a pre-existing local modification:

```text
M constants.py
```

This task did not modify it and did not create new files in the raw directory.

## Validation Result

Validation confirmed that release-repo changes were limited to:

- `audits/local_verieql_raw_directory_probe_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

No `runs/user/` or `output/` runtime artifacts were staged.
