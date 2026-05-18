# Run Artifact Policy

This policy separates legacy retained evidence, local user-run outputs, curated reports, and curated results.

## Case-local Runs

Case-local `runs/` directories are legacy retained evidence surfaces. They must not be deleted, rewritten, bulk-moved, or used as the default destination for new public runner outputs.

## User-run Outputs

User-run outputs belong only under:

```text
runs/user/<run_id>/
```

These files are local experiment outputs. They are not retained paper evidence, not official results, not paper tables, and not leaderboard entries.

The user runner must not write into:

- `cases/`
- case-local `runs/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`

Smoke outputs under `runs/user/` must not be committed. The `runs/.gitignore` file keeps local run outputs ignored by default.

## Curated Results And Reports

`results/retained/` is reserved for curated retained evidence only after separate authorization. User-run outputs must not be written there.

`reports/evaluation/` and `reports/paper/` are reserved for curated evaluation or release reports only after separate authorization. User-run reports must not be written there.

## No Global Leaderboard

SQL-RewriteBench does not create a global leaderboard. User-run reports may include local diagnostic counts for a single run, but they must not claim official ranking, paper-result status, or retained-evidence status.
