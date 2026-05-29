# D035 Alignment Summary

The master plan now aligns with D035 in these ways:

- `benchmarks/` is the final public target for `cases/`, `case_sets/`, `schemas/`, and `inventory/`.
- `src/cli` is the target public-facing CLI/facade location.
- `src/sql_rewrite_bench` remains the internal implementation package.
- `src/dev` is the target location for development and validation tools.
- Local user-run output is `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- Top-level `reports/` and `results/` remain official/paper/release-facing surfaces and are distinct from local `output/`.
- Physical migration is deferred until path resolvers, validators, tests, docs, and references are ready.

Current working paths remain valid:

- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- `scripts/`

This sync does not authorize moving those paths.
