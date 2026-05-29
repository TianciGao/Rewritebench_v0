# Protected Surface Check

Allowed paths changed:
- `baselines/direct_llm_original/`
- `baselines/direct_llm_repair_1/README.md`
- `tests/user_entry/test_direct_llm_adapter.py`
- `audits/direct_llm_provider_adapter_contract_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected paths not modified:
- `src/`
- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- `reports/`
- `results/`
- repository-level `output/`
- committed `runs/user/`
- retained evidence
- external Calcite/SQLSolver/VeriEQL artifacts
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Runtime artifacts:
- Fake-provider smoke wrote local runtime output under `/tmp/sqlrb_direct_llm_provider_adapter_contract_v0/` and internal staging under ignored `runs/user/`.
- Runtime artifacts were not staged.

Secret check:
- No real API keys were committed.
- Test-only placeholder strings remain confined to tests.
- Adapter status metadata records key presence and env var name, not secret values.
