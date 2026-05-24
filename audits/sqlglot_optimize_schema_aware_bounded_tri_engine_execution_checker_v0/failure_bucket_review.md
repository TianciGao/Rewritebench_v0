# Failure Bucket Review

Failure buckets from the 9-row diagnostic:

| bucket | rows | case/engine |
| --- | ---: | --- |
| `none` | 6 | all PostgreSQL rows, MySQL `PERF_0006`, MySQL `CONS_0036`, Spark `PERF_0006` |
| `candidate_execution_failed` | 1 | MySQL `CONS_0005` |
| `mismatch` | 2 | Spark `CONS_0005`, Spark `CONS_0036` |

MySQL `CONS_0005`:
- Candidate includes `ARRAY_ANY`.
- Adapter stderr recorded `ARRAY_ANY is unsupported`.
- MySQL execution rejected the candidate SQL syntax.
- Classification: dialect emission / optimizer output blocker, not schema-context resolution failure.

Spark `CONS_0005`:
- Source and candidate both executed.
- Checker mismatch: source row count 0, candidate row count 1.
- Classification: optimizer semantic mismatch requiring manual triage.

Spark `CONS_0036`:
- Source and candidate both executed.
- Checker mismatch was label-only: values matched, labels differed (`C`/`NAME` vs `c`/`name`) under strict label policy.
- Classification: strict-label local checker mismatch, not an execution failure.

No source execution failures occurred.
