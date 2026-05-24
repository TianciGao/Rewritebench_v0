# Fake Provider Smoke Results

Smoke run id:
- `direct_llm_original_fake_smoke_v2`

Command shape:

```bash
SQLRB_LLM_PROVIDER=fake \
SQLRB_LLM_FAKE_RESPONSE='```sql
SELECT 1 AS direct_llm_fake_smoke;
```' \
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --case-list /tmp/sqlrb_direct_llm_provider_adapter_contract_v0_case_list.txt \
  --engines postgres \
  --adapter-command "python baselines/direct_llm_original/adapter.py" \
  --output-root /tmp/sqlrb_direct_llm_provider_adapter_contract_v0/output \
  --run-id direct_llm_original_fake_smoke_v2
```

Scope:
- `CONS_0036/postgres`
- `PERF_0006/postgres`

Result:
- Selected rows: 2.
- Candidate generated rows: 2.
- Candidate preflight passed rows: 2.
- DB execution was not enabled.
- Checker was not enabled.
- Timing was not collected.
- Live API call was not made.

Adapter metadata checks:
- `provider = fake`.
- `model_id = gpt-5.4`.
- `base_url_host = api.gptsapi.net`.
- `schema_context_status = available` for both rows.
- `raw_response_saved = true` for fake-provider traceability.
- `repair_attempted = false`.
- `official_metric_input = false`.
- `paper_result = false`.

Runtime output:
- Written under `/tmp/sqlrb_direct_llm_provider_adapter_contract_v0/`.
- Not committed.
