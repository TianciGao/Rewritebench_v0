# Command Log

Preflight:
- `git status -sb`
- `git branch --show-current`
- `git fetch origin`
- `git merge-base --is-ancestor 9ef58c5c7ad0a4c450909b34a23b41a113de7072 origin/feature/case-package-v2-external-schema`
- Remote project-control readability checks from `origin/main` and `origin/feature/case-package-v2-external-schema`
- D032/D033/D034/D035 presence check
- `git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb`
- `/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound --help`

Exact gate:
- Parsed `runs/user/common_core_pg_noop_db_checker/ledger.csv` for `CONS_0036` and `CONS_0037`.
- Confirmed both rows were selected, source executable, candidate generated, candidate executable, checker success, and exact.

Runtime:
- Cleared and recreated `/tmp/sqlrb_verieql_bound4_two_row_uniform_policy_pass_v0/`.
- Invoked the existing `write_verieql_canary` wrapper in finite-bound mode with `bound_size=4`, `timeout_seconds=30`, and `cores=1`.

Command shape:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound -f <pairs.jsonl> -s 4 -t 30 -c 1 -o <output.jsonl>
```

Validation:
- `python - <<'PY' ... audit Markdown/CSV/JSON sanity ... PY`
- `git diff --check`
- `python - <<'PY' ... protected-surface status parser ... PY`
- `git status --short runs/user output reports results cases case_sets baselines src tests scripts .github/workflows`
- `git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb`
- `git status -sb`
