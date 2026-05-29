# Verifier Pair Shape Review

For each exact row, the pass executed three logical SQLSolver checks:

- `source_vs_source`
- `candidate_vs_candidate`
- `source_vs_candidate`

The current shared verifier pair schema supports `source_vs_candidate` but not identity-specific pair types. To avoid wrapper changes in this diagnostic task, the SQLSolver wrapper was invoked with contract-valid `pair_type=source_vs_candidate`; the audit CSV records the intended identity check in `logical_pair_type` and `pair_role`.

SQLSolver input handling:

- Query files were copied to `/tmp/sqlrb_sqlsolver_pg_noop_tiny_exact_candidate_pass_v0/sqlsolver_inputs/`.
- SQL comments and psql directives were removed from SQLSolver input copies.
- Schema copies retained only SQLSolver-relevant CREATE TABLE statements.
- Original source/candidate/schema paths are retained in `per_pair_verdicts.csv` and `per_row_identity_summary.csv`.

This avoided modifying repository case SQL, run output, schemas, or wrapper behavior.
