# sqlsolver_external_setup_wrapper_smoke_v0

Closeout verdict: completed.

This task staged SQLSolver externally, implemented SQL-RewriteBench JAR-mode SQLSolver wrapper support, and validated the wrapper with focused tests plus a local-only synthetic smoke.

External SQLSolver source:

- Repository: `https://github.com/SJTU-IPADS/SQLSolver`
- Local external checkout: `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver`
- Commit: `dcc2a91d8971a4c4d30b055f99d7d8428a1b754b`
- JAR: `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/build/libs/sqlsolver-v1.1.0.jar`
- Native library path: `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/lib`

Wrapper status:

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py` now supports external JAR discovery through `SQLRB_SQLSOLVER_JAR`, `SQLRB_SQLSOLVER_ROOT`, `SQLRB_SQLSOLVER_LD_LIBRARY_PATH`, and `SQLRB_SQLSOLVER_JAVA`.
- Command shape: `java -jar <sqlsolver.jar> -sql1=<sql1_file> -sql2=<sql2_file> -schema=<schema_file> -output=<output_file>`.
- SQL/schema/output runtime files are generated in temporary directories.
- Verdicts normalize `EQ`, `NEQ`, `UNKNOWN`, and `TIMEOUT` into the shared verifier vocabulary.
- Missing JAR, missing Java, missing native library path, nonzero command exits, unreadable inputs, and unparseable output fail closed.

Synthetic smoke:

- Equivalent pair: `EQ` -> `equivalent`.
- Non-equivalent pair: `NEQ` -> `non_equivalent`.
- Runtime files were written under `/tmp/sqlrb_sqlsolver_external_setup_wrapper_smoke_v0/` only.

Boundary:

This is verifier-support infrastructure only. It is not official Semantic Equivalence Rate, not paper evidence, not retained evidence, and not leaderboard input.
