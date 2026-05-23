# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git rev-parse --short HEAD
git merge-base --is-ancestor 269fc40 HEAD
rg -n "D034|D035" project_control/DECISION_LOG.md
test -f repository_spec/verifier_support_output_contract_v0_draft.md
test -d src/sql_rewrite_bench/verifier_support
test -f src/sql_rewrite_bench/verifier_support/verieql.py
test -d audits/verifier_support_synthetic_fixture_v1
test -d audits/verieql_bounded_canary_v2
python - <<'PY'  # SQLSolver availability probe
...
PY
```

Required reads:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 180 project_control/MIGRATION_STATUS.md
tail -n 180 project_control/MIGRATION_RUN_LOG.md
sed -n '900,1160p' project_control/DECISION_LOG.md
sed -n '1,300p' repository_spec/verifier_support_output_contract_v0_draft.md
sed -n '1,260p' repository_spec/user_output_contract_v0_draft.md
find audits/verifier_support_output_contract_plan_v0 audits/verifier_support_synthetic_fixture_v1 audits/verieql_bounded_canary_v2 -maxdepth 1 -type f -print
sed -n '1,260p' src/sql_rewrite_bench/verifier_support/pairs.py
sed -n '1,320p' src/sql_rewrite_bench/verifier_support/verdicts.py
sed -n '1,260p' src/sql_rewrite_bench/verifier_support/summary.py
sed -n '1,280p' src/sql_rewrite_bench/verifier_support/fixtures.py
sed -n '1,380p' src/sql_rewrite_bench/verifier_support/verieql.py
sed -n '1,380p' src/cli/main.py
sed -n '1,260p' docs/user_entry_checker_policy.md
```

Detection/fail-closed smoke:

```bash
PYTHONPATH=src python - <<'PY'
from sql_rewrite_bench.verifier_support.sqlsolver import detect_sqlsolver
availability = detect_sqlsolver(env={}, search_path='')
print(f'tool_available={str(availability.tool_available).lower()}')
print(f'tool_version={availability.tool_version or "unknown"}')
print(f'detection_reason={availability.detection_reason}')
PY

PYTHONPATH=src python - <<'PY'
import json
import tempfile
from pathlib import Path
from sql_rewrite_bench.verifier_support.fixtures import synthetic_pair_record
from sql_rewrite_bench.verifier_support.sqlsolver import write_sqlsolver_smoke
with tempfile.TemporaryDirectory() as tmp:
    out = write_sqlsolver_smoke(...)
    ...
PY
```

Validation:

```bash
PYTHONPATH=src pytest tests/user_entry/test_sqlsolver_support.py -q
PYTHONPATH=src pytest tests/user_entry/test_verieql_support.py tests/user_entry/test_verifier_support.py tests/user_entry/test_sqlsolver_support.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/verifier_support/sqlsolver.py src/sql_rewrite_bench/verifier_support/__init__.py
python - <<'PY'  # project-control readability
...
PY
python - <<'PY'  # audit Markdown sanity
...
PY
git diff --check
python - <<'PY'  # protected-surface check
...
PY
git status --short -- runs/user output reports results
```
