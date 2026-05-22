# Final Layout Target

The approved final external/public layout target is:

```text
.github/
benchmarks/
  cases/
  case_sets/
  schemas/
  inventory/
baselines/
docs/
  guide/
  spec/
  templates/
examples/
output/
  results/
  logs/
  reports/
src/
  sql_rewrite_bench/
  cli/
  dev/
CITATION.cff
CONTRIBUTING.md
LICENSE
README.md
pyproject.toml
```

## Semantics

- `benchmarks/` owns benchmark data surfaces: cases, case sets, schemas, and inventory.
- `baselines/` owns baseline adapters and routes.
- `docs/guide`, `docs/spec`, and `docs/templates` own public-facing documentation, specifications, and reusable templates.
- `examples/` owns adapter examples and minimal runnable samples.
- `output/results`, `output/logs`, and `output/reports` own user-run outputs.
- `src/sql_rewrite_bench` remains the core implementation package.
- `src/cli` is the preferred public-facing CLI/facade location.
- `src/dev` owns development and validation tools.

This is a target external layout, not a current-path migration.
