# Command Log

Initial checks:

```text
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,200p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
```

Read-only inspection:

```text
rg --files src/sql_rewrite_bench src/cli tests/user_entry tests/pocr
sed -n '1,260p' src/sql_rewrite_bench/user_run.py
sed -n '1,300p' src/cli/main.py
sed -n '1,240p' src/sql_rewrite_bench/user_output.py
sed -n '980,1025p' src/sql_rewrite_bench/user_output.py
sed -n '1,260p' tests/user_entry/test_cli_facade.py
```

Focused validation:

```text
PYTHONPATH=src python -m py_compile src/cli/main.py src/cli/pocr_diagnostic.py src/sql_rewrite_bench/pocr/diagnostic_output_schema.py src/sql_rewrite_bench/pocr/user_facade.py src/sql_rewrite_bench/pocr/user_output_adapter.py
PYTHONPATH=src pytest tests/pocr/test_diagnostic_output_schema.py tests/pocr/test_user_output_adapter.py tests/pocr/test_user_facade.py tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
PYTHONPATH=src pytest tests/pocr -q
PYTHONPATH=src pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
PYTHONPATH=src python - <<'PY'
from pathlib import Path
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory, EXPECTED_COMMON_CORE_SPLIT
inv = build_common_core_inventory(Path.cwd())
assert inv.parsed_count == 40
assert inv.valid_count == 40
assert inv.pool_split == EXPECTED_COMMON_CORE_SPLIT
assert inv.issues_count == 0
PY
```

Sample optional POCR output smoke, using `/tmp` only:

```text
rm -rf /tmp/sqlrb_pocr_optional_user_run_integration_v0
mkdir -p /tmp/sqlrb_pocr_optional_user_run_integration_v0
printf 'PERF_0006\n' > /tmp/sqlrb_pocr_optional_user_run_integration_v0/case_list.txt
PYTHONPATH=src python -m cli.main user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql \
  --method-id direct_llm_original \
  --route-id direct_llm_original_pg40_pocr_diagnostic \
  --engine postgres \
  --run-id pocr_optional_user_run_sample_v0 \
  --output-root /tmp/sqlrb_pocr_optional_user_run_integration_v0/output \
  --case-list /tmp/sqlrb_pocr_optional_user_run_integration_v0/case_list.txt
```

No live API, API-key read, DB/checker/timing, baseline, local metrics, verifier, official POCR, route-level POCR aggregation, paper rendering, retained-evidence promotion, or leaderboard command was run.

Post-smoke validation:

```text
python - <<'PY'
import csv
from pathlib import Path
for path in [
    Path('/tmp/sqlrb_pocr_optional_user_run_integration_v0/output/results/pocr_optional_user_run_sample_v0/pocr/diagnostic_rows.csv'),
    Path('/tmp/sqlrb_pocr_optional_user_run_integration_v0/output/results/pocr_optional_user_run_sample_v0/pocr/diagnostic_summary_by_pool.csv'),
]:
    with path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    assert rows
PY
python - <<'PY'
from pathlib import Path
for path in sorted(Path('audits/pocr_optional_user_run_integration_v0').glob('*.md')):
    assert path.read_text(encoding='utf-8').strip()
PY
git diff --name-only | rg '^(cases/|output/|reports/|results/|runs/|retained_evidence/)|/skills\.md$|/skill/' || true
rg -n "sk-[A-Za-z0-9_\-]{20,}|Authorization:\s*Bearer\s+[A-Za-z0-9_\-.]+|(OPENAI_API_KEY|SQLRB_LLM_API_KEY)\s*=\s*[A-Za-z0-9_\-]{12,}" src/cli/main.py src/cli/pocr_diagnostic.py src/sql_rewrite_bench/pocr/diagnostic_output_schema.py tests/pocr/test_diagnostic_output_schema.py tests/pocr/test_user_output_adapter.py tests/user_entry/test_cli_facade.py tests/user_entry/test_pocr_optional_user_run_integration.py audits/pocr_optional_user_run_integration_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md || true
git diff --check
PYTHONPATH=src python -m cli.main user pocr-diagnostic
PYTHONPATH=src python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic
git diff --cached --name-status
git diff --cached --name-only | rg '^(cases/|output/|reports/|results/|runs/|retained_evidence/)|/skills\.md$|/skill/' || true
git diff --cached --name-only -z | xargs -0 rg -n "sk-[A-Za-z0-9_\-]{20,}|Authorization:\s*Bearer\s+[A-Za-z0-9_\-.]+|(OPENAI_API_KEY|SQLRB_LLM_API_KEY)\s*=\s*[A-Za-z0-9_\-]{12,}" || true
```
