# Command Log

Preflight:

```bash
git status -sb
rg -n "D034|D035" project_control/DECISION_LOG.md
test -d audits/verieql_adapter_jsonl_compatibility_v0
test -d audits/verieql_dependency_staging_external_env_v0
test -d audits/verieql_cons0007_one_pair_canary_v0
test -d audits/verieql_perf0062_one_pair_canary_v0
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
test -x /home/tianci_gao/.venvs/sqlrb-verieql/bin/python
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout --help
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Synthetic smoke:

```bash
rm -rf /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0
mkdir -p /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/input
printf 'SELECT 1;\n' > /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/input/select_1_a.sql
printf 'SELECT 1;\n' > /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/input/select_1_b.sql
printf 'SELECT 2;\n' > /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/input/select_2.sql
PYTHONPATH=src \
SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL \
SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python \
SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python \
python - <<'PY'
# Built two support_pair_smoke records and called
# sql_rewrite_bench.verifier_support.verieql.write_verieql_canary.
PY
```

Wrapper-built VeriEQL batch command:

```bash
cd /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout \
  -f /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl \
  -t 30 \
  -o /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/verieql_output.jsonl
```

Inspection:

```bash
find /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0 -type f | sort
cat /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/raw_stdout.txt
cat /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/raw_stderr.txt
cat /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/verieql_output.jsonl
cat /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/results/verieql_synthetic_decidable_smoke_v0/verifier/verifier_verdicts.jsonl
cat /tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/results/verieql_synthetic_decidable_smoke_v0/verifier/semantic_equivalence_summary.json
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

No SQLSolver command was run. No Common-core, PERF, CONS, PORT, LONGTAIL, database, timing, or official metrics command was run.
