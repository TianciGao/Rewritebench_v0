# Direct LLM Original Track A 120 Canonical User Rerun v0

Task: `direct_llm_original_track_a_120_canonical_user_rerun_v0`

Branch: `feature/case-package-v2-external-schema`

Scope:

- Common-core v0.
- Engines: `postgres`, `mysql`, `spark`.
- Planned/selected rows: 120.
- Adapter: `baselines/direct_llm_original/adapter.py`.
- Adapter route/method metadata: `direct_llm_original` / `direct_llm_original`.
- Provider: `openai_compatible`.
- Base URL host: `api.gptsapi.net`.
- Model: `gpt-5.4`.

Outcome:

- Live provider enabled: yes.
- Provider health check: HTTP 200, no code 1010.
- Live API calls succeeded: 120/120.
- Candidate extraction/generated: 120/120.
- Source executable rows: 115/120.
- Candidate executable rows: 112/120.
- Checker exact rows: 102/120.
- Mismatch rows: 10.
- Not exact due to execution failure: 8.
- Exact timed rows: 90.

Canonical local metrics from `src/sql_rewrite_bench/local_metrics.py`:

- Generation rate: `1.0`.
- Execution coverage rate: `0.9333333333333333`.
- Result consistency rate: `0.85`.
- GM speedup ratio: `1.0132043433789995`.
- Speedup percentiles P10/P25/P50/P75/P90: `0.9719964696445886` / `0.9869093109718886` / `1.0010427055066198` / `1.012834345802451` / `1.0499237208126873`.

Boundary:

This is local diagnostic output only. It is not official metrics, not official SER, not formal Regression@20, not POCR, not paper results, not retained evidence, and not leaderboard input.
