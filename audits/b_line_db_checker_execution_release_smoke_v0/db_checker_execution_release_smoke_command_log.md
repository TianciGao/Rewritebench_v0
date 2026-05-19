# DB/Checker Execution Release-Smoke Command Log

Task: `b_line_db_checker_execution_release_smoke_v0`

Date: 2026-05-19

## Release Repo Preflight

- `pwd`
  - Outcome: `/home/tianci_gao/code/Rewritebench_v0`
- `git branch --show-current`
  - Outcome: `main`
- `git remote -v`
  - Outcome: `origin` points to `git@github.com:TianciGao/Rewritebench_v0.git`
- `git status -sb`
  - Outcome: clean and aligned with `origin/main`
- `git rev-list --left-right --count HEAD...origin/main`
  - Outcome: `0 0`

## Environment Preflight

- `psql --version`
  - Outcome: `psql (PostgreSQL) 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)`
- `psql -c "select 1;"`
  - Outcome: passed

No DB passwords, full DSNs, or environment variable values were printed or recorded.

## Temporary Checkout Smoke

- `rm -rf /tmp/sqlrb_db_checker_release_smoke`
  - Outcome: removed previous temporary smoke directory if present.
- `git clone /home/tianci_gao/code/Rewritebench_v0 /tmp/sqlrb_db_checker_release_smoke/Rewritebench_v0_db_smoke`
  - Outcome: passed.
- `python -m venv .venv-db-smoke`
  - Outcome: passed.
- `.venv-db-smoke/bin/python -m pip install -e ".[sqlglot]"`
  - Outcome: passed.
- SQLGlot import check
  - Outcome: passed with version `30.8.0`.
- `psql -c "select 1;"` from the temporary clone
  - Outcome: passed.
- Created `tmp_db_checker_smoke_cases.txt` containing `PERF_0006`
  - Outcome: passed.
- Bounded user-run command:

```bash
python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list tmp_db_checker_smoke_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/db_checker_release_smoke_perf0006 \
  --enable-db-execution \
  --enable-checker
```

  - Outcome: passed with one selected row and one generated candidate.

## Output Verification

- Required run files existed: `config.yaml`, `selected_cases.csv`, `ledger.csv`, `summary.json`, `failures.csv`, and `report.md`.
- Required row artifacts existed: `source_result.jsonl`, `candidate_result.jsonl`, and `checker_result.json`.
- Ledger verification passed:
  - `source_execution_status=source_execution_success`
  - `candidate_execution_status=candidate_execution_success`
  - `checker_status=checker_success`
  - `exact_status=exact`
  - `failure_bucket=none`
  - `local_execution_only=true`
  - `official_metric_input=false`
  - `retained_evidence_input=false`
- Temporary clone `git status --short runs/user`: no output.
- Temporary clone `git status --short cases case_sets inventory reports results`: no output.

## Release Repo Validation

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`
  - Outcome: passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/dev/smoke_ledger_fixtures.py`
  - Outcome: passed.
- Summary JSON invariant check
  - Outcome: passed.
- Boundary checks
  - Outcome: no changes under `cases/`, `case_sets/`, `inventory/`, `reports/`, `results/`, or tracked `runs/user`.
- `git diff --check`
  - Outcome: passed before staging.

## Notes

This task did not modify source code, tests, docs, pyproject, cases, case sets, inventory, reports, results, denominators, paper results, retained evidence, raw legacy evidence, or the legacy repository.
