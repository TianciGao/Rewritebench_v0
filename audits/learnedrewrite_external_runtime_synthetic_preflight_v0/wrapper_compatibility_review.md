# Wrapper Compatibility Review

## Current Adapter

`baselines/learnedrewrite/adapter.py` is still a fixture-only scaffold:

- fake mode works;
- command/http real modes fail closed by design;
- no real Java process or network call is made by the adapter;
- schema context is recorded by reference, not serialized to LearnedRewrite schema JSON.

## Command Mode Compatibility

Not compatible yet.

No row-scoped command contract was recovered from this JAR. The JAR is a server entrypoint with `Main-Class: server`, not a single-row CLI wrapper.

## HTTP Mode Compatibility

Partially compatible at the transport level only:

- server starts on `127.0.0.1:6336`;
- `/rewriter` accepts one JSON POST and returns JSON;
- response did not include candidate SQL because runtime setup failed.

Before adapter HTTP mode can be enabled, the wrapper needs:

- runtime URL env gate;
- timeout;
- request JSON serialization;
- response extraction from `data.rewritten_sql`;
- fail-closed mapping for `status=false`;
- no-secret metadata.

## Schema JSON Compatibility

Unproven.

The synthetic schema shape followed the official example style, but the runtime failed due missing relative assets before schema correctness could be evaluated.

## Single-SQL Extraction Compatibility

Not compatible for this preflight result.

No single SQL was extractable. The release adapter should reject this response as `no_rewritten_sql` or `runtime_failed`.

## Metadata / Fail-Closed Behavior

Future adapter metadata should record:

- `runtime_mode=http`
- `external_runtime_configured=true`
- `fake_runtime=false`
- `real_java_runtime_invoked=true`
- `network_invoked=true`
- `candidate_generated=false`
- `fail_closed_reason=runtime_missing_workdir_asset` or `runtime_failed`
- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result=false`

## Verdict

Wrapper compatibility verdict: blocked.

Reason: the runtime server can start and respond, but the safe temp-working-directory invocation cannot find required relative runtime assets and returns no candidate SQL. A temp-only runtime staging fix is needed before any D035 external-runtime smoke.
