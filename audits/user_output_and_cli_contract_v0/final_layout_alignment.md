# Final Layout Alignment

This contract is aligned with D034 and D035.

## D034 Alignment

- Defines the Step 1 user-facing output and CLI/interface contract.
- Promotes failure bucket and tag-slice summaries into the future user output report surface.
- Keeps verifier support separate from rewrite baselines.
- Preserves route-aware and denominator-aware local workbench boundaries.

## D035 Alignment

- Uses `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- Uses `src/cli` as the future public facade target.
- Keeps `src/sql_rewrite_bench` as the internal implementation package.
- Does not physically migrate current paths into `benchmarks/`.

## Deferred Layout Work

This task does not create or migrate:

- `benchmarks/`
- `output/` runtime directories
- `src/cli`
- `src/dev`

Physical layout migration remains deferred until path resolvers, tests, validators, docs, and case-set references are ready.
