# Fail-Closed Smoke Review

Adapter-level no-runtime fail-closed probes were run in temporary directories after the facade smoke. These did not invoke Java, network, DB execution, checker, timing, local metrics, or verifiers.

| Check | Expected bucket | Actual bucket | Candidate written | Passed |
|---|---:|---:|---:|---:|
| missing fake response | `fake_runtime_missing_response` | `fake_runtime_missing_response` | false | true |
| multiple statements | `multiple_sql_statements` | `multiple_sql_statements` | false | true |
| prose-only response | `response_not_sql` | `response_not_sql` | false | true |
| unsupported engine | `unsupported_engine` | `unsupported_engine` | false | true |

All fail-closed probes exited cleanly with code 0 and wrote metadata. They did not write candidate SQL.

Unsupported engines remain out of scope for the fake user-facade smoke and are handled by adapter fail-closed metadata rather than by attempting a real LearnedRewrite runtime.
