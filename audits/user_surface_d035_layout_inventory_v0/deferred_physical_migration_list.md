# Deferred Physical Migration List

The following D035 target moves must wait for separately authorized physical migration or export-layout tasks:

- Move `cases/` to `benchmarks/cases/`.
- Move `case_sets/` to `benchmarks/case_sets/`.
- Move `schemas/` to `benchmarks/schemas/`.
- Move `inventory/` to `benchmarks/inventory/`.
- Move or mirror `scripts/dev/` into `src/dev/`.
- Reorganize docs into `docs/guide/`, `docs/spec/`, and `docs/templates/`.
- Rework internal source-run staging away from `runs/user/<run_id>/`, if desired.

Reasons to defer:

- case path resolvers, validators, tests, manifests, docs, and audit references still assume current working paths.
- D035 explicitly records that physical migration is not authorized yet.
- broad moves risk denominator, case membership, evidence, and validation instability.

Safe now:

- Audit-only documentation of current state.
- Future narrow docs cleanup.
- Future narrow output-contract tests or CLI help wording cleanup if separately authorized.

Not safe now:

- Moving benchmark data under `benchmarks/`.
- Moving all development scripts under `src/dev/`.
- Rewriting runner storage paths broadly.
