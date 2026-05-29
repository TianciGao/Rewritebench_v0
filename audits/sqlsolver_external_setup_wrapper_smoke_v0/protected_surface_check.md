# Protected Surface Check

Allowed release-repo modifications for this task:

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py`
- `tests/user_entry/test_sqlsolver_support.py`
- `audits/sqlsolver_external_setup_wrapper_smoke_v0/`
- `audits/sqlsolver_external_install_review.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces not modified:

- `cases/`
- `case_sets/`
- `baselines/`
- `reports/`
- `results/`
- retained evidence
- repository-level `output/`
- `runs/user/`
- `MIGRATION_MASTER_PLAN.md`
- `DECISION_LOG.md`
- VeriEQL source tree

External SQLSolver source/JAR/libs:

- Located only under `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver`.
- Not staged or committed in the release repository.

Final validation status:

- Audit sanity passed.
- `git diff --check` passed before staging.
- Pre-staging protected path check found no changes under protected benchmark/report/runtime paths.
- External SQLSolver source tree is outside the release repo and remains clean after build.
- Staged VeriEQL source tree remains unchanged except pre-existing `M constants.py`.
- Staged-path check passed; only allowed release-repo paths were staged.
- No third-party SQLSolver source, JAR, Z3 library, ANTLR library, Gradle wrapper/cache, or build output was staged.
- Final clean/up-to-date status remains to be confirmed after commit and push.
