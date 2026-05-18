# SQLGlot Enabled Smoke Command Log

This log records concise command outcomes only. It does not include secrets, tokens, environment dumps, or long raw stdout/stderr payloads.

## Release Repo Preflight

- `git status -sb`
  - Outcome: clean release repo on `main`, tracking `origin/main`.
- Read release metadata from `case_sets/common_core_v0/` and `inventory/case_registry.csv`.
  - Outcome: `PERF_0006` and `PERF_0007` confirmed as Common-core PERF rows with postgres denominator entries.

## Temporary Checkout and Install

- `rm -rf /tmp/sqlrb_sqlglot_enabled_smoke && mkdir -p /tmp/sqlrb_sqlglot_enabled_smoke`
  - Outcome: temporary smoke root reset.
- `git clone /home/tianci_gao/code/Rewritebench_v0 /tmp/sqlrb_sqlglot_enabled_smoke/Rewritebench_v0_sqlglot_smoke`
  - Outcome: temporary clone created.
- `python -m venv .venv-sqlglot-smoke`
  - Outcome: temporary virtual environment created.
- `python -m pip install -e ".[sqlglot]"`
  - Outcome: passed; editable package installed with SQLGlot optional dependency.
- `python - <<'PY' ... import sqlglot ... PY`
  - Outcome: passed; SQLGlot imported with observed version `30.8.0`.

## SQLGlot Adapter Smoke Commands

- `python baselines/sqlglot/sqlglot_user_adapter.py --help`
  - Outcome: passed.
- `python -m sql_rewrite_bench.user_run --case-set common_core_v0 --pool PERF --engine postgres --case-list tmp_sqlglot_smoke_cases.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --out runs/user/sqlglot_enabled_noop_dry_run --dry-run`
  - Outcome: passed; 2 selected rows, 0 adapter invocations, 0 candidate rows.
- `python -m sql_rewrite_bench.user_run --case-set common_core_v0 --pool PERF --engine postgres --case-list tmp_sqlglot_smoke_cases.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --out runs/user/sqlglot_enabled_noop_smoke`
  - Outcome: passed; 2 selected rows, 2 candidate rows.
- `python -m sql_rewrite_bench.user_run --case-set common_core_v0 --pool PERF --engine postgres --case-list tmp_sqlglot_smoke_cases.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize" --out runs/user/sqlglot_enabled_optimize_smoke`
  - Outcome: passed; 2 selected rows, 2 candidate rows.

## Output and Boundary Checks

- Verified expected output files for both real smoke runs.
  - Outcome: `config.yaml`, `selected_cases.csv`, `ledger.csv`, `summary.json`, `failures.csv`, and `report.md` present.
- Verified `candidate_sql/*.sql` files for both real smoke runs.
  - Outcome: 2 candidate SQL files for no-op and 2 for optimize.
- Verified `summary.json` and `ledger.csv`.
  - Outcome: candidate rows generated and non-DB status fields preserved.
- `git status --short runs/user`
  - Outcome: no tracked or staged smoke output in the temporary clone.
- `git status --short cases case_sets inventory reports results`
  - Outcome: no protected-path changes in the temporary clone.

## Release Repo Validation

- `PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`
  - Outcome: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`
  - Outcome: passed.
- Summary JSON parse and invariant check.
  - Outcome: passed.
- Protected-path boundary checks in release repo.
  - Outcome: no changes under `cases/`, `case_sets/`, `inventory/`, `reports/`, `results/`, or `runs/user`.
- `git diff --check`
  - Outcome: passed.
