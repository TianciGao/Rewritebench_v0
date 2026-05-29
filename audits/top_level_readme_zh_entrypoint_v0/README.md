# Top-Level Chinese README Entrypoint

## Purpose

This packet records the documentation-only rewrite of the top-level `README.md` as a Chinese public entrypoint for SQL-RewriteBench.

The README now explains:

- What SQL-RewriteBench evaluates.
- The current `Common-core v0` public scope.
- The safe one-command public smoke path.
- The user adapter contract.
- Optional local PostgreSQL diagnostics.
- How to read a case package.
- Repository directory roles.
- Benchmark interpretation boundaries.

## Scope

Files intentionally changed:

- `README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `audits/top_level_readme_zh_entrypoint_v0/`

No source code, tests, examples, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, denominator scaffolds, paper results, or raw retained evidence were changed.

## Validation Summary

Final validation is recorded in `smoke_results.csv` and `command_log.md`.

The documented public smoke commands were run exactly as shown in the top-level README. Both are non-DB by default and write only local diagnostics under `runs/user/...`; local outputs were removed after recording results.
