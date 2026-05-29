# Migration Plan For Existing Clients

Source inspection identified the current live-capable or live-planned clients below. This task did not refactor them.

## Existing Clients

`baselines/direct_llm_original/adapter.py`

- Uses `SQLRB_LLM_PROVIDER`, `SQLRB_LLM_BASE_URL`, `SQLRB_LLM_API_KEY`, `SQLRB_LLM_MODEL`, `SQLRB_LLM_TEMPERATURE`, `SQLRB_LLM_TOP_P`, `SQLRB_LLM_MAX_TOKENS`, `SQLRB_LLM_TIMEOUT`, `SQLRB_LLM_ALLOW_LIVE`, `SQLRB_LLM_AUTH_HEADER`, and `SQLRB_LLM_SAVE_RAW_RESPONSE`.
- Accepts `GPTSAPI_BASE_URL`, `GPTSAPI_API_KEY`, and `GPTSAPI_MODEL` aliases.
- Fails closed if live is disabled or the key is missing.

`baselines/direct_llm_repair_1/adapter.py`

- Uses the same shared provider aliases as Direct LLM original.
- Keeps Repair-1 route behavior separate from original route behavior.
- Fails closed if live is disabled or the key is missing.

`baselines/rbot/adapter.py`

- Uses shared provider aliases plus route-specific `SQLRB_RBOT_MODE`, `SQLRB_RBOT_FAKE_RESPONSE`, `SQLRB_RBOT_FAKE_SQL`, and `SQLRB_RBOT_TIMEOUT`.
- Live adapted mode is gated by `SQLRB_LLM_ALLOW_LIVE=1`.

`baselines/llm_r2/adapter.py`

- Uses shared provider aliases plus route-specific `SQLRB_LLM_R2_MODE`, `SQLRB_LLM_R2_FAKE_RESPONSE`, `SQLRB_LLM_R2_FAKE_SQL`, `SQLRB_LLM_R2_FAKE_RULE_SEQUENCE`, `SQLRB_LLM_R2_RULE_SYSTEM_CMD`, `SQLRB_LLM_R2_CHECKPOINT_PATH`, and `SQLRB_LLM_R2_DEMO_SELECTOR_PATH`.
- Live adapted mode is gated by `SQLRB_LLM_ALLOW_LIVE=1`.

`src/sql_rewrite_bench/pocr/annotation_client.py`

- Defines a minimal `AnnotationClientConfig` and OpenAI-compatible annotation client.
- Requires explicit `allow_live=True` and caller-supplied API key.

`src/sql_rewrite_bench/pocr/live_smoke.py`

- Internal audit helper using `SQLRB_LLM_PROVIDER`, `SQLRB_LLM_MODEL`, `SQLRB_LLM_BASE_URL`, `SQLRB_LLM_API_KEY`, `SQLRB_LLM_AUTH_HEADER`, `SQLRB_LLM_ALLOW_LIVE`, and `GPTSAPI_*` aliases.
- Requires `--live-enabled` plus environment gate.

`src/sql_rewrite_bench/pocr/calibration_runner.py` and `src/sql_rewrite_bench/pocr/real_route_diagnostic_runner.py`

- Internal audit helpers that reuse `live_smoke._load_provider_env`.
- Require explicit live flags and remain diagnostic-only.

`src/cli/pocr_diagnostic.py`

- User-facing replay/annotation-missing facade.
- Forces `live_enabled=False`; it does not read keys or call APIs.

## Proposed Future Convergence

1. Introduce a shared config loader with preferred `SQLRB_*` public names.
2. Preserve `GPTSAPI_*` aliases for compatibility where current adapters already support them.
3. Document possible `OPENAI_API_KEY` and `VECTOR_ENGINE_*` aliases as compatibility-only if future implementation requires them.
4. Keep route-specific modes such as `SQLRB_RBOT_MODE` and `SQLRB_LLM_R2_MODE` outside the shared provider config.
5. Add common CLI flags in a later implementation task.
6. Add tests proving replay and annotation-missing modes do not read API keys.

## Risks Of Changing Now

- Current adapters already have route-specific fail-closed behavior and audit history.
- Refactoring live clients during contract work could change call gating or status metadata.
- Shared config should be implemented separately with focused tests and no behavior drift.

No behavior changed in this task.
