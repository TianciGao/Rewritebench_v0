# Future Prompt: case_package_v2_common_core40_final_closeout_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Task:
Run a branch-only read-only Common-core 40 v2 final closeout after Wave C is complete.

Scope:
- Review all 40 Common-core v2 case packages.
- Confirm clean-template-minimal status for every converted case.
- Treat retained `sql/dialect_variants/` in PORT semantic cases as optional v2 assets, not blockers.
- Re-run static v2 validators for all 40 cases and unit tests.
- Confirm no `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, `evidence/cases/`, or leaderboard changes.

Required outputs:
- Final Common-core 40 v2 closeout summary.
- Case-level clean-template matrix.
- Dialect-variant retention matrix.
- Validator regression results.
- Protected-boundary checks.
- Next safe action for public-release readiness or narrow provenance follow-up.
