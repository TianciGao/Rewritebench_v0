# Command Log

Release repo preflight:

```bash
git status -sb
git branch --show-current
rg -n "^## D03[45]:" project_control/DECISION_LOG.md
test -d audits/verieql_synthetic_from_clause_smoke_v0
test -d audits/verieql_dependency_staging_external_env_v0
```

VeriEQL environment preflight:

```bash
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
test -x /home/tianci_gao/.venvs/sqlrb-verieql/bin/python
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout --help
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Probe execution:

```bash
rm -rf /tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0
mkdir -p /tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0/input
printf 'SELECT a FROM T;\n' > /tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0/input/select_a_source.sql
printf 'SELECT a FROM T;\n' > /tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0/input/select_a_candidate.sql
printf '{"T":{"a":"integer","b":"integer"}}\n' > /tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0/input/schema.json
PYTHONPATH=src \
SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL \
SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python \
SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python \
python - <<'PY'
# Sequentially ran the same support_pair_smoke at timeouts 30, 120, and 300.
# Stopped early only if normalized_verdict == equivalent and TMO was absent.
PY
```

Review commands:

```bash
cat /tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0/timeout_probe_matrix.csv
for t in 30 120 300; do
  cat /tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0/timeout_${t}/results/verieql_equivalent_timeout_policy_probe_v0_t${t}/verifier/tools/verieql/batch/verieql_output.jsonl
  cat /tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0/timeout_${t}/results/verieql_equivalent_timeout_policy_probe_v0_t${t}/verifier/semantic_equivalence_summary.json
done
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Validation commands:

```bash
python -m json.tool <summary.json>
python - <<'PY'
# Parsed runtime JSONL files and audit CSV files.
PY
git diff --check
git status -sb
```
