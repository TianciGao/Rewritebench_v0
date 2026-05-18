# B-line User Entry CI Smoke Command Log

## Commands And Outcomes

- `pwd && git branch --show-current && git remote -v && git status -sb && git log --oneline -5`
  - Outcome: passed; release repo was on `main`, aligned with `origin/main`, and clean before edits.
- `PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`
  - Outcome: passed; module help, wrapper help, user-entry tests, dry-run smoke, dummy adapter smoke, protected-path checks, and `runs/user` unstaged checks passed.
- `python scripts/dev/smoke_ledger_fixtures.py`
  - Outcome: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python - <<'PY' ... yaml.safe_load('.github/workflows/user_entry_smoke.yml') ... PY`
  - Outcome: passed; PyYAML parsed the workflow file.
- `python - <<'PY' ... json.load('audits/b_line_user_entry_ci_smoke_v0/b_line_user_entry_ci_smoke_summary.json') ... PY`
  - Outcome: passed; summary JSON invariants held.
- `git status --short cases case_sets inventory reports results runs/user`
  - Outcome: passed; protected paths and local smoke output had no status output.
- `git diff --check`
  - Outcome: passed.
- `git diff --stat`
  - Outcome: reviewed before staging.
- `git status -sb`
  - Outcome: reviewed before staging.

## Boundary Notes

No DB engines, checkers, timing workloads, LLM calls, retained-evidence parsers, official metric computation, paper table rendering, reports/results mutation, case migration, `case_sets/` update, inventory update, denominator change, paper-result change, or raw legacy evidence mutation was performed.
