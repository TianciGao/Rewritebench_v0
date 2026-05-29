# Protected Surface Check

Allowed release-repo modifications:

- `audits/sqlsolver_pg_noop_tiny_exact_candidate_pass_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

No code changes were made.

Protected surfaces not modified:

- `src/`
- `tests/`
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
- SQLSolver external source tree
- VeriEQL source tree

Runtime artifacts:

- SQLSolver runtime files were written only under `/tmp/sqlrb_sqlsolver_pg_noop_tiny_exact_candidate_pass_v0/`.
- No runtime files are intended for staging or commit.

Final validation:

- Audit sanity passed.
- Focused SQLSolver tests passed.
- `git diff --check` passed.
- Protected path check passed before staging; no protected paths changed.
- External SQLSolver source tree remains clean.
- Staged VeriEQL source tree remains unchanged except pre-existing `M constants.py`.
- No SQLSolver source, JAR, native library, ANTLR library, or external build output found inside the release repo.
- Staged-path check passed; only this audit packet and project-control files were staged.
- No protected paths, SQLSolver source, JAR, native library, ANTLR library, or external build output were staged.
- Final clean/up-to-date status remains to be confirmed after commit and push.
