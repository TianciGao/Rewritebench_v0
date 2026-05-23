# SQLSolver Status

Implementation status:

- Wrapper module: `src/sql_rewrite_bench/verifier_support/sqlsolver.py`
- Detection helper: `detect_sqlsolver`
- Output normalization helper: `normalize_sqlsolver_output`
- Bounded writer: `write_sqlsolver_smoke`

Local tool status from `sqlsolver_bounded_smoke_v3`:

- `tool_available=false`
- `tool_version=null`
- `detection_reason=sqlsolver_command_not_found`
- Real SQLSolver run performed: no

Fail-closed behavior:

- Unavailable tool writes `not_attempted` verdict rows.
- Raw stdout/stderr artifact paths are still contract-shaped.
- Summary records `semantic_equivalence_rate=null`.
- Summary records `na_reason=sqlsolver_unavailable`.

Future readiness gate:

- Provide an explicit command path or `SQLRB_SQLSOLVER_CMD`.
- Confirm tool version can be detected.
- Run the two-pair synthetic smoke: `SELECT 1` vs `SELECT 1`, then `SELECT 1` vs `SELECT 2`.
- Retain raw stdout/stderr under `output/results/<run_id>/verifier/tools/sqlsolver/`.
- Confirm normalized verdict mapping before any broader use.
