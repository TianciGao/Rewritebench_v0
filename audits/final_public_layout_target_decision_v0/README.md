# Final Public Layout Target Decision v0

Verdict: `completed`

This audit records the team-approved final external/public repository layout target. It is decision/spec/audit only.

No directories were moved, renamed, created as runtime surfaces, or migrated. Current construction paths remain valid until a separate physical layout migration or export-layout restructuring task is authorized.

## Decision

Recorded as D035 in `project_control/DECISION_LOG.md`.

The final public layout target is:

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

Future output contract and CLI contract work must align to this target. In particular, user-run outputs should be designed around:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

`src/cli` is the preferred public-facing CLI/facade location. `src/sql_rewrite_bench` remains the internal implementation package.

## Boundary

This task did not implement `output/`, CLI, verifier support, metrics, timing, retained-evidence promotion, paper rendering, reports/results updates, or leaderboard output. It did not change denominators, case membership, paper results, raw retained evidence, or physical repository layout.

## Next Safe Action

Authorize D034/D035 Step 1: design the `output/results|logs|reports/<run_id>/` contract and user-facing CLI/interface contract against the final layout target, still without moving current repository directories.
