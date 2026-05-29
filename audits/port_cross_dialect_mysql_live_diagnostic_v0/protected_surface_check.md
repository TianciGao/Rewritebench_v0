# Protected Surface Check

Status: passed.

Expected mutation boundary:

- Allowed audit packet: `audits/port_cross_dialect_mysql_live_diagnostic_v0/`.
- Allowed project control updates: `project_control/MIGRATION_STATUS.md` and
  `project_control/MIGRATION_RUN_LOG.md`.
- Local run outputs: `runs/user/port_mysql_source_reference_live/`, ignored and
  not staged.

Protected surfaces that must remain unchanged:

- source code
- scripts
- tests
- docs
- examples
- cases
- manifests
- SQL files
- schema files
- checker files
- validation files
- `case_sets/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- raw retained evidence
- release tags or branches

## Observed Local Output Boundary

- `runs/user/port_mysql_source_reference_live/` exists as local diagnostic
  output.
- `runs/user/port_mysql_source_reference_live/` is ignored by `runs/.gitignore`.
- `git ls-files runs/user/port_mysql_source_reference_live` returned no tracked
  files.
- Local run outputs were not staged.

## Diff Boundary

Only these repository surfaces were intentionally changed:

- `audits/port_cross_dialect_mysql_live_diagnostic_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

No changes were made to source code, scripts, tests, docs, examples, cases,
manifests, SQL files, schema files, checker files, validation files,
`case_sets/`, `reports/`, `results/`, `benchmark_spec/`, `repository_spec/`,
raw retained evidence, release tags, or release branches.

## Validation

- JSON parse check for `live_run_summary.json`: passed.
- CSV parse checks for audit CSV files: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff check: passed.
- `git diff --check`: passed.
- Staged run-output check: passed; no `runs/user/port_mysql_source_reference_live/`
  files were staged.
