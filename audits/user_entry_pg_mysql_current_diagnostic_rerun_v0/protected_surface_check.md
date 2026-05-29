# Protected Surface Check

Allowed changed surfaces for this task:

- `audits/user_entry_pg_mysql_current_diagnostic_rerun_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces not changed by this task:

- Source code under `src/`
- Scripts
- Tests
- Docs outside this audit packet
- Examples
- Cases and manifests
- SQL files
- Schema files
- Checker files
- Validation files
- `case_sets/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- Raw retained evidence
- Root metadata files
- Release tags or export branches

Boundary confirmations:

- Common-core v0 remains 40 cases.
- Track A same-engine denominator remains 120 planned rows.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Reports/results updated: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- `runs/user/` outputs committed: no.
- Local rerun output directories removed after audit extraction: yes.

Validation status: passed.

Validation details:

- `git diff --check`: passed.
- CSV parse checks for audit CSV files: passed.
- JSON parse check for `run_summary.json`: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff/status check: passed; only this audit packet and the two allowed project-control files changed.
- Local run outputs committed: no.
