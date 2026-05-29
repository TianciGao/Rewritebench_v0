# Local Engine Environment Setup v0

This audit packet records the local engine environment setup helper layer.

Task scope:

- Environment setup and documentation only.
- No DB execution backend changes.
- No source execution logic changes.
- No case, manifest, SQL, schema, checker, validation, or case-set changes.
- No metrics, timing, speedup, paper tables, reports/results updates, retained-evidence promotion, or leaderboard.

Files added by the setup layer:

- `docs/LOCAL_ENGINE_SETUP.md`
- `scripts/env_postgres.example.sh`
- `scripts/env_mysql.example.sh`
- `scripts/env_spark.example.sh`
- `scripts/env_all.example.sh`
- `scripts/dev/check_local_engine_env.py`

Supporting changes:

- `.gitignore` now ignores `scripts/env_*.local.sh`, `.env`, and `.env.local` while preserving `runs/user/` as the local user-output ignore and not ignoring all of `runs/`.
- `project_control/MIGRATION_STATUS.md` and `project_control/MIGRATION_RUN_LOG.md` record the task outcome.

Validation summary:

- `git diff --check`: passed.
- `bash -n` passed for all four environment example scripts.
- `PYTHONPATH=src python -m py_compile scripts/dev/check_local_engine_env.py`: passed.
- `python scripts/dev/check_local_engine_env.py`: passed and reported missing optional engine config without failing.
- `.gitignore` checks passed: `runs/user/` ignored, whole `runs/` not ignored, and `scripts/env_mysql.local.sh` ignored.
- Protected-surface check passed.
