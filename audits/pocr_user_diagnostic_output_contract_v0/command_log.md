# Command Log

Read-only and validation commands used for this task:

```text
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
sed -n '1,240p' src/sql_rewrite_bench/pocr/candidate_resolver.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/real_route_diagnostic_runner.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/evidence_validation.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/operation_evidence_policy.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/annotation_schema.py
sed -n '1,240p' src/sql_rewrite_bench/pocr/models.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/inventory.py
sed -n '1,220p' src/sql_rewrite_bench/pocr/skills_parser.py
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/pocr/diagnostic_output_schema.py src/sql_rewrite_bench/pocr/user_output_adapter.py src/sql_rewrite_bench/pocr/user_facade.py src/sql_rewrite_bench/pocr/__init__.py
PYTHONPATH=src pytest tests/pocr/test_diagnostic_output_schema.py tests/pocr/test_user_output_adapter.py tests/pocr/test_user_facade.py -q
PYTHONPATH=src pytest tests/pocr -q
PYTHONPATH=src python - <<'PY'
from pathlib import Path
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory, EXPECTED_COMMON_CORE_SPLIT
inv = build_common_core_inventory(Path.cwd())
assert inv.parsed_count == 40
assert inv.valid_count == 40
assert inv.pool_split == EXPECTED_COMMON_CORE_SPLIT
assert inv.issues_count == 0
PY
python - <<'PY'
import csv
from pathlib import Path
for path in [Path('audits/pocr_user_diagnostic_output_contract_v0/sample_diagnostic_rows.csv'), Path('audits/pocr_user_diagnostic_output_contract_v0/sample_diagnostic_summary_by_pool.csv')]:
    with path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    assert rows
PY
python - <<'PY'
from pathlib import Path
for path in sorted(Path('audits/pocr_user_diagnostic_output_contract_v0').glob('*.md')):
    assert path.read_text(encoding='utf-8').strip()
PY
git diff --name-only | rg '^(cases/|output/|reports/|results/|runs/|retained_evidence/)|/skills\.md$|/skill/' || true
rg -n "sk-[A-Za-z0-9_\-]{20,}|Authorization:\s*Bearer\s+[A-Za-z0-9_\-.]+|(OPENAI_API_KEY|SQLRB_LLM_API_KEY)\s*=\s*[A-Za-z0-9_\-]{12,}" src/sql_rewrite_bench/pocr/diagnostic_output_schema.py src/sql_rewrite_bench/pocr/user_output_adapter.py src/sql_rewrite_bench/pocr/user_facade.py tests/pocr/test_diagnostic_output_schema.py tests/pocr/test_user_output_adapter.py tests/pocr/test_user_facade.py audits/pocr_user_diagnostic_output_contract_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md || true
git diff --check
git diff --cached --name-status
git diff --cached --name-only | rg '^(cases/|output/|reports/|results/|runs/|retained_evidence/)|/skills\.md$|/skill/' || true
git diff --cached --name-only -z | xargs -0 rg -n "sk-[A-Za-z0-9_\-]{20,}|Authorization:\s*Bearer\s+[A-Za-z0-9_\-.]+|(OPENAI_API_KEY|SQLRB_LLM_API_KEY)\s*=\s*[A-Za-z0-9_\-]{12,}" || true
```

Audit sample generation command:

```text
PYTHONPATH=src python - <<'PY'
from pathlib import Path
from sql_rewrite_bench.pocr.user_facade import run_pocr_diagnostic_user_facade
from sql_rewrite_bench.pocr.diagnostic_output_schema import write_diagnostic_rows_csv, write_diagnostic_summary_csv, render_diagnostic_markdown_report

repo = Path.cwd()
audit = repo / 'audits/pocr_user_diagnostic_output_contract_v0'
result = run_pocr_diagnostic_user_facade(
    repo_root=repo,
    run_id='pocr_user_diagnostic_contract_sample_v0',
    candidate_root=Path('runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql'),
    method_id='direct_llm_original',
    route_id='direct_llm_original_pg40_pocr_diagnostic',
    engine='postgres',
    live_enabled=False,
    output_root=None,
    case_ids=('PERF_0006','CONS_0005','PORT_0003','LONGTAIL_0011'),
)
write_diagnostic_rows_csv(audit / 'sample_diagnostic_rows.csv', result.rows)
write_diagnostic_summary_csv(audit / 'sample_diagnostic_summary_by_pool.csv', result.summaries)
(audit / 'sample_pocr_diagnostic_report.md').write_text(
    render_diagnostic_markdown_report(
        run_id='pocr_user_diagnostic_contract_sample_v0',
        rows=result.rows,
        summaries=result.summaries,
    ),
    encoding='utf-8',
)
PY
```

No live API, DB/checker/timing, baseline, local_metrics, verifier, or paper-rendering command was run.
