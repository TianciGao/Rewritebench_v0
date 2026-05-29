# Future Prompt: case_package_v2_clean_template_cleanup_pilot_v0

Repository:

- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Goal:

Perform a branch-only cleanup pilot for the five v2 pilot cases, limited to cleanup actions marked `ready_for_cleanup=true` in:

`audits/case_package_v2_template_parity_gap_review_v0/template_parity_cleanup_readiness.csv`

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Allowed cleanup candidates:

- duplicated nested SQL compatibility directories after confirming no refs remain
- copied case-local notes after verifying external evidence notes
- placeholder-only case-local `runs/README.md` only if maintainer explicitly approves placeholder-runs cleanup

Forbidden actions:

- do not delete case-local `evidence/` without retention mapping
- do not delete case-local schema engine DDL/load until runner/schema_ref compatibility cleanup is authorized
- do not delete metadata until source-of-truth review is complete
- do not delete data/fixtures until witness/data policy review is complete
- do not delete engine-specific validation scripts until shared logic and caller audit are complete
- do not delete `PORT_0003` dialect variants without manual-review decision
- do not modify `case_sets/`, inventory, reports/results, denominators, paper results, or leaderboard outputs
- do not run DB/checker execution or compute official metrics

Required outputs:

- cleanup candidate manifest
- files removed manifest
- protected-boundary checks
- static validator results for all five cases
- exact next safe action
