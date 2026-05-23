# sqlsolver_support_layout_config_contract_v0

Verdict: completed with one narrow test hardening change.

SQLSolver support remains located in the approved verifier-support layer:

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py`
- shared verifier-support helpers under `src/sql_rewrite_bench/verifier_support/`
- focused tests under `tests/user_entry/test_sqlsolver_support.py`

No top-level `SQLSolver_support/`, `sqlsolver_support/`, `tools/sqlsolver/`, `configs/sqlsolver/`, repository-local SQLSolver tree, JAR, native library, ANTLR library, Gradle cache, or build output was found or created.

Configuration discovery is environment-variable based. The approved external JAR path is discovered through `SQLRB_SQLSOLVER_JAR` or `SQLRB_SQLSOLVER_ROOT`, with optional `SQLRB_SQLSOLVER_LD_LIBRARY_PATH` and `SQLRB_SQLSOLVER_JAVA`.

Runtime outputs remain local-only. Audits use `/tmp/...`; user-facing verifier output remains under `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
