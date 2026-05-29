# Command Log

Preflight and source inspection:

- `git status -sb`
- `git branch --show-current`
- `git fetch origin main feature/case-package-v2-external-schema`
- `git merge-base --is-ancestor 7f5dff3825b42eaf2efce6cde9499bce9276c9cc origin/feature/case-package-v2-external-schema`
- `rg -n 'D032|D033|D034|D035' project_control/DECISION_LOG.md`
- `java -version`
- `gradle --version`
- `git --version`
- `sed -n '1,260p' /home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/README.md`

External setup:

- `git clone https://github.com/SJTU-IPADS/SQLSolver /home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver`
- `./gradlew fatJar`
- `LD_LIBRARY_PATH=/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/lib java -jar /home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/build/libs/sqlsolver-v1.1.0.jar -help`

Implementation and tests:

- `python -m py_compile src/sql_rewrite_bench/verifier_support/sqlsolver.py`
- `pytest tests/user_entry/test_sqlsolver_support.py -q`
- `pytest tests/user_entry/test_sqlsolver_support.py tests/user_entry/test_verifier_support.py tests/user_entry/test_cli_facade.py -q`
- `pytest tests/user_entry -q`

Smoke:

- Synthetic SQLSolver smoke executed through `write_sqlsolver_smoke` under `/tmp/sqlrb_sqlsolver_external_setup_wrapper_smoke_v0/`.

Validation:

- Audit Markdown sanity: passed, 12 Markdown files non-empty including `audits/sqlsolver_external_install_review.md`.
- `git diff --check`: passed.
- Protected-surface check: passed before staging; no cases, case sets, baselines, reports, results, repository-level output, `runs/user`, retained evidence, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md` paths changed.
- External SQLSolver source tree status after build: clean.
- Staged VeriEQL source tree status unchanged from preflight except pre-existing `M constants.py`.
- Staged diff check: passed.
- Staged third-party artifact check: passed, no SQLSolver source/JAR/libs/build outputs staged.
