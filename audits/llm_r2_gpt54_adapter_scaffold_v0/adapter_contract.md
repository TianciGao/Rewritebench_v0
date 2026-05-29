# Adapter Contract

## Input Contract

The adapter consumes the standard D035 user-facade environment:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

Optional scaffold variables:

- `SQLRB_LLM_R2_MODE`
- `SQLRB_LLM_R2_FAKE_SQL`
- `SQLRB_LLM_R2_FAKE_RESPONSE`
- `SQLRB_LLM_R2_FAKE_RULE_SEQUENCE`
- `SQLRB_LLM_R2_SCHEMA_CONTEXT`
- `SQLRB_LLM_R2_REQUIRE_RULE_SYSTEM`
- `SQLRB_LLM_R2_RULE_SYSTEM_CMD`
- `SQLRB_LLM_R2_REQUIRE_CHECKPOINT`
- `SQLRB_LLM_R2_CHECKPOINT_PATH`
- `SQLRB_LLM_R2_REQUIRE_DEMO_SELECTOR`
- `SQLRB_LLM_R2_DEMO_SELECTOR_PATH`

Future live provider variables follow Direct LLM:

- `SQLRB_LLM_PROVIDER`
- `SQLRB_LLM_BASE_URL` / `GPTSAPI_BASE_URL`
- `SQLRB_LLM_MODEL` / `GPTSAPI_MODEL`
- `SQLRB_LLM_API_KEY` / `GPTSAPI_API_KEY`
- `SQLRB_LLM_ALLOW_LIVE`

## Output Contract

On success, the adapter writes exactly one SQL statement to
`SQLRB_CANDIDATE_SQL_PATH`. On both success and fail-closed paths, it writes
`llm_r2_status.json` under `SQLRB_WORKSPACE_DIR`.

## Metadata Fields

Key metadata fields include:

- `route_id=llm_r2_gpt54_adapted`
- `method_id=llm_r2`
- `provider_policy=openai_compatible`
- `model_policy=gpt-5.4`
- `adapted_gpt54_local_diagnostic=true`
- `original_paper_reproduction=false`
- `official_llm_r2_stack=false`
- `fake_runtime`
- `live_call`
- `rule_system_runtime_used`
- `checkpoint_used`
- `demonstration_selector_used`
- `rule_sequence_present`
- `extraction_policy`
- `candidate_generated`
- `fail_closed_reason`
- `local_diagnostic_only=true`

## Status Values

Common runtime statuses include `fake_runtime_ok`,
`fake_runtime_malformed_json`, `fake_runtime_unsupported`,
`runtime_unconfigured`, `live_gate_missing`, `missing_api_key`,
`live_not_implemented`, `rule_system_runtime_unavailable`,
`checkpoint_unavailable`, and `demonstration_selector_unavailable`.

Common extraction statuses include `extracted`, `response_empty`,
`sql_extraction_failed`, `ambiguous_markdown`, and
`multiple_sql_blocks_ambiguous`.

## User-Facade Compatibility

The adapter is invoked through `python -m cli.main user evaluate` using
`--adapter-command "python baselines/llm_r2/adapter.py"`. The smoke path uses
fake mode only and does not enable DB execution, checker, timing, local
metrics, or verifier.
