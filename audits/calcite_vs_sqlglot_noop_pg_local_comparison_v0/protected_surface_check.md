# Protected Surface Check

Allowed modifications:

- `audits/calcite_vs_sqlglot_noop_pg_local_comparison_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces:

- `src/`
- `tests/`
- `baselines/`
- `cases/`
- `case_sets/`
- top-level `reports/`
- top-level `results/`
- repository-level `output/`
- `runs/user/`
- external Calcite/SQLSolver/VeriEQL artifacts
- retained evidence

Protected-surface validation result:

- `git status --porcelain -- runs/user output reports results src tests baselines cases case_sets` produced no output.
- No `runs/user`, repository-level `output`, top-level `reports`, or top-level `results` artifacts are staged.
- No source code, tests, baselines, cases, case sets, external artifacts, or retained evidence changed.
- Only the comparison audit packet and project-control files changed.
