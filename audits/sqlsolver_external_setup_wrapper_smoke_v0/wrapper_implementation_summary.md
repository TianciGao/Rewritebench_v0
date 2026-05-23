# Wrapper Implementation Summary

Updated file:

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py`

Implemented behavior:

- Detect external SQLSolver JAR through `SQLRB_SQLSOLVER_JAR`.
- Detect external SQLSolver root through `SQLRB_SQLSOLVER_ROOT` and locate `build/libs/*.jar`.
- Detect Java through `SQLRB_SQLSOLVER_JAVA`, defaulting to `java`.
- Detect native library path through `SQLRB_SQLSOLVER_LD_LIBRARY_PATH`, or infer `<SQLSolver root>/lib`.
- Preserve the existing command-style fail-closed path for tests and developer shims.
- Generate temporary SQLSolver input files for `sql1`, `sql2`, `schema`, and SQLSolver output.
- Store shared verifier output records and raw stdout/stderr under the caller-provided local output root.
- Record metadata including `verifier_mode=jar_cli`, command shape, JAR path, native library path, tool availability, and `result_checker_exactness_used=false`.
- Fail closed for unavailable JAR, Java, native library path, nonzero command exit, missing schema, unreadable inputs, and unparseable output.

Not implemented:

- No SQLSolver source or JAR vendoring.
- No real benchmark-row verifier pass.
- No official Semantic Equivalence Rate computation.
- No paper reports/results update.
