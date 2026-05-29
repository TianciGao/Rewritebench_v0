# Report Artifact Contract

Human-readable reports live under `output/reports/<run_id>/`.

Expected files:

- `summary.md`: run summary, selected scope, adapter route, engine coverage, and headline local diagnostic counts.
- `failure_buckets.md`: explanation of failure bucket counts and representative rows.
- `tag_slices.md`: taxonomy/tag-slice explanation.
- `metrics_summary.md`: local metrics summary with `N.A.` and deferred fields made explicit.
- `verifier_summary.md`: Semantic Equivalence support summary; must state `N.A.` when formal verifier evidence is absent.
- `boundary.md`: local-only and non-official boundary statement.

Reports should be derived from `output/results/<run_id>/` machine-readable artifacts. They must not update top-level `reports/` or `results/` unless a separate official promotion/reporting task is authorized.
