# Command Log

Preflight:

```bash
git status -sb
git fetch origin main feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "D033|D034|D035" project_control
python -m cli.main user evaluate --help
python -m cli.main user compute-local-metrics --help
```

Legacy reference:

```bash
git clone --depth 1 https://github.com/TianciGao/sql-rewrite-bench /tmp/sql-rewrite-bench_legacy_ref
rg -n "Direct LLM|Repair-1|repair|extract|prompt|model|API|failure" /tmp/sql-rewrite-bench_legacy_ref
```

Focused validation:

```bash
pytest tests/user_entry/test_direct_llm_adapter.py -q
python -m py_compile baselines/direct_llm_original/adapter.py tests/user_entry/test_direct_llm_adapter.py
```

Fake-provider smoke:

```bash
printf 'CONS_0036\nPERF_0006\n' > /tmp/sqlrb_direct_llm_provider_adapter_contract_v0_case_list.txt
SQLRB_LLM_PROVIDER=fake SQLRB_LLM_FAKE_RESPONSE='```sql
SELECT 1 AS direct_llm_fake_smoke;
```' python -m cli.main user evaluate --case-set common_core_v0 --case-list /tmp/sqlrb_direct_llm_provider_adapter_contract_v0_case_list.txt --engines postgres --adapter-command "python baselines/direct_llm_original/adapter.py" --output-root /tmp/sqlrb_direct_llm_provider_adapter_contract_v0/output --run-id direct_llm_original_fake_smoke_v2
```

Post-audit validation:

```bash
git diff --check
git status -sb
```

Notes:
- One early shell search against the legacy reference had a quoting error and was repeated with safe patterns.
- No live API call was made.
- No metrics command was run.
