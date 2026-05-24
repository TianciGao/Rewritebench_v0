# LearnedRewrite Adapter Design

## Proposed Location

Future adapter path:

```text
baselines/learnedrewrite/adapter.py
```

This task creates no adapter. The path is a design target only.

## Route Identity

- `route_id = learnedrewrite`
- `method_id = learnedrewrite`
- route family: prior method external wrapper
- initial role: bounded prior-method appendix evidence candidate

## Adapter Command Shape

Future D035 user-facade command shape:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --adapter-command "python baselines/learnedrewrite/adapter.py" \
  --output-root /tmp/sqlrb_learnedrewrite_no_live_or_bounded_output \
  --run-id learnedrewrite_bounded_pg_v0
```

A Track A 120-shaped run must not be attempted until PostgreSQL, MySQL, and Spark support boundaries are explicit and denominator-visible.

## Environment Variables

Suggested future adapter configuration:

- `SQLRB_LEARNEDREWRITE_MODE`: `fake`, `http`, or `cmd`.
- `SQLRB_LEARNEDREWRITE_URL`: external HTTP endpoint for `/rewriter`.
- `SQLRB_LEARNEDREWRITE_CMD`: external command for a row-scoped wrapper.
- `SQLRB_LEARNEDREWRITE_TIMEOUT`: per-row timeout, default 30 seconds.
- `SQLRB_LEARNEDREWRITE_SCHEMA_POLICY`: schema JSON serialization policy id.
- `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME`: required gate for real Java runtime calls.
- `SQLRB_LEARNEDREWRITE_FAKE_RESPONSE`: fixture-only fake JSON response.

No API key is required for LearnedRewrite. If an external runtime path is supplied, metadata should avoid writing sensitive absolute paths unless needed for local debug and clearly marked local-only.

## No-Vendor Policy

The adapter must not import or copy upstream Java source. It must not vendor:

- `rewriter_java.jar`;
- Calcite dependency JARs;
- upstream source files;
- upstream datasets;
- old generated outputs;
- request logs.

## No-Live/No-Runtime Test Mode

Initial fixture tests should use `SQLRB_LEARNEDREWRITE_MODE=fake`.

Fake mode should:

- read D035 row env vars;
- parse a fake JSON response;
- validate one-SQL extraction;
- write candidate SQL on success;
- write status metadata;
- fail closed on malformed or unsupported fixture responses.

Fake mode should not:

- run Java;
- open HTTP connections;
- execute SQL;
- run checker;
- collect timing;
- compute metrics.

## D035 Compatibility

The adapter must read the same D035 row variables used by current baselines and write to `SQLRB_CANDIDATE_SQL_PATH` only when a valid single candidate exists.

The user facade remains responsible for:

- row selection;
- candidate preflight;
- optional DB execution;
- optional checker;
- optional exact-gated timing;
- local metrics only after a complete user-run ledger exists.

## Initial Engine Policy

Initial implementation should be PostgreSQL-first:

- PostgreSQL: eligible for fake-mode and later tiny external-runtime smoke.
- MySQL: fail closed as `unsupported_engine` until dialect support is proven.
- Spark: fail closed as `unsupported_engine` until dialect support is proven.

If a 120-shaped local diagnostic is later attempted, unsupported MySQL/Spark rows must remain visible in the selected denominator.

## Fail-Closed Cases

Fail closed when:

- runtime mode is missing or unsupported;
- real runtime gate is missing for `http` or `cmd`;
- source SQL path is missing;
- schema serialization fails;
- runtime is unavailable;
- runtime times out;
- runtime returns malformed JSON;
- runtime omits `rewritten_sql`;
- candidate SQL is empty, prose, or multiple statements;
- target dialect support is not proven;
- candidate cannot be written to the expected path.
