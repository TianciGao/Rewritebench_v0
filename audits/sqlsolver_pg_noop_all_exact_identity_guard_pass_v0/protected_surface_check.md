# Protected Surface Check

Protected surface policy:

- No `src/` changes.
- No `tests/` changes.
- No `cases/`, `case_sets/`, `baselines/`, `reports/`, `results/`, retained evidence, repository-level `output/`, or `runs/user/` changes.
- No SQLSolver source, JAR, native libraries, ANTLR libraries, Gradle cache, or build outputs committed.
- Runtime files stayed under `/tmp/sqlrb_sqlsolver_pg_noop_all_exact_identity_guard_pass_v0/`.

Expected changed release-repo paths:

- `audits/sqlsolver_pg_noop_all_exact_identity_guard_pass_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result before staging:

- Audit Markdown sanity: 13 Markdown files non-empty.
- CSV sanity: `per_pair_verdicts.csv` has 105 rows; `per_row_identity_summary.csv` has 40 rows.
- JSON sanity: `diagnostic_summary.json` parsed and reported 40 selected rows, 35 exact rows, and 24 corrected decidable rows.
- `pytest tests/user_entry/test_sqlsolver_support.py -q`: 10 passed.
- `git diff --check`: passed.
- Protected path check: only the audit packet plus `project_control/MIGRATION_STATUS.md` and `project_control/MIGRATION_RUN_LOG.md` changed.
- Third-party artifact check: no SQLSolver source, JAR, native library, ANTLR library, Gradle cache, or build output found in the release repo.
- External SQLSolver source tree status: clean at commit `dcc2a91d8971a4c4d30b055f99d7d8428a1b754b`.
- Staged VeriEQL source tree unchanged except pre-existing `M constants.py`.

Staged validation:

- `git diff --cached --check`: passed.
- Staged path check: 18 staged paths, all under the audit packet or project-control files.
- Staged third-party artifact check: no SQLSolver source, JAR, native library, ANTLR library, Gradle cache, or build output staged.
