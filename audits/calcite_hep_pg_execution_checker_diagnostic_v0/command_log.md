# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 2598ea6da2fdf7b34bd13cf8cc4cdf5ac7e8c0e5 HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
source scripts/env_postgres.local.sh && python scripts/dev/check_local_engine_env.py
```

Discarded integration probe:

```bash
python -m cli.main user evaluate ... --enable-db-execution --enable-checker
```

That probe was discarded because existing user-entry PORT role mapping can use cross-dialect source-reference execution for generated PORT rows. Its runtime artifacts were removed from `/tmp` and are not used in this audit.

Recorded PostgreSQL-only diagnostic run:

```bash
ROOT=/tmp/sqlrb_calcite_hep_pg_execution_checker_diagnostic_v0
RUN_ID=calcite_hep_pg_execution_checker
rm -rf "$ROOT" "runs/user/$RUN_ID"
mkdir -p "$ROOT"
source scripts/env_postgres.local.sh
python audits/calcite_hep_pg_execution_checker_diagnostic_v0/run_pg_execution_checker_from_prior_candidates.py   --input-csv audits/calcite_hep_pg_bounded_candidate_generation_v0/per_row_candidate_status.csv   --output-root "$ROOT"   --run-id "$RUN_ID"   --execution-timeout-sec 40   --db-schema-prefix sqlrb_calcite_pg_exec > "$ROOT/run_stdout.txt" 2> "$ROOT/run_stderr.txt"
```

Validation commands are recorded after validation in `protected_surface_check.md`.
