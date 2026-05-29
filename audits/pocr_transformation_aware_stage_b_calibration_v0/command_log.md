# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,240p' project_control/DECISION_LOG.md
sed -n '1,320p' src/sql_rewrite_bench/pocr/static_evidence.py
sed -n '1,360p' src/sql_rewrite_bench/pocr/calibration_runner.py
sed -n '360,760p' src/sql_rewrite_bench/pocr/calibration_runner.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/prompt_builder.py
sed -n '1,320p' tests/pocr/test_static_evidence.py
sed -n '1,260p' tests/pocr/test_calibration_runner.py
sed -n '1,180p' tests/pocr/test_prompt_builder.py
python -m py_compile src/sql_rewrite_bench/pocr/transformation_evidence.py src/sql_rewrite_bench/pocr/operation_evidence_policy.py src/sql_rewrite_bench/pocr/calibration_runner.py src/sql_rewrite_bench/pocr/prompt_builder.py
pytest tests/pocr/test_transformation_evidence.py tests/pocr/test_operation_evidence_policy.py tests/pocr/test_calibration_runner.py tests/pocr/test_prompt_builder.py -q
python - <<'PY'
import os
print('SQLRB_LLM_ALLOW_LIVE', os.environ.get('SQLRB_LLM_ALLOW_LIVE') == '1')
print('api_key_env_present', bool(os.environ.get('SQLRB_LLM_API_KEY') or os.environ.get('GPTSAPI_API_KEY')))
print('base_env_present_or_default', bool(os.environ.get('SQLRB_LLM_BASE_URL') or os.environ.get('GPTSAPI_BASE_URL') or 'https://api.gptsapi.net/v1'))
print('model_env_present_or_default', bool(os.environ.get('SQLRB_LLM_MODEL') or os.environ.get('GPTSAPI_MODEL') or 'gpt-5.4'))
PY
python - <<'PY'
from pathlib import Path
repo=Path.cwd()
for case_id,pool in [('PERF_0006','PERF'),('CONS_0005','CONS'),('PORT_0003','PORT'),('LONGTAIL_0011','LONGTAIL')]:
    for rel in [f'cases/{pool}/{case_id}/sql/source.sql',f'cases/{pool}/{case_id}/sql/pos_01.sql',f'runs/user/common_core_pg_noop_db_checker/candidate_sql/{case_id}__postgres.sql']:
        print(rel, (repo/rel).is_file())
PY
python -m sql_rewrite_bench.pocr.calibration_runner --live-enabled --output-dir audits/pocr_transformation_aware_stage_b_calibration_v0
find audits/pocr_transformation_aware_stage_b_calibration_v0 -maxdepth 1 -type f -printf '%f\n' | sort
python - <<'PY'
import csv,json
from collections import Counter
from pathlib import Path
base=Path('audits/pocr_transformation_aware_stage_b_calibration_v0')
for name in ['selected_cases.csv','candidate_class_inventory.csv','live_call_manifest.csv','annotation_schema_validation.csv','transformation_stage_b_validation_by_class.csv','positive_vs_noop_transformation_comparison.csv']:
    with (base/name).open(newline='', encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    print(name, len(rows))
with (base/'safe_annotation_outputs.jsonl').open(encoding='utf-8') as f:
    rows=[json.loads(line) for line in f if line.strip()]
print('safe_jsonl', len(rows))
PY
python -m py_compile $(rg --files src/sql_rewrite_bench/pocr -g '*.py')
pytest tests/pocr -q
python - <<'PY'
import csv, json
from collections import Counter
from pathlib import Path
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.candidate_resolver import resolve_candidate_sources
repo=Path.cwd()
inv=build_common_core_inventory(repo)
assert len(inv.members)==40
assert Counter(m.pool for m in inv.members)==Counter({'PERF':16,'CONS':9,'PORT':9,'LONGTAIL':6})
resolved=resolve_candidate_sources(repo, candidate_root=Path('runs/user/common_core_pg_noop_db_checker/candidate_sql'), method_id='sqlglot_noop', route_id='common_core_pg_noop_db_checker', engine='postgres')
assert len(resolved)==40
assert sum(1 for r in resolved if r.candidate_present)==40
base=repo/'audits/pocr_transformation_aware_stage_b_calibration_v0'
for name in ['selected_cases.csv','candidate_class_inventory.csv','live_call_manifest.csv','annotation_schema_validation.csv','transformation_stage_b_validation_by_class.csv','positive_vs_noop_transformation_comparison.csv']:
    with (base/name).open(newline='', encoding='utf-8') as f:
        assert list(csv.DictReader(f))
with (base/'safe_annotation_outputs.jsonl').open(encoding='utf-8') as f:
    assert len([json.loads(line) for line in f if line.strip()])==8
PY
```

No DB/checker/timing command, baseline rerun, official POCR computation, route-level POCR aggregation, user-output integration, paper-facing metrics command, `compute-local-metrics`, verifier command, or Track A 120 command was run.

After reviewing the generated comparison rows, the diagnostic risk rule was tightened so a no-op row with zero transformation-supported atoms is not treated as close to a positive row with one supported atom. The two `PORT_0003` risk labels were updated to `low` without additional live calls.
