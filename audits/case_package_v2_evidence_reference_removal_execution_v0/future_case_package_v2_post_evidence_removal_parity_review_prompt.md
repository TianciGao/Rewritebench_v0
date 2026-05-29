# Future Prompt: case_package_v2_post_evidence_removal_parity_review_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify main.
- Do not inspect or modify the legacy repo.

Task title:
`case_package_v2_post_evidence_removal_parity_review_v0`

This is a branch-only read-only parity review after static evidence reference removal.

Pilot cases:
- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Goal:
- Confirm all five pilot cases remain clean-template-minimal under regeneration-first `evidence_policy`.
- Confirm no live case refs to `evidence_ref` or deleted `evidence/cases/<POOL>/<CASE_ID>/` paths remain.
- Confirm `PORT_0003/sql/dialect_variants/` remains the only optional clean-v2 local extension.
- Confirm Common-core 40 conversion planning is safe as a planning-only next step.

Hard boundaries:
- Do not modify cases, schemas, evidence, reports, results, case_sets, or inventory.
- Do not change denominators, paper results, case membership, or official metrics.
- Do not run DB/checker execution.
- Do not create leaderboard output.

Validation:
- Run the v2 static validator for all five pilot cases.
- Run `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Run protected-boundary checks and `git status -sb`.
