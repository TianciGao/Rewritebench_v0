# Current vs Target Layout Delta

The current construction repository still uses legacy/construction paths. D035 records the target layout but does not move anything.

## Current Construction Paths

- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- `scripts/`
- `docs/`
- `templates/`
- `reports/`
- `results/`
- `src/sql_rewrite_bench/`
- `audits/`
- `project_control/`
- `repository_spec/`
- `benchmark_spec/`
- `runs/`

## Target Public Paths

- `benchmarks/cases/`
- `benchmarks/case_sets/`
- `benchmarks/schemas/`
- `benchmarks/inventory/`
- `docs/guide/`
- `docs/spec/`
- `docs/templates/`
- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`
- `src/sql_rewrite_bench/`
- `src/cli/`
- `src/dev/`

## Deferred Physical Migration

Physical migration is deferred because current path resolvers, validators, tests, audits, and Common-core denominator references still expect current construction paths. A later layout migration/export task must update those references deliberately and validate them before any final public export.

Top-level `reports/` and `results/` are not changed by this task. The new `output/results/` path is for local/user-run output and does not authorize paper or official result updates.
