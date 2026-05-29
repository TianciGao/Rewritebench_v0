# Adapter Implementation Summary

Implemented files:
- `baselines/direct_llm_original/adapter.py`
- `baselines/direct_llm_original/README.md`
- `baselines/direct_llm_repair_1/README.md`
- `tests/user_entry/test_direct_llm_adapter.py`

Adapter responsibilities:
- Read the D035 user-run adapter environment.
- Resolve source SQL and per-engine schema/DDL context.
- Build deterministic prompt messages.
- Call a fake provider or an OpenAI-compatible chat/completions endpoint.
- Extract exactly one SQL candidate.
- Write candidate SQL to `SQLRB_CANDIDATE_SQL_PATH`.
- Write `direct_llm_prompt.json`, optional `direct_llm_raw_response.json`, and `direct_llm_status.json` in the workspace.

Fail-closed design:
- Missing API key, disabled live mode, unsupported provider, provider errors, empty responses, ambiguous extraction, and non-SQL responses do not crash the user runner.
- The adapter exits 0 without writing candidate SQL and records an explicit failure bucket.

Schema handling:
- Case-local DDL paths are supported.
- Current external schema profiles under `schemas/` are resolved for PostgreSQL, MySQL, and Spark.

Non-goals:
- No Repair-1 implementation.
- No source SQL mutation.
- No route-specific code under `src/sql_rewrite_bench/`.
- No metrics computation.
- No verifier integration.
- No paper-facing output.
