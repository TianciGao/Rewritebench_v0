# Future Prompt: case_package_v2_wave_c_or_caveat_followup_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not inspect or modify the legacy repo.

Goal:
Plan Wave C/manual-review Common-core v2 conversion using the accepted clean v2 template, while preserving the manifest caveat closeout result.

Context:
- `case_package_v2_manifest_caveat_closeout_v0` reviewed 19 retained manifest caveats across 32 converted v2 cases.
- 17 draft-origin caveats were accepted as non-blocking fallback provenance caveats.
- `PERF_0077` and `PERF_0082` still retain `source_path: manual_review_required` because allowed branch-history provenance leaves `source_entry` blank.

Hard boundaries:
- Do not invent provenance, taxonomy, source identity, benchmark identity, draft origin, or source paths.
- Do not modify `case_sets/`, `inventory/`, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs.
- Do not restore deleted compatibility directories, case-local evidence, case-local runs, or top-level `evidence/cases/`.

Recommended path:
- Proceed with `case_package_v2_common_core40_wave_c_manual_review_plan_v0` as a planning-only task if the maintainer accepts the two JOB source-path caveats as non-blocking for Wave C planning.
- Keep a separate narrow provenance follow-up for `PERF_0077` and `PERF_0082` before final public source-path closeout.
- If a future task has maintainer-provided exact JOB source locators, update only those two manifests and rerun the static v2 validator for all 32 converted cases.
