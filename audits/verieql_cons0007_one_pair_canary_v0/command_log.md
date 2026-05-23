# Command Log

## Preflight

```bash
git status -sb
rg -n "## D034|## D035" project_control/DECISION_LOG.md
test -f src/sql_rewrite_bench/verifier_support/verieql.py
test -d audits/verieql_adapter_jsonl_compatibility_v0
test -d audits/verieql_dependency_staging_external_env_v0
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
test -x /home/tianci_gao/.venvs/sqlrb-verieql/bin/python
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout --help
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Result:

- Release repo was clean and up to date.
- D034 and D035 were present.
- VeriEQL wrapper and prior audits were present.
- VeriEQL root and external venv Python were present.
- Help probe passed.
- VeriEQL source tree had only the pre-existing `M constants.py` modification.

## Required Reads

Read or inspected:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `project_control/DECISION_LOG.md`
- `repository_spec/verifier_support_output_contract_v0_draft.md`
- `audits/local_verieql_raw_directory_probe_v0/`
- `audits/legacy_baseline_smoke_verifier_clue_audit_v0/`
- `audits/verieql_adapter_jsonl_compatibility_v0/`
- `audits/verieql_dependency_staging_external_env_v0/`
- `src/sql_rewrite_bench/verifier_support/verieql.py`
- `src/sql_rewrite_bench/verifier_support/verdicts.py`
- `src/sql_rewrite_bench/verifier_support/summary.py`

## Canary Execution

The canary was executed through the existing wrapper with:

```bash
PYTHONPATH=src \
SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL \
SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python \
SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python \
python - <<'PY'
from pathlib import Path
from sql_rewrite_bench.verifier_support.verieql import write_verieql_canary
from sql_rewrite_bench.verifier_support.pairs import boundary_flags_as_csv

flags = boundary_flags_as_csv()
pair = {
    "pair_id": "CONS_0007_source_vs_positive_pos_01",
    "run_id": "verieql_cons0007_one_pair_canary_v0",
    "tool": "verieql",
    "case_id": "CONS_0007",
    "pool": "CONS",
    "engine": "verifier_support",
    "route_id": "verieql_canary",
    "method_id": "verieql",
    "pair_type": "source_vs_positive",
    "source_sql_path": "cases/CONS/CONS_0007/sql/source.sql",
    "candidate_sql_path": "",
    "positive_sql_path": "cases/CONS/CONS_0007/sql/pos_01.sql",
    "negative_sql_path": "",
    "schema_context_path": "schemas/calcite_core_sql_tests_cons0007_v0/postgres/ddl.sql",
    "checker_context_path": "cases/CONS/CONS_0007/checker/checker.yaml",
    "denominator_id": "common_core_v0_local_verifier_canary",
    **flags,
}
write_verieql_canary(
    output_root=Path("/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0"),
    run_id="verieql_cons0007_one_pair_canary_v0",
    pair_records=[pair],
    command="/home/tianci_gao/.venvs/sqlrb-verieql/bin/python",
    timeout_seconds=30,
    result_consistent_pairs=1,
    dry_run=False,
)
PY
```

The wrapper invoked VeriEQL batch mode from the staged root:

```bash
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout \
  -f /tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl \
  -t 30 \
  -o /tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_output.jsonl
```

Result:

- Batch invocation completed and wrote `verieql_output.jsonl`.
- Normalized verdict: `unsupported`.
- Runtime recorded by wrapper: about `338 ms`.

## Runtime Artifact Review Commands

```bash
find /tmp/sqlrb_verieql_cons0007_one_pair_canary_v0 -type f | sort
sed -n '1,20p' /tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_output.jsonl
sed -n '1,5p' /tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/verifier_verdicts.jsonl
cat /tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/semantic_equivalence_summary.json
```

Result:

- Runtime artifacts were written only under `/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0`.
- No repository-level `output/` artifacts were created.
- The raw VeriEQL JSONL output recorded `states=["NSE"]` and `err="Not supported feature: EXISTS"`.
- The shared verifier record normalized the pair to `unsupported`.
- The summary kept `semantic_equivalence_rate=null`.

## Validation

```bash
python -m json.tool /tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/semantic_equivalence_summary.json
```

Result:

- Summary JSON sanity check passed.

```bash
python - <<'PY'
import json
from pathlib import Path
for path in [
    Path('/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl'),
    Path('/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_output.jsonl'),
    Path('/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/verifier_verdicts.jsonl'),
]:
    for line in path.read_text().splitlines():
        if line.strip():
            json.loads(line)
PY
```

Result:

- JSONL sanity check passed for pair input, raw VeriEQL output, and normalized verdict output.

```bash
find audits/verieql_cons0007_one_pair_canary_v0 -name '*.md' -type f -empty -print
```

Result:

- No empty Markdown audit files were found.

```bash
tail -25 project_control/MIGRATION_STATUS.md
tail -100 project_control/MIGRATION_RUN_LOG.md
```

Result:

- Project-control readability check passed.

```bash
git diff --check
```

Result:

- Passed with no whitespace errors.

```bash
git status --short -- src tests scripts cases case_sets schemas inventory baselines reports results output benchmarks runs/user
```

Result:

- Protected-surface check passed.
- No `runs/user/` or repository `output/` runtime artifacts were staged.

```bash
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status --porcelain
```

Result:

```text
## main...origin/main
 M constants.py
```

```text
 M constants.py
```

The staged VeriEQL tree remained unchanged relative to preflight.
