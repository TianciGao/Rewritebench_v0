# SQLGlot Adapter MVP Command Log

## Commands And Outcomes

- `pwd && git branch --show-current && git remote -v && git status -sb && git log --oneline -5`
  - Outcome: passed; release repo was on `main`, aligned with `origin/main`, and clean before edits.
- `python - <<'PY' ... import sqlglot ... PY`
  - Outcome: SQLGlot unavailable; `ModuleNotFoundError: No module named 'sqlglot'`.
- `python baselines/sqlglot/sqlglot_user_adapter.py --help`
  - Outcome: passed.
- `PYTHONPATH=src python -m unittest discover -s tests/user_entry -v`
  - Outcome: passed; 19 tests run, 2 skipped because SQLGlot is not installed.
- `python -m py_compile baselines/sqlglot/sqlglot_user_adapter.py tests/user_entry/test_sqlglot_adapter.py`
  - Outcome: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --pool PERF --engine postgres --case-list <temp file> --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --out runs/user/sqlglot_noop_dry_run_smoke --dry-run`
  - Outcome: passed; selected 1 row and generated 0 candidates because dry-run does not invoke the adapter.
- `SQLRB_* ... PYTHONPATH=src python baselines/sqlglot/sqlglot_user_adapter.py --route noop`
  - Outcome: expected nonzero exit; dependency guard reported SQLGlot is not installed.
- `python baselines/sqlglot/sqlglot_user_adapter.py --route invalid`
  - Outcome: expected nonzero exit; argparse route validation rejected the route.
- `PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`
  - Outcome: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`
  - Outcome: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected.
- `python - <<'PY' ... json.load('audits/b_line_sqlglot_adapter_mvp_v0/b_line_sqlglot_adapter_mvp_summary.json') ... PY`
  - Outcome: passed; summary JSON invariants held.
- `git status --short cases case_sets inventory reports results runs/user`
  - Outcome: passed; protected paths and local smoke output had no status output.
- `git diff --check`
  - Outcome: passed.

## Boundary Notes

No DB engines, checkers, timing workloads, LLM calls, retained-evidence parsers, official metric computation, paper table rendering, reports/results mutation, case migration, `case_sets/` update, inventory update, denominator change, paper-result change, global leaderboard creation, or raw legacy evidence mutation was performed.
