# Future Prompt: case_package_v2_wave_c_subwave_execution_v0

Repository:
- Work only in /home/tianci_gao/code/Rewritebench_v0.
- Work only on branch feature/case-package-v2-external-schema.
- Do not modify main or inspect/modify the legacy repo.

Task intent:
- Execute only precleared Wave C conversion subwaves from `audits/case_package_v2_common_core40_wave_c_preclearance_v0/`.
- Recommended first writable task: `case_package_v2_common_core40_wave_c_subwave_1_port0005_v0`, converting only `PORT_0005`.

Allowed future conversion scope:
- Convert only cases listed in `wave_c_subwave_recommendations.csv` for the selected subwave.
- Preserve existing `sql/dialect_variants/` for `PORT_0004`, `PORT_0005`, and `PORT_0013`.
- Create per-case external schema packages using the selected schema ids.
- Convert manifests to the semantic v2 contract without inventing source/provenance/taxonomy/dialect fields.
- Use direct SQL paths, profile-first schema references, config-only checker paths, thin validation wrappers, source-as-oracle witness policy, and regeneration-first `evidence_policy`.

Hard boundaries:
- Do not modify cases outside the selected subwave.
- Do not modify `case_sets/`, inventory, reports, results, denominators, paper results, official metrics, DB/checker execution, or leaderboard output.
- Do not delete dialect variants.
- Do not restore or require static evidence surfaces.
- Do not use `git add .`.

Stop conditions:
- Any public-safety/private/raw evidence issue appears.
- External schema copy cannot be verified.
- A manifest field would require invention rather than an explicit caveat.
- Dialect variants would be removed or silently rewritten.
- Static v2 validator or tests fail.

Validation:
- Run the v2 validator for converted cases and all previously converted pilot/Wave A/Wave B cases.
- Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Run JSON/CSV checks, `git diff --check`, and protected-boundary checks.
