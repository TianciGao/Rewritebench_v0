# Command Log

Preflight:

- `git status -sb`
- `git branch --show-current`
- `git fetch origin main feature/case-package-v2-external-schema`
- `git merge-base --is-ancestor 10fe6b3ad4e23ba21e0eb459744701d66933a84e origin/feature/case-package-v2-external-schema`
- Read project-control files from `origin/main` and `origin/feature/case-package-v2-external-schema`.
- `rg -n 'D032|D033|D034|D035' project_control/DECISION_LOG.md`
- `java -version`
- `git -C /home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver status -sb`
- `find . -path '*SQLSolver*' -o -name 'sqlsolver-v1.1.0.jar' -o -name 'libz3.so' -o -name 'libz3java.so' -o -name 'antlr-4.8-complete.jar'`

Run inspection:

- Read `runs/user/common_core_pg_noop_db_checker/ledger.csv`.
- Read `runs/user/common_core_pg_noop_db_checker/selected_cases.csv`.
- Inspected selected source/candidate SQL and schema paths.
- Compared known VeriEQL statuses from prior audit CSVs.

SQLSolver pass:

- Generated SQLSolver input copies under `/tmp/sqlrb_sqlsolver_pg_noop_tiny_exact_candidate_pass_v0/sqlsolver_inputs/`.
- Invoked SQLSolver through `write_sqlsolver_smoke`.
- Runtime output written under `/tmp/sqlrb_sqlsolver_pg_noop_tiny_exact_candidate_pass_v0/`.

Validation:

- Audit Markdown/CSV/JSON sanity passed: 12 Markdown files non-empty, `per_pair_verdicts.csv` has 15 rows, `per_row_identity_summary.csv` has 5 rows, and `diagnostic_summary.json` parsed.
- `pytest tests/user_entry/test_sqlsolver_support.py -q`: 10 passed.
- `git diff --check`: passed.
- Protected-surface check passed before staging; only this audit packet and project-control files changed.
- External SQLSolver source tree status: clean.
- Staged VeriEQL source tree unchanged except pre-existing `M constants.py`.
- No SQLSolver source, JAR, native library, ANTLR library, or external build output found inside the release repo.
- Staged diff check: passed.
- Staged protected-path and third-party artifact checks: passed.
