# Protected Surface Check

Allowed changed paths:

- `audits/verifier_user_facing_rerun_contract_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

No source code, tests, cases, case sets, baselines, top-level reports/results, retained evidence, repository-level output, `runs/user`, SQLSolver external files, or VeriEQL external files should change.

Validation result before staging:

- Audit Markdown sanity: 11 Markdown files non-empty.
- `git diff --check`: passed.
- Protected path check: only this audit packet and project-control files changed.
- External SQLSolver source tree status: clean.
- External VeriEQL source tree status: unchanged except pre-existing `M constants.py`.
- No source code, tests, cases, case sets, baselines, top-level reports/results, retained evidence, repository-level output, or `runs/user` files changed.

Staged validation:

- `git diff --cached --check`: passed.
- Staged path check: 13 staged paths, all under allowed paths.
- No source, test, runtime, external verifier, reports/results, retained-evidence, or `runs/user` paths staged.
