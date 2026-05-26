# LLM API Configuration Plan

This document defines a future shared, user-facing LLM configuration model for SQL-RewriteBench.

The same configuration layer should serve:

- Direct LLM baseline generation.
- Direct LLM Repair-1 / feedback routes.
- POCR Stage A annotation generation.
- Future LLM-backed diagnostic tools.

This is a configuration plan only. It does not call API. It does not read API keys. It does not generate annotation JSONL. It does not modify paper-facing metrics.

## Unified Configuration Object

A future shared implementation should converge on one conceptual config object:

```text
LLMClientConfig:
  provider_label
  base_url
  api_key_env
  model
  temperature
  max_tokens
  timeout_seconds
  response_format
  retry_policy
  prompt_template_id
  prompt_template_version
  live_enabled
  diagnostic_only
```

This task documents the contract first. It does not require a new dataclass or behavior change. Prompt construction, response parsing, and route-specific output schemas remain separate from this shared transport/configuration layer.

## Environment Variable Contract

Preferred public configuration names use the `SQLRB_*` namespace:

- `SQLRB_LLM_PROVIDER`
- `SQLRB_LLM_BASE_URL`
- `SQLRB_LLM_API_KEY`
- `SQLRB_LLM_API_KEY_ENV`
- `SQLRB_LLM_MODEL`
- `SQLRB_LLM_TIMEOUT_SECONDS`
- `SQLRB_LLM_MAX_TOKENS`
- `SQLRB_LLM_TEMPERATURE`
- `SQLRB_LLM_RESPONSE_FORMAT`

Compatibility aliases may remain supported where existing code already uses them:

- `OPENAI_API_KEY`
- `VECTOR_ENGINE_API_KEY`
- `VECTOR_ENGINE_BASE_URL`
- `VECTOR_ENGINE_MODEL`
- `GPTSAPI_API_KEY`
- `GPTSAPI_BASE_URL`
- `GPTSAPI_MODEL`
- `SQLRB_LLM_TIMEOUT`
- `SQLRB_LLM_TOP_P`
- `SQLRB_LLM_ALLOW_LIVE`

Policy:

- Prefer `SQLRB_*` names in public docs and future CLI output.
- Existing aliases may remain supported for compatibility if already implemented.
- API key values must come from environment only.
- API key values must never be printed, written, staged, committed, or included in manifests, logs, reports, or audit packets.
- Manifests may record an environment variable name such as `SQLRB_LLM_API_KEY`; they must not record the value.

## CLI Flag Contract

Future LLM-capable user commands should use consistent flags:

- `--llm-provider`
- `--llm-base-url`
- `--llm-api-key-env`
- `--llm-model`
- `--llm-timeout-seconds`
- `--llm-max-tokens`
- `--llm-temperature`
- `--llm-response-format`
- `--enable-live-llm`
- `--enable-pocr-live-annotation`

Live LLM calls must be opt-in. POCR live annotation must require both POCR diagnostic mode and an explicit live annotation flag. Replay mode must not require or read API keys. Annotation-missing mode must not require or read API keys.

## Provider And Client Boundary

Direct LLM generation and POCR annotation may use the same OpenAI-compatible transport layer, but sharing configuration does not merge route evidence.

- Prompt construction remains route-specific.
- Direct LLM candidate-generation prompts remain distinct from Direct LLM Repair-1 prompts.
- POCR annotation prompts remain distinct from candidate-generation prompts.
- POCR annotation schema is distinct from baseline candidate-generation output schemas.
- Provider call metadata may be recorded, but secrets must never be stored.
- One shared config does not mean shared prompt, shared output schema, shared denominator, or shared evidence status.

Safe metadata includes provider label, model label, base URL domain when appropriate, call timestamp, token counts if available, and provider call status or error type. Unsafe metadata includes API key values, bearer tokens, raw `Authorization` headers, and raw provider secrets.

## POCR Live Annotation Policy

POCR live annotation must remain explicit and default-off.

`sqlrb user pocr-diagnostic` replay and annotation-missing modes must not read API keys and must not call a provider. A future live annotation command must require an explicit live flag in addition to the POCR diagnostic opt-in.

Annotation JSONL is diagnostic evidence only. Generated annotation JSONL must follow `pocr_annotation_artifacts.md`.

Stage A annotation alone is not counted. Stage B transformation-aware validation remains required for diagnostic operation support. No official POCR is computed by live annotation alone. No route-level POCR score is emitted. No paper-facing metric is promoted. No global leaderboard is produced.

## Baseline Generation Relationship

Direct LLM original and Direct LLM Repair-1 may share the same LLM config layer in the future.

This task does not change existing baseline generation behavior. Existing route metadata must remain route-specific. A shared API config must not merge routes or denominators. A shared API config must not create leaderboard output.

## Current Live-Capable Surfaces

Current source inspection found these live-capable or live-planned surfaces:

- `baselines/direct_llm_original/adapter.py`: OpenAI-compatible live generation using `SQLRB_LLM_*` and `GPTSAPI_*` aliases, gated by `SQLRB_LLM_ALLOW_LIVE=1`.
- `baselines/direct_llm_repair_1/adapter.py`: OpenAI-compatible Repair-1 live generation using the same provider aliases and live gate.
- `baselines/rbot/adapter.py`: adapted GPT-5.4 OpenAI-compatible live mode, with route-specific `SQLRB_RBOT_MODE` / fake-response controls and shared `SQLRB_LLM_*` provider config.
- `baselines/llm_r2/adapter.py`: adapted GPT-5.4 OpenAI-compatible live mode, with route-specific `SQLRB_LLM_R2_MODE` and optional rule-system/checkpoint/demo-selector variables.
- `src/sql_rewrite_bench/pocr/annotation_client.py`: minimal OpenAI-compatible POCR annotation client using caller-supplied config.
- `src/sql_rewrite_bench/pocr/live_smoke.py`, `calibration_runner.py`, and `real_route_diagnostic_runner.py`: internal audit helpers that read `SQLRB_LLM_*` / `GPTSAPI_*` aliases and require explicit live flags.
- `src/cli/pocr_diagnostic.py`: user-facing replay/annotation-missing path; it forces `live_enabled=False`.

## Migration Plan

Recommended later implementation steps:

1. Add a shared config loader under `src/sql_rewrite_bench` that resolves only environment variable names and safe metadata unless live mode is explicitly enabled.
2. Preserve existing `SQLRB_LLM_*` and `GPTSAPI_*` aliases while documenting `SQLRB_*` as the public preference.
3. Let Direct LLM original, Repair-1, R-Bot adapted, LLM-R2 adapted, and POCR annotation consume the shared config loader.
4. Keep route-specific prompts, run IDs, method IDs, route IDs, output schemas, and denominator scopes separate.
5. Add future CLI flags only behind explicit live opt-in and keep replay / annotation-missing modes no-key and no-API.
6. Record safe provider metadata in manifests without storing API key values.

Risks of changing now:

- Existing adapters already have bounded fail-closed behavior and route-specific audit history.
- A premature refactor could change live-call gating or output metadata shortly before release v0.
- A shared config object should be introduced with focused tests and no behavior drift in a separate implementation task.

## Non-Goals

- No API call is made.
- No API key is read.
- No annotation JSONL is generated.
- No baseline candidate generation is run.
- No POCR Stage B is run.
- No official POCR is computed.
- No paper-facing metric is promoted.
- No route-level POCR score is emitted.
- No leaderboard is produced.
