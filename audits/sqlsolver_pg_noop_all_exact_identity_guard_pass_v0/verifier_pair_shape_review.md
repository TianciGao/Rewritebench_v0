# Verifier Pair Shape Review

Every exact row was converted into three local-only SQLSolver checks:

- `source_vs_source`: identity sanity for the source SQL.
- `candidate_vs_candidate`: identity sanity for the generated candidate SQL.
- `source_vs_candidate`: method candidate verification.

The wrapper invocation used the SQLSolver JAR CLI shape:

`java -jar <sqlsolver.jar> -sql1=<sql1_file> -sql2=<sql2_file> -schema=<schema_file> -output=<output_file>`

Generated SQL, schema, stdout, stderr, and SQLSolver output files were written only under `/tmp/sqlrb_sqlsolver_pg_noop_all_exact_identity_guard_pass_v0/`.

The committed audit ledger preserves:

- source SQL path;
- candidate SQL path;
- schema source path;
- sanitized runtime input paths under `/tmp`;
- raw SQLSolver output token;
- normalized verdict;
- runtime path references;
- local-only and non-paper flags.

The wrapper contract uses `source_vs_candidate` as its supported pair type. The audit records the actual logical pair role in `logical_pair_type`.
