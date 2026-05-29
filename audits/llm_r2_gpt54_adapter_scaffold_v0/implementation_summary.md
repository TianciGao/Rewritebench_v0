# Implementation Summary

## Files Changed

- Added `baselines/llm_r2/adapter.py`.
- Added `baselines/llm_r2/README.md`.
- Added `tests/user_entry/test_llm_r2_adapter.py`.
- Added this audit packet under `audits/llm_r2_gpt54_adapter_scaffold_v0/`.

## Adapter Functions

The adapter implements:

- user-facade environment loading for one selected row;
- schema context discovery from inline context, case schema files, and
  external schema profile references;
- fake runtime response parsing;
- optional rule-sequence metadata capture;
- single `SELECT` / `WITH` SQL extraction;
- fail-closed metadata writing to `llm_r2_status.json`;
- future live/provider/rule-system/checkpoint/demo-selector placeholders that
  fail closed.

## Fake Runtime Behavior

Fake mode is enabled by `SQLRB_LLM_R2_MODE=fake` with either:

- `SQLRB_LLM_R2_FAKE_SQL`; or
- `SQLRB_LLM_R2_FAKE_RESPONSE` JSON.

The fake response can include `candidate_sql`, `rewritten_sql`, `output_sql`,
`sql`, or `content`, plus optional `rule_sequence` / `rules`.

## Fail-Closed Behavior

The scaffold fails closed without writing candidate SQL for missing source SQL,
missing schema context, unsupported engines, missing fake response, malformed
JSON, unsupported fake status, empty/prose-only/multiple-SQL output, rule-only
responses without candidate SQL, live mode without gate/key, and required
rule-system/checkpoint/demo-selector paths that are not configured.

## Future Hooks

The metadata and environment naming reserve future support for GPTSAPI /
OpenAI-compatible GPT-5.4 calls, an external rule-system runtime, checkpoints,
and demonstration selection. None of those paths execute in this task.
