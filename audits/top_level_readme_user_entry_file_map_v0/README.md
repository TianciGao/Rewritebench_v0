# Top-Level README User-Entry File Map

## Purpose

This packet records the documentation-only update adding a Chinese `用户入口数据流与文件位置` section to the top-level `README.md`.

The new README section maps the safe smoke/user-entry path from CLI arguments through metadata-driven case selection, adapter environment variables, candidate capture, local diagnostic outputs, and optional PostgreSQL/checker diagnostic helpers.

## Scope

Files intentionally changed:

- `README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `audits/top_level_readme_user_entry_file_map_v0/`

No source code, scripts, tests, examples, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, denominator scaffolds, paper results, or raw retained evidence were changed.

## Boundary

The README states that `runs/user/<run_name>/...` outputs are local diagnostics only. They are not official metrics, paper tables, reports/results updates, retained evidence, or leaderboard rows. Default smoke remains non-DB and does not run checkers.
