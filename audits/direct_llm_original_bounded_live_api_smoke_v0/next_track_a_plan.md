# Next Track A Plan

Current status:
- Direct LLM original adapter scaffold exists.
- Fake-provider smoke passed in `direct_llm_provider_adapter_contract_v0`.
- This live-provider smoke did not reach a provider call because the live environment was incomplete.

Next safe action:
- Re-run this bounded canonical smoke after setting:
  - `SQLRB_LLM_ALLOW_LIVE=1`
  - `SQLRB_LLM_PROVIDER=openai_compatible`
  - `SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1`
  - `SQLRB_LLM_MODEL=gpt-5.4`
  - `SQLRB_LLM_API_KEY=<secret>` or `GPTSAPI_API_KEY=<secret>`

After a successful bounded live smoke:
- Inspect extraction and candidate SQL.
- Run the same 2-case x 3-engine smoke with DB execution/checker.
- Only then consider a larger bounded Direct LLM original smoke.

Track A 120 readiness:
- Not ready.
- Required first: successful live provider calls, successful single-SQL extraction, candidate generation, execution/checker behavior, and cost/rate-limit policy.

Repair-1 readiness:
- Still blocked.
- It requires Direct LLM original live outputs and execution/checker feedback contracts.
