# Direct LLM Original Bounded Live API Smoke v0

Task: `direct_llm_original_bounded_live_api_smoke_v0`

Branch: `feature/case-package-v2-external-schema`

Scope:
- Route: `direct_llm_original`.
- Method: `direct_llm_original`.
- Cases: `CONS_0036`, `PERF_0006`.
- Engines: `postgres`, `mysql`, `spark`.
- Planned rows: 6.
- User-facing path: `python -m cli.main user evaluate`.

Outcome:
- Live provider smoke could not be completed because the required live environment was incomplete in this shell.
- No API key was present through `SQLRB_LLM_API_KEY` or `GPTSAPI_API_KEY`.
- `SQLRB_LLM_ALLOW_LIVE` was not set to `1`.
- A no-secret canonical D035 gate smoke was run with non-secret provider/base/model settings and no API key.
- All 6 rows failed closed before any network request with adapter bucket `missing_api_key`.

Run ids:
- `direct_llm_original_bounded_live_api_smoke_v0__postgres`
- `direct_llm_original_bounded_live_api_smoke_v0__mysql`
- `direct_llm_original_bounded_live_api_smoke_v0__spark`

Summary:
- Selected rows: 6.
- Live API calls attempted: 0.
- Live API calls succeeded: 0.
- Candidates extracted: 0.
- Candidates executed/checked: 0.
- Fail-closed rows: 6, all `missing_api_key`.

Boundary:
- No Track A 120 run.
- No timing.
- No verifier.
- No local metrics computation.
- No official metrics.
- No paper reports/results update.
- No retained-evidence promotion.
- No leaderboard output.
- No secrets committed.

Next safe action:
- Re-run the same bounded user-facade smoke only after `SQLRB_LLM_ALLOW_LIVE=1` and an API key are available in the environment.
