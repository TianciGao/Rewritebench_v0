# Route Contract

Route identifiers:

- `method_id`: `calcite_hep_fail_closed`
- `route_id`: `calcite_hep_fail_closed`
- `baseline_family`: `calcite`
- `route_role`: `same_engine_rewrite`
- `route_policy`: `fail_closed`

Adapter boundary:

- Entry command: `python src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py`
- User-entry integration: existing `sqlrb user evaluate --adapter-command ...` facade.
- Required SQL-RewriteBench environment variables are supplied by `adapter_runner`: `SQLRB_RUN_ID`, `SQLRB_CASE_ID`, `SQLRB_POOL`, `SQLRB_ENGINE`, `SQLRB_SOURCE_SQL_PATH`, `SQLRB_CASE_DIR`, `SQLRB_WORKSPACE_DIR`, and `SQLRB_CANDIDATE_SQL_PATH`.
- Optional Calcite discovery variables: `SQLRB_CALCITE_HEP_CMD`, `SQLRB_CALCITE_HEP_JAR`, `SQLRB_CALCITE_HEP_ROOT`, and `SQLRB_CALCITE_HEP_JAVA`.

Per-row status fields written to `calcite_hep_status.json`:

- route and method identifiers
- case, pool, engine, source SQL path, candidate SQL path
- `candidate_generated=false`
- `preflight_status`
- `unsupported_reason`
- discovery metadata for Java and Calcite env vars
- local-only boundary flags

The adapter must not write candidate SQL unless a separately authorized Calcite HEP backend contract exists.
