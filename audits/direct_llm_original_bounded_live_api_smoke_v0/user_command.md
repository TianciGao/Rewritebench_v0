# User Command

The current CLI supports `--case-list`; it does not expose the `--cases` shorthand used in the task sketch.

Case-list file:

```bash
printf 'CONS_0036\nPERF_0006\n' > /tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_v0_case_list.txt
```

Executed no-secret gate-smoke command:

```bash
env -u SQLRB_LLM_API_KEY -u GPTSAPI_API_KEY -u SQLRB_LLM_ALLOW_LIVE \
  SQLRB_LLM_PROVIDER=openai_compatible \
  SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1 \
  SQLRB_LLM_MODEL=gpt-5.4 \
  python -m cli.main user evaluate \
    --case-set common_core_v0 \
    --case-list /tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_v0_case_list.txt \
    --engines postgres,mysql,spark \
    --adapter-command "python baselines/direct_llm_original/adapter.py" \
    --output-root /tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_v0/output \
    --run-id direct_llm_original_bounded_live_api_smoke_v0 \
    --enable-db-execution \
    --enable-checker
```

Why this was not a live-provider call:
- No API key was available.
- `SQLRB_LLM_ALLOW_LIVE=1` was not available.
- The adapter stopped before request construction and recorded `missing_api_key`.

D035 output shape:
- `/tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_v0/output/results/<run_id>/`
- `/tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_v0/output/logs/<run_id>/`
- `/tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_v0/output/reports/<run_id>/`

Runtime outputs were not committed.
