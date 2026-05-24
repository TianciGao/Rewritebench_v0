# Protected Surface Check

Allowed modifications:

- `audits/track_a_120_existing_baseline_evidence_inventory_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces not modified:

| surface | status |
| --- | --- |
| `repository_spec/metrics_contract_v1.md` | not modified |
| `src/sql_rewrite_bench/local_metrics.py` | not modified |
| `src/sql_rewrite_bench/tag_slices.py` | not modified |
| `src/sql_rewrite_bench/verifier_support/*.py` | not modified |
| `baselines/` | not modified |
| `cases/` | not modified |
| `schemas/` | not modified |
| `case_sets/` | not modified |
| `inventory/` | not modified |
| top-level `reports/` | not modified |
| top-level `results/` | not modified |
| `runs/user/` | read only; not modified |
| retained evidence | not modified |
| paper result files | not modified |
| env files/API keys/secrets | not modified |
