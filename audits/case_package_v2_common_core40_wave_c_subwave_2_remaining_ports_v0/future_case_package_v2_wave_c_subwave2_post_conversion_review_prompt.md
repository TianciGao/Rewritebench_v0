# Future Prompt: Wave C Subwave 2 Post-Conversion Review

Task title:
case_package_v2_common_core40_wave_c_subwave2_post_conversion_review_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Scope:
- Read-only review for `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025` after Wave C subwave 2 conversion.
- Regression-check pilot, Wave A, Wave B, and `PORT_0005` cases.
- Do not convert `PORT_0004` or `PORT_0013`.

Required checks:
- All five subwave 2 cases pass the v2 validator.
- Clean-template-minimal structure is present.
- Semantic manifest contract and three-file validation contract pass.
- Per-case external schema packages resolve.
- No dialect variants were created for no-current-dialect cases.
- Protected surfaces remain unchanged.

Next action after review:
- If review passes, authorize the final dialect-variant Wave C subwave for `PORT_0004` and `PORT_0013`, preserving `sql/dialect_variants/spark/` in both cases.
