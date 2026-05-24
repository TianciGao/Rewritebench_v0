# Adapter Contract

## Route Identity

- `route_id = learnedrewrite`
- `method_id = learnedrewrite`
- `adapter_version = learnedrewrite_adapter_scaffold_v0`
- `wrapper_contract_id = learnedrewrite_external_wrapper_contract_v0`

## Input Contract

The adapter reads the D035 row environment:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

Optional fixture/runtime variables:

- `SQLRB_LEARNEDREWRITE_MODE`
- `SQLRB_LEARNEDREWRITE_FAKE_RESPONSE`
- `SQLRB_LEARNEDREWRITE_FAKE_SQL`
- `SQLRB_LEARNEDREWRITE_SCHEMA_JSON`
- `SQLRB_LEARNEDREWRITE_TIMEOUT`
- `SQLRB_LEARNEDREWRITE_CMD`
- `SQLRB_LEARNEDREWRITE_URL`
- `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME`

## Output Contract

On success:

- write exactly one complete SQL statement to `SQLRB_CANDIDATE_SQL_PATH`;
- write `learnedrewrite_status.json` under `SQLRB_WORKSPACE_DIR`;
- exit 0.

On expected fail-closed behavior:

- do not write `SQLRB_CANDIDATE_SQL_PATH`;
- write `learnedrewrite_status.json`;
- exit 0.

Unexpected adapter setup errors exit nonzero.

## Metadata Fields

The status JSON records:

- route and method identity;
- adapter version and wrapper contract id;
- run/case/pool/engine;
- source SQL path and source SQL SHA256;
- schema context status and schema reference;
- runtime mode and future external-runtime configuration booleans;
- fake runtime flag;
- Java/network/DB/checker/timing/local-metrics/verifier invocation booleans;
- extraction policy;
- runtime status;
- extraction status;
- candidate generation status;
- candidate SQL SHA256 when generated;
- fail-closed reason;
- local-only and non-official boundary flags;
- `no_upstream_source_or_jar_vendored=true`.

No secret values are recorded.

## Status Values

Primary successful status:

- `candidate_generated` through `candidate_generated=true` and `failure_bucket=none`.

Fail-closed statuses include:

- runtime configuration failures;
- unsupported engines;
- missing schema context;
- malformed fake JSON;
- unsupported fake status;
- timeout/failure simulation;
- missing or empty candidate SQL;
- prose-only response;
- multiple SQL statements.

## User Facade Compatibility

The adapter follows the same row-level candidate file contract used by current baselines. Future D035 user-facade smoke should pass:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --case-list <small-list> \
  --engines postgres \
  --adapter-command "python baselines/learnedrewrite/adapter.py" \
  --output-root /tmp/sqlrb_learnedrewrite_fake_smoke/output \
  --run-id learnedrewrite_fake_smoke_v0
```

The future smoke must use fake mode only and must not enable DB/checker/timing unless separately authorized.
