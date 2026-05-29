# Master Plan Layout Delta

Before this task, `MIGRATION_MASTER_PLAN.md` still presented an older public release layout as the active target. That older target included top-level active entries such as:

- `cases/`
- `case_sets/`
- `inventory/`
- `scripts/`
- `reports/`
- `results/`

After this task, the layout section records D035 as the authoritative target:

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

The plan now explicitly says the old top-level layout is superseded as the final public target, while current working paths remain valid until a separately authorized physical migration/export task.

No historical decisions were rewritten.
No physical layout migration was performed.
