# Test Coverage Review

Focused SQLSolver tests cover:

- unavailable SQLSolver fails closed without fake verdicts;
- missing command discovery fails closed;
- external JAR env discovery through `SQLRB_SQLSOLVER_ROOT`;
- missing Java fails closed with `java_not_found`;
- JAR command construction;
- result normalization for `EQ`, `NEQ`, `UNKNOWN`, and `TIMEOUT`;
- nonzero command failure fails closed as `tool_error`;
- local result-checker exactness is not used as verifier evidence;
- output paths use temporary `output/results`, `output/logs`, and `output/reports`;
- no leaderboard/ranking/winner fields are emitted.

This task added one focused regression test:

- `test_env_jar_discovery_fails_closed_when_java_missing`

No real SQLSolver installation is required for the focused tests.
