# v2 Rulebook Refinement Command Log

Commands are summarized. No secrets, raw long outputs, DB/checker execution, metric computation, paper rendering, case conversion, schema/evidence deletion, reports/results update, denominator change, or leaderboard creation occurred.

## Preflight

- `pwd`: confirmed `/home/tianci_gao/code/Rewritebench_v0`.
- `git branch --show-current`: confirmed `feature/case-package-v2-external-schema`.
- `git remote -v`: reviewed origin.
- `git status -sb`: confirmed clean branch before edits.
- `git log --oneline -5`: reviewed recent branch commits.
- `git rev-list --left-right --count HEAD...origin/feature/case-package-v2-external-schema`: confirmed branch was not ahead or behind origin.

## Read-only Review

- Read project-control files.
- Read v2 repository specs and prior audit packets.
- Reviewed `src/sql_rewrite_bench/local_result_checker.py`, `src/sql_rewrite_bench/case_package_v2_resolver.py`, and `scripts/dev/validate_case_package_v2_refs.py` to distinguish existing shared modules from planned future modules.

## Writes

- Updated `project_control/MIGRATION_MASTER_PLAN.md` with schema profile-only policy and folder-ordered sequence.
- Added decision log entries for case-local schema profile-only policy and shared checker/validation modules.
- Updated v2 repository specs for case-local schema profile, external executable schema linkage, thin validation wrappers, shared module call graph, and plan artifact validation alignment.
- Created this audit packet under `audits/case_package_v2_rulebook_refinement_folder_order_v0/`.
- Updated migration status and run log.

## Validation

- Branch check: passed.
- Master-plan schema profile-only policy check: passed.
- Repository spec shared-module checks: passed.
- Required audit output existence check: passed.
- CSV header checks: passed.
- Folder-order row check: passed.
- Summary JSON parse and boundary assertions: passed.
- Protected path checks: passed.
- `git diff --check`: passed.
- `git status -sb`: reviewed before explicit staging.
