# Verdict Normalization Review

SQLSolver output vocabulary:

| Raw SQLSolver output | Normalized verdict |
|---|---|
| `EQ` | `equivalent` |
| `NEQ` | `non_equivalent` |
| `UNKNOWN` | `unknown` |
| `TIMEOUT` | `timeout` |

Fail-closed handling:

- Nonzero command exits normalize to `tool_error`.
- Missing JAR, missing Java, missing native library path, missing schema, unreadable input, and unparseable output are visible as fail-closed states.
- Parser/command failures are not converted into equivalence.
- Local result-checker exactness is recorded as unused and cannot substitute for SQLSolver evidence.

Boundary flags remain present:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`
