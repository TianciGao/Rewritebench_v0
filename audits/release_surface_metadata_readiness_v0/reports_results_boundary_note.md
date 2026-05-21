# Reports / Results Boundary Note

## User-Entry Outputs

User-entry outputs stay under `runs/user/{run_name}/`. They are local diagnostics only.

They do not update:

- `reports/`
- `results/`
- paper tables
- retained evidence
- official metric inputs
- leaderboards

## Current Reports / Results Surface

`reports/` and `results/` are currently absent from the release surface. That is preferable to including stale or unauthorized outputs, but public release readiness needs a deliberate policy:

- either add clear placeholder README files later, or
- add curated paper-facing artifacts only after separate authorization.

## Prohibited in This Phase

- No reports/results migration.
- No paper table rendering.
- No retained evidence promotion.
- No official metrics computation.
- No global leaderboard.

## Safe Future Placeholder Boundary

If placeholder directories are authorized, their README files should state that public smoke and user-entry local diagnostics do not write to `reports/` or `results/`, and that official paper-facing artifacts require a separate controlled workflow.
