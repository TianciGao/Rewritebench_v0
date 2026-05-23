# Command Log

Preflight and readback:

```text
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 2289ca0 HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
pytest tests/user_entry/test_verieql_support.py -q
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Selection/read-only inspection:

```text
python - <<'PY'
# inspected runs/user/common_core_pg_noop_db_checker/ledger.csv exact rows
PY
rg -n "schema|ddl|source|positive|case_id|pool" cases/PERF/PERF_0006 cases/CONS/CONS_0005
find cases/PERF/PERF_0006 cases/CONS/CONS_0005 -maxdepth 4 -type f | sort
sed -n '1,260p' src/sql_rewrite_bench/verifier_support/verieql.py
```

Focused code-validation after strict normalization update:

```text
pytest tests/user_entry/test_verieql_support.py -q
pytest tests/user_entry/test_verifier_support.py -q
```

Tiny local pass:

```text
rm -rf /tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0
mkdir -p /tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0
PYTHONPATH=src python - <<'PY'
# selected CONS_0036, PERF_0077, PERF_0082 from existing exact ledger rows
# wrote verifier pairs under /tmp
# invoked write_verieql_canary(... verifier_mode=finite_bound, bound_size=10, timeout_seconds=30, cores=1)
PY
```

Underlying VeriEQL command shape:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound -f /tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0/output/results/verieql_exact_candidate_tiny_local_pass_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl -s 10 -t 30 -c 1 -o /tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0/output/results/verieql_exact_candidate_tiny_local_pass_v0/verifier/tools/verieql/batch/verieql_output.jsonl
```

Validation commands are recorded in `verifier_results_summary.md` and the final task report.

