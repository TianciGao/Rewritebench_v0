# Export Readiness Recommendation

Verdict: a later export/tag planning task is safe.

This branch is ready to plan export mechanics because the major public-v0 surfaces are present, the Common-core 40 case-package layer is closed, user-entry U0-U7 is closed as local diagnostics, and release metadata skeleton/polish is complete.

Before any actual export branch or release tag, maintainers should decide:

- Whether the top-level README should switch to English primary or become bilingual.
- Whether `CITATION.cff` placeholders are acceptable for a pre-release artifact, or whether final paper metadata is required first.
- Whether boundary-only `reports/` and `results/` are acceptable for public v0, given that official metrics and paper tables remain deferred.
- The exact release branch and tag naming policy.
- Whether construction audit packets and project-control files remain in the public construction branch, or whether a separate export surface should be curated later.

Recommended release mechanics posture:

- Treat this task as planning only.
- Do not create a tag or export branch without a later explicit maintainer authorization.
- Keep Common-core v0 membership and the 120-row Track A denominator unchanged.
- Preserve the no-global-leaderboard and denominator-aware reporting boundaries.
- Keep official metrics, paper rendering, timing/speedup, retained-evidence integration, and reports/results migration out of export planning unless separately authorized.

Reports/results boundary-only status is acceptable for export planning, but the future export task must explicitly state whether public v0 is a benchmark/workbench release without regenerated paper tables, or whether curated result artifacts are required before public artifact release.
