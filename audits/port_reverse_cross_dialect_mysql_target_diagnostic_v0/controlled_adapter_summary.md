# Controlled Adapter Summary

Adapter: `examples/user/port_mysql_target_reference_adapter.py`.

Behavior:

- Reads `SQLRB_CASE_DIR`, `SQLRB_CANDIDATE_SQL_PATH`, and `SQLRB_ENGINE`.
- Requires `SQLRB_ENGINE == mysql`.
- Parses `manifest.yaml`.
- Resolves only `local_diagnostic.engine_roles.mysql`.
- Requires `diagnostic_mode == cross_dialect_reference`.
- Requires `target_candidate.role == adapter_output` and `target_candidate.engine == mysql`.
- Requires `target_reference.role == positive_reference`, `target_reference.engine == mysql`, and `target_reference.use_for_checker_oracle == false`.
- Copies the declared `target_reference.query` to the runner-provided candidate path.
- Does not infer `pos_01.sql` from filename.
- Does not execute SQL, compute metrics, compute timing, or write outside the candidate workspace.

This adapter is a local diagnostic control, not a user method or benchmark baseline.
