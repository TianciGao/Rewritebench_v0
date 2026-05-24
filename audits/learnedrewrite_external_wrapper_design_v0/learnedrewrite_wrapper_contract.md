# LearnedRewrite Wrapper Contract

## Future Route Identity

- `route_id = learnedrewrite`
- `method_id = learnedrewrite`
- proposed adapter path: `baselines/learnedrewrite/adapter.py`

This route is a prior-method local diagnostic candidate. It is not an official paper reproduction unless a separate promotion task is authorized.

## Input Contract

The future adapter should consume the standard D035 adapter environment:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

Additional resolved context needed by the adapter:

- `schema_ref` and engine-specific DDL/load paths from the case package resolver.
- source SQL text.
- target engine/dialect: `postgres`, `mysql`, or `spark`.
- per-row timeout.

## External Runtime Contract

Supported future modes:

- `fake`: fixture-only mode, no Java runtime.
- `http`: call an externally running LearnedRewrite HTTP server.
- `cmd`: call a local external row-scoped command wrapper supplied outside this repo.

The adapter must not start or vendor an upstream Java server by default. If a future task authorizes server management, that management should happen outside the release repo or in a temp-only harness.

## HTTP Request Shape

The official README documents:

```text
POST /rewriter
{ "sql": "...", "schema": ... }
```

The release adapter should serialize the schema as a JSON string or JSON array only after a schema fixture contract is tested. It should not infer operation atoms, paper metrics, or verifier evidence from the LearnedRewrite response.

## Expected Output Contract

Accepted runtime output:

- JSON object containing `rewritten_sql`, or a documented equivalent field in fake mode.
- The value must be exactly one complete SQL query.
- The candidate must be written to `SQLRB_CANDIDATE_SQL_PATH`.

Rejected runtime output:

- missing `rewritten_sql`;
- empty string;
- prose;
- multiple SQL statements;
- multiple candidate fields without an explicit selection policy;
- malformed JSON;
- source/runtime stack traces;
- SQL for an unsupported target dialect.

## Status Codes

Recommended normalized statuses:

- `candidate_generated`
- `runtime_unavailable`
- `runtime_timeout`
- `runtime_failed`
- `runtime_invalid_json`
- `no_rewritten_sql`
- `empty_candidate_sql`
- `multiple_sql_statements`
- `unsupported_engine`
- `schema_context_unavailable`
- `schema_serialization_failed`
- `source_like_candidate`
- `candidate_generated_source_like`

## Fail-Closed Rules

The adapter must fail closed with no candidate SQL when:

- source SQL is missing;
- schema context is missing or ambiguous;
- target engine is unsupported by policy;
- external runtime path or URL is missing in real modes;
- runtime exits nonzero or times out;
- response is not parseable JSON;
- response has no valid complete SQL;
- extraction finds multiple statements;
- target dialect guard fails.

Unsupported MySQL/Spark status must remain denominator-visible if a 120-shaped route is attempted.

## Metadata Fields

Future row metadata should include:

- `route_id`
- `method_id`
- `case_id`
- `pool`
- `engine`
- `external_runtime_mode`
- `external_runtime_kind`
- `external_runtime_available`
- `external_runtime_version` when safely available
- `external_runtime_path_present` without printing path if sensitive
- `schema_ref`
- `schema_serialization_policy`
- `wrapper_contract_id`
- `extraction_policy`
- `candidate_sql_sha256` if generated
- `source_like_status`
- `local_diagnostic_only = true`
- `official_metric_input = false`
- `paper_result = false`
- `retained_evidence_promoted = false`
- `leaderboard_input = false`

No environment secret values should appear in metadata.
