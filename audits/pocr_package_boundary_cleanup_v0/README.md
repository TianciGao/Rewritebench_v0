# POCR Package Boundary Cleanup v0

This audit packet records a lightweight package-boundary cleanup for `src/sql_rewrite_bench/pocr/`.

Created:

- `src/sql_rewrite_bench/pocr/README.md`
- `audits/pocr_package_boundary_cleanup_v0/package_map.csv`
- `audits/pocr_package_boundary_cleanup_v0/public_internal_boundary.md`
- `audits/pocr_package_boundary_cleanup_v0/audit_only_helpers_review.md`
- `audits/pocr_package_boundary_cleanup_v0/init_export_review.md`
- `audits/pocr_package_boundary_cleanup_v0/protected_path_review.md`
- `audits/pocr_package_boundary_cleanup_v0/command_log.md`

No files were moved, renamed, deleted, or relocated. No import-breaking refactor was performed. No CLI behavior changed.

The package README defines public entry points, stable internal core modules, Stage A annotation modules, Stage B evidence modules, user diagnostic output modules, and internal audit/calibration helpers.

Boundary:

- This is not official POCR.
- No route-level POCR score is emitted.
- No paper-facing metric is promoted.
- Stage A annotation alone is not counted.
- Stage B transformation-aware validation is diagnostic only.
- Semantic guard atoms are not part of operation coverage numerator.
- No global leaderboard is produced.

No live API call, API key read, DB/checker/timing run, baseline rerun, new POCR diagnostic run, official Positive Operation Coverage Rate computation, route-level POCR aggregation, paper-facing metric promotion, top-level reports/results update, repository `output/` commit, case-package change, `skills.md` change, denominator change, case membership change, paper result change, raw legacy evidence change, route-alias policy, or leaderboard output occurred.

Next safe action: keep POCR as documented diagnostic support for release v0, or separately authorize a larger `src/dev` / `pocr/audit` refactor after release-critical paths are stable.
