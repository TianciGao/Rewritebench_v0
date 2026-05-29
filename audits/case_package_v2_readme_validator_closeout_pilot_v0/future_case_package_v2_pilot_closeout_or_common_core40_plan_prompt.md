# Future Prompt: case_package_v2_pilot_closeout_or_common_core40_plan_v0

Task title: `case_package_v2_pilot_closeout_or_common_core40_plan_v0`

Repository:

- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema` unless a maintainer explicitly authorizes a different branch.
- Do not merge to `main`.
- Do not inspect or modify the legacy repo.

Goal:

Review the completed five-case v2 pilot and decide the next branch-only action:

1. close out the pilot for maintainer review, or
2. draft a Common-core 40 conversion plan using the folder-ordered rulebook.

Required inputs:

- `audits/case_package_v2_readme_validator_closeout_pilot_v0/`
- all earlier `case_package_v2_*` pilot and rulebook audits
- the five pilot case packages
- `repository_spec/*v2*` and related v2 draft specs

Boundaries:

- Do not convert additional cases unless a separate writable task is authorized.
- Do not run DB/checker execution.
- Do not compute official metrics.
- Do not render paper tables.
- Do not update reports/results, case_sets, inventory, denominator values, or paper results.
- Do not create leaderboard output.
- Do not delete case-local evidence or runs.

Expected output:

- a pilot acceptance checklist
- a Common-core 40 conversion readiness matrix
- protected-boundary checks
- exact next safe action
