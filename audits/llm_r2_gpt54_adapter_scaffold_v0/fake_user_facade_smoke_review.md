# Fake User-Facade Smoke Review

## Command

```bash
SQLRB_LLM_R2_MODE=fake \
SQLRB_LLM_R2_FAKE_SQL='SELECT 1 AS llm_r2_fake_candidate' \
PYTHONPATH=src \
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --case-list /tmp/sqlrb_llm_r2_fake_smoke_cases.txt \
  --adapter-command "python baselines/llm_r2/adapter.py" \
  --output-root /tmp/sqlrb_llm_r2_gpt54_adapter_scaffold_v0/output \
  --run-id llm_r2_gpt54_fake_user_facade_smoke_v0 \
  --adapter-timeout 30
```

The case list contained:

- `PERF_0006`
- `CONS_0036`

## Result

- Selected rows: 2.
- Candidate generated rows: 2.
- DB execution: not enabled.
- Checker: not enabled.
- Timing: not enabled.
- `local_metrics.py`: not run.
- Verifier: not run.

## Metadata Checks

Both per-row `llm_r2_status.json` files recorded:

- `route_id=llm_r2_gpt54_adapted`
- `method_id=llm_r2`
- `fake_runtime=true`
- `live_call=false`
- `rule_system_runtime_used=false`
- `checkpoint_used=false`
- `demonstration_selector_used=false`
- `local_diagnostic_only=true`

## Runtime Output Boundary

The smoke wrote temporary user-run outputs under:

- `runs/user/llm_r2_gpt54_fake_user_facade_smoke_v0`
- `/tmp/sqlrb_llm_r2_gpt54_adapter_scaffold_v0/output`

These runtime outputs were reviewed for audit counts only and are not staged or
committed.
