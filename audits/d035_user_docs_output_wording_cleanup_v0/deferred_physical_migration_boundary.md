# Deferred Physical Migration Boundary

This task did not move repository data or implementation directories.

Deferred until separate authorization:

- Move `cases/`, `case_sets/`, `schemas/`, or `inventory/` into `benchmarks/`.
- Move `scripts/dev/` into `src/dev/`.
- Rework internal `runs/user/<run_id>/` staging.
- Change path resolvers, validators, case-set membership, denominator files, reports, results, retained evidence, or benchmark data.

Current working paths remain valid:

- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- `scripts/dev/`

D035 final public target remains documented, but physical migration is not
complete and was not attempted here.
