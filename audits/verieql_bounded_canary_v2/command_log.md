# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
rg -n "D034|D035" project_control/DECISION_LOG.md
test -f repository_spec/verifier_support_output_contract_v0_draft.md
test -d src/sql_rewrite_bench/verifier_support
test -d audits/verifier_support_synthetic_fixture_v1
test -d src/cli
test -f src/sql_rewrite_bench/user_output.py
python - <<'PY'  # VeriEQL availability probe
...
PY
```

Required reads:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 180 project_control/MIGRATION_STATUS.md
tail -n 180 project_control/MIGRATION_RUN_LOG.md
sed -n '900,1120p' project_control/DECISION_LOG.md
sed -n '1,260p' repository_spec/verifier_support_output_contract_v0_draft.md
find audits/verifier_support_output_contract_plan_v0 audits/verifier_support_synthetic_fixture_v1 -maxdepth 1 -type f -print
sed -n '1,260p' docs/user_entry_checker_policy.md
sed -n '1,260p' src/sql_rewrite_bench/verifier_support/pairs.py
sed -n '1,320p' src/sql_rewrite_bench/verifier_support/verdicts.py
sed -n '1,260p' src/sql_rewrite_bench/verifier_support/summary.py
sed -n '1,280p' src/sql_rewrite_bench/verifier_support/fixtures.py
sed -n '1,380p' src/cli/main.py
```

Detection/fail-closed smoke:

```bash
PYTHONPATH=src python - <<'PY'
from sql_rewrite_bench.verifier_support.verieql import detect_verieql
availability = detect_verieql(env={}, search_path='')
print(f'tool_available={availability.tool_available}')
print(f'tool_version={availability.tool_version}')
print(f'detection_reason={availability.detection_reason}')
PY

PYTHONPATH=src python - <<'PY'
import tempfile
from pathlib import Path
from sql_rewrite_bench.verifier_support.fixtures import synthetic_pair_record
from sql_rewrite_bench.verifier_support.verieql import write_verieql_canary
with tempfile.TemporaryDirectory() as tmp:
    out = write_verieql_canary(
        output_root=Path(tmp) / 'output',
        run_id='verieql_fail_closed_smoke',
        pair_records=[synthetic_pair_record(pair_id='p1', run_id='verieql_fail_closed_smoke', tool='verieql')],
        command='/definitely/missing/verieql',
        env={},
        search_path='',
    )
    print(f'tool_available={out.tool_available}')
    print(f'normalized_summary_status={out.summary["semantic_equivalence_rate_status"]}')
    print(f'na_reason={out.summary["na_reason"]}')
    print(f'not_attempted_count={out.summary["not_attempted_count"]}')
PY
```

Validation:

```bash
PYTHONPATH=src pytest tests/user_entry/test_verieql_support.py tests/user_entry/test_verifier_support.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/verifier_support/verieql.py
python - <<'PY'  # project-control readability
...
PY
python - <<'PY'  # audit Markdown sanity
...
PY
git diff --check
```
