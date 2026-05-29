# Direct LLM Original Bounded Live API Smoke Post User-Agent Fix v0

Task: `direct_llm_original_bounded_live_api_smoke_post_user_agent_fix_v0`

Branch: `feature/case-package-v2-external-schema`

Scope:

- Cases: `CONS_0036`, `PERF_0006`
- Engines: `postgres`, `mysql`, `spark`
- Planned rows: 6
- Provider: `openai_compatible`
- Base URL host: `api.gptsapi.net`
- Model: `gpt-5.4`
- Adapter: `baselines/direct_llm_original/adapter.py`
- User-Agent fix: `SQL-RewriteBench/0.1`

Outcome:

- Live provider was enabled and reached.
- Selected rows: 6.
- Live API calls succeeded: 6.
- SQL candidates extracted/generated: 6.
- Source/candidate DB execution succeeded: 6/6.
- Checker exact rows: 6/6.
- Mismatch rows: 0.
- Failure bucket `none`: 6.
- `HTTP 403` / `code 1010` did not recur.

Conclusion:

The User-Agent fix resolved the GPTSAPI access failure for this bounded live smoke. Direct LLM original is ready for a larger bounded canonical smoke, but not yet for Track A 120 because this task validated only a two-case, three-engine live diagnostic and did not collect timing or official metrics.

Unrelated worktree note:

- Existing untracked prior audit directories were present before this task and were not touched or staged:
  - `audits/direct_llm_original_bounded_live_api_smoke_live_enabled_retry_v0/`
  - `audits/direct_llm_original_bounded_live_api_smoke_live_enabled_v0/`

