# Controlled Spark Target Adapter Summary

Adapter: `examples/user/port_spark_target_reference_adapter.py`

Behavior:
- Reads `SQLRB_CASE_DIR`, `SQLRB_CANDIDATE_SQL_PATH`, and `SQLRB_ENGINE`.
- Requires selected engine `spark`.
- Parses `manifest.yaml`.
- Requires `local_diagnostic.engine_roles.spark.diagnostic_mode == cross_dialect_reference`.
- Requires `target_candidate.role == adapter_output` and `target_candidate.engine == spark`.
- Requires `target_reference.role == positive_reference`, `target_reference.engine == spark`, and `target_reference.use_for_checker_oracle == false`.
- Copies only the manifest-declared Spark target reference query to the candidate output path.
- Fails closed with exit code 2 for missing, malformed, unsupported, ambiguous, or non-Spark metadata.
- Does not infer `pos_01.sql` or any dialect variant filename.
- Does not execute SQL, compute metrics, compute timing, write reports/results, or write outside the runner-provided workspace.

Focused adapter tests were added for real-case copy behavior, wrong selected engine, missing `target_reference`, checker-oracle misuse, and declared-path-only behavior.
