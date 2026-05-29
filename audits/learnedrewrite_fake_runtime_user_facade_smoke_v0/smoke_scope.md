# Smoke Scope

## Selected Rows

The smoke used a temporary case list:

```text
PERF_0006
CONS_0036
```

and ran PostgreSQL only. MySQL and Spark were intentionally not selected because the current LearnedRewrite scaffold is PostgreSQL-first and fail-closes unsupported engines.

## Fake Runtime Scope

The adapter was invoked through the D035 user-facing facade with:

- `SQLRB_LEARNEDREWRITE_MODE=fake`
- `SQLRB_LEARNEDREWRITE_FAKE_RESPONSE={"status":"ok","rewritten_sql":"SELECT 1 AS learnedrewrite_fake_candidate"}`

No `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1` was set. No external runtime command or HTTP URL was required.

## Why Fake Runtime Is Enough

This task validates only facade integration, candidate-file emission, metadata writing, single-SQL extraction, and fail-closed behavior. The real LearnedRewrite runtime remains blocked until a separate external-runtime preflight verifies path/configuration, request/response schema, extraction guards, source hygiene, and no-vendor boundaries.

## Claims Not Made

This smoke makes no correctness, performance, official metric, paper, retained-evidence, or Track A 120 claim.
