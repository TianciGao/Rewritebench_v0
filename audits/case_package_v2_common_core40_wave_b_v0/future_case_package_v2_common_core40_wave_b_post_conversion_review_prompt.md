# Future Prompt: case_package_v2_common_core40_wave_b_post_conversion_review_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify main or inspect the legacy repo.

Task:
Run a branch-only read-only parity review for the 22 converted Wave B cases, the five accepted pilot cases, and the five Wave A cases.

Scope:
- Verify all Wave B cases pass the v2 static validator.
- Recheck pilot and Wave A cases for non-regression.
- Confirm manifest shape consistency: direct SQL lists, profile-first schema refs, canonical checker/validation refs, source-as-oracle witness policy, regeneration-first evidence policy, and no mandatory evidence_ref.
- Confirm clean-template-minimal case-local structure and absence of v1 compatibility surfaces.
- Confirm no PORT/manual-review cases, case_sets, inventory, reports, results, denominators, paper results, metrics, DB/checker execution, or leaderboard outputs changed.

Required outputs:
Create `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/` with parity summary, case summary, manifest recheck, clean-template gap matrix, schema policy recheck, protected boundary checks, JSON summary, command log, and a future Wave C/manual-review prompt.

Do not perform conversion or cleanup in the review task.
