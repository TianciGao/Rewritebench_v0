# Fake Runtime Contract

## Mode

Fake mode is enabled with:

```text
SQLRB_LEARNEDREWRITE_MODE=fake
```

It is the only runtime mode implemented in this scaffold.

## Fixture Response Schema

JSON fake response:

```json
{
  "status": "ok",
  "rewritten_sql": "SELECT ..."
}
```

Accepted SQL fields:

- `rewritten_sql`
- `candidate_sql`
- `sql`

Supported fake status values:

- `ok`: extract SQL from the configured SQL field.
- `unsupported` or `no_verifier_support`: fail closed as `unsupported`.
- `timeout` or `timed_out`: fail closed as `runtime_timeout`.
- `error`, `failed`, or `runtime_failed`: fail closed as `runtime_failed`.

Inline fake SQL:

```text
SQLRB_LEARNEDREWRITE_FAKE_SQL='SELECT ...'
```

or a single fenced SQL block.

## No Runtime Boundary

Fake mode never:

- runs Java;
- starts or contacts a server;
- invokes a shell command;
- opens a network connection;
- executes SQL;
- runs the checker;
- collects timing;
- computes local metrics;
- runs SQLSolver or VeriEQL;
- updates reports/results or retained evidence.

## Metadata

Fake-mode status metadata records:

- `runtime_mode=fake`
- `fake_runtime=true`
- `runtime_attempted=true` for a supplied fake fixture response
- `java_runtime_invoked=false`
- `network_invoked=false`
- `db_execution_invoked=false`
- `checker_invoked=false`
- `timing_invoked=false`
- `local_metrics_invoked=false`
- `verifier_invoked=false`
