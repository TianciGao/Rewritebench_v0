# Final Public-Release Closeout Planning Audit

## Purpose

This packet records a read-only planning audit for final public-release closeout after Common-core 40 case-package closeout, Common-core README normalization, and the narrow `PERF_0077` / `PERF_0082` source-path provenance follow-up.

This task did not create a release tag, create an export branch, rewrite history, modify case files, compute metrics, render paper tables, or create a global leaderboard.

## Readiness Verdict

Release readiness verdict: blocked.

The Common-core case-package layer is ready for release planning: all 40 Common-core cases passed the final closeout rerun, all public case READMEs were normalized, and the remaining `PERF_0077` / `PERF_0082` source-path uncertainty was explicitly closed as retained nonblocking provenance uncertainty. The repository is not ready for an actual public release/export because public release-surface gaps remain outside the case packages.

## Evidence Reviewed

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `audits/case_package_v2_common_core40_final_closeout_rerun_v0/`
- `audits/perf_0077_0082_source_path_followup_v0/`
- Project-control entries for the finalized Common-core 40 public README batch
- `case_sets/common_core_v0/cases.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`
- `case_sets/common_core_v0/controls_360.csv`
- `inventory/case_registry.csv`
- Existing top-level release-surface files and directories

## Ready Areas

- Common-core v0 case-package readiness: 40/40 cases closed.
- Public case README readiness: 40/40 Common-core READMEs normalized to the public-facing template.
- Manifest semantic contract readiness: 40/40 cases passed.
- Validation three-file contract readiness: 40/40 cases passed.
- Dialect variant retention: `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013` retain dialect variants as semantic PORT assets.
- Source-path provenance follow-up: `PERF_0077` and `PERF_0082` are safe for public closeout with retained nonblocking uncertainty; no exact JOB source paths are claimed.
- Common-core denominator scaffolding: 40 cases and 120 same-engine denominator rows remain unchanged.

## Release-Blocking Gaps

- `LICENSE`, `CITATION.cff`, and `CONTRIBUTING.md` are not present.
- `benchmark_spec/` is not present as a public benchmark-spec surface.
- Curated public `reports/` and `results/` release surfaces are not present.
- Official metrics, paper-table rendering, and final reproduction outputs are not authorized or produced by this task.
- General retained-evidence adapters and public paper-reproduction flow remain incomplete for release-output claims.
- No clean export branch or release tag has been created.

## Nonblocking Caveats

- `PERF_0077` and `PERF_0082` retain explicit source-path provenance uncertainty. This is nonblocking for case-package and public source-path closeout, but release text must not claim exact JOB source paths for those cases.
- User-facing execution support exists only within the currently documented boundaries; this audit does not promote local smoke outputs to official metrics or paper results.
- Dialect variants are retained as semantic PORT assets and must not be treated as compatibility debris.

## Protected Boundary Summary

This audit writes only the planning packet and project-control status/log updates. It does not modify cases, schemas, manifests, SQL, checker files, validation files, case sets, inventory, reports, results, benchmark specs, repository specs, scripts, tests, source files, raw retained evidence, denominator scaffolds, paper results, or release tags.

## Exact Next Safe Action

Complete the missing public release-surface items in a separate bounded task: add release metadata (`LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`), create or confirm the public benchmark-spec surface, decide the curated `reports/` / `results/` release policy, and define the final export/tag procedure. Then rerun a final public-release closeout audit before any release tag or export branch is created.
