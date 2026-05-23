# Command Log

Preflight:
- `git status -sb`
- `git branch --show-current`
- `git fetch origin`
- `git merge-base --is-ancestor 0c53cc7d492bc14cf4bf9d97506ce86e002b4976 origin/feature/case-package-v2-external-schema`
- GitHub API check for current `user-entry-smoke` and `ledger-fixture-smoke` runs on the branch.
- Remote project-control readability checks from `origin/main` and `origin/feature/case-package-v2-external-schema`.
- `git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb`
- `/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound --help`

Source inspection:
- `find runs/user/common_core_pg_noop_db_checker -maxdepth 3 -type f`
- Parsed `runs/user/common_core_pg_noop_db_checker/ledger.csv` for `CONS_0036` and `CONS_0037`.
- Inspected source SQL, candidate SQL, and PostgreSQL DDL for both rows.

Verifier execution:
- Runtime root was cleared and recreated under `/tmp/sqlrb_verieql_cons0036_cons0037_two_row_exact_candidate_pass_v0/`.
- Invoked the existing `write_verieql_canary` wrapper in finite-bound mode.
- Effective command shape:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound -f <pairs.jsonl> -s 10 -t 30 -c 1 -o <output.jsonl>
```

Execution note:
- An initial local invocation used an audit-script schema path typo with an extra underscore, producing empty schema metadata and `UnknownDatabaseError`.
- That runtime directory was deleted and the pass was rerun with the correct schema paths:
  - `schemas/verieql_cons0036_v0/postgres/ddl.sql`
  - `schemas/verieql_cons0037_v0/postgres/ddl.sql`
- The final recorded results in this audit are from the corrected invocation only.

Validation:
- `pytest tests/user_entry/test_verieql_support.py -q`
- `python - <<'PY' ... audit Markdown/CSV/JSON sanity ... PY`
- `git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb`
- `git diff --check`
- `git status --short runs/user output reports results cases case_sets baselines src tests scripts .github/workflows`
- `python - <<'PY' ... protected-surface status parser ... PY`
- `git status -sb`
