# Protected Path Review

Allowed write surface:

- `src/sql_rewrite_bench/pocr/`
- `tests/pocr/`
- `audits/pocr_candidate_resolver_draft_runner_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected paths:

- `cases/`
- `skills.md`
- `skill/`
- `output/`
- top-level `reports/`
- top-level `results/`
- `runs/`
- retained evidence
- paper result files
- env files
- API keys and secrets

Review result:

- No case package file was modified.
- No `skills.md` file was modified.
- No `skill/` folder was created.
- No `output/`, top-level `reports/`, top-level `results/`, or `runs/` file was created or modified by this task.
- Existing candidate SQL files under `runs/user/common_core_pg_noop_db_checker/candidate_sql/` were read-only inputs and were not staged.
- `cases.zip`, Zone.Identifier sidecars, and unrelated untracked audit directories were left untracked.
