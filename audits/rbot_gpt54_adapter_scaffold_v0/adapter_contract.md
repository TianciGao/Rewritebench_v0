# Adapter Contract

## Input Contract

The adapter reads the standard user-facade row environment:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

It also uses optional fake/runtime variables:

- `SQLRB_RBOT_MODE=fake`
- `SQLRB_RBOT_FAKE_SQL`
- `SQLRB_RBOT_FAKE_RESPONSE`
- `SQLRB_RBOT_REQUIRE_RETRIEVAL`
- `SQLRB_RBOT_RAG_INDEX`

## Output Contract

On success, exactly one candidate SQL statement is written to `SQLRB_CANDIDATE_SQL_PATH`.

For success and fail-closed cases, `rbot_status.json` is written under `SQLRB_WORKSPACE_DIR`.

## Status Values

Fail-closed reasons include:

- `missing_source_sql`
- `missing_schema_context`
- `unsupported_engine`
- `runtime_unconfigured`
- `malformed_json`
- `response_empty`
- `response_not_sql`
- `multiple_sql_statements`
- `ambiguous_markdown`
- `live_gate_missing`
- `missing_api_key`
- `retrieval_unconfigured`
- `live_mode_not_implemented`

## User Facade Compatibility

The scaffold can be invoked by:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --case-list /tmp/cases.txt \
  --adapter-command "python baselines/rbot/adapter.py" \
  --output-root /tmp/sqlrb_rbot_gpt54_adapter_scaffold_v0/output \
  --run-id rbot_gpt54_fake_user_facade_smoke_v0
```

No DB/checker/timing/local metrics/verifier flags are required or used for the fake smoke.
