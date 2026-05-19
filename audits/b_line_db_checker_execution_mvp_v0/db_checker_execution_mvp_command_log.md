# DB/Checker Execution MVP Command Log

Task: `b_line_db_checker_execution_mvp_v0`

Date: 2026-05-18

## Commands and Outcomes

- `pwd`, `git branch --show-current`, `git remote -v`, `git status -sb`, `git log --oneline -5`
  - Outcome: release repo was `/home/tianci_gao/code/Rewritebench_v0`, branch `main`, remote `origin` over SSH, status clean and aligned with `origin/main`.

- `psql --version`
  - Outcome: `psql` was available; observed version `psql (PostgreSQL) 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)`.

- `psql -c "select 1;"`
  - Outcome: passed.

- Environment source check for `SQLRB_POSTGRES_DSN`, `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, and `PGPASSWORD`
  - Outcome: `SQLRB_POSTGRES_DSN` unset; libpq environment variables present.
  - Credential handling: no password, full DSN, or connection secret was printed or stored.

- Read-only review of `PERF_0006` package assets
  - Outcome: `manifest.yaml`, `sql/source.sql`, `sql/positives/pos_01.sql`, `checker/checker.yaml`, `checker/normalization.yaml`, `checker/compare_config.yaml`, `schema/postgres/ddl.sql`, and `schema/postgres/load.sql` were present.

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/user_entry -v`
  - Outcome: passed; 27 tests run, 1 SQLGlot missing-dependency guard skipped because SQLGlot is installed.

- First sandboxed live smoke attempt
  - Outcome: runner completed but its Python subprocess could not access `psql`; execution failed closed locally before source result capture.
  - Follow-up: local smoke output was removed and the smoke was rerun with approved escalation.

- Escalated bounded live smoke:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list /tmp/sqlrb_db_checker_perf0006_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/db_checker_postgres_perf0006_smoke \
  --enable-db-execution \
  --enable-checker
```

  - Outcome: passed with one selected row, one generated candidate, source execution success, candidate execution success, checker success, and local exact status.

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`
  - Outcome: passed.

- `PYTHONDONTWRITEBYTECODE=1 python scripts/dev/smoke_ledger_fixtures.py`
  - Outcome: passed with 38 fixture rows checked and no unexpected pass/fail.

- Boundary checks
  - Outcome: no changes under `cases/`, `case_sets/`, `inventory/`, `reports/`, `results/`, or tracked `runs/user` outputs.

- `git diff --check`
  - Outcome: passed before staging.

## Notes

All DB/checker outputs are local user-run artifacts under `runs/user/`. No DB credentials, full DSNs, long raw stdout/stderr dumps, or environment secrets are recorded here.
