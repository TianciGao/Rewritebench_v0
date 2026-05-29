# Command Log

Preflight:
- `git status -sb`
- `git branch --show-current`
- `git fetch origin`
- `git merge-base --is-ancestor 5864857fa471418f4b1589aa06adc2754fdc4382 origin/feature/case-package-v2-external-schema`
- Remote project-control readability checks from `origin/main` and `origin/feature/case-package-v2-external-schema`
- D032/D033/D034/D035 presence check
- `git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb`
- `/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound --help`

Exact gate:
- Parsed `runs/user/common_core_pg_noop_db_checker/ledger.csv` for `CONS_0037`.
- Confirmed selected, source executable, candidate generated, candidate executable, checker success, and exact.

Runtime:
- Cleared and recreated `/tmp/sqlrb_verieql_cons0037_bound_timeout_policy_probe_v0/`.
- Invoked the existing finite-bound VeriEQL wrapper helper for:
  - `bound_size=1`, `timeout_seconds=30`
  - `bound_size=2`, `timeout_seconds=30`
  - `bound_size=3`, `timeout_seconds=30`
  - `bound_size=4`, `timeout_seconds=30`
  - `bound_size=5`, `timeout_seconds=30`
  - `bound_size=10`, `timeout_seconds=30`
  - `bound_size=5`, `timeout_seconds=120` because bound 5 timed out at 30 seconds
  - `bound_size=10`, `timeout_seconds=120` because bound 10 timed out at 30 seconds

No 300-second run was performed because the 120-second retries remained timeout classifications and did not produce a clean or policy-changing result.

Validation:
- `python - <<'PY' ... audit Markdown/CSV sanity ... PY`
- `git diff --check`
- `python - <<'PY' ... protected-surface status parser ... PY`
- `git status --short runs/user output reports results cases case_sets baselines src tests scripts .github/workflows`
- `git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb`
- `git status -sb`
