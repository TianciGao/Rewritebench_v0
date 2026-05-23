# Command Log

Release repo preflight:

```bash
git status -sb
git branch --show-current
rg -n "^## D03[45]:" project_control/DECISION_LOG.md
test -d audits/verieql_synthetic_decidable_smoke_v0
test -d audits/verieql_dependency_staging_external_env_v0
test -d audits/verieql_adapter_jsonl_compatibility_v0
```

VeriEQL environment preflight:

```bash
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
test -x /home/tianci_gao/.venvs/sqlrb-verieql/bin/python
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout --help
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Smoke execution:

```bash
rm -rf /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0
mkdir -p /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/input
printf 'SELECT a FROM T;\n' > /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/input/select_a_source.sql
printf 'SELECT a FROM T;\n' > /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/input/select_a_candidate.sql
printf 'SELECT b FROM T;\n' > /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/input/select_b_candidate.sql
printf '{"T":{"a":"integer","b":"integer"}}\n' > /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/input/schema.json
PYTHONPATH=src \
SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL \
SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python \
SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python \
python - <<'PY'
from pathlib import Path
from sql_rewrite_bench.verifier_support.pairs import boundary_flags_as_csv
from sql_rewrite_bench.verifier_support.verieql import write_verieql_canary

run_id = "verieql_synthetic_from_clause_smoke_v0"
root = Path("/tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0")
input_dir = root / "input"
flags = boundary_flags_as_csv()
base = {
    "run_id": run_id,
    "tool": "verieql",
    "pool": "synthetic",
    "engine": "synthetic",
    "route_id": "verieql_synthetic_smoke",
    "method_id": "verieql_support_probe",
    "pair_type": "support_pair_smoke",
    "positive_sql_path": "",
    "negative_sql_path": "",
    "schema_context_path": (input_dir / "schema.json").as_posix(),
    "checker_context_path": "",
    "denominator_id": "synthetic_verieql_from_clause_smoke_v0",
    **flags,
}
pairs = [
    {
        **base,
        "pair_id": "synthetic_from_equivalent",
        "case_id": "SYNTHETIC_FROM_EQUIVALENT",
        "source_sql_path": (input_dir / "select_a_source.sql").as_posix(),
        "candidate_sql_path": (input_dir / "select_a_candidate.sql").as_posix(),
    },
    {
        **base,
        "pair_id": "synthetic_from_nonequivalent",
        "case_id": "SYNTHETIC_FROM_NONEQUIVALENT",
        "source_sql_path": (input_dir / "select_a_source.sql").as_posix(),
        "candidate_sql_path": (input_dir / "select_b_candidate.sql").as_posix(),
    },
]
write_verieql_canary(
    output_root=root,
    run_id=run_id,
    pair_records=pairs,
    command="/home/tianci_gao/.venvs/sqlrb-verieql/bin/python",
    timeout_seconds=30,
    result_consistent_pairs=None,
    dry_run=False,
)
PY
```

Review and validation commands:

```bash
find /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0 -type f | sort
cat /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/batch/verieql_output.jsonl
cat /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/results/verieql_synthetic_from_clause_smoke_v0/verifier/verifier_verdicts.jsonl
cat /tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/results/verieql_synthetic_from_clause_smoke_v0/verifier/semantic_equivalence_summary.json
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
git diff --check
```
