# Implementation Summary

## Files Changed

- Added `baselines/learnedrewrite/adapter.py`.
- Updated `baselines/learnedrewrite/README.md`.
- Added `tests/user_entry/test_learnedrewrite_adapter.py`.
- Added `audits/learnedrewrite_adapter_scaffold_v0/`.
- Updated `project_control/MIGRATION_STATUS.md`.
- Appended `project_control/MIGRATION_RUN_LOG.md`.

## Adapter Functions And Classes

The adapter adds:

- `RuntimeConfig`: normalized runtime configuration metadata.
- `RuntimeResult`: normalized fake/fail-closed runtime result.
- `ExtractionResult`: single-SQL extraction result.
- `load_env()`: D035 adapter environment validation.
- `resolve_runtime_config()`: mode/timeout/future hook discovery without invoking tools.
- `resolve_schema_context()`: schema context status and reference discovery.
- `extract_sql_candidate()`: single-SQL extraction from raw text or safe code fences.
- `_fake_runtime_response()`: fixture-only fake runtime handler.
- `_runtime_fail_closed()`: fake/command/http mode fail-closed dispatcher.
- `run()`: per-row adapter entrypoint.

## Fake Runtime Behavior

Fake mode is selected with:

```text
SQLRB_LEARNEDREWRITE_MODE=fake
```

It accepts either:

- `SQLRB_LEARNEDREWRITE_FAKE_RESPONSE`, with JSON object fields such as `status` and `rewritten_sql`; or
- `SQLRB_LEARNEDREWRITE_FAKE_SQL`, with inline SQL or a fenced SQL block.

Fake mode never invokes Java, network, DB, checker, timing, local metrics, or verifier tooling.

## Fail-Closed Behavior

Expected failures exit with code 0 and write `learnedrewrite_status.json` without writing candidate SQL.

Fail-closed buckets include:

- `runtime_unconfigured`
- `unsupported_runtime_mode`
- `command_runtime_missing_env`
- `http_runtime_missing_env`
- `external_runtime_not_implemented`
- `fake_runtime_missing_response`
- `runtime_invalid_json`
- `runtime_timeout`
- `runtime_failed`
- `unsupported`
- `no_rewritten_sql`
- `empty_candidate_sql`
- `response_empty`
- `response_not_sql`
- `multiple_sql_statements`
- `schema_context_unavailable`
- `unsupported_engine`

## Future External Runtime Hooks

Command and HTTP modes are recognized but not executed in this scaffold. They fail closed as future hooks. A separate authorization is required before adding real command or HTTP invocation.
